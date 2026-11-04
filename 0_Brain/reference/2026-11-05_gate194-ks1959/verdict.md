GO WITH NOTES — MERGE (no HOLD-FOR-KAM)

# QA Gate 194 (Tier 1, round 1): PR 2005 / KS-1959 a revoke whose database write does not take effect answers 503, not success

**Subject.** Secuura/Distributed_Secuura PR 2005 (Seat K 14th), 1 commit.
- Start (09:00:25 AEDT, `git ls-remote origin` on the read-only checkout): `refs/pull/2005/head` = `a968818a0038727399663775722017c130d4cb08` (= the claim), `refs/heads/develop` = `e899463d2a0b1b30f2cff46b23d001622620029a` (= the parent).
- End (09:09:19 AEDT): the same two values. Head did not move.
- Merge tree (in my clone): `git merge-tree --write-tree e899463d2a0b… a968818a0038…` gave rc 0, tree `1ce0f210c3832bd333773261322f98739758e5ec`, equal to `a968818a00^{tree}`. For the merge seat: merge onto develop `e899463d2a0b`.
- Host: macOS arm64, Node v26.8.1, vitest and tsc from the head's lock (`npm ci --ignore-scripts` rc 0, shared build rc 0). Node 24 was not run.

**Method.** I wrote the harness `gate_tests/gate194-matrix.test.ts`, adapted from gate 191's file. It is not the seat's file. It drives the real credentialRepo, revocationResolvers, shared verifier, credentials and presentations routers, errorHandler, helmet, cors, boundedJson and rejectNulBytes over a real HTTP server on 127.0.0.1:<ephemeral> with `fetch`. Only two things are replaced: `../db` (an in-memory table whose INSERT, SELECT or UPDATE can be made to throw, and whose UPDATE `rowCount` can be set to the real count, 0, `null`, `undefined` or absent) and the logger.
- Each run used one of two sets of product bytes: the head's, or `credentialRepo.ts` + `routes/credentials.ts` overlaid from develop `e899463d` (overlay blob ids checked equal to develop's). After each run the files were restored from the head blob (blob-equal, `git status` empty).
- Each cell writes one JSON line. `scripts/compare.py` prints the table (`logs/compare_base_head.txt`).
- The restart cells build a second app over fresh module instances (`vi.resetModules`, so `freshModuleInstance: true`) against the same table, and run its real `loadFromDb`.
- Mutants are run by `scripts/mutants.py` on the committed bytes. Suites and static checks are run by `scripts/suites.sh`.
- Every process ran with cwd `cwd/`, under `env -i`, with HOME and TMPDIR inside the workdir.
- I read the PR by GitHub API GET (`scripts/prread.py`; the token was read from the Secuura env file and never printed). The API body is rstrip-equal to the seat's read-back `pr/body.md` (sha1 ffcf5679 matches the seat's record).

## Findings

### G194-F1 — LOW: the stated `rowCount` tolerance is real; an UPDATE that writes nothing but reports a non-number `rowCount` still answers 200, and the credential verifies TRUE (same as base)
**FOUND:** With `rowCount` `null`, `undefined` or the key absent, head answers **200 "Credential revoked successfully"** in 3 of 3 forms. That matches design step 6 and the PR body ("a non-number rowCount is read as success").
- When the UPDATE also really wrote the row (`N-*-W`), the DB row is revoked and verify is FALSE on both routes (6 of 6).
- When it did NOT write (`N-*-N`), the row stays unrevoked and the next verify is **TRUE** on both routes (6 of 6).
- Base gives the identical outcome in all 12 cells, so this is not more permissive than base.
- The residual rests entirely on "pg always sets rowCount for UPDATE".

**TESTED:** 12 cells (3 forms x write/no-write x 2 verify routes), at base and head. The pg claim is NOT measured: no real PostgreSQL was run.

**HOW:** cells `N-null-W/N`, `N-undefined-W/N`, `N-absent-W/N` in `logs/compare_base_head.txt`. Control: the `Z0` cell (numeric 0, no write) answers 503 at head and 200 at base, so the instrument separates numeric from non-numeric.

### G194-F2 — LOW, PRE-EXISTING behaviour (base = head on verify): after a 503 the revoking process verifies the credential TRUE, not FALSE
This contradicts the commission's expectation in question 5; it does not contradict the PR body.

**FOUND:** After a revoke answered 503 (UPDATE threw, the DB row exists), the memory copy is revoked but the DB row is not.
- In the same process, the next healthy verify returns **verified TRUE, errors []** on both routes (the DB row outranks memory, KS-1958).
- This is identical at base, where the same revoke answered 200.
- The PR body states it: "the healthy read wins and the credential verifies as it really is".
- The commission's expected "memory revoked: verify FALSE in that process" is therefore **contradicted** by measurement.
- What remains is that process's memory holding a revoked copy that disagrees with the DB, with a fresh `revokedAt`/reason written by every failed attempt. Readers that fall back to memory on a read failure (getRecordById, getByHash, getReadableByHash; KS-1958 boundary 3, out of scope) would show it as revoked while the DB says it is not.
- That memory state also exists at base after a 200, so it is not new. I did not drive those readers in this state.

**TESTED:** RESTART cell A and matrix cell C (3 shapes x 2 routes), base and head.

**HOW:** `logs/compare_base_head.txt`, RESTART L/R line A: `p1Mem true, dbRow false, p1Verify cred/pres TRUE, p2Verify cred/pres TRUE`.

### G194-F3 — LOW (stated cost; the wording does not fit one case): a memory-only credential answers 503 "Retry the revoke." on every attempt, and no retry can succeed
**FOUND:** In this case the INSERT failed at issuance, so there is no DB row; the DB is healthy.
- First revoke: 503. Retry: 503. Every UPDATE matches 0 rows.
- Verify in that process is FALSE on both routes, because memory is revoked, as at base.
- After a restart the credential is absent and verify is FALSE ("no issuer record") on both routes.
- The PR body states the cost ("every attempt answers 503").
- The fixed text tells the caller to retry, but in this case a retry can never succeed, and the credential in fact already fails verify everywhere.
- This is not a fail-open and not HOLD-class. It is a wording/operability note for the follow-up "durable revocation" card.

**TESTED:** RESTART cell Z, matrix cell `Zreal` x 2 routes, base and head.

**HOW:** RESTART R line Z: `revoke1 503, retry 503, dbRow "no row", p1Mem true, p2Mem absent, p1Verify FALSE, p2Verify FALSE "no issuer record"`. At base: 200/200, with the same verify results.

### G194-F4 — INFO: mutant `me` (route maps ANY error from `revoke()` to 503) survives; I judge it equivalent
**FOUND:** The PR file had 0 of 8 red, and 0 gate cells differed from head.
- By reading, `revoke()` at head has no reachable throw other than `CredentialStoreWriteError`:
  - its `getById` falls back to memory under every hostile SELECT value (guarded);
  - `ensureTable` and `JSON.stringify` sit inside the guarded try.
- I tried to separate it with input: SELECT throwing during the revoke, for all 3 shapes, x 2 routes. All 6 cells answer 200 with the mutant and at head.
- Malformed or unknown ids are refused (404) before `revoke()` is called, outside the try.
- This is a test gap only: no test pins "a non-write error is not a 503".

**TESTED/HOW:** `logs/mutants_table.txt`, row `me`; cells S and UNK.

### G194-F5 — INFO: where the 503 wording reaches beyond the API response (HOLD rule check)
**Condition not met as far as measured, so not written as HOLD-FOR-KAM.**
- **What contains it:** `git grep -F "could not be saved. Retry"` at head finds 4 files:
  - the route constant;
  - the new test;
  - the two new fragments, `Projects Documents/fragments/{flow,cheat}/KS-1959-…html`.
- **Fragments:** these are rendered into the two engineering/QA pages (`docs-fragments.mjs` header: the "Flow" and "QA Tool Cheat Sheet" pages). I found nothing that says a client reads them; that is read, not measured.
- **UI:** no UI string carries the wording. No frontend caller of `POST /api/credentials/:id/revoke` was found (git grep over `frontend/*/src/services` and for `credentials/${…}/revoke`). The issuer frontend's generic `SERVICE_UNAVAILABLE` text exists, but its reach for this route was not measured.
- **Logs:** each 503 also produces one error-level "Error occurred" line from the shared errorHandler, with the fixed wording in its stack. That is an operator log, not shown to a client. The PR body does not mention it.
- Wednesday rules.

## What passed (measured)
1. **Scope.**
   - `git diff --name-only e899463d2a0b a968818a0038` lists 5 paths, exactly the READY's. Numstat:

     | File | Added | Removed |
     |---|---|---|
     | `credentialRepo.ts` | 45 | 2 |
     | `routes/credentials.ts` | 15 | 1 |
     | `__tests__/ks1959-revoke-write-fails-closed.test.ts` (new) | 295 | 0 |
     | `fragments/cheat/KS-1959-revoke-write-fails-closed.html` | 16 | 0 |
     | `fragments/flow/KS-1959-revoke-write-fails-closed.html` | 10 | 0 |

   - Other files: `revocationResolvers.ts` has 0 diff. The openapi file has 0 diff (`src/vc-issuer.openapi.ts`; the commission's `src/openapi/…` path does not exist). There is no api-gateway file and no migration in the diff.
   - credentialRepo.ts has 3 hunks:
     1. the new class after `CredentialStoreReadError`;
     2. the doc comment of `revoke`;
     3. the body of `revoke`.
   - No hunk touches `getById`, `getRecordById`, `getByHash` or `getReadableByHash`.
   - Changed product lines (comments omitted), credentialRepo.ts:
     - `export class CredentialStoreWriteError extends Error { constructor() { super('the credential store could not be updated'); this.name = 'CredentialStoreWriteError'; } }`
     - In `revoke`:
       - `let rowCount: unknown;`
       - `const result = await query(` (was `await query(`)
       - `rowCount = result?.rowCount;`
       - The catch is now `let error: string | null | undefined; try { const m = err?.message; error = m === undefined || m === null ? m : String(m); } catch { error = 'unreadable thrown value'; } logger.warn('DB revoke update failed — the revoke is refused (KS-1959)', { credentialId: credential.id, error }); throw new CredentialStoreWriteError();` It replaces the removed `logger.warn('DB revoke update failed — kept in memory', { error: err?.message });`.
       - `if (typeof rowCount === 'number' && rowCount < 1) { logger.warn('DB revoke update matched no row — the revoke is refused (KS-1959)', { credentialId: credential.id }); throw new CredentialStoreWriteError(); }`
     - The memory write `memoryStore.set(credential.id, revokedCredential);` is unchanged and still comes before the DB write (design step 1).
   - Changed product lines, routes/credentials.ts:
     - `const REVOCATION_NOT_SAVED = 'The revocation could not be saved. Retry the revoke.';`
     - `let revokedCredential: SecuuraCredential | undefined; try { revokedCredential = await credentialRepo.revoke(id, reason); } catch (err) { if (err instanceof credentialRepo.CredentialStoreWriteError) { throw new AppError(REVOCATION_NOT_SAVED, 503); } throw err; }` It replaces the removed `const revokedCredential = await credentialRepo.revoke(id, reason);`.
   - Design steps 1–6 hold line by line.
2. **Base-vs-head matrix over real HTTP.** 34 cells with a verify read, plus 1 unknown-id cell:
   - C (UPDATE throws: pg-like / revoked Proxy / getter-throws) x 2 routes;
   - S (SELECT throws during the revoke) x 3 shapes x 2 routes;
   - Z0 (rowCount 0, row exists), Zreal (true zero rows: INSERT failed);
   - N-null/undefined/absent, each -W and -N;
   - H (healthy), M (no DB), AR (already revoked);
   - UNK.

   Results:
   - **(a)** revoke more permissive than base (2xx where base was non-2xx, or verify TRUE where base was FALSE): **0 of 35**.
   - **(b)** verify more permissive: **0 of 34**. Stricter: 0. Verify (status, verified, errors) equal: **34 of 34**. There is no verify change, so the HOLD rule on verify outcomes is not met.
   - **(c)** revoke outcomes that differ: **10 of 35**, all of them expected:
     - C ordinary x2: 200 -> 503;
     - C proxy and getter x4: 500 -> 503;
     - Z0 x2: 200 -> 503;
     - Zreal x2: 200 -> 503.
     - No other cell differs. H, M, AR, S x6 and N x12 stay 200; UNK stays 404.
   - **(d)** verify outcomes that differ: 0.
   - Per-cell facts: UPDATEs per revoke are 1 on both sides (M: 0; UNK: 0). The DB row and memory flags are identical base -> head in all 35 cells. C and Z0 have the DB row unrevoked and memory revoked on both sides.
   - **Control that can fail, same run:** base shows revoke 200 + verify TRUE for C ordinary (x2) and Z0 (x2), so the instrument can show the fail-open. Mutants `m1`/`mb` (swallow restored) turn the head's 6 C cells back to 200 "Credential revoked successfully".
   - SELECT-throws: 6 of 6 identical base -> head (revoke 200, 1 UPDATE, DB row revoked, memory revoked, verify FALSE). This matches gate 191 q4.
   - 503 body: `{"success":false,"error":{"code":"SERVICE_UNAVAILABLE","message":"The revocation could not be saved. Retry the revoke."}}`. Fixed wording in 10 of 10 503s; `ErrorResponseSchema.safeParse` ok in 10 of 10.
3. **Leak.** Planted `PLANTED-G194-*` in the message, `detail`, `hint`, `where`, a getter-thrown message and a fake stack, plus `vc_credentials_store`, the hostname `db-int-g194.internal`, SQLSTATE `57P01`, `.ts:N`/`.js:N`, `node_modules` and stack-frame text.
   - Search of the whole serialized body and all headers of every revoke response (200/503/404 at head; 200/500/404 at base) and every verify response: **0 hits at head, 0 at base**.
   - Positive controls in the same runs:
     - the captured warn log at revoke time carries the token in 4 of 4 ordinary-shape cells (C x2, S x2), at base and at head;
     - mutant `mf2` (the fresh error carries the thrown message and the route answers it) makes the body search fire (`PLANTED-G194` in C ordinary x2);
     - mutant `m4b` (the seat's raw rethrow, echoed) also changes the body.
   - **The header search has its own positive control:** mutant `mh` copies the thrown message into an `x-g194-err` response header, and the header search fires in C ordinary x2. Gate 191 had no header control.
4. **Availability cost.**
   - Healthy revoke (30 in a row): status 200 x30, exactly 1 UPDATE each. SELECTs per revoke were 2 on both sides (route `getRecordById` + `revoke`'s `getById`): no extra SELECT, no retry.
   - Latency: p50 1.55 ms base vs 1.53 ms head; p90 1.61 vs 1.63. Same band.
   - 503 occurs only on an UPDATE that throws (3 shapes) or a numeric rowCount < 1 (Z0, Zreal). Non-numbers answer 200 (F1).
   - **New 500 paths at head: 0.** Revoke 500s: 4 at base (hostile shapes), 0 at head; they are now 503, as stated.
   - Consequences the PR body states, from the API body read:
     1. 503 instead of 200 while the write fails, and the caller must retry; nothing retries for them;
     2. a memory-only credential can never be revoked with a 2xx;
     3. verify is unchanged;
     4. a 2xx now means the DB row is revoked;
     5. the healthy read wins after a failed revoke.
   - All five are measured true. The only unstated consequence I measured is the error-level operator log line (F5), which is not client-facing.
5. **Restart** (fresh module instances + real `loadFromDb` against the same table; `p2` memory was absent before the load):
   - **After a 503 with no retry (A):** DB row unrevoked; process-1 memory revoked; process-1 verify **TRUE** (F2); fresh process verify **TRUE** on both routes. This **confirms** Wednesday's ruling: the caller was told the revoke was not saved, every process agrees the credential is valid, and it is not a fail-open. At base the same state followed a **200**, which is the fail-open being closed.
   - **After a 503 and then a healthy retry (B):** retry 200; DB row revoked; both processes verify FALSE on both routes.
   - **Memory-only (Z):** 503 then 503 again; process 1 verifies FALSE; the fresh process does not hold the credential and verifies FALSE ("no issuer record").
   - **Asked state** (503, then a healthy retry also 503, but the credential verifies TRUE in the revoking process): **not found**. The only 503-then-503 state is Z, where verify is FALSE.
6. **Mutants.** 16 run, 16 valid, every anchor count 1, every restore sha256-equal. The clean re-run gave PR file 8 of 8 and the gate matrix 37 of 37 with 0 cells differing; `git status` was empty after.

   Seat's 7 reproduced (same anchors):

   | Mutant | PR file red | Gate cells differing | Result |
   |---|---|---|---|
   | m1 | 4 | 7 | KILLED |
   | m2 | 1 | 5 | KILLED |
   | m3 | 2 | 4 | KILLED |
   | m4 | 4 | 7 | KILLED |
   | m4b | 4 | 11 | KILLED |
   | m5 | 5 | 11 | KILLED |
   | m6 | 1 | 11 | KILLED |

   The PR-file red counts equal the seat's 4/1/2/4/4/5/1.

   Gate's own:

   | Mutant | PR file red | Gate cells differing | Result |
   |---|---|---|---|
   | ma: memory written only on DB success, the (b) hazard | 1 | 11 | KILLED: Zreal verify FALSE -> TRUE on both routes; zero-row cell |
   | mb: catch returns success | 4 | 7 | KILLED |
   | mc: rowCount never read | 1 | 5 | KILLED |
   | md: `< 1` -> `< 0` | 1 | 5 | KILLED |
   | me: any error -> 503 | 0 | 0 | **SURVIVED**, equivalent (F4) |
   | mf1: route answers `err.message` | 4 | 11 | KILLED |
   | mf2: thrown message carried and answered | 4 | 11 | KILLED: leak cell fires |
   | mg: memory rolled back on a failed write, the rejected (b) design | 1 | 11 | KILLED: Zreal verify FALSE -> TRUE, more permissive than base |
   | mh: header control | 1 | 2 | KILLED |

   **Raw table count: 15 of 16 killed. 1 survivor (me), judged equivalent.** The headline equals the table.
7. **OpenAPI.**
   - The file is `Blockchain/Dev/services/vc-issuer/src/vc-issuer.openapi.ts`, with the revoke op at line 1113. The PR has no hunk in it.
   - The revoke op declares `503: commonErrorResponses[503]`, i.e. "Service unavailable — temporary outage or required dependency down", with `ErrorResponseSchema` (`{success:false, error:{code, message, details?}, requestId?}`).
   - The measured 503 body parses against that schema (10 of 10). There is **no example wording** in the spec; the fixed text appears only in the route and the fragments.
   - The PR body claims "503 is already in the published contract … so there is no spec change". That claim is true.
   - Schemathesis and any contract-test claim: UNMEASURED.
8. **Merge tree.** rc 0, tree `1ce0f210c383` = `a968818a00^{tree}`. Develop was `e899463d2a0b` at start and end.
9. **Suites and static checks at head.**
   - **Whole vc-issuer:** **766 of 766 in 27 files, rc 0.** Gate 191 at PR 2003's head had 758 in 26; the difference is +8 tests and +1 file (`ks1959-revoke-write-fails-closed.test.ts`, 8 tests).
   - **Red first** (new file vs base product bytes): **5 of 8 red, 5 of 5 by AssertionError** (C ordinary 200, C proxy 500, C getter 500, Z 200, R 200, each against an expected 503). The 3 controls are green. The log has 0 `error TS`, and `tsc -p tsconfig.test.json` with base product bytes gives rc 0 (no TS2554-style arity error appears).
   - **tsc** with tests: rc 0. Service tsconfig `--noEmit`: rc 0. Planted control (`TS2322` in a test-dir file): rc 2. The same grep that counts 0 `error TS` at head counts 1 there.
   - **eslint** on the 3 touched `.ts` files: rc 0. Planted control (unused var + debugger): rc 1, 2 problems.
   - **docs-fragments check:** clean rc 0 ("lint clean, render passes"). A planted unclosed `<div>` gives rc 1 in flow and rc 1 in cheat. Both were restored sha-equal; after restore rc 0. Control files are quarantined in `scratch/_quarantine/`, not deleted.
   - **Guards** (recomputed by `scripts/guards.py` from blobs):
     - base: 5 guards, `68bcdbb5, af4f679e x3, a37a6ec8`;
     - head: 6 guards, the same five byte-equal plus `e1b09425` (the new revoke catch, lines 564-571);
     - planted one-character change (`reason`->`reasom` in the first guard): `68bcdbb5` -> `9075b874`, so the change is detected.
   - **Title** `Refs KS-1959: a revoke whose database write does not take effect answers 503, not success`: **89 chars**, starts `Refs KS-1959:`.
   - **Close words:** `(close[sd]?|fix(e[sd])?|resolve[sd]?)[: ]+(#|KS-|https://linear)` (-i; a superset of gate 191's regex) finds 0 in the body and 0 in title + commit message. The control string finds 2.
   - **PR state:** open, not draft, base develop, head = the claim, 1 commit, 5 files, +381/-3, mergeable true ("unstable": checks not inspected).

## NOT tested
- Node 24 (ran Node v26.8.1).
- A real PostgreSQL or pg pool. In particular, **"pg always sets rowCount for UPDATE" is UNMEASURED**: it is read from pg's documented behaviour and the seat's reading of pg 8.20.0. The pg-like Error imitates a driver error; it was not produced by pg.
- A real deploy, demo or kintsugi.
- A real second replica, i.e. another process revoking or reading the same row concurrently. The "fresh process" is the same Node process with fresh module instances.
- `index.ts` boot: the middleware is reproduced and `jwtAuthenticate` is replaced by a fake SYSTEM_ADMIN user.
- The api-gateway proxy in front of the route, including whether it retries or rewrites a 503.
- Any UI or caller that acts on the 503 (none was found by grep; not driven).
- Latency under a slow or hanging DB, or a timeout.
- The four platform suites (Schemathesis, Akto, Playwright, k6) and the PR's CI checks.
- `getByHash` and `getReadableByHash` were not driven in the post-503 state. They have no diff. `getRecordById` is driven by every revoke cell (the route's ownership read).
- Concurrency: two revokes of the same id racing.
- An UPDATE that answers `rowCount` > 1 (not reachable with a primary-key `WHERE id = $2`; not driven).
- The seat's 54-cell direction matrix was not rerun. My own matrix has 35 cells plus the restart and latency cells.

## Plain answer for Kam
Before this change, if the database failed while someone revoked a credential, the system said "revoked successfully" even though nothing was saved. The credential then kept passing verification. After the merge, the system says so plainly: it answers "The revocation could not be saved. Retry the revoke." (a 503), and a retry that reaches a healthy database revokes it properly. Verification results do not change in any case I measured, and no database text leaks into any answer. Because the failed revoke was never saved, the credential stays valid both in the running service and after a restart, consistently with what the caller was told. One edge remains: a credential that never reached the database at issuance can now never be revoked with a success answer, and every attempt says "retry" (it already fails verification there, as before).
