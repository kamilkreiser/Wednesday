VERDICT: NO GO at head 8e5308a87e14d4a4796e5f838de30dae0838a5bf (tier 1, round 1 of 2; landing tree 0baebeb0868ac473daee7bbb15d854c88e6b2463 on develop 6229a92f2480f0784c31a8d6b652298a7ac10551; 1 blockers, 6 notes)

## BLUF

With Redis healthy, the code does what it claims on both routes. A change or reset whose write landed revokes every session of that account, the caller's included. Other accounts are untouched, and old access and refresh tokens are then refused. I drove this end to end through the real `authenticate()`, real `session.ts` on an in-memory Redis, real `jwt.ts` and the real routes. All 14 new cells pass. 0 develop cells vanished. 11 of 11 admissible author-class and own arms that should die were killed.

**One blocker.** If Redis has dropped (the availability flag is false after an `error` event) when a reset arrives, the reset answers **200**, burns the single-use token and revokes **nothing**. `revokeAllUserSessions` returns 0 silently and does not throw (`session.ts:316`). When Redis comes back, every old session validates again. The PR's own comment on the reset line ("so a failing revocation leaves it usable for a retry") and the READY claim ("Reset survives it, token unburned, retry works") do not hold for this failure class. They hold only for the throw class.

Separately, an OAuth refresh token outlives the revocation (NOTE 1, outside the diff) and so does a session hit by a request already in flight (NOTE 2, outside the diff). Both predate the PR. They are the honest answer to Q2.

## BLOCKERS

**B1. Reset fails open when the session store is unavailable.**
- Where: `routes/auth.ts`, the KS-1407 lines after `updateUserOrThrow` (landing :849-851), calling `services/session.ts:315-326`, where `if (!redisAvailable) return 0;` is at :316.
- What I measured (probe B1, real reset route, real `initRedisSession()` on a fake ioredis):
  - I emitted `error`, then POSTed a valid reset. The answer was `200 {"success":true,"message":"Password has been reset successfully..."}`.
  - Password writes: 1. Token burns: 1. Sessions revoked: 0. The route logged `sessionsRevoked: 0` at info, which reads the same as an account that had no sessions.
  - I then emitted `ready`. `getSession(<old session>)` returned the session, **ACTIVE**.
- Why it is in scope: reset is the flow a user runs after a compromise. The new code reports success, destroys the retry token and leaves the attacker's sessions to come back when Redis recovers. While the flag is false the old sessions are refused anyway (`getSession` returns null), so the exposure is the resurrection after recovery, not the outage itself.
- Change-password is effectively unreachable in this state, because `authenticate()` fails closed when the flag is false (`authenticate.ts:154`). Reset needs no session, so it is reachable.
- Shape of a fix (the author's call): fail closed before the write when the store cannot revoke. Two options:
  - Route-local: check `isRedisAvailable()` and throw a 503 before `updateUserOrThrow`.
  - Shared: make revocation throw when unavailable. That also changes the admin handler (`users.ts:838`) and `userErasedSubscriber.ts:50`, so it is a wider ruling.
- Pin it with a cell. Today no cell covers any revocation failure (see NOTE 3).

## NOTES

**N1 (HIGH; predates the PR; outside the diff). An OAuth refresh token survives `revokeAllUserSessions` and can be replayed.**
- The `grant_type=refresh_token` branch (`oauth.ts:988-1089`) never reads `decoded.sessionId`. It mints a brand-new session at :1078 and does not denylist the jti it redeems.
- Probe C1 (real `session.ts`, real `refreshDenylist.ts`, real `jwt.ts`, the ks823 scaffold):
  - I created a session, minted an OAuth pair bound to public client `pub-1`, then ran `revokeAllUserSessions` (n=1, `getSession` null).
  - The same refresh token then redeemed **200**, and **200 again**. The account had 2 live sessions afterwards.
  - Control in the same case: a client-mismatch redeem was refused 400.
- Consequence: an attacker who obtained an OAuth grant before the change or reset keeps a renewable foothold. That contradicts the PR comment "none of them may outlive it".
- Recommend a separate tier-1 ticket: check the origin session (or a per-user credential epoch) on this grant, and rotate or denylist the jti. Wednesday or Kam should rule whether it rides with this PR or follows it.
- Not run: an authorization code issued before the change and exchanged after it. The code grant also mints a fresh session at :969, so it is plausibly a smaller sibling.

**N2 (MEDIUM-HIGH; predates the PR; `session.ts`). A request in flight can resurrect a revoked session.**
- `updateSessionActivity` (:270-279) runs on every authenticated request (`authenticate.ts:160`). `rotateSessionRefreshToken` (:282-294) does the same read-modify-write. Each does `get` then `setex` of the stale JSON.
- If `revokeSession` lands between those two steps, the stale `isActive:true` record is written back with a fresh 24-hour TTL.
- Probe B3 forced that interleave deterministically:
  - After the revocation (n=1, record inactive), the in-flight write left `getSession` returning the session **ACTIVE**.
  - It was gone from `user_sessions:<id>`, so a second `revokeAllUserSessions` returned **0** and could not find it.
  - Control B3c, the same steps without the interleave: the session stayed revoked.
- An attacker hammering requests on the old token widens the window.
- This affects every revocation path (logout, admin, erase, and now KS-1407). Recommend a ticket: a revoked tombstone checked by `getSession`, or a conditional write.

**N3. The failure mode is not pinned by any cell.**
- My arms OM1 (change) and OM2 (reset), `await revokeAllUserSessions(user.id).catch(() => 0)`: tsc rc 0, **14/14 green: SURVIVED**.
- The behaviour the author describes for the throw class is real, measured with Redis throwing after the write while the flag was still true:
  - **Change (probe A2):** `500 INTERNAL_ERROR`. The password **was** written (1 UPDATE) and nothing was revoked.
  - **Reset (probe B2):** `500`. The password was written and the token was **not** burned. A retry gave 200, burned the token and revoked the session.
- Both A2 and B2 are red at develop, so they bite.
- The reset comment's "before the token is burned" design is therefore correct but unpinned. A cell would catch a future swallow.

**N4. The caller's own session is revoked (stated behaviour, confirmed). No in-repo client calls either route.**
- Probe A1: the caller gets `200 {"success":true,"message":"Password changed successfully"}`, with no re-login hint. The next call with the same token gets `401 {"code":"UNAUTHORIZED","message":"Session has been invalidated"}`. A refresh with the rotated cookie token gets `401 "Invalid email or password"`, a misleading message for a client to show.
- Client search over the landing tree (`git grep`, docs, tests and the auth service excluded):
  - No frontend, mobile or SDK caller of `change-password` or `reset-password`.
  - Positive controls: 7 files call `auth/login` and 3 frontend files call `api/users/me`.
  - The remaining hits are the gateway audit list, OpenAPI docs, e2e specs and schemathesis config.
- Low risk: the schemathesis sweep includes `POST /api/auth/reset-password`, and `/me/change-password` is in the spec. A sweep that ever landed a successful change would revoke its own harness bearer (the KS-517 class).
- I agree with the author that keeping or sparing the caller's session is Kam's product call, not a patch edit.

**N5. Login race, analytical only, NOT RUN.**
- A login that read and verified the OLD hash before the write, and reaches `createSession` (`auth.ts:443`/`:592`) after the revocation's `smembers`, keeps a fresh session. The window is roughly one argon2 verify.
- It needs the old password, which a compromise scenario supplies. MFA is single-request (`auth.ts:409-413`), so there is no pending-token variant.
- Belongs with N2's ticket if anyone wants it closed.

**N6. Landing.**
- develop moved from `11af03696c9b` (brief) to `6229a92f2480` during the gate (#1653: `BACKLOG.md` plus one m365 test).
- `merge-tree` on live develop: rc 0, clean, exactly the 4 PR files, tree **`0baebeb0868a`**. I measured on `48d32156dd4d` (the landing on `11af0369`).
- `services/auth` (`88947cf963be`), `packages/shared` (`26b323dba1df`) and `package-lock.json` (`e53534de57d6`) are byte-identical between the two landings. `services/m365-integration` differs (`22947c849e14` vs `2926047ba820`), the positive control. So every measurement carries over.
- The author's predicted landing `cdc0bcffc9c4` was on an older develop, as the brief expected.

## Answers to the brief's questions

1. **Revocation exactly when it should: YES, with Redis healthy.** One call, for that account, after a landed write. None for:
   - change: wrong current password, weak password, passwordless account, a write that did not land;
   - reset: unknown token, expired token, weak password, a write that did not land.

   On reset it runs before the burn (author cells R1-R2 and C1-C4 on each route, plus probe A1 and B0 through the real routes). Exception: B1.
2. **Adversarial: YES, three ways.** OAuth refresh grant (N1, measured), in-flight resurrection race (N2, measured), login race (N5, analytical).
   - Stores enumerated in auth:
     - Redis `sess:*` and `user_sessions:*`: covered (`session.ts:116-117`, :315-326).
     - `refresh_denylist:*`: a jti list, not a session. The interactive refresh needs `getSession` (`auth.ts:688-689`), so it is covered, as measured in A1.
     - OAuth refresh JWTs: stateless and **not** covered (N1).
     - Connector tokens: carry no `sessionId` by design, 10-minute TTL, minted from sk_ keys rather than the password (`jwt.ts` KS-480 block). Not covered, by design.
     - Test tokens: non-production only (`authenticate.ts:21-27`).
     - `oauthState` and lockout keys: pre-login state, not sessions.
     - `express-session` is a dependency but is not mounted in `index.ts` (grep zero).
   - Access tokens die at once because `authenticate()` validates the session on every request (`authenticate.ts:154-157`).
3. **The caller's own session is revoked: confirmed.** See N4.
4. **Failure mode:** throw class gives 500 with the password changed; reset's token is kept and a retry works (N3). Flag-false class gives 200, token burned, nothing revoked, and the sessions come back (B1).
5. **No weakening: yes.**
   - develop: 1096 cells / 99 files, 0 failed. Landing: 1110 / 101, 0 failed.
   - By file plus full cell name: 0 develop cells missing, 0 not passing at either end, 14 added (exactly the 14 KS-1407 cells).
   - Mutants: see FOUND / TESTED.
6. **Landing:** see N6. Also:
   - `tsc --noEmit` on auth's `tsconfig.json`: rc 0.
   - The two new test files in their own program (`files` = only those two, extending `tsconfig.test.json`, 33 auth source files pulled in): rc 0.
   - Control: the same program on `ks1005-change-password-reads-the-hash-it-verifies.test.ts` reports TS18046 and TS2339, matching its baseline lines. The check can fail.

## FOUND / TESTED / HOW

| # | What | Result | How |
|---|---|---|---|
| T1 | Heads | #1655 `8e5308a87e14` at start and end. develop `11af03696c9b` at start, `6229a92f2480` at end | `ls-remote` from the project (read verb) |
| T2 | Red-first | At develop route files: **6 red / 14** (R1-R3 on each route), all 8 CONTROLs green, 0 load failures | `mut.py` arm X0 |
| T3 | Suites | develop 1096/1096 in 99 files. Landing 1110/1110 in 101 files | `npm test --prefix <auth> -- run --reporter=json`, then a python name-set diff |
| T4 | Author-class arms (7) | **AM1** change no-revoke: red R1, R2, R3. **AM2** change, other account (`user.email`): R1. **AM3** change, revoke before write: R2, C3. **AM4** reset, revoke after burn: R2. **AM5** reset no-revoke: R1, R2, R3. **AM6** reset wrong count: R3. **AM7** reset, revoke before write: R2, C1. **7/7 KILLED** | Each arm: exact-once anchor, `tsc` rc 0, red by assertion, 0 load failures, restore sha256 asserted |
| T5 | Own arms (4) | **OM3** reset revoke twice: R1, R2, KILLED. **OM4** change also revokes on a wrong password: C1, KILLED. **OM1/OM2** swallow the failure: **SURVIVED** (N3) | as T4 |
| T6 | Inadmissible arms and the tsc control | AM5's first cut (`0;`) gave TS6133 (unused import), and was re-cut to `(false as boolean) ? await ... : 0`. Planted duplicate `sessionsRevoked` gave TS2451, INADMISSIBLE, which shows the tsc gate can fail | as T4 |
| T7 | Probes A1, A2, B0, B1, B2, B3, B3c, C1 | as above | At develop route files, A1, A2, B0 and B2 go **red** (by assertion), so the probes bite. B1, B3 and C1 behave the same at develop and at the landing: those behaviours predate the PR and the PR does not change them |
| T8 | Client search | N4 | `git grep` on the landing commit, with controls |

## NOT RUN

- No real Redis. A fake implements the session commands and drives the real `session.ts`.
- No Docker, no platform suites, no preflight legs 3, 4 or 8.
- The full suite was not re-run on the `6229a92f` landing: the auth and shared subtrees are byte-identical (N6).
- Not verified:
  - the OAuth authorization-code variant (N1);
  - a race timing measurement against real Redis (N2);
  - the login race (N5);
  - sk_ key creation as another persistence path (that lives in the security service, outside auth).
- The author's exact 13 arms were not available as files. I re-cut 7 arms of the classes they named. "13/13 killed" is accepted as stated but was not reproduced arm by arm.
- No GitHub or Linear reads or writes beyond `ls-remote` and the fetch into my scratch clone.

## Process

- Scratch clone: `/private/tmp/claude-501/-Volumes-DevMASTER-WEDNESDAY/2a56ac36-e9ca-49f4-8d2d-f02d4a53f9ed/scratchpad/gate_bo1/src`, made with `git clone --shared` of the spark cache.
- The cache lacked the PR commit. I repointed the clone's origin to `git@github.com:Secuura/Distributed_Secuura.git`, with a repo-local `core.sshCommand` set to the Secuura deploy key (read in place). I fetched only the PR ref and develop. No push.
- Setup: `npm ci --ignore-scripts` (rc 0, 1937 packages), then `packages/shared` built (rc 0) before any suite.
- Probes are untracked in that clone under `services/auth/gate_probes/`. Harness and JSON outputs are under `.../gate_bo1/scripts` and `.../gate_bo1/out`.
- Route files were restored and asserted after every arm. The clone's tracked tree is clean.

Wall-clock: 10:37 to 10:56 AEDT 2026-10-20 (about 19 min).
sha256 (method: sed '1d;$d' verdict.md | shasum -a 256): f98395caeffcae6c841ab95a7efb5a5f6c7c0724b36eca2f724d0b426c3fd75e
