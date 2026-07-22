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
| asset_class | enum | `option` / `stock` / `unclassified` | **open enum by design** — `crypto`, `futures`, `bond`, `event_contract` etc. add as values, never as schema migrations. The portfolio scales to any asset class organically (Pop's directive, 2026-07-16) |
| quantity | decimal | `3` | |
| close_price | decimal | `-10` | raw from connector, quirks preserved |
| realized_gain | decimal | `405.00` | |
| strategy | string | `PCS` | filled when matched to remembered structure, else blank |
| strikes | string | `7270/7260` | same condition |
| expiry | ISO date | `2026-07-10` | same condition |
| source | enum | `connector` / `csv_backfill` / `validator` / `reader` / `manual_entry` | provenance always recorded. `reader` = F10 CSV importer; `manual_entry` = M10 Close Trade form (both client-side, both open enum by design — see `asset_class` note above) |
| broker | enum | `robinhood` | portability: schema is broker-agnostic; new brokers (e.g., tastytrade) add rows, never migrations |
| thesis | string | `IV elevated, support held` | F9 journal capture; blank for auto-ingested rows |
| vix_at_entry | decimal | `15.57` | F9 capture (legacy schema field) |

### 4.2 `positions_snapshots.csv` (weekly append)
`snapshot_date · account · kind(stock/option_leg) · symbol/chain · option_id · side · qty · avg_price · strike · put_call · expiry · mark/last · multiplier · opened_at · delta · theta`
One row per position per week. This is the strike-memory substrate.

**`opened_at`/`delta`/`theta` added 2026-07-22** (Pop-approved schema diff, header-only edit — no historical row rewritten). Option-leg rows only; blank for stock rows. `opened_at` passes straight through from `get_option_positions` (already fetched, no new connector call). `delta`/`theta` come from `get_option_quotes` (nullable — illiquid legs write `""`, never estimated). Historical weeks before 2026-07-22 are blank for all three columns — additive-only, no backfill, nothing papered over. Unlocks (not yet built): compliance chips, avg-time-in-trade stat, real per-structure delta/theta display — all logged in `UI_BACKLOG.md`.

### 4.3 `accounts_history.csv` (weekly append)
`snapshot_date · account · total_value · equity_value · options_value · crypto_value · cash · buying_power`

### 4.4 `candidates_journal.csv` (F9 validator, append-only)
`created_at · underlying · strategy · rule · strikes · expiry · qty · net_credit · dte_entry · short_delta · vix · spot · verdict · flags · thesis · status · source` — pre-trade records; executed trades appear separately in the ledger via the archive job.

### 4.5 `_meta.json`
`last_run · rows_appended{ledger,snapshots,accounts} · failures[] · schema_version`

### 4.6 `manual_positions.csv` (M11, client-managed, additive only)
`entered_at · account · kind(stock/option_leg) · symbol · option_id · side · qty · avg_price · strike · put_call · expiry · mark · multiplier · source(always "manual")`

Same row shape as `positions_snapshots.csv` (4.2) plus `entered_at`/`source`, so both feed the same render logic. Purpose: track a structure or stock position opened at the broker before the next weekly snapshot catches up — never touches `positions_snapshots.csv` itself. Merge rule (client-side, in `index.html`): a manual row is dropped from the rendered view once a real snapshot row exists with the same `symbol+strike+expiry+side` (options) or `symbol+account` (stocks) — the broker snapshot "catching up" retires it automatically. Written via the app's Reader tab (New Option Structure / Add Stock Position forms), download-and-replace like every other write path — nothing auto-commits.

### 4.7 `structure_journal.csv` (M11, client-managed, upsert by key)
`structure_key · created_at · updated_at · thesis · tags · rating(1-5) · mindset · notes`

`structure_key` = `symbol|expiry`, matching the same grouping key the Open Structures table already uses (TDD §4 known limitation: two structures sharing symbol+expiry merge into one — journal entries inherit that same limitation). One row per structure, upserted (not appended) — editing an existing entry replaces its row rather than adding a new one, since a structure has one current journal state, not a history of edits. Written via the 📝 toggle on each Open Structures row.

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

**APPROVAL:** ☐ Approved by Pop · date: 16-7-2026 · changes requested: None
