# QA Gate 136 verdict (DELTA, round 2 of 2): Secuura/Distributed_Secuura PR 1952 (KS-1950, governance participant writes), TIER 1

## BLUF
**GO WITH NOTES. There is no FIX-BEFORE-MERGE item.** G134-F1 is closed, and so are the F2 and F3 recommendations.

**How I measured it.** I re-ran my own real-PG loop on the fix head `24d7296c`:
- the REAL governance router, behind the REAL `authenticate()` and `errorHandler`;
- the REAL `db.ts` pool, against REAL PostgreSQL 15.19 (`gate136-pg`, now removed);
- the app role `gate_app` (NOSUPERUSER, NOBYPASSRLS), with `users` under migration 039's FORCE RLS;
- a real second connection for interleaves;
- 300 rounds per race.

Results:
- **Two concurrent FIRST self-registrations of one user: 201|201 in 300/300 rounds, with one correct row in 300/300.** Round-1 head `7fe1d809` on the same harness: 29/300 false 409 (15 + 14). develop `8150eeb3`: 26/300 x 500.
- **Self-register racing propose: 300/300 coherent** (201 | 400 min-stake). Round 1 had 49/300 with a 409. develop had 31 x 500 and 13 x 409.
- **A wallet held under ANOTHER id is still 409 with nothing of the request written,** on all of these:
  - Q3b, Q3b2 and Q3b3 (insert, auto-register and refresh);
  - G3 (wallet 23505 with no own row);
  - G7 (another id takes the wallet before propose's pre-check).
- **F3 is as built:** a 23505 under the pkey name, or any other name, stays **500** with nothing written (G4, G5 on real PG; D3e in the suite).
- **The delta touches only what it should:** 4 files, +98/-21, only governanceService.ts (+12/-4), the KS-1950 test file (+70/-1) and the fragment pair (8/8 each). The product hunk is exactly gate 134's FA + FAC code.
- **The round-1 headline still holds.** At head the admin change survives all 3 paths: 20/21 Q1 cells, and the 21st is selfreg x wallet, which is by design (G134-F4). At base all 21 are reverted. Every non-delta probe cell is byte-identical between round 1 and head, apart from one random UUID.
- **Gate 129's 28 KS-1942 cells** give the same status at base, round 1 and head.
- **Re-measure:**
  - suite 282/282 (16 files);
  - red-first at the round-1 product: exactly D3c and D3d fail, by assertion;
  - tsc including tests 0, eslint 0, docs-fragments clean, each with a planted control that fired;
  - check:openapi rc 0, and a planted drift gives rc 1.
- **Mutants on the fix lines: 4/6 killed by assertion, all sha256-restored.**
  - K2 survives the suite. It is killed on real PG by my cell G2. That makes it a test gap on correct code (G136-F1, recommended).
  - K6 is equivalent (G136-F2).
- **merge-tree onto develop as it is NOW (`9d7e871f`) is clean.** develop moved during the gate (G136-F3). The PR head did not.

## 1. Heads + diffstat
**START** (logs/head_start.log, 2026-11-02T15:54:39Z):
- PR 1952 `24d7296c47602b8928476bb952e2da6baddb188f`;
- develop `8150eeb3802bd9cfe5242ffbc49278c1a3739a84`;
- 1953 `ea6d924eb5de`.

All match the brief.

**END** (logs/head_end.log 16:05:34Z, and logs/head_end2.log 16:06:33Z after teardown):
- **PR 1952 is unchanged at `24d7296c`.**
- **develop MOVED to `9d7e871fb771`**, one commit: "Refs KS-1868: nft-certificate catches coerce an unreadable thrown message...". It is 6 paths, all nft-certificate plus its 2 fragments. 0 are shared with this PR, and 0 are openapi inputs. See G136-F3.
- 1953 is unchanged.

**Delta, 7fe1d809..24d7296c** (logs/delta_stat.txt, logs/delta_log.txt):
- It is one commit, `24d7296c`, whose parent is `7fe1d809`, so a fast-forward.
- **4 files, +98/-21, as claimed:**
  - the ks1950 test +70/-1;
  - governanceService.ts +12/-4;
  - the cheat and flow fragments, 8/8 each.
- No other path.

**Three-dot onto the new develop:** 8 files, +980/-26.
- That equals round 1's +901/-24 plus this delta: the ks1950 test 625 -> 694, and governanceService +111/-20 -> +121/-22.
- The other 6 files have the same numstat as round 1.

**PR body: NOT read.** There is no Secuura gh auth, and the unauthenticated API answers 404 (logs/pr_api_unauth.json). I used F 24th's READY FOR DELTA GATE mail (evidence/ready_batch.txt, lines 24-81).

**Host:** Node v26.8.1 only. **Nothing here is measured on Node 24.**

## 2. The hunks (logs/delta_product.diff)
**`dbInsertParticipantIfAbsent`'s catch.** This line:

`- if (isWalletHeldError(err)) throw new ConflictError(WALLET_HELD_MESSAGE);`

is replaced by:

`+ const own = await dbGetParticipant(p.id); if (own && own.walletAddress === p.walletAddress) return own; throw new ConflictError(WALLET_HELD_MESSAGE);`

That is gate 134's exact code, with a comment.
- What it does NOT change: the SQL, `isWalletHeldError` (it still requires constraint === `svc_governance_participants_wallet_address_key`), the non-wallet branch (log `readableReason`, rethrow, so 500), and the 0-rows re-read and 503.
- A failed re-read throws `dbGetParticipant`'s existing 503. That is the KS-1940 semantics.

**`createProposal` auto-register.** This:

`- if (await dbGetParticipantByAddress(linked)) 409; proposer = await dbInsertParticipantIfAbsent(...)`

is replaced by:

`+ const holder = ...; if (holder && holder.id !== proposerId) 409; proposer = holder ?? (await dbInsertParticipantIfAbsent(...))`

That is gate 134's FAC.
- The 409 text is unchanged.
- The min-stake check that follows now applies to the caller's own stored row (G8: an unstaked own row gives 400, not a false 409).

**Tests:**
- a `throwOn` stand-in hook, with an afterEach assertion that a planted error fired;
- D3c (RED, F1), D3d (RED, F2) and D3e (control, F3).

**New log lines in the delta: none.** Kam's ks1346 rule is unaffected. G134-F7 still holds.

## 3. The behaviour question: real router, real PG, real second connection (scripts/probe.test.ts via scripts/probe.sh; logs/probe_{head,r1,base}.jsonl and probe_table_*.txt)
The probe is gate 134's, ported. One thing is added: a planted fault can run an async `pre` on the second connection before rejecting. G1..G8 and Q3k are new cells. The read vs run split: everything below was RUN.

| cell | develop 8150eeb3 | round 1 7fe1d809 | **fix head 24d7296c** |
|---|---|---|---|
| Q3d selfreg x2 concurrent, same user (300) | 274 ok, **26 x 500** | 271 ok, **29 x false 409** | **300/300 201\|201; row correct 300/300; 0 error logs** |
| Q3e selfreg x propose concurrent (300) | 256 ok, 31 x 500, 13 x 409 | 251 ok, **49 x 409** | **300/300 201 \| 400 min-stake** |
| G1 own row (U1,W1) lands, then the insert raises the WALLET 23505 | (UPSERT, the fault never fired) | **409 (false)** | **201, reports the landed row (did "landed"), nothing more written** |
| G2 own row lands holding ANOTHER wallet, then the wallet 23505 | n/a | 409 | **409**, own row untouched |
| G3 wallet 23505 with no own row | n/a | 409 | **409, nothing written** |
| G4 23505 under the pkey name (self-register) | n/a | 500 | **500, nothing written, `error DB insert participant failed {participantId,error}`** |
| G5 23505 under another name (propose auto-register) | n/a | 500 | **500, nothing written, no proposal** |
| G6 U1's OWN staked row lands before propose's wallet pre-check | 409 | **409 (false)** | **201, pc 0->1 on that row, no insert issued** |
| G7 ANOTHER id takes W1 before propose's wallet pre-check | 409 | 409 | **409, no write** |
| G8 U1's OWN unstaked row lands before the pre-check | 409 | 409 | **400 min-stake, row kept** |
| Q3b / Q3b2 / Q3b3, another id takes the wallet before insert / auto-insert / refresh | 500 / 500 / 500 | 409 / 409 / 409 | **409 / 409 / 409, the other row intact, nothing of the request written** |
| Q3k self-register x another id inserting W1 on the 2nd connection (300) | 409 300/300 | 409 300/300 | **409 300/300, coherent 300/300** (see G136-F4) |

## 4. "Nothing ELSE changed"
**The headline** (Q1, 3 paths x 7 admin changes + controls):
- At head the change survives in 20/21 cells. The one exception is selfreg x wallet, which D-2 resets to the linked wallet by design (G134-F4).
- At develop all 21 are reverted.
- Counters go up by exactly 1.

**Every non-delta probe cell** (Q1, D4, Q3a-c3, a0-v3; normalised timestamps, logs/probe_diff_r1_head.txt) is **identical between round 1 and the fix head**. The only diff is D4b's random new UUID.

**Gate 129's 28 KS-1942 cells** (a0-a6, b1/b2/b3/b5/b7/b9, c1-c6, d1/d3, f1-f4, v1-v3) give the same status at base, round 1 and head.

**Suite** (scripts/runs.sh, logs/runs.log, summ output):
- **head 282/282, 16 suites.**
- The round-1 product with the head tests: 280/282. **Exactly D3c and D3d fail, both by assertion.**
- The develop product with the 3 changed head test files: 12 failed, all by assertion. These are the 8 round-1 RED cells, plus D3c and D3d, plus ks1942's 2 declared write-shape cells (R3c, QB1). D3e passes there, as a control should.

**tsc** (logs/tsc_run.log):
- service tsconfig rc 0;
- including tests: head 0 errors, the round-1 product 0;
- a planted unused const gives 1 error, rc 2, and was restored (sha OK).

**eslint** on the 5 governance .ts files: rc 0. The planted file gives rc 1 (1 error, 1 warning) and was moved to logs/_quarantine.

**docs-fragments:**
- clean rc 0;
- a planted unclosed `<div>` in the flow fragment and in the cheat fragment each give rc 1, naming the file;
- both were restored by sha, and the check is rc 0 after.
- The delta's fragment edits are the new figures (15 -> 18 cells, 279 -> 282, the real-PG race now listed as run).

## 5. Mutants on the fix lines (scripts/mutants.py; product only, tests untouched, anchors asserted unique, the whole governance suite per mutant; "ALL RESTORED" both runs)
| mutant | result |
|---|---|
| K1 F1 undone: the re-read removed (any wallet 23505 is a 409) | **KILLED**: ks1950 D3c (assertion) |
| K2 F1 re-read returns ANY own row (wallet equality dropped) | **SURVIVED the suite**. Killed on real PG by G2 (201 instead of 409, logs/probe_table_mutK2.txt). See G136-F1 |
| K3 F1 equality inverted | **KILLED**: D3c |
| K4 F3: any 23505 is the wallet one (gate 134's surviving M7b) | **KILLED**: D3e |
| K5 F2 undone: any holder is a 409 | **KILLED**: D3d |
| K6 F2 holder ignored, always insert-if-absent | SURVIVED. **Equivalent**: ON CONFLICT (id) DO NOTHING plus the re-read returns the same row, and G6 is still 201 on real PG under K6 (logs/probe_table_mutK6.txt). See G136-F2 |

The first K6 form did not compile (TS18048; logs/mut_K6_run1_did_not_compile.log). It was rewritten with `void holder` and re-run (logs/mutants_table_K6_run2.log).

## 6. merge-tree (scripts/merge_tree.sh, logs/merge_tree.log)
**Onto develop as it is NOW, `9d7e871f`:**
- It is not an ancestor; the merge-base is `8150eeb3`.
- `merge-tree --write-tree` gives **rc 0**, tree `50b43cf9`.
- The merged tree differs from develop in **exactly the PR's 8 paths**, and those paths' blobs equal the PR head's.

**Pair with open PR 1953 (`ea6d924e`):**
- merge-tree rc 0 (tree `b33aa0fb`).
- The one shared path is `Blockchain/Dev/docs/openapi/secuura-api.yaml`.

**check:openapi at this head** (TMPDIR=/tmp/g136; logs/check_openapi_head.log): **rc 0**. "CHECK PASS: on-disk YAML matches generated", and the spec examples are OK (422 blocks).
- The planted drift control (one word in the register 409 text, yaml line 22513) gives **rc 1, "CHECK FAIL"**. It was restored, sha OK.
- develop's move touches no openapi input.

**The second-merger rule** ("whichever of 1952 / 1953 merges SECOND re-runs check:openapi after merging develop in"):
- F 24th's mail states it as Condition 4, and says "The PR body says so too".
- **I could not read the body to confirm it** (G136-F5).

## 7. Kam's ks1346 logging rule
The delta adds no log line. The four round-1 lines still log `readableReason(err)` plus ids only. **Complies.**

## FINDINGS / Notes for the PR body
- **G136-F1 (RECOMMENDED; not FIX-BEFORE-MERGE; a test gap, not a defect).** Mutant K2 drops `own.walletAddress === p.walletAddress` from the F1 re-read, and it survives the suite.
  - The code as built is correct. On real PG, G2 (the own row holds another wallet, then a wallet 23505) answers 409 at head and 201 under K2.
  - **Add one stand-in cell next to D3c:** the hook seeds U_A's row with a DIFFERENT wallet, and throwOn raises the wallet 23505 on the INSERT. Expect 409 `This wallet is registered to another governance participant`, U_A's row unchanged, and no row for the wallet.
  - **It is not the F1 class, and the fix round did not introduce it.** It is an unpinned branch of the correct fix, and it can be done in a follow-up.
- **G136-F2 (INFO).** Mutant K6 (F2's `holder ??` replaced by an unconditional insert-if-absent) is equivalent: DO NOTHING plus the re-read returns the same row, at the cost of one extra statement. No action.
- **G136-F3 (INFO).** develop moved during the gate, `8150eeb3` -> `9d7e871f` (KS-1868 nft-certificate, 6 paths, none shared with this PR, no openapi input). The PR head did not move.
  - merge-tree onto the new develop is clean, and the result is develop plus exactly the PR's 8 paths.
  - The branch no longer contains develop's tip. If the merge policy needs an up-to-date branch, merge develop in; there is no conflict.
- **G136-F4 (INFO).** In Q3k (self-register racing another id's raw INSERT of the same wallet), the raw INSERT won all 300/300 rounds because of HTTP latency. So it measured the "other id first" order, and the response was 409, coherent, in 300/300.
  - The "other id takes the wallet between the check and the write" order is covered deterministically by Q3b, Q3b2, Q3b3, G3 and G7. All give 409 with nothing written.
- **G136-F5 (INFO).** The PR body was not read (no Secuura auth). That it carries the second-merger check:openapi rule rests on F 24th's READY mail only. Wednesday should confirm it in the body before relaying GO.
- The carried notes are unchanged: G134-F4 (D-2 owns wallet and did), G134-F5 (row deleted mid-request; KS-1951 vote power), G134-F6 and G134-F7.

**Cap rule:** no new FIX-BEFORE-MERGE item. G134-F1's instances are closed on real PG (Q3d 300/300, Q3e 300/300, G1, G6). The fix round introduced no defect: every non-delta cell is identical to round 1.

## 8. NOT TESTED
- The PR body (no auth).
- Node 24.
- A booted service, the gateway, the four platform suites, CI, and the author's pre-push legs (quoted only).
- The SQL-only `sqlrace.js` mechanism was not re-run. It is PostgreSQL behaviour, unchanged by this delta, and gate 134 measured it. The route-level Q3d/Q3e loops stand in for it.
- A true interleave of the other-id wallet race at the moment of the INSERT (see G136-F4). It is covered only by the deterministic cells.
- The 1952 x 1953 regeneration after both merge (the second-merger rule covers it).
- The base whole-suite count was not re-run. Gate 134 measured 264/264; I ran only the 3 changed files on the develop product.

## Processes and containers
- I started `gate136-pg` (postgres:15-alpine, 127.0.0.1:55136). It was **removed** with `docker rm -f` (rc 0), and `docker ps -a --filter name=gate136` shows 0 rows.
- I ran one background task, `npm ci --ignore-scripts` + the shared build. It completed rc 0. Every jest, probe and mutant run was in the foreground.
- After teardown, `ps` shows 0 gate136 or jest processes. **Nothing I started is still running.**
- The jest and openapi TMPDIR `/tmp/g136` (17M, my own scratch) was deleted by literal path.
- Probe copies and the planted eslint file are in logs/_quarantine/.
- The clone's `git status --short` prints 0 lines, and the push URL is `no_push_qa_gate`.
- I wrote nothing outside this workdir, apart from the deleted /tmp/g136.
