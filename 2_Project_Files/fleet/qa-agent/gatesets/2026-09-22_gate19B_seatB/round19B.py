"""round19B.py — the ONE source of the Seat B 19th/20th round's pins for every gate19B drafter script (the gate19C round19C.py shape, re-keyed).
Values: the seat's NINE READY mails (mail_seatB19_ready01..03_*.md by Seat B 19th, mail_seatB20_ready04..09_*.md by Seat B 20th; captured 07:58:3xZ
by message id), the 05:24Z (NINE RAISED) / 07:09Z ((2') applied) / 07:55Z (HOLDING 9/9) STATUS mails, the 04:27Z / 07:04Z plan confirmations, the
05:07Z KS-1164 QUESTION, the 06:18Z hand-over wrap, Wednesday's briefs 04:03:07Z (19th) + 06:48:33Z (20th), her ANSWERs 04:10Z (S1) / 04:28Z (plan
19th) / 05:10:31Z (KS-1164 ruled (b)) / 07:05Z (plan 20th), the 06:07Z band/hand-over ADDENDUM, the F-GUARD (2') ADDENDUM 06:22:04Z (to Seat C, the
Seat B 20th brief carries it), the drafter's ls-remote 07:59:11Z (lsremote_1.out). Every value is a CLAIM until a script re-derives it; the scripts
print the disagreement, never adopt. Blobs are the READYs' 12-hex forms unless a script read the 40-hex form from origin objects."""
DEV = '3bad652d17cf111c1e2e1bed1ae7686894637487'; DEV_TREE12 = 'cd9b0f6c7b84'   # the 18th round's END tree; the SAME base as gate19C (Seat C 19th's twelve merge on a SEPARATE GO)
DEV_PRE = '581ed7fa1'            # the checkout's HEAD before Seat B 19th's boot pull (S1, ruled LEAVE 04:10Z)
SEAT_ALL11 = '3df72c02d3250ca584c591fd89734d3391d99337'   # the seat's AMENDED all-11 (nine PRs) tree over DEV (batch11amend_19.py; s-b19-batch octopus d64e15b98 10 parents; three orders one sha)
SEAT_ALL11_UNAMENDED12 = '34728affba20'                    # item 0's pre-amendment all-11 (the KS-1164 canonical test blob) — the CONTROL, differs by construction (READY S4: the stale parenthetical)
SEAT_ALL11_SHORTSTAT = '17 files changed, 642 insertions(+), 13 deletions(-)'
SEAT_PAIR_TREE12 = '64de96836e46'   # #1198 + #1199 over DEV, both orders (the READYs)
D = 'Blockchain/Dev/'; OR = D + 'services/originate/'; KY = D + 'services/kyc/'; SH = D + 'packages/shared/'; SE = D + 'services/security/'; SP = 'systemTest/performance/'
PAIR_PATH = SE + 'src/index.ts'; PAIR_BLOB = '2ad45cd8e5552d5d52e48749406203d149967073'; PAIR_LINES = 1603; PAIR_MODE = '100644'
PAIR_ALONE = {'1198': '7bdaa9cad257', '1199': '5bf6fb62dba8'}
LM = '/Volumes/DevMASTER/WEDNESDAY/2_Project_Files/local-model'
REPO = '/Volumes/DevMASTER/!CODING/Secuura/Blockchain/2_Project_Files'
ORIGIN_URL = 'git@github.com:Secuura/Distributed_Secuura.git'
PUSH = [str(i) for i in range(1, 10)]
# the commission's tier rule (item 1): tier 1 on every PR carrying PRODUCT/TOOLING bytes or an auth-adjacent surface (security/src/index.ts; the ssrf-guard tamper — the 2026-09-05 tiering rule); tier 2 on KS-1229 (test-only cells on EXISTING behaviour, the plan ANSWER)
AUTH_ADJACENT = [SE + 'src/index.ts', SE + 'src/requestSchemas.ts']
# a canonical row: (label, run dir (under LM/runs), file under out.md.checker/, sha256[:16], apply opts ('' = strict), target path)
# a file row: dict(path, kind test|product|tooling, mode new|modify, blob12 (AT THE HEAD), lines, adds, dels[, canon_blob12, canon_lines for the KS-1164 amendment])
PRS = {
 '1': dict(n='1182', key='KS-730', keys=['KS-730'], tags='INGEST500', kind='code_patch', seat='B19', head='8c413d78243a47d144f4049e6cd720a473d4dceb', tree='a37f638adae6b7ec2bc95ec19f2a1d5d17a4c27d',
           branch='refs/heads/feature/ks-730-security-71-inline-handlers-still-return-errmessage-verbatim-r16b-ingest500-1', tier_ready=1, targets=2, adds=119, dels=2, lane='originate',
           files=[dict(path=OR + 'src/__tests__/ks730a-ingest-500-never-answers-err-message.test.ts', kind='test', mode='new', blob12='7bed8c23b331', lines=113, adds=113, dels=0),
                  dict(path=OR + 'src/routes/systemErrors.ts', kind='product', mode='modify', blob12='baba06edeb88', lines=190, adds=6, dels=2)],
           canon=[('730-INGEST500-s2', '2026-09-22_ks730-ornith35b-night', 'section_2.diff', 'ecdcf272778d341c', '', OR + 'src/__tests__/ks730a-ingest-500-never-answers-err-message.test.ts'),
                  ('730-INGEST500-s1', '2026-09-22_ks730-ornith35b-night', 'section_1.diff', '39f91fe1ad38b434', '--recount --ignore-whitespace', OR + 'src/routes/systemErrors.ts')],
           patch_sha16={'2026-09-22_ks730-ornith35b-night': 'c79fc2f253022891'}, a4=[(4, 6)], a5=['6/6'], lane_dev=835, lane_head=841, lock=('05:28:28Z', '05:34:14Z'), ready='05:48:55Z',
           inhook='12/15 legs ran, 3 SKIPPED (3 4 8); shell suites 45/45', title='KS-730 INGEST500: the /ingest 500 answers a constant message, never err.message', claude_written=[]),
 '2': dict(n='1184', key='KS-1028', keys=['KS-1028'], tags='STEP12FANOUT', kind='code_patch', seat='B19', head='dd9ef92274366dd9975203d1376a87f63e7606a4', tree='bce069ddb1ea26b2975359341beba797fec10069',
           branch='refs/heads/feature/ks-1028-gate-f-1-major-a-step-12-throw-skips-the-user_erased-r16b-step12fanout-1', tier_ready=1, targets=2, adds=104, dels=3, lane='originate',
           files=[dict(path=OR + 'src/__tests__/ks1028-step12-throw-does-not-skip-fanout.test.ts', kind='test', mode='new', blob12='81ccc4535838', lines=99, adds=99, dels=0),
                  dict(path=OR + 'src/services/gdprService.ts', kind='product', mode='modify', blob12='7d615f33bb9b', lines=1542, adds=5, dels=3)],
           canon=[('1028-STEP12FANOUT-s2', '2026-09-22_ks1028-ornith35b-night', 'section_2.diff', 'b672697ba64ea08d', '--directory=Blockchain/Dev', OR + 'src/__tests__/ks1028-step12-throw-does-not-skip-fanout.test.ts'),
                  ('1028-STEP12FANOUT-s1', '2026-09-22_ks1028-ornith35b-night', 'section_1.diff', '776f3deeed4f4f7a', '--directory=Blockchain/Dev', OR + 'src/services/gdprService.ts')],
           patch_sha16={'2026-09-22_ks1028-ornith35b-night': 'd15b40882df93570'}, a4=[(2, 4)], a5=['4/4'], lane_dev=835, lane_head=839, lock=('05:41:24Z', '05:47:27Z'), ready='05:50:51Z',
           inhook='12/15 legs ran, 3 SKIPPED (3 4 8); shell suites 45/45', title='KS-1028 STEP12FANOUT: a step-12 throw no longer skips the USER_ERASED fan-out', claude_written=[], excised='ks-754'),
 '3': dict(n='1186', key='KS-1160', keys=['KS-1160'], tags='POSTNORMURL', kind='code_patch', seat='B19', head='8d3c5c9604fc07598bbb67ca2fcdfcead4859df1', tree='42818cb49fe4097bcef914b7e12ad6a26506cd37',
           branch='refs/heads/feature/ks-1160-originate-post-apiwebhooks-persists-the-raw-url-where-patch-r16b-postnormurl-1', tier_ready=1, targets=2, adds=99, dels=2, lane='originate',
           files=[dict(path=OR + 'src/__tests__/ks1160-webhooks-post-persists-normalised-url.test.ts', kind='test', mode='new', blob12='90859d04ad1d', lines=97, adds=97, dels=0),
                  dict(path=OR + 'src/routes/webhooks.ts', kind='product', mode='modify', blob12='eb4efed61381', lines=549, adds=2, dels=2)],
           canon=[('1160-POSTNORMURL-s2', '2026-09-22_ks1160-ornith35b-night', 'section_2.diff', '3c3f262105485a07', '', OR + 'src/__tests__/ks1160-webhooks-post-persists-normalised-url.test.ts'),
                  ('1160-POSTNORMURL-s1', '2026-09-22_ks1160-ornith35b-night', 'section_1.diff', '5ffcdc6799894415', '', OR + 'src/routes/webhooks.ts')],
           patch_sha16={'2026-09-22_ks1160-ornith35b-night': '2c63239f141bc4fb'}, a4=[(2, 3)], a5=['3/3'], lane_dev=835, lane_head=838, lock=('05:54:44Z', '06:00:38Z'), ready='06:03:34Z',
           inhook='12/15 legs ran, 3 SKIPPED (3 4 8); shell suites 45/45', title='KS-1160 POSTNORMURL: POST /api/webhooks persists the normalised url like PATCH', claude_written=[]),
 '4': dict(n='1194', key='KS-1229', keys=['KS-1229'], tags='LOOSE SIDEEFFECTS', kind='test_only', seat='B20', head='97d2e3fe493bb65afa14b768cafa21912e58c02b', tree='e01d8f2d9c9aac2a16ce8fcbba45950eeaef7f0f',
           branch='refs/heads/feature/ks-1229-ks1213-cells-ten-tampers-stay-green-a-refused-issue-can-mint-r16b-loose-sideeffects-1', tier_ready=2, targets=1, adds=45, dels=0, lane='originate',
           files=[dict(path=OR + 'src/__tests__/ks1213-a-derived-writer-relabel-is-refused.test.ts', kind='test', mode='modify', blob12='c881e7c5a17a', lines=354, adds=45, dels=0)],
           canon=[('1229-LOOSE', '2026-09-22_ks1229-ornith35b-night5', 'patch.diff', '288f56140ea44bcd', '', OR + 'src/__tests__/ks1213-a-derived-writer-relabel-is-refused.test.ts'),
                  ('1229-SIDEEFFECTS', '2026-09-22_ks1229-ornith35b-night6', 'patch.diff', '144436f251750687', '', OR + 'src/__tests__/ks1213-a-derived-writer-relabel-is-refused.test.ts')],
           intermediate=('ks1213-a-derived-writer-relabel-is-refused.test.ts after 1229-LOOSE', 'e7c614d3eae9', 311),
           patch_sha16={}, a4=[], a5=[], tampers={'LOOSE': 6, 'SIDEEFFECTS': 6}, tamper_reds='6 red cells over 2 declared titles per tamper; develop cover EMPTY', lane_dev=835, lane_head=850, lock=('06:07:36Z', '06:13:28Z'), ready='07:11:34Z',
           pushed_by='B19 (06:13Z, the ALREADY-PUSHED arm); PR opened by B20', prior_pr='1155',
           inhook='12/15 legs ran, 3 SKIPPED (3 4 8); shell suites 45/45', title='KS-1229 LOOSE SIDEEFFECTS: pin non-string documentType refusal and no upstream sends', claude_written=[]),
 '5': dict(n='1196', key='KS-629', keys=['KS-629'], tags='LIVENESSRT', kind='code_patch', seat='B20', head='79a8955667fae3b34f2e6ab31b1dda35911a28f3', tree='d84e6be6740ceb2d8f823fed584bcfc03bdf9392',
           branch='refs/heads/feature/ks-629-kyc-livenessvideo-is-accepted-by-spec-and-runtime-then-r16b-livenessrt-1', tier_ready=1, targets=2, adds=63, dels=1, lane='kyc',
           files=[dict(path=KY + 'src/__tests__/ks629-kyc-livenessvideo-is-accepted-by-spec.test.ts', kind='test', mode='new', blob12='c845f8b93f8b', lines=63, adds=63, dels=0),
                  dict(path=KY + 'src/index.ts', kind='product', mode='modify', blob12='f473857c5a16', lines=1260, adds=0, dels=1)],
           canon=[('629-LIVENESSRT-s2', '2026-09-22_ks629-ornith35b-night', 'section_2.diff', '773d42c5e28e4642', '', KY + 'src/__tests__/ks629-kyc-livenessvideo-is-accepted-by-spec.test.ts'),
                  ('629-LIVENESSRT-s1', '2026-09-22_ks629-ornith35b-night', 'section_1.diff', 'e072e663c9ee3de8', '', KY + 'src/index.ts')],
           patch_sha16={'2026-09-22_ks629-ornith35b-night': '839aa7e9f935ca21'}, a4=[(1, 3)], a5=['3/3'], lane_dev=26, lane_head=29, lock=('07:10:26Z', '07:15:58Z'), ready='07:19:36Z',
           inhook='12/15 legs ran, 3 SKIPPED (3 4 8); shell suites 45/45', title='KS-629 LIVENESSRT: livenessVideo removed from the runtime selfie schema (Part A)', claude_written=[]),
 '6': dict(n='1198', key='KS-974', keys=['KS-974'], tags='CHECKKEYCP SCOPETRIM', kind='code_patch', seat='B20', head='8ccfed7b64a76627bad51e2402575623d6b6d0e6', tree='4aab1f15d8baf90a14e841f73a50e13b45c14b03',
           branch='refs/heads/feature/ks-974-published-bound-vs-runtime-bound-on-rate-limit-scope-check-r16b-checkkeycp-scopetrim-1', tier_ready=1, targets=4, adds=68, dels=1, lane='security',
           files=[dict(path=SE + 'src/__tests__/ks974-check-key-bound-code-points.test.ts', kind='test', mode='new', blob12='67f14e73428a', lines=31, adds=31, dels=0),
                  dict(path=SE + 'src/__tests__/ks974-published-bound-vs-runtime-bound-on.test.ts', kind='test', mode='new', blob12='a0f1ae176918', lines=30, adds=30, dels=0),
                  dict(path=SE + 'src/index.ts', kind='product', mode='modify', blob12='7bdaa9cad257', lines=1602, adds=6, dels=1),
                  dict(path=SE + 'src/requestSchemas.ts', kind='product', mode='modify', blob12='b8c63d3f0ae5', lines=90, adds=1, dels=0)],
           canon=[('974-CHECKKEYCP-s2', '2026-09-22_ks974-ornith35b-night', 'section_2.diff', 'b5c8de533eba7a72', '--directory=Blockchain/Dev', SE + 'src/__tests__/ks974-check-key-bound-code-points.test.ts'),
                  ('974-CHECKKEYCP-s1', '2026-09-22_ks974-ornith35b-night', 'section_1.diff', '1cc0132e48a8f1fd', '--directory=Blockchain/Dev --recount --ignore-whitespace', SE + 'src/index.ts'),
                  ('974-SCOPETRIM-s2', '2026-09-22_ks974-ornith35b-night2', 'section_2.diff', 'aa3d156ce41fd5ff', '', SE + 'src/__tests__/ks974-published-bound-vs-runtime-bound-on.test.ts'),
                  ('974-SCOPETRIM-s1', '2026-09-22_ks974-ornith35b-night2', 'section_1.diff', 'ff75d1d2329d1fb9', '--recount --ignore-whitespace', SE + 'src/requestSchemas.ts')],
           patch_sha16={'2026-09-22_ks974-ornith35b-night': '07835921cff7f331', '2026-09-22_ks974-ornith35b-night2': '41a0a17ed61a71ac'}, a4=[(2, 3), (2, 3)], a5=['3/3', '3/3'], lane_dev=220, lane_head=226, lock=('07:18:00Z', '07:24:16Z'), ready='07:28:49Z',
           inhook='12/15 legs ran, 3 SKIPPED (3 4 8); shell suites 45/45', title='KS-974 CHECKKEYCP SCOPETRIM: /check bounds the key by code points, scope by trimmed value', claude_written=[]),
 '7': dict(n='1199', key='KS-976', keys=['KS-976'], tags='SCOPE403', kind='code_patch', seat='B20', head='a94180ce7b24a0654418479f0c4ec3db2a63340c', tree='d8b5b673fc1c5a2bb4de1ae246758f3695e61826',
           branch='refs/heads/feature/ks-976-rate-limit-refusals-name-the-wrong-field-400-says-key-r19-scope403-claude-1', tier_ready=1, targets=2, adds=80, dels=2, lane='security',
           files=[dict(path=SE + 'src/__tests__/ks976b-rate-limit-403-says-which-scope-claim-failed.test.ts', kind='test', mode='new', blob12='e508fc97af25', lines=77, adds=77, dels=0),
                  dict(path=SE + 'src/index.ts', kind='product', mode='modify', blob12='5bf6fb62dba8', lines=1598, adds=3, dels=2)],
           canon=[('976-SCOPE403-s2', '2026-09-22_feed11-drafter-precheck/SCOPE403', 'section_2.diff', '3d51eff35b166ab6', '', SE + 'src/__tests__/ks976b-rate-limit-403-says-which-scope-claim-failed.test.ts'),
                  ('976-SCOPE403-s1', '2026-09-22_feed11-drafter-precheck/SCOPE403', 'section_1.diff', '19098d293fab210b', '', SE + 'src/index.ts')],
           patch_sha16={'2026-09-22_feed11-drafter-precheck/SCOPE403': 'c8d4588999ecc9a8'}, a4=[(2, 3)], a5=['3/3'], lane_dev=220, lane_head=223, lock=('07:30:09Z', '07:35:53Z'), ready='07:40:16Z',
           inhook='12/15 legs ran, 3 SKIPPED (3 4 8); shell suites 45/45', title='KS-976 SCOPE403: the rate-limit 403 names which scope claim failed (Claude-written)', claude_written=['976-SCOPE403 (whole PR: GOLDEN run dir)']),
 '8': dict(n='1200', key='KS-1164', keys=['KS-1164'], tags='REPORTPATH', kind='code_patch', seat='B20', head='3a979effb886437ecc1276a547cc41aed830994e', tree='d309bb90f69f1f05506317978133115093d44804',
           tree_unamended12='2a91afd2029e',
           branch='refs/heads/feature/ks-1164-gatereportts-writegatereport-overwrites-the-input-summary-r16b-reportpath-1', tier_ready=1, targets=2, adds=49, dels=1, lane='performance',
           files=[dict(path=SP + 'gate/report.ts', kind='tooling', mode='modify', blob12='0a910cd855c3', lines=350, adds=3, dels=1),
                  dict(path=SP + 'tests/unit/gate/ks1164-write-gate-report-never-overwrites-its-input.test.ts', kind='test', mode='new', blob12='b4edbe5b0d12', lines=46, adds=46, dels=0, canon_blob12='1d41e7033542', canon_lines=43)],
           canon=[('1164-REPORTPATH-s2', '2026-09-22_ks1164-ornith35b-night', 'section_2.diff', '0d4795bd5f4dea68', '', SP + 'tests/unit/gate/ks1164-write-gate-report-never-overwrites-its-input.test.ts'),
                  ('1164-REPORTPATH-s1', '2026-09-22_ks1164-ornith35b-night', 'section_1.diff', '04de3585256bb3ef', '', SP + 'gate/report.ts')],
           patch_sha16={'2026-09-22_ks1164-ornith35b-night': '83391dc6b8d540fb'}, a4=[(1, 2)], a5=['2/2'], lane_dev=1083, lane_head=1085, lock=('07:38:34Z', '07:38:49Z'), ready='07:48:36Z',
           inhook='NO PREFLIGHT — the hook ran NO legs (systemTest/performance/ paths only; the Blockchain/Dev path filter): `[format-gate] systemTest/performance — format:check OK` / `1 package(s) checked, 0 skipped, 0 failed`',
           title='KS-1164 REPORTPATH: writeGateReport never overwrites its input summary', claude_written=['1164 AMENDMENT (the ruled (b) whitespace-only rewrap of the NEW test file, Claude-authored; the canonical is the model\'s)']),
 '9': dict(n='1201', key='KS-1179', keys=['KS-1179'], tags='F2F3', kind='test_only', seat='B20', head='6e675cb815e984f9fa013f54ec4f214b552e56a2', tree='8e86ebc411d6254965bfefc35be2a304580fc5c9',
           branch='refs/heads/feature/ks-1179-safeoutboundrequest-tests-no-cell-pins-dns-layer-r19-f2f3-claude-1', tier_ready=1, targets=1, adds=15, dels=1, lane='shared',
           files=[dict(path=SH + 'src/__tests__/ks932-timeout-bounds-dns.test.ts', kind='test', mode='modify', blob12='4022d4ecd2e5', lines=89, adds=15, dels=1)],
           canon=[('1179-F2F3', '2026-09-22_feed7-drafter-precheck/1179F2F3-R16B', 'patch.diff', '1b38f41e886ad3dc', '', SH + 'src/__tests__/ks932-timeout-bounds-dns.test.ts')],
           patch_sha16={}, a4=[], a5=[], tampers={'T2': 1}, tamper_reds='1 red cell (KS-932 the budget is shared) == declared; develop cover = that same cell (the cover-aware predicate)', tamper_file=SH + 'src/security/ssrf-guard.ts',
           lane_dev=917, lane_head=917, lock=('07:41:57Z', '07:48:13Z'), ready='07:52:33Z', typecheck_delta=-1, prior_pr='1157',
           inhook='12/15 legs ran, 3 SKIPPED (3 4 8); shell suites 45/45', title='KS-1179 F2F3: pin the shared DNS budget at the ssrf guard (Claude-written, test-only)', claude_written=['1179-F2F3 (whole PR: GOLDEN run dir)']),
}
LANES = {'originate': (OR, 'jest', 835, 863), 'kyc': (KY, 'vitest', 26, 29), 'security': (SE, 'vitest', 220, 229), 'shared': (SH, 'vitest', 917, 917), 'performance': (SP, 'vitest', 1083, 1085)}   # (dir, runner, bare develop baseline, the seat's batch count on the all-11 tree)
BATCH = 'originate 863/863 · kyc 29/29 · security 229/229 · shared 917/917 · perf 1085/1085; tsc rc 0 ×5'
TAMPER_FILES = ['boot/my_files19.txt']   # the seat's 17 targets + 2 tamper files list (19 lines) — in its record folder, NOT read by the drafter
# Seat C 19th's twelve on the same base (gate19C's round19C.py — its 21 paths): the partition is scripts / docs / hooks / schemathesis / root CLAUDE.md
SIBLING_GATE_DIR = '/Volumes/DevMASTER/WEDNESDAY/2_Project_Files/fleet/qa-agent/gatesets/2026-09-22_gate19C_seatC'
SEATC_GO = 'GO: merge #1180, #1181, #1183, #1185, #1187, #1188, #1190, #1191, #1192, #1193, #1195, #1197 batch'
SEATC_ALL12 = '5a8458a5697f7ee5b1800864b9f49347c8cbe34e'
REPORT_DIR = '/Volumes/DevMASTER/!CODING/Testing Agent MAIN/projects/secuura/reports/2026-09-22-batch1182-1201-r1/'
PRIOR_REPORT = '/Volumes/DevMASTER/!CODING/Testing Agent MAIN/projects/secuura/reports/2026-09-22-batch1170-1179-r1/'   # the gate18B report (Seat B 18th's seven)
SIBLING_REPORT = '/Volumes/DevMASTER/!CODING/Testing Agent MAIN/projects/secuura/reports/2026-09-22-batch1180-1197-r1/'  # gate19C (Seat C 19th's twelve) — may or may not exist at launch
SEAT_RECORD_19 = '/Volumes/DevMASTER/!CODING/Secuura/Blockchain/5_Project_History/2026-09-22_seatB-19th/'
SEAT_RECORD_20 = '/Volumes/DevMASTER/!CODING/Secuura/Blockchain/5_Project_History/2026-09-22_seatB-20th/'
HANDOVER = '/Volumes/DevMASTER/!CODING/Secuura/Blockchain/5_Project_History/HANDOVER-seatB-19th-successor-2026-09-22.md'
ARCHIVED = ['KS-501', 'KS-480', 'KS-978', 'KS-721', 'KS-522', 'KS-726', 'KS-535', 'KS-867', 'KS-878', 'KS-914', 'KS-1238', 'KS-1282', 'KS-1062', 'KS-971', 'KS-1078', 'KS-921', 'KS-490',
            'KS-597', 'KS-727', 'KS-764', 'KS-879', 'KS-1020', 'KS-835', 'KS-1270', 'KS-549', 'KS-733', 'KS-815', 'KS-1013', 'KS-1058', 'KS-1103', 'KS-666', 'KS-754', 'KS-926', 'KS-487', 'KS-386', 'KS-444', 'KS-1092']   # 37 (the READYs list 36 without KS-1270)
OWN = sorted(set(k for p in PUSH for k in PRS[p]['keys']))   # 9 keys
TIER1_RULE = [p for p in PUSH if any(f['kind'] in ('product', 'tooling') for f in PRS[p]['files']) or any(f['path'] in AUTH_ADJACENT for f in PRS[p]['files']) or PRS[p].get('tamper_file', '').endswith('ssrf-guard.ts')]
TIER1_READY = [p for p in PUSH if PRS[p]['tier_ready'] == 1]
TEST_ONLY = [p for p in PUSH if PRS[p]['kind'] == 'test_only']
GO_STRING = 'GO: merge #1182, #1184, #1186, #1194, #1196, #1198, #1199, #1200, #1201 batch'
def canon_path(row): return LM + '/runs/' + row[1] + '/out.md.checker/' + row[2]
def all_paths(): return [f['path'] for p in PUSH for f in PRS[p]['files']]
def distinct_paths(): return sorted(set(all_paths()))
def ready_regex(): return r'READY FOR QA \(Seat B (?:19|20)th\): PR (\d+) (KS-\d+)[^\n]*? — #(\d+) at head ([0-9a-f]{40})'
if __name__ == '__main__':
    import sys; sys.path.insert(0, SIBLING_GATE_DIR)
    try:
        import round19C as C; cpaths = C.distinct_paths()
    except Exception as e:
        cpaths = None; print('round19C import failed:', e)
    print('PRs', len(PRS), 'file rows', len(all_paths()), 'distinct', len(distinct_paths()), 'canon rows', sum(len(PRS[p]['canon']) for p in PUSH),
          'adds', sum(PRS[p]['adds'] for p in PUSH), 'dels', sum(PRS[p]['dels'] for p in PUSH), '| per-PR adds/dels consistent', all(sum(f['adds'] for f in PRS[p]['files']) == PRS[p]['adds'] and sum(f['dels'] for f in PRS[p]['files']) == PRS[p]['dels'] for p in PUSH))
    print('TIER1 by FILE rule', TIER1_RULE, '| TIER1 by READY', TIER1_READY, '| rule minus ready', sorted(set(TIER1_RULE) - set(TIER1_READY)), '| ready minus rule', sorted(set(TIER1_READY) - set(TIER1_RULE)), '| test-only', TEST_ONLY, '=', [PRS[p]['n'] for p in TEST_ONLY])
    print('OWN keys', len(OWN), OWN, '| targets', [PRS[p]['targets'] for p in PUSH], 'sum', sum(PRS[p]['targets'] for p in PUSH), '| file rows == targets sum:', len(all_paths()) == sum(PRS[p]['targets'] for p in PUSH))
    print('pair path rows:', [PRS[p]['n'] for p in PUSH for f in PRS[p]['files'] if f['path'] == PAIR_PATH], '| distinct 17:', len(distinct_paths()) == 17)
    if cpaths is not None: print('Seat C 19th paths', len(cpaths), '| B ∩ C:', sorted(set(all_paths()) & set(cpaths)) or 'NONE', '| C.SEATB_PATHS ⊂ B paths:', set(C.SEATB_PATHS) <= set(all_paths()), '| C.DEV == DEV:', C.DEV == DEV)
    print('lanes', {k: v[2:] for k, v in LANES.items()}, '| claude_written rows', [(PRS[p]['n'], PRS[p]['claude_written']) for p in PUSH if PRS[p]['claude_written']])
