# UI BACKLOG — Pop's dashboard feedback (crystallized)

Source: Pop's M3 review, 2026-07-18. Every item mapped to a milestone. This file is the single place UI ideas live — add here, never lose them.

## Shipped in M3.1 (same day)
- [x] Dark mode toggle (persisted; Pop's eyes tire in light mode — dark is his default preference)
- [x] Purple accent removed → steel blue (#1d6fc4)
- [x] Tab shell: Overview · Options · Stocks · Crypto — "work by parts", each asset class its own page
- [x] Weekly granularity on P/L chart (Week/Month toggle) alongside range pills
- [x] Explicit scope labels on every section (which account, which asset class)

## M4 (structures table — Options tab)
- [ ] Open structures as single rows: strategy badges, strikes, net premium, open P/L, max loss, net Δ/Θ
- [ ] Compliance chips (🟢/🟡/🔴) per rulebook tolerance zones + tooltip
- [ ] Legs sub-line; expand for per-leg detail
- [ ] Deferred honest cards: avg time in trade, avg % return/risk (need strike-memory pairing)

## M5 (full surface)
- [ ] Stocks tab: positions per account, P/L, % of sleeve, concentration flags
- [ ] Closed trades table with pill filters (Options/Stocks · time ranges)
- [ ] **P/L calendar view** (Pop's explicit like — monthly grid, daily P/L, clean density)
- [ ] Crypto tab: account totals + note on per-coin limitation; per-coin if connector ever exposes it
- [ ] Overview tab: net-worth trend from accounts_history.csv once ≥4 weeks archived

## Later / v1.1+
- [x] Formula tooltips on every stat card (DESIGN §7) — shipped 2026-07-20, all 20 dashboard stat cards (Overview/Options/Stocks/Crypto), hover shows formula + data source + "as of" timestamp
- [x] Journal notes per structure (PI pattern) — shipped as part of M11's `structure_journal.csv`
- [x] Custom layout / widget picker (TViz B12 — Stage 2 flagship) — shipped as part of M11's Overview widget system (DESIGN_SPEC §7 originally reserved this for Stage 2; superseded by the Tortuga audit + Pop's direct request)

## Still open — needs a protected-file schema decision, not a build task
- [ ] Compliance chips (🟢/🟡/🔴 rulebook tolerance zones) — blocked on `opened_at` per position, which the Robinhood connector returns but `positions_snapshots.csv` never captures. Adding it means a schema change to a protected archive file — needs the exact-diff approval per the hard rule before any code changes, not something to build unprompted.
- [ ] "Avg time in trade" / "avg % return on risk" stat cards (deferred since M3) — same `opened_at` blocker as compliance chips.

## Shipped (M12) — structural/visual match, not just features
- [x] Sidebar nested expand for Options (All/Expirations/Underlyings/Analysis as indented sub-items, connecting line) — replaces the in-page pill row
- [x] Win Rate + Profit Factor (new stat) as Chart.js doughnut gauges instead of plain numbers
- [x] Denser default widget grid (Overview/Options/Stocks now default to side-by-side panels, not full-width stacked)
- [x] Persistent year ribbon (Jan–Dec totals) above the calendar in every mode

## Tortuga Trades audit (2026-07-19)

Source: `audit/OpenClaw_Research_Brief_Trading_Dashboards_findings_Tortuga.md` + `audit/screenshots/Tortuga Trades/`. Full findings and steal/avoid lists live in that doc — this section just tracks what's shipped vs. deferred.

### Shipped (M10)
- [x] Trade entry with live validation preview (detected strategy, net credit, realized P/L, max loss, breakevens) before saving — Close Trade card in Reader tab

### Shipped (M11) — the rest of the backlog, all in one pass
- [x] Calendar Year and Week views (was Month only) + P/L-vs-trade-count metric toggle
- [x] Portfolio Options sub-tabs: Expirations (positions-by-expiry with risk bar), Underlyings, Analysis (strategy-level win rate/avg P/L)
- [x] CSV export on Closed Trades tables (Options + Stocks)
- [x] Explicit noun consistency pass (Strategy/Leg/Position/Trade labeled consistently — e.g. Options subtitle now says "open structures" not "open positions")
- [x] Dashboard widget customization — Organize panels edit mode, drag-reorder, click-to-cycle width (33/50/67/100%), add/remove/reset, layout in `localStorage`. Shipped Overview-only 2026-07-20, then extended to **all 5 tabs** same day at Pop's request — engine generalized to be parameterized per-tab (`wState[tab]`, `p_wlayout_<tab>` keys) instead of hardcoded to Overview.
- [x] Strategy journal — new `structure_journal.csv` (DATA_SPEC §4.7), 📝 panel per structure: thesis/tags/rating/mindset/notes, upsert by `structure_key`
- [x] New Trade (open) + Add Stock Position manual entry — new `manual_positions.csv` (DATA_SPEC §4.6), merged into Open Structures/Holdings tagged "manual," auto-drops once the real broker snapshot catches up. "Roll" is deliberately not a separate mechanism — it's Close (M10) + New (M11) in sequence.
- [x] Table column drag-to-reorder on Closed Trades tables (Options + Stocks), order persisted per table in `localStorage`

Tortuga audit fully addressed — every item from the steal-list is shipped or explicitly rejected (see below).

### Explicitly rejected (confirmed already correct or wrong to copy)
- Tortuga's collateral/risk math (raw strike notional, e.g. $1.26M "risk" on a 2-lot short put) — audit flags this as dangerously wrong. Pop's dashboard already does payoff-based max loss (TDD §6); nothing to change, just don't regress it.
- Leg-first Journal — Tortuga's own audit calls this its biggest flaw. Any future Journal build should be strategy-first from day one.

## Shipped (M13) — full nav structure, not just visual treatment
- [x] Full 7-item top-level nav copied from Tortuga: Dashboard, Trades, Calendar, Portfolio, Option Strategy, Reader, Settings (Leaderboard and MTO Opciones excluded per Pop's explicit instruction)
- [x] Trades tab (Overview/Journal/Strategies) — historical activity split out from current holdings
- [x] Calendar promoted to standalone top-level (was nested under Options)
- [x] Portfolio tab (Overview/Options/Stocks/ETFs/Dividends/Crypto) — consolidates the old Options/Stocks/Crypto tabs under one current-holdings umbrella
- [x] Option Strategy tab — Calculator built for real (reuses `economics()`, no save/no file write); Lab and Radar are honest placeholders
- [x] Settings tab — app info + data file links
- [x] "Trades by Tortuga" nav item evaluated and explicitly dropped — curated company/community content, no equivalent in a single-user product, audit's own "skip for MVP" recommendation
- [x] M12's Options sub-tab sidebar-nesting reverted to in-page pills (self-corrected — Tortuga only nests 2 levels deep in its sidebar)

## Design principles confirmed by Pop
- Dark mode matters (eye strain) — default dark, toggle to light
- No purple; palette = green profit / red loss / steel blue accent / neutral grays
- Each asset class deserves its own "page" — no mixed sections; label scope explicitly
