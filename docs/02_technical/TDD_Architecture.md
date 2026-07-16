# TDD — Technical Design Document, Portfolio Dashboard v1

**Status:** DRAFT — awaiting Pop's approval
**Companion docs:** PRD (01_product) · DATA_SPEC (this folder) · DESIGN_SPEC (03_design) · TEST_PLAN (04_quality)

---

## 1. Architecture overview

```
┌─────────────────┐     read-only MCP      ┌──────────────────┐
│ Robinhood        │ ◄───────────────────── │ Claude (Cowork)  │
│ (5 accounts)     │                        │  · weekly job    │
└─────────────────┘                        │  · dashboard     │
                                            └───────┬──────────┘
                                                    │ writes/reads
                                     ┌──────────────▼──────────────┐
                                     │ Pop's Google Drive           │
                                     │ 05_Portfolio/history/        │
                                     │  · trades_ledger.csv         │
                                     │  · positions_snapshots.csv   │
                                     │  · accounts_history.csv      │
                                     └──────────────┬──────────────┘
                                                    │ read on open
                                     ┌──────────────▼──────────────┐
                                     │ Dashboard (Cowork artifact)  │
                                     │ live MCP calls + archive     │
                                     └─────────────────────────────┘
```

**Three components, deliberately decoupled:**
1. **Weekly archive job** (scheduled task, Fridays after close) — the system of record. Works even if the dashboard is never opened.
2. **Dashboard artifact** — a *view*: live MCP calls for "now", archive files for "history". Stateless; can be rebuilt anytime without data loss.
3. **Archive files** — plain CSV in Pop's Drive. Portable, human-readable, platform-independent. Stage 2's seed data.

## 2. Runtime & constraints

- **Platform:** Cowork artifact (self-contained HTML; `window.cowork.callMcpTool`)
- **Allowed CDN libs:** Chart.js 4.5.0 (charting), Grid.js 5.0.2 (tables) — exact pinned tags only
- **No backend, no database** in v1 — archive CSVs are the persistence layer
- **Light mode** design (per Cowork rendering)
- **MCP result parsing:** `r.structuredContent ?? JSON.parse(r.content[0].text)` → payload root is `{data: {...}}`

## 3. Data sources (authoritative tool inventory)

| Tool | Used for | Verified shape |
|---|---|---|
| `get_accounts` | account list, nicknames | ✅ this session |
| `get_portfolio` | per-account values, cash, buying power, crypto total | ✅ |
| `get_equity_positions` | stock qty + avg cost per account | ✅ |
| `get_equity_quotes` | live prices (≤20 symbols per call — batch) | ✅ |
| `get_option_positions` (`nonzero:true`) | open option legs: chain, side, qty, avg price, expiry, multiplier | ✅ |
| `get_option_instruments` (by ids) | strike, put/call, per leg | ✅ |
| `get_option_quotes` | live marks + greeks per leg | ✅ |
| `get_realized_pnl` (`asset_classes:["option"]`) | **golden aggregate** — realized totals & buckets | ✅ (requires explicit asset_classes; errors without) |
| `get_pnl_trade_history` | per-trade realized closes (no strikes) — paginate via `next_cursor` | ✅ |

Full field-level contracts: see DATA_SPEC.

## 4. Structure grouping algorithm

```
Input: open option legs (get_option_positions)
1. Enrich each leg with strike/type (get_option_instruments) and mark (get_option_quotes)
2. Group key = chain_id + expiration_date
3. Within group, sort legs by strike ascending
4. Detect strategy (§5); compute net premium, open P/L, max loss (§6)
Output: one structure object per group
```

Known limitation: two independent structures on the same chain+expiry merge into one "Custom" group. Acceptable for v1 (Pop trades one structure per expiry); revisit with order-id linkage in v1.1.

## 5. Strategy detection rules

| Pattern (after strike sort) | Label |
|---|---|
| 1 leg: long call / long put | Long Call / Long Put |
| 1 leg: short put / short call | CSP / CC (short call) |
| 2 put legs, equal qty, short@higher + long@lower | **PCS** (Put Credit Spread) |
| 2 put legs, short@lower + long@higher | Put Debit Spread |
| 2 call legs, mirrored | CCS / Call Debit Spread |
| 3 strikes K1<K2<K3, puts, mid short with qty = wings total | wings equal → **Butterfly**; wings unequal → **BWB** |
| anything else | Custom (N legs) — never mislabeled, never dropped |

### 5.1 Trade validation rules (F9 — ported from legacy ruleEngine.ts, smoke-tested 2026-07-16)

Deterministic checks against `STRATEGY_RULEBOOK.md` §2; each returns pass/violation with the measured value:
`DTE ∈ [R3]` · `|short delta| ∈ [R4]` · `width = R5` · `credit ∈ [R7]` · `credit/width ratio` · `distance from spot ∈ [R6]` · `position max-loss vs portfolio (R10)`.
Output: verdict (pass/fail) + itemized violations + checks-passed count. Rulebook open questions (§6) surface as violations until Pop rules on them. Validation input comes from screenshot extraction (native multimodal — no OCR service) plus live quote enrichment (delta from `get_option_quotes`, spot from `get_index_quotes`, VIX same call).

## 6. Money math (the part every competitor got wrong)

**Net premium:** Σ per leg — short legs: `+avg_price_abs × qty × multiplier/100`; long legs: negative. (`average_price` from connector is per-contract; multiplier from `trade_value_multiplier`, typically 100.)

**Open P/L:** short leg `(avg − mark) × qty × mult`; long leg `(mark − avg) × qty × mult`. Sum across legs. If any leg's mark is missing → structure P/L renders "n/a", never partial-sums.

**Max loss — payoff evaluation, NOT width shortcuts:**
```
candidates S = {0} ∪ {each strike} ∪ {2 × max strike}
P&L(S) = net_premium + Σ_legs sign(long=+1, short=−1) × qty × mult × intrinsic(S)
   intrinsic: put = max(K−S, 0) · call = max(S−K, 0)
max_loss = min over candidates (floor at expiry; exact for piecewise-linear payoffs)
```
Rationale: asymmetric BWB wings break width-based formulas. Payoff evaluation is strategy-agnostic and provably covers all vertices of the piecewise-linear payoff. **Note:** an earlier hand computation this project produced ($2,075 for the Jul 29 BWB) was wrong; the algorithm gives −$2,575. The Test Plan requires algorithmic verification for exactly this reason.

**Break-evens:** roots of P&L(S)=0 between candidate points (linear interpolation between vertices).

## 7. Options-vs-stock trade classification (closed trades)

Robinhood's per-trade history lacks an asset-class flag. Documented heuristic, validated to-the-cent against option-only aggregates in-session:
1. Symbol ∈ {SPX, SPXW, XSP, NDX, RUT, VIX} → option (index chains)
2. Else: integer qty ≤ 20 → option; qty > 20 or fractional → stock
3. Ambiguity displayed as a filter toggle, never hidden

Post-pipeline, classification becomes exact: closes are matched to remembered open legs (§8).

## 8. Stateful strike memory (fixes the "no strikes on closed trades" gap)

- Weekly snapshot records every open leg **with full contract identity** (option_id, strike, type, expiry)
- When a position later disappears from open + a realized trade appears → match on chain + qty + date window → closed trade inherits full contract detail
- Result: every trade opened after pipeline start carries strikes in the ledger; pre-pipeline history is backfilled from Pop's official Robinhood CSV (one-time import, already in hand)

## 9. Archive job design (scheduled, Fridays 21:30 UTC)

1. Pull: realized trades since last run · open positions (+instruments) · account portfolios
2. Append new realized trades to `trades_ledger.csv` (dedupe key: timestamp+symbol+qty+gain)
3. Append this week's rows to `positions_snapshots.csv` and `accounts_history.csv`
4. Rewrite files **cumulatively** — full history + new rows; never truncate (Pop's explicit requirement: prior weeks must never be deleted)
5. Write `_meta.json`: last run timestamp, row counts, anomalies
6. On any fetch failure: append nothing for that section, log to meta, surface in next dashboard open. Partial data is never silently written.

## 10. Dashboard load sequence

1. Parallel: accounts + portfolios + open option legs + realized aggregate
2. Dependent: instruments + quotes for open legs
3. Cursor loop: trade history (≤6 pages)
4. Read archive CSVs (if reachable) for trend sections
5. Render per-section as data lands; failed sections show error banner + last-archive fallback
6. localStorage: filter/range preferences only — never data

## 11. Error handling & degradation matrix

| Failure | Behavior |
|---|---|
| One MCP tool errors | Section banner; rest of dashboard unaffected |
| Quotes stale (`updated_at` old) | Values shown with "as of <time>" tag |
| Archive unreachable | Live sections work; trends show "history unavailable" |
| Robinhood auth expired | Full-page state: "Reconnect Robinhood in connector settings" |

## 12. Security

- Read-only: no order/write endpoints called, ever (project hard rule)
- No credentials in artifact, archive, or docs
- Archive contains Pop's trade data only — lives in Pop's own Drive

## 13. Stage 2 migration notes (context, not v1 scope)

The archive schema is the future product's ingestion format. Grouping/detection/max-loss logic (§4–6) ports to a backend as pure functions. Broker connectivity for external users: SnapTrade (documented in session as buy-not-build). TViz custom-dashboard pattern (audit B12) is the Stage 2 flagship differentiator.

---

**APPROVAL:** ☐ Approved by Pop · date: ________ · changes requested: ________
