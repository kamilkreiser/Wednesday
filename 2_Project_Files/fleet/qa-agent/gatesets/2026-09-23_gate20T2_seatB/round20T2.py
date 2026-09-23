"""round20T2.py — the ONE source of the round-20 TIER-2 batch's pins for every gate20T2 drafter script (the round19B.py shape, re-keyed).
Seat B 21st (pane Secuura/Blockchain-B; ONE seat this round — no Seat C lane) raises 11 READYs as 10 PRs over develop 2bc5ccf63; Wednesday's 05:12:13Z
plan ANSWER ruled KS-851 to TIER 1, so the TIER-2 batch is EXACTLY seat PRs 1, 2, 4, 5 (KS-965 doc_patch, KS-1019 comment_patch, KS-1081 test_only on
a bash suite, KS-1139 test_only on a bash suite); PRs 3, 6-10 are the TIER-1 gate's (a separate gate, the same base, a separate GO; path-disjoint).
Values: the brief (fleet/briefs_staged/2026-09-23_raise_seatB_21.md GROUPING + QUEUE, its drafter's trees over 2bc5ccf63), the seat's READY mails
(mail_seatB21_ready01/02/04_*.md; READY 5 when it lands), the seat's STATUS 05:21Z / 05:36Z, the drafter's ls-remote (lsremote_1.out).
Every value is a CLAIM until a script re-derives it; the scripts print the disagreement, never adopt.

PR 5 IS PENDING until its READY lands: its PR number, head and branch are read from the captured READY 5 (mail_seatB21_ready05_pr5_ks1139.md) by
load_pr5() — never typed. Until then PR5_PENDING is True and every consumer either predicts PR 5 from its canonical (predict) or REFUSES (fill /
generator / launcher / repin). The seat's own record carries its COMMITTED head (raise/commits.tsv, read 06:3xZ) — EXPECT_PR5_COMMIT — a claim the
fill script asserts against the READY and origin."""
import os, re, glob
G = os.path.dirname(os.path.abspath(__file__))
DEV = '2bc5ccf63b8c40911afb568b03cace066238ffcf'; DEV_TREE = 'b4f2a8beaecdf758d46c719a0f3becc677e421cf'   # round 19's END tree (b4f2a8beaecd — gate19B's predicted COMBINED tree, now develop's)
DEV_PRE = '3bad652d17cf111c1e2e1bed1ae7686894637487'   # the shared checkout's local HEAD (21 first-parent behind; LEAVE — the round-19 S1 ruling)
BRIEF_ALL11 = '30cee235566d3d58debc8b24f39ffadfbe8216db'   # the brief's drafter: all-11 (10 PRs) over DEV, three orders one sha (context: the tier-2 gate does not grade it)
BRIEF_ALL11_SHORTSTAT = '16 files changed, 527 insertions(+), 26 deletions(-)'
D = 'Blockchain/Dev/'; OR = D + 'services/originate/'; SC = D + 'scripts/'
LM = '/Volumes/DevMASTER/WEDNESDAY/2_Project_Files/local-model'
REPO = '/Volumes/DevMASTER/!CODING/Secuura/Blockchain/2_Project_Files'
ORIGIN_URL = 'git@github.com:Secuura/Distributed_Secuura.git'
PUSH = ['1', '2', '4', '5']   # seat push order (tier 2); seat PR 3 (KS-851, #1204) is tier 1 by the 05:12:13Z ANSWER
# a canonical row: (label, run dir (under LM/runs), file under out.md.checker/, sha256[:16], apply opts ('' = strict), target path)
# a file row: dict(path, kind, mode new|modify, blob12 (AT THE HEAD), lines, adds, dels, dev_blob12, dev_lines)
PRS = {
 '1': dict(n='1202', key='KS-965', keys=['KS-965'], tags='ADMINPWDOC', kind='doc_patch', head='49f419e625d7304f724b4a604f542827b7772458', tree='830ed760914309fd38bbf31156a1d437037e2361',
           branch='refs/heads/feature/ks-965-87-documentary-sites-still-publish-the-retired-admin-r20-adminpwdoc-1', tier_ready=2, targets=1, adds=2, dels=2, lane='docs',
           files=[dict(path='USER_TESTING/CREDENTIALS-AND-PORTALS.md', kind='doc', mode='modify', blob12='f2487018dea3', lines=219, adds=2, dels=2, dev_blob12='82bbf39e9595', dev_lines=219)],
           canon=[('965-ADMINPWDOC', '2026-09-23_ks965-ornith35b-night', 'patch.diff', 'f32e4b95d1b5cf3d', '', 'USER_TESTING/CREDENTIALS-AND-PORTALS.md')],
           proof='D4/D5 section-scoped token counts (ADMIN_USER_PASSWORD 0 before / 1 after in `## 2. Default-tenant accounts` (16 lines) and `## 7. Quick smoke` (58 lines)); D6 every changed region inside those two sections; D7 both must-remove lines gone; D8 both + lines present; the checker after.md byte-identical to the applied file',
           lock=('05:49:35Z', '05:49:49Z'), ready='05:53:39Z', inhook='ZERO preflight legs (the hook filters by PATH: a .md outside Blockchain/Dev) — no leg-ratio line printed at all',
           title='KS-965 ADMINPWDOC: CREDENTIALS-AND-PORTALS.md names ADMIN_USER_PASSWORD', subject_len=71, occurrences='2 of 86', content_archived=['KS-547']),
 '2': dict(n='1203', key='KS-1019', keys=['KS-1019'], tags='LEAVEUNTYPED', kind='comment_patch', head='81accbcfeae3628f00d8698ef1743c53b946bfce', tree12='6beda06e9d9e',
           branch='refs/heads/feature/ks-1019-question-the-documents-whole-blockchain-block-is-published-r16b-leaveuntyped-1', tier_ready=2, targets=1, adds=1, dels=0, lane='originate',
           files=[dict(path=OR + 'src/originate.openapi.ts', kind='product-comment', mode='modify', blob12='f9675bf96077', lines=3873, adds=1, dels=0, dev_blob12='2d1b48a0c7ea', dev_lines=3872)],
           canon=[('1019-LEAVEUNTYPED', '2026-09-22_ks1019-ornith35b-night', 'patch.diff', '8ec20706235387ab', '', OR + 'src/originate.openapi.ts')],
           proof='C4 TOKEN EQUIVALENCE: the checker 17679 code tokens (typescript 5.9.3 PARSER LEAVES) identical before/after; the seat 17731 tokens (the typescript 5.9.3 SCANNER, raise/c4tokens.js) before == after, IDENTICAL sha256; planted CODE token 17731 -> 17736 (different hash) FIRES; planted COMMENT byte-identical; C4b directive comments 0/0',
           tokens_checker=17679, tokens_seat=17731, tokens_seat_planted=17736, placement=(601, 590),
           lock=('06:00:38Z', '06:06:46Z'), ready='06:10:31Z', inhook='PREFLIGHT INCOMPLETE — 12/15 legs ran, 3 SKIPPED. Nothing failed.', suite='originate jest BARE 74 suites / 863 tests == PATCHED 74 / 863 (0 cells added); tsc rc 0',
           title='KS-1019 LEAVEUNTYPED: record why the document blockchain block stays z.unknown()', subject_len=80),
 '4': dict(n='1205', key='KS-1081', keys=['KS-1081'], tags='NEITHERTEMPLATE', kind='test_only_bash', head='d29a9b21dd70f8e1fb79c56e595e312499edee43', tree12='3f31d9e91e2f',
           branch='refs/heads/feature/ks-1081-config-drift-two-tracked-env-templates-disagree-by-39-vars-r17-neithertemplate-1', tier_ready=2, targets=1, adds=14, dels=0, lane='shell',
           files=[dict(path=SC + '__tests__/bootstrap_env_canonical_template.test.sh', kind='test', mode='modify', blob12='bbe4907847fa', lines=104, adds=14, dels=0, dev_blob12='7f938694b60c', dev_lines=90)],
           canon=[('1081-NEITHERTEMPLATE', '2026-09-22_ks1081-ornith35b-night2', 'patch.diff', 'e0875f05bd01dab2', '', SC + '__tests__/bootstrap_env_canonical_template.test.sh')],
           tampers={'GUARDGONE': (SC + 'bootstrap-env.sh', 68, ['a tree carrying NEITHER template'])},
           proof='suite 6/6 at develop -> 7/7 at head (+1); tamper GUARDGONE at scripts/bootstrap-env.sh:68 -> 6 ok / 1 FAIL, the single red the declared cell, the suite\'s two CONTROL cells green; restored by bytes (sha256 == pre-tamper, git diff --quiet rc 0)',
           lock=('06:23:09Z', '06:28:49Z'), ready='06:30:48Z', inhook='PREFLIGHT INCOMPLETE — 12/15 legs ran, 3 SKIPPED. Nothing failed.', prior_pr='1191',
           other_branch='refs/heads/feature/ks-1081-config-drift-two-tracked-env-templates-disagree-by-39-vars-r16b-canonenv-1',
           vacuous='the seat\'s FIRST bash driver parsed only `ok <msg>`; this suite prints `PASS: <msg>` -> a green run parsed as ZERO cells, "0/0 cells, +0 vs develop (declared adds 1)" did not stop; fixed (both forms; rc-0 with zero cells = hard STOP; adds != declared = STOP)',
           title='KS-1081 NEITHERTEMPLATE: pin that a tree with neither env template is refused', subject_len=77),
 '5': dict(n=None, key='KS-1139', keys=['KS-1139'], tags='ERREXITBEHAVIOUR', kind='test_only_bash', head=None, tree12='8c02c7b62858',
           branch_expected='refs/heads/feature/ks-1139-bare-arithmetic-command-x-under-set-e-exits-1-at-0-and-bash-r17-errexitbehaviour-1', branch=None, tier_ready=2, targets=1, adds=13, dels=0, lane='shell',
           files=[dict(path=SC + '__tests__/validate_lint_errexit.test.sh', kind='test', mode='modify', blob12='4d11b28d28f6', lines=94, adds=13, dels=0, dev_blob12='bde065b6e068', dev_lines=81)],
           canon=[('1139-ERREXITBEHAVIOUR', '2026-09-22_ks1139-ornith35b-night2', 'patch.diff', '6c6fa6f4efcabf61', '', SC + '__tests__/validate_lint_errexit.test.sh')],
           tampers={'PASSPLUSPLUS': ('systemTest/schemathesis/validate-lint.sh', 33, ['validate-lint.sh has NO bare arithmetic-command post-increment/decrement', 'both counters advance by assignment', 'run_check survives bash -e from PASS_COUNT=0 to the second check']),
                    'FAILPLUSPLUS': ('systemTest/schemathesis/validate-lint.sh', 38, ['validate-lint.sh has NO bare arithmetic-command post-increment/decrement', 'both counters advance by assignment'])},
           proof='the checker: T5 GREEN at the tip 4/4 cells; T6[PASSPLUSPLUS] 3 reds == declared; T6[FAILPLUSPLUS] 2 reds == declared (the brief) — the READY\'s own numbers when it lands',
           prior_pr='1192', other_branch='refs/heads/feature/ks-1139-bare-arithmetic-command-x-under-set-e-exits-1-at-0-and-bash-r16b-errexit-1',
           title='KS-1139 ERREXITBEHAVIOUR: run run_check under bash -e from zero counters', subject_len=72,
           lock=('06:31:32Z', '06:37:49Z'), ready='06:39:32Z', inhook='PREFLIGHT INCOMPLETE — 12/15 legs ran, 3 SKIPPED. Nothing failed.',
           suite='suite 3/3 at develop -> 4/4 at head (+1); PASSPLUSPLUS :33 -> 1 ok / 3 FAIL == the three declared; FAILPLUSPLUS :38 -> 2 ok / 2 FAIL == the two declared (DIFFERENT subsets, flipped separately)'),
}
SEAT_T2SUB = 'd13a26e19c8d1b2faf25f9e41cc087fbcd51ec47'   # READY 5 (06:39:32Z): the TIER-2 SUB-TREE over DEV, three orders one sha — `4 files changed, 30 insertions(+), 2 deletions(-)`
SEAT_T2SUB_SHORTSTAT = '4 files changed, 30 insertions(+), 2 deletions(-)'
SEAT_GO_STRING = 'GO: merge #1202, #1203, #1205, #1206 batch'   # READY 5, verbatim — the GO the seat expects; go_string() must equal it once PR 5 is pinned
EXPECT_PR5_COMMIT = 'bfbaf4366897a97ec20c2f88e67448597739ce46'   # the seat's raise/commits.tsv row ks1139 (read 2026-09-23T06:3xZ, BEFORE its push finished) — a CLAIM
PR5_READY_GLOB = os.path.join(G, 'mail_seatB21_ready05_pr5_ks1139.md')
PR5_PENDING = True
def parse_ready(path, keyslug):
    """(PR number, head 40-hex, refs/heads/<full branch> or None) from a captured READY: the number from `PR #N` / `PR:** #N` in THE FIVE THINGS,
    the head = the first 40-hex after `Head at ORIGIN`, the branch from the BUILD FACTS `branch `feature/<keyslug>-…`` line (full names only)."""
    t = open(path, encoding='utf-8').read()
    body = t.split('## THE FIVE THINGS', 1)[-1]
    mn = re.search(r'PR[: *]*#(\d{4})\b', body)
    mh = re.search(r'Head at ORIGIN.*?\b([0-9a-f]{40})\b', body, re.S)
    mb = re.search(r'branch `(feature/' + re.escape(keyslug) + r'-[a-z0-9_-]+)`', body)
    return (mn.group(1) if mn else None, mh.group(1) if mh else None, ('refs/heads/' + mb.group(1)) if mb else None)
def load_pr5():
    """Fill PRS['5'] n / head / branch from the captured READY 5 (never typed). Returns True when PR 5 is pinned from its READY."""
    global PR5_PENDING
    if not os.path.exists(PR5_READY_GLOB): return False
    n, h, b = parse_ready(PR5_READY_GLOB, 'ks-1139')
    if not (n and h): return False
    PRS['5']['n'] = n; PRS['5']['head'] = h
    PRS['5']['branch'] = b or PRS['5']['branch_expected']
    mb = b
    PRS['5']['branch_from'] = 'READY 5' if mb else 'EXPECTED (raise/branches.tsv; the READY abbreviates it) — the fill asserts it at origin'
    PR5_PENDING = False
    return True
load_pr5()
LANES = {'docs': (None, 'none', None, None), 'originate': (OR, 'jest', 863, 863), 'shell': (SC + '__tests__/', 'bash', None, None)}   # (dir, runner, bare develop count, the seat's head count)
# the tier-1 batch (the OTHER gate over the same base; path-disjoint by the brief's table — 12 paths)
TIER1_PRS = {'3': ('KS-851', '1204'), '6': ('KS-1287', None), '7': ('KS-1245', None), '8': ('KS-1033', None), '9': ('KS-1239', None), '10': ('KS-1084', None)}
TIER1_PATHS = [D + 'services/kyc/src/__tests__/ks386-no-image-payload-written.test.ts',
               D + 'services/vc-issuer/src/__tests__/ks1287-status-check-index-path-param-is-required.test.ts', D + 'services/vc-issuer/src/vc-issuer.openapi.ts',
               SC + '__tests__/smoke_test_degraded_warns.test.sh', SC + 'smoke-test.sh',
               SC + '__tests__/check_no_demo_mutation_missing_base.test.sh', SC + 'check-no-demo-mutation.sh',
               D + 'services/api-gateway/src/__tests__/ks1239-index-takes-no-pre-auth-rawauthorization-copy.test.ts', D + 'services/api-gateway/src/index.ts',
               D + 'services/api-gateway/src/__tests__/ks1084-signatories-forwards-x-tenant-id.test.ts', D + 'services/api-gateway/src/__tests__/ks1084-third-party-verifiers-forwards-x-tenant-id.test.ts', D + 'services/api-gateway/src/routes/proxy.ts']
TAMPER_FILES = sorted(set(v[0] for p in PUSH for v in PRS[p].get('tampers', {}).values()))   # bootstrap-env.sh + validate-lint.sh (+ kyc index.ts is tier 1's)
REPORT_DIR = '/Volumes/DevMASTER/!CODING/Testing Agent MAIN/projects/secuura/reports/2026-09-23-batch1202-t2-r1/'
PRIOR_REPORT_B = '/Volumes/DevMASTER/!CODING/Testing Agent MAIN/projects/secuura/reports/2026-09-22-batch1182-1201-r1/'   # gate19B (Seat B 19th/20th's nine)
PRIOR_REPORT_C = '/Volumes/DevMASTER/!CODING/Testing Agent MAIN/projects/secuura/reports/2026-09-22-batch1180-1197-r1/'   # gate19C (Seat C 19th's twelve; #1191 KS-1081 and #1192 KS-1139 were ITS rows)
SEAT_RECORD = '/Volumes/DevMASTER/!CODING/Secuura/Blockchain/5_Project_History/2026-09-23_seatB-21st/'
BRIEF = '/Volumes/DevMASTER/WEDNESDAY/2_Project_Files/fleet/briefs_staged/2026-09-23_raise_seatB_21.md'
ARCHIVED_NAMED = ['KS-547', 'KS-926', 'KS-386']   # KS-547: content inside KS-965's patch; KS-926 / KS-386: excised from KS-1033 / KS-851 branchNames (tier-1 rows)
OWN = sorted(set(k for p in PUSH for k in PRS[p]['keys']))   # 4 keys
def tier_rule(p):
    """the commission's reading of the tiering rule: tier 1 on product/script bytes that CHANGE BEHAVIOUR or an auth/PII-adjacent tamper; a doc row, a
    comment-only row (token stream identical) and a test-only cell on existing behaviour (tamper on a non-PII script) -> tier 2."""
    k = PRS[p]['kind']
    return 2 if k in ('doc_patch', 'comment_patch', 'test_only_bash') else 1
TIER_RULE = {p: tier_rule(p) for p in PUSH}
def go_string():
    ns = [PRS[p]['n'] for p in PUSH]
    return None if None in ns else 'GO: merge ' + ', '.join('#' + n for n in ns) + ' batch'
def canon_path(row): return LM + '/runs/' + row[1] + '/out.md.checker/' + row[2]
def all_paths(): return [f['path'] for p in PUSH for f in PRS[p]['files']]
def distinct_paths(): return sorted(set(all_paths()))
def ready_regex(): return r'READY FOR QA \(Seat B 21st\): PR (\d+) (KS-\d+)'
if __name__ == '__main__':
    print('PR5_PENDING', PR5_PENDING, '| PR 5', PRS['5']['n'], PRS['5']['head'], PRS['5']['branch'])
    print('PRs', len(PRS), 'file rows', len(all_paths()), 'distinct', len(distinct_paths()), 'canon rows', sum(len(PRS[p]['canon']) for p in PUSH),
          'adds', sum(PRS[p]['adds'] for p in PUSH), 'dels', sum(PRS[p]['dels'] for p in PUSH), '| per-PR adds/dels consistent', all(sum(f['adds'] for f in PRS[p]['files']) == PRS[p]['adds'] and sum(f['dels'] for f in PRS[p]['files']) == PRS[p]['dels'] for p in PUSH))
    print('TIER by rule', TIER_RULE, '| TIER by READY', {p: PRS[p]['tier_ready'] for p in PUSH}, '| agree', all(TIER_RULE[p] == PRS[p]['tier_ready'] for p in PUSH))
    print('OWN keys', OWN, '| targets', [PRS[p]['targets'] for p in PUSH], '| tier-1 paths', len(TIER1_PATHS), '| T2 ∩ T1:', sorted(set(all_paths()) & set(TIER1_PATHS)) or 'NONE', '| T2 ∪ T1 distinct', len(set(all_paths()) | set(TIER1_PATHS)), '(the brief: 16)')
    print('tamper files', TAMPER_FILES, '| ∩ PR paths:', sorted(set(TAMPER_FILES) & set(all_paths())) or 'NONE', '| ∩ tier-1 paths:', sorted(set(TAMPER_FILES) & set(TIER1_PATHS)) or 'NONE')
    for p, f in (('1', 'mail_seatB21_ready01_pr1_ks965.md'), ('2', 'mail_seatB21_ready02_pr2_ks1019.md'), ('4', 'mail_seatB21_ready04_pr4_ks1081.md')):
        n, h, b = parse_ready(os.path.join(G, f), PRS[p]['key'].lower())
        print('  parse_ready control on READY %s: n %s == %s, head == %s, branch == %s' % (p, n, n == PRS[p]['n'], h == PRS[p]['head'], b == PRS[p]['branch']))
    print('canonical files exist:', all(os.path.exists(canon_path(r)) for p in PUSH for r in PRS[p]['canon']), '| GO string:', go_string())
