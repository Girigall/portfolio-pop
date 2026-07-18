# PRD — Pop's Portfolio Dashboard (v1)

**Status:** DRAFT — awaiting Pop's approval
**Author:** Claude (Cowork) · **Owner:** Pop
**Date:** 2026-07-15
**Inputs:** OpenClaw UX audit (`audit/..._findings.md`), Robinhood connector data verified in session, platform failure evidence

---

## 1. Vision

A portfolio dashboard that shows **correct numbers** with **best-in-class presentation** — the Premium Insights look with math that ties to the broker to the cent, plus the one thing no platform on the market does: **multi-leg options structures (including broken-wing butterflies) displayed as single, honestly-priced positions.**

**The product is a standalone digital product — no dependency on any AI session to use it:**
- **The Dashboard (M8):** a web application at a real URL (GitHub Pages), open from any browser or device. Reads Pop's history data directly from his GitHub repository.
- **The Data Pipeline:** a weekly collector that appends Robinhood data to Pop's files and pushes to GitHub. The collector is a *replaceable courier*: v1 uses a Claude scheduled task (only because Robinhood's official agent API authenticates through it); M9 replaces it with a local script + cron on Pop's Mac — zero AI involvement.
- **The current in-app dashboard** is a temporary preview client only. It is NOT the product and is retired when M8 ships.
- **Stage 2 (separate PRD later):** commercial SaaS. Everything above is its prototype and seed dataset.

## 2. Problem & evidence

Pop tested the market with his real data (619-row Robinhood CSV, May 2025–Jul 2026):

| Platform | Failure | Evidence |
|---|---|---|
| Premium Insights | Ignores long legs of spreads → reported **+$188,540** P/L vs true **+$11,852** (16x overstatement) | Import screens, verified against Robinhood aggregates |
| TradesViz | Mispaired an assigned stock lot against a buy 10 months later → phantom **+$4,920** HIMS trade | Cross-checked against broker record (+$577.90 true) |
| Wingman | Handles structures but costs $588/yr | Pricing page |
| OptionIncome / Optioneer | Immature / too simple | Pop's evaluation |

**Root cause across the market:** CSV inference. Every platform guesses trade pairings from ambiguous broker logs. This product does not guess — it reads realized P&L and open-position contracts directly from the broker connection.

## 3. Users

- **v1:** Pop. Options income trader (SPX/SPXW put credit spreads + broken-wing butterflies, ~$1.5–2.5k/mo realized), long-term stock investor, 5 Robinhood accounts, margin user.
- **v2 (context only):** retail options sellers underserved by the platforms above.

## 4. Goals & success criteria

| # | Goal | Measure |
|---|---|---|
| G1 | Every displayed number ties to Robinhood ground truth | Realized totals match `get_realized_pnl` to the cent |
| G2 | Every open multi-leg structure displays as ONE row | Jul 29 SPXW BWB renders as one position with net credit, open P/L, max loss |
| G3 | History accumulates permanently, owned by Pop | Weekly archive files in Pop's Google Drive, cumulative, never overwritten destructively |
| G4 | At-a-glance clarity matching PI's density | ≥8 stat cards above the fold; one-scan comprehension |
| G5 | Zero recurring manual work | After setup, Pop does nothing weekly |

## 5. Non-goals (v1)

- ❌ Trade execution or any write action to Robinhood (hard ban, per project rules)
- ❌ Per-coin crypto detail (connector does not expose it; account-level crypto totals only)
- ❌ Tax reporting (archive supports future tax work; no tax UI in v1)
- ❌ Multi-user + auth (Stage 2 SaaS concerns) — single-user hosting IS in scope (M8, GitHub Pages)
- ❌ Full greeks panel (v1.1) — but net delta + theta per structure ARE in v1 (F4): zero extra data cost, and the F9 validator needs delta anyway

## 6. Features

### F1 — Header: accounts strip `[P0]`
All 5 accounts with masked numbers, nickname, total value; net worth aggregate; margin debit + buying power surfaced for the Stocks account. Data timestamp + refresh note.

### F2 — Stat-card row (the "PI row, fixed") `[P0]`
10 cards, modeled on audit A1, computed correctly:
1. Total options P/L (realized, from broker aggregate)
2. Win rate (per closed options trade)
3. Avg win · 4. Avg loss
5. Open premium (net credit of open structures)
6. **Open risk** (Σ max loss of open structures — payoff-function computed)
7. Open trades count
8. **Avg % return/risk** (realized P/L ÷ risk at entry) — Pop's preferred honest metric
9. Avg time in trade
10. This-month realized P/L vs monthly average
Layout/hierarchy: label small muted, value large bold, PI-style (audit Q7.1).

### F3 — Running P/L chart `[P0]`
Cumulative realized options P/L line + monthly bars toggle. Pill-style range switcher: 30d / 90d / 6M / YTD / ALL (audit Q3 winner). Default: YTD.

### F4 — Open positions table (structures) `[P0]`
One row per structure (not per leg). Columns per audit Q2 ideal-BWB-row: Opened · Underlying · Strategy badge (PCS/CCS/BWB/Fly/CSP/CC/Long) · Strikes · Expiry · Net premium · Open P/L · **Max loss** · **Net Δ / Θ** (per structure — P0 per HAL review #2; data already fetched per leg, display-only cost) · Break-even(s) · Status. Legs listed in a sub-line. Strategy auto-detected (TDD §5).

### F5 — Closed trades table `[P0]`
Pill filters (All / Options / Stocks · time ranges). Columns: Closed date · Underlying · Qty · Realized P/L (green/red). Source: broker per-trade realized history — never inferred.

### F6 — Stocks & accounts section `[P1]`
Stock positions across Stocks + IRA accounts: qty, avg cost, price, value, P/L $ and %, % of account. Concentration flag when one position > 25% of its sleeve.

### F7 — History spine (weekly archive) `[P0]`
Scheduled Friday-after-close job writes to Pop's Drive:
- `trades_ledger.csv` — cumulative realized trades (append-only)
- `positions_snapshots.csv` — weekly open-position snapshots **with full contract detail (strikes remembered while open)**
- `accounts_history.csv` — weekly account values
Dashboard reads the archive to render trends beyond live data (e.g., 12-month P/L once data exists). Files are human-readable, portable, and survive any platform change.

### F8 — States `[P0]`
Loading skeletons per section; partial-failure banners ("marks unavailable — showing last known"); explicit empty states. (Audit Q6: both incumbents are fragile here; we are API-live and cannot be.)

### F9 — Pre-trade validator + journal `[P1]` *(the Ajax Tracker idea, reborn)*
Pop pastes a screenshot of a candidate trade in chat → Claude extracts the setup natively (no OCR infrastructure — the lesson from options-dashboard's death) → validates against `STRATEGY_RULEBOOK.md` → returns verdict + itemized violations → on Pop's confirm, the candidate enters the journal (ledger `candidates` section) with thesis, VIX, and reasoning captured — closing the "data lost after every trade" loop from the Ajax PDR.
**Extraction verification (required — HAL review #3):** before any verdict, the extracted values (structure, strikes, credit, DTE, qty) are shown to Pop for confirmation — "are these numbers correct?" — with a correct/retake path. No verdict on unconfirmed numbers; multimodal extraction is non-deterministic and is treated as such.
**Framing rule (non-negotiable):** the validator checks Pop's own written rules. It never advises, authorizes, or executes. The decision and the click are Pop's, every time.
Origin: legacy rule engine, ported and smoke-tested against real trades (see PROJECT_LINEAGE).

### F10 — CSV Reader (M8 scope) `[P0]` *(Pop's architecture, 2026-07-18)*
An "Import CSV" feature in the M8 web app: Pop downloads Robinhood's activity CSV (~10 min weekly, accepted cost of independence), drops it into the reader → in-browser parse → normalize to master schema → dedupe → append to the master CSVs. Same engine as the proven backfill (`backfill_enrich.py`, 100% coverage). Missed weeks are harmless: next import catches up, dedupe prevents doubles.
**Data honesty rule:** CSV feeds all HISTORICAL sections fully. LIVE sections (open-structure marks, account values) are not in any broker CSV — they display "as of <last update>" with source labeled (courier when available, else last import). Never silently stale.

## 6b. Broker portability (the Tastytrade scenario)

The archive is deliberately broker-agnostic: generic fields (symbol/strike/expiry — no Robinhood IDs as keys), a `broker` column on every row, provenance recorded. If Pop switches brokers (Tastytrade under consideration): history in Drive is untouched, the new broker's connector (native API or SnapTrade) maps into the same ledger, the dashboard continues with a mixed-broker history. **Pop's data never lives inside any broker or platform.**

## 7. Data correctness requirements (the product's soul)

1. Realized totals come from Robinhood's own aggregation endpoints — never recomputed from CSV inference.
2. Structure max loss computed by payoff evaluation at expiry across all legs (TDD §6) — never by width-minus-credit shortcuts that break on asymmetric wings.
3. Any number that cannot be verified displays with an explicit "unverified" marker rather than silently rendering.
4. Options vs stock classification uses the documented heuristic (TDD §7) with its limits stated in-app.

## 8. Risks & mitigations

| Risk | Mitigation |
|---|---|
| Connector schema changes | All tool shapes documented in DATA_SPEC; graceful degradation + banner |
| Closed-trade strikes unavailable pre-pipeline | Archive captures strikes while positions are open; historical gap documented, backfilled from Pop's CSV where possible |
| Artifact declined/unavailable | All logic and archive live outside the artifact; dashboard is a view, not the system |
| Scope creep | v1.1 parking lot at end of this doc; nothing enters v1 without Pop's sign-off |
| **Data-courier dependency** (HAL #1, reframed per Pop 2026-07-18) | The weekly collector currently rides Claude's Robinhood connection. The PRODUCT (M8 web app + files + GitHub) has zero Claude dependency. Roadmap to full pipeline independence: M9 local collector script + cron. Until M9, a missed Friday only delays data — never loses it |

## 9. Release plan

1. Pop approves PRD + TDD + Design Spec + Test Plan
2. Build archive job first (history starts accumulating immediately)
3. Build dashboard clients (preview first, M8 web app as the product)
4. Acceptance run per Test Plan (golden numbers must reconcile)
5. Two-week bake: weekly job runs twice, counts verified to only grow

## 10. v1.1 parking lot

Full greeks panel (gamma/vega/rho — net Δ/Θ are already v1 in F4) · per-structure journal notes (PI journal pattern) · calendar heatmap (TViz B05, lower density) · Avg % capture card (audit Q7.2) · custom widget layout (TViz B12 — Stage 2 flagship)

---

**APPROVAL:** ☐ Approved by Pop · date: 16-7-2026 · changes requested: None