#!/usr/bin/env python3
"""gen_launcher_1032r2.py — derive launchers/launch_qa_secuura_ks1194_1032r2.sh from the round-1 launcher launchers/launch_qa_secuura_ks1194_1032.sh by ASSERTED
substitutions (every anchor must occur exactly as often as stated, or nothing is written). Pins re-read from the repo with read verbs (rev-parse) at develop
3961c2add and at the head; heredoc parity; residual guard (no round-1 head / pin / report / subject / ROUND 1 token left); no git write verb; no control
bytes; bash -n on a tmp file, then os.replace (a .pre-* copy if the output already exists).
Re-points at #1032 ROUND 2: head 430672697; develop 3961c2add = the head merge-base and an ANCESTOR (compare ahead 6 files 3); 22 JUDGED files (the 3 PR files
LANDED at a round-1 OR round-2 blob -> exit 19; + utils/logger.ts and shared tenant-pool-manager.ts added); GUARDED arm unchanged; exit 15 = ROUND 2;
exit 23 = the ROUND 2 subject; exit 24 = REPORT_DIR + the ROUND-1 REPORT (R1_REPORT) + NOT-TESTED.written-first.md; exit 25 also requires "Kam's tap"
in brief and prompt. Env prefix QA1032R2_. Usage: gen_launcher_1032r2.py   Exit: 0 written · 1 anchor/pin disagreed · 2 residual token · 3 bash -n failed"""
import hashlib, os, re, shutil, subprocess, sys
L = '/Volumes/DevMASTER/WEDNESDAY/2_Project_Files/fleet/qa-agent/launchers/'
TPL = L + 'launch_qa_secuura_ks1194_1032.sh'; OUT = L + 'launch_qa_secuura_ks1194_1032r2.sh'
s = open(TPL).read()
def now(f='+%Y-%m-%d %H:%M:%S %Z'): return subprocess.run(['date', f], capture_output=True, text=True).stdout.strip()
print('gen_launcher_1032r2', now(), '| template sha256', hashlib.sha256(s.encode()).hexdigest()[:16], 'lines', s.count('\n'))
REPO = '/Volumes/DevMASTER/!CODING/Secuura/Blockchain/2_Project_Files'
H = '4306726977b55171a7c8c0eb5e42de078587a725'; DEVSHA = '3961c2add8e1637b32e638f8f0952c328c00833e'; HT = '522fc66068'  # tree prefix, re-read below
D = 'Blockchain/Dev/'; A = 'services/auth/'
rp = lambda x: subprocess.run(['git', '-C', REPO, 'rev-parse', '--verify', '-q', x], capture_output=True, text=True).stdout.strip()
HEAD_TREE = rp(H + '^{tree}'); assert HEAD_TREE.startswith('522fc6606'), HEAD_TREE
T1 = A + 'src/__tests__/ks1194-a-failed-verification-request-save-is-never-acknowledged.test.ts'
T2 = A + 'src/__tests__/ks1194-approve-never-restores-pending-over-a-raised-level.test.ts'
PIN = {
 A + 'src/repositories/userRepo.ts': '9060b308e6d6a82c8a79be7387032d2a18c4ac22',
 A + 'src/repositories/dbErrors.ts': 'f94faf0d3d3540990f8626fcb65c746737202ac4',
 A + 'src/middleware/errorHandler.ts': '1cf66e74cd2bbe1d56f53c6f7ef5200e1835ee3c',
 A + 'src/db.ts': 'cf0ee130bb5228214a41e163b3be766b8aebbb72',
 A + 'src/types/index.ts': '9b0b4f08afbf3244f6a28b374dd302786a75aab3',
 A + 'src/index.ts': 'edabbf87182311241662b20ac71d7244e923b5a3',
 A + 'src/utils/logger.ts': 'e35ce776ae82ab828906c93e379712659a516005',
 A + 'src/__tests__/ks1018-security-correctness-three-verification-store-reads.test.ts': '6723276d016e4d6cf4ead8cb4f511ce5dad5ce53',
 A + 'src/__tests__/ks1050-profile-update-zero-rows-is-not-success.test.ts': 'ffb3e801ab371bed4a11accd0dbcc64bd8fdc804',
 A + 'src/__tests__/ks949-platform-admin-seed-identity.test.ts': '4f03e6f4f132bc7a8f3c3577684f6eef3bf8ce03',
 A + 'src/auth.openapi.ts': '2c356c3c7877add99f5e1a3c437d04ac8be3dc76',
 A + 'package.json': '814e88419470b811f26f1593984071bb317608d8',
 A + 'vitest.config.ts': '8bb96293a0f11a14d90e7c7893f32a053277bbdb',
 A + 'vitest.setup.ts': 'bc18c18755cb00f96e3e228ca34d99fd1266c20f',
 A + 'tsconfig.json': 'a7952bdeaf16e933432bb0e7136f484bb7288a40',
 'packages/shared/src/db/tenant-guc.ts': '86953b978062eb1d124abf3154fa1da324c6e110',
 'packages/shared/src/db/tenant-pool-manager.ts': '9c33d89174c8f37d1dc8afdf907f75ec1d68e52c',
 'docs/openapi/secuura-api.yaml': '122d3a2f84cf77bf2b7e2dc51489a0d5f823db1f',
 'eslint.config.mjs': '8c5374c6022eb0a3f449f41a570db61294aa63f1',
}
USERS_DEV = 'c723a68afe3005c22a2c74e95f07d93647a17dae'
LAND = {A + 'src/routes/users.ts': ('8299a25586c8484d30da22430cfdc014c0b33785', '3bfa47dcde0125d9e23cb8a9fbddf7bd40aa0b2d'),
        T1: ('bc8f924c39ee46d23b48d8bfbfd90e1f886ced86', '703c80dca84cde113b585788317f56cb5184f3d3'), T2: (None, 'b79cddd656cbbb54510bb511d09d3066e8f44498')}
bad = []
for p, b in PIN.items():
    if rp(DEVSHA + ':' + D + p) != b: bad.append(('develop', p))
    if rp(H + ':' + D + p) != b: bad.append(('head', p))
if rp(DEVSHA + ':' + D + A + 'src/routes/users.ts') != USERS_DEV: bad.append(('develop users.ts',))
for p, (r1b, r2b) in LAND.items():
    if rp(H + ':' + D + p) != r2b: bad.append(('head LANDED', p))
    if r1b and rp('70ee7b6c03eeb7ef0609d6fc8fa5223e3647c039:' + D + p) != r1b: bad.append(('r1 LANDED', p))
    if p != A + 'src/routes/users.ts' and rp(DEVSHA + ':' + D + p): bad.append(('present at develop', p))
print('pins re-read:', len(PIN) + 1 + len(LAND), 'files | disagreements', bad)
if bad: sys.exit(1)
def sub(old, new, want=1):
    global s
    n = s.count(old)
    if n != want: print('ANCHOR COUNT', n, '!=', want, '::', old[:120]); sys.exit(1)
    s = s.replace(old, new)
# 1. header: everything between line 1 and `set -u`
i0 = s.index('\n') + 1; i1 = s.index('set -u\n')
HEADER = """# launch_qa_secuura_ks1194_1032r2.sh — cross-project QA agent, ONE TIER 1 ROUND 2 DELTA gate (round 2 of 2 under the cap) over Secuura/Blockchain PR #1032
# (KS-1194, Seat A) @ 4306726977b55171a7c8c0eb5e42de078587a725 — round 1 (head 70ee7b6c0) was NO GO on F-1 Major: the level UPDATE landed, updateUser's
# read-back failed, and the approve restored PENDING over the raised level. Round 2: 5d55a72bd merges develop 3961c2add (tree cdd8b90c6 = merge-tree
# 70ee7b6c0 x 3961c2add; under services/auth only package-lock.json), then 430672697 (users.ts +45 -12: after a throwing or null updateUserPlatformScope the
# approve re-reads the level under platform scope — target -> 200 APPROVED; another level -> restore PENDING, 503; unreadable -> keep APPROVED, 503 "could not
# be confirmed"; the round-1 ks1194 test +4 -3; a new round-2 test +212 over the REAL userRepo). TIER 1: the verification level is an assurance level other
# services gate on (#1015 F5; Kam ruled fail-closed). ROUND 2 of 2 is the CAP: a NO GO ships the closed instances and tickets the residue. A GO goes to Kam as
# a card: the merge is Kam's tap, never a seat action on the verdict.
#
# THE SHAPE, as read 01:01-01:21 AEST 2026-09-18 (git ls-remote x3 + the PR, compare and contents APIs agree): develop 3961c2add is the head merge-base AND an
# ANCESTOR of the head, so compare develop...head = merge_base 3961c2add, ahead 6, behind 0, files 3 (asserted as merge_base + ahead + files, exit 10; behind
# NOT asserted). Merged tree over develop = the head tree 522fc6606 (drafter clone).
#
# The develop pin is judged by CONTENT — PATH BLOBS — never by develop's SHA: (a) TWENTY-TWO files by blob at the CURRENT develop — the PR three (auth
# routes/users.ts c723a68af, the ks1194 test ABSENT, the ks1194 round-2 test ABSENT; at a #1032 round-1 OR round-2 blob -> exit 19 LANDED), and what the gate
# runs and reads: repositories/userRepo.ts and dbErrors.ts, middleware/errorHandler.ts, db.ts (query / tenant routing), types/index.ts, src/index.ts,
# utils/logger.ts, the ks1018 / ks1050 / ks949 tests, auth.openapi.ts, auth package.json / vitest.config.ts / vitest.setup.ts / tsconfig.json, shared
# db/tenant-guc.ts and db/tenant-pool-manager.ts, docs/openapi/secuura-api.yaml, Dev eslint.config.mjs — any blob nobody pinned -> exit 18; (b) if develop moved
# past 3961c2add, the compare pinned...develop REFUSES (exit 18) when the delta touches a GUARDED path — services/auth/src/ and its package.json /
# vitest.config.ts / vitest.setup.ts / tsconfig.json, packages/shared/src/, docs/openapi/, eslint.config.mjs — or the move cannot be judged. WHY these paths:
# they are the code and configuration the gate runs in-process (auth routes, repositories, db routing, error handler, the shared GUC + pool helpers) and the
# spec it reads; a develop merge elsewhere (other services, frontends, audit baselines, lockfiles: the gate farms node_modules from the checkout install)
# cannot change what the gate measures, so it must not refuse. DEV_CONTENT_ALLOWED is EMPTY. Open PRs #575, #649, #948 and #1036 edit auth package.json: if
# one lands first this REFUSES by design — re-pin deliberately.
#
# exit 21: the LAUNCH path refuses when stdin is not a TTY. This launcher execs an interactive agent; run it in a cockpit
# pane, never inside a Bash tool — and never run it without --check to "prove" this guard. `--check` runs headless (it launches nothing).
# exit 22: the prompt must require node_modules farmed PER ENTRY (the #1009 gate R-6: a wholesale link can write through to the checkout .vite).
# exit 23: the prompt must carry the exact ROUND 2 verdict subject and name coagent@ as the sender and wednesday-agent@ as the recipient.
# exit 24: brief AND prompt must name the round-2 REPORT DIRECTORY and the ROUND-1 REPORT path (the gate that found F-1; the QA agent has no inbox), and the
#          prompt must name NOT-TESTED.written-first.md (written FIRST, before any run).
# exit 25: brief AND prompt must carry the MERGE ADDENDUM, require the per-finding CLOSED / STILL OPEN / NEW disposition, and say the merge is Kam's tap.
# QA1032R2_CUR_DEV (test override, --check only): stands in for origin develop so the LANDED / GUARDED refusals can be proven.
# QA1032R2_USERS_FILE (test fixture, --check only): a local file stands in for develop auth routes/users.ts (its git blob) so the LANDED and GUARDED
# arms can be proven without a real develop commit.
# A launch with any QA1032R2_* override or fixture set refuses (exit 16).
#
# Generated by gatesets/2026-09-18_gate1032r2/gen_launcher_1032r2.py from launch_qa_secuura_ks1194_1032.sh (asserted substitutions + pins re-read from the
# repo + residual guard + output controls + bash -n): same guard set and exit codes 2..25 (19 = LANDED), re-pointed at #1032 ROUND 2, no content-cleared blob.
#
# Usage: launch_qa_secuura_ks1194_1032r2.sh [--check]
# Exit: 0 launched (or guards passed under --check) · 2..25 a guard refused
"""
s = s[:i0] + HEADER + s[i1:]
s = s.replace('QA1032_', 'QA1032R2_')  # the env prefix everywhere (counted below by the residual guard)
sub('briefs/2026-09-17_secuura-1032-ks1194-tier1.md}', 'briefs/2026-09-18_secuura-1032r2-ks1194-tier1.md}')
sub('briefs/2026-09-17_secuura-1032-ks1194-tier1.prompt.txt}', 'briefs/2026-09-18_secuura-1032r2-ks1194-tier1.prompt.txt}')
sub('HEAD_SHA="${QA1032R2_HEAD:-70ee7b6c03eeb7ef0609d6fc8fa5223e3647c039}"', 'HEAD_SHA="${QA1032R2_HEAD:-4306726977b55171a7c8c0eb5e42de078587a725}"')
sub("MERGE_BASE='0a2b1603fe52f0f3b8152588af78bbeab0237be7'   # the merge-base of the head with develop (#1028s squash), the second parent of the head merge 70ee7b6c0",
    "MERGE_BASE='3961c2add8e1637b32e638f8f0952c328c00833e'   # the merge-base of the head with develop = develop itself (#1033s squash), the second parent of 5d55a72bd")
sub("DEVELOP_SHA='0a2b1603fe52f0f3b8152588af78bbeab0237be7'   # the pin = the merge-base; develop was bb848b828 at draft close (moves judged by PATH BLOB and GUARDED paths, never by this SHA: git ls-remote 22:26:54 + 22:30:34; compare API 22:26:54 AEST)",
    "DEVELOP_SHA='3961c2add8e1637b32e638f8f0952c328c00833e'   # develop at round-2 drafting, an ANCESTOR of the head (moves judged by PATH BLOB and GUARDED paths, never by this SHA: git ls-remote 01:01:06, 01:19:17, 01:20:54; branches API 01:18:05 AEST)")
sub("REPORT_DIR='/Volumes/DevMASTER/!CODING/Testing Agent MAIN/projects/secuura/reports/2026-09-17-ks1194-1032-70ee7b6c0-tier1-r1/'",
    "REPORT_DIR='/Volumes/DevMASTER/!CODING/Testing Agent MAIN/projects/secuura/reports/2026-09-18-ks1194-1032-430672697-tier1-r2/'")
sub("PRIOR_REPORT='/Volumes/DevMASTER/!CODING/Testing Agent MAIN/projects/secuura/reports/2026-09-17-ks1018-1015-77145ce84-tier1-r1/'",
    "R1_REPORT='/Volumes/DevMASTER/!CODING/Testing Agent MAIN/projects/secuura/reports/2026-09-17-ks1194-1032-70ee7b6c0-tier1-r1/'")
sub('REAL_BRIEF="$WED/2_Project_Files/fleet/qa-agent/briefs/2026-09-17_secuura-1032-ks1194-tier1.md"', 'REAL_BRIEF="$WED/2_Project_Files/fleet/qa-agent/briefs/2026-09-18_secuura-1032r2-ks1194-tier1.md"')
sub('echo "REFUSING: #1032 — $HEAD_SHA is not at', 'echo "REFUSING: #1032 ROUND 2 — $HEAD_SHA is not at')
sub("# develop...#1032 = 0a2b1603f ahead 4 files 2 (behind 1 at draft close: develop bb848b828; behind deliberately not asserted).", "# develop...#1032 ROUND 2 = 3961c2add ahead 6 files 3 (behind 0 at draft close; behind deliberately not asserted).")
sub('[ "$COMPARE" = "$MERGE_BASE ahead=4 files=2" ] || { echo "REFUSING: #1032 develop...head reads \'$COMPARE\', brief pins \'$MERGE_BASE ahead=4 files=2\'" >&2; exit 10; }',
    '[ "$COMPARE" = "$MERGE_BASE ahead=6 files=3" ] || { echo "REFUSING: #1032 ROUND 2 develop...head reads \'$COMPARE\', brief pins \'$MERGE_BASE ahead=6 files=3\'" >&2; exit 10; }')
sub('# The develop pin, judged by CONTENT (see the header): nineteen files by PATH BLOB', '# The develop pin, judged by CONTENT (see the header): twenty-two files by PATH BLOB')
# JUDGED dict: rebuild the block between 'JUDGED = {' and the closing '}\n# No REGION judgement'
j0 = s.index('JUDGED = {\n'); j1 = s.index('}\n# No REGION judgement')
rows = ['JUDGED = {\n',
        '  USERS:                                                                ({"%s": DV}, {"%s": "#1032 round 1", "%s": "#1032 round 2"}),\n' % (USERS_DEV, *LAND[A + 'src/routes/users.ts']),
        '  A + "src/__tests__/ks1194-a-failed-verification-request-save-is-never-acknowledged.test.ts": ({"ABSENT": DV}, {"%s": "#1032 round 1", "%s": "#1032 round 2"}),\n' % LAND[T1],
        '  A + "src/__tests__/ks1194-approve-never-restores-pending-over-a-raised-level.test.ts": ({"ABSENT": DV}, {"%s": "#1032 round 2"}),\n' % LAND[T2][1]]
for p, b in PIN.items():
    key = ('A + "%s"' % p[len(A):]) if p.startswith(A) else ('D + "%s"' % p)
    rows.append('  %s ({"%s": DV}, {}),\n' % ((key + ':').ljust(70), b))  # GEN v2: one colon (v1 wrote two; caught by reading the output)
s = s[:j0] + ''.join(rows) + s[j1:]
sub('"LANDED develop " + short + " blob " + blob[:9] + " = " + landed[blob] + " — #1032 has landed; this brief is stale"', '"LANDED develop " + short + " blob " + blob[:9] + " = " + landed[blob] + " — #1032 has landed; this ROUND 2 brief is stale"')
sub('merged tree = the head tree 1111602c4ef8a8ca08b3f500ee241ec5fc1c0577; git ls-remote)', 'merged tree = the head tree %s; git ls-remote)' % HEAD_TREE)
sub('tail = "the gate merges the then-current develop onto 70ee7b6c0 in its own clone, asserts the merged services/auth/src and shared subtrees equal the head, or re-runs the fail-closed census, the tamper table and the suites on the MERGED tree; names the merged-tree OID, drafter bb848b828 -> beee976dd (brief items 1, 4, 5, 6)"',
    'tail = "the gate merges the then-current develop onto 430672697 in its own clone, asserts the merged services/auth/src and shared subtrees equal the head, or re-runs the approve branches, the tamper table and the suites on the MERGED tree; names the merged-tree OID, drafter 3961c2add -> 522fc6606 (brief items 1, 5, 6)"')
sub("grep -q 'ROUND 1' \"$BRIEF\" && grep -q 'ROUND 1' \"$PROMPT_FILE\" || { echo \"REFUSING: brief and prompt disagree about the round (ROUND 1)\" >&2; exit 15; }",
    "grep -q 'ROUND 2' \"$BRIEF\" && grep -q 'ROUND 2' \"$PROMPT_FILE\" || { echo \"REFUSING: brief and prompt disagree about the round (ROUND 2)\" >&2; exit 15; }")
sub("grep -qF '[QA -> Wednesday] TIER 1 GATE #1032 (KS-1194) 70ee7b6c0' \"$PROMPT_FILE\"", "grep -qF '[QA -> Wednesday] TIER 1 GATE #1032 ROUND 2 (KS-1194) 430672697' \"$PROMPT_FILE\"")
sub('{ echo "REFUSING: prompt does not carry the exact #1032 verdict subject, the coagent@ sender and the wednesday-agent@ recipient" >&2; exit 23; }',
    '{ echo "REFUSING: prompt does not carry the exact #1032 ROUND 2 verdict subject, the coagent@ sender and the wednesday-agent@ recipient" >&2; exit 23; }')
sub('grep -qF "$PRIOR_REPORT" "$PROMPT_FILE" && grep -qF "$PRIOR_REPORT" "$BRIEF" \\', 'grep -qF "$R1_REPORT" "$PROMPT_FILE" && grep -qF "$R1_REPORT" "$BRIEF" \\')
sub('{ echo "REFUSING: brief or prompt does not name the report directory $REPORT_DIR and the PRIOR REPORT $PRIOR_REPORT (#1015, KS-1018: its F5 is this ticket), or the prompt does not name NOT-TESTED.written-first.md — the QA agent has no inbox" >&2; exit 24; }',
    '{ echo "REFUSING: brief or prompt does not name the round-2 report directory $REPORT_DIR and the ROUND-1 REPORT $R1_REPORT, or the prompt does not name NOT-TESTED.written-first.md — the QA agent has no inbox" >&2; exit 24; }')
sub("grep -qF 'MERGE ADDENDUM' \"$PROMPT_FILE\" && grep -qF 'MERGE ADDENDUM' \"$BRIEF\" && grep -qF 'CLOSED / STILL OPEN / NEW' \"$PROMPT_FILE\" && grep -qF 'CLOSED / STILL OPEN / NEW' \"$BRIEF\" \\",
    "grep -qF 'MERGE ADDENDUM' \"$PROMPT_FILE\" && grep -qF 'MERGE ADDENDUM' \"$BRIEF\" && grep -qF 'CLOSED / STILL OPEN / NEW' \"$PROMPT_FILE\" && grep -qF 'CLOSED / STILL OPEN / NEW' \"$BRIEF\" && grep -qF \"Kam's tap\" \"$PROMPT_FILE\" && grep -qF \"Kam's tap\" \"$BRIEF\" \\")
sub('{ echo "REFUSING: brief or prompt does not carry the MERGE ADDENDUM and the per-finding CLOSED / STILL OPEN / NEW disposition — the merge seat equality targets and the In Progress hold ride on it" >&2; exit 25; }',
    '{ echo "REFUSING: brief or prompt does not carry the MERGE ADDENDUM, the per-finding CLOSED / STILL OPEN / NEW disposition, or that the merge is Kam\'s tap — the merge seat equality targets, the In Progress hold and the card to Kam ride on it" >&2; exit 25; }')
sub('  echo "  brief and prompt agree on TIER 1 and ROUND 1"', '  echo "  brief and prompt agree on TIER 1 and ROUND 2"')
sub('  echo "  prompt carries the exact #1032 verdict subject, coagent@ sender, wednesday-agent@ recipient"', '  echo "  prompt carries the exact #1032 ROUND 2 verdict subject, coagent@ sender, wednesday-agent@ recipient"')
sub('  echo "  brief and prompt name the report directory and the #1015 PRIOR REPORT (KS-1018 F5); prompt names NOT-TESTED.written-first.md"', '  echo "  brief and prompt name the round-2 report directory and the ROUND-1 REPORT; prompt names NOT-TESTED.written-first.md"')
sub('  echo "  brief and prompt carry the MERGE ADDENDUM and require CLOSED / STILL OPEN / NEW per finding"', '  echo "  brief and prompt carry the MERGE ADDENDUM, require CLOSED / STILL OPEN / NEW per finding, and say the merge is Kam\'s tap"')
# residual guard
RESID = ['70ee7b6c03eeb7ef', '0a2b1603f', 'bb848b828', 'beee976dd', '1111602c4', 'PRIOR_REPORT', "'ROUND 1'", '2026-09-17_secuura-1032-ks1194', 'ks1018-1015-77145ce84', 'QA1032_', 'nineteen', 'NINETEEN',
         '8299a25586c8484d30da22430cfdc014c0b33785": "#1032 own']
hits = [t for t in RESID if t in s and not (t == '70ee7b6c03eeb7ef' and s.count(t) == s.count('reports/2026-09-17-ks1194-1032-70ee7b6c0'))]
# the ROUND-1 REPORT path legitimately carries '70ee7b6c0' (short) — the full round-1 SHA must be gone
full_r1 = s.count('70ee7b6c03eeb7ef0609d6fc8fa5223e3647c039')
print('residual tokens:', hits, '| full round-1 SHA occurrences', full_r1, '| QA1032R2_ occurrences', s.count('QA1032R2_'))
if hits or full_r1: sys.exit(2)
# controls on the output text
ctl = dict(head=s.count(H), develop=s.count(DEVSHA), judged_rows=s.count(': DV}'), landed_r2=s.count('"#1032 round 2"'), round2_grep=s.count("grep -q 'ROUND 2'"),
           subject=s.count('TIER 1 GATE #1032 ROUND 2 (KS-1194) 430672697'), kams_tap=s.count("Kam's tap"), r1_report=s.count('R1_REPORT'))
print('output controls', ctl)
assert ctl['judged_rows'] == 22 and ctl['landed_r2'] == 3 and ctl['round2_grep'] == 2 and ctl['subject'] == 1 and ctl['kams_tap'] >= 3, ctl
for tag in ('PY', 'PYJ'):
    a = s.index("<<'%s'\n" % tag); b = s.index('\n%s\n' % tag, a)
    body = s[a:b]; print('heredoc', tag, 'apostrophes', body.count("'") - 2, 'parens', body.count('('), body.count(')'))
    assert body.count('(') == body.count(')')
    code = body.split('\n', 1)[1]; compile(code, 'heredoc-' + tag, 'exec'); print('heredoc', tag, 'python compile OK')  # GEN v2: bash -n cannot see Python syntax
assert not re.search(r'git -C "\$REPO" (push|commit|fetch|merge|checkout|reset|worktree|apply|update-ref)', s)
assert not re.search(r'[\x00-\x08\x0b\x0c\x0e-\x1f]', s)
tmp = OUT + '.tmp-gen'
open(tmp, 'w').write(s); os.chmod(tmp, 0o755)
p = subprocess.run(['bash', '-n', tmp], capture_output=True, text=True); print('bash -n rc', p.returncode, p.stderr.strip()[:200])
if p.returncode != 0: sys.exit(3)
if os.path.exists(OUT): shutil.copy2(OUT, OUT + '.pre-' + now('+%H%M%S'))
os.replace(tmp, OUT)
print('written', OUT, 'sha256', hashlib.sha256(open(OUT, 'rb').read()).hexdigest()[:16], 'lines', s.count('\n'), 'mode', oct(os.stat(OUT).st_mode)[-3:], '|', now())
