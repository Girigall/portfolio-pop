# Archive Job — weekly procedure (M1)

**Runs:** every Friday after US close. Courier: Claude scheduled task.

**M9 scope decision (2026-07-20):** Robinhood has no official retail API and no CSV export for current positions/balances — only for transaction history. So "zero AI dependency" split in two: **trades** now come from Pop manually via the F10 Reader tab (`index.html`, 100% client-side, zero AI, zero credentials) — the courier **no longer pulls trades**. **Positions and accounts** have no clean manual alternative (no Robinhood export exists for them), so the courier keeps pulling those via Claude. `archive_generate.py` needed zero code changes for this — it already treats an empty/absent `trades[]` as a no-op (0 rows appended, existing ledger rewritten unchanged).

**Code:** `app/archive_generate.py` · **Contracts:** DATA_SPEC §4 · **Tests:** TEST_PLAN §3.

## Procedure (what the courier does)

1. **Pull from Robinhood connector** (account 878912005 unless noted):
   - `get_option_positions` nonzero → `get_option_instruments` (strikes) → `get_option_quotes` (marks + greeks)
   - `get_equity_positions` for 878912005 and 429049521 → `get_equity_quotes` (batches ≤20)
   - `get_portfolio` for all 5 accounts (878912005, 788048817, 429049521, 882733181, 665888434)
   - Trades are **not** pulled here — Pop imports those separately via Reader. (`get_pnl_trade_history` is no longer part of this job.)
2. **Assemble `run_data.json` in /tmp (NEVER in the repo)** (schema: see `archive_generate.py` docstring + git history example): `as_of` (ISO now), `snapshot_date` (YYYY-MM-DD), `positions[]` (option legs with strikes + stocks with last price, accounts as last-4), `accounts[]`. `trades[]` omitted (or empty) — the script no-ops that section cleanly. **As of 2026-07-22:** option-leg position objects also carry `opened_at` (straight through from `get_option_positions`, already fetched — no extra call) and `delta`/`theta` (from `get_option_quotes`, nullable — write `""` when the connector returns null, never a guessed value). Stock-kind positions omit all three keys; `archive_generate.py` defaults them to `""`.
3. **Run:** `python3 app/archive_generate.py run_data.json history/`
4. **Verify:** rows_appended ≥ 0 per section, `failures` empty, ledger count vs previous (must not shrink — the script hard-asserts this).
5. **On any pull failure:** run with `--fail-section <name>` so the failed section's file stays untouched and the failure is logged to `_meta.json`. NEVER write partial data.
6. **Commit** `history/` changes: `git commit -m "archive: weekly snapshot YYYY-MM-DD"` and push to GitHub if Pop has provided the token this session.
7. **Report to Pop** (if interactive): rows appended, failures, notable changes (new/closed structures).

## Concurrency rule

If `.git/index.lock` exists, another session is mid-commit: wait and retry up to 3x (30s apart); only remove a lock older than 5 minutes. Never run two archive jobs simultaneously.

## Invariants (non-negotiable)

- Append-only: row counts never decrease (script asserts; TEST A2)
- Dedupe keys: ledger `timestamp_symbol_qty_gain` · snapshots `date+kind+symbol+option_id` · accounts `date+account`
- Atomic writes (temp + rename) — a crash mid-write cannot corrupt a file
- Strike memory: option legs are snapshotted with full contract identity while open — closes matched later inherit strategy/strikes (TDD §8, M4+)

## First run

2026-07-17: 94 trades, 41 positions, 5 accounts. Options realized reconciled to broker: $12,337.24 exact. Tests A1/A2/A5 passed.
