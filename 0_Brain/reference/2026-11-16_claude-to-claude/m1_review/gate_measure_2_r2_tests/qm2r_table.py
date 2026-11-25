#!/usr/bin/env python3
"""QA-MEASURE-2-R2 task 4: the seat's 25-row old->new table (its STATUS lines 160-186), each row's OLD text searched in the
file at <old> and its NEW text in the file at <new>, both from the git object store; also the line numbers it names.
usage: python3 -I -B qm2r_table.py <clone> <old> <new> <status-file>
Matching: the cell's "⏎" (a line break inside a cell) and every run of whitespace count as one space; "\\|" is "|"; a cell is
FOUND if its normalised text is a substring of the normalised file. The line numbers are checked as "the first line of the
cell's first fragment is at or near that line" (+-3)."""
import re, subprocess, sys
sys.dont_write_bytecode = True
clone, old, new, status = sys.argv[1:5]
FILES = {"RESULT.md": "spikes/U-B2-host-facts/RESULT.md", "BACKLOG.md": "BACKLOG.md", "docs/M0-OUTCOMES.md": "docs/M0-OUTCOMES.md"}
def show(rev, p): return subprocess.run(["git", "-C", clone, "show", "%s:%s" % (rev, p)], capture_output=True, check=True).stdout.decode()
norm = lambda s: re.sub(r"\s+", " ", s.replace("⏎", " ").replace("\\|", "|")).strip()
rows = [l for l in open(status, encoding="utf-8").read().split("\n")[159:186] if l.startswith("| ") and not l.startswith("| #")]
def cells(l):
    out, cur, i = [], "", 1
    while i < len(l):
        if l[i] == "\\" and l[i + 1:i + 2] == "|": cur += "\\|"; i += 2; continue
        if l[i] == "|": out.append(cur.strip()); cur = ""; i += 1; continue
        cur += l[i]; i += 1
    return out
def near(text, frag, line):
    first = norm(frag)[:40]
    for k in range(max(1, line - 3), line + 4):
        lines = text.split("\n")
        if k <= len(lines) and first[:25] in norm(lines[k - 1]): return True
    return False
ok = 0
for l in rows:
    c = cells(l)
    if len(c) < 5: print("UNPARSED", l[:60]); continue
    n, chk, where, o, w = c[:5]
    m = re.match(r"(\S+?):(\d+) → (\d+)", where)
    f = FILES[m.group(1)]; lo, ln = int(m.group(2)), int(m.group(3))
    to, tn = show(old, f), show(new, f)
    fo = norm(o) in norm(to); fn = norm(w) in norm(tn); still_old = norm(o) in norm(tn) and norm(o) != norm(w) and not norm(o) in norm(w)
    lo_ok = near(to, o, lo); ln_ok = near(tn, w, ln)
    ok += fo and fn and not still_old
    print("row %-2s %-24s old found %-5s new found %-5s old text still at new %-5s | line old~%s %s new~%s %s" % (n, chk[:24], fo, fn, still_old, lo, lo_ok, ln, ln_ok))
print("rows: %d ; old found at old AND new found at new AND old gone: %d" % (len(rows), ok))
