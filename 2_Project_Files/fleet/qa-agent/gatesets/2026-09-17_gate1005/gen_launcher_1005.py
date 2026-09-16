#!/usr/bin/env python3
"""gen_launcher_1005.py — derive launch_qa_secuura_ks1073_1005.sh from tonight's #1004 TIER 1 launcher
(launchers/launch_qa_secuura_ks932_1004.sh — the newest guard family: head on origin exit 6, compare exit 10/13, develop judged
BY CONTENT exit 18/19, head SHA named in brief+prompt exit 20, TTY exit 21) by ASSERTED substitutions: every anchor must occur
exactly as often as stated, or the generator refuses and writes nothing. Then a RESIDUAL GUARD (any token of the source gate left
anywhere, after stripping the one permitted template-name mention, is a refusal), output controls (every count measured against
the composed text; '#1005' is ENUMERATED first with --enumerate, which writes only to the scratch path given and prints the lines),
the PY/PYJ-heredoc apostrophe/paren parity, no git write verbs, no control bytes, bash -n. Never overwrites an existing output
without a .pre-* copy.
Usage: gen_launcher_1005.py <template launcher> <output launcher> [--enumerate]
Exit: 0 written · 1 an anchor/control count disagreed · 2 a residual token survived · 3 bash -n failed"""
import datetime, hashlib, os, re, shutil, subprocess, sys

src_path, out_path = sys.argv[1], sys.argv[2]
ENUMERATE = '--enumerate' in sys.argv[3:]
s = open(src_path, encoding='utf-8').read()
def refuse(msg, code):
    print('REFUSING: ' + msg, file=sys.stderr); sys.exit(code)

HEAD = 'e5e7ff99dbc4881784ce0beacefb4e7e36c55cf9'
BASE = 'dd66863dd2858e97344652c1106d38f5e352a41b'     # the PR base = the merge-base
DEVELOP = '40fe4db6963cd11dba06bd46e0b00af39e68ef3a'  # develop at draft time = #1004's squash, a child of the base, packages/shared only
BRANCH = 'refs/heads/feature/ks-1073-ornith-tier2-statusless-carveout'
STEM = '2026-09-17_secuura-1005-ks1073-tier1'
OLD_STEM = '2026-09-16_secuura-1004-ks932-tier1'
TEMPLATE_NAME = 'launch_qa_secuura_ks932_1004.sh'
COUNT_1005 = None if ENUMERATE else 10  # MEASURED by enumeration (the drafter's placeholder was 9 — wrong): header :2 :30; body :57 :63 :76 :94 :111 :117 :176 :177 — gen_launcher.first-run-enumerate-to-scratch.out

NEW_HEADER = '''#!/bin/bash
# launch_qa_secuura_ks1073_1005.sh — cross-project QA agent, ONE TIER 1 ROUND 1 gate over Secuura/Blockchain PR #1005
# (KS-1073, Seat A) @ e5e7ff99dbc4881784ce0beacefb4e7e36c55cf9 — ONE commit on dd66863dd, 2 files under services/api-gateway:
# routes/verification.ts +15 -12 (ONE product line: the statusless on-chain carve-out made tier-1 only via the doc-level
# `_source !== 'anchor_store'` conjunct; the rest comment) and a new 3-cell test file. TIER 1: a product change on the
# verification path — the predicate that decides what a verifier is told is on-chain.
#
# THE SHAPE, as read 00:05-00:14 AEST 2026-09-17 (git + the compare API agree): the head's parent is dd66863dd (#1002's squash),
# and develop is 40fe4db69 (#1004's squash, a child of dd66863dd touching packages/shared only). compare develop...head =
# merge_base dd66863dd, status diverged, ahead 1, behind 1, files 2. The compare is asserted as merge_base + ahead + files
# (exit 10); `behind` is deliberately NOT asserted, so a develop that moves on does not trip this guard — the develop arm judges
# the move by CONTENT.
#
# The develop pin is judged by CONTENT, not bare: (a) EIGHT files by blob at the CURRENT develop — verification.ts (base
# c83a2ae27; the PR's own de34b2de7 -> exit 19 LANDED), api-gateway src/index.ts / vitest.config.ts / package.json /
# tsconfig.json, the ks1057 verify-confidence test, originate routes/documents.ts (the tier-1 document body), anchoring
# src/index.ts (formatAnchorResponse) — any blob nobody pinned -> exit 18 (the new test file is NOT judged: it is absent on
# develop, and verification.ts already detects a landing); (b) if develop moved past 40fe4db69, the compare pinned...develop
# REFUSES (exit 18) only when the delta touches a GUARDED path — services/api-gateway/src/routes/, api-gateway src/index.ts,
# the api-gateway config trio, the ks1057 test, originate routes/documents.ts, anchoring src/index.ts, eslint.config.mjs, or
# the Dev lockfile — or cannot be judged; anything else (#923's ks570 test, #995's utils/trustHeaders.ts, packages/shared)
# proceeds and the gate re-derives counts on the merged tree.
# DEV_CONTENT_ALLOWED is empty: no open lane PR touches a guarded path except dependabot #649/#575 (api-gateway package.json)
# — if one lands, this launcher refuses and the brief is re-pinned deliberately.
#
# exit 21: the LAUNCH path refuses when stdin is not a TTY. This launcher execs an interactive agent; run it in a cockpit
# pane, never inside a Bash tool. `--check` still runs headless (it launches nothing).
#
# Adapted from launch_qa_secuura_ks932_1004.sh by gen_launcher_1005.py (asserted substitutions + residual guard + output
# controls + bash -n): same guards and exit codes, re-pointed at #1005. Exit codes 2..21 (19 = LANDED).
# Written by the generator because it contains a legitimate directory change.
#
# Usage: launch_qa_secuura_ks1073_1005.sh [--check]
# Exit: 0 launched (or guards passed under --check) · 2..21 a guard refused
'''
marker = 'set -u\n'
if s.count(marker) != 1: refuse('header marker set -u count %d' % s.count(marker), 1)
s = NEW_HEADER + s[s.index(marker):]

J = lambda *lines: '\n'.join(lines)
NEW_JUDGED = J(
 '# file -> (develop-OK blobs {blob: label}, LANDED blobs {blob: label})',
 'JUDGED = {',
 '  D + "services/api-gateway/src/routes/verification.ts":                                      ({"c83a2ae27d7ef03a3c1b0c02246154894064f372": "base"}, {"de34b2de7372873d60987f8bc742df3a13140265": "#1005 own"}),',
 '  D + "services/api-gateway/src/index.ts":                                                   ({"6f38c819e48162e3179aaf557085766f91beecc1": "base"}, {}),',
 '  D + "services/api-gateway/vitest.config.ts":                                               ({"5888e0b320d934f6f434e0e5ca3c74a995cecc02": "base"}, {}),',
 '  D + "services/api-gateway/package.json":                                                   ({"841d8c6adcd71e885c01e65c22da9418daff276a": "base"}, {}),',
 '  D + "services/api-gateway/tsconfig.json":                                                  ({"c981e6a92fdd2417fa35070eb979c5f1c77ffbcd": "base"}, {}),',
 '  D + "services/api-gateway/src/__tests__/ks1057-verify-confidence-is-status-aware.test.ts": ({"aceaef1fa4fc33e8daa42f0b799e554eb4762770": "base"}, {}),',
 '  D + "services/originate/src/routes/documents.ts":                                           ({"c3a818ac8ac8de1b385540d15e3fbb23200cea30": "base"}, {}),',
 '  D + "services/anchoring/src/index.ts":                                                      ({"da4abd43292186da45c1533017fe042fa512bd43": "base"}, {}),',
 '}\n')
NEW_GUARDED = J(
 'GUARDED = [D + "services/api-gateway/src/routes/",',
 '           D + "services/api-gateway/src/index.ts",',
 '           D + "services/api-gateway/vitest.config.ts",',
 '           D + "services/api-gateway/package.json",',
 '           D + "services/api-gateway/tsconfig.json",',
 '           D + "services/api-gateway/src/__tests__/ks1057-verify-confidence-is-status-aware.test.ts",',
 '           D + "services/originate/src/routes/documents.ts",',
 '           D + "services/anchoring/src/index.ts",',
 '           D + "eslint.config.mjs",',
 '           D + "package-lock.json"]\n')
NEW_ALLOWED = J(
 '# STYLE NOTE (912r2 launcher, measured): bash scans quote/paren state THROUGH this heredoc because it sits inside a',
 '# command substitution — keep apostrophes and parentheses EVEN (this block uses none of the former), or the outer $( ) breaks.',
 '# CONTENT-JUDGED allowlist: a hit under a GUARDED path clears ONLY if the per-file blob sha in the compare is EXACTLY one',
 '# pinned here. EMPTY for this gate: at draft time 00:07 AEST no open lane PR touched a guarded path except dependabot',
 '# api-gateway package.json bumps, which must NOT clear silently, so every guarded hit falls through to GUARDED and exit 18 — re-pin deliberately.',
 'DEV_CONTENT_ALLOWED = {',
 '}\n')

def block(start, end_marker):
    i = s.find(start)
    if i < 0 or s.count(start) != 1: refuse('block start %r count %d' % (start[:50], s.count(start)), 1)
    j = s.find(end_marker, i)
    if j < 0: refuse('block end %r not found' % end_marker[:40], 1)
    return s[i:j + len(end_marker)]
old_judged = block('# file -> (develop-OK blobs {blob: label}, LANDED blobs {blob: label})', '}\n')
old_guarded = block('GUARDED = [D + "packages/shared/src/security/",', '"package-lock.json"]\n')
old_allowed = block('# STYLE NOTE (912r2 launcher, measured)', 'DEV_CONTENT_ALLOWED = {\n')
old_allowed = old_allowed + s[s.index(old_allowed) + len(old_allowed): s.index('}\n', s.index(old_allowed) + len(old_allowed)) + 2]

subs = [
    (old_judged, NEW_JUDGED, 1),
    (old_guarded, NEW_GUARDED, 1),
    (old_allowed, NEW_ALLOWED, 1),
    ('QA1004_BRIEF', 'QA1005_BRIEF', 2),
    ('QA1004_PROMPT', 'QA1005_PROMPT', 2),
    ('QA1004_HEAD', 'QA1005_HEAD', 2),
    (OLD_STEM, STEM, 3),
    ('refs/heads/feature/ks-932-ornith-timeout-bounds-dns', BRANCH, 1),
    ('6d077d3fe35cd5f3c09d394553d320e97b1abe32', HEAD, 1),
    ("MERGE_BASE='5b4f38a48aeb40c2295895aaa5cd08e273aa7a08'   # the merge-base of the head with develop = the PR base (the head is its direct child)",
     "MERGE_BASE='" + BASE + "'   # the merge-base of the head with develop = the PR base (#1002's squash; develop moved on to #1004)", 1),
    ("DEVELOP_SHA='5b4f38a48aeb40c2295895aaa5cd08e273aa7a08'   # develop at draft time = the base (read 22:56:13, 22:56:27 and 23:11:38 AEST)",
     "DEVELOP_SHA='" + DEVELOP + "'   # develop at draft time = #1004's squash, a child of the base, packages/shared only (read 00:05:37 and 00:07:38 AEST)", 1),
    ('echo "REFUSING: #1004 — $HEAD_SHA is not at', 'echo "REFUSING: #1005 — $HEAD_SHA is not at', 1),
    ('# develop...#1004 = 5b4f38a48 ahead 1 files 2.', '# develop...#1005 = dd66863dd ahead 1 files 2 (behind 1 — #1004 — deliberately not asserted).', 1),
    ('''[ "$COMPARE" = "$MERGE_BASE ahead=1 files=2" ] || { echo "REFUSING: #1004 develop...head reads '$COMPARE', brief pins '$MERGE_BASE ahead=1 files=2'" >&2; exit 10; }''',
     '''[ "$COMPARE" = "$MERGE_BASE ahead=1 files=2" ] || { echo "REFUSING: #1005 develop...head reads '$COMPARE', brief pins '$MERGE_BASE ahead=1 files=2'" >&2; exit 10; }''', 1),
    ('# The develop pin, judged by CONTENT (see the header): eleven files by blob at the CURRENT develop, then — if develop',
     '# The develop pin, judged by CONTENT (see the header): eight files by blob at the CURRENT develop, then — if develop', 1),
    ('" — #1004 has landed; this brief is stale")', '" — #1005 has landed; this brief is stale")', 1),
    ('print("OK " + state + " | origin develop still " + pinned + " (the base; git ls-remote)"); sys.exit(0)',
     'print("OK " + state + " | origin develop still " + pinned + " (#1004 squash on the base, file-disjoint from #1005; git ls-remote)"); sys.exit(0)', 1),
    ('tail = "the gate merges the then-current develop onto 6d077d3fe in its own clone, rebuilds the shared dist there, runs the packages/shared suite on the MERGED tree beside the head tree, names the delta and re-derives every count (brief item 6)"',
     'tail = "the gate merges the then-current develop onto e5e7ff99d in its own clone, rebuilds the shared dist there, runs the api-gateway suite on the MERGED tree beside the base and head trees, names the delta and re-derives every count (brief item 6)"', 1),
    ('''— disjoint from the GUARDED list (packages/shared/src/security/, shared src/index.ts + config trio, the three guard test files, originate webhooks.ts + jest.config.js + __tests__/helpers/, m365 src/index.ts, the lockfile); %s"''',
     '''— disjoint from the GUARDED list (api-gateway src/routes/, api-gateway src/index.ts + config trio, the ks1057 test, originate routes/documents.ts, anchoring src/index.ts, eslint.config.mjs, the lockfile); %s"''', 1),
    ('echo "  head on origin: #1004 $HEAD_SHA at $BRANCH"', 'echo "  head on origin: #1005 $HEAD_SHA at $BRANCH"', 1),
    ('echo "  compare (GitHub API): develop...#1004 = $COMPARE"', 'echo "  compare (GitHub API): develop...#1005 = $COMPARE"', 1),
]
for old, new, n in subs:
    c = s.count(old)
    if c != n: refuse('anchor %r occurs %d times, expected %d' % (old[:70], c, n), 1)
    s = s.replace(old, new)

permitted = 'Adapted from ' + TEMPLATE_NAME
if s.count(permitted) != 1: refuse('permitted template mention count %d' % s.count(permitted), 1)
body = s.replace(permitted, 'Adapted from <template>')
residual = ['1004', '932', 'QA1004', 'ssrf', 'webhooks', 'm365', 'jest.config', 'packages/shared/src/security', 'packages/shared suite',
            '6d077d3fe', '5b4f38a48', 'efd880010', '5a838e0d6', 'aeaf90dad', '2a226c006', '395769231', '1fd016cc2', 'afb0c0d08', '69706c1ef',
            'ffce480e4', 'c88eb97db', '735183662', '1f3a91d4f', '22:56', '22:59', '23:11', 'eleven files', 'ks914', 'timeout-bounds-dns', '#922', '#635']
hits = []
for tok in residual:
    pat = r'(?<![0-9a-fA-F])' + re.escape(tok) + r'(?![0-9a-fA-F])' if tok.isdigit() else re.escape(tok)
    for m in re.finditer(pat, body):
        hits.append((tok, body.count('\n', 0, m.start()) + 1))
# '#1004' / '1004' appear legitimately where the header and messages name develop's #1004 squash: allow ONLY lines that also say 'squash' or '#1004 —' in the behind note.
lines = body.split('\n')
hits = [(t, l) for t, l in hits if not (t == '1004' and ('squash' in lines[l - 1] or 'behind 1 — #1004' in lines[l - 1]))]
if hits:
    for tok, line in hits: print('REFUSING: residual token %r at line %d: %s' % (tok, line, lines[line - 1][:120]), file=sys.stderr)
    sys.exit(2)

if ENUMERATE:
    open(out_path, 'w', encoding='utf-8').write(s)
    for i, l in enumerate(s.split('\n'), 1):
        if '#1005' in l: print('#1005 at line %d: %s' % (i, l[:110]))
    print('ENUMERATED count #1005 = %d (scratch copy written to %s; nothing written to launchers/)' % (s.count('#1005'), out_path)); sys.exit(0)

controls = [
    ('HEAD_SHA="${QA1005_HEAD:-' + HEAD + '}"', 1), ("MERGE_BASE='" + BASE + "'", 1), ("DEVELOP_SHA='" + DEVELOP + "'", 1),
    ("BRANCH='" + BRANCH + "'", 1), (STEM + '.md', 2), (STEM + '.prompt.txt', 1),
    ('exit 2;', 1), ('exit 3;', 1), ('exit 4;', 1), ('exit 5;', 1), ('exit 6', 1), ('exit 7;', 1), ('exit 8;', 1), ('exit 9;', 1),
    ('exit 10;', 1), ('exit 11;', 1), ('exit 12;', 1), ('exit 13;', 1), ('exit 14;', 1), ('exit 15;', 1), ('exit 16;', 2), ('exit 17;', 1),
    ('exit 18; }', 1), ('exit 18 ;;', 1), ('exit 19 ;;', 1), ('exit 20;', 1), ('exit 21;', 1),
    ('DEV_CONTENT_ALLOWED = {', 1), ('print("LANDED ', 1), ('print("GUARDED ', 2), ('print("UNJUDGEABLE ', 3), ('LANDED*)', 1), ('OK*)', 1),
    ('c83a2ae27d7ef03a3c1b0c02246154894064f372', 1), ('de34b2de7372873d60987f8bc742df3a13140265', 1), ('6f38c819e48162e3179aaf557085766f91beecc1', 1),
    ('5888e0b320d934f6f434e0e5ca3c74a995cecc02', 1), ('841d8c6adcd71e885c01e65c22da9418daff276a', 1), ('c981e6a92fdd2417fa35070eb979c5f1c77ffbcd', 1),
    ('aceaef1fa4fc33e8daa42f0b799e554eb4762770', 1), ('c3a818ac8ac8de1b385540d15e3fbb23200cea30', 1), ('da4abd43292186da45c1533017fe042fa512bd43', 1),
    ('ahead=1 files=2', 2), ('[ -t 0 ]', 1), ('exec claude --dangerously-skip-permissions --model opus', 1),
    ('git -C "$REPO"', 2), ('set -u', 1), ('MAIL YOUR VERDICT', 1), ('NEVER print a credential value', 1), ('no memory maintenance', 1),
    ("grep -q 'TIER 1'", 2), ("grep -q 'ROUND 1'", 2), ('D + "services/api-gateway/src/routes/",', 1), ('D + "package-lock.json"]', 1),
    ('#1005', COUNT_1005),
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
