#!/usr/bin/env python3
"""
Archive generator — Pop's Portfolio (M1).
Reads a run-data JSON (pulled from the Robinhood connector by Claude) and
appends to the three history CSVs. Append-only, dedup-safe, atomic writes.

Usage:  python3 archive_generate.py <run_data.json> <history_dir> [--fail-section SECTION]
        --fail-section simulates a failed pull (test A5): that section is skipped,
        its file left untouched, and the failure logged to _meta.json.

Contracts: docs/02_technical/DATA_SPEC_Robinhood_Archive.md §4
Invariant (TEST A2): row counts NEVER decrease. Enforced here — refuses to write fewer rows.
"""
import csv, json, os, sys, tempfile

LEDGER_COLS = ["trade_id","closed_at","account","symbol","asset_class","quantity",
               "close_price","realized_gain","strategy","strikes","expiry","source",
               "broker","thesis","vix_at_entry"]
SNAP_COLS   = ["snapshot_date","account","kind","symbol","option_id","side","qty",
               "avg_price","strike","put_call","expiry","mark","multiplier"]
ACCT_COLS   = ["snapshot_date","account","total_value","equity_value","options_value",
               "crypto_value","cash","buying_power"]
INDEX_UNDERLYINGS = {"SPX","SPXW","XSP","NDX","RUT","VIX"}

def classify(sym, qty):
    if not sym: return "unclassified"
    if sym in INDEX_UNDERLYINGS: return "option"
    try: q = float(qty)
    except: return "unclassified"
    return "option" if (q.is_integer() and 0 < q <= 20) else "stock"

def load_rows(path):
    if not os.path.exists(path): return []
    with open(path) as f: return list(csv.DictReader(f))

def atomic_write(path, cols, rows):
    d = os.path.dirname(path)
    fd, tmp = tempfile.mkstemp(dir=d, suffix=".tmp")
    with os.fdopen(fd, "w", newline="") as f:
        w = csv.DictWriter(f, fieldnames=cols); w.writeheader()
        for r in rows: w.writerow({c: r.get(c, "") for c in cols})
    os.replace(tmp, path)

def main():
    data_path, hist = sys.argv[1], sys.argv[2]
    fail = sys.argv[sys.argv.index("--fail-section")+1] if "--fail-section" in sys.argv else None
    with open(data_path) as f: run = json.load(f)
    os.makedirs(hist, exist_ok=True)
    meta = {"last_run": run["as_of"], "rows_appended": {}, "failures": [], "schema_version": 1}

    # 1) trades_ledger (append-only, dedupe on trade_id)
    lp = os.path.join(hist, "trades_ledger.csv")
    if fail == "trades":
        meta["failures"].append("trades: simulated pull failure — file untouched")
    else:
        existing = load_rows(lp); seen = {r["trade_id"] for r in existing}
        # cross-source dedupe: skip connector rows already imported by the F10 reader
        # (reader IDs differ; match on day+symbol+qty with $5 gain tolerance for fee variance)
        reader_keys = [(r["closed_at"][:10], r["symbol"], r["quantity"], float(r["realized_gain"] or 0))
                       for r in existing if r.get("source") == "reader"]
        new = []
        for t in run.get("trades", []):
            tid = f'{t["timestamp"]}_{t["symbol"] or "UNKNOWN"}_{t["quantity"]}_{t["realized_gain"]}'
            if tid in seen: continue
            g = float(t["realized_gain"] or 0)
            if any(k[0] == t["timestamp"][:10] and k[1] == (t["symbol"] or "UNKNOWN")
                   and k[2] == str(t["quantity"]) and abs(k[3] - g) <= 5 for k in reader_keys):
                continue  # reader already recorded this trade
            new.append({"trade_id": tid, "closed_at": t["timestamp"], "account": run["account_last4"],
                        "symbol": t["symbol"] or "UNKNOWN",
                        "asset_class": classify(t["symbol"], t["quantity"]),
                        "quantity": t["quantity"], "close_price": t["price"],
                        "realized_gain": t["realized_gain"], "strategy": t.get("strategy",""),
                        "strikes": t.get("strikes",""), "expiry": t.get("expiry",""),
                        "source": "connector", "broker": "robinhood", "thesis": "", "vix_at_entry": ""})
        merged = existing + sorted(new, key=lambda r: r["closed_at"])
        assert len(merged) >= len(existing), "A2 violation: ledger would shrink"
        atomic_write(lp, LEDGER_COLS, merged); meta["rows_appended"]["ledger"] = len(new)

    # 2) positions_snapshots (append this snapshot date; dedupe on date+symbol/option_id+kind)
    sp = os.path.join(hist, "positions_snapshots.csv")
    if fail == "positions":
        meta["failures"].append("positions: simulated pull failure — file untouched")
    else:
        existing = load_rows(sp)
        seen = {(r["snapshot_date"], r["kind"], r["symbol"], r["option_id"]) for r in existing}
        new = []
        for p in run.get("positions", []):
            key = (run["snapshot_date"], p["kind"], p["symbol"], p.get("option_id",""))
            if key in seen: continue
            new.append({**p, "snapshot_date": run["snapshot_date"]})
        merged = existing + new
        assert len(merged) >= len(existing), "A2 violation: snapshots would shrink"
        atomic_write(sp, SNAP_COLS, merged); meta["rows_appended"]["snapshots"] = len(new)

    # 3) accounts_history (append; dedupe on date+account)
    ap = os.path.join(hist, "accounts_history.csv")
    if fail == "accounts":
        meta["failures"].append("accounts: simulated pull failure — file untouched")
    else:
        existing = load_rows(ap)
        seen = {(r["snapshot_date"], r["account"]) for r in existing}
        new = [{**a, "snapshot_date": run["snapshot_date"]} for a in run.get("accounts", [])
               if (run["snapshot_date"], a["account"]) not in seen]
        merged = existing + new
        assert len(merged) >= len(existing), "A2 violation: accounts would shrink"
        atomic_write(ap, ACCT_COLS, merged); meta["rows_appended"]["accounts"] = len(new)

    with open(os.path.join(hist, "_meta.json"), "w") as f: json.dump(meta, f, indent=1)
    print(json.dumps(meta))

if __name__ == "__main__":
    main()
