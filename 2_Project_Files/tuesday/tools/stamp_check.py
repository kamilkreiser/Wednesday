#!/usr/bin/env python3
"""stamp_check.py — refuse a kit stamp until every literal the kit tells a seat to MATCH has a measurement.

WHY (ledger _ledger_laptop_datasec.md, 2026-11-12, w=3 REGRESSION of the stamped-text-not-measured family):
in one evening three seats halted on assertions Tuesday stamped without running them: B1544's "the name
appears once" (it was on 2 lines), B1545's step order (a cell needing files a later step makes) and B1545's
quoted `--check` line ("N runtime rows = N committed"; the tool prints "runtime rows N; committed rows N").
Reading a kit checks its sense; only an instrument checks its literals. Rules in memory lost three times.

WHAT IT DOES
  stamp_check.py <kit.md>            list every CLAIM (id, line, the literal, why it was picked) and check the
                                     sidecar <kit.md>.measured; exit 0 only if every claim id has a line there.
  stamp_check.py <kit.md> --init     write a sidecar skeleton (one line per claim, `<id> | TODO`) if none exists.
  stamp_check.py --selftest          run the built-in cases (fire and quiet paths).

A CLAIM is a backticked literal on a line that also asserts what a check will see:
  count words  (once, exactly N, N times, `-c`, prints N, reads N, count N)
  output words (prints, reads, holds, says, starts with, answers, returns, status NNN, rc N)
A sidecar line is `<id> | <what was run> -> <what it printed>`; a line still reading TODO does not count.
It reads only; it writes only the sidecar, and only with --init.
"""
import hashlib, re, sys, os

COUNT = re.compile(r"\b(once|exactly\s+\d+|\d+\s+times|prints\s+\d+|reads\s+\d+|count\s+\d+)\b|(?<![\w-])-c\b", re.I)
OUTPUT = re.compile(r"\b(prints?|reads?|holds?|says|starts?(?:\s+with)?|answers?|returns?|status\s+\d{3}|rc\s+\d)\b", re.I)
TICK = re.compile(r"`([^`\n]{3,200})`")
SKIP = re.compile(r"^\s*(-\s*)?(STAMP|LAUNCH WINDOW|BASE|JIRA|MOVE|CREATE|RECORDS|REC-MERGE|Hard stop|HARD STOP|HEADS AT LAUNCH)\b.*____|READ-WHOLE-BY-TUESDAY", re.I)

QUOTE = re.compile(r'"([^"\n]{6,160})"')
# a clause ends at ';', '. ' or a table cell bar; kit lines are whole paragraphs, so the
# assertion word must sit in the SAME clause as the literal and within WIN characters of it
CLAUSE = re.compile(r";\s|\.\s|\s\|\s")
WIN = 50

def _window(line, a, b):
    """the text around a literal at [a,b), cut at the nearest clause break OUTSIDE the literal"""
    left = line[max(0, a - WIN):a]
    seps = list(CLAUSE.finditer(left))
    if seps:
        left = left[seps[-1].end():]
    right = line[b:b + WIN]
    m = CLAUSE.search(right)
    if m:
        right = right[:m.start()]
    return left + " " + right

def claims(text):
    out = []
    for n, line in enumerate(text.splitlines(), 1):
        # The Stamp section is Tuesday's own text, written AFTER the measurement; it holds no literal a seat matches.
        # (2026-11-13 13:12: the launch gate refused B1551 on the word `.measured` inside Tuesday's stamp line.)
        if re.match(r"^##\s+Stamp\b", line, re.I):
            break
        if SKIP.search(line):
            continue
        for rx_lit, kind in ((TICK, "tick"), (QUOTE, "quote")):
            for m in rx_lit.finditer(line):
                lit = m.group(1)
                if lit.startswith(("/Volumes/", "http", "<<")) or (" " not in lit and re.search(r"\.(md|py|sh|json|ts|tsx|cs|js)$", lit)):
                    continue  # a path or a fill-in is a pointer, not a matched literal
                w = _window(line, m.start(), m.end())
                c, o = COUNT.search(w), OUTPUT.search(w)
                if kind == "quote" and not (c or re.search(r"\b(prints?|line|reads?)\b", w, re.I)):
                    continue
                if not (c or o):
                    continue
                why = ("count" if c else "output") + ("" if kind == "tick" else "/quoted")
                cid = hashlib.sha256(f"{n}:{lit}".encode()).hexdigest()[:8]
                if cid not in {x[0] for x in out}:
                    out.append((cid, n, lit, why))
    return out

def sidecar_ids(path):
    if not os.path.exists(path):
        return set()
    ok = set()
    for l in open(path, encoding="utf-8"):
        if "|" in l:
            cid, rest = l.split("|", 1)
            if rest.strip() and "TODO" not in rest:
                ok.add(cid.strip())
    return ok

def main(argv):
    if argv[1:] == ["--selftest"]:
        return selftest()
    if len(argv) < 2:
        print(__doc__); return 2
    kit = argv[1]; side = kit + ".measured"
    cs = claims(open(kit, encoding="utf-8").read())
    if "--init" in argv[2:]:
        if os.path.exists(side):
            print(f"stamp_check: sidecar exists, not overwritten: {side}"); return 2
        with open(side, "w", encoding="utf-8") as f:
            for cid, n, lit, why in cs:
                f.write(f"{cid} | TODO  (line {n}, {why}: {lit[:90]})\n")
        print(f"stamp_check: wrote {len(cs)} TODO lines to {side}"); return 0
    have = sidecar_ids(side)
    missing = [c for c in cs if c[0] not in have]
    for cid, n, lit, why in cs:
        print(f"{'OK  ' if cid in have else 'MISS'} {cid} line {n} [{why}] {lit[:110]}")
    print(f"stamp_check: {len(cs)} claims, {len(cs)-len(missing)} measured, {len(missing)} not measured (sidecar {side})")
    if missing:
        print("stamp_check: REFUSED — measure each MISS (run the tool, print the result) and record it in the sidecar before stamping.")
        return 1
    return 0

def selftest():
    import tempfile
    ok = True
    kit = ("x\n- (iii) `Foo.Bar` appears once in the file\n- the tool prints `runtime rows N; committed rows N`\n"
           "- see `/Volumes/x/y.md` for detail\n- plain line with `code` and no assertion words\n- STAMP: ____\n")
    cs = claims(kit)
    lits = [c[2] for c in cs]
    def t(name, cond):
        nonlocal ok
        print(("PASS " if cond else "FAIL ") + name); ok &= bool(cond)
    t("count claim found (once)", "Foo.Bar" in lits)
    t("output claim found (prints)", "runtime rows N; committed rows N" in lits)
    t("path pointer ignored", not any(l.startswith("/Volumes/") for l in lits))
    t("plain backtick without assertion ignored", "code" not in lits)
    t("exactly two claims", len(cs) == 2)
    stamped = kit + "## Stamp\n- STAMP: Tuesday read `.measured` once and stamp_check prints `110 claims`\n"
    t("Stamp section text is not a claim", len(claims(stamped)) == 2)
    d = tempfile.mkdtemp(); k = os.path.join(d, "k.md"); open(k, "w").write(kit)
    t("refuses with no sidecar", main(["x", k]) == 1)
    t("--init writes skeleton", main(["x", k, "--init"]) == 0 and os.path.exists(k + ".measured"))
    t("TODO lines do not count", main(["x", k]) == 1)
    with open(k + ".measured", "w") as f:
        for cid, n, lit, why in cs:
            f.write(f"{cid} | grep -c -> 1\n")
    t("passes when every claim measured", main(["x", k]) == 0)
    with open(k + ".measured", "w") as f:
        f.write(f"{cs[0][0]} | grep -c -> 1\n")
    t("refuses when one claim missing", main(["x", k]) == 1)
    print("selftest:", "OK" if ok else "FAILED")
    return 0 if ok else 1

if __name__ == "__main__":
    sys.exit(main(sys.argv))
