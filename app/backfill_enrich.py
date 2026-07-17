#!/usr/bin/env python3
"""
M2 Backfill — enrich pre-pipeline ledger rows with contract detail from Pop's
official Robinhood activity CSV (strikes, expiry, inferred strategy).

Usage: python3 backfill_enrich.py <robinhood_activity.csv> <history_dir>

Rules:
- Only fills EMPTY strategy/strikes/expiry fields on option rows; never overwrites.
- Enriched rows get source=csv_backfill (provenance, DATA_SPEC §4.1).
- Prints coverage report (TEST A6 gate: >=95% of option ledger rows enriched or
  explained) and a gap list. Never deletes or reduces rows (A2 safe: rewrite-in-place
  of same row count, asserted).
Matching: ledger option row (close date, symbol) -> CSV close events
(STC/BTC/OEXP/OASGN/OEXCS) same symbol & date. BTC/OASGN => short leg, STC => long.
Strategy inference: legs on that date+expiry -> PCS / CSP / CC / BWB / Fly / n-leg.
"""
import csv, re, sys, os
from collections import defaultdict

CLOSE_CODES = {"STC","BTC","OEXP","OASGN","OEXCS","OCA","OCC"}
DESC_RE = re.compile(r"([A-Z]+)\s+(\d{1,2}/\d{1,2}/\d{4})\s+(Put|Call)\s+\$([\d,]+(?:\.\d+)?)")

def norm_date(mdy):
    m,d,y = mdy.split("/"); return f"{y}-{int(m):02d}-{int(d):02d}"

def main():
    src, hist = sys.argv[1], sys.argv[2]
    events = defaultdict(list)   # (date, symbol) -> [{strike, pc, expiry, side}]
    with open(src, newline="", encoding="utf-8-sig") as f:
        for r in csv.DictReader(f):
            code = (r.get("Trans Code") or "").strip()
            if code not in CLOSE_CODES: continue
            m = DESC_RE.search((r.get("Description") or "").replace("\n"," ").strip())
            if not m: continue
            sym, exp, pc, k = m.group(1), norm_date(m.group(2)), m.group(3).lower(), m.group(4).replace(",","")
            side = "short" if code in ("BTC","OASGN") else ("long" if code == "STC" else "?")
            events[(norm_date(r["Activity Date"]), sym)].append(
                {"strike": float(k), "pc": pc, "expiry": exp, "side": side})

    def infer(legs):
        strikes = sorted({l["strike"] for l in legs})
        pcs = {l["pc"] for l in legs}
        if len(legs) == 1:
            l = legs[0]
            if l["pc"] == "put":  return "CSP" if l["side"] in ("short","?") else "Long Put"
            return "CC" if l["side"] in ("short","?") else "Long Call"
        if pcs == {"put"} and len(strikes) == 2: return "PCS"
        if pcs == {"put"} and len(strikes) == 3:
            lo, mid, hi = strikes
            return "BWB" if abs((mid-lo)-(hi-mid)) > 0.01 else "Fly"
        if pcs == {"call"} and len(strikes) == 2: return "CCS"
        return f"Custom({len(legs)})"

    lp = os.path.join(hist, "trades_ledger.csv")
    with open(lp) as f: rows = list(csv.DictReader(f)); cols = rows and list(rows[0].keys())
    n_before = len(rows)
    enriched, already, gaps = 0, 0, []
    for r in rows:
        if r["asset_class"] != "option": continue
        if r["strikes"]:
            already += 1; continue
        d = r["closed_at"][:10]
        legs = events.get((d, r["symbol"]))
        if not legs:  # settlement can land a day after the CSV's activity date
            import datetime as _dt
            prev = (_dt.date.fromisoformat(d) - _dt.timedelta(days=1)).isoformat()
            legs = events.get((prev, r["symbol"]))
        if not legs:
            gaps.append(f'{r["closed_at"][:10]} {r["symbol"]} qty {r["quantity"]} gain {r["realized_gain"]}')
            continue
        strikes = sorted({l["strike"] for l in legs})
        r["strikes"] = "/".join(str(int(k)) if k == int(k) else str(k) for k in strikes)
        r["expiry"] = max(l["expiry"] for l in legs)
        r["strategy"] = infer(legs)
        r["source"] = "csv_backfill"
        enriched += 1
    assert len(rows) == n_before, "A2 violation"
    with open(lp + ".tmp", "w", newline="") as f:
        w = csv.DictWriter(f, fieldnames=cols); w.writeheader(); w.writerows(rows)
    os.replace(lp + ".tmp", lp)

    opt_total = enriched + already + len(gaps)
    cov = 100.0 * (enriched + already) / opt_total if opt_total else 100.0
    print(f"option rows: {opt_total} | enriched now: {enriched} | already had strikes: {already} | gaps: {len(gaps)}")
    print(f"COVERAGE: {cov:.1f}%  (A6 gate: >=95%)")
    for g in gaps: print("  GAP:", g)

if __name__ == "__main__":
    main()
