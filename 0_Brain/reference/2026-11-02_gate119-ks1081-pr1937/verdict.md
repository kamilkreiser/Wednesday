# QA Gate 119 verdict (TIER 2 proposed): Secuura/Distributed_Secuura PR 1937 (KS-1081, env.example declares the five compose keys)

## BLUF
**GATE 119 on PR 1937 at 57e0237b2539: GO WITH NOTES, TIER 2 HOLDS. Nothing has to be fixed before merge.**
Five keys are added to `Blockchain/Dev/env.example`, all with an EMPTY value (no placeholder, no credential-shaped text). Bootstrapping a `.env` from the template at head adds exactly those five names and nothing else. The decisive measurement: `docker compose config` renders a byte-identical container environment for all five keys, base vs head, because `docker-compose.yml` already maps an unset host variable to the empty string with `${KEY:-}`. The empty line therefore changes what the auth service receives by nothing. The author's `||` claim is true (userRepo.ts:1371) and the `?? null` warning is recorded in the compose comment (:812-815); but that single `||` is pre-existing, is not exercised by the PR, and no existing test pins it (mutant survives, F1). Tier 2 stands; the pinning test is RECOMMENDED, not FIX-BEFORE-MERGE.
Not measured on Node 24 (host Node v26.8.1). bash is the macOS bash.

## 1. Heads + diffstat (logs/head_start.log, final.log, final2.log)
- PR head `57e0237b2539a13ebabb9fd60c256ca638068e2c` at START and END: identical. Merge-base `8f313815f415`. 1 commit. Three-dot numstat: 4 files, **+102/-0** as claimed (env.example 12/0, new suite 55/0, cheat fragment 18/0, flow fragment 17/0). Nothing outside the declared paths.
- Develop moved twice: the brief said `c70f339063ee`; at the END it is `777643aa6e1a`. Between those two: 6 files changed, 0 of them env.example, docker-compose, bootstrap-env, userRepo, timestamping. Between base and c70f339: 0 of those paths changed (author's claim holds).
- PR body not read (no Secuura gh auth here); the author's READY mail copied into evidence/.

## 2. The hunks / Q1: which keys, which template, which values
Only `Blockchain/Dev/env.example` (the canonical template per bootstrap-env.sh :26-32). Appended after `EMITTER_SIGNING_SECRET=`, a 4-line comment block and:
| key | value at head | compose line (`${KEY:-}`) |
|---|---|---|
| ADMIN_USER_PASSWORD | empty | docker-compose.yml :821 (auth) |
| ENABLE_DEMO_SEED | empty | :626 (originate) |
| ALLOW_DEFAULT_SEED_PASSWORDS | empty | :633 (originate), :791 (auth) |
| TSA_URL | empty | :1255 (timestamping) |
| TSA_AUTH_KEY | empty | :1256 (timestamping) |
Every line is `KEY=` exactly; no placeholder text. The legacy `Blockchain/Dev/.env.example` is untouched and keeps `ENABLE_DEMO_SEED=false`, `ALLOW_DEFAULT_SEED_PASSWORDS=false`, `ADMIN_USER_PASSWORD=` (:104,:109,:133), `TSA_URL=`/`TSA_AUTH_KEY=` (:162-163): the two templates now agree on empty-vs-false only in effect (see F4).

## 3. The behaviour question for config templates: empty vs UNSET, per key (read at the head tree; the four dev-moved files are unchanged since base)
- **ADMIN_USER_PASSWORD.** userRepo.ts:1371 `const requiredSeedPw = (envVar) => process.env[envVar] || null;` and :1407 `password: requiredSeedPw('ADMIN_USER_PASSWORD')`: empty and unset both give null, so the account takes the `account.password === null` branch (:1670). docker-compose.yml :812-815 reads as the author quotes (`'' is falsy ... if that read is ever changed to ?? null, an empty string would become a seeded blank password on the cross-tenant SYSTEM_ADMIN`): VERIFIED, both lines. Other readers: auth-matrix-smoke.sh:41 `${ADMIN_USER_PASSWORD:?...}` (colon form: fails on empty AND unset, identical); systemTest runner.js and tokenisation spec use `|| ''`; personaLogin/loginOutcome helpers only name the variable in messages. No `??`, no `in process.env`, no `-v` reader anywhere in the tree.
- **ENABLE_DEMO_SEED.** userRepo.ts:1336 `!== 'true'`; demoSeedGate.ts :41/:68 `env[flag] === 'true'`; originate adminConfig.ts:2047 `=== 'true'`; api-gateway admin.ts:594 `=== 'true'`. Empty == unset == 'false'.
- **ALLOW_DEFAULT_SEED_PASSWORDS.** userRepo.ts:1332 `!== 'true'`; demoSeedGate; adminConfig.ts:2046 `=== 'true'`. Same.
- **TSA_URL.** timestamping index.ts:179, :476, :852 and qualified-tsa.ts:272 all `process.env.TSA_URL || provider.url`. Empty == unset == code default (the compose comment :1253 says so). docker-compose.production.yml:172 `TSA_URL=${TSA_URL}` (no default): unset renders empty with a compose warning, empty-set renders empty with none; same value.
- **TSA_AUTH_KEY.** qualified-tsa.ts:273-274 `authKey ? 'Bearer '+authKey : undefined`: falsy-safe, empty == unset.
- Connector test helper `describeIfEnvPresent` (tests/connectors/_helpers.ts:15) uses `!process.env[k]`: empty == absent.

### Paths that could turn the new empty line into something different (all checked)
1. **bootstrap-env.sh** (scripts/run/diff, logs/bootstrap_diff.log): ran the real script into scratch dirs at base and head (template from each ref, no slot, openssl keys random, values never printed). Produced `.env` key sets: base 105, head 110; diff = exactly ADMIN_USER_PASSWORD, ALLOW_DEFAULT_SEED_PASSWORDS, ENABLE_DEMO_SEED, TSA_AUTH_KEY, TSA_URL, and nothing else. All five EMPTY at head, ABSENT at base. The script's `fill_if_blank`/`fill_default` calls cover only PII keys, DEMO_SERVICE_*, GATEWAY_VOUCH_SECRET, JWT, passwords/URLs for pg/redis: none of the five is auto-filled.
2. **Compose interpolation** (logs/compose_*.json, scripts/compose_config.sh): `docker compose config` of the head compose with the base `.env` and with the head `.env`: auth ADMIN_USER_PASSWORD, auth+originate ALLOW_DEFAULT_SEED_PASSWORDS, originate ENABLE_DEMO_SEED, timestamping TSA_URL and TSA_AUTH_KEY are EMPTY in both; "identical service env for the five keys: True". So the container sees `""` today (unset, `:-` default) and `""` after. No blank-credential, no weaker default, no different seeded row.
3. **env_file**: the only env_file entries are `.env.local` (compose lines 421, 739, 872, 1423); `.env` is used for interpolation only, so no bare pass-through of an empty variable exists. A value in `.env.local` still wins by the pre-existing rule (the compose comment :789).
4. **Another reader**: none of the above; the integration override compose in systemTest uses `${KEY:-}` too.
5. **Existing `.env`**: bootstrap leaves an existing `.env` untouched; the keys reach only a freshly created one.

### Empty-string actually run through the real seeder (logs/empty_vs_unset3.log; head2 worktree of the PR head, deps installed in my workdir, shared package built)
The existing ks949 suite (31 cells) drives the real `seedDemoUsers` with a mocked DB. I made a copy with `ADMIN_USER_PASSWORD: undefined` replaced by `''` at all 9 sites:
| run | result |
|---|---|
| A. original (undefined), head | 28 pass, 3 fail: first cell timed out on cold start (10.9 s), 2 filesystem-walk cells timed out at the 5 s default (host is slow; the same two time out in every run below) |
| B. variant (`''`), head | 29 pass, same 2 walk timeouts: **every behavioural cell is identical to unset** |
| C. mutant `?? null`, original undefined-driven suite | 29 pass: **mutant SURVIVES** (undefined ?? null is null) |
| D. mutant `?? null`, `''` variant | 6 behavioural cells red (admin reported, hints, id/email-row remediation): the suite would catch it only if driven with `''` |
userRepo.ts sha256-restored after the mutant (RESTORE_OK). So empty == unset at head is MEASURED; and the `||` is unpinned by any test in the repo (F1).

## 4. Q4: do the repo's comments disagree? (read the code; pre-existing, INFO)
Both are true, for different databases. The seed loop (userRepo.ts :1649-1747): when the password is null it first calls getUserById and getUserByEmail. If NEITHER row exists it logs "seeding skipped ... no pre-existing row" and `continue`s: no row is created. If a row exists under that id or that address it is REWRITTEN in place with the sentinel `!disabled:no-seed-password-supplied` and `status='suspended'` (:1715-1722, :1740-1743), then skipped. Hence userRepo.ts :1367-1368 and :1404-1405 ("SKIPS the account", "not seeded") describe a fresh database; docker-compose.yml :799-801 ("written with an unusable password hash and status = 'suspended'") describes an already-seeded one. Neither is wrong, each is incomplete, and the new env.example comment "empty means the account is not seeded" repeats the fresh-database half (F5). Empty and unset take the same branch.

## 5. Re-measure (logs/redfirst_mutants.log, suites_*/summary.txt, final*.log)
- **Red-first**: the author's suite run against the BASE env.example and compose: 2 passed, 5 failed (each `want "1", got "0"`, by assertion). Head: 7 passed, 0 failed, rc 0. Matches the author's 5/7 and 7/7.
- **Remove-one-line mutants** (head env.example, sha256 restored, restore OK x5): removing each of the five lines turns exactly its own cell red (6 passed, 1 failed each, named cell). Extra mutants, all killed by a cell: `TSA_URL=x`; `ADMIN_USER_PASSWORD` commented out; `ADMIN_USER_PASSWORD=` made non-empty; the compose `${TSA_AUTH_KEY:-}` default dropped. The suite does pin "empty", not just "present". Survivors: none.
- **88 existing suites** (every `scripts/__tests__/*.test.sh`, run once at a base worktree and once at a head worktree, same host): 88 at base, 89 at head (the new one); the result line of each of the 88 is **identical** (diff of the two summaries is only the added line). Three suites exit non-zero **identically at base and head**, so not caused by the PR, and they differ from the author's "all exit 0" because of MY environment: `docs_fragments` (80/81; the one failure is B7 "a tree that is not a git checkout is refused", which depends on the scratch dir having no .git ancestor, and mine sits inside the WEDNESDAY repo), `no_tracked_credentials_root` (12/16; four cells whose precondition is "no .git at any ancestor"), `blockchain_testing_target_base_follows_the_slot` (rc 2: "tsx not installed", no node_modules). The docs_fragments cells that lint the two new fragments are among the 80 that pass; the planted-defect step was not repeated.
- `bash -n` on the new suite: rc 0. shellcheck not run.
- **merge-tree** onto develop `777643aa6e1a` (fetched at the end): rc 0, clean; result changes exactly the PR's 4 paths (SAME_PATHS). Also clean onto `c70f339063ee` earlier (logs/final.log).

## 6. TIER (Q3)
**Tier 2 holds.** None of the five keys reaches identity/admin seeding with a behaviour difference: the container environment is identical before and after (section 3.2), and the template is only copied on a fresh `.env`. ADMIN_USER_PASSWORD does reach the cross-tenant SYSTEM_ADMIN seed, and its safety does rest on one `||` with no test that drives an empty string (F1). I do NOT raise to tier 1 for that, because the PR neither introduces nor relies on a new path: compose has delivered `""` to that read for every stack with the variable unset since KS-971; the PR's line makes `.env` say `KEY=` where it said nothing. The pinning test is RECOMMENDED as a follow-up (best placed in the ks949 suite as `ADMIN_USER_PASSWORD: ''`, 6 cells go red under `?? null`), not a merge condition. If Kam rules the seed identity itself tier 1 regardless of delta, F1 is the only item that would change.

## 7. Kam's ks1346 logging rule
No new log line, no thrown-object logging. N/A.

## 8. FINDINGS
- **G119-F1 (RECOMMENDED, follow-up, measured).** Nothing in the repo drives `ADMIN_USER_PASSWORD=''` through `requiredSeedPw`; ks949's `runSeed` only passes `undefined`. Mutant `process.env[envVar] ?? null` survives the whole 31-cell suite and turns 6 cells red only when driven with `''`. Fix (follow-up PR, auth service): in ks949-platform-admin-seed-identity.test.ts add one cell family with `ADMIN_USER_PASSWORD: ''` expecting the same skip/suspend/hint behaviour as `undefined` (and the same for `DEMO_SECUURA_PASSWORD`). Not FIX-BEFORE-MERGE: the PR does not change the container env.
- **G119-F2 (INFO, measured).** Compose already renders all five keys as `""` when unset; `docker compose config` base vs head: identical. This is why the empty template lines are behaviour-neutral. Note for the PR body: the "read in code, not run on a stack" caveat can now say "rendered by docker compose config, identical".
- **G119-F3 (INFO).** Existing guard `KS-966 F1` (ks949 test :505-575) walks files matching `name === '.env.example' || endsWith('.env.example')`. The canonical `env.example` (no leading dot) does NOT match `endsWith('.env.example')`, so a future non-empty `ADMIN_USER_PASSWORD=` in the template this PR edits would not be seen by it. The new shell suite catches it (mutant `ADMIN=nonempty` red), so there is cover, but the older guard has a naming gap (pre-existing since the canonical-template change). Suggest widening the walk to `env.example` in the same follow-up as F1.
- **G119-F4 (INFO).** Two templates now carry the same keys with different literals (`.env.example`: `ENABLE_DEMO_SEED=false`, `ALLOW_DEFAULT_SEED_PASSWORDS=false`; `env.example`: empty). Behaviour-identical (every reader compares to `'true'`), but it is exactly the divergence the open KS-1081 ruling (one-line pointer file, a never-diverge guard) is for; the author states it stays open.
- **G119-F5 (INFO, pre-existing comments, asked in Q4).** The repo's comments disagree only because each describes one database state: fresh database = no row created; already-seeded database = the existing row rewritten with the sentinel hash and set suspended. The new template comment "empty means the account is not seeded" is the fresh-database half only; suggest "...is not seeded (an already-seeded row is suspended)" when next touched. The PR itself changes neither.
- **G119-F6 (INFO).** Template comment says `ENABLE_DEMO_SEED`/`ALLOW_DEFAULT_SEED_PASSWORDS` are "read by the seeder in originate"; they are also read by auth (userRepo.ts:1332/1336, ALLOW forwarded by compose :791) and api-gateway (admin.ts:594). Wording only.
- **G119-F7 (INFO).** Develop moved c70f339063ee -> 777643aa6e1a during the gate; 0 overlap with the PR's paths, merge-tree clean.
- **No FIX-BEFORE-MERGE item.**

## 9. NOT TESTED
- The live PR body, Linear, CI, the author's pre-push hook (13 of 16 legs), Node 24, GNU/Linux bash, shellcheck.
- A real boot of any container; the compose result is the rendered config, not a running service. The seeder was run with a mocked DB, not PostgreSQL.
- The two ks949 filesystem-walk cells and the three host-dependent suites listed in section 5 (environmental, identical at base and head); the docs-fragment planted-defect check.
- docker-compose.production.yml render, the Azure bicep/deploy paths, and any deployed environment's existing `.env` (bootstrap does not touch an existing `.env`; not run against a real one).
- Whether any external tooling parses env.example key counts (the "102 distinct vars" figure in bootstrap-env.sh's comment is now stale by +5; not checked elsewhere).

ADDENDUM 2026-11-02 (post-verdict): the stray background run `scripts/one.sh` (vitest ks949 started without `--root`, so it scanned from the WEDNESDAY root and picked up other copies of the test) was superseded by the `--root` runs in logs/empty_vs_unset3.log, which carry every figure cited above. It was stopped by PID (24454, 24474, 24802 and its esbuild child 62960); no gate119 processes remain. No finding changes.
