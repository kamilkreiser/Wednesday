#!/usr/bin/env python3
"""gen_launcher_1025.py — derive launch_qa_secuura_ks528_1025.sh from the sibling TIER 2 launcher launchers/launch_qa_secuura_ks1211_1021.sh
(same guard family: head on origin exit 6, compare exit 10/13, develop judged BY CONTENT exit 18/19, head SHA named in brief+prompt exit 20,
TTY exit 21) by ASSERTED substitutions: every anchor must occur exactly as often as stated, or the generator refuses and writes nothing.
Two guards are ADDED for this gate: exit 22 (under --check, the launcher reads its own bytes and proves the TTY refusal sits before the exec,
so the TTY guard is shown without a bare launch) and exit 23 (brief and prompt agree on the exact verdict subject and the report dir, and the
prompt names NOT-TESTED.written-first.md and the MERGE ADDENDUM).
Then a RESIDUAL GUARD (any token of the source gate left, after stripping the one permitted template-name mention, is a refusal),
output controls ('#1025' ENUMERATED first with --enumerate, which writes only to the scratch path given), PY/PYJ heredoc apostrophe/paren
parity, no git write verbs, no control bytes, bash -n. Never overwrites an existing output without a .pre-* copy.
Usage: gen_launcher_1025.py <template launcher> <output launcher> [--enumerate]
Exit: 0 written · 1 an anchor/control count disagreed · 2 a residual token survived · 3 bash -n failed"""
import datetime, hashlib, os, re, shutil, subprocess, sys

src_path, out_path = sys.argv[1], sys.argv[2]
ENUMERATE = '--enumerate' in sys.argv[3:]
s = open(src_path, encoding='utf-8').read()
def refuse(msg, code):
    print('REFUSING: ' + msg, file=sys.stderr); sys.exit(code)

HEAD = '9954a7069a16987da140654337555c9a13268b1f'
BASE = 'efaaa6034f036dd9538ee35b189217b1d08b90a9'     # the PR parent = the merge-base = origin develop at draft time (#1023 KS-1207 squash)
DEVELOP = BASE
OLD_HEAD = '742e1c6080f2527973268146611930e4a70edef2'
OLD_BASE = 'f8c7aaa39dabfe6a3916e5be55d9ccd752e7d8ed'
OLD_DEVELOP = '581c9db0db4201c42cbbf702f339b750989acdb1'
BRANCH = 'refs/heads/chore/audit-redate-react-router-rows-v7-landing'
STEM = '2026-09-17_secuura-1025-ks528-tier2'
OLD_STEM = '2026-09-17_secuura-1021-ks1211-colord-tier2'
TEMPLATE_NAME = 'launch_qa_secuura_ks1211_1021.sh'
SUBJECT = '[QA -> Wednesday] TIER 2 GATE #1025 (KS-528) 9954a7069 — <GO | GO WITH FINDINGS | NO GO>'
REPORT_DIR = '/Volumes/DevMASTER/!CODING/Testing Agent MAIN/projects/secuura/reports/2026-09-17-ks528-1025-9954a7069-tier2-r1/'
COUNT_1025 = None if ENUMERATE else int(os.environ.get('COUNT_1025', '-1'))  # MEASURED by --enumerate first; passed in, never guessed

NEW_HEADER = '''#!/bin/bash
# launch_qa_secuura_ks528_1025.sh — cross-project QA agent, ONE TIER 2 ROUND 1 gate over Secuura/Blockchain PR #1025
# (KS-528, Seat B, the re-date of audit-baseline rows 11 and 12, GHSA-wrjc-x8rr-h8h6 and GHSA-337j-9hxr-rhxg, react-router) @
# 9954a7069a16987da140654337555c9a13268b1f — ONE commit on efaaa6034, ONE file: Blockchain/Dev/scripts/audit/audit-baseline.json, both rows
# expires 2026-09-30 -> 2026-10-02 and a dated RE-DATED sentence appended to each reason (Kam 18:31:25 migrate-and-date; landing 2026-10-01).
#
# THE SHAPE, as read 19:24-19:29 AEST 2026-09-17 (git ls-remote + the PR and compare APIs): the head parent is efaaa6034 (#1023, KS-1207),
# which is also origin develop. compare develop...head = merge_base efaaa6034, status ahead, ahead 1, behind 0, files 1. The compare is
# asserted as merge_base + ahead + files (exit 10); `behind` is deliberately NOT asserted, so a develop that moves on does not trip this
# guard — the develop arm judges the move by CONTENT.
#
# The develop pin is judged by CONTENT, not bare: (a) FIFTEEN files by blob at the CURRENT develop — every tracked file under
# Blockchain/Dev/scripts/audit/ at efaaa6034 (audit-baseline.json base 45ef8220f / own e6f2184d2 -> exit 19 LANDED; audit-gate.mjs,
# audit-locks.mjs, baseline-contract.mjs, lock-discovery.mjs, could-not-check.mjs, advisory-fetch-stub.mjs, the three contract test files,
# expected-case-count, package.json, package-lock.json) plus Blockchain/Dev/package-lock.json (the tree audit-gate audits) — any blob nobody
# pinned -> exit 18; (b) if develop moved past efaaa6034, the compare pinned...develop REFUSES (exit 18) only when the delta touches a
# GUARDED path — anything under Blockchain/Dev/scripts/audit/, or Blockchain/Dev/package-lock.json — or cannot be judged; anything else
# proceeds and the gate re-derives every count on the merged tree. Seat B's PR-3 edits audit-baseline.json AND the root lock (held until
# #1025 merges), so it landing first REFUSES here by design: re-pin deliberately. DEV_CONTENT_ALLOWED is empty.
#
# exit 21: the LAUNCH path refuses when stdin is not a TTY. This launcher execs an interactive agent; run it in a cockpit
# pane, never inside a Bash tool. `--check` still runs headless (it launches nothing), and proves the TTY guard by reading this file (exit 22).
# exit 23: brief and prompt must agree on the exact verdict subject and the report dir; the prompt must name NOT-TESTED.written-first.md
# and the MERGE ADDENDUM.
#
# Adapted from launch_qa_secuura_ks1211_1021.sh by gen_launcher_1025.py (asserted substitutions + residual guard + output
# controls + bash -n): same guards and exit codes, re-pointed at #1025, plus exits 22 and 23. Exit codes 2..23 (19 = LANDED).
# Written by the generator because it contains a legitimate directory change.
#
# Usage: launch_qa_secuura_ks528_1025.sh [--check]
# Exit: 0 launched (or guards passed under --check) · 2..23 a guard refused
'''
marker = 'set -u\n'
if s.count(marker) != 1: refuse('header marker set -u count %d' % s.count(marker), 1)
s = NEW_HEADER + s[s.index(marker):]

A = 'scripts/audit/'
J = lambda *lines: '\n'.join(lines)
NEW_JUDGED = J(
 '# file -> (develop-OK blobs {blob: label}, LANDED blobs {blob: label})',
 'JUDGED = {',
 '  D + "' + A + 'audit-baseline.json":         ({"45ef8220f26ac164939da5b0425dab01116f7a18": "base"}, {"e6f2184d2dde6de00fb79618de3621659998e307": "#1025 own"}),',
 '  D + "' + A + 'audit-gate.mjs":              ({"8e236ee70ce1a4634552596fb86fcffce234f221": "base"}, {}),',
 '  D + "' + A + 'audit-locks.mjs":             ({"aff23b0420ced863884787443a35f28cf727bd09": "base"}, {}),',
 '  D + "' + A + 'baseline-contract.mjs":       ({"2504d9a28dc017fcaabfc88248bf1c64431eb38a": "base"}, {}),',
 '  D + "' + A + 'lock-discovery.mjs":          ({"3dd903b527f26c758cc1da84b10cc0a0db3b1d46": "base"}, {}),',
 '  D + "' + A + 'could-not-check.mjs":         ({"92eea6087a6c442f1a14e735ba9fcca74493bd0a": "base"}, {}),',
 '  D + "' + A + 'advisory-fetch-stub.mjs":     ({"29c9fc48f32857d4f24ef944b9868639e0171435": "base"}, {}),',
 '  D + "' + A + 'baseline-contract.test.mjs":  ({"2379c0aeee6e3e3f0c4ef3a2512e3a590ad47d29": "base"}, {}),',
 '  D + "' + A + 'lock-discovery.test.mjs":     ({"f102d9d4c4523091fe4e3119d6c539fb29bfd904": "base"}, {}),',
 '  D + "' + A + 'gate-exit-codes.test.mjs":    ({"40079f6fb41e146a34a66463e352b9c0a49f91e8": "base"}, {}),',
 '  D + "' + A + 'expected-case-count":         ({"04f9fe46068b397a6fc24d647b7e3ec4315c15e7": "base"}, {}),',
 '  D + "' + A + 'package.json":                ({"d5977b6a13638558ef57e8c294809d7ada8be6cd": "base"}, {}),',
 '  D + "' + A + 'package-lock.json":           ({"ffb2b110a2d69c2c9a10e6caf5666c5fa08ec62c": "base"}, {}),',
 '  D + "package-lock.json":                      ({"99db3e7c2434f65eb64ab0d8db5775e11eefd6bd": "base"}, {}),',
 '}\n')
NEW_GUARDED = J(
 'GUARDED = [D + "scripts/audit/",',
 '           D + "package-lock.json"]\n')

def block(start, end_marker):
    if s.count(start) != 1: refuse('block start %r count %d' % (start[:50], s.count(start)), 1)
    i = s.find(start); j = s.find(end_marker, i)
    if j < 0: refuse('block end %r not found' % end_marker[:40], 1)
    return s[i:j + len(end_marker)]
old_judged = block('# file -> (develop-OK blobs {blob: label}, LANDED blobs {blob: label})', '}\n')
old_guarded = block('GUARDED = [D + "scripts/audit/",', '".githooks/pre-push"]\n')

NEW_CHECKS = '''grep -qF "$SUBJECT" "$BRIEF" && grep -qF "$SUBJECT" "$PROMPT_FILE" && grep -qF "$REPORT_DIR" "$BRIEF" && grep -qF "$REPORT_DIR" "$PROMPT_FILE" \\
  && grep -qF 'NOT-TESTED.written-first.md' "$PROMPT_FILE" && grep -qF 'MERGE ADDENDUM' "$PROMPT_FILE" \\
  || { echo "REFUSING: brief and prompt disagree on the verdict subject or report dir, or the prompt omits NOT-TESTED.written-first.md / the MERGE ADDENDUM" >&2; exit 23; }

if [ "${1:-}" = "--check" ]; then
  # The TTY refusal is proven by reading this file, never by a bare launch: the guard line must exist once and sit before the exec.
  TTY_LINE="$(grep -n '^\\[ -t 0 \\] || ' "$0" | cut -d: -f1)"
  EXEC_LINE="$(grep -n '^exec claude ' "$0" | cut -d: -f1)"
  { [ -n "$TTY_LINE" ] && [ -n "$EXEC_LINE" ] && [ "$(printf '%s\\n' "$TTY_LINE" | wc -l | tr -d ' ')" = 1 ] && [ "$TTY_LINE" -lt "$EXEC_LINE" ]; } \\
    || { echo "REFUSING: the TTY guard is missing, duplicated or not before the exec (tty line '$TTY_LINE', exec line '$EXEC_LINE')" >&2; exit 22; }
  echo "all guards pass:"'''

subs = [
    (old_judged, NEW_JUDGED, 1),
    (old_guarded, NEW_GUARDED, 1),
    ('QA1021_BRIEF', 'QA1025_BRIEF', 2),
    ('QA1021_PROMPT', 'QA1025_PROMPT', 2),
    ('QA1021_HEAD', 'QA1025_HEAD', 2),
    (OLD_STEM, STEM, 3),
    ('refs/heads/feature/ks-1211-bump-colord', BRANCH, 1),
    (OLD_HEAD, HEAD, 1),
    ("MERGE_BASE='" + OLD_BASE + "'   # the merge-base of the head with develop = the PR parent (develop moved on to #1019, api-gateway only)",
     "MERGE_BASE='" + BASE + "'   # the merge-base of the head with develop = the PR parent (the #1023 KS-1207 squash; develop has not moved)", 1),
    ("DEVELOP_SHA='" + OLD_DEVELOP + "'   # develop at draft time = #1019's squash (KS-1187), a child of the PR parent, 3 api-gateway files, 0 guarded (ls-remote 17:54:41 AEST)",
     "DEVELOP_SHA='" + DEVELOP + "'   # develop at draft time = the PR parent itself (ls-remote 19:24:23 AEST, branches API 19:28:48 AEST)", 1),
    ("REAL_BRIEF=", "SUBJECT='" + SUBJECT + "'\nREPORT_DIR='" + REPORT_DIR + "'\nREAL_BRIEF=", 1),
    ('echo "REFUSING: #1021 — $HEAD_SHA is not at', 'echo "REFUSING: #1025 — $HEAD_SHA is not at', 1),
    ('# develop...#1021 = f8c7aaa39 ahead 1 files 3 (behind 0 at draft time — deliberately not asserted).',
     '# develop...#1025 = efaaa6034 ahead 1 files 1 (behind 0 at draft time — deliberately not asserted).', 1),
    ('ahead=1 files=3', 'ahead=1 files=1', 2),
    ('''{ echo "REFUSING: #1021 develop...head reads''', '''{ echo "REFUSING: #1025 develop...head reads''', 1),
    ('# The develop pin, judged by CONTENT (see the header): thirteen files by blob at the CURRENT develop, then — if develop',
     '# The develop pin, judged by CONTENT (see the header): fifteen files by blob at the CURRENT develop, then — if develop', 1),
    ('" — #1021 has landed; this brief is stale")', '" — #1025 has landed; this brief is stale")', 1),
    ('" (#1019 squash on the PR parent, api-gateway only; git ls-remote)")', '" (= the PR parent, the #1023 KS-1207 squash; git ls-remote)")', 1),
    ('# pinned here. EMPTY for this gate: at draft time 17:48 AEST no open PR shared a file with #1021 (PR files API, 21 open PRs),',
     '# pinned here. EMPTY for this gate: at draft time 19:28 AEST no open PR shared a file with #1025 (PR files API, 21 open PRs),', 1),
    ('tail = "the gate merges the then-current develop onto 742e1c608 in its own clone, re-runs the lock parse and both audit gates on the MERGED tree beside the base and head trees, and names the delta (brief item 5)"',
     'tail = "the gate merges the then-current develop onto 9954a7069 in its own clone, re-runs the baseline parse, the isLapsed table and the three shipped gates on the MERGED tree beside the develop and head trees, and names the delta (brief item 6)"', 1),
    ('— disjoint from the GUARDED list (Blockchain/Dev/scripts/audit/, Blockchain/Dev/scripts/preflight/, the two harness package.json and package-lock.json, systemTest/CLAUDE.md, .githooks/pre-push); %s"',
     '— disjoint from the GUARDED list (Blockchain/Dev/scripts/audit/, Blockchain/Dev/package-lock.json); %s"', 1),
    ('\nif [ "${1:-}" = "--check" ]; then\n  echo "all guards pass:"', '\n' + NEW_CHECKS, 1),
    ('    state.append(f.split("/")[-1] + " " + blob[:9] + " = " + ok[blob])', '    state.append(short + " " + blob[:9] + " = " + ok[blob])', 1),
    ('echo "  head on origin: #1021 $HEAD_SHA at $BRANCH"', 'echo "  head on origin: #1025 $HEAD_SHA at $BRANCH"', 1),
    ('echo "  compare (GitHub API): develop...#1021 = $COMPARE"', 'echo "  compare (GitHub API): develop...#1025 = $COMPARE"', 1),
    ('  echo "  prompt forbids printing a credential value"\n',
     '  echo "  prompt forbids printing a credential value"\n  echo "  brief and prompt agree on the verdict subject and the report dir; prompt names NOT-TESTED.written-first.md and the MERGE ADDENDUM"\n  echo "  TTY guard present once, at line $TTY_LINE, before the exec at line $EXEC_LINE (read from this file; no launch attempted)"\n', 1),
]
for old, new, n in subs:
    c = s.count(old)
    if c != n: refuse('anchor %r occurs %d times, expected %d' % (old[:70], c, n), 1)
    s = s.replace(old, new)

permitted = 'Adapted from ' + TEMPLATE_NAME
if s.count(permitted) != 1: refuse('permitted template mention count %d' % s.count(permitted), 1)
body = s.replace(permitted, 'Adapted from <template>')
residual = ['1021', '742e1c60', 'f8c7aaa3', '581c9db0', 'ks1211', 'KS-1211', 'colord', 'akto', 'api-explorer', 'systemTest', 'harness', '#1019',
            'KS-1187', 'thirteen', 'THIRTEEN', 'stylelint', 'scripts/preflight/', 'lockfile-cleanroom', 'githooks', '17:4', '17:5', 'feature/ks-']
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
        if '#1025' in l: print('#1025 at line %d: %s' % (i, l[:110]))
    print('ENUMERATED count #1025 = %d (scratch copy written to %s; nothing written to launchers/)' % (s.count('#1025'), out_path)); sys.exit(0)

controls = [
    ('HEAD_SHA="${QA1025_HEAD:-' + HEAD + '}"', 1), ("MERGE_BASE='" + BASE + "'", 1), ("DEVELOP_SHA='" + DEVELOP + "'", 1),
    ("BRANCH='" + BRANCH + "'", 1), (STEM + '.md', 2), (STEM + '.prompt.txt', 1), ("SUBJECT='" + SUBJECT + "'", 1), ("REPORT_DIR='" + REPORT_DIR + "'", 1),
    ('exit 2;', 1), ('exit 3;', 1), ('exit 4;', 1), ('exit 5;', 1), ('exit 6', 1), ('exit 7;', 1), ('exit 8;', 1), ('exit 9;', 1),
    ('exit 10;', 1), ('exit 11;', 1), ('exit 12;', 1), ('exit 13;', 1), ('exit 14;', 1), ('exit 15;', 1), ('exit 16;', 2), ('exit 17;', 1),
    ('exit 18; }', 1), ('exit 18 ;;', 1), ('exit 19 ;;', 1), ('exit 20;', 1), ('exit 21;', 1), ('exit 22;', 1), ('exit 23;', 1),
    ('DEV_CONTENT_ALLOWED = {', 1), ('print("LANDED ', 1), ('print("GUARDED ', 2), ('print("UNJUDGEABLE ', 3), ('LANDED*)', 1), ('OK*)', 1),
    ('45ef8220f26ac164939da5b0425dab01116f7a18', 1), ('e6f2184d2dde6de00fb79618de3621659998e307', 1), ('8e236ee70ce1a4634552596fb86fcffce234f221', 1),
    ('aff23b0420ced863884787443a35f28cf727bd09', 1), ('2504d9a28dc017fcaabfc88248bf1c64431eb38a', 1), ('3dd903b527f26c758cc1da84b10cc0a0db3b1d46', 1),
    ('92eea6087a6c442f1a14e735ba9fcca74493bd0a', 1), ('29c9fc48f32857d4f24ef944b9868639e0171435', 1), ('2379c0aeee6e3e3f0c4ef3a2512e3a590ad47d29', 1),
    ('f102d9d4c4523091fe4e3119d6c539fb29bfd904', 1), ('40079f6fb41e146a34a66463e352b9c0a49f91e8', 1), ('04f9fe46068b397a6fc24d647b7e3ec4315c15e7', 1),
    ('d5977b6a13638558ef57e8c294809d7ada8be6cd', 1), ('ffb2b110a2d69c2c9a10e6caf5666c5fa08ec62c', 1), ('99db3e7c2434f65eb64ab0d8db5775e11eefd6bd', 1),
    ('ahead=1 files=1', 2), ('[ -t 0 ]', 1), ('exec claude --dangerously-skip-permissions --model opus', 1),
    ('git -C "$REPO"', 2), ('set -u', 1), ('MAIL YOUR VERDICT', 1), ('NEVER print a credential value', 1), ('no memory maintenance', 1),
    ("grep -q 'TIER 2'", 2), ("grep -q 'ROUND 1'", 2), ('GUARDED = [D + "scripts/audit/",', 1), ('D + "package-lock.json"]', 1),
    ('if [ "${1:-}" = "--check" ]; then', 1), ('state.append(short + ', 1), ("grep -qF 'NOT-TESTED.written-first.md'", 1), ("grep -qF 'MERGE ADDENDUM'", 1),
    ('#1025', COUNT_1025),
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
