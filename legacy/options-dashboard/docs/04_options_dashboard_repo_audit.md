# Options Dashboard — Technical Repo Audit

**Created:** 2026-06-07 19:15 EDT  
**Owner:** PYROS  
**Status:** READ-ONLY AUDIT

---

## Executive Summary

This is a **functional but un-REBRANDED Lovable-exported repo**. The codebase is surprisingly well-structured for a Lovable export — it has a real Supabase backend with migrations, a component library (shadcn/ui), three working pages (Dashboard, Dataset, Validator), and a working build pipeline.

However, it retains its **Lovable birthmarks** in critical metadata files (package.json name, README, OG tags), has **duplicate utility code** across `lib/tradeUtils.ts` and `lib/tradeAnalytics.ts`, a **mock-only OCR implementation**, and **30 lint errors/warnings**. The build succeeds but has CSS ordering warnings and a large main chunk (1 MB+).

**Overall verdict:** The repo is further along than expected from a typical Lovable product. It needs normalization (Phase 1) before major feature work begins, but it's buildable and usable right now.

---

## Repository Facts

| Item | Value |
|---|---|
| **package.json name** | `vite_react_shadcn_ts` (Lovable default ❌) |
| **package.json version** | `0.0.0` |
| **Framework** | Vite 5 + React 18 + TypeScript 5.8 |
| **UI Library** | shadcn/ui (Radix primitives) |
| **Styling** | Tailwind CSS 3.4 + `tailwindcss-animate` |
| **Routing** | React Router DOM 6 |
| **State/Data** | TanStack React Query 5 |
| **Charts** | Recharts 2.15 |
| **Backend** | Supabase (JS client v2) + Edge Functions (Deno) |
| **Edge Function** | `analyze-trade` (OpenAI gpt-4o-mini) |
| **Package manager** | npm (with bun.lockb also present) |
| **Git commits** | 10+ commits, migration to Supabase visible |
| **Node version target** | Not specified, v22 works |

✅ Framework: **Vite + React + TypeScript + shadcn/ui + Tailwind** — matches product brief.  
✅ Supabase backend with real migrations.  
✅ Edge function for AI analysis exists.

---

## Verification Commands Run

### `npm ci` (clean install)

| Step | Result |
|---|---|
| `npm ci` | ✅ **Success** — 392 packages in 4s |
| Vulnerabilities | 🔶 **17 vulnerabilities** (8 moderate, 9 high) — `npm audit fix` recommended |

### `npm run build`

| Step | Result |
|---|---|
| Build | ✅ **Success** — 2.41s |
| CSS warnings | 🔶 `@import must precede all other statements` — 7 warnings, font imports placed after Tailwind directives |
| Chunk size | 🔶 Main JS chunk **1,056 kB** (gzip: 299 kB) — exceeds 500 kB recommendation |
| Output | `dist/` created with `index.html`, CSS (63 kB), JS (1 MB) |

### `npm run lint`

| Result | Count |
|---|---|
| ❌ **Errors** | 20 |
| ⚠️ **Warnings** | 10 |
| **Total** | 30 problems |

Common error patterns:
- 🔴 `no-useless-escape` — 12 occurrences in `ocrParser.ts`, `OCRUpload.tsx` (escaped `/` and `-` inside regex character classes)
- 🔴 `@typescript-eslint/no-explicit-any` — 3 occurrences in `AddTradeForm.tsx`, `OCRUpload.tsx`, `TradesTable.tsx`
- 🔴 `@typescript-eslint/no-empty-object-type` — 2 occurrences in `command.tsx`, `textarea.tsx` (shadcn boilerplate)
- 🔴 `@typescript-eslint/no-require-imports` — 1 occurrence in `tailwind.config.ts`
- ⚠️ `react-hooks/exhaustive-deps` — 3 occurrences in `Validator.tsx` (missing `resetForm` dependency)
- ⚠️ `react-refresh/only-export-components` — 6 occurrences in shadcn UI files (known pattern, low impact)

### `npm run test`

❌ **No test script exists.** No test framework configured. No unit tests, integration tests, or E2E tests anywhere.

---

## Product Brief Alignment

### ✅ Already Exists

| Feature | Status | Evidence |
|---|---|---|
| Dashboard with KPIs | ✅ Done | `Index.tsx` — 9 KPI cards, equity curve, P&L distribution, trades by ticker, PLR by ticker, recent trades table |
| Trade dataset/management | ✅ Done | `Dataset.tsx` — trades table, filters, add trade form, CSV export, attachment tracking |
| Screenshot/OCR extraction | ✅ Done | `Validator.tsx` + `lib/ocrParser.ts` — upload, OCR parse, data editing, approve/save draft/reject |
| Strategy validation / rule engine | ✅ Done | `lib/ruleEngine.ts` — DTE, delta, spread width, position size, VIX, trend checks |
| Trade approval/denial with reasons | ✅ Done | Validator pass/warning/fail + violation list + approval workflow |
| Open/closed trade tracking | ✅ Done | Trade filters, status badges in Dataset |
| Analytics dashboard | ✅ Done | P&L, win rate, avg P&L, PLR, max drawdown, expectancy, rule compliance |
| CSV export | ✅ Done | `lib/csvExport.ts` + Dataset export button |
| Brokers/data readiness layer | 🔶 Partial | Tradier identified in brief but not wired; MCP CoinGecko exists |
| Supabase backend | ✅ Done | Real DB with migrations, storage for attachments |
| AI trade analysis | ✅ Done | Edge function `analyze-trade` + OpenAI gpt-4o-mini |

### 🔶 Partial / Needs Work

| Feature | Status | Notes |
|---|---|---|
| OCR is mock/placeholder | 🔶 Partial | `performOCR()` returns hardcoded text based on filename. Needs real OCR integration (Tesseract, Google Vision, etc.) |
| Trade data model vs leg-based model | 🔶 Partial | DB schema already has `option_legs` table, but frontend still uses flat `Trade` type. App not leveraging legs yet |
| Repo normalization | 🔶 Not done | package.json name, README, OG images still Lovable defaults |
| Broker integration | 🔶 Not wired | Tradier identified as target, no code exists |
| Journal notes | 🔶 Partial | `notes` field exists on Trade, no dedicated journal UI |
| Pre-trade analysis | 🔶 Partial | Validator handles it, but not in a dedicated pre-trade flow |

### ❌ Missing / Not Started

| Feature | Status |
|---|---|
| Trade ticket generation | ❌ Not implemented |
| Portfolio analytics (beyond P&L) | ❌ Not implemented — no portfolio-level metrics |
| Calendar/ journal context | ❌ Not implemented |
| Tradier sandbox integration | ❌ Not started — brief says Phase 2 |
| Manual trade entry (separate from Validator) | ❌ Dataset has AddTradeForm but limited |
| Greeks sourcing/calculation | ❌ Brief lists this as open question |
| Multi-leg position native UI | ❌ Trade legs table exists in DB but not used in UI |

---

## Technical Debt

### 🔴 High Priority

| # | Item | Location | Impact |
|---|---|---|---|
| 1 | **Duplicate utility functions** | `lib/tradeUtils.ts` and `lib/tradeAnalytics.ts` both export `getClosedTrades`, `getOpenTrades`, `calculateTotalPL`, `calculateWinRate`, `calculateAvgPL`, `calculateAvgPLR`, `calculateTotalMarginInUse`, `getEquityCurveData`, `getPLDistributionData`, `getTradesByTickerData`, `getPLRByTickerData`, `filterTrades`, `getUniqueTickers`, `getExitTypes` | Confusion, stale imports, maintenance burden |
| 2 | **Two type systems for Trade** | `types/trade.ts` (camelCase legacy) vs `types/database.ts` (snake_case DbTrade) + `hooks/useTrades.ts` (Supabase-generated) | Components import from different type files inconsistently; CSV export converts between them |
| 3 | **Mock-only OCR** | `lib/ocrParser.ts:performOCR()` | Can't process real screenshots; demo-only |
| 4 | **Lint errors (20)** | Various | Indicates code quality issues that will compound |
| 5 | **No test infrastructure** | Entire repo | Zero confidence in changes; manual testing only |
| 6 | **17 npm vulnerabilities** | package-lock.json | 9 high severity — `npm audit fix` needed |

### 🔶 Medium Priority

| # | Item | Impact |
|---|---|---|
| 7 | CSS `@import` ordering in `index.css` | Font imports after Tailwind directives cause build warnings; fix: move `@import` to top |
| 8 | Main JS bundle 1 MB+ | Performance concern; code-splitting via lazy routes recommended |
| 9 | `bun.lockb` alongside `package-lock.json` | Mixed package manager artifacts |
| 10 | Shadcn UI components with default Lovable theme | Some unused UI components could be pruned |
| 11 | Hardcoded Supabase keys in `.env` | Not version-controlled (.env is in gitignore), but no `.env.example` exists |
| 12 | `@typescript-eslint/no-unused-vars: off` in eslint config | Hides legitimate dead code |
| 13 | Regex escape issues in `ocrParser.ts` and `OCRUpload.tsx` | Unnecessary escapes `/` and `-` in regex character classes — works but noisy |

### ⚪ Low Priority

| # | Item |
|---|---|
| 14 | `tailwind.config.ts` file uses CommonJS `require()` instead of ESM import |
| 15 | `lovable-tagger` devDependency — can be removed post-Lovable |
| 16 | shadcn `components.json` references non-existent project |

---

## Risks

| Risk | Level | Description |
|---|---|---|
| **Supabase production data** | 🔴 High | `.env` contains real Supabase credentials. If a Supabase project is actively linked, running `npm run dev` points to real data. No test/prod separation. |
| **OpenAI API key exposure** | 🔴 High | API key stored in `app_settings` table (retrieved by edge function). No encryption at rest for the key. |
| **No E2E or unit tests** | 🔴 High | Any refactor or feature addition is blind. |
| **OCR as blocker for validator workflow** | 🔴 High | The core Validator flow depends on OCR. With mock-only OCR, the entire approval/validation workflow is non-functional with real screenshots. |
| **Duplicate type definitions diverging** | 🔶 Medium | `Trade` in `types/trade.ts` and `DbTrade` in `types/database.ts` could diverge when the DB schema changes. |
| **Large JS bundle** | 🔶 Medium | 1 MB+ main chunk for a dashboard with 3 views suggests missing code splitting. |
| **bun vs npm lockfile conflict** | ⚪ Low | `bun.lockb` present but `package-lock.json` used. Potential CI confusion. |

---

## Recommended Phase 1 Tickets

These tickets normalize the repo before feature work and are safe to implement (READ-ONLY analysis — not executing).

### P1-1: Normalize package.json metadata
- Change `name` to `"options-dashboard"`
- Set `version` to `"0.1.0"` (or `"1.0.0"`)
- Remove `lovable-tagger` from devDependencies

### P1-2: Rewrite README
Replace the Lovable template with:
- Project name and purpose
- Stack summary
- Setup instructions (`npm ci`, `npm run dev`)
- Environment variables documentation (without real keys)
- Project structure map
- Deployment notes

### P1-3: Fix metadata in index.html
- Remove Lovable OG image URLs
- Update author/twitter metadata for the project, not Lovable
- Keep title and description (they're already good)

### P1-4: Consolidate duplicate utilities
Choose one source of truth for analytics/utility functions:
- Keep `lib/tradeAnalytics.ts` (it imports from `ruleEngine` and is used by pages)
- Remove or redirect `lib/tradeUtils.ts` (currently imports from `types/trade.ts` which differs)
- Update all imports to use one module

### P1-5: Consolidated type system cleanup
- Align on one `Trade` type (favor the Supabase-generated one from `hooks/useTrades.ts`)
- Remove or deprecate `types/trade.ts` and its imports
- Remove `types/database.ts` (most content is superseded by Supabase-generated types)

### P1-6: Fix lint errors
- Fix unnecessary regex escapes in `ocrParser.ts` and `OCRUpload.tsx`
- Fix `any` types in `AddTradeForm.tsx`, `OCRUpload.tsx`, `TradesTable.tsx`
- Fix empty interfaces in shadcn files (`command.tsx`, `textarea.tsx`)
- Add `resetForm` to `useCallback` deps in `Validator.tsx` (or wrap with `useRef`)

### P1-7: Create `.env.example`
Document VITE_SUPABASE_* vars without real values.

### P1-8: CSS ordering fix
Move `@import` font statements above `@tailwind` directives in `index.css`.

### P1-9: Remove bun.lockb
Keep only `package-lock.json` for consistency.

### P1-10: Add test infrastructure (optional for Phase 1)
- Add Vitest as devDependency
- Add a basic smoke test

---

## Do Not Touch Yet

The following areas require coordination with product owner / brief before changes:

- ✅ **OCR real implementation** — Needs product decision: Tesseract.js (client) vs Google Vision/AWS Textract (server). Not a Phase 1 task.
- ❌ **Supabase schema changes** — Current migrations are stable. Any leg-based table changes need MUSE/HAL approval.
- ❌ **Tradier broker integration** — Blocked until Phase 2 in product brief.
- ❌ **Removing mockTrades.ts** — Mock data is the only way the dashboard works without real Supabase data. Keep until real data flow is verified.
- ❌ **Code splitting / routes** — Only 3 routes; revisit when more pages are added.
- ❌ **Authentication changes** — Supabase connection uses anon key with RLS. Don't change auth until brief specifies.
- ❌ **Migration from Recharts** — Charts work fine; don't replace unless product requires different visualization.

---

*Audit performed by PYROS | No code was edited, only analyzed.*
