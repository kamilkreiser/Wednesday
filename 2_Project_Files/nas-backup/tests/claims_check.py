#!/usr/bin/env python3
# claims_check.py — checks every coverage claim STATUS.md makes against what the suite and the mutant run SHOW.
# ANSWER-4 item 9: "STATUS claims about test coverage are checked against the suite by a program before you write
# them (round 2 claimed 24 shapes covered where 8 were absent)". A claim is a line of tests/claims.tsv:
#     <id> TAB <kind> TAB <argument> TAB <what STATUS says>
# kinds:
#   pass     <text>     a suite line `  PASS  ...<text>...` exists and no `  FAIL  ` line carries <text>
#   passes   <prefix>:<n>   at least <n> PASS lines start with <prefix>, and no FAIL line does
#   mutant   <id>       the mutant run has a `  CAUGHT    <id>-...` line (and no SURVIVED or BROKEN line for it)
#   total    <n>        the suite's last line says `<n> passed, 0 failed`
#   mutants  <n>        the mutant run's last line says `<n> mutants caught, 0 survived or broken`
#   k15                 every mutant the second checker reported as SURVIVED (read from his raw output) is CAUGHT here
#   names40             every one of the second checker's 40 conventional names (read from his script) is planted by T28
# It prints one line per claim and exits 1 if any claim is NOT SUPPORTED. It reads files only.
#   claims_check.py <suite output> <mutants output> [claims.tsv]
import os, re, sys
HERE = os.path.dirname(os.path.realpath(__file__))
QA2 = os.path.realpath(os.path.join(HERE, "..", "..", "..", "0_Brain", "reference", "2026-11-27_qa-nasbackup-r2"))


def lines_of(p):
    with open(p, "r", encoding="utf-8", errors="replace") as fh:
        return fh.read().split("\n")


def main():
    suite, mut = lines_of(sys.argv[1]), lines_of(sys.argv[2])
    claims = sys.argv[3] if len(sys.argv) > 3 else os.path.join(HERE, "claims.tsv")
    passes = [ln[8:] for ln in suite if ln.startswith("  PASS  ")]
    fails = [ln[8:] for ln in suite if ln.startswith("  FAIL  ")]
    caught = dict((ln.split()[1].split("-")[0], ln) for ln in mut if ln.startswith("  CAUGHT "))
    notcaught = dict((ln.split()[1].split("-")[0], ln) for ln in mut if ln.startswith("  SURVIVED") or ln.startswith("  BROKEN"))
    suite_last = [ln for ln in suite if ln.startswith("=== ") and " passed, " in ln]
    mut_last = [ln for ln in mut if ln.startswith("=== ") and " mutants caught" in ln]
    bad = n = 0
    for raw in lines_of(claims):
        if not raw.strip() or raw.startswith("#"):
            continue
        parts = raw.split("\t")
        if len(parts) != 4:
            print("NOT SUPPORTED  (malformed claim line: %r)" % raw[:80])
            bad += 1
            continue
        cid, kind, arg, text = parts
        n += 1
        ok, why = False, ""
        if kind == "pass":
            hit = [p for p in passes if arg in p]
            fl = [p for p in fails if arg in p]
            ok, why = bool(hit) and not fl, "%d PASS line(s), %d FAIL line(s) carry it" % (len(hit), len(fl))
        elif kind == "passes":
            prefix, want = arg.rsplit(":", 1)
            hit = [p for p in passes if p.startswith(prefix)]
            fl = [p for p in fails if p.startswith(prefix)]
            ok, why = len(hit) >= int(want) and not fl, "%d PASS line(s) start with it (claimed at least %s), %d FAIL" % (len(hit), want, len(fl))
        elif kind == "mutant":
            ok, why = arg in caught and arg not in notcaught, (caught.get(arg) or notcaught.get(arg) or "no line for it in the mutant run").strip()[:110]
        elif kind == "total":
            ok = bool(suite_last) and suite_last[-1].startswith("=== %s passed, 0 failed" % arg)
            why = (suite_last[-1] if suite_last else "no summary line")[:60]
        elif kind == "mutants":
            ok = bool(mut_last) and mut_last[-1].startswith("=== %s mutants caught, 0 survived or broken" % arg)
            why = (mut_last[-1] if mut_last else "no summary line")[:70]
        elif kind == "k15":
            surv = [ln.split()[1].split("-")[0] for ln in lines_of(os.path.join(QA2, "raw", "K_my_mutants.out")) if ln.startswith("  SURVIVED")]
            miss = [k for k in surv if k not in caught or k in notcaught]
            ok, why = len(surv) == 15 and not miss, "his output lists %d survivors (%s); not caught here: %s" % (len(surv), " ".join(surv), " ".join(miss) or "none")
        elif kind == "names40":
            src = lines_of(os.path.join(QA2, "scripts", "N11_first_copy.sh"))
            names = []
            for ln in src:
                m = re.match(r"^c(\d\d)\|(.+)$", ln)
                if m and m.group(2) not in names:
                    names.append(m.group(2))
            run = "\n".join(lines_of(os.path.join(HERE, "run.sh")))
            m = re.search(r'^NAMES="([^"]*)"', run, re.M)
            planted = m.group(1).split("|") if m else []
            miss = [x for x in names if x not in planted]
            ok, why = len(names) == 40 and not miss, "his script plants %d names; missing from T28's NAMES: %s" % (len(names), ", ".join(miss) or "none")
        else:
            why = "unknown kind %r" % kind
        print("%-14s %-6s %-8s %s  [%s]" % ("SUPPORTED" if ok else "NOT SUPPORTED", cid, kind, text, why))
        bad += 0 if ok else 1
    print("=== %d claims checked, %d NOT SUPPORTED ===" % (n, bad))
    return 1 if bad or not n else 0


sys.exit(main())
