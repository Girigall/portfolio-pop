#!/usr/bin/env python3
"""
F9 Pre-trade Validator (M6) — validates a candidate trade against Pop's
STRATEGY_RULEBOOK (tolerance zones §0.1: ideal / acceptable / outside) and
appends confirmed candidates to history/candidates_journal.csv (append-only).

Usage:
  validate only : python3 validator.py --validate '<json>'
  journal too   : python3 validator.py --journal  '<json>' <history_dir>

Candidate JSON fields:
  underlying, strategy_hint(optional), legs:[{side,qty,strike,pc}], credit (net, $ per structure),
  expiry (YYYY-MM-DD), entry_date (YYYY-MM-DD), short_delta (abs, optional),
  vix (optional), spot (optional), thesis (optional)

Verdicts: GREEN (all in ideal/acceptable zones) · YELLOW (flags — Pop decides)
          · RED (no matching rulebook chapter)
Never blocks. Describes. The decision is Pop's.  (RULEBOOK §0.1)
"""
import csv, json, os, sys
from datetime import date

def detect(legs):
    puts = [l for l in legs if l["pc"] == "put"]
    strikes = sorted({l["strike"] for l in legs})
    if len(legs) == 1:
        l = legs[0]
        if l["pc"] == "put":  return "CSP" if l["side"] == "short" else "Long Put"
        return "CC" if l["side"] == "short" else "Long Call"
    if len(puts) == len(legs) and len(strikes) == 2 and len(legs) == 2:
        hi = next(l for l in legs if l["strike"] == strikes[1])
        lo = next(l for l in legs if l["strike"] == strikes[0])
        if hi["side"] == "short" and lo["side"] == "long": return "PCS"
        if hi["side"] == "long" and lo["side"] == "short": return "Put Debit"
    if len(puts) == len(legs) and len(strikes) == 3:
        mid = [l for l in legs if l["strike"] == strikes[1]]
        if mid and all(l["side"] == "short" for l in mid):
            return "BWB" if abs((strikes[1]-strikes[0]) - (strikes[2]-strikes[1])) > 0.01 else "Fly"
    return f"Custom({len(legs)})"

def band(val, lo_ok, hi_ok, lo_id=None, hi_id=None):
    """returns (zone, note) — zone: ideal|acceptable|outside"""
    if val is None: return ("unknown", "not provided")
    if lo_id is not None and lo_id <= val <= hi_id: return ("ideal", "")
    if lo_ok <= val <= hi_ok: return ("acceptable", f"{val} in wiggle room")
    return ("outside", f"{val} outside acceptable {lo_ok}–{hi_ok}")

def validate(c):
    legs = c["legs"]
    name = c.get("strategy_hint") or detect(legs)
    strikes = sorted({l["strike"] for l in legs})
    dte = (date.fromisoformat(c["expiry"]) - date.fromisoformat(c["entry_date"])).days
    flags, notes, rule = [], [], None

    if name == "PCS":
        rule = "S1 · SPX Put Credit Spread"
        w = strikes[-1] - strikes[0]
        z, m = band(w, 0, 20, 10, 10);            (flags if z=="outside" else notes).append(f"width: {m or str(w)+' ideal'} ")
        z, m = band(dte, 5, 16, 7, 14);           (flags if z=="outside" else notes).append(f"DTE: {m or str(dte)+' ideal'}")
        sd = c.get("short_delta")
        z, m = band(sd, 0.07, 0.18, 0.10, 0.15);  (flags if z=="outside" else notes).append(f"short delta: {m or (str(sd)+' ideal' if sd is not None else 'not provided')}")
        if c.get("credit") is not None and w:
            notes.append(f"credit/width: {c['credit']/ (w*100*max(1,legs[0]['qty'])):.2f}")
    elif name in ("BWB", "Fly"):
        narrow = min(strikes[1]-strikes[0], strikes[2]-strikes[1])
        if dte <= 28:
            rule = "S2 · Put BWB 13%"
            z, m = band(dte, 19, 23, 21, 21);     (flags if z=="outside" else notes).append(f"DTE: {m or str(dte)+' ideal (21)'}")
        else:
            rule = "S3 · BWB classic"
            z, m = band(dte, 28, 62, 35, 45);     (flags if z=="outside" else notes).append(f"DTE: {m or str(dte)+' in range'}")
        z, m = band(narrow, 20, 30, 25, 25);      (flags if z=="outside" else notes).append(f"narrow wing: {m or str(narrow)+' ideal'}")
        vix = c.get("vix")
        if vix is not None:
            if vix < 15: flags.append(f"VIX {vix} below 15 — rulebook says avoid/reduce size")
            elif vix > 30: notes.append(f"VIX {vix} >30 — post-panic sizing rule applies")
            else: notes.append(f"VIX {vix} in tradeable zone")
    elif name in ("CSP", "CC"):
        rule = "wheel leg (library)"
        notes.append("single-leg wheel — no active ruleset chapter; informational only")
    else:
        return {"strategy": name, "rule": "off-book", "verdict": "RED",
                "flags": ["no matching strategy chapter in rulebook — validator cannot assess"],
                "notes": [], "dte": dte}

    verdict = "YELLOW" if flags else "GREEN"
    return {"strategy": name, "rule": rule, "verdict": verdict,
            "flags": flags, "notes": [n.strip() for n in notes if n.strip()], "dte": dte}

JCOLS = ["created_at","underlying","strategy","rule","strikes","expiry","qty","net_credit",
         "dte_entry","short_delta","vix","spot","verdict","flags","thesis","status","source"]

def journal(c, res, hist):
    p = os.path.join(hist, "candidates_journal.csv")
    exists = os.path.exists(p)
    rows = list(csv.DictReader(open(p))) if exists else []
    strikes = "/".join(str(int(s)) if s==int(s) else str(s) for s in sorted({l["strike"] for l in c["legs"]}))
    rows.append({"created_at": c["entry_date"], "underlying": c["underlying"], "strategy": res["strategy"],
                 "rule": res["rule"], "strikes": strikes, "expiry": c["expiry"],
                 "qty": max(l["qty"] for l in c["legs"]), "net_credit": c.get("credit",""),
                 "dte_entry": res["dte"], "short_delta": c.get("short_delta",""),
                 "vix": c.get("vix",""), "spot": c.get("spot",""),
                 "verdict": res["verdict"], "flags": " | ".join(res["flags"]),
                 "thesis": c.get("thesis",""), "status": "candidate", "source": "validator"})
    tmp = p + ".tmp"
    with open(tmp, "w", newline="") as f:
        w = csv.DictWriter(f, fieldnames=JCOLS); w.writeheader()
        for r in rows: w.writerow({k: r.get(k,"") for k in JCOLS})
    os.replace(tmp, p)
    return len(rows)

if __name__ == "__main__":
    mode, payload = sys.argv[1], json.loads(sys.argv[2])
    res = validate(payload)
    if mode == "--journal":
        n = journal(payload, res, sys.argv[3])
        res["journaled"] = n
    print(json.dumps(res, indent=1))
