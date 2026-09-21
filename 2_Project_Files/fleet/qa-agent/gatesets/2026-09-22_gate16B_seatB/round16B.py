"""round16B.py — the ONE source of this round's pins for every gate16B drafter script (a wrong pin in the prompt is the most expensive slip;
gate15 repeated its table in six files — here every script imports this module and asserts against origin / local objects / the READYs).
Values: the seat's READY mails (mail_seatB16_ready*.md, captured 18:37Z), its 16:54Z + 18:33Z STATUS mails, Wednesday's brief
(briefs_staged/2026-09-22_raise_seatB_successor16.md GROUPING + QUEUE), the drafter's ls-remote 18:35:53Z (lsremote_1.out). Every value is a CLAIM
until a script re-derives it; the scripts print the disagreement, never adopt."""
DEV = '64ab105132eada0621622acf4d6053bc59926780'; DEV_TREE = '87b4aa12d2ebae335f11790ceed9158f7d5614ec'
PARENT15 = '581ed7fa124b85c7c2da89ac05d52f99c2502911'   # the 15th's parent; rev-list --count 581ed7fa1..64ab10513 = 13 (the seat's item 0)
SEAT_ALL8 = 'c54c1ae73ba32d9bdd7ed3258a9c19e59ad5cb1d'   # the eight-PR tree over DEV (the seat's raise/batch8.py; three orders)
SEAT_ALL9 = '649ccf34c6d12ac04dbd4267b8726ba17569713b'   # item 0's all-14 over nine PRs (incl. the HELD KS-1171) — the octopus 2ede08b37's tree
D = 'Blockchain/Dev/'; OR = D + 'services/originate/'; SH = D + 'packages/shared/'; SE = D + 'services/security/'; AN = D + 'services/anchoring/'
LM = '/Volumes/DevMASTER/WEDNESDAY/2_Project_Files/local-model'
REPO = '/Volumes/DevMASTER/!CODING/Secuura/Blockchain/2_Project_Files'
PUSH = ['1', '2', '3', '4', '5', '6', '7', '9']   # seat PR numbers in push order; seat PR 8 (KS-1171) HELD un-pushed (Wednesday 16:50:37Z)
# seat PR -> dict
PRS = {
 '1': dict(n='1147', key='KS-928', tags='DEMOSEEDGATE', head='e456ffb5e9e1e1525f155864452c0aa2cad8752b', tree='075e5670c8b11ee3a497047cc0788ad216243fc4',
           branch='refs/heads/feature/ks-928-the-demo-seed-gates-predicate-is-tested-but-its-call-site-is-r15-demoseedgate-1',
           file=OR + 'src/__tests__/ks928-the-demo-seed-gate-s-predicate.test.ts', mode='new', dev_blob=None, dev_lines=0, blob='a215e136e805694fb21807cb1684a6f0f07135fb', lines=107, adds=107, dels=0,
           lane='originate', runner='jest', cells=4, lane_dev=809, lane_head=813, files_dev=67, files_head=68,
           canon=[('DEMOSEEDGATE', '2026-09-22_ks928-ornith35b-night', '98a5fa3032f0e5a3', 'trunc', 107, 0, '@@ -0,0 +1,97 @@', 'e76b3e90db28', 97, '581ed7fa1')],
           tampers=[('DEMOSEEDGATE', OR + 'src/routes/adminConfig.ts', 1897, 2, [])], lock=('16:50:05Z', '16:56:18Z'), push=('16:50:08Z', '16:56:14Z'), ready='17:01:06Z',
           census=(5, 299, 245, {'anchoring:4005 (unattributed)': 51}), title='KS-928 DEMOSEEDGATE: pin the demo-seed gate\'s CALL SITE on POST /api/admin/seed-demo-users'),
 '2': dict(n='1149', key='KS-1118', tags='F2', head='75f5b924ea28b3a9a68e8d02af8f95f16c28c99d', tree='a7f9258d941f9fe1d8604a62baf9c9752d8e9887',
           branch='refs/heads/feature/ks-1118-post-apiverificationverify-the-documenthash-over-hash-r15-f2-1',
           file=OR + 'src/__tests__/ks1118-verify-documenthash-over-hash.test.ts', mode='new', dev_blob=None, dev_lines=0, blob='01ab706fe9a6b15eb1c5b2f63757b444d15a3969', lines=150, adds=150, dels=0,
           lane='originate', runner='jest', cells=3, lane_dev=809, lane_head=812, files_dev=67, files_head=68,
           canon=[('F2', '2026-09-21_ks1118-ornith35b-night', '3920a191b5d5f3b8', 'strict', 150, 0, '@@ -0,0 +1,150 @@', None, None, '9f0265eb0')],
           tampers=[('F2', OR + 'src/routes/verification.ts', 742, 2, [])], lock=('17:04:27Z', '17:10:11Z'), push=('17:04:28Z', '17:10:07Z'), ready='17:12:44Z',
           census=(5, 299, 245, {'anchoring:4005 (unattributed)': 51}), title='KS-1118 F2: pin documentHash-over-hash precedence on POST /api/verification/verify'),
 '3': dict(n='1151', key='KS-1133', tags='B', head='10c689dcfb1722c993046a115be82b951db0596f', tree='7256a271adf34ac8db0a0c47d789612faf77a93c',
           branch='refs/heads/feature/ks-1133-verify-hash-precedence-v1-hash-last-v2-hash-first-document-r15-b-1',
           file=OR + 'src/__tests__/ks1133-v2-verify-hash-read-first.test.ts', mode='new', dev_blob=None, dev_lines=0, blob='f343c69cd71087c2782dd389021bf77854382c6c', lines=109, adds=109, dels=0,
           lane='originate', runner='jest', cells=4, lane_dev=809, lane_head=813, files_dev=67, files_head=68,
           canon=[('B', '2026-09-21_ks1133-ornith35b-night', '7d469d279b885243', 'trunc', 109, 0, '@@ -0,0 +1,97 @@', 'e9dc6e3899f0', 97, '9f0265eb0')],
           tampers=[('B', OR + 'src/routes/verificationV2.ts', 446, 2, [])], lock=('17:16:52Z', '17:22:33Z'), push=('17:16:52Z', '17:22:27Z'), ready='17:31:00Z',
           census=(5, 299, 245, {'anchoring:4005 (unattributed)': 51}), title='KS-1133 B: pin that the v2 verify-hash route reads hash FIRST, before every alias'),
 '4': dict(n='1153', key='KS-1158', tags='R3', head='be21a0ae404c04a966379773a18ce5b5674f8e4b', tree='8138fe9bb3a8b5dd845737fbd40ee80c7fcd844c',
           branch='refs/heads/feature/ks-1158-l3a-gate-records-912-r2-937-the-placeholder-hash-anchoredat-r15-r3-1',
           file=OR + 'src/__tests__/ks1158-r3-network-carry-second-pin.test.ts', mode='new', dev_blob=None, dev_lines=0, blob='0d1db7f6cad9846cccd12e52c66a55a9fe03eb72', lines=96, adds=96, dels=0,
           lane='originate', runner='jest', cells=5, lane_dev=809, lane_head=814, files_dev=67, files_head=68,
           canon=[('R3', '2026-09-21_ks1158-ornith35b-night', '1d4557e8f2b7578e', 'rc128', 96, 0, '@@ -0,0 +1,97 @@', None, None, '9f0265eb0')],
           tampers=[('R3', OR + 'src/services/anchorStateSync.ts', 166, 2, ['ks1004-anchor-failed-lockout.test.ts :: KS-1004 — markDocumentAnchorFailed reaches a hashed document the txHash is CARRIED FORWARD, not nulled — the failed tx keeps its forensic trail'])],
           lock=('17:29:42Z', '17:35:49Z'), push=('17:29:42Z', '17:35:36Z'), ready='17:40:41Z',
           census=(5, 291, 237, {'anchoring:4005 (unattributed)': 51}), title='KS-1158 R3: pin that a failed anchor\'s network carry keys on the hash, not on truthiness'),
 '5': dict(n='1155', key='KS-1229', tags='AFTERVERIFY SIGNCERT SIGNWALLET UNTYPEDSRCb VERSIONTRIM', head='b455e4594865cfd63aea486139d6afae182eb3c6', tree='4c105c64e6dd4f1ab258beb080ece4d5519aa70b',
           branch='refs/heads/feature/ks-1229-ks1213-cells-ten-tampers-stay-green-a-refused-issue-can-mint-r15-afterverify-signcert-signwallet-untypedsrcb-versiontrim-1',
           file=OR + 'src/__tests__/ks1213-a-derived-writer-relabel-is-refused.test.ts', mode='modify', dev_blob='8082826898c2', dev_lines=226, blob='bbfcd0f98923ca986a5779d937a75398badc03d1', lines=309, adds=84, dels=1,
           lane='originate', runner='jest', cells=95, cells_dev=85, lane_dev=809, lane_head=819, files_dev=67, files_head=67,
           canon=[('AFTERVERIFY', '2026-09-22_ks1229-ornith35b-night', 'cd40d58da5117a33', 'strict', 19, 0, '@@ -118,3 +118,22 @@', None, None, '581ed7fa1'),
                  ('SIGNCERT', '2026-09-22_ks1229-ornith35b-night2', '7ec8970968618911', 'strict', 28, 0, '@@ -115,3 +115,31 @@', None, None, '581ed7fa1'),
                  ('SIGNWALLET', '2026-09-22_ks1229-ornith35b-night3', '74044d4cda9afd95', 'strict', 12, 0, '@@ -141,3 +141,15 @@', None, None, '581ed7fa1'),
                  ('UNTYPEDSRCb', '2026-09-21_ks1229-ornith35b-night2', '264bf565852a205a', 'strict', 13, 1, '@@ -224,3 +224,15 @@', None, None, '581ed7fa1'),
                  ('VERSIONTRIM', '2026-09-22_ks1229-ornith35b-night4', '6a643d4cea7901ba', 'strict', 12, 0, '@@ -123,3 +123,15 @@', None, None, '581ed7fa1')],
           stage_blobs=['c771e61f4cbe042f7ead750951bb2f35a517e928', '51d28696e81ecb37cfc7bff797ba23e02c177728', 'a7ac2c174cad781ae2e6f10792345ff2611a19c8', 'd57c47dac7302f8f5184ccad5ddf10f4d35d807e', 'bbfcd0f98923ca986a5779d937a75398badc03d1'],
           stage_cells=[87, 89, 91, 93, 95],
           tampers=[('AFTERVERIFY', OR + 'src/routes/documents.ts', 2878, 1, []), ('SIGNCERT', OR + 'src/routes/documents.ts', 2609, 1, []), ('SIGNWALLET', OR + 'src/routes/documents.ts', 2878, 1, []),
                    ('UNTYPEDSRC', OR + 'src/routes/documents.ts', 2609, 1, []), ('VERSIONTRIM', OR + 'src/routes/documents.ts', 1993, 1, [])],
           lock=('17:42:24Z', '17:49:05Z'), push=('17:42:24Z', '17:48:56Z'), ready='17:52:32Z',
           census=(31, 1307, 929, {'anchoring:4005 (unattributed)': 367}), title='KS-1229: five cells pin refusals on the relabel, sign-cert and sign-wallet document routes'),
 '6': dict(n='1157', key='KS-1179', tags='F1', head='8b0713d8ff33c1e4e7690ec6b6b8bb1cda0d138f', tree='080b50fb0332003c8b462a2cd884b288aee0ae6b',
           branch='refs/heads/feature/ks-1179-safeoutboundrequest-tests-no-cell-pins-dns-layer-r15-f1-1',
           file=SH + 'src/__tests__/ks1179-safeoutboundrequest-tests-no-cell-pins-dns.test.ts', mode='new', dev_blob=None, dev_lines=0, blob='1dd3a0024fa43701664ef80247f71e2a555ab6a4', lines=98, adds=98, dels=0,
           lane='shared', runner='vitest', cells=7, lane_dev=907, lane_head=914, files_dev=44, files_head=45,
           canon=[('F1', '2026-09-21_ks1179-ornith35b-night', '99f11c834aa60bd9', 'strict', 98, 0, '@@ -0,0 +1,98 @@', None, None, '9f0265eb0')],
           tampers=[('F1', SH + 'src/security/ssrf-guard.ts', 478, 4, [])], lock=('17:56:26Z', '18:02:16Z'), push=('17:56:26Z', '18:02:12Z'), ready='18:06:26Z',
           census=(5, 441, 420, {'203.0.113.7:443 (ks914-shipped-path.test.ts)': 12, 'fast.example:443 (ks932-timeout-bounds-dns.test.ts)': 3, 'slow.example:443 (ks932-timeout-bounds-dns.test.ts)': 3}),
           title='KS-1179 F1: pin DNS-layer SSRF classification in safeOutboundRequest'),
 '7': dict(n='1159', key='KS-1181', tags='F3', head='c6af5ca678c4a1ae3aba6bc4cd7a98f796247929', tree='4e6cf2cbda1ee0a32369ced3588576ca108490d9',
           branch='refs/heads/feature/ks-1181-error-handler-guard-corpus-1-canary-cells-cannot-r15-f3-1',
           file=SH + 'src/__tests__/ks1181-ks-727-error-handler-guard-corpus.test.ts', mode='new', dev_blob=None, dev_lines=0, blob='cab04d1ae61d31c18bbdf856567b92935b84cfca', lines=75, adds=75, dels=0,
           lane='shared', runner='vitest', cells=3, lane_dev=907, lane_head=910, files_dev=44, files_head=45,
           canon=[('F3', '2026-09-21_ks1181-ornith35b-night', '6d42ce5422418cf0', 'trunc', 75, 0, '@@ -0,0 +1,74 @@', '6250385ee49e', 74, '9f0265eb0')],
           tampers=[('F3', SH + 'src/__tests__/ks727-errorhandler-class-guard.test.ts', 32, 1, [])], lock=('18:09:59Z', '18:15:42Z'), push=('18:10:00Z', '18:15:36Z'), ready='18:18:28Z',
           census=(5, 441, 420, {'203.0.113.7:443 (ks914-shipped-path.test.ts)': 12, 'fast.example:443 (ks932-timeout-bounds-dns.test.ts)': 3, 'slow.example:443 (ks932-timeout-bounds-dns.test.ts)': 3}),
           title='KS-1181 F3: pin that the error-handler guard\'s header counts equal its exact sets'),
 '9': dict(n='1161', key='KS-975', tags='ITEM1', head='7f426f1706bd40a5dd800502d5af9a1968611718', tree='c5dd18b13d84d042ea46b9315a68bb967bc40d09',
           branch='refs/heads/feature/ks-975-ratelimitscope-tri-state-a-malformed-sub-silently-became-a-r15-item1-1',
           file=SE + 'src/__tests__/ks975-malformed-sub-is-refused.test.ts', mode='new', dev_blob=None, dev_lines=0, blob='60015bd01b6ab9da09e223214322b38997dd94a3', lines=36, adds=36, dels=0,
           lane='security', runner='vitest', cells=4, lane_dev=216, lane_head=220, files_dev=17, files_head=18,
           canon=[('ITEM1', '2026-09-21_ks975-ornith35b-night', 'cb1568354a105511', 'trunc', 36, 0, '@@ -0,0 +1,34 @@', '1fcffe443b5c', 34, '9f0265eb0')],
           tampers=[('ITEM1', SE + 'src/rateLimitScope.ts', 118, 2, [])], lock=('18:23:01Z', '18:28:49Z'), push=('18:23:01Z', '18:28:45Z'), ready='18:31:47Z',
           census=(5, 30, 30, {}), title='KS-975 ITEM1: pin that a MALFORMED sub with no userId is refused, not tenant-scoped'),
}
HELD = dict(key='KS-1171', commit='685d5f2645c5c936320e8b49c476e8ef19e3e5dd', tree='d3d265b746ba', worktree='s-b16-ks1171',
            branch='feature/ks-1171-guard-3s-re-poll-reads-a-mixed-window-as-absent-one-early-r15-8jguard3s-8j-1',
            files=[AN + 'src/__tests__/ks1171-8j-confirmed-wins-over-polled-zero.test.ts', AN + 'src/__tests__/ks1171-guard-3-s-re-poll-reads.test.ts'],
            canon=[('8J-GUARD3S', '2026-09-21_ks1171-ornith35b-night2', '326284d893a7f1fb', 'strict', 108, 0), ('8J', '2026-09-21_ks1171-ornith35b-night', '812e44a32504d9ef', 'rc128', 128, 0)])
# the seat's item-0 tamper-file blobs at the tip (the plan confirmation): (path, blob12)
TAMPER_BLOBS = [(OR + 'src/routes/adminConfig.ts', '62af28d01706'), (OR + 'src/routes/verification.ts', '7e122e960a98'), (OR + 'src/routes/verificationV2.ts', 'dfa26c0572d6'),
                (OR + 'src/services/anchorStateSync.ts', 'd8e988f7a479'), (OR + 'src/routes/documents.ts', '3f837fc6e656'), (SH + 'src/security/ssrf-guard.ts', 'efd880010d5f'),
                (SH + 'src/__tests__/ks727-errorhandler-class-guard.test.ts', '5127297156ed'), (AN + 'src/anchorSubmission.ts', 'd3ad106d8e57'), (SE + 'src/rateLimitScope.ts', 'cb51abd021bc')]
# Seat C 16th's pushed PRs at the drafter's read (its READYs captured 18:37Z + lsremote_1.out 18:35:53Z); PR 2 (KS-1123 F3b) HELD; more may land
SEATC = [('1148', 'KS-864', 'c4a96cfe012196aa56765b6b26bd63b123980087', D + 'services/api-gateway/src/__tests__/ks864c-portal-env-vars.test.ts'),
         ('1150', 'KS-1180', '250a9b9eda021cb2b3d224d68b9e3ca5e9264d2c', D + 'services/api-gateway/src/__tests__/ks1073-tier-2-verify-has-no-statusless.test.ts'),
         ('1152', 'KS-1185', '28d1e4df6da993e0363537a5144185d0892e4ca3', D + 'services/api-gateway/src/__tests__/ks1185-workflow-approve-forward-default-bound.test.ts'),
         ('1154', 'KS-1199', '889b0539117b2f31e777f47adde1d8f06a5c5de7', D + 'services/api-gateway/src/__tests__/ks1199-status-differing-anchor-tie-verdict.test.ts'),
         ('1156', 'KS-1237', '58d293a87706f58321c8266e4bfeebc2686471d9', D + 'services/api-gateway/src/__tests__/ks1204-a-non-array-allow-list-fails-closed-and-documenttype-wins.test.ts'),
         ('1158', 'KS-855', 'ddac6d7d5fe3362d3e0ff9633628d8367fcc6310', D + 'services/auth/src/__tests__/ks855-the-oauth-available-scopes-list-is.test.ts'),
         ('1160', 'KS-944', 'ef4713cc66c07b1b013cbd7d7ca0ea2fe5a4f5b2', D + 'services/auth/src/__tests__/ks944-the-gateway-s-auth-gate-reads.test.ts'),
         # landed AFTER the drafter's 18:35:53Z ls-remote (read 18:48:44Z, gh_seatc_late_1.out; no READY captured for them at that read):
         ('1162', 'KS-1156', 'b6b70d7870222cd746c8a9b98a423ef95a657568', D + 'services/auth/src/__tests__/ks1156-auth4-gate-records-983-r2-984.test.ts'),
         ('1163', 'KS-1188', '02f12926f248bcc879e1f437d51a306a829b3c8b', D + 'services/auth/src/__tests__/ks1188-getuserbyid-failed-log-meta-keys.test.ts'),
         ('1163', 'KS-1188', '02f12926f248bcc879e1f437d51a306a829b3c8b', D + 'services/auth/src/__tests__/ks1188-mfa-status-503-route.test.ts'),
         ('1163', 'KS-1188', '02f12926f248bcc879e1f437d51a306a829b3c8b', D + 'services/auth/src/__tests__/ks1188-users-me-503-route.test.ts')]
SEATC_KEYS = ['KS-864', 'KS-1123', 'KS-1180', 'KS-1185', 'KS-1199', 'KS-1237', 'KS-855', 'KS-944', 'KS-1156', 'KS-1188', 'KS-1193', 'KS-1217', 'KS-910']
SEATC_DIRS = [D + 'scripts/__tests__/', D + 'services/api-gateway/', D + 'services/auth/']
ARCHIVED = ['KS-501', 'KS-480', 'KS-978', 'KS-721', 'KS-522', 'KS-726', 'KS-535', 'KS-867', 'KS-878', 'KS-914', 'KS-1238', 'KS-1282', 'KS-1062', 'KS-971', 'KS-1078', 'KS-921', 'KS-490',
            'KS-597', 'KS-727', 'KS-764', 'KS-879', 'KS-1020', 'KS-835', 'KS-1270']   # 24 (the READYs' ARCHIVED-TICKET READS block)
CONTENT_LIVE = ['KS-1213', 'KS-1073', 'KS-1050', 'KS-1204', 'KS-1072', 'KS-1183', 'KS-999', 'KS-1018', 'KS-1285', 'KS-1260', 'KS-1209', 'KS-887', 'KS-869', 'KS-1031', 'KS-1175', 'KS-1250', 'KS-1035', 'KS-1036', 'KS-1156', 'KS-1180']   # 20 (the READYs' Live-but-foreign / content block)
OWN = [PRS[p]['key'] for p in PUSH]
def run_patch(d): return LM + '/runs/' + d + '/out.md.checker/patch.diff'
def ready_regex(): return r'READY FOR QA \(Seat B 16th\): PR (\d+) (KS-\d+)[^\n]*? — #(\d+) at head ([0-9a-f]{40})'
