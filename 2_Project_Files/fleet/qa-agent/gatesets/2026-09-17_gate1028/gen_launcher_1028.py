#!/usr/bin/env python3
"""gen_launcher_1028.py — derive launchers/launch_qa_secuura_ks744_1028.sh from launchers/launch_qa_secuura_ks1207_1023.sh (same service, same file,
same guard set; launched, GO, merged) by ASSERTED substitutions: every anchor must occur exactly as often as stated, or the generator refuses and
writes nothing. Shape follows gen_launcher_1023.py + gen_launcher_1018_r2.py (tmp file, bash -n on the tmp, then os.replace; .pre-* copy if the output exists).
Re-points at #1028 (KS-744) ROUND 1: head e39521cfb; merge-base 19f1e5475 (the head's second parent): compare develop...head = merge_base 19f1e5475
ahead 3 files 2 (behind NOT asserted: develop moved to 20ab16f9a during drafting). The develop arm judges TWENTY-THREE files by blob at the CURRENT develop
(auth.ts b8fce678a / the ks744 test ABSENT; at their #1028 blobs -> exit 19 LANDED). GUARDED on a develop move, judged by the compare pinned...current:
services/api-gateway/src/ + its package.json / vitest.config.ts / vitest.setup.ts / tsconfig.json, packages/shared/src/, eslint.config.mjs, the Dev root
package-lock.json — with ONE content-cleared blob: the Dev lock at #1027 (4831bf207, js-yaml 3.15.1->3.15.2 and baseline-browser-mapping, dev deps; the gate
farms node_modules from the checkout install, which still has js-yaml 3.15.1, so the lock cannot change the gate's substrate). Test hook QA1028_LOCK_ALLOW_OFF
empties that allowlist so the lockfile refusal (exit 18) can be proven. Exits: 15 ROUND 1; 23 the #1028 subject; 24 REPORT_DIR + the #1023 PRIOR REPORT in
brief AND prompt + NOT-TESTED.written-first.md in the prompt; 25 MERGE ADDENDUM + CLOSED / STILL OPEN / NEW in brief AND prompt. Residual guard, output
controls, heredoc parity, no git write verb, no control bytes, bash -n.
Usage: gen_launcher_1028.py <template launcher> <output launcher>   Exit: 0 written · 1 anchor/control disagreed · 2 residual token · 3 bash -n failed"""
import hashlib, os, re, shutil, subprocess, sys
TPL, OUT = sys.argv[1], sys.argv[2]
s = open(TPL).read()
def now(f='+%Y-%m-%d %H:%M:%S %Z'): return subprocess.run(['date', f], capture_output=True, text=True).stdout.strip()
print('gen_launcher_1028', now(), '| template sha256', hashlib.sha256(s.encode()).hexdigest()[:16], 'lines', s.count('\n'))
REPO = '/Volumes/DevMASTER/!CODING/Secuura/Blockchain/2_Project_Files'
H = 'e39521cfb54cb5fd47c6bdae64ce707b3c9befce'; MB = '19f1e54750ce2b65312a687add2db4f5628edb7d'; CUR = '20ab16f9a80c5c3c75e613d8c670efefd8f5cafb'
HT = 'b61ed17766d282009b707053cbac6b5961076a0f'; LOCK = '4831bf2074779139926fbfda3f872c404eba177f'
D = 'Blockchain/Dev/'; G = D + 'services/api-gateway/'
rp = lambda x: subprocess.run(['git', '-C', REPO, 'rev-parse', x], capture_output=True, text=True).stdout.strip()
# every pinned blob is re-read from the repo (READ verb) and asserted, so a typo cannot pin a blob nobody has
PIN = {  # path relative to Blockchain/Dev -> blob at the merge-base (develop-OK)
 'services/api-gateway/src/middleware/auth.ts': 'b8fce678a85ecbac82f1e468fd0180059447a43e',
 'services/api-gateway/src/__tests__/ks1207-a-failed-optional-api-key-falls-through-to-the-bearer-check.test.ts': 'f56bd48b9e9213d5afb85df6c94a5eada3c5aa22',
 'services/api-gateway/src/utils/trustHeaders.ts': '15626e80f6caea4866abd1bb9ad171c79e12e788',
 'services/api-gateway/src/index.ts': 'db127dbfa5dd899b0a8e0d844690890d91e27f10',
 'services/api-gateway/src/routes/proxy.ts': '795ae7ca3bdc76be3e563e87fc34a8cc221e5632',
 'services/api-gateway/src/routes/admin.ts': 'f47dd6a655702ffbfc402ca920a33c4619d62c4b',
 'services/api-gateway/src/routes/verification.ts': '28fb5834308a502f5f7b806e3b49a77627601eff',
 'services/api-gateway/src/middleware/rateLimitEnforce.ts': '90bd29378508c8fee54e010b54cdc72ff992aafa',
 'services/api-gateway/src/services/redis.ts': '47659ee9c9f06acf9ac64e09b2dc207113ba92ea',
 'services/api-gateway/src/services/enforcement.ts': 'be466fbf444178bbb41293fb1d811957e55e1d2d',
 'services/api-gateway/src/config/services.ts': '6110888aac8c834c291b5385710943f9b6adf57b',
 'services/api-gateway/src/__tests__/ks1041-vouch-header-strip.test.ts': 'a3e1631f4046288339898170bdaa1f2faff347d5',
 'services/api-gateway/src/__tests__/ks1041-edge-strip-wiring.test.ts': 'c8e279bcc8ba38bf6e9874b625dd19fb99c93199',
 'services/api-gateway/src/__tests__/auth.test.ts': '72348995a66ea324ffe78dc64136f46e64985aad',
 'services/api-gateway/package.json': '841d8c6adcd71e885c01e65c22da9418daff276a',
 'services/api-gateway/vitest.config.ts': '5888e0b320d934f6f434e0e5ca3c74a995cecc02',
 'services/api-gateway/vitest.setup.ts': '22c1107683b8192df3bfd3e929aa94aff3dc7d45',
 'services/api-gateway/tsconfig.json': 'c981e6a92fdd2417fa35070eb979c5f1c77ffbcd',
 'eslint.config.mjs': '8c5374c6022eb0a3f449f41a570db61294aa63f1',
 'packages/shared/src/security/session-validation.ts': '297a0bbd31be5c3868beb1a94d33c8e9d1dcf98d',
 'packages/shared/src/crypto/jwks.ts': 'a131d32caa3faf0f55ca9af1a4fcd889a1affa17',
 'packages/shared/src/db/tenant-guc.ts': '86953b978062eb1d124abf3154fa1da324c6e110',
}
T744 = 'services/api-gateway/src/__tests__/ks744-a-token-missing-a-claim-is-proxied-not-500.test.ts'
LANDED_AU = '6e16683624b3c38a365ece44cccb4fdfac892c71'; LANDED_T = '2ed41a338ffcf2ecbdc952bad431f52a7a981848'
bad = [(p, b, rp(MB + ':' + D + p), rp(CUR + ':' + D + p)) for p, b in PIN.items() if rp(MB + ':' + D + p) != b or rp(CUR + ':' + D + p) != b or (rp(H + ':' + D + p) != b and not p.endswith('middleware/auth.ts'))]
bad += [x for x in [('auth.ts head', rp(H + ':' + D + 'services/api-gateway/src/middleware/auth.ts'))] if x[1] != LANDED_AU]
bad += [x for x in [('ks744 head', rp(H + ':' + D + T744))] if x[1] != LANDED_T]
bad += [x for x in [('lock at CUR', rp(CUR + ':' + D + 'package-lock.json')), ('head tree', rp(H + '^{tree}'))] if x[1] not in (LOCK, HT)]
p = subprocess.run(['git', '-C', REPO, 'cat-file', '-e', MB + ':' + D + T744], capture_output=True); print('ks744 test ABSENT at merge-base (cat-file -e rc != 0):', p.returncode != 0)
if p.returncode == 0: bad.append(('ks744 test present at merge-base',))
print('pinned blobs re-read from the repo (merge-base = head = current develop for the 22 untouched + auth.ts develop blob):', 'OK' if not bad else bad)
if bad: print('REFUSING: pins disagree with the repo; nothing written'); sys.exit(1)
def cut(start, end_incl):
    assert s.count(start) == 1, ('cut start', start[:60], s.count(start))
    i = s.index(start); j = s.index(end_incl, i) + len(end_incl); return s[i:j]
REPORT_DIR = '/Volumes/DevMASTER/!CODING/Testing Agent MAIN/projects/secuura/reports/2026-09-17-ks744-1028-e39521cfb-tier1-r1/'
PRIOR = '/Volumes/DevMASTER/!CODING/Testing Agent MAIN/projects/secuura/reports/2026-09-17-ks1207-1023-2f74491eb-tier1-r1/'
OLD_PRIOR = '/Volumes/DevMASTER/!CODING/Testing Agent MAIN/projects/secuura/reports/2026-09-17-ks1195-1017-cbe29597d-tier1-r1/'
HEADER_OLD = cut('# launch_qa_secuura_ks1207_1023.sh', "# Exit: 0 launched (or guards passed under --check) · 2..25 a guard refused\n")
HEADER_NEW = """# launch_qa_secuura_ks744_1028.sh — cross-project QA agent, ONE TIER 1 ROUND 1 gate over Secuura/Blockchain PR #1028 (KS-744, Seat A)
# @ e39521cfb54cb5fd47c6bdae64ce707b3c9befce — a verified token missing its email or verificationLevel claim is proxied, not answered 500. The fix commit
# 6252f06ac (parent d7e95cd9f): services/api-gateway/src/middleware/auth.ts +3 -2 (x-user-email set only when the claim is truthy; x-verification-level set only
# when truthy, else DELETED) + the ks744 test +93. e39521cfb = a merge of develop 19f1e5475 (which carries #1023 / KS-1207 in the SAME auth.ts) into fb503741a
# (a merge of 81ee4b729 into 6252f06ac); merge-by-content re-derived by the drafter. TIER 1: auth middleware on every proxied route.
#
# THE SHAPE, as read 20:37-20:54 AEST 2026-09-17 (git ls-remote + the PR, compare and contents APIs agree): 19f1e5475 is the head merge-base AND its second
# parent, so compare develop...head = merge_base 19f1e5475, ahead 3, files 2 (asserted, exit 10; behind NOT asserted: develop moved to e02515f8f (#1018),
# 20ab16f9a (#1027) and 75ad0e55c (#1026) while drafting). Head tree b61ed1776 = merge-tree fb503741a x 19f1e5475 in the drafter clone = the seat prediction.
#
# The develop pin is judged by CONTENT, never by develop's SHA: (a) TWENTY-THREE files by blob at the CURRENT develop — the PR two (auth.ts b8fce678a, the ks744
# test ABSENT; at their #1028 blobs -> exit 19 LANDED), trustHeaders.ts (the email half of the fix relies on its strip), index.ts, proxy.ts, admin.ts,
# verification.ts, enforcement.ts, rateLimitEnforce.ts, redis.ts, services.ts, the ks1207 / ks1041 x2 / auth unit tests, api-gateway package.json /
# vitest.config.ts / vitest.setup.ts / tsconfig.json, Dev eslint.config.mjs, shared session-validation.ts / crypto/jwks.ts / db/tenant-guc.ts — any blob nobody
# pinned -> exit 18; (b) if develop moved past 19f1e5475, the compare pinned...develop REFUSES (exit 18) when the delta touches a GUARDED path —
# services/api-gateway/src/ and its config files, packages/shared/src/, eslint.config.mjs, the Dev root lockfile — unless that file's blob is CONTENT-CLEARED,
# or the move cannot be judged. WHY these paths: they are the code the gate runs (the gateway app in-process, the shared auth helpers it imports) and its
# test/type configuration; a develop merge elsewhere (services/auth, other services, frontends, audit baselines) cannot change what the gate measures, so it
# must not make the launcher refuse. DEV_CONTENT_ALLOWED clears ONE blob: Blockchain/Dev/package-lock.json 4831bf207 (#1027: js-yaml and
# baseline-browser-mapping dev bumps; the gate farms node_modules from the checkout install, not from develop's lock).
#
# exit 21: the LAUNCH path refuses when stdin is not a TTY. This launcher execs an interactive agent; run it in a cockpit
# pane, never inside a Bash tool — and never run it without --check to "prove" this guard. `--check` runs headless (it launches nothing).
# exit 22: the prompt must require node_modules farmed PER ENTRY (the #1009 gate R-6: a wholesale link can write through to the checkout .vite).
# exit 23: the prompt must carry the exact #1028 verdict subject and name coagent@ as the sender and wednesday-agent@ as the recipient.
# exit 24: brief AND prompt must name the REPORT DIRECTORY and the PRIOR REPORT on the same file (#1023, KS-1207, merged into this head; the QA agent has no
#          inbox), and the prompt must name NOT-TESTED.written-first.md (written FIRST, before any run).
# exit 25: brief AND prompt must carry the MERGE ADDENDUM and require the per-finding CLOSED / STILL OPEN / NEW disposition.
# QA1028_CUR_DEV (test override, --check only): stands in for origin develop so the LANDED / GUARDED refusals can be proven.
# QA1028_AUTH_FILE (test fixture, --check only): a local file stands in for develop middleware/auth.ts (its git blob) so the LANDED and GUARDED arms can be
# proven without a real develop commit.
# QA1028_LOCK_ALLOW_OFF (test hook, --check only): empties DEV_CONTENT_ALLOWED so the lockfile refusal (exit 18) can be proven.
# A launch with any QA1028_* override, fixture or hook set refuses (exit 16).
#
# Generated by gatesets/2026-09-17_gate1028/gen_launcher_1028.py from launch_qa_secuura_ks1207_1023.sh (asserted substitutions + pins re-read from the repo +
# residual guard + output controls + bash -n): same guard set and exit codes 2..25 (19 = LANDED), re-pointed at #1028 ROUND 1, one content-cleared blob.
#
# Usage: launch_qa_secuura_ks744_1028.sh [--check]
# Exit: 0 launched (or guards passed under --check) · 2..25 a guard refused
"""
JUDGED_OLD = cut('AU = G + "src/middleware/auth.ts"\n', 'content_cleared = set()\n')
rows = ['  AU:' + ' ' * 67 + '({"b8fce678a85ecbac82f1e468fd0180059447a43e": DV}, {"' + LANDED_AU + '": "#1028 own"}),',
        '  G + "src/__tests__/ks744-a-token-missing-a-claim-is-proxied-not-500.test.ts": ({"ABSENT": DV}, {"' + LANDED_T + '": "#1028 own"}),']
for p_, b_ in PIN.items():
    if p_.endswith('middleware/auth.ts'): continue
    k = ('G + "' + p_[len('services/api-gateway/'):] + '"') if p_.startswith('services/api-gateway/') else ('D + "' + p_ + '"')
    rows.append('  %s:%s({"%s": DV}, {}),' % (k, ' ' * max(1, 70 - len(k)), b_))
JUDGED_NEW = 'AU = G + "src/middleware/auth.ts"\nDV = "develop"\n# file -> (develop-OK blobs {blob: label}, LANDED blobs {blob: label}); ABSENT = the contents API answers 404 at develop\nJUDGED = {\n' + '\n'.join(rows) + '\n}\n# No REGION judgement: auth.ts is judged by exact blob (a develop move of auth.ts refuses, exit 18).\ncontent_cleared = set()\n'
GUARD_OLD = cut('GUARDED = [G + "src/",\n', 'DEV_CONTENT_ALLOWED = {}\n')
GUARD_NEW = '''GUARDED = [G + "src/",
           G + "package.json",
           G + "vitest.config.ts",
           G + "vitest.setup.ts",
           G + "tsconfig.json",
           D + "packages/shared/src/",
           D + "eslint.config.mjs",
           D + "package-lock.json"]
# STYLE NOTE (912r2 launcher, measured): bash scans quote/paren state THROUGH this heredoc because it sits inside a
# command substitution — keep apostrophes and parentheses EVEN (this block uses none of the former), or the outer $( ) breaks.
# CONTENT-JUDGED allowlist: ONE blob. #1027 moved the Dev root lock (js-yaml 3.15.1 to 3.15.2 and baseline-browser-mapping, dev deps only; READ by the drafter).
# The gate farms node_modules from the checkout install, so a develop lock cannot change its substrate. Any OTHER lock blob refuses, exit 18.
# QA1028_LOCK_ALLOW_OFF empties it (a --check control that proves the lockfile refusal fires). Re-pin deliberately.
DEV_CONTENT_ALLOWED = {} if os.environ.get("QA1028_LOCK_ALLOW_OFF") else {D + "package-lock.json": {"''' + LOCK + '''": "#1027 dev-dep lock bumps, content-cleared by the drafter"}}
'''
OKLINE_OLD = cut('print("OK " + state + " | origin develop MOVED %s -> %s', 'sys.exit(0)\n')
OKLINE_NEW = 'print("OK " + state + " | origin develop MOVED %s -> %s: commits=%d files=%d — GUARDED hits %d, content-cleared %s (%s) — disjoint from the rest of the GUARDED list (services/api-gateway/src/ + its config files, packages/shared/src/, eslint.config.mjs, the Dev lockfile); %s" % (pinned, cur, c["ahead_by"], len(files), len(hits), " ".join(x.replace(D, "") for x in cleared) or "none", " ".join(by_name[x]["sha"][:9] for x in cleared), tail)); sys.exit(0)\n'
REPL = [
 ('header', HEADER_OLD, HEADER_NEW, 1),
 ('brief var', 'BRIEF="${QA1023_BRIEF:-$WED/2_Project_Files/fleet/qa-agent/briefs/2026-09-17_secuura-1023-ks1207-tier1.md}"', 'BRIEF="${QA1028_BRIEF:-$WED/2_Project_Files/fleet/qa-agent/briefs/2026-09-17_secuura-1028-ks744-tier1.md}"', 1),
 ('prompt var', 'PROMPT_FILE="${QA1023_PROMPT:-$WED/2_Project_Files/fleet/qa-agent/briefs/2026-09-17_secuura-1023-ks1207-tier1.prompt.txt}"', 'PROMPT_FILE="${QA1028_PROMPT:-$WED/2_Project_Files/fleet/qa-agent/briefs/2026-09-17_secuura-1028-ks744-tier1.prompt.txt}"', 1),
 ('branch', "BRANCH='refs/heads/feature/ks-1207-security-an-unknown-sk_-key-on-an-optional-auth-mount-skips'", "BRANCH='refs/heads/feature/ks-744-gateway-500s-on-every-proxied-route-for-a-token-lacking'", 1),
 ('head var', 'HEAD_SHA="${QA1023_HEAD:-2f74491ebd6211e722f778838339c55e8add008d}"', 'HEAD_SHA="${QA1028_HEAD:-' + H + '}"', 1),
 ('merge-base', "MERGE_BASE='581c9db0db4201c42cbbf702f339b750989acdb1'   # the merge-base of the head with develop = develop itself, the second parent of the head merge 2f74491eb (#1019s squash)",
  "MERGE_BASE='" + MB + "'   # the merge-base of the head with develop, the second parent of the head merge e39521cfb (#1025s squash)", 1),
 ('develop', "DEVELOP_SHA='581c9db0db4201c42cbbf702f339b750989acdb1'   # develop at drafting, an ANCESTOR of the head (git ls-remote 18:06:47; compare API 18:19:23 AEST)",
  "DEVELOP_SHA='" + MB + "'   # the pin = the merge-base; develop was 75ad0e55c at draft close (moves judged by CONTENT: git ls-remote 21:07:47; compare API 20:42 AEST)", 1),
 ('report dirs', "REPORT_DIR='/Volumes/DevMASTER/!CODING/Testing Agent MAIN/projects/secuura/reports/2026-09-17-ks1207-1023-2f74491eb-tier1-r1/'\nPRIOR_REPORT='" + OLD_PRIOR + "'\n",
  "REPORT_DIR='" + REPORT_DIR + "'\nPRIOR_REPORT='" + PRIOR + "'\n", 1),
 ('real brief', 'REAL_BRIEF="$WED/2_Project_Files/fleet/qa-agent/briefs/2026-09-17_secuura-1023-ks1207-tier1.md"', 'REAL_BRIEF="$WED/2_Project_Files/fleet/qa-agent/briefs/2026-09-17_secuura-1028-ks744-tier1.md"', 1),
 ('head refuse', 'REFUSING: #1023 — $HEAD_SHA', 'REFUSING: #1028 — $HEAD_SHA', 1),
 ('compare comment', '# develop...#1023 = 581c9db0d ahead 3 files 2 (behind 0 at draft close; behind deliberately not asserted).', '# develop...#1028 = 19f1e5475 ahead 3 files 2 (behind 2 at draft close; behind deliberately not asserted).', 1),
 ('compare assert', '''[ "$COMPARE" = "$MERGE_BASE ahead=3 files=2" ] || { echo "REFUSING: #1023 develop...head reads '$COMPARE', brief pins '$MERGE_BASE ahead=3 files=2'" >&2; exit 10; }''',
                    '''[ "$COMPARE" = "$MERGE_BASE ahead=3 files=2" ] || { echo "REFUSING: #1028 develop...head reads '$COMPARE', brief pins '$MERGE_BASE ahead=3 files=2'" >&2; exit 10; }''', 1),
 ('cur dev', 'CUR_DEV="${QA1023_CUR_DEV:-', 'CUR_DEV="${QA1028_CUR_DEV:-', 1),
 ('develop comment 2', '# The develop pin, judged by CONTENT (see the header): seventeen files by blob at the CURRENT develop (no region judgement), then',
                       '# The develop pin, judged by CONTENT (see the header): twenty-three files by blob at the CURRENT develop (no region judgement), then', 1),
 ('judged', JUDGED_OLD, JUDGED_NEW, 1),
 ('fixture env', '    fixture = os.environ.get("QA1023_AUTH_FILE", "") if f == AU else ""\n', '    fixture = os.environ.get("QA1028_AUTH_FILE", "") if f == AU else ""\n', 1),
 ('landed msg', '" — #1023 has landed; this brief is stale"', '" — #1028 has landed; this brief is stale"', 1),
 ('ok pinned', '" (= the head merge-base, an ANCESTOR of the head: merged tree = the head tree 4bdf1b8c7ea3a679e6b20a21c5970d375ba8776f; git ls-remote)"',
               '" (= the head merge-base, an ANCESTOR of the head: merged tree = the head tree ' + HT + '; git ls-remote)"', 1),
 ('guarded', GUARD_OLD, GUARD_NEW, 1),
 ('tail', 'tail = "the gate merges the then-current develop onto 2f74491eb in its own clone, rebuilds the shared dist there, re-runs the optional-mount census, the legitimate-caller table and the limiter rows on the MERGED tree beside the head and develop trees, names the merged-tree OID and re-derives every count, above all the api-gateway denominator (brief items 1, 2, 3, 6, 7)"',
          'tail = "the gate merges the then-current develop onto e39521cfb in its own clone, asserts the merged api-gateway and shared subtrees equal the head, or re-runs the missing-claim contract rows, the tamper table and the suites on the MERGED tree; names the merged-tree OID (brief items 1, 3, 4, 5)"', 1),
 ('ok moved line', OKLINE_OLD, OKLINE_NEW, 1),
 ('round grep', '''grep -q 'ROUND 1' "$BRIEF" && grep -q 'ROUND 1' "$PROMPT_FILE" || { echo "REFUSING: brief and prompt disagree about the round (ROUND 1)" >&2; exit 15; }''',
                '''grep -q 'ROUND 1' "$BRIEF" && grep -q 'ROUND 1' "$PROMPT_FILE" || { echo "REFUSING: brief and prompt disagree about the round (ROUND 1)" >&2; exit 15; }''', 1),
 ('subject', '''grep -qF '[QA -> Wednesday] TIER 1 GATE #1023 (KS-1207) 2f74491eb' "$PROMPT_FILE"''', '''grep -qF '[QA -> Wednesday] TIER 1 GATE #1028 (KS-744) e39521cfb' "$PROMPT_FILE"''', 1),
 ('subject msg', 'REFUSING: prompt does not carry the exact #1023 verdict subject', 'REFUSING: prompt does not carry the exact #1028 verdict subject', 1),
 ('exit24 msg', 'and the PRIOR REPORT $PRIOR_REPORT (Record R-4 found the defect), or the prompt does not name NOT-TESTED.written-first.md — the QA agent has no inbox',
                'and the PRIOR REPORT $PRIOR_REPORT (#1023 on the same file, merged into this head), or the prompt does not name NOT-TESTED.written-first.md — the QA agent has no inbox', 1),
 ('check head', 'echo "  head on origin: #1023 $HEAD_SHA at $BRANCH"', 'echo "  head on origin: #1028 $HEAD_SHA at $BRANCH"', 1),
 ('check compare', 'echo "  compare (GitHub API): develop...#1023 = $COMPARE"', 'echo "  compare (GitHub API): develop...#1028 = $COMPARE"', 1),
 ('check subject', 'echo "  prompt carries the exact #1023 verdict subject, coagent@ sender, wednesday-agent@ recipient"\n  echo "  brief and prompt name the report directory and the #1017 PRIOR REPORT (R-4); prompt names NOT-TESTED.written-first.md"\n',
                   'echo "  prompt carries the exact #1028 verdict subject, coagent@ sender, wednesday-agent@ recipient"\n  echo "  brief and prompt name the report directory and the #1023 PRIOR REPORT (same file); prompt names NOT-TESTED.written-first.md"\n', 1),
 ('check fixture echo', '  [ -n "${QA1023_CUR_DEV:-}" ] && echo "  (develop read from the QA1023_CUR_DEV test override, not ls-remote)"\n  [ -n "${QA1023_AUTH_FILE:-}" ] && echo "  (develop middleware/auth.ts read from the QA1023_AUTH_FILE fixture, not the contents API)"\n',
  '  [ -n "${QA1028_CUR_DEV:-}" ] && echo "  (develop read from the QA1028_CUR_DEV test override, not ls-remote)"\n  [ -n "${QA1028_AUTH_FILE:-}" ] && echo "  (develop middleware/auth.ts read from the QA1028_AUTH_FILE fixture, not the contents API)"\n  [ -n "${QA1028_LOCK_ALLOW_OFF:-}" ] && echo "  (QA1028_LOCK_ALLOW_OFF test hook: the lockfile allowlist is EMPTY)"\n', 1),
 ('exit16 fixture', '[ -z "${QA1023_BRIEF:-}${QA1023_PROMPT:-}${QA1023_HEAD:-}${QA1023_CUR_DEV:-}${QA1023_AUTH_FILE:-}" ]', '[ -z "${QA1028_BRIEF:-}${QA1028_PROMPT:-}${QA1028_HEAD:-}${QA1028_CUR_DEV:-}${QA1028_AUTH_FILE:-}${QA1028_LOCK_ALLOW_OFF:-}" ]', 1),
]
badn = 0
for label, old, new, want in REPL:
    n = s.count(old)
    if n != want: print('ANCHOR COUNT', label, n, '!=', want); badn += 1; continue
    s = s.replace(old, new); print('  ok', label, n)
if badn: print('REFUSING: %d anchors disagreed; nothing written' % badn); sys.exit(1)
# residual guard over the BODY (the authored header names history legitimately)
BODY = s.replace(HEADER_NEW, '').replace(PRIOR, '')  # the PRIOR path names #1023's head legitimately
RESID = ['QA1023_', '2f74491eb', '581c9db0d', '4bdf1b8c7', '7c985bdce', 'KS-1207)', '#1023 has landed', '#1023 verdict', 'ks1195', '#1017', 'R-4', 'secuura-1023-ks1207',
         'seventeen', 'EMPTY. #1017', 'optional-mount census', 'limiter rows', '0f8b699b4']
res = {t: BODY.count(t) for t in RESID if t in BODY}
if res: print('REFUSING: residual tokens in the body', res, [l[:120] for l in BODY.splitlines() if any(t in l for t in res)][:6]); sys.exit(2)
CTL = {H: 2, MB: 2, HT: 1, REPORT_DIR: 1, PRIOR: 1, '"$PRIOR_REPORT"': 2, 'ahead=3 files=2': 2, 'QA1028_AUTH_FILE': 5, 'QA1028_CUR_DEV': 5, 'QA1028_LOCK_ALLOW_OFF': 6,
       LANDED_AU: 1, LANDED_T: 1, 'b8fce678a85ecbac82f1e468fd0180059447a43e': 1, LOCK: 1, ': DV}': 23, "grep -q 'ROUND 1'": 2, 'content_cleared': 2,
       'CLOSED / STILL OPEN / NEW': None, 'MERGE ADDENDUM': None, 'NOT-TESTED.written-first.md': None, 'exit 19': None, 'exit 21': None, 'exit 22': None,
       'exit 23': None, 'exit 24': None, 'exit 25': None, 'exit 16': None, '[QA -> Wednesday] TIER 1 GATE #1028 (KS-744) e39521cfb': 1, 'packages/shared/src/': None,
       'briefs/2026-09-17_secuura-1028-ks744-tier1.md': 2, 'briefs/2026-09-17_secuura-1028-ks744-tier1.prompt.txt': 1, '[ -t 0 ]': 1,
       'exec claude --dangerously-skip-permissions --model opus': 1}
got = {k: s.count(k) for k in CTL}
print('output controls', {(k[:24] + '…' if len(k) > 24 else k): v for k, v in got.items()})
for k, v in CTL.items():
    if (v is not None and got[k] != v) or got[k] == 0: print('CONTROL DISAGREED', k, got[k], v); sys.exit(1)
for pth, b_ in PIN.items():
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
