#!/usr/bin/env python3
"""gen_launcher_1027.py — derive launch_qa_secuura_ks1211_1027.sh from the sibling TIER 2 launcher launchers/launch_qa_secuura_ks1211_1021.sh
(same guard family: head on origin exit 6, compare exit 10/13, develop judged BY CONTENT exit 18/19, head SHA named in brief+prompt exit 20,
TTY exit 21) by ASSERTED substitutions: every anchor must occur exactly as often as stated, or the generator refuses and writes nothing.
Then a RESIDUAL GUARD (any token of the source gate left, after stripping the one permitted template-name mention, is a refusal),
output controls ('#1027' ENUMERATED first with --enumerate, which writes only to the scratch path given), PY/PYJ heredoc apostrophe/paren
parity, no git write verbs, no control bytes, bash -n. Never overwrites an existing output without a .pre-* copy.
Usage: gen_launcher_1027.py <template launcher> <output launcher> [--enumerate]
Exit: 0 written · 1 an anchor/control count disagreed · 2 a residual token survived · 3 bash -n failed"""
import datetime, hashlib, os, re, shutil, subprocess, sys

src_path, out_path = sys.argv[1], sys.argv[2]
ENUMERATE = '--enumerate' in sys.argv[3:]
s = open(src_path, encoding='utf-8').read()
def refuse(msg, code):
    print('REFUSING: ' + msg, file=sys.stderr); sys.exit(code)

HEAD = 'd7fc6cc5582b918c0773ec6f25f86407de6f86ab'
BASE = '19f1e54750ce2b65312a687add2db4f5628edb7d'     # merge-base of head with develop = the develop the seat merged in (#1025)
DEVELOP = '19f1e54750ce2b65312a687add2db4f5628edb7d'  # origin develop at 20:05:22 and 20:07:07 AEST = the merge-base itself
OLD_HEAD = '742e1c6080f2527973268146611930e4a70edef2'
OLD_BASE = 'f8c7aaa39dabfe6a3916e5be55d9ccd752e7d8ed'
OLD_DEVELOP = '581c9db0db4201c42cbbf702f339b750989acdb1'
BRANCH = 'refs/heads/feature/ks-1211-bump-jsyaml-bbm'
STEM = '2026-09-17_secuura-1027-ks1211-jsyaml-bbm-tier2'
OLD_STEM = '2026-09-17_secuura-1021-ks1211-colord-tier2'
TEMPLATE_NAME = 'launch_qa_secuura_ks1211_1021.sh'
COUNT_1027 = None if ENUMERATE else int(os.environ.get('COUNT_1027', '-1'))  # MEASURED by --enumerate first; passed in, never guessed

NEW_HEADER = '''#!/bin/bash
# launch_qa_secuura_ks1211_1027.sh — cross-project QA agent, ONE TIER 2 ROUND 1 gate over Secuura/Blockchain PR #1027
# (KS-1211, Seat B, PR-3a of the regroup: GHSA-2883-xcg3-v3hh js-yaml HIGH + GHSA-w5vr-8v7q-w6rv baseline-browser-mapping)
# @ d7fc6cc5582b918c0773ec6f25f86407de6f86ab — TWO commits: b51ed77e1 (the change, on efaaa6034) and d7fc6cc55 (a merge of develop
# 19f1e5475 = #1025). TEN files, no manifest: js-yaml 3.15.1 -> 3.15.2 in services/governance, originate, referral, vc-issuer and the
# Blockchain/Dev root lock; baseline-browser-mapping -> 2.11.24 in frontend/admin, issuer, outlook-addin, verifier, services/governance,
# originate, referral and the root lock; the two rows removed from Blockchain/Dev/scripts/audit/audit-baseline.json (34 -> 32).
#
# THE SHAPE, as read 20:05-20:09 AEST 2026-09-17 (git ls-remote + the compare API): head parents b51ed77e1 + 19f1e5475; origin develop
# 19f1e5475. compare develop...head = merge_base 19f1e5475, status ahead, ahead 2, behind 0, files 10. The compare is asserted as
# merge_base + ahead + files (exit 10); `behind` is deliberately NOT asserted, so a develop that moves on does not trip this guard — the
# develop arm judges the move by CONTENT.
#
# The develop pin is judged by CONTENT, not bare: (a) TWENTY-FIVE files by blob at the CURRENT develop — audit-baseline.json (base
# e6f2184d2 / own 017f52bb5), the nine touched locks (base / own blob each; an own blob -> exit 19 LANDED), their nine package.json,
# and scripts/audit/ audit-locks.mjs, audit-gate.mjs, lock-discovery.mjs, baseline-contract.mjs, package.json, package-lock.json — any
# blob nobody pinned -> exit 18; (b) if develop moved past 19f1e5475, the compare pinned...develop REFUSES (exit 18) only when the delta
# touches a GUARDED path — anything under Blockchain/Dev/scripts/audit/, any of the nine touched locks or their package.json — or cannot
# be judged; anything else proceeds and the gate re-derives every count on the merged tree. TEN open Dependabot PRs (#945-#949, #649, 
# #639, #635, #575, #572) touch the root lock, so one of them landing first REFUSES here by design: re-pin deliberately.
# DEV_CONTENT_ALLOWED is empty.
#
# exit 21: the LAUNCH path refuses when stdin is not a TTY. This launcher execs an interactive agent; run it in a cockpit
# pane, never inside a Bash tool. `--check` still runs headless (it launches nothing).
#
# Adapted from launch_qa_secuura_ks1211_1021.sh by gen_launcher_1027.py (asserted substitutions + residual guard + output
# controls + bash -n): same guards and exit codes, re-pointed at #1027. Exit codes 2..21 (19 = LANDED).
# Written by the generator because it contains a legitimate directory change.
#
# Usage: launch_qa_secuura_ks1211_1027.sh [--check]
# Exit: 0 launched (or guards passed under --check) · 2..21 a guard refused
'''
marker = 'set -u\n'
if s.count(marker) != 1: refuse('header marker set -u count %d' % s.count(marker), 1)
s = NEW_HEADER + s[s.index(marker):]

A = 'scripts/audit/'
LOCKS = [  # (member dir, develop lock blob, own lock blob, manifest blob)
 ('frontend/admin',         'e2a3e7b574cd0d828e810d206e18f5f862b08c3b', '3d9acadaf808610c57de3781657c94a598001f32', 'a7fd91ccf3a553d7a2d619caf9cfd4de7ea9d7ac'),
 ('frontend/issuer',        '8ebf271f14e7dd997c974ec95698357922d7f11b', 'b0c47af7144f9228450dc5a82225f742db50b662', '9d229cab1ec88eb5312693d4860b50b66b80383d'),
 ('frontend/outlook-addin', '25ddd7127d618373a5da58cf45284532380b5e19', 'c71cfe57a3e4a6f2c4c641ac395c10e99be9c8ba', '482d51f881b68d462f88df48bd4137d4dc6b5265'),
 ('frontend/verifier',      '39494d91d2ba6aadda5c3b541b2fb1364f65d7c8', '0a13fe2b72adc794ce9bc645a1680fdbbd570d9d', '76ef5149dbedb8a5179d5ea7145058a4ed74dc2e'),
 ('services/governance',    '0f173b26a5c2184201b7a0403425095ad7d499d6', '5fae8f62ca58252800146606ea47877ad9a9a3a6', 'e0644b07509ee7dfbd0b8d267e4246dd3a1e2f65'),
 ('services/originate',     'd91d746efb2b7fcd6d3168838925f40d7282ea32', '040908e22c620b245d7d1c1c0f512409ef94f043', '749912c592e8630fff348cc60e1bf49677c18ab1'),
 ('services/referral',      '009788ecca8eb2ee23629409adf4ceaa7426d602', '725d5d2c21f00e574b2f3986383ca398e322b2aa', '6482d21714eaa92df7a5fc7e8347912eb446c214'),
 ('services/vc-issuer',     'd0e7d22d683bf2ea415cd00e367f33df5ab16009', '05dff4ebb509fdf2c5605f0e4caa2e16a15bb0b5', '98b44b6c9bc95409a834339dda8b14c0f1e51c77'),
 ('',                       '99db3e7c2434f65eb64ab0d8db5775e11eefd6bd', '4831bf2074779139926fbfda3f872c404eba177f', '769b7adbda124bb200dd9827d2e4fbc5883e6124'),
]
AUDIT = [('audit-locks.mjs', 'aff23b0420ced863884787443a35f28cf727bd09'), ('audit-gate.mjs', '8e236ee70ce1a4634552596fb86fcffce234f221'),
         ('lock-discovery.mjs', '3dd903b527f26c758cc1da84b10cc0a0db3b1d46'), ('baseline-contract.mjs', '2504d9a28dc017fcaabfc88248bf1c64431eb38a'),
         ('package.json', 'd5977b6a13638558ef57e8c294809d7ada8be6cd'), ('package-lock.json', 'ffb2b110a2d69c2c9a10e6caf5666c5fa08ec62c')]
BL_BASE, BL_OWN = 'e6f2184d2dde6de00fb79618de3621659998e307', '017f52bb5a358e8cae1d25a729c8642d3ed45bc5'
def mp(d, f): return 'D + "' + ((d + '/') if d else '') + f + '"'
jl = ['# file -> (develop-OK blobs {blob: label}, LANDED blobs {blob: label})', 'JUDGED = {',
      '  D + "' + A + 'audit-baseline.json": ({"' + BL_BASE + '": "base"}, {"' + BL_OWN + '": "#1027 own"}),']
for d, b, o, m in LOCKS:
    jl.append('  ' + mp(d, 'package-lock.json') + ': ({"' + b + '": "base"}, {"' + o + '": "#1027 own"}),')
    jl.append('  ' + mp(d, 'package.json') + ': ({"' + m + '": "base"}, {}),')
for f, b in AUDIT:
    jl.append('  D + "' + A + f + '": ({"' + b + '": "base"}, {}),')
jl.append('}\n')
NEW_JUDGED = '\n'.join(jl)
if NEW_JUDGED.count('": "base"}') != 25: refuse('JUDGED rows %d, want 25' % NEW_JUDGED.count('": "base"}'), 1)
gl = ['GUARDED = [D + "scripts/audit/",']
for d, b, o, m in LOCKS:
    gl.append('           ' + mp(d, 'package-lock.json') + ',')
    gl.append('           ' + mp(d, 'package.json') + ',')
gl[-1] = gl[-1].rstrip(',') + ']\n'
NEW_GUARDED = '\n'.join(gl)

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
    ('QA1021_BRIEF', 'QA1027_BRIEF', 2),
    ('QA1021_PROMPT', 'QA1027_PROMPT', 2),
    ('QA1021_HEAD', 'QA1027_HEAD', 2),
    (OLD_STEM, STEM, 3),
    ('refs/heads/feature/ks-1211-bump-colord', BRANCH, 1),
    (OLD_HEAD, HEAD, 1),
    ("MERGE_BASE='" + OLD_BASE + "'   # the merge-base of the head with develop = the PR parent (develop moved on to #1019, api-gateway only)",
     "MERGE_BASE='" + BASE + "'   # the merge-base of the head with develop = the develop the seat merged in (#1025, KS-528)", 1),
    ("DEVELOP_SHA='" + OLD_DEVELOP + "'   # develop at draft time = #1019's squash (KS-1187), a child of the PR parent, 3 api-gateway files, 0 guarded (ls-remote 17:54:41 AEST)",
     "DEVELOP_SHA='" + DEVELOP + "'   # develop at draft time = the merge-base itself, #1025 squash (ls-remote 20:05:22 and 20:07:07 AEST)", 1),
    ('echo "REFUSING: #1021 — $HEAD_SHA is not at', 'echo "REFUSING: #1027 — $HEAD_SHA is not at', 1),
    ('# develop...#1021 = f8c7aaa39 ahead 1 files 3 (behind 0 at draft time — deliberately not asserted).',
     '# develop...#1027 = 19f1e5475 ahead 2 files 10 (behind 0 at draft time — deliberately not asserted).', 1),
    ('ahead=1 files=3', 'ahead=2 files=10', 2),
    ('''{ echo "REFUSING: #1021 develop...head reads''', '''{ echo "REFUSING: #1027 develop...head reads''', 1),
    ('# The develop pin, judged by CONTENT (see the header): thirteen files by blob at the CURRENT develop, then — if develop',
     '# The develop pin, judged by CONTENT (see the header): twenty-five files by blob at the CURRENT develop, then — if develop', 1),
    ('" — #1021 has landed; this brief is stale")', '" — #1027 has landed; this brief is stale")', 1),
    ('" (#1019 squash on the PR parent, api-gateway only; git ls-remote)")', '" (#1025 squash = the merge-base; git ls-remote)")', 1),
    ('# pinned here. EMPTY for this gate: at draft time 17:48 AEST no open PR shared a file with #1021 (PR files API, 21 open PRs),',
     '# pinned here. EMPTY for this gate: at draft time 20:08 AEST ten open Dependabot PRs share the root lock with #1027 (PR files API, 20 open PRs),', 1),
    ('tail = "the gate merges the then-current develop onto 742e1c608 in its own clone, re-runs the lock parse and both audit gates on the MERGED tree beside the base and head trees, and names the delta (brief item 5)"',
     'tail = "the gate merges the then-current develop onto d7fc6cc55 in its own clone, re-runs the lock parse and both audit gates on the MERGED tree beside the develop and head trees, and names the delta (brief item 5)"', 1),
    ('— disjoint from the GUARDED list (Blockchain/Dev/scripts/audit/, Blockchain/Dev/scripts/preflight/, the two harness package.json and package-lock.json, systemTest/CLAUDE.md, .githooks/pre-push); %s"',
     '— disjoint from the GUARDED list (Blockchain/Dev/scripts/audit/, the nine touched package-lock.json and their package.json); %s"', 1),
    ('echo "  head on origin: #1021 $HEAD_SHA at $BRANCH"', 'echo "  head on origin: #1027 $HEAD_SHA at $BRANCH"', 1),
    ('echo "  compare (GitHub API): develop...#1021 = $COMPARE"', 'echo "  compare (GitHub API): develop...#1027 = $COMPARE"', 1),
]
for old, new, n in subs:
    c = s.count(old)
    if c != n: refuse('anchor %r occurs %d times, expected %d' % (old[:70], c, n), 1)
    s = s.replace(old, new)

permitted = 'Adapted from ' + TEMPLATE_NAME
if s.count(permitted) != 1: refuse('permitted template mention count %d' % s.count(permitted), 1)
body = s.replace(permitted, 'Adapted from <template>')
residual = ['1021', '742e1c60', 'f8c7aaa3', '581c9db0', 'colord', 'akto', 'api-explorer', 'harness', 'systemTest', 'thirteen', 'THIRTEEN',
            '#1019', 'KS-1187', 'stylelint', 'GHSA-2wm5', '17:4', '17:5', '03d1680e3', 'api-gateway', 'lockfile-cleanroom', 'preflight/', 'githooks',
            'ahead=1', 'files=3"']
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
        if '#1027' in l: print('#1027 at line %d: %s' % (i, l[:110]))
    print('ENUMERATED count #1027 = %d (scratch copy written to %s; nothing written to launchers/)' % (s.count('#1027'), out_path)); sys.exit(0)

controls = [
    ('HEAD_SHA="${QA1027_HEAD:-' + HEAD + '}"', 1), ("MERGE_BASE='" + BASE + "'", 1), ("DEVELOP_SHA='" + DEVELOP + "'", 1),
    ("BRANCH='" + BRANCH + "'", 1), (STEM + '.md', 2), (STEM + '.prompt.txt', 1),
    ('exit 2;', 1), ('exit 3;', 1), ('exit 4;', 1), ('exit 5;', 1), ('exit 6', 1), ('exit 7;', 1), ('exit 8;', 1), ('exit 9;', 1),
    ('exit 10;', 1), ('exit 11;', 1), ('exit 12;', 1), ('exit 13;', 1), ('exit 14;', 1), ('exit 15;', 1), ('exit 16;', 2), ('exit 17;', 1),
    ('exit 18; }', 1), ('exit 18 ;;', 1), ('exit 19 ;;', 1), ('exit 20;', 1), ('exit 21;', 1),
    ('DEV_CONTENT_ALLOWED = {', 1), ('print("LANDED ', 1), ('print("GUARDED ', 2), ('print("UNJUDGEABLE ', 3), ('LANDED*)', 1), ('OK*)', 1),
    (BL_BASE, 1), (BL_OWN, 1), ('"#1027 own"', 10), ('": "base"}', 25),
    ('ahead=2 files=10', 2), ('[ -t 0 ]', 1), ('exec claude --dangerously-skip-permissions --model opus', 1),
    ('git -C "$REPO"', 2), ('set -u', 1), ('MAIL YOUR VERDICT', 1), ('NEVER print a credential value', 1), ('no memory maintenance', 1),
    ("grep -q 'TIER 2'", 2), ("grep -q 'ROUND 1'", 2), ('GUARDED = [D + "scripts/audit/",', 1), ('D + "package.json"]', 1),
    ('#1027', COUNT_1027),
] + [(b, 1) for _, b, _, _ in LOCKS] + [(o, 1) for _, _, o, _ in LOCKS] + [(m, 1) for _, _, _, m in LOCKS] + [(b, 1) for _, b in AUDIT]
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
