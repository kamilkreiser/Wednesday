#!/usr/bin/env python3
"""gen_launcher_1037.py — derive launchers/launch_qa_secuura_ks1101_1037.sh from launchers/launch_qa_secuura_ks1215_1034.sh (the launcher that ran cleanly
this morning: same guard set, blob-judged develop arm, GUARDED compare arm, exit 26) by ASSERTED substitutions: every anchor must occur exactly as often as
stated, or the generator refuses and writes nothing. Shape follows gen_launcher_1034.py (pins RE-READ from the repo rather than copied, tmp file, bash -n on
the tmp, then os.replace; .pre-* copy if the output exists).

Re-points at #1037 (KS-1101) ROUND 1, TIER 1: head f87506f47, merge-base / head second parent 34cdcfb26, and the CURRENT develop a105cd32b. DEVELOP MOVED TWICE
during drafting: 34cdcfb26 (the READY mail) -> f6669623c (#1032 KS-1194) -> a105cd32b (#1034 KS-1215, merged while this generator was being written). The
develop pin is RE-READ every run, never copied from the READY mail, per Kam's 2026-09-22 standing rule — and the FIRST generated launcher refused with
exit 18 on exactly that second move, which is the guard working, not a defect.
The develop arm judges TWENTY api-gateway / frontend / script / lint files by PATH BLOB at the CURRENT develop — never by develop's SHA (health.ts
f43052734, the ks1101 test ABSENT; at their #1037 blobs -> exit 19 LANDED). On a develop move the compare pinned...current REFUSES (exit 18) when it touches
services/api-gateway/src/ or its package.json / vitest.config.ts / vitest.setup.ts / tsconfig.json, frontend/admin/src/ or its tsconfig.json / package.json,
frontend/status/, scripts/smoke-test.sh or eslint.config.mjs. DEV_CONTENT_ALLOWED is EMPTY.

TWO DELIBERATE DIFFERENCES FROM THE #1034 LAUNCHER, both stated rather than implied:
 (a) This gate has NO separate brief .md. Its source document is the seat's READY FOR QA mail, gatesets/2026-09-18_gate1037/mail_1037_ready.md, and BRIEF
     points at it. Three cross-document assertions survive and are real: TIER 1 in both (exit 7), the head SHA in both (exit 20), and the NEW exit 27 — the
     READY mail AND the prompt must BOTH name the three findings the seat declared and did NOT fix. The requirements that only Wednesday can state (report
     directory, prior report, MERGE ADDENDUM, CLOSED / STILL OPEN / NEW, the signed-GO merge authority, ROUND 1) are asserted against the PROMPT alone,
     because the seat's mail cannot be expected to carry them and a grep that can never fail is not an assertion.
 (b) packages/shared/ is NOT judged and NOT guarded. Measured, not assumed: services/health.ts imports only config/services, middleware/auth and db, all
     in-gateway. A shared-package move cannot change what this gate measures, and a guard that refuses for nothing gets routed around.

Residual guard, output controls, heredoc parity, no git write verb in the checkout, no control bytes, bash -n.
The merged-tree OID is RE-DERIVED here (read-only) in a throwaway bare repo whose objects/info/alternates points at the checkout: nothing is ever written
into the Secuura repo.
Usage: gen_launcher_1037.py <template launcher> <output launcher>   Exit: 0 written · 1 anchor/control/pin disagreed · 2 residual token · 3 bash -n failed"""
import hashlib, os, re, shutil, subprocess, sys, tempfile
TPL, OUT = sys.argv[1], sys.argv[2]
s = open(TPL).read()
def now(f='+%Y-%m-%d %H:%M:%S %Z'): return subprocess.run(['date', f], capture_output=True, text=True).stdout.strip()
print('gen_launcher_1037', now(), '| template sha256', hashlib.sha256(s.encode()).hexdigest()[:16], 'lines', s.count('\n'))

REPO = '/Volumes/DevMASTER/!CODING/Secuura/Blockchain/2_Project_Files'
H   = 'f87506f476ce83fbbc006e9f84d22454053126ad'   # #1037 head
MB  = '34cdcfb2663b9e4c31025044e6f842ad2c5a10a3'   # merge-base = the head's second parent = develop when the seat pushed
DEV = 'a105cd32b1ed9c6927ae6e797f8259224d8480c6'   # CURRENT develop, RE-READ 10:25:39 AEST after #1034 KS-1215 merged mid-draft
HT  = '4f7ce40b44330cef7a47747319feda569c03967a'   # head tree
P1  = '7f10aa1d8afc3d524562bc2796c75cd57b1f5c68'   # head first parent
MERGED = '6e8e62231f1454268a35292b8a279fbc6faa4d9b'  # merge-tree H x DEV, re-derived below
D = 'Blockchain/Dev/'; A = 'services/api-gateway/'
T1101 = A + 'src/__tests__/ks1101-health-aggregates-surface-degraded.test.ts'
rp = lambda x: subprocess.run(['git', '-C', REPO, 'rev-parse', '--verify', '-q', x], capture_output=True, text=True).stdout.strip()

# path relative to Blockchain/Dev -> blob at the CURRENT develop a105cd32b (develop-OK). Re-read and asserted below, never copied.
PIN = {
 A + 'src/services/health.ts':        'f43052734a10d0b891db11b49aa49b08f66c1ea8',
 # the three files #1034 (KS-1215) put into develop AFTER this head's merge-base: develop is ahead of the head here, by design.
 A + 'src/middleware/auth.ts':        'bf09d315a64443b7f02bc27a74366b7a7f1dae81',
 A + 'src/routes/platform.ts':        'b80a8cd8d4e1af5a944817227f5ee6612c793954',
 A + 'src/__tests__/ks1215-the-connector-branch-never-carries-the-callers-bearer.test.ts': '75006b5cf50fb8b42a5e7588a1d622b9168c1b07',
 A + 'src/routes/system-status.ts':   '956083916a7a1a0bbf16252017cbe8f5f90f6436',
 A + 'src/routes/health-dashboard.ts':'94a1c8063eb71a9ebf0b00eed09bb567806a47a6',
 'frontend/admin/src/services/api.ts':'bd8ddb32fd5b778aeb5b4fd109e65464fb3cf2ae',
 'frontend/status/index.html':        '714fcac6c915fae88d46ce43b9f228859416a6ec',
 A + 'src/index.ts':                  'db127dbfa5dd899b0a8e0d844690890d91e27f10',
 A + 'src/config/services.ts':        '6110888aac8c834c291b5385710943f9b6adf57b',
 A + 'src/db.ts':                     '9144c532bca9911da6cedd569e575c5aa6bc6c52',
 A + 'package.json':                  '841d8c6adcd71e885c01e65c22da9418daff276a',
 A + 'vitest.config.ts':              '5888e0b320d934f6f434e0e5ca3c74a995cecc02',
 A + 'vitest.setup.ts':               '22c1107683b8192df3bfd3e929aa94aff3dc7d45',
 A + 'tsconfig.json':                 'c981e6a92fdd2417fa35070eb979c5f1c77ffbcd',
 'scripts/smoke-test.sh':             'd5d34357a0e4dd36d1ed951367a9ee189a337214',
 'frontend/admin/tsconfig.json':      '08cdcb2c535d7086d61f4df504ce3cc6202e8534',
 'frontend/admin/package.json':       'a7fd91ccf3a553d7a2d619caf9cfd4de7ea9d7ac',
 'eslint.config.mjs':                 '8c5374c6022eb0a3f449f41a570db61294aa63f1',
}
# the six files #1037 changes -> their blob AT THE HEAD (a develop that ever reads one of these means #1037 landed: exit 19)
LANDED = {
 A + 'src/services/health.ts':         '7bedc074583d816d997bd6d679043db010804aed',
 A + 'src/routes/system-status.ts':    'bd0aca9028ecebeeca98540e693781d6dd76693f',
 A + 'src/routes/health-dashboard.ts': '95114beac3fb04d5d2aa0328c119d15fd00f0f04',
 T1101:                                'e03f600d51d441ca42aff15d92e8391bcc66e2cb',
 'frontend/admin/src/services/api.ts': 'f456616177cfabfa3df127d55133fb05e94741d3',
 'frontend/status/index.html':         'b23554a126103c63e1f434dc47c9f0e3bf8bb214',
}
# Files where DEVELOP IS AHEAD of the head: #1034 (KS-1215) merged into develop at a105cd32b AFTER this head's merge-base 34cdcfb26, so these three read
# their pre-#1034 value at the head and their #1034 value at develop. Asserted on BOTH sides rather than skipped — a difference nobody named is the bug.
T1215 = A + 'src/__tests__/ks1215-the-connector-branch-never-carries-the-callers-bearer.test.ts'
DEV_AHEAD = {
 A + 'src/middleware/auth.ts': '6e16683624b3c38a365ece44cccb4fdfac892c71',   # at the HEAD (pre-#1034)
 A + 'src/routes/platform.ts': '4550401f8d7d76afa848855cdf7558a35fd02de0',   # at the HEAD (pre-#1034)
 T1215:                        'ABSENT',                                     # #1034's test does not exist at this head
}
bad = []
for p, b in PIN.items():
    at_dev = rp(DEV + ':' + D + p)
    at_h = rp(H + ':' + D + p) or 'ABSENT'
    if at_dev != b: bad.append(('develop blob', p, b, at_dev))
    if p in LANDED:
        continue                                            # checked below against the head
    elif p in DEV_AHEAD:
        if at_h != DEV_AHEAD[p]: bad.append(('head blob for a develop-ahead file', p, DEV_AHEAD[p], at_h))
        if at_h == at_dev: bad.append(('develop-ahead file is NOT ahead — #1034 may have been reverted', p, at_dev))
    elif at_h != b:
        bad.append(('head blob differs for an untouched file', p, b, at_h))
for p, b in LANDED.items():
    if rp(H + ':' + D + p) != b: bad.append(('landed blob at head', p, b, rp(H + ':' + D + p)))
if rp(H + '^{tree}') != HT: bad.append(('head tree', rp(H + '^{tree}'), HT))
if rp(H + '^1') != P1: bad.append(('head first parent', rp(H + '^1'), P1))
if rp(H + '^2') != MB: bad.append(('head second parent', rp(H + '^2'), MB))
if rp(DEV + '^{commit}') != DEV: bad.append(('develop not a commit', DEV))
q = subprocess.run(['git', '-C', REPO, 'cat-file', '-e', DEV + ':' + D + T1101], capture_output=True)
print('ks1101 test ABSENT at develop (cat-file -e rc != 0):', q.returncode != 0)
if q.returncode == 0: bad.append(('ks1101 test present at develop',))
mbase = subprocess.run(['git', '-C', REPO, 'merge-base', DEV, H], capture_output=True, text=True).stdout.strip()
print('merge-base(develop, head) re-read:', mbase, '== MB', mbase == MB)
if mbase != MB: bad.append(('merge-base', mbase, MB))
print('pinned blobs re-read from the repo (develop %s for all %d; head = develop for the %d untouched; %d develop-AHEAD via #1034; the %d PR files at the head):'
      % (DEV[:9], len(PIN), len(PIN) - 5 - len(DEV_AHEAD), len(DEV_AHEAD), len(LANDED)), 'OK' if not bad else bad)
if bad: print('REFUSING: pins disagree with the repo; nothing written'); sys.exit(1)

# Re-derive the merged tree READ-ONLY: a throwaway bare repo that borrows the checkout's objects via alternates. Nothing is written into the Secuura repo.
tmpr = tempfile.mkdtemp(prefix='gen1037-mt-')
subprocess.run(['git', 'init', '--bare', '-q', tmpr], check=True)
open(os.path.join(tmpr, 'objects', 'info', 'alternates'), 'w').write(REPO + '/.git/objects\n')
for ref, sha in (('refs/heads/h', H), ('refs/heads/d', DEV)):
    subprocess.run(['git', '-C', tmpr, 'update-ref', ref, sha], check=True)
mt = subprocess.run(['git', '-C', tmpr, 'merge-tree', '--write-tree', '--name-only', 'd', 'h'], capture_output=True, text=True)
lines = mt.stdout.strip().split('\n')
print('merge-tree rc', mt.returncode, '| merged tree', lines[0] if lines else '(none)', '| conflicted paths', max(0, len(lines) - 1))
shutil.rmtree(tmpr, ignore_errors=True)
if mt.returncode != 0 or len(lines) != 1 or lines[0] != MERGED:
    print('REFUSING: the merge of the head against the CURRENT develop is not the clean %s it was measured to be — re-pin deliberately' % MERGED[:9]); sys.exit(1)

def cut(start, end_incl):
    assert s.count(start) == 1, ('cut start', start[:60], s.count(start))
    i = s.index(start); j = s.index(end_incl, i) + len(end_incl); return s[i:j]

WEDB = '$WED/2_Project_Files/fleet/qa-agent/'
READY = WEDB + 'gatesets/2026-09-18_gate1037/mail_1037_ready.md'
PROMPT = WEDB + 'briefs/2026-09-18_secuura-1037-ks1101-tier1.prompt.txt'
REPORT_DIR = '/Volumes/DevMASTER/!CODING/Testing Agent MAIN/projects/secuura/reports/2026-09-18-ks1101-1037-f87506f47-tier1-r1/'
PRIOR      = '/Volumes/DevMASTER/!CODING/Testing Agent MAIN/projects/secuura/reports/2026-09-18-ks1215-1034-e4624218b-tier1-r1/'
OLD_REPORT = '/Volumes/DevMASTER/!CODING/Testing Agent MAIN/projects/secuura/reports/2026-09-18-ks1215-1034-e4624218b-tier1-r1/'
OLD_PRIOR  = '/Volumes/DevMASTER/!CODING/Testing Agent MAIN/projects/secuura/reports/2026-09-17-ks1207-1023-2f74491eb-tier1-r1/'
assert os.path.isdir(PRIOR), 'prior report dir missing: ' + PRIOR
assert os.path.isfile(READY.replace('$WED', '/Volumes/DevMASTER/WEDNESDAY')), 'READY mail missing'
assert os.path.isfile(PROMPT.replace('$WED', '/Volumes/DevMASTER/WEDNESDAY')), 'prompt missing'

HEADER_OLD = cut('# launch_qa_secuura_ks1215_1034.sh', '# Exit: 0 launched (or guards passed under --check) · 2..26 a guard refused\n')
HEADER_NEW = """# launch_qa_secuura_ks1101_1037.sh — cross-project QA agent, ONE TIER 1 ROUND 1 gate over Secuura/Blockchain PR #1037 (KS-1101, Seat A)
# @ f87506f476ce83fbbc006e9f84d22454053126ad — services/api-gateway: the health AGGREGATES show a probed service that answers 2xx {status:degraded} as
# degraded, never as up, on /health/deep, on /system/status and /api/system/status (including the /status/simple body) and on /api/system/health/dashboard.
# READINESS IS UNCHANGED: /health/ready and /status/simple keep their 200 / 503 rules with degraded counted as NOT-down. Shape O-SURFACE, ruled 13:30:57Z.
# Three commits: e4ef504a3 (the O-SURFACE edits + the 11-cell test, on 732c13459) -> 7f10aa1d8 (develop 3961c2add merged in) -> f87506f47 (develop 34cdcfb26
# merged in). Head tree 4f7ce40b4. Six files: services/health.ts, routes/system-status.ts, routes/health-dashboard.ts, the new ks1101 test,
# frontend/admin/src/services/api.ts (servicesOnline counts healthy + degraded) and frontend/status/index.html (the degraded style).
# TIER 1: the gateway health surface every deploy check and dashboard reads. A GO is a gate verdict: #1037 merges on WEDNESDAY'S signed GO naming the head
# (the TESTED grant) and on nothing else (exit 26 guards it).
#
# THE SHAPE, re-read live 10:10:45-10:26:59 AEST 2026-09-18 (git ls-remote + the GitHub compare and PR APIs agree): the head has NOT moved since the seat's
# READY at 16:18:10Z. DEVELOP MOVED TWICE DURING DRAFTING: 34cdcfb26 (the READY mail) -> f6669623c (#1032 KS-1194, three files, all services/auth) ->
# a105cd32b (#1034 KS-1215 MERGED mid-draft; three files, ALL api-gateway src: middleware/auth.ts, routes/platform.ts and the ks1215 test). The FIRST
# generated launcher refused with exit 18 on that second move; this is the re-pin. So the merge-base 34cdcfb26 is the head's second parent but two commits
# behind develop, and compare develop...head = merge_base 34cdcfb26, status diverged, ahead 3, files 6, behind 2 (ahead and files asserted, exit 10; behind
# NOT asserted). MEASURED, not reasoned: 0 shared files between #1037's six and the six develop has added since, and the read-only merge-tree of f87506f47
# against a105cd32b is CLEAN — merged tree 6e8e62231f1454268a35292b8a279fbc6faa4d9b, 0 conflicted paths.
# CONSEQUENCE THE GATE MUST CARRY: the merged tree contains #1034's auth.ts, platform.ts AND its ks1215 test, so the api-gateway suite is 59 test files at
# the head and 59 at develop but SIXTY on the merged tree. A merged-tree run still reporting 59 has not picked #1034 up.
#
# The develop pin is judged by CONTENT — PATH BLOBS — never by develop's SHA: (a) TWENTY files by blob at the CURRENT develop — the PR six (health.ts
# f43052734, system-status.ts 956083916, health-dashboard.ts 94a1c8063, admin api.ts bd8ddb32f, status index.html 714fcac6c, the ks1101 test ABSENT; at a
# #1037 blob -> exit 19 LANDED), and what the gate runs and reads: index.ts (the real mount order for /health/*, /system and /api/system), health.ts's whole
# import closure (config/services.ts, middleware/auth.ts, db.ts), #1034's platform.ts and ks1215 test (develop is AHEAD of the head on those three: each is
# pinned at BOTH ends, so a revert of #1034 refuses too), gateway package.json / vitest.config.ts / vitest.setup.ts / tsconfig.json, scripts/
# smoke-test.sh (finding F-1 lives at line 107), frontend/admin tsconfig.json + package.json (the admin tsc program), Dev eslint.config.mjs — any blob
# nobody pinned -> exit 18; (b) if develop moves past a105cd32b, the compare pinned...develop REFUSES (exit 18) when the delta touches a GUARDED path —
# services/api-gateway/src/ and its package.json / vitest.config.ts / vitest.setup.ts / tsconfig.json, frontend/admin/src/ and its tsconfig.json /
# package.json, frontend/status/, scripts/smoke-test.sh, eslint.config.mjs — or the move cannot be judged. WHY these paths: they are the code and
# configuration the gate runs in-process (the real index.ts app, the health service and its imports), the two consumers the PR also changed, and the smoke
# test finding F-1 is about; a develop merge elsewhere (other services, other frontends, lockfiles) cannot change what the gate measures, so it must not
# refuse. packages/shared/ is deliberately NOT judged and NOT guarded: measured, health.ts imports nothing from it. DEV_CONTENT_ALLOWED is EMPTY.
#
# NO SEPARATE BRIEF. This gate's source document is the seat's READY FOR QA mail (gatesets/2026-09-18_gate1037/mail_1037_ready.md) and BRIEF points at it.
# Three cross-document assertions are real and kept: TIER 1 in both (exit 7), the head SHA in both (exit 20), and exit 27 — the READY mail AND the prompt
# must BOTH name the three findings the seat declared and did NOT fix. The requirements only Wednesday can state (report directory, prior report, MERGE
# ADDENDUM, CLOSED / STILL OPEN / NEW, the signed-GO merge authority, ROUND 1) are asserted against the PROMPT alone: the seat's mail cannot carry them, and
# a grep that can never fail is not an assertion.
#
# exit 21: the LAUNCH path refuses when stdin is not a TTY. This launcher execs an interactive agent; run it in a cockpit
# pane, never inside a Bash tool — and never run it without --check to "prove" this guard. `--check` runs headless (it launches nothing).
# exit 22: the prompt must require node_modules farmed PER ENTRY (the #1009 gate R-6: a wholesale link can write through to the checkout .vite).
# exit 23: the prompt must carry the exact #1037 verdict subject and name coagent@ as the sender and wednesday-agent@ as the recipient.
# exit 24: the prompt must name the REPORT DIRECTORY, the PRIOR REPORT (#1034, KS-1215: the same api-gateway service, gated this morning) and
#          NOT-TESTED.written-first.md (written FIRST, before any run). The QA agent has no inbox.
# exit 25: the prompt must carry the MERGE ADDENDUM and require the per-finding CLOSED / STILL OPEN / NEW disposition.
# exit 26: the prompt must name WEDNESDAY'S signed GO as #1037's merge authority and carry no copied Kam's-tap merge condition (that is #1032's).
# exit 27: the seat's READY mail AND the prompt must BOTH name the three NOT-fixed findings — F-1 scripts/smoke-test.sh:107 (a degraded service now FAILS
#          the smoke test), F-2 /health/services (opt-in, still response.ok only), and the UNMEASURED out-of-repo consumers. The gate exists to grade them.
# QA1037_CUR_DEV (test override, --check only): stands in for origin develop so the LANDED / GUARDED refusals can be proven.
# QA1037_HEALTH_FILE (test fixture, --check only): a local file stands in for develop services/health.ts (its git blob) so the LANDED and GUARDED
# arms can be proven without a real develop commit.
# A launch with any QA1037_* override or fixture set refuses (exit 16).
#
# Generated by gatesets/2026-09-18_gate1037/gen_launcher_1037.py from launch_qa_secuura_ks1215_1034.sh (asserted substitutions + pins re-read from the repo +
# a re-derived merged tree + residual guard + output controls + bash -n): same guard set and exit codes 2..26 (19 = LANDED), plus exit 27, re-pointed at
# #1037 ROUND 1, no content-cleared blob.
#
# Usage: launch_qa_secuura_ks1101_1037.sh [--check]
# Exit: 0 launched (or guards passed under --check) · 2..27 a guard refused
"""

JUDGED_OLD = cut('A = D + "services/api-gateway/"\n', 'content_cleared = set()\n')
def key(p_):
    return ('A + "' + p_[len(A):] + '"') if p_.startswith(A) else ('D + "' + p_ + '"')
rows = ['  HEALTHTS:' + ' ' * 61 + '({"' + PIN[A + 'src/services/health.ts'] + '": DV}, {"' + LANDED[A + 'src/services/health.ts'] + '": "#1037 own"}),']
for p_ in (A + 'src/routes/system-status.ts', A + 'src/routes/health-dashboard.ts', 'frontend/admin/src/services/api.ts', 'frontend/status/index.html'):
    k = key(p_); rows.append('  %s:%s({"%s": DV}, {"%s": "#1037 own"}),' % (k, ' ' * max(1, 70 - len(k)), PIN[p_], LANDED[p_]))
rows.append('  A + "src/__tests__/ks1101-health-aggregates-surface-degraded.test.ts": ({"ABSENT": DV}, {"' + LANDED[T1101] + '": "#1037 own"}),')
for p_, b_ in PIN.items():
    if p_ in LANDED: continue
    k = key(p_); rows.append('  %s:%s({"%s": DV}, {}),' % (k, ' ' * max(1, 70 - len(k)), b_))
JUDGED_NEW = ('A = D + "services/api-gateway/"\nHEALTHTS = A + "src/services/health.ts"\nDV = "develop"\n'
              '# file -> (develop-OK blobs {blob: label}, LANDED blobs {blob: label}); ABSENT = the contents API answers 404 at develop\nJUDGED = {\n'
              + '\n'.join(rows) +
              '\n}\n# No REGION judgement: every file is judged by exact blob (a develop move of health.ts, system-status.ts, health-dashboard.ts, index.ts\n'
              '# or smoke-test.sh refuses, exit 18; a #1037 blob, exit 19).\ncontent_cleared = set()\n')

GUARD_OLD = cut('GUARDED = [A + "src/",\n', 'DEV_CONTENT_ALLOWED = {}\n')
GUARD_NEW = '''GUARDED = [A + "src/",
           A + "package.json",
           A + "vitest.config.ts",
           A + "vitest.setup.ts",
           A + "tsconfig.json",
           D + "frontend/admin/src/",
           D + "frontend/admin/tsconfig.json",
           D + "frontend/admin/package.json",
           D + "frontend/status/",
           D + "scripts/smoke-test.sh",
           D + "eslint.config.mjs"]
# STYLE NOTE (912r2 launcher, measured): bash scans quote/paren state THROUGH this heredoc because it sits inside a
# command substitution — keep apostrophes and parentheses EVEN (this block uses none of the former), or the outer $( ) breaks.
# CONTENT-JUDGED allowlist: EMPTY. No lockfile is guarded: the gate names the vitest version it ran against develops lock. Re-pin deliberately.
# packages/shared/src/ is deliberately absent: measured, health.ts imports only config/services, middleware/auth and db, all in-gateway.
DEV_CONTENT_ALLOWED = {}
'''

OKLINE_OLD = cut('print("OK " + state + " | origin develop MOVED %s -> %s', 'sys.exit(0)\n')
OKLINE_NEW = ('print("OK " + state + " | origin develop MOVED %s -> %s: commits=%d files=%d — GUARDED hits %d — disjoint from the GUARDED list '
              '(services/api-gateway/src/ + its package.json / vitest.config.ts / vitest.setup.ts / tsconfig.json, frontend/admin/src/ + its tsconfig.json / '
              'package.json, frontend/status/, scripts/smoke-test.sh, eslint.config.mjs); %s" % (pinned, cur, c["ahead_by"], len(files), len(hits), tail)); sys.exit(0)\n')

EXIT26_OLD = '''grep -qiF "WEDNESDAY'S signed GO" "$PROMPT_FILE" && grep -qiF "WEDNESDAY'S signed GO" "$BRIEF" && ! grep -qiE "waits for Kam.s tap|on Kam.s tap only" "$PROMPT_FILE" "$BRIEF" \\
  || { echo "REFUSING: brief or prompt does not name WEDNESDAY'S signed GO as the #1034 merge authority, or carries a copied Kam's-tap merge condition (that is #1032's, not this PR's)" >&2; exit 26; }
'''
EXIT26_NEW = '''grep -qiF "WEDNESDAY'S signed GO" "$PROMPT_FILE" && ! grep -qiE "waits for Kam.s tap|on Kam.s tap only" "$PROMPT_FILE" "$BRIEF" \\
  || { echo "REFUSING: prompt does not name WEDNESDAY'S signed GO as the #1037 merge authority, or a copied Kam's-tap merge condition survives (that is #1032's, not this PR's)" >&2; exit 26; }
grep -qF 'scripts/smoke-test.sh:107' "$PROMPT_FILE" && grep -qF '/health/services' "$PROMPT_FILE" && grep -qiF 'out-of-repo consumers' "$PROMPT_FILE" \\
  && grep -qF 'scripts/smoke-test.sh:107' "$BRIEF" && grep -qF '/health/services' "$BRIEF" && grep -qiF 'out-of-repo consumers' "$BRIEF" \\
  || { echo "REFUSING: the seat's READY mail and the prompt do not BOTH name the three NOT-fixed findings (F-1 scripts/smoke-test.sh:107, F-2 /health/services, the UNMEASURED out-of-repo consumers) — the gate exists to grade them" >&2; exit 27; }
'''

REPL = [
 ('header', HEADER_OLD, HEADER_NEW, 1),
 ('brief var', 'BRIEF="${QA1034_BRIEF:-$WED/2_Project_Files/fleet/qa-agent/briefs/2026-09-17_secuura-1034-ks1215-tier1.md}"',
               'BRIEF="${QA1037_BRIEF:-' + READY + '}"', 1),
 ('prompt var', 'PROMPT_FILE="${QA1034_PROMPT:-$WED/2_Project_Files/fleet/qa-agent/briefs/2026-09-17_secuura-1034-ks1215-tier1.prompt.txt}"',
                'PROMPT_FILE="${QA1037_PROMPT:-' + PROMPT + '}"', 1),
 ('branch', "BRANCH='refs/heads/feature/ks-1215-api-gateway-a-revoked-session-jwt-plus-a-valid-key-whose'",
            "BRANCH='refs/heads/feature/ks-1101-gateway-health-aggregates-read-anchorings-http-status-only'", 1),
 ('head var', 'HEAD_SHA="${QA1034_HEAD:-e4624218bc29cda4c07b2d31ca18bba422cfbc3e}"', 'HEAD_SHA="${QA1037_HEAD:-' + H + '}"', 1),
 ('merge-base', "MERGE_BASE='3961c2add8e1637b32e638f8f0952c328c00833e'   # the merge-base of the head with develop = develop itself (#1033s squash), the second parent of the merge 96d859467",
                "MERGE_BASE='" + MB + "'   # the merge-base of the head with develop = the head second parent (#1035s squash; develop when the seat pushed, NOT develop now)", 1),
 ('develop', "DEVELOP_SHA='34cdcfb2663b9e4c31025044e6f842ad2c5a10a3'   # the pin = develop after #1035 landed mid-re-pin (NOT the merge-base 3961c2add; moves judged by PATH BLOB and GUARDED paths: git ls-remote 02:02:48 AEST 2026-09-18)",
             "DEVELOP_SHA='" + DEV + "'   # the pin = develop RE-READ at drafting, after #1032 AND #1034 landed (NOT the merge-base " + MB[:9] + "; moves judged by PATH BLOB and GUARDED paths: git ls-remote 10:25:39 AEST 2026-09-18)", 1),
 ('report dirs', "REPORT_DIR='" + OLD_REPORT + "'\nPRIOR_REPORT='" + OLD_PRIOR + "'\n",
                 "REPORT_DIR='" + REPORT_DIR + "'\nPRIOR_REPORT='" + PRIOR + "'\n", 1),
 ('real brief', 'REAL_BRIEF="$WED/2_Project_Files/fleet/qa-agent/briefs/2026-09-17_secuura-1034-ks1215-tier1.md"', 'REAL_BRIEF="' + READY + '"', 1),
 ('head refuse', 'REFUSING: #1034 — $HEAD_SHA is not at $BRANCH on origin — the head moved; the brief is about a different SHA',
                 'REFUSING: #1037 — $HEAD_SHA is not at $BRANCH on origin — the head moved; a verdict is valid ONLY at its head', 1),
 ('compare comment', '# develop...#1034 = 3961c2add ahead 4 files 3 (behind 0 at the re-pin; behind deliberately not asserted). Drafted at fd81a75f0: 27e53ec3a ahead 2 files 2.',
                     '# develop...#1037 = 34cdcfb26 ahead 3 files 6 (behind 2: develop moved to f6669623c then a105cd32b after the seat pushed; behind deliberately NOT asserted). Compare API 00:25:55Z 2026-09-18.', 1),
 ('compare assert', '''[ "$COMPARE" = "$MERGE_BASE ahead=4 files=3" ] || { echo "REFUSING: #1034 develop...head reads '$COMPARE', brief pins '$MERGE_BASE ahead=4 files=3'" >&2; exit 10; }''',
                    '''[ "$COMPARE" = "$MERGE_BASE ahead=3 files=6" ] || { echo "REFUSING: #1037 develop...head reads '$COMPARE', the gateset pins '$MERGE_BASE ahead=3 files=6'" >&2; exit 10; }''', 1),
 ('cur dev', 'CUR_DEV="${QA1034_CUR_DEV:-', 'CUR_DEV="${QA1037_CUR_DEV:-', 1),
 ('develop comment 2', '# The develop pin, judged by CONTENT (see the header): twenty-four files by PATH BLOB at the CURRENT develop (no region judgement), then — if develop',
                       '# The develop pin, judged by CONTENT (see the header): eighteen files by PATH BLOB at the CURRENT develop (no region judgement), then — if develop', 1),
 ('judged', JUDGED_OLD, JUDGED_NEW, 1),
 ('fixture env', '    fixture = os.environ.get("QA1034_AUTH_FILE", "") if f == AUTHTS else ""\n',
                 '    fixture = os.environ.get("QA1037_HEALTH_FILE", "") if f == HEALTHTS else ""\n', 1),
 ('landed msg', '" — #1034 has landed; this brief is stale"', '" — #1037 has landed; this gateset is stale"', 1),
 ('ok pinned', '" (#1035 squash on the head merge-base 3961c2add, NOT an ancestor of the head: merged tree e4624218b x 34cdcfb26 = f1c78bbb888f5c0f875a7ab11ee09d810126f72a, 0 conflicts, re-pinner; git ls-remote)"',
               '" (#1032 KS-1194 then #1034 KS-1215, 0 #1037 files, NOT an ancestor of the head: merged tree ' + H[:9] + ' x ' + DEV[:9] + ' = ' + MERGED + ', 0 conflicts, drafter merge-tree 00:26:59Z; the merged api-gateway suite gains #1034s ks1215 test, 59 -> 60 files; git ls-remote)"', 1),
 ('guarded', GUARD_OLD, GUARD_NEW, 1),
 ('tail', 'tail = "the gate merges the then-current develop onto e4624218b in its own clone, asserts the merged services/api-gateway/src and shared subtrees equal the head, or re-runs the real-gateway matrix, the tamper table and the suites on the MERGED tree; names the merged-tree OID, re-pinner 34cdcfb26 -> f1c78bbb8 (brief items 1, 3, 5, 6)"',
          'tail = "the gate merges the then-current develop onto ' + H[:9] + ' in its own clone, asserts the merged services/api-gateway/src, frontend/admin/src and frontend/status subtrees equal the head, or re-runs the aggregate census, the readiness matrix, the tamper table and the suites on the MERGED tree; names the merged-tree OID, drafter ' + DEV[:9] + ' -> ' + MERGED[:9] + ' (prompt L0 and items 1, 3, 5, 6); the merged api-gateway suite is 60 test files, not 59"', 1),
 ('ok moved line', OKLINE_OLD, OKLINE_NEW, 1),
 ('round', '''grep -q 'ROUND 1' "$BRIEF" && grep -q 'ROUND 1' "$PROMPT_FILE" || { echo "REFUSING: brief and prompt disagree about the round (ROUND 1)" >&2; exit 15; }''',
           '''grep -q 'ROUND 1' "$PROMPT_FILE" || { echo "REFUSING: prompt does not name ROUND 1 — this gate has no separate brief; its source document is the seat's READY mail, which carries no round" >&2; exit 15; }''', 1),
 ('tier msg', 'REFUSING: brief and prompt disagree about the tier', 'REFUSING: the READY mail and the prompt disagree about the tier', 1),
 ('brief path msg', 'REFUSING: prompt does not name the brief path', "REFUSING: prompt does not name the seat's READY mail path", 1),
 ('head sha msg', 'REFUSING: brief or prompt does not name the head SHA $HEAD_SHA — a gate about another SHA is another gate',
                  'REFUSING: the READY mail or the prompt does not name the head SHA $HEAD_SHA — a gate about another SHA is another gate', 1),
 ('subject', '''grep -qF '[QA -> Wednesday] TIER 1 GATE #1034 (KS-1215) e4624218b' "$PROMPT_FILE"''', '''grep -qF '[QA -> Wednesday] TIER 1 GATE #1037 (KS-1101) f87506f47' "$PROMPT_FILE"''', 1),
 ('subject msg', 'REFUSING: prompt does not carry the exact #1034 verdict subject', 'REFUSING: prompt does not carry the exact #1037 verdict subject', 1),
 ('exit24', '''grep -qF "$REPORT_DIR" "$PROMPT_FILE" && grep -qF "$REPORT_DIR" "$BRIEF" && grep -qF 'NOT-TESTED.written-first.md' "$PROMPT_FILE" && grep -qF "$PRIOR_REPORT" "$PROMPT_FILE" && grep -qF "$PRIOR_REPORT" "$BRIEF" \\
  || { echo "REFUSING: brief or prompt does not name the report directory $REPORT_DIR and the PRIOR REPORT $PRIOR_REPORT (#1023, KS-1207: its N-1 is this ticket), or the prompt does not name NOT-TESTED.written-first.md — the QA agent has no inbox" >&2; exit 24; }''',
            '''grep -qF "$REPORT_DIR" "$PROMPT_FILE" && grep -qF 'NOT-TESTED.written-first.md' "$PROMPT_FILE" && grep -qF "$PRIOR_REPORT" "$PROMPT_FILE" \\
  || { echo "REFUSING: prompt does not name the report directory $REPORT_DIR, the PRIOR REPORT $PRIOR_REPORT (#1034, KS-1215: the same api-gateway service, gated this morning) and NOT-TESTED.written-first.md — the QA agent has no inbox" >&2; exit 24; }''', 1),
 ('exit25', '''grep -qF 'MERGE ADDENDUM' "$PROMPT_FILE" && grep -qF 'MERGE ADDENDUM' "$BRIEF" && grep -qF 'CLOSED / STILL OPEN / NEW' "$PROMPT_FILE" && grep -qF 'CLOSED / STILL OPEN / NEW' "$BRIEF" \\
  || { echo "REFUSING: brief or prompt does not carry the MERGE ADDENDUM and the per-finding CLOSED / STILL OPEN / NEW disposition — the merge seat equality targets and the In Progress hold ride on it" >&2; exit 25; }''',
            '''grep -qF 'MERGE ADDENDUM' "$PROMPT_FILE" && grep -qF 'CLOSED / STILL OPEN / NEW' "$PROMPT_FILE" \\
  || { echo "REFUSING: prompt does not carry the MERGE ADDENDUM and the per-finding CLOSED / STILL OPEN / NEW disposition — the merge seat equality targets and the In Progress hold ride on it" >&2; exit 25; }''', 1),
 ('exit26+27', EXIT26_OLD, EXIT26_NEW, 1),
 ('check head', 'echo "  head on origin: #1034 $HEAD_SHA at $BRANCH"', 'echo "  head on origin: #1037 $HEAD_SHA at $BRANCH"', 1),
 ('check compare', 'echo "  compare (GitHub API): develop...#1034 = $COMPARE"', 'echo "  compare (GitHub API): develop...#1037 = $COMPARE"', 1),
 ('check present', 'echo "  brief, prompt, QA project and repo all present"', 'echo "  READY mail, prompt, QA project and repo all present"', 1),
 ('check tier/round', 'echo "  brief and prompt agree on TIER 1 and ROUND 1"', 'echo "  READY mail and prompt agree on TIER 1; prompt names ROUND 1"', 1),
 ('check brief named', 'echo "  prompt opens with the thinking directive and names the brief"', 'echo "  prompt opens with the thinking directive and names the seat READY mail"', 1),
 ('check head sha', 'echo "  brief and prompt both name the head SHA"', 'echo "  READY mail and prompt both name the head SHA"', 1),
 ('check subject', 'echo "  prompt carries the exact #1034 verdict subject, coagent@ sender, wednesday-agent@ recipient"\n  echo "  brief and prompt name the report directory and the #1023 PRIOR REPORT (KS-1207 N-1); prompt names NOT-TESTED.written-first.md"\n  echo "  brief and prompt carry the MERGE ADDENDUM and require CLOSED / STILL OPEN / NEW per finding"\n  echo "  brief and prompt name WEDNESDAY\'S signed GO as the merge authority; no copied Kam\'s-tap merge condition"\n',
                    'echo "  prompt carries the exact #1037 verdict subject, coagent@ sender, wednesday-agent@ recipient"\n  echo "  prompt names the report directory, the #1034 PRIOR REPORT (KS-1215, same service) and NOT-TESTED.written-first.md"\n  echo "  prompt carries the MERGE ADDENDUM and requires CLOSED / STILL OPEN / NEW per finding"\n  echo "  prompt names WEDNESDAY\'S signed GO as the merge authority; no copied Kam\'s-tap merge condition survives"\n  echo "  READY mail and prompt BOTH name the three NOT-fixed findings (smoke-test.sh:107, /health/services, out-of-repo consumers)"\n', 1),
 ('check fixture echo', '  [ -n "${QA1034_CUR_DEV:-}" ] && echo "  (develop read from the QA1034_CUR_DEV test override, not ls-remote)"\n  [ -n "${QA1034_AUTH_FILE:-}" ] && echo "  (develop api-gateway middleware/auth.ts read from the QA1034_AUTH_FILE fixture, not the contents API)"\n',
  '  [ -n "${QA1037_CUR_DEV:-}" ] && echo "  (develop read from the QA1037_CUR_DEV test override, not ls-remote)"\n  [ -n "${QA1037_HEALTH_FILE:-}" ] && echo "  (develop api-gateway services/health.ts read from the QA1037_HEALTH_FILE fixture, not the contents API)"\n', 1),
 ('exit16 fixture', '[ -z "${QA1034_BRIEF:-}${QA1034_PROMPT:-}${QA1034_HEAD:-}${QA1034_CUR_DEV:-}${QA1034_AUTH_FILE:-}" ]',
                    '[ -z "${QA1037_BRIEF:-}${QA1037_PROMPT:-}${QA1037_HEAD:-}${QA1037_CUR_DEV:-}${QA1037_HEALTH_FILE:-}" ]', 1),
]
badn = 0
for label, old, new, want in REPL:
    n = s.count(old)
    if n != want: print('ANCHOR COUNT', label, n, '!=', want); badn += 1; continue
    s = s.replace(old, new); print('  ok', label, n)
if badn: print('REFUSING: %d anchors disagreed; nothing written' % badn); sys.exit(1)

BODY = s.replace(HEADER_NEW, '')
RESID = ['QA1034_', 'fd81a75f0', '96d859467', '6c6fdc94e', '3961c2add', '0a2b1603f', 'f1c78bbb8', '6339c404c', '92256f2df', '6f912843b',
         '5b7431af0', 'twenty-four', 'nineteen', 'AUTHTS', 'QA1034_AUTH_FILE', 'rawAuthorization',
         # NB bf09d315a / 75006b5cf / routes/platform.ts / the word connector are NO LONGER residuals: #1034 merged into develop mid-draft, so those are
         # now this gate's own develop pins. 5b7431af0 (the SUPERSEDED #1034 test blob) stays banned — develop must carry the merged one, not that.
         'ks480', 'ks1207', 'trustHeaders', 'tenant-guc', 'session-validation', 'gracefulShutdown', 'jwks', 'rateLimitEnforce',
         'middleware/scopes.ts', 'services/redis.ts', 'routes/proxy.ts', 'routes/batch.ts', 'routes/admin.ts', 'routes/verification.ts',
         'secuura-1034', '2f74491eb', 'KS-1207', '#1023', '27e53ec3a', 'ks-1215',
         # packages/shared must survive ONLY as the prose note saying why it is not judged: ban every code form of it.
         'D + "packages/shared', 'packages/shared/src/db', 'packages/shared/src/security', 'packages/shared/src/crypto', 'packages/shared/src/utils']
res = {t: BODY.count(t) for t in RESID if t in BODY}
if res:
    print('REFUSING: residual tokens in the body', res, [l[:140] for l in BODY.splitlines() if any(t in l for t in res)][:8]); sys.exit(2)

CTL = {H: None, MB: None, DEV: None, MERGED: None, REPORT_DIR: 1, PRIOR: 1, '"$PRIOR_REPORT"': 1, 'ahead=3 files=6': 2,
       'QA1037_HEALTH_FILE': None, 'QA1037_CUR_DEV': None, ': DV}': 20, "grep -q 'ROUND 1'": 1, 'content_cleared': 2,
       'DEV_CONTENT_ALLOWED = {}': 1, '#1037 own': 6, 'CLOSED / STILL OPEN / NEW': None, 'MERGE ADDENDUM': None,
       'NOT-TESTED.written-first.md': None, 'exit 19': None, 'exit 21': None, 'exit 22': None, 'exit 23': None, 'exit 24': None,
       'exit 25': None, 'exit 26': None, 'exit 27': None, 'exit 16': None,
       # 4 = the header exit-27 note, the two greps (prompt + READY mail) and the refusal message.
       '[QA -> Wednesday] TIER 1 GATE #1037 (KS-1101) f87506f47': 1, 'scripts/smoke-test.sh:107': 4,
       # 3 = BRIEF, REAL_BRIEF and the header NO SEPARATE BRIEF note.
       'gatesets/2026-09-18_gate1037/mail_1037_ready.md': 3, 'briefs/2026-09-18_secuura-1037-ks1101-tier1.prompt.txt': 1,
       '[ -t 0 ]': 1, 'exec claude --dangerously-skip-permissions --model opus': 1, 'A + "vitest.setup.ts"': 2,
       'D + "scripts/smoke-test.sh"': 2, 'D + "frontend/status/index.html"': 1, 'HEALTHTS': 3,
       'A + "src/routes/platform.ts"': 1, 'A + "src/__tests__/ks1215-the-connector-branch-never-carries-the-callers-bearer.test.ts"': 1}
got = {k: s.count(k) for k in CTL}
print('output controls', {(k[:28] + '…' if len(k) > 28 else k): v for k, v in got.items()})
for k, v in CTL.items():
    if (v is not None and got[k] != v) or got[k] == 0: print('CONTROL DISAGREED', k, got[k], v); sys.exit(1)
for pth, b_ in list(PIN.items()) + list(LANDED.items()):
    if s.count(b_) != 1: print('CONTROL DISAGREED pin', pth, b_, s.count(b_)); sys.exit(1)
for tag in ("<<'PY'\n", "<<'PYJ'\n"):
    i = s.index(tag); j = s.index('\nPY' + ('J' if 'PYJ' in tag else '') + '\n', i); blk = s[i:j]
    print('heredoc', tag.strip(), 'apostrophes', blk.count("'") - 2, 'parens (', blk.count('('), ')', blk.count(')'))
    if (blk.count("'") - 2) % 2 or blk.count('(') != blk.count(')'): print('REFUSING: heredoc parity'); sys.exit(1)
if re.search(r'git -C "\$REPO" (fetch|push|checkout|merge|reset|worktree|commit|switch|pull|merge-tree)\b', s): print('REFUSING: git write verb'); sys.exit(1)
if re.search(r'[\x00-\x08\x0b\x0c\x0e-\x1f]', s): print('REFUSING: control bytes'); sys.exit(1)
tmp = OUT + '.gen-tmp'; open(tmp, 'w').write(s)
p = subprocess.run(['bash', '-n', tmp], capture_output=True, text=True); print('bash -n rc', p.returncode, p.stderr.strip()[:300])
if p.returncode: print('REFUSING: bash -n; the tmp file is left for reading at', tmp); sys.exit(3)
if os.path.exists(OUT):
    pre = OUT + '.pre-' + now('+%H%M%S'); shutil.copyfile(OUT, pre); print('existing output copied to', pre)
os.replace(tmp, OUT); os.chmod(OUT, 0o755)
print('written', OUT, 'mode', oct(os.stat(OUT).st_mode & 0o777), 'sha256', hashlib.sha256(open(OUT, 'rb').read()).hexdigest()[:16], 'lines', s.count('\n'))
