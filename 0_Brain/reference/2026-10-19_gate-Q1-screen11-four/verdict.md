VERDICT: #1602 KS-1377: GO WITH NOTE at head 70dc59643b5aaa089606e51a43d2948ab5c671b2. Measured on real PostgreSQL 18.3: every GREATEST/NULL arm is correct, and 20 clients × 25 uses give 500/500 (develop's statement gives 31/500). The two residue sites are acceptable on KS-1377 as Refs. R's :425 reading is overstated (see Q1).
VERDICT: #1603 KS-1617 A.3: GO WITH NOTE at head f51d7cab124b9dc9e15172b1fba0cd01fe41e819. R is right that the status reaches the caller's 400 body. Recommend shipping it as is. The same 400 already carries the provider's whole token-endpoint error body (pre-existing).
VERDICT: #1604 KS-1617 A.2: GO at head 0cc48741299c9d4d8277eafd31c8b6f674ed2da1. Measured with the real logger: the description cannot forge a log line in either mode, and it is not echoed in the response.
VERDICT: #1605 KS-1507: GO at head 934ce30c3c118626647ced229a11ad55a4fabb41. Test-only. Both of my mutants are killed: trim by the whitespace cell, and `=== undefined` by the empty control.

# GATE Q1: the SCREEN_11 four, batched, round 1 of 2

**Method.** Gate O1's method, controls and hard limits, as the brief says.

**Live tip.**
- `git ls-remote` at 13:3x AEDT gave develop `37834600a543cb0276f427d969ac034d9df74fbd`, which equals the brief.
- **Develop MOVED during the gate.** At 13:5x it read `04a4a33938f05312a184fd2ca294745d628ff75d`, tree `24cc02989cf1ad06565b718f1227393e5ec81f46`, re-read at 13:56. That is one commit, "KS-1612: anchor guard reads external ids; migrations 050/051 bar id claims".
  - It touches exactly #1568's 12 file paths: anchoring, originate and migrations 050/051.
  - It changes no blob under `services/security`, `services/auth`, `packages/shared`, `package.json` or `package-lock.json`. Those tree ids are identical before and after.
  - I re-predicted everything onto 04a4a339 and re-ran the suites there. The figures below are on the LIVE tip.
- All four heads equal the brief and R's mail, at both reads.
- Each PR is one commit on 37834600 by `Kam Kreiser <kamil.kreiser@secuura.ai>`, so the author is a Secuura identity.

## Named questions

### Q1. #1602's GREATEST/NULL arms, MEASURED

**Setup.** A scratch cluster: Homebrew PostgreSQL 18.3, initdb in `q1/pgdata`, loopback 127.0.0.1:55432 only, no Docker. It was stopped at the end.
- The probe is `q1/pgprobe/probe.cjs`, using the repo's own `pg` 8.20.0 driver.
- The table has the shape of `migrations/002_verification-tiers.sql:553-567`: `last_used_at TIMESTAMPTZ` and `usage_count BIGINT DEFAULT 0`.
- PostgreSQL infers `$2` as `timestamp with time zone` from the column.

| arm | stored | $2 | #1602 (NEW) | develop (OLD) |
|---|---|---|---|---|
| A1 first use | NULL | T | last_used_at = T, count 1 | T, 1 |
| A2 $2 older | T0 | T0−1d | **T0 kept** | T0−1d (moves back) |
| A3 $2 newer | T0 | T0+1d | T0+1d | T0+1d |
| A4 $2 NULL | T0 | NULL | **T0 kept** (GREATEST ignores NULL) | NULL (wiped) |
| A5 both NULL | NULL | NULL | NULL | NULL |
| A6 usage_count NULL | T0 | T0+1d | count stays **NULL** (NULL + 1) | 1 |

**Concurrency** (separate connections, out-of-order timestamps):
- **N=20 × M=25**: NEW gives `usage_count = 500/500`, and last_used_at equals the max sent. OLD, emulating develop's read-the-row then write `$3 = read + 1`, gives **31/500**, and last_used_at is not the max.
- **N=20 × M=1**: NEW 20, OLD 1. This reproduces the drafter's carried figure, which is now measured rather than carried.
- **Under RLS as the app role.** I provisioned a migrated database the way `docs/DEV-PROCESS.md:135` describes: docker/init/*.sql 11/11, then migrations/*.sql **53/53** from the landing tree. `svc_api_keys` has FORCE RLS on.
  - The security integration suite (`vitest.integration.config.ts`) ran as `secuura_app`: **122/122 on develop and 122/122 on the landing tree**.
  - With `log_statement=mod`, the server log shows the new statement executed **26×** and the old one 26×. So the integration cells really drive `dbRecordApiKeyUsage` under the tenant GUC. Control: 402 `UPDATE svc_api_keys` lines in total.
  - No error was raised on the usage statement. The non-injected errors in the log are the same set on both trees.

**A6 (NULL count) is not reachable in practice.** Mint writes 0 (`index.ts:1374`). Migration 018 adds the column with `DEFAULT 0`, which backfills existing rows, and 019 inserts 0. Only a direct write can make it NULL.

**The two residue sites. My reading differs from R's on :425.**
- **:425 (`apiKeyInsertStatement` upsert)**
  - Mint and the KS-1549 rotate insert a fresh `key_${crypto.randomUUID()}` (`:1362`) with `usageCount: 0`. So `ON CONFLICT DO UPDATE` does not fire on them.
  - It fires on **revoke** (`:1566`). Revoke's key comes from `dbGetApiKey` (`:1511`), which reads the row fresh via `lookupKeyForRevoke` (`:518`).
  - So a revoke writes back the row's count *as it read it*. It loses only the increments that land between that read and the save. Its stale-memory arm is the fallback at `:522`, taken when the lookup throws.
  - Measured: fed a stale count, the upsert turns 500 into 3, and it also **moves last_used_at back** (2026-10-20 to 2026-10-19 05:00). That is a second arm of the same residue that R did not name.
  - Not widened by #1602: the old row was already lossy, and after a revoke the key is dead.
- **:1494 (key list served from `memApiKeys`)**
  - The value it serves is computed exactly as before. Validate refreshes memory from the row (`:1855`) and then adds 1 (`:1899-1900`), with no change in this PR.
  - So the **API's number is unchanged by #1602**. The row moves from lossy (31/500) to exact (500/500).
  - "Widens the API-vs-row divergence" is literally true, because the row became right. API-vs-truth does not move.

**Recommendation: ACCEPTABLE RESIDUE ON KS-1377. Do not hold #1602.** KS-1377 should record the `last_used_at` regress arm of :425 next to the count arm.

### Q2. #1603: does the new text reach the 400 body?

**YES. I re-read the chain at develop and confirm it:**
1. `routes/auth.ts:1030` calls `provider.exchangeCode(code)`.
2. `:1031-1035` catches the throw and throws `new BadRequestError(\`OAuth authentication failed: ${exchangeErr?.message …}\`)`.
3. `BadRequestError` extends `AppError` with 400 (`errorHandler.ts:30-32`).
4. `errorHandler.ts:293` writes `message: err.message`, and `:300` sends `res.status(err.statusCode).json(...)`.
5. It is mounted at `auth/src/index.ts:181`.

The other `exchangeCode` site, POST /social/link (`:1315`), is not caught. A plain Error there falls to the generic 500 (`errorHandler.ts` unknown-error branch), so on that route the new text reaches only the log.

**What a caller learns that it could not learn before:** the HTTP status that **Google's userinfo or Microsoft Graph `/me`** returned *after a successful token exchange*. That is, whether the provider refused the freshly issued token or its scope (401/403), was rate-limiting Secuura's OAuth client (429), or was down (5xx).
- Reaching that branch needs a valid `state` and a code the provider accepts. In practice that is the user doing their own sign-in.
- The **same 400 body already carries the provider's entire token-endpoint error body** on the sibling branch: `google.ts:39-40`, `microsoft-personal.ts:39`, and likewise apple :38, facebook :34, github :38 and linkedin :37. That is a strictly larger disclosure, and it is pre-existing.

**Recommendation: SHIP AS IS.** The alternative shape (status in the log only) would be cleaner in principle. But it buys nothing while the token-exchange branch echoes far more into the same body. If the gate wants that principle, it belongs in a follow-up that closes both branches.

### Q3. #1604: R's logger reading

**CONFIRMED, by reading the source and by measuring it** (`q1/logprobe/probe.ts`, the real `utils/logger.ts` from the head run through tsx).
- **Development mode:** `printf` (`:15-18`) with the meta `JSON.stringify`'d at `:16`.
- **Production mode:** `combine(json())` (`:33-34`).
- The hostile `error_description` was `\r\n` + a fake timestamped `[auth] info: FORGED…` line + an ANSI ESC + U+2028. In both modes it yields **1 line**, with CR/LF and ESC escaped.
- Control: a newline in the *message* splits the dev line (3 lines, forged at line start = 1). So the counter does see splits.
- **Not echoed:** I added a probe assertion to A2-1, temporarily, and restored the file. The 400 body contains neither `redirect_uri_mismatch` nor `invalid_request`, and does contain `OAUTH_PROVIDER_ERROR` (control: the body is searchable). 16/16 passed.
- **R's claim that "A2-3 asserts the raw response carries neither value" is overstated.** A2-3 sends no description and checks only `error`. Non-echo of the description was untested until this probe. See Nit 2.
- U+2028 passes through unescaped (JSON permits it). It is not a line split for a newline-delimited shipper. Observation only.

### Q4. KS-1641

Not gated. My reading of m365-integration `index.ts:465` **agrees** with R's, and adds that the `:464` log line is uncapped too and `:515` reflects the exchange `err.message`.

The admin routes check out: `App.tsx:62` declares `/settings` and no `/integrations`; `basename="/admin"` is at :93 and `base: '/admin/'` at `vite.config.ts:31`.

### Q5. Each PR

**Red-first** (`q1/redfirst.sh`). In each head worktree I swapped develop's product blob in (blob ids asserted equal to develop's), ran the PR's file, then restored it.

| PR | head | red-first | develop's swapped blob(s) | mutants planted / killed by |
|---|---|---|---|---|
| #1602 | 10/10 | 9/1, the failure is W3 only | `index.ts` c945b2f2 | M1 drop GREATEST: W3. M2 back to `$3 = k.usageCount`: W3 |
| #1603 | 5/5 | 3/2, exactly P1 and P2 (assertions) | `google.ts` 6b18d024, `microsoft-personal.ts` a37fd0cb | M3 Google status removed: P1. M4 MS status removed: P2 |
| #1604 | 16/16 | 14/2, exactly A2-1 and A2-2 | `auth.ts` ded3800b | M5 cap removed: A2-2. M6 key always present: A2-3 |
| #1605 | 14/14 | test-only, so mutants instead | n/a | M7 `!DATABASE_URL?.trim()` (R's mutant): the whitespace cell. M8 `=== undefined`: the empty CONTROL |

Every worktree was clean afterwards: tracked porcelain 0.

**Suite counts at the landing parent.** develop 37834600 gives security 346 and auth 1068.
- Security's first develop run was 345/1. The single failure was the ks578-ks643 KS-643 cell, at 5,965 ms (a timeout under a cold cache). The rerun gave 346/346. The cell sits in a file #1602 does not touch.
- Solo landing trees: each head's tree equals its solo merge onto 37834600.

| tree | security | auth | matches R |
|---|---|---|---|
| #1602 solo | 347/347 (the security subtree is identical in the chained tree) | n/a | yes |
| #1603 solo | n/a | 1073/1073 | yes |
| #1604 solo | n/a | 1071/1071 | yes |
| #1605 solo | n/a | 1070/1070 | yes |
| chained, on 37834600 (tree 44a92956) | 347/347 | 1078/1078 | predicted 347 / 1078 |
| **chained, on the live tip 04a4a339 (tree 34ea098a)** | **347/347** | **1078/1078** | predicted 347 / 1078 |

**`git apply --check` on the live tip 04a4a339**, through a temporary index (`q1/applycheck2.sh`):
- All four have rc 0.
- Control: a corrupted copy of #1602 is refused (rc 1).
- Applied cumulatively, the four give **tree 34ea098a022ca58aaff234a13c0603b21402fa14**, the same as the merge-tree chain.
- Control: re-applying #1602 on top of that is refused (rc 1).
- Self-report: my first "cumulative" `apply --check p1 p2 …` did NOT discriminate (the same patch twice still gave rc 0). I discarded it and replaced it with the real sequential apply above.

**Chained landing tree.** `git merge-tree --write-tree`, in order 1602, 1603, 1604, 1605, onto 04a4a339. Every step rc 0, no conflicts.

| step | tree after | solo onto 04a4a339 |
|---|---|---|
| 0 develop 04a4a339 | 24cc02989cf1ad06565b718f1227393e5ec81f46 | n/a |
| #1602 | 4e427c9d8c6241a131e0bf02a0f62eff9960ea7b | 4e427c9d |
| #1603 | 47731c97d4bff95632dcaad4b242d389db2a3702 | 0469f0f2 |
| #1604 | 7dad75679d1028b28e2a84db9dbc549a78b5fc83 | e42c1923 |
| #1605 | **34ea098a022ca58aaff234a13c0603b21402fa14** | a8bb28f8 |

The first chain onto 37834600 ended at tree 44a92956505eee25702cd38307fc936499bdc788.

**Files.**
- develop..final touches exactly 8 files: 2 + 3 + 2 + 1. Pairwise shared-file count is 0 for all 6 pairs. Control: #1602 against itself gives 2.
- **#1597** (head 8ec96bba, unchanged): 0 shared files with each of the four. It is originate only.
- **#1568**: 0 shared files with each, both at d2564aeb and at its newer head d74b7f95 (12 files: anchoring, originate, migrations). No PR in this batch touches a service either of them touches.

### Q6. Test Evidence, per suite per touched service

**Read:** each commit's message, which holds R's evidence: red-first, suite, tsc, ESLint.
**Not read:** the PR bodies on GitHub. The Secuura gh config reports "not logged into any GitHub hosts", and rule 5 bars using the global account. See NOT tested.

The touched services are **security (#1602)** and **auth (#1603-#1605)**. I ran:

| service | suite | develop 37834600 | landing tree |
|---|---|---|---|
| security | `vitest run` (unit) | 346/346 | 347/347 |
| security | **`test:integration`** (real PG, app role, FORCE RLS) | 122/122 | 122/122 |
| auth | `vitest run` (unit) | 1068/1068 | 1078/1078 |
| auth | **`test:auth-integration`** (`integration/ks968…`, DB `ks_full`) | 6/6 | 6/6 |

- tsc `--noEmit` on the landing tree: security rc 0 with 0 lines, auth rc 0 with 0 lines.
- ESLint (json) on all 8 touched files: 0 messages each. Control: the stdin probe with an unused variable reads 1. A first attempt with `--format compact` errored out (rc 2: the formatter is not in core), and the control exposed it.
- R ran neither integration suite. Both are green on both trees.

## Severities (file:line)

- **Minor 1, #1602 residue (not blocking, already on KS-1377):** `services/security/src/index.ts:425`. On revoke, the upsert writes back the count and `last_used_at` as read at `:518`. Measured fed a stale count: 500 becomes 3, and `last_used_at` moves back 19 h. The race window is read-to-save, or the `:522` stale-memory fallback.
- **Minor 2, pre-existing, the #1603 neighbour:** the token-exchange throws echo the provider's raw response body into the callback's 400: `providers/social/google.ts:39-40`, `microsoft-personal.ts:39`, `apple.ts:38`, `facebook.ts:34`, `github.ts:38`, `linkedin.ts:37`, through `routes/auth.ts:1031-1035`. This is larger than anything A.3 adds. It wants its own ticket if the gate rules that provider detail must not reach a browser, the principle `errorHandler.ts:176-190` already states for `error_description`.
- **Nit 1, #1603 scope:** `facebook.ts:44`, `github.ts:48` and `linkedin.ts:47` keep the status-less "Failed to fetch … user profile". A.3 covers 2 of the 5 profile-fetching adapters.
- **Nit 2, #1604 test:** no cell asserts that `error_description` is absent from the response. A2-3 has no description and checks only `error`. The probe above shows it is absent today. One `expect(r.raw).not.toContain('redirect_uri_mismatch')` in A2-1 would pin it.
- **Nit 3, #1602 test:** W3 pins the SQL by regex, not by behaviour. `GREATEST($2, last_used_at)` (equivalent) would red it, and a semantic regression with the same text would pass. The behaviour is what this gate measured on PG.
- **Observation, #1602:** A6. If `usage_count` is ever NULL (direct write only), `usage_count + 1` stays NULL forever, where develop's statement self-healed to 1. `COALESCE(usage_count, 0) + 1` would close it. Not reachable through the service.

## HOW

- **Clone.** `git clone --shared --no-checkout` into `q1/repo`, with origin `git@github.com:Secuura/Distributed_Secuura.git`. Fetched with the master checkout's `core.sshCommand` plus `-o ServerAliveInterval=30`.
- **Worktrees.** All inside q1/: `wt-dev`, `wt-land` (chain on 37834600), `wt-land2` (chain on 04a4a339), and `wt-1602` to `wt-1605` (heads).
  - node_modules are per-entry symlinks into the master checkout (read-only), with the `@secuura/*` links re-created.
  - `packages/shared` was built with tsc (rc 0, 29 dist entries) in every worktree.
- **Commands.** Suites ran by absolute path through `q1/incwd.py`; there was no `cd`.
- **Scripts.** All in q1/, run with /bin/bash: `chain.sh`/`chain2.sh`, `wt.sh`, `suites.sh`, `redfirst.sh`, `mutants.sh` (+`mutate.py`, which asserts one match), `echoprobe.sh` (EXIT-trap restore), `applycheck.sh`/`applycheck2.sh`, `static.sh`, `pgstart2.sh`, `provision.sh`, `pgprobe/*.cjs` and `logprobe/probe.ts`.
- **Hooks.**
  - The no-cd hook refused one inline `git -C $Q/... checkout`. I moved it into a script file; nothing was bypassed.
  - The zsh `=` hook refused a separator.
- **PostgreSQL.**
  - The first start failed: the unix socket path exceeded 103 bytes. I restarted on loopback TCP with no socket.
  - The first provision failed 13 migrations on their tail `INSERT INTO _secuura_migrations`, because there was no tracker table. I dropped the databases, created the tracker first, and re-provisioned: 53/53.
  - The server was stopped at the end (`pg_ctl stop` rc 0).
- **Writes.** None under !CODING, no GitHub or Linear writes, no `rm`, and no stderr sent to /dev/null by me.

## NOT tested

- **The PR bodies on GitHub** (including their Test Evidence sections, if they differ from the commit messages). The reason: no Secuura gh auth on this host, and I would not use the global account.
- **Linear** (KS-1377, KS-1617, KS-1507, KS-1641 ticket text).
- **Any suite of any service the PRs do not touch.** Originate and anchoring were not run: the develop move is theirs, and no PR in this batch touches them.
- **Behind the gateway:** a live sign-in against real Google or Microsoft. The 400 chain was read in source and in the existing harness, not driven end to end. Whether the api-gateway alters a 400 body from auth was **not checked**.
- **R's preflight legs and overlap census across the 24 open PRs.** I checked overlap only against #1597 and #1568.

MODEL: claude-opus-5-5
WALL-CLOCK: 24 minutes (13:33 -> ~13:58 AEDT)
sha256: 05725c3a4f4cae1ca40a57e409278c68ab5a3a2c6dcffa7b144e5e07c38bb1c0 (this file with this last line deleted) | sha256-without-line-1: a40294f324059d5c345a02cafc61a524f6d91b9804b6cf46e208b901de8f013f (this file with its first line and this last line deleted)
