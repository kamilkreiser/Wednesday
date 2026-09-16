#!/usr/bin/env python3
"""gen_launcher_1011.py — derive launch_qa_secuura_ks871_1011.sh from the #1008 TIER 1 launcher (launchers/launch_qa_secuura_ks1087_1008.sh:
the SAME shape — develop is the head's parent, compare ahead 1 behind 0; guard family head on origin exit 6, compare exit 10/13, develop
judged BY CONTENT exit 18/19, head SHA named in brief+prompt exit 20, TTY exit 21) by ASSERTED substitutions: every anchor must occur exactly
as often as stated, or the generator refuses and writes nothing. Adds, in the #1010 set's form: exit 22 (the prompt must require node_modules
farmed PER ENTRY — the #1009 gate's R-6), exit 23 (the prompt must carry the exact verdict subject, the coagent@ sender and the wednesday-agent@
recipient), and a QA1011_CUR_DEV test override (develop read from it instead of ls-remote; refused on a launch, exit 16) so the develop
judgement's LANDED and GUARDED arms can be exercised as negative fixtures. Then a RESIDUAL GUARD (any token of the #1008 gate left anywhere,
after stripping the one permitted template-name mention, is a refusal), output controls (every count measured against the composed text;
'#1011' is ENUMERATED first with --enumerate, which writes only to the scratch path given), PY/PYJ-heredoc apostrophe/paren parity, no git
write verbs, no control bytes, bash -n. Never overwrites an existing output without a .pre-* copy.
Usage: gen_launcher_1011.py <template launcher> <output launcher> [--enumerate]
Exit: 0 written · 1 an anchor/control count disagreed · 2 a residual token survived · 3 bash -n failed"""
import datetime, hashlib, os, re, shutil, subprocess, sys

src_path, out_path = sys.argv[1], sys.argv[2]
ENUMERATE = '--enumerate' in sys.argv[3:]
s = open(src_path, encoding='utf-8').read()
def refuse(msg, code):
    print('REFUSING: ' + msg, file=sys.stderr); sys.exit(code)

HEAD = '0a1f8900c7094fbdaed1099799c029e351296b39'
BASE = 'd067725ff1c7f036dbf0f726b9bf12f4daefebe7'     # the merge-base = develop itself: develop is the head's PARENT
DEVELOP = 'd067725ff1c7f036dbf0f726b9bf12f4daefebe7'  # develop at draft time (git ls-remote 04:03:06 + 04:13:13, branches API 04:07:56)
BRANCH = 'refs/heads/feature/ks-871-ornith-audit-path-captured-at-entry'
STEM = '2026-09-17_secuura-1011-ks871-tier1'
OLD_STEM = '2026-09-17_secuura-1008-ks1087-tier1'
TEMPLATE_NAME = 'launch_qa_secuura_ks1087_1008.sh'
COUNT_1011 = None if ENUMERATE else int(os.environ.get('COUNT_1011', '-1'))  # MEASURED by --enumerate first; passed in, never guessed

NEW_HEADER = '''#!/bin/bash
# launch_qa_secuura_ks871_1011.sh — cross-project QA agent, ONE TIER 1 ROUND 1 gate over Secuura/Blockchain PR #1011
# (KS-871, Seat A successor item A12) @ 0a1f8900c7094fbdaed1099799c029e351296b39 — ONE commit on develop d067725ff, 3 files, all
# services/api-gateway: src/middleware/audit.ts +11 -2 (auditPath = req.originalUrl captured at entry and written as details.path;
# deriveAction reads req.originalUrl) and two new ks871 test files. TIER 1 (Wednesday's ruling): the audit middleware writes the audit
# trail for EVERY audited request, and the audit trail is a security control.
#
# THE SHAPE, as read 04:03-04:13 AEST 2026-09-17 (git + the compare API agree): develop d067725ff is the head's PARENT (merge-base =
# develop, behind 0), so the merged tree IS the head tree. compare develop...head = merge_base d067725ff, status ahead, ahead 1, behind 0,
# files 3. The compare is asserted as merge_base + ahead + files (exit 10); `behind` is deliberately NOT asserted, so a develop that
# moves on does not trip this guard — the develop arm judges the move by CONTENT.
#
# The develop pin is judged by CONTENT, not bare: (a) TWELVE files by blob at the CURRENT develop — audit.ts (base a7be8626f; the PR's
# own f5a83ba2c -> exit 19 LANDED) and eleven more files the gate's census and predictions stand on: api-gateway src/index.ts (the /api/v1
# strip and the audit mount), src/routes/proxy.ts (the erasure door), src/middleware/normalisePath.ts, src/routes/versioning.ts (the
# production 307), src/db.ts (the mocked sink), src/middleware/auth.ts, package.json, vitest.config.ts, vitest.setup.ts, tsconfig.json
# (the exclude the including tsc overrides) and Dev eslint.config.mjs — any blob nobody pinned -> exit 18 (the two new ks871 tests are
# NOT judged by blob: absent on develop, and audit.ts already detects a landing); (b) if develop moved past d067725ff, the compare
# pinned...develop REFUSES (exit 18) only when the delta touches a GUARDED path — those twelve files, the two ks871 tests, the Dev
# lockfile — or cannot be judged; anything else (the file-disjoint sibling lane PRs landing, #1010 among them) proceeds and the gate
# merges develop and re-runs the census on the merged tree.
# DEV_CONTENT_ALLOWED is empty: dependabot #649/#575 touch api-gateway package.json and the Dev lockfile — if one lands, this
# launcher refuses and the brief is re-pinned deliberately.
#
# exit 21: the LAUNCH path refuses when stdin is not a TTY. This launcher execs an interactive agent; run it in a cockpit
# pane, never inside a Bash tool. `--check` still runs headless (it launches nothing).
# exit 22: the prompt must require node_modules farmed PER ENTRY (the #1009 gate's R-6: a wholesale link can write through to the checkout's .vite).
# exit 23: the prompt must carry the exact verdict subject and name coagent@ as the sender and wednesday-agent@ as the recipient.
# QA1011_CUR_DEV: a --check-only test override for the develop SHA (negative fixtures); a launch with it set refuses (exit 16).
#
# Adapted from launch_qa_secuura_ks1087_1008.sh by gen_launcher_1011.py (asserted substitutions + residual guard + output
# controls + bash -n): same guards and exit codes, re-pointed at #1011, plus exits 22/23. Exit codes 2..23 (19 = LANDED).
# Written by the generator because it contains a legitimate directory change.
#
# Usage: launch_qa_secuura_ks871_1011.sh [--check]
# Exit: 0 launched (or guards passed under --check) · 2..23 a guard refused
'''
marker = 'set -u\n'
if s.count(marker) != 1: refuse('header marker set -u count %d' % s.count(marker), 1)
s = NEW_HEADER + s[s.index(marker):]

J = lambda *lines: '\n'.join(lines)
NEW_JUDGED = J(
 '# file -> (develop-OK blobs {blob: label}, LANDED blobs {blob: label})',
 'JUDGED = {',
 '  D + "services/api-gateway/src/middleware/audit.ts":              ({"a7be8626ff1d79a0887fb8d31c44286472157644": "base"}, {"f5a83ba2cde6c64eb5540976c55867d637e8f6eb": "#1011 own"}),',
 '  D + "services/api-gateway/src/index.ts":                         ({"6f38c819e48162e3179aaf557085766f91beecc1": "base"}, {}),',
 '  D + "services/api-gateway/src/routes/proxy.ts":                  ({"b99f45a4c9c89088a7809de5f26c4f56fc94819c": "base"}, {}),',
 '  D + "services/api-gateway/src/middleware/normalisePath.ts":      ({"1a7312a8675ffdfe263060bb5d60aa837111431a": "base"}, {}),',
 '  D + "services/api-gateway/src/routes/versioning.ts":             ({"697bbb48bd93775572c7bde41c303eb4775ee920": "base"}, {}),',
 '  D + "services/api-gateway/src/db.ts":                            ({"9144c532bca9911da6cedd569e575c5aa6bc6c52": "base"}, {}),',
 '  D + "services/api-gateway/src/middleware/auth.ts":               ({"20311010db0eb8ba097644ce105cf8df966ce456": "base"}, {}),',
 '  D + "services/api-gateway/package.json":                         ({"841d8c6adcd71e885c01e65c22da9418daff276a": "base"}, {}),',
 '  D + "services/api-gateway/vitest.config.ts":                     ({"5888e0b320d934f6f434e0e5ca3c74a995cecc02": "base"}, {}),',
 '  D + "services/api-gateway/vitest.setup.ts":                      ({"22c1107683b8192df3bfd3e929aa94aff3dc7d45": "base"}, {}),',
 '  D + "services/api-gateway/tsconfig.json":                        ({"c981e6a92fdd2417fa35070eb979c5f1c77ffbcd": "base"}, {}),',
 '  D + "eslint.config.mjs":                                          ({"8c5374c6022eb0a3f449f41a570db61294aa63f1": "base"}, {}),',
 '}\n')
NEW_GUARDED = J(
 'GUARDED = [D + "services/api-gateway/src/middleware/audit.ts",',
 '           D + "services/api-gateway/src/__tests__/ks871-audit-path-captured-at-entry.test.ts",',
 '           D + "services/api-gateway/src/__tests__/ks871-the-audit-log-records-req-path.test.ts",',
 '           D + "services/api-gateway/src/index.ts",',
 '           D + "services/api-gateway/src/routes/proxy.ts",',
 '           D + "services/api-gateway/src/middleware/normalisePath.ts",',
 '           D + "services/api-gateway/src/routes/versioning.ts",',
 '           D + "services/api-gateway/src/db.ts",',
 '           D + "services/api-gateway/src/middleware/auth.ts",',
 '           D + "services/api-gateway/package.json",',
 '           D + "services/api-gateway/vitest.config.ts",',
 '           D + "services/api-gateway/vitest.setup.ts",',
 '           D + "services/api-gateway/tsconfig.json",',
 '           D + "eslint.config.mjs",',
 '           D + "package-lock.json"]',
 '# SUFFIX-GUARDED: none for this gate — every guarded path above is exact.',
 'GUARDED_SUFFIX = []\n')
NEW_ALLOWED = J(
 '# STYLE NOTE (912r2 launcher, measured): bash scans quote/paren state THROUGH this heredoc because it sits inside a',
 '# command substitution — keep apostrophes and parentheses EVEN (this block uses none of the former), or the outer $( ) breaks.',
 '# CONTENT-JUDGED allowlist: a hit under a GUARDED path clears ONLY if the per-file blob sha in the compare is EXACTLY one',
 '# pinned here. EMPTY for this gate: at draft time 04:12 AEST no open lane PR touched a guarded path except dependabot',
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
old_guarded = block('GUARDED = [D + "services/api-gateway/src/routes/verification.ts",', 'GUARDED_SUFFIX = []\n')
old_allowed = block('# STYLE NOTE (912r2 launcher, measured)', 'DEV_CONTENT_ALLOWED = {\n')
old_allowed = old_allowed + s[s.index(old_allowed) + len(old_allowed): s.index('}\n', s.index(old_allowed) + len(old_allowed)) + 2]

OLD_TAIL_GREPS = '''grep -qi 'NEVER print a credential value' "$PROMPT_FILE" \\
  || { echo "REFUSING: prompt does not forbid printing a credential value" >&2; exit 17; }
'''
NEW_TAIL_GREPS = OLD_TAIL_GREPS + '''grep -qi 'node_modules per ENTRY' "$PROMPT_FILE" \\
  || { echo "REFUSING: prompt does not require node_modules farmed per ENTRY (a wholesale link can write through to the checkout .vite cache)" >&2; exit 22; }
grep -qF '[QA -> Wednesday] TIER 1 GATE #1011 (KS-871) 0a1f8900c' "$PROMPT_FILE" && grep -qF 'coagent@agentmail.to' "$PROMPT_FILE" && grep -qF 'wednesday-agent@agentmail.to' "$PROMPT_FILE" \\
  || { echo "REFUSING: prompt does not carry the exact verdict subject, the coagent@ sender and the wednesday-agent@ recipient" >&2; exit 23; }
'''
subs = [
    (old_judged, NEW_JUDGED, 1),
    (old_guarded, NEW_GUARDED, 1),
    (old_allowed, NEW_ALLOWED, 1),
    ('QA1008_BRIEF', 'QA1011_BRIEF', 2),
    ('QA1008_PROMPT', 'QA1011_PROMPT', 2),
    ('QA1008_HEAD', 'QA1011_HEAD', 2),
    ('[ -z "${QA1011_BRIEF:-}${QA1011_PROMPT:-}${QA1011_HEAD:-}" ]', '[ -z "${QA1011_BRIEF:-}${QA1011_PROMPT:-}${QA1011_HEAD:-}${QA1011_CUR_DEV:-}" ]', 1),
    (OLD_STEM, STEM, 3),
    ('refs/heads/feature/ks-1087-ornith-workflow-approve-keeps-pending', BRANCH, 1),
    ('dd7086d5aa574285beffc515f9371a438621f25d', HEAD, 1),
    ("MERGE_BASE='93629700c3d219c1d8ca61d69150bb9b623fc1be'   # the merge-base of the head with develop = develop itself (develop is an ancestor of the head; behind 0)",
     "MERGE_BASE='" + BASE + "'   # the merge-base of the head with develop = develop itself (develop is the head's parent; behind 0)", 1),
    ("DEVELOP_SHA='93629700c3d219c1d8ca61d69150bb9b623fc1be'   # develop at draft time = the PR base (git ls-remote 00:55:40, branches API 00:57:25 AEST)",
     "DEVELOP_SHA='" + DEVELOP + "'   # develop at draft time = the PR base (git ls-remote 04:03:06 and 04:13:13, branches API 04:07:56 AEST)", 1),
    ('echo "REFUSING: #1008 — $HEAD_SHA is not at', 'echo "REFUSING: #1011 — $HEAD_SHA is not at', 1),
    ('# develop...#1008 = 93629700c ahead 1 files 2 (behind 0; behind deliberately not asserted).', '# develop...#1011 = d067725ff ahead 1 files 3 (behind 0; behind deliberately not asserted).', 1),
    ('''[ "$COMPARE" = "$MERGE_BASE ahead=1 files=2" ] || { echo "REFUSING: #1008 develop...head reads '$COMPARE', brief pins '$MERGE_BASE ahead=1 files=2'" >&2; exit 10; }''',
     '''[ "$COMPARE" = "$MERGE_BASE ahead=1 files=3" ] || { echo "REFUSING: #1011 develop...head reads '$COMPARE', brief pins '$MERGE_BASE ahead=1 files=3'" >&2; exit 10; }''', 1),
    ('# The develop pin, judged by CONTENT (see the header): eleven files by blob at the CURRENT develop, then — if develop',
     '# The develop pin, judged by CONTENT (see the header): twelve files by blob at the CURRENT develop, then — if develop', 1),
    ('CUR_DEV="$(git -C "$REPO" ls-remote origin refs/heads/develop | cut -f1)"',
     'CUR_DEV="${QA1011_CUR_DEV:-$(git -C "$REPO" ls-remote origin refs/heads/develop | cut -f1)}"', 1),
    ('" — #1008 has landed; this brief is stale")', '" — #1011 has landed; this brief is stale")', 1),
    ('print("OK " + state + " | origin develop still " + pinned + " (the PR base, an ancestor of the head: merged tree = head tree; git ls-remote)"); sys.exit(0)',
     'print("OK " + state + " | origin develop still " + pinned + " (the PR base, the head parent: merged tree = head tree; git ls-remote)"); sys.exit(0)', 1),
    ('tail = "the gate merges the then-current develop onto dd7086d5a in its own clone, rebuilds the shared dist there, runs the api-gateway suite on the MERGED tree beside the base and head trees, names the delta and re-derives every count, above all the api-gateway denominator (brief items 8 and 11)"',
     'tail = "the gate merges the then-current develop onto 0a1f8900c in its own clone, rebuilds the shared dist there, runs the api-gateway suite and the audit census on the MERGED tree beside the base and head trees, names the delta and re-derives every count, above all the api-gateway denominator (brief items 1, 8 and 11)"', 1),
    ('''— disjoint from the GUARDED list (api-gateway verification.ts + the ks1087 test + index.ts + auth.ts + redis.ts + enforcement.ts + package.json + vitest config/setup + tsconfig, originate routes/documents.ts, docs/openapi/, eslint.config.mjs, the two route consumers, the Dev lockfile); %s"''',
     '''— disjoint from the GUARDED list (api-gateway audit.ts + the two ks871 tests + index.ts + proxy.ts + normalisePath.ts + versioning.ts + db.ts + auth.ts + package.json + vitest config/setup + tsconfig, eslint.config.mjs, the Dev lockfile); %s"''', 1),
    ('echo "  head on origin: #1008 $HEAD_SHA at $BRANCH"', 'echo "  head on origin: #1011 $HEAD_SHA at $BRANCH"', 1),
    ('echo "  compare (GitHub API): develop...#1008 = $COMPARE"', 'echo "  compare (GitHub API): develop...#1011 = $COMPARE"', 1),
    (OLD_TAIL_GREPS, NEW_TAIL_GREPS, 1),
    ('  echo "  prompt forbids printing a credential value"\n', '  echo "  prompt forbids printing a credential value"\n  echo "  prompt requires node_modules farmed per ENTRY"\n  echo "  prompt carries the exact verdict subject, coagent@ sender, wednesday-agent@ recipient"\n  [ -n "${QA1011_CUR_DEV:-}" ] && echo "  (develop read from the QA1011_CUR_DEV test override, not ls-remote)"\n', 1),
]
for old, new, n in subs:
    c = s.count(old)
    if c != n: refuse('anchor %r occurs %d times, expected %d' % (old[:70], c, n), 1)
    s = s.replace(old, new)

permitted = 'Adapted from ' + TEMPLATE_NAME
if s.count(permitted) != 1: refuse('permitted template mention count %d' % s.count(permitted), 1)
body = s.replace(permitted, 'Adapted from <template>')
residual = ['1008', '1087', 'KS-1087', 'ks1087', 'dd7086d5', '93629700', 'de34b2de7', 'd0585dc34', 'verification.ts', 'redis.ts', 'enforcement.ts',
            'originate', 'documents.ts', 'DocumentList', 'api-client', 'docs/openapi', 'eleven files', '00:55:40', '00:57:25', '00:57 AEST',
            'ahead=1 files=2', 'files 2', 'ancestor of the head', 'workflow', 'pending document', '502', '47659ee9c', '533cd309c', 'c3a818ac8', 'Ornith']
hits = []
for tok in residual:
    pat = r'(?<![0-9a-fA-F])' + re.escape(tok) + r'(?![0-9a-fA-F])' if tok.isdigit() else re.escape(tok)
    for m in re.finditer(pat, body):
        hits.append((tok, body.count('\n', 0, m.start()) + 1))
lines = body.split('\n')
# 'ornith' is legitimate ONLY inside the #1011 branch name (feature/ks-871-ornith-audit-path-captured-at-entry), lower-case; 'Ornith' is residual.
if hits:
    for tok, line in hits: print('REFUSING: residual token %r at line %d: %s' % (tok, line, lines[line - 1][:120]), file=sys.stderr)
    sys.exit(2)

if ENUMERATE:
    open(out_path, 'w', encoding='utf-8').write(s)
    for i, l in enumerate(s.split('\n'), 1):
        if '#1011' in l: print('#1011 at line %d: %s' % (i, l[:110]))
    print('ENUMERATED count #1011 = %d (scratch copy written to %s; nothing written to launchers/)' % (s.count('#1011'), out_path)); sys.exit(0)

controls = [
    ('HEAD_SHA="${QA1011_HEAD:-' + HEAD + '}"', 1), ("MERGE_BASE='" + BASE + "'", 1), ("DEVELOP_SHA='" + DEVELOP + "'", 1),
    ("BRANCH='" + BRANCH + "'", 1), (STEM + '.md', 2), (STEM + '.prompt.txt', 1),
    ('exit 2;', 1), ('exit 3;', 1), ('exit 4;', 1), ('exit 5;', 1), ('exit 6', 1), ('exit 7;', 1), ('exit 8;', 1), ('exit 9;', 1),
    ('exit 10;', 1), ('exit 11;', 1), ('exit 12;', 1), ('exit 13;', 1), ('exit 14;', 1), ('exit 15;', 1), ('exit 16;', 2), ('exit 17;', 1),
    ('exit 18; }', 1), ('exit 18 ;;', 1), ('exit 19 ;;', 1), ('exit 20;', 1), ('exit 21;', 1), ('exit 22;', 1), ('exit 23;', 1),
    ('DEV_CONTENT_ALLOWED = {', 1), ('print("LANDED ', 1), ('print("GUARDED ', 2), ('print("UNJUDGEABLE ', 3), ('LANDED*)', 1), ('OK*)', 1),
    ('a7be8626ff1d79a0887fb8d31c44286472157644', 1), ('f5a83ba2cde6c64eb5540976c55867d637e8f6eb', 1), ('6f38c819e48162e3179aaf557085766f91beecc1', 1),
    ('b99f45a4c9c89088a7809de5f26c4f56fc94819c', 1), ('1a7312a8675ffdfe263060bb5d60aa837111431a', 1), ('697bbb48bd93775572c7bde41c303eb4775ee920', 1),
    ('9144c532bca9911da6cedd569e575c5aa6bc6c52', 1), ('20311010db0eb8ba097644ce105cf8df966ce456', 1), ('841d8c6adcd71e885c01e65c22da9418daff276a', 1),
    ('5888e0b320d934f6f434e0e5ca3c74a995cecc02', 1), ('22c1107683b8192df3bfd3e929aa94aff3dc7d45', 1), ('c981e6a92fdd2417fa35070eb979c5f1c77ffbcd', 1),
    ('8c5374c6022eb0a3f449f41a570db61294aa63f1', 1),
    ('ahead=1 files=3', 2), ('[ -t 0 ]', 1), ('exec claude --dangerously-skip-permissions --model opus', 1),
    ('git -C "$REPO"', 2), ('set -u', 1), ('MAIL YOUR VERDICT', 1), ('NEVER print a credential value', 1), ('no memory maintenance', 1),
    ("grep -q 'TIER 1'", 2), ("grep -q 'ROUND 1'", 2), ('GUARDED = [D + "services/api-gateway/src/middleware/audit.ts",', 1), ('D + "package-lock.json"]', 1),
    ('GUARDED_SUFFIX = []', 1), ('for g in GUARDED_SUFFIX if x["filename"].endswith(g)', 1), ('QA1011_CUR_DEV', 5), ("grep -qi 'node_modules per ENTRY'", 1),
    ("grep -qF '[QA -> Wednesday] TIER 1 GATE #1011 (KS-871) 0a1f8900c'", 1),
    ('#1011', COUNT_1011),
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
