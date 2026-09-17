#!/usr/bin/env python3
"""repin_launcher_1034.py — RE-PIN the #1034 launcher from fd81a75f0 / develop 27e53ec3a to e4624218b / develop 3961c2add by ASSERTED substitutions
(each old string must occur exactly the stated number of times). Adds exit 26 (merge-authority wording). Writes in place; backup = .pre-0918-repin.
Residual guard after: no fd81a75f0 outside the history comment, no 27e53ec3a outside history, no 'waits for Kam', bash -n rc 0."""
import subprocess, hashlib, re, datetime
L = '/Volumes/DevMASTER/WEDNESDAY/2_Project_Files/fleet/qa-agent/launchers/launch_qa_secuura_ks1215_1034.sh'
s = open(L).read(); orig = s
assert s == open(L + '.pre-0918-repin').read(), 'launcher differs from its backup: stop'
H = 'e4624218bc29cda4c07b2d31ca18bba422cfbc3e'; D = '3961c2add8e1637b32e638f8f0952c328c00833e'
def sub(old, new, n=1):
    global s
    c = s.count(old); assert c == n, (old[:80], c, n); s = s.replace(old, new); print('sub count', c, '::', old[:70].replace('\n', '\\n'))
sub("# @ fd81a75f0688f6cbe1e5f79b061bb1369c88f477 — services/api-gateway:",
    "# @ e4624218bc29cda4c07b2d31ca18bba422cfbc3e (RE-PINNED 2026-09-18 from fd81a75f0) — services/api-gateway:")
sub("# cells per Wednesday's 11:59:12Z ruling, completeness). fd81a75f0 = develop 27e53ec3a merged in; tree 6339c404c = merge-tree 6c6fdc94e x 27e53ec3a.\n",
    "# cells per Wednesday's 11:59:12Z ruling, completeness). fd81a75f0 = develop 27e53ec3a merged in; tree 6339c404c = merge-tree 6c6fdc94e x 27e53ec3a.\n"
    "# RE-PIN: 96d859467 = develop 3961c2add merged in (tree 92256f2df = merge-tree fd81a75f0 x 3961c2add); e4624218b = the PRE-GATE FIX (Wednesday 13:51:51Z):\n"
    "# routes/platform.ts authHeaders forwards req.headers.authorization, never rawAuthorization (register-connector sent the caller's Bearer to /api/tenants,\n"
    "# /api/keys, /api/audit), +4 register-connector cells (20 in the ks1215 test). Head tree 6f912843b; a fast-forward from fd81a75f0.\n")
sub("# TIER 1: gateway authentication on every mount; the source is the #1023 gate's N-1 (a revoked session's Bearer forwarded beside a valid key). A GO is NOT a\n# merge authorisation: the merge waits for Kam's tap.\n",
    "# TIER 1: gateway authentication on every mount; the source is the #1023 gate's N-1 (a revoked session's Bearer forwarded beside a valid key). A GO is a gate\n# verdict: #1034 merges on WEDNESDAY'S signed GO naming the head (the TESTED grant), NOT on Kam's tap (corrected at the re-pin; exit 26 guards it).\n")
sub("# THE SHAPE, as read 23:03-23:40 AEST 2026-09-17 (git ls-remote + the PR and compare APIs agree): develop 27e53ec3a is the head merge-base AND its second\n# parent AND develop at drafting, so compare develop...head = merge_base 27e53ec3a, ahead 2, files 2 (asserted, exit 10; behind NOT asserted).\n",
    "# THE SHAPE, as re-read 01:38-01:40 AEST 2026-09-18 (git ls-remote + the PR and compare APIs agree): develop 3961c2add is the head merge-base AND the second\n# parent of 96d859467 AND origin develop, so compare develop...head = merge_base 3961c2add, status ahead, ahead 4 (6c6fdc94e, fd81a75f0, 96d859467, e4624218b),\n# behind 0, files 3 (auth.ts, platform.ts, the ks1215 test) (asserted, exit 10; behind NOT asserted). (Drafted at fd81a75f0: 27e53ec3a ahead 2 files 2.)\n")
sub("# The develop pin is judged by CONTENT — PATH BLOBS — never by develop's SHA: (a) TWENTY-FOUR files by blob at the CURRENT develop — the PR two (middleware/auth.ts\n# 6e1668362, the ks1215 test ABSENT; at a #1034 blob -> exit 19 LANDED), and what the gate runs and reads: index.ts (mount order, the rawAuthorization capture,\n# the unhandledRejection handler), routes/proxy.ts, platform.ts (authHeaders reads rawAuthorization), batch.ts,",
    "# The develop pin is judged by CONTENT — PATH BLOBS — never by develop's SHA: (a) TWENTY-FOUR files by blob at the CURRENT develop — the PR three (middleware/auth.ts\n# 6e1668362, routes/platform.ts 4550401f8, the ks1215 test ABSENT; at a #1034 blob -> exit 19 LANDED), and what the gate runs and reads: index.ts (mount order, the\n# rawAuthorization capture, the unhandledRejection handler), routes/proxy.ts, batch.ts,")
sub("# any blob nobody pinned -> exit 18; (b) if develop moved past 27e53ec3a,", "# any blob nobody pinned -> exit 18; (b) if develop moved past 3961c2add,")
sub("# exit 25: brief AND prompt must carry the MERGE ADDENDUM and require the per-finding CLOSED / STILL OPEN / NEW disposition.\n",
    "# exit 25: brief AND prompt must carry the MERGE ADDENDUM and require the per-finding CLOSED / STILL OPEN / NEW disposition.\n"
    "# exit 26: brief AND prompt must name WEDNESDAY'S signed GO as #1034's merge authority and carry no copied Kam's-tap merge condition (added at the re-pin).\n")
sub("# residual guard + output controls + bash -n): same guard set and exit codes 2..25 (19 = LANDED), re-pointed at #1034 ROUND 1, no content-cleared blob.\n",
    "# residual guard + output controls + bash -n): same guard set and exit codes 2..25 (19 = LANDED), re-pointed at #1034 ROUND 1, no content-cleared blob.\n"
    "# RE-PINNED 2026-09-18 by gatesets/2026-09-17_gate1034/repin_launcher_1034.py (asserted substitutions; backup .pre-0918-repin): head, develop, compare,\n"
    "# JUDGED LANDED blobs (platform.ts b80a8cd8d, ks1215 test 75006b5cf + the superseded 5b7431af0), report directory, verdict subject, exit 26.\n")
sub('HEAD_SHA="${QA1034_HEAD:-fd81a75f0688f6cbe1e5f79b061bb1369c88f477}"', 'HEAD_SHA="${QA1034_HEAD:-' + H + '}"')
sub("MERGE_BASE='27e53ec3aa010b50cd9b2e4a1d15cbb34605ba7d'   # the merge-base of the head with develop (#1029s squash), the second parent of the head merge fd81a75f0",
    "MERGE_BASE='" + D + "'   # the merge-base of the head with develop = develop itself (#1033s squash), the second parent of the merge 96d859467")
sub("DEVELOP_SHA='27e53ec3aa010b50cd9b2e4a1d15cbb34605ba7d'   # the pin = the merge-base = develop at drafting (moves judged by PATH BLOB and GUARDED paths, never by this SHA: git ls-remote 23:03:08 + 23:08:34; compare API 23:04:04 AEST)",
    "DEVELOP_SHA='" + D + "'   # the pin = the merge-base = develop at the re-pin (moves judged by PATH BLOB and GUARDED paths, never by this SHA: git ls-remote 01:38:08 + 01:40:22; compare API 01:38:38 AEST 2026-09-18)")
sub("REPORT_DIR='/Volumes/DevMASTER/!CODING/Testing Agent MAIN/projects/secuura/reports/2026-09-17-ks1215-1034-fd81a75f0-tier1-r1/'",
    "REPORT_DIR='/Volumes/DevMASTER/!CODING/Testing Agent MAIN/projects/secuura/reports/2026-09-18-ks1215-1034-e4624218b-tier1-r1/'")
sub("# develop...#1034 = 27e53ec3a ahead 2 files 2 (behind 0 at draft close; behind deliberately not asserted).",
    "# develop...#1034 = 3961c2add ahead 4 files 3 (behind 0 at the re-pin; behind deliberately not asserted). Drafted at fd81a75f0: 27e53ec3a ahead 2 files 2.")
sub('[ "$COMPARE" = "$MERGE_BASE ahead=2 files=2" ] || { echo "REFUSING: #1034 develop...head reads \'$COMPARE\', brief pins \'$MERGE_BASE ahead=2 files=2\'" >&2; exit 10; }',
    '[ "$COMPARE" = "$MERGE_BASE ahead=4 files=3" ] || { echo "REFUSING: #1034 develop...head reads \'$COMPARE\', brief pins \'$MERGE_BASE ahead=4 files=3\'" >&2; exit 10; }')
sub('  A + "src/__tests__/ks1215-the-connector-branch-never-carries-the-callers-bearer.test.ts": ({"ABSENT": DV}, {"5b7431af0fbb203e7582d8f188eca3f15d5d05fe": "#1034 own"}),',
    '  A + "src/__tests__/ks1215-the-connector-branch-never-carries-the-callers-bearer.test.ts": ({"ABSENT": DV}, {"75006b5cf50fb8b42a5e7588a1d622b9168c1b07": "#1034 own", "5b7431af0fbb203e7582d8f188eca3f15d5d05fe": "#1034 own superseded fd81a75f0"}),')
sub('  A + "src/routes/platform.ts":                                          ({"4550401f8d7d76afa848855cdf7558a35fd02de0": DV}, {}),',
    '  A + "src/routes/platform.ts":                                          ({"4550401f8d7d76afa848855cdf7558a35fd02de0": DV}, {"b80a8cd8d4e1af5a944817227f5ee6612c793954": "#1034 own"}),')
sub('# No REGION judgement: every file is judged by exact blob (a develop move of auth.ts, index.ts or platform.ts refuses, exit 18).',
    '# No REGION judgement: every file is judged by exact blob (a develop move of auth.ts, index.ts or platform.ts refuses, exit 18; a #1034 blob, exit 19).')
sub('    print("OK " + state + " | origin develop still " + pinned + " (= the head merge-base, an ANCESTOR of the head: merged tree = the head tree 6339c404c05fcfbfa3b6505b6bfb7955303c1ccd; git ls-remote)"); sys.exit(0)',
    '    print("OK " + state + " | origin develop still " + pinned + " (= the head merge-base, an ANCESTOR of the head: merged tree = the head tree 6f912843b54cdcbcc7e6398d6766398f0e0c5ca9; git ls-remote)"); sys.exit(0)')
sub('tail = "the gate merges the then-current develop onto fd81a75f0 in its own clone, asserts the merged services/api-gateway/src and shared subtrees equal the head, or re-runs the real-gateway matrix, the tamper table and the suites on the MERGED tree; names the merged-tree OID, drafter 27e53ec3a -> 6339c404c = the head tree (brief items 1, 3, 5, 6)"',
    'tail = "the gate merges the then-current develop onto e4624218b in its own clone, asserts the merged services/api-gateway/src and shared subtrees equal the head, or re-runs the real-gateway matrix, the tamper table and the suites on the MERGED tree; names the merged-tree OID, re-pinner 3961c2add -> 6f912843b = the head tree (brief items 1, 3, 5, 6)"')
sub("grep -qF '[QA -> Wednesday] TIER 1 GATE #1034 (KS-1215) fd81a75f0' \"$PROMPT_FILE\"", "grep -qF '[QA -> Wednesday] TIER 1 GATE #1034 (KS-1215) e4624218b' \"$PROMPT_FILE\"")
sub('  || { echo "REFUSING: brief or prompt does not carry the MERGE ADDENDUM and the per-finding CLOSED / STILL OPEN / NEW disposition — the merge seat equality targets and the In Progress hold ride on it" >&2; exit 25; }\n',
    '  || { echo "REFUSING: brief or prompt does not carry the MERGE ADDENDUM and the per-finding CLOSED / STILL OPEN / NEW disposition — the merge seat equality targets and the In Progress hold ride on it" >&2; exit 25; }\n'
    "grep -qiF \"WEDNESDAY'S signed GO\" \"$PROMPT_FILE\" && grep -qiF \"WEDNESDAY'S signed GO\" \"$BRIEF\" && ! grep -qiE \"waits for Kam.s tap|on Kam.s tap only\" \"$PROMPT_FILE\" \"$BRIEF\" \\\n"
    "  || { echo \"REFUSING: brief or prompt does not name WEDNESDAY'S signed GO as the #1034 merge authority, or carries a copied Kam's-tap merge condition (that is #1032's, not this PR's)\" >&2; exit 26; }\n")
sub('  echo "  brief and prompt carry the MERGE ADDENDUM and require CLOSED / STILL OPEN / NEW per finding"\n',
    '  echo "  brief and prompt carry the MERGE ADDENDUM and require CLOSED / STILL OPEN / NEW per finding"\n  echo "  brief and prompt name WEDNESDAY\'S signed GO as the merge authority; no copied Kam\'s-tap merge condition"\n')
sub("# Exit: 0 launched (or guards passed under --check) · 2..25 a guard refused", "# Exit: 0 launched (or guards passed under --check) · 2..26 a guard refused")
# residual guard: old SHAs may appear only in the history comment lines (start with '#')
bad = [(i + 1, l[:120]) for i, l in enumerate(s.split('\n')) if re.search(r'fd81a75f0|27e53ec3a|6339c404c|5b7431af0', l) and not l.lstrip().startswith('#') and '#1034 own superseded fd81a75f0' not in l]
print('residual old-pin tokens outside comments:', bad)
assert not bad
assert "waits for Kam's tap" not in s and "on Kam's tap only" not in s  # run 1 asserted 'waits for Kam', which the exit-26 guard's own regex (Kam.s) contains
open(L, 'w').write(s)
p = subprocess.run(['bash', '-n', L], capture_output=True, text=True); print('bash -n rc', p.returncode, p.stderr.strip())
q = s[s.index("<<'PY'"):]
for tag in ('PY', 'PYJ'):
    a = s.index("<<'%s'\n" % tag) ; b = s.index('\n%s\n' % tag, a)
    body = s[a:b]; print('heredoc', tag, 'apostrophes', body.count("'") - 2 if tag else 0, 'parens', body.count('('), body.count(')'))
print('launcher sha256', hashlib.sha256(s.encode()).hexdigest()[:16], 'lines', s.count('\n'), 'at', datetime.datetime.now().astimezone().strftime('%H:%M:%S %Z'))
