"""round18B.py — the ONE source of this round's pins for every gate18B drafter script (a wrong pin in the prompt is the most expensive slip; every
script imports this module and asserts against origin / local objects / the READYs — the gate16B / gate18C round*.py shape).
Values: the seat's SEVEN READY mails (mail_seatB18_ready*.md, captured 01:15:52Z; EIGHT READY rows — PR 4 carries KS-1171 8J-TSFIX + GUARD3S-TSFIX),
its 23:47Z (SEVEN RAISED + COMMITTED) STATUS and its 01:08:36Z HOLDING STATUS (the HOLD), its 22:50Z plan confirmation (ITEM 0) + 23:29Z baselines
QUESTION, Wednesday's brief (briefs_staged/2026-09-22_raise_seatB_18.md GROUPING + QUEUE, as the seat's ITEM 0 restates it), her plan ANSWER
22:52:30Z and her (b) ruling 23:30:26Z, the drafter's ls-remote 01:14:19Z (lsremote_1.out) and its `git diff --raw --abbrev=40 3916eacd1 <head>` x7
(local_reads_1.out — the 40-hex blobs). Every value is a CLAIM until a script re-derives it; the scripts print the disagreement, never adopt."""
PARENT = '3916eacd12af23bfd464440b4c770f7da0f2dd96'; PARENT_TREE = '4b573853be61832f3adc14656de742b6051d5622'   # every head's parent (the seat's item-0 tip, BEFORE #1036); subject "KS-910 LEGCOMMENT: ... (#1166)"
DEV = '8c2f7b3fd4fde915b2a24542bc32259b24e092a0'; DEV_TREE = '04b05e093ad8b3d6e55b0fe553d7deb96b247050'         # origin develop at the drafter's reads (the #1036 squash "KS-763: qs in range on express 4 ... (#1036)"; first-parent count 3916eacd1..8c2f7b3fd = 1)
PR1036_HEAD = '4b251997a96034ee8a3359aac357ee17d222c3ef'   # #1036's head; the seat's item 0: merge-tree 3916eacd1 x 4b251997a -> 04b05e093ad8 (= DEV_TREE); 50 paths (20 package.json + 29 package-lock.json + scripts/audit/audit-baseline.json)
TIP64 = '64ab105132eada0621622acf4d6053bc59926780'          # the R16 checker tip (KS-1265, KS-1171 x2, KS-811)
TIP19F = '19f1e5475'; TIP75A = '75ad0e55c'                  # the older comment rows' checker tips (KS-1118 F3b; KS-1158 R5b + KS-1181 F3w) — short forms as the READYs carry them
SEAT_ALL7 = 'a36532029483c3f8a4ca0cd33ec1219076ef9219'     # the all-7 (eight READY rows) tree over PARENT (the seat's item 0 + batch: forward / reverse / seed-18 shuffle ONE sha; = the s-b18-batch octopus 5185c65cf's tree, never pushed)
SEAT_ALL7_SHORTSTAT = '9 files changed, 513 insertions(+), 11 deletions(-)'
SEAT_OCTOPUS = '5185c65cf'   # the seat's s-b18-batch octopus (8 parents, first parent 3916eacd1) — in the shared store at the drafter's read (local_reads_1.out)
D = 'Blockchain/Dev/'; OR = D + 'services/originate/'; SH = D + 'packages/shared/'; SE = D + 'services/security/'; AN = D + 'services/anchoring/'; AU = D + 'services/auth/'; AG = D + 'services/api-gateway/'; SC = D + 'scripts/'
LM = '/Volumes/DevMASTER/WEDNESDAY/2_Project_Files/local-model'
REPO = '/Volumes/DevMASTER/!CODING/Secuura/Blockchain/2_Project_Files'
PUSH = ['1', '2', '3', '4', '5', '6', '7']
# a canonical row: (label, run dir, file name under out.md.checker/, sha256[:16], apply options ('' = strict on EVERY row this round — the seat's Q5; no .opts carries an option), adds, dels, first hunk header)
# a file row: dict(path, kind test|product, mode new|modify, dev_blob (40) or None, dev_lines, blob (40 = the head blob), lines, adds, dels, cells_dev, cells, controls, canon=[...], tampers=[(label, path, line, from_count_substring, from_count_wholeline, reds_declared, cover_cells_at_develop, scope_line, scope_text)])
PRS = {
 '1': dict(n='1170', key='KS-1118', tags='F3b', kind='comment', head='3e9f7d7b707da88e666ff94c769658f2ba3894b8', tree='93d47128217761a588c54a51f60a78ef19a9c91b',
           branch='refs/heads/feature/ks-1118-post-apiverificationverify-the-documenthash-over-hash-r18-f3b-1', lane='originate', runner='jest', tier=2,
           files=[dict(path=OR + 'src/__tests__/ks1103-verify-hash-field.test.ts', kind='test', mode='modify', dev_blob='ac76fc1da6861c9c8e3a76c17035c3c5c7791346', dev_lines=266,
                       blob='58eefc2aecd2fa274be2f2d916d5a6f7ab68aa2f', lines=271, adds=7, dels=2, cells_dev=14, cells=14, controls=None,
                       canon=[('F3b', '2026-09-17_ks1118-ornith35b-night2', 'patch.diff', 'd0b78a1ab0fa2bcc', '', 7, 2, None)], tampers=[])],
           adds=7, dels=2, comment_lines=9, lane_dev=835, lane_head=835, files_dev=71, files_head=71, typecheck=[(0, 0)], eslint=[(0, 0)],
           lock=('23:52:36Z', '23:58:52Z'), push=('23:52:36Z', '23:58:46Z'), ready='00:02:34Z', shell='45 passed, 0 failed (of 45)', a4=None,
           census=(3, 107, 89, {'anchoring:4005 (unattributed)': 17}), title='KS-1118 F3b: narrow the why-comment in the v1 verify-hash pins to alias-carrying bodies',
           comments=0, prior_prs=['1149'], excised=None, tip='19f1e5475', boot_state='In Progress', bot_walk=False),
 '2': dict(n='1172', key='KS-1158', tags='R5b', kind='comment', head='d74b04678574f5cb7828a82f84577882a3496a66', tree='25f2d6767be9ad1f7c34196a0c97636e56bcf48f',
           branch='refs/heads/feature/ks-1158-l3a-gate-records-912-r2-937-the-placeholder-hash-anchoredat-r18-r5b-1', lane='originate', runner='jest', tier=2,
           files=[dict(path=OR + 'src/__tests__/ks1058-anchor-failed-preserves-thread-token.test.ts', kind='test', mode='modify', dev_blob='1c78b4a618d1ae5ffaab03ccb40bb27df0d22e70', dev_lines=198,
                       blob='0a9573c19f3c89c5973ca4fec6efb4110ba4231e', lines=198, adds=1, dels=1, cells_dev=6, cells=6, controls=None,
                       canon=[('R5b', '2026-09-17_ks1158-ornith35b-night', 'patch.diff', '1fb99c3994dc07e9', '', 1, 1, None)], tampers=[])],
           adds=1, dels=1, comment_lines=2, lane_dev=835, lane_head=835, files_dev=71, files_head=71, typecheck=[(0, 0)], eslint=[(0, 0)],
           lock=('00:05:32Z', '00:11:23Z'), push=('00:05:33Z', '00:11:20Z'), ready='00:14:13Z', shell='45 passed, 0 failed (of 45)', a4=None,
           census=(3, 103, 85, {'anchoring:4005 (unattributed)': 17}), title="KS-1158 R5b: re-point the anchor-failed test header's shallow-spread citation",
           comments=0, prior_prs=['1153'], excised=None, tip='75ad0e55c', boot_state='In Progress', bot_walk=False),
 '3': dict(n='1174', key='KS-1265', tags='EARLYGUARD', kind='code_patch', head='e1dea649c7e338ba70a67acd8ce2957edd8058c9', tree='d8a095b551987c6926cbeb7f1a1f2a973cf17ad0',
           branch='refs/heads/feature/ks-1265-post-apidocuments-saves-the-document-and-its-provenance-row-r16-earlyguard-1', lane='originate', runner='jest', tier=1,
           files=[dict(path=OR + 'src/__tests__/ks549-documents-create-issuer-name-persist.test.ts', kind='test', mode='modify', dev_blob='62c767fccf5525ed67316500803b1163eeb547b9', dev_lines=163,
                       blob='d32b112102fdf39a9d82cbb3b6a0f1ea6236a304', lines=160, adds=4, dels=7, cells_dev=4, cells=4, controls=3,
                       canon=[('EARLYGUARD-s2', '2026-09-22_ks1265-ornith35b-night', 'section_2.diff', '375f588f53cfea3e', '', 4, 7, '@@ -141,11 +141,8 @@')], tampers=[]),
                  dict(path=OR + 'src/routes/documents.ts', kind='product', mode='modify', dev_blob='3f837fc6e656d5a10f9cc349b1cb2a876a2be09b', dev_lines=3060,
                       blob='1089377e11466bd847cb13420f8129aa7737a1ef', lines=3068, adds=8, dels=0, cells_dev=None, cells=None, controls=None,
                       canon=[('EARLYGUARD-s1', '2026-09-22_ks1265-ornith35b-night', 'section_1.diff', '0dc85536c0fe8565', '', 8, 0, '@@ -611,6 +611,14 @@')], tampers=[])],
           adds=12, dels=7, lane_dev=835, lane_head=835, files_dev=71, files_head=71, typecheck=[(0, 0)], eslint=[(0, 0), (0, 0)],   # typecheck on the TEST file (delta 0); documents.ts eslint develop 0 -> head 0
           canon_full=('EARLYGUARD', '2026-09-22_ks1265-ornith35b-night', 'patch.diff', 'd955f73e1c5d70c3'),   # cat(section_1, section_2) == patch.diff
           lock=('00:18:09Z', '00:23:58Z'), push=('00:18:09Z', '00:23:54Z'), ready='00:27:02Z', shell='45 passed, 0 failed (of 45)',
           a4={'EARLYGUARD': (1, 4, ['KS-549 POST /api/documents — top-level issuerName persists into data never persists an email-shaped issuerName (E-01 guard parity)'])},
           census=(3, 107, 89, {'anchoring:4005 (unattributed)': 17}), title='KS-1265 EARLYGUARD: refuse an email-shaped issuerName before the document is saved',
           comments=0, prior_prs=[], excised=None, tip='64ab10513', boot_state='Backlog', bot_walk=True),
 '4': dict(n='1176', key='KS-1171', tags='8J-TSFIX GUARD3S-TSFIX', kind='test_only', head='8ced0d50bb457d04b186b58a504e69b28052afb5', tree='96b4b7c9a42bb82a5141b6b1286f17fcd973c638',
           branch='refs/heads/feature/ks-1171-guard-3s-re-poll-reads-a-mixed-window-as-absent-one-early-r16-8j-tsfix-guard3s-tsfix-1', lane='anchoring', runner='vitest run', tier=2,
           files=[dict(path=AN + 'src/__tests__/ks1171-8j-confirmed-wins-over-polled-zero.test.ts', kind='test', mode='new', dev_blob=None, dev_lines=0,
                       blob='c0c345bd0aae0d01c825cac91819db2870e53b9f', lines=127, adds=127, dels=0, cells_dev=0, cells=3, controls=1,
                       canon=[('8J-TSFIX', '2026-09-22_ks1171-ornith35b-night', 'patch.diff', 'b1d9f5127e3b210f', '', 127, 0, '@@ -0,0 +1,127 @@')],
                       tampers=[('8J', AN + 'src/anchorSubmission.ts', 260, 2, 1, ['RED KS-1171 8j - an injected confirmed:true with polled 0 CONFIRMS the row', 'RED KS-1171 8j - no never-reached-the-chain log wh'], [], 255, 'const current = await deps.getAnchor(anchorId);')]),
                  dict(path=AN + 'src/__tests__/ks1171-guard-3-s-re-poll-reads.test.ts', kind='test', mode='new', dev_blob=None, dev_lines=0,
                       blob='a7d2c4bb37996e452bfd62b5952b191cc73c5946', lines=107, adds=107, dels=0, cells_dev=0, cells=3, controls=1,
                       canon=[('GUARD3S-TSFIX', '2026-09-22_ks1171-ornith35b-night2', 'patch.diff', '03a43332e63fbc36', '', 107, 0, '@@ -0,0 +1,107 @@')],
                       tampers=[('8J', AN + 'src/anchorSubmission.ts', 260, 2, 1, ['RED KS-1171 8j - an injected confirmed:true with polled 0 CONFIRMS the row', 'RED KS-1171 8j - no never-reached-the-chain log wh'], [], 255, 'const current = await deps.getAnchor(anchorId);')])],
           adds=234, dels=0, lane_dev=329, lane_head=335, lane_dev_red=1, lane_head_red=1, files_dev=22, files_head=24, typecheck=[(0, 0), (0, 0)], eslint=[(0, 0), (0, 0)],
           lock=('00:30:20Z', '00:36:26Z'), push=('00:30:21Z', '00:36:20Z'), ready='00:40:21Z', shell='45 passed, 0 failed (of 45)', a4=None,
           census=(8, 0, 0, {}), title='KS-1171 8J-TSFIX GUARD3S-TSFIX: pin confirmed-wins-over-polled-zero at the anchor confirm',
           comments=0, prior_prs=[], excised=None, tip='64ab10513', boot_state='Backlog', bot_walk=True),
 '5': dict(n='1177', key='KS-811', tags='F7SETPIN', kind='test_only', head='13030ac59743c0df869bcf56ae10311445ae94d7', tree='b7fd625c7c73de5b93ccbc2d5bbd86362316c698',
           branch='refs/heads/feature/ks-811-nothing-asserts-815s-403-code-set-against-what-the-route-r16-f7setpin-1', lane='auth', runner='vitest', tier=1,
           files=[dict(path=AU + 'src/__tests__/ks811-social-callback-403-code-set-agrees.test.ts', kind='test', mode='new', dev_blob=None, dev_lines=0,
                       blob='b6fbff22e99ca13930608f87ea70829e3c5f07f8', lines=111, adds=111, dels=0, cells_dev=0, cells=6, controls=2,
                       canon=[('F7SETPIN', '2026-09-22_ks811-ornith35b-night', 'patch.diff', '153d942ec3df0ece', '', 111, 0, '@@ -0,0 +1,111 @@')],
                       tampers=[('SPECRENAME', AU + 'src/auth.openapi.ts', 2097, 1, 1, ['RED KS-811 - the operation 403 block in auth.openapi.ts names exactly those four', 'RED KS-811 - the published 403 set and the thrown '], [], None, None),
                                ('ROUTECOLLAPSE', AU + 'src/routes/auth.ts', 1081, 1, 1, ['RED KS-811 - the callback route can throw exactly ', 'RED KS-811 - the published 403 set and the thrown '],
                                 ['ks795-social-link-verified-email.test.ts :: refuses terminally when the provider supplies no email and nothing matched by identity'], 1077, 'if (!user && !profileEmail) {')])],
           adds=111, dels=0, lane_dev=818, lane_head=824, files_dev=74, files_head=75, typecheck=[(0, 0)], eslint=[(0, 0)],
           lane_head_preload=824, lane_wall=('3.4 s', '3.4 s'),
           lock=('00:39:13Z', '00:45:43Z'), push=('00:39:13Z', '00:45:38Z'), ready='00:49:17Z', shell='45 passed, 0 failed (of 45)', a4=None,
           census=(4, 218, 218, {}), title="KS-811 F7SETPIN: pin the social-callback 403 code set against the route's thrown classes",
           comments=1, prior_prs=[], excised=None, tip='64ab10513', boot_state='Backlog', bot_walk=True),
 '6': dict(n='1178', key='KS-1188', tags='MFASIBLINGS', kind='test_only', head='e48b90e747def96b708f02890d2aa66ce10e52c0', tree='d081ff92369d8c4959a49f02d96d9532036b7410',
           branch='refs/heads/feature/ks-1188-1013-gate-findings-the-getuserbyid-route-level-503-r16-mfasiblings-1', lane='auth', runner='vitest', tier=1,
           files=[dict(path=AU + 'src/__tests__/ks1188-mfa-sibling-sites-503.test.ts', kind='test', mode='new', dev_blob=None, dev_lines=0,
                       blob='3e9b78aeaf5b5c7e28e88577e0d0ddab5cd739fd', lines=147, adds=147, dels=0, cells_dev=0, cells=4, controls=2,
                       canon=[('MFASIBLINGS', '2026-09-22_ks1188-ornith35b-night4', 'patch.diff', '00c50c7ad6828df2', '', 147, 0, '@@ -0,0 +1,147 @@')],
                       tampers=[('F1C', AU + 'src/routes/mfa.ts', 166, 1, 1, ['RED KS-1188 F1c - POST /api/auth/mfa/setup/start answers 503 SERVICE_UNAVAILABLE'], [], 161, "mfaRoutes.post('/setup/start', authenticate(), asy"),
                                ('F1D', AU + 'src/routes/mfa.ts', 396, 1, 1, ['RED KS-1188 F1d - POST /api/auth/mfa/backup-codes/regenerate answers 503 SERVICE'], [], 391, "mfaRoutes.post('/backup-codes/regenerate', authent")])],
           adds=147, dels=0, lane_dev=818, lane_head=822, files_dev=74, files_head=75, typecheck=[(0, 0)], eslint=[(0, 0)],
           lane_head_preload=822, lane_wall=('3.5 s', '3.6 s'),
           lock=('00:47:57Z', '00:53:49Z'), push=('00:47:58Z', '00:53:46Z'), ready='00:57:02Z', shell='45 passed, 0 failed (of 45)', a4=None,
           census=(4, 226, 226, {}), title='KS-1188 MFASIBLINGS: pin the 503 on a getUserById DEK fault at the two MFA sibling sites',
           comments=0, prior_prs=['1163'], excised='ks-999', tip='3916eacd1', boot_state='In Progress', bot_walk=False),
 '7': dict(n='1179', key='KS-1181', tags='F3w', kind='comment', head='e62555dd00eb2cdfa8d73c0f9329f4ac467ffa0c', tree='560e6992e4da482ec5ca38a59ece99868f2df155',
           branch='refs/heads/feature/ks-1181-error-handler-guard-corpus-1-canary-cells-cannot-r18-f3w-1', lane='shared', runner='vitest run', tier=2,
           files=[dict(path=SH + 'src/__tests__/ks727-errorhandler-class-guard.test.ts', kind='test', mode='modify', dev_blob='5127297156ed9b970ad17e804b3e3211894b6f8c', dev_lines=946,
                       blob='35eb27404fd615886d3f03ba7e691be97051f1ee', lines=946, adds=1, dels=1, cells_dev=103, cells=103, controls=None,
                       canon=[('F3w', '2026-09-17_ks1181-ornith35b-night2', 'patch.diff', 'd628409f8774aaf2', '', 1, 1, None)], tampers=[])],
           adds=1, dels=1, comment_lines=2, lane_dev=917, lane_head=917, files_dev=46, files_head=46, typecheck=[(1, 1)], eslint=[(0, 0)],   # the seat's F7: ONE pre-existing TS1378 (top-level await :243) at develop AND head under the targeted tsconfig — delta 0
           lane_head_preload=917, lane_wall=('4.3 s', '4.0 s'),
           lock=('00:55:30Z', '01:01:22Z'), push=('00:55:30Z', '01:01:18Z'), ready='01:05:17Z', shell='45 passed, 0 failed (of 45)', a4=None,
           census=(3, 369, 362, {'203.0.113.7:443 (ks914-shipped-path.test.ts)': 4, 'fast.example:443 (ks932-timeout-bounds-dns.test.ts)': 1, 'first-name.invalid:60922 (ks914-pinned-address.test.ts)': 1, 'pinned-target.invalid:60918 (ks914-pinned-address.test.ts)': 1, 'pinned-target.invalid:60920 (ks914-pinned-address.test.ts)': 1, 'slow.example:443 (ks932-timeout-bounds-dns.test.ts)': 1, 'totally-different-name.invalid:60922 (ks914-pinned-address.test.ts)': 1}),
           title='KS-1181 F3w: the error-handler guard header names the surplus handler, not a tenth',
           comments=0, prior_prs=['1159'], excised='ks-727', tip='75ad0e55c', boot_state='In Progress', bot_walk=False),
}
BATCH = dict(originate=(835, 835), anchoring=(334, 335), auth=(828, 828), shared=(917, 917))   # the seat's batch-tree suites (s-b18-batch over PARENT); anchoring's ONE known red = threadTokenMint.test.ts; auth +10 = 6 + 4; shared +0
BASELINES = dict(originate=(835, 835, 71), anchoring=(328, 329, 22), auth=(818, 818, 74), shared=(917, 917, 46))   # the seat's lane baselines of record at PARENT (BARE — Wednesday's (b) ruling 23:30:26Z; auth / shared measured twice)
# the seat's item-0 tamper-file blobs (4 files; identical at 3916eacd1 AND 8c2f7b3fd — the drafter's rev-parse, local_reads_1.out)
TAMPER_BLOBS = [(AN + 'src/anchorSubmission.ts', 'd3ad106d8e5764a526456b3218e1e8d9ad1a38ba'), (AU + 'src/auth.openapi.ts', '2c356c3c7877add99f5e1a3c437d04ac8be3dc76'),
                (AU + 'src/routes/auth.ts', '18946cd7c5c394d89ecbecf860ab66a96b1e22c7'), (AU + 'src/routes/mfa.ts', '87d3ee1079fe90010f45955dbaf4307ae595b205')]
# the seat's plant shas (checker plant.out == the seat's ×6): 8J c5ac3e51d569 ×2 · SPECRENAME ccf50b0e8760 · ROUTECOLLAPSE 534342d878f6 · F1C 128f88bb0b1b · F1D b0c3617e3a2c
PLANT_SHAS = {'8J': 'c5ac3e51d569', 'SPECRENAME': 'ccf50b0e8760', 'ROUTECOLLAPSE': '534342d878f6', 'F1C': '128f88bb0b1b', 'F1D': 'b0c3617e3a2c'}
# Seat C 18th's six PRs (its READYs captured beside 01:15:52Z; heads = the drafter's ls-remote 01:14:19Z): (n, key, head, [paths]) — ten distinct paths, every one under services/api-gateway/
SEATC = [('1167', 'KS-947', '4f2b87547d8060646763a5f15ef4a165a1e436bd', [AG + 'src/__tests__/ks733-users-mfa-rate-limit-mount.test.ts']),
         ('1168', 'KS-1123', 'e17efafa7eac15108cd51bf27eca04902c149603', [AG + 'src/__tests__/ks1123-api-gateway-verify-an-empty-string.test.ts']),
         ('1169', 'KS-1192', '9088a3509730c1663ecae3b380e18d17561f9f77', [AG + 'src/__tests__/ks1192-real-app-production-erasure-door.test.ts']),
         ('1171', 'KS-1231', 'f17ec0af49d9b3d97e5671176adc70dc3212b7f4', [AG + 'src/__tests__/ks1231-a-connector-allow-list-fails-open.test.ts', AG + 'src/routes/verification.ts', AG + 'src/__tests__/ks1231-info-reader-malformed-container-refused.test.ts', AG + 'src/services/health.ts']),
         ('1173', 'KS-1246', '611c9d504463eacd12c37e0be8af11ba67e65c82', [AG + 'src/__tests__/ks1246-f-2-health-services-still-reads.test.ts', AG + 'src/services/health.ts']),
         ('1175', 'KS-1257', 'be3fb14b6eef1b32cf510a3603287a1ce0e925f7', [AG + 'src/__tests__/ks1230-settings-write-validates-allowed-document-types.test.ts', AG + 'src/routes/admin.ts'])]
SEATC_KEYS = ['KS-947', 'KS-1123', 'KS-1192', 'KS-1231', 'KS-1246', 'KS-1257']
SEATC_DIRS = [AG]
SEATC_GO = 'GO: merge #1167, #1168, #1169, #1171, #1173, #1175 batch'; SEATC_ALL6 = '52853c8bf6c4ff43585cdade61c637ff8cbaa5d0'
SEATC_TAMPERS = [AG + 'src/index.ts', AG + 'src/routes/verification.ts']
ARCHIVED = ['KS-501', 'KS-480', 'KS-978', 'KS-721', 'KS-522', 'KS-726', 'KS-535', 'KS-867', 'KS-878', 'KS-914', 'KS-1238', 'KS-1282', 'KS-1062', 'KS-971', 'KS-1078', 'KS-921', 'KS-490',
            'KS-597', 'KS-727', 'KS-764', 'KS-879', 'KS-1020', 'KS-835', 'KS-1270', 'KS-549', 'KS-733', 'KS-815', 'KS-1013', 'KS-1058', 'KS-1103']   # 30 (the READYs' ARCHIVED-TICKET READS block: the standing 24 + six)
CONTENT_LIVE = ['KS-999', 'KS-1230', 'KS-871', 'KS-763', 'KS-775', 'KS-1285', 'KS-1260', 'KS-1209', 'KS-887', 'KS-869', 'KS-1175', 'KS-1250', 'KS-1280', 'KS-730', 'KS-692', 'KS-1195', 'KS-910', 'KS-1273', 'KS-958']   # 19 (the READYs' Live-but-foreign / content block)
DEFERRED = 'KS-1227'   # the brief's DEFERRED row (Backlog, 0 attachments)
OWN = [PRS[p]['key'] for p in PUSH]
TIER1 = ['3', '5', '6']   # KS-1265 (product bytes on originate documents.ts) + KS-811 / KS-1188 (auth-surface test-only pins) — the commission item 1
CODE_PATCH = ['3']; TEST_ONLY = ['4', '5', '6']; COMMENT = ['1', '2', '7']
def run_dir(rd): return LM + '/runs/' + rd
def canon_path(row): return LM + '/runs/' + row[1] + '/out.md.checker/' + row[2]
def ready_regex(): return r'READY FOR QA \(Seat B 18th\): PR (\d+) (KS-\d+)[^\n]*? — #(\d+) at head ([0-9a-f]{40})'
def all_paths(): return [f['path'] for p in PUSH for f in PRS[p]['files']]
def distinct_paths(): return sorted(set(all_paths()))
def product_paths(): return sorted(f['path'] for p in PUSH for f in PRS[p]['files'] if f['kind'] == 'product')
GO_STRING = 'GO: merge #1170, #1172, #1174, #1176, #1177, #1178, #1179 batch'
HOLD_MSGID = '<010001a0c6a8589e-ac002160-ff81-44fb-b837-7a9f37b65a6a-000000@email.amazonses.com>'
