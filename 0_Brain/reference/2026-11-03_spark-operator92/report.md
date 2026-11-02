# Spark operator 92, 2026-11-03 08:03 to 09:12 AEDT: KS-1868, 10 passes HELD

## BLUF
- HELD (10): O92-P1 .. P11 except P2. All golden BYTE-IDENTICAL, strict=True, A6 no new red. Files: ls night | grep O92.
- Skipped: P2 (originate routes/documents.ts GET /:id outer catch). The brief was written and linted, but the builder REFUSED it (open PR 1964 lists documents.ts; file-level gate), so it was moved to skipped/ and never queued. Also, a hostile value thrown by the document read itself is turned into a TypeError by the inner `dbErr?.message?.includes` catch (line 1126) before it reaches the outer catch; that inner catch drives control flow and is a separate site.
- Skipped inside documentRepo.ts: saveDocument catch (517) and its inner FK catch (503): 503 drives control flow (owner-less retry) and a hostile value reaches 517 only through 503.
- Failed rounds: one. P11 control REFUSED 09:02:49 (builder could not read PR #1928 state: RemoteDisconnected from GitHub, class: transient network). Re-queued, CONTROL-PASS 09:06:49, model PASS 09:09:39. Also one of my own test defects caught before any round: P11 first test version never reached the CREATE TABLE statement (ensureTable's schema-privilege probe skipped the DDL); fixed and rebuilt before its control ran (queued control line removed by me, then re-queued).
- Tip: develop b85b7b6786fa at start and for every round up to P11's control; ddd770cab4aa at the end (tip_end.out; tip moved 09:0x, demo-service/state.ts only, none of my files; P11 control and model ran at ddd770cab4aa). Open PRs: start 20 PRs / 110 files (planted control services/originate 8 entries), end 23 PRs / 135 files (control 8). New at end: PR 1969 (referral db/milestone/fraud/referralService, includes the O90-P11 hunks) now lists referralService.ts, see P3.
- Spark: busy 08:19 to 09:10 with one gap-free queue except short seams (queue never empty between 08:22 and 09:10).
- Harness events: deps lock key matched the tip at every round; build_deps.sh NOT run. No "deps store lock key" failure.
- Stopped: loop92.sh (pid 87207) and holdloop92.sh (pid 87208) exited on the STOP file at 09:10:55 / 09:10:40; queue empty; no background process left.

## Never-brief list used
Every product file in held READY files of operators 83-91 (heldlist.py output: held_paths.out, 434 paths at start); every open PR file (prscan_start.out / prscan_end.out); Seat R 77th remaining raise files; accountLockout; packages/shared/**; anchoring index.ts. DEVIATION to state: the five supply files you named (documentRepo.ts, documents.ts, prism db.ts, referralService.ts, timestamping db.ts) are all in held READY paths (O65-P2, KS-1709, O83-P2/P3, O89-P1/P7, O90-P11), so the literal never-brief rule would have excluded them. I followed your supply instructions (disjoint hunks, named per pass). Checked at the tip: O89-P1 / O89-P7 (prism and timestamping db.ts pool-error and ready-hook guards) are ALREADY MERGED (PR 1966; the tip file shows them), so P4/P5 conflict with nothing; O65-P2 (documentRepo verifyDbReady) is also already at the tip.

## Held passes
| Pass | Service / file | Tier | Cells red/total | Hunks | Raise-order constraint |
|---|---|---|---|---|---|
| O92-P1 | originate src/repositories/documentRepo.ts getDocument (265), listDocuments (298), updateDocument (697) | 2 | 6/10 | 3 | none; held KS-1709 / O83-P2 / O83-P3 edit routes/documents.ts, not this file; O65-P2 hunk (137) is merged |
| O92-P3 | referral src/services/referralService.ts dbSaveReferralCode (68), dbGetCodeByString (228-229) | 2 | 4/6 | 2 | RAISE AFTER the referral PR carrying O90-P11 merges (now open PR 1969, hunks 165/177/201/213); hunks disjoint by 12+ lines |
| O92-P4 | prism src/db.ts probeDb (123-124) | 3 | 3/5 | 1 | none; O89-P1 already merged |
| O92-P5 | timestamping src/db.ts probeDb (98-99) | 3 | 3/5 | 1 | none; O89-P7 already merged |
| O92-P6 | wallet-connector src/server.ts 67, 189, 217, 301 (POST/GET/DELETE session, GET sessions) | 3 | 8/12 | 4 | none |
| O92-P7 | staking src/routes/stake.ts verifyDbReady (147-148) | 3 | 3/5 | 1 | none |
| O92-P8 | timestamping src/index.ts lookup catches 777, 789, 801 | 2 | 6/9 | 3 | none; same file as P11 (hunks 650 lines apart) |
| O92-P9 | referral src/routes/leaderboard.ts buildLeaderboard (285-286) | 3 | 3/5 | 1 | none |
| O92-P10 | transfer src/index.ts loadFromDb (326-327) | 3 | 3/5 | 1 | none |
| O92-P11 | timestamping src/index.ts ensureTable (119-120) | 3 | 3/5 | 1 | none; same file as P8 |

hold_ready lines (verbatim, from hold_pN.log):
- P1: golden: BYTE-IDENTICAL; touched=2 product_plus=25 product_minus=4 red=6/10 green=10/10 suite=2349->2359 strict=True
- P3: golden: BYTE-IDENTICAL; touched=2 product_plus=18 product_minus=2 red=4/6 green=6/6 suite=36->42 strict=True
- P4: golden: BYTE-IDENTICAL; touched=2 product_plus=8 product_minus=1 red=3/5 green=5/5 suite=39->44 strict=True
- P5: golden: BYTE-IDENTICAL; touched=2 product_plus=8 product_minus=1 red=3/5 green=5/5 suite=105->110 strict=True
- P6: golden: BYTE-IDENTICAL; touched=2 product_plus=32 product_minus=4 red=8/12 green=12/12 suite=76->88 strict=True
- P7: golden: BYTE-IDENTICAL; touched=2 product_plus=8 product_minus=1 red=3/5 green=5/5 suite=93->98 strict=True
- P8: golden: BYTE-IDENTICAL; touched=2 product_plus=24 product_minus=3 red=6/9 green=9/9 suite=105->114 strict=True
- P9: golden: BYTE-IDENTICAL; touched=2 product_plus=8 product_minus=1 red=3/5 green=5/5 suite=36->41 strict=True
- P10: golden: BYTE-IDENTICAL; touched=2 product_plus=8 product_minus=1 red=3/5 green=5/5 suite=139->144 strict=True
- P11: golden: BYTE-IDENTICAL; touched=2 product_plus=8 product_minus=1 red=3/5 green=5/5 suite=105->110 strict=True

Each brief (night/briefs/ks_1868_o92_pN_*/KS-1868.md) carries callers, the ordinary-Error-vs-hostile comparison and the BEHAVIOUR CHANGE text for the PR. Notes for raise seats:
- P1: getDocument's catch also moves the `err?.message?.includes('invalid input syntax for type uuid')` test into the guard `try` (a throw there counts as not a uuid refusal and is logged). Original value is rethrown. saveDocument 503/517 deliberately untouched.
- P3: generateCode's custom-code uniqueness check treats a failed lookup as "code free", the same as for an ordinary Error today.
- P4/P5: the guard variable is `string | undefined` (return type `error?: string`); a `null` message is now reported as absent, said in the BEHAVIOUR CHANGE text. Today a hostile value makes probeDb reject, which also ENDS the background retry chain (scheduleRetry never re-armed).
- P6/P8/P10/P11: the real index.ts / server.ts runs in the test (listens on an ephemeral port at import); P8/P11 share the file with each other only.
- P2 (skipped) test and brief kept in skipped/ in this workdir for a later round once PR 1964 merges.

## Round log (done.md row times, AEDT)
- 08:22:09 P1 control PASS; 08:30:51 P1 model PASS 7/7
- 08:32:08 P3 control; 08:40:02 P3 model. 08:33:15 P4 control; 08:42:54 P4 model. 08:34:22 P5 control; 08:46:05 P5 model.
- 08:35:39 P6 control; 08:51:00 P6 model. 08:36:49 P7 control; 08:53:25 P7 model. 08:38:01 P8 control; 08:57:36 P8 model.
- 08:41:06 P9 control; 09:00:08 P9 model. 08:44:08 P10 control; 09:02:19 P10 model.
- 09:02:49 P11 control REFUSED (PR state read failed, transient); 09:06:49 P11 control PASS; 09:09:39 P11 model PASS.
- Every model round: one attempt, no rebrief used. Every control PASS first time (harness proven by the P1 control, so the later controls were queued together).

## UNMEASURED
- tsc and eslint on the new test files outside the checker; real Postgres / Redis / Express boot beyond the stand-ins; whether any live path throws such a value (KS-1868 says the same).
- State of tickets/PRs beyond the PR list (live lanes not checked). PR 1969 hunks vs P3 were compared by hunk headers only.
