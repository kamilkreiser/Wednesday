#!/usr/bin/env python3
"""gen_launcher_1034.py — derive launchers/launch_qa_secuura_ks1215_1034.sh from launchers/launch_qa_secuura_ks1194_1032.sh (the latest generated launcher: same
guard set, blob-judged develop arm, GUARDED compare arm) by ASSERTED substitutions: every anchor must occur exactly as often as stated, or the generator refuses and
writes nothing. Shape follows gen_launcher_1032.py (pins re-read from the repo, tmp file, bash -n on the tmp, then os.replace; .pre-* copy if the output exists).
Re-points at #1034 (KS-1215) ROUND 1: head fd81a75f0; the pinned develop 27e53ec3a is the head's second parent AND merge-base AND develop at drafting, so
compare develop...head = merge_base 27e53ec3a ahead 2 files 2 (behind NOT asserted). The develop arm judges TWENTY-FOUR api-gateway / shared / lint files by PATH
BLOB at the CURRENT develop — never by develop's SHA (auth.ts 6e1668362, the ks1215 test ABSENT; at their #1034 blobs -> exit 19 LANDED). On a develop move the
compare pinned...current REFUSES (exit 18) when it touches services/api-gateway/src/ or its package.json / vitest.config.ts / vitest.setup.ts / tsconfig.json,
packages/shared/src/ or eslint.config.mjs. DEV_CONTENT_ALLOWED is EMPTY (no lockfile is guarded: the gate reads the vitest version develop's lock pins and says
which one ran). Test fixture QA1034_AUTH_FILE stands in for develop auth.ts (content and git blob).
Residual guard, output controls, heredoc parity, no git write verb, no control bytes, bash -n.
Usage: gen_launcher_1034.py <template launcher> <output launcher>   Exit: 0 written · 1 anchor/control disagreed · 2 residual token · 3 bash -n failed"""
import hashlib, os, re, shutil, subprocess, sys
TPL, OUT = sys.argv[1], sys.argv[2]
s = open(TPL).read()
def now(f='+%Y-%m-%d %H:%M:%S %Z'): return subprocess.run(['date', f], capture_output=True, text=True).stdout.strip()
print('gen_launcher_1034', now(), '| template sha256', hashlib.sha256(s.encode()).hexdigest()[:16], 'lines', s.count('\n'))
REPO = '/Volumes/DevMASTER/!CODING/Secuura/Blockchain/2_Project_Files'
H = 'fd81a75f0688f6cbe1e5f79b061bb1369c88f477'; MB = '27e53ec3aa010b50cd9b2e4a1d15cbb34605ba7d'; FIX = '6c6fdc94e869c98a73e6ffaa1b66be1d3b20d7b3'
HT = '6339c404c05fcfbfa3b6505b6bfb7955303c1ccd'
D = 'Blockchain/Dev/'; A = 'services/api-gateway/'
rp = lambda x: subprocess.run(['git', '-C', REPO, 'rev-parse', '--verify', '-q', x], capture_output=True, text=True).stdout.strip()
T1215 = A + 'src/__tests__/ks1215-the-connector-branch-never-carries-the-callers-bearer.test.ts'
PIN = {  # path relative to Blockchain/Dev -> blob at develop 27e53ec3a (develop-OK); re-read and asserted below
 A + 'src/middleware/auth.ts': '6e16683624b3c38a365ece44cccb4fdfac892c71',
 A + 'src/index.ts': 'db127dbfa5dd899b0a8e0d844690890d91e27f10',
 A + 'src/routes/proxy.ts': '795ae7ca3bdc76be3e563e87fc34a8cc221e5632',
 A + 'src/routes/platform.ts': '4550401f8d7d76afa848855cdf7558a35fd02de0',
 A + 'src/routes/batch.ts': 'f2f48dca32e5611732d25c7d36b03da0e0d145cb',
 A + 'src/routes/admin.ts': 'f47dd6a655702ffbfc402ca920a33c4619d62c4b',
 A + 'src/routes/verification.ts': '28fb5834308a502f5f7b806e3b49a77627601eff',
 A + 'src/middleware/rateLimitEnforce.ts': '90bd29378508c8fee54e010b54cdc72ff992aafa',
 A + 'src/middleware/scopes.ts': '7aef335b93acf7a94fbcadc61c353d7a5dde90c5',
 A + 'src/services/redis.ts': '47659ee9c9f06acf9ac64e09b2dc207113ba92ea',
 A + 'src/utils/trustHeaders.ts': '15626e80f6caea4866abd1bb9ad171c79e12e788',
 A + 'src/db.ts': '9144c532bca9911da6cedd569e575c5aa6bc6c52',
 A + 'src/__tests__/ks1207-a-failed-optional-api-key-falls-through-to-the-bearer-check.test.ts': 'f56bd48b9e9213d5afb85df6c94a5eada3c5aa22',
 A + 'src/__tests__/ks480-connector-auth.test.ts': 'eca492723115531d8daa52d1d8b52b1b9b99970a',
 A + 'package.json': '841d8c6adcd71e885c01e65c22da9418daff276a',
 A + 'vitest.config.ts': '5888e0b320d934f6f434e0e5ca3c74a995cecc02',
 A + 'vitest.setup.ts': '22c1107683b8192df3bfd3e929aa94aff3dc7d45',
 A + 'tsconfig.json': 'c981e6a92fdd2417fa35070eb979c5f1c77ffbcd',
 'packages/shared/src/db/tenant-guc.ts': '86953b978062eb1d124abf3154fa1da324c6e110',
 'packages/shared/src/security/session-validation.ts': '297a0bbd31be5c3868beb1a94d33c8e9d1dcf98d',
 'packages/shared/src/crypto/jwks.ts': 'a131d32caa3faf0f55ca9af1a4fcd889a1affa17',
 'packages/shared/src/utils/gracefulShutdown.ts': '5550416464de399e86f6c4041a3279962119af82',
 'eslint.config.mjs': '8c5374c6022eb0a3f449f41a570db61294aa63f1',
}
LANDED = {A + 'src/middleware/auth.ts': 'bf09d315a64443b7f02bc27a74366b7a7f1dae81', T1215: '5b7431af0fbb203e7582d8f188eca3f15d5d05fe'}
bad = []
for p, b in PIN.items():
    at_mb, at_h = rp(MB + ':' + D + p), rp(H + ':' + D + p)
    if at_mb != b: bad.append(('develop blob', p, b, at_mb))
    if p not in LANDED and at_h != b: bad.append(('head blob differs for an untouched file', p, b, at_h))
for p, b in LANDED.items():
    if rp(H + ':' + D + p) != b or rp(FIX + ':' + D + p) != b: bad.append(('landed blob at head and at the fix', p, b, rp(H + ':' + D + p), rp(FIX + ':' + D + p)))
if rp(H + '^{tree}') != HT: bad.append(('head tree', rp(H + '^{tree}')))
if rp(H + '^2') != MB: bad.append(('head second parent', rp(H + '^2')))
if rp(H + '^1') != FIX: bad.append(('head first parent', rp(H + '^1')))
p = subprocess.run(['git', '-C', REPO, 'cat-file', '-e', MB + ':' + D + T1215], capture_output=True); print('ks1215 test ABSENT at develop (cat-file -e rc != 0):', p.returncode != 0)
if p.returncode == 0: bad.append(('ks1215 test present at develop',))
print('pinned blobs re-read from the repo (develop 27e53ec3a for all %d; head = develop for the %d untouched; the 2 PR files at head and at the fix 6c6fdc94e):' % (len(PIN) + 1, len(PIN) - 1), 'OK' if not bad else bad)
if bad: print('REFUSING: pins disagree with the repo; nothing written'); sys.exit(1)
def cut(start, end_incl):
    assert s.count(start) == 1, ('cut start', start[:60], s.count(start))
    i = s.index(start); j = s.index(end_incl, i) + len(end_incl); return s[i:j]
REPORT_DIR = '/Volumes/DevMASTER/!CODING/Testing Agent MAIN/projects/secuura/reports/2026-09-17-ks1215-1034-fd81a75f0-tier1-r1/'
PRIOR = '/Volumes/DevMASTER/!CODING/Testing Agent MAIN/projects/secuura/reports/2026-09-17-ks1207-1023-2f74491eb-tier1-r1/'
OLD_REPORT = '/Volumes/DevMASTER/!CODING/Testing Agent MAIN/projects/secuura/reports/2026-09-17-ks1194-1032-70ee7b6c0-tier1-r1/'
OLD_PRIOR = '/Volumes/DevMASTER/!CODING/Testing Agent MAIN/projects/secuura/reports/2026-09-17-ks1018-1015-77145ce84-tier1-r1/'
assert os.path.isdir(PRIOR), 'prior report dir missing'
HEADER_OLD = cut('# launch_qa_secuura_ks1194_1032.sh', "# Exit: 0 launched (or guards passed under --check) · 2..25 a guard refused\n")
HEADER_NEW = """# launch_qa_secuura_ks1215_1034.sh — cross-project QA agent, ONE TIER 1 ROUND 1 gate over Secuura/Blockchain PR #1034 (KS-1215, Seat A)
# @ fd81a75f0688f6cbe1e5f79b061bb1369c88f477 — services/api-gateway: the connector branch never carries the caller's Bearer. authenticateToken's valid-key
# branch drops req.headers.authorization as its FIRST statement, before any await (Wednesday's ruling O3, 11:22:22Z); a successful connector-token exchange
# still sets the connector JWT, a failed one forwards no Bearer. The change commit 6c6fdc94e (parent 0a2b1603f): middleware/auth.ts +9 (one delete + comment),
# the ks1215 test +302 (16 cells: runtime on optional /api/credentials + required /api/documents, one production /api/v1 row, two STRUCTURAL direct-call
# cells per Wednesday's 11:59:12Z ruling, completeness). fd81a75f0 = develop 27e53ec3a merged in; tree 6339c404c = merge-tree 6c6fdc94e x 27e53ec3a.
# TIER 1: gateway authentication on every mount; the source is the #1023 gate's N-1 (a revoked session's Bearer forwarded beside a valid key). A GO is NOT a
# merge authorisation: the merge waits for Kam's tap.
#
# THE SHAPE, as read 23:03-23:40 AEST 2026-09-17 (git ls-remote + the PR and compare APIs agree): develop 27e53ec3a is the head merge-base AND its second
# parent AND develop at drafting, so compare develop...head = merge_base 27e53ec3a, ahead 2, files 2 (asserted, exit 10; behind NOT asserted).
#
# The develop pin is judged by CONTENT — PATH BLOBS — never by develop's SHA: (a) TWENTY-FOUR files by blob at the CURRENT develop — the PR two (middleware/auth.ts
# 6e1668362, the ks1215 test ABSENT; at a #1034 blob -> exit 19 LANDED), and what the gate runs and reads: index.ts (mount order, the rawAuthorization capture,
# the unhandledRejection handler), routes/proxy.ts, platform.ts (authHeaders reads rawAuthorization), batch.ts, admin.ts, verification.ts, middleware
# rateLimitEnforce.ts and scopes.ts, services/redis.ts, utils/trustHeaders.ts, db.ts, the ks1207 and ks480 tests, gateway package.json / vitest.config.ts /
# vitest.setup.ts / tsconfig.json, shared db/tenant-guc.ts, security/session-validation.ts, crypto/jwks.ts, utils/gracefulShutdown.ts, Dev eslint.config.mjs —
# any blob nobody pinned -> exit 18; (b) if develop moved past 27e53ec3a, the compare pinned...develop REFUSES (exit 18) when the delta touches a GUARDED path —
# services/api-gateway/src/ and its package.json / vitest.config.ts / vitest.setup.ts / tsconfig.json, packages/shared/src/, eslint.config.mjs — or the move
# cannot be judged. WHY these paths: they are the code and configuration the gate runs in-process (the real index.ts app, its middleware and routes, the shared
# session / JWKS / tenant / shutdown helpers); a develop merge elsewhere (other services, frontends, audit baselines, lockfiles) cannot change what the gate
# measures, so it must not refuse. DEV_CONTENT_ALLOWED is EMPTY. Open PRs #575 / #649 (api-gateway package.json), #923 (an api-gateway test), #995
# (utils/trustHeaders.ts) and #922 (shared src) touch GUARDED paths: if one lands first this REFUSES by design — re-pin deliberately.
#
# exit 21: the LAUNCH path refuses when stdin is not a TTY. This launcher execs an interactive agent; run it in a cockpit
# pane, never inside a Bash tool — and never run it without --check to "prove" this guard. `--check` runs headless (it launches nothing).
# exit 22: the prompt must require node_modules farmed PER ENTRY (the #1009 gate R-6: a wholesale link can write through to the checkout .vite).
# exit 23: the prompt must carry the exact #1034 verdict subject and name coagent@ as the sender and wednesday-agent@ as the recipient.
# exit 24: brief AND prompt must name the REPORT DIRECTORY and the PRIOR REPORT (#1023, KS-1207: its N-1 is this ticket; the QA agent has no inbox), and the
#          prompt must name NOT-TESTED.written-first.md (written FIRST, before any run).
# exit 25: brief AND prompt must carry the MERGE ADDENDUM and require the per-finding CLOSED / STILL OPEN / NEW disposition.
# QA1034_CUR_DEV (test override, --check only): stands in for origin develop so the LANDED / GUARDED refusals can be proven.
# QA1034_AUTH_FILE (test fixture, --check only): a local file stands in for develop middleware/auth.ts (its git blob) so the LANDED and GUARDED
# arms can be proven without a real develop commit.
# A launch with any QA1034_* override or fixture set refuses (exit 16).
#
# Generated by gatesets/2026-09-17_gate1034/gen_launcher_1034.py from launch_qa_secuura_ks1194_1032.sh (asserted substitutions + pins re-read from the repo +
# residual guard + output controls + bash -n): same guard set and exit codes 2..25 (19 = LANDED), re-pointed at #1034 ROUND 1, no content-cleared blob.
#
# Usage: launch_qa_secuura_ks1215_1034.sh [--check]
# Exit: 0 launched (or guards passed under --check) · 2..25 a guard refused
"""
JUDGED_OLD = cut('A = D + "services/auth/"\n', 'content_cleared = set()\n')
def key(p_):
    return ('A + "' + p_[len(A):] + '"') if p_.startswith(A) else ('D + "' + p_ + '"')
rows = ['  AUTHTS:' + ' ' * 63 + '({"' + PIN[A + 'src/middleware/auth.ts'] + '": DV}, {"' + LANDED[A + 'src/middleware/auth.ts'] + '": "#1034 own"}),',
        '  A + "src/__tests__/ks1215-the-connector-branch-never-carries-the-callers-bearer.test.ts": ({"ABSENT": DV}, {"' + LANDED[T1215] + '": "#1034 own"}),']
for p_, b_ in PIN.items():
    if p_ in LANDED: continue
    k = key(p_); rows.append('  %s:%s({"%s": DV}, {}),' % (k, ' ' * max(1, 70 - len(k)), b_))
JUDGED_NEW = ('A = D + "services/api-gateway/"\nAUTHTS = A + "src/middleware/auth.ts"\nDV = "develop"\n'
              '# file -> (develop-OK blobs {blob: label}, LANDED blobs {blob: label}); ABSENT = the contents API answers 404 at develop\nJUDGED = {\n' + '\n'.join(rows) +
              '\n}\n# No REGION judgement: every file is judged by exact blob (a develop move of auth.ts, index.ts or platform.ts refuses, exit 18).\ncontent_cleared = set()\n')
GUARD_OLD = cut('GUARDED = [A + "src/",\n', 'DEV_CONTENT_ALLOWED = {}\n')
GUARD_NEW = '''GUARDED = [A + "src/",
           A + "package.json",
           A + "vitest.config.ts",
           A + "vitest.setup.ts",
           A + "tsconfig.json",
           D + "packages/shared/src/",
           D + "eslint.config.mjs"]
# STYLE NOTE (912r2 launcher, measured): bash scans quote/paren state THROUGH this heredoc because it sits inside a
# command substitution — keep apostrophes and parentheses EVEN (this block uses none of the former), or the outer $( ) breaks.
# CONTENT-JUDGED allowlist: EMPTY. No lockfile is guarded: the gate names the vitest version it ran against develop-s lock. Re-pin deliberately.
DEV_CONTENT_ALLOWED = {}
'''
OKLINE_OLD = cut('print("OK " + state + " | origin develop MOVED %s -> %s', 'sys.exit(0)\n')
OKLINE_NEW = 'print("OK " + state + " | origin develop MOVED %s -> %s: commits=%d files=%d — GUARDED hits %d — disjoint from the GUARDED list (services/api-gateway/src/ + its package.json / vitest.config.ts / vitest.setup.ts / tsconfig.json, packages/shared/src/, eslint.config.mjs); %s" % (pinned, cur, c["ahead_by"], len(files), len(hits), tail)); sys.exit(0)\n'
REPL = [
 ('header', HEADER_OLD, HEADER_NEW, 1),
 ('brief var', 'BRIEF="${QA1032_BRIEF:-$WED/2_Project_Files/fleet/qa-agent/briefs/2026-09-17_secuura-1032-ks1194-tier1.md}"', 'BRIEF="${QA1034_BRIEF:-$WED/2_Project_Files/fleet/qa-agent/briefs/2026-09-17_secuura-1034-ks1215-tier1.md}"', 1),
 ('prompt var', 'PROMPT_FILE="${QA1032_PROMPT:-$WED/2_Project_Files/fleet/qa-agent/briefs/2026-09-17_secuura-1032-ks1194-tier1.prompt.txt}"', 'PROMPT_FILE="${QA1034_PROMPT:-$WED/2_Project_Files/fleet/qa-agent/briefs/2026-09-17_secuura-1034-ks1215-tier1.prompt.txt}"', 1),
 ('branch', "BRANCH='refs/heads/feature/ks-1194-auth-verification-requests-a-failed-save-still-answers-200-a'", "BRANCH='refs/heads/feature/ks-1215-api-gateway-a-revoked-session-jwt-plus-a-valid-key-whose'", 1),
 ('head var', 'HEAD_SHA="${QA1032_HEAD:-70ee7b6c03eeb7ef0609d6fc8fa5223e3647c039}"', 'HEAD_SHA="${QA1034_HEAD:-' + H + '}"', 1),
 ('merge-base', "MERGE_BASE='0a2b1603fe52f0f3b8152588af78bbeab0237be7'   # the merge-base of the head with develop (#1028s squash), the second parent of the head merge 70ee7b6c0",
  "MERGE_BASE='" + MB + "'   # the merge-base of the head with develop (#1029s squash), the second parent of the head merge fd81a75f0", 1),
 ('develop', "DEVELOP_SHA='0a2b1603fe52f0f3b8152588af78bbeab0237be7'   # the pin = the merge-base; develop was bb848b828 at draft close (moves judged by PATH BLOB and GUARDED paths, never by this SHA: git ls-remote 22:26:54 + 22:30:34; compare API 22:26:54 AEST)",
  "DEVELOP_SHA='" + MB + "'   # the pin = the merge-base = develop at drafting (moves judged by PATH BLOB and GUARDED paths, never by this SHA: git ls-remote 23:03:08 + 23:08:34; compare API 23:04:04 AEST)", 1),
 ('report dirs', "REPORT_DIR='" + OLD_REPORT + "'\nPRIOR_REPORT='" + OLD_PRIOR + "'\n", "REPORT_DIR='" + REPORT_DIR + "'\nPRIOR_REPORT='" + PRIOR + "'\n", 1),
 ('real brief', 'REAL_BRIEF="$WED/2_Project_Files/fleet/qa-agent/briefs/2026-09-17_secuura-1032-ks1194-tier1.md"', 'REAL_BRIEF="$WED/2_Project_Files/fleet/qa-agent/briefs/2026-09-17_secuura-1034-ks1215-tier1.md"', 1),
 ('head refuse', 'REFUSING: #1032 — $HEAD_SHA', 'REFUSING: #1034 — $HEAD_SHA', 1),
 ('compare comment', '# develop...#1032 = 0a2b1603f ahead 4 files 2 (behind 1 at draft close: develop bb848b828; behind deliberately not asserted).', '# develop...#1034 = 27e53ec3a ahead 2 files 2 (behind 0 at draft close; behind deliberately not asserted).', 1),
 ('compare assert', '''[ "$COMPARE" = "$MERGE_BASE ahead=4 files=2" ] || { echo "REFUSING: #1032 develop...head reads '$COMPARE', brief pins '$MERGE_BASE ahead=4 files=2'" >&2; exit 10; }''',
                    '''[ "$COMPARE" = "$MERGE_BASE ahead=2 files=2" ] || { echo "REFUSING: #1034 develop...head reads '$COMPARE', brief pins '$MERGE_BASE ahead=2 files=2'" >&2; exit 10; }''', 1),
 ('cur dev', 'CUR_DEV="${QA1032_CUR_DEV:-', 'CUR_DEV="${QA1034_CUR_DEV:-', 1),
 ('develop comment 2', '# The develop pin, judged by CONTENT (see the header): nineteen files by PATH BLOB at the CURRENT develop (no region judgement), then',
                       '# The develop pin, judged by CONTENT (see the header): twenty-four files by PATH BLOB at the CURRENT develop (no region judgement), then', 1),
 ('judged', JUDGED_OLD, JUDGED_NEW, 1),
 ('fixture env', '    fixture = os.environ.get("QA1032_USERS_FILE", "") if f == USERS else ""\n', '    fixture = os.environ.get("QA1034_AUTH_FILE", "") if f == AUTHTS else ""\n', 1),
 ('landed msg', '" — #1032 has landed; this brief is stale"', '" — #1034 has landed; this brief is stale"', 1),
 ('ok pinned', '" (= the head merge-base, an ANCESTOR of the head: merged tree = the head tree 1111602c4ef8a8ca08b3f500ee241ec5fc1c0577; git ls-remote)"',
               '" (= the head merge-base, an ANCESTOR of the head: merged tree = the head tree ' + HT + '; git ls-remote)"', 1),
 ('guarded', GUARD_OLD, GUARD_NEW, 1),
 ('tail', 'tail = "the gate merges the then-current develop onto 70ee7b6c0 in its own clone, asserts the merged services/auth/src and shared subtrees equal the head, or re-runs the fail-closed census, the tamper table and the suites on the MERGED tree; names the merged-tree OID, drafter bb848b828 -> beee976dd (brief items 1, 4, 5, 6)"',
          'tail = "the gate merges the then-current develop onto fd81a75f0 in its own clone, asserts the merged services/api-gateway/src and shared subtrees equal the head, or re-runs the real-gateway matrix, the tamper table and the suites on the MERGED tree; names the merged-tree OID, drafter 27e53ec3a -> ' + HT[:9] + ' = the head tree (brief items 1, 3, 5, 6)"', 1),
 ('ok moved line', OKLINE_OLD, OKLINE_NEW, 1),
 ('subject', '''grep -qF '[QA -> Wednesday] TIER 1 GATE #1032 (KS-1194) 70ee7b6c0' "$PROMPT_FILE"''', '''grep -qF '[QA -> Wednesday] TIER 1 GATE #1034 (KS-1215) fd81a75f0' "$PROMPT_FILE"''', 1),
 ('subject msg', 'REFUSING: prompt does not carry the exact #1032 verdict subject', 'REFUSING: prompt does not carry the exact #1034 verdict subject', 1),
 ('exit24 msg', 'and the PRIOR REPORT $PRIOR_REPORT (#1015, KS-1018: its F5 is this ticket), or the prompt does not name NOT-TESTED.written-first.md — the QA agent has no inbox',
                'and the PRIOR REPORT $PRIOR_REPORT (#1023, KS-1207: its N-1 is this ticket), or the prompt does not name NOT-TESTED.written-first.md — the QA agent has no inbox', 1),
 ('check head', 'echo "  head on origin: #1032 $HEAD_SHA at $BRANCH"', 'echo "  head on origin: #1034 $HEAD_SHA at $BRANCH"', 1),
 ('check compare', 'echo "  compare (GitHub API): develop...#1032 = $COMPARE"', 'echo "  compare (GitHub API): develop...#1034 = $COMPARE"', 1),
 ('check subject', 'echo "  prompt carries the exact #1032 verdict subject, coagent@ sender, wednesday-agent@ recipient"\n  echo "  brief and prompt name the report directory and the #1015 PRIOR REPORT (KS-1018 F5); prompt names NOT-TESTED.written-first.md"\n',
                   'echo "  prompt carries the exact #1034 verdict subject, coagent@ sender, wednesday-agent@ recipient"\n  echo "  brief and prompt name the report directory and the #1023 PRIOR REPORT (KS-1207 N-1); prompt names NOT-TESTED.written-first.md"\n', 1),
 ('check fixture echo', '  [ -n "${QA1032_CUR_DEV:-}" ] && echo "  (develop read from the QA1032_CUR_DEV test override, not ls-remote)"\n  [ -n "${QA1032_USERS_FILE:-}" ] && echo "  (develop auth routes/users.ts read from the QA1032_USERS_FILE fixture, not the contents API)"\n',
  '  [ -n "${QA1034_CUR_DEV:-}" ] && echo "  (develop read from the QA1034_CUR_DEV test override, not ls-remote)"\n  [ -n "${QA1034_AUTH_FILE:-}" ] && echo "  (develop api-gateway middleware/auth.ts read from the QA1034_AUTH_FILE fixture, not the contents API)"\n', 1),
 ('exit16 fixture', '[ -z "${QA1032_BRIEF:-}${QA1032_PROMPT:-}${QA1032_HEAD:-}${QA1032_CUR_DEV:-}${QA1032_USERS_FILE:-}" ]', '[ -z "${QA1034_BRIEF:-}${QA1034_PROMPT:-}${QA1034_HEAD:-}${QA1034_CUR_DEV:-}${QA1034_AUTH_FILE:-}" ]', 1),
]
badn = 0
for label, old, new, want in REPL:
    n = s.count(old)
    if n != want: print('ANCHOR COUNT', label, n, '!=', want); badn += 1; continue
    s = s.replace(old, new); print('  ok', label, n)
if badn: print('REFUSING: %d anchors disagreed; nothing written' % badn); sys.exit(1)
BODY = s.replace(HEADER_NEW, '')
RESID = ['QA1032_', '70ee7b6c0', '0a2b1603f', '1111602c4', 'KS-1194', '#1032', 'ks1194', 'users.ts', 'USERS', 'services/auth', 'secuura-1032', 'bb848b828', 'beee976dd',
         '#1015', 'KS-1018', 'nineteen', 'docs/openapi', 'auth.openapi', 'userRepo', 'fail-closed census']
res = {t: BODY.count(t) for t in RESID if t in BODY}
if res: print('REFUSING: residual tokens in the body', res, [l[:120] for l in BODY.splitlines() if any(t in l for t in res)][:6]); sys.exit(2)
CTL = {H: 2, MB: 2, HT: 1, REPORT_DIR: 1, PRIOR: 1, '"$PRIOR_REPORT"': 2, 'ahead=2 files=2': 2, 'QA1034_AUTH_FILE': 5, 'QA1034_CUR_DEV': 5,
       ': DV}': 24, "grep -q 'ROUND 1'": 2, 'content_cleared': 2, 'DEV_CONTENT_ALLOWED = {}': 1, '#1034 own': 2,
       'CLOSED / STILL OPEN / NEW': None, 'MERGE ADDENDUM': None, 'NOT-TESTED.written-first.md': None, 'exit 19': None, 'exit 21': None, 'exit 22': None,
       'exit 23': None, 'exit 24': None, 'exit 25': None, 'exit 16': None, '[QA -> Wednesday] TIER 1 GATE #1034 (KS-1215) fd81a75f0': 1, 'packages/shared/src/': None,
       'briefs/2026-09-17_secuura-1034-ks1215-tier1.md': 2, 'briefs/2026-09-17_secuura-1034-ks1215-tier1.prompt.txt': 1, '[ -t 0 ]': 1,
       'exec claude --dangerously-skip-permissions --model opus': 1, 'A + "vitest.setup.ts"': 2, 'D + "packages/shared/src/utils/gracefulShutdown.ts"': 1, 'A + "src/routes/platform.ts"': 1}
got = {k: s.count(k) for k in CTL}
print('output controls', {(k[:24] + '…' if len(k) > 24 else k): v for k, v in got.items()})
for k, v in CTL.items():
    if (v is not None and got[k] != v) or got[k] == 0: print('CONTROL DISAGREED', k, got[k], v); sys.exit(1)
for pth, b_ in list(PIN.items()) + list(LANDED.items()):
    if s.count(b_) != 1: print('CONTROL DISAGREED pin', pth, s.count(b_)); sys.exit(1)
for tag in ("<<'PY'\n", "<<'PYJ'\n"):
    i = s.index(tag); j = s.index('\nPY' + ('J' if 'PYJ' in tag else '') + '\n', i); blk = s[i:j]
    print('heredoc', tag.strip(), 'apostrophes', blk.count("'") - 2, 'parens (', blk.count('('), ')', blk.count(')'))
    if (blk.count("'") - 2) % 2 or blk.count('(') != blk.count(')'): print('REFUSING: heredoc parity'); sys.exit(1)
if re.search(r'git -C "\$REPO" (fetch|push|checkout|merge|reset|worktree|commit|switch|pull)\b', s): print('REFUSING: git write verb'); sys.exit(1)
if re.search(r'[\x00-\x08\x0b\x0c\x0e-\x1f]', s): print('REFUSING: control bytes'); sys.exit(1)
tmp = OUT + '.gen-tmp'; open(tmp, 'w').write(s)
p = subprocess.run(['bash', '-n', tmp], capture_output=True, text=True); print('bash -n rc', p.returncode, p.stderr.strip()[:300])
if p.returncode: print('REFUSING: bash -n; the tmp file is left for reading at', tmp); sys.exit(3)
if os.path.exists(OUT):
    pre = OUT + '.pre-' + now('+%H%M%S'); shutil.copyfile(OUT, pre); print('existing output copied to', pre)
os.replace(tmp, OUT); os.chmod(OUT, 0o755)
print('written', OUT, 'mode', oct(os.stat(OUT).st_mode & 0o777), 'sha256', hashlib.sha256(open(OUT, 'rb').read()).hexdigest()[:16], 'lines', s.count('\n'))
