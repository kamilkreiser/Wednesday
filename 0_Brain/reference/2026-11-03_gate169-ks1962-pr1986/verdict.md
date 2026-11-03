GO WITH NOTES — MERGE (no HOLD-FOR-KAM)
# QA Gate 169 (Tier 1, round 1): PR 1986 / KS-1962 anchoring registry trusts no UTxO when the registry read fails

## Subject
- Repo Secuura/Distributed_Secuura. Client checkout `/Volumes/DevMASTER/!CODING/Secuura/Blockchain/2_Project_Files` used READ-ONLY (ls-remote, diff, show only).
- `ls-remote` at START 04:06:49Z: `refs/pull/1986/head` 90196c0eeb9537d791b02b4a3c6585bbe34a631d, `refs/heads/develop` 67309f28ab2132ca7b6a45b28c731aa480642a9a.
- `ls-remote` at END 04:26:05Z: the same two hashes. The head did not move and develop did not move.
- Head is one commit on 27fe5476526c (merge-base with develop = 27fe5476526c). 5 files, +279/-37: the module, 2 test files, 2 doc fragments.
- `git merge-tree --write-tree 67309f28 90196c0e` (in the gate clone): rc 0, tree df1eb19d46919fdb5cbac587dc888f6bd40196c5. 0 shared paths (develop changed 4 paths since the merge-base; an instrument control comparing develop with itself gave 4). The merged threadTokenIndex.ts is byte-identical to head's.
- Host: macOS (Darwin 27), Node v26.8.1, vitest 4.1.12, TypeScript 5.9.3, eslint 10.7.0, pg 8.20.0, winston 3.19.0, Postgres 15.19 (postgres:15-alpine, throwaway container `gate169-pg`, now stopped and removed). NOT run on: Linux, the service's Docker image, Node 20 (the image's runtime), any deployed environment.

## Method
I made a `--shared` clone and fetched the PR ref and develop from GitHub. I made sparse worktrees for base (27fe5476) and head (90196c0e), plus `redb` (base code with head's two test files). The checkout's own installed dependencies are stale against develop: zod 3, and the shared dist has no `zod3-compat`, which gave 63 environment failures at base and at head alike (kept in `runs/stale-deps/`). So all final runs resolve `node_modules` READ-ONLY from the author's worktree `worktrees/s-s15-ks1962` (zod 4.6.7). Before relying on it I proved its `@secuura/shared` dist is a build of head's source: I compiled head's `packages/shared` into my workdir and compared 91 .js files, with 0 differences (shared is identical at base, head and develop). Afterwards, no file under that worktree's or the checkout's `.vite` caches or `shared/dist` was newer than the gate start.

Two instruments drive the REAL `threadTokenIndex.ts`, the real `@secuura/shared` trust helpers and the real winston logger (with a capture transport added). The harness files are byte-identical in the base and head trees:
1. `harness/g169-realpg.test.ts`. Nothing is mocked: real `db.ts`, the real `pg` driver and a real Postgres 15 with the real migration 010. The table holds 1 active preprod row plus 1 burned row and 1 mainnet row as controls.
2. `harness/g169-standin.test.ts`. A faithful `db` stand-in that rejects, throws or resolves 22 kinds of value, plus a logger-throws switch.

Each cell runs in both modes and loads a fresh module copy, because STRICT_MODE is read at load. Each cell records `utxoIsTrusted(FOREIGN)`, `utxoIsTrusted(GENUINE)`, `filterUtxosByRegistry([GENUINE, FOREIGN])`, `loadActiveRegistry`, and the log lines. `harness/table.js` marks any head observation that is more permissive than base. Other checks:
- Red-first: head's tests run on base code.
- Full suite at base and at head.
- tsc and eslint, each with a positive control.
- 12 mutants (`harness/mutants.js`), checked against the PR's tests and against the gate matrix, with every restore verified by sha256.

## Findings

### G169-F1 — LOW (PRE-EXISTING, outside the ruled design): a registry read that stalls after connecting has no deadline, so the caller waits until Postgres answers
- **FOUND:** `db.ts` builds the Pool with `connectionTimeoutMillis: 5000` and no `statement_timeout` or `query_timeout`. When the server stalls after the connection is open (for example, a lock on `state_thread_registry`), all three functions stay pending until the server answers, at base and at head alike. A hang never yields trusted. When the lock is released, the call resolves with the correct populated answer: trusted=false for the foreign UTxO, resolved 18-20 ms after the release. A stall during CONNECT is bounded: it rejected at 5.0 s ("Connection terminated due to connection timeout"). Head then answers false and [] in non-strict mode and rejects in strict mode, while base answers trusted in non-strict mode.
- **TESTED:** real Postgres, real `db.ts`. `BEGIN; LOCK TABLE state_thread_registry IN ACCESS EXCLUSIVE MODE` held from a separate client. All 4 calls stayed pending for 4.0 s each, in both modes and both trees (16 observations). A silent TCP server tested the connect stall. I did not hold a stall longer than 4 s per call, and did not test pool exhaustion (10 stalled reads).
- **HOW:** `runs/realpg_table.txt`, rows `hang-under-lock` and `connect-timeout-silent-server`. The cell's control is the `statement-timeout-57014-under-lock` row: the same lock, with a server-side `statement_timeout=300` passed in the URL, rejected at ~310 ms (head: false/[]). This shows the lock was really taken and that a deadline would turn the stall into a refusal. Note: the PR's T-C6 ("a hang never yields trusted") also PASSES AT BASE (`runs/red_base.json`). It is a valid guard, but it does not show the fix working.

### G169-F2 — LOW (PRE-EXISTING; strict mode deliberately untouched): strict mode still logs the thrown value's message text
- **FOUND:** the strict branch (byte-identical base and head) logs `error: <message text>`. A value planted in a real Postgres error (`database "plant_g169_secretmark" does not exist`) and planted messages in the stand-in appear in strict-mode log lines at base AND head: 5 of 25 strict stand-in rows each, plus real-pg rows 3D000, 42P01, ECONNREFUSED and timeouts. Head's NON-strict line carries `thrownType` only (see Q6). This finding records the residual on the strict side so a reader does not assume the log-hygiene card (secuura-ks1346 = a) now covers the whole function.
- **TESTED:** both instruments, in both modes.
- **HOW:** `runs/standin_{base,head}.jsonl` field `secretInLogs`; `runs/realpg_*.jsonl` field `logs`.

### G169-F3 — LOW (test gap, not a trust gap): the PR's tests do not cover a throwing logger in non-strict mode
- **FOUND:** mutant M10 removes the `try/catch` around the non-strict `logger.error`. It SURVIVES the PR's 20 cells. The gate matrix kills it (1 row: a revoked Proxy with a throwing logger, where `loadActiveRegistry` rejects with the logger's Error instead of the original value). Under M10, trust stays closed (false/[]); only the identity of the rejected value changes.
- **TESTED:** the PR's 2 test files and the gate stand-in matrix (50 cells).
- **HOW:** `runs/mutants.txt`.

### G169-F4 — INFO: the comment on the unreachable trailing throw says "non-strict returned above"; it THROWS above
- **FOUND:** `threadTokenIndex.ts:118`. The code is correct and the line is unreachable (see Q2, mutant M8). Only the comment's verb is wrong.

### G169-F5 — INFO (PRE-EXISTING): the threadTokenMint 'deterministic per-seed policyId' failure depends on load and is not deterministic
- **FOUND:** in the full suite it fails at base and at head with identical text (`Error: STACK_TRACE_ERROR`, compared after path normalisation: `runs/ttm_fail_{base,head}.txt`). Run in isolation it PASSED 2 of 2 times at base and 2 of 2 at head (`runs/ttm_*`). The PR does not touch the file, and the file does not import threadTokenIndex. The author's isolated head rerun failed with a different message ("Could not serialize the data"), so "same failure at base" holds inside the suite, but the cell is a flake rather than a fixed red. The author's first mutant run also had an unmutated-control flake (19/20, `mutants.out`) before the clean rerun.

## What passed (measured)
- **Q1, can any error yield trusted or an unfiltered list?** No, in either mode. Head was more permissive than base in 0 of 280 observations (real pg: 80; stand-in: 200).
  - **Non-strict mode, real pg.** 8 failure kinds: missing table 42P01, unknown database 3D000, bad password 28P01, ECONNREFUSED, DATABASE_URL unset, connect timeout (5.0 s), statement timeout 57014, hang. Base: trusted=true for FOREIGN and GENUINE, and the filter passed both UTxOs through unattributed (7 kinds; the hang was pending). Head: false, false, `[]`, and `loadActiveRegistry` rejects (7 kinds; the hang stays pending).
  - **Non-strict mode, stand-in.** 20 failure kinds: ordinary Error, pg-shaped Error with code and detail, string, null, undefined, 0, Symbol, revoked Proxy, getPrototypeOf trap, throwing constructor getter, throwing constructor.name getter, throwing message getter, 42P01-shaped, AggregateError, thrown thenable (not adopted), synchronous throw, `rows:null`, throwing rows getter, `rows:[null]`, resolves undefined. All 20 refuse at head: false/false/[]/rejected. Base was trusted and unfiltered for all 20.
  - **Logger throws.** Base rejects every call (it never trusts). Head answers false/[] and rethrows the ORIGINAL value. Both refuse.
  - **Strict mode.** Every failure kind rejects from all three functions, identically at base and head (real pg 8 kinds plus stand-in 20 kinds; the hang is pending in both).
  - **Class bar.** Every non-strict failure kind at head ends in the same state as head's ordinary Error (false/false/[]/rejected). The PR's T-R1 checks that the rejected value is identical to the thrown one; my harness recorded only its type.
- **Q2, success paths.**
  - The populated registry gives identical results at base and head in both modes: FOREIGN false, GENUINE true, filter `[doc-1]`. The burned row and the mainnet row stay excluded.
  - The EMPTY readable registry in non-strict mode still passes through (trusted true; both UTxOs returned with null attribution). In strict mode an empty registry gives false/[] at base and head.
  - The strict lines are byte-identical: base 76-88 equals head 105-117 (13 lines, `cmp`); the control of one more line differs as expected.
  - The trailing `throw err` (head line 119) is unreachable. Mutant M8 replaces it with a fabricated trusted registry row and SURVIVES all 20 PR cells and all 50 matrix cells, which makes it equivalent.
- **Q3, contract census (head and develop, `git grep` over the whole repo).**
  - `loadActiveRegistry`, `filterUtxosByRegistry`, `utxoIsTrusted` and `threadTokenIndex` have no importer outside the module itself. Other hits are only docs (`STATE_THREAD_NFT_DESIGN.md`, `Projects Documents/fragments/*`) and 2 test files: the ks1868 file, updated in this PR to expect the rejection, and the new ks1962 file.
  - Positive controls fired: `selectThreadTokenUtxos` was found in 5 files (shared, the module, a test, docs), and `'../utils/logger'` importers in anchoring numbered 5.
  - The two in-module callers translate as designed. Through `readRegistryOrNull`, a non-strict rejection becomes `null`, which becomes false or `[]`; a strict rejection propagates.
  - The only things outside the module that now receive a rejection they did not receive before are the ks1868 test cells C2, C3, R1, R2 and R3, which were changed on purpose.
- **Q4, hang.** See G169-F1: never trusted, no deadline, and the caller blocks for as long as the server stalls (measured ≥4.0 s per call; it ended only when the lock was released). A connect stall is capped at 5 s and then refused.
- **Q5, red-first and the suite.**
  - Head's 2 test files on base code: 10 of 20 cells fail, all 10 by AssertionError (5 ks1962 T-R1 cells, plus ks1868 C2, C3, R1, R2 and R3). The 10 that pass at base include T-C6 (hang, see F1).
  - On head: 20/20 pass.
  - Full anchoring suite: base 816/817 (99.88%), head 827/828 (99.88%). The +11 is the new file's cells. The single failure is threadTokenMint in both (F5). This matches the author's counts.
  - tsc `--noEmit`: base and head both rc 0 with 0 lines; a planted type error gave 1 error.
  - eslint on the changed .ts files: base 2 files and head 3 files, 0 errors and 0 warnings; the positive control (max-len 40) gave 161.
  - Mutants: 12 run. The unmutated control passed 20/20, with 0 matrix rows differing. Against the PR's tests, 10 were killed (all by assertion) and 2 survived: M8 (equivalent: unreachable) and M10 (not equivalent: F3). Against the gate matrix, 11 were killed and 1 survived: M8 (equivalent). I counted the raw table in `runs/mutants.txt`, and it matches this headline.
  - merge-tree: rc 0, 0 shared paths.
- **Q6, secrets in logs.** Head's non-strict line has the meta `{thrownType}` only. The values seen: Error, string, null, undefined, number, symbol, unreadable, AggregateError, Object, TypeError, DatabaseError.
  - Planted marker in a log line, non-strict stand-in: base 5 of 25 rows (positive control), head 0 of 25.
  - Real pg with a planted database name: base logged `database "plant_g169_secretmark" does not exist`; head logged `thrownType: "DatabaseError"`.
  - Strict mode is unchanged (F2).

## NOT tested
- Any production or HTTP caller: none exists (census, Q3), so no route was driven. "No production caller" is a repo-wide `git grep` result; dynamic or string-built imports from outside this repo were not checked.
- Stalls longer than 4 s per call; pool exhaustion by 10 or more concurrent stalled reads (pg's 5 s wait for a client would then reject, which head answers as false; I reasoned this from the config and did not measure it); TCP half-open or keepalive behaviour.
- The `afterRelease` column of the `statement-timeout-57014-under-lock` cell depends on timing (it differed between my two runs). Only its four main columns, which were stable across both runs, are used above.
- Node 20, Linux, the service container, a deployed environment, and any network other than preprod (the mainnet row was only used as an exclusion control).
- The 2 HTML doc fragments were not reviewed for content.
- Whether the empty-registry pass-through is still the wanted behaviour (it is the ruled design; it is unchanged).

## Plain answer for Kam
Before this change, if the anchoring service could not read its list of trusted document tokens, for any reason (database down, wrong password, missing table, a timeout), it quietly treated every on-chain record as trustworthy. After this change, a failed read trusts nothing: I tried 28 different ways of making the read fail, against a real database and a stand-in, and none of them led to anything being trusted. When the list reads fine, nothing changes: real tokens are still trusted, forged ones are still rejected, and an empty list still behaves as it did before. If the database freezes partway through a read, the check waits rather than guessing. It does not have a time limit, but it never says "trusted" while it waits. Nothing in the product calls this code yet, so merging changes no user-visible behaviour today; it makes the check safe for when it is wired in.
