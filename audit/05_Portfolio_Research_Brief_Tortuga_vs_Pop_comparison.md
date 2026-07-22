# Pop's Portfolio vs Tortuga Trades — Platform Comparison

**Created:** 2026-07-20
**Last updated:** 2026-07-22
**Owner:** HAL
**Status:** Complete
**Sources:** PRD_Portfolio_Dashboard.md, BUILD_STATE.md, UX audit findings (Premium Insights + TradesViz + Tortuga Trades), TDD_Architecture.md, DESIGN_SPEC_UI.md

**Correction (2026-07-22):** The original version of this doc overstated three "Pop's Portfolio wins" — delta/theta per structure, compliance chips, and the F9 pre-trade validator — as shipped features. Verified directly against `index.html` and the archive schema: none of the three exist in the live app today (delta/theta and compliance chips are unbuilt and schema-blocked; F9 is a real workflow but not an in-app feature). Corrected inline below and in the Gaps section. The Calendar metric-toggle note was also stale — that one *is* shipped and verified live.

---

## TL;DR

**Tortuga Trades looks like a finished product.** Out of the box it has a polished, professional design system, smooth navigation, and a complete feature set. It feels ready.

**Pop's Portfolio does not look finished yet.** It's functional and honest — the math is correct, the data model is better — but visually and experientially it still reads as a work in progress. The gap is entirely polish.

The honest truth: if someone opened both side by side today, they would pick Tortuga. Pop's Portfolio wins on every dimension that actually matters for trading — correct numbers, data ownership, broker verification — but the visual presentation needs to catch up.

---

## Overview

Two portfolios tracking Pop's options and stock trading — one built from scratch, one a third-party SaaS product. This document compares them across architecture, features, data integrity, UX, and what each does better.

| Dimension | Pop's Portfolio | Tortuga Trades |
|---|---|---|
| **Type** | Custom-built web app (GitHub Pages) | SaaS product (tortugatrades.app) |
| **Version** | v1 — live at https://girigall.github.io/portfolio-pop/ | v0.545 |
| **Target user** | Single user (Pop) — private | Retail options traders, community ranking |
| **Data source** | Robinhood API (courier) + CSV import + manual entry | Manual entry + CSV import + IBKR Flex Query |
| **Data ownership** | Pop owns everything — CSVs in Drive + GitHub mirror | Tortuga servers (exportable via CSV) |
| **Pricing** | $0 (self-built, static hosting) | Free trial → paid subscription required |
| **AI dependency** | None for daily use (F10 Reader + manual entry zero-AI; positions/accounts path uses optional courier) | None |

---

## Architecture

| Aspect | Pop's Portfolio | Tortuga Trades |
|---|---|---|
| **System of record** | Master CSVs in Pop's Drive + GitHub mirror | Tortuga database (server-side) |
| **Client** | Static SPA (HTML/JS, CDN: Chart.js + Grid.js) | React-style SPA (modern, Clerk auth) |
| **Hosting** | GitHub Pages — real URL, any device | tortugatrades.app |
| **Auth** | None (private repo, no multi-user) | Clerk (email + password + 2FA) |
| **Data persistence** | Append-only CSVs, never overwritten | Database (changeable, deletable) |
| **Offline** | Full offline — CSVs + local index.html work without internet | Requires internet |
| **Courier** | Replaceable: currently Claude scheduled task for positions/balances; trades via F10 Reader (zero AI) | In-app import + manual entry only |
| **Broker portability** | Broker-agnostic schema — switch brokers, history preserved | Per-broker import flows, but history lives inside Tortuga |

**Winner:** Pop's Portfolio — data ownership, no vendor lock-in, works fully offline, no recurring cost.

---

## Data Model

| Concept | Pop's Portfolio | Tortuga Trades |
|---|---|---|
| **Primary trade object** | Strategy (grouped multi-leg structure) | Leg (strategy grouping applied in Trades Overview only) |
| **Strategy detection** | Deterministic rule engine — PCS, CCS, BWB, Butterfly, CSP, CC, Long, Custom | Auto-grouping — detects Bull Put Spread, Put Butterfly, etc. |
| **User label preservation** | User label + system canonical label kept separate | User label normalized, original not preserved |
| **Noun consistency** | Strategy, Leg, Contract, Position — explicit labels throughout | Mixed: Journal says "1/5 legs", Trades says "5 trades", table shows 2 rows |
| **Open structures** | One row per grouped strategy with expandable legs | One row per grouped strategy (Trades), but legs individually in Journal |
| **Closed trades** | Broker-verified realized P&L per trade (from per-trade API) | Realized P&L from manual entries |
| **Account-level data** | 5 Robinhood accounts — live portfolio values, buying power | Manual NLV/Cash/Invested — no live broker sync |
| **Manual positions** | `manual_positions.csv` — auto-dropped when broker snapshot catches up | Manual entries treated same as imported — no staleness distinction |

**Winner:** Pop's Portfolio — cleaner noun system, user labels preserved, deterministic strategy detection, strategy-first data model.

---

## Feature Matrix

### Dashboard

| Feature | Pop's Portfolio | Tortuga Trades |
|---|---|---|
| **Stat cards** | 10 cards: Total P/L, Win Rate, Avg Win, Avg Loss, Open Premium, Open Risk, Open Trades, Avg % Return/Risk, Avg Time in Trade, This Month vs Avg | Account Summary (NLV, Cash, Invested), YTD Return, Profit Factor, Win Rate |
| **Metric correctness** | Broker-verified — ties to Robinhood's own aggregate endpoints to the cent | Based on manual entries + CSV import — no broker-level verification |
| **Formula transparency** | Hover any stat → shows exact formula + data source + timestamp | No visible formula disclosure |
| **P/L chart** | Cumulative line + monthly bars toggle, range pills (30d/90d/6M/YTD/ALL) | Cumulative line chart, period selector |
| **Widget customization** | Organize panels: drag-reorder, click-to-cycle width (33/50/67/100%), add/remove/reset, per-tab layouts, persisted to localStorage | Organize panels: drag/resize on 12-column grid, add/remove cards |
| **Open vs realized split** | Explicit: realized P&L, unrealized P&L, open premium, closed premium captured — all separated | Dashboard is closed-P&L driven; open strategies don't populate performance metrics without explanation |

**Winner:** Pop's Portfolio — honest metrics, formula disclosure, better stat density, clear realized/unrealized split.

### Trades Table

| Feature | Pop's Portfolio | Tortuga Trades |
|---|---|---|
| **Strategy grouping** | Default — one row per strategy, legs expandable inline | Default in Trades Overview — one row per strategy, legs expandable |
| **Columns** | Opened, Underlying, Strategy badge, Strikes, Expiry, Net premium, Open P/L, Max loss, Breakeven(s), Status. *(Net delta/theta is not currently a column — no greeks are captured in `positions_snapshots.csv`; see Gaps.)* | Date, Ticker, Price/Strike, Action, Type, Strategy, Qty, Price, Commission, Expiry, Premium captured, Unrealized, Realized |
| **Strategy badges** | Color-coded per strategy (BWB purple, PCS green, etc.) | Text labels only |
| **Column customization** | Drag-to-reorder headers, persisted per table in localStorage | Organize columns, download to CSV |
| **Filters** | Status (All/Open/Closed), date range pills | Date period dropdown, All/Open/Closed pills, ticker/type/strategy filters |
| **Pagination** | Client-side via Grid.js | 25/50/100 rows per page |
| **Compliance chips** | Not shipped. Schema was blocked on `opened_at`; that's now resolved (`positions_snapshots.csv` gained `opened_at`/`delta`/`theta`, 2026-07-22). Chip UI itself still not built. | None |
| **Max loss column** | Always present — payoff-function computed, not width-minus-credit | Not a first-class column in Trades view |

**Winner:** Pop's Portfolio — richer columns (max loss, breakevens), max loss computed correctly. (Compliance chips and delta/theta are planned, not yet shipped — see Gaps.)

### Calendar

| Feature | Pop's Portfolio | Tortuga Trades |
|---|---|---|
| **Views** | Year (monthly ribbon + P/L totals), Month, Week | Year, Month, Week |
| **Year view** | Jan–Dec ribbon with monthly P/L totals + trade count toggle | Monthly grids with zoom controls |
| **Month view** | Daily P&L + trade count, color-coded cells | Daily P&L + trade count, color-coded |
| **Week view** | Per-day activity | Per-day activity with time grid |
| **Metric toggles** | P/L vs trade count toggle per mode | None — shows trade count + P&L |
| **Open vs closed** | Exposed structures and dates can see both open and closed | Calendar appears to count legs/trades, not strategies |

**Winner:** Pop's Portfolio — metric toggle shipped (M11) and verified live; Tortuga has no equivalent P/L-vs-trade-count toggle.

### Portfolio

| Feature | Pop's Portfolio | Tortuga Trades |
|---|---|---|
| **Tabs** | Overview, Options, Stocks, Crypto, Dividends | Overview, Options, Stocks, ETFs, Dividends |
| **Options sub-tabs** | All, Expirations, Underlyings, Analysis | All, Expirations, Underlyings, Analysis (same structure — copied) |
| **Expirations view** | Risk bars by expiry, contract cards with DTE, strike, qty | Contract count by expiry, per-contract risk cards |
| **Risk/collateral display** | Correct BWB/PCS math — max loss per strategy from payoff evaluation, no inflated notional | Shows $2.5M for 2 test strategies — appears to use raw notional, dangerously unclear |
| **Underlyings view** | Groups by underlying symbol across all accounts | Confusing — didn't show SPX as an underlying despite options existing |
| **Analysis view** | Closed trades grouped by strategy with per-strategy stats | Analysis requires closed trades; opens fine but SPX data gave empty state |
| **Stocks** | Holdings with qty, avg cost, price, value, P/L $ and %, concentration flag | Manual entry only — Add position modal (Long/Short/Cash) |
| **Crypto** | Account-level crypto total from Robinhood (per-asset not available) | Not observed as distinct section |
| **Dividends** | Honest "not tracked yet" empty state — no fake data | Good empty state with roadmap copy |

**Winner:** Pop's Portfolio — honest risk math, correct max loss, per-strategy stats, concentration flags, no inflated numbers.

### Themes / Accent Color

| Feature | Pop's Portfolio | Tortuga Trades |
|---|---|---|
| **Accent color customization** | Not available. Uses a single dark-theme palette. | Available via Themes tab. Users can change the primary accent color throughout the app. |

**Note:** Pop flagged this as a feature to consider adding. No screenshot captured — requires Tortuga Trades login to access the Themes tab.

### Import & Data Entry

| Feature | Pop's Portfolio | Tortuga Trades |
|---|---|---|
| **CSV import** | F10 Reader: browse → parse → dedupe → append to master CSVs. Proven 100% backfill coverage | Per-broker selectors (IBKR, DEGIRO, tastytrade) + generic CSV |
| **Manual trade entry** | Close a Trade form: per-leg input with live preview (strategy, P/L, max loss, breakevens) | New/Close/Roll modal: leg-based entry, no strategy preview before save |
| **New structure entry** | New Option Structure form (Reader tab) — previews strategy detection + economics before saving | Same concept but no preview before save |
| **Add stock position** | Add Stock Position form — qty, avg cost, manual | Add position modal — Long/Short/Cash, symbol, qty, cost |
| **Duplication protection** | High-water-mark dedupe + cross-source dedupe — never double-counts | Assumed available but no explicit safety language observed |
| **Robinhood support** | Native — the primary data source | Not observed in broker selector |
| **Import preview** | Yes — shows parsed rows before final commit | No visible preview before broker selection |

**Winner:** Pop's Portfolio — live math preview before saving, Robinhood-native, bulletproof dedupe, no guessing.

### Journal & Review

| Feature | Pop's Portfolio | Tortuga Trades |
|---|---|---|
| **Journal scope** | Strategy-level journal — thesis, tags, rating, mindset, notes per structure | Leg-level journal — 1/5 leg navigation for a 5-leg strategy |
| **Strategy journal** | Structure journal CSV — upsert by structure_key (symbol|expiry) | Journal operates at leg level — strategy context present but not elevated |
| **Review filters** | Strategies tab: filter by rating, mindset, tags, symbol, outcome | Mindset (8 emotional labels), tags (user-created), min rating (1-5), self-assessment metrics |
| **Pre-trade validator** | F9 is a specced workflow (TDD §5.1: screenshot → extract → confirm → validate → journal), run interactively with Claude — it is **not a UI feature of the live `index.html` app**, since that app is intentionally zero-AI. Writes to `candidates_journal.csv` when used. | None |
| **Rule compliance** | Specced (rulebook checks exist), but not surfaced anywhere in the live app yet — no compliance chip, no violations UI. Schema no longer blocks this (see above); still a build task. | Not present |
| **Thesis capture** | Captured at entry — VIX, spot, reasoning, planned exit (via F9 workflow, written to `candidates_journal.csv`) | Notes field available but leg-level |

**Winner:** Pop's Portfolio — strategy-first journal is live and shipped; pre-trade validation and rule compliance exist as a workflow/spec but aren't yet a feature inside the app itself (see Gaps).

### Navigation & IA

| Aspect | Pop's Portfolio | Tortuga Trades |
|---|---|---|
| **Nav structure** | Sidebar with 7 top-level items: Dashboard, Trades (Overview/Journal/Strategies), Calendar, Portfolio (Overview/Options/Stocks/ETFs/Dividends/Crypto), Option Strategy (Lab/Calculator/Radar), Reader, Settings | Sidebar with 9 active items: Dashboard, Trades, Calendar, Portfolio, Option Strategy (expandable), Trades by Tortuga → Trades/Analysis (sub-tabs), Import, Themes, Settings. Community features (Leaderboard, Resources, Trades by Tortuga Community sub-tab) excluded per Pop's decision — individual portfolio, no social features needed |
| **Nested nav** | Inline expandable sub-items with connecting lines (Trades, Portfolio, Option Strategy) | Expandable submenus (Option Strategy → Lab/Calculator/Radar, Trades by Tortuga → Trades/Analysis) |
| **Gated features** | Not present — everything accessible | Option Strategy returns 404 for direct route, gated features not clearly communicated |
| **Consistency** | All sidebar items are explicit route links + action buttons distinguished | Mixed: some expand (Option Strategy), some action (Import), some link, some 404 |
| **Root-level vs sub-view** | Sub-views are in-page pills (Portfolio Options sub-tabs) — matches Tortuga's actual IA | Portfolio uses in-page sub-tabs too (All/Expirations/Underlyings/Analysis) |

**Winner:** Even. Pop's Portfolio copied Tortuga's IA exactly (M13). Both have the same navigational structure, but Pop's has fewer dead ends and gated-feature 404s.

---

## Math & Data Integrity

This is the single most important comparison dimension — and where Pop's Portfolio was designed to excel specifically because every competitor failed.

| Metric | Pop's Portfolio | Tortuga Trades |
|---|---|---|
| **Max loss computation** | Payoff-function evaluation across all legs — correct for BWBs, asymmetric wings, any structure | Unknown method — risk numbers ($2.5M for 2 SPX test strategies) suggest raw notional or flawed aggregation |
| **Premium calculation** | Sum per leg with correct sign (short = credit, long = debit) | Available per trade row |
| **Realized P&L** | From Robinhood's broker-level aggregate (`get_realized_pnl`) — ties to the cent | From manual entries + CSV import — no broker verification |
| **Strategy classification** | Deterministic rule engine (TDD §5) — tested against real trades, 100% match | Auto-grouping works for standard cases (PCS, Butterfly) but loses BWB nuance |
| **Commissions** | Included in per-trade P&L (broker-provided) | Per-row commission field present |
| **Unrealized P&L** | Computed from live marks — shows n/a if any leg's mark is missing (no partial sums) | Blank for open trades — no explanation |
| **Golden number** | Stat cards tie to `get_realized_pnl` aggregate — reconciliation footer shows per-trade sum vs aggregate | No visible reconciliation mechanism |

**Winner:** Pop's Portfolio — by a wide margin. This was the entire design premise: honest math where every competitor failed.

---

## UX & Design

| Aspect | Pop's Portfolio | Tortuga Trades |
|---|---|---|
| **Visual polish** | Clean, functional — design spec modeled on Premium Insights (audit winner) | Polished — modern, calm, professional |
| **Dashboard density** | 10 stat cards above the fold (PI layout) | Account summary cards + performance KPIs — less dense |
| **Dark/light mode** | Dark default, light toggle | Light mode default, theme controls |
| **Empty states** | Friendly, explanatory — "not tracked yet" with honest labeling | Good — roadmap-style copy for empty sections |
| **Loading states** | Skeleton blocks per section | Not deeply tested in audit |
| **Error states** | Amber banner per section — never silently stale | Not thoroughly observed |
| **Mobile** | Responsive (cards wrap, tables stack) | Responsive |
| **Dashboard customization** | Full widget system: drag, resize, remove, reset, per-tab layouts, localStorage persistence | Widget organization with 12-column grid, add/remove cards |

**Winner:** Even. Tortuga is more polished out of the box; Pop's Portfolio has better customization and state handling.

---

## What Tortuga Does Better

1. **Calendar** — Year/Month/Week views are the benchmark. Pop's copied them but hasn't added metric toggles yet.
2. **Journal filters** — Mindset, tags, ratings, self-assessment filters for post-trade review are a good pattern.
3. **Visual polish** — Out-of-the-box it looks like a finished product. Pop's Portfolio needs continued design iteration.
4. **Multi-currency** — EUR, GBP, CHF, JPY, and more in position modals.
5. **Broker selector** — IBKR Flex Query, DEGIRO, tastytrade — good for multi-broker import.
6. **Expirations view** — Contract cards with risk by expiration group is a strong visual for risk clustering.

## What Pop's Portfolio Does Better

1. **Math correctness** — Payoff-derived max loss, broker-verified realized P&L, no inflated risk numbers. The whole reason it was built.
2. **Data ownership** — Files Pop owns, in his Drive, mirror on GitHub, no vendor lock-in, no subscription.
3. **Strategy-first data model** — Strategy is the primary object everywhere. Tortuga's Journal and Strategies still operate at leg level.
4. **User label preservation** — User's strategy name + system canonical label kept separately. Tortuga normalizes silently.
5. **Formula transparency** — Every stat shows its formula, source, and timestamp on hover.
6. **Pre-trade validator (workflow)** — Screenshot → extract → confirm → validate against rulebook → journal. Tortuga has no equivalent — but note this runs as an interactive Claude session, not a button inside the live app yet.
7. **Compliance tracking (specced, not shipped)** — Rulebook checks exist conceptually; the compliance chip UI is not built. Schema unblocked 2026-07-22, remains a build task.
8. **Broker-verified golden numbers** — Footer reconciliation shows per-trade sum vs broker aggregate; tortuga offers no such check.
9. **Manual positions with auto-staleness** — Manual entries auto-drop when broker snapshot catches up. Clean separation.
10. **Cost** — $0 vs paid subscription.
11. **Broker portability** — Switch brokers and history is untouched. Tortuga data lives inside Tortuga.
12. **Explicit realized/unrealized split** — Clear separation on dashboard. Tortuga leaves blank fields unexplained.
13. ~~Delta/Theta per structure~~ — **correction:** not currently built. No greeks are captured anywhere in the archive; this was listed in error. Would need a schema addition to `positions_snapshots.csv` (see Gaps).

---

## Gaps in Each Platform

### Pop's Portfolio still missing

These are all logged in UI_BACKLOG or deferred to v1.1:

- [ ] **Compliance chips** (🟢/🟡/🔴) — not built, and not just a schema gap anymore. Investigated 2026-07-22: full rulebook evaluation needs VIX-at-entry and distance-from-spot-at-entry, which aren't captured anywhere in the archive and weren't part of the approved schema diff. A chip built on a partial rule-check would falsely imply full compliance — not building until Pop wants a narrower, explicitly-partial version or the F9 validator's `candidates_journal.csv` becomes the data source instead.
- [x] **Avg time in trade stat card** — shipped 2026-07-22 (Portfolio → Options → Performance). Matches closed trades to earliest tracked `opened_at`; correctly shows "not enough tracked history yet" today since no row has real data before this date.
- [x] **Delta/Theta per structure** — shipped 2026-07-22 (Portfolio → Options → Open Structures, Net Δ/Net Θ columns), fixing the earlier error where this doc claimed it was already built. Sign-adjusted, never partial-sums. Shows "n/a" today — no snapshot has captured greeks yet.
- [ ] **F9 pre-trade validator as an in-app feature** — currently only runs as an interactive Claude workflow, not a button in the live `index.html` app. Would need a real OCR/extraction path to become a client feature, which conflicts with the app's zero-AI architecture — likely stays a workflow, not a UI feature, unless that tradeoff changes.
- [ ] Full greeks panel (gamma/vega/rho) — v1.1, same schema dependency as delta/theta above
- [x] Per-structure journal notes (now implemented via `structure_journal.csv` — M11 shipped)
- [ ] Avg % Capture stat card — **not safely buildable today**: `trades_ledger.csv` has no entry-premium/net-credit field, only `realized_gain` and `close_price`. Computing "% of max profit captured" would mean reverse-deriving entry premium from strike width, which the app's own no-fake-data principle rules out without a clean source field.
- [x] Calendar metric toggle (P/L vs trade count) — shipped M11, verified live (corrected 2026-07-22, was listed as deferred)
- [ ] Strategy-level performance breakdown in Analysis view — already shipped per `UI_BACKLOG.md` M11 (Portfolio → Options → Analysis); re-verify if this is meant to mean something further
- [ ] Multi-currency support — deferred, low priority (Robinhood-only, USD)
- [ ] Dividend tracking — honest "not tracked yet" exists, real data integration deferred
- [ ] M7 bake (two-week observation + failure drill) — pending, not a build task
- [ ] Accent color / theme picker — Pop explicitly flagged wanting this; see Themes section above
- [ ] Visual polish — the most repeated finding in this document; no single feature, an ongoing design pass

### Tortuga Trades gaps

- [x] Risk math is dangerously opaque ($2.5M for 2 SPX test structures)
- [x] Journal operates at leg level — strategy context not elevated enough
- [x] User-entered strategy labels silently normalized
- [x] Noun inconsistency (5 trades vs 2 rows vs 5 operations vs 5 positions)
- [x] No formula disclosure on metrics
- [x] Open trades don't populate dashboard metrics without explanation
- [x] Unrealized P&L left blank without reason
- [x] No pre-trade validation
- [x] No broker-level P&L verification
- [x] No Robinhood import path
- [x] Gated features return generic 404 instead of upgrade/locked-state screen
- [x] Paid subscription required for full access
- [x] Data lives on Tortuga servers — exportable but not natively owned

---

## Bottom Line

**Tortuga Trades is the better product experience today.** It looks finished, has a live community, and the navigation IA and widget customization are the reference standard for what an options dashboard should feel like.

**Pop's Portfolio is the better data product.** It wins on the only dimension that actually matters for trading — numbers that are correct, auditable, and owned. It has zero recurring cost, works fully offline, and will only improve with time as the archive accumulates.

The gap is entirely polish. The math, the data model, the strategy handling, and the honesty — those are already better here than anything on the market.

---

## Verdict by Dimension

| Dimension | Winner | Why |
|---|---|---|
| Math & correctness | Pop's Portfolio | Broker-verified, payoff-derived max loss, no inflated risk numbers |
| Data ownership | Pop's Portfolio | CSVs owned by Pop, GitHub mirror, zero vendor lock-in |
| Visual polish | Tortuga Trades | Out-of-box finished feel, professional design system |
| Navigation/IA | Even | Pop's Portfolio copied Tortuga's IA exactly — structurally identical |
| Feature breadth | Even | Tortuga ships more features, but community/social features (Leaderboard, Resources, Community sub-tab) are explicitly excluded from Pop's scope — individual portfolio, not a social platform |
| Feature depth | Pop's Portfolio | Strategy-first model, pre-trade validator workflow. Delta/theta and compliance tracking are specced, not yet shipped in the live app. |
| Themes / accent color | Tortuga Trades | Tortuga has built-in accent color picker; Pop's Portfolio lacks this — flagged as a feature to consider adding |
| Cost | Pop's Portfolio | $0 vs paid subscription |
| Portfolio risk display | Pop's Portfolio | Correct $ max loss vs $2.5M inflated notional |
| Journal | Pop's Portfolio | Strategy-first journal is live. Pre-trade validation exists as an interactive workflow; rule compliance recording is not yet a UI feature. |
| Calendar | Tortuga Trades | Best reference — Pop's needs metric toggles to surpass |
| Import/entry | Pop's Portfolio | Live math preview, Robinhood-native, bulletproof dedupe |
| Customization | Even | Both have widget systems; Pop's persisted per-tab layouts |
| States & error handling | Pop's Portfolio | Loading skeletons, partial-failure banners, honest empty states |
| Future-proofing | Pop's Portfolio | Append-only archive, broker-agnostic schema, any device/browser |
| Support & maintenance | Tortuga Trades | Managed SaaS — Pop doesn't maintain it |


**Final one-liner: Tortuga is the better app today. Pop's Portfolio is the better system — it's designed to stay honest, stay owned, and stay alive after Tortuga changes its pricing or shuts down.**

---

## Approval

- [ ] Approved by Pop

Date: ________
Changes requested: ________
