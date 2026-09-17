#!/usr/bin/env python3
"""gen_launcher_1031.py — derive launchers/launch_qa_secuura_ks1213_1031.sh from launchers/launch_qa_secuura_ks744_1028.sh (the latest generated launcher: same
guard set, blob-judged develop arm, residual guard) by ASSERTED substitutions: every anchor must occur exactly as often as stated, or the generator refuses and
writes nothing. Shape follows gen_launcher_1028.py + gen_launcher_1018_r2.py (pins re-read from the repo, tmp file, bash -n on the tmp, then os.replace; .pre-*
copy if the output exists). Re-points at #1031 (KS-1213) ROUND 1: head be8596a29; develop 75ad0e55c is the head's second parent AND merge-base: compare
develop...head = merge_base 75ad0e55c ahead 2 files 3 (behind NOT asserted). The develop arm judges EIGHTEEN originate / spec / lint files by PATH BLOB at the
CURRENT develop — never by develop's SHA (documents.ts de9b5ae25, certifications.ts 59bfe1c62, the ks1213 test ABSENT; at their #1031 blobs -> exit 19 LANDED).
On a develop move the compare pinned...current REFUSES (exit 18) when it touches services/originate/src/ or its package.json / jest.config.js / tsconfig.json,
packages/shared/src/, docs/openapi/ or eslint.config.mjs. DEV_CONTENT_ALLOWED is EMPTY (no lockfile is guarded: the gate farms node_modules from the checkout
install). Test fixture QA1031_DOCS_FILE stands in for develop documents.ts (content and git blob). Exits: 15 ROUND 1; 23 the #1031 subject; 24 REPORT_DIR + the
#1024 PRIOR REPORT in brief AND prompt + NOT-TESTED.written-first.md in the prompt; 25 MERGE ADDENDUM + CLOSED / STILL OPEN / NEW in brief AND prompt. Residual
guard, output controls, heredoc parity, no git write verb, no control bytes, bash -n.
Usage: gen_launcher_1031.py <template launcher> <output launcher>   Exit: 0 written · 1 anchor/control disagreed · 2 residual token · 3 bash -n failed"""
import hashlib, os, re, shutil, subprocess, sys
TPL, OUT = sys.argv[1], sys.argv[2]
s = open(TPL).read()
def now(f='+%Y-%m-%d %H:%M:%S %Z'): return subprocess.run(['date', f], capture_output=True, text=True).stdout.strip()
print('gen_launcher_1031', now(), '| template sha256', hashlib.sha256(s.encode()).hexdigest()[:16], 'lines', s.count('\n'))
REPO = '/Volumes/DevMASTER/!CODING/Secuura/Blockchain/2_Project_Files'
H = 'be8596a29af15477cb0cbf4b8684e35e63c38e9f'; MB = '75ad0e55c6335a5f34f6d0b74dfe00b334b2eb2e'; FIX = '450e3429ddd66a479231d259cd201fcddbe2b5a4'
HT = '75ed56fb43ee919be4f16671defddacb6168b650'
D = 'Blockchain/Dev/'; O = 'services/originate/'
rp = lambda x: subprocess.run(['git', '-C', REPO, 'rev-parse', '--verify', '-q', x], capture_output=True, text=True).stdout.strip()
PIN = {  # path relative to Blockchain/Dev -> blob at develop 75ad0e55c (develop-OK); re-read and asserted below
 O + 'src/routes/documents.ts': 'de9b5ae25984ea29eff01d6c4e73f9bc0dc6573a',
 O + 'src/routes/certifications.ts': '59bfe1c62cad4d324505344582d374f4c6035a6d',
 O + 'src/repositories/documentRepo.ts': '6e059d36c50a82016faca14111c28ec35bc4f237',
 O + 'src/repositories/certificationRepo.ts': '2bfeab1352c9f47be0c033e8d1fb1e845c7cdf6b',
 O + 'src/services/provenance.ts': '483aa9eb331d2caa5af285e20d9668a9dbcd92a6',
 O + 'src/index.ts': '44d4e4f341f5d314f5b95405b209a9450cde1d3e',
 O + 'src/middleware/auth.ts': 'f08ee1a895bc878bc2656f649833706f665686e7',
 O + 'src/middleware/rbac.ts': 'df26ceecac323f8b9c0ae4b99ea0c2bfb0436c0c',
 O + 'src/originate.openapi.ts': '2d1b48a0c7ea93521d553cc28ccb53b4fe3fd19c',
 O + 'src/__tests__/helpers/sharedModuleMock.ts': '9645a3d1df053e11122012f23304daad0c9496ca',
 O + 'src/__tests__/ks1202-a-mismatched-data-documenttype-is-refused.test.ts': 'ada07f0536ad003754cb2a08f514fc04f8996b27',
 O + 'src/testUtils/uuid-cjs.ts': None,
 O + 'package.json': '749912c592e8630fff348cc60e1bf49677c18ab1',
 O + 'jest.config.js': '735183662feea56d39f664eb6379cae1a2eec957',
 O + 'tsconfig.json': 'd1b46ece71ad5b2559ccad3648c23a5231e43b09',
 'docs/openapi/secuura-api.yaml': '122d3a2f84cf77bf2b7e2dc51489a0d5f823db1f',
 'eslint.config.mjs': '8c5374c6022eb0a3f449f41a570db61294aa63f1',
}
PIN[O + 'src/testUtils/uuid-cjs.ts'] = rp(MB + ':' + D + O + 'src/testUtils/uuid-cjs.ts')
T1213 = O + 'src/__tests__/ks1213-a-derived-writer-relabel-is-refused.test.ts'
LANDED = {O + 'src/routes/documents.ts': 'e3eeb5a6873d1edd7cae0d1c2b1eb2410faedb77', O + 'src/routes/certifications.ts': '20934ee94abdb0c406df06a9f6025b2d989d4dbd',
          T1213: '8082826898c21c20822001ecaadbe998a818c144'}
bad = []
for p, b in PIN.items():
    at_mb, at_h = rp(MB + ':' + D + p), rp(H + ':' + D + p)
    if not b or at_mb != b: bad.append(('develop blob', p, b, at_mb))
    if p not in LANDED and at_h != b: bad.append(('head blob differs for an untouched file', p, b, at_h))
for p, b in LANDED.items():
    if rp(H + ':' + D + p) != b or rp(FIX + ':' + D + p) != b: bad.append(('landed blob', p, b, rp(H + ':' + D + p), rp(FIX + ':' + D + p)))
if rp(H + '^{tree}') != HT: bad.append(('head tree', rp(H + '^{tree}')))
if rp(H + '^2') != MB: bad.append(('head second parent', rp(H + '^2')))
p = subprocess.run(['git', '-C', REPO, 'cat-file', '-e', MB + ':' + D + T1213], capture_output=True); print('ks1213 test ABSENT at develop (cat-file -e rc != 0):', p.returncode != 0)
if p.returncode == 0: bad.append(('ks1213 test present at develop',))
print('pinned blobs re-read from the repo (develop 75ad0e55c; head = develop for the %d untouched; the 3 PR files at fix = head):' % (len(PIN) - 2), 'OK' if not bad else bad)
if bad: print('REFUSING: pins disagree with the repo; nothing written'); sys.exit(1)
def cut(start, end_incl):
    assert s.count(start) == 1, ('cut start', start[:60], s.count(start))
    i = s.index(start); j = s.index(end_incl, i) + len(end_incl); return s[i:j]
REPORT_DIR = '/Volumes/DevMASTER/!CODING/Testing Agent MAIN/projects/secuura/reports/2026-09-17-ks1213-1031-be8596a29-tier1-r1/'
PRIOR = '/Volumes/DevMASTER/!CODING/Testing Agent MAIN/projects/secuura/reports/2026-09-17-ks1202-1024-d1a328088-tier1-r1/'
OLD_REPORT = '/Volumes/DevMASTER/!CODING/Testing Agent MAIN/projects/secuura/reports/2026-09-17-ks744-1028-e39521cfb-tier1-r1/'
OLD_PRIOR = '/Volumes/DevMASTER/!CODING/Testing Agent MAIN/projects/secuura/reports/2026-09-17-ks1207-1023-2f74491eb-tier1-r1/'
assert os.path.isdir(PRIOR), 'prior report dir missing'
HEADER_OLD = cut('# launch_qa_secuura_ks744_1028.sh', "# Exit: 0 launched (or guards passed under --check) · 2..25 a guard refused\n")
HEADER_NEW = """# launch_qa_secuura_ks1213_1031.sh — cross-project QA agent, ONE TIER 1 ROUND 1 gate over Secuura/Blockchain PR #1031 (KS-1213, Seat A)
# @ be8596a29af15477cb0cbf4b8684e35e63c38e9f — the four derived-document writers of originate refuse, 400 BAD_REQUEST before any write, a caller type that
# differs from the type they store: POST /api/documents/:id/version, /:id/sign-cert and /:id/sign-wallet compare metadata.documentType with source.type;
# POST /api/certifications/issue with parentDocumentId compares data.documentType with type || verification_certificate. The change commit 450e3429d (parent
# 19f1e5475): documents.ts +15, certifications.ts +10, the ks1213 test +226 (85 cells). be8596a29 = a merge of develop 75ad0e55c into 450e3429d; tree 75ed56fb4
# = merge-tree 450e3429d x 75ad0e55c in the drafter clone; the merge brought exactly develop 19f1e5475..75ad0e55c (14 files, patch-id equal, none under
# originate/src). TIER 1: the served type decides the verify-gate level and the connector allow-list outcome (#1024 gate N-A, KS-1213).
#
# THE SHAPE, as read 21:15-21:3x AEST 2026-09-17 (git ls-remote + the PR, compare and contents APIs agree): develop 75ad0e55c is the head merge-base AND its
# second parent, so compare develop...head = merge_base 75ad0e55c, ahead 2, files 3 (asserted, exit 10; behind NOT asserted).
#
# The develop pin is judged by CONTENT — PATH BLOBS — never by develop's SHA: (a) EIGHTEEN files by blob at the CURRENT develop — the PR three (originate
# routes/documents.ts de9b5ae25, routes/certifications.ts 59bfe1c62, the ks1213 test ABSENT; at a #1031 blob -> exit 19 LANDED), and what the gate runs and
# reads: repositories/documentRepo.ts (fromDbRow: the served spread) and certificationRepo.ts (saveCertification), services/provenance.ts (the onBehalfOf
# path ahead of the /version guard), index.ts, middleware auth.ts + rbac.ts, originate.openapi.ts, the KS-1061 sharedModuleMock helper, the ks1202 create-guard
# test, testUtils/uuid-cjs.ts, originate package.json / jest.config.js / tsconfig.json, docs/openapi/secuura-api.yaml, Dev eslint.config.mjs — any blob nobody
# pinned -> exit 18; (b) if develop moved past 75ad0e55c, the compare pinned...develop REFUSES (exit 18) when the delta touches a GUARDED path —
# services/originate/src/ and its package.json / jest.config.js / tsconfig.json, packages/shared/src/, docs/openapi/, eslint.config.mjs — or the move cannot be
# judged. WHY these paths: they are the code and configuration the gate runs in-process (originate routers, repositories, provenance, the shared helpers the
# routes import) and the spec it reads; a develop merge elsewhere (api-gateway, auth, frontends, audit baselines, lockfiles: the gate farms node_modules from the
# checkout install) cannot change what the gate measures, so it must not refuse. DEV_CONTENT_ALLOWED is EMPTY. Open PR #995 edits originate src/index.ts: if it
# lands first this REFUSES by design — re-pin deliberately.
#
# exit 21: the LAUNCH path refuses when stdin is not a TTY. This launcher execs an interactive agent; run it in a cockpit
# pane, never inside a Bash tool — and never run it without --check to "prove" this guard. `--check` runs headless (it launches nothing).
# exit 22: the prompt must require node_modules farmed PER ENTRY (the #1009 gate R-6: a wholesale link can write through to the checkout .vite).
# exit 23: the prompt must carry the exact #1031 verdict subject and name coagent@ as the sender and wednesday-agent@ as the recipient.
# exit 24: brief AND prompt must name the REPORT DIRECTORY and the PRIOR REPORT (#1024, KS-1202: its N-A is this ticket; the QA agent has no inbox), and the
#          prompt must name NOT-TESTED.written-first.md (written FIRST, before any run).
# exit 25: brief AND prompt must carry the MERGE ADDENDUM and require the per-finding CLOSED / STILL OPEN / NEW disposition.
# QA1031_CUR_DEV (test override, --check only): stands in for origin develop so the LANDED / GUARDED refusals can be proven.
# QA1031_DOCS_FILE (test fixture, --check only): a local file stands in for develop originate routes/documents.ts (its git blob) so the LANDED and GUARDED
# arms can be proven without a real develop commit.
# A launch with any QA1031_* override or fixture set refuses (exit 16).
#
# Generated by gatesets/2026-09-17_gate1031/gen_launcher_1031.py from launch_qa_secuura_ks744_1028.sh (asserted substitutions + pins re-read from the repo +
# residual guard + output controls + bash -n): same guard set and exit codes 2..25 (19 = LANDED), re-pointed at #1031 ROUND 1, no content-cleared blob.
#
# Usage: launch_qa_secuura_ks1213_1031.sh [--check]
# Exit: 0 launched (or guards passed under --check) · 2..25 a guard refused
"""
JUDGED_OLD = cut('AU = G + "src/middleware/auth.ts"\n', 'content_cleared = set()\n')
def key(p_):
    return ('O + "' + p_[len(O):] + '"') if p_.startswith(O) else ('D + "' + p_ + '"')
rows = ['  DOCS:' + ' ' * 65 + '({"' + PIN[O + 'src/routes/documents.ts'] + '": DV}, {"' + LANDED[O + 'src/routes/documents.ts'] + '": "#1031 own"}),',
        '  O + "src/routes/certifications.ts":' + ' ' * 38 + '({"' + PIN[O + 'src/routes/certifications.ts'] + '": DV}, {"' + LANDED[O + 'src/routes/certifications.ts'] + '": "#1031 own"}),',
        '  O + "src/__tests__/ks1213-a-derived-writer-relabel-is-refused.test.ts": ({"ABSENT": DV}, {"' + LANDED[T1213] + '": "#1031 own"}),']
for p_, b_ in PIN.items():
    if p_ in LANDED: continue
    k = key(p_); rows.append('  %s:%s({"%s": DV}, {}),' % (k, ' ' * max(1, 70 - len(k)), b_))
JUDGED_NEW = ('O = D + "services/originate/"\nDOCS = O + "src/routes/documents.ts"\nDV = "develop"\n'
              '# file -> (develop-OK blobs {blob: label}, LANDED blobs {blob: label}); ABSENT = the contents API answers 404 at develop\nJUDGED = {\n' + '\n'.join(rows) +
              '\n}\n# No REGION judgement: every file is judged by exact blob (a develop move of documents.ts or certifications.ts refuses, exit 18).\ncontent_cleared = set()\n')
G_DEF_OLD = 'G = D + "services/api-gateway/"\n'
GUARD_OLD = cut('GUARDED = [G + "src/",\n', 'DEV_CONTENT_ALLOWED = {} if os.environ.get("QA1028_LOCK_ALLOW_OFF") else {D + "package-lock.json": {"4831bf2074779139926fbfda3f872c404eba177f": "#1027 dev-dep lock bumps, content-cleared by the drafter"}}\n')
GUARD_NEW = '''GUARDED = [O + "src/",
           O + "package.json",
           O + "jest.config.js",
           O + "tsconfig.json",
           D + "packages/shared/src/",
           D + "docs/openapi/",
           D + "eslint.config.mjs"]
# STYLE NOTE (912r2 launcher, measured): bash scans quote/paren state THROUGH this heredoc because it sits inside a
# command substitution — keep apostrophes and parentheses EVEN (this block uses none of the former), or the outer $( ) breaks.
# CONTENT-JUDGED allowlist: EMPTY. No lockfile is guarded: the gate farms node_modules from the checkout install. Re-pin deliberately.
DEV_CONTENT_ALLOWED = {}
'''
OKLINE_OLD = cut('print("OK " + state + " | origin develop MOVED %s -> %s', 'sys.exit(0)\n')
OKLINE_NEW = 'print("OK " + state + " | origin develop MOVED %s -> %s: commits=%d files=%d — GUARDED hits %d — disjoint from the GUARDED list (services/originate/src/ + its package.json / jest.config.js / tsconfig.json, packages/shared/src/, docs/openapi/, eslint.config.mjs); %s" % (pinned, cur, c["ahead_by"], len(files), len(hits), tail)); sys.exit(0)\n'
REPL = [
 ('header', HEADER_OLD, HEADER_NEW, 1),
 ('brief var', 'BRIEF="${QA1028_BRIEF:-$WED/2_Project_Files/fleet/qa-agent/briefs/2026-09-17_secuura-1028-ks744-tier1.md}"', 'BRIEF="${QA1031_BRIEF:-$WED/2_Project_Files/fleet/qa-agent/briefs/2026-09-17_secuura-1031-ks1213-tier1.md}"', 1),
 ('prompt var', 'PROMPT_FILE="${QA1028_PROMPT:-$WED/2_Project_Files/fleet/qa-agent/briefs/2026-09-17_secuura-1028-ks744-tier1.prompt.txt}"', 'PROMPT_FILE="${QA1031_PROMPT:-$WED/2_Project_Files/fleet/qa-agent/briefs/2026-09-17_secuura-1031-ks1213-tier1.prompt.txt}"', 1),
 ('branch', "BRANCH='refs/heads/feature/ks-744-gateway-500s-on-every-proxied-route-for-a-token-lacking'", "BRANCH='refs/heads/feature/ks-1213-derived-document-writers-still-relabel-the-served-type-post'", 1),
 ('head var', 'HEAD_SHA="${QA1028_HEAD:-e39521cfb54cb5fd47c6bdae64ce707b3c9befce}"', 'HEAD_SHA="${QA1031_HEAD:-' + H + '}"', 1),
 ('merge-base', "MERGE_BASE='19f1e54750ce2b65312a687add2db4f5628edb7d'   # the merge-base of the head with develop, the second parent of the head merge e39521cfb (#1025s squash)",
  "MERGE_BASE='" + MB + "'   # the merge-base of the head with develop = develop itself (#1026s squash), the second parent of the head merge be8596a29", 1),
 ('develop', "DEVELOP_SHA='19f1e54750ce2b65312a687add2db4f5628edb7d'   # the pin = the merge-base; develop was 75ad0e55c at draft close (moves judged by CONTENT: git ls-remote 21:07:47; compare API 20:42 AEST)",
  "DEVELOP_SHA='" + MB + "'   # the pin = the merge-base = develop at drafting (moves judged by PATH BLOB and GUARDED paths, never by this SHA: git ls-remote 21:15:12; compare API 21:26:53 AEST)", 1),
 ('report dirs', "REPORT_DIR='" + OLD_REPORT + "'\nPRIOR_REPORT='" + OLD_PRIOR + "'\n", "REPORT_DIR='" + REPORT_DIR + "'\nPRIOR_REPORT='" + PRIOR + "'\n", 1),
 ('real brief', 'REAL_BRIEF="$WED/2_Project_Files/fleet/qa-agent/briefs/2026-09-17_secuura-1028-ks744-tier1.md"', 'REAL_BRIEF="$WED/2_Project_Files/fleet/qa-agent/briefs/2026-09-17_secuura-1031-ks1213-tier1.md"', 1),
 ('head refuse', 'REFUSING: #1028 — $HEAD_SHA', 'REFUSING: #1031 — $HEAD_SHA', 1),
 ('compare comment', '# develop...#1028 = 19f1e5475 ahead 3 files 2 (behind 2 at draft close; behind deliberately not asserted).', '# develop...#1031 = 75ad0e55c ahead 2 files 3 (behind 0 at draft close; behind deliberately not asserted).', 1),
 ('compare assert', '''[ "$COMPARE" = "$MERGE_BASE ahead=3 files=2" ] || { echo "REFUSING: #1028 develop...head reads '$COMPARE', brief pins '$MERGE_BASE ahead=3 files=2'" >&2; exit 10; }''',
                    '''[ "$COMPARE" = "$MERGE_BASE ahead=2 files=3" ] || { echo "REFUSING: #1031 develop...head reads '$COMPARE', brief pins '$MERGE_BASE ahead=2 files=3'" >&2; exit 10; }''', 1),
 ('cur dev', 'CUR_DEV="${QA1028_CUR_DEV:-', 'CUR_DEV="${QA1031_CUR_DEV:-', 1),
 ('develop comment 2', '# The develop pin, judged by CONTENT (see the header): twenty-three files by blob at the CURRENT develop (no region judgement), then',
                       '# The develop pin, judged by CONTENT (see the header): eighteen files by PATH BLOB at the CURRENT develop (no region judgement), then', 1),
 ('gateway def', G_DEF_OLD, '', 1),
 ('judged', JUDGED_OLD, JUDGED_NEW, 1),
 ('fixture env', '    fixture = os.environ.get("QA1028_AUTH_FILE", "") if f == AU else ""\n', '    fixture = os.environ.get("QA1031_DOCS_FILE", "") if f == DOCS else ""\n', 1),
 ('landed msg', '" — #1028 has landed; this brief is stale"', '" — #1031 has landed; this brief is stale"', 1),
 ('ok pinned', '" (= the head merge-base, an ANCESTOR of the head: merged tree = the head tree b61ed17766d282009b707053cbac6b5961076a0f; git ls-remote)"',
               '" (= the head merge-base, an ANCESTOR of the head: merged tree = the head tree ' + HT + '; git ls-remote)"', 1),
 ('guarded', GUARD_OLD, GUARD_NEW, 1),
 ('tail', 'tail = "the gate merges the then-current develop onto e39521cfb in its own clone, asserts the merged api-gateway and shared subtrees equal the head, or re-runs the missing-claim contract rows, the tamper table and the suites on the MERGED tree; names the merged-tree OID (brief items 1, 3, 4, 5)"',
          'tail = "the gate merges the then-current develop onto be8596a29 in its own clone, asserts the merged originate and shared subtrees equal the head, or re-runs the writer contract rows, the tamper table and the suites on the MERGED tree; names the merged-tree OID (brief items 1, 3, 4, 7)"', 1),
 ('ok moved line', OKLINE_OLD, OKLINE_NEW, 1),
 ('subject', '''grep -qF '[QA -> Wednesday] TIER 1 GATE #1028 (KS-744) e39521cfb' "$PROMPT_FILE"''', '''grep -qF '[QA -> Wednesday] TIER 1 GATE #1031 (KS-1213) be8596a29' "$PROMPT_FILE"''', 1),
 ('subject msg', 'REFUSING: prompt does not carry the exact #1028 verdict subject', 'REFUSING: prompt does not carry the exact #1031 verdict subject', 1),
 ('exit24 msg', 'and the PRIOR REPORT $PRIOR_REPORT (#1023 on the same file, merged into this head), or the prompt does not name NOT-TESTED.written-first.md — the QA agent has no inbox',
                'and the PRIOR REPORT $PRIOR_REPORT (#1024, KS-1202: its N-A is this ticket), or the prompt does not name NOT-TESTED.written-first.md — the QA agent has no inbox', 1),
 ('check head', 'echo "  head on origin: #1028 $HEAD_SHA at $BRANCH"', 'echo "  head on origin: #1031 $HEAD_SHA at $BRANCH"', 1),
 ('check compare', 'echo "  compare (GitHub API): develop...#1028 = $COMPARE"', 'echo "  compare (GitHub API): develop...#1031 = $COMPARE"', 1),
 ('check subject', 'echo "  prompt carries the exact #1028 verdict subject, coagent@ sender, wednesday-agent@ recipient"\n  echo "  brief and prompt name the report directory and the #1023 PRIOR REPORT (same file); prompt names NOT-TESTED.written-first.md"\n',
                   'echo "  prompt carries the exact #1031 verdict subject, coagent@ sender, wednesday-agent@ recipient"\n  echo "  brief and prompt name the report directory and the #1024 PRIOR REPORT (KS-1202 N-A); prompt names NOT-TESTED.written-first.md"\n', 1),
 ('check fixture echo', '  [ -n "${QA1028_CUR_DEV:-}" ] && echo "  (develop read from the QA1028_CUR_DEV test override, not ls-remote)"\n  [ -n "${QA1028_AUTH_FILE:-}" ] && echo "  (develop middleware/auth.ts read from the QA1028_AUTH_FILE fixture, not the contents API)"\n  [ -n "${QA1028_LOCK_ALLOW_OFF:-}" ] && echo "  (QA1028_LOCK_ALLOW_OFF test hook: the lockfile allowlist is EMPTY)"\n',
  '  [ -n "${QA1031_CUR_DEV:-}" ] && echo "  (develop read from the QA1031_CUR_DEV test override, not ls-remote)"\n  [ -n "${QA1031_DOCS_FILE:-}" ] && echo "  (develop originate routes/documents.ts read from the QA1031_DOCS_FILE fixture, not the contents API)"\n', 1),
 ('exit16 fixture', '[ -z "${QA1028_BRIEF:-}${QA1028_PROMPT:-}${QA1028_HEAD:-}${QA1028_CUR_DEV:-}${QA1028_AUTH_FILE:-}${QA1028_LOCK_ALLOW_OFF:-}" ]', '[ -z "${QA1031_BRIEF:-}${QA1031_PROMPT:-}${QA1031_HEAD:-}${QA1031_CUR_DEV:-}${QA1031_DOCS_FILE:-}" ]', 1),
]
badn = 0
for label, old, new, want in REPL:
    n = s.count(old)
    if n != want: print('ANCHOR COUNT', label, n, '!=', want); badn += 1; continue
    s = s.replace(old, new); print('  ok', label, n)
if badn: print('REFUSING: %d anchors disagreed; nothing written' % badn); sys.exit(1)
BODY = s.replace(HEADER_NEW, '')
RESID = ['QA1028_', 'e39521cfb', '19f1e5475', 'b61ed1776', 'KS-744', '#1028', 'ks744', 'api-gateway', 'AU = ', 'AUTH_FILE', 'LOCK_ALLOW_OFF', '4831bf207', '#1023', 'twenty-three',
         'missing-claim', 'secuura-1028', 'b8fce678a', 'trustHeaders', 'G + "']
res = {t: BODY.count(t) for t in RESID if t in BODY}
if res: print('REFUSING: residual tokens in the body', res, [l[:120] for l in BODY.splitlines() if any(t in l for t in res)][:6]); sys.exit(2)
CTL = {H: 2, MB: 2, HT: 1, REPORT_DIR: 1, PRIOR: 1, '"$PRIOR_REPORT"': 2, 'ahead=2 files=3': 2, 'QA1031_DOCS_FILE': 5, 'QA1031_CUR_DEV': 5,
       ': DV}': 18, "grep -q 'ROUND 1'": 2, 'content_cleared': 2, 'DEV_CONTENT_ALLOWED = {}': 1, '#1031 own': 3,
       'CLOSED / STILL OPEN / NEW': None, 'MERGE ADDENDUM': None, 'NOT-TESTED.written-first.md': None, 'exit 19': None, 'exit 21': None, 'exit 22': None,
       'exit 23': None, 'exit 24': None, 'exit 25': None, 'exit 16': None, '[QA -> Wednesday] TIER 1 GATE #1031 (KS-1213) be8596a29': 1, 'packages/shared/src/': None,
       'briefs/2026-09-17_secuura-1031-ks1213-tier1.md': 2, 'briefs/2026-09-17_secuura-1031-ks1213-tier1.prompt.txt': 1, '[ -t 0 ]': 1,
       'exec claude --dangerously-skip-permissions --model opus': 1}
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
