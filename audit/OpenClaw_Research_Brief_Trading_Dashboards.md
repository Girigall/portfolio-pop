# Research Brief — Trading Dashboard UX Audit

**For:** OpenClaw (executing agent)
**Requested by:** Pop
**Consumed by:** Claude (Cowork) — findings are the raw material for a **PRD** (Product Requirements Document) and a **TSD/TDD** (Technical Spec / Design Document), both of which Pop approves BEFORE any development starts
**Date:** 2026-07-13
**Estimated effort:** 1.5–2.5 hours of guided browsing

> **Detail bar:** because these findings must survive translation into a PRD and TDD, capture the *most minimal details* — exact labels, number formats, defaults, colors, states. When in doubt whether a detail is too small to record: record it. A spec cannot be written from vibes.

---

## 1. Mission & end goal

Audit two options-trading analytics platforms — **Premium Insights** (premiuminsights.ai) and **TradesViz** (tradesviz.com) — and document their data visualization and UX patterns in the exact format specified in Section 5.

The goal is NOT a review or opinion piece. It is a **component inventory**: what exists on screen, how each number is defined, and how trades are displayed. The consumer of this document is another AI agent that will rebuild the best of these patterns. Precision beats prose.

### 1.0 Process rule — questions BEFORE work

After reading this brief and before touching either platform: if anything is ambiguous, contradictory, or missing (access, scope, output format), **raise all questions to Pop first and wait for answers**. Do not resolve ambiguity by guessing mid-task.

### 1.1 What this research feeds — the app being built

Pop is building a **portfolio tracking app from scratch**, in two stages:

- **Stage 1 (immediate):** a personal full-portfolio dashboard — all brokerage accounts, stock positions with P&L, and an options trading desk where multi-leg structures (put credit spreads, butterflies, **broken-wing butterflies**) display as single grouped positions with net premium, open P&L, and max loss. History accumulates weekly into a permanent archive. Data comes live from Robinhood's API — pairing and math computed from broker ground truth, never inferred from CSVs.
- **Stage 2 (later):** a commercial product competing in the same category as the two platforms under audit.

Context that sharpens the audit — both platforms FAILED Pop's data-accuracy test:

- **Premium Insights:** reported +$188,540 P/L on a portfolio whose true P/L is +$11,852 — its engine ignores the long legs of spreads. Excellent *visual design*, broken *math*. We steal presentation, not engine.
- **TradesViz:** mispaired an assigned stock lot against a purchase 10 months later, inventing a phantom +$4,920 trade. Deep features, dated presentation.

Therefore always separate **how it looks** (valuable) from **what it computes** (known broken). A beautiful widget showing a wrong number can still be a "steal" for layout — record both facts.

### 1.2 Key research questions the findings must answer

1. What is the single best at-a-glance view of options income on each platform, and what makes it work (layout, hierarchy, color)?
2. How does each platform render a multi-leg structure in a table row — and based on the best elements seen, what WOULD a good broken-wing butterfly row look like?
3. How is time handled — range pickers, period comparisons, calendar views? Which pattern is most efficient?
4. What (if anything) do they show about **capital at risk / collateral / return on risk**? This is Pop's preferred honest metric.
5. Which filters and drill-downs earn their screen space, and which are decoration?
6. What do empty, loading, and error states look like? (The Stage 1 app reads a live API; these states matter.)
7. Anything either platform does that positively surprised you — flag patterns not asked about here.

---

## 2. Access & Safety Rules (non-negotiable)

1. **Read-only conduct.** Do not edit, delete, merge, or modify any trade, position, or setting on either platform. Do not click any "Import", "Sync", "Delete", or "Edit" button. Browsing and screenshots only.
2. **Logins — Pop has active accounts on BOTH platforms with real imported data. Audit the logged-in dashboards, NOT the public marketing pages.** Both are journals — no money can move through them. Credentials are stored in your Bitwarden vault under these entry names:

   | Platform | Bitwarden entry |
   |---|---|
   | Premium Insights (premiuminsights.ai) | `premiuminsights.ai` |
   | TradesViz (tradesviz.com) | `TradesViz` |

   Retrieve them from the vault only. Never write, repeat, or log the passwords in chat, files, memory, or the findings document. Use them on their own sites only.
3. **Never request, use, or store Robinhood credentials.** They are not needed for this task. If any page asks to connect a brokerage, skip it.
4. Do not export, download, or transmit Pop's trade data anywhere outside the deliverable document.
5. If a page errors or a section is empty because of missing data, note it and move on. Do not attempt to fix data.

---

## 3. Platform A — Premium Insights (premiuminsights.ai)

Pop's account has an imported dataset (~116 trades staged). Audit these areas:

### 3.1 Main dashboard
- Screenshot the full dashboard, top to bottom.
- For EVERY stat card (e.g., Total P/L, Win Rate, Avg Win, Avg Loss): record label, value format, time period it covers, and — if discoverable via tooltips/help — how it's calculated.
- Running P/L chart: chart type, what the Y axis is (cumulative? per-period?), available time ranges (14d/30d/60d/90d/6M/1Y/YTD/ALL), what happens on hover.

### 3.2 Trades table
- Screenshot the open & closed trades table.
- Record every column name and its format (e.g., "Strike: $ with 0 decimals").
- Record available filters (status, strategy) and what the Edit action allows (open the dialog, screenshot it, do NOT save).
- How are multi-leg positions displayed — one row or multiple? What does the "Strategy" column call a put credit spread? Is there any butterfly label?

### 3.3 Strategy analytics
- Screenshot any per-strategy breakdown (win rate by strategy, avg premium, return %).
- List which strategies the platform recognizes (CSP, CC, PCS, etc.).

### 3.4 Other
- Trade journal / thesis feature: screenshot the flow (do not submit entries).
- Import flow: screenshot the import summary screen only (do NOT click final Import).
- Monthly yield / "return on capital" views: screenshot + define the denominator if shown.

---

## 4. Platform B — TradesViz (tradesviz.com)

Pop's account has synced/imported Robinhood data. Audit these areas:

### 4.1 Main dashboard
- Screenshot default dashboard. List every widget present (calendar heatmap, cumulative P/L, win %, etc.) with its label and period.
- Note which widgets are customizable (their "Custom Dashboard" feature) — screenshot the widget-picker list if accessible.

### 4.2 Trades & grouping
- Screenshot the trades list. Record all columns + formats.
- Find one multi-leg options position (any SPX/SPXW trade). Screenshot how legs are displayed and how the platform names the strategy.
- Screenshot any "options-specific" views: options stats page, expiration calendars, strategy tagging.

### 4.3 Charts & analytics
- Screenshot 3–5 of the most information-dense analytics views (e.g., P/L by day-of-week, by symbol, by tag, drawdown chart).
- For each: chart type, axes definitions, filters available.

### 4.4 Other
- Per-account views (multiple accounts UI): screenshot the account switcher/aggregation.
- AI features (AI Q&A, AI coach): one screenshot each, note input/output format.

---

## 5. Deliverable — exact output format

Return ONE markdown document titled `Dashboard_UX_Audit_Findings.md` plus a folder of numbered screenshots. Structure:

```
# Findings

## A. Premium Insights
### A1. Component inventory
| # | Component | Screenshot | What it shows | Period/filter | Formula (if known) | Verdict: steal / skip / improve |

### A2. Trades table spec
| Column | Format | Notes |

### A3. Strategy handling
- Recognized strategies: [...]
- Multi-leg display: [...]
- Butterfly/BWB support: [...]

## B. TradesViz
(same structure: B1 inventory, B2 table spec, B3 strategy handling)

## C. Cross-platform verdicts
- Top 5 components worth rebuilding (ranked, one line each on why)
- Top 3 things both platforms do badly (one line each)
- Any interaction pattern that stood out (hover, drill-down, filters)

## D. Spec-grade raw details (feeds the PRD/TDD directly)
### D1. Page inventory (per platform)
| Page/view | URL path | Purpose | Reachable from |

### D2. Design tokens observed (per platform)
- Colors: profit green (hex if inspectable), loss red, accent, backgrounds, badge colors + their meanings
- Typography: font family if identifiable, approximate sizes for hero numbers vs labels vs table text
- Density: rows per screen in tables, card padding style (airy vs compact)

### D3. Formats & defaults
- Number formats: currency decimals, negative style (-$X vs ($X) vs red), percent decimals, large-number abbreviations
- Date formats used in tables vs charts
- Default sort of trades tables · default time range of charts · pagination or infinite scroll
- Default landing page after login

### D4. States
- Empty state (no data): screenshot + copy text
- Loading state: skeleton / spinner / blank
- Error state if encountered: screenshot + copy text
```

**Verdict column rules:** "steal" = rebuild as-is · "improve" = good idea, flawed execution (say what's flawed in ≤10 words) · "skip" = noise.

---

## 6. Delivery — exact destination and structure (mandatory)

Deliver everything inside the existing `audit` folder at this path:

```
/Users/cor/Library/CloudStorage/GoogleDrive-helloivannu@gmail.com/My Drive/Obsidian/Obsidian Vault/00_POP/Projects/04_System/05_Portfolio/audit/
```

Required structure — nothing outside it, no loose files in 05_Portfolio:

```
05_Portfolio/
└── audit/
    ├── OpenClaw_Research_Brief_Trading_Dashboards.md            ← this brief
    ├── OpenClaw_Research_Brief_Trading_Dashboards_findings.md   ← your output (exact name)
    └── screenshots/
        ├── A01_pi_dashboard.png        ← numbered, prefixed by platform
        ├── A02_pi_trades_table.png
        ├── B01_tviz_dashboard.png
        └── ...
```

- Findings filename is **exactly** the brief's name + `_findings` suffix.
- Every screenshot referenced in the findings tables must use its filename (e.g., "A03") so rows and images cross-reference cleanly.

**Flexibility clause:** if OpenClaw already maintains its own folder/naming conventions in memory, it MAY adapt this structure to match them — under two hard constraints: (1) everything stays inside `05_Portfolio/audit/` (or a single clearly-named folder inside `05_Portfolio/`), never loose in the parent folder; (2) the adapted structure is stated at the top of the findings file so Claude can navigate it without guessing.

---

## 7. Definition of done

- [ ] Questions (if any) raised to Pop and answered BEFORE starting the audit
- [ ] All 7 research questions from Section 1.2 explicitly answered in the findings
- [ ] Section D (spec-grade details: page inventory, design tokens, formats, states) fully filled for BOTH platforms
- [ ] Every section 3.x and 4.x has at least one screenshot
- [ ] Every stat card on both main dashboards is in a component inventory row
- [ ] Both trades-table specs are complete (all columns)
- [ ] Section C verdicts are filled
- [ ] Zero edits/imports/deletes performed on either platform
- [ ] Findings + screenshots delivered inside `05_Portfolio/audit/` exactly as Section 6 specifies — no files anywhere else
