#!/usr/bin/env python3
"""gen_launcher_1020.py — derive launch_qa_secuura_ks769_1020.sh from the sibling TIER 2 launcher launchers/launch_qa_secuura_ks864_1009.sh
(same guard family: head on origin exit 6, compare exit 10/13, develop judged BY CONTENT exit 18/19, head SHA named in brief+prompt exit 20,
TTY exit 21) by ASSERTED substitutions: every anchor must occur exactly as often as stated, or the generator refuses and writes nothing.
Then a RESIDUAL GUARD (any token of the source gate left anywhere, after stripping the one permitted template-name mention, is a refusal),
output controls ('#1020' ENUMERATED first with --enumerate, which writes only to the scratch path given), PY/PYJ heredoc apostrophe/paren
parity, no git write verbs, no control bytes, bash -n. Never overwrites an existing output without a .pre-* copy.
Usage: gen_launcher_1020.py <template launcher> <output launcher> [--enumerate]
Exit: 0 written · 1 an anchor/control count disagreed · 2 a residual token survived · 3 bash -n failed"""
import datetime, hashlib, os, re, shutil, subprocess, sys

src_path, out_path = sys.argv[1], sys.argv[2]
ENUMERATE = '--enumerate' in sys.argv[3:]
s = open(src_path, encoding='utf-8').read()
def refuse(msg, code):
    print('REFUSING: ' + msg, file=sys.stderr); sys.exit(code)

HEAD = '71bd80a35b406b9c99c7b96955a7521032d33c20'
BASE = 'd7e95cd9f153e9036ed77935a73c93504fa6e3dc'     # the PR parent = the merge-base = develop at draft time (the KS-1195 #1017 squash)
DEVELOP = BASE
BRANCH = 'refs/heads/chore/audit-fuse-mobile-tree-dormant-redate'
STEM = '2026-09-17_secuura-1020-ks769-tier2'
OLD_STEM = '2026-09-17_secuura-1009-ks864-tier2'
TEMPLATE_NAME = 'launch_qa_secuura_ks864_1009.sh'
COUNT_1020 = None if ENUMERATE else int(os.environ.get('COUNT_1020', '-1'))  # MEASURED by --enumerate first; passed in, never guessed

NEW_HEADER = '''#!/bin/bash
# launch_qa_secuura_ks769_1020.sh — cross-project QA agent, ONE TIER 2 ROUND 1 gate over Secuura/Blockchain PR #1020
# (KS-769, Seat A) @ 71bd80a35b406b9c99c7b96955a7521032d33c20 — ONE commit on d7e95cd9f, ONE file, +5 -1:
# Blockchain/Dev/scripts/audit/lock-discovery.mjs, OUT_OF_SCOPE_LOCKS mobile/secuura-app expires 2026-09-17 -> 2026-10-19 plus a
# four-line ruling comment (Kam ruled KS-769 "Dormant but kept"). The lapsed fuse refuses every Blockchain/Dev push at preflight legs 5 and 7.
#
# THE SHAPE, as read 15:42-15:46 AEST 2026-09-17 (git ls-remote + the compare API agree): the head parent is d7e95cd9f (the KS-1195 #1017
# squash) and origin develop IS d7e95cd9f. compare develop...head = merge_base d7e95cd9f, status ahead, ahead 1, behind 0, files 1. The
# compare is asserted as merge_base + ahead + files (exit 10); `behind` is deliberately NOT asserted, so a develop that moves on (#1018 and
# #1019 are open in the same lineage) does not trip this guard — the develop arm judges the move by CONTENT.
#
# The develop pin is judged by CONTENT, not bare: (a) TWELVE files by blob at the CURRENT develop — lock-discovery.mjs (base 2f54840ce; the
# PR own 3dd903b52 -> exit 19 LANDED), lock-discovery.test.mjs, baseline-contract.mjs (utcToday + isLapsed), baseline-contract.test.mjs,
# gate-exit-codes.test.mjs, audit-locks.mjs, audit-gate.mjs, audit-baseline.json (the other dated fuses), expected-case-count (59, leg 5),
# scripts/audit/package.json, scripts/preflight/preflight.sh, and the Dev package.json (the audit:contract script) — any blob nobody pinned
# -> exit 18; (b) if develop moved past d7e95cd9f, the compare pinned...develop REFUSES (exit 18) only when the delta touches a GUARDED
# path — anything under Blockchain/Dev/scripts/audit/, preflight.sh, the Dev package.json, or .githooks/pre-push — or cannot be judged;
# anything else proceeds and the gate re-derives every count on the merged tree. Lockfiles are deliberately NOT guarded: a dependency bump
# landing changes which advisories the gates report, and the gate re-measures that on the merged tree rather than refusing to start.
# DEV_CONTENT_ALLOWED is empty.
#
# exit 21: the LAUNCH path refuses when stdin is not a TTY. This launcher execs an interactive agent; run it in a cockpit
# pane, never inside a Bash tool. `--check` still runs headless (it launches nothing).
#
# Adapted from launch_qa_secuura_ks864_1009.sh by gen_launcher_1020.py (asserted substitutions + residual guard + output
# controls + bash -n): same guards and exit codes, re-pointed at #1020. Exit codes 2..21 (19 = LANDED).
# Written by the generator because it contains a legitimate directory change.
#
# Usage: launch_qa_secuura_ks769_1020.sh [--check]
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
 '  D + "' + A + 'lock-discovery.mjs":          ({"2f54840ce6470e4e8eadeab603a9db7fa3eb49b9": "base"}, {"3dd903b527f26c758cc1da84b10cc0a0db3b1d46": "#1020 own"}),',
 '  D + "' + A + 'lock-discovery.test.mjs":     ({"f102d9d4c4523091fe4e3119d6c539fb29bfd904": "base"}, {}),',
 '  D + "' + A + 'baseline-contract.mjs":       ({"2504d9a28dc017fcaabfc88248bf1c64431eb38a": "base"}, {}),',
 '  D + "' + A + 'baseline-contract.test.mjs":  ({"2379c0aeee6e3e3f0c4ef3a2512e3a590ad47d29": "base"}, {}),',
 '  D + "' + A + 'gate-exit-codes.test.mjs":    ({"40079f6fb41e146a34a66463e352b9c0a49f91e8": "base"}, {}),',
 '  D + "' + A + 'audit-locks.mjs":             ({"aff23b0420ced863884787443a35f28cf727bd09": "base"}, {}),',
 '  D + "' + A + 'audit-gate.mjs":              ({"8e236ee70ce1a4634552596fb86fcffce234f221": "base"}, {}),',
 '  D + "' + A + 'audit-baseline.json":         ({"03d1680e3c7a87f8df70e71082b67775536acde5": "base"}, {}),',
 '  D + "' + A + 'expected-case-count":         ({"04f9fe46068b397a6fc24d647b7e3ec4315c15e7": "base"}, {}),',
 '  D + "' + A + 'package.json":                ({"d5977b6a13638558ef57e8c294809d7ada8be6cd": "base"}, {}),',
 '  D + "scripts/preflight/preflight.sh":       ({"28d3636c13a4259bbdade8b15ac527cbe93742c3": "base"}, {}),',
 '  D + "package.json":                         ({"769b7adbda124bb200dd9827d2e4fbc5883e6124": "base"}, {}),',
 '}\n')
NEW_GUARDED = J(
 'GUARDED = [D + "scripts/audit/",',
 '           D + "scripts/preflight/preflight.sh",',
 '           D + "package.json",',
 '           ".githooks/pre-push"]\n')

def block(start, end_marker):
    if s.count(start) != 1: refuse('block start %r count %d' % (start[:50], s.count(start)), 1)
    i = s.find(start); j = s.find(end_marker, i)
    if j < 0: refuse('block end %r not found' % end_marker[:40], 1)
    return s[i:j + len(end_marker)]
old_judged = block('# file -> (develop-OK blobs {blob: label}, LANDED blobs {blob: label})', '}\n')
old_guarded = block('GUARDED = [D + "services/api-gateway/src/__tests__/ks864a-dead-estate-helper.test.ts",', 'D + "package-lock.json"]\n')

subs = [
    (old_judged, NEW_JUDGED, 1),
    (old_guarded, NEW_GUARDED, 1),
    ('QA1009_BRIEF', 'QA1020_BRIEF', 2),
    ('QA1009_PROMPT', 'QA1020_PROMPT', 2),
    ('QA1009_HEAD', 'QA1020_HEAD', 2),
    (OLD_STEM, STEM, 3),
    ('refs/heads/feature/ks-864-f1-portal-env-var-cells', BRANCH, 1),
    ('6ec0cb19834407887daa7bf5994f2da169abd30e', HEAD, 1),
    ("MERGE_BASE='0308b7a0447a2c01c12aad358c9b4d04a5178210'   # the merge-base of the head with develop = the PR parent (the KS-864 parts A+B squash; develop moved on to the KS-844 squash)",
     "MERGE_BASE='" + BASE + "'   # the merge-base of the head with develop = the PR parent (the KS-1195 #1017 squash; develop has not moved)", 1),
    ("DEVELOP_SHA='73d3fcb902d2a78fe68a4349903ff6c6bd24d4d5'   # develop at draft time = the KS-844 squash, a child of the base, 0 api-gateway files (ls-remote 01:28:30 and 03:03:43, compare API 01:29:57 AEST)",
     "DEVELOP_SHA='" + DEVELOP + "'   # develop at draft time = the PR parent itself (ls-remote 15:42:00, compare API 15:46:12 AEST)", 1),
    ('echo "REFUSING: #1009 — $HEAD_SHA is not at', 'echo "REFUSING: #1020 — $HEAD_SHA is not at', 1),
    ('# develop...#1009 = 0308b7a04 ahead 1 files 3 (behind 1 — the KS-844 squash — deliberately not asserted).',
     '# develop...#1020 = d7e95cd9f ahead 1 files 1 (behind 0 at draft time — deliberately not asserted).', 1),
    ('ahead=1 files=3', 'ahead=1 files=1', 2),
    ('''{ echo "REFUSING: #1009 develop...head reads''', '''{ echo "REFUSING: #1020 develop...head reads''', 1),
    ('# The develop pin, judged by CONTENT (see the header): nine files by blob at the CURRENT develop, then — if develop',
     '# The develop pin, judged by CONTENT (see the header): twelve files by blob at the CURRENT develop, then — if develop', 1),
    ('" — #1009 has landed; this brief is stale")', '" — #1020 has landed; this brief is stale")', 1),
    ('" (the KS-844 squash on the base, 0 api-gateway files; git ls-remote)")', '" (= the PR parent, the KS-1195 #1017 squash; git ls-remote)")', 1),
    ('# pinned here. EMPTY for this gate: at draft time 01:29 AEST no open lane PR touched a guarded path except dependabot\n# api-gateway package.json and lockfile bumps, which must NOT clear silently, so every guarded hit falls through to GUARDED and exit 18 — re-pin deliberately.',
     '# pinned here. EMPTY for this gate: at draft time 15:46 AEST no open PR touched a guarded path (PR files API, 20 open PRs),\n# so every guarded hit falls through to GUARDED and exit 18 — re-pin deliberately.', 1),
    ('tail = "the gate merges the then-current develop onto 6ec0cb198 in its own clone, rebuilds the shared dist there, runs the api-gateway suite on the MERGED tree beside the base and head trees, names the delta and re-derives every count (brief item 6)"',
     'tail = "the gate merges the then-current develop onto 71bd80a35 in its own clone, runs the audit legs on the MERGED tree beside the base and head trees, names the delta and re-derives every count and the fuse census (brief item 6)"', 1),
    ('— disjoint from the GUARDED list (api-gateway ks864a/b/c tests, routes/system-status.ts, src/index.ts, vitest.config.ts, vitest.setup.ts, package.json, tsconfig.json, eslint.config.mjs, the lockfile); %s"',
     '— disjoint from the GUARDED list (Blockchain/Dev/scripts/audit/, scripts/preflight/preflight.sh, the Dev package.json, .githooks/pre-push); %s"', 1),
    ('echo "  head on origin: #1009 $HEAD_SHA at $BRANCH"', 'echo "  head on origin: #1020 $HEAD_SHA at $BRANCH"', 1),
    ('echo "  compare (GitHub API): develop...#1009 = $COMPARE"', 'echo "  compare (GitHub API): develop...#1020 = $COMPARE"', 1),
]
for old, new, n in subs:
    c = s.count(old)
    if c != n: refuse('anchor %r occurs %d times, expected %d' % (old[:70], c, n), 1)
    s = s.replace(old, new)

permitted = 'Adapted from ' + TEMPLATE_NAME
if s.count(permitted) != 1: refuse('permitted template mention count %d' % s.count(permitted), 1)
body = s.replace(permitted, 'Adapted from <template>')
residual = ['1009', '1007', '0308b7a0', '73d3fcb9', '6ec0cb19', 'ks864', 'ks-864', 'KS-864', 'KS-844', 'api-gateway', 'system-status', 'vitest',
            'tsconfig', 'eslint', 'nine files', 'NINE files', '01:28', '01:29', '03:03', 'dependabot', 'shared dist', '649', '575']
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
        if '#1020' in l: print('#1020 at line %d: %s' % (i, l[:110]))
    print('ENUMERATED count #1020 = %d (scratch copy written to %s; nothing written to launchers/)' % (s.count('#1020'), out_path)); sys.exit(0)

controls = [
    ('HEAD_SHA="${QA1020_HEAD:-' + HEAD + '}"', 1), ("MERGE_BASE='" + BASE + "'", 1), ("DEVELOP_SHA='" + DEVELOP + "'", 1),
    ("BRANCH='" + BRANCH + "'", 1), (STEM + '.md', 2), (STEM + '.prompt.txt', 1),
    ('exit 2;', 1), ('exit 3;', 1), ('exit 4;', 1), ('exit 5;', 1), ('exit 6', 1), ('exit 7;', 1), ('exit 8;', 1), ('exit 9;', 1),
    ('exit 10;', 1), ('exit 11;', 1), ('exit 12;', 1), ('exit 13;', 1), ('exit 14;', 1), ('exit 15;', 1), ('exit 16;', 2), ('exit 17;', 1),
    ('exit 18; }', 1), ('exit 18 ;;', 1), ('exit 19 ;;', 1), ('exit 20;', 1), ('exit 21;', 1),
    ('DEV_CONTENT_ALLOWED = {', 1), ('print("LANDED ', 1), ('print("GUARDED ', 2), ('print("UNJUDGEABLE ', 3), ('LANDED*)', 1), ('OK*)', 1),
    ('2f54840ce6470e4e8eadeab603a9db7fa3eb49b9', 1), ('3dd903b527f26c758cc1da84b10cc0a0db3b1d46', 1), ('f102d9d4c4523091fe4e3119d6c539fb29bfd904', 1),
    ('2504d9a28dc017fcaabfc88248bf1c64431eb38a', 1), ('2379c0aeee6e3e3f0c4ef3a2512e3a590ad47d29', 1), ('40079f6fb41e146a34a66463e352b9c0a49f91e8', 1),
    ('aff23b0420ced863884787443a35f28cf727bd09', 1), ('8e236ee70ce1a4634552596fb86fcffce234f221', 1), ('03d1680e3c7a87f8df70e71082b67775536acde5', 1),
    ('04f9fe46068b397a6fc24d647b7e3ec4315c15e7', 1), ('d5977b6a13638558ef57e8c294809d7ada8be6cd', 1), ('28d3636c13a4259bbdade8b15ac527cbe93742c3', 1),
    ('769b7adbda124bb200dd9827d2e4fbc5883e6124', 1),
    ('ahead=1 files=1', 2), ('[ -t 0 ]', 1), ('exec claude --dangerously-skip-permissions --model opus', 1),
    ('git -C "$REPO"', 2), ('set -u', 1), ('MAIL YOUR VERDICT', 1), ('NEVER print a credential value', 1), ('no memory maintenance', 1),
    ("grep -q 'TIER 2'", 2), ("grep -q 'ROUND 1'", 2), ('GUARDED = [D + "scripts/audit/",', 1), ('".githooks/pre-push"]', 1),
    ('#1020', COUNT_1020),
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
