#!/usr/bin/env python3
"""Summarise the gate r4 mutation logs: per mutant, the seat's failing tests and gate_r4's, with
the first assertion text of each failing test. usage: mutsummary.py <mutlogs dir> <mutation json>"""
import json, os, re, sys

logs, js = sys.argv[1], sys.argv[2]
meta = json.load(open(js)) if os.path.exists(js) else {}
out = {}
for f in sorted(os.listdir(logs)):
    if not f.endswith(".log"):
        continue
    mid = f[:-4]
    log = open(os.path.join(logs, f)).read()
    failed = sorted(set(re.findall(r"^test (\S+) \.\.\. FAILED", log, re.M)))
    texts = {}
    for t in failed:
        m = re.search(r"thread '" + re.escape(t) + r"' \(\d+\) panicked at ([^\n]+):\n(.{0,240})", log, re.S)
        if m:
            texts[t] = (m.group(1) + " :: " + m.group(2).split("\n")[0])[:300]
    seat = [t for t in failed if not t.startswith("r4_")]
    mine = [t for t in failed if t.startswith("r4_")]
    compile_error = bool(re.search(r"^error(\[E\d+\])?: ", log, re.M)) and "could not compile" in log
    out[mid] = dict(rule=meta.get(mid, {}).get("rule", ""), compile_error=compile_error,
                    seat_killed=seat, r4_killed=mine, texts=texts)
    status = "COMPILE-ERROR" if compile_error else ("KILLED" if failed else "SURVIVED")
    print(f"{mid} [{out[mid]['rule']}] {status}: seat {len(seat)} {seat[:6]} | r4 {len(mine)} {mine}")
json.dump(out, open(os.path.join(os.path.dirname(logs), "mutation_r4_summary.json"), "w"), indent=1)
