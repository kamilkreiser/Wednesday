# LAUNCH BRIEF: Seat B 30th, Secuura/Blockchain. The successor build seat (round 26). From Wednesday

## BLUF
You are **Seat B 30th**, the successor to Seat B 29th (wrapped 22:4xZ). You are the ONLY build seat. The only other live Secuura seat is **Seat M1** (pane `Secuura/Blockchain-E`), which builds nothing, pushes nothing and merges wrapped authors' PRs on Wednesday's signed GOs. Your queue has 8 items, in order:
- item 1: adopt and finish **KS-730 PR 3** (`adminConfig.ts`);
- items 2-4: three **FIX ROUNDS, each round 1 of 2**: #1274 (KS-934), #1268 (KS-1318 + KS-1142 + KS-1316), #1261 (KS-1293). Their authors have wrapped, so you push fast-forward commits on THEIR branches;
- item 5: raise **KS-766** from a held local-model READY;
- item 6: **KS-1333**, only after #1281 merges;
- item 7: the **tenant-DB groundwork**: one docs PR and one parent ticket;
- item 8: file **N-DEV-1** as one ticket.

Every change ends at **READY FOR QA** → gate → Wednesday's GO → **M1 merges**. You merge nothing. **You deploy nothing.**
**Develop now:** `185194f6649e3b3328c6bb6c318570771f455728` (#1272, KS-849), read by the drafter with `ls-remote` at 23:03Z and again at 23:07Z (09:03 and 09:07 AEST).

**Seat identity**
- Pane: `Secuura/Blockchain`.
- Inbox: `secuura-blockchain@agentmail.to`. It is SHARED with Seat M1. Mail tagged for another seat is not yours; filter on `(Seat B 30th)`.
- Tag every subject you send `(Seat B 30th)`.
- PROPOSED, for you to confirm in ITEM 0:
  - record folder `/Volumes/DevMASTER/!CODING/Secuura/Blockchain/5_Project_History/2026-09-26_seatB-30th/`;
  - NEW worktrees `s-b30-*` at the ABSOLUTE path `/Volumes/DevMASTER/!CODING/Secuura/Blockchain/worktrees/`, never under the clone (0 exist at 23:0xZ);
  - new branches `feature/ks-<key>-<slug>-b30-<n>`;
  - the named exceptions (ADOPTED, not yours by token): B 29th's worktree `s-b29-ks730c` and its branch `feature/ks-730-adminconfig-prod-message-b29-9` (item 1), and the three foreign PR branches of items 2-4.

**Authority**
- Kam's week instruction (`WEEK-INSTRUCTION.md`, valid_until 2026-09-27): *"continue with the tickets, both local LLM and through the Claude agents"*.
- Kam's standing rule of 2026-09-13: as many agents as the code partition allows, with no two agents on the same code. Overnight is working time.
- Kam's open-ended TESTED grant of 2026-09-11 covers merges; Wednesday's GO naming the head SHA is the approval. M1 executes it.
- Kam's ruling (c) on card `secuura-ks1304-withtenant-tenant-pool-and-admin-writes`, with his note "start planning the database", is the authority for item 7, and for NOTHING beyond it (nothing is built).

## READ FIRST
- **Seat B 29th's handover**: its history entry, the `Seat B 29th` block at `/Volumes/DevMASTER/!CODING/Secuura/Blockchain/5_Project_History/history.md` lines 24-44. Read it WHOLE. It gives you four things to inherit:
  - **THE COMPILE-BREAKING TAMPER.** A red arm that deletes a line can orphan an import, a declaration or an `err`. Then `tsc` refuses the file and jest reports **0 passed AND 0 failed**, which looks exactly like "the tamper applied and was inert". **Reference every identifier the deleted line used**, and have a LOADFAIL verdict separate from a pass. It happened six times in B 29th's session.
  - **Every cell asserts the write was REACHED before it asserts what was written** (the `persistHealedAnchor` sibling whose fixture never reaches `updateDocument`).
  - **A comment can be load-bearing and wrong** (the `gdpr.ts` "no logger import" claim, measured false). Correct it in place; never silently contradict it.
  - **Prettier can reflow a line and silently move a tamper anchor.** After a format fix, re-run the suite, `tsc` AND every red arm.
- `/Volumes/DevMASTER/WEDNESDAY/2_Project_Files/fleet/STANDING_LINES.md`. Apply: the five READY artefacts, INSTRUMENTS, the three-dot rule, the tamper-anchor rule, one red arm per conjunct, restoring disk modes after `git apply`, **re-key the PROSE in inherited tools**, **a parser fix is tested against captured real output**, the §5f `live sweep owed` canonical handle, and the search-before-filing rule.
- B 29th's tools, `/Volumes/DevMASTER/!CODING/Secuura/Blockchain/5_Project_History/2026-09-26_seatB-29th/raise/`: `lock25.sh`, `push25.sh`, `push25_ff.sh` (the fast-forward push onto another seat's branch, used for #1245 round 3), `namecheck25.py`, `rekey_check.py`, `env_up_b29.sh`. Make NEW copies in your own folder. Do not run B 29th's copies.
- The three gate reports for items 2-4 (paths in the QUEUE). Read each finding WHOLE, not only the lines quoted here.

## YOUR FILES / NOT YOURS
- **YOURS:** any file that is NOT held by an open PR you do not own and NOT under "Nobody's". Your queue touches exactly these:
  - `Blockchain/Dev/services/originate/src/routes/adminConfig.ts` and the NEW cell `src/__tests__/ks730c-adminconfig-500-never-answers-err-message.test.ts` (item 1; in NO open PR);
  - #1274's two files, `services/m365-integration/src/index.ts` and `src/__tests__/ks934-teams-notify-request-path-bound.test.ts` (item 2);
  - #1268's two files, `packages/shared/src/__tests__/entrypoint-corpus.test.ts` and `…/ks781-p3-3-body-parser-order.test.ts` (item 3);
  - #1261's one file, `services/originate/src/__tests__/ks1293-originate-suite-is-hermetic.test.ts` (item 4);
  - `Blockchain/Dev/scripts/base-image-watch.sh` (item 5);
  - `services/originate/src/services/anchorStateSync.ts`, but ONLY after #1281 merges (item 6);
  - `Blockchain/Dev/docs/MULTI-TENANCY.md` (item 7a).
- **NOT YOURS: every file of an open PR you do not own** (the drafter listed them via the PULLS API at 23:05Z; re-list them in ITEM 0):
  - B 29th's PRs, which are waiting on gates (a fix round on any of them comes to you only by a later ANSWER):
    - #1270: `repositories/lifecycleEventRepo.ts`, `routes/documents.ts`;
    - #1273: `ks978-published-contract-organizationuuid.test.ts`;
    - #1276: `originate.openapi.ts`, `ks794-…test.ts`, `docs/openapi/secuura-api.yaml`;
    - #1279: `ks597-issuer-organization-id.integration.test.ts`;
    - #1280: `routes/verification.ts`, `routes/verificationV2.ts`, `ks1129-…test.ts`;
    - #1281: `services/anchorStateSync.ts`, `ks1074-…test.ts`;
    - #1282: `routes/systemErrors.ts`, `ks730a-…test.ts`;
    - #1283: `routes/gdpr.ts`, `ks730b-…test.ts`;
    - #1245 (round 3, `cb31a58c190f`): `systemTest/performance/tests/unit/support/capturedChildOutput.ts`, `…/utils/unitSuiteSlotIndependence.test.ts`.
  - Seat L7's (wrapped): #1271 (`systemTest/performance/gate/report.ts`, `runner/k6_docker.ts`, two ks1164 cells), #1275 (`packages/shared/src/security/ssrf-guard.ts`, the ks1179 cell), #1277 (`packages/shared/src/__tests__/walkTimeouts.test.ts`), #1278 (`systemTest/performance/tests/unit/config/sheddingCeiling.test.ts`, `…/support/readYamlRouting.ts`).
  - Seat L5's (wrapped): #1250 (`scripts/run-shell-suites.sh`, `scripts/__tests__/run_shell_suites.test.sh`), #1253 (`scripts/__tests__/pre_push_hook_base_fixture_guard.test.sh`).
  - Older open PRs: #1241, #995, #989, #927, #923, #920, #887, #809, #1129 (their paths are in the API listing), plus the 10 dependabot PRs.
- **Nobody's:** every `package.json` and lockfile; `scripts/preflight/`; `scripts/audit/`; `audit-baseline.json`; `.github/`; `migrations/` (never edit an applied migration).
- Any byte outside YOURS is a STOP.
- **Readers outside your lane:** `packages/shared`'s guard suites read originate sources by TEXT (ks860 listen calls, ks879 control bytes; #1263 changed ks879's figures). Run `packages/shared` on every head you raise. Point any new cell at `127.0.0.1:2`, never `:1` (KS-1266: undici refuses a Fetch-spec bad port before a socket exists).
- **KS-1304 stays unbuilt.** `adminConfig.ts` carries 9 of the 11 `withTenant(` call sites. Kam ruled (c): leave it until per-tenant databases are planned. Item 1 must not touch a `withTenant` call.

## ITEM 0: PLAN CONFIRMATION, before ANY push
1. **Refuse the launcher's single-session pull**, and say so. Write nothing to the shared checkout `2_Project_Files` or its `.git`. The only exceptions are `worktree add` in your own namespace and a `git fetch origin develop` (plus the three foreign PR branches) taken under `.push-lock-26`. **Develop's tip `185194f6649e` is ABSENT from the local object store** (`cat-file` rc 128 at 23:04Z), so your first fetch is needed.
2. Re-measure develop with `ls-remote`. **The diff decides, not the SHA.** If develop has moved from `185194f6649e`, read the move with `git diff --name-only` against your paths. It will move while M1 merges gate25T2's batch (#1270, #1271, #1273).
3. Re-read every ticket you will touch, INCLUDING all of its comments. Sort comments client-side; never use `last:N`.
4. Send a QUESTION mail, topic `plan confirmation (Seat B 30th)`. It carries every launcher preflight warning VERBATIM, and answers:
   - **Q1** Your seat, pane, inbox filter, record folder and namespace. Confirm the launcher pull was refused.
   - **Q2** Your tools. Make new copies of B 29th's `lock25.sh`, `push25.sh`, `push25_ff.sh` and `namecheck25.py` as `lock26.sh`, `push26.sh`, `push26_ff.sh` and `namecheck26.py`. Re-key the namespace, the PROSE and the lock path (`.push-lock-26`). The seat name must be a REQUIRED argument with no default. **No default may make a factual claim.** Name push logs by head sha. Grep every copy for `Seat B 29th`, `s-b29-`, `-b29-` and `.push-lock-25`, and show every hit gone, EXCEPT the named adoption of item 1. Prove each tool before it guards anything:
     - a refusal AND a genuine pass;
     - `lock26.sh` refuses to wait forever on a lock dir that has no holder file (B 29th found that INFINITE WAIT in the inherited script);
     - `push26_ff.sh` refuses a non-fast-forward, and never force-pushes.
   - **Q-ADOPT** Item 1's worktree and branch are B 29th's (`-b29-` token). Proposed: adopt both as they are, with no rename (a rename writes the shared ref store), and state the adoption in the PR body and the ticket comment. Your namespace scanner gets ONE named exception for that branch. Say if you would rather re-home the change onto a `-b30-` branch, and why.
   - **Q-FF** Items 2-4 push fast-forward commits onto three FOREIGN branches (`-l8r25-6`, `-l7r25-1`, `-r24-e-1`). Name each branch, its head (`ls-remote`) and the wrapped author's history entry that proves the author has wrapped. Your scanner gets exactly those three named exceptions. **No merge-in of develop.** The branches sit on older bases (#1274 and #1268 on `4db87c3e4b98` per their ticket comments; #1261's merge base `fa25c9b10fb4` per gate24T2c line 575). Say how you will test them against a develop that has moved: the gate re-predicts over the current develop; you report your base.
   - **Q-1274** Item 2's shape: which of the gate's three fix-shapes you will build, and why. See the QUEUE: the gate's regression cell (a second call attempts `wh-50…wh-59`) cannot be met by its option 2 alone.
   - **Q-1268** Item 3's shape: the gate's "never referenced except its own declaration" rule, and the `NewExpression` argument rule.
   - **Q-1261** Item 4's shape: the explicit 9-file subject manifest, the exact pin, or the reaches-anchoring derivation.
   - **Q-TENANT** Item 7b: KS-598 already has a parent (KS-772). A Linear issue has ONE parent. Propose one of: re-parent it; link it to the new ticket as "related" and leave KS-772; or ask Kam. Do not re-parent without the ANSWER.
   - **Q-PORTS** Your range is **55440-55449**. None of your items is expected to need a database. **The merged ks1263 integration file refuses any DSN outside `127.0.0.1:55410-55419`** (`:504`), so never run it on your range. If any item needs a database, say which one and ask.
   - **Q8** Branch names and subjects, run through the hyphenated-key scanner AND the namespace-token scanner (see SHARED RESOURCES).
   - **Q-DEPLOY** You deploy nothing. Confirm.

   Proceed only on Wednesday's ANSWER.

## QUEUE
Scope is quoted from the ticket or the gate report. Tier proposals are Wednesday's to rule. **A gate's fix-shape is a PROPOSAL, not a must-change list. If a cell cannot be built as stated, measure why and ask.**
1. **KS-730 PR 3 of 3, `routes/adminConfig.ts`** (In Progress; PR 1 is #1282 and PR 2 is #1283). **ADOPT, do not redo.**
   - The source change is DONE and UNCOMMITTED in `/Volumes/DevMASTER/!CODING/Secuura/Blockchain/worktrees/s-b29-ks730c`, on branch `feature/ks-730-adminconfig-prod-message-b29-9` (not on origin), at base `d7cdecf1d2ee`.
   - The diff is `adminConfig.ts` +69/−46. At the base there are 46 `NODE_ENV === 'production'` lines. In the worktree 1 remains, and it is inside a comment (`:89`).
   - The worktree has `node_modules` and a built `packages/shared/dist`.
   - Develop's move `d7cdecf1` → `185194f6` touched 0 lines of `adminConfig.ts` (GitHub compare, 10 files, none under `routes/`).
   - **THE DIAGNOSED CAUSE of the cell's reported 9 of 12 failures:** the routes read through `runWithPlatformScope(() => queryWithTenantGuc(defaultPool, …))` (for example `adminConfig.ts:2057`, `:2060`, `:2121`, `:2139`). The new cell mocks `@secuura/shared` with `queryWithTenantGuc: jest.fn()` (`:44`), a bare mock that resolves `undefined`, so a route can fail before it ever reaches the catch being tested.
   - **The fix is in the CELL's mock, never in product code.** Make `queryWithTenantGuc` return the shape the route reads, per route.
   - Every cell must first prove its route REACHED the throwing call and the catch. B 29th's lesson: a 500 from a mock-shaped crash would pass a "no err.message in the body" assertion for the wrong reason.
   - Re-measure the 9 of 12 figure yourself before you fix it. The drafter did NOT re-run it.
   - The rest as B 29th's plan ANSWER ruled:
     - log + one small local helper per file;
     - a cell in KS-727's shape across `development`, `demo`, `test` and unset, with the typed-client-error control;
     - re-sweep to zero, excluding comments and log lines.
   - **Tier 1.** Red at `d7cdecf1d2ee`, green at your head. Push under `.push-lock-26`.
2. **#1274 KS-934 FIX ROUND, round 1 of 2** (gate25T1 NO GO). The author, Seat L8, has wrapped: push a fast-forward on `feature/ks-934-teams-notify-request-path-bound-l8r25-6` (head `1a37bde12d55`). The finding, quoted from `/Volumes/DevMASTER/!CODING/Testing Agent MAIN/projects/secuura/reports/2026-09-26-batch1267-t1/report.md`, lines 38-47:
   > **#1274 KS-934 — NO GO** at `1a37bde12d55563f77e192519ca7db62461dbf6f`, over `df5e9f5da6d2`. … **BLOCKING — LIMIT-TRUNC (MEASURED AT RUNTIME):** With 60 active rows the route answers `{sent 50, failed 0, skipped 0, total 50, deadlineExceeded false}`. Rows 51–60 are neither attempted nor reported. A second call re-sends the same first 50 and never reaches the rest: a silent, permanent starvation of the newest webhooks. This contradicts the PR's own obligation 4, its body ("reported as such", "call again") and its code comment.

   and lines 559-569 (the merge addendum):
   > **#1274** (**NOT on this GO — NO GO**, F-1274-1) … Would squash `1a37bde12d55563f77e192519ca7db62461dbf6f`. Subject: `KS-934: bound POST /api/teams/notify with a LIMIT and an aggregate deadline (#1274)` (83 ≤ 92). Files (2 over 2 paths) … A new head needs a re-gate.

   - **The fix-shape at lines 301-304 is a PROPOSAL, "any one of":**
     1. drop the LIMIT;
     2. fetch `MAX_ROWS + 1`, and report `truncated`/`notAttempted`;
     3. order fairly (`ORDER BY last_sent_at ASC NULLS FIRST, created_at ASC`).
   - **Its regression cell (line 305):** "60 rows, defaults → the body reports 10 not attempted (or `truncated:true`), and a second call attempts `wh-50…wh-59`."
   - **Measure before you choose:**
     - option 2 alone reports the truncation but still re-sends the first 50, so it cannot meet the cell's second half;
     - option 3 needs a column the drafter did not verify exists on `svc_teams_webhooks`;
     - option 1 departs from the ticket's shape ("a LIMIT with paging").
   - Put the measured choice in Q-1274.
   - **Also in the same round, non-blocking, the gate's polish:** F-1274-4, `beforeAll(boot, 60_000)` in place of `boot()` inside `beforeEach` (line 267).
   - **F-1274-2 (ENV-NAN/ENV-ZERO) was dispositioned TICKET by the gate (Wednesday routes it; the gate filed nothing). It is NOT built or filed here**, unless Wednesday rules otherwise.
   - Red at `1a37bde12d55`, green at your head. m365 runs on vitest.
   - **Tier 1** (it was gated at tier 1).
3. **#1268 KS-1318 + KS-1142 + KS-1316 FIX ROUND, round 1 of 2** (gate25T2 NO GO). The author, Seat L7, has wrapped: push a fast-forward on `feature/ks-1318-ks781-default-shapes-tag-set-l7r25-1` (head `a8e0fca70ed4`). Quoted from `/Volumes/DevMASTER/!CODING/Testing Agent MAIN/projects/secuura/reports/2026-09-26-batch1268-t2/report.md`:
   - VERDICT (line 14):
     > THE READER RULE: the shape #1268's own walk comment names — "a bound arrow invoked only through an alias … still read `true`" — reads **`guarded: false`** at the head (develop read `true`, which is also the truth). Eight more invocation shapes flip correct → wrong the same way. All under-report (fail-closed); reach in the tree **0 of 794 files**. KS-1318 and KS-1142 are proven and are held with the vehicle.
   - "Reader rule #1268" (line 243):
     > **FAIL on the named alias shape → NO GO.** Of the COMMISSION's LEGITIMATE SHAPES, `.call`/`.apply`/`.bind()()` and returned-invoked read false (wrong); `await` IIFE, `?.()`, a called declaration and const-called-later read true (right). K1b: 3 false-green shapes, all hypothetical with reach 0.
   - The #1268 addendum (line 325):
     > **HELD, NO GO at `a8e0fca70ed41ef061cc99a325b610d27f08c7fb`; no squash.** For a re-gated head, use the same shape: MG-1 … Body: the commit message, keys {KS-1318, KS-1142, KS-1316}, `KS1143` un-hyphenated if the PR body is used. Subject (90): `KS-1318 + KS-1142 + KS-1316: ks781 tag set, corpus containment, guard reachability (#1268)`.
   - **The proposal (lines 69-79):**
     - treat a bound function expression as a DEFINITION only when its binding is never referenced in the continuation except by its own declaration;
     - treat `NewExpression` arguments like call arguments;
     - correct the code comment.
   - **Regression cells W14-W18** must each read `guarded: true`: alias, `.call`, `.bind()()`, `new Promise(…)`, `mk()()`. Add the control that W9 still reads `false`.
   - The K1b source-text finding (lines 81-94) is non-blocking, NOT PINNED. Build it only if Wednesday rules it in.
   - Keep KS-1318's and KS-1142's proven work byte-identical.
   - **Tier 2.**
4. **#1261 KS-1293 FIX ROUND, round 1 of 2** (gate24T2c NO GO). The author, Seat B 28th, has wrapped: push a fast-forward on `feature/ks-1293-pin-originate-suite-hermeticity-r24-e-1` (head `eab8d7031b1b`). Quoted from `/Volumes/DevMASTER/!CODING/Testing Agent MAIN/projects/secuura/reports/2026-09-26-batch1245r2-t2c/report.md`, line 58:
   > **READER: WRONG on 3 real shapes** (REVERT-SKIPS). Deleting the env line of ks1228 (:26), of ks1264 (:16) or of ks1213 (:30) leaves CONFIGPINNED GREEN. This is the shape the file's own header names and the ticket's Done-when requires to red.

   - Cause (lines 456-458): "The subject set is derived from 'who mentions the key', so the shape the file exists to catch erases its own subject."
   - **The fix-shape (lines 459-462) is the HOLD, relayed as a PROPOSAL, "any of":**
     - an explicit 9-file subject manifest;
     - an exact pin (`pinned === 11`);
     - subjects derived from what reaches anchoring.
   - **Regression cells:** RS1, RS2 and RS3a as fixtures the new rule must red.
   - Non-blocking, same round if cheap: N-1261-a NODNS-EGRESS (the spy answers non-loopback names itself and never calls the real resolver), and N-1261-c (un-hyphenate the foreign keys in the squash body).
   - The originate suite runs on jest `--runInBand`.
   - **Tier 2.**
5. **KS-766 raise** from the held Spark READY. These are the ADD's instructions to B 29th (`2026-09-26_ADD_seatB29_raise_ks766.md`), VERBATIM. **Three substitutions govern, and they follow the quote.**
   > **Add as the LAST item of your queue** (after your lane items and the #1261 fix round): raise **KS-766** as ONE PR from the held READY.
   > - **The patch:** `/Volumes/DevMASTER/WEDNESDAY/2_Project_Files/local-model/night/READY_KS-766-BASEIMAGEWATCH_spark-dsv4_SELFTEST-PASS_2026-09-26.diff.md` (the diff block inside it). One file: `Blockchain/Dev/scripts/base-image-watch.sh`, 3 hunks, written by the Spark local model, checked by Wednesday's harness (strict apply at d7cdecf1; red with the test hunk alone (exit 12), green with all three (exit 0), 20→22 PASS lines). Wednesday read it line by line: identical to the verified golden.
   > - **Base:** it was checked at d7cdecf1. develop is now df5e9f5da6d2, and the move touched 0 files under `Blockchain/Dev/scripts/` (GitHub compare, read by Wednesday). Apply it strict (`git apply --check` with no recount) on a worktree at the current develop tip. If it does not apply strictly, STOP and mail; do not recount.
   > - **Your own proof, not the harness's:** run `bash Blockchain/Dev/scripts/base-image-watch.sh --self-test` at the tip (expect 20 PASS) and at your head (expect 22 PASS, exit 0). Reproduce the red: the test hunk alone gives exit 12. Put all three in the Test Evidence block and name the base your worktree contains.
   > - **Partition:** `Blockchain/Dev/scripts/` belongs to no live seat (L5 has wrapped). This is a new worktree on your own namespace token (`-b29-`), under `.push-lock-25`.
   > - **PR body:** "Refs KS-766". No closing keyword. Credit the patch's origin plainly ("patch produced by the local model under a Wednesday brief, re-verified by this seat").
   > - It then goes to the next gate. Tier: by its diff. It is a host-script change, so the gate decides.

   **The substitutions for you:**
   1. your token is `-b30-` and your lock is `.push-lock-26`;
   2. develop is now `185194f6649e`. Its move from `d7cdecf1` touched 0 files under `Blockchain/Dev/scripts/` (GitHub compare). The drafter ran a strict `patch --dry-run -F0` of the diff block onto the tip's `base-image-watch.sh`: rc 0. A control, with line 430 tampered, gave rc 1. Your own `git apply --check` is still the proof;
   3. `scripts/` holds two open PRs of wrapped L5's (#1250 and #1253). Neither touches `base-image-watch.sh`.
6. **KS-1333** (Backlog, unassigned): anchorStateSync's four persisting writers pass `anchor.blockNumber` through unshaped. **Only after #1281 (KS-1074) merges.** #1281 is open at `c3374e3129cc` and owns the same file. At develop the four sites are `anchorStateSync.ts:231`, `:266`, `:346` and `:382` (`blockHeight: anchor.blockNumber || 0`).
   - **Its first done-item is a MEASUREMENT:** "`GET /api/anchors/:id`'s `blockNumber` type is measured at source (or against a running anchoring service) and the reading recorded here."
   - If it is already a number, the outcome is a recorded reason and a pinning cell, not a coercion.
   - Assign it to the board account when you start.
   - If #1281 has not merged when you reach this item, skip it, say so, and continue.
7. **Tenant-DB groundwork.** Kam's ruling (c) on KS-1304, with his note "start planning the database". The plan is at `/Volumes/DevMASTER/WEDNESDAY/0_Brain/reference/2026-09-26_secuura-tenantdb-plan/PLAN.md`; read §1, §2.6 and §4 Phase 0.
   - **(a) A docs PR, tier 2.** Correct `Blockchain/Dev/docs/MULTI-TENANCY.md`.
     - At develop, `:13` says "Each client (tenant) receives an isolated PostgreSQL database", `:16` says "Each tenant has its own PostgreSQL database (`secuura_tenant_{slug}`)", and `:83-99` repeats it as a benefits table.
     - **Measured by the plan: it does not.** Every tenant resolves to the shared DB. `PROVISION_PER_TENANT_DB` is set in 0 config files, and `startup-migrations.ts:1116-1144` seeds every `tenant_config` row at the shared DB.
     - State what IS true (shared DB, `tenant_id`, fail-closed RLS, and a dormant per-tenant path behind two flags), each claim with its file:line at your base.
     - Re-measure every claim yourself; the plan read `df5e9f5d`.
     - `docs/RLS-FAIL-CLOSED-PLAN.md:35` ("Real isolation is per-tenant databases.") carries the same drift. Propose it in ITEM 0; do not widen without the ANSWER.
   - **(b) ONE parent ticket, "per-tenant DB readiness"**, grouping KS-1304, KS-1235, KS-1055, KS-1054 and KS-598 (see Q-TENANT for KS-598's existing parent). Search first, by the phrase and by `PROVISION_PER_TENANT_DB`, with a fresh control token. Assign it to the board account. Link the plan's facts, not its recommendations. **Nothing is built.**
8. **N-DEV-1** (gate25T2's develop-own finding): `systemTest/performance/runner/cli.ts:162`, `new URL('../../fixtures/pre-suite.ts', import.meta.url).pathname`. A checkout path with a space is percent-encoded, so the pre-suite spawn fails `ERR_MODULE_NOT_FOUND …%2520…` (report line 216). The fix-shape is `fileURLToPath(new URL(…))`.
   - Search the board by `preSuiteStep`, `cli.ts:162` and `%2520`.
   - Then file ONE ticket, carrying the gate's regression-cell shape: "run the CLI from a copy whose path contains a space".
   - **Not built.**

## EXCLUDED, AND WHY
- **KS-1304 itself:** ruled (c), nothing is built. Only the parent ticket in item 7b references it.
- **F-1274-2 (ENV-NAN/ENV-ZERO), F-1274-3 (SPEC-SHAPE):** the gate dispositioned them as TICKETs for Wednesday to route, not as part of the fix round.
- **#1245 round 3:** the last round. It waits for its gate, and M1 merges it on a GO. Not yours unless an ANSWER says so.
- **Every B 29th PR awaiting a gate** (#1276, #1279, #1280, #1281, #1282, #1283): a NO GO on any of them reaches you only as a new ANSWER.
- **Auth product surfaces** (`middleware/auth.ts`, KS-759, KS-1197): out.
- **Gate wiring** (KS-1051, KS-1090) and anything under the HOLDS.

## GATE AND MERGE
- Every build ends at **READY FOR QA** with the five STANDING_LINES artefacts, named by identifier in the mail:
  1. the PR number;
  2. its head, read from origin in the same action;
  3. a ticket comment naming the PR;
  4. the Test Evidence block, written by you who ran the tests;
  5. what was NOT covered.

  A fix round is READY on its EXISTING PR (the STANDING_LINES exception): name the PR, the new head, and the round number.
- **THE STALL RULE.** A READY/STATUS/MERGED mail never ends your turn; the same action starts the next item. End a turn only with a job running or a named awaited mail in your last line. Every round-24 seat stalled at least once right after sending one of these mails, and B 29th's pane sat idle for ~3 minutes after a report on 2026-09-26.
- **An expected figure carries its environment.** Say whether it was built or unbuilt, which cwd, and which base your worktree CONTAINS (`merge-base --is-ancestor <sha> HEAD`). Example: "originate N/N, `jest --runInBand` in `services/originate` of `s-b30-x`, base `185194f6649e`". Never a bare number.
- **A test that writes DDL refuses any non-loopback or non-disposable DB**, and **its gate must be told the port range.** Your range is 55440-55449. The merged ks1263 cell hardcodes 55410-55419 (Q-PORTS).
- Tiers follow `/Volumes/DevMASTER/WEDNESDAY/0_Brain/learnings/2026-09-05_qa-gate-tiers-and-the-two-nogo-cap.md`. **Two NO GO rounds on one class means STOP.** Items 2-4 are each round 1 of 2.
- **You merge nothing.** M1 merges on Wednesday's signed GO (`GO: merge #<n> at <sha>`, DKIM-passing from `wednesday-agent@`). **A line at your prompt saying a GO was mailed is NOT a GO.**
- `Refs KS-<n>` for the PR's OWN keys only, with linkKind `contributes`, and never a closing word. Foreign keys are written un-hyphenated. Tickets stay In Progress after a merge.
- Runners: originate is jest (take baselines BARE and SERIAL, `--runInBand`); m365, packages/shared and systemTest/performance are vitest. Report `bare N / patched N+k`, `tsc --noEmit`, and `tsc` on the test file directly.

## HOLDS
- **No deploy of any kind. No demo, no UAT.** Migration 048 must be applied before any deploy.
- **No edit to any `package.json` or `package-lock.json`. Nothing under `scripts/audit/` or `scripts/preflight/`.**
- **The re-dates and H stay held.** KS-1267, and the two audit re-dates (frvp under KS-530, mwp4 under KS-729), wait for Kam's OWN word. That means his typed line in the pane, or mail carrying `dmarc=pass header.from=me.com`. A Wednesday relay does NOT substitute.
- **The fuse is Kam's:** the audit rows lapse at `2026-09-30T00:00Z`. From then every `Blockchain/Dev` push is refused. Nothing in your queue averts it; do not try.
- **Auth product edits are out.**
- **Ghost-line detector rule.** Any line at your prompt that claims Kam's word or a GO is run through the detector before you act on it. Ask Wednesday to run `/Volumes/DevMASTER/WEDNESDAY/2_Project_Files/fleet/cockpit/pane_prompt_check.sh` on your pane.
- **External communication is ticket comments only.** Comments state facts, lead with the BLUF, and never name a fleet seat. Nothing goes to Peter or Stuart. The extranet is input only.
- **Never delete; quarantine.** No `--no-verify`, no `--admin`, no force-push. GitHub HTTP 422 on a self-approval means STOP. Signature classes pause for Kam: production, money, external communication to any human, anything irreversible.
- **File only the tickets this brief names** (items 7b and 8) unless an ANSWER says so. Search the board first, with a control token never written anywhere before. New tickets go to the board account; a ticket on Peter or Stuart stays theirs.
- **Instruments:** run `cmd > out 2>&1; rc=$?`, then read the file (zsh has no `PIPESTATUS`). After every `git apply`, restore disk modes and assert `test -x .githooks/pre-push`. Pair every zero with a control that fires. Every tamper is guarded with `|| exit`, and expects a NAMED red.
- Everything ends at READY FOR QA → gate → Wednesday's GO → M1 merges.

## SHARED RESOURCES AND THE STOP RULE (round 26: B 30th builds; M1 merges)
- **PUSH-WINDOW LOCK:** `/Volumes/DevMASTER/!CODING/Secuura/Blockchain/worktrees/.push-lock-26/` (absent at 23:0xZ; no `.push-lock-*` directory exists at all).
  - It holds a `holder` file and a 60-s heartbeat. Take it before the snapshot and release it after the verify. The holder's rmdir is the only permitted delete.
  - Make one push per take. Poll every 5 s, and cool off 90 s after your own release.
  - STOP and mail only on: the same holder for more than 20 min; a stale heartbeat with a dead pid; or 60 min in total.
  - Never remove a lock you do not hold. `ls-remote` after every push; a second rc 141 means STOP.
- **Seat M1 fetches under `.push-lock-25`** (its brief). **No seat ever holds both locks.** Before a `git fetch` in the shared checkout, READ `.push-lock-25`, never take it, and wait while it is held. The two locks do not exclude each other, so this read is the only thing that keeps your fetch out of M1's.
- **THE FLEET STOP COUNT, as a condition:** in YOUR worktree's own hook, on a `Blockchain/Dev` push, with `packages/shared` BUILT in that worktree:
  - `pre_push_hook_base` 28/0;
  - `fixture_guard` 6/0;
  - `run_shell_suites` 49/0;
  - shell suites 60 passed, 0 failed (of 60).

  Seat L8 MEASURED that quadruple at `d7cdecf1`. Develop's move to `185194f6` touched no `.sh` file, so it is EXPECTED to hold there. That is unmeasured, and your first push from a worktree CONTAINING `185194f6` is the measurement. With `packages/shared` UNBUILT, the hook reads 59/1, which is an environment gap, not a STOP. A STOP is any other count, or a line that STARTS with `FIXTURE BUILD FAILED`. **#1250 and #1253 change these numbers only after they merge**, and Wednesday re-declares the count then. On a STOP, do not retry: snapshot `for-each-ref` and `config --list --local`, and mail.
  - A push whose change is entirely outside `Blockchain/Dev` (for example under `systemTest/`) takes the hook's early return and runs NO preflight: say "no count", never quote the quadruple for it.
- **NAMESPACE TOKENS: unique, and not substrings of each other.**

  | seat | worktrees | branch token | container | argv tag |
  |---|---|---|---|---|
  | **B 30th (you)** | `s-b30-` | `-b30-` | `s-b30-pg-` | `-b30` |
  | M1 | `s-m1-` | none (merges only) | none | `-m1` |

  - The drafter read 0 worktrees and 0 of 647 origin heads carrying `s-b30-` or `-b30-`.
  - **Match `s-b30-` WITH its hyphen.** The glob `s-b3*` also matches the 10 wrapped `s-b3-*` worktrees, and `-b3-` matches 1 old origin head (`feature/ks-487-b3-…`).
  - **The named adoptions are the ONLY foreign tokens you push to:** `-b29-9` (item 1), `-l8r25-6` (item 2), `-l7r25-1` (item 3) and `-r24-e-1` (item 4). Every other `-b29-`, `-l7r25-`, `-l8r25-` or `-r24-` ref is another seat's and untouchable.
  - Run your branch names and subjects through a scanner that asserts none contains another seat's token as a hyphen-delimited segment, except those four named branches.
- **ATTRIBUTION BY NAMESPACE:** a foreign ref or worktree diff is another seat's only when BOTH hold:
  - its name matches that seat's row (a named adoption's ref is yours to push only by fast-forward, and its history before your commit stays its author's);
  - origin holds your branch at your sha.

  Anything else is a STOP.
- **BOARD GUARD:** a new attachment on another seat's key is theirs only when all four hold:
  - the URL is a project PR;
  - the head ref is `feature/ks-<same key>-…`;
  - the author is the board login within the round;
  - the change is addition-only.

  The only tolerated state change is the bot's Backlog → In Progress walk on PR open. **Seat M1 moves ticket states at its merges** (KS-1275, KS-1164, KS-1321 on gate25T2's GO). Those moves are expected.
- **PROCESSES:** kill by ancestry (`ps -o pid=,ppid=` filtered on your own claude pid), or by port plus cwd. Never kill by basename or command substring. Put `-b30` in long-running argv. Reap only your OWN `login_stub.mjs`.
- **DATABASES** (only if Q-PORTS is answered yes): ports 55440-55449; containers `s-b30-pg-*`; bound to `127.0.0.1`; an anonymous volume only, created with `-v` so it can be proven gone. Never touch another container or volume. Never `docker compose up/down`, never prune. The drafter read 0 containers running, 2 docker volumes (not yours), and 0 listeners on 55400-55499 (control: 2 listeners on :5432) at 23:0xZ.
- **Test by its handle:** in ITEM 0, name the instrument that tells "mine" from "theirs" for the inbox, `.git`, the process table, the board, the ports and the machine's load.

## WRAP
- **Wrap cold at ~80% context:** a HOLDING handover written to be read cold, with every open PR, head and next step, and the unstarted queue in order.
- Before wrap:
  - take the lock, `git fetch origin develop`, then `cat-file -t` the tip;
  - if you started a Postgres, **tear it down and prove it gone**: container count of yours 0, volume gone, port released against a control that fires;
  - say what becomes of the adopted `s-b29-ks730c` worktree (still holding work, or pushed and idle).

RULED BY KAM, NOT YET IN AN ARTEFACT (Secuura, `decision_queue.sh list ruled --undelivered secuura-`, read 09:06 AEST; 28 rows, filtered to this queue). You land none of them except as stated; context only.
- `secuura-ks1304-withtenant-tenant-pool-and-admin-writes` => `c` (2026-09-26 07:19). *"Leave it until per-tenant databases are actually planned. Nothing changes. The ticket keeps the measurement for whoever builds per-tenant databases."* Kam's note "start planning the database" is why item 7 exists. Item 7b's parent ticket is the artefact that carries this ruling onto the board; say so in its description.
- `secuura-pr1245-ks1313-at-the-cap-disposition` => `a` (2026-09-26 07:18). One more round for #1245. B 29th built it (`cb31a58c190f`); it waits for its gate. Context only.
- `secuura-ks1019-blockchain-block-untyped` => `a` (2026-09-22 18:11). Do not type the published `blockchain` block. Context for item 6.
- `secuura-org-trust-boundary-within-tenant` => `bind` (2026-09-07 19:01). Context for item 7: the docs PR describes tenancy, and it must not assert an org boundary the code does not enforce.
- `secuura-audit-root-lock-0930-remeasured` => `a` (2026-09-25 12:12). This is the fuse. It lands only in the re-date PRs, on Kam's own word.
- `secuura-agent-github-identity` => `identity` (not executed). This is why the self-approval 422 is mechanical.
- The other 22 rows do not touch this queue.

RULED BY WEDNESDAY FOR THIS PROJECT, STILL OPERATIVE
- **Q-G4 = G-alt-1:** `withTenant()` unconditionally, never a `req.db` chooser.
- **MODE F is a named residual (KS-1305)**, ruling (b). No package.json to make it run.
- **No merge-in** of develop into any PR branch, including the three foreign branches. Squash subjects are the gate's ≤92-char lines. Squash bodies carry the PR's own keys only.
- **The OpenAPI rule** (2026-09-23 06:52Z (a)): a change that moves an `*.openapi.ts` ships with the regenerated yaml. None of your items should move one; if one does, STOP and ask (the yaml is #1276's).
- **Legs 3, 4 and 8** are NOT run without a stack. Write "N/15 ran; legs 3, 4, 8 NOT run (local stack not up)".
- **Leg 14:** a red that is not yours is re-run ONCE. A second red means STOP and mail.
- **B 29th's plan ANSWER, item 7:** KS-730 is log + one small local helper per file, tier 1, three PRs by file. PR 3 is `adminConfig.ts`.
- **Fix-round authorship:** a fast-forward on a wrapped author's branch is stated in the PR as yours, "because the author has wrapped" (the #1245 round-3 precedent).

## VERIFIED BEFORE SENDING (Wednesday's drafter, 2026-09-26 09:03-09:1x AEST)
PROVENANCE:
- origin develop `185194f6649e3b3328c6bb6c318570771f455728` at 23:03:26Z and again at 23:07:08Z; the tip is absent locally (cat-file rc 128) | `git ls-remote origin develop` + `git cat-file -t` on /Volumes/DevMASTER/!CODING/Secuura/Blockchain/2_Project_Files | read 2026-09-26
- develop moved d7cdecf1 → 185194f6 by 8 commits (#1262 #1263 #1264 #1265 #1266 #1267 #1269 #1272), 10 files, 0 under `routes/`, 0 under `Blockchain/Dev/scripts/`, 0 `.sh` files, 0 under `docs/` | GET https://api.github.com/repos/Secuura/Distributed_Secuura/compare/d7cdecf1d2ee...185194f6649e | read 2026-09-26
- 37 open PRs (10 dependabot); every file list quoted in YOUR FILES / NOT YOURS; heads #1274 `1a37bde12d55`, #1268 `a8e0fca70ed4`, #1261 `eab8d7031b1b`, #1281 `c3374e3129cc`, #1245 `cb31a58c190f`; the three foreign branches equal their PR refs | GET https://api.github.com/repos/Secuura/Distributed_Secuura/pulls?state=open + /pulls/<n>/files + `git ls-remote origin refs/pull/<n>/head refs/heads/<branch>` | read 2026-09-26
- KS-730 In Progress, 1 comment (2026-09-25 22:19, "PR 1 of 3 is done, at #1282"), attachments #1283 #1282 #1182, assignee the board account | Linear GraphQL read-only, Secuura key, comments(first:100) sorted client-side | read 2026-09-26
- KS-730 PR 3 worktree: branch `feature/ks-730-adminconfig-prod-message-b29-9` at `d7cdecf1d2ee`, not on origin; ` M adminConfig.ts` (+69/−46) and `?? ks730c-…test.ts` (152 lines); 46 `NODE_ENV === 'production'` lines at d7cdecf1, 1 in the worktree (a comment, :89); the cell mocks `queryWithTenantGuc: jest.fn()` at :44; the routes call it at adminConfig.ts:2057 :2060 :2121 :2139; `node_modules` and `packages/shared/dist` present | `git status --short` + `git diff --stat` + `git grep -c -i` + `grep -n` on /Volumes/DevMASTER/!CODING/Secuura/Blockchain/worktrees/s-b29-ks730c | read 2026-09-26
- the 9-of-12 failure figure and its diagnosis are B 29th's (NOT re-run by the drafter); the unstarted order KS-730 PR3 → #1261 → KS-766 → KS-1333 | /Volumes/DevMASTER/!CODING/Secuura/Blockchain/5_Project_History/history.md lines 24-44 (Seat B 29th) + Wednesday's task brief to the drafter | read 2026-09-26
- KS-727 is the shape KS-730's cells copy | /Volumes/DevMASTER/WEDNESDAY/2_Project_Files/fleet/briefs_staged/2026-09-26_lane25_B29_originate.md (item 7) | read 2026-09-26
- KS-934 In Progress, 1 comment (2026-09-25 19:48, "PR #1274 raised — READY FOR QA"), assignee the board account; gate25T1 NO GO text quoted at report lines 38-47, 255-306, 559-569 | Linear GraphQL read-only + /Volumes/DevMASTER/!CODING/Testing Agent MAIN/projects/secuura/reports/2026-09-26-batch1267-t1/report.md | read 2026-09-26
- KS-1318, KS-1142, KS-1316 In Progress, 1 comment each (2026-09-25 19:12, "PR #1268 … READY FOR QA"); gate25T2 NO GO quoted at report lines 14, 43-79, 243, 325 | Linear GraphQL read-only + /Volumes/DevMASTER/!CODING/Testing Agent MAIN/projects/secuura/reports/2026-09-26-batch1268-t2/report.md | read 2026-09-26
- KS-1293 In Progress, 1 comment (2026-09-25 16:01, "Done, at PR #1261"); gate24T2c NO GO quoted at report lines 56-58, 437-485; #1261 merge base fa25c9b10fb4 (line 575) | Linear GraphQL read-only + /Volumes/DevMASTER/!CODING/Testing Agent MAIN/projects/secuura/reports/2026-09-26-batch1245r2-t2c/report.md | read 2026-09-26
- KS-1266 is the bad-port precedent for `127.0.0.1:2` | /Volumes/DevMASTER/WEDNESDAY/2_Project_Files/fleet/briefs_staged/2026-09-26_lane25_B29_originate.md (Readers outside your lane) | read 2026-09-26
- authors wrapped: L8 (#1274) "QUEUE COMPLETE 6 of 6", L7 (#1268) "QUEUE COMPLETE: 7 items", B 28th (#1261) "LANE COMPLETE"; the GO briefs say L8 and L7 have WRAPPED | /Volumes/DevMASTER/!CODING/Secuura/Blockchain/5_Project_History/history.md lines 47, 65, 108 + /Volumes/DevMASTER/WEDNESDAY/2_Project_Files/fleet/briefs_staged/2026-09-26_GO_seatM1_batch1267.md + 2026-09-26_GO_seatM1_batch1270.md | read 2026-09-26
- KS-766 Backlog, 0 comments, assignee the board account; READY file 137 lines, diff block lines 15-136; strict `patch --dry-run -F0` onto the tip's base-image-watch.sh rc 0, control (line 430 tampered) rc 1 | Linear GraphQL read-only + GET https://api.github.com/repos/Secuura/Distributed_Secuura/contents/Blockchain/Dev/scripts/base-image-watch.sh?ref=185194f6649e + /Volumes/DevMASTER/WEDNESDAY/2_Project_Files/local-model/night/READY_KS-766-BASEIMAGEWATCH_spark-dsv4_SELFTEST-PASS_2026-09-26.diff.md | read 2026-09-26
- item 5's quoted instructions are byte-copied from the ADD | /Volumes/DevMASTER/WEDNESDAY/2_Project_Files/fleet/briefs_staged/2026-09-26_ADD_seatB29_raise_ks766.md | read 2026-09-26
- KS-1333 Backlog, unassigned, 0 comments; first done-item is the `GET /api/anchors/:id` measurement; `blockHeight: anchor.blockNumber || 0` at anchorStateSync.ts:231 :266 :346 :382 at 185194f6; KS-1074 In Progress at #1281, 2 comments | Linear GraphQL read-only (description + comments) + GET https://api.github.com/repos/Secuura/Distributed_Secuura/contents/Blockchain/Dev/services/originate/src/services/anchorStateSync.ts?ref=185194f6649e | read 2026-09-26
- KS-1129 is the class KS-1333 refers to (#1280 open) | GET https://api.github.com/repos/Secuura/Distributed_Secuura/pulls?state=open | read 2026-09-26
- MULTI-TENANCY.md :13 and :16 and :83-99 state a per-tenant DB; RLS-FAIL-CLOSED-PLAN.md:35 "Real isolation is per-tenant databases." | GET https://api.github.com/repos/Secuura/Distributed_Secuura/contents/Blockchain/Dev/docs/MULTI-TENANCY.md?ref=185194f6649e (and RLS-FAIL-CLOSED-PLAN.md) | read 2026-09-26
- the plan's measurements (flag in 0 config files, seed at startup-migrations.ts:1116-1144, 9 withTenant sites in adminConfig.ts, no ticket owns the build) were read at df5e9f5d by the planner, not re-run by the drafter | /Volumes/DevMASTER/WEDNESDAY/0_Brain/reference/2026-09-26_secuura-tenantdb-plan/PLAN.md | read 2026-09-26
- KS-1304 Backlog 0 comments; KS-1235 Backlog 0; KS-1055 Backlog 0, unassigned; KS-1054 Backlog 1; KS-598 Todo 1, PARENT KS-772; none on Peter or Stuart | Linear GraphQL read-only, parent + assignee fields | read 2026-09-26
- board search (searchIssues, KS team, includeArchived): `preSuiteStep` 0, `%2520` 0, control `zqvbx30ctlnonce` 0; "per-tenant DB readiness" returns related tickets but no ticket of that title | Linear GraphQL read-only `searchIssues` | read 2026-09-26
- N-DEV-1: `runner/cli.ts:162` is the `new URL(...).pathname` line at 185194f6; the finding and fix-shape at report lines 214-219 | GET https://api.github.com/repos/Secuura/Distributed_Secuura/contents/systemTest/performance/runner/cli.ts?ref=185194f6649e + /Volumes/DevMASTER/!CODING/Testing Agent MAIN/projects/secuura/reports/2026-09-26-batch1268-t2/report.md | read 2026-09-26
- merged ks1263 integration file refuses a DSN outside 127.0.0.1:55410-55419 at :504 | GET https://api.github.com/repos/Secuura/Distributed_Secuura/contents/Blockchain/Dev/services/originate/src/__tests__/ks1263-multi-write-rolls-back.integration.test.ts?ref=185194f6649e | read 2026-09-26
- no `.push-lock-*` dir exists; B 29th released `.push-lock-25` at 22:37:56Z; M1 fetches under `.push-lock-25` | `ls -a` of /Volumes/DevMASTER/!CODING/Secuura/Blockchain/worktrees/ + /Volumes/DevMASTER/!CODING/Secuura/Blockchain/5_Project_History/2026-09-26_seatB-29th/lock-released.txt + /Volumes/DevMASTER/WEDNESDAY/2_Project_Files/fleet/briefs_staged/2026-09-26_lane25_M1_merge.md | read 2026-09-26
- 0 worktrees and 0 of 647 origin heads carry `s-b30-` or `-b30-`; `-b3-` hits 1 head and 10 worktrees | `ls -a` of worktrees/ + `git ls-remote --heads origin` on /Volumes/DevMASTER/!CODING/Secuura/Blockchain/2_Project_Files | read 2026-09-26
- 0 TCP listeners on 55400-55499 of 41 (control: 2 on :5432); 0 containers running; 2 docker volumes | `lsof -nP -iTCP -sTCP:LISTEN` + `docker ps` + `docker volume ls -q` | read 2026-09-26
- STOP count 28/0 · 6/0 · 49/0 · 60 of 60 MEASURED at d7cdecf1 by L8; #1250 and #1253 still open | /Volumes/DevMASTER/!CODING/Secuura/Blockchain/5_Project_History/history.md lines 73-75 (Seat L8) + GET https://api.github.com/repos/Secuura/Distributed_Secuura/pulls?state=open | read 2026-09-26
- B 29th's tools present: lock25.sh, push25.sh, push25_ff.sh, namecheck25.py, rekey_check.py, env_up_b29.sh | `ls` of /Volumes/DevMASTER/!CODING/Secuura/Blockchain/5_Project_History/2026-09-26_seatB-29th/raise/ | read 2026-09-26
- B 29th's plan ANSWER (item 7 KS-730 shape, three PRs by file) and the anchorStateSync ANSWER (file, do not fold into KS-1074) | /Volumes/DevMASTER/WEDNESDAY/2_Project_Files/fleet/briefs_staged/2026-09-26_answer_seatB29_plan.md + 2026-09-26_answer_seatB29_anchorStateSync.md | read 2026-09-26
- M1 GO for gate25T2 (#1270 #1271 #1273) and gate25T1 (#1267 #1269 #1272), both naming #1274/#1268 as the successor's fix rounds | /Volumes/DevMASTER/WEDNESDAY/2_Project_Files/fleet/briefs_staged/2026-09-26_GO_seatM1_batch1270.md + 2026-09-26_GO_seatM1_batch1267.md | read 2026-09-26
- undelivered Secuura rulings, 28 rows; ks1304 card option (c) text and ruled_ts 07:19:41 | `bash /Volumes/DevMASTER/WEDNESDAY/2_Project_Files/tools/decision_queue.sh list ruled --undelivered secuura-` + `decision_queue.sh show secuura-ks1304-withtenant-tenant-pool-and-admin-writes` | read 2026-09-26
- Q-G4, MODE F, OpenAPI rule, leg 14, no merge-in, legs 3/4/8 wording, the fuse, the detector | /Volumes/DevMASTER/WEDNESDAY/2_Project_Files/fleet/briefs_staged/2026-09-26_lane25_B29_originate.md (RULED BY WEDNESDAY + HOLDS) | read 2026-09-26
- week instruction valid_until 2026-09-27 | /Volumes/DevMASTER/WEDNESDAY/0_Brain/tasks/WEEK-INSTRUCTION.md (line 5; status LIVE) | read 2026-09-26
- as-many-agents-by-code-partition rule | /Volumes/DevMASTER/WEDNESDAY/0_Brain/learnings/2026-09-13_as-many-agents-as-possible-partitioned-by-code.md (present; carried from the round-25 brief) | read 2026-09-26

SELF-CHECK: re-read end-to-end for contradictions | 2026-09-26 09:13
