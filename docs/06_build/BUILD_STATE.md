# BUILD STATE — resume protocol & milestone tracker

**Purpose:** token/session-outage insurance. Any new session resumes the build by reading THIS FILE FIRST — no context re-derivation, no repeated work, no lost progress.

## Resume protocol (for any future Claude session)

1. Read this file → find the first ⬜ milestone
2. Read only the docs that milestone lists (not everything)
3. Build it → test per TEST_PLAN IDs listed → commit → flip ⬜ to ✅ here → commit again
4. If a session dies mid-milestone: the last commit is always a working state; partial work is committed with prefix `WIP:` and noted below

## Rules of the build

- Every milestone fits in ONE session and ships something independently useful
- Code lives in `app/` as committed files — every client is generated from `app/dashboard.html`, never authored directly
- Commit after every milestone, no exceptions
- Golden numbers & tests: DATA_SPEC §6 + TEST_PLAN

## Milestones

| # | Milestone | Ships | Reads | Tests | Status |
|---|---|---|---|---|---|
| M1 | **Archive job** — weekly Friday task writing trades_ledger, positions_snapshots, accounts_history to `history/` | History starts accumulating | TDD §9, DATA_SPEC §4 | A1–A5 | ✅ 2026-07-17 |
| M2 | **Backfill** — import Pop's official Robinhood CSV into ledger | Complete history since May 2025 | DATA_SPEC §4.1, §6 | A6, R4 | ✅ 2026-07-17 |
| M3 | **Dashboard core** — `app/dashboard.html`: accounts strip + 10 stat cards + P/L chart | Daily-usable dashboard | PRD F1–F3, DESIGN §2–4 | R1–R3, D2, D6 | ✅ 2026-07-18 |
| M4 | **Structures table** — grouping, strategy badges, max loss, Δ/Θ, compliance chips | The flagship feature | TDD §4–6, RULEBOOK, DESIGN S3/S3b | S1–S7 | ✅ 2026-07-18 |
| M5 | **Closed trades + stocks sections** | Full v1 surface | PRD F5–F6 | R5, D4 | ✅ 2026-07-18 |
| M6 | **F9 validator** — screenshot → confirm → validate → journal | Pre-trade workflow | TDD §5.1, RULEBOOK §0.1 | V1–V4 | ✅ 2026-07-18 |
| M7 | **Bake** — two Fridays + failure drill | v1 done | TEST_PLAN §6 | bake gates | ⬜ |
| M8 | **Standalone web app (THE product)** — static SPA at repo root (`index.html`), reads history CSVs via fetch; F10 Reader with FIFO pairing + high-water-mark + cross-source dedupe; real account names (Options/Equity/Crypto) | Dashboard at a URL, any device, zero AI dependency | TDD §1 | P1–P6 | ✅ built 2026-07-18 · ⏳ Pop enables Pages (Settings→Pages→main/root) |
| M8.1 | **Platform shell** — sidebar app layout (nav rail: Overview/Options/Stocks/Crypto/Reader), page headers per section, uppercase category labels grouping cards (Accounts/Performance/Trends, Positions/Activity, etc.), brand block + net worth in sidebar. Same data/render functions, zero JS logic changes — pure structural/CSS pass. | Looks like a product, not a single-page dashboard | DESIGN_SPEC §2–4 | P1–P6 (rerun) | ✅ 2026-07-19 |
| M9 | **Collector independence** — local Python script + macOS cron replaces the Claude courier | Pipeline with zero AI dependency | TDD §1 comp.2 | A-tests rerun | ⬜ |

## Session log

| Date | Session did | Commits |
|---|---|---|
| 2026-07-16 | Spec phase closed: docs approved, rulebook v2 + tolerance model, HAL review applied, repo consolidated | 70be898…latest |
| 2026-07-17 | **M2 shipped:** backfill_enrich.py — 82/82 option rows enriched with strikes/strategy from official CSV (100%, A6 gate 95%), R4 HIMS +$577.90 exact, ±1-day settlement matching, official CSV archived in history/backfill/ | this session |
| 2026-07-17 | **M1 shipped:** archive_generate.py + archive_job.md, first snapshot (94 trades / 41 positions / 5 accounts), tests A1/A2/A5 passed, options ledger reconciled to broker exact ($12,337.24), Friday task scheduled (5:34 PM local). Notable: Jul 17 spread closed early +$570; three BWBs open (Jul 29, Aug 3, Aug 6); Jul 29 fly has pending closing order | this session |

| 2026-07-19 | **M8.1 shipped:** Pop viewed the live Pages URL and said it "looks like a dashboard, not a digital product" — flat page, top pill-tabs, no visual categories. Rebuilt shell: left sidebar nav (icons+labels), per-page headers, uppercase section labels (Performance/Positions/Holdings/etc.) grouping the same cards. No JS/data logic touched — same IDs, same functions, verified via node syntax check + required-ID scan before push. | 9ca1a7e |

## WIP notes

M8 notes: Reader P/L is net-of-fees (broker figures differ ~$1-2/trade — disclosed in UI); exercise/assignment closes flagged needs_review; compliance chips deferred on product (snapshots lack opened_at — add column at next courier run, then port chips); preview artifact stays until Pop confirms Pages URL works (test P1), then retire. Golden test: full-CSV pairing 179 closes, hwm guard returns 0 when current ✓.

M3 notes: stat cards adjusted vs PRD F2 for data honesty — 'avg time in trade' and 'avg % return/risk' deferred to M4 (need strike-memory pairing); replaced with YTD + this-month realized. In-page R1 reconciliation footer (per-trade sum vs broker aggregate) renders live.
