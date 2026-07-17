# STRATEGY RULEBOOK — Pop's Options Playbook (multi-strategy)

**Status:** CANONICAL v2 — rebuilt 2026-07-16 from Pop's full strategy library (`03_Investing/04_Options/`), replacing the single-strategy v1
**Consumed by:** F9 validator — each candidate trade is matched to its strategy first, then validated against THAT strategy's rules
**Source docs:** `STRA_SPX Strategy` · `STRAT_Put BWB 13%` · `STRAT_BWB` · `STRAT_Double BWB` · legacy v1/v2 (git history)

---

## 0. How the validator uses this book

1. Detect structure (PCS, BWB, etc. — TDD §5)
2. Match to a strategy chapter below (by structure + DTE profile)
3. Validate against that chapter's parameters only
4. No matching chapter → "no rules defined for this structure" — flagged, never guessed

### 0.1 Tolerance philosophy (Pop's directive, 2026-07-16)

Rules are **zones, not walls**. Option chains don't always offer the ideal strike; real entries are a combo of factors. Every numeric parameter therefore has two bands:

| Band | Meaning | Chip |
|---|---|---|
| **Ideal** | The textbook zone | 🟢 counts as clean |
| **Acceptable** | Wiggle room — fine when the chain forces it | 🟢 clean, noted in tooltip only |
| **Outside** | Beyond wiggle room | 🟡 flag (never a block) |

The overall verdict is holistic: one parameter slightly outside its acceptable band while everything else is ideal → 🟡 with context, not a failure. The validator describes; Pop decides.

**Standing bands (resolve OQ1/OQ2):**
- S1 spread width: ideal 10 · acceptable up to 20
- S2 narrow wing: ideal 25 · acceptable 20–30 (broken wing ~2× narrow)
- DTE: ±2 days around each chapter's range
- Deltas: ±0.03 around each chapter's targets

---

## S1 — SPX Put Credit Spread (income core)

| Parameter | Rule |
|---|---|
| Structure | Bull put spread, SPX/SPXW |
| Width | 10 points |
| DTE | 7–14 |
| Short delta | 0.10–0.15 |
| Distance | 4–6% below spot |
| Credit | $0.80–1.00 per 10-wide |
| Profit take | 50–70% of max profit |
| Stop loss | 200–250% of credit — hard |
| Risk/trade | 1–3% of portfolio |
| Avoid | FOMC, CPI, earnings-like events |

## S2 — Put Broken-Wing Butterfly "13%" (the live BWB strategy)

| Parameter | Rule |
|---|---|
| Structure | +1 put above / −2 puts at short strike / +1 put below (wider) |
| Wings | 25 narrow / 50 broken (live trades run ~20/50 — see OQ2) |
| DTE | 21 at entry · exit ~7 DTE · hold ≈14 days |
| Deltas | upper long ~32 · shorts ~28 · lower long ~21 (starting points) |
| VIX | <15 avoid/reduce · 15–20 acceptable · 20–30 ideal · >30 post-panic, smaller |
| Best entry | After a down day (higher IV, farther strikes) |
| Bias | Bullish-to-neutral · no upside risk |
| Avoid | 0 DTE, expiration week, all-time highs, pre-macro events |

**Evidence of fit:** Jul 29 SPXW fly (7200/7250×2/7270) was opened Jul 8 = exactly 21 DTE ✓. This is the strategy the live BWBs belong to.

## S3 — Broken-Wing Butterfly (classic, longer duration)

| Parameter | Rule |
|---|---|
| DTE | 30–60 (ideal 35–45) · avoid 0–7 |
| Deltas | upper long 20–30 · shorts 15–20 · lower long 5–10 |
| VIX | same table as S2; best after vol expansion, expecting contraction |
| Goal | SPX finishes near short strike; often opened for a credit |

## S4 — Double BWB (neutral regime)

| Parameter | Rule |
|---|---|
| Structure | Independent put BWB + call BWB, same expiry, entered as two orders |
| DTE | 35–45 preferred (30–60 acceptable) · avoid 0–21 |
| Deltas | longs ~20 · shorts 15–18 · far longs 5–8 |
| Bias | Neutral, post-vol-expansion |

## S5 — Library, not yet active

`Calendar Spreads · Butterfly · LEAPS · Collar · VIX strategies · Long Call Condor · Low Risk Strategies` — documented in `04_Options/`, no live trades matched. The validator reports "library strategy, no active ruleset" if encountered. Chapters get promoted here when Pop starts trading them.

## S6 — Operational rule: Robinhood leg-netting hazard

From Pop's own case study (`SPX Rules_Robinhood.md`): opening overlapping strikes on the same expiration (e.g., PCS + BWB sharing strikes) causes Robinhood to re-pair legs, merging strategies, distorting collateral, and making legs hard to close.
**Rule:** the validator warns whenever a candidate shares strikes/expiry with an existing open structure. (This also documents the real-world limit in TDD §4 grouping.)

## 7. Open questions — ALL RESOLVED ✅

| # | Question | Resolution |
|---|---|---|
| OQ1 | 20-wide spreads vs S1's 10 | ✅ Tolerance bands (§0.1): ideal 10, acceptable to 20 |
| OQ2 | BWB narrow wing 20 vs 25 | ✅ Tolerance bands (§0.1): ideal 25, acceptable 20–30 |
| OQ3 | Violations display | ✅ DESIGN_SPEC §3b: calm chips + tooltip, never blocking |

---

**APPROVAL:** ✅ Approved by Pop (confirmed in chat: strategies match his files) · date: 2026-07-17
