GO WITH NOTES. MERGE (no HOLD-FOR-KAM). Nothing is FIX-BEFORE-MERGE.

# QA GATE 163: Secuura Platform K PR 1980 (KS-1957, referral award routes: owner or platform role), TIER 1, round 1

**The authorisation bar holds at both routes through the real service.** At head, an award or a qualification happens only for:
- the owner on `/check` (`req.user.userId`, a non-empty string, exactly equal to the path id), or
- a platform role under the shared `isPlatformRole` (SYSTEM_ADMIN / SUPER_ADMIN, ASCII case fold, non-strings refused).

Every other principal class I drove is refused. Every refusal leaves the database untouched: 0 award rows, 0 row writes, and 0 SQL statements sent by the app role. Every figure the author gave matched when I measured it again. My mutant run had 20 mutants: 16 killed, 2 equivalent, and 2 LOW test gaps that the live matrix covers (G163-F3).

Subject:
- Head `7d6130ba0d4edb9294dbb81f39c0bcb76268dfa0`. This equals Wednesday's pin and `refs/pull/1980/head` (ls-remote at 01:16:45Z and 01:17:05Z).
- Fetched from GitHub into my own `git clone --shared` (`repo/`, push URL disabled).
- PR parent / base `66cbe4e52d5a`.
- develop re-read by ls-remote: `0a6575f7fd92` at the start, `df0d1f8e4be5` at 01:17Z, still moving.
- PR 1979 `eeb4ab58d6d1`.
- Host Node v26.8.1. node_modules were cloned (cp -c) from gate 153's clone. The lockfiles, package.jsons and the `packages/shared` tree have the same blob ids at gate153, pr/1980 and develop.

## How it was measured (the real stack)

`scripts/g163.cjs` boots the **real** `services/referral/src/index.ts` (node + tsx) once per version: base worktree, head, and the combined tree. Everything in that boot is real:
- `helmet`, `boundedJson` and `rejectNulBytes`.
- `app.use('/api', authenticate())` from `@secuura/shared`, the real routes and services, and real `pg`.
- A real PostgreSQL 15 container of my own, `g163-pg`, now stopped and removed.

Each principal is a **real RS256 JWT** signed by a key whose public half is the service's `JWT_PUBLIC_KEY`. The claims reach the route exactly as the verifier decodes them.

Each of the 92 cells per version does a TRUNCATE plus seed, then sends one request. The seed is:
- target A: 1 QUALIFIED referral, so a check that runs awards FIRST;
- referee Q: PENDING from B;
- referrer id `"1957"`: 1 QUALIFIED.

It then measures:
- the status;
- milestone-reward rows, referral-reward rows and the referral's status;
- every row write, captured by AFTER triggers on all 6 tables into an admin-owned log;
- every statement the app role sent (`log_statement=all` for the app role, bracketed by admin markers).

Positive controls: an allowed `/check` shows 1 award, 1 write and 3 statements. An allowed `/qualify` shows 3 award effects (milestone row, referral reward, referral QUALIFIED), 3 writes and 7 statements.

**How the principal reaches the route:** only through the JWT. `index.ts:86` mounts `jwtAuthenticate()` on `/api` with `required` defaulted to true. The referral source reads no identity header: `git grep` for `req.headers|req.get(|x-user|x-tenant|x-gateway` finds only a comment and the user-agent log. The gateway forwards `Authorization` (`proxy.ts:311`), and referral verifies it itself. A direct caller to port 4016 therefore cannot forge identity with headers (measured: cells 35 and 71). It also cannot forge a token: a foreign RSA key, HS256 keyed by the public PEM, and `alg:none` all get 401.

## Question 1: can anyone else cause an award or a qualification? Cell counts (`logs/matrix_table.txt`)

| version | /check 200 | /check refused | /qualify 200 | /qualify refused | award effects in refused cells | writes / statements in refused cells |
|---|---|---|---|---|---|---|
| base | **44** | 5×401, 1×404 | **33** | 6×401, 3×400 | 0 | 0 / 0 |
| head | 10 | 34×403, 5×401, 1×404 | 5 | 29×403, 6×401, 2×400 | **0** | **0 / 0** |
| combined (develop + 1979 + 1980) | 10 | same as head | 5 | same as head | 0 | 0 / 0 |

**At base**, every authenticated principal awarded or qualified. That is 77 cells and 143 award effects, which confirms G153-F3 and its /qualify twin.

**At head, the 10 `/check` 200 cells (1 award each) are all owner or platform:**
- SYSTEM_ADMIN, SUPER_ADMIN, super_admin, system_admin and Super_Admin, each checking A;
- owner USER;
- owner ORG_ADMIN (self);
- owner via a trailing-slash path;
- string userId `"1957"` on path `/check/1957`;
- SUPER_ADMIN on path `/check/1957`.

**At head, the 5 `/qualify` 200 cells (3 effects each) are the 5 platform spellings.**

**Refused at head with 403, on both routes:**
- other USER, ORG_ADMIN, ADMIN, ISSUER_ADMIN, ISSUER_APPROVER, OWNER-role, VERIFIER and `connector`;
- lowercase `admin` (auth's local platform list accepts it) and `platform_admin` (tokenisation's list);
- the arrays `["SUPER_ADMIN"]` and `["SYSTEM_ADMIN"]`;
- Unicode and whitespace tricks: dotless-i (U+0131) in SUPER_ADMıN and SYSTEM_ADMıN, long-s ſUPER_ADMIN, leading or trailing space, trailing `\n`, NUL suffix, fullwidth Ｓ, a zero-width joiner;
- non-string roles: object, null, missing, number;
- forged `x-user-id`, `x-user-role: SYSTEM_ADMIN`, `x-gateway-vouch` and `x-forwarded-user` headers on a USER token.

**Refused at head on `/check` only:**
- the owner id upper-cased or with a trailing space in the token;
- another user with a %-encoded path;
- `sub`=A with no `userId` claim;
- `userId: [A]`;
- **numeric `userId: 1957` against path "1957"**;
- empty `userId` against A;
- a token with no `userId`.

**Refused at head on `/qualify` only:** the referee itself, the referrer itself, and the referee sending a bad body (403 before the body is read).

The empty path `/check/` is 404 at both versions. A request with no principal is 401 at both versions, from `authenticate()` before the route.

**Answer: no.** Nobody other than the owner (on /check) or a platform role causes an award or a qualification at head.

## Question 2: does a refusal change state?

No. Across all 63 head 403 cells plus the 401, 404 and 400 cells: 0 award rows, 0 row writes on any table, and 0 SQL statements from the app role. So getReferralsByReferrer, checkAndAwardMilestones and qualifyReferral are never reached, because each of them issues SQL. The PR's spy assertions say the same at unit level (25 of 25 green).

## Findings

**G163-F1 (INFO, positive): the authorisation matrix, 92 cells × 3 versions, as above.**
- FOUND: Head is strictly narrower than base. 0 head cells are more permissive than base. Every head 200 is owner or platform. Combined equals head in every status and award count. The only differences are 1 extra row write and 2 extra statements in the allowed `/check` cells, which is PR 1979's progress save.
- TESTED: `logs/probe/{base,head,combined}.json`, `logs/matrix_table.txt`, `logs/matrix_head_vs_combined.txt`.
- HOW: `scripts/g163.cjs`, `scripts/table.py`.

**G163-F2 (LOW, info for Kam): the "platform" predicate is the shared one; the platform's vocabulary split remains.**
- FOUND: Both routes import `isPlatformRole` from `@secuura/shared` (`packages/shared/src/security/keyRevokePolicy.ts:140`). It is the same predicate billing, governance, security, staking and wallet-connector use. The PR rolls no copy of its own.
- Line-by-line comparison with the other platform lists in the repo:
  - `auth/routes/users.ts:193` `PLATFORM_ADMIN_ROLES = ['SYSTEM_ADMIN','SUPER_ADMIN','admin','super_admin']`, exact match. Auth accepts **`admin`**, which shared refuses. Shared accepts `system_admin` and `Super_Admin` (any ASCII casing), which auth refuses.
  - `auth/middleware/authenticate.ts:249`: SYSTEM_ADMIN / super_admin / SUPER_ADMIN, exact.
  - `tokenisation/index.ts:223`: adds **`platform_admin`**, which shared refuses.
- Consequence: a principal carrying lowercase `admin` or `platform_admin` as a platform admin gets 403 on both routes, which I measured. The seeded platform admin carries `super_admin` (auth's own comment) and is accepted. This is the pre-existing KS-1536 split, not introduced here. The PR picked the platform-wide shared predicate, which is the right one.
- TESTED: cells 13, 14, 17–19, 49, 50, 53–55.

**G163-F3 (LOW, test gaps): 20 mutants on the two route files: 16 killed, all by AssertionError; 4 survive.**
- Killed: either guard removed; loose `String(userId) ===`; owner inverted; `||` changed to `&&`; the siblings' fail-open form; the `String(role).toUpperCase()` set test (KS-1591) on each route; ADMIN admitted on each route; any role admitted; the referee admitted on /qualify; no principal let through on each route; 403 changed to 401; the /qualify guard moved after the body parse.
- Survivors:
  - M4 (drop `!== ''`) and M5 (drop `typeof === 'string'` while keeping `===`) are **equivalent**. Express never yields an empty path param (measured 404), and a strict `===` against the string path can never match a non-string.
  - M6 (a case-insensitive owner compare) and M18 (role `.trim()` before the predicate) **survive the PR's suite**. My live matrix kills both (cells 75, 25–27, 61–62). Suggested cells for a later pass, not blocking: owner id upper-cased, and `" SUPER_ADMIN"`.
- HOW: `scripts/mutants.py`, `logs/mutants.json` (sha-restored, restore OK).

**G163-F4 (INFO): the in-route "no principal" fail-closed branch cannot be reached in the deployed stack.**
- FOUND: `authenticate()` answers 401 first, at base and head alike (cells 0 and 36). The branch only matters if the routes were ever mounted without `authenticate()`. As defence in depth it is fine.
- FOUND: `/check` needs the `userId` claim. A `sub`-only token is refused. Auth always signs `userId` (`auth/services/jwt.ts:194/220`), so no legitimate break.

**G163-F5 (INFO, question 4): no in-repo caller is refused.**
- FOUND: I re-ran the whole-repo `git grep` at develop `df0d1f8e4` (5,586 files, every top-level dir), searching for `referrals/qualify|milestones/check|qualifyReferral(|checkAndAwardMilestones(` outside the referral service's own routes, services and tests. It finds only the OpenAPI yaml, the service's route-list and openapi files, and one Schemathesis baseline key.
- Positive control: `referrals/generate` is found in 15 files, including 1 issuer-frontend file.
- The 2 frontend files that mention milestones only render `milestoneProgress` data.
- The gateway proxies `/api/milestones` and `/api/referrals` with path identity.
- The Schemathesis default persona is `super_admin` (`systemTest/schemathesis/config/settings.py:51`), so the sweep's default path is still admitted. The author's "would now see 403" caveat applies only to a non-default persona.
- `connector` tokens (`auth/jwt.ts`, role `connector`) are refused, which I measured. A future service-to-service caller needs a platform token.
- Pre-existing, unchanged: nothing in the repo ever calls `/qualify`, so the "svc-to-svc on first paid action" step has no implementation.

**G163-F6 (INFO): question 5 and the author's figures, all re-measured and matched.**
- 25 new cells. Red first, with base route files under head's tests: **16 of 25 fail, every one an AssertionError** ("expected 200 to be 403" and "expected 400 to be 403"). 9 controls pass.
- The KS-444 file passes under the base routes too: 17 of 33 green.
- Head: 33 of 33 (25 new + 8 in qualify.validation.test.ts).
- Whole referral suite: base 12 files / 77 tests; head 13 / 102, twice, rc 0.
- tsc, service config and tests-included, at base, head and combined: 0 errors.
- KS-444 file diff: one comment line replaced, plus an injected SYSTEM_ADMIN principal middleware. **No assertion line changed.**

**G163-F7 (INFO): 1979 × 1980 merge.**
- **Shared files: none.** 1980 touches 6 files and 1979 touches 5. Their intersection is empty.
- develop moved 27 files since base. 0 are shared with either PR, 0 are under services/referral, and 0 are in shared or the lockfiles.
- `merge-tree --write-tree`, all rc 0:

  | merge | tree |
  |---|---|
  | 1980 onto develop `df0d1f8e4` | `a1f150c72f11` |
  | 1979 onto develop | `ef480fd75785` |
  | (develop+1980)+1979 | `7dd066981a69` |
  | (develop+1979)+1980 | `7dd066981a69` |

  **Both orders give the identical tree.**
- Combined tree, whole referral suite: 14 files / 119 tests. Run 1 had 1 failure, the known G153-F8 cold-import timeout (`control ks1868 C1`, 8116 ms, in a file neither PR touches). Run 2 was 119 of 119. tsc 0.
- Combined principal matrix: identical authorisation to head.
- Note: 1980 on its own does not stop the **owner or a platform role** re-awarding by calling `/check` again. That is KS-1956, PR 1979, gate 162. At head without 1979 the allowed check writes the reward row but no progress row. Merge both.

**G163-F8 (PRE-EXISTING, HIGH, not this PR, card it): `POST /api/referrals/apply` takes the referee from the BODY, with no owner check.**
- FOUND (measured at head through the real service, `logs/probe/head_apply.json`): USER X sends `{code: A's code, userId: V}` for a victim V who never signed in. The service answers **201** and writes three rows: a PENDING referral A→V, A's code usage +1, and a **25 SECURA REFERRAL_BONUS reward row for V**.
- `ipAddress` and `deviceId`, the fraud-check inputs, are also taken from the body (`ipAddress: body.ipAddress || req.ip`).
- Impact: any signed-in user can bind any user id to any referrer's code, with fraud inputs of their choosing. When V is later qualified, which this PR now restricts to a platform role, A is paid. This is the same class as G153-F3, the defect this PR fixes on the sibling routes. It is not introduced or touched by PR 1980.

## NOT tested
- The api-gateway hop live (read only: `proxy.ts:1079-1088`, Authorization forwarded).
- JWKS key resolution (static `JWT_PUBLIC_KEY` path only).
- Whether a refresh token is accepted as a bearer token (pre-existing, both versions alike).
- Callers outside this repo (crons, other repos).
- The Schemathesis sweep itself.
- The four platform suites, CI, and Node 24.
- PR 1979's own correctness (gate 162).
- Mutating the shared `isPlatformRole` (it has its own KS-1591 tests).
- Concurrency on the allowed paths.

## Plain answer for Kam
Before this change, anyone signed in could make the referral service pay milestone rewards for any user and mark any referral qualified, which pays the referrer. With it, only the user themselves (for their own milestone check) or a platform admin can. I tried 92 caller cases (about 50 kinds of caller) against the running service, including tricked-up role names and forged headers. Every refused one changed nothing in the database. It merges cleanly with the re-award fix (PR 1979) in either order, and the two should go in together. Separately, and older than this PR: the "apply a referral code" route lets one user sign someone else up under any referrer's code. That deserves its own card.
