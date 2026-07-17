# Archive Job — weekly procedure (M1)

**Runs:** every Friday ~21:30 UTC (after US close) via Cowork scheduled task, or on demand ("run the archive job").
**Code:** `app/archive_generate.py` · **Contracts:** DATA_SPEC §4 · **Tests:** TEST_PLAN §3.

## Procedure (what the scheduled Claude session does)

1. **Pull from Robinhood connector** (account 878912005 unless noted):
   - `get_pnl_trade_history` span `all`, paginate via `next_cursor`
   - `get_option_positions` nonzero → `get_option_instruments` (strikes) → `get_option_quotes` (marks)
   - `get_equity_positions` for 878912005 and 429049521 → `get_equity_quotes` (batches ≤20)
   - `get_portfolio` for all 5 accounts (878912005, 788048817, 429049521, 882733181, 665888434)
2. **Assemble `run_data.json` in /tmp (NEVER in the repo)** (schema: see `archive_generate.py` docstring + git history example): `as_of` (ISO now), `snapshot_date` (YYYY-MM-DD), `trades[]`, `positions[]` (option legs with strikes + stocks with last price, accounts as last-4), `accounts[]`.
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
