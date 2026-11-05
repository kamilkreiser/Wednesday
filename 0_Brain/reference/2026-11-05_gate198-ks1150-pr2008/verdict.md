GO WITH NOTES

# Gate 198: KS-1150 R-2 + R-3, PR 2008, tier 1, round 1 of 2

**The verdict applies to the SHA, not the PR.** Head `65142195fca6a01a1ded43dd59d5ae527b3e3b33` on base develop `5fc5569ed96ac61f64823cc9e1fa841899aa1f62`. Both were read by ls-remote from the shared checkout at three points: 17:40 at the start, about 17:50 mid-run and 17:55 at the end. All three readings were identical, for `refs/pull/2008/head` and `refs/heads/develop`.

## BLUF

- **R-2 meets its Done-when.** I ran the real route with real RS256 jwt sign and verify and the real `refreshDenylist` module. Only Redis, the session store, the db and `userRepo` were doubled.
  - A refresh token redeems once (200), and a second presentation is refused with 400 `invalid_grant` "Refresh token revoked".
  - After the first redeem, its jti is denylisted with TTL = remaining lifetime (604800 s).
  - 10 refused presentations write nothing to the denylist. In each of the 8 cases where it can be tested, the same token still redeems afterwards.
  - The denylist write comes before `createSession` and the mint.
  - If the write fails, the response is 500, no token pair is delivered, no session is created, and a retry of the same token gets 200.
  - Base answered 200/200 on replay.
- **R-3 meets its Done-when.**
  - A `ServiceUnavailableError` from either user lookup gets 503 with the fixed body. A planted marker in the thrown message appears 0 times in the body and headers.
  - Every other throw (10 shapes, including a revoked Proxy and a Proxy whose `getPrototypeOf` throws) gets 500, the same as base, and the request is always answered.
- **D1 holds.** On both success and replay there are 0 calls to session revoke, rotate or `getSession`, and 0 grep hits.
- **Direction:** 72 of 72 presentations are no more permissive at head than at base.
- **Mutants:** I reproduced 4 of the seat's 9, plus 2 of my own. All 6 were killed by assertion, all admissible (tsc 0 `error TS` lines).
- **Suites:** the whole auth suite has no new failure. The one failing cell is the same ks949 load timeout on both sides, and it passes alone on both. tsc, eslint and the test-type ratchet are clean, and each has a planted-defect control that turned red.
- **Merge tree:** rc 0.
- **PR body:** it carries all five required items.
- **The notes:** F1 is the one I would want written into the PR body before merge. The rest are information only.

## Findings

**F1. Minor. A failure after the denylist write burns the token with no replacement. MEASURED AT RUNTIME.**
- Where: `services/auth/src/routes/oauth.ts:1120-1123` (the write) and `:1128` (`createSession`).
- What happens: if `createSession` (Redis) or the mint throws after the write has landed, the response is 500 and the presented token is already denylisted. A retry then gets 400 "Refresh token revoked" and the client has to re-authorize. At base, the retry got 200.
- The ordering itself is right: D1 requires the write before the mint, and the other ordering risks delivering a pair while the old token stays live.
- The problem is the text. The code comment and the PR body both say "the request answers 500 and can be retried". That is true only when the denylist write is the thing that fails. Neither mentions this case.
- Evidence: `evidence/probe-table.txt` (INFO Q2-late-fail: head 500, burned=True, retry 400; base retry 200), `evidence/probe-head.json`, `evidence/probe-base.json`.
- Fix: no code change needed. Add a line to the PR body's NOT-covered list and to the comment: "a failure after the write (session store, mint) costs the client a re-authorization". Optionally add a cell that pins it.

**F2. Note. A token with a jti but no `exp` is not denylisted and replays 200/200 at head. MEASURED AT RUNTIME. Declared.**
- Where: `oauth.ts:1120`.
- The PR body and the READY both declare this. `jwt.ts` always mints `exp`, and the session path behaves the same way.
- Evidence: the `Q2-no-exp` and `Q2-no-jti` rows in `evidence/probe-table.txt`.
- Fix: none required here. If the owner wants this closed, refuse a refresh token without `exp` (a separate ticket).

**F3. Note. `temporarily_unavailable` is not a token-endpoint error code. READ ONLY.**
- Where: `oauth.ts:1172`.
- RFC 6749 defines `temporarily_unavailable` for the authorization endpoint (§4.1.2.1). The token endpoint's error list (§5.2) has no such code.
- The 503 also carries no `Retry-After` header. No auth route sets one, so this is consistent with the rest of the service.
- This is Wednesday's D2 shape, so it is not a defect. I record it so the choice is known to be deliberate.
- Fix: none, unless a client SDK is found that parses §5.2 strictly.

**F4. Note. The concurrent-replay race is declared, but the double did not reproduce it. PROBED.**
- Two `Promise.all` presentations of one token gave 200 + 400 in all 3 runs: `evidence/race-head-{0,1,2}.json`.
- The in-memory Redis double has no I/O latency between `exists` and `setex`, so this result is not evidence that the race is absent.
- The source reads as read-then-write (`oauth.ts:1081` reads, `:1122` writes), as the PR declares.
- Fix: none here. This belongs to the board search the seat already owes for its wrap.

**F5. Note. A `ServiceUnavailableError` from the client lookup also answers 503. MEASURED AT RUNTIME. Declared.**
- The mapping is by class ("from any step of the route"). `getAppByClientId` throwing that class gives 503 at head and 500 at base. Every non-SUE throw from that lookup stays 500.
- This matches D2 as worded ("ServiceUnavailableError -> 503").
- Evidence: the `Q4:refresh-appLookup:*` rows.

## Answers to the commission

1. **Scope.** The diff touches exactly the 6 paths (`evidence/q1_scope.txt`).
   - ks823 and ks835 each have exactly 1 hunk: the mock line, plus 2 comment lines.
   - Every other line is byte-equal: 277 of 277 and 219 of 219, with the sha256 prefix equal.
   - The changed lines contain 0 `expect` tokens.
2. **R-2.** Table (probe = real route, real jwt, real `refreshDenylist`, Redis/session/db/userRepo doubled):

   | presentation | base | head |
   |---|---|---|
   | first redeem | 200 | 200, jti denylisted, TTL 604800 |
   | same token again | **200** | **400** Refresh token revoked |
   | successor token | 200 | 200 |
   | bad secret / no secret (confidential) / unknown client / inactive client | 401, 0 writes | 401, 0 writes, later proper presentation 200 |
   | wrong binding / user suspended / user not found / Redis null on read | 400, 0 writes | 400, 0 writes, later 200 |
   | expired / access token as refresh | 400, 0 writes | 400, 0 writes |
   | order | no write | exists, userLookup, **setex, createSession, mint** |
   | denylist write throws | 200 (no write exists) | 500, no pair, createSession not called, retry 200 |
   | createSession throws after write | 500, retry 200 | 500, retry **400** (F1) |
   | public client replay | 200/200 | 200/400 |

3. **D1.** Grep of head `oauth.ts` (`evidence/q3-d1-grep.txt`):
   - `revokeSession`, `revokeAllUserSessions`, `rotateSessionRefreshToken`, `getSession` and `decoded.sessionId`: 0 hits at head, 0 at base. Control: `createSession` has 3 hits.
   - `session.ts` and `routes/auth.ts` are unchanged.
   - Behavioural cell `Q3-session`: no session touches on success or on replay.
   - KS-1690's half is untouched.
4. **R-3.** 39 cells: 13 throw shapes at 3 sites (refresh user lookup, code user lookup, refresh client lookup).
   - SUE, a SUE subclass, and a Proxy whose prototype reads as SUE all give 503 `SERVICE_UNAVAILABLE` / `temporarily_unavailable` / the fixed description. The marker appears in 0 bodies and 0 headers, and no token is burned.
   - Error, TypeError, an AppError(503) that is not SUE, BadRequestError, a string, null, undefined, a revoked Proxy, and a Proxy whose `getPrototypeOf` throws all give 500, equal to base, and every request is answered.
   - Evidence: `evidence/probe-table.txt`.
5. **Direction.** 72 of 72 presentations are no more permissive at head: there is no case where head returns a pair and base did not.
6. **Mutants.** All 6 killed. Restores were sha-asserted, and the clone's `git status` is clean afterwards. Summary in `evidence/mutants/summary*.json`, per-mutant logs and tables in `evidence/mutants/`.

   | mutant | killed by the seat's cells | killed by my probe |
   |---|---|---|
   | seat M1, no denylist write | 3 of 11 | 3 |
   | seat M5, write after mint | 1 | 2 |
   | seat M7, 503 for every throw | 3 + 2 ks1868 cells | 22 |
   | seat M8, unguarded instanceof | ks1868 R3 revoked-Proxy token cell (reproduces the seat's claim) | 6 |
   | own (i), write before the success checks | 2 | 7 (refused tokens burned) |
   | own (ii), 503 echoes `err.message` | 1 | 9 (marker in body) |

   M1 and M7 as I first wrote them failed tsc with TS6133. They were rewritten as admissible versions (`void denylistRefreshJti`, `|| true`), and only those are counted. The inadmissible runs are kept in `summary.json`.
7. **Suites.** Vitest 4.1.12, run from each tree's own `services/auth` directory. Both trees are clones of the SHAs in this folder.
   - **Whole auth suite.**
     - Base: 1,686 of 1,687 pass.
     - Head: 1,697 of 1,698 pass.
     - The single failing cell is the same on both sides: ks949 "the enumeration actually finds seed sites", 5004 ms, a 5000 ms timeout at load about 6 to 10.
     - Run alone, ks949 passes 31 of 31 on both sides at load 7.8.
     - Classification: same-on-base, load-induced. New failures: 0.
     - `auth.integration` passed in both full runs.
   - **First run was invalid.** My first base run used the wrong cwd, which caused cwd-dependent failures in ks1009 and ks1467. That run is quarantined in `_quarantine_2026-11-05/` and was not used.
   - **tsc --noEmit:** rc 0 on both sides. Control: one planted type error gives rc 2 with 2 `error TS` lines.
   - **eslint (touched files):** 0 errors and 0 warnings on both sides. Control: a planted unused variable gives 1 warning. That rule is warn-level, so eslint reads the file but its rc stays 0.
   - **Test-type ratchet:** 0 new on both sides, 41 baselined. Head examines 193 files, base 192. Control: a planted test-file TS2322 gives rc 1.
   - **Vitest control:** a planted failing cell gives rc 1 with 1 failure.
   - All planted defects were restored byte-equal.
   - Evidence: `evidence/statics.out`, `evidence/controls.out`, `evidence/suite-{head,base}.json`, `evidence/suite-summary-run1.txt`, `evidence/ks949-alone-*.json`.
8. **Merge tree.** `git merge-tree --write-tree` gives rc 0 and tree `288b225dc3d7ffb5cd096043edc1bd9b7438b9da`. That equals the head commit's tree (one commit on the base). Evidence: `evidence/merge-tree.txt`.
9. **PR body.** `gh` was not available: the project's gh config is not logged in, and I did not use the global one.
   - I read the seat's `5_Project_History/2026-11-05_seatJ-16th/drafts/pr_body.md` whole.
   - Its SHA-1, with trailing newline stripped, is `7378ccc42a18fc6c4fa22cdc8a3d6f4535de6dad`. That equals the `body_sha1` the seat recorded from the API read-back in `evidence/pr_ks1150.json`.
   - It carries all five required items:
     - D1's boundary ("does not read `decoded.sessionId`, rotates no session record, does not burn a session").
     - The 503 mapping and its fixed body.
     - The concurrent-replay race as a known limit, not fixed.
     - "Node v26.8.1 (**not** an LTS line; nothing here was measured on Node 24)".
     - The NOT-run list.
   - The Linear URL is present, and the Schemathesis and Akto boxes are honestly unticked. The one gap is F1.

## What was NOT tested

- A real Redis. The double has setex/exists/TTL semantics but no latency, so the race in F4 cannot be shown.
- A booted auth service, the gateway, or any live environment.
- Schemathesis, Akto, Playwright and k6. They are not commissioned and there is no stack.
- Node 24 LTS. Everything ran on host Node v26.8.1.
- The real `createSession` and `userRepo` against Postgres and Redis.
- eslint repo-wide. Only the touched files were linted.
- The docs-fragments check was not re-run.
- The other 5 of the seat's 9 mutants were not reproduced.

## Substrate

- **Source of the trees.**
  - The head tree is a `git clone` of the shared checkout, checked out at the head SHA.
  - The base tree is a worktree of that clone at the base SHA.
  - The shared checkout was read only: no write verbs were run against it.
- **Source of `node_modules`.**
  - `node_modules`, `packages/shared/dist` and `packages/shared/node_modules` are APFS clones (`cp -c`) of gate 197's install for the same base SHA `5fc5569e`.
  - `package-lock.json`, `services/auth/package-lock.json`, the root `package.json` and `packages/shared/package.json` are sha256-equal between the two trees.
  - The PR changes no dependency file.
- My probe files were placed in each tree only while they ran, then moved to `_quarantine_2026-11-05/`. Both trees' `git status` is clean.
