#!/usr/bin/env python3
"""gen_launcher_1009.py — derive launch_qa_secuura_ks864_1009.sh from the sibling TIER 2 launcher launchers/launch_qa_secuura_ks864_1007.sh
(the same shape: head parent != develop, compare diverged; guard family head on origin exit 6, compare exit 10/13, develop judged BY CONTENT exit
18/19, head SHA named in brief+prompt exit 20, TTY exit 21) by ASSERTED substitutions: every anchor must occur exactly as often as stated, or
the generator refuses and writes nothing. Then a RESIDUAL GUARD (any token of the source gate left anywhere, after stripping the one permitted
template-name mention, is a refusal), output controls (every count measured against the composed text; '#1009' ENUMERATED first with
--enumerate, which writes only to the scratch path given), PY/PYJ-heredoc apostrophe/paren parity, no git write verbs, no control bytes,
bash -n. Never overwrites an existing output without a .pre-* copy.
Usage: gen_launcher_1009.py <template launcher> <output launcher> [--enumerate]
Exit: 0 written · 1 an anchor/control count disagreed · 2 a residual token survived · 3 bash -n failed"""
import datetime, hashlib, os, re, shutil, subprocess, sys

src_path, out_path = sys.argv[1], sys.argv[2]
ENUMERATE = '--enumerate' in sys.argv[3:]
s = open(src_path, encoding='utf-8').read()
def refuse(msg, code):
    print('REFUSING: ' + msg, file=sys.stderr); sys.exit(code)

HEAD = '6ec0cb19834407887daa7bf5994f2da169abd30e'
BASE = '0308b7a0447a2c01c12aad358c9b4d04a5178210'     # the PR parent = the merge-base (the KS-864 parts A+B squash)
DEVELOP = '73d3fcb902d2a78fe68a4349903ff6c6bd24d4d5'  # develop at draft time = the KS-844 squash, a child of the base, 0 api-gateway files
BRANCH = 'refs/heads/feature/ks-864-f1-portal-env-var-cells'
STEM = '2026-09-17_secuura-1009-ks864-tier2'
OLD_STEM = '2026-09-17_secuura-1007-ks864-tier2'
TEMPLATE_NAME = 'launch_qa_secuura_ks864_1007.sh'
COUNT_1009 = None if ENUMERATE else int(os.environ.get('COUNT_1009', '-1'))  # MEASURED by --enumerate first; passed in, never guessed

NEW_HEADER = '''#!/bin/bash
# launch_qa_secuura_ks864_1009.sh — cross-project QA agent, ONE TIER 2 ROUND 1 gate over Secuura/Blockchain PR #1009
# (KS-864, the tier-2 follow-up F-1 of the parts A+B gate, Seat A) @ 6ec0cb19834407887daa7bf5994f2da169abd30e — ONE commit on 0308b7a04,
# 3 files, all services/api-gateway/src/__tests__: a new 6-cell ks864c-portal-env-vars.test.ts (each portal env var under NODE_ENV
# staging and development) and the P-1 type fixes in ks864a/b. TEST ONLY: system-status.ts blob 956083916 at base, head and develop.
#
# THE SHAPE, as read 01:28-03:04 AEST 2026-09-17 (git + the compare API agree): the head parent is 0308b7a04 (the KS-864 parts A+B squash);
# develop is 73d3fcb90 (the KS-844 squash, a child of 0308b7a04: 2 packages/shared test files + 3 demo-service files, 0 api-gateway files).
# compare develop...head = merge_base 0308b7a04, status diverged, ahead 1, behind 1, files 3. The compare is asserted as merge_base + ahead +
# files (exit 10); `behind` is deliberately NOT asserted, so a develop that moves on does not trip this guard — the develop arm judges the
# move by CONTENT.
#
# The develop pin is judged by CONTENT, not bare: (a) NINE files by blob at the CURRENT develop — ks864a (base eb6ea8c22; the PR own
# 6d119d23d -> exit 19 LANDED), ks864b (base a073703d2; own 3cfb1da89 -> exit 19 LANDED), routes/system-status.ts (956083916, what the cells
# pin), api-gateway src/index.ts, vitest.config.ts, vitest.setup.ts, package.json, tsconfig.json (the exclude the including tsc overrides),
# and the Dev eslint.config.mjs — any blob nobody pinned -> exit 18 (the new ks864c is NOT judged by blob: absent on develop, and ks864a/b
# already detect a landing); (b) if develop moved past 73d3fcb90, the compare pinned...develop REFUSES (exit 18) only when the delta touches
# a GUARDED path — those nine files, ks864c, or the Dev lockfile — or cannot be judged; anything else (the file-disjoint sibling lane PRs
# landing) proceeds and the gate re-derives the api-gateway denominator on the merged tree.
# DEV_CONTENT_ALLOWED is empty: dependabot #649/#575 touch api-gateway package.json and the Dev lockfile — if one lands, this
# launcher refuses and the brief is re-pinned deliberately.
#
# exit 21: the LAUNCH path refuses when stdin is not a TTY. This launcher execs an interactive agent; run it in a cockpit
# pane, never inside a Bash tool. `--check` still runs headless (it launches nothing).
#
# Adapted from launch_qa_secuura_ks864_1007.sh by gen_launcher_1009.py (asserted substitutions + residual guard + output
# controls + bash -n): same guards and exit codes, re-pointed at #1009. Exit codes 2..21 (19 = LANDED).
# Written by the generator because it contains a legitimate directory change.
#
# Usage: launch_qa_secuura_ks864_1009.sh [--check]
# Exit: 0 launched (or guards passed under --check) · 2..21 a guard refused
'''
marker = 'set -u\n'
if s.count(marker) != 1: refuse('header marker set -u count %d' % s.count(marker), 1)
s = NEW_HEADER + s[s.index(marker):]

J = lambda *lines: '\n'.join(lines)
NEW_JUDGED = J(
 '# file -> (develop-OK blobs {blob: label}, LANDED blobs {blob: label})',
 'JUDGED = {',
 '  D + "services/api-gateway/src/__tests__/ks864a-dead-estate-helper.test.ts":  ({"eb6ea8c22abcced1af61263edc7c0caeb332cdce": "base"}, {"6d119d23d71f2e97fd3d48419e46a0a4296d3dd7": "#1009 own"}),',
 '  D + "services/api-gateway/src/__tests__/ks864b-dead-estate-portals.test.ts": ({"a073703d2b532e86c18c4c47eaa2b98b14cea0c1": "base"}, {"3cfb1da89406f67fcd4d1a4e7499adb7b46fd456": "#1009 own"}),',
 '  D + "services/api-gateway/src/routes/system-status.ts": ({"956083916a7a1a0bbf16252017cbe8f5f90f6436": "base"}, {}),',
 '  D + "services/api-gateway/src/index.ts":                ({"6f38c819e48162e3179aaf557085766f91beecc1": "base"}, {}),',
 '  D + "services/api-gateway/vitest.config.ts":            ({"5888e0b320d934f6f434e0e5ca3c74a995cecc02": "base"}, {}),',
 '  D + "services/api-gateway/vitest.setup.ts":             ({"22c1107683b8192df3bfd3e929aa94aff3dc7d45": "base"}, {}),',
 '  D + "services/api-gateway/package.json":                ({"841d8c6adcd71e885c01e65c22da9418daff276a": "base"}, {}),',
 '  D + "services/api-gateway/tsconfig.json":               ({"c981e6a92fdd2417fa35070eb979c5f1c77ffbcd": "base"}, {}),',
 '  D + "eslint.config.mjs":                                ({"8c5374c6022eb0a3f449f41a570db61294aa63f1": "base"}, {}),',
 '}\n')
NEW_GUARDED = J(
 'GUARDED = [D + "services/api-gateway/src/__tests__/ks864a-dead-estate-helper.test.ts",',
 '           D + "services/api-gateway/src/__tests__/ks864b-dead-estate-portals.test.ts",',
 '           D + "services/api-gateway/src/__tests__/ks864c-portal-env-vars.test.ts",',
 '           D + "services/api-gateway/src/routes/system-status.ts",',
 '           D + "services/api-gateway/src/index.ts",',
 '           D + "services/api-gateway/vitest.config.ts",',
 '           D + "services/api-gateway/vitest.setup.ts",',
 '           D + "services/api-gateway/package.json",',
 '           D + "services/api-gateway/tsconfig.json",',
 '           D + "eslint.config.mjs",',
 '           D + "package-lock.json"]\n')

def block(start, end_marker):
    if s.count(start) != 1: refuse('block start %r count %d' % (start[:50], s.count(start)), 1)
    i = s.find(start); j = s.find(end_marker, i)
    if j < 0: refuse('block end %r not found' % end_marker[:40], 1)
    return s[i:j + len(end_marker)]
old_judged = block('# file -> (develop-OK blobs {blob: label}, LANDED blobs {blob: label})', '}\n')
old_guarded = block('GUARDED = [D + "services/api-gateway/src/routes/system-status.ts",', 'D + "package-lock.json"]\n')

subs = [
    (old_judged, NEW_JUDGED, 1),
    (old_guarded, NEW_GUARDED, 1),
    ('QA1007_BRIEF', 'QA1009_BRIEF', 2),
    ('QA1007_PROMPT', 'QA1009_PROMPT', 2),
    ('QA1007_HEAD', 'QA1009_HEAD', 2),
    (OLD_STEM, STEM, 3),
    ('refs/heads/feature/ks-864-ornith-dead-estate-pointers', BRANCH, 1),
    ('b28ed490ada70df2056763f4512c98443285a694', HEAD, 1),
    ("MERGE_BASE='40fe4db6963cd11dba06bd46e0b00af39e68ef3a'   # the merge-base of the head with develop = the PR parent (the KS-932 squash; develop moved on to the #1005 squash)",
     "MERGE_BASE='" + BASE + "'   # the merge-base of the head with develop = the PR parent (the KS-864 parts A+B squash; develop moved on to the KS-844 squash)", 1),
    ("DEVELOP_SHA='93629700c3d219c1d8ca61d69150bb9b623fc1be'   # develop at draft end = the #1005 squash, a child of the base, file-disjoint from #1007 (ls-remote 00:42:59, compare API 00:43:14 AEST)",
     "DEVELOP_SHA='" + DEVELOP + "'   # develop at draft time = the KS-844 squash, a child of the base, 0 api-gateway files (ls-remote 01:28:30 and 03:03:43, compare API 01:29:57 AEST)", 1),
    ('echo "REFUSING: #1007 — $HEAD_SHA is not at', 'echo "REFUSING: #1009 — $HEAD_SHA is not at', 1),
    ('# develop...#1007 = 40fe4db69 ahead 1 files 3 (behind 1 — the #1005 squash — deliberately not asserted).',
     '# develop...#1009 = 0308b7a04 ahead 1 files 3 (behind 1 — the KS-844 squash — deliberately not asserted).', 1),
    ('''{ echo "REFUSING: #1007 develop...head reads''', '''{ echo "REFUSING: #1009 develop...head reads''', 1),
    ('# The develop pin, judged by CONTENT (see the header): seven files by blob at the CURRENT develop, then — if develop',
     '# The develop pin, judged by CONTENT (see the header): nine files by blob at the CURRENT develop, then — if develop', 1),
    ('" — #1007 has landed; this brief is stale")', '" — #1009 has landed; this brief is stale")', 1),
    ('" (the #1005 squash on the base, file-disjoint from #1007; git ls-remote)")', '" (the KS-844 squash on the base, 0 api-gateway files; git ls-remote)")', 1),
    ('# pinned here. EMPTY for this gate: at draft time 00:34 AEST no open lane PR touched a guarded path except dependabot',
     '# pinned here. EMPTY for this gate: at draft time 01:29 AEST no open lane PR touched a guarded path except dependabot', 1),
    ('tail = "the gate merges the then-current develop onto b28ed490a in its own clone, rebuilds the shared dist there, runs the api-gateway suite and the parity probe on the MERGED tree beside the base and head trees, names the delta and re-derives every count (brief items 1 and 10)"',
     'tail = "the gate merges the then-current develop onto 6ec0cb198 in its own clone, rebuilds the shared dist there, runs the api-gateway suite on the MERGED tree beside the base and head trees, names the delta and re-derives every count (brief item 6)"', 1),
    ('— disjoint from the GUARDED list (api-gateway routes/system-status.ts, src/index.ts, vitest.config.ts, vitest.setup.ts, package.json, tsconfig.json, eslint.config.mjs, the lockfile); %s"',
     '— disjoint from the GUARDED list (api-gateway ks864a/b/c tests, routes/system-status.ts, src/index.ts, vitest.config.ts, vitest.setup.ts, package.json, tsconfig.json, eslint.config.mjs, the lockfile); %s"', 1),
    ('echo "  head on origin: #1007 $HEAD_SHA at $BRANCH"', 'echo "  head on origin: #1009 $HEAD_SHA at $BRANCH"', 1),
    ('echo "  compare (GitHub API): develop...#1007 = $COMPARE"', 'echo "  compare (GitHub API): develop...#1009 = $COMPARE"', 1),
]
for old, new, n in subs:
    c = s.count(old)
    if c != n: refuse('anchor %r occurs %d times, expected %d' % (old[:70], c, n), 1)
    s = s.replace(old, new)

permitted = 'Adapted from ' + TEMPLATE_NAME
if s.count(permitted) != 1: refuse('permitted template mention count %d' % s.count(permitted), 1)
body = s.replace(permitted, 'Adapted from <template>')
residual = ['1007', '1005', 'b28ed490', '40fe4db6', '93629700', 'ornith-dead-estate', '5b39da2ee', 'KS-932', 'seven files', 'SEVEN files',
            '00:29', '00:34', '00:42:59', '00:43:14', 'parity probe', 'items 1 and 10']
hits = []
for tok in residual:
    pat = r'(?<![0-9a-fA-F])' + re.escape(tok) + r'(?![0-9a-fA-F])' if tok.isdigit() else re.escape(tok)
    for m in re.finditer(pat, body): hits.append((tok, body.count('\n', 0, m.start()) + 1))
lines = body.split('\n')
if hits:
    for tok, line in hits: print('REFUSING: residual token %r at line %d: %s' % (tok, line, lines[line - 1][:120]), file=sys.stderr)
    sys.exit(2)

if ENUMERATE:
    open(out_path, 'w', encoding='utf-8').write(s)
    for i, l in enumerate(s.split('\n'), 1):
        if '#1009' in l: print('#1009 at line %d: %s' % (i, l[:110]))
    print('ENUMERATED count #1009 = %d (scratch copy written to %s; nothing written to launchers/)' % (s.count('#1009'), out_path)); sys.exit(0)

controls = [
    ('HEAD_SHA="${QA1009_HEAD:-' + HEAD + '}"', 1), ("MERGE_BASE='" + BASE + "'", 1), ("DEVELOP_SHA='" + DEVELOP + "'", 1),
    ("BRANCH='" + BRANCH + "'", 1), (STEM + '.md', 2), (STEM + '.prompt.txt', 1),
    ('exit 2;', 1), ('exit 3;', 1), ('exit 4;', 1), ('exit 5;', 1), ('exit 6', 1), ('exit 7;', 1), ('exit 8;', 1), ('exit 9;', 1),
    ('exit 10;', 1), ('exit 11;', 1), ('exit 12;', 1), ('exit 13;', 1), ('exit 14;', 1), ('exit 15;', 1), ('exit 16;', 2), ('exit 17;', 1),
    ('exit 18; }', 1), ('exit 18 ;;', 1), ('exit 19 ;;', 1), ('exit 20;', 1), ('exit 21;', 1),
    ('DEV_CONTENT_ALLOWED = {', 1), ('print("LANDED ', 1), ('print("GUARDED ', 2), ('print("UNJUDGEABLE ', 3), ('LANDED*)', 1), ('OK*)', 1),
    ('eb6ea8c22abcced1af61263edc7c0caeb332cdce', 1), ('6d119d23d71f2e97fd3d48419e46a0a4296d3dd7', 1), ('a073703d2b532e86c18c4c47eaa2b98b14cea0c1', 1),
    ('3cfb1da89406f67fcd4d1a4e7499adb7b46fd456', 1), ('956083916a7a1a0bbf16252017cbe8f5f90f6436', 1), ('6f38c819e48162e3179aaf557085766f91beecc1', 1),
    ('5888e0b320d934f6f434e0e5ca3c74a995cecc02', 1), ('22c1107683b8192df3bfd3e929aa94aff3dc7d45', 1), ('841d8c6adcd71e885c01e65c22da9418daff276a', 1),
    ('c981e6a92fdd2417fa35070eb979c5f1c77ffbcd', 1), ('8c5374c6022eb0a3f449f41a570db61294aa63f1', 1),
    ('ahead=1 files=3', 2), ('[ -t 0 ]', 1), ('exec claude --dangerously-skip-permissions --model opus', 1),
    ('git -C "$REPO"', 2), ('set -u', 1), ('MAIL YOUR VERDICT', 1), ('NEVER print a credential value', 1), ('no memory maintenance', 1),
    ("grep -q 'TIER 2'", 2), ("grep -q 'ROUND 1'", 2), ('D + "services/api-gateway/src/__tests__/ks864c-portal-env-vars.test.ts",', 1), ('D + "package-lock.json"]', 1),
    ('#1009', COUNT_1009),
]
bad = [(k, want, s.count(k)) for k, want in controls if s.count(k) != want]
if bad: refuse('output controls %r' % bad, 1)
if 'git -C $' in s: refuse('git -C $VAR form', 1)
verbs = re.findall(r'git (?:-C "\$REPO" )?(fetch|checkout|worktree|merge-tree|merge|pull|push|reset|switch|clone)\b', s)
if verbs: refuse('git write verbs in the launcher %r' % verbs, 1)
pyj = s.split("<<'PYJ'")[1].split('PYJ\n')[0]
if pyj.count("'") % 2: refuse('odd apostrophes inside the PYJ heredoc (%d)' % pyj.count("'"), 1)
if pyj.count('(') != pyj.count(')'): refuse('unbalanced parentheses inside the PYJ heredoc (%d/%d)' % (pyj.count('('), pyj.count(')')), 1)
py = s.split("<<'PY'")[1].split('PY\n')[0]
if py.count("'") % 2: refuse('odd apostrophes inside the PY heredoc (%d)' % py.count("'"), 1)
raw = s.encode('utf-8')
if sum(1 for b in raw if (b < 0x20 and b not in (9, 10, 13)) or b == 0x7f): refuse('control bytes', 1)
if os.path.exists(out_path):
    bak = out_path + '.pre-' + datetime.datetime.now().strftime('%m%d%H%M%S')
    shutil.copyfile(out_path, bak); print('existing output copied to', bak)
open(out_path, 'w', encoding='utf-8').write(s)
os.chmod(out_path, 0o755)
rc = subprocess.run(['bash', '-n', out_path]).returncode
print(datetime.datetime.now().astimezone().strftime('%H:%M:%S %Z'), 'wrote', out_path, 'lines', s.count('\n'), 'sha256', hashlib.sha256(raw).hexdigest()[:16],
      'subs', len(subs), 'controls', len(controls), 'residual guard clean', 'bash -n rc', rc, 'pyj apostrophes', pyj.count("'"))
sys.exit(0 if rc == 0 else 3)
