#!/usr/bin/env python3
"""rekey_c4.py — the gate76 drafter's ONE-SHOT re-key of c4_docs_gate73.py (sed'ed gate73->gate76 first) into c4_docs_gate76.py.
Every replacement asserts its anchor count first (validate all anchors, then mutate, then write)."""
import sys
F = sys.argv[1]; s = open(F, encoding='utf-8').read()


def rep(a, b, n=1):
    global s
    c = s.count(a)
    if c != n: raise SystemExit('anchor count %d != %d for %r' % (c, n, a[:80]))
    s = s.replace(a, b)


i = s.index('r"""'); end = 'rc 0 PASS / 1 FAIL / 2 refused by name."""'; j = s.index(end) + len(end)
s = s[:i] + open(sys.argv[2], encoding='utf-8').read().rstrip('\n') + s[j:]
rep("'GIT_AUTHOR_DATE': '2026-10-07T00:00:00Z', 'GIT_COMMITTER_DATE': '2026-10-07T00:00:00Z'",
    "'GIT_AUTHOR_DATE': '2026-10-08T00:00:00Z', 'GIT_COMMITTER_DATE': '2026-10-08T00:00:00Z'")
i = s.index('def balance(text):'); j = s.index('def readback(')
s = s[:i] + open(sys.argv[3], encoding='utf-8').read() + '\n\n' + s[j:]
rep("import io, itertools, json, os, re, subprocess, sys, tarfile, tempfile", "import collections, io, itertools, json, os, re, subprocess, sys, tarfile, tempfile")
rep("balance('\\n'.join(blk)) == (0, 0)", "balance('\\n'.join(blk)) == ()")
rep("the base tail section (KS-1136) is a section card", "the other row\\'s cheat block (KS-1274) IS a section card")
i = s.index("    man = os.path.join(os.path.dirname(os.path.abspath(__file__)), '..', '2026-10-06_gate71'"); j = s.index("    return t.end()\n\n\ndef qm(")
s = s[:i] + open(sys.argv[4], encoding='utf-8').read() + s[j:]
rep("'c4: REFUSED — --order must name 1-4 distinct rows of %s", "'c4: REFUSED — --order must name 1-2 distinct rows of %s")
i = s.index('# ---------------- self-test ----------------'); j = s.index('def main():')
s = s[:i] + open(sys.argv[5], encoding='utf-8').read() + '\n\n' + s[j:]
rep('table/div balance %s == develop %s', 'tag balance %s == develop %s')
rep('table/div balance head %s == base %s', 'tag balance head %s == base %s')
rep('union table/div balance %s vs composer %s', 'union tag balance %s vs composer %s')
open(F, 'w', encoding='utf-8').write(s); print('rekey_c4: ok')
