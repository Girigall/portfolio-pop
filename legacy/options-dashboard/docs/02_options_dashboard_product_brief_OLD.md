# 01_AJAX_Tracker_Product_Brief

Created: 2026-05-25 15:12 EDT  
Updated: 2026-05-25 15:12 EDT  
Folder: `03_Personal/01_Projects/03_Ajax Tracker`  
Sources consolidated: `02_AJAX PDR.md`, `02_AJAX PDR v2.md`  
Do not touch: `01_spx_strategy.md`  
Status: Consolidated product direction  

---

## What This Document Is

This document consolidates only the two AJAX Tracker PDR files:

```text
02_AJAX PDR.md
02_AJAX PDR v2.md
```

It intentionally does **not** consolidate, modify, or replace:

```text
01_spx_strategy.md
```

That file remains the separate source strategy document for Pop's SPX Put Credit Spread strategy.

---

## Folder Verdict

The two AJAX PDR files are not equal duplicates.

They are:

```text
v1 = initial proposal + Pop critique
v2 = revised direction after Pop feedback
```

Current interpretation:

```text
Use v2 as the active product direction.
Preserve v1 only for lessons learned, rejected assumptions, and Pop's correction history.
```

---

## Source Status

| File | Role | Status |
|---|---|---|
| `02_AJAX PDR.md` | First PDR proposal with Pop inline feedback | Superseded by v2, historically valuable |
| `02_AJAX PDR v2.md` | Revised AJAX Tracker PDR after Pop feedback | Current product direction |

---

# 1. Product Problem

Pop does most trading through SPX options, especially Put Credit Spreads.

Current workflow:

```text
1. Pop takes a screenshot of the options chain.
2. Pop sends it to ChatGPT for strategy evaluation.
3. ChatGPT approves or denies.
4. If approved, Pop executes the trade manually.
5. Data is lost afterward: no structured record, tracker, analytics, or learning loop.
```

Premium Insights helps after the fact through CSV import, but it does not solve the full workflow:

```text
no pre-trade analysis
no approval workflow
no direct API
manual CSV import
no real-time/open portfolio tracking
limited asset coverage
```

---

# 2. Active Product Direction

AJAX Tracker should be a personal finance/trading dashboard that unifies:

```text
pre-trade screenshot analysis
strategy approval/denial
portfolio tracking
open and historical trades
analytics
journal
calendar
settings/strategies
```

Approved location:

```text
mc.ivan-nunez.com/ajax
```

Reason:

```text
Same subdomain and deployment surface as Mission Control, so there is only one dashboard stack to maintain.
```

Authentication:

```text
Cloudflare Access with Google Auth.
Access limited to Pop and his wife.
```

Design direction:

```text
Independent design system from Mission Control.
Dark mode required.
Visual references should be researched before implementation.
```

Important boundary:

```text
AJAX is read-only. It does not execute trades.
```

---

# 3. Current Architecture Direction

Use the Mission Control app as the host, with an AJAX route:

```text
mc.ivan-nunez.com/ajax
```

Core architecture:

```text
Frontend: NextJS, same app/deploy as MC
Route: /ajax
Vision/OCR: multimodal model reads screenshots
Evaluation: AJAX evaluates extracted trade against active strategy
Broker sync: Robinhood read-only sync where possible
Market data: daily price/mark-to-market source such as yfinance
Database: SQLite local
Auth: Cloudflare Access
```

Current preferred stack from v2:

| Layer | Direction | Reason |
|---|---|---|
| Frontend | NextJS inside MC app | One codebase and deploy |
| Route | `/ajax` | Same authenticated dashboard surface |
| Vision | multimodal model | Reads screenshot directly |
| Evaluation | AJAX | Matches agent purpose |
| Broker sync | Robinhood via `robin_stocks` | Potential auto-import without CSV |
| Market data | `yfinance` or equivalent | Daily mark-to-market support |
| Data store | SQLite | Local, free, open source |
| Auth | Cloudflare Access | Avoid custom login code |

---

# 4. Important Correction From v1 To v2

## Vision model confusion

v1 mentioned GPT-4o Vision. Pop questioned why GPT-4 was involved.

v2 revised the direction toward HAL/AJAX using a multimodal model instead of assuming GPT-4o.

Durable lesson:

```text
Do not default to external paid APIs when Pop expects local/free/open-source alternatives unless there is a clear reason.
```

## Live P/L ambiguity

Pop asked how live P/L tracking would technically work.

v2 clarified a daily sync/mark-to-market model:

```text
Robinhood Sync daily for positions and account data.
yfinance daily for market prices and mark-to-market.
```

This is not true high-frequency live trading infrastructure. It is portfolio tracking and analytics.

## Crypto execution misunderstanding

Pop corrected that crypto is tracking only, not execution.

Rule:

```text
AJAX Tracker tracks portfolio data. It does not execute trades.
```

## Stop-loss notifications removed from MVP

v1 proposed stop-loss alerts.

Pop rejected them for MVP.

Rule:

```text
No stop-loss notifications in MVP.
```

## Branding corrected

v1 implied AJAX could follow MC branding.

Pop corrected this.

Rule:

```text
AJAX Tracker should have its own dark-mode design system, separate from Mission Control.
```

## Need for more original thinking

Pop explicitly criticized v1 because it mostly repeated what he had already said.

Lesson:

```text
For product docs, HAL/AJAX must add judgment, options, comparisons, technical reasoning, and better feature coverage, not just restate Pop's idea.
```

---

# 5. Active Workflow

Current intended flow:

```text
1. Pop uploads a screenshot by drag/drop or clipboard.
2. HAL Vision / multimodal layer extracts structured trade data:
   - strike
   - short/long legs
   - Greeks
   - IV
   - credit
   - spread width
   - DTE
   - underlying
3. AJAX evaluates the candidate trade against the selected strategy.
4. AJAX returns APPROVED or DENIED with reasons.
5. If approved, Pop manually executes the trade in Robinhood.
6. Pop confirms execution or Robinhood Sync detects the position.
7. Trade is stored in SQLite as OPEN.
8. Daily sync updates positions, pricing, Greeks where available, and mark-to-market.
9. When closed, the trade becomes CLOSED and contributes to analytics, tax reporting, calendar, and journal.
```

Important wording:

```text
AJAX approves/denies. Pop executes.
```

---

# 6. MVP Scope

The revised MVP should include:

```text
Screenshot upload and extraction
AJAX approval against SPX strategy
Portfolio tracker for open/closed trades
SQLite local storage
Dashboard with key P/L, win rate, open premium, and open risk metrics
Calendar with monthly profits
Robinhood sync if technically viable and safe
Basic trade journal
```

Not MVP:

```text
trade execution
stop-loss notifications
complex multi-user product behavior
custom auth system
full tax platform beyond basic export/reporting
```

---

# 7. Complete Feature Direction

## Screener

```text
Screenshot upload
Manual trade entry option
Structured extraction
Strategy selection
AJAX approval/denial
History of evaluated screenshots/trades
```

## Portfolio

```text
Open trades
Closed trades
Unrealized P/L
Realized P/L
Greeks where available
DTE
Progress toward max profit
Duration
ROI
Roll assistant later, not necessarily MVP
```

## Calendar

```text
Monthly view
Profit markers by day
Filters by ticker, strategy, month
Click day to see trades that expired or closed that day
```

## Analytics

This is especially important to Pop.

Required direction:

```text
granular dashboard
win rate global and by strategy
equity curve
cumulative P/L
drawdown
heatmap of positions
open risk
open premium
comparison of AJAX-approved trades vs actual outcomes
filters by strategy/ticker/month/status
```

## Trade Journal

```text
Notes per trade
Lessons learned
Emotional/context notes
Timeline connection to each trade
```

## Tax Report

```text
Annual gains/losses report
CSV export for accountant
Potential wash-sale awareness, but verify scope before promising automation
```

## Settings

```text
Strategy parameters
Robinhood connection settings
Account preferences
Notification preferences, with stop-loss notifications off for MVP
```

---

# 8. Active Decisions

| Question | Current Decision |
|---|---|
| Route or separate domain? | `/ajax` under `mc.ivan-nunez.com` |
| Database | SQLite, local/free/open source |
| Supabase | Not preferred for MVP |
| Crypto | Tracking only |
| Trade execution | No execution, read-only only |
| Broker | Robinhood, investigate/use read-only sync if viable |
| Stop-loss notifications | Not in MVP |
| Design | Own dark-mode design system, not MC branding |
| Analytics | High priority, must be granular |
| Screenshots | Must be stored or referenced in a clear data model |

---

# 9. Open Technical Questions

These need technical design before implementation:

```text
Where screenshots are stored.
How screenshots map to extracted JSON.
How extracted candidate trades map to executed trades.
Whether Robinhood sync through robin_stocks is stable/safe enough.
How MFA/session handling works for read-only Robinhood access.
How credentials are stored without exposing secrets.
How daily sync jobs run.
How yfinance handles SPX options/Greeks limitations.
What exact data is reliable from Robinhood vs inferred.
How to reconcile manual execution confirmation with broker-detected positions.
What schema handles multi-leg options cleanly.
How analytics are calculated and cached.
```

---

# 10. Data Model Direction

v1 proposed a single `trades` table with spread fields. That is useful as a starting sketch, but may not be sufficient for multi-leg options.

Better likely direction:

```text
trades = high-level trade/position lifecycle
trade_legs = individual option/equity/crypto legs
strategy_evaluations = screenshot/candidate approval records
screenshots = uploaded source files and metadata
broker_sync_runs = sync audit trail
market_snapshots = price/greek/mark-to-market snapshots
journal_entries = notes and learning records
accounts = brokerage/account metadata
```

Reason:

```text
SPX Put Credit Spreads are multi-leg positions. A single strike/strike2 model can work for MVP, but a leg-based model is cleaner and scales better.
```

---

# 11. Lessons From v1 Feedback

Pop's v1 feedback produced these durable product-process lessons:

```text
Do not merely mirror Pop's input; improve it.
Do not assume paid/external APIs without explaining why.
Do not call it live tracking unless the mechanism is clear.
Do not confuse portfolio tracking with trade execution.
Do not add notifications Pop explicitly does not want in MVP.
Do not force AJAX into MC's visual identity.
Research alternatives and references before design implementation.
Analytics and data depth are not secondary; they are core value.
```

---

# 12. Final Product Summary

AJAX Tracker should be a dark-mode, separate-design trading dashboard hosted inside Mission Control at `/ajax`. Its job is to preserve and improve Pop's SPX options workflow by turning screenshot-based pre-trade analysis into structured approvals, trade records, portfolio tracking, analytics, calendar, and journal. v2 supersedes v1 as the product direction, but v1 is preserved as correction history because Pop's feedback clarified the real constraints: read-only only, no execution, local/free/open-source bias, no stop-loss notifications in MVP, separate design system, and much stronger analytics/data depth.
