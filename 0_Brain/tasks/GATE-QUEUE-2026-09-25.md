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
