#!/usr/bin/env python3
"""gen_launcher_1004.py — derive launch_qa_secuura_ks932_1004.sh from tonight's #1001 TIER 1 launcher
(launchers/launch_qa_secuura_ks1165_1001.sh — the newest guard family: head on origin exit 6, compare exit 10/13, develop
judged BY CONTENT exit 18/19, head SHA named in brief+prompt exit 20, TTY exit 21) by ASSERTED substitutions: every anchor
must occur exactly as often as stated, or the generator refuses and writes nothing. Then a RESIDUAL GUARD (any token of the
source gate left anywhere, after stripping the one permitted template-name mention in the header, is a refusal), output
controls (every count measured against the composed text), the PY/PYJ-heredoc apostrophe parity, no git write verbs, no
control bytes, bash -n. Never overwrites an existing output without a .pre-* copy.
Usage: gen_launcher_1004.py <template launcher> <output launcher>
Exit: 0 written · 1 an anchor/control count disagreed · 2 a residual token survived · 3 bash -n failed"""
import datetime, hashlib, os, re, shutil, subprocess, sys

src_path, out_path = sys.argv[1], sys.argv[2]
s = open(src_path, encoding='utf-8').read()
def refuse(msg, code):
    print('REFUSING: ' + msg, file=sys.stderr); sys.exit(code)

HEAD = '6d077d3fe35cd5f3c09d394553d320e97b1abe32'
BASE = '5b4f38a48aeb40c2295895aaa5cd08e273aa7a08'   # develop at draft time = the PR base = the merge-base
BRANCH = 'refs/heads/feature/ks-932-ornith-timeout-bounds-dns'
STEM = '2026-09-16_secuura-1004-ks932-tier1'
OLD_STEM = '2026-09-16_secuura-1001-ks1165-tier1'
TEMPLATE_NAME = 'launch_qa_secuura_ks1165_1001.sh'

NEW_HEADER = '''#!/bin/bash
# launch_qa_secuura_ks932_1004.sh — cross-project QA agent, ONE TIER 1 ROUND 1 gate over Secuura/Blockchain PR #1004
# (KS-932, Seat A) @ 6d077d3fe35cd5f3c09d394553d320e97b1abe32 — ONE commit on develop 5b4f38a48, 2 files under
# packages/shared: ssrf-guard.ts +12 -3 (timeoutMs now bounds DNS: resolvePublicAddresses races a timer that returns
# reason blocked; DNS and the request share one budget via remainingMs) and a new 3-cell test file. TIER 1: a security
# surface — the SSRF guard every product webhook POST goes through, edited where each resolved address is classified.
#
# THE SHAPE, as read 22:56-23:11 AEST 2026-09-16 (git + the compare API agree): the head is a direct child of develop
# 5b4f38a48 (compare develop...head = merge_base 5b4f38a48, ahead 1, behind 0, files 2). The compare is asserted as
# merge_base + ahead + files (exit 10); `behind` is deliberately NOT asserted, so a develop that moves on does not trip
# this guard — the develop arm judges the move by CONTENT.
#
# The develop pin is judged by CONTENT, not bare: (a) ELEVEN files by blob at the CURRENT develop — ssrf-guard.ts (base
# 5a838e0d6; the PR's own efd880010 -> exit 19 LANDED), shared src/index.ts / vitest.config.ts / package.json /
# tsconfig.json, the three guard test files (ssrf-guard.test.ts, ks914-shipped-path, ks914-pinned-address), originate
# routes/webhooks.ts / jest.config.js, m365-integration src/index.ts — any blob nobody pinned -> exit 18 (the new test
# file is NOT judged: it is absent on develop, and ssrf-guard.ts already detects a landing); (b) if develop moved, the
# compare base...develop REFUSES (exit 18) only when the delta touches a GUARDED path — packages/shared/src/security/,
# shared src/index.ts, the shared config trio, the three guard test files, originate routes/webhooks.ts / jest.config.js /
# src/__tests__/helpers/, m365 src/index.ts, or the Dev lockfile — or cannot be judged; anything else (other shared tests
# such as #922's, api-gateway, auth) proceeds and the gate re-derives counts on the merged tree, dist rebuilt there.
# DEV_CONTENT_ALLOWED is empty: no open lane PR touches a guarded path (dependabot #649/#635/#575 touch
# packages/shared/package.json — if one lands, this launcher refuses and the brief is re-pinned deliberately).
#
# exit 21: the LAUNCH path refuses when stdin is not a TTY. This launcher execs an interactive agent; run it in a cockpit
# pane, never inside a Bash tool. `--check` still runs headless (it launches nothing).
#
# Adapted from launch_qa_secuura_ks1165_1001.sh by gen_launcher_1004.py (asserted substitutions + residual guard + output
# controls + bash -n): same guards and exit codes, re-pointed at #1004. Exit codes 2..21 (19 = LANDED).
# Written by the generator because it contains a legitimate directory change.
#
# Usage: launch_qa_secuura_ks932_1004.sh [--check]
# Exit: 0 launched (or guards passed under --check) · 2..21 a guard refused
'''

marker = 'set -u\n'
if s.count(marker) != 1: refuse('header marker set -u count %d' % s.count(marker), 1)
s = NEW_HEADER + s[s.index(marker):]

J = lambda *lines: '\n'.join(lines)
D_SH = 'packages/shared/'
NEW_JUDGED = J(
 '# file -> (develop-OK blobs {blob: label}, LANDED blobs {blob: label})',
 'JUDGED = {',
 '  D + "packages/shared/src/security/ssrf-guard.ts":                   ({"5a838e0d6440b371ab7ffa27ea1ec4ea878db150": "base"}, {"efd880010d5f31c5ea17d6229ef3f86f15321ea2": "#1004 own"}),',
 '  D + "packages/shared/src/index.ts":                                 ({"aeaf90dadff7ad1d426111756c5ec54ee2b34fb8": "base"}, {}),',
 '  D + "packages/shared/vitest.config.ts":                             ({"2a226c0068faa65538cda8d43d03bb9bee2944f1": "base"}, {}),',
 '  D + "packages/shared/package.json":                                 ({"3957692311221fbe87c4ab19447de8cec44aa19a": "base"}, {}),',
 '  D + "packages/shared/tsconfig.json":                                ({"1fd016cc28803cc8f36cc84db4628941a2af9c50": "base"}, {}),',
 '  D + "packages/shared/src/__tests__/ssrf-guard.test.ts":             ({"afb0c0d0809ea62c3a963be3272342fec5a2d04a": "base"}, {}),',
 '  D + "packages/shared/src/__tests__/ks914-shipped-path.test.ts":     ({"69706c1ef6b9fdeda03cece3051f94705fe17cf2": "base"}, {}),',
 '  D + "packages/shared/src/__tests__/ks914-pinned-address.test.ts":   ({"ffce480e4ddec290fe31c73578cb1ac9fa1adea3": "base"}, {}),',
 '  D + "services/originate/src/routes/webhooks.ts":                    ({"c88eb97db5a2466e9456506c2c1bf5094e3c5d4e": "base"}, {}),',
 '  D + "services/originate/jest.config.js":                            ({"735183662feea56d39f664eb6379cae1a2eec957": "base"}, {}),',
 '  D + "services/m365-integration/src/index.ts":                       ({"1f3a91d4f4f1e98db4d54c9be0e86c768b79cde4": "base"}, {}),',
 '}\n')
NEW_GUARDED = J(
 'GUARDED = [D + "packages/shared/src/security/",',
 '           D + "packages/shared/src/index.ts",',
 '           D + "packages/shared/vitest.config.ts",',
 '           D + "packages/shared/package.json",',
 '           D + "packages/shared/tsconfig.json",',
 '           D + "packages/shared/src/__tests__/ssrf-guard.test.ts",',
 '           D + "packages/shared/src/__tests__/ks914-shipped-path.test.ts",',
 '           D + "packages/shared/src/__tests__/ks914-pinned-address.test.ts",',
 '           D + "services/originate/src/routes/webhooks.ts",',
 '           D + "services/originate/jest.config.js",',
 '           D + "services/originate/src/__tests__/helpers/",',
 '           D + "services/m365-integration/src/index.ts",',
 '           D + "package-lock.json"]\n')
NEW_ALLOWED = J(
 '# STYLE NOTE (912r2 launcher, measured): bash scans quote/paren state THROUGH this heredoc because it sits inside a',
 '# command substitution — keep apostrophes and parentheses EVEN (this block uses none of the former), or the outer $( ) breaks.',
 '# CONTENT-JUDGED allowlist: a hit under a GUARDED path clears ONLY if the per-file blob sha in the compare is EXACTLY one',
 '# pinned here. EMPTY for this gate: at draft time 22:59 AEST no open lane PR touched a guarded path except dependabot',
 '# package.json bumps, which must NOT clear silently, so every guarded hit falls through to GUARDED and exit 18 — re-pin deliberately.',
 'DEV_CONTENT_ALLOWED = {',
 '}\n')

def block(start, end_marker):
    i = s.find(start)
    if i < 0 or s.count(start) != 1: refuse('block start %r count %d' % (start[:50], s.count(start)), 1)
    j = s.find(end_marker, i)
    if j < 0: refuse('block end %r not found' % end_marker[:40], 1)
    return s[i:j + len(end_marker)]

old_judged = block('# file -> (develop-OK blobs {blob: label}, LANDED blobs {blob: label})', '}\n')
old_guarded = block('GUARDED = [D + "services/api-gateway/src/middleware/",', '"package-lock.json"]\n')
old_allowed = block('# STYLE NOTE (912r2 launcher, measured)', 'DEV_CONTENT_ALLOWED = {\n')
old_allowed = old_allowed + s[s.index(old_allowed) + len(old_allowed): s.index('}\n', s.index(old_allowed) + len(old_allowed)) + 2]

subs = [
    (old_judged, NEW_JUDGED, 1),
    (old_guarded, NEW_GUARDED, 1),
    (old_allowed, NEW_ALLOWED, 1),
    ('QA1001_BRIEF', 'QA1004_BRIEF', 2),
    ('QA1001_PROMPT', 'QA1004_PROMPT', 2),
    ('QA1001_HEAD', 'QA1004_HEAD', 2),
    (OLD_STEM, STEM, 3),
    ('refs/heads/feature/ks-1165-ornith-v2-verify-csrf-exclusion', BRANCH, 1),
    ('3925d4c072b940eb91de462b7b92eabfe8889c75', HEAD, 1),
    ("MERGE_BASE='0b25f823f6660ac52b665f14055799ff0c3b616d'   # the merge-base of the head with develop = the PR base (the head is its direct child)",
     "MERGE_BASE='" + BASE + "'   # the merge-base of the head with develop = the PR base (the head is its direct child)", 1),
    ("DEVELOP_SHA='0b25f823f6660ac52b665f14055799ff0c3b616d'   # develop at draft time = the base (read 21:45:11 and 21:53:14 AEST)",
     "DEVELOP_SHA='" + BASE + "'   # develop at draft time = the base (read 22:56:13, 22:56:27 and 23:11:38 AEST)", 1),
    ('echo "REFUSING: #1001 — $HEAD_SHA is not at', 'echo "REFUSING: #1004 — $HEAD_SHA is not at', 1),
    ('# develop...#1001 = 0b25f823f ahead 1 files 2.', '# develop...#1004 = 5b4f38a48 ahead 1 files 2.', 1),
    ('''[ "$COMPARE" = "$MERGE_BASE ahead=1 files=2" ] || { echo "REFUSING: #1001 develop...head reads '$COMPARE', brief pins '$MERGE_BASE ahead=1 files=2'" >&2; exit 10; }''',
     '''[ "$COMPARE" = "$MERGE_BASE ahead=1 files=2" ] || { echo "REFUSING: #1004 develop...head reads '$COMPARE', brief pins '$MERGE_BASE ahead=1 files=2'" >&2; exit 10; }''', 1),
    ('# The develop pin, judged by CONTENT (see the header): ten files by blob at the CURRENT develop, then — if develop',
     '# The develop pin, judged by CONTENT (see the header): eleven files by blob at the CURRENT develop, then — if develop', 1),
    ('" — #1001 has landed; this brief is stale")', '" — #1004 has landed; this brief is stale")', 1),
    ('tail = "the gate merges the then-current develop onto 3925d4c07 in its own clone, runs the api-gateway suite on the MERGED tree beside the head tree, names the delta and re-derives every count (brief item 4)"',
     'tail = "the gate merges the then-current develop onto 6d077d3fe in its own clone, rebuilds the shared dist there, runs the packages/shared suite on the MERGED tree beside the head tree, names the delta and re-derives every count (brief item 6)"', 1),
    ('''— disjoint from the GUARDED list (api-gateway src/middleware/, src/index.ts, src/routes/proxy.ts, the api-gateway config trio, originate verificationV2.ts + middleware/auth.ts + src/index.ts, the lockfile); %s"''',
     '''— disjoint from the GUARDED list (packages/shared/src/security/, shared src/index.ts + config trio, the three guard test files, originate webhooks.ts + jest.config.js + __tests__/helpers/, m365 src/index.ts, the lockfile); %s"''', 1),
    ('echo "  head on origin: #1001 $HEAD_SHA at $BRANCH"', 'echo "  head on origin: #1004 $HEAD_SHA at $BRANCH"', 1),
    ('echo "  compare (GitHub API): develop...#1001 = $COMPARE"', 'echo "  compare (GitHub API): develop...#1004 = $COMPARE"', 1),
]
for old, new, n in subs:
    c = s.count(old)
    if c != n: refuse('anchor %r occurs %d times, expected %d' % (old[:70], c, n), 1)
    s = s.replace(old, new)

# RESIDUAL GUARD — tokens of the source gate; the header's one permitted template-name mention is stripped first.
permitted = 'Adapted from ' + TEMPLATE_NAME
if s.count(permitted) != 1: refuse('permitted template mention count %d' % s.count(permitted), 1)
body = s.replace(permitted, 'Adapted from <template>')
residual = ['1001', '1165', '999', 'QA1001', '3925d4c07', '0b25f823f', 'csrf', 'api-gateway', 'verificationV2', 'contentType', 'normalisePath',
            'proxy.ts', 'middleware/auth', 'v2-verify', 'a81722795', '1f16e2f89', '6f38c819e', '5b5b3e734', '1a7312a86', 'b99f45a4c',
            '5888e0b32', '22c110768', '841d8c6ad', 'dfa26c057', 'f08ee1a89', '21:45', '21:47', '21:53', 'brief item 4', 'ten files']
hits = []
for tok in residual:
    pat = r'(?<![0-9a-fA-F])' + re.escape(tok) + r'(?![0-9a-fA-F])' if tok.isdigit() else re.escape(tok)
    for m in re.finditer(pat, body):
        hits.append((tok, body.count('\n', 0, m.start()) + 1))
# api-gateway appears legitimately in the header's "anything else ... api-gateway, auth" sentence: allow exactly that one.
hits = [(t, l) for t, l in hits if not (t == 'api-gateway' and 'such as #922' in body.split('\n')[l - 2] + body.split('\n')[l - 1])]
if hits:
    for tok, line in hits: print('REFUSING: residual token %r at line %d' % (tok, line), file=sys.stderr)
    sys.exit(2)

# OUTPUT CONTROLS — every count measured against the composed text, never guessed.
controls = [
    ('HEAD_SHA="${QA1004_HEAD:-' + HEAD + '}"', 1), ("MERGE_BASE='" + BASE + "'", 1), ("DEVELOP_SHA='" + BASE + "'", 1),
    ("BRANCH='" + BRANCH + "'", 1), (STEM + '.md', 2), (STEM + '.prompt.txt', 1),
    ('exit 2;', 1), ('exit 3;', 1), ('exit 4;', 1), ('exit 5;', 1), ('exit 6', 1), ('exit 7;', 1), ('exit 8;', 1), ('exit 9;', 1),
    ('exit 10;', 1), ('exit 11;', 1), ('exit 12;', 1), ('exit 13;', 1), ('exit 14;', 1), ('exit 15;', 1), ('exit 16;', 2), ('exit 17;', 1),
    ('exit 18; }', 1), ('exit 18 ;;', 1), ('exit 19 ;;', 1), ('exit 20;', 1), ('exit 21;', 1),
    ('DEV_CONTENT_ALLOWED = {', 1), ('print("LANDED ', 1), ('print("GUARDED ', 2), ('print("UNJUDGEABLE ', 3), ('LANDED*)', 1), ('OK*)', 1),
    ('efd880010d5f31c5ea17d6229ef3f86f15321ea2', 1), ('5a838e0d6440b371ab7ffa27ea1ec4ea878db150', 1),
    ('aeaf90dadff7ad1d426111756c5ec54ee2b34fb8', 1), ('2a226c0068faa65538cda8d43d03bb9bee2944f1', 1), ('3957692311221fbe87c4ab19447de8cec44aa19a', 1),
    ('1fd016cc28803cc8f36cc84db4628941a2af9c50', 1), ('afb0c0d0809ea62c3a963be3272342fec5a2d04a', 1), ('69706c1ef6b9fdeda03cece3051f94705fe17cf2', 1),
    ('ffce480e4ddec290fe31c73578cb1ac9fa1adea3', 1), ('c88eb97db5a2466e9456506c2c1bf5094e3c5d4e', 1), ('735183662feea56d39f664eb6379cae1a2eec957', 1),
    ('1f3a91d4f4f1e98db4d54c9be0e86c768b79cde4', 1),
    ('ahead=1 files=2', 2), ('[ -t 0 ]', 1), ('exec claude --dangerously-skip-permissions --model opus', 1),
    ('git -C "$REPO"', 2), ('set -u', 1), ('MAIL YOUR VERDICT', 1), ('NEVER print a credential value', 1), ('no memory maintenance', 1),
    ("grep -q 'TIER 1'", 2), ("grep -q 'ROUND 1'", 2), ('D + "packages/shared/src/security/",', 1), ('D + "package-lock.json"]', 1),
    ('#1004', 9),   # MEASURED by enumeration (1st run left it unset -> refused at 9; 2nd run wrote to scratch and grep -n listed: header :2 :29; body :56 :62 :75 :93 :113 :181 :182)
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
