PR 2239: GO WITH NOTES (at head 9036b3d0c78a5a83d8e08092d4c0a08eb37793d7; tier 1, delta round 2 of 2)

Gate 364 (tier 1 delta, Opus). Run 2026-11-15 23:37 to 23:54 AEDT. Findings only: nothing fixed, pushed, posted, commented, mailed, merged or written to Linear or GitHub. Every figure is from my own files in `scratch/`.

**Pins** (`gh api`, account kksecura; `scratch/pin1.out` 23:37:10, `scratch/pin2.out` 23:53:42):
- PR 2239 head 9036b3d0c78a5a83d8e08092d4c0a08eb37793d7, open, not merged, 3 commits, 6 files +352 −21, at both reads.
- PR 2160 head b02bd2716cc2, open, at both reads.
- develop was bbb75755064e at 23:37 and **moved to 09b11a163694 by 23:53**: 2 commits (KS-716, KS-1415), 2 paths, 0 originate, 0 packages/, 0 package*.json, 0 overlap with the head's paths. new develop × head: rc 0 both orders, tree 6b163d180a30. The merged certifications.ts (473e968f72ed) and test file (aac6cb5163a4) equal the head's, and 0 originate/packages paths differ from the merge I measured (`scratch/mt3.out`). So every run below carries to the new develop.

The delta f1ac5fec9b67..9036b3d0c78a is 2 commits, 2 files, +76 −3, equal to the READY: the ks1699 test file (+73 −2) and certifications.ts (+4 −2, comment only).

## FOUND

**G364-2239-1 (Low; client-readable claim; one update before posting).** The KS-1699 comment draft's last bullet says "A delta gate reads round 2 next". Once this verdict exists that sentence is stale.
- Exact action: replace that sentence with this verdict's line 1, verbatim, the same way the bullet already quotes gate 363's line 1.
- Every other factual sentence is ACCURATE at the new head (graded under Q5 below).
- The rest of the draft does not need to change.

**G364-2239-2 (Info; test-comment attribution, no behaviour).** S13's comment (test file, the round-2 block above S13) calls `("A same-tenant ORG_ADMIN may share and recertify too")` "D2, Wednesday's ruling on Kam's card 1115 = b".
- That quoted text is the card's option-b **detail** text (the file's own header, lines 21-22, labels it that way). Kam's ruling is "Also a company's own admin", and D2 is Wednesday's tenant-wide reading of it.
- The cells pin D2 correctly. Only the attribution in the comment is loose. A later tidy-up can fix it; it is not worth a re-push on the last round.

**G364-2239-3 (Info; what "drives the REAL resolver" does and does not prove).** S12 and R12 execute the real `resolveRequestTenantId`, measured below. One limit applies:
- A harness stub that just assigns `DEFAULT_TENANT_ID` (my `harness_resolver_stubbed_default`) reddens 0. On this path (unvouched, no upstream tenant) the real resolver and that constant behave identically.
- So the cells prove that the fallback in the real code is what is exercised. They do not test the resolver's other arms, which were never their job.

**G364-2239-4 (Info; pre-existing, develop-side).** My first develop suite run (dev-1) had 1 file error: `ks488-smtp-opt-in.test.ts`, TS2300 "Duplicate identifier 'EmailModule'" colliding with `ks1937-…`.
- This is the same pre-existing ks488/ks1937 pair the READY names on its tsc-with-tests line.
- It was cold-cache only: dev-2 and dev-3 are clean, and none of the 6 runs failed on this PR's files. It is not this PR's.

Round 1's notes:
- **G363-2239-1: CLOSED.**
- **G363-2239-3: CLOSED.**
- **G363-2239-4: CLOSED**, with the one update in G364-2239-1.
- **G363-2239-2** stays Info for Kam (tenant-wide, as ruled; now pinned by S13 and R13).

## TESTED

**Q1. G363-2239-1: is it closed?** Yes (`scratch/plants.out`, `j-p-*.json`).
- **Red against the mutant.** Against round 1's own `claim_defaults_to_default_tenant` edit, copied byte for byte into my plant.py, exactly 4 cells go red: S12 ×2 and R12 ×2 (no claim; empty claim), all by `expect` assertion. 0 other cells go red, and 0 of KS-1695's 37.
- **Green at the head.** At the raw head (wt-head) and at the merge: 60/60 + 37/37 (`scratch/run1.out`).
- **Each claim shape has its own cell.**
  - `only_undefined_claim_defaults` (`??`) reddens only the no-claim S12 and R12 (2).
  - `only_empty_claim_defaults` reddens only the empty-claim S12 and R12 (2).
  - `claim_defaults_to_request_tenant` reddens 8: S8 ×2, R8 ×2, S12 ×2, R12 ×2.
- **The REAL resolver runs.**
  - `resolveRequestTenantId` is imported from `../utils/requestTenant`, and the test file has no `jest.mock` of that module. The mocks are only certificationRepo, db, chargeEvents, notificationClient, events, documentRepo, middleware/auth and logger.
  - Mutating the REAL `utils/requestTenant.ts` fallback (`resolver_fallback_not_default`) reddens exactly S12 ×2 and R12 ×2 and nothing else. So does `resolver_reads_unvouched_header_or_aa`.
  - Disabling the harness's resolver branch (`harness_resolver_mode_ignored`) reddens the same 4.
  - The comparator (the default tenant's own ORG_ADMIN → 201) can fail, and does under these mutants.
- **Every pre-existing cell stays on direct mode.**
  - `tenantFrom` is reset to `'direct'` (and `gatewayProvenance` to undefined) in the top-level `beforeEach`. It is set to `'resolver'` only in the nested `beforeEach` of the S12/R12 describe.
  - The real-resolver mutant reddens 0 of the other 56 cells. So none of the 54 earlier cells or S13/R13 depends on the resolver.

**Q2. G4 → S13/R13 pins D2 as ruled ("Also a company's own admin" → tenant-wide; a same-tenant sibling organisation's admin is admitted).**
- S13 and R13 (ORG_ADMIN, same tenant, `organizationId: 'org-sibling-b'`) give 201 with exactly one of each side effect.
- `org_bound_D2` (round 1's edit) reddens exactly S13 and R13 (2), by assertion. My `org_bound_only_if_not_sibling_a` also reddens exactly those 2.
- My `org_scope_passed_row_org` (passes an `organisationScope` to `decideTenantAccess`) reddens 37.

**Q3. G363-2239-3: the comment sentence** (`scratch/q34.out`).
- Head lines 159-162, 4 lines, max 116 columns. Unwrapped, the text **equals round 1's proposed sentence byte for byte** (359 = 359 characters, equal: true).
- `callerMayReadCertification`'s function text (TS AST, declaration start to end) hashes sha256 620fb7a84da3fdd2 at round 1's head, at the new head and at develop. It is byte-unchanged.
- `callerMayShareOrRecertify` hashes 4a389ecf40792b4d at both heads.

**Q4. The delta changed no product logic** (`scratch/q34.out`).
- In the diff f1ac5fec9b67..9036b3d0c78a on certifications.ts, every +/− line is a ` * ` JSDoc line (0 non-comment changed lines).
- The TypeScript printer with `removeComments` gives identical output for round 1's and the new certifications.ts (sha 0742f893bd5d5694). The comment-skipping token streams are also equal.
- Control: a one-token planted change (`!decideTenantAccess`) makes both comparisons differ.
- The only other file in the delta is the test file. No `src/` product file besides certifications.ts is touched.

**Q5. G363-2239-4: the corrected Linear draft** (`push/linear_comment_ks1699.md`, R 121st's record), read as a client-readable claim:
- "head `9036b3d0c78a`, three commits on develop `daa54a26d163`": TRUE. The merge-base is daa54a26d163, and the PR has 3 commits.
- The helper, party-rule-OR-same-tenant-ORG_ADMIN, one word per route, and before the revoked check and every write: unchanged since round 1 (product logic proven unchanged, Q4). The order mutants still redden (share/recert after revoked 2 each; after charge/anchor 16 each).
- "tenant-wide … sibling organisation admitted": TRUE (S13/R13).
- Still refused: another tenant's ORG_ADMIN, a claim-less ORG_ADMIN, and "every other **non-platform** role (`ISSUER_ADMIN`, `ADMIN`, `USER`)". TRUE: `PLATFORM_ROLES` = {SYSTEM_ADMIN, SUPER_ADMIN} (`keyRevokePolicy.ts:60`), so ADMIN is non-platform. Fix 2 is applied correctly.
- The fold sentence (`org_admin` passes, dotless i does not): TRUE (fold mutants 2 red each).
- The revoke clause is gone (Fix 1 is applied as DROP). Unchanged line: TRUE (P1-P3, V1; the revoke-widened and verify-guarded mutants still redden 1 each).
- Reachability bullet: unchanged from round 1's grading, minus the dropped clause.
- "24 to 60 cells (54 in the first commit, 6 added in round 2)": TRUE (60 measured; round 1 measured 54).
- "37 fail over the PR 2233 routes, all by assertion": TRUE. develop's certifications.ts under the head's cells gives 37 of 60 red: the 31 from round 1 plus S12 ×2, R12 ×2, S13 and R13. 0 non-assertion, 0 of KS-1695's 37.
- "all 60 pass": TRUE.
- "16 planted tampers each turn at least 2 cells red": the builder's list (READY), consistent with my independent classes.
- "the gate's two mutants … (4 cells red) and … (2 cells red)": TRUE, measured 4 and 2.
- "gate 363 ruled …": verbatim equal to round 1's verdict line 1.
- "A delta gate reads round 2 next": stale after this verdict (G364-2239-1).
- No `@` in the draft, so no mention can form.

**Q6. Whole originate suite** (`scratch/suites.out`, `suites3.out`; jest JSON, interleaved dev → merge ×3; load1 at the starts was 6.82, 7.64, 7.73, 7.74, 7.60, 7.87, all ≤ 8):

| Tree | Run 1 | Run 2 | Run 3 |
|---|---|---|---|
| develop bbb75755064e | 223 files / 2625 pass, 1 file error (ks488 TS2300, G364-2239-4) | 2633 / 2633, rc 0 | 2633 / 2633, rc 0 |
| merge f7b543fa8508 (develop × head) | 2669 / 2669, rc 0 | 2669 / 2669, rc 0 | 2669 / 2669, rc 0 |

- 2633 + 36 = 2669. This equals the READY's develop 2633 / branch 2669.
- KS-1695's file is 37/37 in every cell run and every plant.
- Porcelain was 0 after each run.

**Q7. R 121st's leg-1 finding: CONFIRMED.**
- On wt-head, `npm run check:openapi` with a 125-character TMPDIR exits rc 1 with tsx `listen EINVAL … tsx-501/<pid>.pipe`. With my 52-character TMPDIR it exits rc 0 with "CHECK PASS".
- The EINVAL output matches neither of preflight.sh leg 1's classifiers (`:313` esbuild 0 hits, `:320` STALE 0 hits; EINVAL control 2 hits).
- So it falls through to `:333` "FAIL — spec drifted". The leg misreports an IPC-socket path-length crash as spec drift (`scratch/leg1_long.out`, `leg1_short.out`, `leg1_classify.out`). The board seat may ticket a classifier branch for `listen EINVAL`.

**Mutants: 32 runs** (`scratch/plant.py`, `plants.out`). Each run used the ks1699 file plus KS-1695's file (97 cells). Every product mutant was restored by content and hash-checked at 473e968f72ed; requestTenant.ts and the test file were restored by checkout, with a porcelain-0 assert after each run. Every red is an `expect` assertion: 0 non-assertion reds, 0 file errors, and 0 KS-1695 reds in any run.

| Mutant | red of 97 |
|---|---|
| none | 0 |
| develop blob | 37 |
| claim defaults to default tenant (G363) | 4 (S12 ×2, R12 ×2) |
| org-bound D2 (G363) | 2 (S13, R13) |
| claim defaults to request tenant | 8 |
| only undefined claim defaults / only empty claim defaults | 2 / 2 |
| organisationScope passed (row org) | 37 |
| org-bound unless org-a | 2 |
| tenant compared to DEFAULT | 33 |
| REAL resolver fallback not default | 4 |
| REAL resolver reads unvouched header | 4 |
| harness resolver branch ignored | 4 |
| harness resolver stubbed to DEFAULT | 0 (G364-2239-3, equivalent on this path) |
| admin arm removed / tenant allow inverted | 37 / 37 |
| role only (no tenant) / tenant only (no role) | 12 / 14 |
| ISSUER_ADMIN admitted / toUpperCase fold / exact ORG_ADMIN only | 2 / 2 / 2 |
| arm moved into the read helper | 3 |
| share reverted / recertify reverted to the read helper | 20 / 17 |
| share after revoked / recertify after revoked | 2 / 2 |
| share after charge / recertify after anchor | 16 / 16 |
| share refusal 403 / recertify with share's body | 17 / 17 |
| revoke widened / verify guarded | 1 / 1 |

**Overlap with PR 2160** (`scratch/m2160.out`).
- head × 2160: rc 0 both orders, tree d11624b7203b (= the READY).
- (develop+2239) × 2160: rc 0 both orders, tree ae684e5110d0.
- Both changes keep their meaning in the combined file:
  - combined vs (dev+2239), certifications.ts: patch-id 1c7ddb91d071 = 2160's own;
  - combined vs (dev+2160): 05b675b689f0 = 2239's own certifications.ts patch (merge-base..head).
- Controls:
  - A planted edit on 2160's line (base :935 → head :967) gives rc 1, 1 CONFLICT, in both orders.
  - A far edit at line 20 gives rc 0 in both orders.

**Develop × head** (`scratch/mt.out`).
- rc 0 both orders, tree 1b6128cefd85 (= the READY). The merged blobs equal the head's.
- Patch-id of merge-vs-develop equals the head's own (1e7c7169a45b).
- 0 originate paths moved on develop since daa54a26; packages/ moved 2 test files only; 0 package*.json.
- Control: an edit on develop at the head's first changed line (:57) gives rc 1 in both orders.

**tsc and eslint** (`scratch/tsc_lint.out`).
- `tsc --noEmit -p services/originate/tsconfig.json`: rc 0 / 0 errors at develop and at the merge. A planted TS2322 gives rc 2 (1 error).
- eslint (root flat config, API) on certifications.ts and the ks1699 test file: 0 errors / 0 warnings at the merge and at develop. Planted `var` + `debugger` gives 2 errors. Restored to 473e968f72ed.

## HOW
- **Clone:** my own clone `scratch/clone`: `git init` plus alternates to the Blockchain object store and gate 363's and gate 356's clones (read-only). Fetched by `gh auth git-credential` (kksecura). Push URL DISABLED.
- **Worktrees:** sparse `wt-dev` (develop bbb75755), `wt-merge` and `wt-plant` (local probe f7b543fa8508), and `wt-head` (the raw head).
  - node_modules were APFS-cloned from gate 363's wt-dev (package*.json unchanged 2daedc20..bbb75755).
  - packages/shared was rebuilt in each tree (rc 0).
- **Local-only objects, no refs, never pushed:** the probe and control commits (author gate364).
- **TMPDIR:** `/Volumes/DevMASTER/WEDNESDAY/0_Brain/reference/g364t` (52 characters), plus a 125-character subfolder for the Q7 probe only.
- No writes outside this folder and g364t. No `cd`, no `rm`.

## NOT TESTED (UNMEASURED)
- A running stack, Postgres/RLS, a real gateway + originate pair, the real email send and anchoring. The cells use an in-process router, a mocked repository honouring the tenant, and a mocked `authenticate()`, as in round 1.
- The demo's tenant/company/ORG_ADMIN layout (G363-2239-2 remains Kam's to weigh).
- tsc over the test files (the READY's "4 pre-existing lines, 0 new" was not re-run). The docs-fragments checker, `check:test-types`, the pre-push hook end to end, Schemathesis, Akto, Playwright and k6.
- Linear: KS-1699's state was not read. The posting tool's `--dry` was not re-run.
- The builder's 16 plants were not re-run verbatim; my 32 runs measure the same classes independently.
- Node: the host's node (READY: 26.8.1, not LTS); not re-measured under an LTS line.
