# Options Dashboard — Fix Roadmap

**Created:** 2026-06-07 19:47 EDT  
**Owner:** APOLLO 🚀  
**Status:** ROADMAP  
**Sources:** Repo audit (PYROS), Product brief (HAL), Pop context  
**Repo path:** `/Users/cor/.openclaw/workspace/projects/03_Investing/04_Options/01_options-dashboard`

---

## 1. Executive Summary

The Options Dashboard repo is **functional but incomplete** for Pop's primary workflow: SPX bull put credit spread tracking via screenshot import.

### What works ✅
- Dashboard with 9 KPI cards, equity curve, P&L distribution, trades by ticker
- Dataset page with table, filters, CSV export, add trade form
- Validator page with upload → OCR → validation → approve/draft/reject
- Rule engine (DTE, delta, spread width, position size, VIX, trend)
- Supabase backend with real DB migrations, attachment storage
- Edge function for AI trade analysis (analyze-trade + openai gpt-4o-mini)
- shadcn/ui + TanStack Query + Recharts — good stack

### What's blocking Pop 🔴
1. **OCR is mock-only** — `performOCR()` returns hardcoded text based on filename. Cannot process real SPX screenshots.
2. **Trade ticket fields missing** — no debit/credit selection, limit price, TIF, market hours in the data model or UI.
3. **No trade ticket generation** — Validator ends at "Approve & Create Trade" but Pop needs a ticket preview/edit step before committing.
4. **SPX parsing not tested** — OCR parser optimized for Robinhood equity options, not SPX/SPXW index option chains.
5. **Duplicate type systems** — `Trade` (camelCase) vs `DbTrade` (snake_case) causes import confusion and friction.
6. **30 lint errors, 0 tests, 17 npm vulnerabilities** — technical debt that will slow down every change.

### Strategic recommendation
Fix the repo foundation first (Phase 0-1), then build the SPX intake pipeline (Phase 2-3), then the ticket/tracker layer (Phase 4-5). Do not attempt broker integration until the core screenshot → validation → registration flow works end-to-end with Pop's actual screenshots.

---

## 2. Product North Star

Options Dashboard = Pop's personal SPX options workflow command center.

```
[Upload Screenshot] → [OCR Parse SPX Chain] → [Validate vs Rules]
    → [Generate Trade Ticket] → [Approve/Edit] → [Register Trade]
    → [Track Open/Closed] → [Analytics & Review]
```

AJAX = the validation and reasoning layer. Not the UI.

### Core user story (Pop)
1. Take screenshot of SPXW option chain / order ticket from broker app
2. Upload to dashboard → OCR extracts: ticker, expiry, strikes, bid/ask, IV, OI, volume, delta
3. Dashboard validates against SPX bull put credit spread strategy rules
4. Pop reviews extracted data, edits if needed, selects debit/credit direction
5. Dashboard generates a structured trade ticket with limit price, TIF, quantity
6. Pop approves → trade registered in tracker with legs, screenshot attached
7. Dashboard shows position in portfolio analytics, P&L tracking, rule compliance

---

## 3. Current State From Audit

| Dimension | Status | Verdict |
|---|---|---|
| Build | ✅ Pass | Vite 5 + React 18, 2.41s build |
| Lint | 🔴 20 errors, 10 warnings | Fixable, mostly regex escapes and `any` types |
| Tests | ❌ None | Zero test infrastructure |
| OCR | 🔴 Mock only | `performOCR()` returns hardcoded demo text |
| Type system | 🔴 Two competing types | `Trade` (trade.ts) vs `DbTrade` (database.ts) |
| Data model | 🔶 Leg table exists but unused | `option_legs` in DB, flat `Trade` in UI |
| CSS | 🔶 Build warnings | `@import` ordering, 1 MB+ main chunk |
| npm | 🔶 17 vulnerabilities (9 high) | `npm audit fix` recommended |
| Backend | ✅ Supabase with migrations | Real DB, working edge function |
| AI analysis | ✅ Edge function exists | `analyze-trade` + gpt-4o-mini |
| Broker integration | ❌ Not wired | Tradier identified, no code |
| Trade ticket generation | ❌ Missing | Validator → direct create, no ticket step |
| SPX-specific parsing | ❌ Not implemented | Robinhood-centric OCR patterns |

---

## 4. Keep / Fix / Remove / Defer Matrix

### ✅ Keep (don't touch, these work)
- **Dashboard page** (Index.tsx) — 9 KPI cards, equity curve, P&L distribution, trades by ticker, PLR by ticker, recent trades table
- **Recharts** — charting library works fine, no need to replace
- **shadcn/ui + Radix** — component system is standard and maintainable
- **TanStack React Query** — state management and caching are solid
- **Tailwind CSS** — styling approach is correct
- **Supabase backend + migrations** — real DB with working queries
- **Rule engine** (ruleEngine.ts) — DTE, delta, spread width, position size, VIX, trend checks
- **AI edge function** (analyze-trade) — working, useful as advisory layer
- **CSV export** (csvExport.ts) — functional
- **AppLayout** component — standard navigation shell
- **`mockTrades.ts`** — keep as development fallback until real data flow is verified

### 🔶 Fix (needs repair or upgrade)
- **`performOCR()`** → Replace mock with real OCR (Tesseract.js or Vision API)
- **`parseOCRText()`** → Add SPX/SPXW format support, debit/credit fields, limit price, TIF, order type
- **`TradeCandidate` type** → Add `debit_or_credit`, `limit_price`, `time_in_force`, `market_hours`, `order_side`, `order_type`
- **Duplicate utilities** → Consolidate `tradeUtils.ts` and `tradeAnalytics.ts` into one source of truth
- **Duplicate type systems** → Align on Supabase-generated types, deprecate `types/trade.ts`
- **Validator.tsx** → Refactor to add trade ticket preview/edit step before approve
- **Lint errors (20)** → Fix regex escapes, `any` types, missing deps, empty interfaces
- **package.json name** → `vite_react_shadcn_ts` → `options-dashboard`
- **README** → Replace Lovable template with real project docs
- **CSS ordering** → Move `@import` font statements above `@tailwind` directives
- **`.env`** → Create `.env.example` without secrets
- **`bun.lockb`** → Remove, keep only `package-lock.json`
- **npm vulnerabilities** → Run `npm audit fix`

### 🔴 Remove (actively harmful or useless)
- **`lib/tradeUtils.ts`** → Once consolidated, remove this file entirely (all functions duplicated in `tradeAnalytics.ts`)
- **`types/trade.ts`** → Once consolidated, remove this file (all types superseded by database.ts + Supabase generated types)
- **`lovable-tagger` devDependency** → Lovable artifact, no purpose post-export
- **Lovable OG image references in index.html** → Brand identity pollution
- **`@typescript-eslint/no-unused-vars: off` in eslint config** → Hides dead code

### ⏸ Defer (important but not blocking MVP)
- **Tradier broker integration** — Wait until core screenshot → validation → registration flow works
- **Robinhood observation** — Only if Pop wants portfolio-level view; not blocking
- **Trade leg-native UI** — `option_legs` table exists, but flat model works for MVP. Convert when multi-leg analysis is needed.
- **Code splitting / lazy routes** — Only 3 routes; revisit when more pages are added
- **Test infrastructure** — Important but not blocking MVP flow. Add Vitest when features stabilize.
- **Authentication changes** — Supabase anon key + RLS works; don't change yet
- **Greeks sourcing** — Open question in product brief; not blocking initial SPX intake
- **Portfolio analytics (beyond P&L)** — Brief mentions it, not blocking MVP
- **Calendar/journal UI** — Notes field exists, dedicated journal can wait
- **Supabase schema migrations** — Current schema is stable; avoid schema changes until Phase 4

---

## 5. Phase 0 — Stabilize Repo

**Goal:** Get the repo clean, buildable, and maintainable before adding features.

| Task | Est. effort | Status | Blockers |
|---|---|---|---|
| P0-1: Normalize `package.json` name/version | 5 min | 🔴 Not started | None |
| P0-2: Rewrite README | 30 min | 🔴 Not started | None |
| P0-3: Clean up `index.html` metadata | 5 min | 🔴 Not started | None |
| P0-4: Create `.env.example` | 5 min | 🔴 Not started | None |
| P0-5: Run `npm audit fix` (17 vulnerabilities) | 5 min | 🔴 Not started | None |
| P0-6: Remove `bun.lockb`, `lovable-tagger` | 2 min | 🔴 Not started | None |
| P0-7: Fix CSS `@import` ordering | 5 min | 🔴 Not started | None |
| P0-8: Fix 20 lint errors | 1-2 hr | 🔴 Not started | None |
| P0-9: Enable `no-unused-vars` lint rule, fix resulting issues | 30 min | 🔴 Not started | P0-8 |

**Total Phase 0:** ~3-4 hours. Safe to automate. PYROS can execute without design decisions.

---

## 6. Phase 1 — Normalize Product Identity

**Goal:** Remove all Lovable birthmarks, align codebase with Options Dashboard brand.

| Task | Est. effort | Status | Blockers |
|---|---|---|---|
| P1-1: Consolidate `tradeUtils.ts` into `tradeAnalytics.ts`, remove `tradeUtils.ts` | 1-2 hr | 🔴 Not started | None (verify all imports) |
| P1-2: Deprecate `types/trade.ts`, align all components on Supabase-generated types | 1-2 hr | 🔴 Not started | P1-1 (uses `Trade` from hooks) |
| P1-3: Update Validator to import from single source | 30 min | 🔴 Not started | P1-1, P1-2 |
| P1-4: Update Dashboard (Index) imports to single source | 30 min | 🔴 Not started | P1-1 |
| P1-5: Update Dataset imports to single source | 30 min | 🔴 Not started | P1-1 |
| P1-6: Validate build passes cleanly after consolidation | 5 min | 🔴 Not started | P1-1 through P1-5 |

**Total Phase 1:** ~4-6 hours. Requires careful import tracing. PYROS should verify no broken references.

---

## 7. Phase 2 — Screenshot/OCR Intake for SPX Chain

**Goal:** Pop uploads a real SPX option chain/ticket screenshot and gets structured data back.

### What Pop's screenshots look like
```
Dark screen, SPX options chain
Expiration: 11D Thu Jun 18 (or similar)
Columns: Strike, IV, Delta, Bid, Ask, OI, Volume
Side panel: SPXW Put Credit Spread
  Leg 1: Buy to open 6/18 7,020 Put
  Leg 2: Sell to open 6/18 7,030 Put
  Quantity: 5
  Price direction: ERROR (missing debit/credit selection)
  Limit price: [empty]
  TIF: Good for day
  Market hours
```

### What needs to be extracted
1. **Header**: Ticker (SPX/SPXW), expiration, strategy type
2. **Leg details**: Side (Buy/Sell), action (Open/Close), strike, put/call, quantity per leg
3. **Pricing**: Bid, Ask, IV per strike (from chain), credit/debit (from ticket)
4. **Order params**: Price direction (debit/credit), limit price, TIF, market hours
5. **Chain context**: DTE, deltas, OI, volume

### Implementation

| Task | Est. effort | Status | Blockers |
|---|---|---|---|
| P2-1: Evaluate OCR approach — Tesseract.js (client) vs Google Vision (server) vs Supabase Edge Function + GPT-4o Vision | 1 hr | 🔴 Not started | Decision needed from Pop |
| P2-2: Extend `TradeCandidate` type — add `debit_or_credit`, `limit_price`, `time_in_force`, `market_hours`, `order_side` (buy/sell), `order_action` (open/close), `legs[]` support | 1 hr | 🔴 Not started | P2-1 |
| P2-3: Add SPX/SPXW-specific parsing patterns to `parseOCRText()` — index options, 4-digit strikes (e.g., 7020), expiry format "11D Thu Jun 18" | 2-4 hr | 🔴 Not started | P2-2 |
| P2-4: Implement real OCR in `performOCR()` using chosen approach | 2-4 hr | 🔴 Not started | P2-1 |
| P2-5: Build format-adaptive OCR router — detect broker type from screenshot layout (Robinhood, TOS, Schwab, etc.) | 2-3 hr | 🔴 Not started | P2-3, P2-4 |
| P2-6: Add confidence indicators per extracted field (not just overall %), highlight low-confidence fields in UI | 1-2 hr | 🔴 Not started | P2-3, P2-4 |
| P2-7: Test with Pop's actual SPX screenshots, iterate on parsing accuracy | 2-4 hr | 🔴 Not started | P2-1 through P2-6 |

**Total Phase 2:** ~11-19 hours. Highest risk phase — OCR accuracy is the critical path.

### ⚠️ Open decisions needed from Pop
- **Client-side OCR (Tesseract.js)** — Free, private, slower, less accurate on financial screenshots. Good for MVP.
- **Server-side Vision API (Google Cloud Vision)** — Faster, more accurate, costs pennies per scan, requires API key. Better for production.
- **GPT-4o Vision via Supabase Edge Function** — Most accurate for complex layouts, $0.01-0.03 per image. Leverages existing OpenAI infra. Best for complex SPX screenshots.

**APOLLO recommendation:** Start with **GPT-4o Vision** via the existing `analyze-trade` Edge Function (rename to `vision-process` or add a new `ocr-vision` function). It will give the best results on Pop's specific screenshot format, uses infrastructure already in place, and can return structured JSON directly without regex parsing.

---

## 8. Phase 3 — SPX Strategy Validation Engine

**Goal:** Validate extracted SPX trade against Pop's bull put credit spread rules.

### Current rule engine checks (already exists)
- DTE range
- Delta short leg range
- Spread width match
- Position size % of portfolio
- VIX limit
- Trend condition

### What needs to be added for SPX bull put credit spread

| Task | Est. effort | Status | Blockers |
|---|---|---|---|
| P3-1: Add SPX-specific rule checks — SPX/SPXW expiration rules (monthly vs weekly), SPAN margin calcs | 1-2 hr | 🔴 Not started | P2-3 |
| P3-2: Add rules for multi-leg consistency — verify legs form a valid spread (same expiry, different strikes, same underlying) | 1-2 hr | 🔴 Not started | P2-2 (legs support) |
| P3-3: Add credit/debit direction validation — warn if credit spread has debit pricing or vice versa (Pop's screenshot shows this error) | 1 hr | 🔴 Not started | P2-2 |
| P3-4: Add max loss / max profit calculation for multi-leg spreads | 1 hr | 🔴 Not started | None |
| P3-5: Add breakeven calculation specific to put credit spreads | 30 min | 🔴 Not started | None |
| P3-6: VIX/Trend context for SPX — add SPX-specific VIX thresholds, trend validation | 1 hr | 🔴 Not started | None |
| P3-7: Add position sizing rules based on account buying power (Tradier minimum margin for SPX spreads) | 1 hr | 🔴 Not started | Decision on broker |

**Total Phase 3:** ~5-8 hours. Lower risk than Phase 2 — most of the engine exists.

---

## 9. Phase 4 — Trade Tracker Data Model

**Goal:** When Pop approves a trade, it registers correctly with leg structure and all ticket fields.

### Current state
- DB has `option_legs` table but frontend creates flat trades
- `DbTrade` has legacy flat-strike fields (`short_strike`, `long_strike`)
- `DbOptionLeg` has proper structure but is not populated by the UI

### What needs to change

| Task | Est. effort | Status | Blockers |
|---|---|---|---|
| P4-1: When creating trade from Validator, populate `option_legs` table with extracted leg data | 1-2 hr | 🔴 Not started | P2-2, P3-2 |
| P4-2: Add trade ticket preview step between validation and approval — show extracted legs, pricing, calculated max loss/profit, breakeven, ROC | 2-4 hr | 🔴 Not started | P2-3, P4-1 |
| P4-3: Add screenshot attachment auto-link to trade on approve | 30 min | 🔴 Not started | None (pattern exists) |
| P4-4: Add entry price direction selection (debit/credit) — this fixes Pop's "price direction error" issue | 1 hr | 🔴 Not started | P2-2 |
| P4-5: Add limit price, TIF, market hours to trade creation flow | 1 hr | 🔴 Not started | P2-2 |
| P4-6: Add `strategy_evaluations` table and write approval record (rule pass/fail, score, violations, user decision) | 1-2 hr | 🔴 Not started | Schema change needs HAL approval |

**Total Phase 4:** ~7-11 hours. Heaviest UI work. Blocks the core "screenshot → registered trade" pipeline.

---

## 10. Phase 5 — Dashboard Analytics

**Goal:** Dashboard reflects SPX trades with meaningful KPIs for Pop's strategy.

### What exists
- 9 KPI cards, equity curve, P&L distribution, trades by ticker, PLR by ticker, recent trades
- Rule compliance percentage

### What's missing for SPX focus

| Task | Est. effort | Status | Blockers |
|---|---|---|---|
| P5-1: Add SPX-specific KPIs — credit collected this month, average ROC, win rate by DTE bucket | 1-2 hr | 🔴 Not started | Trades in DB |
| P5-2: Add open position dashboard view — active spreads with current P&L, DTE remaining, distance from strikes | 2-4 hr | 🔴 Not started | P4-1 (legs populated) |
| P5-3: Add strategy performance breakdown — by DTE range, delta, spread width, VIX at entry | 2-3 hr | 🔴 Not started | P4-1 |
| P5-4: Add rule compliance trend over time | 1 hr | 🔴 Not started | P4-6 (strategy_evaluations) |
| P5-5: Add attachment viewer in trade detail — see original screenshot alongside P&L | 1-2 hr | 🔴 Not started | P4-3 |

**Total Phase 5:** ~7-12 hours. Iterative — can be built from real trade data as it accumulates.

---

## 11. Phase 6 — Broker/Data Integration Readiness

**Goal:** Lay groundwork for Tradier integration without executing trades.

| Task | Est. effort | Status | Blockers |
|---|---|---|---|
| P6-1: Create `broker_sync_runs` table schema and migrations | 30 min | 🔴 Not started | Schema change needs HAL |
| P6-2: Create `market_snapshots` table (store SPX price, VIX at trade time) | 30 min | 🔴 Not started | Schema change needs HAL |
| P6-3: Add Tradier sandbox API client (read-only) — fetch option chain, market data | 2-4 hr | 🔴 Not started | Tradier sandbox account |
| P6-4: Add "Sync with Tradier" button in Dataset page — compare registered trades with broker positions (read-only) | 2-3 hr | 🔴 Not started | P6-3 |
| P6-5: Add manual price refresh — fetch current SPX/VIX for open trades | 1-2 hr | 🔴 Not started | P6-2, P6-3 |

**Total Phase 6:** ~6-10 hours. Not needed for MVP but valuable for position tracking.

---

## 12. Phase 7 — Security & Secrets Cleanup

**Goal:** Eliminate risk from exposed credentials and add best practices.

| Task | Est. effort | Status | Blockers |
|---|---|---|---|
| P7-1: Audit `.env` — verify no real Supabase keys are committed. Add `.env.example` | 30 min | 🔴 Not started | None |
| P7-2: Audit `app_settings` table for OpenAI key encryption | 1 hr | 🔴 Not started | None |
| P7-3: Add RLS policy review for trades table | 30 min | 🔴 Not started | None |
| P7-4: Create `.gitignore` verification — ensure `dist/`, `.env`, `node_modules/` not tracked | 5 min | 🔴 Not started | None |

**Total Phase 7:** ~2 hours. Not blocking but reduces risk.

---

## 13. Proposed PYROS Tickets

Tickets in priority order. Each maps to a specific deliverable in the phases above.

### P0 — Stabilize Repo (safe to queue immediately)

| Ticket | Description | Dependencies | Effort |
|---|---|---|---|
| `OPS-1` | Normalize `package.json` (name→`options-dashboard`, version→`0.1.0`), remove `lovable-tagger`, remove `bun.lockb` | None | 10 min |
| `OPS-2` | Rewrite README with real project docs, setup instructions, env docs, structure map | OPS-1 | 30 min |
| `OPS-3` | Clean `index.html` metadata — remove Lovable OG images, update author tags | None | 5 min |
| `OPS-4` | Create `.env.example` with documented Supabase vars (no real values) | None | 5 min |
| `OPS-5` | Fix CSS `@import` ordering in `index.css` | None | 5 min |
| `OPS-6` | Run `npm audit fix`, verify build | None | 10 min |
| `OPS-7` | Fix 20 lint errors (regex escapes, `any` types, empty interfaces, missing deps) | None | 2 hr |
| `OPS-8` | Enable `no-unused-vars` lint rule, fix resulting dead code | OPS-7 | 30 min |

### P1 — Normalize Codebase Identity

| Ticket | Description | Dependencies | Effort |
|---|---|---|---|
| `OPS-9` | Consolidate `tradeUtils.ts` into `tradeAnalytics.ts`, update all imports, remove `tradeUtils.ts` | OPS-8 | 2 hr |
| `OPS-10` | Deprecate `types/trade.ts`, align all components on Supabase-generated types from `hooks/useTrades.ts` | OPS-9 | 2 hr |

### P2 — SPX OCR Intake

| Ticket | Description | Dependencies | Effort |
|---|---|---|---|
| `SPX-1` | **Decision:** Choose OCR approach (recommend GPT-4o Vision via Edge Function) | Pop decision | — |
| `SPX-2` | Extend `TradeCandidate` type: debit/credit, limit_price, TIF, market_hours, order_side, order_action, legs array support | OPS-10 | 1 hr |
| `SPX-3` | Add SPX/SPXW parsing to `parseOCRText()` — 4-digit strikes, index option format, expiry parsing from "11D Thu Jun 18" | SPX-2 | 3 hr |
| `SPX-4` | Implement real OCR (Tesseract.js or GPT-4o Vision Edge Function) replacing mock `performOCR()` | SPX-1 | 4 hr |
| `SPX-5` | Add per-field confidence indicators in Validator UI | SPX-3, SPX-4 | 2 hr |
| `SPX-6` | Test with Pop's actual SPX screenshots, iterate on extraction accuracy | SPX-4 | 4 hr |

### P3 — SPX Validation Engine

| Ticket | Description | Dependencies | Effort |
|---|---|---|---|
| `SPX-7` | Add multi-leg spread validation rules (leg consistency, spread structure) | SPX-2 | 2 hr |
| `SPX-8` | Add debit/credit direction validation and max loss/profit calculations | SPX-2 | 2 hr |
| `SPX-9` | Add SPX-specific thresholds (VIX, DTE, delta) for bull put spread rules | None | 1 hr |

### P4 — Trade Tracker

| Ticket | Description | Dependencies | Effort |
|---|---|---|---|
| `TRK-1` | Populate `option_legs` table when creating trades from Validator | SPX-2, OPS-10 | 2 hr |
| `TRK-2` | Build trade ticket preview/edit step between validation and approval | SPX-3, SPX-7, SPX-8 | 4 hr |
| `TRK-3` | Add debit/credit selection, limit price, TIF, market hours to ticket UI | SPX-2 | 2 hr |
| `TRK-4` | Create `strategy_evaluations` table, write approval records | Schema approval | 2 hr |

### P5 — Analytics

| Ticket | Description | Dependencies | Effort |
|---|---|---|---|
| `ANL-1` | Add SPX-specific KPIs (credit/month, win rate by DTE, ROC) | Trades in DB | 2 hr |
| `ANL-2` | Build open position dashboard with current P&L and distance from strikes | TRK-1 | 4 hr |
| `ANL-3` | Add strategy performance breakdown (by DTE, delta, spread width, VIX) | TRK-1 | 3 hr |

---

## 14. Decisions Needed From Pop

These are **blockers** — something cannot proceed until Pop decides.

### 🔴 High Priority (blocking Phase 2+)

| # | Question | Context | Options |
|---|---|---|---|
| 1 | **OCR approach:** How should screenshots be processed? | Current mock returns hardcoded text. Need real OCR. | (a) **Tesseract.js** — free, client-side, ~5s per image, moderate accuracy. (b) **GPT-4o Vision via Edge Function** — ~$0.01-0.03/image, best accuracy for complex layouts, uses existing OpenAI infra. (c) **Google Cloud Vision** — ~$0.0015/image, good accuracy, requires new API key. |
| 2 | **Broker source:** Which broker are the SPX screenshots from? | OCR parser needs format-adaptive parsing. Different brokers = different layouts. | Robinhood? TOS (Thinkorswim)? Schwab? Tradier? Interactive Brokers? Other? |
| 3 | **SPX vs SPXW:** Which index options do you trade? | Affects expiry rules and parsing. SPX = monthly, SPXW = weekly. | SPX, SPXW, or both? |
| 4 | **Strategy rules confirmation:** What are your current SPX bull put credit spread parameters? | Rule engine exists but uses default values. Need Pop's actual parameters. | DTE range, delta range, spread width, max position size, VIX limit, allowed trend conditions. |

### 🔶 Medium Priority (blocking Phase 4+)

| # | Question | Context | Options |
|---|---|---|---|
| 5 | **Ticket workflow:** After validation, do you want a ticket preview/edit step before the trade is registered? | Current flow goes directly from validation → create trade. A ticket step adds friction but prevents errors. | (a) **Direct approve** (current) — faster but riskier. (b) **Ticket preview** — review, edit fields, then confirm. (c) **Two-step** — quick-approve bypasses ticket for experienced users. |
| 6 | **Portfolio size:** What's your approximate account size for position sizing? | Needed for position size % validation and margin calcs. | Dollar amount or rough range. |
| 7 | **Data source for current market data:** SPX price and VIX at trade time? | Currently needs manual entry. Can auto-fetch from CoinGecko MCP or Tradier. | (a) Manual entry. (b) CoinGecko MCP. (c) Tradier sandbox. (d) Yahoo Finance. |

### ⚪ Low Priority (nice to have)

| # | Question | Context |
|---|---|---|
| 8 | **Journal notes:** Do you want per-trade journal notes or a separate calendar context? | Notes field exists in schema. Dedicated journal UI is deferred. |
| 9 | **Export format:** CSV is current. PDF report needed? | CSV export exists. PDF is out of scope for MVP. |

---

## 15. What Not To Build Yet

**These are explicitly out of scope for the MVP fix roadmap.** If Pop asks about any of these, redirect to the product brief.

| Feature | Why Not |
|---|---|
| **Autonomous trading** | Brief says Phase 3, blocked by Tradier, approval workflow, risk gates. No execution without Pop approval. |
| **Stop-loss notifications** | Requires real-time data stream, broker integration. Post-MVP. |
| **Tax platform / tax lot matching** | Entirely different product. Brief explicitly says out of scope. |
| **Multi-user / authentication** | Single-user tool. Supabase RLS is sufficient. |
| **Custom auth system** | Supabase anon key + RLS works. Don't add auth complexity. |
| **Robinhood options execution** | Agentic account has no options tools enabled. Not suitable. |
| **Full Tradier execution** | Only read-only sandbox in Phase 2. Live execution blocked until all risk gates are met. |
| **Replace Recharts** | Charts work fine. Don't refactor working visualization. |
| **Code splitting** | Only 3 routes. Not worth the complexity yet. |
| **Desktop app / Electron** | Vite dev server + browser is the right distribution for MVP. |
| **Mobile app** | Desktop-first tool for trade analysis. No mobile requirement. |
| **Real-time price streaming** | Requires WebSocket infra. Manual refresh is fine for MVP. |
| **Multiple strategy support** | SPX bull put credit spread is the first strategy. Extend later. |
| **Dark/light theme polish** | Theme system exists (next-themes). Don't invest in theme tuning. |

---

*Roadmap produced by APOLLO 🚀 | Based on PYROS repo audit + HAL product brief + Pop context*
*Next step: Pop reviews decisions in Section 14, then PYROS starts Phase 0 tickets.*
