## QA GATE 64, TIER 1, ROUND 1: KS-1860 #1876 (PR 3 of 4)

**BLUF: GO WITH NOTES.** With `MULTI_TENANCY_ENABLED` on, originate's existing `extractTenantContext` check now answers 403 to a request made as a suspended or an archived tenant. The two are treated identically, apart from the word in the message. With the flag off nothing changes. `getPool` is unchanged: I captured a 55-cell snapshot covering every status, per-tenant DB off and on, fresh and cached pools, a failed refresh and a failed boot refresh. It is **byte-identical** at base and at the head (same sha256). The status route admits exactly the four ruled moves. Every other pair answers 409 with no write and no audit row, an unknown id answers 404, and on real Postgres 15 no race got a refused move through. I wrote 21 mutants of my own and all 21 were killed. The merge onto develop `32e8fe25` is clean, the regenerated YAML is exactly what the generator produces, and tsc is clean for both packages. Nothing blocks the merge. There are three minor notes:
1. The status map **fails open at boot** and stays **stale for as long as the platform database is unreachable**. Nothing says this; the fragments promise "within one 60-second refresh".
2. The Schemathesis KS-1042 isolation fixture will hit a precondition failure, permanently, on any slot where an isolation tenant is archived.
3. P5 pins `getPool` only with per-tenant DB off. A variant of SM4 gets past all 16 PR cells.

- PR https://github.com/Secuura/Distributed_Secuura/pull/1876 · ticket KS-1860 · author Seat S 9th · commissioned by Wednesday, Sun 1 Nov 2026 · ruling card `secuura-ks1860-suspended-tenant-enforcement-1031` (a)
- **Head at START** (2026-10-31T17:19:36Z, `git ls-remote`): `refs/pull/1876/head` = `33bce392e924bcf1985a2a91a7ea0b6fd0412cb8`, develop = `32e8fe25cb24e8357605a693b01050e51c3d4007` (`evidence/lsremote_start.txt`)
- **Head at END**: (2026-10-31T17:45:42Z) `refs/pull/1876/head` = `33bce392e924bcf1985a2a91a7ea0b6fd0412cb8`, which is **unchanged**. develop **moved** to `b331ffb8e9ca809d9821e5f92595721ce9db4f50`: one commit, "KS-1887: refresh the two pages from fragments (#1877)", 2 files, neither of them the PR's (`evidence/lsremote_end.txt`, `develop_moved_end_*.txt`). Re-merged: `merge-tree --write-tree b331ffb8 33bce392` gave rc 0 and tree `eeba679f…`, clean (`evidence/merge_tree_end.txt`).
- Clone: `0_Brain/reference/2026-11-01_gate64-ks1860-1876/repo`. `rev-parse --show-toplevel` equalled the clone directory before any fetch. The clone was left at the head with a clean working tree (`git status --porcelain` empty after the base swaps, the mutants, the openapi plant and the probes were restored or removed).
- Host: Apple Silicon Mac, **Node v26.8.1. This is not an LTS run.** Node 24 LTS: UNMEASURED.

## VERDICT: GO WITH NOTES

## Findings

**G64-F1 · minor (docs accuracy plus a design point for Kam; reword before merge if cheap).** The status map **fails open at boot**, and it **keeps its last reading indefinitely** while the platform database is down. `refreshConfigs` catches every error (`tenant-pool-manager.ts:333-335`). `init()` awaits it once, then sets a fixed 60 000 ms `setInterval` (`:186-190`, `DEFAULT_REFRESH_INTERVAL` `:69`, which no option can change). Measured with a pg fake that fails (`scripts/gate64-probe.test.ts`, all green at the head):
- **F1**: if the first refresh fails, a suspended tenant and an archived tenant are both **served**.
- **F5**: after a failed boot refresh, they are served until the next refresh that succeeds.
- **F2**: a tenant suspended after the last refresh is served until the next refresh.
- **F3**: if every later refresh fails, it is served on every request, indefinitely.
- **F4**: the mirror case is last-known-status. A tenant reactivated while refreshes are failing stays **refused**, but every other tenant is unaffected, so it is not fail-closed for everyone.
- **F6**: the timer fires at exactly 60 000 ms and not at 59 999.

This is not a regression, because base never refused anyone. But the cheat fragment says "within one 60-second refresh of the status change" with no condition, and the flow fragment says "takes effect within one refresh". Both are true only while the platform database is reachable, and only per originate process. Reword to "within one successful refresh (60 s), per process; if the platform database is unreachable at start-up or afterwards, the last statuses read stay in force, and none are enforced until a first refresh succeeds". Whether the boot fail-open is acceptable is Kam's call. It is the same posture as before this change.

**G64-F2 · minor (platform suites; fix in `systemTest` before the next Schemathesis run on a slot that has one).** `systemTest/schemathesis/tests/isolation_tenant_fixtures.py:36-43`: `_ensure_tenant` re-activates any isolation tenant whose status is not `active` (`needs_reactivation`, `support/isolation_tenants.py:57`) with `PATCH …/status {"status":"active"}`, and `pytest.fail`s on anything but 200. The comment there says "A sweep can suspend or archive any tenant". At the head, `archived -> active` answers 409 (PR cell R1, my TP matrix). Slugs are unique and `archived` is now terminal through the API. So a slot whose isolation tenant A or B was ever archived (develop let a sweep do `active -> archived` in one call) will fail every run with "KS-1042 precondition: could not re-activate" until someone deletes the row. A sweep can still archive one through `suspended -> archived`. The PR lists the four platform suites as UNMEASURED and does not mention this caller. Found by code reading only; not run live.

**G64-F3 · minor (test strength, follow-up).** P5 runs only with `perTenantDbEnabled: false`, where an active config and an absent config both give the default pool. My **G64-M5** loads suspended and archived rows into the pool map *as active*, so `getPool` would hand them their own per-tenant pool instead of the fallback. It **passed all 16 PR cells** and was killed only by the gate's G1 snapshot, in the per-tenant-DB-on cells. **G64-M9** makes the refresh interval 600 s; it also passed all 16 PR cells and was killed only by gate cell F6. S's SM4 (the `continue` removed) **is** killed by P5, through `getPool` throwing "is suspended — access denied" (`evidence/mut_G64-M4_pr.log`). P5 asserts the right thing (the base fallback), but in one mode only. Fix: run P5/P6 with per-tenant DB on as well, and pin the interval with fake timers.

**G64-F4 · file-only (docs, presumably PR 4 of 4).** `docs/MULTI-TENANCY.md:202-207` still says suspended and archived are "Known deviation (KS-1860)… nothing refuses the tenant's requests" and that the status route "enforces no order". `:461` says "nothing enforces it". All three are stale as soon as this merges. The PR does not touch the file. Confirm that PR 4 carries it.

**G64-F5 · file-only (`PROVISION_PER_TENANT_DB`, existing behaviour, unchanged).** My snapshot (`evidence/getpool_snapshot_{base,head}.json`, identical) shows what happens with per-tenant DB **on**:
- A suspended or archived tenant with no cached pool gets the **default** pool. That is the shared database, not its own, so "public verification of that tenant's documents still works" (cheat fragment) holds only in the single-DB configuration (every configuration file today, per MULTI-TENANCY.md).
- A tenant that had a pool cached *before* it was suspended keeps getting **its own** pool afterwards (`tenantPools` is checked before `tenantConfigs`, `:209-214`) until it is evicted.
- After a failed boot refresh, even an active per-tenant-DB tenant gets the default pool.

None of this changes in this PR. I could not read the PR body (UNMEASURED), so I cannot say whether its stated per-tenant-pool caching limit matches these three facts. The facts above are measured.

**G64-F6 · file-only (cosmetic race).** The 409 message comes from a second statement (`SELECT status`, `index.ts:453-458`). Under a race it can name a status the tenant has already left, for example "Cannot change tenant status from suspended to archived", which is itself an allowed move. The write is atomic (Q4). A 404 can only follow a row deleted between the two statements, and 404 is then true.

**G64-F7 · file-only (for Kam).** There is no platform-admin exemption. A super-admin's `X-Tenant-Override` to a suspended tenant gets originate's 403 on **every** originate route, because the middleware is app-wide (`originate/src/index.ts:226-240`). That includes the admin portal's document views for that tenant. The flow fragment states this openly.

**G64-F8 · file-only (scope).** The transition order in tenant-provisioning is unconditional: it applies whatever `MULTI_TENANCY_ENABLED` says. Only the 403 enforcement depends on the flag. This matches the ruling's wording ("Works only where MULTI_TENANCY_ENABLED is on" is about the 403). Stated here so nobody reads the flag as gating the 409s.

## Q1. Enforcement through tenant-context; archived == suspended; flag off
**FOUND: yes.** `getTenantStatus` now reads `tenantStatuses`, which `refreshConfigs` fills from every row of `tenants` (the `WHERE t.status IN ('active','provisioning')` is gone, `:302-317`). `extractTenantContext` (`tenant-context.ts:79-88`, unchanged) answers `403 {error:'Tenant access denied', message:'Tenant is <status>'}` and returns before `getPool`/`next()`. `getTenantStatus` has exactly one non-test caller, `tenant-context.ts:80` (git grep). The middleware is mounted app-wide in originate only when `MULTI_TENANCY_ENABLED === 'true'` (`originate/src/index.ts:226`), ahead of the public routers. The gateway sets `x-tenant-id` only from a verified JWT or API key, or from a super-admin override (`api-gateway/src/middleware/auth.ts:503`, `:592-598`). So an anonymous public verifier carries no suspended tenant's id, and a verifier from an active tenant reading a suspended tenant's document passes the check and reaches `getPool(home tenant)` unchanged.
**Archived == suspended:** same branch, same status code, same body except the word; per-tenant DB off and on (gate F8, PR C1/C2). The default tenant stays exempt (C6).
**Off:** the manager's `init()` never queries (F7: 0 platform queries), the map stays empty, and originate does not even mount the middleware. Suspended and archived tenants are served exactly as at base (C5, F7). Mutant M10 (the `isEnabled()` guard dropped) was killed by C5.
**TESTED:** PR shared file 16/16 at the head, 6 red at base product code (P1, P2, P7, P9, C1, C2), exactly S's six. Mutants M1 (map not consulted), M2 (archived dropped from the refused set), M3 (status recorded after the filter): killed.

## Q2. `getPool` unchanged
**FOUND: byte-for-byte unchanged.** `getPool` (`:203-266`) reads `tenantPools` and `tenantConfigs`, never `tenantStatuses`. `tenantConfigs` gets exactly the same rows as at base: the `continue` at `:317` admits exactly `'active'`/`'provisioning'`, the same set as the dropped SQL `IN`, and NULL is excluded both ways. The values and the insertion order are the same. All 23 non-test `getPool` call sites (originate verification.ts:281/:571, verificationV2.ts:354, documents.ts:1122, adminConfig.ts:2214, tenant-context.ts:93, and 17 `db.ts` helpers) therefore see the same result. The PR touches none of them.
**TESTED:** gate G1 is a 55-cell snapshot, run on base product code and on the head. **sha256 `978159bb…e5ee` for both, `cmp` rc 0.** S's SM4 equivalent (my M4, the `continue` removed) is killed by P5, because `getPool` throws "is suspended — access denied". P5 asserts the right thing, the base fallback to the default pool, but only with per-tenant DB off (G64-F3, M5).

## Q3. Status-map refresh failure / staleness
**FOUND: last-known-status, fail-open at boot.** Details and measurements are in G64-F1. The maximum staleness while the database is reachable is about 60 s plus query time, per originate process. While it is unreachable there is no bound. Mutants M6 (failure clears the map), M7 (failure turns every status active), M8 (map never cleared, so removed tenants linger) and M9 (interval ×10) were all killed, M9 by the gate probe only.

## Q4. Transitions
**FOUND: exactly the ruled table.** `STATUS_REACHABLE_FROM` (`index.ts:437-441`): active ← {provisioning, suspended}, suspended ← {active}, archived ← {suspended}. The target is validated first against the three values (`:445-448`), so the lookup is always defined. The schema allows exactly the four statuses (`docker/init-platform/01-platform-schema.sql:24`).
**TESTED:**
- Gate TP matrix: all **12** from×to pairs through the real entry module, with a statement log. Allowed pairs: 200, statements exactly `[UPDATE_GUARDED, INSERT]`, the row changed. Refused pairs: 409 with the exact body, statements exactly `[UPDATE_GUARDED, SELECT]`, **no INSERT**, the row unchanged. Each cell also checks that the guarded UPDATE carried the right from-list.
- Unknown id: 404, `[UPDATE_GUARDED, SELECT]`.
- Seven invalid targets (`provisioning`, `["active"]`, null, `''`, `Active`, `__proto__`, `constructor`): 400 with **zero** statements.
- The PR's cells cover the same 12 pairs (A1-A4, R1-R8) plus N1-N3. 18/18 at the head, 11 red at base, exactly S's eleven.
- **Race, on real Postgres 15** (`scripts/race.sh`, `evidence/race.log`, `postgres:15-alpine` with `--network none`, removed by recorded ID). T1 holds the row lock inside a transaction; T2 runs the PR's exact statement in autocommit:
  - suspended→archived vs suspended→active: T2 `UPDATE 0`, final archived. **archived→active did not slip through.**
  - Two concurrent active→suspended: T2 `UPDATE 0`.
  - suspended→active vs suspended→archived: T2 `UPDATE 0`, final active.
  - active→suspended vs →active: T2 `UPDATE 0`.
  - **Control:** the check-then-write shape (read, decide in the app, then an unconditional UPDATE) ended `active` after an archive. The single statement is what prevents that.
- Mutants M11-M21 (two disallowed moves admitted, same-status admitted, reactivation removed, WHERE dropped, audit on refusal, 404/409 swapped, unknown→409, wrong message, refusal answers 200, wrong param slot): all killed.

## Q5. Own mutants (`scripts/mutants.py`, `evidence/own_mutants.json`)
Each mutant is a unique-anchor replacement (anchor count asserted == 1), run against the PR file and then the gate probe, restored, and **sha256 asserted equal**. All 21 restorations passed. Controls: shared 26/26, tp 39/39.

| # | Mutant | PR cells red | Gate probe red | Result |
|---|---|---|---|---|
| M1 | getTenantStatus reads the pool map again (status map not consulted) | 6 | 5 | killed |
| M2 | archived dropped from the refused set | 1 | 1 | killed |
| M3 | status recorded after the active/provisioning filter | 6 | 5 | killed |
| M4 | rows into the pool map (SM4) | 1 (P5) | 2 | killed |
| M5 | rows into the pool map as active | **0** | 1 (G1) | killed, **gate only** |
| M6 | refresh failure clears the status map | 1 | 1 | killed |
| M7 | refresh failure treated as active | 1 | 1 | killed |
| M8 | status map never cleared | 1 | 0 | killed |
| M9 | refresh interval 600 s | **0** | 1 (F6) | killed, **gate only** |
| M10 | isEnabled() guard dropped | 1 | 0 | killed |
| M11 | active→archived admitted | 1 | 5 | killed |
| M12 | archived→active admitted | 1 | 4 | killed |
| M13 | suspended→suspended admitted | 1 | 4 | killed |
| M14 | suspended→active refused | 1 | 4 | killed |
| M15 | conditional WHERE dropped | 8 | 14 | killed |
| M16 | audit row written on refusal | 15 | 13 | killed |
| M17 | 404/409 swapped | 11 | 9 | killed |
| M18 | unknown id answers 409 | 3 | 1 | killed |
| M19 | 409 names the requested status twice | 5 | 5 | killed |
| M20 | refusal answers 200 (silent no-op) | 8 | 8 | killed |
| M21 | from-list replaced by [target] | 7 | 13 | killed |

**21/21 killed. 19/21 are killed by the PR's own cells.** I did not re-run S's 19 mutants; S's claim is UNVERIFIED as stated.

## Q6. Scope / merge / spec / tsc
- **Scope:** exactly the 8 files named (`evidence/pr_files.txt`), +506/-11, one commit on `c63d3dc6`.
- **Merge:** `git merge-tree --write-tree 32e8fe25 33bce392`: rc 0, tree `e6edc0a0…`, clean. Develop moved 8 commits and 30 files since `c63d3dc6`. **0 of the PR's 8 paths** are among them (control: the same `grep -x -F -f` matches a known moved file, 1). Develop did touch `api-gateway/src/routes/platform.ts`, but only the KS-1410 templates/clone 500 bodies. The status forwarder (`:395-411`) is identical, and it forwards the upstream status and body (`res.status(r.status).json(data)`).
- **Spec:** `npm run check:openapi`: rc 0, "CHECK PASS: on-disk YAML matches generated", spec examples OK. **Control:** a planted description change made `--check` exit rc 1 with "CHECK FAIL"; the file was restored and its sha256 checked. Both YAML hunks fall under `/api/platform/tenants/{id}/status` (path key at line 36436, no other path key before the second hunk): the description, the 404 wording, and the new 409. Nothing else changed.
- **tsc --noEmit:** packages/shared rc 0, tenant-provisioning rc 0. **eslint** on `tenant-pool-manager.ts` plus its test: rc 0, but there was no planted-error control and I did not confirm which config resolved, so treat it as weak.
- `docs-fragments.mjs check`: OK, lint clean, 19 new entries per page.
- **Whole suites at the head:** tenant-provisioning **9 files, 72/72** (S: 72/72). packages/shared **57 files, 1095/1097** (`evidence/vitest_shared_full_cwd.log`; S: 1093/1097). The two reds, each run alone: `threadToken` "different policy IDs" passed alone, 15/15 (a 30 s timeout at load1 about 13-17). `wallet-signature` "accepts a valid wallet signature" **fails alone too** (`expected false to be true`, the KS-1727 cell S names). It imports only `../cardano/wallet`, which is outside the PR's diff. I did not run it at base. A first run with cwd = the WEDNESDAY folder broke 7 repo-wide guard files at collection ("could not locate the Dev root"). That was a harness artefact, fixed by running with cwd = the package (`evidence/vitest_shared_full.log` kept). originate (jest, against the head's `@secuura/shared` dist) **154 suites, 1871/1871**, rc 0 (`evidence/jest_originate_full.log`; S: 1871/1871). Not re-run on the merged tree: develop changed nothing under `packages/shared/src/db`, `tenant-provisioning`, originate's index or the gateway forwarder (the `32e8fe25` diff shows only the KS-1410 bodies in `platform.ts`).
- **Per-tenant-pool caching limit:** see G64-F5. The PR body is unread.

## Q7. Node
Everything ran on **Node v26.8.1** (not LTS). Node 24 LTS: **UNMEASURED.**

## COUNTS
- Findings: 0 blocker · 0 major · 3 minor (F1 fail-open/stale wording, F2 Schemathesis fixture, F3 P5 one-mode) · 5 file-only (F4-F8)
- PR cells: 34/34 at the head. Base product code: 6/16 and 11/18 red (17 total), exactly as claimed
- Gate cells: 10 shared probe (G1 + F1-F9) and 21 tp probe (12 matrix + TP-U + 7 TP-V + TP-C), all green at the head. At base: 5 shared and 13 tp red, as expected
- getPool snapshot: 55 cells, base == head (sha256 equal)
- Real-PG race: 4 scenarios plus 1 control
- Own mutants: 21, killed 21 (19 by the PR's cells)
- Whole suites: tenant-provisioning 72/72, shared 1095/1097 (2 explained above), originate 1871/1871

## SPARK SHADOW AND CALIBRATION
- `spark_gate.sh` (non-pytest mode, the two ks1860 files, `--node-modules` = the clone's root `node_modules`, `--work` = `…/scratchpad/gate64_spark`, base `develop`, `--out` = `evidence/spark/facts`): **rc 0 in 31 s**. It reported head 34/0, base product 17/17, diff 8 files +506/-11, merge-base `c63d3dc6`, base tip `32e8fe25`. All five match my figures.
- `spark_review.py` (`--ticket KS-1860`, `--pr-body-file evidence/commit_message.txt`, because the PR body could not be read): rc 0, one attempt, 112.7 s, valid schema, 46.3K prompt tokens. **Spark verdict: NO GO**: 6 Major, 4 Minor, 1 Note (`evidence/spark/review/review.json`). Only 2 of the 11 findings carry `evidence_quote_found_in_input: true`.

| # | Spark finding | Sev (Spark) | Mine | Call |
|---|---|---|---|---|
| 1 | The gateway may not forward the 409/404 | Major | `platform.ts:406-407` forwards status and body unchanged, at the head and on develop | **False positive** |
| 2 | auth/gateway/security still have no suspension check | Major | True as a fact, but it is the ruled scope ("Fix the existing check… one shared file plus the status handler"), stated in both fragments | **Not a defect** (out of ruled scope) |
| 3 | The shared fake only models the old WHERE, so the real query is untested | Major | The fake accepts the no-WHERE query (`if (rest !== '')`, test line 66). At base the WHERE is applied. M3/M4/M8 killed | **False positive** |
| 4 | The follow-up SELECT makes the "one conditional UPDATE" claim false | Major | The write is one statement, and race-safe on real PG (Q4). Only the message can be stale | **Partial**, Note-level (= G64-F6) |
| 5 | provisioning→active is dead because create sets active | Major | It is in the ruled table. Create sets provisioning then active in sequence (`index.ts:240`, `:307`) | **False positive** |
| 6 | The spec's 409 is unverified at the gateway | Major | Same as #1. check:openapi passes with a control | **False positive** |
| 7 | P9 does not show that a later successful refresh clears stale entries | Minor | P8 and gate F5 cover exactly that | **False positive** |
| 8 | getTenantStatus semantics changed | Minor | One caller only (tenant-context:80) | **Note** |
| 9 | "Portal discards the answer" unverified | Minor | `frontend/admin/src/services/api.ts:1062-1067` returns `res.ok` only, so the claim is true | **False positive** |
| 10 | Whole-suite figures imply full coverage | Minor | The fragments mark the platform suites UNMEASURED | **Disagree** |
| 11 | The interval is "configurable via options" | Note | It is a constant; no option exists (`:69`, `:189`) | **False positive** (the interval point itself is real: G64-F3/M9) |
| — | — | — | G64-F1 fail-open at boot / stale indefinitely (measured) | Spark missed |
| — | — | — | G64-F2 Schemathesis fixture vs archived | Spark missed |
| — | — | — | G64-F3 P5 one-mode (M5 survives the PR cells) | Spark missed |
| — | — | — | G64-F4 stale MULTI-TENANCY.md, G64-F5 per-tenant pool, G64-F7 admin override | Spark missed |

| | Verdict |
|---|---|
| Spark | **NO GO** (6 Major: 4 false positives, 1 out-of-scope, 1 partial at Note level) |
| Gate 64 | **GO WITH NOTES** |

## UNMEASURED
- **The PR description on GitHub.** `gh pr view` with the Blockchain project's `GH_CONFIG_DIR` gave rc 4, "gh auth login" (`evidence/pr_view.err`). I checked against the commit message and the two fragments instead. So I cannot say whether the PR body states the per-tenant-pool caching limit, or whether its statement matches G64-F5.
- Node 24 LTS. The four platform suites (Schemathesis, Akto, Playwright, k6); G64-F2 is from code reading. A running stack, the real gateway → originate chain, and a real platform database behind the pool manager. Postgres was used only for the isolated race probe.
- S's 19 mutants (I ran 21 of my own). A planted-error control for eslint.
- Which deployed boxes have `MULTI_TENANCY_ENABLED` on, and whether any tenant there is already suspended or archived (and would start getting 403 the moment this deploys).
- Multi-replica behaviour (each originate process has its own map and timer).

## HOW
- Clone: `git clone --filter=blob:none --no-checkout` over the Blockchain deploy key, then the toplevel assertion, `fetch refs/pull/1876/head develop`, a detached checkout of `33bce392`, `npm ci --ignore-scripts` at `Blockchain/Dev` (rc 0; gate 62's `node_modules` was **not** reused, because its `@secuura/*` workspace links point into gate 62's own tree) and `npm run build` in `packages/shared` (rc 0).
- Suites: `nice -n 10 node_modules/.bin/vitest run --root <pkg> --maxWorkers=2` with TMPDIR set to the gate `tmp/`. originate: `jest -c services/originate/jest.config.js --maxWorkers=2`. Load1 stayed 9.8-12.6 throughout, so I never had to wait for it to fall below 16.
- Probes: `scripts/gate64-probe.test.ts` (shared) and `scripts/gate64-tp-probe.test.ts` (tenant-provisioning), copied into `src/__tests__/` for each run and removed afterwards. The originals live in `scripts/`.
- Base product code and mutants: `scripts/mutants.py base|mutants`. The base swap writes the `c63d3dc6` blobs of `tenant-pool-manager.ts` and `tenant-provisioning/src/index.ts`, then restores them, with sha256 asserted (`evidence/base_runs.json`).
- Race: `scripts/race.sh` against container `gate64-race-pg` (`--network none`), ID recorded in `evidence/race_container.id`, removed by that ID (`docker ps -a --filter id=` → 0).
- Processes: background jobs were `spark_gate.sh`, `spark_review.py`, the mutant run and the suite run. All exited on their own. I killed nothing by name and left no container running.
