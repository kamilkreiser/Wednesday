# QA Gate 134 verdict: Secuura/Distributed_Secuura PR 1952 (KS-1950, stale whole-row participant writes no longer revert an admin's change), TIER 1

## BLUF
**NO GO as it stands, because of one FIX-BEFORE-MERGE (G134-F1).** It is a 5-line change that I measured. Once it lands with a covering cell, the PR is **GO WITH NOTES**. Everything else re-measures clean.

**How I ran it.** I ran the REAL governance router behind the REAL shared `authenticate()` (RS256 key generated in the probe) and the REAL `errorHandler`. Under it was the REAL `db.ts`, against a **REAL PostgreSQL 15.19** (throwaway container `gate134-pg`, now removed). The setup:
- The governance tables are verbatim from `docker/init/04-sprint2-service-tables.sql`, including `wallet_address UNIQUE`.
- `users` has migration 039's `tenant_isolation` policy with ENABLE + FORCE RLS.
- The app connects as `gate_app` (NOSUPERUSER, NOBYPASSRLS).
- Admin changes came from a **REAL second connection** (`gate_app`, its own backend pid), or from the REAL admin route over HTTP. They ran just before each path's first participant write, which is after that path's reads.
- The one stub is a wrapper on `pg.Client.prototype.query`. Its only job is to run that hook first.

**(1) The headline holds at head and is reverted at base.** These are measured cells.
- **createProposal and castVote** were each tested against 7 admin changes: de-stake, DRep off, committee off, did, wallet, re-stake up, and the real admin route. **Every change survives at head (7/7 and 7/7).** proposals_created and votes_cast go up by **exactly 1**.
- **At base every one of those 14 is reverted.** The stale UPSERT wrote the read row back.
- **self-register at head:** stake, DRep, committee, did and re-stake survive, and so does the admin route's change. The 201 reports the stored row (RETURNING): after a de-stake it reports stake 0.
  - The wallet column is the exception. It is reset to the caller's linked wallet, which D-2 owns by design (G134-F4).
  - At base, all of them are reverted.

**(2) D-1..D-6 are built as approved.** There are exactly **5 participant write statements**, found by grep and by runtime capture, with a positive control. No path writes a column it does not own.

**(3) The edges:**
- The deterministic wallet race gives 409 with nothing written, on all 3 paths. Base gave 500.
- A row gone at the bump gives a warn, the request still succeeds, and nothing is re-created. Base re-INSERTed the stale row.
- A row created mid-request gives DO NOTHING, then a re-read: the admin's staked row is kept and reported.
- **But two concurrent first self-registrations of the SAME user answer a FALSE 409 in 20 of 150 rounds** ("This wallet is registered to another governance participant", although it is the caller's own wallet and id). Base answered 500 in 13 of 150. The cause is a real PostgreSQL behaviour, not the code's logic: `ON CONFLICT (id)` makes only the pkey the arbiter, so the non-arbiter UNIQUE(wallet_address) raises 23505 in the race. Raw SQL on 2 connections, 2000 rounds: **507 x 23505** with the PR's form, against **0** with the untargeted form (G134-F1).

**(4) The KS-1942 property holds:** all 28 of gate 129's D1a/D2a/D3a cells give the same status at base and head.

**(5) OpenAPI:** check:openapi rc 0, and both 409s are present.

**Re-measure:**
- Red-first at base: 10 failures, all by assertion. That is 8 RED cells in the new file (0 label mismatches) plus 2 declared changed cells in ks1942. Green at head: 82/82.
- Suite: **264/264 (15 files) -> 279/279 (16)**.
- tsc including tests: 0 -> 0.
- eslint: 0.
- docs-fragments: clean, and both planted defects were caught.
- **Mutants: 16/17 killed by assertion.** M7b survived. It is equivalent on today's schema (G134-F3).
- merge-tree onto 8150eeb3 is clean. develop is an ancestor of the head, the merged tree equals the head tree, and exactly 8 paths change.

## Heads
- START, logs/head_start.log (2026-11-02T15:02:22Z): `refs/pull/1952/head` = `7fe1d809936440ac8049a994a11edd8d4d90dee9`, and develop = `8150eeb3802bd9cfe5242ffbc49278c1a3739a84`. Both match Wednesday's read. The merge-base is `8150eeb3`, because the author merged develop in. There is one product commit, `fbff5877`, plus two develop merge-ins (`8f001e04`, `7fe1d809`).
- END, logs/head_end.log (15:15:11Z): **both unchanged**, and the clone's `git status` shows 0 lines.
- Diffstat, three-dot (logs/diffstat.log): **8 files, +901/-24**, as claimed:
  - governanceService.ts +111/-20;
  - governance.openapi.ts +5/-1;
  - secuura-api.yaml +8/-1;
  - the new ks1950 test +625;
  - ks1942 test +56/-2 (harness + 2 write-shape assertions);
  - ks1940 test +50/-0 (harness only);
  - the fragment pair, flow +24 and cheat +22.
- No db.ts, routes, SQL, migration, shared or package path is touched.
- **PR body not read** (no Secuura gh auth). I used the READY mail in evidence/ready_f24_pr1952.txt.
- Host: Node v26.8.1 only, so **nothing here is measured on Node 24**. load1 was 3.4-6 throughout. Jest ran with `--maxWorkers=2`, and the probe and mutants ran one run at a time.

## FINDINGS
- **G134-F1 (FIX-BEFORE-MERGE; measured on real PG)** Concurrent first registrations of the SAME user can answer a false 409.
  - **The cause.** `dbInsertParticipantIfAbsent` uses `INSERT ... ON CONFLICT (id) DO NOTHING`. With a conflict target, only the pkey is the arbiter. When two first registrations race, both pass the arbiter pre-check. The loser's insert into the NON-arbiter `svc_governance_participants_wallet_address_key` then waits for the winner and raises 23505. `isWalletHeldError` maps that to `ConflictError(WALLET_HELD_MESSAGE)`. The approved D-3 ("0 rows -> re-read and carry on") never runs.
  - Route race, 150 rounds (logs/probe_head.jsonl, Q3d): **201|201 x130, 409|201 x10, 201|409 x10**. The stored row was correct in every round (150/150).
  - selfreg racing propose, Q3e: 26/150 rounds include a 409.
  - Base, same cells: 500 in 13/150 (Q3d). So no data is harmed and the success rate is no worse. But the PR turns an honest 500 into an affirmatively false 409, under text this PR adds to the OpenAPI contract, and it does not meet D-3 or commission (3) "both get a coherent answer".
  - Mechanism without app code (scripts/sqlrace.js, logs/sqlrace.log), 2 gate_app connections, 2000 rounds each:
    - the PR's form: 1493 inserted+nothing, **507 x 23505 on the wallet key**;
    - untargeted `ON CONFLICT DO NOTHING`: 2000/2000, 0 errors.
  - The author's stand-in could not show this, because it checks `t.has(id)` before the wallet. That is the non-concurrent order, and the READY mail says the races were "proved on the stand-in" only.
  - **Exact fix, which stays inside the approved D-3/D-3b SQL.** In `dbInsertParticipantIfAbsent`'s catch, replace `if (isWalletHeldError(err)) throw new ConflictError(WALLET_HELD_MESSAGE);` with:
    ```ts
    if (isWalletHeldError(err)) {
      // UNIQUE(wallet_address) is not this INSERT's arbiter: a concurrent first registration of the SAME id
      // and wallet surfaces here instead of as DO NOTHING, so re-read by id first.
      const own = await dbGetParticipant(p.id);
      if (own && own.walletAddress === p.walletAddress) return own;
      throw new ConflictError(WALLET_HELD_MESSAGE);
    }
    ```
    Measured as gate variant FA (logs/prod/fix/, logs/probe_fixFA.jsonl):
    - Q3d gives **201|201 in 300/300 rounds**.
    - Q3b, Q3b2 and Q3b3 still give 409 with nothing written.
    - Every other probe cell is identical to head.
    - The governance suite is 279/279 (logs/fixFA_whole.json).
  - **Add a cell:** the stand-in throws the wallet 23505 on the INSERT while a row with the SAME id and wallet exists. Expect 201, that row reported, and no second write.
  - The alternative is the untargeted `ON CONFLICT DO NOTHING`, then on 0 rows a re-read by id, and if that finds nothing, 409. Note that today's 0-rows branch answers 503 when the re-read finds nothing, so that branch would have to change too.
- **G134-F2 (RECOMMENDED; pre-existing since KS-1942; measured)** createProposal's auto-register pre-check `if (await dbGetParticipantByAddress(linked)) 409` also gives a false 409 when the caller's OWN row appears between its by-id read and that pre-check, which happens when it races the caller's self-register.
  - Measured: 3/150 at base, and 3/300 under variant FA. It is part of head's Q3e count.
  - Fix, 3 lines (variant FAC, logs/fix_FAC.diff): `const holder = await dbGetParticipantByAddress(linked); if (holder && holder.id !== proposerId) throw ...; proposer = holder ?? (await dbInsertParticipantIfAbsent(...));`.
  - Under FAC, Q3e gives 300/300 coherent and the suite is 279/279. Fold it into F1's fix or file it as a follow-up.
- **G134-F3 (RECOMMENDED; surviving mutant M7b)** `isWalletHeldError` ignoring the constraint name (any 23505 -> 409) survives the suite.
  - It is equivalent on today's schema: these statements can only raise 23505 on the wallet key, because the pkey is the INSERT's arbiter and the UPDATE does not change the id.
  - Add one cell where the stand-in throws 23505 with another constraint name, and expect 500 (not 409), so the name check is pinned.
- **G134-F4 (INFO; measured; by design)** D-2 makes wallet_address and did columns owned by self-register.
  - An admin change to the row's wallet made mid-request is reset to the caller's linked wallet (Q1 selfreg x wallet).
  - A body `did` overrides an admin's did set mid-request (Q1 selfregDid x did).
  - An omitted did keeps the admin's did, through COALESCE (Q1 selfreg x did).
  - Stake, tier, vote power, DRep and committee are never written by self-register.
- **G134-F5 (INFO; measured)** Two more edges: a row deleted mid-request, and a failure after the save.
  - A row deleted between self-register's read and its refresh: the refresh returns 0 rows, the path inserts a fresh UNSTAKED row, and the 201 reports it (Q3c3). Base re-saved the stale staked row.
  - A counter-bump failure after the proposal or vote is saved still answers 500 with the save landed. That ordering is pre-existing, and D-5 accepts it (no transaction).
  - castVote still weighs the vote at the power read at the start. That is KS-1951 territory, and the READY mail declares it.
- **G134-F6 (INFO; read)** D-1 is built as one helper, `dbBumpParticipantCounter(id, 'proposals_created' | 'votes_cast')`, over two fixed SQL strings, rather than as the two names in the design. The SQL is exactly as approved: counter + 1 and last_active_at, with a warn on 0 rows.
- **G134-F7 (INFO; Kam's ks1346 rule: complies)** The PR adds four new log lines:
  - `error 'DB bump participant counter failed' {participantId, counter, error}`;
  - `warn 'Participant row not found at counter bump' {participantId, counter}`;
  - `error 'DB refresh participant failed' {participantId, error}`;
  - `error 'DB insert participant failed' {participantId, error}`.
  - In each, `error` is `readableReason(err)`. That is the message text, `String(err)`, or the constant `'unreadable thrown value'` when reading the error throws. It is the same pattern gate 129 accepted (G129-F6).
  - None logs a thrown object, its fields, or a request body. The 409 paths log nothing.
- **G134-F8 (INFO)** The PR body is not read. The 409 text the PR documents is exactly the runtime's.

## Q1. The headline: real router, real PG, real second connection (scripts/probe.test.ts via scripts/probe.sh; logs/probe_{base,head}.jsonl, logs/probe_table_{base,head}.txt)
The seed for every cell was reset each time:
- U2 is linked to W2, with a row at 50000 / whale / 75000 / DRep / committee / did, proposals_created 2, votes_cast 3.
- P1 is an active proposal.
- Hooks fired before the first participant write. At head that is BUMP pc, BUMP vc or REFRESH. At base it is the UPSERT. The `hookFiredBefore` field records which.

| path x admin change | base | head |
|---|---|---|
| propose x destake / drep / committee / did / wallet / restake / admin route | 201; **every change REVERTED**, pc 2->3 | 201; **every change SURVIVES**, pc 2->3 exactly |
| vote x the same 7 | 200; every change REVERTED, vc 3->4 | 200; every change SURVIVES, vc 3->4 exactly |
| selfreg x destake / drep / committee / did / restake / admin route | 201; REVERTED, and the 201 shows the stale row | 201; SURVIVES, and the 201 reports the stored row (RETURNING) |
| selfreg x wallet | reverted | reset to the linked wallet (D-2 owns it, G134-F4) |
| controls, no change (propose, vote, selfreg, selfreg+did) | 201/200/201/201 | the same; counters +1 and did written |

## Q2. D-1..D-6 as built, and every write to svc_governance_participants
- **Method 1** (logs/grep_table_writes.log): `git grep -i -E "(insert into|update|delete from) +svc_governance_participants"`, tests excluded.
  - Head: **5 hits, all in governanceService.ts**: :182 the admin UPSERT, :206 and :207 the bumps, :256 the refresh, :274 insert-if-absent. A sixth hit is a fragment's prose.
  - Base: 1 hit (:180). That is the positive control.
  - Callers (logs/grep_writers_head.log): `dbSaveParticipant` only at :600 (registerParticipant, the admin route); refresh :659; insert-if-absent :661 and :745; bump :796 and :942.
  - The other table mentions are DDL (3 files) and a doc.
- **Method 2, runtime** (logs/runtime_writes.log). Every participant write the app issued across all probe cells:
  - head: exactly those 5 statements;
  - base: the one UPSERT, 51 times.
- **Columns per statement:**
  - D-1 bump: the counter + 1 and last_active_at.
  - D-2 refresh: wallet_address, `did = COALESCE($3, did)` and last_active_at, then `RETURNING *`. The 201 reports that row.
  - D-3 insert-if-absent: all columns, only for a new id. The values are unstaked (0 / basic / 0 / false / false / 0 / 0). On 0 rows it re-reads, and it writes nothing over the existing row (Q3a: an admin's staked row made mid-request is kept and reported, 201 at stake 5000; base overwrote it to 0).
  - D-3b: wallet 23505 gives the existing 409 text (Q3b on self-register, Q3b2 on propose, Q3b3 on refresh; base gave 500 on all three).
  - D-4: the admin UPSERT's conflict SET no longer has the counters (D4: a bump to 9/9 landing mid-admin-write is kept at head; base reverted it to 2/3). It keeps wallet, did, stake, tier, vote_power, drep, committee and last_active_at.
  - D-5: separate statements, no BEGIN in these paths.
  - D-6: see Q5.
- No path writes a column it does not own, apart from the admin route, which owns stake and roles by KS-1942.

## Q3. Concurrency edges
- Q3a and Q3a2: a row with the caller's id appears before the insert. Head: DO NOTHING, then a re-read, and the stored row is used (propose: 201 with pc +1 on the admin-staked row). Base: overwritten.
- Q3b, Q3b2 and Q3b3: another id takes the wallet after the 409 check. Head: **409, nothing of this request written, the other row intact**. Base: 500.
- Q3c and Q3c2: the row is deleted before the bump. Head: **201/200, `warn Participant row not found at counter bump {participantId, counter}`, no row re-created**. Base: the stale row was re-INSERTed.
- Q3c3: see G134-F5.
- Q3d and Q3e: concurrent first registrations. See **G134-F1** and **G134-F2**.

## Q4. KS-1942's property (gate 129 cells re-run, logs/probe_table_*.txt)
These cells give the same status and the same rows at base and head:
- a0-a6 (a body stake, flag or extras gets 403, or 201 at 0 / basic / 0);
- b1, b2, b3, b5, b7 and b9 (another wallet, no wallet, cross-tenant, Unicode role: 403; the control gets 201);
- c1-c6 (c4 gets 409; c5 re-binds a legacy row, now through the refresh);
- d1 and d3 (admin applied);
- f1-f4 (D1a: an unstaked proposer gets 400);
- v1-v3 (v3: body `votePower`/`stakedAmount` ignored, vc +1).

Nothing about stake or vote power is caller-chosen. Unhandled rejections: 0 at base and 0 at head.

## Q5. OpenAPI (logs/check_openapi_head.log, logs/check_openapi_planted.log)
- `npm --prefix Blockchain/Dev run check:openapi`: **rc 0**, "CHECK PASS: on-disk YAML matches generated", and the spec examples are OK.
- The planted drift control (one word changed in the new yaml 409 text): rc 1, "CHECK FAIL". The yaml was restored and its sha checked.
- In the yaml, `/api/governance/participants/register` has a new `"409"`: "The linked wallet is registered to another governance participant". `/api/governance/proposals` POST has its 409 widened ("...cap is already reached, or the linked wallet is registered to another governance participant").

## Re-measure (scripts/runs.sh, tsc_lint.sh, eslint.js, frag.sh; logs/runs_summary.log, logs/red_labels.log)
- Head, the 3 changed test files: **82/82**.
- Red-first, base product with the head tests: **10 failed, all by assertion**.
  - ks1950: 8 RED fail and 7 controls pass, with **0 label mismatches** (F1, F1v, F1s, D4, D3, D3b, D3b-refresh, D1).
  - ks1942: R3c and QB1 fail. Those are the two declared write-shape assertion changes.
  - The ks1940 edit is harness-only (+50 lines) and stays green.
  - The RED labels on the ks1940/ks1942 cells that pass belong to the earlier PRs.
- Whole governance suite: base (base product + base tests) **264/264, 15 suites** -> head **279/279, 16 suites**.
- tsc: `tsconfig.json --noEmit` rc 0. Including tests, with a scratch config extending it: **base 0 -> head 0 errors**. The planted unused const gives 1 error, rc 2, and was restored (sha OK).
- eslint, flat config with cwd Blockchain/Dev, on the 5 changed .ts files: **rc 0, 0 problems**. The planted file gives 1 error and 1 warning, rc 1, and was moved to logs/_quarantine.
- docs-fragments:
  - clean: rc 0, "flow 117 legacy + 103 new, cheat 112 legacy + 103 new";
  - a planted unclosed `<div>` in the KS-1950 flow fragment gives rc 1, naming it, and the same for the cheat fragment;
  - both were restored by sha256, and the check is rc 0 after.
- Not re-run: the author's pre-push hook (PREFLIGHT INCOMPLETE 13/16, legs 3/4/8 skipped; quoted) and their own real-PG checks. My probe stands in for those.

## Mutants (scripts/mutants.py; product file only, tests untouched, each anchor asserted unique, sha256 restored after every run: "ALL RESTORED"; whole governance suite per mutant)
**16/17 KILLED, every kill by AssertionError.**
- M1s and M7 did not compile on the first run: an unused helper or const (TS6133), then TS2322 and TS2367. I rewrote them with `void`, a type annotation, and `String()`, and both were then killed. The failed runs are kept in logs/mutants_table_run1.log, logs/mutants_table_run2.log and logs/mut_*_run1_did_not_compile.log.
- M7b survived; see G134-F3.

| mutant | result (cells red) |
|---|---|
| M1 createProposal re-saves the whole proposer row (the bug) | KILLED: ks1950 F1 D4 D1 C1, ks1942 C4, ks1940 T6b |
| M1v castVote re-saves the whole voter row | KILLED: F1v C2 |
| M1s self-register re-saves the whole existing row | KILLED: F1s D3b-refresh, ks1942 R3c QB1 |
| M2 / M2v the counter written from the read value | KILLED: F1 D4 D1 C1 + 4 / F1v C2 |
| M2b the bump SQL writes +0 | KILLED: 8 cells incl. F1 C1 |
| M3 refresh drops RETURNING (201 reports the stale read) | KILLED: F1s C3 C3d C6 D3b-refresh + 5 |
| M3b insert drops RETURNING | KILLED: D3 D3b C5 + 5 |
| M4 first registration overwrites on conflict | KILLED: D3, ks1940 T6 |
| M4b admin upsert writes the counters again (D-4 undone) | KILLED: D4 |
| M5 refresh clears an omitted did (no COALESCE) | KILLED: C3 F1s + 8 |
| M6 bump on a missing row throws | KILLED: D1 + 27 |
| M6b bump on a missing row is silent (no warn) | KILLED: D1 |
| M7 wallet 23505 not recognised | KILLED: D3b D3b-refresh |
| **M7b any 23505 is a wallet 409** | **SURVIVED** (equivalent on today's schema; G134-F3) |
| M8 0 rows answers 503 instead of re-reading | KILLED: D3 |
| M9 refresh also writes stake and roles from the stale read | KILLED: F1s C3 + 6 |

No existing cell catches G134-F1. That is shown by the head suite being green while the real-PG race fails.

## merge-tree (scripts/merge_tree.sh, logs/merge_tree.log)
- develop `8150eeb3` (unchanged at END) is an ancestor of the PR head.
- `merge-tree --write-tree` gives rc 0 and tree `1fe26067`, which **equals the head tree**.
- The merged tree differs from develop in exactly the PR's 8 paths.

## Kam's ks1346 logging rule
Complies (G134-F7).

## Notes for the PR body
1. **G134-F1 (FIX-BEFORE-MERGE):** on real PostgreSQL, two concurrent first registrations of the same user answer a false 409 in about 13% of tight races (20/150).
   - The cause: `ON CONFLICT (id)` makes only the pkey the arbiter, so the UNIQUE(wallet_address) index raises 23505.
   - The fix: re-read by id inside the wallet-23505 branch of `dbInsertParticipantIfAbsent`, and return the caller's own row (code in G134-F1).
   - Add a stand-in cell for it.
   - Measured fixed: 300/300 coherent, with the suite at 279/279.
2. G134-F2 (recommended): createProposal's auto-register pre-check should 409 only when `holder.id !== proposerId`, and use `holder` otherwise. Do it here or as a follow-up.
3. G134-F3 (recommended): add a cell where a 23505 under another constraint name stays 500 (it pins M7b).
4. G134-F4 (info): self-register owns wallet_address and did by D-2. An admin's wallet change made mid-request is reset to the linked wallet. Stake and roles are never written.
5. Gate 134 measured on real PostgreSQL 15.19, with the real router, the real authenticate and a real second connection. The admin change survives on all 3 paths at head and is reverted at base. Counters go up by exactly 1.

## NOT TESTED
- The PR body (no Secuura gh auth).
- Node 24.
- A booted service or the gateway hop. The app was built as index.ts does it, without helmet, cors or the request logger.
- delegate and cancel: they do not write participants (read from source and confirmed by grep).
- The four platform suites, CI, and the pre-push legs (quoted only).
- Live data: whether any production rows show past reverts.
- Whether the textual yaml merge with S 13th's PR 3 equals a regeneration (the author says the one that merges second regenerates).
- G134-F1's fix as a committed PR change: I measured it only as a gate-made variant, not as the author's code.

## Processes and containers
- I started `gate134-pg` (postgres:15-alpine, 127.0.0.1:55134). It was **removed** with `docker rm -f` (rc 0), and `docker ps -a --filter name=gate134` afterwards shows 0 rows.
- One background task, `npm ci --ignore-scripts` + shared build, completed rc 0. Every jest, probe and sqlrace run was in the foreground. **Nothing I started is still running.**
- The jest TMPDIR `/private/tmp/g134t` (38M, my own scratch) was deleted by literal path.
- Probe copies, base-time test moves and the planted eslint file are in logs/_quarantine/. The clone's `git status --short` prints 0 lines, and push is disabled (`no_push_qa_gate`).
