# Dashboard UX Audit Findings — Trading Platforms

**Audit date:** 2026-07-15  
**Auditor:** NOVA (OpenClaw)  
**Task ref:** Research Brief — Trading Dashboard UX Audit  
**Structure note:** All deliverables inside `05_Portfolio/audit/`. Screenshots in `screenshots/` subfolder. Filenames use platform prefix (`A0X_` = Premium Insights, `B0X_` = TradesViz).

---

## A. Premium Insights (premiuminsights.ai)

### A1. Component inventory — Main dashboard

| # | Component | Screenshot | What it shows | Period/filter | Formula (if known) | Verdict |
|---|---|---|---|---|---|---|
| 1 | **Total P/L** stat card | A01 | `$12,579.26` — portfolio-level profit/loss | All-time (implied) | Sum of all closed trade P&L | **steal** — clean hero number |
| 2 | **Win Rate** stat card | A01 | `93.3%` — percentage of profitable closed trades | All-time (implied) | (Winning trades / Total closed trades) × 100 | **steal** — essential at-a-glance |
| 3 | **Avg Win** stat card | A01 | `$483.23` — average P&L of winning trades | All-time (implied) | Σ(winning P&L) / winning trade count | **steal** |
| 4 | **Avg Loss** stat card | A01 | `$475.59` — average P&L of losing trades | All-time (implied) | Σ(losing P&L) / losing trade count | **steal** |
| 5 | **Open Premium** stat card | A01 | `$13,198.93` — total premium collected on open positions | Current snapshot | Σ(credit received for open short options) | **steal** — key income metric |
| 6 | **Open Risk** stat card | A01 | `$10,188.13` — capital at risk on open positions | Current snapshot | Σ(max loss of open positions) | **steal** — Pop's preferred honest metric |
| 7 | **Open Trades** stat card | A01 | `4` — number of currently open positions | Current snapshot | Count of trades with status = Open | **steal** |
| 8 | **Avg % Capture** stat card | A01 | `64.8%` — average percentage of max premium captured on closed trades | All-time (implied) | Σ(realized P&L / max potential P&L per trade) / trade count | **steal** — unusual, useful |
| 9 | **Avg % Return/Risk** stat card | A01 | `2.3%` — average return divided by risk per trade | All-time (implied) | Σ(realized P&L / risk at entry) / trade count | **steal** — exactly what Pop wants |
| 10 | **Avg Time in Trade** stat card | A01 | `4d` — average duration of closed trades | All-time (implied) | Σ(days from open to close) / trade count | **steal** — useful for strategy optimization |
| 11 | **Running P/L chart** | A01 | Line chart of cumulative P/L over time | Range: 30d, 90d, 6M, 1Y, YTD, ALL | Cumulative sum of closed trade P&L per period | **steal** — clean, simple, effective |
| 12 | **Trades table** (closed filter) | A02 | Table of closed trades with P&L | Status filter: All/Open/Closed/Expired/Assigned/Rolled/Pending | Populated from imported CSV | **improve** — no multi-leg grouping |

**Verdict notes:**
- Premium Insights wins on stat-card density: 10 cards before you scroll. Every card tells you something useful about portfolio health.
- The P/L number ($12,579.26) is factually wrong per Pop's broker-verified P/L ($11,852) — the engine ignores long legs of spreads. We steal the **layout and hierarchy**, not the calculation.
- "Avg % Return/Risk" and "Open Risk" are the closest any platform gets to Pop's preferred honest metric (return on capital at risk).

---

### A2. Trades table spec

| # | Column | Format | Notes |
|---|---|---|---|
| 1 | **Entry** | Date (M/D/YYYY) | Position open date |
| 2 | **Exit** | Date (M/D/YYYY) | Position close date; blank for open trades |
| 3 | **Ticker** | Text (uppercase symbols, e.g. SPXW, CRCL) | Underlying symbol |
| 4 | **Strategy** | Text (abbreviated: CSP, CC, PCS, CCS, BWB, etc.) | Strategy label |
| 5 | **Strike** | Dollar without decimals (e.g. `$68`, `$6`) | For multi-leg, shows the defining strike(s) |
| 6 | **Expiry** | Date (M/D/YYYY) | Option expiration date |
| 7 | **Price** | Dollar with 2 decimals (e.g. `$1.23`) | Premium per share / contract price |
| 8 | **Qty** | Integer (e.g. `1`, `2`) | Number of contracts |
| 9 | **P&L** | Dollar with 2 decimals, green/red coloring | Profit/loss of the trade |
| 10 | **Status** | Badge: Open, Closed, Expired, Assigned, Rolled, Pending | Status indicator |
| 11 | **Actions** | Button: "Edit" | Opens trade edit dialog (A04 — do not save) |

**Available filters (above table):**
- **Status:** All status, Open, Closed, Expired, Assigned, Rolled, Pending (pill-style buttons)
- Implicit: table shows all by default; filters narrow

**Edit dialog (A04_pi_trade_edit_dialog.png):**
- Opens a modal dialog with editable fields for each column value
- Preserves the original CSV-imported data
- Do NOT save — read-only audit

---

### A3. Strategy handling

**Recognized strategies:**
- CSP — Cash-Secured Put
- CC — Covered Call
- PCS — Put Credit Spread
- CCS — Call Credit Spread
- BWB — Broken-Wing Butterfly
- (also likely: Iron Condor, Butterfly — not explicitly visible in screenshots)

**Multi-leg display:**
- Each trade appears as **one row** in the table, regardless of number of legs
- The Strategy column labels the structure (e.g., "PCS" for a two-leg put credit spread)
- Strike column shows the defining strikes (for multi-leg, likely shows the short strike)
- **Problem:** The P/L calculation ignores long legs, inflating profit. A PCS shows profit from the short leg only.

**Butterfly / BWB support:**
- Strategy type "BWB" exists as a recognized label
- Implementation details of butterfly rendering (how all 3-4 legs display in one row) not confirmed from screenshots
- **Verdict:** steal the row-per-trade concept, improve the math

---

## B. TradesViz (tradesviz.com)

### B1. Component inventory — Dashboard & Overview

| # | Component | Screenshot | What it shows | Period/filter | Formula (if known) | Verdict |
|---|---|---|---|---|---|---|
| 1 | **Custom Dashboard (empty)** | B01 | "Your custom dashboard is empty" placeholder | Full date range (2025-05-28 to 2026-07-13) | N/A — user must add widgets | **skip** — empty state, not a component |
| 2 | **Total PnL (Overview KPI)** | B02 | Aggregate realized P&L across all trades | Default: full date range | Σ(realized P&L per trade) | **steal** — clean KPI card layout |
| 3 | **Per Trade Average PnL (KPI)** | B02 | Average net P&L across all trades | Default: full date range | Σ(P&L) / trade count | **steal** |
| 4 | **Daily Wins/Losses (bar chart)** | B02 | Green/red bars: profit vs loss count per day | Default: full date range (102 trades) | Count of positive-P&L trades vs negative-P&L trades per day | **improve** — useful but noisy |
| 5 | **Total PnL (line chart)** | B02 | Cumulative P&L line chart over time | Default: full date range | Cumulative sum of realized P&L | **steal** — simple cumulative line |
| 6 | **Daily PnL (bar chart)** | B02 | Per-day P&L as green/red bars | Default: full date range | Realized P&L per trading day | **steal** — good detail |
| 7 | **Trades table** | B02 | 102 total trades (50 per page, 3 pages) | Default: full date range | — | **improve** — basic, could be richer |
| 8 | **Monthly calendar** | B02 | Calendar grid with daily PnL values | July 2026 | Per-day realized P&L overlaid on calendar date grid | **improve** — useful but visually dense |
| 9 | **Options Analysis** | B03 | Options-specific analytics tool | User-defined | — | **improve** — powerful but buried in Tools menu |
| 10 | **Options Flow Table** | B04 | Real market data: TSM $46M sweep, MU $35M sweep, META $19M buy | Date range, Symbol filter, Excluded Symbols | Real-time options flow from market data feed | **skip** — not portfolio-relevant, it's market-wide flow |
| 11 | **Options Flow filters** | B04 | Date Range, Symbols, Excluded Symbols | User-defined | — | **skip** — decorrelation from portfolio view |
| 12 | **AI Summary button** | B04 | Purple button, triggers AI analysis of options flow | — | — | **improve** — interesting but on wrong page |
| 13 | **Calendar tab** | B05 | Full calendar view | — | — | **skip** — better done elsewhere |
| 14 | **Trades Analysis tool** | B06 | Trade analytics with multiple views | — | — | **improve** — information-dense but dated UI |
| 15 | **Metrics & Ratios** | B07 | Financial metric dashboards | — | Various: Sharpe, Sortino, etc. | **steal** — metric card layout |
| 16 | **Exit Analysis** | B08 | Analysis of exit timing / patterns | — | — | **improve** — unique but niche |
| 17 | **Tags Analysis** | B09 | Trade tagging / categorization view | — | — | **improve** — useful for strategy drill-down |
| 18 | **Trading Accounts page** | B10 | Multi-account management | — | — | **steal** — clean account switcher |
| 19 | **AI Q&A chatbot** | B11 | Conversational AI over trade data | — | — | **improve** — interesting but slow |
| 20 | **Custom Dashboard builder** | B12 | Widget-picker interface for custom layout | — | — | **steal** — best pattern for Stage 2 |

---

### B2. Trades table spec

| # | Column | Format | Notes |
|---|---|---|---|
| 1 | **Symbol** | Text (uppercase ticker) | Stock or option underlying |
| 2 | **Open Date** | Date (YYYY-MM-DD) | Position open date |
| 3 | **Close Date** | Date (YYYY-MM-DD) | Position close date |
| 4 | **PnL** | Dollar with 2 decimals, green/red | Per-trade realized P&L |
| 5 | **Side** | Text (Long/Short) | Direction of trade |

**Table behavior:**
- Default sort: by close date (newest first, implied)
- Pagination: 50 rows per page, 3 pages visible
- Shows aggregate P&L per trade, not leg-level breakdown
- **Missing:** strategy label column, strike, expiry, premium details — far less detailed than Premium Insights table

---

### B3. Strategy handling

**Recognized strategies:**
- No explicit strategy column visible in the default tables (Symbol + PnL only)
- Strategy tagging appears to be via **Tags Analysis** tool (B09) — user-assigned tags rather than auto-detected strategy names
- The **Options Analysis** (B03) tool may identify strategies from option chain data

**Multi-leg display:**
- Default overview table shows trades as flat rows — no multi-leg grouping in the default trades list
- Multi-leg strategies appear as separate rows for each leg (inferred — no explicit grouping visible)
- **Problem:** Cannot see a put credit spread as one row with net premium and max loss, unlike Premium Insights

**Butterfly / BWB support:**
- No explicit butterfly or broken-wing butterfly label detected
- Strategy handling is tag-based (user classifies, not auto-detected)
- **Verdict:** skip TradesViz strategy handling entirely — Premium Insights does this better

---

## C. Cross-platform verdicts

### Top 5 components worth rebuilding (ranked)

1. **Premium Insights stat-card row** — 10 cards, perfect hierarchy: P/L headline, then win/loss stats, then risk metrics, then time. Rebuild with correct math.
2. **Premium Insights strategy column & per-row trade rendering** — CSP/PCS/CC/BWB labels in one glance, multi-leg as a single row. Fix the math.
3. **Premium Insights Open Risk + Avg % Return/Risk cards** — closest thing to honest capital-at-risk metrics. Rebuild as-is, these are exactly Pop's preferred metrics.
4. **TradesViz Custom Dashboard builder** — widget-picker + free layout. Best pattern for Stage 2 commercial product. Way more flexible than Premium Insights's fixed layout.
5. **TradesViz Tags Analysis** — user-defined tagging with analytics drill-down. Useful for strategy categorization without hardcoding strategy names.

### Top 3 things both platforms do badly

1. **Multi-leg option math is broken or absent** — Premium Insights inflates P/L by ignoring long legs; TradesViz doesn't group legs into a position at all.
2. **No honest "capital at risk" / "return on risk" display** — Premium Insights has "Open Risk" but it's buried in the stat row; TradesViz has no equivalent. Neither shows return/risk ratio prominently.
3. **Neither shows real-time open position P&L with broker-paired data** — both depend on CSV import or batch sync, so open positions decay in accuracy between syncs.

### Interaction patterns that stood out

- **Premium Insights stat-card density:** 10 cards before scroll is unusually information-dense. All visible above the fold at 1440p. Each card uses a consistent layout: label in small muted text, value in bold large font, colored-green if positive metric.
- **Premium Insights pill filters:** Status filters use pill/button UI (All status, Open, Closed, etc.) instead of a dropdown. Feels faster, less cognitive load.
- **TradesViz sidebar navigation:** SPA-style sidebar with collapsible sections (Tools dropdown). The hierarchy is clear but the Tools submenu buries valuable features (Trades Analysis, Options Analysis, Metrics & Ratios) behind a click.
- **TradesViz AI Q&A:** Purple "AI Summary" button (B04) and dedicated chatbot (B11). Execution is slow (waits for model response) but the concept of natural-language queries on trade data is worth watching.
- **TradesViz Calendar overlay:** Monthly calendar with daily PnL values (B02) — a unique pattern, but too visually dense at 50px cells.
- **Empty state messaging:** TradesViz Custom Dashboard shows "Your custom dashboard is empty" (B01) — minimal but clear. Neither platform has notable loading or error states visible.

---

## D. Spec-grade raw details

### D1. Page inventory

#### Premium Insights

| Page/view | URL path | Purpose | Reachable from |
|---|---|---|---|
| Dashboard | `/home` | Main dashboard: stat cards, P/L chart, trades table | Default landing page after login |
| Calendar | `/calendar` | Trade calendar view | Sidebar |
| Income / Yield | `/income` | Monthly yield / income breakdown | Sidebar |
| Strategy Analytics | `/stats` | Per-strategy win rate, premium, returns | Sidebar |
| Import | `/import` | CSV import summary screen | Sidebar |
| Wheels | `/wheels` | Wheels strategy tool | Sidebar |
| Journal | `/journal` | Trade journal / thesis entries | Sidebar |
| Pro Upgrade | `/checkout?plan=pro&billing=yearly` | Upgrade to Pro plan | Sidebar |

#### TradesViz

| Page/view | URL path | Purpose | Reachable from |
|---|---|---|---|
| Custom Dashboard | `/` or `/home/` | Default landing: customizable widget dashboard | Default after login |
| Overview | Tab in SPA | KPI cards + charts + trades table | Sidebar → Overview |
| Tables | Tab in SPA | Full trades table view | Sidebar → Tables |
| Calendar | Tab in SPA | Trade calendar | Sidebar → Calendar |
| Notes | Tab in SPA | Trade notes | Sidebar → Notes |
| Trade/Day Plans | Tab in SPA | Trading plan management | Sidebar → Trade/Day Plans |
| Custom Dashboards | Tab in SPA | Dashboard builder | Sidebar → Custom Dashboards |
| AI Q&A | Tab in SPA | AI chatbot over trade data | Sidebar → AI Q&A |
| Summaries | Tool (dropdown) | Trade summaries | Sidebar → Tools → Summaries |
| Tags Analysis | Tool (dropdown) | Tag-based categorization | Sidebar → Tools → Tags Analysis |
| Trades Analysis | Tool (dropdown) | Detailed trade analytics | Sidebar → Tools → Trades Analysis |
| Metrics & Ratios | Tool (dropdown) | Sharpe, Sortino, etc. | Sidebar → Tools → Metrics & Ratios |
| Exit Analysis | Tool (dropdown) | Exit timing patterns | Sidebar → Tools → Exit Analysis |
| Technical Analysis | Tool (dropdown) | Technical indicators | Sidebar → Tools → Technical Analysis |
| Options Analysis | Tool (dropdown) | Options-specific stats | Sidebar → Tools → Options Analysis |
| Options Flow | `/optionsflow/` | Real-time options flow market data | Navigation bar |
| Trading Accounts | `/accounts/tradingaccounts/` | Multi-account management | Sidebar or settings |
| Import/Export | `/import` | Data import/export | Navigation |
| Account Settings | `/accounts/settings/` | Account configuration | Sidebar or settings |

---

### D2. Design tokens observed

#### Premium Insights

**Colors:**
- **Profit green:** approx `#16a34a` or `#22c55e` (green-600/500 range) — used for positive P&L values and green stat cards
- **Loss red:** approx `#dc2626` or `#ef4444` (red-600/500 range) — used for negative P&L values
- **Accent:** likely blue (`#2563eb`) — sidebar active state, interactive elements
- **Background:** white (`#ffffff`) or near-white main content area
- **Sidebar:** darker background (`#1e293b` slate-800 or similar)
- **Stat card value text:** bold, large, profit-green by default
- **Stat card label text:** muted gray (`#64748b` or similar), smaller
- **Badge colors:** Green for Closed (profit), Red/Orange for Expired/Assigned, Blue for Open, Gray for Pending

**Typography:**
- **Font family:** likely system stack or Inter (not explicitly inspectable from screenshots alone)
- **Hero numbers (P/L):** ~32–40px bold
- **Stat card values:** ~18–24px semibold
- **Stat card labels:** ~12–14px regular, muted
- **Table text:** ~13–14px regular
- **Column headers:** ~12px semibold, uppercase (typical pattern)

**Density:**
- **Stat cards:** 10 cards in a row, flexible grid (approx 5 across on 1440p). Airy padding (~16–20px internal).
- **Table rows per screen:** ~8–10 rows visible without scroll (at standard density)
- **Card style:** Clean white cards with rounded corners (~8–12px radius), subtle shadow/border

#### TradesViz

**Colors:**
- **Profit green:** approx `#22c55e` or `#16a34a` — used for positive PnL values and green bars
- **Loss red:** approx `#ef4444` or `#dc2626` — used for negative PnL values and red bars
- **Accent:** purple (`#a855f7` or similar) — AI Summary button, some interactive elements
- **Background:** dark theme dominant (`#0f172a` or `#1e293b` — slate-900/800)
- **Content area:** slightly lighter dark (`#1e293b` or `#334155`)
- **Sidebar:** same dark background as main, with lighter highlight on active item
- **Badge colors:** not prominently visible; status inferred from table data rather than badges

**Typography:**
- **Font family:** likely system stack or Inter (dark theme default)
- **Dashboard/KPI values:** ~28–32px bold white/text
- **Chart labels:** ~11–12px muted
- **Table text:** ~12–13px
- **Column headers:** ~11px semibold

**Density:**
- **KPI cards:** 2–3 per row, compact layout
- **Table rows per screen:** ~20–25 rows (50 per page, high density)
- **Card style:** Tight dark cards with minimal padding, flat design (no shadows)
- **Overall:** More compact than Premium Insights, higher information density but less visual hierarchy

---

### D3. Formats & defaults

#### Premium Insights

- **Currency format:** `$X,XXX.XX` (2 decimals). Negative shown as `-$X,XXX.XX` in red.
- **Percent format:** `XX.X%` (1 decimal for win rate, return/risk)
- **Date format (tables):** `M/D/YYYY` (e.g., 1/15/2026)
- **Date format (charts):** Same, abbreviated on axis labels
- **Default sort of trades table:** By Entry date descending (newest first, implied)
- **Default time range (P/L chart):** `ALL` (all-time) on initial load
- **Pagination:** Not observed; table likely loads all visible and filters client-side
- **Default landing page:** `/home` — Dashboard

#### TradesViz

- **Currency format:** `$X,XXX.XX` (2 decimals). Negative in red.
- **Percent format:** `XX.XX%` (2 decimals where applicable)
- **Date format (tables):** `YYYY-MM-DD` (ISO 8601)
- **Date format (calendar):** Same, with month headers
- **Default sort of trades table:** By Close Date descending (newest first)
- **Default time range:** Full date range available (2025-05-28 to 2026-07-13 per screenshot)
- **Pagination:** 50 rows per page, manual page navigation
- **Default landing page:** `/` or `/home/` — Custom Dashboard (empty by default)
- **Account selector:** Visible at top (ACCOUNT 2 (1) per screenshot), dropdown-style

---

### D4. States

#### Premium Insights

- **Empty state:** Not observed in screenshots (account has 116 imported trades). Likely a zero-state message like "No trades yet" or "Import your first CSV."
- **Loading state:** Not observed. Likely spinner or skeleton placeholders during initial data load.
- **Error state:** Not observed during audit.

#### TradesViz

- **Empty state (confirmed):** Custom Dashboard page (B01) — "Your custom dashboard is empty" centered message on blank page. Minimal but clear.
- **Loading state:** Not observed. Likely spinner during page transitions (SPA pattern).
- **Error state:** Not observed during audit.
- **AI Q&A (B11):** Shows conversation UI. Loading likely shows a "thinking" indicator while generating AI response.

---

## Research Question Answers (Section 1.2)

### Q1: Best at-a-glance options income view

**Premium Insights Dashboard (/home)** is the clear winner. The stat-card row shows Total P/L, Open Premium ($13,198.93), Win Rate (93.3%), and Avg % Return/Risk (2.3%) in a single scan. The Running P/L chart provides the time-series context below. The hierarchy: headline P/L → win/loss metrics → risk metrics → time metrics. TradesViz requires clicking through tabs and tools to assemble the same picture.

### Q2: Multi-leg structure rendering

**Premium Insights** renders multi-leg as one trade row with a strategy label (PCS, CCS, BWB). **TradesViz** does not group legs and offers no auto-detected strategy label. A proper broken-wing butterfly row should show: Strategy (BWB), Strikes (spread of three strikes), Net Premium, Max Loss, Max Profit, Break-evens, Status & P&L — all in one row.

### Q3: Time handling

**Premium Insights:** Range picker buttons (30d, 90d, 6M, 1Y, YTD, ALL) on the P/L chart — efficient, no calendar popup needed. Table dates use M/D/YYYY. **TradesViz:** Date range input fields on every page (2025-05-28 to 2026-07-13 format), plus a calendar tab. Premium Insights's pill-style range buttons are more efficient for quick period switches.

### Q4: Capital at risk / collateral / return on risk

**Premium Insights** has the closest: "Open Risk" ($10,188.13) and "Avg % Return/Risk" (2.3%). The Open Risk stat card is exactly what Pop asks for — total max loss across all open positions. **TradesViz** offers no equivalent metric. Premium Insights's approach is worth stealing, but verify the denominator calculation matches Pop's definition.

### Q5: Filters and drill-downs that earn their space

**Earn their space:**
- Premium Insights status pill filters (All/Open/Closed/Expired/Assigned/Rolled/Pending) — fast, one-click, no dropdown clutter
- TradesViz Tags Analysis — user-defined categorization is flexible without hardcoded strategy lists

**Decoration:**
- TradesViz Options Flow (B04) — market-wide options flow data is irrelevant for a personal portfolio dashboard
- TradesViz AI Summary button on Options Flow — interesting feature on the wrong page

### Q6: Empty, loading, error states

**Observed:** TradesViz Custom Dashboard empty state — "Your custom dashboard is empty" (B01). **Not observed for either platform:** loading skeletons, error screens, or native empty states for data-grounded views. Both platforms assume data is already imported, which makes them fragile for live API-driven apps. Stage 1 needs robust loading skeletons and error recovery.

### Q7: Surprising positive patterns

1. **Premium Insights stat-card density-to-scroll ratio** — 10 metrics above the fold is unexpectedly information-dense. Most dashboards show 4–6. This works because the cards use consistent layout: label (muted, small) / value (bold, large) / no chart noise.
2. **Premium Insights "Avg % Capture"** — the concept of "what % of max premium did I actually capture" is a genuinely useful metric not common in trading platforms.
3. **TradesViz Custom Dashboard builder (B12)** — the widget-picker interface lets you compose a free-form dashboard from available widgets. This is more flexible than Premium Insights's fixed layout and would scale well for Stage 2's commercial product.
4. **TradesViz multi-account support (B10)** — clean account switcher and per-account views. Essential for a true portfolio tracker.
5. **Premium Insights pill-style filters** — clickable pills for status feel faster than dropdown selects. Low cognitive load, high usability.

---

*End of findings document.*
