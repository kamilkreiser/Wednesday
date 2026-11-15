PR 2231: GO WITH NOTES (at head 5dccb159d12960f14d31dd6bca20e7c524952486; tier 1)

Gate 353 (tier 1, Opus), 2026-11-15 15:45 to 15:57 AEDT. Findings only: nothing was fixed, pushed, posted, commented, mailed, merged, or written to Linear or GitHub.

**Pins.**
- Read by `gh api` at 15:45:42, then `git ls-remote` at 15:46:19 (`scratch/pin1.out`), then both again at 15:56:18 AEDT (`scratch/pin2.out`).
  - develop 4e4347818772cf259cd3b4849ea576b7495f3453
  - refs/pull/2231/head 5dccb159d12960f14d31dd6bca20e7c524952486
- Neither moved, and both equal the commission.
- The PR is ONE commit on 48883ba5976b, the develop before B 176th's merge of PR 2089.
- `merge-tree --write-tree` of develop and the head gives tree fdc92b4f5ff9 in both orders, rc 0 (`scratch/out-mt.txt`).
  - Merge vs head: 1 path differs, the api-gateway ks1493 test file.
  - The kyc `index.ts` blob in the merge is e2bef0b96435, identical to the head's.
  - So the kyc tree at the head IS the kyc tree at the merge.
- kyc `index.ts` goes from 9becd6065b3e (develop, identical at 48883ba) to e2bef0b96435 (head).

## FOUND

**G353-2231-1 (Low; pre-existing; NOT this PR's scope; for the board).** The seat's "Not in scope (a)" is confirmed at source and by measurement, and it is slightly understated.

Confirmed at source:
- The live handler is `packages/shared/src/errors/index.ts:232`. kyc's `@secuura/shared` re-exports it via `export * from './errors'`.
- `errors/error-handler.ts` is a second copy that is NOT on the public surface; its own comment says so.
- The live handler's first statement reads `err.message` and `err.stack` unguarded.

Measured with `scratch/q4probe.mjs` against the built package:
- `errorHandler(revokedProxy)` throws "Cannot perform 'get' on a proxy that has been revoked".
- `errorHandler(undefined)` throws "Cannot read properties of undefined".
- Control: `errorHandler(new Error('secret'))` answers the generic 500 with no 'secret'.

What the seat's note understates:
- **Six call sites, not four.** kyc has six `next(error)` sites: initiate `:804`, document `:985`, selfie `:1053` and review `:1227` in `index.ts`, plus `routes/microsoft-verification.ts:106` (start) and `:193` (issue). The PR body names "four POST routes".
- **Each of those catches runs `error instanceof z.ZodError` first.** On a revoked Proxy that throws (measured: THROWS; control on a plain Error: no throw). So at those six sites an unreadable value never reaches the handler at all. It becomes a rejection of the async handler: the request goes unanswered and the rejection is unhandled. That is the KS-2185 defect class itself, not "the handler crashes".

**Reachable today?** I found no path. Read: the db helpers those routes await (`dbGetVerification`, `dbSaveVerification`, `dbSaveConsent`, and `dbGetVerificationsByUser` without `throwOnError`) log and swallow, and `dbSaveImage` throws an `AppError`.

**Grade:** a latent hazard, Low.

**Exact action for the board:** one ticket to make the shared `errorHandler` total, so that no read of the thrown value can throw (guarded reads, coercing a non-Error to a generic Error), and to drop the `instanceof` that comes first in the six catches. That one fix also closes G353-2231-2.

**G353-2231-2 (Low; residual of this PR's own guard; unreachable today).**
- **What the guard covers.** The catch probes `.message` only. A value whose `.message` is readable, but whose `.stack` read or `getPrototypeOf` throws, passes the probe.
- **What happens to such a value.** It reaches the shared handler, which throws (at `dist/errors/index.js:214` and `:215`, in `logger.error` and the `instanceof ZodError` test).
- **What the caller sees** (my probes G8 and G9, at the head): Express's default handler answers 500 with an HTML page carrying "TypeError", the stack, and absolute server paths (`/Volumes/...`, `node_modules`). `NODE_ENV=test`; KS-658 says the demo runs `development`, which takes the same branch.
- **Reachability: none in the erasure's real throwers.** I read them all:
  - pg `DatabaseError` and connection errors;
  - `Error('DATABASE_URL not configured')` (`db.ts:26`);
  - `SubjectKeyDestroyedError` and the plain `Error`s in `shared/src/crypto/subjectDek.ts`;
  - a JSON or crypto error from `rowToVerification` (caught there).

  All are ordinary Errors.
- **Why it is still a finding.** The catch's comment says the guarded read handles "a value it cannot read"; it handles a value whose `.message` cannot be read. That is narrower than the comment, and it is the same root as G353-2231-1. Not a NO GO: the PR closes every case it claims, measured.

**G353-2231-3 (Info; the shared handler's 4xx passthrough; unreachable from the erasure).**
- **A numeric `status` passes through with its text.** A thrown value carrying a numeric 4xx `status` is answered with that status AND its own message. Measured with G7, a thrown `Error(SECRET)` with `status: 404`: the caller got 404 `{"code":"BAD_REQUEST","message":"ks2185-thrown-text-must-not-reach-the-caller"}`. The cause is the body-parser branch of the shared handler (`errors/index.ts`, `typeof bp.status === 'number'`).
- **Not reachable from the erasure.** No erasure thrower carries `status`; I read `db.ts` and `subjectDek.ts`.
- **A thrown string `'route'`.** It is answered 404 NOT_FOUND (G10): Express treats `next('route')` as "skip the route". It is unreachable.

Both are outside this PR, and recorded so that the shared-handler ticket in -1 covers them.

**G353-2231-4 (Info; partial erasure; unchanged by this PR).**

`dbDeleteUserData` (`index.ts:374`, outside the diff's single hunk at `@@ -1270`) is four statements with no transaction:
1. the legacy image-id DELETE;
2. the images DELETE by `user_id`;
3. the consents DELETE;
4. the verifications DELETE;

then `subjectDeks.evict`.

| Case (probe at the head) | Caller sees | Erased | Kept | DEK evicted |
|---|---|---|---|---|
| G2: consents DELETE fails | generic 500, no thrown text | images | consents, verifications | no |
| G3: verifications DELETE fails | generic 500, no thrown text | images, consents | verifications | no |

- **What the caller cannot tell.** The answer does not say whether anything was erased. A retry re-runs every DELETE and is idempotent: the legacy ids are re-collected from the surviving verification rows.
- **Before the PR,** the same statements ran in the same order and the caller got no answer at all. My G1 (statement texts and order, evict once) passes at develop AND at the head.
- **Success:** byte-identical body (O1 at both trees) and the same statements.

So nothing is erased differently on success or on partial failure. This PR is failure-path only, as claimed.

**G353-2231-5 (Info; test thinness, not a gap).**
- Every RED cell of the PR reddened under at least one plant. O1 (the success control) reddened under none of my plants, by design.
- The PR's 10 cells fail only the read and the FIRST DELETE. A failure of the 2nd or 3rd DELETE is pinned by my G2 and G3, not by the PR.
- The `platformMayRead=false` argument is pinned only by the KS-2166 file (3 reds under my `check_platform_may` plant, 0 in the ks2185 file). That is acceptable, since the line is KS-2166's.

## TESTED

**Q1. The route and errorHandler, read at the head (`index.ts:1273-1307`, `shared/src/errors/index.ts:232-298`).**
- **Order:**
  1. `callerMayActOn(req, req.params.userId, false)` (synchronous);
  2. 403 `NOT_THE_SUBJECT`;
  3. `try { await dbDeleteUserData; log; res.json(200) }`;
  4. `catch`: a guarded `.message` read, then `next(forHandler)`.
- **The 403 check is byte-for-byte unchanged and before the first await.** I extracted its three lines with awk from the develop, 48883ba and head blobs: sha256 59dbc345… for all three (non-empty). Only the comment line above it changed. My `check_after_await` plant (check moved inside the try, after the await) reddened 19 cells, including O2, O3 and 17 KS-2166 cells. My `check_removed` plant reddened the same 19.
- **A rejecting erasure now answers through the shared handler, and the process keeps running:**
  - R1a and R1b: 500 with the generic body.
  - R2a and R2b: 0 unhandled rejections.
  - At develop the same cells get no answer within 2.5 s, and 1 unhandled rejection is counted.
  - On Node 26, an unhandled rejection exits 1: my `node -e "Promise.reject(...)"` returned rc 1, and the handled control rc 0. I did not observe the exit of the kyc process itself.

**Q2. Leak.** No thrown text in the answer for any value the erasure can produce. At the head:

| Thrown value | Answer |
|---|---|
| `Error(SECRET)` (R3a) | generic 500, no SECRET |
| revoked Proxy (R3b) | generic 500, no stack or path text |
| `undefined` (R3c) | generic 500 |
| `null` (G4) | generic 500 |
| the string SECRET (G5) | generic 500, no SECRET |
| pg-shaped Error with `code`, `detail`, `table` and SECRET in the message and detail (G6) | generic 500, no SECRET |

The exceptions are contrived values, not reachable: G7, G8, G9 and G10 (findings -2 and -3).

**Q3. Erasure semantics.** Unchanged on success and on partial failure (G353-2231-4).

**Q4. The seat's note.** Confirmed and graded Low, out of scope (G353-2231-1).

**Q5. Red-proof and mutants** (vitest JSON; `scratch/out-redproof-*`, `out-probes-dev`, `out-plant-*`).
- **The PR's red-proof, reproduced by me:**
  - The PR's file on develop's `index.ts`: **7 failed / 3 passed** (R1a, R1b, R2a, R2b, R3a, R3b, R3c), every one an AssertionError ("expected undefined to be 500" ×5, "expected 1 to be +0" ×2). This equals the READY.
  - At the head: 10/10.
- **My plants.** Each run covers the ks2185, ks2166 and gate353 probe files (103 tests). The baseline at the head has 4 failures: my OBSERVE cells G7 to G10, which assert the ideal and record the finding.

| Plant | Reds beyond baseline |
|---|---|
| check after the await | O2, O3 + 17 ks2166 |
| check removed | same 19 |
| `platformMayRead=true` | 3 ks2166 (ks2185 file: 0) |
| `next(error)` raw (the PR's tamper) | R3b, R3c, G4 |
| guard → `error == null` only | R3b |
| catch leaks `String(message)` | R1a, R1b, R3a, R3b, R3c, G2 to G6 |
| catch answers 200 success | R1a, R1b, R3a to R3c, G2 to G6, G10 |
| catch rethrows (the PR's tamper) | R1a to R3c (7), G2 to G6, G10 |
| 200 sent before the erasure | R1a, R1b, R3a to R3c, G2 to G6, G10, ks2166 control C |

  Each plant was restored with `git checkout HEAD --`, and `hash-object` read back e2bef0b96435 every time. Worktree porcelain ended at 0.
- **Whole kyc suite**, interleaved dev → head ×2, Node v26.8.1, vitest 4.1.12:

| Tree | Run 1 | Run 2 |
|---|---|---|
| develop 4e4347818772 | 18 files, 177/177, rc 0 | same |
| head (= the merge's kyc tree) | 19 files, 187/187, rc 0 | same |

  177 + 10 = 187. These equal the READY.
- **tsc** `--noEmit -p services/kyc/tsconfig.json`: rc 0 at both trees. A planted TS2322 gives rc 2, then restored.
- **eslint** (ESLint API, Dev root flat config): 0/0 on `index.ts` and on the new test file. Planted control (`var`, `debugger`): 2 errors.
- **Docs fragments:** read (both accurate against my measurements). The `docs-fragments.mjs check` was NOT run (sparse worktree; UNMEASURED).

## HOW
- **Clone:** `scratch/clone`, `git clone --reference` to the Blockchain project's object store (read-only alternates). Fetched with that project's deploy key via a one-shot `GIT_SSH_COMMAND`; push URL `DISABLED` (shown in pin2).
- **Worktrees:** `wt-dev` at 4e4347818772 and `wt-head` at 5dccb159d129, sparse on `Blockchain/Dev`. Each had its own root `npm ci --ignore-scripts` and its own `packages/shared` build (rc 0).
- **Probe file:** `scratch/probe/gate353-probes.test.ts`, built from the PR's own harness plus an evict counter. It was copied in only for runs and moved out after.
- **GitHub:** PR JSON read with `gh api` GET (kksecura); body in `scratch/pr2231.json`.
- **No writes outside this folder.**

## NOT TESTED (UNMEASURED)
- A running stack, Postgres, a real token through the gateway, the `user.erased` bus path, and the kyc process exit itself.
- Node 24, a container build, Schemathesis, Akto, Playwright, k6.
- The docs-fragments checker, the pre-push preflight, and `check:test-types`.
- Linear: KS-2185's state and comment were not read.
- Reachability of an unreadable or `status`-bearing thrown value at the six other `next(error)` sites, beyond reading the helpers they await.
