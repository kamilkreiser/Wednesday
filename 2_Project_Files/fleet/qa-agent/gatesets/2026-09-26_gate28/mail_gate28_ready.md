# CAPTURE for gate28 (QA/Secuura-batch1286) — 2026-09-26T06:52:25Z

NO READY MESSAGE ID reached the drafter for any PR of this kit (the seat records carry none; a listing would mark mail seen). Each PR's seat
claims are captured from its PR BODY, its head COMMIT MESSAGE and the seat HANDOVER files below, each verbatim with its TEXT_SHA256.

## #1286 KS-1336 (Seat B 30th (round 1 + fix round 1, fast-forward), T3) — head da5f3dd837dd5b6c706e7816bd4028070029d5e1

#1286 ticket line: #1286 is KS-1336.

### PR BODY (gh_body_1286.md) TEXT_SHA256 ecd52a5e4713e9673a881a40bca9050bdabbb545f0c3b02b719c7bc2d22016b8

#1286 docs: correct the tenancy docs to the shared database the code actually uses
head da5f3dd837dd5b6c706e7816bd4028070029d5e1

## BLUF
Both tenancy documents describe a **per-tenant-database architecture that has never existed in any
deployed environment**. A reader of either overestimates the isolation in place. The worst of them is
the **Security Considerations** table, which told anyone checking the security posture that tenants
are physically separated with *"no shared tables"*.

Every claim below is measured at `00de57baeb405d0081fe8b6f192bd40d35acef61` and cited to the source
that implements it. **Nothing here is a plan or a recommendation** — whether the dormant path is
completed or removed is Kam's decision and is deliberately not recorded.

## What is true, and where it lives
- **Every tenant resolves to one shared application database.**
  `services/api-gateway/src/startup-migrations.ts:1116-1144` writes every `tenant_config` row with a
  single `db_name`, `db_host` and `db_port` taken from `DATABASE_URL`. Its own comment reads
  *"On Azure there is a single DB; per-tenant DBs are not provisioned."*
- **Isolation inside it is `tenant_id` + row-level security, fail-closed since
  `migrations/039_rls_fail_closed.sql`.** An unset `app.current_tenant_id` returns **zero** rows,
  where before 039 it returned **all** rows. The deliberate escape is
  `app.tenant_scope_bypass = 'platform_admin'` via `runWithPlatformScope`.
- **Two carve-outs keep 038's permissive policy, both named in 039's header:**
  `platform_document_registry` (public verify-by-hash is cross-tenant by design) and
  `svc_m365_connections` (its `tenant_id` holds the Microsoft/Entra directory id, so the comparison
  could never match).
- **The per-tenant path is dormant behind two flags set in no config file:**
  `MULTI_TENANCY_ENABLED` and `PROVISION_PER_TENANT_DB` (`tenant-pool-manager.ts:151-152`).
  *Control for that zero: 25 config files do mention `DATABASE_URL`, so the search is not blind.*

## FIVE assertions corrected in `MULTI-TENANCY.md`, not the two this change set out to fix
The extra three were found by **sweeping the file for the claim** rather than trusting the line
numbers I was handed. A docs PR that corrects one false line and leaves three standing is worse than
none, because the corrected line lends the rest credibility.

| where | was |
|---|---|
| `:13` summary | "Each client (tenant) receives an isolated PostgreSQL database" |
| `:16` key point | "Each tenant has its own PostgreSQL database (`secuura_tenant_{slug}`)" |
| the architecture **diagram** | drew `secuura_tenant_{slug}` beside `secuura_platform` as though it exists |
| **onboarding steps** | "Provisions a new PostgreSQL database" — a step that does not run |
| **Security Considerations** table | "Each tenant has its own PostgreSQL database — no shared tables" |

The benefits table is kept but re-cast as **intended vs. what holds today**, because three of its five
rows (independent backups, performance isolation, per-tenant residency/deletion) are **not available**
on a shared database and a reader is entitled to know which.

## `RLS-FAIL-CLOSED-PLAN.md` — `:35`, and its neighbour
`:35` claimed *"Real isolation is per-tenant databases."* **False, and false when written.**

Its neighbouring bullet claimed RLS was *"permanently on its fail-open branch — inert today"*. That was
true on 2026-05-29 and **039 has since made it false**. Correcting `:35` alone would have left the
document contradicting its own corrected line, so both are superseded in place. **This is one bullet
wider than the change was scoped to, and it is flagged rather than absorbed** — it can be reverted.

Both are struck through and superseded rather than deleted, because the document's later sections still
reason from them and a reader needs to know **which way** they changed. Everything from "The hard
problem" onwards is unreviewed against today's tree and is left marked a proposal; `status: proposed`
in the front matter is untouched.

## Verification
- **Re-swept after editing:** no live assertion of a per-tenant database remains in either file. The
  four remaining matches are my own correction notice, the struck-through quote, and a reference to
  KS-1055. *Control: the sweep still finds 4 occurrences of `secuura_tenant_`, so it is not silently
  matching nothing.*
- Docs-only: **no code, no migration, no config, no test** changes.
- Push gate `28/0 · 6/0 · 49/0 · 60 of 60`; preflight **12/15 legs ran, 3 SKIPPED (3, 4, 8 — no local
  stack), nothing failed** — not quoted as a pass.
- Base this worktree **CONTAINS**: `00de57baeb40`, develop's tip.

## NOT covered
- The readiness work itself is **not** done here; it is tracked on the parent ticket with its five
  children.
- `docs/TOKENISATION.md` and `docs/DEPLOYMENT.md` were **not** swept for the same drift — out of scope
  for this change, and worth a look by whoever picks up the parent.
- No opinion is offered on whether to build or delete the dormant path.

Refs KS-1336



### EVERY COMMIT MESSAGE IN THE CHAIN (oldest first) TEXT_SHA256 cda287b3ff0f426b8483fbb5cebd5b67169b86abf8c8cf4e7366868b79ed3485

--- commit 27480bb649477435b4a683059d3fcbded3611377
docs: correct the tenancy docs to the shared database the code actually uses

Both tenancy documents describe a per-tenant-database architecture that has
never existed in any deployed environment. Anyone reading either one
overestimates the isolation that is in place, and the Security Considerations
table is the worst of them: it told a reader checking the security posture that
tenants are physically separated with no shared tables.

Every claim below is measured at 00de57baeb405d0081fe8b6f192bd40d35acef61 and
cited to the source that implements it. Nothing here is a plan or a
recommendation: whether the dormant path is completed or removed is Kam's
decision and is deliberately not recorded.

WHAT IS TRUE, and where it is implemented:

  * every tenant resolves to one shared application database.
    startup-migrations.ts:1116-1144 writes every tenant_config row with a single
    db_name, db_host and db_port taken from DATABASE_URL. Its own comment says
    "On Azure there is a single DB; per-tenant DBs are not provisioned."
  * isolation inside that database is tenant_id plus row-level security, and the
    policy has been FAIL-CLOSED since 039_rls_fail_closed.sql: an unset
    app.current_tenant_id now returns ZERO rows where it previously returned ALL
    rows. The deliberate escape is app.tenant_scope_bypass = 'platform_admin' via
    runWithPlatformScope.
  * two tables keep the older permissive policy by design, both named in 039's
    header: platform_document_registry, because public verify-by-hash is
    cross-tenant on purpose, and svc_m365_connections, whose tenant_id holds the
    Microsoft/Entra directory id so the comparison could never match.
  * the per-tenant path exists in code and is dormant behind two flags that are
    set in NO configuration file: MULTI_TENANCY_ENABLED and
    PROVISION_PER_TENANT_DB (tenant-pool-manager.ts:151-152).

FIVE live assertions were corrected in MULTI-TENANCY.md, not the two this change
set out to fix. The extra three were found by sweeping the file for the claim
rather than trusting the line numbers I was given: the architecture diagram, the
onboarding steps that describe provisioning a database that is never
provisioned, and the Security Considerations row.

In RLS-FAIL-CLOSED-PLAN.md the neighbouring bullet is corrected as well as :35.
It asserted RLS was "inert today", which 039 has since made false; correcting :35
alone would have left the document contradicting its own corrected line. Both are
struck through and superseded in place rather than deleted, because the later
sections still reason from them and a reader needs to know which way they
changed. Everything from "The hard problem" onwards is unreviewed against today's
tree and is left marked as a proposal.

Refs KS1336

Co-Authored-By: Claude Opus 5 <noreply@anthropic.com>

--- commit da5f3dd837dd5b6c706e7816bd4028070029d5e1
docs: correct the flag-state sentence — the two flags are NOT in the same state

Fix round 1 for #1286, on N-1286-1. The blocking finding is mine and it is the
exact failure this PR exists to correct: a claim wider than its measurement,
written into a document I was correcting for making claims wider than the code.

I measured PROVISION_PER_TENANT_DB in .env/.example/.yml/.yaml/.json and found
zero. I then wrote, twice, that "two flags" are "set in no configuration file" --
generalising from a one-flag search that never looked at the second flag and never
covered .bicep at all.

MEASURED now, and each citation read at the line before it was written:

  * PROVISION_PER_TENANT_DB is absent from deployment/ entirely. It is the flag
    that actually gates per-tenant databases, and it is off everywhere. The
    original claim was true of this flag alone.
  * MULTI_TENANCY_ENABLED is "true" in deployment/azure/env.dev.json:7,
    deployment/azure/env.demo.json:7 and deployment/azure/services.bicep:798. It
    is ON in dev and demo. It enables tenant ROUTING; with the other flag off,
    every tenant still routes to the shared database.

Both sentences now say that, with the two flags distinguished rather than merged.
The conclusion each supported is unchanged and still holds: the per-tenant path is
dormant, because the flag that gates it is off.

Also N-1286-2, the one-line citation the gate named: the onboarding step cited the
boot seed of 8 fixed tenant ids. A new tenant's tenant_config row is written by
tenant-provisioning/src/index.ts:245-274, the INSERT at :271. Verified by reading
both lines.

Nothing else is changed. The gate's other notes (N-1286-3 through N-1286-6) are
not in this round and are named in the READY instead of quietly folded in.

Refs KS-1336

Co-Authored-By: Claude Opus 5 <noreply@anthropic.com>



### PUSH LOG STOP COUNTS (READ, bounded region; /Volumes/DevMASTER/!CODING/Secuura/Blockchain/5_Project_History/2026-09-26_seatB-30th/raise/s-b30-tenantdocs-ff-da5f3dd837dd-push.out)

```
{
 "log": "/Volumes/DevMASTER/!CODING/Secuura/Blockchain/5_Project_History/2026-09-26_seatB-30th/raise/s-b30-tenantdocs-ff-da5f3dd837dd-push.out",
 "lines": 1300,
 "pre_push_hook_base": "28/0",
 "fixture_guard": "6/0",
 "run_shell_suites_region": "49/0",
 "run_shell_suites_prefixed": "49/0",
 "shell_suites": "60 passed, 0 failed, 0 skipped (of 60)",
 "CONTROL_absent_header": "NOT FOUND",
 "fixture_build_failed_lines": 0,
 "verdict_line": "PREFLIGHT INCOMPLETE \u2014 12/15 legs ran, 3 SKIPPED. Nothing failed.",
 "preflight_ran": true,
 "rc": "0",
 "start": "2026-09-26T04:35:08Z PUSH START",
 "end": "2026-09-26T04:42:29Z push rc=0"
}
```

## #1288 KS-1341 (Seat B 31st (local-model patch, Spark spark-dsv4flash under a Wednesday brief, re-verified by the seat), T1) — head cb58d3a59c8921a3a1caede3c6acfb4b599bf959

#1288 ticket line: #1288 is KS-1341.

### PR BODY (gh_body_1288.md) TEXT_SHA256 750b780bc5e3a7fd8019472905fe2b105265ae8758b6beb629458e525d54cd80

#1288 KS-1341 part A: route the webhooks GET / and POST / 500s through a fail500 helper
head cb58d3a59c8921a3a1caede3c6acfb4b599bf959

## BLUF

`routes/webhooks.ts` answered **500 with the thrown error's own text on seven unconditional sites, with no `NODE_ENV` guard**, so internal detail reached the client in every environment including production. **This is part A of 3:** it adds the file's `fail500` helper and converts the first two sites (`GET /` and `POST /`). **Parts B and C convert the remaining five and are NOT in this change** — the ticket stays In Progress after this merges.

Same helper shape already merged three times for this family under KS730 (`routes/gdpr.ts`, `routes/systemErrors.ts`): log the thrown text server-side with the route named, answer a constant body.

**Origin, stated plainly: the patch was produced by the local model (`spark-dsv4flash`) under a Wednesday brief, and re-verified by this seat.** The harness's own figures are quoted below as the harness's; every figure under "ran" is mine, measured in the environment named.

## What changed

| file | change |
|---|---|
| `Blockchain/Dev/services/originate/src/routes/webhooks.ts` | +20 / −2 — a `fail500(res, context, err)` helper, and `GET /` + `POST /` routed through it |
| `Blockchain/Dev/services/originate/src/__tests__/ks1341a-webhooks-500-never-answers-err-message.test.ts` | new, 173 lines — 4 red-first cells + 4 controls |

`message: err.message` in this file: **7 → 5** (the five are parts B and C). `fail500(` appears **3 times** — one declaration, two calls.

## Test Evidence

**Environment these figures name:** worktree detached at develop `e080174c86c671349c508560744644fc0ef33388`, which the worktree **contains** (`merge-base --is-ancestor` asserted); `npm ci` at `Blockchain/Dev`; **`packages/shared` BUILT** (`npm run build`, 28 files in `dist/`). Without that build 60 of 80 originate suites fail on `Cannot find module '@secuura/shared'` — that is the environment, not a regression, and every count below is from the built tree.

**Touched:** `services/originate` (product + a new unit cell). Read-only consumers: `packages/shared`, whose guards read originate sources by text.

**Ran:**

| check | command | result |
|---|---|---|
| red-first, cell alone (product hunks NOT applied) | `jest --runInBand <cell>` | **4 failed / 4 passed / 8 total** — the 4 declared cells red, all 4 controls green |
| green, both files | `jest --runInBand <cell>` | **8 passed / 8 total** |
| whole originate suite, BARE at the tip | `jest --runInBand` | **80 suites, 943 tests, 0 failed** |
| whole originate suite, PATCHED at this head | `jest --runInBand` | **81 suites, 951 tests, 0 failed** — `bare 943 / patched 951`, **0 new reds** (set difference on FAIL lines) |
| project type-check | `tsc --noEmit` | rc 0, no output |
| type-check **including the test file** | `tsc -p <extends tsconfig, exclude:[]>` | **rc 0, 0 errors** |
| `packages/shared` | `vitest run` | **48 files, 945 tests, 0 failed** |
| lint at the tip | `npm run lint` (`eslint src`) | rc 0 — **22 problems (0 errors, 22 warnings)**; `webhooks.ts` mentioned 0× |
| lint at this head | `npm run lint` | rc 0 — **22 problems (0 errors, 22 warnings)**; `webhooks.ts` 0×, the new cell 0× |

**Each red proved it reached the code under test, not merely that the body was clean.** The A1 reds fail with `"leaked": true` — the thrown text *is* in the 500 body at the tip. The A2 reds fail because the logger was never called with the route's context. All four are `toEqual` assertion failures; none is a load failure or a mock crash. **0 passed and 0 failed would have been a load failure, not a pass** — 4 passing controls in the same run prove the file loaded.

**The `GET /` trap is handled and pinned.** `GET /`'s list query carries `.catch((e) => { logger.warn(...); return []; })`, so a *rejected* `$queryRaw` is swallowed into a 200 with an empty list and never reaches the catch under test. The cell therefore makes `$queryRaw` throw **synchronously**, and `control KS-1341 A0` pins the swallowing branch so it cannot come back silently. Measured separately: **no catch block in this file tests error text at all** (no `includes(`, no `.code ===`), so no fixture string can be routed down a benign branch here.

**Two zeros that were controlled rather than asserted:**
- **The lint zeros.** `eslint src` covers **137 files, 86 of them under `__tests__`**, and the new cell is in that set. A planted `debugger` + unused variable in the cell yields **1 error and 1 warning** — so the instrument fires on this exact file. The file was then restored and the restore verified by sha256.
- **The type-check zero.** The project's own `tsconfig.json` **excludes `src/__tests__`**, so `tsc --noEmit` rc 0 covers 626 files and **zero** test files — it says nothing about the new cell. `--listFilesOnly` on a config that extends it with `exclude: []` shows the cell present and 86 test files in the program; that run is the rc 0 quoted above.

**NOT run:** the local stack is not up, so nothing integration-level, no gateway, no Postgres, no container. No deploy of any kind — not local, not demo, not UAT.

**Migrations + config:** none. No migration, no `package.json`, no lockfile, no `.github/`, nothing under `scripts/`.

## NOT COVERED — and one comment that is wrong at this PR

🔴 **The helper's docblock opens: *"KS-1341: the only place in this router that turns a caught error into a 500."* That sentence is FALSE at this PR.** After part A, **5** response lines in this file still carry `message: err.message`. It becomes true only once parts B and C land. It is raised this way deliberately: the diff is **byte-identical** to the local model's reviewed output (sha256 `65720c1d4caa05f503f4d331cd3b4588b9d60b09b94647f8e3c8c4ab6ca9d67b`, `cmp` rc 0 against both the golden and the run's canonical patch), and that provenance is worth more than a tidier comment parts B and C will make accurate. The same docblock's *"Declared at the END of the file"* was checked and **is** accurate — the helper sits at the end, immediately before the file's last line.

Also not covered: the other **five** `err.message` sites in this file (parts B and C); whether any further file in this family remains unswept (the ticket says that was not swept); and any behaviour of the five routes this change does not touch.

Refs KS-1341

## The push gate, as it actually ran on this head

`cb58d3a59c89` pushed under `.push-lock-27`; the in-hook preflight ran for ~6.5 min.

- **`pre_push_hook_base` 28/0 · `pre_push_hook_base_fixture_guard` 6/0 · `run_shell_suites` 49/0 · shell suites 60 passed, 0 failed, 0 skipped (of 60)** — the declared fleet condition, now **measured** on this tree (it was declared, not measured, at `e080174c86c6`: develop had moved 13 commits since the last measurement, one of them a `.sh` file).
- **0** lines starting `FIXTURE BUILD FAILED`.
- **`PREFLIGHT INCOMPLETE — 12/15 legs ran, 3 SKIPPED. Nothing failed.`** — 12/15 ran; legs 3, 4 and 8 **NOT run** (local stack not up on `http://localhost:6882`; all three skip lines say so). A skip is not a pass, which is why the verdict line says INCOMPLETE rather than PASSED.

Counts were parsed by **exact basename per suite block**, because `pre_push_hook_base` is a prefix of both `pre_push_hook_base_fixture_guard` and `pre_push_hook_base_leg_comment` — read loosely it reports 6/0 or 4/0 where the truth is 28/0, and an under-reported count reads as a missing gate. The three resolve distinctly: 28/0, 6/0, 4/0. The log carries **two** count-line formats (26 bare-indented, 25 name-prefixed), so each figure was confirmed in whichever form its own suite uses.



### EVERY COMMIT MESSAGE IN THE CHAIN (oldest first) TEXT_SHA256 9c01e923ba955c2615822baf5ef335e8404e2291f74e5fbd1ff1c19d2100311a

--- commit cb58d3a59c8921a3a1caede3c6acfb4b599bf959
KS-1341 part A: route the webhooks GET / and POST / 500s through a fail500 helper

routes/webhooks.ts answered 500 with the thrown error's own text on seven
unconditional sites, with no NODE_ENV guard, so internal detail reached the
client in every environment including production. Part A adds the file's
fail500 helper and converts the first two sites (GET / and POST /); parts B
and C convert the remaining five and are NOT in this change.

Same helper shape already merged three times for this family under KS730.

Patch produced by the local model under a Wednesday brief, re-verified by this
seat: strict apply at develop's tip, red-first on the untouched tip, green with
the product hunks, whole-suite delta and lint measured at both trees.

Refs KS-1341

Co-Authored-By: Claude Opus 5 <noreply@anthropic.com>



### PUSH LOG STOP COUNTS (READ, bounded region; /Volumes/DevMASTER/!CODING/Secuura/Blockchain/5_Project_History/2026-09-26_seatB-31st/raise/s-b31-ks1341a-cb58d3a59c89-push.out)

```
{
 "log": "/Volumes/DevMASTER/!CODING/Secuura/Blockchain/5_Project_History/2026-09-26_seatB-31st/raise/s-b31-ks1341a-cb58d3a59c89-push.out",
 "lines": 1305,
 "pre_push_hook_base": "28/0",
 "fixture_guard": "6/0",
 "run_shell_suites_region": "49/0",
 "run_shell_suites_prefixed": "49/0",
 "shell_suites": "60 passed, 0 failed, 0 skipped (of 60)",
 "CONTROL_absent_header": "NOT FOUND",
 "fixture_build_failed_lines": 0,
 "verdict_line": "PREFLIGHT INCOMPLETE \u2014 12/15 legs ran, 3 SKIPPED. Nothing failed.",
 "preflight_ran": true,
 "rc": "0",
 "start": "2026-09-26T06:10:24Z PUSH START",
 "end": "2026-09-26T06:17:23Z push rc=0"
}
```

## #1289 KS-1318 (Seat B 31st (hunk 3 of #1268's ks781 diff, raised alone), T2) — head 1e24633b9c196c5d3dd5bb83519bce860ca79758

#1289 ticket line: #1289 is KS-1318.

### PR BODY (gh_body_1289.md) TEXT_SHA256 7ebab1c2d84a81e676aa8abcbb83e5b1f6ec821a776dd6be34aa472ce31327b1

#1289 KS-1318: assert the ks781 combined default-shapes control by tag set, not by count
head 1e24633b9c196c5d3dd5bb83519bce860ca79758

## BLUF

The J2 **combined** default-shapes control in `ks781-p3-3-body-parser-order.test.ts` asserted `toHaveLength(3)` — the **count** of shapes `defaultShapesOf()` found, not **which** shapes. So it was green under any permutation of the walk, and under any relabelling that kept the cardinality, **including the two shapes the fixture exists to tell apart being detected under one another's name** — the ticket's own words. It now asserts the set of tags in source order with `toEqual`.

**One hunk, one file, +10 / −1.** Test-only: no product byte changes.

## Why this is a new PR, and what it is NOT

This hunk was first raised inside **#1268**, which carries it *and* KS1316's two hunks. #1268 failed at the two-NO-GO cap on KS1316's guard-reachability rule, so it ships nothing and stays open — **this PR does not touch it: no push to it, no close** (its disposition is not a seat's call). **#1287** carried KS1142's `entrypoint-corpus.test.ts` alone and the gate correctly amended its squash to name KS1142 alone. **So nothing of KS-1318 has merged**; on develop the cell still reads `toHaveLength(3)`.

**Nothing of KS1316 is in this PR**, and that is measured rather than asserted: a KS1316-only token (`W9`) appears **0×** in this PR's diff and **7×** in the full three-hunk diff, so the check can see the thing it reports absent. This PR's diff carries **1 hunk**; the develop→#1268 diff carries 3.

The file's blob is `e96215365a6d` at **both** #1268's merge base (`4db87c3e4b98`) and develop, so the hunk's pre-image is unchanged and it applied to develop strictly — `patch -F0` / `git apply --check` rc 0, with a control (the anchor line tampered) failing 1 of 1 hunks.

## Test Evidence

**Environment these figures name:** worktree detached at develop `e080174c86c671349c508560744644fc0ef33388`, which it **contains** (`merge-base --is-ancestor` asserted); `npm ci` at `Blockchain/Dev`; `packages/shared` **BUILT** (`npm run build`, 28 files in `dist/`). Runner: vitest.

**Touched:** `packages/shared` — one assertion in one existing test cell. No product file. No other package.

**Ran — two arms, each at BOTH trees, each red set asserted EXACTLY (not "contains"):**

| arm | at develop (`toHaveLength(3)`) | at this head (`toEqual([…])`) |
|---|---|---|
| **A — permutation:** `return shapes;` → `return shapes.reverse();` | **0 red, file 242/242 green** — the blindness this ticket reports | **1 red: the combined cell ALONE**; all three per-shape rows green |
| **B — relabel, cardinality preserved:** the default-function and alias branches swap their `shapes.push` labels | **2 red: the two per-shape rows only; the combined cell stays GREEN** | **3 red: the two rows AND the combined cell** |

Arm A proves the new assertion is **necessary**; arm B proves it does **not over-fire** (the per-shape rows behave identically at both trees — only the combined cell changes). **Both arms matched a red set predicted before the run, 2/2 at each tree.**

Every tamper: anchor uniqueness asserted **before** the edit (`count == 1`; `return shapes;` occurs exactly once, at `:4927` inside `defaultShapesOf` at `:4906`), restored **by content**, and the restore verified by a **sha256 of the whole file**. `git checkout` was not used — it reverts more than the tamper if anything else in the tree moved. The runner also refuses a 0-cell result as a load failure rather than a pass.

| suite / check | tip | this head |
|---|---|---|
| `ks781-p3-3-body-parser-order.test.ts` | **242 passed** | **242 passed** |
| whole `packages/shared` (`vitest run`) | **48 files, 945 tests, 0 failed** | **48 files, 945 tests, 0 failed** |
| `tsc -p . --noEmit` | rc 0, **0 errors** | rc 0, **0 errors** |
| `npm run lint` (`eslint src`) | rc 1 — **36 problems (1 error, 35 warnings)** | rc 1 — **36 problems (1 error, 35 warnings)** |

The cell count does not move because this edits an assertion inside an existing cell rather than adding one.

🔴 **The lint run is red at BOTH trees, and it is pre-existing, not introduced here.** The single error is `no-control-regex` on the KS703 control-byte guard at `src/middleware/index.ts:539` — a rule firing on code whose purpose is to match control bytes. It is already on the backlog (`BACKLOG.md:876`, which records it at `:521` with 31 warnings; the line has since moved to `:539` and the warnings to 35 — a count names the tree it was measured on). **The two lint outputs are byte-identical after normalising the worktree path**, and `ks781` is mentioned in neither, so this change is provably lint-neutral. The tip figure is taken from a second worktree in which this file is at develop's blob (`e96215365a6d`, asserted) with `packages/shared` clean.

**NOT run:** the local stack is not up, so nothing integration-level, no gateway, no Postgres, no container. Legs 3, 4 and 8 of the push preflight do not run without it. Nothing deployed — no local stack, no demo, no UAT.

**Migrations + config:** none. No migration, no `package.json`, no lockfile, nothing under `scripts/` or `.github/`.

## NOT COVERED

- **KS1316's two hunks** (the walk and cells W9–W13) — not in this PR, and `#1268`'s cap and disposition are not addressed here.
- Whether `defaultShapesOf`'s **walk** is correct — this change pins what the combined cell *asserts*, not the walker. The walker's correctness at this tree is what the per-shape rows and KS1144's own cells cover.
- A third arm (e.g. a branch made to fire twice) was not written; arms A and B already separate necessity from over-firing.
- Nothing integration-level, and nothing deployed.

Refs KS-1318

## The push gate, as it ran on this head

`1e24633b9c19` pushed under `.push-lock-27`, taken 06:30:10Z and released 06:36:58Z by me; push rc **0**.

**`pre_push_hook_base` 28/0 · `pre_push_hook_base_fixture_guard` 6/0 · `run_shell_suites` 49/0 · shell suites 60 passed, 0 failed, 0 skipped (of 60)** — the fleet condition, met. **0** lines starting `FIXTURE BUILD FAILED`. `PREFLIGHT INCOMPLETE — 12/15 legs ran, 3 SKIPPED. Nothing failed.` — legs 3, 4, 8 **NOT run** (local stack not up). Counts parsed per suite block by exact basename; the three prefix-sharing suites resolve distinctly as 28/0, 6/0 and 4/0, so an under-read (which would look like a missing gate) is excluded.



### EVERY COMMIT MESSAGE IN THE CHAIN (oldest first) TEXT_SHA256 da2ca841037754d48dd46bdbed1c72a3165fbc8345b80ce2638b30099dec3d4b

--- commit 1e24633b9c196c5d3dd5bb83519bce860ca79758
KS-1318: assert the ks781 combined default-shapes control by tag set, not by count

The J2 combined control cell asserted toHaveLength(3) on defaultShapesOf's
return, so it was green under any permutation of the walk and under any
relabelling that kept the cardinality — including the two shapes the fixture
exists to tell apart being detected under one another's name. The per-shape
rows above it are fed ONE shape each, so they cannot witness an interaction
between branches, which is the only thing the combined fixture is for.

It now asserts the SET of tags in source order with toEqual.

Measured at both trees: with the walk's whole return reversed, develop stays
242/242 green and this cell alone reds here; with two push labels swapped
(cardinality preserved) develop reds only the two per-shape rows and keeps the
combined cell green, while here the combined cell reds as well.

This hunk was first raised inside PR #1268 alongside KS1316's two hunks. #1268
is at its two-NO-GO cap on KS1316's guard-reachability rule and ships nothing,
and #1287 carried KS1142's corpus file only, so nothing of this ticket has
merged. It is re-raised here alone; nothing of KS1316 is in it.

Refs KS-1318

Co-Authored-By: Claude Opus 5 <noreply@anthropic.com>



### PUSH LOG STOP COUNTS (READ, bounded region; /Volumes/DevMASTER/!CODING/Secuura/Blockchain/5_Project_History/2026-09-26_seatB-31st/raise/s-b31-ks1318j2-1e24633b9c19-push.out)

```
{
 "log": "/Volumes/DevMASTER/!CODING/Secuura/Blockchain/5_Project_History/2026-09-26_seatB-31st/raise/s-b31-ks1318j2-1e24633b9c19-push.out",
 "lines": 1305,
 "pre_push_hook_base": "28/0",
 "fixture_guard": "6/0",
 "run_shell_suites_region": "49/0",
 "run_shell_suites_prefixed": "49/0",
 "shell_suites": "60 passed, 0 failed, 0 skipped (of 60)",
 "CONTROL_absent_header": "NOT FOUND",
 "fixture_build_failed_lines": 0,
 "verdict_line": "PREFLIGHT INCOMPLETE \u2014 12/15 legs ran, 3 SKIPPED. Nothing failed.",
 "preflight_ran": true,
 "rc": "0",
 "start": "2026-09-26T06:30:10Z PUSH START",
 "end": "2026-09-26T06:36:58Z push rc=0"
}
```

## SEAT RECORD /Volumes/DevMASTER/!CODING/Secuura/Blockchain/5_Project_History/HANDOVER-seatB30-2026-09-26.md TEXT_SHA256 ec1cfa9ee5b8cf20bff6e960e0be69520ae05bf098f6b4e68b1868be4945fe56

# HANDOVER — Seat B 30th, Secuura/Blockchain, round 26 + gate27 (2026-09-25 23:14Z → 04:5xZ). WRAPPED.

Written to be read COLD. Nothing here assumes you were in the room.

## STATE IN ONE LINE
**Five PRs MERGED (#1261, #1274, #1284, #1285, #1287). Three open.** Queue complete; every gate verdict
that came back was actioned. Four tickets filed. **Nothing deployed.**

## MERGED — by me, on Wednesday's signed GO, after M1 wrapped
| PR | ticket | squash |
|---|---|---|
| #1284 | KS-730 PR 3 | merged into develop |
| #1274 | KS-934 | merged |
| #1261 | KS-1293 | merged |
| **#1285** | KS-766 | **`c40b3a460098228bb2977f94ea478614a5ece666`** |
| **#1287** | KS-1142 | **`e080174c86c671349c508560744644fc0ef33388`** |

**I merged the last two myself** — M1 had wrapped and Wednesday's gate27 GO named me as their author.
Each verified after the fact: merged at the pin, blob == the equality target (**mode 100755 checked**
on #1285), squash touched its own path only, message byte-exact. develop is now `e080174c86c6`.

## OPEN — and what each needs
| PR | head | state |
|---|---|---|
| **#1286** | `da5f3dd837dd5b6c706e7816bd4028070029d5e1` | **fix round 1 of 2 READY — goes to the next gate.** |
| **#1268** | `5ac42fafeee1` | **NO GO at the cap. Ships nothing. DO NOT CLOSE — that is Kam's.** |
| **#1278** | `18cca0a7e0fe` | **NO GO at the cap. Ships nothing. DO NOT CLOSE — that is Kam's.** |

## THE FIRST THING A SUCCESSOR SHOULD DO
**Re-raise KS-1318's J2 hunk alone.** #1287 carried KS-1142's file only. KS-1318's work — the combined
default-shapes control asserting the three tags with `toEqual` in source order instead of by count —
lives in `packages/shared/src/__tests__/ks781-p3-3-body-parser-order.test.ts`, which #1287 deliberately
excluded. On develop, J2 still reads `toHaveLength(3)`. **KS-1318 is In Progress with nothing merged.**
My #1287 PR body wrongly credited it; the gate corrected the squash to name KS-1142 alone and was right.

## THEN, IN ORDER
1. **#1286 round 2** if the gate asks for one. Four known notes are already named and untouched:
   N-1286-3 ("writes *every* `tenant_config` row" — it is the 8 seeded ids; provisioning writes the
   rest), N-1286-4 ("the only tenant isolation" is overstated: 21 service files also filter on
   `tenant_id`), N-1286-5 (RLS-plan `:57` still reasons from per-tenant DBs, unmarked), N-1286-6
   ("*the* deliberate exception" omits 039 §3's `secuura_auth_lookup` path).
2. **KS-1333** — still blocked only by #1281's merge state; check it.
3. **KS-1334** (High), **KS-1335**, **KS-1337** — filed this round, none built.

## TICKETS FILED THIS ROUND
- **KS-1334** (High) — four handlers in `adminConfig.ts` return `err.message` with **no `NODE_ENV`
  guard**, so they leak in production. Pre-existing. `KS-730 C4 SOURCE` pins them; **fixing one will
  red that cell — that is the intended signal.**
- **KS-1335** — `last_sent_at` is written only on success, so a permanently failing webhook defeats
  #1274's rotation. **Cell R3 pins today's behaviour and will red when this is fixed.**
- **KS-1336** — per-tenant DB readiness parent. KS-1304/1235/1055/1054 are sub-issues; **KS-598 keeps
  KS-772 (Stuart's stream) and is linked `related` — do not re-parent it.**
- **KS-1337** — `runner/cli.ts:162` takes a path from `URL.pathname`. **The QA gate's own checkout
  (`…/Testing Agent MAIN/`) has spaces**, so it is live on this fleet.

## THE TRAPS — including four of my own
1. **A fixture that routes the subject down a different branch yields green cells about code that
   never ran.** KS-730's cell failed 9/12 because its error string contained `does not exist`, which
   all four routes' benign catch branch tests for. Three cells were PASSING unexercised.
2. **Re-measure a DIAGNOSIS, not just a figure.** The brief's cause for that was four line numbers in
   a route the cell never calls. Wednesday owned it.
3. **A gate's prescribed fix can be insufficient.** #1268's two ruled shapes could not satisfy its own
   required cell (the returned arrow has no binding). Measure the stated fix before assuming it works.
4. 🔴 **MY #1268 THIRD RULE MISSED PARENTHESES.** I added an escape rule for a returned function
   expression and did not unwrap a `ParenthesizedExpression` — with a paren-unwrap branch sitting a few
   lines above. That is the residue that put #1268 at the cap.
5. 🔴 **MY #1278 AST READER LEFT A THIRD DOOR.** It matches a callee named `require`; a
   `createRequire(import.meta.url)` result bound to another identifier is not matched, reads 0 hits,
   file stays green. **Same indirect-route class as the original defect, one level out.**
6. 🔴 **MY #1278 HEAD TURNED `npm run lint` RED — 7 errors.** I ran `tsc` and the suites and took that
   for clean. **`tsc` green is not lint green; run the package's own lint script.**
7. 🔴 **MY #1286 SENTENCE WAS WIDER THAN MY MEASUREMENT.** I grepped one flag and wrote a claim about
   two. `MULTI_TENANCY_ENABLED` is `"true"` in three config files; my globs never covered `.bicep`.
8. **`pre_push_hook_base` is a PREFIX of `pre_push_hook_base_fixture_guard`** — a substring parser
   reports 6/0 where the truth is 28/0, and an under-reported STOP count reads as a **missing gate**.
9. **Counts are indented** in the push log and the base-image self-test: `grep -c '^PASS'` returns 0
   on a healthy run. Count unanchored, keep the anchored count as a control.
10. **0 passed AND 0 failed is LOADFAIL, never a pass.** I wrote compile-breaking tampers twice.
11. **A control that fails for a different reason is not a control.** Reproducing a base lint figure,
    I restored one file without its dependent; the run died on `tsc` TS2305, proving nothing.
12. **Linear relations are DIRECTIONAL** — a one-sided `relations` query reads `[]` and looks failed.
13. **A count names the tree it was measured on** — `packages/shared` reads 930 on one base and 941 on
    another; that is `walkTimeouts` landing between them, not a regression.

## 🔴 THE INSTRUMENT THAT LIED
My inbox watcher reported *"no new Wednesday mail"* for **43 consecutive polls while its matcher was a
`SyntaxError`**. The crash matched neither success nor error branch and fell through to the reassuring
`else`. Two mails sat unread behind it. **My "proof" that it worked had tested a reimplementation, not
the script.** Rewritten: the matcher is its own file, and a poll that does not print `SCANNED n` reports
**"MATCHER BROKEN, THIS POLL PROVES NOTHING"**. Both arms proven by driving the real script.
**A second, subtler failure followed:** it exits on first fire by design, and I restarted it with a
`since` old enough to fire immediately on already-seen mail — so it died again and was not watching
when the gate27 GO arrived. **Anchor a restart on the newest mail, not the last one you read.**

## STATE AT WRAP
Shared checkout **never written**: boot and wrap identical — HEAD `3bad652d17cf`, **17 `??` / 0
non-`??`**, local `develop` unmoved, `.git/config` byte-identical across every `worktree add` and all
four fetches (every worktree detached from a raw SHA, never `-b`). `.push-lock-26` released; each fetch
took it only after reading `.push-lock-25`. **No Postgres started**: 0 containers `s-b30-pg-`, 0
listeners in 55440-55449 (control: 2 on `:5432`).
Worktrees `s-b30-{ks934,ks1318,ks1293,ks766,tenantdocs,ks1314,corpus}` — all pushed, all removable.
**The adopted `s-b29-ks730c`** is at `dfc2468a5`, **porcelain 0, merged as #1284 — safe to remove.**
Tools and every proof: `5_Project_History/2026-09-26_seatB-30th/raise/`.

## 🔴 STILL WITH KAM
- **The audit fuse lapses `2026-09-30T00:00Z`** — from then **every `Blockchain/Dev` push is refused**,
  including any round 2 on #1286. **Needs Kam's own word; a relay does not substitute.**
- **#1268 and #1278 are at the cap and must NOT be closed by a seat** — Kam's disposition.
- **KS-1304** (ruled (c)) and **KS-1267** remain with him.


## SEAT RECORD /private/tmp/claude-501/-Volumes-DevMASTER-WEDNESDAY/6a51240d-d642-471f-b7c2-1011f35eb0ce/scratchpad/gate28/gh_comments_1286.md TEXT_SHA256 176ee99beeb0bdb3eef12736be1bd35313ac678c1f1737e9b9c650ad2d03364a

--- comment 5841924450 by linear[bot] at 2026-09-26T01:25:07Z
<!-- linear-linkback -->
<details>
<summary><a href="https://linear.app/secuura/issue/KS-1336/per-tenant-db-readiness-the-dormant-per-tenant-database-path-and-the">KS-1336 Per-tenant DB readiness: the dormant per-tenant-database path, and the five tickets that each break it</a></summary>
<p>

## BLUF

**Every tenant shares one database today.** Isolation comes from a `tenant_id` column plus
fail-closed RLS. A per-tenant-database path exists in the code and is **switched off**. This is the
parent for the five tickets that each break that path in a different way, so the work has one place
rather than five.

**Nothing is built by this ticket.** It exists because Kam ruled option (c) on KS-1304 — *"Leave it*
*until per-tenant databases are actually planned. Nothing changes. The ticket keeps the measurement for*
*whoever builds per-tenant databases"* (2026-09-26 07:19) — with the note **"start planning the**
**database"**. This ticket is the artefact that carries that ruling onto the board.

## Measured at `00de57baeb405d0081fe8b6f192bd40d35acef61` (develop's tip), by this seat

Re-measured here rather than carried over from the planning document, which read an older tree.

1. **The flag is set in 0 config files.** `PROVISION_PER_TENANT_DB` occurs in exactly **two source**
   **files** — `packages/shared/src/db/tenant-pool-manager.ts:152` and
   `services/tenant-provisioning/src/index.ts:245` — and in **no** `.env`, `.example`, `.yml`,
   `.yaml` or `.json` config file. *Control: 25 config files do mention* `DATABASE_URL`*, so the*
   *config-file search is not blind.*
2. **Every tenant is seeded onto the shared database, and the code says so in its own comment.**
   `services/api-gateway/src/startup-migrations.ts:1116-1144` writes all eight `tenant_config` rows
   with the same `db_name`, `db_host` and `db_port`, derived from `DATABASE_URL`. The comment at
   `:1116-1117` reads: *"Ensure all tenants have a tenant_config entry pointing to the shared*
   *'secuura' database. On Azure there is a single DB; per-tenant DBs are not provisioned."*
3. **The docs state the opposite.** `docs/MULTI-TENANCY.md:13` — *"Each client (tenant) receives an*
   *isolated PostgreSQL database"* — and `:16` — *"Each tenant has its own PostgreSQL database*
   *(*`secuura_tenant_{slug}`*)"*. `docs/RLS-FAIL-CLOSED-PLAN.md:35` — *"Real isolation is per-tenant*
   *databases."* **The second of those is internally contradictory**: the two lines immediately above
   it say RLS is *"permanently on its fail-open branch — inert today"*, so that document simultaneously
   says isolation comes from per-tenant databases and that the mechanism which would route to them is
   not in use. A reader of either doc will overestimate the isolation that exists.

A docs PR correcting both files is raised separately and links here.

## The five tickets, and why each blocks switching the path on

* **KS-1304** — `documents.ts` mixes a tenant-pool read with a default-pool write. Ruled (c): left
  until per-tenant databases are planned. `adminConfig.ts` carries 9 of the 11 `withTenant(` sites.
* **KS-1235** — auth's tenant-pool statements carry no tenant GUC.
* **KS-1055** — per-tenant databases never receive the file migrations. Measured on that ticket: a new
  tenant database comes up with RLS forced on and **zero policies**, so the app can read nothing.
* **KS-1054** — migration-runner ordering and exit status.
* **KS-598** — the MULTI_TENANCY registry upsert silently collapses. **KS-598 keeps KS-772 as its**
  **parent** (Stuart's review stream — re-parenting it would silently remove an item from a human's
  queue) and is linked here as *related* instead.

## What this ticket is NOT

* It does not choose between building the opt-in dedicated-database tier and deleting the dormant path
  and hardening RLS. **That decision is Kam's**, and it turns on whether a named customer or contract
  needs physical separation (data residency, per-tenant restore or deletion, customer-held keys) or
  whether this is defence in depth.
* It carries **facts only**. The planning document's recommendations and phasing are deliberately not
  reproduced here, so the board does not record a plan as though it were agreed.

## Search before filing

`searchIssues`, KS team, `includeArchived: true`, every page literal-matched client-side:
`per-tenant DB readiness` **0**, `tenant database readiness` **0**, `dedicated database tier` **0**;
`PROVISION_PER_TENANT_DB` returns **3** — KS-1055, KS-1304, KS-1235, i.e. the children, **no parent**;
`per-tenant database` returns 2, both children. Controls: `tenant` **49** literal hits and
`multi-tenancy` **8** (the matcher fires), a nonce token never written anywhere **0**.
</p>
</details>
<!-- linear-review-link -->
<p><a href="https://linear.app/secuura/review/docs-correct-the-tenancy-docs-to-the-shared-database-the-code-actually-3669363ed09c">Review in Linear</a></p>

--- comment 5843252951 by kksecura at 2026-09-26T04:43:11Z
## FIX ROUND 1 of 2 — N-1286-1 TWO-FLAGS-FALSE. New head `da5f3dd837dd5b6c706e7816bd4028070029d5e1`

**The blocking finding is mine, and it is the exact failure this PR exists to correct.**

I measured `PROVISION_PER_TENANT_DB` across `.env` / `.example` / `.yml` / `.yaml` / `.json` and found
zero. I then wrote, **twice**, that *"two flags"* are *"set in **no** configuration file"* — generalising
from a search that never looked at the second flag and never covered `.bicep` at all. A claim wider
than its measurement, written into a document I was correcting **for making claims wider than the code**.

### What is true, each citation read at the line before writing it
| flag | state | where |
|---|---|---|
| `PROVISION_PER_TENANT_DB` | **set in no configuration file** — absent from `deployment/` entirely | `tenant-pool-manager.ts:152`, `tenant-provisioning/src/index.ts:245` |
| `MULTI_TENANCY_ENABLED` | **`"true"` in dev and demo** | `deployment/azure/env.dev.json:7`, `env.demo.json:7`, `services.bicep:798` |

The distinction matters: `PROVISION_PER_TENANT_DB` is the flag that actually gates per-tenant
databases and it is off everywhere; `MULTI_TENANCY_ENABLED` enables tenant **routing**, and with the
other flag off every tenant still routes to the shared database. **The conclusion each sentence
supported is unchanged and still holds** — the per-tenant path is dormant, because the flag that gates
it is off. Only the reason was wrong.

### Also in this round — N-1286-2, the one-line citation
The onboarding step cited `startup-migrations.ts:1116-1144`, which is the boot seed of 8 fixed tenant
ids. A **new** tenant's `tenant_config` row is written by
`tenant-provisioning/src/index.ts:245-274`, the INSERT at `:271`. Both lines read before citing them.

### NOT in this round, and named rather than quietly folded in
The gate raised four more notes. The GO authorised the two sentences plus the one-line citation and
said *"change nothing else"*, so these are **not** done here:
- **N-1286-3** — *"writes **every** `tenant_config` row"* is wrong for the cited block (it is the 8
  seeded ids; provisioning writes the rest).
- **N-1286-4** — *"the only tenant isolation that exists"* is overstated: 21 non-test service files
  also filter on `tenant_id` at the application layer.
- **N-1286-5** — RLS-plan `:57`'s third bullet still reasons from per-tenant DBs, unmarked.
- **N-1286-6** — *"**The** deliberate exception"* omits 039 §3's `secuura_auth_lookup` path.

Each is a real correction and each would widen this round past what was authorised.

### Test Evidence
Docs-only: **no code, no migration, no config, no test**. Diff is **22 changed lines** across the two
documents. Base this worktree CONTAINS `00de57baeb40`; no merge-in.
Push gate `28/0 · 6/0 · 49/0 · 60 passed, 0 failed, 0 skipped (of 60)`; preflight **12/15 legs ran,
3 SKIPPED (3, 4, 8 — no local stack), nothing failed** — not quoted as a pass.
Re-swept after editing: **no surviving claim that both flags are unset**.

Refs KS-1336


## SEAT RECORD /Volumes/DevMASTER/!CODING/Secuura/Blockchain/5_Project_History/2026-09-26_seatB-31st/raise/b31-1341a-ticketcomment.final.md TEXT_SHA256 3e00dc05679d5d581b552c1ed3178bf8a5f86270f5567f6f8404912162c2e3f3

**Part A raised at PR [#1288](https://github.com/Secuura/Distributed_Secuura/pull/1288)** — head `cb58d3a59c8921a3a1caede3c6acfb4b599bf959`, base `develop` `e080174c86c671349c508560744644fc0ef33388`. **READY FOR QA.** Not merged; nothing merges without a signed GO naming the head. Facts only.

**What it ships.** The file's `fail500(res, context, err)` helper plus the first two of the seven sites — `GET /` and `POST /`. `message: err.message` in `routes/webhooks.ts` goes **7 → 5**; `fail500(` appears 3 times (1 declaration, 2 calls). **Parts B and C convert the remaining five and are not in this PR**, so this ticket stays In Progress after it merges.

**The defect is reproduced, not assumed.** With the new cell applied and the product hunks absent, the four red cells fail on their own assertions, and the `A1` pair fails with `"leaked": true` — the thrown text is in the 500 body at develop's tip, in every `NODE_ENV` the cell drives (production, development, test, unset). With the product hunks, 8 of 8 pass.

**Measured, in a worktree detached at the tip with `packages/shared` built:**

| check | result |
|---|---|
| red-first, cell alone | 4 failed / 4 passed / 8 total — all four controls green |
| green, both files | 8 / 8 |
| originate BARE at the tip | 80 suites, **943** tests, 0 failed |
| originate PATCHED at this head | 81 suites, **951** tests, 0 failed — 0 new reds |
| `tsc --noEmit`, and a run whose program **includes** the new cell | rc 0, 0 errors |
| `packages/shared` (`vitest run`) | 48 files, 945 tests, 0 failed |
| `npm run lint` at the tip / at this head | rc 0 both — 22 problems (0 errors, 22 warnings) at each; `webhooks.ts` and the new cell mentioned 0× at both |

**Two zeros were controlled rather than asserted.** `eslint src` covers 137 files, 86 under `__tests__`, and the new cell is in that set — a planted `debugger` and unused variable make it report 1 error and 1 warning, and the file was restored with the restore verified by sha256. Separately, the service's own `tsconfig.json` **excludes `src/__tests__`**, so a bare `tsc --noEmit` rc 0 covers 626 files and zero test files; the rc 0 quoted above is from a config that extends it with `exclude: []`, with `--listFilesOnly` showing the cell present and 86 test files in the program.

**The `GET /` swallowing branch.** `GET /`'s list query carries `.catch(... return [])`, so a rejected `$queryRaw` becomes a 200 with an empty list and never reaches the catch under test. The cell throws **synchronously** for that route, and `control KS-1341 A0` pins the swallow so it cannot return silently. Measured separately: no catch block in this file tests error text at all, so no fixture string can be diverted down a benign branch here.

**Provenance.** The patch was produced by the local model (`spark-dsv4flash`) under a Wednesday brief and re-verified by this seat before raising: diff sha256 `65720c1d4caa05f503f4d331cd3b4588b9d60b09b94647f8e3c8c4ab6ca9d67b`, `cmp` rc 0 against both the reviewed golden and the run's canonical patch, and a strict `git apply --check` per section at the tip (control: with `export default webhooksRouter;` tampered, the same apply fails 1 of 3 hunks).

🔴 **One comment in the diff is wrong at this PR, and it is raised that way on purpose.** The helper's docblock opens *"the only place in this router that turns a caught error into a 500"*. **That is false until parts B and C land** — five `err.message` lines survive part A. It is stated in the PR body and under NOT COVERED rather than edited, because the diff is byte-identical to the reviewed output and that provenance is worth more than a comment parts B and C will make true. The same docblock's *"Declared at the END of the file"* was checked and is accurate.

**Not covered:** the other five sites in this file; whether any further file in this family remains unswept (this ticket says that was not swept); the local stack is not up, so nothing integration-level ran, and nothing was deployed.


## SEAT RECORD /Volumes/DevMASTER/!CODING/Secuura/Blockchain/5_Project_History/2026-09-26_seatB-31st/raise/b31-1341a-RED.out TEXT_SHA256 a27dd19aa37576d64665af30d05e751f536a00ba1b5b306035b1876ccfac8d91

FAIL src/__tests__/ks1341a-webhooks-500-never-answers-err-message.test.ts
  KS-1341 part A: GET / and POST / never answer a 500 with the thrown text
    ✕ RED KS-1341 A1 GET /: the thrown message is not in the 500 body under production, development, test or unset (15 ms)
    ✕ RED KS-1341 A1 POST /: the thrown message is not in the 500 body under production, development, test or unset (16 ms)
    ✕ RED KS-1341 A2 GET /: the thrown message is logged once, server-side, with this route named (1 ms)
    ✕ RED KS-1341 A2 POST /: the thrown message is logged once, server-side, with this route named (2 ms)
    ✓ control KS-1341 A0: a REJECTED list query is still swallowed into a 200 and never reaches the catch (1 ms)
    ✓ control KS-1341 A: a create that does NOT throw answers 201 and logs nothing (1 ms)
    ✓ control KS-1341 A: an authored 400 keeps its own text and logs nothing (1 ms)
    ✓ control KS-1341 A: the LEAK string is the thrown text and dodges every benign branch

  ● KS-1341 part A: GET / and POST / never answer a 500 with the thrown text › RED KS-1341 A1 GET /: the thrown message is not in the 500 body under production, development, test or unset

    expect(received).toEqual(expected) // deep equality

    - Expected  - 1
    + Received  + 1

      Object {
    -   "leaked": false,
    +   "leaked": true,
        "nodeEnv": "production",
        "status": 500,
      }

      112 |     for (const nodeEnv of NODE_ENVS) {
      113 |       const reply = await call(route, nodeEnv);
    > 114 |       expect({ nodeEnv, status: reply.status, leaked: reply.text.includes(LEAK) }).toEqual({ nodeEnv, status: 500, leaked: false });
          |                                                                                    ^
      115 |       expect(JSON.parse(reply.text)).toEqual(CONSTANT_BODY);
      116 |       // REACHED, not merely clean: only fail500 logs this route's context with the thrown text.
      117 |       expect(mockLoggerError.mock.calls.at(-1)).toEqual([route.context, { error: LEAK }]);

      at src/__tests__/ks1341a-webhooks-500-never-answers-err-message.test.ts:114:84

  ● KS-1341 part A: GET / and POST / never answer a 500 with the thrown text › RED KS-1341 A1 POST /: the thrown message is not in the 500 body under production, development, test or unset

    expect(received).toEqual(expected) // deep equality

    - Expected  - 1
    + Received  + 1

      Object {
    -   "leaked": false,
    +   "leaked": true,
        "nodeEnv": "production",
        "status": 500,
      }

      112 |     for (const nodeEnv of NODE_ENVS) {
      113 |       const reply = await call(route, nodeEnv);
    > 114 |       expect({ nodeEnv, status: reply.status, leaked: reply.text.includes(LEAK) }).toEqual({ nodeEnv, status: 500, leaked: false });
          |                                                                                    ^
      115 |       expect(JSON.parse(reply.text)).toEqual(CONSTANT_BODY);
      116 |       // REACHED, not merely clean: only fail500 logs this route's context with the thrown text.
      117 |       expect(mockLoggerError.mock.calls.at(-1)).toEqual([route.context, { error: LEAK }]);

      at src/__tests__/ks1341a-webhooks-500-never-answers-err-message.test.ts:114:84

  ● KS-1341 part A: GET / and POST / never answer a 500 with the thrown text › RED KS-1341 A2 GET /: the thrown message is logged once, server-side, with this route named

    expect(received).toEqual(expected) // deep equality

    - Expected  - 8
    + Received  + 1

    - Array [
    -   Array [
    -     "Webhook list failed (GET /api/webhooks)",
    -     Object {
    -       "error": "connect ECONNREFUSED 10.0.4.17:5432 ks1341a-private-detail",
    -     },
    -   ],
    - ]
    + Array []

      122 |     const reply = await call(route, 'production');
      123 |     expect(reply.status).toBe(500);
    > 124 |     expect(mockLoggerError.mock.calls).toEqual([[route.context, { error: LEAK }]]);
          |                                        ^
      125 |   });
      126 |
      127 |   it('control KS-1341 A0: a REJECTED list query is still swallowed into a 200 and never reaches the catch', async () => {

      at src/__tests__/ks1341a-webhooks-500-never-answers-err-message.test.ts:124:40

  ● KS-1341 part A: GET / and POST / never answer a 500 with the thrown text › RED KS-1341 A2 POST /: the thrown message is logged once, server-side, with this route named

    expect(received).toEqual(expected) // deep equality

    - Expected  - 8
    + Received  + 1

    - Array [
    -   Array [
    -     "Webhook create failed (POST /api/webhooks)",
    -     Object {
    -       "error": "connect ECONNREFUSED 10.0.4.17:5432 ks1341a-private-detail",
    -     },
    -   ],
    - ]
    + Array []

      122 |     const reply = await call(route, 'production');
      123 |     expect(reply.status).toBe(500);
    > 124 |     expect(mockLoggerError.mock.calls).toEqual([[route.context, { error: LEAK }]]);
          |                                        ^
      125 |   });
      126 |
      127 |   it('control KS-1341 A0: a REJECTED list query is still swallowed into a 200 and never reaches the catch', async () => {

      at src/__tests__/ks1341a-webhooks-500-never-answers-err-message.test.ts:124:40

Test Suites: 1 failed, 1 total
Tests:       4 failed, 4 passed, 8 total
Snapshots:   0 total
Time:        3.272 s
Ran all test suites matching /src\/__tests__\/ks1341a-webhooks-500-never-answers-err-message.test.ts/i.


## SEAT RECORD /Volumes/DevMASTER/!CODING/Secuura/Blockchain/5_Project_History/2026-09-26_seatB-31st/raise/b31-1341a-GREEN.out TEXT_SHA256 8bddeba33742e6635f04889f3830a107c1b4c6c3dd2039f55a6f699d4b317519

PASS src/__tests__/ks1341a-webhooks-500-never-answers-err-message.test.ts
  KS-1341 part A: GET / and POST / never answer a 500 with the thrown text
    ✓ RED KS-1341 A1 GET /: the thrown message is not in the 500 body under production, development, test or unset (23 ms)
    ✓ RED KS-1341 A1 POST /: the thrown message is not in the 500 body under production, development, test or unset (25 ms)
    ✓ RED KS-1341 A2 GET /: the thrown message is logged once, server-side, with this route named (1 ms)
    ✓ RED KS-1341 A2 POST /: the thrown message is logged once, server-side, with this route named (1 ms)
    ✓ control KS-1341 A0: a REJECTED list query is still swallowed into a 200 and never reaches the catch (1 ms)
    ✓ control KS-1341 A: a create that does NOT throw answers 201 and logs nothing
    ✓ control KS-1341 A: an authored 400 keeps its own text and logs nothing (1 ms)
    ✓ control KS-1341 A: the LEAK string is the thrown text and dodges every benign branch

Test Suites: 1 passed, 1 total
Tests:       8 passed, 8 total
Snapshots:   0 total
Time:        3.953 s, estimated 4 s
Ran all test suites matching /src\/__tests__\/ks1341a-webhooks-500-never-answers-err-message.test.ts/i.


## SEAT RECORD /Volumes/DevMASTER/!CODING/Secuura/Blockchain/5_Project_History/2026-09-26_seatB-31st/raise/b31-1318-correction-comment.final.md TEXT_SHA256 49708552eed4d77d0db53f28d35f3d37e3942b901af2bad7a3f4b36f65268e95

**Correction to the comment of 2026-09-26 02:59 on this ticket, and this ticket's work is now raised on its own at PR [#1289](https://github.com/Secuura/Distributed_Secuura/pull/1289)** — head `1e24633b9c196c5d3dd5bb83519bce860ca79758`, base `develop` `e080174c86c671349c508560744644fc0ef33388`. **READY FOR QA.** Not merged. Facts only.

**The correction.** That comment says this ticket was *"re-raised on its own at #1287"*. It was not. **#1287 carried `entrypoint-corpus.test.ts` alone** — KS1142's file — and the gate corrected #1287's squash to name KS1142 alone, which was right. **Nothing of KS-1318 has merged.** On develop the combined cell still reads `toHaveLength(3)`.

**Where the work actually lived, and why a new PR.** This ticket's change is **one hunk** in `packages/shared/src/__tests__/ks781-p3-3-body-parser-order.test.ts`. That hunk was first raised inside **#1268**, which carries this hunk *and* KS1316's two hunks and failed at the two-NO-GO cap on KS1316's guard-reachability rule — so #1268 ships nothing and stays open (closing it is not this seat's call, and this seat pushed nothing to it). #1287 deliberately excluded the ks781 file. Raising this hunk alone keeps it from being lost with either vehicle.

**The hunk, measured rather than quoted.** `git diff e080174c86c6 5ac42fafeee1` on that file gives **3 hunks**; hunks 1 and 2 are KS1316's and are **not** in this PR. This PR is hunk 3 alone, renumbered into develop's line space: **+10 / −1, one file.** The file's blob is `e96215365a6d` at both #1268's merge base and develop, so the pre-image is unchanged. Containment was checked with a control: a KS1316-only token (`W9`) appears **0×** in this PR's diff and **7×** in the full three-hunk diff.

**What it changes.** The combined control cell asserts the **set of tags in source order** instead of their count:

    -    expect(defaultShapesOf(src)).toHaveLength(3);
    +    expect(defaultShapesOf(src)).toEqual([
    +      'export default function',
    +      'export default <Identifier>',
    +      'export { x as default }',
    +    ]);

**Red-proved, and the red set asserted exactly.** Two arms, each run at **both** trees, each with its red set asserted **exactly** — not "contains". Every tamper's anchor was proven unique (`count == 1`) before the edit, restored by content, and the restore verified by a sha256 of the whole file.

| arm | at develop (`toHaveLength(3)`) | at this head (`toEqual([…])`) |
|---|---|---|
| **A — permutation.** `return shapes;` → `return shapes.reverse();` | **0 red — the file stays 242/242 green.** This is the blindness this ticket names. | **1 red: the combined cell ALONE.** The three per-shape rows stay green (each is fed one shape, so reversing a one-element array changes nothing). |
| **B — relabel, cardinality preserved.** The default-function branch and the alias branch swap their `shapes.push` labels | **2 red: the two per-shape rows only. The combined cell stays GREEN.** This is the ticket's own sentence — *"it would pass if two shapes were detected under one another's name."* | **3 red: the two rows AND the combined cell.** |

Arm A proves the new assertion is **necessary** (it catches what the old one cannot). Arm B proves it is **not over-firing** (the per-shape rows behave identically at both trees; only the combined cell changes behaviour). Both arms matched their predicted red set exactly, 2/2 at each tree — predictions were written before the runs and are recorded, not fitted afterwards.

**Suites, with the environment named** — worktree detached at develop `e080174c86c6` which it contains, `npm ci` at `Blockchain/Dev`, `packages/shared` **BUILT** (28 files in `dist/`):

- `ks781-p3-3-body-parser-order.test.ts`: **242 passed** at both trees (this change edits an assertion inside an existing cell, so the cell count does not move).
- whole `packages/shared` (`vitest run`): **48 files, 945 tests, 0 failed** — bare **945**, patched **945**.
- `tsc -p packages/shared --noEmit`: **rc 0, 0 errors at both trees**; the two outputs differ only in the worktree path, which is what shows the comparison ran on two different trees.
- `npm run lint -w packages/shared`: **rc 1 at both trees, 36 problems (1 error, 35 warnings), byte-identical after normalising the worktree path.** The one error is pre-existing and already on the backlog — `no-control-regex` on the KS703 control-byte guard in `src/middleware/index.ts:539`. This change is lint-neutral; `ks781` is not mentioned in either run.

**Not covered:** KS1316's two hunks (not in this PR, and #1268 is not touched by this seat — no push to it, no close); `#1268`'s disposition; the local stack is not up, so nothing integration-level ran and nothing was deployed.

Refs KS-1318


## SEAT RECORD /Volumes/DevMASTER/!CODING/Secuura/Blockchain/5_Project_History/2026-09-26_seatB-31st/raise/b31-1318-arms-TIP.out TEXT_SHA256 6a177ad622ead828cbfc439ed6a2d8467a3d507bee00f488c64cdf4448be1d68

=== TIP: file sha256 29749418e558a33b… ===
    TIP-base: 242 cells, 0 red, rc=0
  baseline red set: []
  --- TIP-reverse: anchor occurs 1x  ('return shapes;')
    TIP-reverse: 242 cells, 0 red, rc=0
    restore VERIFIED byte-identical (sha256 29749418e558a33b…)
    PREDICTED 0 red, GOT 0 — set matches EXACTLY
  --- TIP-relabel: anchor occurs 1x  ("shapes.push('export default function');")
  --- TIP-relabel: anchor occurs 1x  ("shapes.push('export { x as default }');")
    TIP-relabel: 242 cells, 2 red, rc=1
    restore VERIFIED byte-identical (sha256 29749418e558a33b…)
    PREDICTED 2 red, GOT 2 — set matches EXACTLY
       RED : defaultShapesOf SEES 'export default function'
       RED : defaultShapesOf SEES 'export { x as default }'
=== TIP: 2/2 arms matched their prediction exactly; file sha256 29749418e558a33b… ===


## SEAT RECORD /Volumes/DevMASTER/!CODING/Secuura/Blockchain/5_Project_History/2026-09-26_seatB-31st/raise/b31-1318-arms-HEAD.out TEXT_SHA256 ab0ed5683e1a2cecb606b9634566ec5631816e158f19724231acf7c18ae0f7cb

=== HEAD: file sha256 2f30226d50bc1a6d… ===
    HEAD-base: 242 cells, 0 red, rc=0
  baseline red set: []
  --- HEAD-reverse: anchor occurs 1x  ('return shapes;')
    HEAD-reverse: 242 cells, 1 red, rc=1
    restore VERIFIED byte-identical (sha256 2f30226d50bc1a6d…)
    PREDICTED 1 red, GOT 1 — set matches EXACTLY
       RED : all three shapes at once, and the object-literal default is still ignored
  --- HEAD-relabel: anchor occurs 1x  ("shapes.push('export default function');")
  --- HEAD-relabel: anchor occurs 1x  ("shapes.push('export { x as default }');")
    HEAD-relabel: 242 cells, 3 red, rc=1
    restore VERIFIED byte-identical (sha256 2f30226d50bc1a6d…)
    PREDICTED 3 red, GOT 3 — set matches EXACTLY
       RED : all three shapes at once, and the object-literal default is still ignored
       RED : defaultShapesOf SEES 'export default function'
       RED : defaultShapesOf SEES 'export { x as default }'
=== HEAD: 2/2 arms matched their prediction exactly; file sha256 2f30226d50bc1a6d… ===


