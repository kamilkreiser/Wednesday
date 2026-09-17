#!/usr/bin/env python3
"""gen_launcher_1032.py — derive launchers/launch_qa_secuura_ks1194_1032.sh from launchers/launch_qa_secuura_ks1213_1031.sh (the latest generated launcher: same
guard set, blob-judged develop arm, GUARDED compare arm) by ASSERTED substitutions: every anchor must occur exactly as often as stated, or the generator refuses and
writes nothing. Shape follows gen_launcher_1031.py (pins re-read from the repo, tmp file, bash -n on the tmp, then os.replace; .pre-* copy if the output exists).
Re-points at #1032 (KS-1194) ROUND 1: head 70ee7b6c0; the pinned develop 0a2b1603f is the head's second parent AND merge-base; develop had MOVED to bb848b828
(KS-1211 lock bumps, 0 GUARDED) at drafting, so compare develop...head = merge_base 0a2b1603f ahead 4 files 2 (diverged; behind NOT asserted). The develop arm
judges NINETEEN auth / shared / spec / lint files by PATH BLOB at the CURRENT develop — never by develop's SHA (users.ts c723a68af, the ks1194 test ABSENT; at
their #1032 blobs -> exit 19 LANDED). On a develop move the compare pinned...current REFUSES (exit 18) when it touches services/auth/src/ or its package.json /
vitest.config.ts / vitest.setup.ts / tsconfig.json, packages/shared/src/, docs/openapi/ or eslint.config.mjs. DEV_CONTENT_ALLOWED is EMPTY (no lockfile is
guarded: the gate farms node_modules from the checkout install). Test fixture QA1032_USERS_FILE stands in for develop users.ts (content and git blob).
Residual guard, output controls, heredoc parity, no git write verb, no control bytes, bash -n.
Usage: gen_launcher_1032.py <template launcher> <output launcher>   Exit: 0 written · 1 anchor/control disagreed · 2 residual token · 3 bash -n failed"""
import hashlib, os, re, shutil, subprocess, sys
TPL, OUT = sys.argv[1], sys.argv[2]
s = open(TPL).read()
def now(f='+%Y-%m-%d %H:%M:%S %Z'): return subprocess.run(['date', f], capture_output=True, text=True).stdout.strip()
print('gen_launcher_1032', now(), '| template sha256', hashlib.sha256(s.encode()).hexdigest()[:16], 'lines', s.count('\n'))
REPO = '/Volumes/DevMASTER/!CODING/Secuura/Blockchain/2_Project_Files'
H = '70ee7b6c03eeb7ef0609d6fc8fa5223e3647c039'; MB = '0a2b1603fe52f0f3b8152588af78bbeab0237be7'; FIX = '00236c10bc9c237e64e008f6bb927c816a8bb29c'
HT = '1111602c4ef8a8ca08b3f500ee241ec5fc1c0577'; NEWDEV = 'bb848b8283eb5ee6a6180067315b76f1321e7b6b'; MERGED = 'beee976ddcd75978e7b99f49cc175c85f7abfdb1'
D = 'Blockchain/Dev/'; A = 'services/auth/'
rp = lambda x: subprocess.run(['git', '-C', REPO, 'rev-parse', '--verify', '-q', x], capture_output=True, text=True).stdout.strip()
T1194 = A + 'src/__tests__/ks1194-a-failed-verification-request-save-is-never-acknowledged.test.ts'
PIN = {  # path relative to Blockchain/Dev -> blob at develop 0a2b1603f (develop-OK); re-read and asserted below (and equal at bb848b828: 0 of these moved)
 A + 'src/routes/users.ts': 'c723a68afe3005c22a2c74e95f07d93647a17dae',
 A + 'src/repositories/userRepo.ts': '9060b308e6d6a82c8a79be7387032d2a18c4ac22',
 A + 'src/repositories/dbErrors.ts': 'f94faf0d3d3540990f8626fcb65c746737202ac4',
 A + 'src/middleware/errorHandler.ts': '1cf66e74cd2bbe1d56f53c6f7ef5200e1835ee3c',
 A + 'src/db.ts': 'cf0ee130bb5228214a41e163b3be766b8aebbb72',
 A + 'src/types/index.ts': '9b0b4f08afbf3244f6a28b374dd302786a75aab3',
 A + 'src/index.ts': 'edabbf87182311241662b20ac71d7244e923b5a3',
 A + 'src/__tests__/ks1018-security-correctness-three-verification-store-reads.test.ts': '6723276d016e4d6cf4ead8cb4f511ce5dad5ce53',
 A + 'src/__tests__/ks1050-profile-update-zero-rows-is-not-success.test.ts': 'ffb3e801ab371bed4a11accd0dbcc64bd8fdc804',
 A + 'src/__tests__/ks949-platform-admin-seed-identity.test.ts': '4f03e6f4f132bc7a8f3c3577684f6eef3bf8ce03',
 A + 'src/auth.openapi.ts': '2c356c3c7877add99f5e1a3c437d04ac8be3dc76',
 A + 'package.json': '814e88419470b811f26f1593984071bb317608d8',
 A + 'vitest.config.ts': '8bb96293a0f11a14d90e7c7893f32a053277bbdb',
 A + 'vitest.setup.ts': 'bc18c18755cb00f96e3e228ca34d99fd1266c20f',
 A + 'tsconfig.json': 'a7952bdeaf16e933432bb0e7136f484bb7288a40',
 'packages/shared/src/db/tenant-guc.ts': '86953b978062eb1d124abf3154fa1da324c6e110',
 'docs/openapi/secuura-api.yaml': '122d3a2f84cf77bf2b7e2dc51489a0d5f823db1f',
 'eslint.config.mjs': '8c5374c6022eb0a3f449f41a570db61294aa63f1',
}
LANDED = {A + 'src/routes/users.ts': '8299a25586c8484d30da22430cfdc014c0b33785', T1194: 'bc8f924c39ee46d23b48d8bfbfd90e1f886ced86'}
bad = []
for p, b in PIN.items():
    at_mb, at_h, at_nd = rp(MB + ':' + D + p), rp(H + ':' + D + p), rp(NEWDEV + ':' + D + p)
    if at_mb != b: bad.append(('develop blob', p, b, at_mb))
    if at_nd != b: bad.append(('moved develop bb848b828 blob differs', p, b, at_nd))
    if p not in LANDED and at_h != b: bad.append(('head blob differs for an untouched file', p, b, at_h))
for p, b in LANDED.items():
    if rp(H + ':' + D + p) != b or rp(FIX + ':' + D + p) != (b if p == T1194 else rp(FIX + ':' + D + p)): bad.append(('landed blob', p, b, rp(H + ':' + D + p)))
if rp(H + '^{tree}') != HT: bad.append(('head tree', rp(H + '^{tree}')))
if rp(H + '^2') != MB: bad.append(('head second parent', rp(H + '^2')))
p = subprocess.run(['git', '-C', REPO, 'cat-file', '-e', MB + ':' + D + T1194], capture_output=True); print('ks1194 test ABSENT at develop (cat-file -e rc != 0):', p.returncode != 0)
if p.returncode == 0: bad.append(('ks1194 test present at develop',))
p2 = subprocess.run(['git', '-C', REPO, 'cat-file', '-e', NEWDEV + ':' + D + T1194], capture_output=True); print('ks1194 test ABSENT at moved develop bb848b828:', p2.returncode != 0)
if p2.returncode == 0: bad.append(('ks1194 test present at bb848b828',))
print('pinned blobs re-read from the repo (develop 0a2b1603f = bb848b828 for all %d; head = develop for the %d untouched; the 2 PR files at head):' % (len(PIN), len(PIN) - 1), 'OK' if not bad else bad)
if bad: print('REFUSING: pins disagree with the repo; nothing written'); sys.exit(1)
def cut(start, end_incl):
    assert s.count(start) == 1, ('cut start', start[:60], s.count(start))
    i = s.index(start); j = s.index(end_incl, i) + len(end_incl); return s[i:j]
REPORT_DIR = '/Volumes/DevMASTER/!CODING/Testing Agent MAIN/projects/secuura/reports/2026-09-17-ks1194-1032-70ee7b6c0-tier1-r1/'
PRIOR = '/Volumes/DevMASTER/!CODING/Testing Agent MAIN/projects/secuura/reports/2026-09-17-ks1018-1015-77145ce84-tier1-r1/'
OLD_REPORT = '/Volumes/DevMASTER/!CODING/Testing Agent MAIN/projects/secuura/reports/2026-09-17-ks1213-1031-be8596a29-tier1-r1/'
OLD_PRIOR = '/Volumes/DevMASTER/!CODING/Testing Agent MAIN/projects/secuura/reports/2026-09-17-ks1202-1024-d1a328088-tier1-r1/'
assert os.path.isdir(PRIOR), 'prior report dir missing'
HEADER_OLD = cut('# launch_qa_secuura_ks1213_1031.sh', "# Exit: 0 launched (or guards passed under --check) · 2..25 a guard refused\n")
HEADER_NEW = """# launch_qa_secuura_ks1194_1032.sh — cross-project QA agent, ONE TIER 1 ROUND 1 gate over Secuura/Blockchain PR #1032 (KS-1194, Seat A)
# @ 70ee7b6c03eeb7ef0609d6fc8fa5223e3647c039 — services/auth: a verification-request save that did not persist is never acknowledged. saveVerificationRequest
# writes the row first and sets memory only after it lands (infrastructure -> 503, anything else rethrown -> 500); the review's approve saves the APPROVED row
# BEFORE updateUserPlatformScope, and a level update that throws or answers null restores PENDING and answers 503. The change commit 00236c10b (parent d7e95cd9f):
# routes/users.ts +67 -31, the ks1194 test +219 (11 cells). 70ee7b6c0 = the third develop merge (0a2b1603f) into the branch; tree 1111602c4 = merge-tree
# c82f5edd5 x 0a2b1603f in the drafter clone; each of the three merges equals merge-tree of its own parents and brought exactly develop's own delta.
# TIER 1: the verification level is an assurance level other services gate on (#1015 gate F5; Kam ruled fail-closed). A GO is NOT a merge authorisation:
# the merge waits for Kam's tap.
#
# THE SHAPE, as read 22:13-22:30 AEST 2026-09-17 (git ls-remote + the PR, compare and contents APIs agree): develop 0a2b1603f is the head merge-base AND its
# second parent; develop MOVED to bb848b828 during drafting (KS-1211 vitest lock bumps, 43 files, 0 GUARDED), so compare develop...head = merge_base 0a2b1603f,
# diverged, ahead 4, files 2 (asserted, exit 10; behind NOT asserted). Drafter merged tree 70ee7b6c0 x bb848b828 = beee976dd.
#
# The develop pin is judged by CONTENT — PATH BLOBS — never by develop's SHA: (a) NINETEEN files by blob at the CURRENT develop — the PR two (auth routes/users.ts
# c723a68af, the ks1194 test ABSENT; at a #1032 blob -> exit 19 LANDED), and what the gate runs and reads: repositories/userRepo.ts (updateUser,
# updateUserPlatformScope, updateUserOrThrow) and dbErrors.ts, middleware/errorHandler.ts, db.ts, types/index.ts, index.ts, the ks1018 / ks1050 / ks949 tests,
# auth.openapi.ts, auth package.json / vitest.config.ts / vitest.setup.ts / tsconfig.json, shared db/tenant-guc.ts, docs/openapi/secuura-api.yaml, Dev
# eslint.config.mjs — any blob nobody pinned -> exit 18; (b) if develop moved past 0a2b1603f, the compare pinned...develop REFUSES (exit 18) when the delta
# touches a GUARDED path — services/auth/src/ and its package.json / vitest.config.ts / vitest.setup.ts / tsconfig.json, packages/shared/src/, docs/openapi/,
# eslint.config.mjs — or the move cannot be judged. WHY these paths: they are the code and configuration the gate runs in-process (auth routes, repositories,
# error handler, the shared scope helpers the repo imports) and the spec it reads; a develop merge elsewhere (other services, frontends, audit baselines,
# lockfiles: the gate farms node_modules from the checkout install) cannot change what the gate measures, so it must not refuse. DEV_CONTENT_ALLOWED is EMPTY.
# Open PRs #575, #649 and #948 edit auth package.json: if one lands first this REFUSES by design — re-pin deliberately.
#
# exit 21: the LAUNCH path refuses when stdin is not a TTY. This launcher execs an interactive agent; run it in a cockpit
# pane, never inside a Bash tool — and never run it without --check to "prove" this guard. `--check` runs headless (it launches nothing).
# exit 22: the prompt must require node_modules farmed PER ENTRY (the #1009 gate R-6: a wholesale link can write through to the checkout .vite).
# exit 23: the prompt must carry the exact #1032 verdict subject and name coagent@ as the sender and wednesday-agent@ as the recipient.
# exit 24: brief AND prompt must name the REPORT DIRECTORY and the PRIOR REPORT (#1015, KS-1018: its F5 is this ticket; the QA agent has no inbox), and the
#          prompt must name NOT-TESTED.written-first.md (written FIRST, before any run).
# exit 25: brief AND prompt must carry the MERGE ADDENDUM and require the per-finding CLOSED / STILL OPEN / NEW disposition.
# QA1032_CUR_DEV (test override, --check only): stands in for origin develop so the LANDED / GUARDED refusals can be proven.
# QA1032_USERS_FILE (test fixture, --check only): a local file stands in for develop auth routes/users.ts (its git blob) so the LANDED and GUARDED
# arms can be proven without a real develop commit.
# A launch with any QA1032_* override or fixture set refuses (exit 16).
#
# Generated by gatesets/2026-09-17_gate1032/gen_launcher_1032.py from launch_qa_secuura_ks1213_1031.sh (asserted substitutions + pins re-read from the repo +
# residual guard + output controls + bash -n): same guard set and exit codes 2..25 (19 = LANDED), re-pointed at #1032 ROUND 1, no content-cleared blob.
#
# Usage: launch_qa_secuura_ks1194_1032.sh [--check]
# Exit: 0 launched (or guards passed under --check) · 2..25 a guard refused
"""
JUDGED_OLD = cut('O = D + "services/originate/"\n', 'content_cleared = set()\n')
def key(p_):
    return ('A + "' + p_[len(A):] + '"') if p_.startswith(A) else ('D + "' + p_ + '"')
rows = ['  USERS:' + ' ' * 64 + '({"' + PIN[A + 'src/routes/users.ts'] + '": DV}, {"' + LANDED[A + 'src/routes/users.ts'] + '": "#1032 own"}),',
        '  A + "src/__tests__/ks1194-a-failed-verification-request-save-is-never-acknowledged.test.ts": ({"ABSENT": DV}, {"' + LANDED[T1194] + '": "#1032 own"}),']
for p_, b_ in PIN.items():
    if p_ in LANDED: continue
    k = key(p_); rows.append('  %s:%s({"%s": DV}, {}),' % (k, ' ' * max(1, 70 - len(k)), b_))
JUDGED_NEW = ('A = D + "services/auth/"\nUSERS = A + "src/routes/users.ts"\nDV = "develop"\n'
              '# file -> (develop-OK blobs {blob: label}, LANDED blobs {blob: label}); ABSENT = the contents API answers 404 at develop\nJUDGED = {\n' + '\n'.join(rows) +
              '\n}\n# No REGION judgement: every file is judged by exact blob (a develop move of users.ts or userRepo.ts refuses, exit 18).\ncontent_cleared = set()\n')
DOCS_DEF_OLD = 'DOCS = O + "src/routes/documents.ts"\n'
GUARD_OLD = cut('GUARDED = [O + "src/",\n', 'DEV_CONTENT_ALLOWED = {}\n')
GUARD_NEW = '''GUARDED = [A + "src/",
           A + "package.json",
           A + "vitest.config.ts",
           A + "vitest.setup.ts",
           A + "tsconfig.json",
           D + "packages/shared/src/",
           D + "docs/openapi/",
           D + "eslint.config.mjs"]
# STYLE NOTE (912r2 launcher, measured): bash scans quote/paren state THROUGH this heredoc because it sits inside a
# command substitution — keep apostrophes and parentheses EVEN (this block uses none of the former), or the outer $( ) breaks.
# CONTENT-JUDGED allowlist: EMPTY. No lockfile is guarded: the gate farms node_modules from the checkout install. Re-pin deliberately.
DEV_CONTENT_ALLOWED = {}
'''
OKLINE_OLD = cut('print("OK " + state + " | origin develop MOVED %s -> %s', 'sys.exit(0)\n')
OKLINE_NEW = 'print("OK " + state + " | origin develop MOVED %s -> %s: commits=%d files=%d — GUARDED hits %d — disjoint from the GUARDED list (services/auth/src/ + its package.json / vitest.config.ts / vitest.setup.ts / tsconfig.json, packages/shared/src/, docs/openapi/, eslint.config.mjs); %s" % (pinned, cur, c["ahead_by"], len(files), len(hits), tail)); sys.exit(0)\n'
REPL = [
 ('header', HEADER_OLD, HEADER_NEW, 1),
 ('brief var', 'BRIEF="${QA1031_BRIEF:-$WED/2_Project_Files/fleet/qa-agent/briefs/2026-09-17_secuura-1031-ks1213-tier1.md}"', 'BRIEF="${QA1032_BRIEF:-$WED/2_Project_Files/fleet/qa-agent/briefs/2026-09-17_secuura-1032-ks1194-tier1.md}"', 1),
 ('prompt var', 'PROMPT_FILE="${QA1031_PROMPT:-$WED/2_Project_Files/fleet/qa-agent/briefs/2026-09-17_secuura-1031-ks1213-tier1.prompt.txt}"', 'PROMPT_FILE="${QA1032_PROMPT:-$WED/2_Project_Files/fleet/qa-agent/briefs/2026-09-17_secuura-1032-ks1194-tier1.prompt.txt}"', 1),
 ('branch', "BRANCH='refs/heads/feature/ks-1213-derived-document-writers-still-relabel-the-served-type-post'", "BRANCH='refs/heads/feature/ks-1194-auth-verification-requests-a-failed-save-still-answers-200-a'", 1),
 ('head var', 'HEAD_SHA="${QA1031_HEAD:-be8596a29af15477cb0cbf4b8684e35e63c38e9f}"', 'HEAD_SHA="${QA1032_HEAD:-' + H + '}"', 1),
 ('merge-base', "MERGE_BASE='75ad0e55c6335a5f34f6d0b74dfe00b334b2eb2e'   # the merge-base of the head with develop = develop itself (#1026s squash), the second parent of the head merge be8596a29",
  "MERGE_BASE='" + MB + "'   # the merge-base of the head with develop (#1028s squash), the second parent of the head merge 70ee7b6c0", 1),
 ('develop', "DEVELOP_SHA='75ad0e55c6335a5f34f6d0b74dfe00b334b2eb2e'   # the pin = the merge-base = develop at drafting (moves judged by PATH BLOB and GUARDED paths, never by this SHA: git ls-remote 21:15:12; compare API 21:26:53 AEST)",
  "DEVELOP_SHA='" + MB + "'   # the pin = the merge-base; develop was bb848b828 at draft close (moves judged by PATH BLOB and GUARDED paths, never by this SHA: git ls-remote 22:26:54 + 22:30:34; compare API 22:26:54 AEST)", 1),
 ('report dirs', "REPORT_DIR='" + OLD_REPORT + "'\nPRIOR_REPORT='" + OLD_PRIOR + "'\n", "REPORT_DIR='" + REPORT_DIR + "'\nPRIOR_REPORT='" + PRIOR + "'\n", 1),
 ('real brief', 'REAL_BRIEF="$WED/2_Project_Files/fleet/qa-agent/briefs/2026-09-17_secuura-1031-ks1213-tier1.md"', 'REAL_BRIEF="$WED/2_Project_Files/fleet/qa-agent/briefs/2026-09-17_secuura-1032-ks1194-tier1.md"', 1),
 ('head refuse', 'REFUSING: #1031 — $HEAD_SHA', 'REFUSING: #1032 — $HEAD_SHA', 1),
 ('compare comment', '# develop...#1031 = 75ad0e55c ahead 2 files 3 (behind 0 at draft close; behind deliberately not asserted).', '# develop...#1032 = 0a2b1603f ahead 4 files 2 (behind 1 at draft close: develop bb848b828; behind deliberately not asserted).', 1),
 ('compare assert', '''[ "$COMPARE" = "$MERGE_BASE ahead=2 files=3" ] || { echo "REFUSING: #1031 develop...head reads '$COMPARE', brief pins '$MERGE_BASE ahead=2 files=3'" >&2; exit 10; }''',
                    '''[ "$COMPARE" = "$MERGE_BASE ahead=4 files=2" ] || { echo "REFUSING: #1032 develop...head reads '$COMPARE', brief pins '$MERGE_BASE ahead=4 files=2'" >&2; exit 10; }''', 1),
 ('cur dev', 'CUR_DEV="${QA1031_CUR_DEV:-', 'CUR_DEV="${QA1032_CUR_DEV:-', 1),
 ('develop comment 2', '# The develop pin, judged by CONTENT (see the header): eighteen files by PATH BLOB at the CURRENT develop (no region judgement), then',
                       '# The develop pin, judged by CONTENT (see the header): nineteen files by PATH BLOB at the CURRENT develop (no region judgement), then', 1),
 ('judged', JUDGED_OLD, JUDGED_NEW, 1),
 ('fixture env', '    fixture = os.environ.get("QA1031_DOCS_FILE", "") if f == DOCS else ""\n', '    fixture = os.environ.get("QA1032_USERS_FILE", "") if f == USERS else ""\n', 1),
 ('landed msg', '" — #1031 has landed; this brief is stale"', '" — #1032 has landed; this brief is stale"', 1),
 ('ok pinned', '" (= the head merge-base, an ANCESTOR of the head: merged tree = the head tree 75ed56fb43ee919be4f16671defddacb6168b650; git ls-remote)"',
               '" (= the head merge-base, an ANCESTOR of the head: merged tree = the head tree ' + HT + '; git ls-remote)"', 1),
 ('guarded', GUARD_OLD, GUARD_NEW, 1),
 ('tail', 'tail = "the gate merges the then-current develop onto be8596a29 in its own clone, asserts the merged originate and shared subtrees equal the head, or re-runs the writer contract rows, the tamper table and the suites on the MERGED tree; names the merged-tree OID (brief items 1, 3, 4, 7)"',
          'tail = "the gate merges the then-current develop onto 70ee7b6c0 in its own clone, asserts the merged services/auth/src and shared subtrees equal the head, or re-runs the fail-closed census, the tamper table and the suites on the MERGED tree; names the merged-tree OID, drafter bb848b828 -> ' + MERGED[:9] + ' (brief items 1, 4, 5, 6)"', 1),
 ('ok moved line', OKLINE_OLD, OKLINE_NEW, 1),
 ('subject', '''grep -qF '[QA -> Wednesday] TIER 1 GATE #1031 (KS-1213) be8596a29' "$PROMPT_FILE"''', '''grep -qF '[QA -> Wednesday] TIER 1 GATE #1032 (KS-1194) 70ee7b6c0' "$PROMPT_FILE"''', 1),
 ('subject msg', 'REFUSING: prompt does not carry the exact #1031 verdict subject', 'REFUSING: prompt does not carry the exact #1032 verdict subject', 1),
 ('exit24 msg', 'and the PRIOR REPORT $PRIOR_REPORT (#1024, KS-1202: its N-A is this ticket), or the prompt does not name NOT-TESTED.written-first.md — the QA agent has no inbox',
                'and the PRIOR REPORT $PRIOR_REPORT (#1015, KS-1018: its F5 is this ticket), or the prompt does not name NOT-TESTED.written-first.md — the QA agent has no inbox', 1),
 ('check head', 'echo "  head on origin: #1031 $HEAD_SHA at $BRANCH"', 'echo "  head on origin: #1032 $HEAD_SHA at $BRANCH"', 1),
 ('check compare', 'echo "  compare (GitHub API): develop...#1031 = $COMPARE"', 'echo "  compare (GitHub API): develop...#1032 = $COMPARE"', 1),
 ('check subject', 'echo "  prompt carries the exact #1031 verdict subject, coagent@ sender, wednesday-agent@ recipient"\n  echo "  brief and prompt name the report directory and the #1024 PRIOR REPORT (KS-1202 N-A); prompt names NOT-TESTED.written-first.md"\n',
                   'echo "  prompt carries the exact #1032 verdict subject, coagent@ sender, wednesday-agent@ recipient"\n  echo "  brief and prompt name the report directory and the #1015 PRIOR REPORT (KS-1018 F5); prompt names NOT-TESTED.written-first.md"\n', 1),
 ('check fixture echo', '  [ -n "${QA1031_CUR_DEV:-}" ] && echo "  (develop read from the QA1031_CUR_DEV test override, not ls-remote)"\n  [ -n "${QA1031_DOCS_FILE:-}" ] && echo "  (develop originate routes/documents.ts read from the QA1031_DOCS_FILE fixture, not the contents API)"\n',
  '  [ -n "${QA1032_CUR_DEV:-}" ] && echo "  (develop read from the QA1032_CUR_DEV test override, not ls-remote)"\n  [ -n "${QA1032_USERS_FILE:-}" ] && echo "  (develop auth routes/users.ts read from the QA1032_USERS_FILE fixture, not the contents API)"\n', 1),
 ('exit16 fixture', '[ -z "${QA1031_BRIEF:-}${QA1031_PROMPT:-}${QA1031_HEAD:-}${QA1031_CUR_DEV:-}${QA1031_DOCS_FILE:-}" ]', '[ -z "${QA1032_BRIEF:-}${QA1032_PROMPT:-}${QA1032_HEAD:-}${QA1032_CUR_DEV:-}${QA1032_USERS_FILE:-}" ]', 1),
]
badn = 0
for label, old, new, want in REPL:
    n = s.count(old)
    if n != want: print('ANCHOR COUNT', label, n, '!=', want); badn += 1; continue
    s = s.replace(old, new); print('  ok', label, n)
if badn: print('REFUSING: %d anchors disagreed; nothing written' % badn); sys.exit(1)
BODY = s.replace(HEADER_NEW, '')
RESID = ['QA1031_', 'be8596a29', '75ad0e55c', '75ed56fb4', 'KS-1213', '#1031', 'ks1213', 'originate', 'DOCS', '450e3429d', 'secuura-1031', 'de9b5ae25', '#1024', 'eighteen',
         '#995', 'O + "', 'documents.ts', 'certification', 'KS-1202']
res = {t: BODY.count(t) for t in RESID if t in BODY}
if res: print('REFUSING: residual tokens in the body', res, [l[:120] for l in BODY.splitlines() if any(t in l for t in res)][:6]); sys.exit(2)
CTL = {H: 2, MB: 2, HT: 1, REPORT_DIR: 1, PRIOR: 1, '"$PRIOR_REPORT"': 2, 'ahead=4 files=2': 2, 'QA1032_USERS_FILE': 5, 'QA1032_CUR_DEV': 5,
       ': DV}': 19, "grep -q 'ROUND 1'": 2, 'content_cleared': 2, 'DEV_CONTENT_ALLOWED = {}': 1, '#1032 own': 2,
       'CLOSED / STILL OPEN / NEW': None, 'MERGE ADDENDUM': None, 'NOT-TESTED.written-first.md': None, 'exit 19': None, 'exit 21': None, 'exit 22': None,
       'exit 23': None, 'exit 24': None, 'exit 25': None, 'exit 16': None, '[QA -> Wednesday] TIER 1 GATE #1032 (KS-1194) 70ee7b6c0': 1, 'packages/shared/src/': None,
       'briefs/2026-09-17_secuura-1032-ks1194-tier1.md': 2, 'briefs/2026-09-17_secuura-1032-ks1194-tier1.prompt.txt': 1, '[ -t 0 ]': 1,
       'exec claude --dangerously-skip-permissions --model opus': 1, 'A + "vitest.setup.ts"': 2}
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
