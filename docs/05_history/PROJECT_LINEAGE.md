# PROJECT LINEAGE — how 14 months of attempts became this project

**Purpose:** provenance record. Every rule, schema, and feature in the current docs traces to one of these sources. The original folders were deleted after absorption (2026-07-16); this file is what remains, by design.

---

## The four ancestors

| # | Project | Period | What it was | Fate |
|---|---|---|---|---|
| 1 | **Ajax Tracker** | May 2026 | PDR docs: screenshot → validate → approve → track → journal. Named the core problem: *"data lost after every trade"* | Absorbed → PRD F9 |
| 2 | **options-dashboard** | Jun 2026 | Working MVP: Apple Vision OCR + rule engine + PocketBase. Stalled under infrastructure weight | Logic absorbed → STRATEGY_RULEBOOK + TDD validation; trade exports → `history/backfill/` |
| 3 | **wealth-dashboard** | Jun 2026 | Lovable scaffold for personal finance | Nothing worth keeping — deleted whole |
| 4 | **This project** | Jul 2026 | Full spec-first rebuild on Cowork + Robinhood connector + Drive archive | Active |

## What was absorbed, exactly

| Asset | From | Now lives in |
|---|---|---|
| SPX strategy rules (v1+v2 merged) | Ajax + options-dashboard | `docs/01_product/STRATEGY_RULEBOOK.md` |
| Rule engine validation logic | `ruleEngine.ts` | TDD §5.1 (spec) — ported & smoke-tested 2026-07-16 against real trades: faithful (reproduced recorded violations exactly) |
| 24-column trade journal schema | `options-trades-master.csv` | DATA_SPEC ledger schema (fields: VIX at entry, trend, reason, % portfolio, time of entry) |
| Real trade exports (Jun 2026) | options-dashboard | `history/backfill/` — seed/backfill data |
| Product problem statement | Ajax PDR | PRD §2 |

## The lesson all three deaths teach (institutionalized in PRD §8)

Every attempt died building **infrastructure before value**: OCR servers, Swift compiles, local databases, UI scaffolds. The current architecture has no infrastructure to build — screenshots are read natively, the broker connection replaces parsing, Drive replaces the database, the artifact replaces the app shell. Only product remains.