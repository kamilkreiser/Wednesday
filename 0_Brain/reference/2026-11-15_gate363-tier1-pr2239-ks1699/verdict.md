PR 2239: GO WITH NOTES (at head f1ac5fec9b679f8cde1a406cbeeb6cd58ee7c13d; tier 1)

Gate 363 (tier 1, Opus). Run 2026-11-15 22:06 to 22:29 AEDT. Findings only. Nothing was fixed, pushed, posted, commented, mailed, merged, or written to Linear or GitHub. Every figure comes from my own files in `scratch/`.

**Pins** (`gh api`, account kksecura; `scratch/pin1.out` 22:06:50, `scratch/pin2.out` 22:28:16):
- PR 2239 head f1ac5fec9b679f8cde1a406cbeeb6cd58ee7c13d, open, not merged, both reads.
- PR 2160 head b02bd2716cc2, open, both reads.
- develop was 2daedc204a51 at 22:06 and **moved to 7b452b1bbb96 by 22:28**. That move is KS-1197: 2 api-gateway files, 0 originate paths, 0 packages/shared paths, 0 overlap with the head's 6 paths. merge-tree of 7b452b1 × head: rc 0 both orders, tree 82494d0959a7, certifications.ts c20e597d1e6c, 0 originate/packages paths differ from my measured merge (`scratch/mt2.out`). So every run below, made on develop 2daedc20, carries to the new develop.

The diff is ONE commit on daa54a26d163: 6 files, +276 −18 (product +32 −3), equal to the READY. merge-tree develop 2daedc20 × head: rc 0 both orders, tree 64f6d9505a7a. The merge holds the head's certifications.ts (c20e597d1e6c). Merge-vs-develop patch-id equals the head's own (5e630ae3b9f0) (`scratch/mt.out`).

## FOUND

**G363-2239-1 (Low; test gap on a ruled decision; recommended before merge, not a block).** D1's "refused, **not defaulted**" has no cell that can tell the two apart.
- My mutant `claim_defaults_to_default_tenant` turns a missing claim into the default tenant, the gateway's own pattern (`api-gateway/middleware/auth.ts`, `if (!decoded.tenantId) decoded.tenantId = DEFAULT_TENANT_ID`). It reddens **0 of the PR's 54 cells** and 0 of KS-1695's 37.
- Why S8 and R8 miss it: every cell's request tenant is `…00aa`, never the default tenant. A defaulted claim therefore still mismatches and is still refused.
- In the live single-tenant configuration (originate `index.ts`, "the live config"; migration 039 backfilled rows into the default tenant), that regression would admit **every tenant-less ORG_ADMIN to every default-tenant certification**. Two in-repo seed paths still create tenant-less ORG_ADMINs (confirmed below).
- My cell G8 catches it (2/2): an ORG_ADMIN with no claim, or an empty one, on a default-tenant row via an unvouched request gets 404; the default tenant's own ORG_ADMIN gets 201.
- The new flow fragment says "Rulings the cells pin. The claim is compared, not defaulted". For "not defaulted", that overstates what the cells pin.
- **Exact action:** add one cell per route, shaped like G8: row in `a0000000-0000-4000-8000-000000000001`, ORG_ADMIN with no tenantId claim → 404 + 0 side effects, with the default-tenant ORG_ADMIN → 201 as the comparator. The cell source is in `scratch/gatecells/tail.ts`.

**G363-2239-2 (Info, for Kam's awareness; ruled D2, not a defect).** "A company's own admin" is built as tenant-wide.
- The code is exactly D2: `decideTenantAccess` is called with no `organisationScope`, so the organisation is never read. My mutant `org_bound_D2` (refuse an ORG_ADMIN who carries an organisation) reddens **0 of 54**: the PR has no cell where the admin carries an organisation. My cell G4 (an ORG_ADMIN with `organizationId: org-sibling-b` → 201 on both routes) pins it.
- What tenant-wide means where several companies share one tenant: the builder's slot-4 read (`evidence/d1_slot4.out`) shows 2 of 5 ORG_ADMINs in the DEFAULT tenant, and all 5 have no organisation.
- On such a tenant, any company's ORG_ADMIN may share any co-tenant company's certification, which sends email to addresses it chooses and writes a share charge. It may also recertify one, which saves a new certificate naming that admin as issuer and writes a verification_certificate charge.
- The PR body states this plainly ("Tenant-wide, sibling organisations included"). The demo's tenant/company layout was not measured.
- If Kam's "a company's own admin" meant the admin's own organisation, that is the organisation-scope follow-up the body names; it is not one line, because the row has no organisation.

**G363-2239-3 (Low; doc-only; the builder's offered amend is graded TAKE).** `callerMayReadCertification`'s doc comment (head `:159-160`, identical at develop) still says share and recertify "apply the same rule". That is now false: those two routes apply that rule plus a same-tenant ORG_ADMIN.
- The risk is a future reader "simplifying" the routes back onto the read helper, or the reverse. My `arm_into_read_helper` mutant is caught only by P3 (3 cells), so the comment is the first line of defence.
- No amend text exists yet; the READY and the body only offer one. A sentence that would be accurate: "KS-1699: `POST /:id/share` and `POST /:id/recertify` apply this rule PLUS a same-tenant ORG_ADMIN, through `callerMayShareOrRecertify` (card secuura-ks1699-admin-means-platform-admin-1115 = b); do not add that arm here, because GET /:id, lineage and evidence-bundle keep an ORG_ADMIN non-party at 404. `POST /:id/verify` deliberately applies neither (card c)."
- Fold it into the same re-push as G363-2239-1 if there is one; otherwise make it a follow-up. It is comment-only, and it changes the head, so a re-pin is needed.

**G363-2239-4 (Low; client-readable claim; two wording fixes before posting).** The KS-1699 comment draft (`push/linear_comment_ks1699.md`) is graded ACCURATE with 2 wording fixes plus 1 update. Every factual sentence was read against the head:
- These hold, all measured: the head and parent shas; one new helper; the party rule OR an ORG_ADMIN whose claim equals the looked-up tenant; one word per route; before the revoked check and every write. Also the "Unchanged" line (GET/lineage/evidence-bundle 404, revoke issuer-only 403, verify open; cells P1-P3, V1); 24 → 54 cells; 31 red over the PR 2233 routes, all by assertion; 54/54 green.
- These hold, read: the slot-4 figures match `evidence/d1_slot4.out`. Both seed paths insert ORG_ADMIN users with no `tenant_id` column: adminConfig.ts seed list, 4 ORG_ADMIN at `:2076-2095`; seed-azure-dev.sql, 3. `users.tenant_id` has no column default (migration 030 adds it bare; 039 backfills once), so those rows are NULL.
- **Fix 1:** "such an admin is refused here, as revoke already refuses it". Certification revoke refuses every non-issuer, for a different reason. If "revoke" means `/api/keys` revoke (`decideTenantAccess` "caller has no tenant"), say so; otherwise drop the clause.
- **Fix 2:** "every other role (ISSUER_ADMIN, ADMIN, USER)". Platform admins are admitted (through the party rule). Say "every other non-platform role".
- **Update:** change "Next: the tier 1 gate" to cite this verdict.
- "16 planted tampers each turn at least 2 cells red" is true of the builder's list. It is not a claim that every tamper is caught; G363-2239-1 and -2 show two that are not.

## TESTED

**Q1. Who share and recertify admit, and where the check sits.**
- `callerMayShareOrRecertify` (head `:199-204`) returns `callerMayReadCertification(req, cert) || (isPlatformOrOrgAdminRole(role) && decideTenantAccess(authUser, getReqTenantId(req)).allow)`.
- It is a strict superset of the old check, so no previously admitted caller is refused.
- `getReqTenantId(req)` is the same value `getCertification(id, tenant)` used: share `:1376`; recertify `:1490` then `:1492`.
- Call sites: the new helper's definition plus share `:1388` and recertify `:1503` (3 occurrences). The read helper is unchanged at GET `:1132`, lineage `:1665` and evidence-bundle `:1758`.
- Order at the head: 401 → lookup → not-found 404 → **guard** → revoked 400 → per recipient `saveShare` + `notifyDocumentShared` (EMAIL) → `createChargeEvent('share')`. For recertify: … → guard → revoked 400 → anchor `fetch POST /api/anchors` → save → charge. Refusals are byte-identical to each route's own not-found.
- Identity: the role and claim come from `req.user`, which originate's `authenticate()` sets to its OWN verified JWT payload (`middleware/auth.ts` `setUser(req, decoded)`), so the tenantId is the signed claim, never a header.

**Red-proof, reproduced** (`scratch/plants_table.out`, `j-p-develop_blob.json`):
- develop's certifications.ts (6eff2cfa755c) over the head's cells: **31 of 54 fail**, all `expect(...)` assertion failures (S3, R3, S10, R10, S11, R11, S11b, R11b, S7×2, R7×2, S8×2, R8×2, S9×6, R9×6, P3×3), and 0 of KS-1695's 37 fail.
- At the head: 54/54 + 37/37 (`scratch/run1.out`). This equals the READY.

**Mutants: 21 of mine plus develop's blob** (`scratch/plant.py`, `plants.out`, `plants_table.out`). Each was restored and the hash read back c20e597d1e6c; every red is an assertion (0 non-assertion, 0 file errors).

| Mutant | PR 2239 cells red (of 54) | my G cells red (of 16) |
|---|---|---|
| admin arm removed | 31 | 10 |
| role only (tenant compare dropped) | 8 (S7, R7, S8, R8, S11, R11) | 8 |
| tenant only (role check dropped) | 14 (S9, R9, S11b, R11b) | 2 |
| tenant allow inverted | 31 | 14 |
| **claim defaults to the default tenant** | **0** | 2 (G8), G363-2239-1 |
| role also admits ISSUER_ADMIN | 2 (S9, R9) | 0 |
| role by `toUpperCase()` (dotless i folds) | 2 (S9, R9 `org_admın`) | 2 |
| role exact `ORG_ADMIN` only (no fold) | 2 (S10, R10) | 2 |
| **organisation-bound (D2 reversed)** | **0** | 2 (G4), G363-2239-2 |
| arm written into the read helper | 3 (P3) | 0 |
| share reverted to the read helper | 17 | 5 |
| recertify reverted to the read helper | 14 | 5 |
| share guard after the revoked check | 2 (S5, S11) | 0 |
| recertify guard after the revoked check | 2 (R5, R11) | 0 |
| share guard after the email loop and charge | 14 | 3 |
| recertify guard after the anchor POST | 14 (anchors counted on a real local server) | 3 |
| share refusal 403 | 15 | 4 |
| recertify refuses with share's body | 15 | 4 |
| revoke widened to the new helper | 1 (P2) | 0 |
| verify guarded with the new helper | 1 (V1) | 0 |

**Q2. D1, D2 and D3 as ruled, each with a cell.**
- **D1:** S8 and R8 (no claim / empty claim → 404, 0 side effects) pass, plus my G8 and G6 (an array tenantId claim → 404).
  - Holds in the live path: originate verifies the JWT itself, and the gateway's `decoded.tenantId = DEFAULT` default only rewrites the gateway's own copy and `x-tenant-id`, never the forwarded token. A tenant-less ORG_ADMIN through the gateway gets request tenant = default and claim = none → refused.
  - Gap: G363-2239-1.
- **D2:** holds by construction (no `organisationScope`); the body states it. The PR has no cell; my G4 pins it (G363-2239-2).
- **D3:** S10 and R10 (`org_admin` admitted), S9 and R9 (`org_admın` U+0131, `ORG_ADMINS`, `platform_admin`, `ADMIN`, `ISSUER_ADMIN`, `USER` refused), my G5 (`Org_Admin` admitted) and G6 (array role refused). The fold mutants are caught both ways.

**Q3. Nothing else moved.**
- The product diff touches only the import, the new helper and one word plus one comment line per route. `callerMayReadCertification`'s body is byte-unchanged.
- Cells: P1 (revoke 403 to a stranger), P2 (revoke 403 to the admitted ORG_ADMIN), P3 ×3 (GET /:id, lineage and evidence-bundle 404 to the admitted ORG_ADMIN, byte-equal to unknown-id), V1 (verify 200 + 1 charge to a stranger).
- Each one reddens under its own mutant (table). KS-1695's 37 cells are green at the head.

**Q4. A cross-tenant ORG_ADMIN, and how the request tenant is derived.**
- **Derivation.** `req.tenantId = resolveRequestTenantId(req)` (`utils/requestTenant.ts`, mounted unconditionally at `index.ts:264`) resolves to:
  - an upstream `req.tenantId` (multi-tenant `extractTenantContext`, from the raw header behind the provenance strip); else
  - `x-tenant-id` only on a gateway-vouched request; else
  - `DEFAULT_TENANT_ID`.
- `getReqTenantId` adds the same default.
- The gateway writes `x-tenant-id` from the verified claim (`api-gateway/middleware/auth.ts:694-702`). It writes DEFAULT for a claim-less token; only `isPlatformRole` may override it.
- So through the gateway, an ORG_ADMIN's request tenant always equals its claim. The claim compare is a second wall that matters on direct, unvouched or multi-tenant-header paths.
- **Cross-tenant:** S7 and R7 (a) are the lookup wall (`getCertification` is `WHERE id AND tenant_id`, `certificationRepo.ts:170-177`). S7 and R7 (b) are the claim wall. Both give 404 with 0 side effects. My G3 (vouched header = the row's tenant, claim = another tenant → 404) runs through the REAL resolver.
- **Default-tenant fallback, measured with the real resolver** (`scratch/run2.out`, 70/70 at the head). A caller with a tenant claim can NOT reach default-tenant rows through the admin arm:
  - G1: unvouched request, so the request falls back to the default tenant. An ORG_ADMIN with claim `…00aa` on a default-tenant row gets 404 with 0 side effects. The default tenant's own ORG_ADMIN gets 201.
  - G2: an unvouched forged `x-tenant-id` naming the admin's own tenant is ignored. The lookup runs in the default tenant, so a TENANT row gives 404. Vouched, it gives 201.
- G1 and G3 redden under `role_only_no_tenant` and under `share_after_charge` / `recert_after_anchor` (side effects), so they can fail.
- The party arm's behaviour on that fallback is unchanged by this PR and was not examined.

**Q5. Overlap with PR 2160** (`scratch/m2160c.sh`, `m2160.out`).
- head × 2160: rc 0 both orders, tree f5a100365115, 0 conflicts. This equals the READY.
- (develop+2239 probe dcc5701504de) × 2160: rc 0 both orders, tree d8e3ad668f84.
- 2160 changes base `:935` (the `/issue` catch, KS-2017). 2239 changes `:57`, `:178`, `:1360` and `:1474`. The hunks are disjoint.
- Both changes keep their meaning in the combined file:
  - combined vs (dev+2239) has patch-id 1c7ddb91d071 = 2160's own;
  - combined vs (dev+2160) has patch-id 1b59d2c5e625 = 2239's own cert.ts patch;
  - KS-2017 appears ×1 and `callerMayShareOrRecertify` ×3.
- Planted control: an edit on the head's `:965` (2160's base `:935`, located by text) conflicts in both orders (rc 1, 1 CONFLICT each). A far edit at line 20 merges rc 0 in both orders.

**Q6. The doc-comment amend:** see G363-2239-3 (TAKE).

**Q7. The KS-1699 comment draft:** see G363-2239-4.

**Whole originate suite** (jest JSON, interleaved dev → merge ×2; each run started at load1 ≤ 8: 6.23, 7.80, 7.83, 7.83; `scratch/suites.out`):

| Tree | Run 1 | Run 2 |
|---|---|---|
| develop 2daedc204a51 | 223 files / 2633 tests, 2633 pass, rc 0 | same |
| merge dcc5701504de | 223 / 2663, 2663 pass, rc 0 | same |

2633 + 30 = 2663, equal to the READY. Porcelain was 0 after each run.

**tsc and eslint** (`scratch/tsc_lint.out`):
- `tsc --noEmit -p services/originate/tsconfig.json`: rc 0 / 0 errors at develop and at the merge. A planted TS2322 in the new helper gives rc 2 (1 error).
- eslint (Dev root flat config, ESLint API) on certifications.ts + the ks1699 test file: 0 errors / 0 warnings at the merge and at develop. Planted `var` + `debugger`: 2 errors. Then restored to c20e597d1e6c.

**Body** (live, 9,619 characters, `scratch/pr2239_body.md`):
- Title starts `Refs KS-1699:`. Close-words regex: 0. "NOT for merge until a gate verdict names its head" is the gate hold, not a self-hold on scope.
- The ruling is quoted verbatim, and D1-D3 are stated, including "sibling organisations included".
- Test Evidence is present. `13/16 legs ran, 3 SKIPPED` is quoted. NOT COVERED is listed.

## HOW
- **Clone:** my own clone `scratch/clone`: `git init` plus alternates to the Blockchain object store and to gate 356's clone (read-only). Fetched by `gh auth git-credential` (kksecura): develop, pull/2239/head, pull/2160/head. Push URL `DISABLED`.
- **Worktrees:** sparse `wt-dev` (develop 2daedc20), `wt-merge` and `wt-plant` (local probe dcc5701504de = develop + head, tree 64f6d9505a7a).
  - `node_modules` were APFS-cloned (`cp -c`) from gate 356's wt-dev. package.json, package-lock and packages/ are unchanged between its develop ce35818d and this one.
  - packages/shared was rebuilt in each tree (rc 0).
- **Local-only objects, never pushed, no refs:** probe commits (dev+2239, dev×2160, (dev+2239)×2160), the planted-conflict and far-control commits (author gate363).
- **wt-plant** holds my untracked `gate363-ks1699-extra.test.ts`: the head's 54 cells with a real-resolver tenant middleware, plus 16 G cells. It is the only porcelain line in the tree. The product file was restored by content after every mutant.
- No writes outside this folder. No `cd`, no `rm`.

## NOT TESTED (UNMEASURED)
- A running stack, Postgres/RLS, a real gateway + originate pair, the real email send, and the anchoring service. The cells use an in-process router, a mocked repository honouring the tenant, and a mocked `authenticate()`; only the anchor counter is a real local server.
- The demo's tenant/company/ORG_ADMIN layout (G363-2239-2) and whether any live ORG_ADMIN lacks a tenant. The slot-4 figures are the builder's; I read his output, not the database.
- Multi-tenant mode (`MULTI_TENANCY_ENABLED=true`) end to end. It was argued from source only; the claim compare protects the admin arm regardless of the header.
- Portal rendering: whether the issuer portal shows Share or Recertify to a non-party ORG_ADMIN.
- Node 24, the docs-fragments checker, `check:test-types`, pre-push hook legs, Schemathesis, Akto, Playwright and k6.
- Linear: KS-1699's state and comments were not read.
- The builder's 16 plants were not re-run verbatim. My table measures the same classes independently.
