VERDICT: GO WITH NOTE at head 893506989ae7c656e69408d4a6489b052b728e33 (tier 1, round 2 of 2; landing tree 2346900a5105fe24f8b3777a73123dd6df80a2a5 on develop f4259b8ed3875316a269d3228031c198eec39edd; 0 blockers, 5 notes)

## BLUF

**B1 is closed on both routes.** I tested through the real routes, the real `session.ts` (real `initRedisSession` with its real `error`/`ready` listeners, on a fake ioredis) and, for change-password, the real `authenticate()` and `jwt.ts`.

**Reset with the store already down:**
- answers **503**, writes nothing and leaves the token unburned;
- after recovery, a retry answers **200**, burns the token once and revokes the old session.

**Store reachable at the pre-check, down at revocation (step 4):**
- reset answers **503 "WAS reset"** with the token unburned. A retry with the same token completes and the old session dies.
- change-password answers **503 "WAS changed"**. The advised retry ("change it again") completes and the attacker session dies.

**The author's measurements reproduce exactly:**
- A1′ reds 7 of 9.
- A3 reds 4 of 9 (B1-R2, B1-R3, B1-R5, B1-C3), so step 4 is earned.
- A4 fires.
- A5 reds 0 of the author's cells.
- Suites: 99/1096 on develop, 103/1119 on the landing, 0 vanished. `tsc` rc 0.
- The landing tree matches the author's `2346900a5105` on live develop.

**What is left is residue, not a blocker.**
- The throw class (the author's own A5) is still unpinned. On change-password it leaves the password changed and the sessions alive behind a generic 500 (NOTE 1).
- A fake-only interleave shows the unguarded `del` in `session.ts` can orphan sessions from a retry (NOTE 2).
- Neither answers 200 over a revocation that did not happen on the first call, and neither changed between round 1 and round 2.

## BLOCKERS

None.

## NOTES

**N1 (MEDIUM; the author's stated gap A5; behaviour unchanged since round 1). A revocation that THROWS after the write is fail-closed on reset and only half fail-closed on change-password. No author cell pins either.**
- **Reset (probe R3):** `500 {"code":"INTERNAL_ERROR","message":"An unexpected error occurred"}`. Writes 1, burns **0**. After recovery the old session is still ACTIVE. The retry gave **200**, burned the token once, and the old session died. Fail-closed: the token survives for a retry, and nothing claims success.
- **Change-password (probe C3):** `500 INTERNAL_ERROR`. The password **was** written (1 UPDATE), and the attacker session is **ACTIVE** after recovery.
  - The caller is not told the password changed, nor that sessions survive.
  - The natural retry with the old current password gets `400 "Current password is incorrect"`.
  - This is the one state where an old session validates after recovery and the caller is told only "unexpected error". It is not a 200, and the user can recover by changing again with the new password.
- **Unpinned:** the author's A5 arm (`.catch(() => 0)` on both routes) reds **0** of the 23 KS-1407 cells. That swallow would turn this 500 into a **200** with nothing revoked, because the flag stays true. My R3 and C3 kill it.
- **Unchanged since round 1:** R3 and C3 are green under arm A1′ (the round-1 product). This is BO1's N3 class, which round 1 did not rule a blocker.
- **Recommend:** wrap the revoke in each route and map a throw onto the same post-write 503 (with the "WAS changed/WAS reset" wording), plus one cell per route. A follow-up, or ride it on KS-1692.

**N2 (LOW-MEDIUM; `session.ts`, outside the diff; deterministic only with a fake). If the flag flips during the revoke loop, the unguarded `del` orphans the remaining sessions, and the retry then reports success.**
- `revokeAllUserSessions` (:315-326) checks the flag once at :316. Each `revokeSession` re-checks it at :298 and returns `false` silently. `redis.del(user_sessions:<id>)` at :323 is **not** guarded.
- **Probe R4:** 3 sessions, and an `error` event fired as session 2 was being revoked.
  - First reset: **503 "WAS reset"**, token unburned. The records were `[false, false, true]`, so session 3 was untouched, and the index set was deleted anyway.
  - After `ready`, the retry: `smembers` was empty, it revoked 0 and answered **200**, token burned.
  - **Session 3 is still ACTIVE.** The caller was told success.
- **Realism, reasoned and not measured:** with real ioredis, a command issued during an outage resolves only after `ready` (so the flag is already true again) or rejects (the N1 class). That makes this window narrow.
- Same root as KS-1691 (a revoked session is not tombstoned) and KS-1692 (silent zeros). It belongs there, not in this PR.

**N3. The new refusal cells mock `isRedisAvailable` and `revokeAllUserSessions` independently** (both `*-refuses-when-the-store-cannot-revoke` files, in their `vi.mock('../services/session')`). They therefore cannot detect a check that consults a different store. Q4 is settled by the code and by my probes, which drive the real coupling (below). No change is needed. This is a statement of what the cells can and cannot see.

**N4 (wording, trivial).**
- Change-password's post-write 503 says "Sign in again with the new password". The caller's own session was not revoked (C2: the same bearer token made the advised retry, which answered 200), so signing in again is unnecessary.
- The comments cite `session.ts:317-318` and `:156`. At the head the silent zero is at **:316** and `createSession`'s throw is at **:155**.

**N5. KS-1690 / KS-1692 scoping:** see Q7. The KS-1690 scoping is correct, with two conditions.

## Answers to the brief's questions

**1. B1 closed, both routes, through the real routes: YES.**
- **Reset R1 (the BO1 B1 probe, want inverted)** at the head:
  - `503 {"code":"SERVICE_UNAVAILABLE","message":"Your password was NOT reset: ... your reset link has not been used ..."}`, writes 0, burns 0.
  - After `ready`, the retry gave 200, writes 1, burns 1, and the old session was null.
- **Same probe, controls:**
  - At the round-1 product (arm A1′): **red by assertion**. This is BO1's B1 reproduced.
  - At develop's route files (arm X0): red by assertion. develop does not revoke at all.
- **Change-password:**
  - Store down at arrival (C0b): `authenticate()` refuses first (`401 "Session has been invalidated"`, 0 writes), so the route guard is defence in depth, as the comment says.
  - Store dropping after `authenticate()` and before the write (C1, an `error` fired on the hash read): **503 "NOT changed"**, 0 UPDATEs. Red at A1′ and at X0.
- **The step-4 window:** R2 and C2, below.

**2. Step 4 is honest.**
- **Reset R2:**
  - The first call answers 503 with the "WAS reset ... link has NOT been used" wording and no `success:true`. Writes 1, burns 0.
  - After recovery and before the retry, the old session validates (ACTIVE). The caller was told.
  - The retry gave **200**, writes 2, burns 1, and the old session was null. **The retry completes.**
- **Change-password C2:**
  - The first call answers 503 with the "WAS changed" wording, 1 UPDATE.
  - After recovery the attacker session is ACTIVE. The caller was told.
  - The advised re-change gave 200, and the attacker session was null.
- **The author's A3, re-run:** removing ONLY the two re-asserts reds exactly **4 of 9** (B1-R2, B1-R3, B1-R5, B1-C3), all by assertion, plus my C2, R2 and R4.
- **An old session validating after recovery without the caller being told:** two cases. The throw class on change-password (N1: told only "unexpected error") and the fake-only orphan (N2: told success on the retry). Neither is introduced by this round.

**3. A5, a throw after the write.**
- Reset: 500, token unburned, the retry completes. Fail-closed.
- Change-password: 500, password changed, sessions alive, caller not told. Fail-closed against a false 200, not against a stale session.
- Unpinned by the author's cells. This is residue, not a blocker (N1).

**4. No new door: same store, same flag, same client.** In `services/session.ts` at the head:
- one module-level `let redis` (:16) and `let redisAvailable` (:17);
- `isRedisAvailable()` returns that same variable (:83-85);
- `revokeAllUserSessions` reads it at :316 and uses that same `redis` at :319 and :323; `revokeSession` does the same at :298 and :300-308;
- the flag is written only at :22 (the test hook), :55 (init), :60 (`error`), :68 (`ready`) and :73 (init failure).

Both routes import both functions from the same `'../services/session'` module (`auth.ts:17`, `users.ts:21`). The caveat is that this is an event-driven flag, not a live round trip. A dead socket reads `true` until `error` fires, and the revoke then throws: that is N1, not a silent zero.

**5. Collateral: no assertion changed, and each file still reaches its check.**

| File | `expect(` before → after | Cells before → after |
|---|---|---|
| ks1005 (vs develop) | 15 → 15 | 6 → 6 |
| ks1052 (vs develop) | 27 → 27 | 12 → 12 |
| ks1407-change…revokes (vs round 1 `8e5308a87`) | 17 → 17 | 7 → 7 |
| ks1407-reset…revokes (vs round 1 `8e5308a87`) | 17 → 17 | 7 → 7 |

- The only diff in each file is the mock line or lines.
- **Reach arms**, each `tsc` rc 0, red by assertion, restore sha256 equal:
  - **K1:** change-password back to `getUserById` reds ks1005 cells A-D (4).
  - **K2:** reset burns the token before the write reds ks1052 "does NOT burn the single-use reset token when the write could not be confirmed".
  - **X0:** develop routes red R1-R3 in both original ks1407 files.

**6. No weakening, and the landing.**
- **Suites:** develop 99 files / 1096 tests / 0 non-passed. Landing 103 / 1119 / 0 non-passed, which matches the author.
- **By file plus full cell name:** 0 develop cells missing, 0 not passing, +23, all four KS-1407 files (7+7+5+4). Name-diff control: a planted removal is detected (1).
- **`tsc --noEmit`** on auth's `tsconfig.json` at the landing: rc 0, empty output. tsc control: arm TC (the guards replaced, the imports left) is **INADMISSIBLE, TS6133**, so the gate can fail.
- **Arms** (each anchor count-asserted == 1, each `tsc` rc 0, each red by assertion with 0 load failures, each restored with sha256 equality asserted):

| Arm | Reds among the author's 9 | Reds in total (23 KS-1407 cells + 10 probes) |
|---|---|---|
| A1′ (author) | **7** | 12 |
| A3 (author) | **4** | 7 |
| A4 (author) | B1-R5, B1-C3 | 3 |
| A5 (author) | **0** | 2 (only my R3, C3) |
| **O1** (own): reset burns before the re-assert | B1-R2 | 3, KILLED |
| **O2** (own): change-password pre-check moved after the write | B1-R4 | 3, KILLED |

- **Merge-tree** on live develop `f4259b8ed387`: rc 0, tree **`2346900a5105fe24f8b3777a73123dd6df80a2a5`**, the same as the author's. develop had not moved past the author's measurement.
- Between head and landing, `services/auth` and `package-lock.json` are byte-identical. `packages/shared` differs (develop's `encryptedField.ts`), so I ran everything on a synthesized landing commit with shared rebuilt.

**7. KS-1690 / KS-1692 (from the code; I read neither ticket).** The KS-1690 scoping is correct for what KS-1407 needs. Every OAuth refresh pair is minted against a session (`oauth.ts:1078` then `:1082`, `generateTokenPair(user, session.id, …)`). That session is listed in `user_sessions:<id>`, so a redemption check that the origin session is still alive would make `revokeAllUserSessions` kill the whole OAuth chain. That closes BO1 N1's post-revocation foothold without the rotation/denylist half. KS-1150 R-2's half (the jti is not denylisted, so one token redeems twice) is a replay defect independent of password change, so keeping it separate is right.

Two conditions for KS-1690:
- (a) It must fail closed on a refresh token with no or unknown `sessionId`, or a legacy token walks around it.
- (b) It does not cover the authorization-code sibling, which BO1 flagged as not run: a code issued before the change and exchanged after it mints a fresh session at `:969` with no origin session to check. That needs either a credential epoch or code invalidation, and it should be named in KS-1690 or KS-1692 rather than left implicit.

N2 here also belongs with KS-1691 and KS-1692. It is the unguarded `del` at `session.ts:323`, on the same silent-false path.

## FOUND / TESTED / HOW

| # | What | Result | How |
|---|---|---|---|
| T1 | Heads | #1655 `893506989ae7`, develop `f4259b8ed387`, at start (00:25Z) and end (00:35Z) | `ls-remote` with the Secuura deploy key, read in place |
| T2 | Landing | tree `2346900a5105`, rc 0 | `merge-tree --write-tree` in my clone; `commit-tree` landing commit `e1b91f90969c` (local only) |
| T3 | Suites | develop 1096/99, landing 1119/103, 0 non-passed, 0 vanished | `npm test --prefix <auth> -- run --reporter=json`, then `diffnames.py` (with control) |
| T4 | Probes R0-R4, C0, C0b, C1-C3 | 10/10 green at the landing; X0 reds 9 of 10 (C0b not red) | `gate_probes/bs1-*.test.ts`, untracked in my clone |
| T5 | Arms | as in Q6 | `scripts/arms.py` |
| T6 | Collateral reach | K1 4 red, K2 1 red | `scripts/collateral.py` |
| T7 | Q4 coupling | same module variable and client | code read at the head, lines cited |

## NOT RUN

- No real Redis or ioredis: no measured event ordering. N2's realism argument is reasoned.
- No Docker, no platform suites, no preflight legs, no leg-16 test-file type-check.
- No gateway in front of auth: 503 body pass-through is verified only at auth's own `errorHandler`, which passes `AppError` messages through.
- Author arm A2 was not re-run (3 of 5 author arms plus A4 were).
- The KS-1690, KS-1691 and KS-1692 ticket texts were not read: Q7 is from the code and the claim.
- No GitHub or Linear reads or writes beyond `ls-remote` and the fetch into my clone. No push.

## Process

- Clone: `/private/tmp/claude-501/-Volumes-DevMASTER-WEDNESDAY/4cf20ec9-03c1-4724-89c4-ae3e1635cfad/scratchpad/gate_bs1/src` (`git clone --shared` of the spark cache).
  - The PR ref and develop were fetched by URL with a command-scoped `core.sshCommand`. Origin was not repointed.
  - `npm ci --ignore-scripts` rc 0 (1937 packages). `packages/shared` built rc 0 at the head and again at the landing.
- Harness and outputs are under `.../gate_bs1/scripts` and `.../gate_bs1/out`.
- The clone's tracked tree is clean: only `gate_probes/` is untracked.
- `git -C /Volumes/DevMASTER/WEDNESDAY status --short`: the only untracked path is `2_Project_Files/fleet/briefs_staged/2026-10-20_answer_seatG12_ks758_erasure_reason.md` (an allowed area). There are **0 untracked paths outside the allowed areas**.

Wall-clock: 11:25 to 11:37 AEDT 2026-10-20 (about 12 min).
sha256 (method: sed '1d;$d' verdict.md | shasum -a 256): 8480cd2c56efcba6c61a0dd6fdcad690d13f5b981ec3e00ef84f1ae80ca7080d
