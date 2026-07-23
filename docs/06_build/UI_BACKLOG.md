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

## Shipped 2026-07-22 — using the opened_at/delta/theta schema addition
- [x] "Avg time in trade" stat card (Portfolio → Options → Performance) — matches closed `trades_ledger.csv` rows to their earliest tracked `opened_at` across all historical `positions_snapshots.csv` weeks (by symbol+expiry+strike), averages days open. Shows "not enough tracked history yet" honestly (real state today — no row has `opened_at` populated before 2026-07-22). Logic verified correct against synthetic data (11.5-day match on a fabricated 2-leg PCS).
- [x] Real per-structure Net Δ / Net Θ columns (Portfolio → Options → Open Structures) — sign-adjusted sum of per-leg delta/theta × qty (short inverts sign). Shows "n/a" for the whole structure if any leg's greek is missing, matching the existing P/L never-partial-sum discipline (TDD §6). Replaces the earlier erroneous claim that this was already built (corrected in the Tortuga comparison doc). Currently "n/a" everywhere live — no snapshot has captured greeks yet.

## Still open — not a schema blocker anymore, a data-completeness blocker
- [ ] **Compliance chips (🟢/🟡/🔴 rulebook tolerance zones)** — investigated after the schema unblock. Full rulebook evaluation (STRATEGY_RULEBOOK.md S1–S4) needs VIX-at-entry and distance-from-spot-at-entry, neither of which are captured anywhere in the archive (`positions_snapshots.csv` has no VIX/spot field, and adding them would need a second schema round). DTE-at-entry and width/credit are now checkable via `opened_at`, but a chip built on a partial rule-check would visually claim "compliant" for dimensions never actually evaluated — that's worse than no chip, not better. Not building until either (a) Pop wants a narrower "DTE+width only" chip, explicitly labeled as partial, or (b) the F9 validator's `candidates_journal.csv` (which does capture VIX/spot at entry) becomes the actual data source for chips instead of `positions_snapshots.csv`.
- [ ] "Avg % return on risk" stat card (deferred since M3) — separate blocker, not resolved by this schema change (needs strike-memory pairing, per TDD §8).

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

## Shipped (M14) — filled in the tabs that felt thin vs Tortuga
Pop agreed with the audit's "feels incomplete" critique and asked to close the gap specifically on tabs with real Tortuga reference behavior — not a blanket "make everything look done" pass. Read the actual Tortuga audit findings for each tab before building, and skipped the ones with no real data source (ETFs, Dividends, Crypto per-coin) or no real reference to copy (Option Strategy → Lab, which Tortuga's own audit never got to see — gated/404).
- [x] Portfolio → Overview: period-selectable Portfolio Tracker chart, holdings heatmap (stocks/ETFs, P/L%-colored), Top Holdings summary table. No Time-Weighted Return — no deposit/withdrawal log exists to compute it honestly; substituted a plainly-labeled "value change" instead.
- [x] Trades → Journal: leg detail shown in the journal panel, new risk-plan/close-roll-plan fields (`structure_journal.csv` header addition — file was empty of data rows, zero migration risk), Tags + Thesis snippet added to the list view.
- [x] Trades → Strategies: reworked from journal-only (always empty until you journal something) to a real search over every closed trade, journal fields as optional overlay filters. Added Result (win/loss) and Period filters Tortuga has that we were missing; added P&L and Date columns to the result table.

## Shipped (M15) — Radar, dropped Lab/Calculator
Pop saw `C58_tortuga_sidebar_market_lab_radar.png` and said drop Lab, drop Calculator (was real/working, removed anyway per explicit instruction), Super Investors was never built (non-issue), but build Radar for real. Option Strategy collapsed to a flat top-level "Radar" tab (only one sub-item left, no reason to keep a sidebar expand group for it).
- [x] `history/radar_snapshot.csv` schema (DATA_SPEC §4.8) — header-only, courier-managed, ticker universe = Pop's own Robinhood watchlist(s), not a fixed list or a broad scan.
- [x] Radar UI: freshness label, symbol/trend/IV-rank filters, table, honest "waiting on first data pull" empty state.
- [x] Rulebook-fit matcher — VIX-tier regime band (S2-S4 share one table) applies to any ticker, not just SPX/SPXW (VIX describes the market, not the underlying) — **corrected 2026-07-23** after Pop flagged the original index-only gate was wrong ("I have to check stocks too"). Also added a per-ticker IV-rank read (elevated/low premium) for real differentiation beyond the shared VIX signal. Strike/width/delta selection still isn't attempted — genuinely needs option-chain data this scan doesn't have, for any ticker.
- [x] ~~Sync mechanism — "Queue sync" button~~ **removed same day (M16).** Pop tried the actual flow and correctly called it out: download a request file, replace it in Drive, come back later, ask Claude in words, wait, download a second file, replace it again — that's not a sync button, it's a manual relay race. Scrapped rather than kept as a fallback.
- [ ] **M16 replacement — a scheduled task, not a button.** Claude scheduled task (same mechanism as the Friday archive courier, shorter interval — proposed 30–60 min during market hours) pulls Pop's chosen watchlist automatically and commits `radar_snapshot.csv`; Pop just opens Radar and the data is there. New ticker outside the watchlist: ask Claude directly in a session, pulled same turn, no request file. Not created yet — needs the Robinhood connector reconnected (still disconnected as of 2026-07-23) and Pop's watchlist/interval confirmed first.
- [ ] Term structure, skew, VRP, bid-ask spread% — deliberately deferred, need option-chain data across multiple expiries and real quant validation before showing up on a screen meant to inform real trades.
- [ ] "Changes since yesterday" feed — needs ≥2 real pulls to diff against, trivial once the pipeline exists.

## Design principles confirmed by Pop
- Dark mode matters (eye strain) — default dark, toggle to light
- No purple; palette = green profit / red loss / steel blue accent / neutral grays
- Each asset class deserves its own "page" — no mixed sections; label scope explicitly
