#!/usr/bin/env python3
"""gen_launcher_1001.py — derive launch_qa_secuura_ks1165_1001.sh from the #873 TIER 1 launcher
(launchers/launch_qa_secuura_873_ks931.sh — the newest guard family: head on origin exit 6, compare exit 10/13, develop
judged BY CONTENT exit 18/19, head SHA named in brief+prompt exit 20, TTY exit 21) by ASSERTED substitutions: every anchor
must occur exactly as often as stated, or the generator refuses and writes nothing. Then a RESIDUAL GUARD (any token of the
source gate left anywhere, after stripping the one permitted template-name mention in the header, is a refusal), output
controls (every count measured against the composed text), the PYJ-heredoc apostrophe parity, no git write verbs, no
control bytes, bash -n. Never overwrites an existing output without a .pre-* copy.
Usage: gen_launcher_1001.py <template launcher> <output launcher>
Exit: 0 written · 1 an anchor/control count disagreed · 2 a residual token survived · 3 bash -n failed"""
import datetime, hashlib, os, re, shutil, subprocess, sys

src_path, out_path = sys.argv[1], sys.argv[2]
s = open(src_path, encoding='utf-8').read()
def refuse(msg, code):
    print('REFUSING: ' + msg, file=sys.stderr); sys.exit(code)

HEAD = '3925d4c072b940eb91de462b7b92eabfe8889c75'
BASE = '0b25f823f6660ac52b665f14055799ff0c3b616d'   # develop at draft time = the PR base = the merge-base
BRANCH = 'refs/heads/feature/ks-1165-ornith-v2-verify-csrf-exclusion'
STEM = '2026-09-16_secuura-1001-ks1165-tier1'
TEMPLATE_NAME = 'launch_qa_secuura_873_ks931.sh'

NEW_HEADER = '''#!/bin/bash
# launch_qa_secuura_ks1165_1001.sh — cross-project QA agent, ONE TIER 1 ROUND 1 gate over Secuura/Blockchain PR #1001
# (KS-1165, Seat A) @ 3925d4c072b940eb91de462b7b92eabfe8889c75 — ONE commit on develop 0b25f823f, 2 files under
# services/api-gateway: csrf.ts +2 (the entry /api/v2/verification/verify added to excludedPaths beside the v1 entry,
# matched by req.path.startsWith) and a new 7-cell test file. TIER 1: a security surface — a CSRF exclusion removes a
# guard for cookie-bearing callers on a path PREFIX (403 CSRF_TOKEN_MISSING -> passes through). No rendered surface.
#
# THE SHAPE, as read 21:45-21:53 AEST 2026-09-16 (git + the compare API agree): the head is a direct child of develop
# 0b25f823f (compare develop...head = merge_base 0b25f823f, ahead 1, behind 0, files 2). The compare is asserted as
# merge_base + ahead + files (exit 10); `behind` is deliberately NOT asserted, so a develop that moves on does not trip
# this guard — the develop arm judges the move by CONTENT.
#
# The develop pin is judged by CONTENT, not bare: (a) TEN files by blob at the CURRENT develop — csrf.ts (base 1f16e2f89;
# the PR's own a81722795 -> exit 19 LANDED), api-gateway index.ts / contentType.ts / normalisePath.ts / proxy.ts /
# vitest.config.ts / vitest.setup.ts / package.json, originate verificationV2.ts / middleware/auth.ts — any blob nobody
# pinned -> exit 18 (the new test file is NOT judged: it is absent on develop, and csrf.ts already detects a landing);
# (b) if develop moved, the compare base...develop REFUSES (exit 18) only when the delta touches a GUARDED path —
# api-gateway src/middleware/, src/index.ts, src/routes/proxy.ts, the api-gateway config trio, originate
# verificationV2.ts / middleware/auth.ts / src/index.ts, or the Dev lockfile — or cannot be judged; anything else
# (#999 routes/verification.ts + api-gateway __tests__/, #1000 an auth test) proceeds and the gate re-derives counts on
# the merged tree. DEV_CONTENT_ALLOWED is empty: no live lane PR touches a guarded path.
#
# exit 21: the LAUNCH path refuses when stdin is not a TTY. This launcher execs an interactive agent; run it in a cockpit
# pane, never inside a Bash tool. `--check` still runs headless (it launches nothing).
#
# Adapted from launch_qa_secuura_873_ks931.sh by gen_launcher_1001.py (asserted substitutions + residual guard + output
# controls + bash -n): same guards and exit codes, re-pointed at #1001. Exit codes 2..21 (19 = LANDED).
# Written by the generator because it contains a legitimate directory change.
#
# Usage: launch_qa_secuura_ks1165_1001.sh [--check]
# Exit: 0 launched (or guards passed under --check) · 2..21 a guard refused
'''

marker = 'set -u\n'
if s.count(marker) != 1: refuse('header marker set -u count %d' % s.count(marker), 1)
s = NEW_HEADER + s[s.index(marker):]

J = lambda *lines: '\n'.join(lines)
NEW_JUDGED = J(
 '# file -> (develop-OK blobs {blob: label}, LANDED blobs {blob: label})',
 'JUDGED = {',
 '  D + "services/api-gateway/src/middleware/csrf.ts":            ({"1f16e2f899af46b8afc5e3872261e079c2cf88f5": "base"}, {"a81722795302100ce8d7db4ea788be0de3f89942": "#1001 own"}),',
 '  D + "services/api-gateway/src/index.ts":                      ({"6f38c819e48162e3179aaf557085766f91beecc1": "base"}, {}),',
 '  D + "services/api-gateway/src/middleware/contentType.ts":     ({"5b5b3e7342d04451ea8a7dff0823fc5763122059": "base"}, {}),',
 '  D + "services/api-gateway/src/middleware/normalisePath.ts":   ({"1a7312a8675ffdfe263060bb5d60aa837111431a": "base"}, {}),',
 '  D + "services/api-gateway/src/routes/proxy.ts":               ({"b99f45a4c9c89088a7809de5f26c4f56fc94819c": "base"}, {}),',
 '  D + "services/api-gateway/vitest.config.ts":                  ({"5888e0b320d934f6f434e0e5ca3c74a995cecc02": "base"}, {}),',
 '  D + "services/api-gateway/vitest.setup.ts":                   ({"22c1107683b8192df3bfd3e929aa94aff3dc7d45": "base"}, {}),',
 '  D + "services/api-gateway/package.json":                      ({"841d8c6adcd71e885c01e65c22da9418daff276a": "base"}, {}),',
 '  D + "services/originate/src/routes/verificationV2.ts":         ({"dfa26c0572d6a3888d7b07bc6172b4b7ef4852e0": "base"}, {}),',
 '  D + "services/originate/src/middleware/auth.ts":              ({"f08ee1a895bc878bc2656f649833706f665686e7": "base"}, {}),',
 '}\n')
NEW_GUARDED = J(
 'GUARDED = [D + "services/api-gateway/src/middleware/",',
 '           D + "services/api-gateway/src/index.ts",',
 '           D + "services/api-gateway/src/routes/proxy.ts",',
 '           D + "services/api-gateway/vitest.config.ts",',
 '           D + "services/api-gateway/vitest.setup.ts",',
 '           D + "services/api-gateway/package.json",',
 '           D + "services/originate/src/routes/verificationV2.ts",',
 '           D + "services/originate/src/middleware/auth.ts",',
 '           D + "services/originate/src/index.ts",',
 '           D + "package-lock.json"]\n')
NEW_ALLOWED = J(
 '# STYLE NOTE (912r2 launcher, measured): bash scans quote/paren state THROUGH this heredoc because it sits inside a',
 '# command substitution — keep apostrophes and parentheses EVEN (this block uses none of the former), or the outer $( ) breaks.',
 '# CONTENT-JUDGED allowlist: a hit under a GUARDED path clears ONLY if the per-file blob sha in the compare is EXACTLY one',
 '# pinned here. EMPTY for this gate: at draft time 21:47 AEST no open lane PR touched a guarded path, so every guarded hit',
 '# falls through to GUARDED and exit 18 — re-pin deliberately.',
 'DEV_CONTENT_ALLOWED = {',
 '}\n')

def block(start, end_marker):
    i = s.find(start)
    if i < 0 or s.count(start) != 1: refuse('block start %r count %d' % (start[:50], s.count(start)), 1)
    j = s.find(end_marker, i)
    if j < 0: refuse('block end %r not found' % end_marker[:40], 1)
    return s[i:j + len(end_marker)]

old_judged = block('# file -> (develop-OK blobs {blob: label}, LANDED blobs {blob: label})', '}\n')
old_guarded = block('GUARDED = [D + "packages/shared/",', '"package-lock.json"]\n')
old_allowed = block('# STYLE NOTE (912r2 launcher, measured)', 'DEV_CONTENT_ALLOWED = {\n')
old_allowed = old_allowed + s[s.index(old_allowed) + len(old_allowed): s.index('}\n', s.index(old_allowed) + len(old_allowed)) + 2]

subs = [
    (old_judged, NEW_JUDGED, 1),
    (old_guarded, NEW_GUARDED, 1),
    (old_allowed, NEW_ALLOWED, 1),
    ('QA873_BRIEF', 'QA1001_BRIEF', 2),
    ('QA873_PROMPT', 'QA1001_PROMPT', 2),
    ('QA873_HEAD', 'QA1001_HEAD', 2),
    ('2026-09-14_secuura-873-ks931-tier1-r1', STEM, 3),
    ('refs/heads/kamilkreiser/ks-931-safeoutboundrequest-can-throw', BRANCH, 1),
    ('c624c9a8dd24129dad46cf7a204ae75ecb875dc3', HEAD, 1),
    ("MERGE_BASE='852e1fff773bd358170c11334d59496f05fdd8a7'   # M45 = the merge-base of the head with develop (M45 is an ancestor of the head)",
     "MERGE_BASE='" + BASE + "'   # the merge-base of the head with develop = the PR base (the head is its direct child)", 1),
    ("DEVELOP_SHA='bc067e3e91821116f3344b2aa5a1d7a5cc968d18'   # M46 = develop at draft time (M45 + one docs file)",
     "DEVELOP_SHA='" + BASE + "'   # develop at draft time = the base (read 21:45:11 and 21:53:14 AEST)", 1),
    ('echo "REFUSING: #873 — $HEAD_SHA is not at', 'echo "REFUSING: #1001 — $HEAD_SHA is not at', 1),
    ('# develop...#873 = M45 ahead 2 files 2.', '# develop...#1001 = 0b25f823f ahead 1 files 2.', 1),
    ('''[ "$COMPARE" = "$MERGE_BASE ahead=2 files=2" ] || { echo "REFUSING: #873 develop...head reads '$COMPARE', brief pins '$MERGE_BASE ahead=2 files=2'" >&2; exit 10; }''',
     '''[ "$COMPARE" = "$MERGE_BASE ahead=1 files=2" ] || { echo "REFUSING: #1001 develop...head reads '$COMPARE', brief pins '$MERGE_BASE ahead=1 files=2'" >&2; exit 10; }''', 1),
    ('# The develop pin, judged by CONTENT (see the header): eight files by blob at the CURRENT develop, then — if develop\n# moved — the M46...develop delta against the GUARDED list with the DEV_CONTENT_ALLOWED blobs cleared.',
     '# The develop pin, judged by CONTENT (see the header): ten files by blob at the CURRENT develop, then — if develop\n# moved — the pinned...develop delta against the GUARDED list with the DEV_CONTENT_ALLOWED blobs cleared.', 1),
    ('" — #873 has landed; this brief is stale")', '" — #1001 has landed; this brief is stale")', 1),
    ('" | origin develop still " + pinned + " (M46; git ls-remote)")', '" | origin develop still " + pinned + " (the base; git ls-remote)")', 1),
    ('tail = "the gate merges the then-current develop onto c624c9a8d in its own clone, runs the packages/shared suite on the MERGED tree beside the head tree, names the delta and re-derives every count (brief TARGET)"',
     'tail = "the gate merges the then-current develop onto 3925d4c07 in its own clone, runs the api-gateway suite on the MERGED tree beside the head tree, names the delta and re-derives every count (brief item 4)"', 1),
    ('''print("OK " + state + " | origin develop MOVED %s -> %s: commits=%d files=%d, cleared BY BLOB under guarded paths: %s (#922 / KS-679 landed — packages/shared gains its ks256 cells; the two lane files untouched) — %s" % (pinned, cur, c["ahead_by"], len(files), ",".join(x.split("/")[-1] for x in cleared), tail)); sys.exit(0)''',
     '''print("OK " + state + " | origin develop MOVED %s -> %s: commits=%d files=%d, cleared BY BLOB under guarded paths: %s — %s" % (pinned, cur, c["ahead_by"], len(files), ",".join(x.split("/")[-1] for x in cleared), tail)); sys.exit(0)''', 1),
    ('''— disjoint from the GUARDED list (packages/shared/, originate routes/webhooks.ts, the originate ks914 test + __tests__/helpers/, originate jest.config.js, m365 src/index.ts, the lockfile); %s"''',
     '''— disjoint from the GUARDED list (api-gateway src/middleware/, src/index.ts, src/routes/proxy.ts, the api-gateway config trio, originate verificationV2.ts + middleware/auth.ts + src/index.ts, the lockfile); %s"''', 1),
    ('echo "  head on origin: #873 $HEAD_SHA at $BRANCH"', 'echo "  head on origin: #1001 $HEAD_SHA at $BRANCH"', 1),
    ('echo "  compare (GitHub API): develop...#873 = $COMPARE"', 'echo "  compare (GitHub API): develop...#1001 = $COMPARE"', 1),
]
for old, new, n in subs:
    c = s.count(old)
    if c != n: refuse('anchor %r occurs %d times, expected %d' % (old[:70], c, n), 1)
    s = s.replace(old, new)

# RESIDUAL GUARD — tokens of the source gate; the header's one permitted template-name mention is stripped first.
permitted = 'Adapted from ' + TEMPLATE_NAME
if s.count(permitted) != 1: refuse('permitted template mention count %d' % s.count(permitted), 1)
body = s.replace(permitted, 'Adapted from <template>')
residual = ['873', '931', 'c624c9a8', '852e1fff7', 'bc067e3e9', 'M45', 'M46', 'ssrf', 'ks914', 'KS-679', '#922', 'ks256',
            'packages/shared', 'm365', 'webhooks.ts', 'jest.config', 'kamilkreiser', 'safeoutbound', 's232', '2026-09-14',
            '5a838e0d6', '69706c1ef', 'a1203248f', '944a5530c', 'afb0c0d08', 'ffce480e4', '2a226c006', 'c88eb97db',
            'eb655301e', '1f3a91d4f', '72533d3b0', 'b54d26929', '-r1.md', '-r1.prompt']
hits = []
for tok in residual:
    pat = r'(?<![0-9a-fA-F])' + re.escape(tok) + r'(?![0-9a-fA-F])' if tok.isdigit() else re.escape(tok)
    for m in re.finditer(pat, body):
        hits.append((tok, body.count('\n', 0, m.start()) + 1))
if hits:
    for tok, line in hits: print('REFUSING: residual token %r at line %d' % (tok, line), file=sys.stderr)
    sys.exit(2)

# OUTPUT CONTROLS — every count measured against the composed text, never guessed.
controls = [
    ('HEAD_SHA="${QA1001_HEAD:-' + HEAD + '}"', 1), ("MERGE_BASE='" + BASE + "'", 1), ("DEVELOP_SHA='" + BASE + "'", 1),
    ("BRANCH='" + BRANCH + "'", 1), (STEM + '.md', 2), (STEM + '.prompt.txt', 1),
    ('exit 2;', 1), ('exit 3;', 1), ('exit 4;', 1), ('exit 5;', 1), ('exit 6', 1), ('exit 7;', 1), ('exit 8;', 1), ('exit 9;', 1),
    ('exit 10;', 1), ('exit 11;', 1), ('exit 12;', 1), ('exit 13;', 1), ('exit 14;', 1), ('exit 15;', 1), ('exit 16;', 2), ('exit 17;', 1),
    ('exit 18; }', 1), ('exit 18 ;;', 1), ('exit 19 ;;', 1), ('exit 20;', 1), ('exit 21;', 1),
    ('DEV_CONTENT_ALLOWED = {', 1), ('print("LANDED ', 1), ('print("GUARDED ', 2), ('print("UNJUDGEABLE ', 3), ('LANDED*)', 1), ('OK*)', 1),
    ('a81722795302100ce8d7db4ea788be0de3f89942', 1), ('1f16e2f899af46b8afc5e3872261e079c2cf88f5', 1),
    ('6f38c819e48162e3179aaf557085766f91beecc1', 1), ('5b5b3e7342d04451ea8a7dff0823fc5763122059', 1), ('1a7312a8675ffdfe263060bb5d60aa837111431a', 1),
    ('b99f45a4c9c89088a7809de5f26c4f56fc94819c', 1), ('5888e0b320d934f6f434e0e5ca3c74a995cecc02', 1), ('22c1107683b8192df3bfd3e929aa94aff3dc7d45', 1),
    ('841d8c6adcd71e885c01e65c22da9418daff276a', 1), ('dfa26c0572d6a3888d7b07bc6172b4b7ef4852e0', 1), ('f08ee1a895bc878bc2656f649833706f665686e7', 1),
    ('ahead=1 files=2', 2), ('ahead=2', 0), ('[ -t 0 ]', 1), ('exec claude --dangerously-skip-permissions --model opus', 1),
    ('git -C "$REPO"', 2), ('set -u', 1), ('MAIL YOUR VERDICT', 1), ('NEVER print a credential value', 1), ('no memory maintenance', 1),
    ("grep -q 'TIER 1'", 2), ("grep -q 'ROUND 1'", 2), ('D + "services/api-gateway/src/middleware/",', 1), ('D + "package-lock.json"]', 1),
    ('#1001', 9),   # MEASURED by enumeration (2nd run refused on a guessed 7): header :2 :27; body :54 :60 :73 :91 :110 :175 :176
]
bad = [(k, want, s.count(k)) for k, want in controls if s.count(k) != want]
if bad: refuse('output controls %r' % bad, 1)
if 'git -C $' in s: refuse('git -C $VAR form', 1)
verbs = re.findall(r'git (?:-C "\$REPO" )?(fetch|checkout|worktree|merge-tree|merge|pull|push|reset|switch|clone)\b', s)
if verbs: refuse('git write verbs in the launcher %r' % verbs, 1)
pyj = s.split("<<'PYJ'")[1].split('PYJ\n')[0]
if pyj.count("'") % 2: refuse('odd apostrophes inside the PYJ heredoc (%d)' % pyj.count("'"), 1)
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
