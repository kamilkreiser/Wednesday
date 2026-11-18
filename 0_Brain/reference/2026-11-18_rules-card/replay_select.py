#!/usr/bin/env python3
"""Replay-test sample selector (deterministic, no randomness). Re-run:
   python3 0_Brain/reference/2026-11-18_rules-card/replay_select.py [--full]
Friday live ledger: EVERY dated row whose Type cell matches (?i)correction|self-found|implicit|defect|regression.
Other five files: dated table rows whose text matches (?i)correction|self-found|regression,
in file order, every Nth row (N = eligible // quota), starting at index N//2, quota per file below."""
import re, sys, os, json
L = os.path.join(os.path.dirname(os.path.abspath(__file__)), "..", "..", "learnings")
QUOTA = [("_ledger_friday_archive.md", 12), ("_ledger.md", 8), ("_ledger_archive.md", 40),
         ("_ledger_laptop_datasec.md", 6), ("_ledger_laptop_datasec_archive.md", 24)]
ROW = re.compile(r"^\|\s*\*{0,2}(20\d\d-\d\d-\d\d)")
KEY = re.compile(r"correction|self-found|regression", re.I)
def rows(fn):
    out = []
    for n, line in enumerate(open(os.path.join(L, fn), encoding="utf-8"), 1):
        m = ROW.match(line)
        if m:
            cells = [c.strip() for c in line.strip().strip("|").split(" | ")]
            typ = cells[-4] if len(cells) >= 6 else "?"
            les = cells[-2] if len(cells) >= 6 else "?"
            out.append(dict(file=fn, line=n, date=m.group(1), type=typ, lesson=les, text=line.strip()))
    return out
sample = []
fr = rows("_ledger_friday.md")
FTYPE = re.compile(r"correction|self-found|implicit|defect|regression", re.I)  # praise, grant, preference, restriction rows are skipped
keep = [r for r in fr if FTYPE.search(r["type"])]
print(f"_ledger_friday.md dated={len(fr)} kept={len(keep)} skipped_types={[r['type'] for r in fr if r not in keep]}", file=sys.stderr)
sample += keep
for fn, q in QUOTA:
    allr = rows(fn); el = [r for r in allr if KEY.search(r["text"])]
    n = max(1, len(el) // q); pick = el[n // 2::n][:q]
    print(f"{fn} dated={len(allr)} eligible={len(el)} N={n} picked={len(pick)}", file=sys.stderr)
    sample += pick
full = "--full" in sys.argv
for i, r in enumerate(sample, 1):
    t = r["text"] if full else r["text"][:1100]
    print(f"### {i} | {r['file']}:{r['line']} | {r['date']} | type={r['type'][:60]} | lesson={r['lesson'][:300]}\n{t}\n")
json.dump([{k: r[k] for k in ("file","line","date","type","lesson")} for r in sample], open(os.path.join(os.path.dirname(os.path.abspath(__file__)), "replay_sample.json"), "w"), indent=0)
