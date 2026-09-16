#!/usr/bin/env python3
"""gen_launcher_1006.py — derive launch_qa_secuura_ks844_1006.sh from tonight's #1005 TIER 1 launcher
(launchers/launch_qa_secuura_ks1073_1005.sh — guard family: head on origin exit 6, compare exit 10/13, develop judged BY CONTENT exit
18/19, head SHA named in brief+prompt exit 20, TTY exit 21) by ASSERTED substitutions: every anchor must occur exactly as often as
stated, or the generator refuses and writes nothing. Then a RESIDUAL GUARD (any token of the source gate left anywhere, after stripping
the one permitted template-name mention, is a refusal), output controls (every count measured against the composed text; '#1006' is
ENUMERATED first with --enumerate, which writes only to the scratch path given and prints the lines), PY/PYJ-heredoc apostrophe/paren
parity, no git write verbs, no control bytes, bash -n. Never overwrites an existing output without a .pre-* copy.
Usage: gen_launcher_1006.py <template launcher> <output launcher> [--enumerate]
Exit: 0 written · 1 an anchor/control count disagreed · 2 a residual token survived · 3 bash -n failed"""
import datetime, hashlib, os, re, shutil, subprocess, sys

src_path, out_path = sys.argv[1], sys.argv[2]
ENUMERATE = '--enumerate' in sys.argv[3:]
s = open(src_path, encoding='utf-8').read()
def refuse(msg, code):
    print('REFUSING: ' + msg, file=sys.stderr); sys.exit(code)

HEAD = '86fe59e6bf07108142fb3dbd06bef8747d2a4687'
BASE = '40fe4db6963cd11dba06bd46e0b00af39e68ef3a'     # the merge-base = develop itself: develop is an ANCESTOR of the head
DEVELOP = '40fe4db6963cd11dba06bd46e0b00af39e68ef3a'  # develop at draft time (git ls-remote 00:28:49, branches API 00:31:54)
BRANCH = 'refs/heads/feature/ks-844-demo-service-error-handler'
STEM = '2026-09-17_secuura-1006-ks844-tier1'
OLD_STEM = '2026-09-17_secuura-1005-ks1073-tier1'
TEMPLATE_NAME = 'launch_qa_secuura_ks1073_1005.sh'
COUNT_1006 = None if ENUMERATE else 12  # MEASURED by --enumerate (gen_launcher.enumerate-to-scratch.out, 00:4x): the drafter's placeholder was 10 — wrong; line 96 carries two

NEW_HEADER = '''#!/bin/bash
# launch_qa_secuura_ks844_1006.sh — cross-project QA agent, ONE TIER 1 ROUND 1 gate over Secuura/Blockchain PR #1006
# (KS-844, Seat A) @ 86fe59e6bf07108142fb3dbd06bef8747d2a4687 — TWO commits on develop 40fe4db69 (e28c91f9b the change, 86fe59e6b a
# comment-only KS-727 header count), 5 files: demo-service app.ts +5 (mounts an exported errorHandler), middleware/errorHandler.ts
# (new), ks844 test (new); packages/shared guard tests ks727-errorhandler-class-guard +5 -3 (one corpus-1 entry in both exact sets +
# the header count) and ks781-p3-3-body-parser-order +14 -4 (the KS-832 marker spliced ahead of demo-service's errorHandler). TIER 1:
# it edits two packages/shared SECURITY GUARD test files and the handler that decides what an error response leaks.
#
# THE SHAPE, as read 00:28-00:42 AEST 2026-09-17 (git + the compare API agree): develop 40fe4db69 is an ANCESTOR of the head
# (merge-base = develop, behind 0), so the merged tree IS the head tree. compare develop...head = merge_base 40fe4db69, status ahead,
# ahead 2, behind 0, files 5. The compare is asserted as merge_base + ahead + files (exit 10); `behind` is deliberately NOT asserted,
# so a develop that moves on does not trip this guard — the develop arm judges the move by CONTENT.
#
# The develop pin is judged by CONTENT, not bare: (a) TWELVE files by blob at the CURRENT develop — demo-service app.ts (base
# 81bc26cb3; the PR's own dd714042d -> exit 19 LANDED), ks727-errorhandler-class-guard.test.ts (base 2274c71ac; the PR's 512729715 or
# its first commit's 288d5daf7 -> LANDED), ks781-p3-3-body-parser-order.test.ts (base 9bcdb4259; the PR's ca1fe34a7 -> LANDED), and nine
# files the gate's predictions stand on: demo-service package.json / package-lock.json / tsconfig.json / middleware/demoGuard.ts,
# packages/shared middleware/index.ts (rejectControlBytes) / __tests__/entrypoint-corpus.ts / vitest.config.ts / package.json /
# tsconfig.json — any blob nobody pinned -> exit 18 (the new errorHandler.ts and ks844 test are NOT judged: they are absent on develop,
# and app.ts already detects a landing); (b) if develop moved past 40fe4db69, the compare pinned...develop REFUSES (exit 18) only when
# the delta touches a GUARDED path — services/demo-service/, the three shared guard files, packages/shared/src/middleware/ or errors/,
# the shared vitest config or package.json, the Dev lockfile, or ANY */middleware/errorHandler.ts (a new corpus-1 member changes the
# exact sets) — or cannot be judged; anything else proceeds and the gate re-derives counts on the merged tree.
# DEV_CONTENT_ALLOWED is empty: dependabot #649/#575 touch demo-service package.json and the Dev lockfile — if one lands, this
# launcher refuses and the brief is re-pinned deliberately.
#
# exit 21: the LAUNCH path refuses when stdin is not a TTY. This launcher execs an interactive agent; run it in a cockpit
# pane, never inside a Bash tool. `--check` still runs headless (it launches nothing).
#
# Adapted from launch_qa_secuura_ks1073_1005.sh by gen_launcher_1006.py (asserted substitutions + residual guard + output
# controls + bash -n): same guards and exit codes, re-pointed at #1006. Exit codes 2..21 (19 = LANDED).
# Written by the generator because it contains a legitimate directory change.
#
# Usage: launch_qa_secuura_ks844_1006.sh [--check]
# Exit: 0 launched (or guards passed under --check) · 2..21 a guard refused
'''
marker = 'set -u\n'
if s.count(marker) != 1: refuse('header marker set -u count %d' % s.count(marker), 1)
s = NEW_HEADER + s[s.index(marker):]

J = lambda *lines: '\n'.join(lines)
NEW_JUDGED = J(
 '# file -> (develop-OK blobs {blob: label}, LANDED blobs {blob: label})',
 'JUDGED = {',
 '  D + "services/demo-service/src/app.ts":                                        ({"81bc26cb31edd20713fde703675965bf052a5b10": "base"}, {"dd714042dbcd1f37f6e26997f1e31c7392af910d": "#1006 own"}),',
 '  D + "packages/shared/src/__tests__/ks727-errorhandler-class-guard.test.ts":    ({"2274c71acaa9638617242300a0e90b385b81d093": "base"}, {"5127297156ed9b970ad17e804b3e3211894b6f8c": "#1006 own", "288d5daf76c9e0bd1b2a61b4bebd7857a8276751": "#1006 first commit"}),',
 '  D + "packages/shared/src/__tests__/ks781-p3-3-body-parser-order.test.ts":     ({"9bcdb42593925603bdbc617cd13b0f91c863bc9c": "base"}, {"ca1fe34a74880305cebf87e034d9d9ffa9c94f3c": "#1006 own"}),',
 '  D + "services/demo-service/package.json":                                      ({"02aef8bbc26660fc295251f3705ac971f8ff0405": "base"}, {}),',
 '  D + "services/demo-service/package-lock.json":                                 ({"c043455f53353117f49ee5aeaf3dfc4360e436d8": "base"}, {}),',
 '  D + "services/demo-service/tsconfig.json":                                     ({"ae20f7922d4270e7447e463668d6a087d971cd87": "base"}, {}),',
 '  D + "services/demo-service/src/middleware/demoGuard.ts":                       ({"0da9a28f75cd17249993d4ca374da54ac2f398c2": "base"}, {}),',
 '  D + "packages/shared/src/middleware/index.ts":                                 ({"3a67987a7be4a4c02f8326bf8a840a2c2b4efbf3": "base"}, {}),',
 '  D + "packages/shared/src/__tests__/entrypoint-corpus.ts":                      ({"a7abd31efe0872a269828c00aa30da86e0f240da": "base"}, {}),',
 '  D + "packages/shared/vitest.config.ts":                                        ({"2a226c0068faa65538cda8d43d03bb9bee2944f1": "base"}, {}),',
 '  D + "packages/shared/package.json":                                            ({"3957692311221fbe87c4ab19447de8cec44aa19a": "base"}, {}),',
 '  D + "packages/shared/tsconfig.json":                                           ({"1fd016cc28803cc8f36cc84db4628941a2af9c50": "base"}, {}),',
 '}\n')
NEW_GUARDED = J(
 'GUARDED = [D + "services/demo-service/",',
 '           D + "packages/shared/src/__tests__/ks727-errorhandler-class-guard.test.ts",',
 '           D + "packages/shared/src/__tests__/ks781-p3-3-body-parser-order.test.ts",',
 '           D + "packages/shared/src/__tests__/entrypoint-corpus.ts",',
 '           D + "packages/shared/src/middleware/",',
 '           D + "packages/shared/src/errors/",',
 '           D + "packages/shared/vitest.config.ts",',
 '           D + "packages/shared/package.json",',
 '           D + "package-lock.json"]',
 '# SUFFIX-GUARDED: any error-handler module anywhere changes KS-727 corpus 1 (its two EXACT sets) on the merged tree.',
 'GUARDED_SUFFIX = ["/middleware/errorHandler.ts"]\n')
NEW_ALLOWED = J(
 '# STYLE NOTE (912r2 launcher, measured): bash scans quote/paren state THROUGH this heredoc because it sits inside a',
 '# command substitution — keep apostrophes and parentheses EVEN (this block uses none of the former), or the outer $( ) breaks.',
 '# CONTENT-JUDGED allowlist: a hit under a GUARDED path clears ONLY if the per-file blob sha in the compare is EXACTLY one',
 '# pinned here. EMPTY for this gate: at draft time 00:31 AEST no open lane PR touched a guarded path except dependabot',
 '# bumps of demo-service package.json and the Dev lockfile, which must NOT clear silently, so every guarded hit falls through to GUARDED and exit 18 — re-pin deliberately.',
 'DEV_CONTENT_ALLOWED = {',
 '}\n')

def block(start, end_marker):
    i = s.find(start)
    if i < 0 or s.count(start) != 1: refuse('block start %r count %d' % (start[:50], s.count(start)), 1)
    j = s.find(end_marker, i)
    if j < 0: refuse('block end %r not found' % end_marker[:40], 1)
    return s[i:j + len(end_marker)]
old_judged = block('# file -> (develop-OK blobs {blob: label}, LANDED blobs {blob: label})', '}\n')
old_guarded = block('GUARDED = [D + "services/api-gateway/src/routes/",', '"package-lock.json"]\n')
old_allowed = block('# STYLE NOTE (912r2 launcher, measured)', 'DEV_CONTENT_ALLOWED = {\n')
old_allowed = old_allowed + s[s.index(old_allowed) + len(old_allowed): s.index('}\n', s.index(old_allowed) + len(old_allowed)) + 2]

subs = [
    (old_judged, NEW_JUDGED, 1),
    (old_guarded, NEW_GUARDED, 1),
    (old_allowed, NEW_ALLOWED, 1),
    ('hits = sorted({x["filename"] for x in files for g in GUARDED if x["filename"] == g or (g.endswith("/") and x["filename"].startswith(g))})',
     'hits = sorted({x["filename"] for x in files for g in GUARDED if x["filename"] == g or (g.endswith("/") and x["filename"].startswith(g))} | {x["filename"] for x in files for g in GUARDED_SUFFIX if x["filename"].endswith(g)})', 1),
    ('QA1005_BRIEF', 'QA1006_BRIEF', 2),
    ('QA1005_PROMPT', 'QA1006_PROMPT', 2),
    ('QA1005_HEAD', 'QA1006_HEAD', 2),
    (OLD_STEM, STEM, 3),
    ('refs/heads/feature/ks-1073-ornith-tier2-statusless-carveout', BRANCH, 1),
    ('e5e7ff99dbc4881784ce0beacefb4e7e36c55cf9', HEAD, 1),
    ("MERGE_BASE='dd66863dd2858e97344652c1106d38f5e352a41b'   # the merge-base of the head with develop = the PR base (#1002's squash; develop moved on to #1004)",
     "MERGE_BASE='" + BASE + "'   # the merge-base of the head with develop = develop itself (develop is an ancestor of the head; behind 0)", 1),
    ("DEVELOP_SHA='40fe4db6963cd11dba06bd46e0b00af39e68ef3a'   # develop at draft time = #1004's squash, a child of the base, packages/shared only (read 00:05:37 and 00:07:38 AEST)",
     "DEVELOP_SHA='" + DEVELOP + "'   # develop at draft time = the PR base (git ls-remote 00:28:49, branches API 00:31:54 AEST)", 1),
    ('echo "REFUSING: #1005 — $HEAD_SHA is not at', 'echo "REFUSING: #1006 — $HEAD_SHA is not at', 1),
    ('# develop...#1005 = dd66863dd ahead 1 files 2 (behind 1 — #1004 — deliberately not asserted).', '# develop...#1006 = 40fe4db69 ahead 2 files 5 (behind 0; behind deliberately not asserted).', 1),
    ('''[ "$COMPARE" = "$MERGE_BASE ahead=1 files=2" ] || { echo "REFUSING: #1005 develop...head reads '$COMPARE', brief pins '$MERGE_BASE ahead=1 files=2'" >&2; exit 10; }''',
     '''[ "$COMPARE" = "$MERGE_BASE ahead=2 files=5" ] || { echo "REFUSING: #1006 develop...head reads '$COMPARE', brief pins '$MERGE_BASE ahead=2 files=5'" >&2; exit 10; }''', 1),
    ('# The develop pin, judged by CONTENT (see the header): eight files by blob at the CURRENT develop, then — if develop',
     '# The develop pin, judged by CONTENT (see the header): twelve files by blob at the CURRENT develop, then — if develop', 1),
    ('" — #1005 has landed; this brief is stale")', '" — #1006 has landed; this brief is stale")', 1),
    ('print("OK " + state + " | origin develop still " + pinned + " (#1004 squash on the base, file-disjoint from #1005; git ls-remote)"); sys.exit(0)',
     'print("OK " + state + " | origin develop still " + pinned + " (the PR base, an ancestor of the head: merged tree = head tree; git ls-remote)"); sys.exit(0)', 1),
    ('tail = "the gate merges the then-current develop onto e5e7ff99d in its own clone, rebuilds the shared dist there, runs the api-gateway suite on the MERGED tree beside the base and head trees, names the delta and re-derives every count (brief item 6)"',
     'tail = "the gate merges the then-current develop onto 86fe59e6b in its own clone, rebuilds the shared dist there, runs the packages/shared and demo-service suites on the MERGED tree beside the base and head trees, names the delta and re-derives every count, above all the KS-727 exact sets and the KS-800 parsing-unit set (brief items 3 and 7)"', 1),
    ('''— disjoint from the GUARDED list (api-gateway src/routes/, api-gateway src/index.ts + config trio, the ks1057 test, originate routes/documents.ts, anchoring src/index.ts, eslint.config.mjs, the lockfile); %s"''',
     '''— disjoint from the GUARDED list (services/demo-service/, the three shared guard files, shared src/middleware/ + src/errors/ + vitest config + package.json, the Dev lockfile, any */middleware/errorHandler.ts); %s"''', 1),
    ('echo "  head on origin: #1005 $HEAD_SHA at $BRANCH"', 'echo "  head on origin: #1006 $HEAD_SHA at $BRANCH"', 1),
    ('echo "  compare (GitHub API): develop...#1005 = $COMPARE"', 'echo "  compare (GitHub API): develop...#1006 = $COMPARE"', 1),
]
for old, new, n in subs:
    c = s.count(old)
    if c != n: refuse('anchor %r occurs %d times, expected %d' % (old[:70], c, n), 1)
    s = s.replace(old, new)

permitted = 'Adapted from ' + TEMPLATE_NAME
if s.count(permitted) != 1: refuse('permitted template mention count %d' % s.count(permitted), 1)
body = s.replace(permitted, 'Adapted from <template>')
residual = ['1005', '1073', 'QA1005', 'e5e7ff99d', 'dd66863dd', 'ornith-tier2', 'statusless', 'verification', 'api-gateway', 'ks1057',
            'originate', 'anchoring', 'c83a2ae27', 'de34b2de7', '6f38c819e', '5888e0b32', '841d8c6ad', 'c981e6a92', 'aceaef1fa', 'c3a818ac8',
            'da4abd432', 'eslint.config', 'eight files', '#1004', '00:05:37', '00:07:38', 'ahead=1', 'files=2', '#923', '#995']
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
        if '#1006' in l: print('#1006 at line %d: %s' % (i, l[:110]))
    print('ENUMERATED count #1006 = %d (scratch copy written to %s; nothing written to launchers/)' % (s.count('#1006'), out_path)); sys.exit(0)

controls = [
    ('HEAD_SHA="${QA1006_HEAD:-' + HEAD + '}"', 1), ("MERGE_BASE='" + BASE + "'", 1), ("DEVELOP_SHA='" + DEVELOP + "'", 1),
    ("BRANCH='" + BRANCH + "'", 1), (STEM + '.md', 2), (STEM + '.prompt.txt', 1),
    ('exit 2;', 1), ('exit 3;', 1), ('exit 4;', 1), ('exit 5;', 1), ('exit 6', 1), ('exit 7;', 1), ('exit 8;', 1), ('exit 9;', 1),
    ('exit 10;', 1), ('exit 11;', 1), ('exit 12;', 1), ('exit 13;', 1), ('exit 14;', 1), ('exit 15;', 1), ('exit 16;', 2), ('exit 17;', 1),
    ('exit 18; }', 1), ('exit 18 ;;', 1), ('exit 19 ;;', 1), ('exit 20;', 1), ('exit 21;', 1),
    ('DEV_CONTENT_ALLOWED = {', 1), ('print("LANDED ', 1), ('print("GUARDED ', 2), ('print("UNJUDGEABLE ', 3), ('LANDED*)', 1), ('OK*)', 1),
    ('81bc26cb31edd20713fde703675965bf052a5b10', 1), ('dd714042dbcd1f37f6e26997f1e31c7392af910d', 1), ('2274c71acaa9638617242300a0e90b385b81d093', 1),
    ('5127297156ed9b970ad17e804b3e3211894b6f8c', 1), ('288d5daf76c9e0bd1b2a61b4bebd7857a8276751', 1), ('9bcdb42593925603bdbc617cd13b0f91c863bc9c', 1),
    ('ca1fe34a74880305cebf87e034d9d9ffa9c94f3c', 1), ('02aef8bbc26660fc295251f3705ac971f8ff0405', 1), ('c043455f53353117f49ee5aeaf3dfc4360e436d8', 1),
    ('ae20f7922d4270e7447e463668d6a087d971cd87', 1), ('0da9a28f75cd17249993d4ca374da54ac2f398c2', 1), ('3a67987a7be4a4c02f8326bf8a840a2c2b4efbf3', 1),
    ('a7abd31efe0872a269828c00aa30da86e0f240da', 1), ('2a226c0068faa65538cda8d43d03bb9bee2944f1', 1), ('3957692311221fbe87c4ab19447de8cec44aa19a', 1),
    ('1fd016cc28803cc8f36cc84db4628941a2af9c50', 1),
    ('ahead=2 files=5', 2), ('[ -t 0 ]', 1), ('exec claude --dangerously-skip-permissions --model opus', 1),
    ('git -C "$REPO"', 2), ('set -u', 1), ('MAIL YOUR VERDICT', 1), ('NEVER print a credential value', 1), ('no memory maintenance', 1),
    ("grep -q 'TIER 1'", 2), ("grep -q 'ROUND 1'", 2), ('D + "services/demo-service/",', 1), ('D + "package-lock.json"]', 1),
    ('GUARDED_SUFFIX = ["/middleware/errorHandler.ts"]', 1), ('for g in GUARDED_SUFFIX if x["filename"].endswith(g)', 1),
    ('#1006', COUNT_1006),
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
