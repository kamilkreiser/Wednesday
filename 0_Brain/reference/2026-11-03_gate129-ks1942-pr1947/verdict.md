# QA Gate 129 verdict: Secuura/Distributed_Secuura PR 1947 (KS-1942, governance register binds the linked wallet; stake and roles admin-set), TIER 1

## BLUF
**GO WITH NOTES. Nothing has to be fixed before merge.** I ran the REAL governance router (POST /participants/register and POST /proposals) behind the REAL shared `authenticate()` (RS256 tokens signed with a key generated in the probe) and the REAL shared `errorHandler`, over the REAL `services/governance/src/db.ts`, against a **REAL PostgreSQL 15.19** (throwaway container `gate129-pg`, now removed). The governance tables come verbatim from `docker/init/04-sprint2-service-tables.sql`, including `wallet_address UNIQUE`. `users` has migration 039's fail-closed `tenant_isolation` policy with ENABLE + FORCE RLS. The probe connected as `gate_app` (NOSUPERUSER, NOBYPASSRLS). Nothing was stubbed except one wrapper on `pg.Client.prototype.query`, which lets a cell make ONE named statement reject or run a hook first. I ran 48 records at base (merge-base `1584c0f0`) and the same 48 at head (`31ba0236`).
**Head matches the approved design in 46 of 46 judged cells (2 more are finding probes). Unhandled rejections: 0 at base and 0 at head** (logs/probe_table.md).
- (a) A non-admin using its own linked wallet is stored at 0 / basic / 0 / false / false. Any stake, DRep or committee value other than the stored one gets a **403 under D2a**, with nothing written; the request is not ignored.
- (b) Another wallet, no linked wallet, no tenant, a cross-tenant user, a non-uuid id, or a Unicode-fold role string: each gets 403 with nothing written.
- (c) A wallet held under another id gets 409 with the row unchanged. The same user re-registering gets 201 with every stored value kept.
- (d) Admin paths work, and they are the only code that sets stake.
- (e) KS-1940 holds for admin AND non-admin callers: 503, nothing written.
- (f) createProposal now auto-registers unstaked (D1a) and then answers 400.

The other numbers re-measure exactly as the author claims:
- Red first at the base: 31 failures, all by assertion. That is 29 in the new file plus the two declared changed cells (KS-1940 T6 and the governance.test auto-register cell), with 0 label mismatches. Green at head.
- Suite: 221/221 (14 files) at base, 264/264 (15 files) at head.
- tsc including tests: 0 errors at base and 0 at head.
- eslint on the changed files: 0.
- docs-fragments is clean, and both planted defects were caught.
- **20/20 mutants killed by assertion**, including the four the commission names.
- merge-tree is clean onto 3043c5bc and onto 9a9bf869, the develop that moved during this gate.

**Three recommended notes:**
- G129-F1: a stale full-row write-back can revert an admin's stake or role change. It is pre-existing, and this PR widens it to the committee flag, wallet and did.
- G129-F2: an admin who stakes a wallet BEFORE its owner self-registers strands that owner on 409.
- G129-F3: the new 409 is not in the OpenAPI spec.

None of them lets a caller choose a stake.

## Heads
- START (logs/head_start.log, 2026-11-02T13:04:14Z = 00:04 AEDT 11-03):
  - `refs/pull/1947/head` = `31ba0236afd6442985df222c12282ebf2b883352`, which matches Wednesday's read.
  - develop = `3043c5bcf4e9f437c8caf2594caaaeab284c59a8`, which matches.
  - merge-base = `1584c0f0ff808fddf35245bee41b6b5f9231054c`, the develop the author merged in.
  - There is one non-merge product commit, `ee765aa8`, plus three develop merge-ins (`aa2d9064`, `298b2227`, `31ba0236`).
- END (logs/head_end.log, 13:19:23Z):
  - The PR head is **unchanged** at `31ba0236`.
  - **develop MOVED to `9a9bf86967e3`** (KS-1724, JSON structural caps). I re-ran merge-tree onto it (Q6).
  - The working tree is clean: `git status --short` prints 0 lines.
- Diffstat, three-dot against the merge-base (logs/diffstat.log): **8 files, +1184/-55**, all of them in the declared partition:
  - db.ts +55/-0;
  - routes/governance.ts +25/-6;
  - governanceService.ts +127/-20;
  - new test file +887;
  - ks1940 test +34/-20;
  - governance.test.ts +10/-9;
  - the fragment pair, +24 and +22.
  - No package.json, lock, SQL, migration, shared or OpenAPI path is touched.
- **PR body not read.** This gate has no gh login for the Secuura account. I used the author's READY mail (evidence/ready_f24_pr1947.txt) and the commit message instead.
- Host: Node v26.8.1 only, so **no figure here is measured on Node 24**. load1 was 7.6-11.2 at each run start (logged in line 1 of every run log), and runs were limited to `--maxWorkers=2`.

## FINDINGS
- **G129-F1 (RECOMMENDED follow-up; pre-existing class, WIDENED by this PR; measured)** createProposal (governanceService.ts:702), castVote (:851, read from source) and selfRegisterParticipant (:566) re-save a WHOLE participant row read earlier through `dbSaveParticipant`. An admin change made between that read and the write is reverted.
  - Probe f8: an admin set U2 to 0 / basic / 0 / DRep false / committee false while U2's POST /proposals was in flight (the hook ran just before the proposal INSERT). The final UPSERT wrote back 50000 / whale / 75000 / DRep true, at base and at head.
  - At **head the committee flag is reverted as well** (true). At base it stayed false, because the base SET list left `is_constitutional_committee` out. This PR's widened SET list (it now also writes wallet_address, did and is_constitutional_committee) adds those three columns to what a stale write can revert.
  - The caller cannot pick the value: the most it can do is restore what it held at read time. It is a race, so it is not a merge block.
  - Fix, as a follow-up: the counters go through a targeted `UPDATE ... SET proposals_created = proposals_created + 1, last_active_at = $2 WHERE id = $1` (the same for votes_cast). The self-register refresh updates only wallet_address, did and last_active_at.
  - This answers question (f): no route lets a caller SET or OVERWRITE stake with a value of its own choosing. This revert window is the only other path that writes stake.
- **G129-F2 (RECOMMENDED: state it in the PR body, follow-up candidate; measured g1/g2)** Order matters when an admin stakes a wallet.
  - g1: U1 self-registers, then a SUPER_ADMIN registers W1 at stake 5000 with isDRep true, then U1 proposes. Every step gets 201, and the stake lands on U1's OWN row (id = userId).
  - g2: the admin acts FIRST. The admin path creates the row under a NEW uuid (registerParticipant :490). U1's self-register then gets **409**, and U1's POST /proposals gets **409**, until a data change re-keys that row. castVote, cancel and delegate also never find it.
  - At base, g2 "worked" only through the 1000-stake auto-register with wallet = userId (201 -> 201 -> 201).
  - The author raised this as a follow-up candidate, and D3a was approved knowing it. The PR body should give the operating rule ("the user self-registers first, then the admin sets stake"). The follow-up is for the admin path to bind to the user whose `users.wallet_address` matches.
- **G129-F3 (RECOMMENDED; read from source)** `governance.openapi.ts` for POST /api/governance/participants/register lists 400/401/403/429/500/404/502/503 and **no 409**. The runtime now answers 409 when the wallet is held by another participant.
  - The 409 on POST /proposals is documented only as "The per-tenant active-proposal cap is already reached" (:859). It now also means "wallet held by another participant".
  - The design said the spec stays unchanged, so this is spec text only. The schemathesis status-conformance check would flag an undocumented 409 if a fuzz run ever reached it.
  - Patch it here, or file it as a follow-up.
- **G129-F4 (INFO: the commission's wording vs the approved design)**
  - (a) says "registered with stake 0 whatever the body sends". D2a, as approved, REFUSES a body that asks for a stake or flag different from the stored one: 403 "Only an admin can set stake or roles", 0 writes (a1, a2, a3, a6). Fields the base handler never accepted (tier, votePower, id, role, proposalsCreated) are stripped by zod: a4 got 201 at 0 / basic / 0, and no `forged` row was written.
  - (c) says "a duplicate register = 409". D3a gives 409 only when the linked wallet is held under ANOTHER id (c4, f4).
    - The same user re-registering gets 201 with stake, roles, did and vote power untouched (c1).
    - The same user asking for a different stake or flag gets 403 with the row unchanged (c2, c3).
  - Head matches the design in each case.
- **G129-F5 (INFO, how the probe instrument behaved)** On the `pool.query` path, a revoked Proxy injected at `Client.query` reaches governance as a READABLE error: pg-pool's own callback handling catches it first, and `error: "invalid_argument"` is logged. So the byId and byAddress "revokedProxy" cells in my probe really exercise an ordinary error.
  - On the users read (a direct client query), the unreadable value DID reach governance: `error: "unreadable thrown value"` was logged, and the answer was 503.
  - The author's service-level unreadable cells (R6b, NT1b, KS-1940 T2b) cover the readLinkedWallet and lookup guards, and every one is green.
- **G129-F6 (INFO, Kam's ks1346 logging rule: complies)** The PR adds two log lines:
  - `logger.error('DB get linked wallet failed', { userId, error: reason })`, where reason is the message text or the constant `'unreadable thrown value'`. `String(err)` of a readable non-Error is the same pattern as every KS-1868 site.
  - `logger.info('Participant self-registered', { participantId, tier, votePower })`.
  - Neither logs a thrown object or the request body. The `walletAddress` in 'DB get participant by address failed' predates this PR.
- **G129-F7 (INFO, question (g))**
  - The commit message states the client-visible change: a stake or flag gets 403, a foreign or unlinked wallet gets 403, a held wallet gets 409, a failed users read gets 503, and under D1a an unstaked proposer gets 400. I could not read the PR body. The author should confirm that it carries Appendix B's "Client-visible behaviour change" list, as the brief required.
  - No first-party client calls register: `git grep` over services and frontend finds only GovernanceDashboard's GET calls. So nothing in the repo breaks on the new 403.
- **G129-F8 (INFO)** develop moved during the gate, 3043c5bc -> 9a9bf869 (KS-1724). merge-tree is clean onto both. Paths shared with the PR: 0, against controls of 7 and 48. KS-1724 touches `services/governance/src/index.ts` (the body parser), which is not a PR path.

## Q1. Behaviour: the real router on real PostgreSQL, base vs head (scripts/probe.test.ts, run by scripts/probe.sh; logs/probe_{base,head}.jsonl, logs/probe_table.md, logs/probe_rows.log)
The seed for every cell, reset each time:
- users (T1 unless named):
  - U1: wallet W1, no participant row;
  - U2: wallet W2, with a participant row at stake 50000, whale, vote power 75000, DRep, committee, did;
  - U3: no wallet;
  - U4: tenant T2, wallet W4;
  - UA: the admin.
- `initDb()`: available at both versions. At head `getLinkedWalletAddress` is a function; at base it is undefined.

The fields the base handler accepted, enumerated from base routes/governance.ts:44-49 and `RegisterParticipantSchema` (types:440-446, `z.object`, so unknown keys are stripped): **walletAddress, stakedAmount (tier and vote power are derived from it), did, isDRep, isConstitutionalCommittee.** Every one is exercised below.

| cell | base | head |
|---|---|---|
| a0 own W1, stake 0 | 201, row written | 201; U1 row: W1, 0 / basic / 0 / false / false |
| a1 own W1, stake 1e6 | 201, stake 1e6 written (partner, vote power 2e6, DRep true) | **403** "Only an admin can set stake or roles"; 0 writes, tables unchanged |
| a2 / a3 isDRep true / committee true | 201, written | 403, 0 writes |
| a4 extras: tier, votePower, id, role, proposalsCreated | 201 | 201 at 0 / basic / 0, proposals_created 0, no `forged` row |
| a5 did plus explicit false flags | 201 | 201 with the did |
| a6 role `admin` (not a platform role), stake 1e6 | 201 written | 403, 0 writes |
| b1 names U2's W2 at stake 0 | **201: U2's row overwritten to 0 / basic / 0, DRep false** | 403 "walletAddress is not the wallet linked..."; no byAddress read, 0 writes |
| b2 an unregistered wallet with stake 1e6 + DRep | 201 written | 403, 0 writes |
| b3 no linked wallet / b4 no tenant / b5 a T2 user with a T1 token / b6 a non-uuid id | 201 written | 403 "Link a wallet to your account first", 0 writes |
| b7 role `ſuper_admin` (U+017F) / b8 `super_admın` (U+0131) name W2 at 1e6 | 201, W2 overwritten | 403, 0 writes (not an admin) |
| b9 the T2 user, own wallet, own tenant (control) | 201 | 201 at 0 |
| c1 U2 re-registers W2 at 50000, flags omitted | 201 | 201; row unchanged (50000 / whale / 75000 / DRep / committee / did) |
| c2 U2 at stake 0 / c3 U2 isDRep false | 201, row changed | 403, row unchanged, 0 writes |
| c4 a legacy row holds W1 under another id | 201 (legacy row re-saved) | **409**, 0 writes, no U1 row |
| c5 / c6 legacy self row (wallet = id, stake 1000) re-registers W1 at 1000 / at 0 | 201 / 201 | 201, wallet re-bound to W1 with stake 1000 kept / 403, unchanged |
| d1 SUPER_ADMIN sets W2 to 200000, DRep false | 201 applied | 201 applied (partner, vote power 400000) |
| d2 SYSTEM_ADMIN, new wallet, 5000, committee | 201 (new uuid) | 201 (new uuid) |
| d3 `super_admin` (lower case) re-registers W2, flags omitted | 201 | 201, DRep, committee and did kept |
| d4 SUPER_ADMIN registers W1 (U1's linked wallet) at 3000 | 201 (uuid row) | 201 (uuid row): see G129-F2 |
| e1 admin, byAddress fails (ordinary / Proxy) | 503, 0 writes | 503, 0 writes |
| e2 non-admin U2, byAddress fails | 503, 0 writes | 503, 0 writes |
| e3 non-admin new user, byId fails | 201 written (base never reads byId) | **503, 0 writes** |
| e4 non-admin, users read fails | 201 written | **503** "Linked wallet store...", 0 writes |
| e5 non-admin legacy self row, byAddress fails | 503 | 503, 0 writes |
| f1 unregistered U1 proposes | 201; 1000 stake granted, wallet = user id (INSERT uuid, DELETE, INSERT, proposal, INSERT) | **400** "Minimum stake of 1000..."; one INSERT (U1, W1, 0 / basic / 0); 0 proposals |
| f2 staked U2 proposes (control) | 201 | 201, proposals_created 2 -> 3, stake unchanged |
| f3 U3 (no wallet) proposes / f4 a legacy row holds W1 | 201 with a 1000 grant | 403 / 409, 0 writes |
| f5 U2 proposes, byId fails | 503, 0 writes | 503, 0 writes |
| f6 users read fails / f7 byAddress fails | 201 granted / 503 | 503 / 503, 0 writes |
| f8 an admin de-stakes U2 mid-proposal | stake/DRep REVERTED, committee kept | stake/DRep/**committee** REVERTED (G129-F1) |
| g1 self-register -> admin stake -> propose | 201 -> 201 -> 201 | 201 -> 201 -> 201 (stake on U1's own row) |
| g2 admin stake -> self-register -> propose | 201 -> 201 -> 201 | 201 -> **409 -> 409** (G129-F2) |

The real-PG run also confirms the RLS read without a stand-in: b5 (a T2 user with a T1 GUC) reads nothing, and b9 (the same user under its own tenant) is found.

**(d) Every writer of stake, vote power, DRep or roles.**
- Method 1: `git grep` for `dbSaveParticipant|svc_governance_participants|staked_amount|vote_power|is_drep|registerParticipant|selfRegisterParticipant|...` over services and packages, tests excluded (logs/grep_writers_head.log). The only INSERT or UPDATE of the table is `dbSaveParticipant` (:180). Its callers are registerParticipant :505 (admin only, reached from the route only under `isPlatformRole`), selfRegisterParticipant :566, createProposal :650 (unstaked) and :702 (stats), and castVote :851 (stats).
- Method 2: a whole-repo search for the table name (logs/grep_table_all.log) gives 3 DDL files, 1 doc, 4 governance tests, the service and the fragment. A search for `insert into|update|delete from svc_governance_participants` (logs/grep_table_writes.log) returns exactly one hit, :180. That hit is the positive control.
- `DELETE` is gone from createProposal at head (f1 base vs head).
- staking's `tiers.ts:308 calculateVotePower` computes a value in a response and writes nothing to governance. Staking's own caller-asserted stake is KS-1948, not this PR.
- So the only way to set a stake is the platform-role branch, apart from the stale write-back of G129-F1.

## Q2. The hunks (logs/product_diff.log)
- **db.ts +55:** `getLinkedWalletAddress(userId, tenantId)`.
  - It returns null for no tenant or a non-uuid id.
  - In degraded mode it THROWS. That differs from referral's copy, deliberately and correctly: no wallet means a 403.
  - Under `runWithTenantId` it opens one client and runs BEGIN, `applyTenantGuc`, `SET LOCAL statement_timeout = 3000`, then `SELECT wallet_address FROM users WHERE id = $1 AND tenant_id::text = $2 LIMIT 1`, then COMMIT. On error it rolls back and rethrows. It always releases the client.
- **routes +25/-6:** a 401 when `req.user.userId` is absent. `isPlatformRole(user.role)` decides between `registerParticipant` (unchanged signature) and `selfRegisterParticipant`. POST /proposals passes `{ tenantId }` to createProposal. The request schema is unchanged.
- **service +127/-20:**
  - `dbSaveParticipant`'s SET list adds `wallet_address`, `did` and `is_constitutional_committee`.
  - `readLinkedWallet` turns every throw into `ServiceUnavailableError('Linked wallet store')` with the KS-1868 guarded reason.
  - `unstakedParticipant()` is added.
  - `registerParticipant` keeps an omitted did and flags from the existing row.
  - `selfRegisterParticipant` runs in this order: linked-wallet read -> 403 / 403 -> byAddress -> 409 -> byId -> D2a 403 -> one save. **Every lookup comes before the only write.**
  - createProposal's auto-register runs: linked read -> 403 -> byAddress -> 409 -> one unstaked save. The 1000 grant, the uuid row and the DELETE are removed.
- **Not changed:** castVote, delegate, cancel, submit, execute, process-expired, the schema, the OpenAPI spec, migrations, and @secuura/shared.

## Q3. Re-measure (scripts/runs.sh, scripts/summ.py; logs/runs_summary.log, logs/red_labels.log)
- Head, the 3 changed test files: **140/140** (new file 43/43, ks1940 24/24, governance.test 73/73).
- Red first, base product with the head tests: **31 failed / 109 passed, all 31 by assertion.**
  - New file: 14 passed (all `control`) and 29 failed (all `RED`), with 0 label mismatches.
  - KS-1940 control T6 and the governance.test auto-register cell fail at base, as declared (D1a).
- Whole governance suite: base (base product + base tests) **221/221, 14 suites** -> head **264/264, 15 suites**. The author's numbers re-measure exactly.
- tsc:
  - `tsconfig.json --noEmit` rc 0.
  - Governance has no `tsconfig.test.json` and no leg-16 baseline, so I used a scratch config that extends it and includes `src/__tests__` (scripts/tsconfig.gate129-tests.json): **base 0 errors -> head 0 errors**.
  - Planted control: an unused const in the new test file gives 1 error, rc 2. The file was restored and its sha checked.
- eslint (run with cwd = Blockchain/Dev through `spawnSync`, flat config) on the 6 changed .ts files: **0 problems, rc 0**. Planted control file: 1 error (no-debugger) and 1 warning, rc 1. The file was moved to logs/_quarantine.
- docs-fragments (logs/frag_outer.log):
  - Clean: rc 0, "flow 117 legacy + 96 new, cheat 112 legacy + 96 new".
  - Planted unclosed `<div>` in flow: rc 1, naming the KS-1942 flow fragment. In cheat: rc 1, naming the cheat fragment.
  - Both were restored by sha256, and the check was rc 0 after.
  - On the merged tree (develop 3043c5bc + PR): rc 0, "97 new" (logs/frag_merged.log).
- NOT re-run: the author's own real-PG checks (15) and the pre-push hook (PREFLIGHT INCOMPLETE 13/16, legs 3, 4 and 8 skipped). Both are quoted from the READY mail. My own real-PG probe stands in for the first.

## Q4. Mutants (scripts/mutants.py; product files only, tests untouched, each anchor asserted unique, sha256 restore asserted after each: "ALL RESTORED"; logs/mutants_table.log, logs/mutants_table_M5_run3.log, per-run logs/mut_<id>.log)
**20/20 KILLED, every failure an AssertionError.** M5 failed to compile twice: first as `true` (TS18048, the same failure the author hit), then as `|| true`. I rewrote it as `isPlatformRole(user.role) || user.userId.length > 0`, and it was then killed. Those runs are kept as logs/mutants_table_run1_M5_M7_did_not_compile.log and logs/mut_M5_run2_did_not_compile.log. M7 first failed compile (an unused import), was rewritten with `void applyTenantGuc;`, and was then killed.

| mutant | result (cells red) |
|---|---|
| M1 **accept the body's stake** (D2a gone, body stake/flags stored) | KILLED: R2 R2b R3 R3b QA1b |
| M1b ignore the body stake/flag silently | KILLED: R2 R2b R3 R3b QA1b |
| M2 **skip the wallet-link check** (body wallet bound) | KILLED: R1 R4 R5 R5b R7 R7b R7c M6 |
| M2b drop only the differing-wallet 403 | KILLED: R1 R4 M6 |
| M2c drop the no-linked-wallet 403 | KILLED: R5 R5b R7 R7b R7c |
| M3 **skip the 409** (self-register) | KILLED: R9b |
| M3b skip the 409 (createProposal) | KILLED: KS-1940 T6, R8c, R8e |
| M4 **write before the lookup** (self-register) | KILLED: 28 cells incl. NT1 NT1b NT1c NT1n R1 R2 |
| M4b write before the lookup (createProposal) | KILLED: T6, R8 R8b R8c R8d R8e, governance.test |
| M5 role check removed | KILLED: 21 cells incl. R1-R6, M6, NT1c |
| M5b Unicode `toUpperCase()` role compare | KILLED: M6 |
| M6 users-read failure swallowed into "no wallet" | KILLED: R6 R6b R6c R8d |
| M7 tenant GUC dropped | KILLED: 27 cells incl. C3, NT1, NT2 |
| M7b degraded mode reads as no wallet | KILLED: R6c |
| M8 admin flags reset again on omit | KILLED: C2 |
| M9 createProposal keeps the 1000 grant | KILLED: T6, R8 |
| M10 SET list loses the committee flag | KILLED: QA2 |
| M11 non-admin byId failure swallowed (KS-1940 twin) | KILLED: NT1c |
| M12 non-admin byAddress failure swallowed (KS-1940 twin) | KILLED: NT1 NT1b NT1n |
| M13 existing participant not kept on self re-register | KILLED: NT2 QA1 QB1 QB2 R3c |

The tenant bind in the SQL (`AND tenant_id::text = $2`, KS-1582 m2) was not mutated: under FORCE RLS, with an app role that cannot bypass it, that bind is defence in depth. The author's real-PG check covers it with RLS bypassed.

## Q5. KS-1940 for admin AND non-admin (from Q1 and Q4)
- Real PG: e1 (admin) and e2, e3, e4 and e5 (non-admin), with both an ordinary error and a Proxy, all answer **503 with 0 writes and the tables byte-equal**. So do f5, f6 and f7 on POST /proposals.
- Committed cells: the NT twins (NT1, NT1n, NT1b, NT1c, NT2) carry the non-admin property. M11 and M12 prove that those cells, not only the admin-run T3, T3n and T2b, guard it.
- The KS-1940 register cells now run as SUPER_ADMIN with their assertions unchanged. That is a test-only edit, and I diffed it whole (Q2): only the role header, the db stand-in and T6 changed.

## Q6. merge-tree (scripts/merge_tree.sh, scripts/merge_tree2.sh; logs/merge_tree.log, logs/merge_tree2.log)
- Onto `3043c5bc` (KS-1943): **rc 0, tree `c85dce707026`**. develop moved 7 paths since 1584c0f0, and 0 are shared with the PR's 8 (control: the moved list against itself gives 7). The merged tree differs from develop in exactly the PR's 8 paths. The PR's governance and fragment bytes in the merged tree are identical to the head's. docs-fragments on the merged tree: rc 0.
- Onto `9a9bf869` (KS-1724, which moved during the gate): **rc 0, tree `eb81b8080269`**. It moved 48 paths, 0 shared (control 48). The merged tree differs from develop in exactly the PR's 8 paths. KS-1724 changes `services/governance/src/index.ts`, outside the PR. I did not re-run the suite on this tree.

## Q7. Kam's ks1346 logging rule
Complies (G129-F6). The only new error log carries the message text or a constant, never a thrown object's fields or values. The new info log carries ids and derived numbers only.

## Notes for the PR body
1. G129-F1 (recommended follow-up): createProposal, castVote and self-register re-save a stale whole row. Measured, an admin de-stake made during a proposal is reverted. The PR's wider SET list now also reverts the committee flag, did and wallet. Follow-up: targeted counter UPDATEs.
2. G129-F2 (recommended): add the operating rule. "Self-register first. An admin who registers the wallet first creates a uuid row, and the owner then gets 409 on register and on POST /proposals until that row is re-keyed (a data change, Kam's)." Measured g1/g2.
3. G129-F3 (recommended): add 409 to the register path in `governance.openapi.ts`, and widen the description of the POST /proposals 409. Do it here or as a follow-up.
4. Gate 129 measured on real PostgreSQL 15.19, with the real router, the real authenticate and the real db.ts. Head equals the design in 46/46 cells, against 48 records at base and at head.

## NOT TESTED
- The PR body text: I have no Secuura gh auth, so (g) is answered from the commit message.
- Node 24.
- A booted service or the gateway hop: I built the app myself the way index.ts does (express.json, rejectNulBytes, authenticate, routes, errorHandler), without helmet, cors or the request logger.
- castVote's and delegate's write-back under a race: read from source only.
- The governance suite on the merged tree onto 9a9bf869.
- The four platform suites, CI, and the pre-push hook legs (quoted only).
- Live row counts for the 409 / legacy rows (no box read).
- Degraded mode end-to-end on real PG: covered only by the author's R6c and my M7b.
- An unreadable value on the pool.query path under real pg-pool, which converts it (G129-F5).
- The tenant-bind SQL mutant.

## Processes and containers
- I started `gate129-pg` (postgres:15-alpine, 127.0.0.1:55129). It was **removed** with `docker rm -f` (rc 0), and `docker ps -a --filter name=gate129` afterwards shows 0 rows.
- One background task, `npm ci` + shared build, completed with rc 0.
- Every jest run was in the foreground. Nothing I started is still running.
- Probe test files and planted files were moved into logs/_quarantine/, and the clone's `git status` is clean.
