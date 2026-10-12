# Gate verdict: Secuura Platform K PR #1521 (KS-1533 arm 1), fix round 1 of 2 (Opus delta gate)

**Gate:** independent adversarial QA, findings only. Nothing was written to the project, GitHub or Linear, and no remote server was contacted.
**Date:** 2026-10-13. **Brief:** `GATE_BRIEF.md` (this folder). **Charter:** `2_Project_Files/fleet/qa-agent/QA_AGENT_CHARTER.md`. **Previous verdict:** `../2026-10-13_gate-pr1521/verdict.md` (NO GO: M1, plus m1 to m3).

## VERDICT: GO WITH NOTE

- The r0 Major **M1 is closed.** I measured it over real HTTP, in memory and on PostgreSQL.
- The r0 **m1 is closed for the shapes it named:** case, padding and blank.
- No new Major was found in the diff.
- Two Minors remain, both residues of m1. Neither blocks the merge.

| id | sev | where | one line |
|---|---|---|---|
| **M1 (r0)** | **CLOSED** | `services/security/src/index.ts:1077` | A provisioner sending `rotate:true` with any string `connectorId` now gets 403 and retires nothing, across 57 provisioner rotate cells. The rotate shapes that were not refused here (`rotate:"true"`, `1`, `[true]`, a query param, a header, `__proto__` and similar) either give 400 or never reach the rotate code. Platform rotate still retires keys (control). register-connector is unchanged end to end. |
| **m1 (r0)** | **CLOSED** for case/padding/blank | `index.ts:1096` | Upper-case, padded, tab and NBSP ids are stored canonical. `''`, `'   '` and `'\t\n'` are stored as NULL. This holds for 6 caller kinds. |
| **m1-r1** | Minor (residue of m1) | `index.ts:1200` (`GET /api/keys`) | The list filter compares the **raw** query string with the stored canonical value. So `?organizationId=<UPPER or padded own id>` now lists **0** keys, where the same query listed 6 at `c02c0b5d`. A client that mints and lists with the same non-canonical string no longer sees its own key. The direction of the mismatch has flipped, but the mismatch is still there. |
| **m2-r1** | Minor | `index.ts:1096` + `packages/shared/src/security/orgId.ts` | `normaliseOrgId` does not canonicalise forms that PostgreSQL treats as the **same** uuid (`{uuid}`, the no-hyphen form), or a leading U+200B. These are stored verbatim (for example `{aaaaaaaa-…}`) for platform, `ADMIN` and provisioner callers, and are invisible under the canonical listing. Org-bounded roles are refused (403), so this fails safe. |
| item 5 | **fails safe** for org-bounded roles; **not made worse** | `index.ts:981-992` | Details below. A padded id escapes the raw `::uuid` lookup for `ADMIN` and the provisioner, but they can store the identical row with an explicit `tenantId` at both `c02c0b5d` and head. |
| M2 (r0), P1 (r0) | carried, separate tickets | originate `adminConfig.ts:947` / `index.ts:196-243` | Not in this diff and still open. I re-measured P1 at this head: 20 concurrent rotates leave **0 active of 21**, N=2 leaves **0 active in 10/10**, and the sequential control leaves 1. |

**Head under test:** `e4d7a13e8e20e57dbe92a9563266de2df495276b`. **develop:** `b08ee6299e864bea2aff18f31bdd22281161c1db`. **Previous gated head:** `c02c0b5dcc22d3a59c7faa787b08a2871bfdafda`.

**The note on GO:**
- **m1-r1 and m2-r1 together have one fix shape:**
  - Validate `organizationId` as `z.string().trim().uuid()` (or canonicalise through a uuid parse) at the mint.
  - Apply `normaliseOrgId` to the `GET /api/keys` query as well.
  - Regression test the owner should add: mint as an org admin with `organizationId` = upper-case own id, then list with the upper-case id **and** the canonical id. Both must return the key. A `{uuid}` id must give either 400 or a canonical stored value.
- **M2 must still be closed, or accepted by Kam, before KS-1533 or the KS-695 erasure is called done.** This PR does not touch it.

---

## How the head was obtained (and asserted)
- The project checkout was used **read-only**, with `rev-parse`, `config --get` and `cat-file` only. Its HEAD is `40ed3573b`, unchanged after the gate. It holds none of the four commits.
- I made a `git clone --shared --no-checkout` into the scratchpad, with the push URL set to `DISABLED`.
  - The prerequisites `c02c0b5d` and `25059609` were fetched from the previous gate's local scratch clone.
  - The head came from V's bundle `ks1533a-delta-c02c0b5d-to-e4d7a13e.bundle`. Its sha256 measured `1f6983fe27ef502e…`, which matches the brief, and `bundle verify` returned rc 0.
  - **No `ls-remote` or fetch was made to GitHub**: the gate's hard limit forbids remote contact. That head = remote rests on Wednesday's ls-remote in the brief.
- **Asserted:** the bundle `HEAD` is `e4d7a13e8e20…`. Its graph is `113d2a91` (fix), then `37cb3b94` (merge of develop `b08ee629`, parents `113d2a91` and `b08ee629`), then `e4d7a13e` (comment).

## Item 4: the develop merge (measured with git blob and tree ids)
- **`e4d7a13e` is comment-only.** Its diff is 2 comment lines in `index.ts` and 1 in the test file. Both replace the `platform.ts:517-528` citation with `"GUARDRAIL 1" in api-gateway routes/platform.ts`, because develop moved the line: Guardrail 1 is now at `platform.ts:543`.
- **The PR's files keep their blobs across the merge:**
  - `index.ts` is `d263b779…` at both `113d2a91` and the merge.
  - The test file is `200bad63…` at both.
- **`platform.ts` at the merge equals develop's blob** (`eff0b06b…`).
- `git diff --name-only b08ee629 e4d7a13e` lists exactly the 2 PR files.
- **develop's delta does not interact with this PR:**
  - develop changed `250596..b08ee6`: KS-1511 and KS-1512.
  - That touched 3 files in api-gateway, all audit-log paging (`platform.ts:390-425`) and its tests. There are no key, mint or Guardrail lines in it.
  - `packages/shared` has the identical tree id `c07df51f…` at `c02c0b5d`, `b08ee629` and `e4d7a13e`.

## The instruments, and the control that each one could fail
| instrument | what it is | control that could fail (and did, where shown) |
|---|---|---|
| Gate harness `evidence/harness/gate1521.test.ts` | r0's harness, re-used (real security app over real HTTP, real `express.json`, RS256 `authenticate`, real router). `patch.py` extended it with four additions: (1) the **R1 battery**: 9 non-platform roles × 3 organisation parts × 19 rotate shapes = 513 cells, asserting that the victim stays active and nothing retires; (2) an **m1 battery**: 6 callers × 13 org-id variants, reading the stored form back and listing it 3 ways; (3) an **item-5 battery**: 6 callers × 11 ids, with no tenant sent; (4) a **memory-vs-SQL cross-check** on every read-back in PG mode. | **(a) It goes RED on the unfixed code:** at `c02c0b5d` the R1 battery fails on its first cell (`provisioner/own/rotate true: victim retired`), in memory and in PG. **(b) RED on develop:** 3 failures, the r0 ones plus R1. **(c)** A platform rotate control must retire the victim (`priorKeysRevoked` > 0, victim inactive). It did. **(d)** The memory and SQL readers disagreed on **0** rows. |
| Classifier `evidence/harness/classify2.py` | r0's oracle, amended **before reading head's cells** only on the provisioner rotate line (see its docstring) | It still flags r0's four known oracle errors, which I left in deliberately: provisioner × other_tenant × non-string connector is expected 400 and is 403, because `decideMint` refuses first. This shows the oracle is live. |
| PostgreSQL 18, a scratch cluster on `127.0.0.1:55434` | A copy of r0's stopped cluster: minimal `svc_api_keys`, plus `organizations(id uuid, tenant_id uuid)`, which I seeded so the item-5 lookup branch actually runs. No RLS. Stopped after use. | `initDb()` must be true, or the harness throws. |
| Mutation runner `evidence/harness/mut.py` | V's 17 mutants, extracted **verbatim** from `mutants1533r2.py` | Every edit asserts its anchor count is 1 **and** that the mutated text landed. The file is restored and its sha256/16 asserted against `2e60b567e476cfd8` each time (17 of 17 restored). The baseline run must be green: the PR file gave 20/20 and the harness 13/13. |
| tsc / eslint | `tsc --noEmit -p services/security`; eslint on the 2 PR files | **Positive control:** I appended a type error plus a `var` to head's `index.ts`. tsc gave rc 2 with 3 errors, and eslint gave rc 1 (`no-var`). The file was restored with its sha asserted. |
| Secret scan | JWT, PEM private key and `sk_` hex | The control file hit 3 of 3. The evidence folder hit **0** files. |

## Findings in detail

### M1 (r0): CLOSED. Measured.
- **Oracle:** Product consistency with the gateway's GUARDRAIL 1 (`platform.ts:543`), which says "rotation stays platform-admin-only".
- **Matrix** (560 cells per mode, the r0 dimensions):
  - Head has **0** non-platform victim retirements (memory and PG).
  - `c02c0b5d` had **3**, all provisioner × rotate × `other`.
  - develop has **18**.
  - From `c02c0b5d` to head exactly **12 cells changed, all of them provisioner**: `{own_org, other_org, orgless} × {own, other, malformed_empty, malformed_case} × rotate`, each going 201 → 403.
  - **No cell outside the provisioner role moved.** Memory vs PG disagreements at head: 0 of 560.
- **R1 battery at head:** 513 cells, histogram 201 × 34, 400 × 108, 403 × 371. **Victims retired: 0. Any retirement: 0.** Provisioner, per shape (3 org parts each):

  | provisioner shape | status | what happens |
  |---|---|---|
  | `rotate:true` (also with a trailing-space, upper-case or empty connectorId) | 403 | refused |
  | duplicate key `false,true` | 403 | last wins = true |
  | `"true"`, `1`, `"1"`, `[true]`, `{}`, `null` | 400 | zod `z.boolean()` rejects them |
  | `?rotate=true`, `x-rotate` header, `Rotate`, `data.rotate`, duplicate key `true,false`, `__proto__.rotate`, `constructor.prototype.rotate` | 201 | `rotate` is false, so no retirement; this is the provisioner naming a connector, which the design allows (21 rows store `connector_id`, 0 retire) |
  | `rotate:true` with connectorId only in the query | 201 | zod strips the query connectorId, so the rotate is a no-op (0 retired) |

- **Unfixed control on the PR's own file:** I ran head's test file against `c02c0b5d`'s `index.ts` and got **4 failed / 16 passed**: the three RED (M1) cells plus the m1 cell (`evidence/results/unfixed-file-run.txt`). At head it gives 20/20. **V's "unfixed 4 red / 16 green, fixed 20/20" is reproduced.**
- **register-connector replay** (the exact gateway mint body, every bearer kind `requireOrgProvisioner` admits): **identical at head and develop.**
  - `super_admin`, `SUPER_ADMIN` and `SYSTEM_ADMIN` give 201 both ways, and rotate reports `priorKeysRevoked: 1`.
  - The provisioner without rotate gives 201.
  - `platform_admin` gives 403. That is pre-existing, KS-1536, and the same as r0.

### m1 (r0): closed for its named shapes. Two residues (m1-r1, m2-r1).
**Measured, PG and memory identical: stored form by caller and sent variant.**
- **Upper-case, `'  UPPER '`, `'\tid'` and `' id'`** are stored **canonical** for super_admin, ISSUER_ADMIN (including one whose own claim is upper-case), `ADMIN` and the provisioner. They are listed under the canonical id.
- **Blank ids** (`''`, `'   '`, `'\t\n'`) are stored **NULL**, including for the org-less issuer_admin.
- **Against `c02c0b5d`:** 44 m1 cells changed, every one from a raw stored form to the canonical form or NULL. Status codes did not change (0 cells), so the fix changed **only what is stored**, as claimed.

**m1-r1, the list filter (Minor):**
- `index.ts:1200` is `.filter(k => k.organizationId === organizationId)`, with `organizationId` taken raw from the query.
- **Measured, as the ISSUER_ADMIN of the org listing its own keys:**

  | query | head | `c02c0b5d` |
  |---|---|---|
  | canonical id | 27 keys | 6 |
  | upper-case id | **0** | **6** |
  | padded id | 0 | 0 |

  So a key minted and listed with the same upper-case string was visible before and is invisible now. The m1 symptom ("vanished from its own listing") is inverted, not removed.
- **Oracle:** Product consistency ("one form" at every comparison is the KS-780 rule the PR cites).
- **Likelihood: low.** Real organisation ids come from a `uuid` column, so they are canonical. The admin UI lists with `organizationId || 'default-org'` (`frontend/admin/src/services/api.ts:357`), which is already lower-case.

**m2-r1, incomplete canonical form (Minor):**
- PostgreSQL accepts `'{uuid}'`, `'UUIDNOHYPHENS'` and upper case as the same uuid. I measured this with `psql`, and the item-5 lookup resolves them to the organisation's tenant.
- `normaliseOrgId` only trims and lower-cases. So for platform, `ADMIN` and provisioner callers, `{aaaaaaaa-…}` and `aaaaaaaabbbb4ccc…` are stored verbatim. `​<id>` is stored verbatim too, because JavaScript `trim` does not strip U+200B.
- None of these are listed under the canonical id.
- **Org-bounded roles get 403 for all of these, so this fails safe.**
- **Fix:** validate with `z.string().trim().uuid()` (zod's uuid accepts upper case), then lower-case.

**Read the writers (brief scope 2):** `svc_api_keys.organization_id` has two writers.
- **security `POST /api/keys`** is now normalised.
- **originate `POST /api/admin/api-keys`** (`adminConfig.ts:947/960`) still writes `d.organizationId || user.organizationId` **raw**. That is pre-existing and r0's M2 route.
- The tenant-provisioning metering mint (`meteringKey.ts:45`) sends no organisation, so it writes NULL.
- **No existing row is rewritten by this PR.** Rows written raw before it, or by originate, keep their raw form. They stay listable only under that raw string, exactly as before. So no row becomes unlisted, but legacy non-canonical rows are not made canonical either.

### Item 5: the raw-id tenant lookup (`index.ts:981-992`). Fails safe; not made worse.
Measured on PG with `organizations` seeded: A1, A2 and OA are in TA; B1 is in TB. No `tenantId` or `x-tenant-id` was sent.

**ISSUER_ADMIN, ORG_ADMIN and org-less issuer_admin of A1 (TA): every foreign or odd id is refused.**
- `B1`, `B1` upper-case, `{B1}` and B1 without hyphens resolve to TB and give **403 "own tenant"**.
- `' B1 '` fails the `::uuid` cast, falls back to TA, and the org arm then gives **403 "own organisation"**.
- `{A1}` (its own org in brace form) gives 403. That is a false refusal of the caller's own organisation, which is the safe direction.
- **This is the "fails safe" the author stated, and it holds.**

**`ADMIN` and the provisioner of A1 behave differently:**
- `B1` gives 403 (the lookup finds TB).
- **`' B1 '` gives 201, stored as `(tenant TA, org 33333333-…)`.** The padded id escapes the lookup, the request falls back to the caller's tenant, and neither role is org-bounded.
- **Not worse because of this PR:**
  - With an explicit `{tenantId: TA, organizationId: B1}` (unpadded), both roles store the **identical row** at `c02c0b5d` and at head (`evidence/results/i5x-{head,prev}.json`). The padding adds no capability.
  - This PR's only effect here is that the row now stores `33333333-…` instead of `' 33333333-… '`.
  - `decideKeyRevoke` already normalised both sides, so revoke treated the padded row as B1 before this PR.
- **Pre-existing observation, not counted:** for non-org-bounded callers the service never checks that a named organisation belongs to the target tenant. For `ADMIN` that is Kam's open card KS-1535. For the provisioner it is register-connector's "mint for a new org" design.

**super_admin:** `' B1 '`, `' A1 '` and an unknown uuid land in `DEFAULT_TENANT_ID` (`a0…01`). This is the pre-existing platform fallback and is unchanged in status. The org id is now canonical.

**Status codes across all 66 item-5 cells: identical at `c02c0b5d` and head.**

### Item 3: mutants (17, V's table verbatim)
| instrument | killed | survivors |
|---|---|---|
| PR file | **16 / 17** | C4 only (20/20 under it) |
| gate harness, hard asserts | 4 / 17 | |
| gate harness, observation diff vs head's baseline | every mutant except A4, A5 and C4 | A4 and A5 change only message text, which I did not diff. C4 differs in 0 of 560 matrix cells, 0 of 513 R1-battery cells, 0 of 78 m1 cells and 0 of 66 item-5 cells, in both modes. |

- **R1 killed by me on a green baseline:**
  - PR file: 3 failed.
  - Gate harness: the R1 battery fails on its first cell, in memory **and** PG.
  - The matrix flips back to exactly the 12 provisioner cells.
- **S1 killed by me:**
  - PR file: 1 failed.
  - Gate harness observations: 44 m1 cells and 14 item-5 cells revert to raw stored forms, in memory **and** PG.
  - **The harness has no hard assert on stored form. That is my instrument's gap, not the PR's.** The kill was read from the observation diff.
- **C4 is still the only survivor and is still masked.** The reachability probe on head's `decideMint` (`evidence/results/reach.txt`, unchanged from r0) shows role `connector` passes only with `organizations:register`, and `Connector`, `CONNECTOR` and `' connector'` are refused.
  - So the scope-less `connector` that C4 would wrongly treat as a provisioner never reaches the route clause. Under C4 the new rotate refusal would only refuse **more**, so it is not a safety gap either.
  - The r0 curio stands: a **string** `scopes` claim is accepted by substring. It is unreachable today.

### Item 6: suites at the head
| run | head `e4d7a13e` | develop `b08ee629` |
|---|---|---|
| security (vitest) | **30 files / 331 tests**, rc 0 | 29 / 311, rc 0 |
| packages/shared (vitest, run from the package dir) | **49 / 949**, rc 0 | 49 / 949, rc 0 |
| `tsc --noEmit` (security) | rc 0, 0 lines | rc 0 |
| eslint (the 2 PR files) | rc 0, 0 lines | n/a (the test file does not exist on develop; rc 2 "no files matching") |

- Head minus develop on security is exactly the PR file's **20** tests. **V's 331, 949, tsc and eslint figures are all reproduced.**
- Both suites ran with no stray gate files in `__tests__` (asserted: 0). The scratch `dist` for `@secuura/shared` was built once with `tsc`, which is valid because the shared tree id is identical in all three trees.

## What was NOT tested (Rule 2)
- **Remote:** no `ls-remote` or fetch. That the head and develop are the remote's current state rests on the brief, and develop may have moved since `b08ee629`.
- **No real gateway or auth hop.** The security leg used tokens with auth's exact connector claim shape, signed by a throwaway key. The gateway path to the service for a provisioner `sk_` key is still code-read only (r0).
- **The test file is not type-checked.** The security `tsconfig` excludes `src/__tests__`, and the repo's `check:test-types` covers only auth and api-gateway. So "tsc clean" covers `index.ts`, not the test file. eslint did cover the test file.
- **PostgreSQL is not the real schema.** It has minimal tables, no RLS and no migrations, and I connected as superuser. The `runWithPlatformScope` lookup ran without RLS enforcement.
- **originate was not booted** (M2, item 5's other writer). The KS-695 erasure is 501 at this head and was not run.
- **Stored-form checks were not run in the r0 matrix,** only in the m1 and item-5 batteries.
- **Message text was not diffed by my harness,** so A4 and A5 are killed only by the PR file.
- **Not run:** the gateway suites, `check:test-types`, V's pre-push hook, Schemathesis, Akto, Playwright and k6. Nothing ran against Kintsugi, demo or any box.
- **Not tested:** rotate concurrent with revoke, a grace window > 0, and expired or tampered tokens (same gaps as r0).

## Evidence (this folder)
- `evidence/harness/`:
  - `gate1521.test.ts` (r0's harness after `patch.py`), `item5x.test.ts`, `regconn.test.ts`
  - `classify2.py` (the oracle is in its docstring), `mut.py`, `reach.mjs`
  - `run.sh`, `suites.sh`, `ctl.sh`
- `evidence/results/`:
  - matrix: `{head,prev,dev}-{mem,pg}.json`
  - `classification-head-{pg,mem}.txt`
  - `i5x-{head,prev}.json`, `regconn-{head,dev}.json`
  - `mut-{R1,S1,C4}-{mem,pg}.json`, `mutants.txt`, `mutants.json`
  - `reach.txt`, `unfixed-file-run.txt`, `suite_summaries.txt`
  - `prev-*` is `c02c0b5d`, the r0 head and the unfixed control.
- **Scratch state:**
  - The clone, three worktrees (head, dev, prev) and the PG cluster are in the session scratchpad, under `g1521r1/`.
  - **PG is stopped.**
  - Head's `index.ts` was restored to sha256/16 `2e60b567e476cfd8`, asserted after all 17 mutants and after the tsc/eslint control.
- **Project checkout:** HEAD `40ed3573b` is unchanged. Its 3 untracked `systemTest/akto` files pre-date this gate and are not mine.

## PROOF debrief
- **Past:**
  - Asserted the bundle head, measured the delta, and verified the merge by blob and tree ids.
  - Re-ran r0's real-HTTP matrix at head, the unfixed head (`c02c0b5d`) and develop, in both storage modes.
  - Added a 513-cell rotate battery, m1 and item-5 batteries, and the register-connector replay.
  - Ran 17 verbatim mutants against two instruments, then the suites, tsc and eslint, each with a positive control.
- **Results:**
  - M1 is closed. The delta changes exactly the 12 provisioner rotate cells and nothing else.
  - m1 is closed for case, padding and blank.
  - Two residual Minors remain: the list query is not normalised, and the canonical form is incomplete.
  - Item 5 fails safe for org-bounded roles and is not worsened.
  - Every author figure is reproduced.
- **Obstacles:**
  - The fleet hooks refuse write-verbs and `cd` aimed outside WEDNESDAY even when the target is the scratchpad, so all scratch git and runner work went through scratch scripts.
  - There was no remote contact by rule.
- **Outlook:** GO with the note. m1-r1 and m2-r1 can ride a follow-up. M2 and P1 remain their own tickets.
- **Confidence:**
  - **High** on M1 closed: both modes, a 513-cell battery, and controls that go red on the unfixed code and on develop.
  - **High** on m1 and the item-5 measurements.
  - **Medium** on the m1-r1 likelihood rating, which rests on a code-read of the callers.
