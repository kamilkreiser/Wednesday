VERDICT: GO WITH NOTE at head c2cfd51f3fb3 (tier 1, round 1 of 2; landing tree 3a31507c3da9 on develop 0f472ec20093; 0 blockers, 4 notes)
model: claude-opus-5-5 -- G1 (tier 1, platform-wide notification record write guard) -- P1-P4 no -- gauge 52%

## BLUF

- **GO WITH NOTE.** The guard is correct, exact-match, by id not by role, returns before any write, and uses the house 403 shape. All 7 mutants I planted were killed. The api-gateway suite at the landing is 1,169/1,169 (120 files) against develop's 1,163/1,163 (119 files): 0 vanished, 0 changed status, and the only new cells are the PR's 6.
- **Develop moved** after the brief (N1). Live develop is `0f472ec20093` (KS-1671, one m365-integration test file). The landing tree on live develop is `3a31507c3da9`, not the predicted `22b9299dd24a`. The predicted tree does reproduce on the brief's develop `09336b240721`, so the move is benign.
- **Reach (Q1), from repo evidence only:** no real principal can carry `userId === 'platform-settings'`. Real JWT userIds are `users.id` or `platform_admins.id`, both UUID columns. API-key principals are `connector:<id>`, and a connector Bearer is refused. The only path is a test token, which needs NODE_ENV in {development, test} AND ENABLE_TEST_TOKENS=true. Whether any live server meets both is decided by that server's own `.env` and was NOT measured (N2).
- **Not this PR's fix, both measured:** the per-user GET still hands the full platform record to that id (N3). A sibling reserved id `default` lets its holder write the bucket every anonymous GET reads (N4). Both have the same reach as the bug itself.

## Findings

### Blockers
None.

### Notes

**N1. Develop moved, so the landing tree differs from the prediction. Benign.**
- Live develop at start and at the re-read (15:38Z) is `0f472ec20093995381d938aca5c5380f7caf6fef`. The brief's develop was `09336b240721…`.
- The one new commit is `0f472ec20` "Refs KS-1671: cells for the OAuth callback's code read". It changes only `services/m365-integration/src/__tests__/ks1671-the-oauth-callback-drops-a-non-string-code.test.ts`.
- `git merge-tree --write-tree`:
  - on live develop: `3a31507c3da9ea587ddebc0894730c9756abb1f4`;
  - on `09336b240721`: `22b9299dd24aa8ff8b1dd1c48a3acd6d9cfd1446`, which equals the author's prediction.
- `git diff --name-only 22b9299d 3a31507c` lists only that m365 test file. `git diff --quiet 09336b24 0f472ec2 -- packages services/api-gateway` is clean. The positive control for that zero is the same diff, which shows the m365 file.
- Merge-base is `88b8ceb9`. Three-dot develop...PR is 2 files, matching the PR: `admin.ts` +5 and the new test +138.

**N2. Reach is test-token-only in every shipped configuration. Live state is unmeasured, and it sets severity.**
- **User JWT** (`services/auth/src/services/jwt.ts:194`): `userId: user.id`. `users.id` is `UUID PRIMARY KEY` (`migrations/001_initial-schema.sql`). `platform_admins.id` is `UUID PRIMARY KEY` (`docker/init-platform/01-platform-schema.sql:75`). A non-UUID id cannot be stored, so it cannot be minted.
- **Connector**: the userId is `connector:${connectorId||'api-key'}`, in the gateway at `auth.ts:392` and in auth at `jwt.ts:291`. The prefix makes `platform-settings` impossible. A connector JWT presented as a Bearer is refused (`auth.ts` KS-1198).
- **Shared `token-rotation.ts`** (HS-style secret): no service imports it. The only hit outside its own source is its own test. The gateway verifier is RS256-pinned in any case.
- **Test tokens** (`parseTestToken`, `auth.ts:122`): return null unless NODE_ENV is in {development, test} AND `configureAuth({enableTestTokens})`. That flag is fed by `ENABLE_TEST_TOKENS === 'true'` (`index.ts:214`).
  - `index.ts:79-91` exits FATAL at boot if NODE_ENV is production, staging or demo with that flag on.
  - Probe P5 (below) confirmed refusal with 401 under NODE_ENV demo, staging, production, `dev` and empty, with the flag on. Positive control: `development` gives 200.
- **Azure** (`deployment/azure/services.bicep:613`): the gateway's NODE_ENV is the `environment` param. `deploy.sh` allows only `dev` or `demo`. ENABLE_TEST_TOKENS is never set (case-insensitive grep: 0 hits; positive control: NODE_ENV hits in the same file). Neither `dev` nor `demo` passes the env gate.
- **Compose (the kintsugi/demo VM shape)**: `docker-compose.yml:427` sets `NODE_ENV=${NODE_ENV:-development}` and `:521` sets `ENABLE_TEST_TOKENS=${ENABLE_TEST_TOKENS:-false}`. The repo defaults leave test tokens OFF, but NODE_ENV defaults to `development`. So a server whose own `.env` sets `ENABLE_TEST_TOKENS=true` without setting NODE_ENV to demo, staging or production WOULD accept a test token with `sub: platform-settings`.
- Kintsugi's `.env` is authored on the box and is not in the repo (`KINTSUGI-DEV-SERVER-PLAN.md:93`). Read nothing, touched nothing.
- **Severity as measured**: defence in depth on every repo-visible config. It becomes a live non-admin overwrite of the platform record only on a box with that `.env` combination. The ticket should stay open until someone reads those two variables on kintsugi and demo, as the author already says.

**N3. The read side still returns the whole platform record to that id. Same reach as N2. Not this PR's fix.**
- `admin.ts:1478`: `GET /api/settings/notifications` reads `getNotificationSettings(userId)` with no reserved-id check.
- Probe P1: a test-token principal `platform-settings` gets 200 with the seeded `general` block, and the whole record is spread into the body, including `integrations[].config`.
- `/api/verification/policy` already exposes only the `verification` sub-block publicly. This path exposes the rest, including the connector allow-lists.
- Not reachable by a real principal per N2. Suggest the same one-line guard on the GET, or the separate-key-space shape, as a follow-up on KS-1262.

**N4. A sibling reserved id, `default`, is not covered. Same reach as N2. Not this PR's fix.**
- The anonymous GET reads bucket `'default'` (`admin.ts:1477`, `req.user?.userId || 'default'`). The PUT writes `notif:<userId>` for any id except `platform-settings`.
- Probe P3: a test-token principal with `sub: 'default'` PUTs `{planted}` with a 200. An anonymous GET then returns `planted`.
- P4 is the positive control: before any write, the anonymous GET returns the documented defaults and no `planted`.
- This is the KS-719 shared-anonymous-bucket class, reopened through an id rather than through missing auth. It needs a UUID-shaped real id to be impossible, which it is (N2), so it shares this bug's reach exactly.
- The narrow guard was a deliberate choice, disclosed in the PR. A separate key space would close both N3 and N4. Worth a ticket.

## Questions answered

1. **Reach**: N2. No real principal per repo evidence; test-token only; the live `.env` is unmeasured.
2. **Completeness**: `git grep` over the whole tree at the PR head for `NotificationSettings|notif:|platform-settings` and `secuura:gateway|gateway:notif|REDIS_PREFIX`, tests excluded:
   - Positive control: it found both known writers, `admin.ts:1146` and `:1499`.
   - Writers: those two only. Readers: `admin.ts:1119, 1144, 1154, 1478`; `verification.ts:783, 857`; `health.ts:64`.
   - The only raw key construction is `redis.ts:672/681`, as `secuura:gateway:notif:<key>`. No other service builds that prefix; the only other hits are api-gateway test files.
   - No other route passes a caller-chosen key.
   - **Normalisation**: none. The guard is `===`. Redis keys are binary-safe and exact; the in-memory fallback is a `Map`, also exact. `Platform-Settings`, ` platform-settings`, `platform-settings ` with a trailing space, `platform-settings\u0000`, `PLATFORM-SETTINGS`, `platform-settings%00` and `../platform-settings` are distinct keys. Probe P2: all 7 return 200, each writes its own key, and the platform record is unchanged.
   - The userId comes from the verified token, not the URL. The route has no path parameter, so URL-encoding and `..` have nothing to act on.
3. **Read side**: N3.
4. **Cells can fail**: 7 mutants planted in my clone's `admin.ts` by exact-string replacement. Every one was killed, and the tree was restored to blob `15b37033f` after each.

   | Mutant | Killed by |
   | -- | -- |
   | guard removed | R1, R2, R3 |
   | role-conditional (`&& role !== 'admin'`) | R2 |
   | no `return` after the 403, so it falls through and writes | R1, R2, R3 |
   | refuse everyone | C1, C2 |
   | case-insensitive compare | C2 |
   | `startsWith` prefix | C2 |
   | status 400 instead of 403 | R1, R2 |

   - **Red-first**: develop's `admin.ts` (blob `046a17226`) under the PR's test fails R1, R2 and R3; 3 passed.
   - **403 shape**: all 3 `status(403)` sites in `admin.ts` use `{ success: false, error: { code: 'FORBIDDEN', … } }`. The new one matches.
   - **Nothing written on refusal**: asserted by R1 and R2 (`writes` equals `[]`) and R3 (record equals SEED). The no-return mutant proves those cells can see a write.
5. **Landing**:
   - Merge-tree: N1.
   - Full suite, by cell name, via vitest JSON, rc 0 at both:
     - develop `0f472ec2`: 119 files, 1,163 passed, 0 failed, 0 skipped, 0 todo;
     - landing commit `1901a441` (tree `3a31507c`): 120 files, 1,169 passed, 0 failed, 0 skipped, 0 todo;
     - vanished 0; status changes 0; new 6, all in the KS-1262 file.
   - **Test type-check**: `scripts/typecheck-tests/check.cjs services/api-gateway`: rc 0, 155 files examined (120 under `__tests__`), 27 errors, all in the baseline, 0 new, 0 stale. Planted control: a `string`→`number` assignment appended to the new test gives rc 1 and is reported as 1 new TS2322 at line 140. The file was restored to blob `1010b8d67`.
   - **Build**: `tsc -p services/api-gateway/tsconfig.json --noEmit`: rc 0.
   - **Blobs**: the post-images equal the Spark diff's declared `15b37033f` and `1010b8d67`, and the pre-image equals develop's `046a17226`. The PR is one commit on parent `88b8ceb9`.

## How

- Clone: `git clone --shared` from `2_Project_Files/local-model/spark/cache/src` into the scratchpad `gate_aw1/`.
- Fetch: `refs/pull/1635/head` and develop, with the Secuura deploy key set as that clone's `core.sshCommand`. Literal paths throughout.
- Dependencies: the cache's `node_modules` symlinked per entry. `@secuura/*` was copied as relative links, so it resolves into my clone. The lockfile and package.json files are identical between the cache HEAD `390cc0a3` and the PR head.
- `packages/shared` was built with the clone's tsc (rc 0).
- Every tool ran as `node <clone>/node_modules/...` with `--root` set into the clone.
- The probe cells P1-P5 were written into the clone as `zz-gate-aw1-probe.test.ts`, run (5/5 pass), then moved out to `scratchpad/aw1_tools/` before the suites ran. The clone's `git status` was clean before the suites.
- Logs are in `scratchpad/aw1_tools/`: `suite_origin_develop.json`, `suite_aw1-landing.json` and `tc_planted.log`.

## NOT RUN

- No live environment was read or driven: kintsugi, demo, the Azure dev/demo Container Apps, and any server `.env` (N2 stays open).
- No real Redis. P2's key-distinctness was shown on the recording stand-in plus the source read of `redis.ts`, not against a Redis server.
- No real RS256 JWT carrying `platform-settings`, since none can be minted (UUID columns).
- No ESLint run and no preflight. Docker is prohibited.
- The GitHub PR body, PR comments and the Linear ticket were not read. Census of other open PRs touching these files: not re-run.
- Suites other than api-gateway were not run. The PR touches only api-gateway.
- Wednesday tree check (`git -C /Volumes/DevMASTER/WEDNESDAY status --short`), taken before this file was written: 0 lines, so 0 untracked paths outside the allowed roots. The positive control is that this verdict.md must now appear as untracked.

sha256: eb9bb0477251b2e00b8a1e134a47a710bc043ee27e315361d17a495996dc8d18
