## QA GATE 59, TIER 1, ROUND 1: KS-1851 #1869

**BLUF: GO WITH NOTES.** The revoke route at `6c150b5a` uses the same check as `GET /api/credentials/:id`: the same `getRecordById` call, then `!record || !mayRead(req, record.owner)`, then the same `AppError('Credential not found', 404)`. It works on both storage paths. The check runs before anything is written. A refused caller gets a response identical to an unknown id. `reason` is not logged on a refusal. The change adds no new role and no admin bypass. All 24 refused-caller cells fail at base for the product reason, "expected 200 to be 404". I wrote 12 mutants of my own and all 12 were killed. The head merges cleanly onto develop `007cc464`. Nothing here blocks the merge. There are two minor findings: the "nothing is logged" wording is wrong (the shared error handler writes one error-level line for each refusal, the same line an unknown id gets, and it never contains `reason`), and the refusal cells for owner-less rows assert less than the others. The remaining notes are file-only, for Kam's deferred revoke question.

- PR https://github.com/Secuura/Distributed_Secuura/pull/1869 · ticket KS-1851 · author Seat E 22nd · commissioned by Wednesday, Sat 31 Oct 2026
- **Head at START** (10:44:02 UTC, `git ls-remote`): `refs/pull/1869/head` = `6c150b5aff1dbd8eaebc4092358b04d674f82ab5`, develop = `007cc464b063d7cf0733257fd44a570aea1c964b` (`evidence/lsremote_start.txt`)
- **Head at END** (10:58:00 UTC): `refs/pull/1869/head` = `6c150b5aff1dbd8eaebc4092358b04d674f82ab5`, develop = `007cc464b063…`. **Unchanged** (`evidence/lsremote_end.txt`)
- Clone: `0_Brain/reference/2026-10-31_gate59-ks1851-1869/repo`. `rev-parse --show-toplevel` equalled the clone directory before any fetch. The clone was left at the head and its working tree is clean (0 tracked changes after mutants and base swaps were restored).
- Host: Apple Silicon Mac, Node v26.8.1. **This is not an LTS run.** Node 24 was not measured, the same gap E reported.

## VERDICT: GO WITH NOTES

## Findings

**G59-F1 · minor (docs accuracy, fix-before-merge only if cheap).** Three places say a refused revoke has "nothing written or logged": the cheat fragment (`Projects Documents/fragments/cheat/KS-1851-…html`), the flow fragment, and the header of the test file (lines 8-9). Not true. The live `@secuura/shared` `errorHandler` (`packages/shared/src/errors/index.ts:236`) logs `logger.error('Error occurred', {error, stack, code, statusCode})` for every refusal. Measured: the head run's stdout carries 43 `Error occurred` lines whose stack points at `credentials.ts:302:13`. That is the same throw site an unknown id uses, so the line cannot tell the two apart. `ks1851-reason-marker` appears **0** times. Control: `Credential not found` appears 86 times in the same stdout, so the shared logger's output was visible to the grep. The D3 requirement ("`reason` is not logged for a refused call") **is met**. Only the stronger wording is wrong. Fix: reword to "nothing is written, and `reason` is not logged". The test's `expectNothingLoggedForTheRefusal` watches only the vc-issuer logger mock, so it cannot see the shared logger. Spying on the shared logger as well would make the assertion cover what its name says.

**G59-F2 · minor (test strength, before-deploy or a follow-up).** The refusal cells for owner-less rows (V8b, V8c, V8d, V8e, V9×2) assert 404 plus no UPDATE. They do **not** assert that the body is byte-identical to an unknown id's, and they do not run `expectNothingLoggedForTheRefusal`. Both are asserted only for the FOREIGN_CALLERS cells. There are also no owner-less cells on the memory path. There is no live gap: every refusal goes through the one `throw` at `:302`. But my mutants M5 (403 on refusal) and M6 (different message) were killed only by the V2–V13b cells. A future split of the branch for owner-less rows would get past the V8b–V9 cells.

**G59-F3 · file-only (for Kam's deferred tenant-admin revoke question).** Revoke now gives a tenant administrator **write** access to an owner-less row stamped with that administrator's tenant: ORG_ADMIN or SYSTEM_ADMIN with a userId (cells V8×2 pin 200). This comes from `ownerlessRowReadable` (`ownership.ts:92-97`, KS-1116 ruling (a), card `secuura-ks1116-null-owner-who-reads-1020`). It is **not** a widening. Develop let every authenticated caller revoke, and the head is exactly the KS-1116 read rule. D3 and brief line 55 order exactly this. Two points for Kam. First, card `secuura-ks1695-ownerless-records-who-reads-1020` = b names "Platform S's connectors and platform administrators only" for owner-less records, while `ownership.ts` admits tenant administrators. The divergence predates this PR and lives in `ownership.ts`, but revoke now inherits it as a write. Second, the cheat fragment states this admission openly. That is honest, but it is part of the deferred tenant-admin question.

**G59-F4 · file-only (defence in depth).** `credentialRepo.revoke` itself is still unbound, and it re-reads the row with `getById` after the route's `getRecordById`. It has one non-test caller, the route (`credentials.ts:305`), and the brief's grep confirms this. No code path changes a row's owner: no `UPDATE … created_by_*` exists anywhere in `Blockchain/Dev`, the INSERT's `ON CONFLICT` rewrites only `credential`, and `memoryOwners` is set only if absent. So the double read is **not** a TOCTOU today. A future second caller of `revoke()` would be unbound.

**G59-F5 · file-only (scope clarity).** A second revoke surface, `POST /api/status/:id/revoke` and `/unrevoke` (`status.ts:247`, `:304`), is still gated by platform role (`STATUS_WRITE_ROLES`, KS-692 interim posture), not by `mayRead`. The PR title holds for `/api/credentials/:id/revoke` only. Out of scope; tracked on KS-692.

**G59-F6 · file-only (existing behaviour, unchanged).** The owner can revoke an already-revoked credential again, which overwrites `revokedAt` and `revocationReason`. This PR does not change that.

## Q1. Same predicate as GET, on both paths?
**FOUND: yes.** The GET handler `credentials.ts:273-279` and the revoke handler `:300-303` are token-identical: `const record = await credentialRepo.getRecordById(id); if (!record || !mayRead(req, record.owner)) { throw new AppError('Credential not found', 404); }`. `getRecordById` (`credentialRepo.ts:137-161`) returns the owner from whichever path found the row: `ownerFromRow(row)` on the database path, `memoryOwners.get(id) ?? OWNERLESS` on the memory path. So the same `mayRead` decides on both. Of the four product files, only the route differs between the head and develop: the `credentialRepo.ts`, `ownership.ts` and route blobs are equal at `85cd24d8`, `ddc644fb` and `007cc464`, and only `credentials.ts` changes at the head.
**TESTED:** memory-path cells (V1, V2–V13b, V5) and database-path cells (D1, D2×9, V8–V9) are 29/29 green at the head. Mutant M12 forces the owner to OWNERLESS, i.e. a check that ignored the row's owner. Killed (4 cells).
**HOW:** read both handlers at `6c150b5a`; `git rev-parse` of the blobs at each commit.

## Q2. Strictly before any write or side effect? TOCTOU?
**FOUND: yes, before every write.** On a refusal the route throws before `credentialRepo.revoke`. That function does the memory `set` (`:458`) and the `UPDATE` (`:464`), and `logger.info('Credential revoked', {reason})` comes after it (`:311`). The revoke route has no status-list update, no event emit and no cache. The row is read twice (`getRecordById`, then `getById` inside `revoke`), but no owner mutation path exists (G59-F4), so there is no TOCTOU. A Map-miss on the memory path (KS-1116 Q1) yields OWNERLESS with a null tenant, which `mayRead` refuses for everyone: it fails closed.
**TESTED:** M3 moves the check after the write. Killed (24 cells: on the memory path the stored copy changed, on the database path an UPDATE was issued). The D2 cells assert `updates()` = [] on refusal, and the memory cells assert the stored JSON is unchanged.
**HOW:** read the repo and the route; grep for writers of `vc_credentials_store` across `Blockchain/Dev` (the only UPDATE is `credentialRepo.ts:465`). Control: the same grep finds the 4 migration/init files and that UPDATE.

## Q3. No existence oracle; `reason` not logged on refusal?
**FOUND: no oracle.** Refused and unknown share one `throw` (`:302`, the `!record ||` disjunct), so status, body, error class and code are identical. The route sets no headers. `requestLogger` logs method/path/status only, never the body. Both paths do the same database work: one `getRecordById` and no `revoke()`. The shared error handler logs an identical error line for both, and it never reaches the response. **`reason` is not logged on refusal** (G59-F1 has the measurement and its control). The wording that says nothing is logged is wrong (G59-F1).
**TESTED:** `expectByteIdentical(refused, unknown)` in 18 cells. M5 (403) and M6 (different message) were killed, 24 cells each. M7 (log `reason` before the check) was killed (18 cells).
**HOW:** read `errorHandler.ts` (vc-issuer), `packages/shared/src/errors/index.ts:230-292` and `requestLogger.ts`; grepped the head test stdout.

## Q4. Owner-less records: develop vs head
**FOUND:** At develop, any authenticated caller could revoke any row, owner-less or not. At the head, an owner-less row can be revoked only by ORG_ADMIN or SYSTEM_ADMIN, with a userId, whose token tenant equals the row's `created_by_tenant_id`. An owner-less row with a null tenant (pre-migration-054) can be revoked by nobody. SUPER_ADMIN and OWNER are refused. This is exactly KS-1116's `ownerlessRowReadable`, so there is **no widening** beyond KS-1116. The ruling divergence is in G59-F3.
**TESTED:** V8 (2 cells, 200 green at base and at the head, as controls), V8b–V8e and V9×2 (404 at the head, red at base). M8 admits all owner-less rows. Killed (6 cells). M11 removes the no-userId guard. Killed (V8d).

## Q5. No new platform or tenant admin bypass
**FOUND: none added.** The diff is 9 added lines in the revoke handler, with no role literal. `ownership.ts` is unchanged (same blob as develop).
**TESTED:** V6 (SYSTEM_ADMIN), V6c (SUPER_ADMIN) and V7 (ORG_ADMIN) are refused on both paths. M9 (SYSTEM_ADMIN bypass) was killed (3 cells). M10 (bypass for an ORG_ADMIN of the same tenant) was killed (3 cells).

## Q6. Red-first for the named reason; own mutants
**TESTED:** I put base product code back (`credentials.ts` from `85cd24d8`, the same blob as at `ddc644fb` and `007cc464`) under the head's test file. Result: **24 failed / 5 passed**. All 24 failures read `expected 200 to be 404`, i.e. the route let the revoke through. None is a fixture artefact. The 5 green cells are the controls: V1, V5, D1, V8×2. This covers well over 3 refused cells plus a control, across both paths (`evidence/ks1851_base.log`). Spark's runner got the same 24/5 independently.

**My own mutants** (`scripts/mutants.py`, `evidence/own_mutants.json`). Each run executed the ks1851 file; the unmutated control is 29/29:

| # | Mutant | Result |
|---|---|---|
| M1 | userId conjunct dropped (`mayRead`) | killed, 8 cells |
| M2 | tenant conjunct dropped (`mayRead`) | killed, 4 cells |
| M3 | check moved after the write | killed, 24 |
| M4 | predicate deleted (existence only) | killed, 24 |
| M5 | refused gets 403 | killed, 24 |
| M6 | refused gets a different 404 message | killed, 24 |
| M7 | `reason` logged before the check | killed, 18 |
| M8 | owner-less always admitted | killed, 6 |
| M9 | SYSTEM_ADMIN bypass | killed, 3 |
| M10 | ORG_ADMIN same-tenant bypass | killed, 3 |
| M11 | no-userId guard removed | killed, 1 |
| M12 | owner forced OWNERLESS (owner from the row ignored) | killed, 4 |

**12/12 killed.** I did not re-run E's own 12 mutants (I don't have them); E's claim is UNVERIFIED as stated.

## Q7. Existing tests still reach their checks?
**FOUND:** the change touched **no shared function**. The only mutation is inside the `router.post('/:id/revoke')` handler, so no early return was added to code anyone else calls. The existing callers of the revoke route are ks1352 (R1, R2), ks1375 (E-CRED, E-PRES, own-id) and ks1116 Q1. Each issues and revokes as the **same** principal, so it is still the creator. ks1352 R1, ks1375 and ks1116 Q1 assert `status 200` on the revoke. ks1352 R2 asserts that the re-read shows `revoked: true`. So any of them would go red if the new check refused them; none could pass silently. ks1116 Q1 revokes as ALICE on `ALICE_ROW_ID` (created by Alice), so it still reaches its Map-miss check.
**TESTED:** full vc-issuer suite at the head: **20 files, 442/442**, rc 0 (`evidence/vitest_head_full.log`). `tsc --noEmit` rc 0. eslint on the two changed `.ts` files rc 0. Control: a planted `var` + `debugger` file gave rc 1 with 2 errors. Test-type ratchet `check.cjs` for vc-issuer: 34 files, 20 tests examined, 0 new errors (20 matches the number of test files on disk). `docs-fragments.mjs check`: OK, 2 new entries per page, lint clean.

## Q8. Develop moved to `007cc464`
**FOUND:** develop gained 10 commits since `ddc644fb` (KS-1791, 1850, 1807×2, 1881, 1585, 1804, 1844, 1845, 1403), touching 47 files. **0 of the PR's 4 files** are among them. Control: the same `grep -x -F -f` matches a known changed file (1). No `services/vc-issuer` or `packages/shared` path appears either. Control: the same file has 27 `services/` lines. `git merge-tree --write-tree 007cc464 6c150b5a` gives tree `3ee109e5…` with **rc 0, clean** (`evidence/merge_tree.txt`). Not re-run: the vc-issuer suite on the merged tree. It is unnecessary for vc-issuer, because develop changed no file under it.

## Spark half (Kam's 2026-10-26 pilot)
- `spark_gate.sh`, non-pytest mode, with the ks1851 test file and `--node-modules` pointing at my clone's install: rc 0 in 14 s. It reported head 29/0, base product 5/24, diff 4 files +325/-0, merge-base `ddc644fb`. All four match my figures (`evidence/spark/facts/`).
  - **Harness note:** `spark_gate.sh` refuses a `--work` directory under `/Volumes/DevMASTER/WEDNESDAY`. That conflicts with "work only under the gate folder". So `--work` was the session scratchpad (`…/scratchpad/g59work`, holding Spark's worktree), and `--out` went under `evidence/spark/`.
- `spark_review.py`: rc 0, one attempt, 41.7 s, valid JSON. **Spark verdict: NO GO** (`evidence/spark/review/review.json`). It got the ticket text (4,277 chars) but **not** `ownership.ts`, because only touched files are sent, and the PR description was empty (14 chars).

**Calibration**

| Spark finding | Severity (Spark) | Mine | Call |
|---|---|---|---|
| A tenant admin might revoke a legacy row with null owner and null tenant; "`mayRead` null-tenant path not tested" | Major | `ownership.ts:96` refuses `rowTenantId === null`. V9×2 test exactly that through the route, and M8 was killed by them. Spark's own `evidence_quote_found_in_input: false` | **Spark false positive.** This drove its NO GO |
| `expectNothingLoggedForTheRefusal` checks only two strings, not the absence of all logging | Minor | Close to G59-F1 and G59-F2. The real gap is that the shared logger is unobserved and does write a line | **Partial agree.** Spark saw the weak assertion but not the line actually emitted |
| 12/12 mutants not backed by `facts.json` | Note | True as a fact. I ran my own 12/12 instead | **Agree** |
| — | — | G59-F1 doc overstatement (measured) | Spark missed |
| — | — | G59-F2 owner-less refusal cells weaker | Spark missed |
| — | — | G59-F3 tenant-admin write on owner-less rows vs card ks1695 (b) | Spark missed |
| — | — | G59-F4 unbound `revoke()` / double read | Spark missed |
| — | — | G59-F5 second revoke surface on `status.ts` | Spark missed |
| — | — | G59-F6 re-revoke overwrites the reason | Spark missed |

Spark's verdict (NO GO) disagrees with mine (GO WITH NOTES). The difference comes from one false-positive Major, caused by `ownership.ts` being left out of its prompt.

## NOT TESTED
- The four platform suites (Schemathesis, Akto, Playwright, k6), a running stack, a real PostgreSQL (the database path is a hoisted mock), the gateway path with real `jwtAuthenticate`.
- Node 24 LTS (everything here ran on v26.8.1).
- E's own 12 mutants (I ran 12 of my own instead).
- The vc-issuer suite on the `007cc464` merge result (develop touched nothing in vc-issuer or shared).
- Timing measurement (code reading only: both paths do the same database work).
- The PR description on GitHub: not read, because `gh` is not used from this seat.
- Multi-replica behaviour (memory stores held per process).
