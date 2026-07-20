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
- [ ] Formula tooltips on every stat card (DESIGN §7)
- [ ] Journal notes per structure (PI pattern)
- [ ] Custom layout / widget picker (TViz B12 — Stage 2 flagship)

## Tortuga Trades audit (2026-07-19)

Source: `audit/OpenClaw_Research_Brief_Trading_Dashboards_findings_Tortuga.md` + `audit/screenshots/Tortuga Trades/`. Full findings and steal/avoid lists live in that doc — this section just tracks what's shipped vs. deferred.

### Shipped (M10)
- [x] Trade entry with live validation preview (detected strategy, net credit, realized P/L, max loss, breakevens) before saving — Close Trade card in Reader tab

### Deferred — confirmed with Pop, not built yet
- [ ] Dashboard widget customization (Organize-panels style: movable/resizable 12-col grid, add/remove cards, save/reset layout) — Pop: skip for now
- [ ] Strategy journal (notes/thesis/tags per structure, not per leg) — needs a new `structure_journal.csv`, own milestone, never touches the 3 protected archive files
- [ ] New Trade / Roll Trade manual entry — no clean row shape in current schema (opens live in `positions_snapshots.csv`, broker-snapshot-only by design); would need a new "open positions" concept first
- [ ] Calendar Year and Week views (currently Month only)
- [ ] Calendar metric toggles: realized / unrealized / net premium / strategies opened vs. closed
- [ ] Portfolio Options sub-tabs: Expirations (positions-by-expiry with risk bar), Underlyings, Analysis
- [ ] Explicit noun consistency pass: label every count as Strategy / Leg / Position / Event everywhere (cheap now, Tortuga's own audit shows what happens if you don't)
- [ ] Table column organization + CSV export on Closed Trades tables (Tortuga's Trades table has both)

### Explicitly rejected (confirmed already correct or wrong to copy)
- Tortuga's collateral/risk math (raw strike notional, e.g. $1.26M "risk" on a 2-lot short put) — audit flags this as dangerously wrong. Pop's dashboard already does payoff-based max loss (TDD §6); nothing to change, just don't regress it.
- Leg-first Journal — Tortuga's own audit calls this its biggest flaw. Any future Journal build should be strategy-first from day one.

## Design principles confirmed by Pop
- Dark mode matters (eye strain) — default dark, toggle to light
- No purple; palette = green profit / red loss / steel blue accent / neutral grays
- Each asset class deserves its own "page" — no mixed sections; label scope explicitly
