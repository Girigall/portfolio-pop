# TEST PLAN — Acceptance Criteria, Portfolio Dashboard v1

**Status:** DRAFT — awaiting Pop's approval
**Rule:** the build ships only when every P0 test passes. Golden numbers come from DATA_SPEC §6 (broker-verified in-session).

---

## 1. Reconciliation tests (the soul — PRD §7)

| ID | Test | Pass condition |
|---|---|---|
| R1 | All-time realized options P/L | Dashboard total = `get_realized_pnl` options-only `total_returns`, to the cent |
| R2 | Frozen golden number | Through 2026-07-10 the value is exactly **+$11,852.24** (later dates: recompute via R1) |
| R3 | Per-underlying breakdown | Σ per-underlying = R1 total (session reconciliation reproduced) |
| R4 | HIMS regression (the TradesViz bug) | HIMS lifetime realized shows **+$577.90** — NOT $4,920, NOT dated 2026 |
| R5 | Closed-trades footer checkmark | Appears only when table sum equals aggregate endpoint |

## 2. Structure grouping tests (the differentiator — PRD G2)

| ID | Test | Pass condition |
|---|---|---|
| S1 | BWB renders as one row | Jul 29 SPXW 7200/7250×2/7270 → single row, badge "BWB" |
| S2 | BWB net premium | Row shows +$425 net credit (2×$46.45 − $38.55 − $50.10, ×100) |
| S3 | **Max loss via payoff algorithm** | Jul 29 BWB max loss = **−$2,575** (payoff at S≤7200: −30 pts × 100 + 425). Explicitly NOT the −$2,075 a width-shortcut produced earlier — this test exists because of that error |
| S4 | PCS grouping | Any open put credit spread → one row, correct width/credit/max loss |
| S5 | The Premium Insights bug cannot reproduce | For every spread: reported P/L accounts for ALL legs (long legs included) |
| S6 | Unknown structures degrade safely | Unrecognized combo → "Custom (N legs)", all legs listed, math still payoff-derived |
| S7 | Missing marks | Any leg without a quote → structure P/L = "n/a", never a partial sum |

## 3. Archive tests (Pop's #1 requirement: history never shrinks)

| ID | Test | Pass condition |
|---|---|---|
| A1 | Append-only ledger | Run job twice consecutively → row count identical (dedupe) then grows only with new trades |
| A2 | **Monotonic row counts** | Every run: new count ≥ old count for all 3 CSVs; violation = hard failure alert |
| A3 | Strike memory | A structure open in week N, closed in week N+1 → ledger row carries strategy/strikes/expiry |
| A4 | Provenance | Every row has `source` ∈ {connector, csv_backfill} |
| A5 | Partial-failure discipline | Simulated tool failure → affected file unchanged, `_meta.json` logs it, dashboard banners it |
| A6 | **Backfill coverage gate** (HAL #4) | Ledger rows from backfill ≥ 95% of trade rows in Pop's official Robinhood CSV; gap list produced for the remainder — no silent omissions |

## 3b. Validator tests (F9)

| ID | Test | Pass condition |
|---|---|---|
| V1 | Regression vs legacy engine | Jun 10 legacy trade (SPXW 7290/7280, DTE 6, Δ0.47, credit $3.80) → REJECTED with the same 2+ violations the old export recorded |
| V2 | Rulebook conflict surfacing | A 20-wide spread → width violation cited until Pop rules on RULEBOOK §6 Q1 |
| V3 | Journal capture | Confirmed candidate lands in ledger with `source=validator`, thesis, VIX |
| V4 | Framing guardrail | Output contains verdict + violations only — never "you should take this trade" |

## 4. Dashboard behavior tests

| ID | Test | Pass condition |
|---|---|---|
| D1 | Fresh open reflects live data | New trade closed today appears without manual steps |
| D2 | Accounts strip | 5 accounts, masked numbers, net worth = Σ account totals to the cent |
| D3 | Range pills persist | Choice survives close/reopen (localStorage) |
| D4 | Classification toggle | Options/Stocks filter present; unclassified rows visible under "All", flagged |
| D5 | Stale quote labeling | Quotes older than session-fresh render with "as of <time>" |
| D6 | Loading skeletons | Every section shows skeleton before data; no blank white flashes |
| D7 | Single-section failure isolation | Kill one tool → that section banners, all others render |

## 5. Design conformance (spot checks vs DESIGN_SPEC)

- ≥8 stat cards above the fold at 1280px · label/value hierarchy per spec
- Negative currency red with leading minus; percent 1 decimal
- Badges carry text (not color-only) · contrast pairs pass 4.5:1
- Formula tooltip present on every stat card

## 6. Two-week bake (post-launch gate)

1. Friday job runs twice unattended → A1/A2 verified both times
2. One mid-week manual dashboard open → D1 verified against Robinhood app by Pop
3. **Failure drill (HAL #5):** one simulated Friday with the Robinhood connector unreachable → archive files unchanged · `_meta.json` logs the failure · dashboard banners it on next open · zero partial writes
4. Pop signs the bake-complete line below; only then is v1 "done"

## 7. M8 product tests (the standalone web app)

| ID | Test | Pass condition |
|---|---|---|
| P1 | URL loads anywhere | Dashboard renders on desktop browser + phone with Claude fully closed |
| P2 | Historical completeness from files alone | With no courier for 2+ weeks, all historical sections still render fully from master CSVs |
| P3 | As-of honesty | Every live-ish section shows its data date; nothing silently stale |
| P4 | F10 Reader idempotency | Import the same broker CSV twice → second import appends 0 rows |
| P5 | F10 Reader correctness | Import a fresh weekly CSV → new trades appear with strikes/strategy; totals still reconcile to broker aggregate on next courier check |
| P6 | Preview retirement | In-app artifact removed/marked deprecated once P1–P5 pass |

---

**APPROVALS**
☐ Test plan approved (pre-build) — Pop · date: 16-7-2026
☐ All P0 tests passed (pre-ship) — date: 16-7-2026
☐ Two-week bake complete — Pop · date: 16-7-2026
