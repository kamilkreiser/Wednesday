VERDICT: GO at head 009749ed25651065445e3a3ee76eab83b6e38aec (tier 1, round 1 of 2; landing tree db51b5bb4c807cadbacd08720e530a87a6e90509 on develop 722e07f19cee; 0 blockers, 4 notes)

# Gate X1: PR #1613 (KS-1195), tier 1, round 1 of 2. Opus, findings only

**Head under gate:** `009749ed25651065445e3a3ee76eab83b6e38aec` (tree `2a094dd9eb39fc78781c61381f7bb6d96df0753e`, this matches E's claim)
**Live develop:** `722e07f19cee683ea037930e601e380a9491f7b5`. I read it by `ls-remote` at the start and again at 06:08Z before writing this verdict, and it had not moved. The PR head had not moved either.
**Landing tree** (`git merge-tree --write-tree origin/develop 009749ed2565`): **`db51b5bb4c807cadbacd08720e530a87a6e90509`**, with no conflicts.
**Merge-base:** `846ae2788b3b`, which is E's base. Develop has gained one commit since then (`722e07f19`, KS-1634). It touches originate only: `routes/verification.ts` plus two tests, 3 files.
**Instrument:** my own `git clone --shared` in scratch. I fetched develop and `refs/pull/1613/head` from origin over the checkout's deploy key. I committed the landing tree as a scratch-only commit (`b96393313`, never pushed) and worked in a scratch worktree. The `node_modules` are symlinks to the checkout's install, except `@secuura/*`, which resolves to the worktree's own packages. I built `packages/shared` with `tsc` (rc 0). I wrote nothing under `!CODING`.

## Findings (no blockers)

- **N1 (note, pre-existing, not this PR): ROTATE reaches 3,000 only when a platform role does the rotating.** The security service refuses `rotate:true` from a provisioning connector (`services/security/src/index.ts`, the `isProvisioner && data.rotate === true` 403, at ~:1347). So if Platform S's own instance key calls register-connector with `rotate`, it still gets a 502 there, the same as it does today. A rotate carried out by an admin or super_admin mints at 3,000, which I measured in cell X1-C below. This fits Kam's "rotating a live key is Kam's", and #1613 changes nothing about it. E's ROTATE cell drives the route as super_admin, so it covers the reachable path.
- **N2 (observation on the red-first claim):** 17/2 is real, and I reproduced it exactly. However, **13 of the 17 go red with `TypeError: resolveConnectorRateLimit is not a function`** (the export is missing at develop), not with a behavioural assertion. Only the 4 route cells go red behaviourally (`expected undefined to be 3000/2500`). The 13 resolver cells do discriminate behaviour: my M2 mutation below reds exactly one of them.
- **N3 (doc nit, outside the diff):** `services/api-gateway/src/docs/developer-portal.html:564` still says "Per API key / OAuth app: 1,000 req/hour". That remains true for every key except new S connector keys, so it now under-describes those. This is not a blocker and not in the PR's file list.
- **N4 (truth of the PR's own comments):** the PR comment says `services/security/src/index.ts:666` is `rateLimit: z.number().int().min(1).max(10000).default(1000)`. I confirmed that exact line on live develop.

## Q1: Does a NEW key actually get the ruled ceiling? **Yes, end to end in code, and the stored value measured in-process.**

The chain, read on live develop plus the PR:
1. **Gateway:** `routes/platform.ts` register-connector `POST ${securityServiceUrl}/api/keys` body carries `rateLimit: resolveConnectorRateLimit()`. This is the only mint call on the route, and it is reached for a new organisation and for an explicit `rotate`.
2. **Security, the same route** (`app.post('/api/keys', …)` at index.ts:1161): `createApiKeySchema.parse(req.body)`, where the schema at :666 is `rateLimit: z.number().int().min(1).max(10000).default(1000)`. It is accepted, not stripped. Then `apiKey.rateLimit = data.rateLimit` (:1372) and the key is saved via `dbSaveApiKey` / `saveKeyAndRetirePriors`. Both use `apiKeyInsertStatement`, which writes the `rate_limit` column ($8, :421/:436). The read-back mapper is `converters.ts:167` `rateLimit: Number(r.rate_limit)`.
3. **Validate** (`/api/keys/validate`, :1916) returns `rateLimit: apiKey.rateLimit, rateLimitWindow`.
4. **Gateway auth** `validateApiKey` (`middleware/auth.ts:248`) sets `meta.rateLimit = data.rateLimit || 100`. The sk_ branch copies it to `req.user.rateLimit` (:402) and records a per-key bucket. `enforceClientRateLimit` (`middleware/rateLimitEnforce.ts`) uses `limit = user.rateLimit`, `windowMs = user.rateLimitWindow*1000`. Develop's own `ks1195-per-key-rate-limiter-runs-after-authentication.test.ts` already proves that the limiter 429s at the `rateLimit` returned by validate.
5. **Not binding:** the global limiter (`index.ts:479`) is 300/min/IP in prod (10,000 non-prod). That works out to 18,000/h, so it does not undercut 3,000/h.

**Measured.** I wrote a scratch-only cell, `services/security/src/__tests__/x1-gate-ratelimit-readback.test.ts`, never pushed. It uses ks908's pattern: the real app on loopback, real RS256 tokens, no DB. Result: **9/9 green**.
- X1-A: platform role, `rateLimit 3000` gives 201 echoing 3000, and `/api/keys/validate` returns `{valid:true, rateLimit:3000, rateLimitWindow:3600}`.
- X1-B: **the real caller shape** (org-less `connector` + `organizations:register` instance key) with a connectorId, minting at 3000, gives validate 3000.
- X1-C: platform-role rotate of an existing connector, with the new key at 3000, gives validate 3000.
- X1-D: instance-provisioner rotate is refused with 403 (this is N1).
- CONTROL-1, the positive control for "the field is not ignored": with `rateLimit` omitted, validate returns **1000**. The instrument therefore tells "accepted" apart from "defaulted".
- CONTROL-2 (bounds): 0 gives 400, 10001 gives 400, 1 gives 201, 10000 gives 201.

The gateway suite is under Q5.

## Q2: Are existing keys unchanged? **Yes, by code and by E's controls.**

On the `if (!rotate)` branch for an existing organisation, the route returns `alreadyRegistered` **before** the mint. The only key call on the route is a `POST /api/keys` INSERT; its `ON CONFLICT (id)` touches only usage, active and connector_id, never `rate_limit`, and ids are fresh `key_<uuid>`. E's CONTROL-1 (zero `/api/keys` hits on re-register) and CONTROL-2 (the recorder does see a key-surface PATCH) are green on the landing tree, and green at develop's `platform.ts` as well. With `rotate`, a new key gets the ruled value: E's ROTATE cell, plus my X1-C at the security service. A rotate by the Platform S provisioner is refused upstream (N1). I did not rotate any live key.

## Q3: Validation. **Each input behaves as E claims, and the bounds are the security service's own.**

The bounds are `CONNECTOR_RATE_LIMIT_MIN = 1` and `MAX = 10000`, equal to `services/security/src/index.ts:666` `.min(1).max(10000)`. I measured `resolveConnectorRateLimit(raw)` in a scratch cell with the logger.warn spied:

| input | result | warn |
|---|---|---|
| `"3000abc"` | 3000 (fallback) | 1 |
| `"3e4"` | 3000 (fallback) | 1 |
| `"0"` | 3000 (fallback) | 1 |
| `"10001"` | 3000 (fallback) | 1 |
| `" 3000 "` | 3000 (accepted, trimmed) | 0 |
| `""` | 3000 (default) | 0 |
| unset (`undefined`) | 3000 (default) | 0 |
| `"1"` / `"10000"` | 1 / 10000 | 0 |
| extra: `"03000"` | 3000 accepted | 0 |
| extra: `"+3000"`, `"3 000"`, Arabic-Indic `"٣٠٠٠"`, `"0x10"`, `"2500.0"`, `"99999999999999999999"` | 3000 fallback | 1 each |
| extra: `"3000\n"` | 3000 accepted | 0 |

With no argument (the env-read path), unset gives 3000 and `PLATFORM_S_CONNECTOR_RATE_LIMIT=4321` gives 4321. That shows the value is read per call, not at module load.

## Q4: Is red-first real? **Yes: 17/2, then 19/19. Both of my mutations go red.**

- At develop's `platform.ts` with E's test file present: **17 failed / 2 passed**. The two that pass are exactly CONTROL-1 and CONTROL-2 (N2 explains the failure classes).
- Restored: **19/19**.
- **M1 (my own): send rateLimit only when the env var is set:** `rateLimit: process.env.PLATFORM_S_CONNECTOR_RATE_LIMIT ? resolveConnectorRateLimit() : undefined`. This reds **2**: "mints at the ruled 3,000/hour when the env var is unset" and "ROTATE …".
- **M2 (my own): lower bound off by one** (`n < CONNECTOR_RATE_LIMIT_MIN` changed to `n < 0`). This reds **1**: "falls back … below the schema minimum".
- I reverted each mutation with `git checkout --` in scratch, and `diff --stat` came back empty after each.

## Q5: Landing. **Clean.**

- `merge-tree` onto live develop `722e07f19` gives tree **`db51b5bb4c807cadbacd08720e530a87a6e90509`**, no conflicts.
- **The api-gateway full suite on the landing tree: 117 files, 1151 passed, 0 failed, rc 0.** This equals E's 1151/1151 at 117 files, as expected, since develop's only new commit is originate-only.
- Develop control: the same suite with develop's `platform.ts` and E's test excluded gives **116 files, 1132 tests**, matching E's control counts. One cell (ks1090, the in-suite test-typecheck gate) went red **only because of my own setup**: E's test file and my scratch file stayed on disk while `platform.ts` was develop's, which gave 2 "new" TS2305 errors. That is not a develop defect, and the same cell is green in the landing run.
- `tsc -p tsconfig.json --noEmit` on landing gives rc 0 with 0 lines.
- `tsc -p tsconfig.test.json` gives 27 errors. All 27 are in 7 pre-existing test files (csrf, ks1165, ks1374, ks1457, ks1464, ks695, rateLimitEnforce), and **0 are in `platform.ts` or the new test**. Positive control: `--listFilesOnly` shows both files inside the program. This matches E's "27 in the baseline, 0 new". The in-suite ks1090 gate is also green on landing.
- The 3-dot file list (`develop...009749ed2565`) is **exactly 2 files: `routes/platform.ts` (+64) and `__tests__/ks1195-register-connector-mints-the-ruled-rate-limit.test.ts` (+282), 346 insertions, 0 deletions**, which matches E.

## Q6: `mergeable_state: unstable`. **What is readable shows CI jobs that never started, repo-wide. #1613's code did not cause it.**

These are read-only GETs with the project's `GH_TOKEN`. `pulls/1613` returns 200: `mergeable: true`, `mergeable_state: "unstable"`, head `009749ed2565`, base `develop@722e07f19`. As E reported, `check-runs`, `status` and `branches/develop/protection` return **403**. However, **`actions/runs?head_sha=…` and `actions/runs/{id}/jobs` return 200**:
- 6 workflow runs on the head. 5 concluded `failure`: pr-premerge-ack, pr, PR Security Gates (KS-168), PR Lockfiles, and Security Scanning. Dependabot was `skipped`.
- **Every failed job has 0 steps and an empty `runner_name`.** The jobs never started on a runner. That includes trivial ones such as "Linear ticket present".
- It is the same on other heads. The 60 most recent runs repo-wide (all 2026-10-19) are 53 failure and 7 skipped, with 0 successes. A develop `push` run (`39205923364`, Code Security Gates) shows the same 0 steps and no runner. The newest `success` run anywhere is 2026-10-14 (dependabot), and the newest PR success is 2026-10-12.

So "unstable" comes from failed, non-required, never-started Actions jobs that affect the whole repo. **Why** the jobs are not getting runners (billing, spending limit, runner availability) is not readable with this token, because annotations live behind check-runs, which return 403. I am not guessing at the cause.

## What I did NOT run

- No live stack, Docker, Postgres or Redis. I did not prove end to end that a 3,000 key is throttled at the 3,001st request. That is E's declared gap: Stuart's `@k-live` run.
- No DB round trip: X1 ran in memory, and the `rate_limit` column write/read is proven by code only (:421/:436, converters.ts:167).
- No eslint and no push-preflight hooks.
- I did not run the security service's full suite. I ran only my 9 cells.
- No frontend.
- No GitHub, Linear or agentmail writes. The only GitHub calls were GETs.

## Scratch artefacts (not pushed)
`…/scratchpad/x1/` contains: `repo/` (clone, branch `x1-landing`), `land/` (worktree), `full_landing.out`, `full_develop.out`, `redfirst.out`, `M1.out`, `M2.out`, `restored.out`, `table.txt`, `tsc_main.out`, `tsc_test.out`, `gh_*.json`, `jobs_*.json` and `runs_*.json`. The two scratch cells are at `land/Blockchain/Dev/services/security/src/__tests__/x1-gate-ratelimit-readback.test.ts` and `land/Blockchain/Dev/services/api-gateway/src/__tests__/x1-gate-resolve-table.test.ts`.
sha256: 2c633ea76b30870c0048776ce6450c113374ff0a999cf14834f312364f30c2ba
