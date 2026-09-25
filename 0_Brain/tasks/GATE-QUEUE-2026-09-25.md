# Gate queue — Secuura round 21 + lanes L1-L4 (2026-09-25)

Batched per tier (the 09-18 batch rule). A row enters on its READY mail and only after Wednesday reads the head at origin (`ls-remote`) in the same action. Gate brief shape: `fleet/qa-agent/BRIEF_TEMPLATE.md`. Carry into every gate brief: the anchoring wording (KS-562), legs 3/4/8 (the stack comes up ONCE per gate for surfaced PRs; Docker is down now), and the load false-red note (KS-1155).

| tier | PR | key | seat | head (origin, read by Wednesday) | surface → legs 3/4/8 | READY at |
|---|---|---|---|---|---|---|
| 1 | #1213 | KS-530 | B 25th | f2751859c015 (ls-remote 13:1x) | none (lockfile/overrides) | 02:10Z |
| 1 | #1214 | KS-528 | B 25th | 6fce4d0b1886 (ls-remote 13:1x) | none | 02:10Z |
| 2 | #1215 | KS-1288 | L3 | 5e3419a46db5 (ls-remote 03:0x) | none (packages/shared test) | 03:06Z |
| 1 | #1216 | KS-975 it.2 | L2 | c44b15dddadd (ls-remote 13:1x) | security module; legs 3/4/8 OWED | 03:14Z |
| 1 | #1217 | KS-976 it.1 | L2 | e83f34447402 (ls-remote 13:1x) | /reset 400 message; legs 3/4/8 OWED | 03:14Z |
| 2 | #1218 | KS-897+896 | L4 | 999623d28f7c (ls-remote 13:1x) | none (scripts test) | 03:17Z |

| 2 | #1220 | KS-1129 | L2 | 9c2021ba3e77 (ls-remote 13:3x) | anchoring response field; legs 3/4/8 OWED; anchoring wording | 03:29Z |
| 2 | #1221 | KS-1266 | L1 | 0a561a5db393 (ls-remote 13:4x) | none (originate tests; port-1 fix) | 03:41Z |
| 2 | #1222 | KS-1181 F2 | L3 | 9bce90229ad6 (ls-remote 13:4x) | none (packages/shared test) | 03:48Z |
| 2 | #1223 | KS-1118 | L1 | 759726d8d (ls-remote 13:5x) | none (originate test + comment) | 03:49Z |
| 2 (NEXT batch) | #1225 | KS-1291 | L1 | 120420a2e (ls-remote 14:1x) | originate route guard removed; legs 3/4/8 OWED | 04:14Z |
| 1 (NEXT batch) | #1224 | KS-1179 | L3 | d4862b3eee35 (ls-remote 14:2x) | security ssrf-guard | 04:20Z wrap |
| 1 (NEXT batch) | #1226 | KS-872 | L3 | fcda1a6ef7e4 (ls-remote 14:2x) | none (type-only) | 04:20Z wrap |
| 2 (NEXT batch) | #1227 | KS-1252+1253 | L4 | 69a72726e8ee (ls-remote 14:4x) | none (scripts contract.mjs) | 04:40Z |
| 1 (NEXT batch) | #1228 | KS-1171 (Kam c) | L2 (wrapped) | 43279280f76e (ls-remote 14:4x) | anchoring; legs 3/4/8 OWED; integration cells | 04:41Z |
| 2 (NEXT batch) | #1229 | KS-865 + KS-808 (3) | L4 | ed85bd81d0ac (ls-remote 15:0x) | none (scripts) | 05:00Z |
| 1 (NEXT batch, when READY) | — | KS-1127+1089+1135 | L4 | 6320a61d8 (L4's mail, not re-read) | tier 1 per L4 | pushing |
| 1 (NEXT batch, 4th → LAUNCH) | #1230 | KS-1131 F-A+F-B | B 25th | 1116dab04664 (ls-remote 15:1x) | none; residual + property-2 relaxation | 05:15Z |
| 2 (NEXT batch) | #1231 | KS-1281 | B 25th | bd1d2daec2bf (ls-remote 15:1x) | none; least-priv SELECT unmeasured | 05:15Z |
| 2 (NEXT batch) | #1232 | KS-1128 | B 25th | ec0d7efcf682 (ls-remote 15:1x) | none; fake-pg only | 05:15Z |
| 3 | #1219 | KS-1277 | L1 | 5d5129a03af0 (ls-remote 13:2x) | none (comment-only) | 03:23Z |

**15:1x: TIER 1 next batch = 4 READY (#1224 #1226 #1228 #1230) → the drafter is widened to four (kit gate21T1b). TIER 2 next batch = 5 READY (#1225 #1227 #1229 #1231 #1232) → second drafter (gate21T2b).**

**TIER 2 = 4 READY at 13:4x (#1215, #1218, #1220, #1221) -> gate commissioned (a second drafter).**
**TIER-1 batch21T1 MERGED 14:40: #1216 feb5cf0c4, #1217 bc092c667 (L2); #1214 ba4016fb8814, #1213 → develop ecb1aa75aefa (Seat B 25th).**
**TIER 1 = 4 READY at 13:1x -> gate commissioned (drafter writing the brief).** 
Pending READY, known: B 25th ×3 Ornith PRs (tier 1 batch with #1213/#1214) · L1 A/B/C/J (tier 3/2/2/2) · L2 KS-975, KS-976 (tier 1), KS-1129 (tier 2) · L3 GF-2 (stacked on #1215) · L4 PR 1 (tier 2).
Rule for launching: launch a tier's gate when ≥4 of that tier are READY, or when the oldest READY in it is 60 min old, whichever is first.

**15:4x TIER-2 GATE batch1215 VERDICT (QA 05:33:03Z, report sha256 55cfc49a… verified on disk):** GO #1215 #1220 #1221 #1222 → SIGNED GOs: Seat B 25th merges #1220 → #1215 → #1222 (wrapped authors L2/L3); L1 merges #1221. NO GO #1218 (L4, FIXTURE-LASTCMD + FIXTURE-GITENV — the fixture can push from the caller's repo) and #1223 (L1, PRECEDENCE-DUP vs #1149): round 2 of 2 each, then the next tier-2 batch. Fleet safety warning on `pre_push_hook_base.test.sh` sent to all three seats. Pane %11 closed.

**15:4x MERGED + VERIFIED by Wednesday (ls-remote + PR API merged=True):** #1220 → 847159dcc, #1215 → 54d741e1c, #1222 → 379c6eb1d (Seat B 25th, wrapped-author PRs). develop == 379c6eb1d45905f398fae67ee7dd2f46ad40432f. #1221 (L1) pending its fetch under the lock. The next tier-1 kit is pinned to ecb1aa75, so its repin step 3b re-predicts over the moved develop at launch.

**15:5x THIRD tier-2 batch (after 21T2b):** #1235 KS-1140 GF-1 1c899947ea31 · #1236 KS-1110 A+B 4296ba6d090c (Seat B 25th, ls-remote 15:5x) + #1218 r2 (L4, d971aa4f2 per mail) + #1223 r2 (L1, 2892e5286 per mail) when READY → 4 = launch. Seat B 25th HOLDS by design for the re-dates (Kam's word).

**16:1x THIRD tier-2 batch COMMISSIONED (drafter → scratchpad gate21T2c, frozen at 7):** tier 2: #1218 r2 d971aa4f2 (L4) · #1233 KS-1133 6892124d9 (L1) · #1235 1c899947e · #1236 4296ba6d0 (B 25th) · #1237 KS-1229 cfa16eb70 (L1); tier 3: #1219 KS-1277 · #1238 KS-1158 0f3ffbb09 (L1). All heads read by `ls-remote` 16:0x. #1223 r2 joins only if its READY exists at capture. Tier-1 gate batch1224 running (%12). Tier-2b drafter (5 PRs) still building.

**16:2x NEXT tier-1 batch (after batch1224):** #1234 KS-1127+1089+1135 6320a61d86b5 (L4) · #1239 KS-1263 G 42c20e998a1a (L1; behavioural rollback cells OWED at the gate, both MULTI_TENANCY modes) — both by `ls-remote` 16:2x. 2 READY; launch at 4 or when the oldest is 60 min (#1234 READY 06:17Z → 07:17Z).

**16:3x TIER-2b GATE `QA/Secuura-batch1225` LAUNCHED 06:28:57Z (%13)** over develop 379c6eb1d (END_TREE 4da02cbfc813), 5 PRs #1225 #1227 #1229 #1231 #1232; kit 46/46 controls; routing line added (backup .pre-0925-1630-gate21T2b). Rulings for its GO: the pre-existing silent `!isDbAvailable()` path does NOT block #1231 (reported separately → ticket); squash bodies un-hyphenate foreign keys (KS-318 archived in #1229's body); squash subjects = the gate's ≤92-char lines. **#1223 r2 READY 06:27Z, head 2892e5286 (`ls-remote`)** → added to tier-2c (now 8, frozen).

**16:3x #1221 KS-1266 MERGED + VERIFIED** (`ls-remote` develop == 9e744421ada2166c8944764017cad76d94737286; PR API merged=True, same sha). Tier-2 batch1215 fully disposed: 4 merged (#1215 #1220 #1221 #1222), 2 NO GO → round 2 (#1218 in tier-2c, #1223 in tier-2c). The running gates batch1224 (t1) and batch1225 (t2b) were pinned to 379c6eb1d: their repin/merge steps handle the move (base-invariant).

**17:0x TIER-1 GATE batch1224 VERDICT (QA 07:02:18Z; report sha256 e551d0dc…, 53,220 B, verified on disk): ALL FOUR GO WITH FINDINGS, 0 Majors** (#1224, #1226, #1228, #1230); legs 3 + 8 RAN on #1228, leg 4 NOT RUN (demo login 401). BASE_GO 9e744421a == develop. The completion check passes (#1228 = ruling c, truth table 16/16; #1230 residuals R1/R2 recorded). **SIGNED GO → Seat B 26th** (the authors wrapped), addendum lines 273-276 + MG-3 line 115 pasted verbatim. #1226's KS-1292 link left. Pane %12 closed. Develop-move re-check per PR at each squash.

**17:1x TIER-1 batch1224 ALL FOUR MERGED + VERIFIED** (PR API merged=True; `ls-remote`): #1224 → 4ade45465, #1226 → c20e32bad, #1228 → 89a616165, #1230 → cf3de2c4c. develop == cf3de2c4cef5c636446d87fd68fed1073fc964ad. Merged by Seat B 26th on the 07:03Z GO (DKIM pass).

**17:3x TIER-2b batch1225 VERDICT (QA 07:27:37Z; report sha256 d7aa2dfd… verified on disk): ALL FIVE GO WITH FINDINGS.** Heads unmoved; develop cf3de2c4c == BASE_GO. #1231: the new fallback is LOUD (non-blocking); the pre-existing silent P-1 → a ticket (ruled). **SIGNED GO → Seat B 26th** with addendum lines 300-304 verbatim + foreign-key and subject rulings. %13 closed. Remaining gate: tier-2c (drafter; 8 PRs). Next tier-1: #1234 + #1239 (launch at 4 or 07:17Z → overdue: bring in with tier-2c or a small tier-1 kit).

**17:3x TIER-2b batch1225 ALL FIVE MERGED + VERIFIED** (PR API merged=True; `ls-remote`): #1225 → 1ded2f817, #1227 → 7f06f3d40, #1229 → ab7826afb, #1231 → b83f986fd, #1232 → aa600af94. develop == aa600af94d69ad59db279d32cbbd7596931a739b. Seat B 26th, merge22, dry-first each. Day total: 17 merged.

**17:3x READY #1240 KS-789 NOCIBACKSTOP (Seat B 26th, tier 3 doc-only, CONTRIBUTING.md), head 50800b9320ad by `ls-remote`.** Tier 3 = no gate: the next seat reads the diff against Kam's ruling (the CI clause struck + a `--no-verify` push must say so on the PR; the hook stays out → a new ticket), confirms doc-only, then GOs Seat B 26th.

**17:44 #1240 KS-789 (tier 3) GO sent to Seat B 26th** (head 50800b93 by ls-remote; diff = CONTRIBUTING.md +7/-2; DEV-PROCESS pointer verified at head). **#1241 KS-1226 item 2 READY 07:42Z, TIER 2, head e2d0518df402 (per the mail, not re-read)** -> the NEXT tier-2 batch (tier-2c is frozen at 8). Tier-2c + tier-1c kits were ORPHANED by the 17:3x rotation (no README); re-commissioned to drafters in the new seat scratchpad `d384786a…/scratchpad/gate21T2c|gate21T1c`.

**18:04 #1242 KS-980 READY (Seat B 26th, TIER 2, head a35569aa020e by Wednesday ls-remote; disposable Postgres torn down 08:01:56Z per its mail).** NEXT tier-2 batch = #1241 + #1242 (2). Seat B 26th told to file the pg_isready finding and stay up to merge the tier-2c / tier-1c GOs.

**18:19 TIER-2c GATE `QA/Secuura-batch1218` LAUNCHED 08:18:27Z (%15)** over develop d9515f4a06e0 (END_TREE 15dfe75db96e), 8 PRs #1218 r2 #1219 #1223 r2 #1233 #1235 #1236 #1237 #1238; kit re-drafted in the 17:40 seat (43/43 controls, repin dry-run rc 0) and moved to `gatesets/2026-09-25_gate21T2c/`; routing line added (backup `.pre-0925-*-gate21T2c`). Wednesday RULED the #1225 x #1219 declared overlap acceptable (#1219 comment-only; hunks far apart; clean merge, byte-identical lines). Rung 5 verified: the pane is creating its report dir `reports/2026-09-25-batch1218-t2c`, ctx 9%. Next tier-2: #1241 + #1242. Tier-1c kit still drafting.

**18:53 TIER-1c GATE `QA/Secuura-batch1234` LAUNCHED 08:53:44Z (%16)** over develop d9515f4a06e0 (END_TREE 1a3069159), #1234 KS-1127+1089+1135 @6320a61d8 + #1239 KS-1263 G @42c20e998 (ls-remote 18:5x). Kit 72/72 controls both ways; rollback cells in mode F and mode T (T = true + PLATFORM_DATABASE_URL, else it silently runs single-tenant). RULINGS at launch: (1) R4 (withTenant always uses the default pool; a dedicated-DB tenant may write to the wrong DB) = the gate measures and rules; (2) #1234 MERGES AFTER #1218 (its Q3 whole-runner before/after cannot run while the no-standalone rule stands); (3) mergeable null accepted after 3 reads; (4) squash bodies own key only, subjects <=92 chars. Both gates now running: %15 tier-2c, %16 tier-1c.

**19:05 TIER-2c batch1218 VERDICT (QA 09:04:09Z; report sha256 70dc4c98… 70,301 B verified on disk): 7 GO WITH FINDINGS + #1238 GO, 0 NO GO.** Completion check: heads unmoved (ls-remote), develop == BASE_GO d9515f4a0. #1233 legs 3+8 RAN (321/321; 309/343 json==yaml), leg 4 NOT RUN (401, KS-1040); the served-spec probe == merged blob. **SIGNED GO -> Seat B 26th** (#1218 first; new STOP count 28/0 + 6/0 + 60/60 after it; addendum pasted verbatim; NB findings ticketed after the merges). Gate pane %15 to close once its final line is read.

**19:16 TIER-2c batch1218 ALL EIGHT MERGED + VERIFIED by Wednesday** (PR API merged=True, base develop; `ls-remote` develop == c41e268eb935): #1218 -> 1609ecbf61e1 (FIRST), #1219 -> c0863525a142, #1223 -> 61e2bd81e8aa, #1233 -> 1f1da7f35040, #1235 -> 565e7afb4ebb, #1236 -> 2208acc0638a, #1237 -> e119781ac993, #1238 -> c41e268eb935. Day total: 18 + 8 = 26 merged, 0 deployed. New fleet STOP count in force (28/0 + 6/0 + 60/60). Tier-1c (%16) running; #1234 may now merge (#1218 is on develop). Next tier-2: #1241 + #1242.

**19:31 TIER-1c batch1234 VERDICT (QA 09:29:44Z; report sha256 a97d1547… 51,396 B verified on disk): #1234 GO WITH FINDINGS (0 Major / 3 Minor); #1239 NO GO (Major ROLLBACK-CELLS-SCHEMA, READ not run: the shipped cells insert a non-uuid target_id / NULL document_id; + G-S2-TXCLIENT, PLATFORM-URL-TRAP Minors; POOL-IDENTITY Minor -> ticket).** Heads + develop c41e268eb re-read. RULED: #1234 option (ii) the whole-runner before/after, authorised as ONE standalone run now #1218 is on develop, then merge on the signed GO; #1239 round 2 of 2 to Seat B 26th (measure the Major on its own disposable Postgres first). Pane %16 closed. FLEET ITEM: gate stack slots 2/3/4 all hold KEPT volumes and two gates raced slot 4 (the t1c gate mounted t2c's volume; migrations exit 2; read-only SELECTs only) -> no free slot for a full stack now.

**19:58 #1234 MERGED + VERIFIED** (PR API merged=True; develop == e68e2f0e837d by ls-remote). Whole-runner: round 1 (unbuilt packages/shared) 59/1 both sides, NOT merged on it; round 2 after the build 60/0 both sides; STOP count 28/0 + 6/0. Day total 27, 0 deployed. #1239 round 2 next (Seat B 26th). Next tier-2: #1241 + #1242 (kit drafting).

**20:57 TIER-2d GATE `QA/Secuura-batch1241` LAUNCHED 10:57:07Z (%18)** over develop e68e2f0e8 (END_TREE 4ee2ff4a5f43), #1241 KS-1226 item 2 @e2d0518df + #1242 KS-980 @a35569aa0 (ls-remote 20:5x). Disposable Postgres `qa-g21d-pg-ks980` (its own named volume, removed at teardown). Lead: #1241 regex may be inert on real vitest 4 output (READ, gate runs it). GO goes to Seat B 27th (%17).

**21:06 #1239 KS-1263 ROUND 2 READY (Seat B 27th, tier 1, head c8e1875c21e9 == ls-remote).** Ticket comment ee4f5108 on KS-1263 per its mail. Seat evidence: MODE T head 5/5, BASE 1/4 red on rows; G-S2 tamper 29/29 -> 1/28; MODE F 5/5 fail by name (KS-1305). Tier-1 kit gate21T1d commissioned (drafter, scratchpad). Round 2 of 2 = the cap.

**21:27 TIER-2d batch1241 VERDICT (QA 11:25:31Z; report sha256 ef04788f… 41,708 B verified on disk): #1241 NO GO (LIVE-SHAPE NULL: vitest 4.1.11 prints skipped AFTER passed; the head regex is NULL on every real summary with skips; the ticket example was a line the 09-17 gate COMPOSED), #1242 GO WITH FINDINGS (T-GUC separates).** Heads + develop re-read. SIGNED GO #1242 -> Seat B 27th; #1241 round 2 of 2 -> Seat B 27th (real captured vitest lines; a cell through :103). Asked: was the 11:08:26Z merge-tree --write-tree in the shared store its merge23 --dry? %18 closed.

**21:32 #1242 KS-980 MERGED + VERIFIED** (PR API merged=True; develop == 33ccff807eb2 by ls-remote). Day total 28 merged, 0 deployed. Seat B 27th confirmed the 11:08:26Z merge-tree was its merge23 --dry (5 loose tree objects, no ref/index/worktree touched) and has contained it. Open: #1241 fix round (Seat B 27th); #1239 tier-1 round-2 kit drafting.

**21:42 #1241 KS-1226 ROUND 2 READY (Seat B 27th, tier 2, head b4427d416592 == ls-remote; FF from e2d0518df).** Seat evidence: captured real vitest lines (5 shapes) — develop and round-1 both NULL on all, round 2 reads them; both red arms fire; the 15-leg preflight did NOT run on this push (hook design). Tier-2 kit gate21T2e commissioned (drafter, scratchpad). Round 2 of 2 = the cap. Routing will be QA/Secuura-batch1241r2.

**21:49 TIER-1d GATE `QA/Secuura-batch1239` (#1239 round 2 of 2) LAUNCHED 11:48:53Z (%19)** over develop 33ccff807eb2 (END_TREE e666fb6e08b7). Kit 90/90 both ways; disposable Postgres qa-g21T1d-pg-ks1263 with compose-shaped init + secuura_platform (the gate builds MODE T properly; the seat's MODE T may have lacked a real platform DB — READ lead). RULED: disposable not a slot; /transfer-custody route cell absence = the gate's call; no prisma generate; squash own key only.

**22:17 TIER-1d #1239 r2 VERDICT (QA 12:16:06Z; report sha256 86dbbcab… 39,941 B verified on disk): GO WITH FINDINGS** — MODE T 5/5 witnessed; BASE red reproduced on rows; MODE F loud; 0 Major; Minors C-CUSTODY-ROUTE (ticket) + POOL-IDENTITY (KS-1304). SIGNED GO -> Seat B 27th (+ residue tickets, container teardown incl. anon volume). %19 closed.

**22:18 TIER-2e GATE `QA/Secuura-batch1241r2` (#1241 round 2 of 2) LAUNCHED 12:18:43Z (%20)** over develop 33ccff807eb2 (END_TREE c0f0e7c91b2e). Kit 91/91; drafter READ-predicts NO GO (fail-only/skip-only/todo-only lines -> NULL via the second renderer); THE RULE unchanged.

**22:25 #1239 KS-1263 MERGED + VERIFIED** (PR API merged=True; develop == 6e2a00bfed57 by ls-remote). Day total 29 merged, 0 deployed. Tier-2e #1241 r2 gate still running (%20).

**22:39 TIER-2e #1241 r2 VERDICT (QA 12:38:05Z; report sha256 b6b2c0f1… 32,179 B verified on disk): NO GO AT THE CAP** — LIVE-SHAPE NULL on 3 real vitest shapes (the second renderer omits passed when 0: fail-only / skip-only / todo-only), CALLSITE NOT PINNED. Nothing ships. Seat B 27th: file the residue ticket (verbatim from the report), comment PR #1241 + KS-1226, leave the PR OPEN, then wrap. %20 closed. Round-21 queue EMPTY.

## Round 24 (lanes B 28th / L5 / L6, lock .push-lock-24)
**23:29 READY: #1243 KS-1117 + KS-1300 items 2-4 (Seat L6, TIER 2, head 0c89e2b503d9 == ls-remote).** First of the round. Batch rule: launch a tier when 4 are READY or the oldest is 60 min old (13:27Z → 14:27Z).
**23:36 READY: #1244 KS-1111 (Seat L6, tier 2, head 146b620fd by ls-remote).**
**23:54 READY: #1245 KS-1313 (Seat L6, tier 2, head 1700b5ae7 by ls-remote).** Tier-2 READY: #1243 #1244 #1245 (3).
**23:54 TIER-2 kit gate24T2a COMMISSIONED** (drafter → this seat's scratchpad `gate24T2a/`, frozen at #1243 #1244 #1245; routing QA/Secuura-batch1243; #1245 gets the mandatory piped LIVE-SHAPE).
**23:56 #1246 KS-1312 + KS-1298 (Seat B 28th) READY → TIER 3, GO sent on Wednesday's own diff read** (head 73b633700508; 3 files +15/−13; 6 unused eslint directives + 2 comment corrections; condition: eslint 0 no-var-requires at head).
**00:00 #1247 KS-1294 (Seat L5) READY → re-tiered 3 (comment-only hook; 0 non-comment lines, control 138 on #1245), GO sent** (head 5b5becd63a9c).
**00:10 READY: #1248 KS-1143 GF-2 (Seat L6, tier 2, head 2b4960172644 by ls-remote) → gate24T2a WIDENED to 4 and FROZEN** (#1243 #1244 #1245 #1248; the drafter was told via SendMessage). Seat B 28th: merge24 proven, eslint 0 no-var-requires at #1246 head (per its mail) → merging #1246.
