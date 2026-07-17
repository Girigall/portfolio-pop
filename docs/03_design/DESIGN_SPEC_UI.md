# DESIGN SPEC — Portfolio Dashboard v1 UI

**Status:** DRAFT — awaiting Pop's approval
**Design DNA:** Premium Insights' presentation (audit winner) + honest metrics + states neither incumbent has. Evidence refs = audit findings sections/screenshots.

---

## 1. Design principles

1. **Density with hierarchy** — 10 stat cards above the fold works because each card is label-small / value-big / zero chart noise (audit Q7.1)
2. **Color = meaning only** — green profit, red loss, accent for interaction; never decorative rainbow
3. **One row = one position** — legs are detail, structures are the object (audit Q2)
4. **Every number auditable** — hover/tap shows source + timestamp
5. **States are first-class** — loading, empty, partial-failure designed up front (audit Q6 gap)

## 2. Design tokens

| Token | Value | Source |
|---|---|---|
| Profit green | `#16a34a` | audit D2 (PI) |
| Loss red | `#dc2626` | audit D2 |
| Accent | `#5b4fd1` (indigo) | differentiates from both incumbents |
| Background | `#f7f7fb` page · `#ffffff` cards | PI light theme won the audit |
| Text primary | `#1a1a2e` · muted `#6b7280` | |
| Card | radius 12px · border `#e5e7eb` 1px · no heavy shadow | PI card style, flattened |
| Badges | Open `#e2f0fd/#1d6fc4` · Closed-profit green pair · Expired amber pair · BWB `#efe9ff/#5b4fd1` · PCS `#e2f7ef/#0b7a55` | audit D2 badge semantics, extended per strategy |

**Typography:** system stack / Inter. Hero value 32px/600 · card value 22px/600 · card label 12px/400 muted · table 13px · column headers 12px/500. Two weights only (400/600).

## 3. Layout (desktop-first, single column ~1100px)

```
[H1  Accounts strip — 5 compact cards + net worth chip]
[S1  Stat-card row — 10 cards, 5×2 grid]
[S2  Running P/L chart + range pills]
[S3  Open positions (structures) table]
[S4  Closed trades table + pill filters]
[S5  Stocks section (per account)]
[S6  History trends (renders once archive ≥ 4 weeks)]
[footer: data timestamps · source notes · known-gaps line]
```
Mobile: cards wrap 2-across; tables become stacked rows (structure header + legs collapse).

## 4. Component specs

### S1 — Stat cards (10)
Grid `repeat(auto-fit, minmax(180px,1fr))`, gap 12. Card: label · value · sub-line (context, e.g., "vs $2,463 monthly avg"). Values color-code only when signed (P/L). Metrics & formulas per PRD F2 — formula shown on hover (audit A1 pattern, but we disclose math).

### S2 — Running P/L chart
Chart.js line (cumulative) with bar toggle (monthly). Height 260px. Range pills right-aligned above: `30d · 90d · 6M · YTD · ALL` — active pill accent-filled (audit Q3 winner). Default YTD. Persist choice in localStorage.

### S3 — Open structures table (the flagship)
Columns: Opened · Underlying · **Strategy badge** · Strikes (`7200 / 7250 / 7270`) · Expiry · Net premium (+green/−red) · Open P/L · **Max loss** (always red, always present) · Break-even(s) · Status.
Leg sub-line under strategy, muted 11.5px: `+1 7200P  −2 7250P  +1 7270P`.
BWB row is the acceptance benchmark (PRD G2, audit Q2 ideal-row).

### S4 — Closed trades
Pill filters row: `All · Options · Stocks` + `YTD · 90d · All time` (two pill groups, audit Q5 winner). Table: Closed · Underlying · Qty · Realized P/L. Footer line: "N trades · net +$X — ties to Robinhood ✓" with reconciliation checkmark when totals match the aggregate endpoint.

### S5 — Stocks section
Per-account subsections (Stocks, IRA). Columns: Symbol · Qty · Avg cost · Price · Value · P/L $ · P/L % · % of sleeve. Concentration flag icon past 25%.

### S6 — History trends (archive-fed)
Weekly net-worth line · monthly options income bars · realized-vs-unrealized area. Section renders a friendly "collecting history — first trend at 4 weeks" empty state until data suffices.

## 5. Formats

| Thing | Format |
|---|---|
| Currency | `$1,234.56` · negatives `-$1,234.56` in red (PI convention, audit D3) |
| Percent | 1 decimal (`93.3%`) |
| Dates (UI) | `M/D/YYYY` tables · `Jul 10` chart axes |
| Large numbers | no abbreviation below $1M |
| Timestamps | "as of 4:00 PM ET · Jul 15" footer chips |

## 6. States (each section independently)

| State | Treatment |
|---|---|
| Loading | Gray skeleton blocks matching final geometry — no spinners on cards |
| Partial failure | Amber banner in-section: "Live marks unavailable — showing last archive (Jul 11)" |
| Empty | Plain-language line + the one action that fixes it |
| Auth expired | Full-width card: "Robinhood connection needs re-authorization → connector settings" |
| Stale quotes | Value + muted "as of <time>" tag (never silently stale) |

## 7. Interaction

- Hover any stat value → tooltip: formula + data source + timestamp
- Click structure row → expand legs with per-leg marks/greeks (v1: expand only; no modal)
- Pill filters persist per user (localStorage)
- No drag-drop, no custom layout in v1 (TViz B12 pattern reserved for Stage 2)

## 8. Accessibility

- Text contrast ≥ 4.5:1 on all tokens above (verified pairs)
- Color never sole signal: signs (+/−) accompany color; badges carry text
- Charts: aria-label summaries + table fallback text

---

**APPROVAL:** ☐ Approved by Pop · date: 16-7-2026 · changes requested: None
