# Gate verdict: Secuura Platform K pull request 1541 (KS-1584), OPUS tier 1

Report sha256/16: 3df0f1ae2c007542
(Recipe: sha256 of this file with the single "Report sha256/16:" line deleted, first 16 hex characters.)

- **Head under test:** `7d9cad92afa7e9d1be2e2a03515afd5754538d0d` (my own fetch of `refs/pull/1541/head`; `git ls-remote` again at 2026-10-13T03:53:07Z still returned it).
- **Base:** develop `a7cffc8d9831e67d91f6dd24d0047ffe3e26c97e` (still the live develop tip at 03:53:07Z).
- **Gate:** independent QA, findings only. Clone `--shared` in my scratchpad, push URL `DISABLED`. My own PostgreSQL 15.14 on 127.0.0.1:55413, now stopped. Nothing was written inside `!CODING`. I ran no git write verb in the project, pushed nothing, wrote nothing to GitHub or Linear, and touched no remote box.

## VERDICT: GO WITH NOTE

**The note blocks the deploy round, not this merge.**

The diff does what it says at the two routes it changes. On my stack, every number the author gave reproduced. The register-connector refusal, which the author named as the biggest gap, is now **observed over real HTTP** through the real gateway app and the real security service. It refuses identically in status, body and timing, and 13 bypass spellings could not get past it.

**But the two-hop escape is NOT closed for the round.** There is a second hop-1 that this PR does not touch: originate's `POST /api/admin/api-keys`, which is reachable through the gateway. An `ORG_ADMIN` can still mint an `organizations:register` key there with no organisation, a whitespace organisation or a **foreign** organisation. On **this head**, that key then mints `{organizationId: A2, connectorId: conn_of_A2}`, and I measured **201**. The row is stored with `organization_id=A2` and `connector_id=conn_of_A2`. That is M1's erasure shape exactly (finding **M1** below). It was there before this PR and lies outside the diff, but it defeats KS-1584's stated purpose.

Wednesday chooses how to close it: fold the fix into this PR, or open a sibling ticket in the same round. Either way, the round (PR A + KS-1564 + PR B + KS-1584) must not deploy until it is closed. Do not recommend deploying.

| ID | Severity | One line |
|---|---|---|
| **M1** | **Major** (pre-existing, outside the diff, deploy-blocking for KS-1584's purpose) | originate `POST /api/admin/api-keys` is a second hop-1 with no provisioning rule. An ORG_ADMIN gets an UNBOUNDED or foreign-organisation provisioning key, and hop 2 then mints into A2 with A2's connector: **201 on head** |
| m1 | Minor | The PR body's R2 deploy census counts only `organization_id IS NULL`. Keys with `''` or whitespace in that column are also unbounded and the census misses them. Measured: 1 of 3 unbounded rows found |
| m2 | Minor (test) | The shared truth-table "case-insensitive" cell is vacuous: `OWN` has no hex letters, so `.toUpperCase()` changes nothing. Mutant G11 survives every behaviour cell |
| m3 | Minor (test) | Whitespace-organisation paths are pinned only by my cells: mutants G8 (hop-1 reads the org raw) and G3 (connectorId check reads it raw) survive all of the author's cells |
| n1 | Nit | The ks1215 comment cites `ks1584-register-connector-organisation-bound.test.ts`. No such file exists |
| n2 | Nit | `isProvisioningCapable` throws on a non-array `scopes` claim (develop's `hasScope` returned a value). It fails closed and the `sk_` path cannot reach it |

---

## FOUND / TESTED / HOW

### Item 1: the author's 14 cells and the 1535 gate's M1 cell, three runs per tree

Instrument: vitest `vitest.integration.config.ts`, the service connecting as `secuura_app` (rolsuper f, rolbypassrls f), FORCE RLS on `svc_api_keys`, `organizations` and `admin_organisation_scopes` (`results/pg_roles.txt`). Migrations: `applied=51 failed=0`, with an explicit `Applying 049_admin_organisation_scopes.sql` line (`results/pgsetup_head.txt`).

| Tree | Author `ks1584-provisioning-key-organisation-bound.integration.test.ts` (14) | 1535 gate `gate1535-d-twohop` (3 arms) | Runs |
|---|---|---|---|
| head | **14/14 pass** | arm 1 (UNSCOPED ADMIN) **fails at hop 1 with 403**, which inverts its `expect(201)` (the ruled default deny). Arms 2 and 3 **pass**: hop 2 = 403, no row stored | 3/3 identical |
| develop | **7 fail / 7 pass**. The 7 passes are the controls | **all 3 arms fail**: hop 2 = **201**, row stored `organization_id=A2`, `connector_id=conn_of_A2` (`runs/gateD_ledger_dev_1.json`) | 3/3 identical |

- **Control that each harness can fail:** the develop column itself, where the same files go red on the tree without the fix.
- **On the author's numbers:** they said 6 of 13 failed red-first. I measured 7 of 14 failed on develop. The extra cell is the case cell, added after the red-first run; it fails on develop as well, so the two counts agree.
- **Cells named:** the 7 red on develop are the three `RED:` hop-1 cells, the two `RED: … may NOT mint for A2` cells, `the bound folds CASE`, and `RED: a BOUNDED provisioner may not name a connectorId`. Files are under `results/runs/cells_{head,dev}_{1,2,3}.txt`.
- **Both tenancy modes.** I also ran with `MULTI_TENANCY_ENABLED=true` and `PLATFORM_DATABASE_URL` set: head 64/64, develop 57/64 (the same 7 reds).
- **The "falling back to single-tenant" grep is meaningless for security.** That string exists only in `services/originate/src/db.ts:371`. The security logs had 0 `TenantPoolManager` lines in both modes, so security starts no tenant manager. The control that the grep can find such lines: the originate run logged 9 of them.

### Item 2: the escape over the real mint route, every principal (`gatetests/gate1541-matrix.integration.test.ts`)

I wrote the expected status for head AND develop into the file before running. There are 40 hop-1 cells, 9 hop-2 chains (32 requests), and 4 hop-2 requests that use originate-minted keys. The full ledger is in `results/runs/matrix*_ledger_*.json`.

- **Head:** 50/50 cells matched in 3 of 3 runs.
- **Develop:** 50/50 matched its own develop column in 3 of 3 runs.
- **Control:** running head's expectations against develop fails (`runs/matrix_CONTROL_headexp_on_dev.txt`).

Hop-1 findings (head / develop):

- **Refused on head, 201 on develop:** every unqualified provisioning-capable mint by a non-platform caller. That covers `ADMIN{A1}`, `ADMIN{A1,A2}`, `ADMIN{}`, lowercase `admin`, `ISSUER_ADMIN(A1)`, `ORG_ADMIN(A1)` and `ORG_ADMIN(no org)` with no organisation, plus `''`, `'   '`, and the scope sets `[*]` and `[organizations:*]`.
- **Unchanged (403 on both trees):** naming an organisation outside the caller's bound. That covers `{A1}` naming A2, `{A1}`, `not-a-uuid`, `ADMIN{}` naming A1, and `ORG_ADMIN(no org)` naming A1.
- **Spellings of the caller's own organisation, allowed and stored normalised:** `A1-UPPER`, padded, and NBSP-prefixed (JS `trim` strips NBSP).
- **201 on both trees:** platform roles (`SYSTEM_ADMIN`, `super_admin`) with no organisation, and `ORGANIZATIONS:REGISTER` (upper case is not provisioning-capable anywhere; see the table in item 4).
- **403 on both trees:** connector callers (`register` bounded, `register` org-less, `*`, `organizations:*`), refused at admission.

Hop-2 findings (head / develop):

- **A1-bounded key** (minted by ADMIN{A1}, ISSUER_ADMIN, ORG_ADMIN, by SYSTEM_ADMIN naming A1, or minted from an upper-case A1):
  - Refused on head, 201 on develop: A2, A3 (a sibling), `{A1}`, `not-a-uuid`, `A2-UPPER`, A1 with a connectorId, no organisation with a connectorId.
  - Allowed on both trees: A1, A1-UPPER, padded A1, and no organisation (a tenant-level key).
  - 403 on both trees: other tenant, rotate, and the provisioning scope itself.
- **A2 key** minted by ADMIN{A1,A2}: refused for A1 on head.
- **A `[organizations:register, *]` key:** bounded on head.
- **An `organizations:*`-only key:** 403 on both trees (admission).
- **Org-less SYSTEM_ADMIN key:** A2 with a connectorId gives 201 on both trees (the ruled, unbounded Platform S path); rotate gives 403 on both.

### Item 3: legacy and platform-minted keys

- **What an org-less provisioning key can still do after this PR** (measured): mint into any organisation of its tenant, **with any connectorId**, and register-connector can create new organisations and re-register any of them (live R8 and R9). That is the ruled behaviour (R2).
- **Can a tenant admin still CREATE one? At security, no.** Hop-1 refuses it, and security has no update route: `PATCH` and `PUT` on `/api/keys` do not exist (`index.ts` route list). Rotation is refused for every connector caller.
- **But yes, through originate. That is M1.**
- **A platform-minted BOUNDED key** (SYSTEM_ADMIN naming A1) is bounded like any other: A2 gives 403, a connectorId gives 403.
- **Can a bounded key rotate into another organisation? No.** `A1 + connectorId + rotate` gives 403 on head; the refusal comes from the bounded-connectorId check, before the rotate check.
- **PR B interplay** (code read): removing an organisation from an admin's scope does not disable a key already minted for it. That is ruled and stated in the PR body.

### Item 4: the HOP-1 default deny, legitimate callers, and the predicate

**Which scope sets count as provisioning-capable.** I built this table from the compiled source (`tools/pred_table.js`, output in `results/predicate_table.txt`). A scope set is provisioning-capable exactly when it contains **`organizations:register`, `organizations:*` or `*`**, whatever else it holds. These are NOT provisioning-capable: `ORGANIZATIONS:REGISTER`, `organizations:Register`, padded variants, `*:*`, `*:register`, `organizations:`, `[]`, `[null]`. For every array input, head's `isProvisioningCapable` gives the same answer as develop's gateway gate (`hasScope`) on all 24 rows. The one difference is a non-array string (n2).

**Callers of POST /api/keys** (git grep across services, scripts, docs, e2e, systemTest and frontend):
- Admin UI `frontend/admin/src/pages/ApiKeys.tsx:177-181` (KS-1564) mints `['read','write']` and names `dialogOrgId`. Not provisioning-capable, so untouched.
- `tenant-provisioning/src/meteringKey.ts:45-55` mints `metering:read`. Untouched.
- register-connector's own mint names `organizationId` with the §8 scopes. Untouched.
- e2e and systemTest mint through originate `/api/admin/api-keys` with `['read']`. Untouched.
- No caller in the repo mints an unqualified provisioning-capable key. The only real one is the Platform S instance key, minted by hand (`Notes (MASTER)/daily/2026-07-30.md:47`) and, per that note, by a platform role.

**Who the deny now refuses:** any tenant admin minting an unqualified `organizations:register`, `organizations:*` or `*` key. An `ORG_ADMIN` with no organisation claim (KS-779's population) can no longer mint any provisioning key at security. **I found no legitimate caller this breaks.**

**On the narrowing of point (b):** I judge it sound and in the safe direction. The shared predicate governs the gateway's admission, the register-connector bound, the hop-1 deny, the hop-2 bound and the bounded-connectorId check. `decideMint`'s admission and the connectorId exemption at `index.ts:1254` stay literal.
- **Consequence 1:** mutant G1 (the hop-2 arm on the literal scope) is **equivalent**, because a wildcard-only connector can never reach `decideTenantAccess` at the mint (it is refused at admission). Measured: G1 survives every cell, mine included.
- **Consequence 2, the residual asymmetry, which is a code read and was there before this PR:** an org-less `*` or `organizations:*` key is admitted at register-connector. It INSERTs the organisation, then its mint is refused by security admission, so the call returns 502 and leaves an orphan organisation row. After this PR only platform-minted or legacy keys can have that shape.

### Items 5 and 3: register-connector over REAL HTTP (`gatetests/gate1541-register-live.test.ts`)

**Set-up:**
- The real gateway app (`index.ts`, **no db mock**), using `secuura_app` on my Postgres.
- The real security service of the same tree in a child process (`gatetests/gate1541-secserver.ts`). Keys were really minted and validated there.
- The **only stand-in** is the HTTP wrapper of auth's `/internal/connector-token`. It validates the key at the real security service and signs exactly the claims of `generateConnectorToken` (`services/auth/src/services/jwt.ts:281-297`).
- Expectations for head and develop were written before the run.

**Results:** head 25/25 and develop 25/25 in 3 of 3 runs each. Control: running head's expectations against develop gives **18 failed** (`runs/live_CONTROL_headexp_on_dev.txt`).

| Cell | Head | Develop |
|---|---|---|
| R1 bounded A1 key, own externalRef | 200, alreadyRegistered, organisation = A1 | 200 |
| R2 bounded A1 key, A2's externalRef (same tenant) | **403** | **200, returns A2's organizationId** |
| R3 bounded A1 key, another tenant's externalRef | **403** | 404 |
| R4 bounded A1 key, unknown externalRef | **403, no organisation created** | **201, organisation created and key minted** |
| R5 the three refusals, byte for byte | **1 distinct (status + body identical)** | more than 1 distinct |
| R6 bounded key renames A2 | **403, name unchanged** | **200, renamed to "PWNED by g1541"** |
| R7 `*` key bound to A1, A2's externalRef | **403** | 200 |
| R8 CONTROL org-less key creates a new organisation | 201 + key | 201 + key |
| R9 CONTROL org-less key re-registers A2 | 200 | 200 |
| R10 CONTROL non-provisioning key | 403 (requireOrgProvisioner) | 403 |

**Timing**, from 40 samples each of the sibling, other-tenant and unknown refusals:
- Head medians differ by at most 0.03 ms across 3 runs: run 1 at 1.195, 1.190 and 1.196 ms; run 3 at 1.353, 1.340 and 1.349 ms.
- **The instrument can resolve the difference:** on develop it separates "unknown" at 3.66 to 3.94 ms from the 1.36 to 1.43 ms of the other two, in all 3 runs.

**Bypass attempts with the bounded key on A2:** every one returned 403 with the bound's message, or 405 or 404, and none contained A2's id.
- Spellings tried: trailing slash, upper-case path, `/api/v1` and `/API/V1` aliases, a double slash, a padded externalRef.
- Headers and body tried: `x-organization-id` set to A2 or empty, body `organizationId: A2`, `X-HTTP-Method-Override: PUT`, `?_method=PUT`.
- Method: `PUT` returned 405.
- `tenantSlug` returned 404 earlier, at the slug lookup.
- I found no second route that registers organisations for a connector. originate's `/api/admin/organizations` requires SYSTEM_ADMIN or ORG_ADMIN, and a connector is refused there.

### Item 6: the shared policy at its source, every caller

**Callers** (git grep, tests excluded):
- `decideTenantAccess`: security mint `index.ts:1213`; `decideKeyRevoke`, which security revoke `:1482`, originate adminConfig revoke `:1057` and the erasure (`connectorOrganisationErasure.ts:333`) all call.
- `isProvisioningCapable`: `keyRevokePolicy.ts:298`, `:374`; gateway `platform.ts:107`; security `index.ts:1192`, `:1279`.
- `decideProvisionerRegistration`: `platform.ts:657`.
- `decideMint`: `index.ts:1088`.

**The erasure is unaffected.** It passes `{role:'connector', tenantId, organizationId}` with **no scopes**, so `isProvisioningCapable(undefined)` is false and the new arm does not engage (code read). No caller is left on an old signature: `scopes` is optional, and tsc gives 0 on all three packages.

**The 8 `normaliseOrgId(` sites the ks780 count pins**, all in `keyRevokePolicy.ts`:

| Lines | Arm | What is normalised |
|---|---|---|
| :199, :200 | organisation arm | target, caller |
| :261, :269 | ADMIN arm | target, each scope entry |
| :299, :303 | provisioner arm | target, caller claim |
| :373, :378 | registration | own organisation, existing organisation |

**The write and read sides agree.**
- **Write:** security normalises at mint (`index.ts:1313`). The gateway compares `organizations.id`, which is canonical lower-case uuid text. Both sides use one function, so case, padding and NBSP agree (measured: A1-UPPER, padded A1 and NBSP all store and compare as A1).
- **Exception, one writer:** originate (M1) stores `organization_id` **raw**. That is how `'   '` reaches the table.

### Item 7: the four moved tests

- **ks1533 retargets: honest.**
  - Mutant **T1** (provisioner rotate refusal removed) reddens all three retargeted `RED (M1): a PROVISIONER rotating…` cells.
  - Mutant **T2** (unbounded-provisioner connectorId exemption removed) reddens the retargeted `CONTROL: an UNBOUNDED PROVISIONER may choose a connectorId`.
  - Each cell still pins the guard it was written for.
- **ks1215 stub: honest, and the change was necessary.**
  - Running **develop's** ks1215 file (whose stub has organisation `org-ks1215`) against head code gives **4 failed / 37 passed**. All four failures are register-connector cells. They went red, not vacuously green.
  - With head's org-less stub, mutant **T3** (the connector branch keeps the caller's Bearer) reddens the two register-connector cells that assert no caller Bearer is forwarded (`🔴 … REVOKED session's JWT…` and `RED … exchange REFUSED…`), plus 10 other ks1215 cells. The other two register-connector cells are controls, where the exchange succeeds and overwrites the header.
- **ks780 = 8: correct.** Mutant **T4** (a ninth call) reddens S2.
- **"Platform S's real instance key is ORG-LESS".** This is confirmed by function, not by the live row:
  - `docs/S-K-OWNERSHIP-CONTRACT.md:100-108`: one provisioning key per **S instance**, `organizations:register` only, which "registers an Organisation + receives that org's key". Creating a new organisation is impossible for a bounded key (live R4), so the key must be org-less to work at all.
  - The ks480 fixture (`ks480-org-provisioner-gate.test.ts:48`) and ks742's `PROVISIONER_A` (`ks742-keys-tenancy-route-contract.test.ts:86-89`) model it with no organisation.
  - `Notes (MASTER)/daily/2026-07-30.md:47` records the demo key `key_5ea91706-…` as "`organizations:register` only", but not its organisation.
  - **I did NOT read the live row.** If that key carries an `organization_id`, Platform S registration breaks at deploy. The R2 census must confirm the key is org-less (as fixed in m1).

### Item 8: mutants, by cell name (`tools/mutants.py`; `results/mutants_by_cell.txt`, `results/mutants_T_by_cell.txt`)

**How each mutant was run:**
- Each is a replacement of exactly one occurrence. It is INVALID unless its anchor appears exactly once.
- `packages/shared` is rebuilt after every shared mutation and after each restore.
- Bytes are restored and checked byte-identical (all 22 were).
- Baseline before the run: shared 58/58, security unit 42/42, security integration 64/64, gateway 95/95.
- Control: **M0, comment-only, reddens nothing.**

| Mutant | Result | Killing author cells (A) / gate cells (G) |
|---|---|---|
| M1 provisioner arm removed | KILLED | A3: `RED: ADMIN scoped {A1} …`, `RED: ISSUER_ADMIN …`, `the bound folds CASE`; G8 |
| M2 bound compared raw | KILLED | A2: ks780 S2, `the bound folds CASE` |
| M3 hop-1 deny removed | KILLED | A3: the three `RED:` hop-1 cells; G11 |
| M4 wildcards not capable | KILLED | A4 incl. ks480 `admits it via a resource wildcard`; G2 |
| M5 bounded key may name connectorId | KILLED | A2: ks1533 `KS-1584: a BOUNDED provisioner…`, `RED: a BOUNDED provisioner…`; G2 |
| M6 bounded key may create | KILLED | A2: truth-table `may NOT create`, `answers … IDENTICALLY`; G2 (live R4, R5) |
| M7 org-less key becomes bounded | KILLED | A5 incl. ks1533 CONTROL, ks742 F-8 CONTROL; G3 (live R8) |
| M8 org-less exemption ignored | KILLED | A6 incl. 4 ks1215 register-connector cells; G2 |
| G1 hop-2 arm on literal scope only | **SURVIVED (equivalent)** | none possible: admission is literal (item 4) |
| G2 bound against the tenant, not the key organisation | KILLED | A5; G5 |
| G3 connectorId boundedness read raw | KILLED | **A0**; G1 (`H2 originate keys`, the whitespace key) |
| G4 registration refusal reasons made distinct | KILLED | A1: `answers … IDENTICALLY` |
| G4b gateway answers 404 for would-create | KILLED | **A0**; G2 (live R4, R5). Only the HTTP probe catches this |
| G5 `organizations:*` dropped from the predicate | KILLED | A3; G1 |
| G7 hop-1 deny exempts ADMIN | KILLED | A3; G8 |
| G8 hop-1 reads the body organisation raw | KILLED | **A0**; G1 (`H1 ADMIN{A1} whitespace`) |
| G11 registration own-org compared case-sensitively | KILLED | **A1, structural only** (ks780 S2). The truth-table case cell stays green (m2) |
| T1 to T4 (item 7) | KILLED | as stated in item 7 |

**Tally:** I re-derived the author's 8 and all 8 die. My 9 kill 8; G1 is an equivalent survivor. The author's cells alone would leave **G3, G4b and G8** alive, and G11 is caught only structurally.

### Item 9: scope and hygiene

- **Diff against develop** (`results/scope.txt`): 10 files, +624 / -11, one commit. Migrations, docker and prisma: **0 diff lines**.
- **Spec:** `npm run check:openapi` gives rc 0, `CHECK PASS`, 414 example blocks OK (`suites/check_openapi_head.txt`). Control: a one-word edit to `docs/openapi/secuura-api.yaml` gives `CHECK FAIL`, rc 1. The file was restored byte-identical.
- **Merge-tree** (`results/mergetree.txt`):
  - With live develop: clean, tree `598fd914…`, matching the author's claim.
  - With PR 1539's head as the brief named it (`61c30de5`): clean, tree `845b1cdc…`.
  - **PR 1539's head has since moved to `fdf314e0`.** With that head: clean, tree `87e61f61…`.
  - Control: a synthetic develop commit editing the same `platform.ts` import line gives exit 1 with a conflict.
  - The only file both PRs touch is `services/security/src/index.ts` (in different regions).
- **Suites on head, all rc 0:** shared 52 files / 994 tests; security unit 31 / 337; security integration 5 / 74; api-gateway 118 / 1146. tsc gives 0 on all three packages (control: an injected TS2322 gives rc 2). eslint `--max-warnings=0` on the 5 changed source files gives rc 0 (control: a file with `var` and `debugger` gives 2 errors and 1 warning).
- **PR body against the code:** the body is accurate on the code and the numbers. Three things in it are wrong or open:
  - Its census under-counts (m1).
  - The ks1215 comment points at a file that does not exist (n1).
  - "Closes the two-hop escape" is true only for the security route; a reader would take it to mean every route (M1).
- **Linear:** I did not check the attachment's linkKind and wrote nothing (out of my read scope).

---

## Severities: file:line, how to reproduce, minimal fix

### M1, Major (pre-existing, outside the diff, deploy-blocking for KS-1584's purpose)

**Where:**
- `services/originate/src/routes/adminConfig.ts:924-983`, the `POST /api/admin/api-keys` handler. `:947` sets `orgId = body.organizationId || claim || null`, stored **raw**. `:948` passes caller-chosen `permissions` through unchecked.
- `:38` has `requireRole('SYSTEM_ADMIN','ORG_ADMIN')`.
- It is reachable through the gateway: `api-gateway/src/routes/proxy.ts:1227-1241` (`PROXY_ADMIN_ROLES` includes `ORG_ADMIN`).

**How it was measured:**
- The real `adminConfigRouter`, real `authenticate`, real `requireRole`, and the production tenant wiring copied from `originate/src/index.ts:218-258` (tenant resolver + `tenantGucContext()`).
- As `secuura_app` under FORCE RLS, in **both** tenancy modes (`gatetests/gate1541-originate-mint.integration.test.ts`; `runs/keys_orig_app_mt{false,true}.json`).
- Control: with `tenantGucContext` removed, the same INSERT returns 500 (RLS refuses it). So the 201s are real and are not an artefact of RLS being bypassed.

**What an ORG_ADMIN gets:**
- `ORG_ADMIN` with **no organisation claim** (KS-779's population), `{permissions:['organizations:register']}`: 201, `organization_id NULL`, which is **unbounded**.
- `ORG_ADMIN(A1)`, `{permissions:['organizations:register'], organizationId:'   '}`: 201, `organization_id '   '`, which is **unbounded** (`normaliseOrgId('   ')` is null).
- `ORG_ADMIN(A1)`, `{…, organizationId: A2}`: 201, a key bounded to **A2**, which is a foreign organisation.
- `ORG_ADMIN(A1)`, `{permissions:['*']}`: 201.
- Controls: ADMIN gives 403, ISSUER_ADMIN gives 403, no token gives 401.

**Hop 2 on HEAD security, using those keys** (`runs/matrixO_ledger_head_{1,2,3}.json`, 3 of 3 runs):
- The org-less key and the `'   '` key, minting `{organizationId:A2, connectorId:'conn_of_A2'}`: **201**, row stored with `organization_id=A2`, `connector_id=conn_of_A2`.
- The A2-bounded key: A2 gives 201, A1 gives 403.

Develop gives the same results, so this PR did not introduce it. But it is M1's exact shape (the KS-695 erasure trusts that row), and this PR's hop-1 deny was meant to make it impossible for a tenant admin.

**Minimal fix:** in originate's `POST /api-keys`:
- (a) Refuse any `permissions` set where `isProvisioningCapable(permissions)` holds unless `isPlatformRole(caller)`. For an ORG_ADMIN, provisioning keys are simply not mintable there; the security route is the place for them.
- (b) Store `normaliseOrgId(orgId)`, so `'   '` is stored as absent.
- (c) Optionally bound `body.organizationId` to the caller's own organisation for ORG_ADMIN. That is the same class of gap as the KS-1533 arm and needs its own ruling.

**Regression cells:** `gate1541-originate-mint.integration.test.ts` (cases o2, o3, o4 should become 403) plus the matrix `H2 originate keys` cell. The census (m1) must also run against keys originate has already written.

### m1, Minor

**Where:** the R2 census SQL in the PR body (`5_Project_History/2026-10-13_seatV-7th/logs/pr_ks1584_body.md`, section R2).

**Measured** (`results/census_sql.txt`, in a transaction that was rolled back): I seeded `NULL`, `''`, `'   '` and `A1` provisioning rows.
- Query 2 returns **1** row.
- Query 1 files `''` and `'   '` under `orgless = f`, which reads as bounded.
- The code treats **3** of the rows as unbounded.

**Fix:** use `(organization_id IS NULL OR organization_id ~ '^[[:space:] ]*$')` in both queries (JS `trim` also strips NBSP and other Unicode spaces, so prefer `normaliseOrgId` semantics if it is scripted).

### m2, Minor (test)

**Where:** `packages/shared/src/__tests__/ks1584-provisioner-registration-bound.test.ts:20,48-51`.

**Problem:** `OWN = '11111111-1111-4111-8111-111111111111'` contains no hex letters, so `OWN.toUpperCase() === OWN` and the "case-insensitive" cell tests nothing. Mutant G11 (own organisation compared case-sensitively at `keyRevokePolicy.ts:373`) leaves every behaviour cell green; only ks780's structural count catches it.

**Fix:** use a uuid with letters, as the integration file's `A1` does.

### m3, Minor (test)

**Problem:** whitespace organisations are pinned by no author cell.
- **G8:** `index.ts:1194` changed to `!data.organizationId` lets `organizationId:'   '` through hop 1. The ADMIN arm then treats it as unqualified, and an **org-less provisioning key is minted**.
- **G3:** `index.ts:1280` read raw.

My `H1 ADMIN{A1} whitespace` and `H2 originate keys` cells kill both.

**Fix:** add `''` and `'   '` cells at hop 1, and a whitespace-claim connector at the connectorId check.

### n1, Nit

**Where:** `services/api-gateway/src/__tests__/ks1215-the-connector-branch-never-carries-the-callers-bearer.test.ts:196`.

**Problem:** it names `ks1584-register-connector-organisation-bound.test.ts`, but the cell is in `packages/shared/src/__tests__/ks1584-provisioner-registration-bound.test.ts`. git ls-tree finds no file by the cited name.

### n2, Nit

**Where:** `packages/shared/src/security/scopes.ts:210-214`.

**Problem:** a truthy non-array `scopes` value throws (`scopes.filter is not a function`). Develop's `hasScope("organizations:register", …)` returned true through `String.includes`. It fails closed and the `sk_` path cannot reach it (scopes come from a JSONB array).

**Fix:** an `Array.isArray` guard.

**Observations (no severity, for Kam's awareness):**
- A **bounded** provisioning key can still mint **unqualified** (tenant-level) keys (`H2 K_A1 :: none` gives 201, and the author asserts it). That is consistent with the KS-779 ruling for admins, who can already mint such keys directly. For a *platform-minted* bounded key, though, it is reach beyond its one organisation.
- PR 1539's head moved during this gate (from `61c30de5` to `fdf314e0`). Both merge cleanly.

---

## NOT tested (and whether it could hide a Major)

- **No live environment.** I did not read the demo or prod `svc_api_keys` rows. Whether Platform S's real instance key is org-less, and how many legacy `NULL`, `''` or whitespace provisioning keys exist, is unmeasured. **This could hide a Major:** a bounded S key would break registration at deploy, and many unbounded legacy keys would keep M1 open. The census (fixed per m1) must run before deploy.
- **The four platform suites were not run** (Schemathesis, **Akto BFLA/BOLA**, Playwright, k6). Akto is the relevant authorisation suite. My matrix and live probe cover the BFLA/BOLA shapes of these two routes, but not the rest of the API surface. **Could hide a Major elsewhere, not in this diff.**
- **Preflight legs 3, 4 and 8 and the shell suites were not run** (they need the local stack and the shared checkout's history).
- **The KS-695 erasure running against a hop-2 key** is a code read only, as the author and the 1535 gate also had it.
- **Auth's real `/internal/connector-token` service was not booted.** I used a wrapper that signs `generateConnectorToken`'s claims. The gateway's own HTTP hop to originate for M1 was not exercised: I read `proxy.ts:1227-1241` and drove originate's router directly.
- **originate MT=true was run with a single seeded tenant.** I did not probe the `X-Tenant-Override` variants.
- **My first originate run gave a misleading result.** It omitted `tenantGucContext()`, and every INSERT got a 500 from RLS. I caught that against the production wiring and re-ran; that first run is in `runs/orig_head_1.txt`, labelled here, and is not evidence.

**Evidence:** `evidence/` beside this file. It holds `gatetests/` (my 4 cell files and the security server), `tools/` (runner, mutant runner, predicate table, PG setup) and `results/` (all runs, ledgers, suites, mutants, merge-tree, census). Throwaway `sk_` keys are redacted; no DB password appears in it, which I checked against a positive control.
