#!/usr/bin/env python3
"""gen_launcher_1010.py — derive launch_qa_secuura_ks1183_1010.sh from tonight's #1008 TIER 1 launcher (launchers/launch_qa_secuura_ks1087_1008.sh — same route,
same test file, same guard family: head on origin exit 6, compare exit 10/13, develop judged BY CONTENT exit 18/19, head SHA named exit 20, TTY exit 21)
by ASSERTED substitutions: every anchor must occur exactly as often as stated, or the generator refuses and writes nothing. Adds: exit 22 (the prompt
must require node_modules farmed PER ENTRY — the #1009 gate's R-6), exit 23 (the prompt must name the exact verdict subject, the coagent@ sender and
the wednesday-agent@ recipient), and a QA1010_CUR_DEV test override (so the develop arm's LANDED/GUARDED refusals can be proven with --check; a
launch with any override set refuses, exit 16). Then a RESIDUAL GUARD (any #1008-only token left, after stripping the one permitted template-name
mention), output controls, heredoc apostrophe/paren parity, no git write verbs, no control bytes, bash -n. Never overwrites without a .pre-* copy.
Usage: gen_launcher_1010.py <template launcher> <output launcher> [--enumerate]
Exit: 0 written · 1 an anchor/control count disagreed · 2 a residual token survived · 3 bash -n failed"""
import datetime, hashlib, os, re, shutil, subprocess, sys

src_path, out_path = sys.argv[1], sys.argv[2]
ENUMERATE = '--enumerate' in sys.argv[3:]
s = open(src_path, encoding='utf-8').read()
def refuse(msg, code):
    print('REFUSING: ' + msg, file=sys.stderr); sys.exit(code)

HEAD = 'c3213b04e3ad96068c367f7e0ba426822d32cda9'
BASE = 'f7c2f4acb28875e3665a61c8eaaad5c54bd3aa55'      # the merge-base = the PR parent (#1008's squash)
DEVELOP = 'd067725ff1c7f036dbf0f726b9bf12f4daefebe7'   # develop at draft time (#1009's squash; git ls-remote 03:47:16, branches API 03:55:15)
BRANCH = 'refs/heads/feature/ks-1183-workflow-approve-the-forward-to-originate-has-no-timeout-so'
STEM = '2026-09-17_secuura-1010-ks1183-tier1'
OLD_STEM = '2026-09-17_secuura-1008-ks1087-tier1'
TEMPLATE_NAME = 'launch_qa_secuura_ks1087_1008.sh'
COUNT_1010 = None if ENUMERATE else int(os.environ.get('COUNT_1010', '-1'))

NEW_HEADER = '''#!/bin/bash
# launch_qa_secuura_ks1183_1010.sh — cross-project QA agent, ONE TIER 1 ROUND 1 gate over Secuura/Blockchain PR #1010
# (KS-1183, Seat A successor) @ c3213b04e3ad96068c367f7e0ba426822d32cda9 — ONE commit on f7c2f4acb (#1008's squash), 2 files, both
# services/api-gateway: routes/verification.ts +42 -15 (the approve route's forward to originate gets proxyReq.setTimeout, default
# ORIGINATE_FORWARD_TIMEOUT_MS 15_000, optional deps.originateForwardTimeoutMs; at the bound 502 ORIGINATE_FORWARD_FAILED status 0, the
# pending document kept; proxyRes error/aborted/close settle 0) and the rebuilt ks1087 test (+241 -129). TIER 1: a new failure mode on an
# authenticated route mounted in every environment, deciding whether a pending document is DELETED.
#
# THE SHAPE, as read 03:47-03:55 AEST 2026-09-17 (git + the compare API agree): develop MOVED past the PR base before drafting —
# develop d067725ff (#1009's squash, 3 ks864 test files, file-disjoint) is NOT an ancestor of the head; compare develop...head =
# merge_base f7c2f4acb, diverged, ahead 1, behind 1, files 2. The compare is asserted as merge_base + ahead + files (exit 10); `behind`
# is deliberately NOT asserted — the develop arm judges every move by CONTENT, and the gate builds the merged tree itself.
#
# The develop pin is judged by CONTENT, not bare: (a) FIFTEEN files by blob at the CURRENT develop — verification.ts (base d0585dc34;
# the PR's own 04b3d980f -> exit 19 LANDED), the ks1087 test (base 7832724f3; the PR's own 4450587dc -> exit 19 LANDED), api-gateway
# src/index.ts (the mount, passes no override), src/middleware/auth.ts, src/services/redis.ts, src/services/enforcement.ts, package.json,
# vitest.config.ts, vitest.setup.ts, tsconfig.json, originate src/routes/documents.ts (the forward target), Dev eslint.config.mjs and the
# three nginx-gateway confs the 15 s default is measured against (nginx.conf 120 s, nginx-demo.conf 60 s, nginx-production.conf 30 s) —
# any blob nobody pinned -> exit 18; (b) if develop moved past d067725ff, the compare pinned...develop REFUSES (exit 18) when the delta
# touches a GUARDED path — those files, docs/openapi/, docker/nginx-gateway/, deployment/caddy/, any */nginx.conf, the Dev lockfile, issuer
# DocumentList.tsx, mcp-server api-client.ts — or cannot be judged; anything else proceeds and the gate re-derives the merged denominator.
# DEV_CONTENT_ALLOWED is empty: dependabot #649/#575 touch api-gateway package.json and the Dev lockfile — if one lands, re-pin deliberately.
#
# exit 21: the LAUNCH path refuses when stdin is not a TTY. This launcher execs an interactive agent; run it in a cockpit
# pane, never inside a Bash tool — and never run it without --check to "prove" this guard. `--check` runs headless (it launches nothing).
# exit 22: the prompt must require node_modules farmed PER ENTRY (the #1009 gate's R-6: a wholesale link can write through to the checkout's .vite).
# exit 23: the prompt must carry the exact verdict subject and name coagent@ as the sender and wednesday-agent@ as the recipient.
# QA1010_CUR_DEV (test override, --check only): stands in for origin develop so the LANDED / GUARDED refusals can be proven.
#
# Adapted from launch_qa_secuura_ks1087_1008.sh by gen_launcher_1010.py (asserted substitutions + residual guard + output
# controls + bash -n): same guards and exit codes, re-pointed at #1010, plus exits 22/23. Exit codes 2..23 (19 = LANDED).
# Written by the generator because it contains a legitimate directory change.
#
# Usage: launch_qa_secuura_ks1183_1010.sh [--check]
# Exit: 0 launched (or guards passed under --check) · 2..23 a guard refused
'''
marker = 'set -u\n'
if s.count(marker) != 1: refuse('header marker set -u count %d' % s.count(marker), 1)
s = NEW_HEADER + s[s.index(marker):]

J = lambda *lines: '\n'.join(lines)
NEW_JUDGED = J(
 '# file -> (develop-OK blobs {blob: label}, LANDED blobs {blob: label})',
 'JUDGED = {',
 '  D + "services/api-gateway/src/routes/verification.ts":           ({"d0585dc34ceb5e3580ade38633250a6ffeaebd69": "base"}, {"04b3d980f657b13717060e9547d92970100b2557": "#1010 own"}),',
 '  D + "services/api-gateway/src/__tests__/ks1087-workflow-approve-deletes-the-pending-document.test.ts": ({"7832724f3f5f97fa1260e3525dee8c68bda21ba4": "base"}, {"4450587dc2a0530a60c0bf5d5117b4831f754de3": "#1010 own"}),',
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
 '  D + "docker/nginx-gateway/nginx.conf":                           ({"3c5576adaba1e3073b715335ba68d6cbbadd739a": "base"}, {}),',
 '  D + "docker/nginx-gateway/nginx-demo.conf":                      ({"005a4bc279c0dc18830e0eb1d0c5bd3fcae37163": "base"}, {}),',
 '  D + "docker/nginx-gateway/nginx-production.conf":                ({"562891b4cb0d3257912f14e0c335478500ec0d12": "base"}, {}),',
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
 '           D + "docker/nginx-gateway/",',
 '           D + "deployment/caddy/",',
 '           D + "eslint.config.mjs",',
 '           D + "frontend/issuer/src/components/DocumentList.tsx",',
 '           D + "services/mcp-server/src/api-client.ts",',
 '           D + "package-lock.json"]',
 '# SUFFIX-GUARDED: any portal or service nginx.conf in front of the gateway.',
 'GUARDED_SUFFIX = ["/nginx.conf"]\n')
NEW_ALLOWED = J(
 '# STYLE NOTE (912r2 launcher, measured): bash scans quote/paren state THROUGH this heredoc because it sits inside a',
 '# command substitution — keep apostrophes and parentheses EVEN (this block uses none of the former), or the outer $( ) breaks.',
 '# CONTENT-JUDGED allowlist: a hit under a GUARDED path clears ONLY if the per-file blob sha in the compare is EXACTLY one',
 '# pinned here. EMPTY for this gate: at draft time 03:55 AEST no open lane PR touched a guarded path except dependabot',
 '# bumps of api-gateway package.json and the Dev lockfile, which must NOT clear silently, so every guarded hit falls through to GUARDED and exit 18 — re-pin deliberately.',
 'DEV_CONTENT_ALLOWED = {',
 '}\n')

def block(start, end_marker):
    if s.count(start) != 1: refuse('block start %r count %d' % (start[:50], s.count(start)), 1)
    i = s.find(start); j = s.find(end_marker, i)
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
grep -qF '[QA -> Wednesday] TIER 1 GATE #1010 (KS-1183) c3213b04e' "$PROMPT_FILE" && grep -qF 'coagent@agentmail.to' "$PROMPT_FILE" && grep -qF 'wednesday-agent@agentmail.to' "$PROMPT_FILE" \\
  || { echo "REFUSING: prompt does not carry the exact verdict subject, the coagent@ sender and the wednesday-agent@ recipient" >&2; exit 23; }
'''
subs = [
    (old_judged, NEW_JUDGED, 1),
    (old_guarded, NEW_GUARDED, 1),
    (old_allowed, NEW_ALLOWED, 1),
    ('QA1008_BRIEF', 'QA1010_BRIEF', 2),
    ('QA1008_PROMPT', 'QA1010_PROMPT', 2),
    ('QA1008_HEAD', 'QA1010_HEAD', 2),
    ('[ -z "${QA1010_BRIEF:-}${QA1010_PROMPT:-}${QA1010_HEAD:-}" ]', '[ -z "${QA1010_BRIEF:-}${QA1010_PROMPT:-}${QA1010_HEAD:-}${QA1010_CUR_DEV:-}" ]', 1),
    (OLD_STEM, STEM, 3),
    ('refs/heads/feature/ks-1087-ornith-workflow-approve-keeps-pending', BRANCH, 1),
    ('dd7086d5aa574285beffc515f9371a438621f25d', HEAD, 1),
    ("MERGE_BASE='93629700c3d219c1d8ca61d69150bb9b623fc1be'   # the merge-base of the head with develop = develop itself (develop is an ancestor of the head; behind 0)",
     "MERGE_BASE='" + BASE + "'   # the merge-base of the head with develop = the PR parent f7c2f4acb (#1008's squash); develop has moved past it (behind 1)", 1),
    ("DEVELOP_SHA='93629700c3d219c1d8ca61d69150bb9b623fc1be'   # develop at draft time = the PR base (git ls-remote 00:55:40, branches API 00:57:25 AEST)",
     "DEVELOP_SHA='" + DEVELOP + "'   # develop at draft time = #1009's squash, NOT an ancestor of the head (git ls-remote 03:47:16, branches API 03:55:15 AEST)", 1),
    ('echo "REFUSING: #1008 — $HEAD_SHA is not at', 'echo "REFUSING: #1010 — $HEAD_SHA is not at', 1),
    ('# develop...#1008 = 93629700c ahead 1 files 2 (behind 0; behind deliberately not asserted).', '# develop...#1010 = f7c2f4acb ahead 1 files 2 (behind 1 at draft time; behind deliberately not asserted).', 1),
    ('''[ "$COMPARE" = "$MERGE_BASE ahead=1 files=2" ] || { echo "REFUSING: #1008 develop...head reads '$COMPARE', brief pins '$MERGE_BASE ahead=1 files=2'" >&2; exit 10; }''',
     '''[ "$COMPARE" = "$MERGE_BASE ahead=1 files=2" ] || { echo "REFUSING: #1010 develop...head reads '$COMPARE', brief pins '$MERGE_BASE ahead=1 files=2'" >&2; exit 10; }''', 1),
    ('# The develop pin, judged by CONTENT (see the header): eleven files by blob at the CURRENT develop, then — if develop',
     '# The develop pin, judged by CONTENT (see the header): fifteen files by blob at the CURRENT develop, then — if develop', 1),
    ('CUR_DEV="$(git -C "$REPO" ls-remote origin refs/heads/develop | cut -f1)"',
     'CUR_DEV="${QA1010_CUR_DEV:-$(git -C "$REPO" ls-remote origin refs/heads/develop | cut -f1)}"', 1),
    ('" — #1008 has landed; this brief is stale")', '" — #1010 has landed; this brief is stale")', 1),
    ('print("OK " + state + " | origin develop still " + pinned + " (the PR base, an ancestor of the head: merged tree = head tree; git ls-remote)"); sys.exit(0)',
     'print("OK " + state + " | origin develop still " + pinned + " (NOT an ancestor of the head: the gate builds the merged tree head + " + pinned[:9] + " in its own clone; git ls-remote)"); sys.exit(0)', 1),
    ('tail = "the gate merges the then-current develop onto dd7086d5a in its own clone, rebuilds the shared dist there, runs the api-gateway suite on the MERGED tree beside the base and head trees, names the delta and re-derives every count, above all the api-gateway denominator (brief items 8 and 11)"',
     'tail = "the gate merges the then-current develop onto c3213b04e in its own clone, rebuilds the shared dist there, runs the api-gateway suite and the outcome probe on the MERGED tree beside the base and head trees, names the delta and re-derives every count, above all the api-gateway denominator (brief items 1, 8 and 9)"', 1),
    ('''— disjoint from the GUARDED list (api-gateway verification.ts + the ks1087 test + index.ts + auth.ts + redis.ts + enforcement.ts + package.json + vitest config/setup + tsconfig, originate routes/documents.ts, docs/openapi/, eslint.config.mjs, the two route consumers, the Dev lockfile); %s"''',
     '''— disjoint from the GUARDED list (api-gateway verification.ts + the ks1087 test + index.ts + auth.ts + redis.ts + enforcement.ts + package.json + vitest config/setup + tsconfig, originate routes/documents.ts, docs/openapi/, docker/nginx-gateway/, deployment/caddy/, any nginx.conf, eslint.config.mjs, the two route consumers, the Dev lockfile); %s"''', 1),
    ('echo "  head on origin: #1008 $HEAD_SHA at $BRANCH"', 'echo "  head on origin: #1010 $HEAD_SHA at $BRANCH"', 1),
    ('echo "  compare (GitHub API): develop...#1008 = $COMPARE"', 'echo "  compare (GitHub API): develop...#1010 = $COMPARE"', 1),
    (OLD_TAIL_GREPS, NEW_TAIL_GREPS, 1),
    ('  echo "  prompt forbids printing a credential value"\n', '  echo "  prompt forbids printing a credential value"\n  echo "  prompt requires node_modules farmed per ENTRY"\n  echo "  prompt carries the exact verdict subject, coagent@ sender, wednesday-agent@ recipient"\n  [ -n "${QA1010_CUR_DEV:-}" ] && echo "  (develop read from the QA1010_CUR_DEV test override, not ls-remote)"\n', 1),
]
for old, new, n in subs:
    c = s.count(old)
    if c != n: refuse('anchor %r occurs %d times, expected %d' % (old[:70], c, n), 1)
    s = s.replace(old, new)

permitted = 'Adapted from ' + TEMPLATE_NAME
if s.count(permitted) != 1: refuse('permitted template mention count %d' % s.count(permitted), 1)
body = s.replace(permitted, 'Adapted from <template>')
# '#1008' is legitimate ONLY as #1008's squash (the PR parent); every other #1008 form is residual
residual = ['#1008 has landed', '#1008 own', 'develop...#1008', 'REFUSING: #1008', 'origin: #1008', 're-pointed at #1008', 'launch_qa_secuura_ks1087_1008.sh by', 'KS-1087 item 1', 'ks-1087-ornith', 'dd7086d5', '93629700', 'de34b2de7', 'd0585dc34ceb5e3580ade38633250a6ffeaebd69": "#1008', 'Ornith', 'eleven files', '00:55:40', '00:57:25', '00:57 AEST', 'ancestor of the head: merged tree = head tree', 'QA1008']
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
        if '#1010' in l: print('#1010 at line %d: %s' % (i, l[:110]))
    print('ENUMERATED count #1010 = %d (scratch copy written to %s; nothing written to launchers/)' % (s.count('#1010'), out_path)); sys.exit(0)

controls = [
    ('HEAD_SHA="${QA1010_HEAD:-' + HEAD + '}"', 1), ("MERGE_BASE='" + BASE + "'", 1), ("DEVELOP_SHA='" + DEVELOP + "'", 1),
    ("BRANCH='" + BRANCH + "'", 1), (STEM + '.md', 2), (STEM + '.prompt.txt', 1),
    ('exit 2;', 1), ('exit 3;', 1), ('exit 4;', 1), ('exit 5;', 1), ('exit 6', 1), ('exit 7;', 1), ('exit 8;', 1), ('exit 9;', 1),
    ('exit 10;', 1), ('exit 11;', 1), ('exit 12;', 1), ('exit 13;', 1), ('exit 14;', 1), ('exit 15;', 1), ('exit 16;', 2), ('exit 17;', 1),
    ('exit 18; }', 1), ('exit 18 ;;', 1), ('exit 19 ;;', 1), ('exit 20;', 1), ('exit 21;', 1), ('exit 22;', 1), ('exit 23;', 1),
    ('DEV_CONTENT_ALLOWED = {', 1), ('print("LANDED ', 1), ('print("GUARDED ', 2), ('print("UNJUDGEABLE ', 3), ('LANDED*)', 1), ('OK*)', 1),
    ('d0585dc34ceb5e3580ade38633250a6ffeaebd69', 1), ('04b3d980f657b13717060e9547d92970100b2557', 1), ('7832724f3f5f97fa1260e3525dee8c68bda21ba4', 1), ('4450587dc2a0530a60c0bf5d5117b4831f754de3', 1),
    ('6f38c819e48162e3179aaf557085766f91beecc1', 1), ('20311010db0eb8ba097644ce105cf8df966ce456', 1), ('47659ee9c9f06acf9ac64e09b2dc207113ba92ea', 1),
    ('533cd309c56b8167ebe00b620744259b3cc186cc', 1), ('841d8c6adcd71e885c01e65c22da9418daff276a', 1), ('5888e0b320d934f6f434e0e5ca3c74a995cecc02', 1),
    ('22c1107683b8192df3bfd3e929aa94aff3dc7d45', 1), ('c981e6a92fdd2417fa35070eb979c5f1c77ffbcd', 1), ('c3a818ac8ac8de1b385540d15e3fbb23200cea30', 1),
    ('8c5374c6022eb0a3f449f41a570db61294aa63f1', 1), ('3c5576adaba1e3073b715335ba68d6cbbadd739a', 1), ('005a4bc279c0dc18830e0eb1d0c5bd3fcae37163', 1), ('562891b4cb0d3257912f14e0c335478500ec0d12', 1),
    ('ahead=1 files=2', 2), ('[ -t 0 ]', 1), ('exec claude --dangerously-skip-permissions --model opus', 1),
    ('git -C "$REPO"', 2), ('set -u', 1), ('MAIL YOUR VERDICT', 1), ('NEVER print a credential value', 1), ('no memory maintenance', 1), ('node_modules per ENTRY', 1),
    ("grep -q 'TIER 1'", 2), ("grep -q 'ROUND 1'", 2), ('GUARDED = [D + "services/api-gateway/src/routes/verification.ts",', 1), ('D + "package-lock.json"]', 1),
    ('GUARDED_SUFFIX = ["/nginx.conf"]', 1), ('for g in GUARDED_SUFFIX if x["filename"].endswith(g)', 1), ('D + "docs/openapi/",', 1), ('D + "docker/nginx-gateway/",', 1),
    ('${QA1010_CUR_DEV:-}', 2), ('QA1010_CUR_DEV:-$(git', 1),
    ('#1010', COUNT_1010),
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
