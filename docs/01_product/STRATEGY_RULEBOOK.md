# STRATEGY RULEBOOK — Pop's SPX Premium-Selling System

**Status:** CANONICAL — single source of truth for trade validation (feeds PRD F9)
**Consolidated from:** legacy strategy docs v1 (May 2026) + v2 (Jun 2026), now absorbed here
**Rule of the rulebook:** if a live trade and this document disagree, that's a decision for Pop — never silently resolved.

---

## 1. Philosophy (unchanged across versions)

Systematic premium selling on SPX. Edge = probability + theta + risk control + consistency — **not prediction**. Many small wins, occasional controlled losses. Survival depends entirely on sizing and stops.

## 2. Machine-readable parameters (what the F9 validator enforces)

| # | Parameter | Rule | Typical |
|---|---|---|---|
| R1 | Underlying | SPX / SPXW only | — |
| R2 | Structure | Bull put credit spread | — |
| R3 | DTE | 7–14 | 10–12 |
| R4 | Short-leg delta | 0.10–0.15 | 0.12–0.14 |
| R5 | Spread width | 10 pts preferred; 15 occasional | 10 |
| R6 | Distance from spot | 4–6% OTM (3–4% aggressive · 6%+ conservative) | 4–6% |
| R7 | Credit target | $0.80–1.00 on 10-wide · $1.20–1.80 in high IV | ~$1.00 |
| R8 | Profit taking | Close at 50–70% of max profit | 65–70% |
| R9 | Stop loss | 200–250% of credit received — **hard** | — |
| R10 | Position sizing | Max loss vs portfolio; flagged historically weakest discipline | — |

## 3. Entry conditions

**Enter when:** market stabilizes after weakness · VIX elevated but not panic · SPX above major support · no imminent macro event.
**Avoid:** chasing green rallies · low-VIX complacency · violent breakdowns.

## 4. VIX framework

| Regime | Behavior |
|---|---|
| VIX ~14–16 | Smaller size, further OTM, conservative (compressed premium, expansion risk) |
| VIX ~20–30 | Better premium and edge — sizing discipline still absolute |

## 5. Known psychological failure cycle (self-documented)

Winning streak → size up → ignore stop → one large loss → revenge trading. The system works only while rules stay mechanical.

## 6. ⚠️ OPEN QUESTIONS for Pop (found by running the rulebook against live trades)

| # | Conflict | Evidence | Pop's ruling |
|---|---|---|---|
| Q1 | **20-point widths in live use** vs R5 (10 preferred / 15 occasional) | Jul 17 SPX 7360/7340 spread is 20-wide | ☐ update rule · ☐ drift |
| Q2 | **Broken-wing butterflies traded live** but absent from this rulebook | Jul 22 + Jul 29 + Aug 3 SPXW BWBs | ☐ add BWB rule section · ☐ experimental, no rules yet |
| Q3 | Historic trades violated delta cap (0.47 vs 0.15 max, Jun 10) | Legacy export, recorded violations | ☐ acknowledged, rules stand |

Until ruled, the F9 validator flags these as violations — by design, never silently.

---

**APPROVAL:** ☐ Approved by Pop (including §6 rulings) · date: ________
