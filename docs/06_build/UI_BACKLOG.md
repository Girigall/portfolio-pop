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

## Design principles confirmed by Pop
- Dark mode matters (eye strain) — default dark, toggle to light
- No purple; palette = green profit / red loss / steel blue accent / neutral grays
- Each asset class deserves its own "page" — no mixed sections; label scope explicitly
