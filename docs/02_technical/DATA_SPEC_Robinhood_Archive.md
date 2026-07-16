# DATA SPEC — Robinhood Connector Contracts & Archive Schemas

**Status:** DRAFT — awaiting Pop's approval
**Purpose:** field-level contracts so the build never guesses. Every shape below was verified live in-session on Pop's accounts.

---

## 1. Accounts (fixed inputs)

| Account | Number (masked) | Type | Role |
|---|---|---|---|
| Stocks | ••••2005 | Individual, margin, options L3 | All options trading + stock book + margin debit |
| Cripto | ••••8817 | Individual, cash | Crypto (post-reorganization) |
| Roth IRA | ••••9521 | IRA | Commodity ETFs (COPX/PPLT/PICK) |
| Options | ••••3181 | Individual, cash | Empty (renaming plan pending) |
| Agentic | ••••8434 | Individual, cash | Empty |

Full account numbers are passed to tools unmasked; UI always masks to last 4.

## 2. Connector field contracts (consumed fields only)

### get_portfolio → `data`
`total_value` · `equity_value` · `options_value` · `crypto_value` · `cash` (negative = margin debit) · `buying_power.buying_power` — all decimal strings. **Crypto is account-total only; per-coin is NOT exposed.**

### get_equity_positions → `data.positions[]`
`symbol` · `quantity` · `average_buy_price` (may be absent — e.g., rights like EOSER) · `type` (flag when ≠ "long")

### get_equity_quotes → `data.results[]`
`quote.last_trade_price` vs `quote.last_non_reg_trade_price` — use the more recent timestamp; check freshness before calling it "current". `close.price` = official prior close (fallback: `quote.previous_close`). **Batch ≤20 symbols** or closes are dropped.

### get_option_positions (nonzero:true) → `data.positions[]`
`option_id` · `chain_id` · `chain_symbol` · `type` (long/short) · `quantity` · `average_price` (per-contract, signed: negative = credit received) · `expiration_date` · `trade_value_multiplier` · `opened_at` · `pending_*` (warn if non-zero)

### get_option_instruments (ids) → `data.instruments[]`
`id` · `strike_price` · `type` (call/put) · `expiration_date` · `state`/`tradability` (flag when not active/tradable) · `sellout_datetime`

### get_option_quotes → `data.results[]`
`quote.mark_price` (current) · `quote.updated_at` (freshness gate) · greeks (nullable — e.g., illiquid XOVR returns nulls) · `close.price` for 1D P/L

### get_realized_pnl → `data`
**Requires `asset_classes` explicitly** (`["option"]` etc.) — errors without it. `total_returns` = golden reconciliation number. `data_points[]` buckets: null gain + 0 trades = "no trades", render n/a not $0. Bucket width varies by span.

### get_pnl_trade_history → `data.trades[]`
`timestamp` · `symbol` (may be empty — e.g., crypto rows) · `quantity` · `price` (quirks: 0 for expirations; negative for buybacks) · `realized_gain`. **No strikes, no side, no asset class** → heuristics in TDD §7, permanent fix via TDD §8. Paginate with `next_cursor` until empty.

## 3. Known data gaps (displayed, never papered over)

| Gap | Impact | Handling |
|---|---|---|
| No per-coin crypto | Crypto = one number per account | Label "composition not available" |
| No strikes on closed trades | Pre-pipeline history is contract-blind | Strike memory (TDD §8) + one-time CSV backfill |
| No margin maintenance per symbol | Margin-call distance is an estimate | Show as range with assumptions labeled |
| Blank-symbol trades in history | Unclassifiable rows (e.g., −$4,971.68 crypto row, Jun 15) | Excluded from options stats; kept in ledger flagged `unclassified` |

## 4. Archive schemas (files in `05_Portfolio/history/`)

### 4.1 `trades_ledger.csv` (append-only, cumulative)
| Column | Type | Example | Notes |
|---|---|---|---|
| trade_id | string | `2026-07-10T18:55:54Z_SPXW_1_405` | dedupe key: timestamp+symbol+qty+gain |
| closed_at | ISO 8601 | `2026-07-10T18:55:54Z` | |
| account | string | `2005` | last-4 |
| symbol | string | `SPXW` | empty → `UNKNOWN` |
| asset_class | enum | `option` / `stock` / `unclassified` | heuristic v1; exact post-pipeline |
| quantity | decimal | `3` | |
| close_price | decimal | `-10` | raw from connector, quirks preserved |
| realized_gain | decimal | `405.00` | |
| strategy | string | `PCS` | filled when matched to remembered structure, else blank |
| strikes | string | `7270/7260` | same condition |
| expiry | ISO date | `2026-07-10` | same condition |
| source | enum | `connector` / `csv_backfill` | provenance always recorded |

### 4.2 `positions_snapshots.csv` (weekly append)
`snapshot_date · account · kind(stock/option_leg) · symbol/chain · option_id · side · qty · avg_price · strike · put_call · expiry · mark/last · multiplier`
One row per position per week. This is the strike-memory substrate.

### 4.3 `accounts_history.csv` (weekly append)
`snapshot_date · account · total_value · equity_value · options_value · crypto_value · cash · buying_power`

### 4.4 `_meta.json`
`last_run · rows_appended{ledger,snapshots,accounts} · failures[] · schema_version`

## 5. Format standards (all files & UI)

- Dates: ISO 8601 in files; `M/D/YYYY` in UI (per Design Spec)
- Currency: plain decimals in files (no `$`, no thousands separators); UI formats per Design Spec
- Encoding UTF-8, comma-delimited, header row, no quoted newlines
- **Append-only discipline:** rewrites always contain the full prior content + new rows; row counts must be monotonically non-decreasing (Test Plan gate)

## 6. Golden reconciliation numbers (frozen from session, for Test Plan)

| Metric | Value | Source |
|---|---|---|
| All-time realized options P/L (through 2026-07-10) | **+$11,852.24** | get_realized_pnl, options-only, span all |
| Per-underlying sum reconciliation | SPX/SPXW +9,375 · MSFT +1,605 · SMR +677 · OKLO +636 · FIG +456 · VIXM +325.44 · HIMS +146 · SOFI +56 · TE +5 · CRCL −375 · NU −192 · UVIX −862.20 | reconciled to the cent in-session |
| HIMS lifetime realized (options+stock) | +$577.90 | trade history; the number TradesViz corrupted to +$4,920 |
| YTD options realized (Jan 1–Jul 10, 2026) | +$9,286.24 | get_realized_pnl custom window |

---

**APPROVAL:** ☐ Approved by Pop · date: ________ · changes requested: ________
