#!/usr/bin/env python3
"""threshold_study.py <braindb.sh> <questions.tsv> - the WEAK MATCH threshold study (ANSWER-3 item 11).

Runs every question of the TSV through `braindb.sh search` (default order) against whatever cluster that
braindb.sh is addressed to, with the confidence figure measured on the rarest 3 and the rarest 4 terms,
judges the FIRST result against the regex written beside the question BEFORE the run, and prints:
  1. the table (question, right or wrong, first result, old all-terms score, confidence k=3, k=4);
  2. for each measure, how well any one threshold separates right first results from wrong ones.
It reads only; it changes nothing. Standard library only.
"""
import sys, os, re, subprocess

tool, tsv = sys.argv[1], sys.argv[2]
FIRST = re.compile(r"^ 1\. \S+  \[[^\]]*\]  (.*)$")
LAST = re.compile(r"first result: score ([0-9.]+); (.*)\)$")
HOLD = re.compile(r"holds (?:all )?(\d+)")
LACK = re.compile(r"lacks (\d+)")


def ask(q, k):
    env = dict(os.environ, BRAINDB_TOPK=str(k))
    r = subprocess.run(["/bin/bash", tool, "search", q], env=env, stdout=subprocess.PIPE)
    out = r.stdout.decode("utf-8", errors="replace").split("\n")
    first = next((FIRST.match(l).group(1) for l in out if FIRST.match(l)), "")
    m = next((LAST.search(l) for l in out if LAST.search(l)), None)
    held = int(HOLD.search(m.group(2)).group(1)) if m and HOLD.search(m.group(2)) else 0
    lack = int(LACK.search(m.group(2)).group(1)) if m and LACK.search(m.group(2)) else 0
    return first, (float(m.group(1)) if m else 0.0), held, held + lack


rows = []
for line in open(tsv, encoding="utf-8"):
    if line.startswith("#") or not line.strip():
        continue
    qid, src, q, want, why = line.rstrip("\n").split("\t")
    first, score, held, total = ask(q, 4)
    verdict = "?" if want == "?" else ("WRONG" if want == "-" or not re.search(want, first) else "RIGHT")
    rows.append(dict(id=qid, q=q, verdict=verdict, first=first, score=score, held=held, total=total))

print("ROUND 3, after the confidence figure was dropped: what the neutral line says for each question.")
print("%-4s %-6s %7s %6s  %-58s %s" % ("id", "first", "score", "holds", "first result", "question"))
for r in rows:
    print("%-4s %-6s %7.4f %3d/%-2d  %-58s %s" % (r["id"], r["verdict"], r["score"], r["held"], r["total"], r["first"][-58:], r["q"]))
judged = [r for r in rows if r["verdict"] != "?"]
right = [r for r in judged if r["verdict"] == "RIGHT"]
wrong = [r for r in judged if r["verdict"] == "WRONG"]
print()
print("questions: %d; judged: %d (first result RIGHT %d, WRONG %d); not judged: %d"
      % (len(rows), len(judged), len(right), len(wrong), len(rows) - len(judged)))
for name, grp in (("RIGHT", right), ("WRONG", wrong)):
    allk = sum(1 for r in grp if r["held"] == r["total"] and r["total"])
    half = sum(1 for r in grp if r["total"] and r["held"] * 2 >= r["total"] and r["held"] != r["total"])
    print("   %s first results: %d hold every rare word of the question, %d hold at least half, %d hold fewer than half"
          % (name, allk, half, len(grp) - allk - half))
print("   (no line is drawn from these counts: they are printed so a reader can see the neutral line is not a verdict either)")
