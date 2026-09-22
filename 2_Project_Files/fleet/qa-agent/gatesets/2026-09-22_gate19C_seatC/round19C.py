"""round19C.py — the ONE source of the Seat C 19th round's pins for every gate19C drafter script (the gate18C round18C.py shape, re-keyed).
Values: the seat's TWELVE READY mails (mail_seatC19_ready01..12_*.md, captured 07:25:5xZ by message id), its 05:08Z (12/12 RAISED) and 07:22:26Z
(HOLDING) STATUS mails, its 04:25Z plan confirmation + 06:25Z #1189 QUESTION, Wednesday's brief 04:03:27Z + the 04:10Z develop-moved ADDENDUM +
her plan ANSWER 04:27:09Z + the F-GUARD (2') ADDENDUM 06:22:04Z + the #1189 ANSWER 06:26:54Z, the drafter's ls-remote 07:28:09Z (lsremote_1.out).
Every value is a CLAIM until a script re-derives it; the scripts print the disagreement, never adopt. Blobs are the READYs' 12-hex forms unless a
script read the 40-hex form from origin objects (predict_batch_scratch_gate19C.py prints them)."""
DEV = '3bad652d17cf111c1e2e1bed1ae7686894637487'; DEV_TREE12 = 'cd9b0f6c7b84'   # the 18th round's END tree (13 PRs merged: Seat C 18th's six + Seat B 18th's seven); Seat B 19th's S1 (581ed7fa1 -> 3bad652d1 in the shared checkout) ruled LEAVE
DEV_PRE = '581ed7fa1'            # the checkout's HEAD before Seat B 19th's boot pull (the 04:10Z addendum)
SEAT_ALL14 = '5a8458a5697f7ee5b1800864b9f49347c8cbe34e'   # the seat's all-14 (twelve PRs) tree over DEV (item 0 three orders; the s-c19-batch worktree by sequential ort merges)
SEAT_ALL14_SHORTSTAT = '21 files changed, 915 insertions(+), 29 deletions(-)'
SEAT_PAIR_TREE12 = 'eaa961172883'   # #1180 + #1181 over DEV, both orders (the READYs)
PAIR_PATH = 'Start_Up/start-secuura.sh'; PAIR_BLOB = '58cdd3dc846b730e9f7eb5b517a6e4108ac05fdb'; PAIR_LINES = 736; PAIR_MODE = '100755'
D = 'Blockchain/Dev/'; SC = D + 'scripts/'; T = SC + '__tests__/'
LM = '/Volumes/DevMASTER/WEDNESDAY/2_Project_Files/local-model'
REPO = '/Volumes/DevMASTER/!CODING/Secuura/Blockchain/2_Project_Files'
ORIGIN_URL = 'git@github.com:Secuura/Distributed_Secuura.git'
PUSH = [str(i) for i in range(1, 13)]
# the commission's tier-1 script list (item 1): a PR whose bytes touch any of these is tier 1 by the FILE rule
TIER1_SCRIPTS = ['.githooks/pre-push', SC + 'preflight/preflight.sh', SC + 'run-migrations.sh', SC + 'check-stack-safety.sh', SC + 'bootstrap-env.sh', 'Start_Up/start-secuura.sh']
EXEC_SCRIPTS = ['Start_Up/start-secuura.sh', SC + 'run-migrations.sh', SC + 'check-stack-safety.sh', '.githooks/pre-push', SC + 'bootstrap-env.sh']   # the HOLD: 100755 where the tip does
# a canonical row: (label, run dir (under LM/runs), file under out.md.checker/, sha256[:16], apply opts ('' = strict), target path)
# a file row: dict(path, kind suite|script|doc, mode new|modify, blob12, lines, adds, dels)
PRS = {
 '1': dict(n='1180', key='KS-972', keys=['KS-972'], tags='BANNER', kind='bash_patch', head='ad86ffdbf504c250c1144f7d59ddcdba4966568d', tree='491f2e1d263c1fb546fb515bc593a3e4c7af3e0b',
           branch='refs/heads/feature/ks-972-start-secuurash-banner-prints-adminsecuuracom-admin123-which-r16b-banner-1', tier_ready=1, targets=2, adds=79, dels=1,
           files=[dict(path=T + 'start_secuura_banner.test.sh', kind='suite', mode='new', blob12='60db49e9364c', lines=78, adds=78, dels=0),
                  dict(path='Start_Up/start-secuura.sh', kind='script', mode='modify', blob12='1882bb0c5114', lines=722, adds=1, dels=1)],
           canon=[('972-BANNER-s2', '2026-09-22_ks972-ornith35b-night', 'section_2.diff', '3089354086978ae7', '', T + 'start_secuura_banner.test.sh'),
                  ('972-BANNER-s1', '2026-09-22_ks972-ornith35b-night', 'section_1.diff', '221f351eb6139679', '--recount --ignore-whitespace', 'Start_Up/start-secuura.sh')],
           b4=(1, 2, 2), b5=4, b6=4, inhook='46 passed, 0 failed (of 46)', lock=('05:12:56Z', '05:19:24Z'), polls=0, ready='05:24:08Z',
           title='KS-972 BANNER: start-secuura.sh no longer prints the retired admin default credential', excised=None),
 '2': dict(n='1181', key='KS-1011', keys=['KS-1011'], tags='MARKERWARN', kind='bash_patch', head='b2c0ac2d94387f9ce63c76ec437a465aca63a85f', tree='8bde36b1c7d8abca9f12918f9751df792318212d',
           branch='refs/heads/feature/ks-1011-stack-marker-reads-unknown-for-r16b-markerwarn-1', tier_ready=1, targets=2, adds=70, dels=0,
           files=[dict(path=T + 'start_secuura_marker_unknown_warning.test.sh', kind='suite', mode='new', blob12='7c3010a18153', lines=56, adds=56, dels=0),
                  dict(path='Start_Up/start-secuura.sh', kind='script', mode='modify', blob12='9bb5e5e1272d', lines=736, adds=14, dels=0)],
           canon=[('1011-MARKERWARN-s2', '2026-09-22_ks1011-ornith35b-night', 'section_2.diff', 'a2c7a2b01a5170cb', '', T + 'start_secuura_marker_unknown_warning.test.sh'),
                  ('1011-MARKERWARN-s1', '2026-09-22_ks1011-ornith35b-night', 'section_1.diff', 'ef76b4b6252a7499', '', 'Start_Up/start-secuura.sh')],
           b4=(1, 4, 1), b5=5, b6=4, inhook='46 passed, 0 failed (of 46)', lock=('05:21:09Z', '05:28:11Z'), polls=0, ready='05:31:51Z',
           title='KS-1011 MARKERWARN: start-secuura.sh warns, loud and named, on unknown stack markers', excised='ks-666'),
 '3': dict(n='1183', key='KS-1031', keys=['KS-1031'], tags='EXIT3', kind='bash_patch', head='03fab6783d5e1ad5893178027abc2291abeb627e', tree='4e1393f8a8e5aedb53d68b825ac975b909cc2199',
           branch='refs/heads/feature/ks-1031-gate-f-4-deploy-condition-apply-048-before-rolling-r16b-exit3-1', tier_ready=1, targets=2, adds=116, dels=6,
           files=[dict(path=T + 'run_migrations_failure_exit_code.test.sh', kind='suite', mode='new', blob12='c998bd7ed21d', lines=105, adds=105, dels=0),
                  dict(path=SC + 'run-migrations.sh', kind='script', mode='modify', blob12='633e92de2308', lines=163, adds=11, dels=6)],
           canon=[('1031-EXIT3-s2', '2026-09-22_ks1031-ornith35b-night', 'section_2.diff', 'fdf6d090392ceb31', '', T + 'run_migrations_failure_exit_code.test.sh'),
                  ('1031-EXIT3-s1', '2026-09-22_ks1031-ornith35b-night', 'section_1.diff', 'ae04617ec3fa419a', '', SC + 'run-migrations.sh')],
           b4=(1, 2, 3), b5=5, b6=1, inhook='46 passed, 0 failed (of 46)', lock=('05:34:29Z', '05:40:26Z'), polls=4, ready='05:44:01Z',
           title='KS-1031 EXIT3: run-migrations.sh exits 3 on a migration failure, never 0', excised='ks-754'),
 '4': dict(n='1185', key='KS-1033', keys=['KS-1033'], tags='DEMOBASE', kind='bash_patch', head='46e174169084318329b49f1c2109e210e7b8f743', tree='ce359c0eeba4409f8e103fd5a8a39e545d6dd983',
           branch='refs/heads/feature/ks-1033-residue-the-three-guards-that-could-not-be-wired-and-r16b-demobase-1', tier_ready=1, targets=2, adds=132, dels=2,
           files=[dict(path=T + 'check_no_demo_mutation_base.test.sh', kind='suite', mode='new', blob12='78324a8d8fa8', lines=126, adds=126, dels=0),
                  dict(path=SC + 'check-no-demo-mutation.sh', kind='script', mode='modify', blob12='3b4af5b463b1', lines=144, adds=6, dels=2)],
           canon=[('1033-DEMOBASE-s2', '2026-09-22_ks1033-ornith35b-night', 'section_2.diff', '7333dd7d50c254f2', '', T + 'check_no_demo_mutation_base.test.sh'),
                  ('1033-DEMOBASE-s1', '2026-09-22_ks1033-ornith35b-night', 'section_1.diff', '32b68acb0feeb2d9', '--recount', SC + 'check-no-demo-mutation.sh')],
           b4=(1, 2, 3), b5=5, b6=0, inhook='46 passed, 0 failed (of 46)', lock=('05:48:16Z', '05:54:35Z'), polls=6, ready='05:57:50Z',
           title='KS-1033 DEMOBASE: the demo-mutation guard reads its commit-range base correctly', excised='ks-926'),
 '5': dict(n='1187', key='KS-1034', keys=['KS-1034', 'KS-1093'], tags='HOOKENV + LATESTSLOT', kind='bash_patch', head='40d352edcb386a63083ff22422b3604f945575df', tree='9b64b87e8509c52188d014c88a1b6747e0d3327f',
           branch='refs/heads/feature/ks-1034-check-stack-safetysh-resolves-the-wrong-repo-root-inside-a-r16b-hookenv-latestslot-1', tier_ready=1, targets=3, adds=143, dels=2,
           files=[dict(path=T + 'check_stack_safety_hook_env.test.sh', kind='suite', mode='new', blob12='e673f5979922', lines=71, adds=71, dels=0),
                  dict(path=T + 'check_stack_safety_latest_slot_symlink.test.sh', kind='suite', mode='new', blob12='25c325a07f51', lines=67, adds=67, dels=0),
                  dict(path=SC + 'check-stack-safety.sh', kind='script', mode='modify', blob12='894ba4612b16', lines=424, adds=5, dels=2)],
           canon=[('1034-HOOKENV-s2', '2026-09-22_ks1034-ornith35b-night', 'section_2.diff', '397009793d67fefe', '', T + 'check_stack_safety_hook_env.test.sh'),
                  ('1034-HOOKENV-s1', '2026-09-22_ks1034-ornith35b-night', 'section_1.diff', '6b372a204a3ac911', '', SC + 'check-stack-safety.sh'),
                  ('1093-LATESTSLOT-s2', '2026-09-22_ks1093-ornith35b-night', 'section_2.diff', 'ec9d5d280132bbf3', '', T + 'check_stack_safety_latest_slot_symlink.test.sh'),
                  ('1093-LATESTSLOT-s1', '2026-09-22_ks1093-ornith35b-night', 'section_1.diff', 'e37a7f61a2bd5537', '', SC + 'check-stack-safety.sh')],
           intermediate=('check-stack-safety.sh after 1034-HOOKENV-s1', 'ed53fafc1730', 422),
           b4=(1, 2, 3), b5=5, b6=1, b4b=(1, 3, 3), b5b=6, inhook='47 passed, 0 failed (of 47)', lock=('06:00:53Z', '06:07:12Z'), polls=4, ready='06:11:10Z',
           title='KS-1034 HOOKENV: check-stack-safety.sh repo root under GIT_DIR; latest-slot symlink check', excised=None),
 '6': dict(n='1188', key='KS-1040', keys=['KS-1040'], tags='SWEEPRC', kind='bash_patch', head='fa13f78e8a87769d82c51b070d165f24e677a3a3', tree='3fbacc0c71dc6a2784f9c43a947912435d04495e',
           branch='refs/heads/feature/ks-1040-push-preflight-leg-4-reports-a-published-path-is-unroutable-r16b-sweeprc-1', tier_ready=1, targets=2, adds=103, dels=1,
           files=[dict(path=T + 'preflight_leg4_sweep_not_run.test.sh', kind='suite', mode='new', blob12='65c09b0f213a', lines=97, adds=97, dels=0),
                  dict(path=SC + 'preflight/preflight.sh', kind='script', mode='modify', blob12='270b8913c009', lines=784, adds=6, dels=1)],
           canon=[('1040-SWEEPRC-s2', '2026-09-22_ks1040-ornith35b-night', 'section_2.diff', '6281e19019dbc94e', '', T + 'preflight_leg4_sweep_not_run.test.sh'),
                  ('1040-SWEEPRC-s1', '2026-09-22_ks1040-ornith35b-night', 'section_1.diff', '215cb4d912865eb4', '', SC + 'preflight/preflight.sh')],
           b4=(1, 2, 3), b5=5, b6=9, inhook='46 passed, 0 failed (of 46)', lock=('06:13:58Z', '06:20:13Z'), polls=5, ready='06:23:03Z',
           title='KS-1040 SWEEPRC: preflight leg 4 reports sweep-not-run on the sweep rc', excised=None),
 '7': dict(n='1190', key='KS-1047', keys=['KS-1047'], tags='STACKLEGS', kind='bash_patch', head='6b836f0afab7c129747e8818626be9edd1975932', tree='2e6a60fed3b7175b973348ddc9ba89e53030059a',
           branch='refs/heads/feature/ks-1047-pre-push230-names-the-stack-dependent-legs-as-3-4-7-measured-r16b-stacklegs-2', tier_ready=1, targets=2, adds=75, dels=1,
           files=[dict(path='.githooks/pre-push', kind='script', mode='modify', blob12='ea44b2277e12', lines=282, adds=1, dels=1),
                  dict(path=T + 'pre_push_stack_legs_comment.test.sh', kind='suite', mode='new', blob12='e77bf0be28e1', lines=74, adds=74, dels=0)],
           canon=[('1047-STACKLEGS-s2', '2026-09-22_ks1047-ornith35b-night', 'section_2.diff', 'ea928563fe8bd663', '', T + 'pre_push_stack_legs_comment.test.sh'),
                  ('1047-STACKLEGS-s1', '2026-09-22_ks1047-ornith35b-night', 'section_1.diff', 'fe70b038cc4c8b56', '', '.githooks/pre-push')],
           b4=(1, 2, 2), b5=4, b6=7, inhook='46 passed, 0 failed (of 46)', lock=('06:29:42Z', '06:34:57Z'), polls=0, ready='06:38:54Z',
           title='KS-1047 STACKLEGS: pre-push comment drops the stale (3, 4, 7) leg enumeration', excised=None,
           closed_pr='1189', closed_branch='refs/heads/feature/ks-1047-pre-push230-names-the-stack-dependent-legs-as-3-4-7-measured-r16b-stacklegs-1', close_comment_id='5772145479'),
 '8': dict(n='1191', key='KS-1081', keys=['KS-1081'], tags='CANONENV', kind='bash_patch', head='b7dc03c142c9e65cd5112b5eee63c863bc368a93', tree='83d5f748fe1cdb6f96c2103abdf68c684373494d',
           branch='refs/heads/feature/ks-1081-config-drift-two-tracked-env-templates-disagree-by-39-vars-r16b-canonenv-1', tier_ready=1, targets=2, adds=106, dels=3,
           files=[dict(path=T + 'bootstrap_env_canonical_template.test.sh', kind='suite', mode='new', blob12='7f938694b60c', lines=90, adds=90, dels=0),
                  dict(path=SC + 'bootstrap-env.sh', kind='script', mode='modify', blob12='76958c117fe8', lines=334, adds=16, dels=3)],
           canon=[('1081-CANONENV-s2', '2026-09-22_ks1081-ornith35b-night', 'section_2.diff', '2a1027d8bfa1d291', '', T + 'bootstrap_env_canonical_template.test.sh'),
                  ('1081-CANONENV-s1', '2026-09-22_ks1081-ornith35b-night', 'section_1.diff', '4e327b042aeb8387', '', SC + 'bootstrap-env.sh')],
           b4=(1, 4, 2), b5=6, b6=2, inhook='46 passed, 0 failed (of 46)', lock=('06:37:15Z', '06:43:35Z'), polls=0, ready='06:47:49Z',
           title='KS-1081 CANONENV: bootstrap-env.sh reads env.example as the canonical template', excised=None),
 '9': dict(n='1192', key='KS-1139', keys=['KS-1139'], tags='ERREXIT', kind='bash_patch', head='fe9cd46daa4a8e50ed37fca3f48fd23e6d05e44a', tree='30b5b314d873fe2a8914901852bd5b78e989e74a',
           branch='refs/heads/feature/ks-1139-bare-arithmetic-command-x-under-set-e-exits-1-at-0-and-bash-r16b-errexit-1', tier_ready=1, targets=2, adds=83, dels=2,
           files=[dict(path=T + 'validate_lint_errexit.test.sh', kind='suite', mode='new', blob12='bde065b6e068', lines=81, adds=81, dels=0),
                  dict(path='systemTest/schemathesis/validate-lint.sh', kind='script', mode='modify', blob12='f5fd1883cc7e', lines=75, adds=2, dels=2)],
           canon=[('1139-ERREXIT-s2', '2026-09-22_ks1139-ornith35b-night', 'section_2.diff', '2f8252aa67c13b08', '', T + 'validate_lint_errexit.test.sh'),
                  ('1139-ERREXIT-s1', '2026-09-22_ks1139-ornith35b-night', 'section_1.diff', '9373c53b94acf50e', '', 'systemTest/schemathesis/validate-lint.sh')],
           b4=(1, 2, 1), b5=3, b6=0, inhook='46 passed, 0 failed (of 46)', lock=('06:46:33Z', '06:53:01Z'), polls=0, ready='06:56:38Z',
           title='KS-1139 ERREXIT: validate-lint.sh arithmetic counters survive set -e', excised=None),
 '10': dict(n='1193', key='KS-1097', keys=['KS-1097'], tags='CONTRIBUTING (REVIEWREQ + PRPROCESS)', kind='doc_patch', head='deb7ddb99c799d50969f1c70720d3d0cc3004d34', tree='e7712b5e481cdf0ddca0eb27b9f9c386e0f73b13',
           branch='refs/heads/feature/ks-1097-merge-rule-docs-after-957-the-v4-footer-and-two-gate-r16b-contributing-reviewreq-prprocess-1', tier_ready=2, targets=1, adds=5, dels=6,
           files=[dict(path=D + 'CONTRIBUTING.md', kind='doc', mode='modify', blob12='bbcc95cfc9f1', lines=689, adds=5, dels=6)],
           canon=[('1097-REVIEWREQ', '2026-09-22_ks1097-ornith35b-night2', 'patch.diff', '58b583ae7bd59f2f', '', D + 'CONTRIBUTING.md'),
                  ('1097-PRPROCESS', '2026-09-22_feed9-drafter-precheck/PRPROCESS', 'patch.diff', '544029f477a292da', '', D + 'CONTRIBUTING.md')],
           intermediate=('CONTRIBUTING.md after 1097-REVIEWREQ', '44e28201ebe9', 689), claude_written=['1097-PRPROCESS'],
           b4=None, b5=None, b6=None, inhook='45 passed, 0 failed (of 45)', lock=('06:55:30Z', '07:01:25Z'), polls=0, ready='07:04:36Z',
           title='KS-1097 CONTRIBUTING: the review requirement and PR process say TESTED + GO', excised=None),
 '11': dict(n='1195', key='KS-1097', keys=['KS-1097'], tags='DEVPROCESS', kind='doc_patch', head='48061f24a0510e4133a9fa0be51b0f7b30b8fc85', tree='8c236a82053ac51f40027b3d4af233196f72af41',
           branch='refs/heads/feature/ks-1097-merge-rule-docs-after-957-the-v4-footer-and-two-gate-r16b-devprocess-1', tier_ready=2, targets=1, adds=2, dels=2,
           files=[dict(path=D + 'docs/DEV-PROCESS.md', kind='doc', mode='modify', blob12='4b86a3d8df44', lines=278, adds=2, dels=2)],
           canon=[('1097-DEVPROCESS', '2026-09-22_ks1097-ornith35b-night4', 'patch.diff', '4f36b0df0226ec09', '', D + 'docs/DEV-PROCESS.md')],
           b4=None, b5=None, b6=None, inhook='45 passed, 0 failed (of 45)', lock=('07:03:06Z', '07:09:05Z'), polls=0, ready='07:12:21Z',
           title='KS-1097 DEVPROCESS: DEV-PROCESS.md says TESTED as defined, not a second seat', excised=None),
 '12': dict(n='1197', key='KS-1097', keys=['KS-1097'], tags='CLAUDEMD', kind='doc_patch', head='661da6c23e233c682f30c3de83b71ef46c8a5bbb', tree='fb3ef4004c6efacab684a3ca3a8ca01188f15306',
           branch='refs/heads/feature/ks-1097-merge-rule-docs-after-957-the-v4-footer-and-two-gate-r16b-claudemd-1', tier_ready=2, targets=1, adds=1, dels=3,
           files=[dict(path='CLAUDE.md', kind='doc', mode='modify', blob12='eccdb71822da', lines=492, adds=1, dels=3)],
           canon=[('1097-CLAUDEMD', '2026-09-22_ks1097-ornith35b-night5', 'patch.diff', 'dc54e1f344372f81', '', 'CLAUDE.md')],
           b4=None, b5=None, b6=None, inhook='NO PREFLIGHT (the hook early return by PATH: no Blockchain/Dev/ path)', lock=('07:16:32Z', '07:16:40Z'), polls=5, ready='07:20:13Z',
           title='KS-1097 CLAUDEMD: CLAUDE.md branching says raise-to-1 is pending, Kam applies it', excised=None),
}
LANE_DEV = 45; BATCH_LANE = 55   # run-shell-suites.sh: 45 at develop (the seat's bare baseline); 55 on the all-14 tree (45 + 10 NEW suites)
BASH_N = 8   # the eight touched scripts on the batch tree
# Seat B 19th/20th's PRs on the same base (READYs captured beside): (n, key, head, [paths]) — its partition: packages/shared, services/kyc, services/originate, services/security, systemTest/performance
OR = D + 'services/originate/'; KY = D + 'services/kyc/'; SH = D + 'packages/shared/'; SE = D + 'services/security/'; SP = 'systemTest/performance/'
SEATB = [('1182', 'KS-730', '8c413d78243a47d144f4049e6cd720a473d4dceb', [OR + 'src/__tests__/ks730a-ingest-500-never-answers-err-message.test.ts', OR + 'src/routes/systemErrors.ts']),
         ('1184', 'KS-1028', 'dd9ef92274366dd9975203d1376a87f63e7606a4', [OR + 'src/__tests__/ks1028-step12-throw-does-not-skip-fanout.test.ts', OR + 'src/services/gdprService.ts']),
         ('1186', 'KS-1160', '8d3c5c9604fc07598bbb67ca2fcdfcead4859df1', [OR + 'src/__tests__/ks1160-webhooks-post-persists-normalised-url.test.ts', OR + 'src/routes/webhooks.ts']),
         ('1194', 'KS-1229', '97d2e3fe493bb65afa14b768cafa21912e58c02b', [OR + 'src/__tests__/ks1213-a-derived-writer-relabel-is-refused.test.ts']),
         ('1196', 'KS-629', '79a8955667fae3b34f2e6ab31b1dda35911a28f3', [KY + 'src/__tests__/ks629-kyc-livenessvideo-is-accepted-by-spec.test.ts', KY + 'src/index.ts'])]
SEATB_KEYS = ['KS-730', 'KS-1028', 'KS-1160', 'KS-1229', 'KS-629', 'KS-974', 'KS-976', 'KS-1164', 'KS-1179']   # its nine own keys (the brief); #1198 and onward not yet captured at the drafter's read
SEATB_DIRS = [SH, KY, OR, SE, SP]
SEATB_PATHS = [p_ for x in SEATB for p_ in x[3]]
SIBLING_GATE_DIR = None   # Seat B 20th's gate is not yet commissioned at the drafter's read
REPORT_DIR = '/Volumes/DevMASTER/!CODING/Testing Agent MAIN/projects/secuura/reports/2026-09-22-batch1180-1197-r1/'
PRIOR_REPORT = '/Volumes/DevMASTER/!CODING/Testing Agent MAIN/projects/secuura/reports/2026-09-22-batch1167-1175-r1/'   # the gate18C report (Seat C 18th's six)
EARLIER_REPORT = '/Volumes/DevMASTER/!CODING/Testing Agent MAIN/projects/secuura/reports/2026-09-22-batch1170-1179-r1/'   # the gate18B report (Seat B 18th's seven)
OLDER_REPORT = '/Volumes/DevMASTER/!CODING/Testing Agent MAIN/projects/secuura/reports/2026-09-22-batch1148-1166-r1/'    # the gate16C report
SEAT_RECORD = REPO + '/5_Project_History/2026-09-22_seatC-19th/'   # NOT under 2_Project_Files: the seat's record folder is /Volumes/DevMASTER/!CODING/Secuura/Blockchain/5_Project_History/2026-09-22_seatC-19th/
SEAT_RECORD = '/Volumes/DevMASTER/!CODING/Secuura/Blockchain/5_Project_History/2026-09-22_seatC-19th/'
ARCHIVED = ['KS-501', 'KS-480', 'KS-978', 'KS-721', 'KS-522', 'KS-726', 'KS-535', 'KS-867', 'KS-878', 'KS-914', 'KS-1238', 'KS-1282', 'KS-1062', 'KS-971', 'KS-1078', 'KS-921', 'KS-490',
            'KS-597', 'KS-727', 'KS-764', 'KS-879', 'KS-1020', 'KS-835', 'KS-1270', 'KS-549', 'KS-733', 'KS-815', 'KS-1013', 'KS-1058', 'KS-1103', 'KS-666', 'KS-754', 'KS-926', 'KS-487', 'KS-386', 'KS-444', 'KS-1092']   # 37
CONTENT_LIVE = ['KS-1213', 'KS-932', 'KS-1206', 'KS-763', 'KS-775', 'KS-1230', 'KS-1285', 'KS-1175', 'KS-1250', 'KS-1280', 'KS-692', 'KS-1195', 'KS-1265', 'KS-910']   # 14
OWN = sorted(set(k for p in PUSH for k in PRS[p]['keys']))   # 11 keys
TIER1_RULE = [p for p in PUSH if any(f['path'] in TIER1_SCRIPTS for f in PRS[p]['files'])]   # by the commission's FILE rule: 1 2 3 5 6 7 8
TIER1_READY = [p for p in PUSH if PRS[p]['tier_ready'] == 1]                                  # the seat's proposal: 1..9
DOCS = ['10', '11', '12']
GO_STRING = 'GO: merge #1180, #1181, #1183, #1185, #1187, #1188, #1190, #1191, #1192, #1193, #1195, #1197 batch'
def canon_path(row): return LM + '/runs/' + row[1] + '/out.md.checker/' + row[2]
def all_paths(): return [f['path'] for p in PUSH for f in PRS[p]['files']]
def distinct_paths(): return sorted(set(all_paths()))
def ready_regex(): return r'READY FOR QA \(Seat C 19th\): PR (\d+) (KS-\d+)[^\n]*? — #(\d+) at head ([0-9a-f]{40})'
if __name__ == '__main__':
    print('PRs', len(PRS), 'file rows', len(all_paths()), 'distinct', len(distinct_paths()), 'canon rows', sum(len(PRS[p]['canon']) for p in PUSH),
          'adds', sum(PRS[p]['adds'] for p in PUSH), 'dels', sum(PRS[p]['dels'] for p in PUSH), '| per-PR adds/dels consistent', all(sum(f['adds'] for f in PRS[p]['files']) == PRS[p]['adds'] and sum(f['dels'] for f in PRS[p]['files']) == PRS[p]['dels'] for p in PUSH))
    print('TIER1 by FILE rule', TIER1_RULE, '| TIER1 by READY', TIER1_READY, '| rule minus ready', sorted(set(TIER1_RULE) - set(TIER1_READY)), '| ready minus rule', sorted(set(TIER1_READY) - set(TIER1_RULE)), '=', [PRS[p]['n'] for p in sorted(set(TIER1_READY) - set(TIER1_RULE))])
    print('OWN keys', len(OWN), OWN, '| targets', [PRS[p]['targets'] for p in PUSH], 'sum', sum(PRS[p]['targets'] for p in PUSH))
    print('SEATB', len(SEATB), 'paths', len(SEATB_PATHS), '| C paths ∩ B paths:', sorted(set(all_paths()) & set(SEATB_PATHS)) or 'NONE', '| B under its dirs:', all(any(q.startswith(d) for d in SEATB_DIRS) for q in SEATB_PATHS), '| C under B dirs:', [q for q in all_paths() if any(q.startswith(d) for d in SEATB_DIRS)] or 'NONE')
    print('exec scripts', EXEC_SCRIPTS, '| pair', PAIR_PATH, PAIR_BLOB[:12], PAIR_LINES, PAIR_MODE)
