# Options Dashboard — Product Brief

Created: 2026-06-07 18:59 EDT  
Updated: 2026-06-07 18:59 EDT  
Owner: HAL / Pop  
Status: Active product direction  
Project folder: `projects/03_Investing/04_Options/01_options-dashboard/00_project_docs`  
Repository: `Girigall/options-dashboard`  
Local code path: `/Users/cor/.openclaw/workspace/projects/03_Investing/04_Options/01_options-dashboard`  
Supersedes: `02_options_dashboard_product_brief_OLD.md`  

---

## What This Document Is

This is the updated product brief for **Options Dashboard**, continuing the earlier AJAX Tracker product work with the current HAL OS / AJAX architecture.

The previous document is preserved as:

```text
02_options_dashboard_product_brief_OLD.md
```

That old brief remains useful for product history, Pop feedback, and original scope decisions, but it is no longer the active implementation reference.

---

## Product Name

**Current product name:** Options Dashboard

**Previous names:**

```text
AJAX Tracker
Ajax Tracker
```

Naming decision:

```text
Options Dashboard = the user-facing product and interface.
AJAX = the financial intelligence agent / analysis engine behind the product.
```

Reason: the product should be understandable as a dashboard, while AJAX remains the internal agent responsible for reasoning, validation, ticketing, and strategy checks.

---

## Project Location

### Workspace

```text
/Users/cor/.openclaw/workspace/projects/03_Investing/04_Options/01_options-dashboard/00_project_docs
```

### Obsidian visible copy

```text
/Users/cor/Library/CloudStorage/GoogleDrive-helloivannu@gmail.com/My Drive/Obsidian/Obsidian Vault/openclaw/workspace/projects/03_Investing/04_Options/01_options-dashboard/00_project_docs
```

### Code repository

```text
/Users/cor/.openclaw/workspace/projects/03_Investing/04_Options/01_options-dashboard
```

### GitHub

```text
Girigall/options-dashboard
```

---

## Current Architecture Direction

The old brief assumed a NextJS route inside Mission Control:

```text
mc.ivan-nunez.com/ajax
```

That is now deprecated for this project.

The current implementation is a separate Lovable-exported / GitHub-backed React app:

```text
Vite + React + TypeScript + shadcn/ui + Tailwind CSS
```

Current repo evidence:

```text
package.json
src/pages/Validator.tsx
src/pages/Dataset.tsx
src/lib/ocrParser.ts
src/lib/ruleEngine.ts
src/lib/tradeAnalytics.ts
src/hooks/useTrades.ts
src/types/trade.ts
```

This confirms the repo already maps to the core product direction: screenshot/OCR parsing, rule validation, dataset/trade tracking, and analytics.

---

## Active Product Direction

Options Dashboard should become Pop's personal SPX options workflow dashboard.

Its purpose is to unify:

```text
pre-trade analysis
screenshot/OCR extraction
SPX strategy validation
trade ticket generation
open/closed trade tracking
portfolio analytics
calendar/journal context
broker/data integration
```

---

## Role of AJAX

AJAX is not the UI.

AJAX is the reasoning and validation layer behind the dashboard.

AJAX handles:

```text
strategy validation
risk framing
spread evaluation
ticket structuring
broker/data-source reasoning
human-in-the-loop execution checks
```

---

## MVP Boundary

The MVP remains conservative.

### In scope

```text
Screenshot upload or manual trade entry
OCR/structured extraction
SPX bull put credit spread validation
Approval/denial with reasons
Open and closed trade tracking
Analytics dashboard
CSV/export support
Journal notes
Broker/data-source readiness layer
```

### Out of scope for MVP

```text
autonomous live trading
stop-loss notifications
multi-user product behavior
custom authentication system
full tax platform
automated execution without Pop approval
```

---

## Broker Direction

The old brief assumed Robinhood read-only sync.

Current reality changed after the 2026-06-07 broker audit.

### Robinhood

```text
Status: Not suitable for SPX options execution right now.
Reason: Agentic account does not expose options tools and has no options level enabled.
```

### Tradier

```text
Status: Recommended broker target for SPX/SPXW options.
Reason: REST API, sandbox, SPX/SPXW support, multi-leg spreads, direct credit spread order structure.
```

Current broker direction:

```text
Tradier = primary candidate for options execution testing.
Robinhood = portfolio/account observation only if useful.
CoinGecko = crypto market data source already connected via MCP.
```

---

## Execution Phases

### ✅ Phase 1 — Analysis / Read-only

Options Dashboard supports analysis, validation, and tracking. No trades are executed.

### 🔶 Phase 2 — Sandbox Ticketing

AJAX creates structured tickets and validates them against strategy rules. PYROS may connect a Tradier sandbox wrapper.

### 🔴 Phase 3 — Live Execution

Blocked until all of the following are true:

```text
Tradier account ready
sandbox flow verified
multi-leg spread order confirmed
Pop approval workflow implemented
audit log implemented
risk gates implemented
```

No autonomous execution is allowed.

---

## Data Model Direction

The previous brief correctly identified that a single-table model is weak for options spreads.

Current preferred model:

```text
trades
trade_legs
strategy_evaluations
screenshots
broker_sync_runs
market_snapshots
journal_entries
accounts
```

Reason:

```text
SPX bull put credit spreads are multi-leg positions. A leg-based schema scales better and avoids brittle strike1/strike2 assumptions.
```

---

## Repo Normalization Needed

PYROS should normalize the Lovable-exported repo before major work.

Required updates:

```text
package.json name: options-dashboard
README: replace Lovable placeholder text with real project documentation
App title / metadata: Options Dashboard
local env example: document future API keys without secrets
project structure map: document pages, hooks, libs, types
```

---

## Open Questions

```text
Where screenshots are stored.
Whether OCR runs locally or through an AI vision tool.
How extracted trades map to confirmed executions.
Whether Tradier sandbox becomes the first broker integration.
Whether portfolio data comes from broker sync, manual entry, or both.
How Greeks are sourced or calculated.
How to separate analysis-only mode from execution-ready mode.
```

---

## Final Product Summary

Options Dashboard is the continuation of the AJAX Tracker concept under the current HAL OS architecture.

The product is now a standalone GitHub-backed React dashboard connected to the AJAX financial intelligence layer. Its first purpose is to support Pop's SPX bull put credit spread workflow through structured analysis, validation, tracking, and analytics. Execution remains blocked until Tradier or another broker is fully verified through sandbox, approval workflow, and audit controls.
