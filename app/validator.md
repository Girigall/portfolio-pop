# F9 Pre-trade Validator — chat procedure (M6)

**Trigger:** Pop pastes a screenshot of a candidate trade (Robinhood order ticket, option chain, or any readable layout) and says anything like "validate this" / "check this trade".
**Code:** `app/validator.py` (tolerance zones per RULEBOOK §0.1) · **Journal:** `history/candidates_journal.csv` (append-only)

## The flow (Claude executes, Pop decides)

1. **Extract** from the screenshot natively (no OCR service): underlying, legs (side/qty/strike/put-call), net credit/debit, expiry. Note anything unreadable.
2. **CONFIRMATION GATE (mandatory — HAL #3):** echo the extracted values to Pop: *"I read: SPXW +1 7360P / −2 7410P / +1 7430P, $4.15 credit, exp Aug 6. Correct?"* Wait for confirm/correct/retake. **No verdict on unconfirmed numbers. Unconfirmed extractions are discarded.**
3. **Enrich** (live, via Robinhood connector): VIX + SPX spot (`get_index_quotes`), short-leg delta (`get_option_instruments` by chain/expiry/strike → `get_option_quotes`). Warn if a structure would share strikes+expiry with an existing open position (RULEBOOK S6 netting hazard — check `get_option_positions`).
4. **Validate:** `python3 app/validator.py --validate '<json>'` → verdict GREEN / YELLOW / RED + itemized flags & notes citing rulebook chapters.
5. **Report** to Pop: verdict, flags, notes, DTE, max loss (payoff), break-evens. **Framing rule: describe, never advise.** No "you should take this trade" — ever (TEST V4).
6. **Journal on Pop's confirm only:** ask for a one-line thesis (optional), then `--journal` mode appends to `history/candidates_journal.csv` with `status=candidate`. If Pop later executes it, the archive job's ledger picks up the real trade; the journal row remains the pre-trade record (thesis, VIX, verdict at entry — the "Reveal & Reflect" seed).

## Verdicts (zones, not walls — §0.1)

| Verdict | Meaning |
|---|---|
| 🟢 GREEN | All parameters in ideal or acceptable (wiggle-room) zones |
| 🟡 YELLOW | One or more parameters outside acceptable bands — listed, Pop decides |
| 🔴 RED | No matching strategy chapter — validator cannot assess, never guesses |

## Journal schema
`created_at · underlying · strategy · rule · strikes · expiry · qty · net_credit · dte_entry · short_delta · vix · spot · verdict · flags · thesis · status(candidate/executed/skipped) · source(validator)`

## Tests passed (2026-07-18)
V1 legacy regression: Jun-10 trade → YELLOW, delta 0.47 flagged (DTE 6 now wiggle-room per Pop's tolerance directive — intentional difference from the old binary engine) · V2 20-wide → GREEN with note · live Aug-6 BWB → GREEN, S2 matched · V-RED custom → RED · V3 journal append verified · V4 output contains no advice language by construction.
