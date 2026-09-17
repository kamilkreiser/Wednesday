#!/usr/bin/env python3
"""gen_launcher_1033.py — derive launch_qa_secuura_ks763_1033.sh from the #1030 launcher launchers/launch_qa_secuura_ks1211_1030.sh (lock/override
class, verdicted GO WITH FINDINGS tonight) by ASSERTED substitutions and asserted SEGMENT replacement: every anchor must occur exactly as often as
stated, or the generator refuses and writes nothing.
The develop arm stays PATH BLOBS ONLY, never develop's SHA: the 4 non-audit PR paths (root lock + manifest, originate lock + manifest), EVERY file of
Blockchain/Dev/scripts/audit/ (13; the listing must name exactly these), plus 3 REACH paths with no #1033 blob (originate Dockerfile = the runtime
step, prisma/schema.prisma = the datasource provider, packages/shared/package-lock.json = the /shared tree the image copies). Pins are re-read from
the Secuura checkout with read-only `git rev-parse` at generation time.
CHANGED ON PURPOSE vs #1030: tier/round greps TIER 1; exit 26 now requires unique container naming + jest --runInBand + load average (containers are
ALLOWED for this gate, the #1030 "Docker is NOT available" guard would be false); exit 27 requires RUNTIME REACH FIRST; NEW exit 28 requires the
npm-version-dependent root-lock recipe finding (host npm 11.5.1 cannot reproduce 646c19f6f; npm 11.19.0 does). QA1033_CUR_DEV --check-only override.
Then a RESIDUAL GUARD (tokens of the #1030 gate), output controls, heredoc apostrophe/paren parity, no git write verbs, no control bytes, bash -n.
Never overwrites an existing output without a .pre-* copy.
Usage: gen_launcher_1033.py <template launcher> <output launcher>
Exit: 0 written · 1 an anchor/control count disagreed · 2 a residual token survived · 3 bash -n failed"""
import datetime, hashlib, os, re, shutil, subprocess, sys

src_path, out_path = sys.argv[1], sys.argv[2]
s = open(src_path, encoding='utf-8').read()
def refuse(msg, code):
    print('REFUSING: ' + msg, file=sys.stderr); sys.exit(code)
REPO = '/Volumes/DevMASTER/!CODING/Secuura/Blockchain/2_Project_Files'
HEAD = '2cab54988b4e7b71d403576719f5fd80e470fa92'
BASE = 'bb848b8283eb5ee6a6180067315b76f1321e7b6b'      # merge-base of head with develop = the develop 2cab54988 merged in (#1030 squash)
DEVELOP = '27e53ec3aa010b50cd9b2e4a1d15cbb34605ba7d'   # origin develop at draft (#1029, one api-gateway test file) — informational, NOT a guard
OLD_HEAD = 'e43af493418a1f13cfb60c994380fb74d79ad07e'
OLD_BASE = '20ab16f9a80c5c3c75e613d8c670efefd8f5cafb'
OLD_DEVELOP = '75ad0e55c6335a5f34f6d0b74dfe00b334b2eb2e'
BRANCH = 'refs/heads/feature/ks-763-override-mysql2'
STEM = '2026-09-17_secuura-1033-ks763-mysql2-tier1'
OLD_STEM = '2026-09-17_secuura-1030-ks1211-vitest-tier2'
REPORT_DIR = '/Volumes/DevMASTER/!CODING/Testing Agent MAIN/projects/secuura/reports/2026-09-17-ks763-1033-2cab54988-tier1-r1/'
OLD_REPORT_DIR = '/Volumes/DevMASTER/!CODING/Testing Agent MAIN/projects/secuura/reports/2026-09-17-ks1211-1030-e43af4934-tier2-r1/'
SUBJECT = '[QA -> Wednesday] TIER 1 GATE #1033 (KS-763) 2cab54988 — '
OLD_SUBJECT = '[QA -> Wednesday] TIER 2 GATE #1030 (KS-1211) e43af4934 — '
AUDIT_DIR = 'Blockchain/Dev/scripts/audit'
REACH = ['Blockchain/Dev/services/originate/Dockerfile', 'Blockchain/Dev/prisma/schema.prisma', 'Blockchain/Dev/packages/shared/package-lock.json']

def git(*a):
    p = subprocess.run(['git', '-C', REPO] + list(a), capture_output=True, text=True)
    if p.returncode != 0: refuse('git %r rc %d %s' % (a, p.returncode, p.stderr[-200:]), 1)
    return p.stdout.strip()
pr_paths = git('diff', '--name-only', BASE + '...' + HEAD).splitlines()
if len(pr_paths) != 5: refuse('PR paths %d, want 5' % len(pr_paths), 1)
nonaudit = [p for p in pr_paths if not p.startswith(AUDIT_DIR + '/')]
if len(nonaudit) != 4: refuse('non-audit PR paths %d, want 4' % len(nonaudit), 1)
audit_files = [l.split('\t')[1].rsplit('/', 1)[1] for l in git('ls-tree', BASE, AUDIT_DIR + '/').splitlines() if l.split()[1] == 'blob']
if len(audit_files) != 13 or 'audit-baseline.json' not in audit_files: refuse('scripts/audit files %d' % len(audit_files), 1)
if git('rev-parse', DEVELOP + ':' + AUDIT_DIR) != git('rev-parse', BASE + ':' + AUDIT_DIR): refuse('scripts/audit tree differs base vs draft develop', 1)
rows = []
for p in nonaudit:
    b, h, c = git('rev-parse', BASE + ':' + p), git('rev-parse', HEAD + ':' + p), git('rev-parse', DEVELOP + ':' + p)
    if b == h or b != c: refuse('pin sanity %s base %s head %s develop %s' % (p, b[:9], h[:9], c[:9]), 1)
    rows.append((p, b, h))
for p in REACH:
    b, h, c = git('rev-parse', BASE + ':' + p), git('rev-parse', HEAD + ':' + p), git('rev-parse', DEVELOP + ':' + p)
    if not (b == h == c): refuse('reach pin sanity %s base %s head %s develop %s' % (p, b[:9], h[:9], c[:9]), 1)
    rows.append((p, b, ''))
arows = []
for n in sorted(audit_files):
    p = AUDIT_DIR + '/' + n
    b, h = git('rev-parse', BASE + ':' + p), git('rev-parse', HEAD + ':' + p)
    if (n == 'audit-baseline.json') != (b != h): refuse('audit pin sanity %s' % n, 1)
    arows.append((n, b, h if b != h else ''))
if sum(1 for r in arows if r[2]) != 1: refuse('audit own blobs', 1)

NEW_HEADER = '''#!/bin/bash
# launch_qa_secuura_ks763_1033.sh — cross-project QA agent, ONE TIER 1 ROUND 1 gate over Secuura/Blockchain PR #1033
# (KS-763, Seat B, PR-7: mysql2 override to 3.23.1 against prisma's exact pin "3.15.3"; GHSA-rgwj-5xj2-c3m3 moderate + GHSA-3f6p-5ww8-9rcr high)
# @ 2cab54988b4e7b71d403576719f5fd80e470fa92 — TWO commits: 9fd3cb924 (2 manifests, 2 locks, 2 baseline rows removed, 31 -> 29) and 2cab54988
# (a merge of develop bb848b828 = #1026 + #1028 + #1030). 5 files vs develop: Blockchain/Dev/package.json + package-lock.json,
# services/originate/package.json + package-lock.json, scripts/audit/audit-baseline.json. TIER 1 because mysql2 ships in the originate runtime image.
#
# THE SHAPE, as read 22:46-23:02 AEST 2026-09-17 (git ls-remote + the PR and compare APIs): head parents 9fd3cb924 + bb848b828; origin develop
# 27e53ec3a (#1029, one api-gateway test file — 0 of the 5). compare develop...head = merge_base bb848b828, status diverged, ahead 2, behind 1,
# files 5. Asserted: merge_base + ahead + files (exit 10); behind is NOT asserted.
#
# THE DEVELOP ARM IS JUDGED BY PATH BLOBS, NEVER BY DEVELOP'S SHA (develop moves often). GUARDED PATHS, each read from its parent directory's
# GitHub contents listing at the CURRENT develop (5 listings):
#   (a) the 4 non-audit PR paths: Blockchain/Dev/{package.json, package-lock.json}; Blockchain/Dev/services/originate/{package.json, package-lock.json};
#   (b) EVERY file of Blockchain/Dev/scripts/audit/ (13 at draft, incl. audit-baseline.json, audit-gate.mjs, audit-locks.mjs); the listing must
#       name exactly these 13;
#   (c) 3 REACH paths with no #1033 blob: services/originate/Dockerfile (the runtime step), prisma/schema.prisma (the datasource provider),
#       packages/shared/package-lock.json (the /shared tree the image copies).
# Every path at its merge-base blob -> OK (develop's SHA is printed, not judged). ALL 5 PR paths at their #1033 blobs (reach paths unmoved) -> exit 19
# LANDED. Any path at a blob nobody pinned, a file absent, a scripts/audit/ file added or removed, or a PARTIAL landing -> exit 18 GUARDED.
# TEN open Dependabot PRs touch the root lock (#949 #948 #947 #946 #945 #649 #639 #635 #575 #572; #949 prisma 7.8.0 -> 7.10.0 and #575 also
# services/originate/package.json; #945 and #920 the root package.json): one of them landing first REFUSES here by design — re-pin deliberately.
#
# exit 21: the LAUNCH path refuses when stdin is not a TTY. This launcher execs an interactive agent; run it in a cockpit pane, never inside a
# Bash tool — and never run it without --check to "prove" this guard. `--check` runs headless (it launches nothing).
# exit 22: the prompt must require node_modules farmed PER ENTRY.
# exit 23: brief AND prompt must carry the exact #1033 verdict subject; the prompt must name coagent@ as sender and wednesday-agent@ as recipient.
# exit 24: brief AND prompt must name the REPORT DIRECTORY; the prompt must name NOT-TESTED.written-first.md (written FIRST, before any run).
# exit 25: brief AND prompt must carry the MERGE ADDENDUM.
# exit 26: the prompt must require every container named uniquely, jest --runInBand in containers, and the host load average beside every timed run.
# exit 27: brief AND prompt must carry the RUNTIME REACH FIRST rule (the verdict's first line; the tier depends on it).
# exit 28: brief AND prompt must carry the npm-version dependent root-lock finding (host npm cannot reproduce the root lock; a false NO GO trap).
# QA1033_CUR_DEV (test override, --check only): stands in for origin develop so the LANDED / GUARDED arms and an older develop can be proven.
# A launch with any QA1033_* override set refuses (exit 16).
#
# Generated by gatesets/2026-09-17_gate1033/gen_launcher_1033.py from launch_qa_secuura_ks1211_1030.sh (asserted substitutions + segment
# replacement + pins re-read from the repo + residual guard + output controls + bash -n). Exit codes 2..28 (19 = LANDED).
# Written by the generator because it contains a legitimate directory change.
#
# Usage: launch_qa_secuura_ks763_1033.sh [--check]
# Exit: 0 launched (or guards passed under --check) · 2..28 a guard refused
'''
marker = 'set -u\n'
if s.count(marker) != 1: refuse('header marker set -u count %d' % s.count(marker), 1)
s = NEW_HEADER + s[s.index(marker):]

def segment(start, end):
    if s.count(start) != 1: refuse('segment start %r count %d' % (start[:60], s.count(start)), 1)
    i = s.index(start); j = s.find(end, i)
    if j < 0: refuse('segment end %r not found' % end[:40], 1)
    return s[i:j + len(end)]

# 1) the JUDGED dict
old_j = segment('JUDGED = {\n', '\n}\n# EVERY file of Blockchain/Dev/scripts/audit/')
new_j = 'JUDGED = {\n' + '\n'.join('  "%s": ["%s", "%s"],' % r for r in rows) + '\n}\n# EVERY file of Blockchain/Dev/scripts/audit/'
s = s.replace(old_j, new_j)
# 2) the AUDIT dict
old_a = segment('AUDIT = {\n', '\n}\nfor n, v in AUDIT.items():')
new_a = 'AUDIT = {\n' + '\n'.join('  "%s": ["%s", "%s"],' % r for r in arows) + '\n}\nfor n, v in AUDIT.items():'
s = s.replace(old_a, new_a)

subs = [
    ('QA1030_BRIEF', 'QA1033_BRIEF', 2),
    ('QA1030_PROMPT', 'QA1033_PROMPT', 2),
    ('QA1030_HEAD', 'QA1033_HEAD', 2),
    ('QA1030_CUR_DEV', 'QA1033_CUR_DEV', 4),
    (OLD_STEM, STEM, 3),
    ("BRANCH='refs/heads/feature/ks-1211-bump-vitest'", "BRANCH='" + BRANCH + "'", 1),
    (OLD_HEAD, HEAD, 1),
    ("MERGE_BASE='" + OLD_BASE + "'   # the merge-base of the head with develop = the develop 566107f01 merged in (#1027 squash, on #1018)",
     "MERGE_BASE='" + BASE + "'   # the merge-base of the head with develop = the develop 2cab54988 merged in (#1030 squash)", 1),
    ("DEVELOP_SHA='" + OLD_DEVELOP + "'   # develop at draft = #1026 squash (ls-remote 21:06:26 and 21:08:32 AEST) — PRINTED, never a guard",
     "DEVELOP_SHA='" + DEVELOP + "'   # develop at draft = #1029 squash (ls-remote 22:46:44, 22:50:15 and 23:02:00 AEST) — PRINTED, never a guard", 1),
    ("REPORT_DIR='" + OLD_REPORT_DIR + "'", "REPORT_DIR='" + REPORT_DIR + "'", 1),
    ("SUBJECT='" + OLD_SUBJECT + "'", "SUBJECT='" + SUBJECT + "'", 1),
    ('echo "REFUSING: #1030 — $HEAD_SHA is not at', 'echo "REFUSING: #1033 — $HEAD_SHA is not at', 1),
    ('# develop...#1030 = 20ab16f9a ahead 3 files 43 (behind 1 at draft time: #1026 — deliberately not asserted).',
     '# develop...#1033 = bb848b828 ahead 2 files 5 (behind 1 at draft time: #1029 — deliberately not asserted).', 1),
    ('ahead=3 files=43', 'ahead=2 files=5', 2),
    ('''{ echo "REFUSING: #1030 develop...head reads''', '''{ echo "REFUSING: #1033 develop...head reads''', 1),
    ('# path -> [merge-base blob = develop-OK, the #1030 blob = LANDED]; read by generator from the Secuura checkout with git rev-parse',
     '# path -> [merge-base blob = develop-OK, the #1033 blob = LANDED, empty for the 3 REACH paths]; read by generator from the Secuura checkout with git rev-parse', 1),
    ('# EVERY file of Blockchain/Dev/scripts/audit/ -> [merge-base blob, #1030 blob or empty]', '# EVERY file of Blockchain/Dev/scripts/audit/ -> [merge-base blob, #1033 blob or empty]', 1),
    ('%d of %d at the #1030 blob', '%d of %d at the #1033 blob', 1),
    ('all %d #1030 blobs present — #1030 has landed; this brief is stale', 'all %d #1033 blobs present — #1033 has landed; this brief is stale', 1),
    ('[42 PR paths + all %d files of scripts/audit/]', '[4 PR paths + 3 reach paths + all %d files of scripts/audit/]', 1),
    ("grep -q 'TIER 2' \"$BRIEF\" && grep -q 'TIER 2' \"$PROMPT_FILE\"", "grep -q 'TIER 1' \"$BRIEF\" && grep -q 'TIER 1' \"$PROMPT_FILE\"", 1),
    ('''grep -qi 'Docker is NOT available' "$PROMPT_FILE" && grep -qi 'load average' "$PROMPT_FILE" \\
  || { echo "REFUSING: prompt does not say Docker is NOT available or does not require the host load average beside timed runs" >&2; exit 26; }''',
     '''grep -qi 'name it uniquely' "$PROMPT_FILE" && grep -qF -- '--runInBand' "$PROMPT_FILE" && grep -qi 'load average' "$PROMPT_FILE" \\
  || { echo "REFUSING: prompt does not require unique container names, jest --runInBand in containers, or the host load average beside timed runs" >&2; exit 26; }''', 1),
    ('''grep -qF 'TIER 1 TRIGGERED' "$PROMPT_FILE" && grep -qF 'TIER 1 TRIGGERED' "$BRIEF" \\
  || { echo "REFUSING: brief or prompt does not carry the TIER 1 TRIGGERED rule" >&2; exit 27; }''',
     '''grep -qF 'RUNTIME REACH FIRST' "$PROMPT_FILE" && grep -qF 'RUNTIME REACH FIRST' "$BRIEF" \\
  || { echo "REFUSING: brief or prompt does not carry the RUNTIME REACH FIRST rule" >&2; exit 27; }
grep -qi 'npm-version dependent' "$PROMPT_FILE" && grep -qi 'npm-version dependent' "$BRIEF" \\
  || { echo "REFUSING: brief or prompt does not carry the npm-version dependent root-lock finding (host npm cannot reproduce the root lock)" >&2; exit 28; }''', 1),
    ('does not carry the exact #1030 verdict subject', 'does not carry the exact #1033 verdict subject', 1),
    ('echo "  head on origin: #1030 $HEAD_SHA at $BRANCH"', 'echo "  head on origin: #1033 $HEAD_SHA at $BRANCH"', 1),
    ('echo "  compare (GitHub API): develop...#1030 = $COMPARE"', 'echo "  compare (GitHub API): develop...#1033 = $COMPARE"', 1),
    ('echo "  brief and prompt agree on TIER 2 and ROUND 1"', 'echo "  brief and prompt agree on TIER 1 and ROUND 1"', 1),
    ('echo "  prompt requires node_modules farmed per ENTRY; says Docker is NOT available; requires the host load average beside timed runs"',
     'echo "  prompt requires node_modules farmed per ENTRY; unique container names; jest --runInBand in containers; the host load average beside timed runs"', 1),
    ('echo "  brief and prompt carry the MERGE ADDENDUM and the TIER 1 TRIGGERED rule"',
     'echo "  brief and prompt carry the MERGE ADDENDUM, the RUNTIME REACH FIRST rule and the npm-version dependent root-lock finding"', 1),
    ('echo "  guarded paths (blobs at the current develop): the 42 non-audit PR paths + every file of Blockchain/Dev/scripts/audit/ (13, incl. audit-baseline.json)"',
     'echo "  guarded paths (blobs at the current develop): the 4 non-audit PR paths + 3 reach paths (originate Dockerfile, prisma/schema.prisma, packages/shared lock) + every file of Blockchain/Dev/scripts/audit/ (13, incl. audit-baseline.json)"', 1),
]
for old, new, n in subs:
    c = s.count(old)
    if c != n: refuse('anchor %r occurs %d times, expected %d' % (old[:70], c, n), 1)
    s = s.replace(old, new)

residual = ['1030', 'e43af493', '20ab16f9', '75ad0e55', 'vitest', 'KS-1211', 'GHSA-82fw', 'issuer', 'ahead=3', 'files=43', '42 non-audit', '42 PR',
            'TIER 2', 'TIER 1 TRIGGERED', 'Docker is NOT available', '566107f01', '#1027', '#1018', '#1026', '21:0', '21:1', '21:2', 'twenty']
permitted = [('from launch_qa_secuura_ks1211_1030.sh (asserted', 1), ('(a merge of develop bb848b828 = #1026 + #1028 + #1030)', 1),
             ('(#1030 squash)', 1)]
body = s
for ph, n in permitted:
    if body.count(ph) != n: refuse('permitted phrase %r count %d, want %d' % (ph, body.count(ph), n), 1)
    body = body.replace(ph, '<permitted>')
hits = []
for tok in residual:
    pat = r'(?<![0-9a-fA-F])' + re.escape(tok) + r'(?![0-9a-fA-F])' if tok.isdigit() else re.escape(tok)
    for m in re.finditer(pat, body): hits.append((tok, body.count('\n', 0, m.start()) + 1))
lines = body.split('\n')
if hits:
    for tok, line in hits: print('REFUSING: residual token %r at line %d: %s' % (tok, line, lines[line - 1][:120]), file=sys.stderr)
    sys.exit(2)

controls = [
    ('HEAD_SHA="${QA1033_HEAD:-' + HEAD + '}"', 1), ("MERGE_BASE='" + BASE + "'", 1), ("DEVELOP_SHA='" + DEVELOP + "'", 1),
    ("BRANCH='" + BRANCH + "'", 1), (STEM + '.md', 2), (STEM + '.prompt.txt', 1), ("REPORT_DIR='" + REPORT_DIR + "'", 1), ("SUBJECT='" + SUBJECT + "'", 1),
    ('exit 2;', 1), ('exit 3;', 1), ('exit 4;', 1), ('exit 5;', 1), ('exit 6', 1), ('exit 7;', 1), ('exit 8;', 1), ('exit 9;', 1),
    ('exit 10;', 1), ('exit 11;', 1), ('exit 12;', 1), ('exit 13;', 1), ('exit 14;', 1), ('exit 15;', 1), ('exit 16;', 2), ('exit 17;', 1),
    ('exit 18; }', 1), ('     exit 18 ;;', 1), ('exit 19 ;;', 1), ('exit 20;', 1), ('exit 21;', 1), ('exit 22;', 1), ('exit 23;', 1), ('exit 24;', 1),
    ('exit 25;', 1), ('exit 26;', 1), ('exit 27;', 1), ('exit 28;', 1),
    ('print("LANDED ', 1), ('print("GUARDED ', 2), ('print("UNJUDGEABLE ', 1), ('LANDED*)', 1), ('OK*)', 1),
    ('ahead=2 files=5', 2), ('[ -t 0 ]', 1), ('exec claude --dangerously-skip-permissions --model opus', 1),
    ('set -u', 1), ('MAIL YOUR VERDICT', 1), ('NEVER print a credential value', 1), ('no memory maintenance', 1),
    ("grep -q 'TIER 1'", 2), ("grep -q 'ROUND 1'", 2), ('QA1033_CUR_DEV', 5), ("'name it uniquely'", 1), ("'RUNTIME REACH FIRST'", 2), ("'npm-version dependent'", 2),
] + [('  "%s": ["%s", "%s"],' % r, 1) for r in rows] + [('  "%s": ["%s", "%s"],' % r, 1) for r in arows]
bad = [(k, want, s.count(k)) for k, want in controls if s.count(k) != want]
if bad: refuse('output controls %r' % bad, 1)
if s.count('JUDGED = {') != 1 or len(re.findall(r'^  "Blockchain/Dev/[^"]+": \["[0-9a-f]{40}", "(?:[0-9a-f]{40})?"\],$', s, flags=re.M)) != 7: refuse('JUDGED row count', 1)
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
      'subs', len(subs), '+ 2 segments', 'controls', len(controls), 'judged', len(rows), '(4 PR + 3 reach) + audit', len(arows), 'residual guard clean', 'bash -n rc', rc,
      'pyj apostrophes', pyj.count("'"), 'pyj parens', pyj.count('('))
sys.exit(0 if rc == 0 else 3)
