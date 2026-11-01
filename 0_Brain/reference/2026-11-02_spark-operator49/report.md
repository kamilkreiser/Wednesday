# Spark operator 49, 2026-11-02: KS-1898, KS-1868 security x2, KS-1868 billing, KS-1841
Written by the operator (Bash heredoc). Run folder: this directory (briefs/generators in gen/, outputs ctl*/rnd*/hold*).

## BLUF
Four tasks, five held PASSes, all 7/7, all BYTE-IDENTICAL to the golden, all strict, all on the ORIGINAL brief (no rebrief spent). No task skipped: the final open-PR scan (22 PRs, 128 files, read at the end; the start scan was 23 PRs, 134 files) shows no open PR touching any briefed product or test file. PR 1897 is open (mcp-server); 1894, 1895, 1896 are no longer open. Tip: began at develop d7691f35312e; develop moved during the session (8126b22bd5aa, ad78fa106785, ca36945e9740), round.sh read the new tip each round, none of the named files changed; per-row tips are in done.md.

## Held (pasted from ls)
See held_files.txt in this folder (copied below by the operator at the end of the run).

## Per task
### 1. KS-1898 (vc-issuer ks1851 revoke test), tier test_only, tip d7691f35312e
- hold_ready: golden: BYTE-IDENTICAL; touched=1 product_plus=31 product_minus=4 red=13/36 green=36/36 suite=710->714 strict=True kind=test_only product_unchanged=True
- Change: V8b-g (shared it.each body) and V9 get `expectNothingLoggedForTheRefusal()` + `expectByteIdentical(refused, unknown-id answer)`, titles extended; NEW memory-path owner-less cell V14a-d (store with default OWNERLESS owner, four same-tenant callers incl. SUPER_ADMIN, byte-identical, unchanged, not logged). Ticket named V8b-e; V8f/V8g share the body and are declared red too.
- Red proof: tamper at credentials.ts:306, a one-line conditional on `record.owner.userId === null` that logs the reason and adds `details` to the body. 13 declared cells red by assertion, 36/36 green at the tip, whole vc-issuer suite no new red, tsc rc 0.
- Control r1 FAILED (my defect): the first tamper fired for owned-row refusals too, so the existing control cells V2-V13/D2 went red (A4 "red but not for the right reason"); narrowed, control r2 PASS.
- Caveat: the red proof is a PLANT chosen by me (an owner-less-only divergence plus a log call). It proves the added assertions can fail; it does not prove they catch every regression.

### 2. KS-1868 security/src/index.ts :293 (P1) and :400 (P2), code_patch2, sequenced
- P1 hold_ready: golden: BYTE-IDENTICAL; touched=2 product_plus=7 product_minus=1 red=2/3 green=3/3 suite=372->375 strict=True. P2 identical line (suite 372->375).
- Combined: both product hunks applied with `patch` in order to the tip file, textually OK (disjoint: old-side 289-296 and 396-403). Combined tests and tsc are UNMEASURED (as O47).
- Callers and the behaviour each raise PR must state:
  - :293 revokePriorConnectorKeys: callers are saveKeyAndRetirePriors :380 and the ks577 test seam. :380 is inside the `!isDbAvailable()` branch and revokePriorConnectorKeys returns at :280 BEFORE its try when the DB is unavailable, so through the route the :293 catch is reachable only if availability flips between two reads. In that window a hostile throw today makes the route (:1399) answer 503/500 "could not be saved" and drop the key; after the fix it returns null and the route answers 201 with priorKeysRevoked null. Mostly a test-seam / defence-in-depth fix.
  - :400 inside the rotate transaction (route :1395, only when `rotate && connectorId`): **BEHAVIOUR CHANGE.** A hostile throw from the retire UPDATE today throws out of the transaction callback after ROLLBACK TO SAVEPOINT, db.ts transaction() issues a full ROLLBACK, the route answers 500/503 "no key was issued", nothing committed, prior key still live. After the fix the savepoint catch returns null, the transaction COMMITs, the NEW KEY IS MINTED, the prior key stays active, and the 201 carries priorKeysRevoked: null, exactly what an ordinary retire error already does (KS-577 contract). The raise PR must say this: a rotate that used to refuse now mints and tells the caller the old credential is still live.
- Test design: direct calls (no app), console.log spy (the service logs via console.log JSON), outcome captured with `.then(ok, rejected)` so the hostile value never reaches an assertion message; P2 mocks `transaction` with a stand-in client rejecting only the `UPDATE svc_api_keys` statement and asserts `ROLLBACK TO SAVEPOINT ks1549_retire` ran and the key is in memApiKeys.
- Controls PASS first time for both.

### 3. KS-1868 billing/src/routes/webhooks.ts :316 replay handler, code_patch2
- hold_ready: golden: BYTE-IDENTICAL; touched=2 product_plus=7 product_minus=1 red=2/3 green=3/3 suite=328->331 strict=True. Tip ca36945e9740 (control at ad78fa10, file unchanged).
- Response stays the constant 500 `{success:false,error:{code:'INTERNAL_ERROR',message:'Replay failed'}}` in the cells (full-body toEqual in all three cells). Behaviour change to state: a hostile throw today leaves the admin replay request UNANSWERED (Express 4 does not see the async rejection); after the fix it answers the same constant 500 an ordinary DB error gets, logging `error: unreadable thrown value`. The route is admin-only and not gateway-routed. Note (unchanged by this PR): handleWebhookEvent's credit grant runs before the status UPDATE, so a throw from the UPDATE leaves credits granted and status unchanged in both old and new code.
- Harness: webhooks-replay-auth.test.ts pattern (real router, real shared authenticate(), RS256 token, loopback listener); unhandled rejection counted by the test, not the runner.

### 4. KS-1841 api-gateway/Dockerfile:34-35, code_patch2 (1 Dockerfile hunk, 1 existing test edited in 3 hunks, 1 NEW test)
- hold_ready: golden: BYTE-IDENTICAL; touched=3 product_plus=2 product_minus=2 red=6/13 green=13/13 suite=1368->1373 strict=True.
- New line: `RUN find ./docs/openapi -mindepth 1 -maxdepth 1 ! -name secuura-api.yaml -exec rm -rf {} +` (one level deep, rm -rf so a folder is also removed, exit 0 when nothing matches; the ticket's `-delete` variant would fail on a non-empty subfolder).
- Proof (no docker daemon): the NEW ks1841 vitest reads the Dockerfile's own RUN line and runs it with `sh -c` in a temp tree holding the spec, eight missed name shapes (.bak, ~, .orig, .swp, prefixed copy, WORKFLOWS.md, pre-ks508, rollback-...) and a folder; asserts only secuura-api.yaml remains byte-identical, idempotent, plus a control showing the old two-glob command leaves the gap. Red at the tip by assertion (no find line).
- The existing ks1823 test pinned the old command (R1/R2/R3 would go red), so R1/R2 were rewritten, RM_LINE updated, C3's `\brm\b` filter narrowed to `RUN rm` lines.
- NOT done, raise seat owns it: the docs fragments describing the two-glob line (Projects Documents/fragments/cheat/legacy/0104-..., flow/legacy/0108-..., and the two big HTML pages) are now stale; whether the repo's docs-fragments check or pre-push requires them is UNMEASURED. BusyBox find (alpine) not exercised; only host sh/find in the fixture; no docker build.
- Control failed twice before PASS (my brief defects, no model call): r1 A2b (deleting a cell), r2 A4 (edited existing cells red without the product hunk must be declared in Red cells), plus a blank context line refused by build_input.

## Generator lessons (also appended to IMPROVEMENTS.md)
Narrow tamper; modified-test cell count / Red cells declaration / context n=1; assert-before-run for a command read from product; control re-runs go to -control-rN; hold_ready arguments; develop moves mid-session.

## Model behaviour
No failed model round: 4 of 4 first-sample PASS, byte-identical. Model times 49.6 / 64.1 / 75.3 / 50.9 / 60.3 s. The backslash briefs (KS-1898, KS-1841) carried an explicit "keep every backslash" warning and passed.

## UNMEASURED
Combined tests and tsc of P1+P2 together; BusyBox find in the real image; docker build; the real transaction() ROLLBACK/COMMIT (the P2 stand-in does not emulate it, the old behaviour is read from db.ts:59-70 not run); real Postgres; the docs-fragments check; eslint; whether live lanes beyond open PRs touch these files; the Linear ticket text of KS-1898/1841 was taken from Wednesday's screen, not re-read.

## Held files (ls night | grep O49)
READY_KS-1841-KS-1841-O49-P4_spark-dsv4flash_BRIEFED-CODEPATCH2-GATEWAY-DOCKERFILE-FIND-KEEPS-ONLY-SPEC-PASS-7of7_2026-11-02.diff.md
READY_KS-1868-KS-1868-O49-P1_spark-dsv4flash_BRIEFED-CODEPATCH2-SECURITY-REVOKE-PRIOR-CONNECTOR-KEYS-PASS-7of7_2026-11-02.diff.md
READY_KS-1868-KS-1868-O49-P2_spark-dsv4flash_BRIEFED-CODEPATCH2-SECURITY-SAVE-KEY-AND-RETIRE-PRIORS-PASS-7of7_2026-11-02.diff.md
READY_KS-1868-KS-1868-O49-P3_spark-dsv4flash_BRIEFED-CODEPATCH2-BILLING-WEBHOOK-REPLAY-PASS-7of7_2026-11-02.diff.md
READY_KS-1898-KS-1898-O49-P1_spark-dsv4flash_BRIEFED-TESTONLY-VCISSUER-REVOKE-BYTE-IDENTICAL-PASS-7of7_2026-11-02.diff.md
