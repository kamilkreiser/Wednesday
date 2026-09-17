#!/usr/bin/env python3
"""gen_launcher_1023.py — derive launch_qa_secuura_ks1207_1023.sh from launchers/launch_qa_secuura_ks1187_1019r2.sh (same service, same guard set) by ASSERTED
substitutions: every anchor must occur exactly as often as stated, or the generator refuses and writes nothing. Re-points at #1023 (KS-1207) ROUND 1: head 2f74491eb /
merge-base = develop 581c9db0d (an ANCESTOR of the head): compare develop...head = merge_base 581c9db0d ahead 3 files 2. The develop arm judges SEVENTEEN files by blob
at the current develop (auth.ts + the ks1207 test at their PR blobs -> exit 19 LANDED); the proxy.ts REGION judgement is REMOVED (auth.ts is judged by exact blob: any
develop move of auth.ts refuses exit 18 — KS-744 is queued on the same file). GUARDED on a develop move: services/api-gateway/src/ + its config files, packages/shared/src/
(isSessionActive, runWithTenantId), eslint.config.mjs, the Dev lockfile. Exits: 15 ROUND 1; 23 the #1023 subject; 24 REPORT_DIR + the #1017 R-4 PRIOR REPORT in brief AND
prompt + NOT-TESTED.written-first.md in the prompt; 25 MERGE ADDENDUM + CLOSED / STILL OPEN / NEW in brief AND prompt. Test hooks QA1023_*. Residual guard, output
controls, heredoc parity, no git write verb, no control bytes, bash -n. Never overwrites an existing output (writes a .pre-* copy first).
Usage: gen_launcher_1023.py <template launcher> <output launcher>   Exit: 0 written · 1 anchor/control disagreed · 2 residual token · 3 bash -n failed"""
import hashlib, os, re, shutil, subprocess, sys
TPL, OUT = sys.argv[1], sys.argv[2]
s = open(TPL).read()
def now(f='+%Y-%m-%d %H:%M:%S %Z'): return subprocess.run(['date', f], capture_output=True, text=True).stdout.strip()
print('gen_launcher_1023', now(), '| template sha256', hashlib.sha256(s.encode()).hexdigest()[:16], 'lines', s.count('\n'))
def cut(start, end_incl):
    assert s.count(start) == 1, ('cut start', start[:60], s.count(start))
    i = s.index(start); j = s.index(end_incl, i) + len(end_incl); return s[i:j]
REPORT_DIR = '/Volumes/DevMASTER/!CODING/Testing Agent MAIN/projects/secuura/reports/2026-09-17-ks1207-1023-2f74491eb-tier1-r1/'
PRIOR = '/Volumes/DevMASTER/!CODING/Testing Agent MAIN/projects/secuura/reports/2026-09-17-ks1195-1017-cbe29597d-tier1-r1/'
HEADER_OLD = cut('# launch_qa_secuura_ks1187_1019r2.sh', "# Exit: 0 launched (or guards passed under --check) · 2..25 a guard refused\n")
HEADER_NEW = """# launch_qa_secuura_ks1207_1023.sh — cross-project QA agent, ONE TIER 1 ROUND 1 gate over Secuura/Blockchain PR #1023 (KS-1207, Seat A)
# @ 2f74491ebd6211e722f778838339c55e8add008d — a failed optional API key falls through to the Bearer check. The fix commit 0f8b699b4 (parent d7e95cd9f):
# services/api-gateway/src/middleware/auth.ts +14 -10 (a presented sk_ key that fails validation on an OPTIONAL mount no longer calls next() at once; the Bearer
# path and its KS-257 session-revocation check run; with no Bearer the request stays anonymous) + the ks1207 test +185. 2f74491eb = a merge of develop 581c9db0d
# into 9bd0fd333 (a merge of f8c7aaa39 into 0f8b699b4); no file overlap. TIER 1: authentication middleware on every optional-auth mount.
#
# THE SHAPE, as read 18:06-18:19 AEST 2026-09-17 (git ls-remote + the PR, compare and contents APIs agree): develop 581c9db0d is the head merge-base AND an
# ANCESTOR of the head, so compare develop...head = merge_base 581c9db0d, ahead 3, behind 0, files 2 (asserted as merge_base + ahead + files, exit 10; behind NOT
# asserted). Merged tree over develop = the head tree 4bdf1b8c7 (= merge-tree 0f8b699b4 x 581c9db0d in the drafter clone = the seat prediction).
#
# The develop pin is judged by CONTENT, not bare: (a) SEVENTEEN files by blob at the CURRENT develop — the PR two (auth.ts 7c985bdce, the ks1207 test ABSENT; at
# their PR blobs -> exit 19 LANDED), index.ts, rateLimitEnforce.ts, routes/proxy.ts, routes/admin.ts, services/redis.ts, config/services.ts, rateLimitSkip.ts, the
# ks1195 and auth unit tests, api-gateway package.json / vitest.config.ts / vitest.setup.ts / tsconfig.json, Dev eslint.config.mjs, shared session-validation.ts —
# any blob nobody pinned -> exit 18 (no region judgement: auth.ts is judged by exact blob); (b) if develop moved past 581c9db0d, the compare pinned...develop
# REFUSES (exit 18) when the delta touches a GUARDED path — services/api-gateway/src/ and its config files, packages/shared/src/, eslint.config.mjs, the Dev
# lockfile — or the move cannot be judged. DEV_CONTENT_ALLOWED is EMPTY.
#
# exit 21: the LAUNCH path refuses when stdin is not a TTY. This launcher execs an interactive agent; run it in a cockpit
# pane, never inside a Bash tool — and never run it without --check to "prove" this guard. `--check` runs headless (it launches nothing).
# exit 22: the prompt must require node_modules farmed PER ENTRY (the #1009 gate R-6: a wholesale link can write through to the checkout .vite).
# exit 23: the prompt must carry the exact #1023 verdict subject and name coagent@ as the sender and wednesday-agent@ as the recipient.
# exit 24: brief AND prompt must name the REPORT DIRECTORY and the PRIOR REPORT that found the defect (#1017 round 1, Record R-4; the QA agent has no inbox), and
#          the prompt must name NOT-TESTED.written-first.md (written FIRST, before any run).
# exit 25: brief AND prompt must carry the MERGE ADDENDUM and require the per-finding CLOSED / STILL OPEN / NEW disposition.
# QA1023_CUR_DEV (test override, --check only): stands in for origin develop so the LANDED / GUARDED refusals can be proven.
# QA1023_AUTH_FILE (test fixture, --check only): a local file stands in for develop middleware/auth.ts (its git blob) so the LANDED and GUARDED arms can be
# proven without a real develop commit.
# A launch with any QA1023_* override or fixture set refuses (exit 16).
#
# Generated by gatesets/2026-09-17_gate1023/gen_launcher_1023.py from launch_qa_secuura_ks1187_1019r2.sh (asserted substitutions + residual guard + output
# controls + bash -n): same guard set and exit codes 2..25 (19 = LANDED), re-pointed at #1023 ROUND 1, the proxy.ts region judgement removed.
#
# Usage: launch_qa_secuura_ks1207_1023.sh [--check]
# Exit: 0 launched (or guards passed under --check) · 2..25 a guard refused
"""
JUDGED_OLD = cut('PX = G + "src/routes/proxy.ts"\n', 'content_cleared = set()\n')
JUDGED_NEW = '''AU = G + "src/middleware/auth.ts"
DV = "develop"
# file -> (develop-OK blobs {blob: label}, LANDED blobs {blob: label}); ABSENT = the contents API answers 404 at develop
JUDGED = {
  AU:                                                                  ({"7c985bdcefc26293815bfbe0cbf315f929b48835": DV}, {"b8fce678a85ecbac82f1e468fd0180059447a43e": "#1023 own"}),
  G + "src/__tests__/ks1207-a-failed-optional-api-key-falls-through-to-the-bearer-check.test.ts": ({"ABSENT": DV}, {"f56bd48b9e9213d5afb85df6c94a5eada3c5aa22": "#1023 own"}),
  G + "src/index.ts":                                                  ({"db127dbfa5dd899b0a8e0d844690890d91e27f10": DV}, {}),
  G + "src/middleware/rateLimitEnforce.ts":                            ({"90bd29378508c8fee54e010b54cdc72ff992aafa": DV}, {}),
  G + "src/routes/proxy.ts":                                           ({"795ae7ca3bdc76be3e563e87fc34a8cc221e5632": DV}, {}),
  G + "src/routes/admin.ts":                                           ({"f47dd6a655702ffbfc402ca920a33c4619d62c4b": DV}, {}),
  G + "src/services/redis.ts":                                         ({"47659ee9c9f06acf9ac64e09b2dc207113ba92ea": DV}, {}),
  G + "src/config/services.ts":                                        ({"6110888aac8c834c291b5385710943f9b6adf57b": DV}, {}),
  G + "src/middleware/rateLimitSkip.ts":                               ({"cfde7cdffb7ab73214c5f009d4be0609d040c2ab": DV}, {}),
  G + "src/__tests__/ks1195-per-key-rate-limiter-runs-after-authentication.test.ts": ({"4b1fc017da158de4e7a3a47565b7dbccc1ea3872": DV}, {}),
  G + "src/__tests__/auth.test.ts":                                    ({"72348995a66ea324ffe78dc64136f46e64985aad": DV}, {}),
  G + "package.json":                                                  ({"841d8c6adcd71e885c01e65c22da9418daff276a": DV}, {}),
  G + "vitest.config.ts":                                              ({"5888e0b320d934f6f434e0e5ca3c74a995cecc02": DV}, {}),
  G + "vitest.setup.ts":                                               ({"22c1107683b8192df3bfd3e929aa94aff3dc7d45": DV}, {}),
  G + "tsconfig.json":                                                 ({"c981e6a92fdd2417fa35070eb979c5f1c77ffbcd": DV}, {}),
  D + "eslint.config.mjs":                                             ({"8c5374c6022eb0a3f449f41a570db61294aa63f1": DV}, {}),
  D + "packages/shared/src/security/session-validation.ts":            ({"297a0bbd31be5c3868beb1a94d33c8e9d1dcf98d": DV}, {}),
}
# No REGION judgement for #1023: auth.ts is judged by exact blob (a develop move of auth.ts refuses, exit 18 — KS-744 edits the same file next).
content_cleared = set()
'''
LOOP_REGION_OLD = cut('    if blob not in ok and f == PX:\n', '        continue\n')
GUARD_OLD = cut('GUARDED = [G + "src/",\n', '           D + "package-lock.json"]\n')
GUARD_NEW = '''GUARDED = [G + "src/",
           G + "package.json",
           G + "vitest.config.ts",
           G + "vitest.setup.ts",
           G + "tsconfig.json",
           D + "packages/shared/src/",
           D + "eslint.config.mjs",
           D + "package-lock.json"]
'''
REPL = [
 ('header', HEADER_OLD, HEADER_NEW, 1),
 ('brief var', 'BRIEF="${QA1019R2_BRIEF:-$WED/2_Project_Files/fleet/qa-agent/briefs/2026-09-17_secuura-1019r2-ks1187-tier1.md}"', 'BRIEF="${QA1023_BRIEF:-$WED/2_Project_Files/fleet/qa-agent/briefs/2026-09-17_secuura-1023-ks1207-tier1.md}"', 1),
 ('prompt var', 'PROMPT_FILE="${QA1019R2_PROMPT:-$WED/2_Project_Files/fleet/qa-agent/briefs/2026-09-17_secuura-1019r2-ks1187-tier1.prompt.txt}"', 'PROMPT_FILE="${QA1023_PROMPT:-$WED/2_Project_Files/fleet/qa-agent/briefs/2026-09-17_secuura-1023-ks1207-tier1.prompt.txt}"', 1),
 ('branch', "BRANCH='refs/heads/feature/ks-1187-security-an-absolute-form-request-target-bypasses-the-ks-843'", "BRANCH='refs/heads/feature/ks-1207-security-an-unknown-sk_-key-on-an-optional-auth-mount-skips'", 1),
 ('head var', 'HEAD_SHA="${QA1019R2_HEAD:-82f09c8bd1bfab28e4d23c180cbaffea251685be}"', 'HEAD_SHA="${QA1023_HEAD:-2f74491ebd6211e722f778838339c55e8add008d}"', 1),
 ('merge-base', "MERGE_BASE='f8c7aaa39dabfe6a3916e5be55d9ccd752e7d8ed'   # the merge-base of the head with develop = develop itself, the second parent of the head merge 82f09c8bd (#1020s squash on #1017s squash)",
  "MERGE_BASE='581c9db0db4201c42cbbf702f339b750989acdb1'   # the merge-base of the head with develop = develop itself, the second parent of the head merge 2f74491eb (#1019s squash)", 1),
 ('develop', "DEVELOP_SHA='f8c7aaa39dabfe6a3916e5be55d9ccd752e7d8ed'   # develop at round-2 drafting, an ANCESTOR of the head (git ls-remote 16:44:13, 16:44:54, 16:48:17; branches API 16:50 AEST)",
  "DEVELOP_SHA='581c9db0db4201c42cbbf702f339b750989acdb1'   # develop at drafting, an ANCESTOR of the head (git ls-remote 18:06:47; compare API 18:19:23 AEST)", 1),
 ('report dirs', "REPORT_DIR='/Volumes/DevMASTER/!CODING/Testing Agent MAIN/projects/secuura/reports/2026-09-17-ks1187-1019r2-82f09c8bd-tier1-r2/'\nR1_REPORT='/Volumes/DevMASTER/!CODING/Testing Agent MAIN/projects/secuura/reports/2026-09-17-ks1187-1019-8b8996f8b-tier1-r1/'\n",
  "REPORT_DIR='" + REPORT_DIR + "'\nPRIOR_REPORT='" + PRIOR + "'\n", 1),
 ('real brief', 'REAL_BRIEF="$WED/2_Project_Files/fleet/qa-agent/briefs/2026-09-17_secuura-1019r2-ks1187-tier1.md"', 'REAL_BRIEF="$WED/2_Project_Files/fleet/qa-agent/briefs/2026-09-17_secuura-1023-ks1207-tier1.md"', 1),
 ('head refuse', 'REFUSING: #1019 ROUND 2 — $HEAD_SHA', 'REFUSING: #1023 — $HEAD_SHA', 1),
 ('compare comment', '# develop...#1019 ROUND 2 = f8c7aaa39 ahead 4 files 3 (behind 0 at draft close; behind deliberately not asserted).', '# develop...#1023 = 581c9db0d ahead 3 files 2 (behind 0 at draft close; behind deliberately not asserted).', 1),
 ('compare assert', '''[ "$COMPARE" = "$MERGE_BASE ahead=4 files=3" ] || { echo "REFUSING: #1019 ROUND 2 develop...head reads '$COMPARE', brief pins '$MERGE_BASE ahead=4 files=3'" >&2; exit 10; }''',
                    '''[ "$COMPARE" = "$MERGE_BASE ahead=3 files=2" ] || { echo "REFUSING: #1023 develop...head reads '$COMPARE', brief pins '$MERGE_BASE ahead=3 files=2'" >&2; exit 10; }''', 1),
 ('cur dev', 'CUR_DEV="${QA1019R2_CUR_DEV:-', 'CUR_DEV="${QA1023_CUR_DEV:-', 1),
 ('develop comment 2', '# The develop pin, judged by CONTENT (see the header): twenty-one files by blob at the CURRENT develop (proxy.ts also by region), then',
                       '# The develop pin, judged by CONTENT (see the header): seventeen files by blob at the CURRENT develop (no region judgement), then', 1),
 ('judged', JUDGED_OLD, JUDGED_NEW, 1),
 ('fixture env', '    fixture = os.environ.get("QA1019R2_PROXY_FILE", "") if f == PX else ""\n', '    fixture = os.environ.get("QA1023_AUTH_FILE", "") if f == AU else ""\n', 1),
 ('landed msg', '" — #1019 has landed; this ROUND 2 brief is stale"', '" — #1023 has landed; this brief is stale"', 1),
 ('loop region', LOOP_REGION_OLD, '', 1),
 ('ok pinned', '" (= the head merge-base, an ANCESTOR of the head: merged tree = the head tree 99df1503e4f18ac444baed015659fecbb912bbb0; git ls-remote)"',
               '" (= the head merge-base, an ANCESTOR of the head: merged tree = the head tree 4bdf1b8c7ea3a679e6b20a21c5970d375ba8776f; git ls-remote)"', 1),
 ('guarded', GUARD_OLD, GUARD_NEW, 1),
 ('allow comment', '# CONTENT-JUDGED allowlist: EMPTY for round 2. #1017 has MERGED (its squash d7e95cd9f is on develop f8c7aaa39, the pin), so no sibling blob is pre-cleared.\n# proxy.ts is judged by its REGION above. Every other guarded hit falls through to exit 18. Re-pin deliberately.\n',
                   '# CONTENT-JUDGED allowlist: EMPTY. #1017 and #1019 have MERGED (on develop 581c9db0d, the pin), so no sibling blob is pre-cleared.\n# Every guarded hit falls through to exit 18. Re-pin deliberately.\n', 1),
 ('tail', 'tail = "the gate merges the then-current develop onto 82f09c8bd in its own clone, rebuilds the shared dist there, re-runs the round-1 harness census on the MERGED tree beside the round-1, round-2 and head trees, names the merged-tree OID and re-derives every count, above all the api-gateway denominator (brief items 1, 2, 5)"',
          'tail = "the gate merges the then-current develop onto 2f74491eb in its own clone, rebuilds the shared dist there, re-runs the optional-mount census, the legitimate-caller table and the limiter rows on the MERGED tree beside the head and develop trees, names the merged-tree OID and re-derives every count, above all the api-gateway denominator (brief items 1, 2, 3, 6, 7)"', 1),
 ('moved msg', '(services/api-gateway/src/ + its config files, originate gdpr routes + index, eslint.config.mjs, the Dev lockfile) or cleared by the proxy.ts region judgement; %s',
               '(services/api-gateway/src/ + its config files, packages/shared/src/, eslint.config.mjs, the Dev lockfile); %s', 1),
 ('round grep', '''grep -q 'ROUND 2' "$BRIEF" && grep -q 'ROUND 2' "$PROMPT_FILE" || { echo "REFUSING: brief and prompt disagree about the round (ROUND 2)" >&2; exit 15; }''',
                '''grep -q 'ROUND 1' "$BRIEF" && grep -q 'ROUND 1' "$PROMPT_FILE" || { echo "REFUSING: brief and prompt disagree about the round (ROUND 1)" >&2; exit 15; }''', 1),
 ('subject', '''grep -qF '[QA -> Wednesday] TIER 1 GATE #1019 ROUND 2 (KS-1187) 82f09c8bd' "$PROMPT_FILE"''', '''grep -qF '[QA -> Wednesday] TIER 1 GATE #1023 (KS-1207) 2f74491eb' "$PROMPT_FILE"''', 1),
 ('subject msg', 'REFUSING: prompt does not carry the exact ROUND 2 verdict subject', 'REFUSING: prompt does not carry the exact #1023 verdict subject', 1),
 ('exit24', '''grep -qF "$REPORT_DIR" "$PROMPT_FILE" && grep -qF "$REPORT_DIR" "$BRIEF" && grep -qF 'NOT-TESTED.written-first.md' "$PROMPT_FILE" && grep -qF "$R1_REPORT" "$PROMPT_FILE" && grep -qF "$R1_REPORT" "$BRIEF" \\''',
            '''grep -qF "$REPORT_DIR" "$PROMPT_FILE" && grep -qF "$REPORT_DIR" "$BRIEF" && grep -qF 'NOT-TESTED.written-first.md' "$PROMPT_FILE" && grep -qF "$PRIOR_REPORT" "$PROMPT_FILE" && grep -qF "$PRIOR_REPORT" "$BRIEF" \\''', 1),
 ('exit24 msg', 'and the ROUND-1 REPORT $R1_REPORT, or the prompt does not name NOT-TESTED.written-first.md — the QA agent has no inbox; a carry-forward with no pointer can only be answered with I could not',
                'and the PRIOR REPORT $PRIOR_REPORT (Record R-4 found the defect), or the prompt does not name NOT-TESTED.written-first.md — the QA agent has no inbox', 1),
 ('exit25 msg', 'disposition — round 2 of 2: closed instances ship and residue is ticketed', 'disposition — the merge seat equality targets and the In Progress hold ride on it', 1),
 ('check head', 'echo "  head on origin: #1019 ROUND 2 $HEAD_SHA at $BRANCH"', 'echo "  head on origin: #1023 $HEAD_SHA at $BRANCH"', 1),
 ('check compare', 'echo "  compare (GitHub API): develop...#1019 ROUND 2 = $COMPARE"', 'echo "  compare (GitHub API): develop...#1023 = $COMPARE"', 1),
 ('check round', 'echo "  brief and prompt agree on TIER 1 and ROUND 2"', 'echo "  brief and prompt agree on TIER 1 and ROUND 1"', 1),
 ('check subject', 'echo "  prompt carries the exact ROUND 2 verdict subject, coagent@ sender, wednesday-agent@ recipient"\n  echo "  brief and prompt name the round-2 report directory and the ROUND-1 REPORT; prompt names NOT-TESTED.written-first.md"\n',
                   'echo "  prompt carries the exact #1023 verdict subject, coagent@ sender, wednesday-agent@ recipient"\n  echo "  brief and prompt name the report directory and the #1017 PRIOR REPORT (R-4); prompt names NOT-TESTED.written-first.md"\n', 1),
 ('check fixture echo', '  [ -n "${QA1019R2_CUR_DEV:-}" ] && echo "  (develop read from the QA1019R2_CUR_DEV test override, not ls-remote)"\n  [ -n "${QA1019R2_PROXY_FILE:-}" ] && echo "  (develop routes/proxy.ts read from the QA1019R2_PROXY_FILE fixture, not the contents API)"\n',
  '  [ -n "${QA1023_CUR_DEV:-}" ] && echo "  (develop read from the QA1023_CUR_DEV test override, not ls-remote)"\n  [ -n "${QA1023_AUTH_FILE:-}" ] && echo "  (develop middleware/auth.ts read from the QA1023_AUTH_FILE fixture, not the contents API)"\n', 1),
 ('exit16 fixture', '[ -z "${QA1019R2_BRIEF:-}${QA1019R2_PROMPT:-}${QA1019R2_HEAD:-}${QA1019R2_CUR_DEV:-}${QA1019R2_PROXY_FILE:-}" ]', '[ -z "${QA1023_BRIEF:-}${QA1023_PROMPT:-}${QA1023_HEAD:-}${QA1023_CUR_DEV:-}${QA1023_AUTH_FILE:-}" ]', 1),
]
bad = 0
for label, old, new, want in REPL:
    n = s.count(old)
    if n != want: print('ANCHOR COUNT', label, n, '!=', want); bad += 1; continue
    s = s.replace(old, new); print('  ok', label, n)
if bad: print('REFUSING: %d anchors disagreed; nothing written' % bad); sys.exit(1)
RESID = ['QA1019R2_', 'QA1019_', 'ROUND 2', 'R1_REPORT', 'ahead=4', '82f09c8bd', 'f8c7aaa39', '99df1503e', 'b99f45a4c', 'db1534753', '389e51e1d', '76c0137ee', '06b499605',
         'region_sha', 'WANT', 'SEGS', 'PX', 'ks1187', 'KS-1187', 'originate', 'gdpr', 'erasure', '#1019 has landed']
res = {t: s.count(t) for t in RESID if t in s}
PERMITTED_RESID = {'ks1187': 1, 'f8c7aaa39': 1}  # the template file name in the generated-by header line; the 9bd0fd333 merge named in the new header
for k, v in PERMITTED_RESID.items():
    if res.get(k) == v: res.pop(k)
if res: print('REFUSING: residual tokens', res); sys.exit(2)
CTL = {'2f74491ebd6211e722f778838339c55e8add008d': 2, '581c9db0db4201c42cbbf702f339b750989acdb1': 2, '4bdf1b8c7ea3a679e6b20a21c5970d375ba8776f': 1,
       REPORT_DIR: 1, PRIOR: 1, '"$PRIOR_REPORT"': 2, 'ahead=3 files=2': 2, 'QA1023_AUTH_FILE': 5, 'QA1023_CUR_DEV': 5,
       'b8fce678a85ecbac82f1e468fd0180059447a43e': 1, 'f56bd48b9e9213d5afb85df6c94a5eada3c5aa22': 1, '7c985bdcefc26293815bfbe0cbf315f929b48835': 1,
       'DEV_CONTENT_ALLOWED = {}': 1, ': DV}': 17, "grep -q 'ROUND 1'": 2, 'content_cleared': 2, 'CLOSED / STILL OPEN / NEW': None, 'MERGE ADDENDUM': None,
       'NOT-TESTED.written-first.md': None, 'exit 19': None, 'exit 21': None, 'exit 22': None, 'exit 23': None, 'exit 24': None, 'exit 25': None, 'exit 16': None,
       '[QA -> Wednesday] TIER 1 GATE #1023 (KS-1207) 2f74491eb': 1, 'packages/shared/src/': None}
got = {k: s.count(k) for k in CTL}
print('output controls', {(k[:24] + '…' if len(k) > 24 else k): v for k, v in got.items()})
for k, v in CTL.items():
    if (v is not None and got[k] != v) or got[k] == 0: print('CONTROL DISAGREED', k, got[k], v); sys.exit(1)
for tag in ("<<'PY'\n", "<<'PYJ'\n"):
    i = s.index(tag); j = s.index('\nPY' + ('J' if 'PYJ' in tag else '') + '\n', i); blk = s[i:j]
    print('heredoc', tag.strip(), 'apostrophes', blk.count("'") - 2, 'parens (', blk.count('('), ')', blk.count(')'))
    if (blk.count("'") - 2) % 2 or blk.count('(') != blk.count(')'): print('REFUSING: heredoc parity'); sys.exit(1)
if re.search(r'git -C "\$REPO" (fetch|push|checkout|merge|reset|worktree|commit|switch|pull)\b', s): print('REFUSING: git write verb'); sys.exit(1)
if re.search(r'[\x00-\x08\x0b\x0c\x0e-\x1f]', s): print('REFUSING: control bytes'); sys.exit(1)
if os.path.exists(OUT):
    pre = OUT + '.pre-' + now('+%H%M%S'); shutil.copyfile(OUT, pre); print('existing output copied to', pre)
open(OUT, 'w').write(s); os.chmod(OUT, 0o755)
p = subprocess.run(['bash', '-n', OUT], capture_output=True, text=True)
print('bash -n rc', p.returncode, p.stderr.strip()[:300])
if p.returncode: sys.exit(3)
print('written', OUT, 'mode', oct(os.stat(OUT).st_mode & 0o777), 'sha256', hashlib.sha256(s.encode()).hexdigest()[:16], 'lines', s.count('\n'))
