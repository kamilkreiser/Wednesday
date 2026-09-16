#!/usr/bin/env python3
"""gen_launcher_1008.py — derive launch_qa_secuura_ks1087_1008.sh from tonight's #1006 TIER 1 launcher
(launchers/launch_qa_secuura_ks844_1006.sh — guard family: head on origin exit 6, compare exit 10/13, develop judged BY CONTENT exit
18/19, head SHA named in brief+prompt exit 20, TTY exit 21) by ASSERTED substitutions: every anchor must occur exactly as often as
stated, or the generator refuses and writes nothing. Then a RESIDUAL GUARD (any token of the source gate left anywhere, after stripping
the one permitted template-name mention, is a refusal), output controls (every count measured against the composed text; '#1008' is
ENUMERATED first with --enumerate, which writes only to the scratch path given and prints the lines), PY/PYJ-heredoc apostrophe/paren
parity, no git write verbs, no control bytes, bash -n. Never overwrites an existing output without a .pre-* copy.
Usage: gen_launcher_1008.py <template launcher> <output launcher> [--enumerate]
Exit: 0 written · 1 an anchor/control count disagreed · 2 a residual token survived · 3 bash -n failed"""
import datetime, hashlib, os, re, shutil, subprocess, sys

src_path, out_path = sys.argv[1], sys.argv[2]
ENUMERATE = '--enumerate' in sys.argv[3:]
s = open(src_path, encoding='utf-8').read()
def refuse(msg, code):
    print('REFUSING: ' + msg, file=sys.stderr); sys.exit(code)

HEAD = 'dd7086d5aa574285beffc515f9371a438621f25d'
BASE = '93629700c3d219c1d8ca61d69150bb9b623fc1be'     # the merge-base = develop itself: develop is an ANCESTOR of the head
DEVELOP = '93629700c3d219c1d8ca61d69150bb9b623fc1be'  # develop at draft time (git ls-remote 00:55:40, branches API 00:57:25)
BRANCH = 'refs/heads/feature/ks-1087-ornith-workflow-approve-keeps-pending'
STEM = '2026-09-17_secuura-1008-ks1087-tier1'
OLD_STEM = '2026-09-17_secuura-1006-ks844-tier1'
TEMPLATE_NAME = 'launch_qa_secuura_ks844_1006.sh'
COUNT_1008 = None if ENUMERATE else int(os.environ.get('COUNT_1008', '-1'))  # MEASURED by --enumerate first; passed in, never guessed

NEW_HEADER = '''#!/bin/bash
# launch_qa_secuura_ks1087_1008.sh — cross-project QA agent, ONE TIER 1 ROUND 1 gate over Secuura/Blockchain PR #1008
# (KS-1087 item 1, Seat A) @ dd7086d5aa574285beffc515f9371a438621f25d — ONE commit on develop 93629700c, 2 files, both
# services/api-gateway: routes/verification.ts +9 -1 (POST /api/workflow-instances/:id/approve awaits the forward status: non-2xx or a
# transport error answers 502 ORIGINATE_FORWARD_FAILED and keeps the pending document; only a 2xx deletes it) and a new 3-cell
# ks1087 test. TIER 1: a new 502 on an authenticated route mounted in every environment, deciding whether a document is DELETED.
#
# THE SHAPE, as read 00:55-01:06 AEST 2026-09-17 (git + the compare API agree): develop 93629700c is an ANCESTOR of the head
# (merge-base = develop, behind 0), so the merged tree IS the head tree. compare develop...head = merge_base 93629700c, status ahead,
# ahead 1, behind 0, files 2. The compare is asserted as merge_base + ahead + files (exit 10); `behind` is deliberately NOT asserted,
# so a develop that moves on does not trip this guard — the develop arm judges the move by CONTENT.
#
# The develop pin is judged by CONTENT, not bare: (a) ELEVEN files by blob at the CURRENT develop — verification.ts (base
# de34b2de7; the PR's own d0585dc34 -> exit 19 LANDED) and ten files the gate's predictions stand on: api-gateway src/index.ts (the
# unconditional mount), src/middleware/auth.ts (authenticateToken), src/services/redis.ts (the pending-document TTL),
# src/services/enforcement.ts (who writes the pending document), package.json, vitest.config.ts, vitest.setup.ts, tsconfig.json
# (the exclude the including tsc overrides), originate src/routes/documents.ts (the forward target) and Dev eslint.config.mjs —
# any blob nobody pinned -> exit 18 (the new ks1087 test is NOT judged: it is absent on develop, and verification.ts already
# detects a landing); (b) if develop moved past 93629700c, the compare pinned...develop REFUSES (exit 18) only when the delta touches
# a GUARDED path — those eleven files, the ks1087 test, docs/openapi/, the Dev lockfile, issuer DocumentList.tsx, mcp-server
# api-client.ts — or cannot be judged; anything else (the file-disjoint sibling lane PRs landing) proceeds and the gate re-derives
# the api-gateway denominator on the merged tree.
# DEV_CONTENT_ALLOWED is empty: dependabot #649/#575 touch api-gateway package.json and the Dev lockfile — if one lands, this
# launcher refuses and the brief is re-pinned deliberately.
#
# exit 21: the LAUNCH path refuses when stdin is not a TTY. This launcher execs an interactive agent; run it in a cockpit
# pane, never inside a Bash tool. `--check` still runs headless (it launches nothing).
#
# Adapted from launch_qa_secuura_ks844_1006.sh by gen_launcher_1008.py (asserted substitutions + residual guard + output
# controls + bash -n): same guards and exit codes, re-pointed at #1008. Exit codes 2..21 (19 = LANDED).
# Written by the generator because it contains a legitimate directory change.
#
# Usage: launch_qa_secuura_ks1087_1008.sh [--check]
# Exit: 0 launched (or guards passed under --check) · 2..21 a guard refused
'''
marker = 'set -u\n'
if s.count(marker) != 1: refuse('header marker set -u count %d' % s.count(marker), 1)
s = NEW_HEADER + s[s.index(marker):]

J = lambda *lines: '\n'.join(lines)
GW = 'services/api-gateway/'
NEW_JUDGED = J(
 '# file -> (develop-OK blobs {blob: label}, LANDED blobs {blob: label})',
 'JUDGED = {',
 '  D + "services/api-gateway/src/routes/verification.ts":           ({"de34b2de7372873d60987f8bc742df3a13140265": "base"}, {"d0585dc34ceb5e3580ade38633250a6ffeaebd69": "#1008 own"}),',
 '  D + "services/api-gateway/src/index.ts":                         ({"6f38c819e48162e3179aaf557085766f91beecc1": "base"}, {}),',
 '  D + "services/api-gateway/src/middleware/auth.ts":               ({"20311010db0eb8ba097644ce105cf8df966ce456": "base"}, {}),',
 '  D + "services/api-gateway/src/services/redis.ts":                ({"47659ee9c9f06acf9ac64e09b2dc207113ba92ea": "base"}, {}),',
 '  D + "services/api-gateway/src/services/enforcement.ts":          ({"533cd309c56b8167ebe00b620744259b3cc186cc": "base"}, {}),',
 '  D + "services/api-gateway/package.json":                         ({"841d8c6adcd71e885c01e65c22da9418daff276a": "base"}, {}),',
 '  D + "services/api-gateway/vitest.config.ts":                     ({"5888e0b320d934f6f434e0e5ca3c74a995cecc02": "base"}, {}),',
 '  D + "services/api-gateway/vitest.setup.ts":                      ({"22c1107683b8192df3bfd3e929aa94aff3dc7d45": "base"}, {}),',
 '  D + "services/api-gateway/tsconfig.json":                        ({"c981e6a92fdd2417fa35070eb979c5f1c77ffbcd": "base"}, {}),',
 '  D + "services/originate/src/routes/documents.ts":                ({"c3a818ac8ac8de1b385540d15e3fbb23200cea30": "base"}, {}),',
 '  D + "eslint.config.mjs":                                          ({"8c5374c6022eb0a3f449f41a570db61294aa63f1": "base"}, {}),',
 '}\n')
NEW_GUARDED = J(
 'GUARDED = [D + "services/api-gateway/src/routes/verification.ts",',
 '           D + "services/api-gateway/src/__tests__/ks1087-workflow-approve-deletes-the-pending-document.test.ts",',
 '           D + "services/api-gateway/src/index.ts",',
 '           D + "services/api-gateway/src/middleware/auth.ts",',
 '           D + "services/api-gateway/src/services/redis.ts",',
 '           D + "services/api-gateway/src/services/enforcement.ts",',
 '           D + "services/api-gateway/package.json",',
 '           D + "services/api-gateway/vitest.config.ts",',
 '           D + "services/api-gateway/vitest.setup.ts",',
 '           D + "services/api-gateway/tsconfig.json",',
 '           D + "services/originate/src/routes/documents.ts",',
 '           D + "docs/openapi/",',
 '           D + "eslint.config.mjs",',
 '           D + "frontend/issuer/src/components/DocumentList.tsx",',
 '           D + "services/mcp-server/src/api-client.ts",',
 '           D + "package-lock.json"]',
 '# SUFFIX-GUARDED: none for this gate — every guarded path above is exact or a directory prefix.',
 'GUARDED_SUFFIX = []\n')
NEW_ALLOWED = J(
 '# STYLE NOTE (912r2 launcher, measured): bash scans quote/paren state THROUGH this heredoc because it sits inside a',
 '# command substitution — keep apostrophes and parentheses EVEN (this block uses none of the former), or the outer $( ) breaks.',
 '# CONTENT-JUDGED allowlist: a hit under a GUARDED path clears ONLY if the per-file blob sha in the compare is EXACTLY one',
 '# pinned here. EMPTY for this gate: at draft time 00:57 AEST no open lane PR touched a guarded path except dependabot',
 '# bumps of api-gateway package.json and the Dev lockfile, which must NOT clear silently, so every guarded hit falls through to GUARDED and exit 18 — re-pin deliberately.',
 'DEV_CONTENT_ALLOWED = {',
 '}\n')

def block(start, end_marker):
    i = s.find(start)
    if i < 0 or s.count(start) != 1: refuse('block start %r count %d' % (start[:50], s.count(start)), 1)
    j = s.find(end_marker, i)
    if j < 0: refuse('block end %r not found' % end_marker[:40], 1)
    return s[i:j + len(end_marker)]
old_judged = block('# file -> (develop-OK blobs {blob: label}, LANDED blobs {blob: label})', '}\n')
old_guarded = block('GUARDED = [D + "services/demo-service/",', 'GUARDED_SUFFIX = ["/middleware/errorHandler.ts"]\n')
old_allowed = block('# STYLE NOTE (912r2 launcher, measured)', 'DEV_CONTENT_ALLOWED = {\n')
old_allowed = old_allowed + s[s.index(old_allowed) + len(old_allowed): s.index('}\n', s.index(old_allowed) + len(old_allowed)) + 2]

subs = [
    (old_judged, NEW_JUDGED, 1),
    (old_guarded, NEW_GUARDED, 1),
    (old_allowed, NEW_ALLOWED, 1),
    ('QA1006_BRIEF', 'QA1008_BRIEF', 2),
    ('QA1006_PROMPT', 'QA1008_PROMPT', 2),
    ('QA1006_HEAD', 'QA1008_HEAD', 2),
    (OLD_STEM, STEM, 3),
    ('refs/heads/feature/ks-844-demo-service-error-handler', BRANCH, 1),
    ('86fe59e6bf07108142fb3dbd06bef8747d2a4687', HEAD, 1),
    ("MERGE_BASE='40fe4db6963cd11dba06bd46e0b00af39e68ef3a'   # the merge-base of the head with develop = develop itself (develop is an ancestor of the head; behind 0)",
     "MERGE_BASE='" + BASE + "'   # the merge-base of the head with develop = develop itself (develop is an ancestor of the head; behind 0)", 1),
    ("DEVELOP_SHA='40fe4db6963cd11dba06bd46e0b00af39e68ef3a'   # develop at draft time = the PR base (git ls-remote 00:28:49, branches API 00:31:54 AEST)",
     "DEVELOP_SHA='" + DEVELOP + "'   # develop at draft time = the PR base (git ls-remote 00:55:40, branches API 00:57:25 AEST)", 1),
    ('echo "REFUSING: #1006 — $HEAD_SHA is not at', 'echo "REFUSING: #1008 — $HEAD_SHA is not at', 1),
    ('# develop...#1006 = 40fe4db69 ahead 2 files 5 (behind 0; behind deliberately not asserted).', '# develop...#1008 = 93629700c ahead 1 files 2 (behind 0; behind deliberately not asserted).', 1),
    ('''[ "$COMPARE" = "$MERGE_BASE ahead=2 files=5" ] || { echo "REFUSING: #1006 develop...head reads '$COMPARE', brief pins '$MERGE_BASE ahead=2 files=5'" >&2; exit 10; }''',
     '''[ "$COMPARE" = "$MERGE_BASE ahead=1 files=2" ] || { echo "REFUSING: #1008 develop...head reads '$COMPARE', brief pins '$MERGE_BASE ahead=1 files=2'" >&2; exit 10; }''', 1),
    ('# The develop pin, judged by CONTENT (see the header): twelve files by blob at the CURRENT develop, then — if develop',
     '# The develop pin, judged by CONTENT (see the header): eleven files by blob at the CURRENT develop, then — if develop', 1),
    ('" — #1006 has landed; this brief is stale")', '" — #1008 has landed; this brief is stale")', 1),
    ('tail = "the gate merges the then-current develop onto 86fe59e6b in its own clone, rebuilds the shared dist there, runs the packages/shared and demo-service suites on the MERGED tree beside the base and head trees, names the delta and re-derives every count, above all the KS-727 exact sets and the KS-800 parsing-unit set (brief items 3 and 7)"',
     'tail = "the gate merges the then-current develop onto dd7086d5a in its own clone, rebuilds the shared dist there, runs the api-gateway suite on the MERGED tree beside the base and head trees, names the delta and re-derives every count, above all the api-gateway denominator (brief items 8 and 11)"', 1),
    ('''— disjoint from the GUARDED list (services/demo-service/, the three shared guard files, shared src/middleware/ + src/errors/ + vitest config + package.json, the Dev lockfile, any */middleware/errorHandler.ts); %s"''',
     '''— disjoint from the GUARDED list (api-gateway verification.ts + the ks1087 test + index.ts + auth.ts + redis.ts + enforcement.ts + package.json + vitest config/setup + tsconfig, originate routes/documents.ts, docs/openapi/, eslint.config.mjs, the two route consumers, the Dev lockfile); %s"''', 1),
    ('echo "  head on origin: #1006 $HEAD_SHA at $BRANCH"', 'echo "  head on origin: #1008 $HEAD_SHA at $BRANCH"', 1),
    ('echo "  compare (GitHub API): develop...#1006 = $COMPARE"', 'echo "  compare (GitHub API): develop...#1008 = $COMPARE"', 1),
]
for old, new, n in subs:
    c = s.count(old)
    if c != n: refuse('anchor %r occurs %d times, expected %d' % (old[:70], c, n), 1)
    s = s.replace(old, new)

permitted = 'Adapted from ' + TEMPLATE_NAME
if s.count(permitted) != 1: refuse('permitted template mention count %d' % s.count(permitted), 1)
body = s.replace(permitted, 'Adapted from <template>')
residual = ['1006', '844', 'KS-844', 'ks844', '86fe59e6', 'e28c91f9', '40fe4db6', 'demo', 'errorHandler', 'ks727', 'ks781', 'KS-727', 'KS-832',
            'KS-800', 'corpus', 'exact sets', 'shared guard', 'parsing-unit', 'dd714042d', '81bc26cb3', '2274c71ac', '5127297156', '288d5daf7',
            '9bcdb4259', 'ca1fe34a7', '02aef8bbc', 'c043455f5', 'ae20f7922', '0da9a28f7', '3a67987a7', 'a7abd31ef', '2a226c006', '395769231',
            '1fd016cc2', 'twelve files', 'ahead=2', 'files=5', '00:28:49', '00:31:54', '00:31 AEST', 'src/errors/']
hits = []
for tok in residual:
    pat = r'(?<![0-9a-fA-F])' + re.escape(tok) + r'(?![0-9a-fA-F])' if tok.isdigit() else re.escape(tok)
    for m in re.finditer(pat, body):
        hits.append((tok, body.count('\n', 0, m.start()) + 1))
lines = body.split('\n')
if hits:
    for tok, line in hits: print('REFUSING: residual token %r at line %d: %s' % (tok, line, lines[line - 1][:120]), file=sys.stderr)
    sys.exit(2)

if ENUMERATE:
    open(out_path, 'w', encoding='utf-8').write(s)
    for i, l in enumerate(s.split('\n'), 1):
        if '#1008' in l: print('#1008 at line %d: %s' % (i, l[:110]))
    print('ENUMERATED count #1008 = %d (scratch copy written to %s; nothing written to launchers/)' % (s.count('#1008'), out_path)); sys.exit(0)

controls = [
    ('HEAD_SHA="${QA1008_HEAD:-' + HEAD + '}"', 1), ("MERGE_BASE='" + BASE + "'", 1), ("DEVELOP_SHA='" + DEVELOP + "'", 1),
    ("BRANCH='" + BRANCH + "'", 1), (STEM + '.md', 2), (STEM + '.prompt.txt', 1),
    ('exit 2;', 1), ('exit 3;', 1), ('exit 4;', 1), ('exit 5;', 1), ('exit 6', 1), ('exit 7;', 1), ('exit 8;', 1), ('exit 9;', 1),
    ('exit 10;', 1), ('exit 11;', 1), ('exit 12;', 1), ('exit 13;', 1), ('exit 14;', 1), ('exit 15;', 1), ('exit 16;', 2), ('exit 17;', 1),
    ('exit 18; }', 1), ('exit 18 ;;', 1), ('exit 19 ;;', 1), ('exit 20;', 1), ('exit 21;', 1),
    ('DEV_CONTENT_ALLOWED = {', 1), ('print("LANDED ', 1), ('print("GUARDED ', 2), ('print("UNJUDGEABLE ', 3), ('LANDED*)', 1), ('OK*)', 1),
    ('de34b2de7372873d60987f8bc742df3a13140265', 1), ('d0585dc34ceb5e3580ade38633250a6ffeaebd69', 1), ('6f38c819e48162e3179aaf557085766f91beecc1', 1),
    ('20311010db0eb8ba097644ce105cf8df966ce456', 1), ('47659ee9c9f06acf9ac64e09b2dc207113ba92ea', 1), ('533cd309c56b8167ebe00b620744259b3cc186cc', 1),
    ('841d8c6adcd71e885c01e65c22da9418daff276a', 1), ('5888e0b320d934f6f434e0e5ca3c74a995cecc02', 1), ('22c1107683b8192df3bfd3e929aa94aff3dc7d45', 1),
    ('c981e6a92fdd2417fa35070eb979c5f1c77ffbcd', 1), ('c3a818ac8ac8de1b385540d15e3fbb23200cea30', 1), ('8c5374c6022eb0a3f449f41a570db61294aa63f1', 1),
    ('ahead=1 files=2', 2), ('[ -t 0 ]', 1), ('exec claude --dangerously-skip-permissions --model opus', 1),
    ('git -C "$REPO"', 2), ('set -u', 1), ('MAIL YOUR VERDICT', 1), ('NEVER print a credential value', 1), ('no memory maintenance', 1),
    ("grep -q 'TIER 1'", 2), ("grep -q 'ROUND 1'", 2), ('GUARDED = [D + "services/api-gateway/src/routes/verification.ts",', 1), ('D + "package-lock.json"]', 1),
    ('GUARDED_SUFFIX = []', 1), ('for g in GUARDED_SUFFIX if x["filename"].endswith(g)', 1), ('D + "docs/openapi/",', 1),
    ('#1008', COUNT_1008),
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
