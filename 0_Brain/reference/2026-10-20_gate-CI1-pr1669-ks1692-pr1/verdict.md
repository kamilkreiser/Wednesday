VERDICT: GO WITH NOTE at head 4728c1d613038a8082625f79e564837953bd7453 (tier 1, round 1 of 2; landing tree 79390c21c079e27d296fd3c0fe2ebfa574b5f891 on develop c3ea4dc79af72f62ad7f211d1dbf8b9920ea094d; 0 blockers, 4 notes)

## BLUF

**BS1 N1 is closed on both password routes.** The catch wraps only the revoke call. It re-throws the same post-write `ServiceUnavailableError` and never swallows. The log line carries `userId` and the error text, and nothing secret.

**Reset-password.** When the revoke throws, the route answers 503 "WAS reset". The password is written and the token is not burned, and a retry finishes the job. I tried to break this through the router, using the real `session.ts` on a fake ioredis:
- a revoke that rejects with a string, `undefined`, `null` or a plain object;
- a revoke that has a partial effect and then rejects, two shapes.

None of these burns the token or reports success. No path in the route burns the token while telling the caller it failed. The only burns before a refusal are the pre-existing expired and unknown-user branches.

**Change-password.** When the revoke throws, the route answers 503 "WAS changed" with one UPDATE, and both sessions are still alive. A retry with the OLD current password gets **400 "Current password is incorrect"**, which reproduces the author's reading. A retry with the NEW password as current gets 200, and the attacker session dies.

**The author's arms reproduce exactly:**
- A5 → T1 T2 T3
- A6 → T1 T2 T3
- A8 → T3 alone
- A9′ → B1-R2 B1-R3 (reset-only. Over both routes it reds 5 cells.)

My three own arms are all killed by the author's cells. No arm reds any other KS-1407 cell.

**Suites and type-check:**
- Auth suite at develop: 105 files / 1132 tests. At the head: 105 / 1137 (twice). 0 failed, +5 by name, 0 vanished.
- Leg 16's own check: "42 in the baseline, 0 new".
- Both new test files type-check in their own program (rc 0). A planted error reds (positive control).

**Develop moved during the gate** (`f01ba49d` → `c3ea4dc7`, m365-integration test files only). The claimed landing `9c7962e7` is stale. The live landing is `79390c21`, and its `services/auth`, `packages`, `package-lock.json` and `scripts` trees are byte-identical to what I tested (N4).

The notes are about wording and comment accuracy. None needs a change before merge.

## BLOCKERS

None.

## NOTES

**N1 (LOW; users.ts wording premise). "The caller's own session is not revoked on this path" is true when the revoke fails BEFORE any effect. It is false for a partial throw.**
- Probe P-C3 uses the real `session.ts` and two sessions (caller listed first). `setex` rejects on the 2nd revoke. Result:
  - 503 with no "sign in again";
  - the caller's session is **revoked** (`validateSession` false);
  - the attacker's session is still alive.
- So the caller who follows "change it again" hits 401 and must sign in first.
- Probe P-C1 (rejection before any effect) keeps both sessions alive, so there the clause cut is right.
- T3's throw half uses a mock that throws before any effect. It therefore pins the wording, not the premise.
- Impact is low: the 401 itself prompts a sign-in, and the success path signs the caller out anyway (P-C0). Worth one sentence in PR 2's wording pass. No change needed here.

**N2 (LOW; comment accuracy, users.ts:1018-1024). "the pre-check above is defence in depth only" overstates it.**
- `authenticate()` refuses a store that is down at ARRIVAL. The code path is:
  - `getSession` returns null on `!redisAvailable` (session.ts:256);
  - `validateSession` then answers false (:359);
  - `authenticate` throws Unauthorized (authenticate.ts:154-157).
- Between authenticate and the pre-check, the handler awaits a DB read, an argon2 verify and an argon2 hash (users.ts:983, :988, :996). The flag is event-driven, so the pre-check (users.ts:1003) is reachable in that window.
- BS1 measured exactly that window: its probe C1 got 503 "NOT changed" with 0 UPDATEs.
- Also, under `NODE_ENV` development or test, the test-token branch (authenticate.ts:143-147) skips `validateSession` entirely.
- Correct split:
  - the post-write mapping (users.ts:1025-1035 plus the re-assert at :1038) is the main live half;
  - the pre-check is live in a narrow window, and is not depth only.

**N3 (TRIVIAL; wording and cosmetics).**
- (a) The 503 says "change it again", but not "use your new password as the current one". The natural retry with the old password gets a confusing 400 (P-C2). This is carried from BS1 and is not new here.
- (b) The KS-1692 comment inside the `ServiceUnavailableError(` argument at users.ts:1040-1043 starts at 8 spaces, then lines 1041-1043 drop to 6 inside an 8-space argument list. Cosmetic only.

**N4 (process). The claimed landing is stale because develop moved; the measurement still holds.**
- live develop is `c3ea4dc79af7` (one commit: `ks1682-*` test files in `services/m365-integration`);
- merge-tree rc 0, tree **`79390c21c079e27d296fd3c0fe2ebfa574b5f891`**;
- `services/auth` tree `596e5b6e` is equal at the head and at the landing; so are `packages` `2865bfbd`, `package-lock.json` `e53534de` and `scripts` `7715ee3c`;
- against the claimed develop `f01ba49da56d`, merge-tree reproduces the author's `9c7962e77f2ae5616fbfc962822bb8138bc31372` (rc 0). That is also the head's own tree, since the PR is one commit on that develop.

## Answers to the brief's questions

**1. Scope and product diff: confirmed.** The diff is 4 files, +141/-3, exactly as claimed:
- auth.ts +24/-1 (the brief says +24/-1; `--stat` shows 25 lines changed);
- users.ts +29/-2;
- the two test files +38 and +50, with **0 deleted lines**, so no existing assertion was touched.

In both routes, `try` contains only `sessionsRevoked = await revokeAllUserSessions(user.id)`:
- auth.ts:873-883;
- users.ts:1025-1035.

The `catch` logs and then `throw new ServiceUnavailableError(...)`; nothing else. Nothing swallows.

The log meta is `{ userId, error: err instanceof Error ? err.message : String(err) }`. P-R5 asserts:
- one THREW log line;
- its keys are exactly `error` and `userId`;
- the dump contains the injected error text (non-vacuous);
- the dump contains none of the reset token, the new password, `$argon2` or the email.

The change-password log line is the same shape (code read, not probed).

**2. Reset-password: fail-closed, the token survives, and the retry completes.** All probes go through the real router and the real `session.ts` on a fake ioredis (`gate_probes/ci1-reset.test.ts`):

| Probe | First call | Retry |
|---|---|---|
| P-R1: `smembers` rejects with a string, `undefined`, `null` or `{code:'X'}` | 503 SERVICE_UNAVAILABLE "WAS reset … link has NOT been used", no `success:true`, written 1, burned 0, session still alive | not run |
| P-R2: partial, `setex` rejects on the 2nd of 3 revokes | 503, burned 0, sessions `[dead, alive, alive]` | 200, burned 1, all 3 dead |
| P-R3: all sessions revoked, then the index `del` rejects | 503, burned 0 | 200, burned 1, both dead |
| P-R4: the post-write re-assert itself throws (`isRedisAvailable` on its 2nd call) | 500 generic, written 1, burned 0, no `success:true` | not run |

P-R4 is the pre-existing `next(error)` class, and it is unreachable in practice: `isRedisAvailable` is a plain variable read (session.ts:83-85).

No path burns the token while reporting failure. `consumeResetToken` (auth.ts:893) comes after both refusals. The only earlier burns are the expired-token branch (:833, 400) and the unknown-user branch (:841, 404), which are pre-existing and intended.

**3. Change-password: confirmed, with N1 on the wording premise.**
- **The write lands and the 503 is mapped.** T2 is green at the head and red under A5, A6 and O3. My P-C1: 503 "WAS changed", 1 UPDATE, caller and attacker sessions both alive.
- **The retry with the OLD current password gets 400 "Current password is incorrect".** Reproduced in P-C2 with a fake db that persists the written hash. The attacker session is still alive after that 400. With the NEW password as current: 200, and both sessions die.
- **Wording.** `git grep -i -c "sign in again"` over `services/auth/src/routes`:
  - develop: 1 hit, the old message (positive control);
  - head: 1 hit, which is the new explanatory comment at users.ts:1040. No message in either route says it.
- **Cell T3** checks both 503s (the flag drop and the throw). Under A8 (the clause restored in both) T3 reds alone among the author's cells.
- **The premise.** It holds for a pre-effect throw and for a flag that is false at entry. It does not hold for a partial throw (N1).

**4. The authenticate() claim: partly confirmed (N2).**
- The cited chain is accurate at source:
  - session.ts:256 `if (!redisAvailable) return null`;
  - :357-359 `validateSession` returns `session !== null && session.isActive`;
  - authenticate.ts:154-157 throws `UnauthorizedError('Session has been invalidated')`.
- If the flag is true but the client throws, `getSession`'s `redis.get` rejects inside `authenticate`'s try, which goes to `next(error)`. The handler is not reached either way.
- **Live vs depth:**
  - the post-write mapping is the main reachable half;
  - the pre-write check is live in the window after authentication (BS1 C1) and under dev/test test tokens, so it is not depth only.

**5. Collateral and counts.**
- **Isolated first.** The six guards (ks949, ks1186, all five ks1188 files, ks999, s130-f6, ks488) plus the two changed files: 12 files, 92 tests, 0 failed, rc 0. All 14 KS-1407 cells in the two files are green by name: the 9 pre-existing (B1-R1..R5, B1-C1..C4) and the 5 new (T1, T1C, T2, T3, T4).
- **Whole suite:**
  - develop's 4 files: 105 files / 1132 tests / 0 non-passed / rc 0;
  - head, run 1 and run 2: 105 / 1137 / 0 non-passed / rc 0 each.
- **By full cell name:** 0 vanished, 0 develop cells now failing, +5 (exactly the five above). Control: a planted removal of one develop name is detected (1).
- **Timeouts:** 0 failures in 4 runs, so there is no elapsed time to read against 5000 ms. The slowest cell in head run 2 was ks949 at **4490 ms**, 510 ms under vitest's 5000 ms default. That corroborates the author's load-sensitivity report without reproducing a failure.
- **Arms.** Each is anchor-count-asserted. Each compiles (`tsc --noEmit -p services/auth/tsconfig.json` rc 0) before it counts, and is run over all 4 KS-1407 files (28 cells) plus my 13 probes. Every red is an AssertionError, with 0 load failures. Route files were restored after each arm, with sha256 equality asserted.

| Arm | Author cells red | My probes red |
|---|---|---|
| A0 (none) | none (28/28) | none |
| X0 (develop's route files) | T1 T2 T3 | 10 |
| A5 `.catch(() => 0)`, both routes | T1 T2 T3 | 10 |
| A6 catch removed (500), both routes | T1 T2 T3 | 10 |
| A8 clause restored in both users.ts 503s | **T3 alone** | P-C1, P-C3 |
| A9′ reset re-assert removed | **B1-R2 B1-R3** | P-R4 |
| A9′ both re-asserts removed (variant) | B1-R2 B1-R3 B1-R5 B1-C3 T3 | P-R4 |
| **O1 (own):** map only on reset | T2 T3, KILLED | 3 |
| **O2 (own):** reset catch burns the token before re-throwing | T1, KILLED | 6 |
| **O3 (own):** throw mapped to a 500 (`new Error`) on both routes | T1 T2 T3, KILLED | 9 |

The author's A9′ result matches my reset-only variant exactly, so A9′ was reset-only. A7 was not re-run.

**6. Type-check and merge-tree.**
- **Own program for the two test files:** a `tsconfig` extending `tsconfig.test.json` with only those 2 `files` (listFilesOnly shows both). `tsc` rc 0, no output.
- **Positive control:** a copy of the reset file with a planted `const x: number = "…"` gives rc 2 with exactly the 4 planted TS2322s, so the program can fail.
- My first attempt put the tsconfig outside the package. It produced a spurious TS2741 (`node:http` vs `http` Server types from a different `@types` resolution root), so I discarded it and re-ran from inside `services/auth`.
- **Leg 16:**
  - preflight.sh:767 is the `step "16/16 Test files are type-checked against the shrinking baseline (KS-1000 / KS-1487)"` header, and :775 runs `scripts/preflight/test-types-ratchet.sh`. That script runs `node scripts/typecheck-tests/check.cjs <svc>` with `services/auth` in its default list (:47).
  - I ran `check.cjs services/auth` at the head: rc 0, "examined 156 files, 105 of them under __tests__; 42 errors: 42 in the baseline, 0 new; 0 stale baseline entries". The baseline has no ks1407 entry and the PR does not touch `scripts/typecheck-tests/`.
- **Merge-tree:** see N4.

## FOUND / TESTED / HOW

| # | What | Result | How |
|---|---|---|---|
| 1 | Heads | start 03:14:25Z: #1669 `4728c1d61303`, develop `f01ba49da56d` (= the claim). End 03:25:21Z and 03:26:19Z: #1669 unchanged, develop **`c3ea4dc79af7`** | `ls-remote` from my clone (origin repointed in the clone to the GitHub URL, Secuura deploy key via the clone-local `core.sshCommand`) |
| 2 | Landing | `9c7962e7` on the claimed develop; **`79390c21`** on live develop, auth subtree identical | `merge-tree --write-tree`, `rev-parse <tree>:<path>` |
| 3 | Product diff | catch wraps only the revoke; re-throws a 503; log carries no secret | full diff read; P-R5 |
| 4 | Reset throw paths | 9 probe cells (P-R0..R5, P-R1 ×4), all fail-closed, retries complete | `gate_probes/ci1-reset.test.ts` (real session.ts, fake ioredis) |
| 5 | Change throw paths | P-C0..C3 as above; N1 found | `gate_probes/ci1-change.test.ts` (hash-persisting fake db) |
| 6 | Arms | table in Q5 | `scripts/arms.py` (tsc gate, JSON reporter, sha256 restore) |
| 7 | Suites | develop 1132/105; head 1137/105 ×2; +5, 0 vanished | `npm test --prefix <auth> -- run --reporter=json`, `scripts/names.py` with control |
| 8 | Type-check | own program rc 0, control rc 2; leg-16 check 0 new | `tsc -p gate_probes/tsconfig.ci1-*.json`; `check.cjs services/auth` (cwd = `Blockchain/Dev`) |
| 9 | authenticate claim | chain confirmed; window and test-token caveats (N2) | source read, lines cited |

Probe controls: all 13 probes are green at the head. Under X0 (develop's routes), 10 of them red by assertion. The three that stay green are expected: P-R0 and P-C0 are healthy-path controls, and P-R4's re-assert path is unchanged by the PR.

## NOT RUN

- No real Redis or ioredis. Which real conditions reject rather than resolve is not established here; the author says the same. The partial-effect shapes are fake-only.
- No Docker, no platform suites, no preflight run as a whole. Only leg 16's `check.cjs` was run, by hand.
- No gateway in front of auth: the 503 bodies are verified at auth's own `errorHandler` only.
- Author arm A7 was not re-run (A5, A6, A8 and A9′ were).
- originate and m365 were not run. The PR touches neither, so `@electric-sql/pglite` was not needed, and the shared build (`npm run build --prefix packages/shared`) was all auth required.
- The change-password THREW log line was checked by code read, not probed.
- No GitHub or Linear reads or writes beyond `ls-remote` and fetches into my clone. No push.

## Process

- **Clone:** `/private/tmp/claude-501/-Volumes-DevMASTER-WEDNESDAY/2d22076e-ad72-46a3-8b8a-b18a3ab3782c/scratchpad/gate_ci1/src` (`git clone --shared` of the spark cache).
  - `npm ci --prefix Blockchain/Dev` rc 0 (1937 packages); `packages/shared` built rc 0.
  - All npm, vitest and tsc commands ran with an explicit `--prefix`, path or cwd inside the clone. No `cd`, no `rm`.
- **Outputs:** `.../gate_ci1/out` (JSON, logs, head sha file) and `.../gate_ci1/scripts`.
- **Clone state:** the tracked tree is clean at `pr1669`. Only `Blockchain/Dev/services/auth/gate_probes/` is untracked (2 probe files, 2 tsconfigs, 1 planted control). `.../gate_ci1/tc/` is an empty leftover directory in the scratchpad.
- **`git -C /Volumes/DevMASTER/WEDNESDAY status --short`:** every untracked path is under `0_Brain/` (reference gate folders, the `NEXT-PICKUP` backup), `2_Project_Files/fleet/briefs_staged/` or `2_Project_Files/local-model/`. There are **0 untracked paths outside the allowed areas**. I wrote nothing in WEDNESDAY except this file.

Wall-clock: 14:13 to 14:27 AEDT 2026-10-20 (about 14 min).
sha256 (method: sed '1d;$d' verdict.md | shasum -a 256): 376f5c7ad0d5fc599c86baf7c2fdd6829e1fc7b5db50c18f96851c1747848261
