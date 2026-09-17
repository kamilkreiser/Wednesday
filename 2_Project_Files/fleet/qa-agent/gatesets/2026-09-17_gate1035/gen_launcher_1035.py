#!/usr/bin/env python3
"""gen_launcher_1035.py — derive launchers/launch_qa_secuura_ks1204_1035.sh from launchers/launch_qa_secuura_ks1215_1034.sh (same guard set, blob-judged develop arm,
GUARDED compare arm) by ASSERTED substitutions: every anchor must occur exactly as often as stated, or nothing is written. Shape: gen_launcher_1034.py (pins re-read
from the repo, tmp file, bash -n on the tmp, then os.replace; a .pre-* copy if the output exists).
Re-points at #1035 (KS-1204) ROUND 1: head 4b1fb0621 = ONE commit on 732c13459 (its only parent = the merge-base = develop when the seat pushed). Develop is now
3961c2add (#1033: lockfiles, audit baseline, originate), so compare develop...head = merge_base 732c13459, ahead 1, files 2 (behind NOT asserted).
The develop arm judges NINETEEN files by PATH BLOB at the CURRENT develop (verification.ts 28fb58343, the ks1204 test ABSENT; at their #1035 blobs -> exit 19
LANDED). On a develop move the compare pinned...current REFUSES (exit 18) when it touches services/api-gateway/src/ or its package.json / vitest.config.ts /
vitest.setup.ts / tsconfig.json, packages/shared/src/, eslint.config.mjs, frontend/admin/src/pages/Settings.tsx (the probe transcribes its save), or the two
mcp-server readers. DEV_CONTENT_ALLOWED is EMPTY. Test fixture QA1035_VER_FILE stands in for develop verification.ts (content and git blob).
Usage: gen_launcher_1035.py <template launcher> <output launcher>   Exit: 0 written · 1 anchor/control disagreed · 2 residual token · 3 bash -n failed"""
import hashlib, os, re, shutil, subprocess, sys
TPL, OUT = sys.argv[1], sys.argv[2]
s = open(TPL).read()
def now(f='+%Y-%m-%d %H:%M:%S %Z'): return subprocess.run(['date', f], capture_output=True, text=True).stdout.strip()
print('gen_launcher_1035', now(), '| template sha256', hashlib.sha256(s.encode()).hexdigest()[:16], 'lines', s.count('\n'))
REPO = '/Volumes/DevMASTER/!CODING/Secuura/Blockchain/2_Project_Files'
H = '4b1fb0621e58ff00bba096751130bc6e53df4714'; MB = '732c13459d76f5b05ade94bb91de7e47585b0e7d'; CURDEV = '3961c2add8e1637b32e638f8f0952c328c00833e'
HT = 'cad39d37d4fd15b44ff2d095f810813662ae6208'; MERGED = 'd21341805c976676a417755032ba781a7b6da3b7'
D = 'Blockchain/Dev/'; A = 'services/api-gateway/'
rp = lambda x: subprocess.run(['git', '-C', REPO, 'rev-parse', '--verify', '-q', x], capture_output=True, text=True).stdout.strip()
VER = A + 'src/routes/verification.ts'
T1204 = A + 'src/__tests__/ks1204-a-non-array-allow-list-fails-closed-and-documenttype-wins.test.ts'
PIN = {  # path relative to Blockchain/Dev -> blob at develop 732c13459 (= 3961c2add for every one; asserted below)
 VER: '28fb5834308a502f5f7b806e3b49a77627601eff',
 A + 'src/index.ts': 'db127dbfa5dd899b0a8e0d844690890d91e27f10',
 A + 'src/routes/admin.ts': 'f47dd6a655702ffbfc402ca920a33c4619d62c4b',
 A + 'src/services/health.ts': 'f43052734a10d0b891db11b49aa49b08f66c1ea8',
 A + 'src/services/redis.ts': '47659ee9c9f06acf9ac64e09b2dc207113ba92ea',
 A + 'src/services/enforcement.ts': 'be466fbf444178bbb41293fb1d811957e55e1d2d',
 A + 'src/middleware/auth.ts': None,
 A + 'src/middleware/contentType.ts': None,
 A + 'src/__tests__/ks1176-connector-key-level-ranks-as-none.test.ts': '43cebf8d75376f5a40252c5096fd02747c4f0a9e',
 A + 'package.json': '841d8c6adcd71e885c01e65c22da9418daff276a',
 A + 'vitest.config.ts': '5888e0b320d934f6f434e0e5ca3c74a995cecc02',
 A + 'vitest.setup.ts': '22c1107683b8192df3bfd3e929aa94aff3dc7d45',
 A + 'tsconfig.json': 'c981e6a92fdd2417fa35070eb979c5f1c77ffbcd',
 'packages/shared/src/utils/gracefulShutdown.ts': '5550416464de399e86f6c4041a3279962119af82',
 'frontend/admin/src/pages/Settings.tsx': None,
 'services/mcp-server/src/tools/info.ts': None,
 'services/mcp-server/src/package-generator.ts': None,
 'eslint.config.mjs': '8c5374c6022eb0a3f449f41a570db61294aa63f1',
}
for p in list(PIN):
    if PIN[p] is None: PIN[p] = rp(MB + ':' + D + p); print('  pin read from the repo (732c13459):', p, PIN[p][:9])
LANDED = {VER: 'f888e8cd0bd10c98a508542d75902ab122595157', T1204: 'f1f9840edd15ba8cbb764f675f5c2fdeef228dc7'}
bad = []
for p, b in PIN.items():
    at_mb, at_cur, at_h = rp(MB + ':' + D + p), rp(CURDEV + ':' + D + p), rp(H + ':' + D + p)
    if not b or at_mb != b: bad.append(('develop 732c13459 blob', p, b, at_mb))
    if at_cur != b: bad.append(('develop 3961c2add blob', p, b, at_cur))
    if p not in LANDED and at_h != b: bad.append(('head blob differs for an untouched file', p, b, at_h))
for p, b in LANDED.items():
    if rp(H + ':' + D + p) != b: bad.append(('landed blob at head', p, b, rp(H + ':' + D + p)))
if rp(H + '^{tree}') != HT: bad.append(('head tree', rp(H + '^{tree}')))
if rp(H + '^1') != MB: bad.append(('head parent', rp(H + '^1')))
if rp(H + '^2'): bad.append(('head has a second parent', rp(H + '^2')))
p = subprocess.run(['git', '-C', REPO, 'cat-file', '-e', CURDEV + ':' + D + T1204], capture_output=True); print('ks1204 test ABSENT at develop 3961c2add (cat-file -e rc != 0):', p.returncode != 0)
if p.returncode == 0: bad.append(('ks1204 test present at develop',))
print('pinned blobs re-read from the repo (%d files at 732c13459 AND 3961c2add; head = develop for the %d untouched; the 2 PR files at head):' % (len(PIN) + 1, len(PIN) - 1), 'OK' if not bad else bad)
if bad: print('REFUSING: pins disagree with the repo; nothing written'); sys.exit(1)
def cut(start, end_incl):
    assert s.count(start) == 1, ('cut start', start[:60], s.count(start))
    i = s.index(start); j = s.index(end_incl, i) + len(end_incl); return s[i:j]
REPORT_DIR = '/Volumes/DevMASTER/!CODING/Testing Agent MAIN/projects/secuura/reports/2026-09-18-ks1204-1035-4b1fb0621-tier1-r1/'
PRIOR = '/Volumes/DevMASTER/!CODING/Testing Agent MAIN/projects/secuura/reports/2026-09-17-ks1176-1014r2-9ba0caf78-tier1-r2/'
OLD_REPORT = '/Volumes/DevMASTER/!CODING/Testing Agent MAIN/projects/secuura/reports/2026-09-17-ks1215-1034-fd81a75f0-tier1-r1/'
OLD_PRIOR = '/Volumes/DevMASTER/!CODING/Testing Agent MAIN/projects/secuura/reports/2026-09-17-ks1207-1023-2f74491eb-tier1-r1/'
assert os.path.isdir(PRIOR), 'prior report dir missing'
HEADER_OLD = cut('# launch_qa_secuura_ks1215_1034.sh', "# Exit: 0 launched (or guards passed under --check) · 2..25 a guard refused\n")
HEADER_NEW = """# launch_qa_secuura_ks1204_1035.sh — cross-project QA agent, ONE TIER 1 ROUND 1 gate over Secuura/Blockchain PR #1035 (KS-1204, Seat A)
# @ 4b1fb0621e58ff00bba096751130bc6e53df4714 — services/api-gateway: a connector allow-list that is not an array fails closed; documentType-over-type is pinned.
# POST /api/documents: a connector whose stored allowedDocumentTypes is present, not null and not an array (a string, an object, an empty string, a number, a
# boolean) is refused 403 FORBIDDEN on EVERY create, typed or untyped, before enforcement (Wednesday's receipt accepted the three veto defaults: 403 FORBIDDEN,
# empty string = configured-not-a-list, untyped refused). ONE commit on develop 732c13459: routes/verification.ts +11 -1, the ks1204 test +292 (9 cells).
# TIER 1: an AUTHORISATION decision on the connector create path; the source is the #1014 round-2 gate's N-2 (a STRING allow-list substring-matched) + N-3
# (no cell pinned documentType-over-type). A GO is NOT a merge authorisation: the merge waits for Kam's tap.
#
# THE SHAPE, as read 01:04-01:20 AEST 2026-09-18 (git ls-remote + the PR and compare APIs agree): the head's only parent 732c13459 is the merge-base; develop has
# moved to 3961c2add (#1033: Dev root package.json / package-lock.json (mysql2 only), audit baseline, originate package files), so compare develop...head =
# merge_base 732c13459, ahead 1, files 2 (asserted, exit 10; behind NOT asserted). Merged tree over 3961c2add = d21341805 (re-drafter clone, 0 conflicts).
#
# The develop pin is judged by CONTENT — PATH BLOBS — never by develop's SHA: (a) NINETEEN files by blob at the CURRENT develop — the PR two (routes/verification.ts
# 28fb58343, the ks1204 test ABSENT; at a #1035 blob -> exit 19 LANDED), and what the gate runs and reads: index.ts (mount order, body parsers, the /api/v1 rewrite),
# routes/admin.ts (the platform-settings writer), services/health.ts (the connector-info reader), services/redis.ts, services/enforcement.ts, middleware/auth.ts,
# middleware/contentType.ts, the ks1176 test, gateway package.json / vitest.config.ts / vitest.setup.ts / tsconfig.json, shared utils/gracefulShutdown.ts, frontend
# admin pages/Settings.tsx (the probe transcribes its save), mcp-server tools/info.ts and package-generator.ts (readers), Dev eslint.config.mjs — any blob nobody
# pinned -> exit 18; (b) if develop moved past 732c13459, the compare pinned...develop REFUSES (exit 18) when the delta touches a GUARDED path —
# services/api-gateway/src/ and its package.json / vitest.config.ts / vitest.setup.ts / tsconfig.json, packages/shared/src/, eslint.config.mjs, Settings.tsx, the two
# mcp-server readers — or the move cannot be judged. WHY these paths: they are the code the gate runs in-process (the real index.ts app, the create route, the
# admin writer, the info reader) and the readers it censuses; a develop merge elsewhere (other services, lockfiles, audit baselines) cannot change what the gate
# measures, so it must not refuse. DEV_CONTENT_ALLOWED is EMPTY. Open PRs #1034 (middleware/auth.ts), #575 / #649 / #1036 (api-gateway package.json), #923 (an
# api-gateway test), #995 (utils/trustHeaders.ts) and #922 (shared src) touch GUARDED paths: if one lands first this REFUSES by design — re-pin deliberately.
#
# exit 21: the LAUNCH path refuses when stdin is not a TTY. This launcher execs an interactive agent; run it in a cockpit
# pane, never inside a Bash tool — and never run it without --check to "prove" this guard. `--check` runs headless (it launches nothing).
# exit 22: the prompt must require node_modules farmed PER ENTRY (the #1009 gate R-6: a wholesale link can write through to the checkout .vite).
# exit 23: the prompt must carry the exact #1035 verdict subject and name coagent@ as the sender and wednesday-agent@ as the recipient.
# exit 24: brief AND prompt must name the REPORT DIRECTORY and the PRIOR REPORT (#1014 round 2, KS-1176: its N-2 + N-3 are this ticket; the QA agent has no
#          inbox), and the prompt must name NOT-TESTED.written-first.md (written FIRST, before any run).
# exit 25: brief AND prompt must carry the MERGE ADDENDUM and require the per-finding CLOSED / STILL OPEN / NEW disposition.
# QA1035_CUR_DEV (test override, --check only): stands in for origin develop so the LANDED / GUARDED refusals can be proven.
# QA1035_VER_FILE (test fixture, --check only): a local file stands in for develop routes/verification.ts (its git blob) so the LANDED and GUARDED
# arms can be proven without a real develop commit.
# A launch with any QA1035_* override or fixture set refuses (exit 16).
#
# Generated by gatesets/2026-09-17_gate1035/gen_launcher_1035.py from launch_qa_secuura_ks1215_1034.sh (asserted substitutions + pins re-read from the repo +
# residual guard + output controls + bash -n): same guard set and exit codes 2..25 (19 = LANDED), re-pointed at #1035 ROUND 1, no content-cleared blob.
#
# Usage: launch_qa_secuura_ks1204_1035.sh [--check]
# Exit: 0 launched (or guards passed under --check) · 2..25 a guard refused
"""
JUDGED_OLD = cut('A = D + "services/api-gateway/"\nAUTHTS = A + "src/middleware/auth.ts"\n', 'content_cleared = set()\n')
def key(p_):
    return ('A + "' + p_[len(A):] + '"') if p_.startswith(A) else ('D + "' + p_ + '"')
rows = ['  VERTS:' + ' ' * 64 + '({"' + PIN[VER] + '": DV}, {"' + LANDED[VER] + '": "#1035 own"}),',
        '  A + "src/__tests__/ks1204-a-non-array-allow-list-fails-closed-and-documenttype-wins.test.ts": ({"ABSENT": DV}, {"' + LANDED[T1204] + '": "#1035 own"}),']
for p_, b_ in PIN.items():
    if p_ in LANDED: continue
    k = key(p_); rows.append('  %s:%s({"%s": DV}, {}),' % (k, ' ' * max(1, 70 - len(k)), b_))
JUDGED_NEW = ('A = D + "services/api-gateway/"\nVERTS = A + "src/routes/verification.ts"\nDV = "develop"\n'
              '# file -> (develop-OK blobs {blob: label}, LANDED blobs {blob: label}); ABSENT = the contents API answers 404 at develop\nJUDGED = {\n' + '\n'.join(rows) +
              '\n}\n# No REGION judgement: every file is judged by exact blob (a develop move of verification.ts, admin.ts or health.ts refuses, exit 18).\ncontent_cleared = set()\n')
GUARD_OLD = cut('GUARDED = [A + "src/",\n', 'DEV_CONTENT_ALLOWED = {}\n')
GUARD_NEW = '''GUARDED = [A + "src/",
           A + "package.json",
           A + "vitest.config.ts",
           A + "vitest.setup.ts",
           A + "tsconfig.json",
           D + "packages/shared/src/",
           D + "eslint.config.mjs",
           D + "frontend/admin/src/pages/Settings.tsx",
           D + "services/mcp-server/src/tools/info.ts",
           D + "services/mcp-server/src/package-generator.ts"]
# STYLE NOTE (912r2 launcher, measured): bash scans quote/paren state THROUGH this heredoc because it sits inside a
# command substitution — keep apostrophes and parentheses EVEN (this block uses none of the former), or the outer $( ) breaks.
# CONTENT-JUDGED allowlist: EMPTY. No lockfile is guarded: the gate names the vitest version it ran against develop-s lock. Re-pin deliberately.
DEV_CONTENT_ALLOWED = {}
'''
OKLINE_OLD = cut('print("OK " + state + " | origin develop MOVED %s -> %s', 'sys.exit(0)\n')
OKLINE_NEW = 'print("OK " + state + " | origin develop MOVED %s -> %s: commits=%d files=%d — GUARDED hits %d — disjoint from the GUARDED list (services/api-gateway/src/ + its package.json / vitest.config.ts / vitest.setup.ts / tsconfig.json, packages/shared/src/, eslint.config.mjs, frontend admin Settings.tsx, mcp-server tools/info.ts + package-generator.ts); %s" % (pinned, cur, c["ahead_by"], len(files), len(hits), tail)); sys.exit(0)\n'
REPL = [
 ('header', HEADER_OLD, HEADER_NEW, 1),
 ('brief var', 'BRIEF="${QA1034_BRIEF:-$WED/2_Project_Files/fleet/qa-agent/briefs/2026-09-17_secuura-1034-ks1215-tier1.md}"', 'BRIEF="${QA1035_BRIEF:-$WED/2_Project_Files/fleet/qa-agent/briefs/2026-09-17_secuura-1035-ks1204-tier1.md}"', 1),
 ('prompt var', 'PROMPT_FILE="${QA1034_PROMPT:-$WED/2_Project_Files/fleet/qa-agent/briefs/2026-09-17_secuura-1034-ks1215-tier1.prompt.txt}"', 'PROMPT_FILE="${QA1035_PROMPT:-$WED/2_Project_Files/fleet/qa-agent/briefs/2026-09-17_secuura-1035-ks1204-tier1.prompt.txt}"', 1),
 ('branch', "BRANCH='refs/heads/feature/ks-1215-api-gateway-a-revoked-session-jwt-plus-a-valid-key-whose'", "BRANCH='refs/heads/feature/ks-1204-a-string-alloweddocumenttypes-substring-matches-and-no-cell'", 1),
 ('head var', 'HEAD_SHA="${QA1034_HEAD:-fd81a75f0688f6cbe1e5f79b061bb1369c88f477}"', 'HEAD_SHA="${QA1035_HEAD:-' + H + '}"', 1),
 ('merge-base', "MERGE_BASE='27e53ec3aa010b50cd9b2e4a1d15cbb34605ba7d'   # the merge-base of the head with develop (#1029s squash), the second parent of the head merge fd81a75f0",
  "MERGE_BASE='" + MB + "'   # the merge-base of the head with develop (#1031s squash) = the only parent of the one-commit head 4b1fb0621", 1),
 ('develop', "DEVELOP_SHA='27e53ec3aa010b50cd9b2e4a1d15cbb34605ba7d'   # the pin = the merge-base = develop at drafting (moves judged by PATH BLOB and GUARDED paths, never by this SHA: git ls-remote 23:03:08 + 23:08:34; compare API 23:04:04 AEST)",
  "DEVELOP_SHA='" + MB + "'   # the pin = the merge-base; develop was 3961c2add at draft close (moves judged by PATH BLOB and GUARDED paths, never by this SHA: git ls-remote 00:57:58 + 01:05:56; compare API 01:04:26 AEST 2026-09-18)", 1),
 ('report dirs', "REPORT_DIR='" + OLD_REPORT + "'\nPRIOR_REPORT='" + OLD_PRIOR + "'\n", "REPORT_DIR='" + REPORT_DIR + "'\nPRIOR_REPORT='" + PRIOR + "'\n", 1),
 ('real brief', 'REAL_BRIEF="$WED/2_Project_Files/fleet/qa-agent/briefs/2026-09-17_secuura-1034-ks1215-tier1.md"', 'REAL_BRIEF="$WED/2_Project_Files/fleet/qa-agent/briefs/2026-09-17_secuura-1035-ks1204-tier1.md"', 1),
 ('head refuse', 'REFUSING: #1034 — $HEAD_SHA', 'REFUSING: #1035 — $HEAD_SHA', 1),
 ('compare comment', '# develop...#1034 = 27e53ec3a ahead 2 files 2 (behind 0 at draft close; behind deliberately not asserted).', '# develop...#1035 = 732c13459 ahead 1 files 2 (behind 1 at draft close: develop 3961c2add; behind deliberately not asserted).', 1),
 ('compare assert', '''[ "$COMPARE" = "$MERGE_BASE ahead=2 files=2" ] || { echo "REFUSING: #1034 develop...head reads '$COMPARE', brief pins '$MERGE_BASE ahead=2 files=2'" >&2; exit 10; }''',
                    '''[ "$COMPARE" = "$MERGE_BASE ahead=1 files=2" ] || { echo "REFUSING: #1035 develop...head reads '$COMPARE', brief pins '$MERGE_BASE ahead=1 files=2'" >&2; exit 10; }''', 1),
 ('cur dev', 'CUR_DEV="${QA1034_CUR_DEV:-', 'CUR_DEV="${QA1035_CUR_DEV:-', 1),
 ('develop comment 2', '# The develop pin, judged by CONTENT (see the header): twenty-four files by PATH BLOB at the CURRENT develop (no region judgement), then',
                       '# The develop pin, judged by CONTENT (see the header): nineteen files by PATH BLOB at the CURRENT develop (no region judgement), then', 1),
 ('judged', JUDGED_OLD, JUDGED_NEW, 1),
 ('fixture env', '    fixture = os.environ.get("QA1034_AUTH_FILE", "") if f == AUTHTS else ""\n', '    fixture = os.environ.get("QA1035_VER_FILE", "") if f == VERTS else ""\n', 1),
 ('landed msg', '" — #1034 has landed; this brief is stale"', '" — #1035 has landed; this brief is stale"', 1),
 ('ok pinned', '" (= the head merge-base, an ANCESTOR of the head: merged tree = the head tree 6339c404c05fcfbfa3b6505b6bfb7955303c1ccd; git ls-remote)"',
               '" (= the head merge-base, an ANCESTOR of the head: merged tree = the head tree ' + HT + '; git ls-remote)"', 1),
 ('guarded', GUARD_OLD, GUARD_NEW, 1),
 ('tail', 'tail = "the gate merges the then-current develop onto fd81a75f0 in its own clone, asserts the merged services/api-gateway/src and shared subtrees equal the head, or re-runs the real-gateway matrix, the tamper table and the suites on the MERGED tree; names the merged-tree OID, drafter 27e53ec3a -> 6339c404c = the head tree (brief items 1, 3, 5, 6)"',
          'tail = "the gate merges the then-current develop onto 4b1fb0621 in its own clone, asserts the merged services/api-gateway, shared, frontend/admin and mcp-server subtrees equal the head, or re-runs the real-app census, the tamper table and the suites on the MERGED tree; names the merged-tree OID, re-drafter 3961c2add -> ' + MERGED[:9] + ' (brief items 3, 4, 5, 6)"', 1),
 ('ok moved line', OKLINE_OLD, OKLINE_NEW, 1),
 ('subject', '''grep -qF '[QA -> Wednesday] TIER 1 GATE #1034 (KS-1215) fd81a75f0' "$PROMPT_FILE"''', '''grep -qF '[QA -> Wednesday] TIER 1 GATE #1035 (KS-1204) 4b1fb0621' "$PROMPT_FILE"''', 1),
 ('subject msg', 'REFUSING: prompt does not carry the exact #1034 verdict subject', 'REFUSING: prompt does not carry the exact #1035 verdict subject', 1),
 ('exit24 msg', 'and the PRIOR REPORT $PRIOR_REPORT (#1023, KS-1207: its N-1 is this ticket), or the prompt does not name NOT-TESTED.written-first.md — the QA agent has no inbox',
                'and the PRIOR REPORT $PRIOR_REPORT (#1014 round 2, KS-1176: its N-2 + N-3 are this ticket), or the prompt does not name NOT-TESTED.written-first.md — the QA agent has no inbox', 1),
 ('check head', 'echo "  head on origin: #1034 $HEAD_SHA at $BRANCH"', 'echo "  head on origin: #1035 $HEAD_SHA at $BRANCH"', 1),
 ('check compare', 'echo "  compare (GitHub API): develop...#1034 = $COMPARE"', 'echo "  compare (GitHub API): develop...#1035 = $COMPARE"', 1),
 ('check subject', 'echo "  prompt carries the exact #1034 verdict subject, coagent@ sender, wednesday-agent@ recipient"\n  echo "  brief and prompt name the report directory and the #1023 PRIOR REPORT (KS-1207 N-1); prompt names NOT-TESTED.written-first.md"\n',
                   'echo "  prompt carries the exact #1035 verdict subject, coagent@ sender, wednesday-agent@ recipient"\n  echo "  brief and prompt name the report directory and the #1014 round-2 PRIOR REPORT (KS-1176 N-2 + N-3); prompt names NOT-TESTED.written-first.md"\n', 1),
 ('check fixture echo', '  [ -n "${QA1034_CUR_DEV:-}" ] && echo "  (develop read from the QA1034_CUR_DEV test override, not ls-remote)"\n  [ -n "${QA1034_AUTH_FILE:-}" ] && echo "  (develop api-gateway middleware/auth.ts read from the QA1034_AUTH_FILE fixture, not the contents API)"\n',
  '  [ -n "${QA1035_CUR_DEV:-}" ] && echo "  (develop read from the QA1035_CUR_DEV test override, not ls-remote)"\n  [ -n "${QA1035_VER_FILE:-}" ] && echo "  (develop api-gateway routes/verification.ts read from the QA1035_VER_FILE fixture, not the contents API)"\n', 1),
 ('exit16 fixture', '[ -z "${QA1034_BRIEF:-}${QA1034_PROMPT:-}${QA1034_HEAD:-}${QA1034_CUR_DEV:-}${QA1034_AUTH_FILE:-}" ]', '[ -z "${QA1035_BRIEF:-}${QA1035_PROMPT:-}${QA1035_HEAD:-}${QA1035_CUR_DEV:-}${QA1035_VER_FILE:-}" ]', 1),
]
badn = 0
for label, old, new, want in REPL:
    n = s.count(old)
    if n != want: print('ANCHOR COUNT', label, n, '!=', want); badn += 1; continue
    s = s.replace(old, new); print('  ok', label, n)
if badn: print('REFUSING: %d anchors disagreed; nothing written' % badn); sys.exit(1)
BODY = s.replace(HEADER_NEW, '')
RESID = ['QA1034_', 'fd81a75f0', '27e53ec3a', '6339c404c', 'KS-1215', '#1034', 'ks1215', 'AUTHTS', 'AUTH_FILE', 'secuura-1034', '#1023', 'KS-1207', 'twenty-four',
         'real-gateway matrix', '6c6fdc94e', 'ks1207', 'ks480', 'platform.ts', 'rawAuthorization']
res = {t: BODY.count(t) for t in RESID if t in BODY}
if res: print('REFUSING: residual tokens in the body', res, [l[:120] for l in BODY.splitlines() if any(t in l for t in res)][:6]); sys.exit(2)
CTL = {H: 2, MB: 2, HT: 1, REPORT_DIR: 1, PRIOR: 1, '"$PRIOR_REPORT"': 2, 'ahead=1 files=2': 2, 'QA1035_VER_FILE': 5, 'QA1035_CUR_DEV': 5,
       ': DV}': 19, "grep -q 'ROUND 1'": 2, 'content_cleared': 2, 'DEV_CONTENT_ALLOWED = {}': 1, '#1035 own': 2,
       'CLOSED / STILL OPEN / NEW': None, 'MERGE ADDENDUM': None, 'NOT-TESTED.written-first.md': None, 'exit 19': None, 'exit 21': None, 'exit 22': None,
       'exit 23': None, 'exit 24': None, 'exit 25': None, 'exit 16': None, '[QA -> Wednesday] TIER 1 GATE #1035 (KS-1204) 4b1fb0621': 1, 'packages/shared/src/': None,
       'briefs/2026-09-17_secuura-1035-ks1204-tier1.md': 2, 'briefs/2026-09-17_secuura-1035-ks1204-tier1.prompt.txt': 1, '[ -t 0 ]': 1,
       'exec claude --dangerously-skip-permissions --model opus': 1, 'A + "vitest.setup.ts"': 2, 'D + "frontend/admin/src/pages/Settings.tsx"': 2, 'A + "src/services/health.ts"': 1}
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
