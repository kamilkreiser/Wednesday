# notes.md: drafter for Seat B 187th (2026-11-16 07:27 to about 07:50 AEDT)

Brief: /Volumes/DevMASTER/WEDNESDAY/2_Project_Files/fleet/briefs_staged/2026-11-16_seatB187_merge.md (about 51 KB; B 186th's was 52 KB, so carried prose was compressed; the per-row files +/- figures were dropped from the BLUF 3 table, merge-bases and commits-ahead moved here, and the per-ticket Linear lines are below).
Scripts (session scratchpad, not durable; durable copies in _work/scripts/): mt.py (merge trees, chain, K overlap, pairs, plants), show.py, matcher.py, kit.py, kit2.py, cr.sh, gates.py, lin.py, s2080.sh, fetch2.sh, kfetch.sh, api.sh; run output mt187.json. Nothing written under !CODING; GitHub and Linear read-only; no credential printed (Linear key from the Secuura Blockchain project .env read inside python only).

## Measured
- develop 6185f0f1ace8344efa81df091d2e5dd718e7f9e4 (PR 2146 squash by Seat K 34th, committer 2026-11-15T20:32:10Z, ONE parent a129a5f03f88040b6fc6b537209f703675685548, tree d4e004ad51f88a094d14cee0af000b32d5c3831b), read via gh api 07:34:21 and 07:38:04 and the clone fetch 07:34:46. Before it: a129a5f03f88 (PR 2129 squash by B 186th, 20:20:07Z, tree 2c4676eb8ee7da21eb10954e9fc9ac858d904ce7), read 07:27:31; the whole merge run was done on a129 (07:30:23) and repeated on 6185 (07:34:53).
- 22 queue rows: all open, unmerged, heads equal B 186th's table, base develop, not draft; mergeable read empty at 07:27 and true/unstable at 07:36; 0 success check-runs. No REMOVED row. K rows: 2146 merged; 23 open, 24 of 24 heads equal K 34th's queue_k34.json.
- Merge trees: 22 of 22 rc 0 both orders, same tree each; stacked chain 22 of 22 rc 0 (after row 22 d8c8c29b1363 on 6185; bb3550783bc7 on a129 = B 186th's after-row-23 figure). Planted controls (first ten): positives 10/10 rc 1 in both orders, negatives 20/20 rc 0.
- Both-sided rows: 2080 (NEW, m365 index.ts), 2162 (1 path), 2066 (2), 2059 (1), 2075 (1), 2073 (2), 2052 (3): 7 rows, 11 paths. 2100 has none. K-row overlap: none. adminConfig.ts: no B row, no K row.
- 2080 re-measure on 6185: hunks (base lines) 557, 688, 868, 874, 1173; 2129's hunks 1276, 1294, 1489; rc 0 both orders tree dbb2c47390ae (52d2b0d6756f on a129); 22 of 22 of 2080's distinct added lines and 14 of 14 of 2129's present in the merged index.ts; assertSafeOutboundUrl count 3 on develop, 2080 head, merged.
- Matcher (scratch copies of b186_match.py, sha16 02f7da408637521d, 11,777 bytes): original 765 distinct, head B 185th; control 774/774; edited n 770, 779/779; no-P1 778/779; own-seat mutant 779/780; bare rule 773/774 (rewrites B 1186th to B 1187th); no-predecessor 778/778. B 187th PRESENT (only entry with 187th), B 186th ABSENT; B 287th, B 1087th, B 1187th, B 1487th, B 1587th ABSENT; B 286th, B 1086th, B 1186th, B 1486th, B 1586th, B 1077th, B 1177th, B 1477th, B 1577th, B 1185th, B 1485th, B 1585th, B 285th, B 1184th, B 1183rd PRESENT.
- Kit (B 186th's tools + evidence): tools 39 regular, src_b185 39, src_b185_evidence 54 (all 54 present shifted in evidence), evidence 142 top-level; engine set 93 files, 88 carry b186, 571 hits (0 digit-preceded; 3 session-id hits => 568 designed); B186 26 in 9; 186th 302 (91 files) + 1 dp; 186TH 2; 187th 1; 185th 4 (3 files) + 1 dp; 184th 1 + 1; 183rd 1 + 1; b185 0; b184 2; dir token seatB-186th 71 in 66 files, seatB-185th 1. Adjacency (116 top-level .py/.sh of tools+evidence): 16 hits in 9 files = 9 designed (merge_trees_plan 4 + its before_pin_edit 4, rekey 1) + 7 session-id (ctx_usage, go_gate_fixture_run, faults_count, faults_count.before_amname, send_ready_2129 1 each; setup 2); b186d9de in 11 files recursively; plain shift 717 vs 710 with the exclusion; plain shift would write b187d9de 7 times. UUID: ready_build2_b186.py holds 4705-b177-af2deef051a3 once, 4705-b186 zero; rekey_b186.py 4705-b185- once, 4705-b186- zero. Baselines v3 626c3252ee8a0c88, v1 e78e5c14e2f22dcd, v2 e85a2aa53042f85d (31 lines each) = B 186th's FINAL. setup_b186.py: 9942bae93563 x4 (40-hex x1), ba52b1d7cc43 x3, anchors ["B 185th", x1, "B 1585th" x3, neighbours B 286th/B 1086th/B 1186th/B 1486th x2 each. Own-authored 8 present, 0 shifted; finish_by_hand_2158_b185.sh is in REC185 only.
- Ordinal: Seat B 187th 0; Seat B 186th 1 (line 9); Seat B 185th 2 (lines 9, 26); B 184th 2; B 183rd 2; control B 176th 1 (line 494); K 34th 1 (line 1); K 33rd 2; K 35th 0.
- Host 07:38: df 2023 GiB free 46%; load 5.01/5.51/6.13; rate limit core 4847; push queue 1 entry (Seat C 42nd pid 63182, joined 20:29:45Z). Machine date 2026-11-16 throughout. Floor: wednesday %0, -D %140, -S %137, -C %128, fleet-monitor %1; no -B, no -K.
- K 34th WRAPPED (history line 1; HANDOVER FINAL ~07:37): r 51.2, READY +17.9 (PLAN 20.0, SET-UP CLOSED 31.4, READY 49.3), next K row PR 2143; TRAP: nine packages/shared guard files are cwd-dependent (use npm --prefix <pkg> test); develop-only originate flake ks488/ks1937.
- B 186th HANDOVER FINAL text clock 'about 07:27 AEDT = 20:27Z' vs file mtime 07:24:29, wrap_sent.json mtime 07:24:53, K 34th's text WRAPPED at 20:24:49Z.

## Linear (read 07:37; state, comments, newest comment UTC)
KS-1868 IP 90 2026-11-15T16:01:09Z; KS-1205 IP 8 11-06T20:38:39Z; KS-1208 IP 3 11-09T05:21:16Z; KS-1670 IP 3 11-06T18:25:31Z; KS-624 IP 3 11-09T05:59:06Z; KS-785 IP 1 11-09T04:40:53Z; KS-2122 IP 1 11-10T01:45:42Z; KS-2071 IP 1 11-06T18:28:06Z; KS-2074 IP 1 11-06T20:06:34Z; KS-1473 IP 2 11-09T06:35:30Z; KS-590 IP 6 11-09T09:06:18Z; KS-1991 IP 1 11-10T01:25:27Z; KS-2032 IP 1 11-06T13:53:50Z; KS-1410 IP 10 11-06T20:47:52Z; KS-1214 Backlog 4 11-06T20:47:53Z; KS-2151 IP 1 11-09T08:30:02Z; KS-2083 IP 2 11-08T10:08:43Z; KS-1807 IP 16 11-09T08:12:36Z; KS-1152 IP 4 11-08T11:07:32Z; KS-625 IP 2 11-09T06:16:52Z; KS-1081 IP 7 11-08T11:24:27Z; KS-1864 IP 2 11-08T16:45:25Z; KS-1090 IP 11 11-11T20:01:50Z; KS-784 IP 5 11-09T05:41:15Z; KS-1641 DONE 10 2026-10-26T13:14:00Z (B 186th's drafter: NOT FOUND); KS-2147 IP 1 11-09T12:01:07Z.

## Full table on develop 6185f0f1ace8 (PR | head40 | merge-base12 | commits ahead on develop | files | rc d,h / h,d | tree12 (both orders) | stacked tree12 after the row)

| 2100 | eb4a08362cfb6ce90ffa094078bd8620caebe5e7 | c0e6e744b7b2 | 129 | 4 | 0/0 | 407792ffde4d | 407792ffde4d |
| 2064 | 6c8856baf1025d8048969a4facc7101ea30cbb7b | 9cdb9321aa8a | 152 | 4 | 0/0 | 240adb155132 | 2459bddc9434 |
| 2128 | c7e84537d2aeb6b1c11aeaebdff203a7aa6ff181 | 4d6b7bb17fd3 | 111 | 4 | 0/0 | 1bc90db721c5 | f1f1f1c5611b |
| 2080 | 83ee8509c985b656e2f2b635bc753148a2de3b2b | c5c26b2835df | 154 | 4 | 0/0 | dbb2c47390ae | 2e399e7d4c08 |
| 2130 | 11a39402623328f2ee8368284cd397630bca13d5 | 204e62acdc35 | 110 | 4 | 0/0 | 404103bda568 | 31254cd9a8aa |
| 2127 | 7dc6ff72cf61de04bb65a0e859cf670e9ff0ac85 | 4d6b7bb17fd3 | 111 | 5 | 0/0 | d998d57a228a | fe3fc52c6956 |
| 2162 | 30048d8b295e6be51540b015033aa4bb20ca5fe4 | 0115269abd11 | 102 | 5 | 0/0 | a9a8c281841c | 36e5786f5edd |
| 2067 | 0d08681c616d9459b87387ef9c5ab11f478678e8 | cd773edc2bb8 | 150 | 6 | 0/0 | f5e173b6fa48 | b31e02a6f459 |
| 2085 | 4d4726ca41d99d5eab8c4a5a27b3a4317917beb8 | 35bcfa000b44 | 149 | 6 | 0/0 | b5c46cb5a402 | 3c15634fc72d |
| 2132 | ba0ab4f453497257e9848c16f884ae8900a2f195 | 204e62acdc35 | 110 | 7 | 0/0 | fb714ed354a1 | b8d3b68d194e |
| 2138 | fdf80425e9d5c4f99f0a7b5c5c7521b0f7a39ec1 | f98afb113c2d | 107 | 9 | 0/0 | 77880bdbe27e | 6e7c1074c2a5 |
| 2161 | 0e50defb7819fe53a92ef6711a8a91e6b2d20f04 | 07d4218e9776 | 103 | 11 | 0/0 | 2da2a3aa8e90 | eb01438fec03 |
| 2066 | baf577c78e7f876551e132e407d0982232622de9 | 35bcfa000b44 | 149 | 14 | 0/0 | 2e1e8369fc00 | ea9549e88f57 |
| 2059 | 5d8969b36a24914c24bc6a839f819ec8be3772e9 | c5c26b2835df | 154 | 14 | 0/0 | 8bd4170bbd9d | cfa7e394514f |
| 2136 | b907ba03bea2e2fdcd6c1fe7aa0dc73f4c7f1edd | e8d23ce366e2 | 108 | 3 | 0/0 | f948cfb07ac9 | c80154b42501 |
| 2075 | 32aa0d06bc0aceccb790443bbf16384ff0c8e930 | 631ccfb8266a | 145 | 4 | 0/0 | 03cd018e2624 | 07bb7a216391 |
| 2135 | e2ada9bf1ea9db6c901a3a33723241e9d38be031 | e8d23ce366e2 | 108 | 3 | 0/0 | 44a37d6b04ba | ca16b21ad425 |
| 2073 | 2684a29d8f576ff74634f07ad6576af5bd00370b | bdbb11b21585 | 147 | 8 | 0/0 | 74cb8610a187 | b968d89c893a |
| 2131 | 89081fae75e54e78e509d50a81cb0cd82c00eedd | 204e62acdc35 | 110 | 6 | 0/0 | f0b2bce9e16e | e683a162a41d |
| 2052 | b61674e7b7635a50d51f837849cb9caf1259235d | cfb6c1573ba9 | 135 | 32 | 0/0 | 3ec9c7a26b43 | 6072edf16931 |
| 2102 | 247e62dc7337a0f87e2b8a20d9c6107e6fcccf14 | fa0592f3b6f5 | 127 | 5 | 0/0 | 47802390432d | 575df3aa8f1a |
| 2191 | 96ac07b0cd0daf45a8a27580ca0750de8c826f17 | 16a5c67e676e | 85 | 9 | 0/0 | c21bf1061af1 | d8c8c29b1363 |

Both-sided paths per row (all under Blockchain/Dev/): 2080 Blockchain/Dev/services/m365-integration/src/index.ts; 2162 Blockchain/Dev/services/api-gateway/src/__tests__/ks1448-notification-create-own-id-only.test.ts; 2066 Blockchain/Dev/docs/security/ROLES-AND-AUTHORIZATION-INVENTORY.md, Blockchain/Dev/packages/shared/src/security/keyRevokePolicy.ts; 2059 Blockchain/Dev/MCP Deployment/troubleshooting.md; 2075 Blockchain/Dev/services/auth/src/routes/users.ts; 2073 Blockchain/Dev/docs/openapi/secuura-api.yaml, Blockchain/Dev/services/api-gateway/src/routes/platform.ts; 2052 Blockchain/Dev/scripts/check-stack-safety.sh, Blockchain/Dev/scripts/verify-slot-credential-isolation.sh, Blockchain/Dev/services/auth/src/__tests__/ks949-platform-admin-seed-identity.test.ts

## Planted controls (first ten; path, lines base->develop, pure insertion?, positive rc both orders, negatives vs next two rows in the ring of ten)
- 2100 Blockchain/Dev/services/originate/src/services/email.ts [[139, 139]] ins=False pos=[1, 1] negs=[2064, 2128] [[0, 0], [0, 0]]
- 2064 Blockchain/Dev/services/api-gateway/src/middleware/rateLimitEnforce.ts [[167, 167], [168, 168]] ins=True pos=[1, 1] negs=[2128, 2080] [[0, 0], [0, 0]]
- 2128 Blockchain/Dev/services/api-gateway/src/middleware/auth.ts [[12, 12], [13, 13]] ins=True pos=[1, 1] negs=[2080, 2130] [[0, 0], [0, 0]]
- 2080 Blockchain/Dev/services/m365-integration/src/index.ts [[557, 557], [558, 558]] ins=True pos=[1, 1] negs=[2130, 2127] [[0, 0], [0, 0]]
- 2130 Blockchain/Dev/services/prism/src/index.ts [[27, 27]] ins=False pos=[1, 1] negs=[2127, 2162] [[0, 0], [0, 0]]
- 2127 Blockchain/Dev/scripts/__tests__/check_slot_credentials.test.sh [[387, 387], [388, 388]] ins=True pos=[1, 1] negs=[2162, 2067] [[0, 0], [0, 0]]
- 2162 Blockchain/Dev/services/api-gateway/src/__tests__/ks1448-notification-create-own-id-only.test.ts [[163, 172]] ins=False pos=[1, 1] negs=[2067, 2085] [[0, 0], [0, 0]]
- 2067 Blockchain/Dev/services/staking/.env.example [[19, 19], [20, 20]] ins=True pos=[1, 1] negs=[2085, 2132] [[0, 0], [0, 0]]
- 2085 Blockchain/Dev/services/security/src/index.ts [[363, 363], [364, 364]] ins=True pos=[1, 1] negs=[2132, 2100] [[0, 0], [0, 0]]
- 2132 Blockchain/Dev/services/api-gateway/src/__tests__/ks1461-case-variants-keep-the-gateway-checks.test.ts [[207, 207]] ins=False pos=[1, 1] negs=[2100, 2064] [[0, 0], [0, 0]]

## Pairs (head-vs-head rc,tree12; develop+A+B rc,tree12; develop+B+A rc,tree12; equal)
- 2127+2052 ['Blockchain/Dev/scripts/check-slot-credentials.sh'] hh=[0, '3c44e0388b8e'] ab=[0, '31918a7e834b'] ba=[0, '31918a7e834b'] eq=True
- 2085+2066 ['Blockchain/Dev/services/security/src/index.ts'] hh=[0, '284e3322c0e5'] ab=[0, '8a5f4ccdeeef'] ba=[0, '8a5f4ccdeeef'] eq=True
- 2138+2161 ['Blockchain/Dev/services/originate/src/routes/verification.ts', 'Blockchain/Dev/services/originate/src/routes/verificationV2.ts'] hh=[0, '13ead6a75bdb'] ab=[0, '08187f87eb64'] ba=[0, '08187f87eb64'] eq=True
- 2136+2135 ['Blockchain/Dev/docs/S-K-OWNERSHIP-CONTRACT.md'] hh=[0, '8f92fa25ce9b'] ab=[0, '6f6b3d8589b1'] ba=[0, '6f6b3d8589b1'] eq=True
- 2136+2073 ['Blockchain/Dev/docs/S-K-OWNERSHIP-CONTRACT.md'] hh=[0, '461982053b45'] ab=[0, '79378e9decab'] ba=[0, '79378e9decab'] eq=True
- 2135+2073 ['Blockchain/Dev/docs/S-K-OWNERSHIP-CONTRACT.md'] hh=[0, 'c63939bbf42d'] ab=[0, '3f5efbe8845d'] ba=[0, '3f5efbe8845d'] eq=True
- 2073+2131 ['Blockchain/Dev/docs/openapi/secuura-api.yaml'] hh=[0, '990fb4912eb6'] ab=[0, '11bc8a7f5d65'] ba=[0, '11bc8a7f5d65'] eq=True

## Judgement calls (declared)
- Row 1 forecast READY +14 to +18 from SET-UP CLOSED: seven measured first rows (+14.6, +14.7, +14.9, +15.0, +15.0, +17.4, +17.9). B 182nd/B 183rd/K 33rd/K 34th figures are from the predecessors' briefs and K 34th's FINAL, not re-opened.
- 2138 flagged HOLD-pending-card in W-7 on the commission's instruction; the card text was read only through the daily note's line (rec a, default nothing changes); the card itself was not opened.
- PR 2064, 2131, 2132 named in W-7 by TITLE only as audit/verification-adjacent (UNMEASURED beyond the title).
- 2080 expected rc 1 from the merge tool's blob check is REASONED from B 186th's TRAP 4 and the both-sided rule; no merge tool was run.
- The 07:16:08 Kam line is carried verbatim as the commission gives it; the learning file does not hold it (0 hits for 'personal fields').
- Brief is under 51,200 bytes (50 KiB) but above 50,000; the per-row files +/- and merge-base columns were cut to get there.

## UNMEASURED
- Any install, suite, tsc, eslint, vitest, jest, fragments run; every cost and leg forecast; whether originate needs its own install.
- Open-PR census; develop after 07:38; a K 35th launch; mail after wrap files; coagent inbox.
- Gate contents beyond named lines; whether gate 245/257 items for Kam were ruled; the launcher preflight; matcher, derive and date handling on the REAL kit; whether finish_by_hand_2158_b185.sh survives a shift.
