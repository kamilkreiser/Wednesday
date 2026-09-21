"""round16C.py — the ONE source of this round's pins for every gate16C drafter script (a wrong pin in the prompt is the most expensive slip; every
script imports this module and asserts against origin / local objects / the READYs — the gate16B drafter's round16B.py shape).
Values: the seat's TWELVE READY mails (mail_seatC16_ready*.md, captured 19:13Z), its 16:46Z / 16:51Z / 16:56Z / 19:12Z STATUS mails, its 16:08Z plan
confirmation, Wednesday's brief (briefs_staged/2026-09-22_raise_seatC_16.md GROUPING + QUEUE), the drafter's ls-remote 19:12:22Z (lsremote_1.out) and
its `git diff --raw --abbrev=40 64ab10513 <head>` ×12 (the 40-hex blobs; the READYs carry 12-hex on the two KS-910 files). Every value is a CLAIM until a
script re-derives it; the scripts print the disagreement, never adopt."""
DEV = '64ab105132eada0621622acf4d6053bc59926780'; DEV_TREE = '87b4aa12d2ebae335f11790ceed9158f7d5614ec'
PARENT15 = '581ed7fa124b85c7c2da89ac05d52f99c2502911'   # the 15th's parent; rev-list --count 581ed7fa1..64ab10513 = 13 (the seat's item 0)
TIP9F = '9f0265eb06ecf24d4de18149ce862ad2330a61ee'      # the 14th's tip — five of the fifteen run patches were checked there
SEAT_ALL12 = '4817a9c2ea2334b89395c4faa588312cfd609550'  # the TWELVE-PR (all-15) tree over DEV (the seat's boot/measure17b.json; three orders + the heads' blobs)
SEAT_ALL13 = '48528fa3c35578e78a3559254530a7047f42597a'  # item 0's all-16 over THIRTEEN PRs incl. the HELD KS-1123 F3b — the s-c16-batch octopus tree (its suites)
D = 'Blockchain/Dev/'; AG = D + 'services/api-gateway/'; AU = D + 'services/auth/'; SC = D + 'scripts/'
LM = '/Volumes/DevMASTER/WEDNESDAY/2_Project_Files/local-model'
REPO = '/Volumes/DevMASTER/!CODING/Secuura/Blockchain/2_Project_Files'
PUSH = ['1', '3', '4', '5', '6', '7', '8', '9', '10', '11', '12', '13']   # seat PR numbers in push order; seat PR 2 (KS-1123 F3b) HELD un-pushed (Wednesday 16:53:40Z)
# a canonical row: (label, run dir, sha256[:16], mode, adds, dels, first hunk header, the seat's STRICT blob12 (truncation rows) or None, its strict line count or None, run tip9)
# a file row: dict(path, mode new|modify, dev_blob (40) or None, dev_lines, blob (40, the RECOUNT blob = the head blob), lines, adds, dels, canon=[...], tampers=[(label, path, line, reds, cover[])])
PRS = {
 '1': dict(n='1148', key='KS-864', tags='F1009b', head='c4a96cfe012196aa56765b6b26bd63b123980087', tree='631a38ab6d4b78c0ab80b719fa667740f426ed8b',
           branch='refs/heads/feature/ks-864-dead-estate-pointers-in-runtime-source-outside-r15-f1009b-1', lane='api-gateway', runner='vitest', tier=2,
           files=[dict(path=AG + 'src/__tests__/ks864c-portal-env-vars.test.ts', mode='modify', dev_blob='f886bdadf7065b4a40d7d54b13fa3f70f9cc35cf', dev_lines=80,
                       blob='1cf9959146c097db35fdb20b0bac8246377194cd', lines=94, adds=16, dels=2, cells_dev=6, cells=10, controls=3,
                       canon=[('F1009b', '2026-09-21_ks864-ornith35b-night2', '0f274204b12b5514', 'rc128', 16, 2, '@@ -48,2 +48,7 @@', None, None, '581ed7fa1')],
                       tampers=[('F1009', AG + 'src/routes/system-status.ts', 446, 1, [])])],
           adds=16, dels=2, lane_dev=697, lane_head=701, files_dev=71, files_head=71, typecheck=[(0, 0)],
           lock=('16:57:47Z', '17:03:29Z'), push=('16:57:47Z', '17:03:25Z'), ready='17:06:23Z', shell='44 passed, 0 failed (of 44)',
           census=(7, 1415, 1382, {'anchoring:4005 (ks1072-the-latest-anchor-selector-docume)': 15, 'anchoring:4005 (ks815-verification-router-guards-its-own)': 3, 'localhost:6000 (ks815-verification-router-guards-its-own)': 12}),
           title='KS-864 F1009b: pin the served environment.env to NODE_ENV under each portal block', comments=6, prior_prs=['1007', '1009', '1064', '1073'], excised=None),
 '3': dict(n='1150', key='KS-1180', tags='P1P2P4', head='250a9b9eda021cb2b3d224d68b9e3ca5e9264d2c', tree='bb7f9a2ac972e33206a058baf29ed72f0d341065',
           branch='refs/heads/feature/ks-1180-ks1073-verify-cells-the-tier-guard-is-not-a-tier-witness-the-r15-p1p2p4-1', lane='api-gateway', runner='vitest', tier=2,
           files=[dict(path=AG + 'src/__tests__/ks1073-tier-2-verify-has-no-statusless.test.ts', mode='modify', dev_blob='26f521ebd2e8aeb6d8884f4245e32235d9c8b1fc', dev_lines=188,
                       blob='6d28adb1f8ba31780fd35aa3ca4edbff7533ec4d', lines=210, adds=26, dels=4, cells_dev=3, cells=5, controls=1,
                       canon=[('P1P2P4', '2026-09-22_ks1180-ornith35b-night', '6a7e9f26a05dd819', 'strict', 26, 4, '@@ -10,5 +10,5 @@', None, None, '581ed7fa1')],
                       tampers=[('P1P2P4', AG + 'src/routes/verification.ts', 722, 2, [])])],
           adds=26, dels=4, lane_dev=697, lane_head=699, files_dev=71, files_head=71, typecheck=[(0, 1)],   # delta -1: the patch REMOVES the develop file's TS18046 idiom
           lock=('17:10:56Z', '17:16:40Z'), push=('17:10:57Z', '17:16:37Z'), ready='17:19:05Z', shell='44 passed, 0 failed (of 44)',
           census=(7, 1419, 1386, {'anchoring:4005 (ks1072-the-latest-anchor-selector-docume)': 15, 'anchoring:4005 (ks815-verification-router-guards-its-own)': 3, 'localhost:6000 (ks815-verification-router-guards-its-own)': 12}),
           title='KS-1180 P1P2P4: tier-2 verify cells count anchor-store hits, pin the _source carve-out', comments=2, prior_prs=['1029'], excised=None),
 '4': dict(n='1152', key='KS-1185', tags='F4', head='28d1e4df6da993e0363537a5144185d0892e4ca3', tree='1ffa57af71fb1475f950a32657e46e6daa69275d',
           branch='refs/heads/feature/ks-1185-gate-follow-ups-validate-the-approve-forward-timeout-r15-f4-1', lane='api-gateway', runner='vitest', tier=2,
           files=[dict(path=AG + 'src/__tests__/ks1185-workflow-approve-forward-default-bound.test.ts', mode='new', dev_blob=None, dev_lines=0,
                       blob='e231e3eac8cb959876db2694aac8eaeb2a9677b1', lines=108, adds=108, dels=0, cells_dev=0, cells=2, controls=1,
                       canon=[('F4', '2026-09-21_ks1185-ornith35b-night', 'f11b7d7af5e08411', 'trunc', 108, 0, '@@ -0,0 +1,97 @@', '4f68a823f31f', 97, '9f0265eb0')],
                       tampers=[('F4', AG + 'src/routes/verification.ts', 431, 1, [])])],
           adds=108, dels=0, lane_dev=697, lane_head=699, files_dev=71, files_head=72, typecheck=[(0, 0)],
           lock=('17:23:11Z', '17:28:54Z'), push=('17:23:11Z', '17:28:49Z'), ready='17:31:42Z', shell='44 passed, 0 failed (of 44)',
           census=(5, 1423, 1390, {'anchoring:4005 (ks1072-the-latest-anchor-selector-docume)': 15, 'anchoring:4005 (ks815-verification-router-guards-its-own)': 3, 'localhost:6000 (ks815-verification-router-guards-its-own)': 12}),
           title='KS-1185 F4: pin the approve route\'s production forward-timeout default (15000 ms)', comments=0, prior_prs=[], excised='ks-1183'),
 '5': dict(n='1154', key='KS-1199', tags='R15', head='889b0539117b2f31e777f47adde1d8f06a5c5de7', tree='f96a6cad291b350584870b2b9c0d2c47730f86e6',
           branch='refs/heads/feature/ks-1199-ks1072-verify-cells-pin-no-verdict-on-a-tie-whose-rows-r15-1', lane='api-gateway', runner='vitest', tier=2,
           files=[dict(path=AG + 'src/__tests__/ks1199-status-differing-anchor-tie-verdict.test.ts', mode='new', dev_blob=None, dev_lines=0,
                       blob='374193ef56832779b8a8c5922412ad93b9d2cc04', lines=113, adds=113, dels=0, cells_dev=0, cells=4, controls=1,
                       canon=[('R15', '2026-09-21_ks1199-ornith35b-night', '43dbab44c004f11d', 'strict', 113, 0, '@@ -0,0 +1,113 @@', None, None, '9f0265eb0')],
                       tampers=[('R15', AG + 'src/routes/verification.ts', 306, 3, [])])],
           adds=113, dels=0, lane_dev=697, lane_head=701, files_dev=71, files_head=72, typecheck=[(0, 0)],
           lock=('17:35:51Z', '17:41:46Z'), push=('17:35:51Z', '17:41:42Z'), ready='17:44:28Z', shell='44 passed, 0 failed (of 44)',
           census=(5, 1427, 1394, {'anchoring:4005 (ks1072-the-latest-anchor-selector-docume)': 15, 'anchoring:4005 (ks815-verification-router-guards-its-own)': 3, 'localhost:6000 (ks815-verification-router-guards-its-own)': 12}),
           title='KS-1199: pin the verdict on an equal-blockNumber anchor tie whose rows differ in status', comments=0, prior_prs=[], excised=None),
 '6': dict(n='1156', key='KS-1237', tags='ARRAYLIKE', head='58d293a87706f58321c8266e4bfeebc2686471d9', tree='6bb07e098ae86e8ff5621da06174e95b00b74698',
           branch='refs/heads/feature/ks-1237-ks1204-cells-three-tampers-stay-green-the-array-like-allow-r15-arraylike-1', lane='api-gateway', runner='vitest', tier=2,
           files=[dict(path=AG + 'src/__tests__/ks1204-a-non-array-allow-list-fails-closed-and-documenttype-wins.test.ts', mode='modify', dev_blob='f1f9840edd15ba8cbb764f675f5c2fdeef228dc7', dev_lines=292,
                       blob='6683a0c16446b5372ed2728d70e0e7723effd2ca', lines=299, adds=8, dels=1, cells_dev=9, cells=10, controls=1,
                       canon=[('ARRAYLIKE', '2026-09-22_ks1237-ornith35b-night', '5e5c810330cf04c9', 'strict', 8, 1, '@@ -243,3 +243,10 @@', None, None, '581ed7fa1')],
                       tampers=[('ARRAYLIKE', AG + 'src/routes/verification.ts', 1226, 1, [])])],
           adds=8, dels=1, lane_dev=697, lane_head=698, files_dev=71, files_head=71, typecheck=[(0, 0)],
           lock=('17:49:39Z', '17:55:27Z'), push=('17:49:40Z', '17:55:24Z'), ready='17:58:12Z', shell='44 passed, 0 failed (of 44)',
           census=(7, 1415, 1382, {'anchoring:4005 (ks1072-the-latest-anchor-selector-docume)': 15, 'anchoring:4005 (ks815-verification-router-guards-its-own)': 3, 'localhost:6000 (ks815-verification-router-guards-its-own)': 12}),
           title='KS-1237 ARRAYLIKE: an array-like allowedDocumentTypes object is not a list and fails closed', comments=1, prior_prs=[], excised=None),
 '7': dict(n='1158', key='KS-855', tags='SCOPETABLE', head='ddac6d7d5fe3362d3e0ff9633628d8367fcc6310', tree='6a1150f85f47bac11ef329bc00fc34813db7763d',
           branch='refs/heads/feature/ks-855-the-oauth-available_scopes-list-is-a-second-divergent-scope-r15-scopetable-1', lane='auth', runner='vitest', tier=1,
           files=[dict(path=AU + 'src/__tests__/ks855-the-oauth-available-scopes-list-is.test.ts', mode='new', dev_blob=None, dev_lines=0,
                       blob='6942187fc7730710b920d95cdb5b8662664e6d8f', lines=82, adds=82, dels=0, cells_dev=0, cells=4, controls=1,
                       canon=[('SCOPETABLE', '2026-09-22_ks855-ornith35b-night', '500f8ca4aa5ccc3e', 'strict', 82, 0, '@@ -0,0 +1,82 @@', None, None, '581ed7fa1')],
                       tampers=[('SCOPETABLE', AU + 'src/services/oauth.ts', 66, 2, [])])],
           adds=82, dels=0, lane_dev=786, lane_head=790, files_dev=66, files_head=67, typecheck=[(0, 0)],
           lock=('18:03:00Z', '18:09:12Z'), push=('18:03:00Z', '18:09:09Z'), ready='18:11:58Z', shell='44 passed, 0 failed (of 44)',
           census=(5, 624, 624, {}), title='KS-855 SCOPETABLE: pin how the OAuth scope list and the shared SCOPES vocabulary relate', comments=0, prior_prs=[], excised=None),
 '8': dict(n='1160', key='KS-944', tags='SPECPIN', head='ef4713cc66c07b1b013cbd7d7ca0ea2fe5a4f5b2', tree='a1541f731c609fa48a9a45ae1013afccf181d985',
           branch='refs/heads/feature/ks-944-the-gateways-auth-gate-reads-the-specs-security-nothing-pins-r15-specpin-1', lane='auth', runner='vitest', tier=1,
           files=[dict(path=AU + 'src/__tests__/ks944-the-gateway-s-auth-gate-reads.test.ts', mode='new', dev_blob=None, dev_lines=0,
                       blob='5fca556553a626c9b96d49da02ac0ebd1cbfcecd', lines=57, adds=57, dels=0, cells_dev=0, cells=3, controls=1,
                       canon=[('SPECPIN', '2026-09-22_ks944-ornith35b-night', '25a6cc7721ccf6e2', 'strict', 57, 0, '@@ -0,0 +1,57 @@', None, None, '581ed7fa1')],
                       tampers=[('SPECPIN', AU + 'src/auth.openapi.ts', 1829, 1, [])])],
           adds=57, dels=0, lane_dev=786, lane_head=789, files_dev=66, files_head=67, typecheck=[(0, 0)],
           lock=('18:16:41Z', '18:22:55Z'), push=('18:16:42Z', '18:22:50Z'), ready='18:25:36Z', shell='44 passed, 0 failed (of 44)',
           census=(5, 624, 624, {}), title='KS-944 SPECPIN: pin the security list the six wallet operations declare in the auth spec', comments=0, prior_prs=[], excised=None),
 '9': dict(n='1162', key='KS-1156', tags='R15', head='b6b70d7870222cd746c8a9b98a423ef95a657568', tree='8f0a5145c5dd2ba840b08352cb6fa5e5f3ac5d31',
           branch='refs/heads/feature/ks-1156-auth4-gate-records-983-r2-984-r2-986-987-h-limiter-r15-r15-1', lane='auth', runner='vitest', tier=1,
           files=[dict(path=AU + 'src/__tests__/ks1156-auth4-gate-records-983-r2-984.test.ts', mode='new', dev_blob=None, dev_lines=0,
                       blob='56ef7e523469f3a0e63523f8af8fbc3d761b22da', lines=111, adds=111, dels=0, cells_dev=0, cells=3, controls=2,
                       canon=[('R15', '2026-09-21_ks1156-ornith35b-night', 'c6214df3bf4b6178', 'strict', 111, 0, '@@ -0,0 +1,111 @@', None, None, '581ed7fa1')],
                       tampers=[('R15', AU + 'src/routes/auth.ts', 677, 1, [])])],
           adds=111, dels=0, lane_dev=786, lane_head=789, files_dev=66, files_head=67, typecheck=[(0, 0)],
           lock=('18:29:29Z', '18:35:34Z'), push=('18:29:30Z', '18:35:30Z'), ready='18:38:17Z', shell='44 passed, 0 failed (of 44)',
           census=(6, 840, 840, {}), title='KS-1156 R-C2: POST /api/auth/refresh refuses a label-only OAuth refresh token', comments=0, prior_prs=['1146'], excised=None),
 '10': dict(n='1163', key='KS-1188', tags='F1a F1b F2', head='02f12926f248bcc879e1f437d51a306a829b3c8b', tree='41b33c17d906b18b9ab59d777a5a0827061fdc1c',
           branch='refs/heads/feature/ks-1188-1013-gate-findings-the-getuserbyid-route-level-503-r15-f1a-f1b-f2-1', lane='auth', runner='vitest', tier=1,
           files=[dict(path=AU + 'src/__tests__/ks1188-mfa-status-503-route.test.ts', mode='new', dev_blob=None, dev_lines=0,
                       blob='5213553cca6ad057bee0e7d2fc5888f15ebd07eb', lines=136, adds=136, dels=0, cells_dev=0, cells=5, controls=2,
                       canon=[('F1a', '2026-09-22_ks1188-ornith35b-night', '1da74333f4903fbe', 'strict', 136, 0, '@@ -0,0 +1,136 @@', None, None, '581ed7fa1')],
                       tampers=[('F1A', AU + 'src/routes/mfa.ts', 143, 3, [])]),   # `from` occurs THREE times in mfa.ts (:143, :166, :397) — the anchor-ambiguity row
                  dict(path=AU + 'src/__tests__/ks1188-users-me-503-route.test.ts', mode='new', dev_blob=None, dev_lines=0,
                       blob='2cd754d9ba5629a46aea8b2b3ebc8491a88ce153', lines=144, adds=144, dels=0, cells_dev=0, cells=5, controls=2,
                       canon=[('F1b', '2026-09-22_ks1188-ornith35b-night2', '81ac27882e17b4e5', 'strict', 144, 0, '@@ -0,0 +1,144 @@', None, None, '581ed7fa1')],
                       tampers=[('F1B', AU + 'src/routes/users.ts', 910, 3, [])]),
                  dict(path=AU + 'src/__tests__/ks1188-getuserbyid-failed-log-meta-keys.test.ts', mode='new', dev_blob=None, dev_lines=0,
                       blob='cb0905a4d4e1ad3f7345d7f67471b9e91c3da791', lines=122, adds=122, dels=0, cells_dev=0, cells=5, controls=2,
                       canon=[('F2', '2026-09-21_ks1188-ornith35b-night', '10c953d4604b4618', 'trunc', 122, 0, '@@ -0,0 +1,97 @@', '686a707056af', 97, '9f0265eb0')],
                       tampers=[('F2', AU + 'src/repositories/userRepo.ts', 413, 3, [])])],
           adds=402, dels=0, lane_dev=786, lane_head=801, files_dev=66, files_head=69, typecheck=[(0, 0), (0, 0), (0, 0)],
           lock=('18:37:03Z', '18:43:01Z'), push=('18:37:03Z', '18:42:57Z'), ready='18:46:40Z', shell='44 passed, 0 failed (of 44)',
           census=(13, 1480, 1480, {}), title='KS-1188 F1a+F1b+F2: pin the 503 on a DEK-read fault (mfa/status, users/me) and its log meta', comments=0, prior_prs=[], excised='ks-999'),
 '11': dict(n='1164', key='KS-1193', tags='F1 F2', head='ba730c6ac4fee7c7994531b8e4b9b62fed297830', tree='3759873dfbd503f1378a7e8b36e1deb6e28b0fd0',
           branch='refs/heads/feature/ks-1193-1015-gate-findings-the-message-form-pool-timeout-the-r15-f1-f2-1', lane='auth', runner='vitest', tier=1,
           files=[dict(path=AU + 'src/__tests__/ks1193-verification-reads-codeless-pool-timeout.test.ts', mode='new', dev_blob=None, dev_lines=0,
                       blob='42213aa17a54759d114e12193ebb498e7d8f9657', lines=153, adds=153, dels=0, cells_dev=0, cells=4, controls=1,
                       canon=[('F1', '2026-09-21_ks1193-ornith35b-night', 'ffd0347dfac13ad8', 'trunc', 153, 0, '@@ -0,0 +1,124 @@', '610c209861d1', 124, '9f0265eb0')],
                       tampers=[('F1', AU + 'src/routes/users.ts', 17, 3, [])]),
                  dict(path=AU + 'src/__tests__/ks1193-review-read-query-error-is-not-503.test.ts', mode='new', dev_blob=None, dev_lines=0,
                       blob='862f7ea5cc053afa2b2fcfcfc9c64d68ff7cfc1c', lines=117, adds=117, dels=0, cells_dev=0, cells=3, controls=1,
                       canon=[('F2', '2026-09-22_ks1193-ornith35b-night', '25df949c29a47684', 'strict', 117, 0, '@@ -0,0 +1,117 @@', None, None, '581ed7fa1')],
                       tampers=[('F2', AU + 'src/routes/users.ts', 1199, 2, [])])],
           adds=270, dels=0, lane_dev=786, lane_head=793, files_dev=66, files_head=68, typecheck=[(0, 0), (0, 0)],
           lock=('18:44:45Z', '18:50:54Z'), push=('18:44:45Z', '18:50:50Z'), ready='18:53:20Z', shell='44 passed, 0 failed (of 44)',
           census=(10, 1268, 1268, {}), title='KS-1193 F1+F2: a codeless pool timeout answers 503 on each verification read; a pg error not', comments=0, prior_prs=[], excised='ks-1018'),
 '12': dict(n='1165', key='KS-1217', tags='TESTPINFULLMESSAGE', head='4ecb09cf2c1d623e59bf3ec03db262b1d6108f64', tree='395e34b93d13662a239c2c41d81df61be005d424',
           branch='refs/heads/feature/ks-1217-ks1050-c1-pins-only-the-helper-message-prefix-plus-a-3-r15-testpinfullmessage-1', lane='auth', runner='vitest', tier=1,
           files=[dict(path=AU + 'src/__tests__/ks1050-profile-update-zero-rows-is-not-success.test.ts', mode='modify', dev_blob='ffb3e801ab371bed4a11accd0dbcc64bd8fdc804', dev_lines=185,
                       blob='80ddfb3f0fa712f42db71ec61908f94855e63732', lines=186, adds=2, dels=1, cells_dev=4, cells=4, controls=1,
                       canon=[('TESTPINFULLMESSAGE', '2026-09-22_ks1217-ornith35b-night', 'cdaf4d17e0308c8e', 'strict', 2, 1, '@@ -143,10 +143,11 @@', None, None, '581ed7fa1')],
                       tampers=[('TESTPINFULLMESSAGE', AU + 'src/repositories/userRepo.ts', 973, 1, [])])],
           adds=2, dels=1, lane_dev=786, lane_head=786, files_dev=66, files_head=66, typecheck=[(0, 0)],
           lock=('18:52:43Z', '18:58:52Z'), push=('18:52:43Z', '18:58:49Z'), ready='19:02:02Z', shell='44 passed, 0 failed (of 44)',
           census=(8, 840, 840, {}), title='KS-1217: the zero-row profile update cell pins the WHOLE 503 message, not its prefix', comments=0, prior_prs=[], excised=None),
 '13': dict(n='1166', key='KS-910', tags='LEGCOMMENT', head='a08741f513510f979936ee2a0dcc48d270f21a65', tree='fa1771ac07e554c999bbb36a4ab04752939d78d0',
           branch='refs/heads/feature/ks-910-preflight-leg-12-executes-zero-suite-cells-it-is-a-r15-legcomment-1', lane='scripts', runner='bash', tier=2,
           files=[dict(path=SC + '__tests__/pre_push_hook_base.test.sh', mode='modify', dev_blob='affdf027bff11e3690d374e902e3e93274788c62', dev_lines=646,
                       blob='e33da9a44e112c64bd887e7b434c9a39b0ecc7eb', lines=646, adds=3, dels=3, cells_dev=28, cells=28, controls=0,
                       canon=[('section_1', 'section_1.diff.reanchored', '9d6dccc83f8020df', 'strict', 3, 3, '@@ -46,9 +46,9 @@', None, None, '9f0265eb0')], tampers=[]),
                  dict(path=SC + '__tests__/pre_push_hook_base_leg_comment.test.sh', mode='new', dev_blob=None, dev_lines=0,
                       blob='a1598f1163d730e15951f2e3449d6a8ea7d55ceb', lines=58, adds=58, dels=0, cells_dev=0, cells=4, controls=2,
                       canon=[('section_2', 'section_2.diff', 'ebb9a15ecfa32f88', 'strict', 58, 0, '@@ -0,0 +1,58 @@', None, None, '9f0265eb0')], tampers=[])],
           adds=61, dels=3, lane_dev=28, lane_head=32, files_dev=1, files_head=2, typecheck=[],
           lock=('19:00:45Z', '19:06:34Z'), push=('19:00:46Z', '19:06:31Z'), ready='19:08:40Z', shell='45 passed, 0 failed (of 45)',   # F-45: the NEW bash suite ran in-hook as the 45th
           census=None, title='KS-910 LEGCOMMENT: the pre-push base suite\'s comment names leg 14, not 12; a suite pins it', comments=0, prior_prs=[], excised=None),
}
KS910_RUN = '2026-09-21_ks910-ornith35b-night'   # its patch.diff b660b8c4b260f1f5 / 4097 B does NOT apply at 64ab10513 (strict rc 1, --recount rc 1) — the two section files are the canonical
KS910_FENCE16 = 'b660b8c4b260f1f5'
HELD = dict(key='KS-1123', tag='F3b', commit='b8335a32e', worktree='s-c16-ks1123', file=AG + 'src/__tests__/ks1123-api-gateway-verify-an-empty-string.test.ts',
            canon=('F3b', '2026-09-21_ks1123-ornith35b-night3', 'e27114b1b3ae0fb7', 'strict', 215, 0), blob12='71056725acfc', tree12='7e484101c067',
            defect="src/__tests__/ks1123-api-gateway-verify-an-empty-string.test.ts(158,10): error TS18046: 'body' is of type 'unknown'.")
# the seat's item-0 tamper-file blobs (8 files; the drafter's rev-parse 19:1xZ: identical at 581ed7fa1 and 9f0265eb0)
TAMPER_BLOBS = [(AG + 'src/routes/system-status.ts', 'e911ce1fdaa4b755e9b7b6428f899cdbd63889cb'), (AG + 'src/routes/verification.ts', 'f888e8cd0bd10c98a508542d75902ab122595157'),
                (AU + 'src/services/oauth.ts', '8995edec6a43b7623def6c9d1b002ed0a1b0dc86'), (AU + 'src/auth.openapi.ts', '2c356c3c7877add99f5e1a3c437d04ac8be3dc76'),
                (AU + 'src/routes/auth.ts', '18946cd7c5c394d89ecbecf860ab66a96b1e22c7'), (AU + 'src/routes/mfa.ts', '87d3ee1079fe90010f45955dbaf4307ae595b205'),
                (AU + 'src/routes/users.ts', '3bfa47dcde0125d9e23cb8a9fbddf7bd40aa0b2d'), (AU + 'src/repositories/userRepo.ts', '9060b308e6d6a82c8a79be7387032d2a18c4ac22')]
# Seat B 16th's EIGHT pushed PRs (its READYs captured beside 19:13Z; its PR 8 KS-1171 HELD): (n, key, head, path)
OR = D + 'services/originate/'; SH = D + 'packages/shared/'; SE = D + 'services/security/'; AN = D + 'services/anchoring/'
SEATB = [('1147', 'KS-928', 'e456ffb5e9e1e1525f155864452c0aa2cad8752b', OR + 'src/__tests__/ks928-the-demo-seed-gate-s-predicate.test.ts'),
         ('1149', 'KS-1118', '75f5b924ea28b3a9a68e8d02af8f95f16c28c99d', OR + 'src/__tests__/ks1118-verify-documenthash-over-hash.test.ts'),
         ('1151', 'KS-1133', '10c689dcfb1722c993046a115be82b951db0596f', OR + 'src/__tests__/ks1133-v2-verify-hash-read-first.test.ts'),
         ('1153', 'KS-1158', 'be21a0ae404c04a966379773a18ce5b5674f8e4b', OR + 'src/__tests__/ks1158-r3-network-carry-second-pin.test.ts'),
         ('1155', 'KS-1229', 'b455e4594865cfd63aea486139d6afae182eb3c6', OR + 'src/__tests__/ks1213-a-derived-writer-relabel-is-refused.test.ts'),
         ('1157', 'KS-1179', '8b0713d8ff33c1e4e7690ec6b6b8bb1cda0d138f', SH + 'src/__tests__/ks1179-safeoutboundrequest-tests-no-cell-pins-dns.test.ts'),
         ('1159', 'KS-1181', 'c6af5ca678c4a1ae3aba6bc4cd7a98f796247929', SH + 'src/__tests__/ks1181-ks-727-error-handler-guard-corpus.test.ts'),
         ('1161', 'KS-975', '7f426f1706bd40a5dd800502d5af9a1968611718', SE + 'src/__tests__/ks975-malformed-sub-is-refused.test.ts')]
SEATB_KEYS = ['KS-928', 'KS-1118', 'KS-1133', 'KS-1158', 'KS-1229', 'KS-1179', 'KS-1181', 'KS-1171', 'KS-975']
SEATB_DIRS = [OR, SH, SE, AN]
SEATB_ALL8 = 'c54c1ae73ba32d9bdd7ed3258a9c19e59ad5cb1d'
ARCHIVED = ['KS-501', 'KS-480', 'KS-978', 'KS-721', 'KS-522', 'KS-726', 'KS-535', 'KS-867', 'KS-878', 'KS-914', 'KS-1238', 'KS-1282', 'KS-1062', 'KS-971', 'KS-1078', 'KS-921', 'KS-490',
            'KS-597', 'KS-727', 'KS-764', 'KS-879', 'KS-1020', 'KS-835', 'KS-1270']   # 24 (the READYs' ARCHIVED-TICKET READS block)
CONTENT_LIVE = ['KS-1213', 'KS-1073', 'KS-1050', 'KS-1204', 'KS-1072', 'KS-1183', 'KS-999', 'KS-1018', 'KS-1285', 'KS-1031', 'KS-1175', 'KS-1250', 'KS-1273', 'KS-958']   # 14 (the READYs' Live-but-foreign / content / HOLDS block)
OWN = [PRS[p]['key'] for p in PUSH]
OWN13 = ['KS-864', 'KS-1123', 'KS-1180', 'KS-1185', 'KS-1199', 'KS-1237', 'KS-855', 'KS-944', 'KS-1156', 'KS-1188', 'KS-1193', 'KS-1217', 'KS-910']
AUTH_PINS = ['7', '8', '9', '10', '11', '12']   # the six auth-surface pins — tier 1 (the commission item 1)
def run_patch(d): return LM + '/runs/' + d + '/out.md.checker/patch.diff'
def ks910_section(name): return LM + '/runs/' + KS910_RUN + '/out.md.checker/' + name
def canon_path(row):
    return ks910_section(row[1]) if row[1].startswith('section_') else run_patch(row[1])
def ready_regex(): return r'READY FOR QA \(Seat C 16th\): PR (\d+) (KS-\d+)[^\n]*? — #(\d+) at head ([0-9a-f]{40})'
def all_paths(): return [f['path'] for p in PUSH for f in PRS[p]['files']]
