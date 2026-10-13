VERDICT: GO WITH NOTE (0 Major, 1 Minor, 6 Info). Gate PR 1547 (KS-1594) fix round 1, DELTA, Opus tier 1
Report sha256/16: ccbe317fcbf769f3
(Recipe: delete this file's line 2, sha256 the rest, first 16 hex.)

- **Head gated:** `0f97a0157635690ee41d51bf620586e05fff65c2`. One commit; its parent is the round-1 head `a897f57e`.
- **Develop measured:** `026c2d1614065c79fc8d96007ac0d80f19fb9363` (the brief's base, where all the boundary work ran). Develop **moved during the gate** to `d53d80cbb2d50a5525c3d881a2da7a31eba67fb5` (KS-1032), and the merge prediction ran on that live tip (section 5).
- **How the shas were taken:** my own fetch into a `--shared` scratch clone (push URL `DISABLED`) plus `git ls-remote origin`, at 10:19:08Z and again at 10:38:07Z. The PR head was unmoved at both; develop moved once (`evidence/shas_start.txt`, `shas_end.txt`).
- **What I touched:** nothing inside `!CODING`. No push, no GitHub or Linear write, no Docker, no remote box. Every mutant edited the scratch worktree only, and each restore was asserted by sha256 (`814ba6c61ed5c077`).
- **Database:** my own throwaway PG 15.14 on **127.0.0.1:55471**. lsof on 55471 gave rc 1 (no listener); the same instrument saw the 5432 listener as a control. Listeners on 55416, 55418, 55440 and 55521 belong to others and I left them alone. Schema came from the repo's `docker/init/*` and then `scripts/run-migrations.sh`: `applied=51 failed=0`.
- **Roles:** the app connects as `secuura_app` (rolsuper f, rolbypassrls f). `svc_api_keys` has RLS and FORCE RLS on, and `organization_id` is nullable (`runs/pg_roles.txt`).
- **Build:** `npm ci --ignore-scripts` ran in both trees. I used the scripts flag because without it `blake2`'s node-gyp fails on this machine's SDK, and round 1's tree has no `blake2/build` either. `packages/shared` was rebuilt from source and `npm run generate` (Prisma) ran in both trees, rc 0 each.

---

## FOUND / TESTED / HOW, by brief step

### 1. The delta, a897f57e..0f97a015 (`evidence/delta.patch`)
**FOUND:** 2 files, nothing else. Instrument: `git diff --numstat`. The test file is +54/−0 and `adminConfig.ts` is +34/−7. Against develop it is still exactly 2 files.

**The hunks:**
- **H1** `adminConfig.ts @@ -945`: a comment-only change, "Both decisions" becomes "All three decisions".
- **H2** `adminConfig.ts @@ -954,18 +954,45` makes three changes:
  - It adds the m2 guard at **:961-966**: `organizationId` present, not null and not a string returns **400** `BAD_REQUEST`. The guard runs before `normaliseOrgId` and before any decision.
  - It moves rule (a) **after** normalisation, to **:987**: `isProvisioningCapable(requestedScopes) && !callerIsPlatform && requestedOrg === null` returns 403. `requestedOrg` is `normaliseOrgId(BODY organizationId)` (:969), with no fall-back to the claim.
  - It replaces (a)'s message with the security route's exact string.
  - (c) at :1000 and the write at :1020 (`requestedOrg ?? callerOrg`) are unchanged.
- **H3** test file `@@ -257,6 +257,60`: one new `describe` with:
  - c16: ORG_ADMIN(A1) + register + org A1 gives 201, bound to A1;
  - c17 ×4: array, object, number and boolean, each as SYSTEM_ADMIN, give 400 and 0 rows;
  - c18 ×2: super_admin and SUPER_ADMIN with register give 201.

**Result:** the code is exactly the rule the brief states.

### 2. Do the two doors give the same verdict? Re-read and then measured

**Re-read at develop 026c2d16:**
- **Security route condition:** `services/security/src/index.ts:1244-1247`. It is `isProvisioningCapable(scopes) && !isPlatformRole(role) && normaliseOrgId(data.organizationId ?? null) === null` → 403. The author's ":1239-1247" includes the tail of the comment block; the condition itself is at :1244-1247.
- **Same predicates and same body-only test.** That rule matches originate :987 term for term.
- **The org arm:** `decideTenantAccess` (`keyRevokePolicy.ts:198-247`) gives ORG_ADMIN/ISSUER_ADMIN these outcomes:
  - target null: allow;
  - caller org null: deny;
  - mismatch after normalisation: deny.
  Originate's (c) at :1000 gives the same outcomes for ORG_ADMIN.
- **The differences, from reading:**
  - Security parses with zod: `organizationId: z.string().optional()` (:659) and `scopes: z.array(z.string())` (:665). So security answers **400 for `null`** and for malformed `scopes`.
  - Security has a tenant floor; originate trusts `req.tenantId`.

**Measured.** I wrote a second harness, `gatetests/gate1547r2-securitydoor.integration.test.ts`:
- It drives the **real security app** at develop: `SECURITY_DISABLE_BOOT=1`, the same pattern as the repo's own KS-1584 cells, with RS256 tokens and the app running as `secuura_app`.
- It sends the **same** 10 admitted role/claim variants × 18 permission shapes (sent as `scopes`) × 18 organizationId shapes. That is **3240 requests**.
- I compared each request cell by cell against the originate head matrix. Instrument: `tools/doors.js`; output in `matrix/doors_head.txt`.

| bucket (security-door cells) | cells | same verdict class | allow/refuse differ | refusal code differ | stored org differs (both allow) |
|---|---|---|---|---|---|
| well-formed permissions × string or absent org | 1680 | **1680** | **0** | **0** | 232 (see i2) |
| non-string organizationId | 700 | **700** (all 400 at both) | 0 | 0 | 0 |
| `organizationId: null` | 140 | 0 | 120 | 20 | 0 (see i3) |
| malformed permissions (string, nested, `[null,…]`, object) | 720 | 200 | 395 | 125 | 0 (pre-existing, see i4) |

- **Control:** the same comparison against **develop's** originate finds **430** allow/refuse differences in the well-formed bucket.
- **Answer:** on every well-formed (role, permission, organizationId) shape, the two doors now give **the same verdict**.
- **Where they still differ:**
  - **`null`**: security gives 400, originate treats it as absent. That is the brief's own instruction.
  - **Malformed `permissions` arrays**: security gives 400, originate falls back or stores inert values. This is pre-existing.
  - **Which org is stored** when the body names none: originate binds to the claim, security stores NULL. This is the c9b choice accepted in round 1.
- **No escape in any difference:** none of them lets a non-platform caller store a provisioning-capable key that is org-less or foreign. The matrix below shows 0 such rows.

**The round-1 matrix, re-run on the new head.**
- **Harness:** the round-1 file, with the request unchanged. I only added `roleV`, `permV` and `orgV` to each result so the classifier can judge the BODY value.
- **Volume:** 19 roles × 18 permissions × 18 orgs, plus 2 tenant-header probes = **6158 requests per run**. I ran it 4 times: head and develop, each in MT=false and MT=true.
- **Classifier:** `tools/classify2.js`, updated to the ruled rule. It uses the head's own shared `isProvisioningCapable`, `normaliseOrgId` and `isPlatformRole`. It also carries an independent oracle of the rule that predicts status **and** stored org for every row.

| category (classify2.js) | head MT=f | head MT=t | develop MT=f (control) | develop MT=t | zero-control |
|---|---|---|---|---|---|
| FALSE PASS: non-platform 201, stored scopes provisioning-capable, stored org NULL | **0** | **0** | 80 | 80 | develop |
| FALSE PASS: non-platform 201, provisioning-capable, BODY org normalises to null (the ruled clause) | **0** | **0** | 251 | 251 | develop |
| FALSE PASS: non-platform 201 stored under an org ≠ its own claim (foreign) | **0** | **0** | 900 | 900 | develop |
| non-platform with an org claim stored NULL | **0** | **0** | 108 | 108 | develop |
| stored org not normalised | **0** | **0** | 1422 | 1422 | develop |
| FALSE REFUSAL: oracle says 201, got something else (admitted roles, header = token tenant) | **0** | **0** | 0 | 0 | R0 = round-1 code: **75**; R7: 155; perturbation: 1 |
| ORG_ADMIN naming its OWN org with a provisioning set: 201 bound to own | **75 / 75** | **75 / 75** | 75 | 75 | R0 (round-1 code): **0 / 75** (75 false refusals) |
| non-string org (900 cases, platform AND non-platform): not 400 | **0** | **0** | 900 | 900 | develop |
| non-string org: row written | **0** | **0** | 900 | 900 | develop |
| `null` vs absent: status or stored org differ (342 pairs) | **0** | **0** | 0 | 0 | R7 mutant: **180**; perturbation: 1 |
| row written on a refusal | **0** | **0** | 0 | 0 | perturbation: 1 |
| 5xx | **0** | **0** | 0 | 0 | perturbation: 1 |
| oracle mismatch (status or stored org), all 6156 same-tenant rows | **0** | **0** | 2568 | 2568 | develop |

- **The 75 own-org provisioning cases:** 3 own-claim spellings (A1, A1-UPPER, whitespace-A1) × 5 provisioning sets (register, `*`, `organizations:*`, read+register, `[null,register]`) × 5 own-org spellings (exact, upper, spaces, tab/newline, NBSP-wrapped). Any case or whitespace gives 201, stored as canonical lower-case A1.
- **Head status histogram:** 201 = 1766, 400 = 900, 403 = 3492. Among the same-tenant 201s, 1170 are platform (5 variants × 18 permissions × 13 non-malformed org shapes) and 595 are non-platform.
- **Tenancy modes:** MT=false and MT=true give identical status, stored org and scopes on all 6158 rows, in both trees. Control: a one-row perturbation is seen (`matrix/compare.txt`).
- **Perturbation controls:** each zero category goes 0 → 1 when one synthetic defect is planted in a copy of the head data (`tools/perturb.js`, `matrix/perturb_controls.txt`).

### 3. m2: non-string → 400 with no row, for platform AND non-platform; null and absent behave as absent

**TESTED in the matrix:**
- **900 non-string cases** across the 10 admitted variants: 5 platform and 5 ORG_ADMIN claim variants, × 18 permissions × 5 shapes (number, `[own]`, `[foreign]`, `{id}`, `true`). All are 400 and all write 0 rows, in both modes.
- **ORG_ADMIN with `[A2]`**, which round 1 found silently bound to A1, is now 400.
- **`null`:** 342 null/absent pairs are identical in status and stored org.
- **Platform + register + `null`:** gives 201 with org NULL, exactly like absent. That is the platform's intended org-less instance key.

**The gap:** the author's c17 cells exercise only a **platform** caller, and no cell sends `null`. See m1.

### 4. Mutants (`mutants/mutants_run.txt`, `mutants/summary.json`, `tools/mutants2.py`)

**Method:**
- Every mutant compiles (tsc rc 0) and every run loaded **23 of 23** cells.
- Each red cell's failure block was parsed. A kill counts only if every red block carries an Expected/Received pair or a thrown message.
- **Empty-message detector control:** X0 (a deliberate type error) loads as 23 red with **22 empty blocks**. The detector flags them, so a load failure cannot pass as a kill.
- **Comment-only control:** C0 leaves 23 of 23 green.
- **tsc control:** X0 gives rc 2 with TS2322.

| mutant (author's ten, re-spelled from their names) | red cells | result |
|---|---|---|
| T1 (a) disabled | c1 c2 c4 c5 | KILLED |
| T2 (a) platform test inverted | c1 c2 c4 c5 c14 c18 c18 | KILLED |
| T3 write not normalised | c8 c9 c9b c10 | KILLED |
| T4 (c) requested side raw | c8 | KILLED |
| T5 (c) disabled | c3 c6 | KILLED |
| T6 (c) caller side raw | c15 | KILLED |
| G7a (a) `requestedOrg === null` clause deleted (= round-1 rule a) | c16 | KILLED |
| G7b (a) clause inverted | c1 c2 c4 c5 c16 | KILLED |
| G8 platform = literal `SYSTEM_ADMIN` only | **c18 c18** (Expected 201 / Received 403) + c13 | KILLED **behaviourally**. The c18 messages are real, not a load failure. |
| M2m m2 guard removed | c17 ×4 | KILLED |

| mutant (gate's own) | red cells | result |
|---|---|---|
| R1 400 guard moved AFTER (a) and (c) | none | **SURVIVES** cells. The matrix kills it: 125 non-400. |
| R2 guard tests the NORMALISED value (dead guard) | c17 ×4 | KILLED |
| R3 (a) tests the raw body value's truthiness | c2 | KILLED |
| R4 (a) tests the post-fall-back value `requestedOrg ?? callerOrg` | c1 c2 c5 | KILLED |
| R5 platform check reads the BODY `role` (wrong field) | c10 c14 c18 c18 | KILLED |
| R6 platform check reads `user.organizationId` (wrong field) | c10 c14 c18 c18 | KILLED |
| R7 guard drops the null exemption (`null` → 400) | none | **SURVIVES** cells. The matrix kills it: 180 null≠absent, 155 false refusals. |
| R8 guard catches objects only | c17 (number, boolean) | KILLED |
| R9 guard only for platform callers | none | **SURVIVES** cells. The matrix kills it: 450 non-400, 325 rows written. |
| R10 guard only for non-platform callers | c17 ×4 | KILLED |
| R11 (a) only when MULTI_TENANCY_ENABLED=true | MT=f: c1 c2 c4 c5 · MT=t: none | KILLED in MT=false only, so both modes stay required |
| R0 whole file = round-1 code a897f57e (red-first control) | c16 c17 ×4 | **5 failed**, matching the author's "red-first 5 failed" |
| X0 type error / C0 comment-only | all 23 (22 empty) / none | controls |

- **Author's claims:** all ten are confirmed as kills carrying real messages.
- **Three gate mutants survive the cells:** R1, R7 and R9 (m1).
- **None of the three is a false pass:** in each, the matrix FALSE PASS categories stay at 0, and the deviations are status codes or own-org rows only.

### 5. Merge prediction on the live develop tip d53d80cb

- **Overlap:** develop moved 026c2d16 → d53d80cb, one commit (KS-1032), touching 10 files. Overlap with the PR's 2 files is **0**. Instrument: `comm -12` on sorted name lists. Planted control (adminConfig.ts added to develop's list): **1** (`evidence/merge_overlap.txt`).
- **merge-tree:** `git merge-tree --write-tree d53d80cb 0f97a015` gives rc 0, a clean tree `2ee82f7a`.
- **Negative control:** a scratch commit on d53d80cb that edits the develop-side `const orgId` line the PR replaces. Running `merge-tree` against it gives rc 1 and `CONFLICT (content)` in adminConfig.ts (`merge_tree_negctl.txt`).
- **Predicted merged tree (b4ebb448, scratch only):**
  - tsc rc 0;
  - KS-1594 cells **23/23 in MT=false and 23/23 in MT=true**;
  - originate unit suite **107 suites / 1337 tests passed**. KS-1032 adds 2 suites; the head and develop alone give 105/1321 each.

---

## Findings

### m1: Minor. The m2 rule and the null-as-absent rule are each pinned for one caller class only, so three mutants survive the 23 cells

- **Where:** test file `ks1594-admin-mint-provisioning-and-org-bound.integration.test.ts:292-293`. All four c17 shapes use `tok('SYSTEM_ADMIN')`. No cell sends `organizationId: null`: `grep -i` finds 0 such calls, with 16 `mint(` calls found by the same instrument as the control.
- **The survivors:**
  - **R9** (the guard narrowed to platform callers): an ORG_ADMIN `[A2]` request is again silently treated as absent, giving 201 bound to its own org. That is the round-1 m2 behaviour for ORG_ADMIN.
  - **R1** (the guard after the decisions): an ORG_ADMIN sending a non-string gets 403, not 400.
  - **R7** (`null` refused as 400): this breaks the brief's "null and absent still behave as absent".
- **Why it is Minor:** the implementation is correct today (matrix: 0 of 900 non-400, 0 of 342 null/absent differences), and none of the survivors creates a false pass. The cells simply do not hold the line the brief asks for, "platform AND non-platform".
- **Minimal fix:** add two cells:
  - ORG_ADMIN(A1), `permissions:['organizations:register']`, `organizationId:[A2]` → 400 and 0 rows;
  - SYSTEM_ADMIN or ORG_ADMIN(A1), `organizationId:null`, `permissions:['read']` → the same status and stored org as with the field absent.
- **Can ride:** later. It does not block.

### Info

- **i1. The doors agree.** On the 1680 well-formed shapes, the security route at develop and originate at the head give the same verdict class: 0 allow/refuse and 0 refusal-code differences. Against develop's originate the same comparison finds 430 differences. Kam's ruling b is now the rule at both doors.
- **i2. Stored org when the body names none.**
  - **What differs:** 232 cells where both doors allow but originate stores the caller's claim while security stores NULL.
  - **Breakdown:** 176 are ORG_ADMIN (the c9b choice, accepted in round 1). 56 are platform tokens that carry an org claim (SYSTEM_ADMIN(A1) and super_admin(A1)): originate binds their key to the claim where security mints a tenant-level key.
  - **Assessment:** this is the pre-existing `body || claim` default, and it is stricter, never looser. Platform S's org-less token still stores NULL.
- **i3. `null` is 400 at security and treated as absent at originate.** 180 cells differ. This follows the brief's instruction, and with a provisioning set a non-platform `null` is still 403 at originate. It is fail-closed on the class that matters.
- **i4. Malformed `permissions`** (a string, nested arrays, `[null,…]`, an object) are 400 at security. At originate they fall back to `['read']` or are stored inertly. This is round 1's i5 and pre-existing. The classifier finds 0 non-platform rows with provisioning-capable stored scopes.
- **i5. The tenant floor now covers the provisioning class.**
  - **On the gated head:** I sent ORG_ADMIN(A1) + register + `organizationId: A1` with a forged `x-tenant-id: T2` **directly to the router**. It gives **201, stored in tenant T2**, bound to A1 (`matrix/t2probe.txt`).
  - **For comparison:** round-1 code refused it, since (a) banned all ORG_ADMIN provisioning mints; develop at 026c2d16 gives 201 too; the security route would refuse it as cross-tenant.
  - **Why it is Info:** it is pre-existing (round 1's i1), and the m1 relaxation was the ruled change.
  - **What KS-1032 changes, by reading only:** **KS-1032, now on live develop d53d80cb**, makes `gatewayProvenance` strip trust headers whenever `GATEWAY_VOUCH_SECRET` is unset (fail-closed). The KS-458 resolution also reads `x-tenant-id` only on a vouched request. So on the merged tree this direct-forgery path is closed **by reading**. My harness mounts the router without `index.ts`'s middleware, so this is not tested end to end.
- **i6. The brief's line reference.** The author's ":1239-1247" is the comment tail plus the condition; the condition is at :1244-1247. Nothing turns on it.

## NOT tested

| not tested | why | could it hide a Major? |
|---|---|---|
| Hop 2 end to end: a key minted here then calling register-connector on a live gateway | no stack or Docker, by rule | Low. Stored scopes are judged with the gateway's own predicate, and an ORG_ADMIN key is now always bound to its own org. |
| The gateway → originate path with `GATEWAY_VOUCH_SECRET` set or unset, i.e. KS-1032 on the merged tree end to end | the harness mounts the router only | Not for this diff. It bears on i5 (pre-existing tenant trust). |
| The security-door matrix on the live tip d53d80cb | it ran at 026c2d16 | No. KS-1032 touches no security-service file (`dev_moved_files.txt`). |
| `perTenantDb=true` | shared-database harness | Low. The decisions run before any database call. |
| Live or demo `svc_api_keys` nullability | no live access | Not a code Major. It is a deploy-seat check (unchanged from round 1). |
| The live PR body and the Linear linkKind | no gh or Linear read path in scope | Paperwork only. I did not check whether the body now cites Kam's 12:55 ruling b (round-1 m1's ask); the code comment at :976-980 does cite it. |
| Schemathesis, Akto, Playwright, k6 | no Docker | Low. The route is in no OpenAPI spec. |
| Unit suite sensitivity | it was not re-run against mutants this round | Round 1 showed it cannot see this behaviour; the integration cells and the matrix are the pins. |

**Gate verdict: GO WITH NOTE for `0f97a0157635690ee41d51bf620586e05fff65c2`.**
- **Round-1 findings:** m1 (the ruling) is fixed; the doors now agree on every well-formed shape. m2 (malformed org) is fixed for both caller classes, as measured. m3 (alias cells) is fixed; G8 is killed behaviourally.
- **The note:** m1 here asks for two more cells (non-platform non-string, and null). It can ride this PR or the next.
- **Merge:** clean on live develop d53d80cb, with the merged tree green.
- **Deploy:** only in the KS-1570 round. Merge only on Wednesday's head-bound GO.
