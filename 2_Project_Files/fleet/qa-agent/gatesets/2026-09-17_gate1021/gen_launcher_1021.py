#!/usr/bin/env python3
"""gen_launcher_1021.py — derive launch_qa_secuura_ks1211_1021.sh from the sibling TIER 2 launcher launchers/launch_qa_secuura_ks769_1020.sh
(same guard family: head on origin exit 6, compare exit 10/13, develop judged BY CONTENT exit 18/19, head SHA named in brief+prompt exit 20,
TTY exit 21) by ASSERTED substitutions: every anchor must occur exactly as often as stated, or the generator refuses and writes nothing.
Then a RESIDUAL GUARD (any token of the source gate left, after stripping the one permitted template-name mention, is a refusal),
output controls ('#1021' ENUMERATED first with --enumerate, which writes only to the scratch path given), PY/PYJ heredoc apostrophe/paren
parity, no git write verbs, no control bytes, bash -n. Never overwrites an existing output without a .pre-* copy.
Usage: gen_launcher_1021.py <template launcher> <output launcher> [--enumerate]
Exit: 0 written · 1 an anchor/control count disagreed · 2 a residual token survived · 3 bash -n failed"""
import datetime, hashlib, os, re, shutil, subprocess, sys

src_path, out_path = sys.argv[1], sys.argv[2]
ENUMERATE = '--enumerate' in sys.argv[3:]
s = open(src_path, encoding='utf-8').read()
def refuse(msg, code):
    print('REFUSING: ' + msg, file=sys.stderr); sys.exit(code)

HEAD = '742e1c6080f2527973268146611930e4a70edef2'
BASE = 'f8c7aaa39dabfe6a3916e5be55d9ccd752e7d8ed'     # the PR parent = the merge-base (develop when the PR was cut)
DEVELOP = '581c9db0db4201c42cbbf702f339b750989acdb1'  # origin develop at 17:54:41 AEST: #1019's squash (KS-1187), a child of BASE, 3 api-gateway files
OLD_HEAD = '71bd80a35b406b9c99c7b96955a7521032d33c20'
OLD_BASE = 'd7e95cd9f153e9036ed77935a73c93504fa6e3dc'
BRANCH = 'refs/heads/feature/ks-1211-bump-colord'
STEM = '2026-09-17_secuura-1021-ks1211-colord-tier2'
OLD_STEM = '2026-09-17_secuura-1020-ks769-tier2'
TEMPLATE_NAME = 'launch_qa_secuura_ks769_1020.sh'
COUNT_1021 = None if ENUMERATE else int(os.environ.get('COUNT_1021', '-1'))  # MEASURED by --enumerate first; passed in, never guessed

NEW_HEADER = '''#!/bin/bash
# launch_qa_secuura_ks1211_1021.sh — cross-project QA agent, ONE TIER 2 ROUND 1 gate over Secuura/Blockchain PR #1021
# (KS-1211, Seat B, row 6 of the audit-baseline fix work, GHSA-2wm5-q62r-hmrv colord) @ 742e1c6080f2527973268146611930e4a70edef2 —
# ONE commit on f8c7aaa39, THREE files: colord 2.9.3 -> 2.10.0 in systemTest/akto/package-lock.json and
# systemTest/api-explorer/package-lock.json (declarer stylelint ^2.9.3, dev-only), and the colord row removed from
# Blockchain/Dev/scripts/audit/audit-baseline.json (38 -> 37). No manifest.
#
# THE SHAPE, as read 17:46-17:56 AEST 2026-09-17 (git ls-remote + the compare API): the head parent is f8c7aaa39. origin develop was
# f8c7aaa39 at 17:46 and MOVED to 581c9db0d (#1019, KS-1187, api-gateway only: proxy.ts + two tests) by 17:54. compare develop...head =
# merge_base f8c7aaa39, status ahead, ahead 1, files 3 (behind 0 at 17:48, behind 1 after #1019). The
# compare is asserted as merge_base + ahead + files (exit 10); `behind` is deliberately NOT asserted, so a develop that moves on does not
# trip this guard — the develop arm judges the move by CONTENT.
#
# The develop pin is judged by CONTENT, not bare: (a) THIRTEEN files by blob at the CURRENT develop — the three PR files
# (audit-baseline.json base 03d1680e3 / own c73fcebed, the akto lock base 6b348adcc / own c4d30077f, the api-explorer lock base 8be03ee9c /
# own 78589de7e; an own blob -> exit 19 LANDED), the two harness package.json, audit-locks.mjs, audit-gate.mjs, lock-discovery.mjs,
# baseline-contract.mjs, scripts/audit/package.json, preflight.sh, lockfile-cleanroom.sh and systemTest/CLAUDE.md (the harness quality-gate
# rule) — any blob nobody pinned -> exit 18; (b) if develop moved past f8c7aaa39, the compare pinned...develop REFUSES (exit 18) only when the
# delta touches a GUARDED path — anything under Blockchain/Dev/scripts/audit/ or Blockchain/Dev/scripts/preflight/, either harness
# package.json or package-lock.json, systemTest/CLAUDE.md, or .githooks/pre-push — or cannot be judged; anything else proceeds and the gate
# re-derives every count on the merged tree. Seat B's next row PRs all edit audit-baseline.json, so one of them landing first REFUSES here
# by design: re-pin deliberately. DEV_CONTENT_ALLOWED is empty.
#
# exit 21: the LAUNCH path refuses when stdin is not a TTY. This launcher execs an interactive agent; run it in a cockpit
# pane, never inside a Bash tool. `--check` still runs headless (it launches nothing).
#
# Adapted from launch_qa_secuura_ks769_1020.sh by gen_launcher_1021.py (asserted substitutions + residual guard + output
# controls + bash -n): same guards and exit codes, re-pointed at #1021. Exit codes 2..21 (19 = LANDED).
# Written by the generator because it contains a legitimate directory change.
#
# Usage: launch_qa_secuura_ks1211_1021.sh [--check]
# Exit: 0 launched (or guards passed under --check) · 2..21 a guard refused
'''
marker = 'set -u\n'
if s.count(marker) != 1: refuse('header marker set -u count %d' % s.count(marker), 1)
s = NEW_HEADER + s[s.index(marker):]

A = 'scripts/audit/'
J = lambda *lines: '\n'.join(lines)
NEW_JUDGED = J(
 '# file -> (develop-OK blobs {blob: label}, LANDED blobs {blob: label})',
 'JUDGED = {',
 '  D + "' + A + 'audit-baseline.json":         ({"03d1680e3c7a87f8df70e71082b67775536acde5": "base"}, {"c73fcebeda52cab362533193a961b661010a92b3": "#1021 own"}),',
 '  "systemTest/akto/package-lock.json":         ({"6b348adcccdf1c3bc7ff216eb4936c2d057a7fd0": "base"}, {"c4d30077f8857e9579897097a6fd362e8ed367f1": "#1021 own"}),',
 '  "systemTest/api-explorer/package-lock.json": ({"8be03ee9cd6d388e630cb153535da4a310521a5e": "base"}, {"78589de7e1165c64ef74707fdc75e1515fd6eae5": "#1021 own"}),',
 '  "systemTest/akto/package.json":              ({"3aecaf4852620ea29dcf4d0473761111cbbf92f6": "base"}, {}),',
 '  "systemTest/api-explorer/package.json":      ({"46141226323996c6a24fb16a01155395e5c959cf": "base"}, {}),',
 '  D + "' + A + 'audit-locks.mjs":             ({"aff23b0420ced863884787443a35f28cf727bd09": "base"}, {}),',
 '  D + "' + A + 'audit-gate.mjs":              ({"8e236ee70ce1a4634552596fb86fcffce234f221": "base"}, {}),',
 '  D + "' + A + 'lock-discovery.mjs":          ({"3dd903b527f26c758cc1da84b10cc0a0db3b1d46": "base"}, {}),',
 '  D + "' + A + 'baseline-contract.mjs":       ({"2504d9a28dc017fcaabfc88248bf1c64431eb38a": "base"}, {}),',
 '  D + "' + A + 'package.json":                ({"d5977b6a13638558ef57e8c294809d7ada8be6cd": "base"}, {}),',
 '  D + "scripts/preflight/preflight.sh":       ({"28d3636c13a4259bbdade8b15ac527cbe93742c3": "base"}, {}),',
 '  D + "scripts/preflight/lockfile-cleanroom.sh": ({"518bffeeaf4a3c47a4660f594f822f34e26c2d15": "base"}, {}),',
 '  "systemTest/CLAUDE.md":                      ({"357015b941af9e8dfcbb2e159f150dadbcde6e27": "base"}, {}),',
 '}\n')
NEW_GUARDED = J(
 'GUARDED = [D + "scripts/audit/",',
 '           D + "scripts/preflight/",',
 '           "systemTest/akto/package.json",',
 '           "systemTest/akto/package-lock.json",',
 '           "systemTest/api-explorer/package.json",',
 '           "systemTest/api-explorer/package-lock.json",',
 '           "systemTest/CLAUDE.md",',
 '           ".githooks/pre-push"]\n')

def block(start, end_marker):
    if s.count(start) != 1: refuse('block start %r count %d' % (start[:50], s.count(start)), 1)
    i = s.find(start); j = s.find(end_marker, i)
    if j < 0: refuse('block end %r not found' % end_marker[:40], 1)
    return s[i:j + len(end_marker)]
old_judged = block('# file -> (develop-OK blobs {blob: label}, LANDED blobs {blob: label})', '}\n')
old_guarded = block('GUARDED = [D + "scripts/audit/",', '".githooks/pre-push"]\n')

subs = [
    (old_judged, NEW_JUDGED, 1),
    (old_guarded, NEW_GUARDED, 1),
    ('QA1020_BRIEF', 'QA1021_BRIEF', 2),
    ('QA1020_PROMPT', 'QA1021_PROMPT', 2),
    ('QA1020_HEAD', 'QA1021_HEAD', 2),
    (OLD_STEM, STEM, 3),
    ('refs/heads/chore/audit-fuse-mobile-tree-dormant-redate', BRANCH, 1),
    (OLD_HEAD, HEAD, 1),
    ("MERGE_BASE='" + OLD_BASE + "'   # the merge-base of the head with develop = the PR parent (the KS-1195 #1017 squash; develop has not moved)",
     "MERGE_BASE='" + BASE + "'   # the merge-base of the head with develop = the PR parent (develop moved on to #1019, api-gateway only)", 1),
    ("DEVELOP_SHA='" + OLD_BASE + "'   # develop at draft time = the PR parent itself (ls-remote 15:42:00, compare API 15:46:12 AEST)",
     "DEVELOP_SHA='" + DEVELOP + "'   # develop at draft time = #1019's squash (KS-1187), a child of the PR parent, 3 api-gateway files, 0 guarded (ls-remote 17:54:41 AEST)", 1),
    ('echo "REFUSING: #1020 — $HEAD_SHA is not at', 'echo "REFUSING: #1021 — $HEAD_SHA is not at', 1),
    ('# develop...#1020 = d7e95cd9f ahead 1 files 1 (behind 0 at draft time — deliberately not asserted).',
     '# develop...#1021 = f8c7aaa39 ahead 1 files 3 (behind 0 at draft time — deliberately not asserted).', 1),
    ('ahead=1 files=1', 'ahead=1 files=3', 2),
    ('''{ echo "REFUSING: #1020 develop...head reads''', '''{ echo "REFUSING: #1021 develop...head reads''', 1),
    ('# The develop pin, judged by CONTENT (see the header): twelve files by blob at the CURRENT develop, then — if develop',
     '# The develop pin, judged by CONTENT (see the header): thirteen files by blob at the CURRENT develop, then — if develop', 1),
    ('" — #1020 has landed; this brief is stale")', '" — #1021 has landed; this brief is stale")', 1),
    ('" (= the PR parent, the KS-1195 #1017 squash; git ls-remote)")', '" (#1019 squash on the PR parent, api-gateway only; git ls-remote)")', 1),
    ('# pinned here. EMPTY for this gate: at draft time 15:46 AEST no open PR touched a guarded path (PR files API, 20 open PRs),',
     '# pinned here. EMPTY for this gate: at draft time 17:48 AEST no open PR shared a file with #1021 (PR files API, 21 open PRs),', 1),
    ('tail = "the gate merges the then-current develop onto 71bd80a35 in its own clone, runs the audit legs on the MERGED tree beside the base and head trees, names the delta and re-derives every count and the fuse census (brief item 6)"',
     'tail = "the gate merges the then-current develop onto 742e1c608 in its own clone, re-runs the lock parse and both audit gates on the MERGED tree beside the base and head trees, and names the delta (brief item 5)"', 1),
    ('— disjoint from the GUARDED list (Blockchain/Dev/scripts/audit/, scripts/preflight/preflight.sh, the Dev package.json, .githooks/pre-push); %s"',
     '— disjoint from the GUARDED list (Blockchain/Dev/scripts/audit/, Blockchain/Dev/scripts/preflight/, the two harness package.json and package-lock.json, systemTest/CLAUDE.md, .githooks/pre-push); %s"', 1),
    ('echo "  head on origin: #1020 $HEAD_SHA at $BRANCH"', 'echo "  head on origin: #1021 $HEAD_SHA at $BRANCH"', 1),
    ('echo "  compare (GitHub API): develop...#1020 = $COMPARE"', 'echo "  compare (GitHub API): develop...#1021 = $COMPARE"', 1),
]
for old, new, n in subs:
    c = s.count(old)
    if c != n: refuse('anchor %r occurs %d times, expected %d' % (old[:70], c, n), 1)
    s = s.replace(old, new)

permitted = 'Adapted from ' + TEMPLATE_NAME
if s.count(permitted) != 1: refuse('permitted template mention count %d' % s.count(permitted), 1)
body = s.replace(permitted, 'Adapted from <template>')
residual = ['1020', '71bd80a3', 'd7e95cd9', 'ks769', 'KS-769', 'KS-1195', '#1017', 'Dormant', 'dormant', 'fuse was', 'mobile', 'twelve', 'TWELVE',
            '15:42', '15:46', 'expected-case-count', 'gate-exit-codes', 'lock-discovery.test', 'baseline-contract.test', '769b7adbd', 'the Dev package.json']
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
        if '#1021' in l: print('#1021 at line %d: %s' % (i, l[:110]))
    print('ENUMERATED count #1021 = %d (scratch copy written to %s; nothing written to launchers/)' % (s.count('#1021'), out_path)); sys.exit(0)

controls = [
    ('HEAD_SHA="${QA1021_HEAD:-' + HEAD + '}"', 1), ("MERGE_BASE='" + BASE + "'", 1), ("DEVELOP_SHA='" + DEVELOP + "'", 1),
    ("BRANCH='" + BRANCH + "'", 1), (STEM + '.md', 2), (STEM + '.prompt.txt', 1),
    ('exit 2;', 1), ('exit 3;', 1), ('exit 4;', 1), ('exit 5;', 1), ('exit 6', 1), ('exit 7;', 1), ('exit 8;', 1), ('exit 9;', 1),
    ('exit 10;', 1), ('exit 11;', 1), ('exit 12;', 1), ('exit 13;', 1), ('exit 14;', 1), ('exit 15;', 1), ('exit 16;', 2), ('exit 17;', 1),
    ('exit 18; }', 1), ('exit 18 ;;', 1), ('exit 19 ;;', 1), ('exit 20;', 1), ('exit 21;', 1),
    ('DEV_CONTENT_ALLOWED = {', 1), ('print("LANDED ', 1), ('print("GUARDED ', 2), ('print("UNJUDGEABLE ', 3), ('LANDED*)', 1), ('OK*)', 1),
    ('03d1680e3c7a87f8df70e71082b67775536acde5', 1), ('c73fcebeda52cab362533193a961b661010a92b3', 1), ('6b348adcccdf1c3bc7ff216eb4936c2d057a7fd0', 1),
    ('c4d30077f8857e9579897097a6fd362e8ed367f1', 1), ('8be03ee9cd6d388e630cb153535da4a310521a5e', 1), ('78589de7e1165c64ef74707fdc75e1515fd6eae5', 1),
    ('3aecaf4852620ea29dcf4d0473761111cbbf92f6', 1), ('46141226323996c6a24fb16a01155395e5c959cf', 1), ('aff23b0420ced863884787443a35f28cf727bd09', 1),
    ('8e236ee70ce1a4634552596fb86fcffce234f221', 1), ('3dd903b527f26c758cc1da84b10cc0a0db3b1d46', 1), ('2504d9a28dc017fcaabfc88248bf1c64431eb38a', 1),
    ('d5977b6a13638558ef57e8c294809d7ada8be6cd', 1), ('28d3636c13a4259bbdade8b15ac527cbe93742c3', 1), ('518bffeeaf4a3c47a4660f594f822f34e26c2d15', 1),
    ('357015b941af9e8dfcbb2e159f150dadbcde6e27', 1),
    ('ahead=1 files=3', 2), ('[ -t 0 ]', 1), ('exec claude --dangerously-skip-permissions --model opus', 1),
    ('git -C "$REPO"', 2), ('set -u', 1), ('MAIL YOUR VERDICT', 1), ('NEVER print a credential value', 1), ('no memory maintenance', 1),
    ("grep -q 'TIER 2'", 2), ("grep -q 'ROUND 1'", 2), ('GUARDED = [D + "scripts/audit/",', 1), ('".githooks/pre-push"]', 1),
    ('#1021', COUNT_1021),
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
