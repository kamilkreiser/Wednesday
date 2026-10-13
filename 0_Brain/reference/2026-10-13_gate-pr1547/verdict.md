# Gate verdict: PR 1547 (KS-1594), originate POST /api/admin/api-keys. Opus tier 1
Report sha256/16: c7a359227342f0b6
(Recipe: delete this file's line 2, sha256 the rest, first 16 hex.)

**VERDICT: GO WITH NOTE**: 0 Major, 3 Minor, 9 Info.

- **Head gated:** `a897f57eba3d39afd8fd19e2895cb0e83188ab58`. This is one commit whose parent is develop.
- **Develop measured:** `026c2d1614065c79fc8d96007ac0d80f19fb9363`.
- **How the shas were taken:** my own fetch into a `--shared` scratch clone, with push disabled, plus `git ls-remote origin`. Both shas were unmoved at the end of the run (`evidence/shas.txt`).
- **What I touched:** nothing was written inside `!CODING`. There was no push, no GitHub or Linear write, no Docker and no remote box.
- **Database:** my own throwaway PG 15.14 on **127.0.0.1:55463**. I checked it with lsof first: 0 listeners. The other gates were listening on 55416, 55418, 55440 and 55521, and I left them alone.
- **Schema:** built by the repo's own `docker/init/*` then `scripts/run-migrations.sh`, giving `applied=51 failed=0` (`evidence/runs/pgsetup_head.txt`).
- **Roles and RLS:** the app connects as `secuura_app` (rolsuper f, rolbypassrls f). `svc_api_keys` has relrowsecurity t and relforcerowsecurity t (`evidence/runs/pg_roles.txt`).
- **Build steps:** `npm ci` ran in both trees. `packages/shared` was rebuilt from source in both trees. `npm run generate` ran in both trees, so the Prisma client exists (KS-1305) (`evidence/runs/`).

The Minor items need a word, not a rework. **m1** is a divergence from a ruling that Wednesday approved but the PR does not name. **m2** is malformed-input handling on the platform arm. **m3** is two mutants that survive the cells. None of them is a false pass for a non-platform caller.

---

## 1. The 16 cells: head and develop, both tenancy modes

Instrument: jest `jest.integration.config.js`, the author's file run unchanged. Driven by `evidence/tools/orig.sh`.

| tree | MULTI_TENANCY_ENABLED=false | =true |
|---|---|---|
| head a897f57e | **16 passed / 16** | **16 passed / 16** |
| develop 026c2d16 (cell file copied in) | **11 failed, 5 passed** | **11 failed, 5 passed** |

- **Develop reds:** c1–c6 `Received: 201` (403 expected). c8, c9, c9b and c10 store the raw string. c13 fails because the predicates are absent.
- **Develop passes:** c7, c11, c12, c14 and c15. This agrees with the author's "11 failed / 3 passed" on 14 cells: c14 and c15 were added later and pass before the fix by design.
- **The reds are wrong values, not errors:** `Received: 500` appears 0 times. Control: `Received: 201` appears 6 times in the same file (`evidence/runs/cells_dev_mtfalse.txt`).
- **Controls that the harness can fail:**
  - develop itself (11 red);
  - X0, a deliberate type error, which gives 16 of 16 red as a load failure;
  - the mutants in section 6.

**Originate unit suite** (jest default config):
- Head and develop both give **105 suites, 1321 tests, all passed**, rc 0 (`runs/unit_{head,dev}.txt`).
- Control: with X0 applied, the two suites that import adminConfig fail (2 failed, rc 1).
- The unit suite **does not pin this behaviour**. Mutant T3 passes it 29/29 (`runs/` and `mutants/unit_control_*`), so it is a regression check only.

**tsc** (`npx tsc --noEmit -p tsconfig.json`, services/originate):
- rc 0 on head and on develop.
- Control: X0 gives rc 2 with TS2322.

## 2. Caller survey, re-derived (`evidence/caller_survey.txt`)

Instrument: `git grep -i` over the whole repo at the head. Three patterns:
- `admin[/\\._-]+api[-_]?keys`;
- a bare `'api-keys'` path segment;
- `admin` within 80 characters of `api-keys` on the same line.

**FOUND: the same five POST callers the author lists, and no others:**
- `setup_api_key.py`;
- `test_tenant_isolation_writes.py` (relative `/admin/api-keys`);
- `repro-api-keys.sh`;
- `ks-4-phase5b-reconcile.api.spec.ts`;
- `ks1206…test.ts`.

| caller file | organizationId lines | organizations: lines |
|---|---|---|
| each of the 5 files | **0** (the one hit in the e2e spec is a comment at :387) | **0** |

- **Control:** the same instrument finds 12 lines in the KS-1594 cell file.
- **Admin frontend:** `frontend/admin/src/services/api.ts:396,411,430` all target `/api/security/keys`. The only `'api-keys'` hits in the frontend are a tab id (`ClientDetail.tsx:45,355`).
- **Inline runner:** `systemTest/inline-runner/runner.js` p11 calls `GET /api/api-keys`, not this route.
- **Other services:** zero server-side callers.

**Outside the repo, plausibly affected:** any human or ops script holding an ORG_ADMIN JWT that posts `organizationId`, through the gateway (`/api/admin` is proxied, `api-gateway/src/index.ts:392`). The repo itself states that 10 of 10 org-bounded accounts are org-less (keyRevokePolicy.ts comment). For such a token, **every** non-blank `organizationId` is now 403. On develop it was 201 for any organisation. Org-less tenant-level mints still work. Platform S is steered away from this route by the client-facing doc.

## 3. THE BOUNDARY

### Matrix design (`evidence/gatetests/gate1547-matrix.integration.test.ts`)

**Wiring:** the same as the author's cells. That is the real router, real RS256 `authenticate`, real `requireRole`, `extractTenantContext` in MT mode, the KS-458 resolver and `tenantGucContext`, with the app running as `secuura_app`.

**The 19 role/claim variants:**
- ORG_ADMIN, with claim A1, none, A1-UPPER, whitespace-A1, or blank;
- SYSTEM_ADMIN, with claim none or A1;
- SUPER_ADMIN;
- super_admin, with claim none or A1;
- system_admin (lower case);
- org_admin (lower case);
- ADMIN;
- ISSUER_ADMIN;
- platform_admin;
- connector;
- `SYSTEM_ADMıN` (dotless i);
- the role as an array `['SUPER_ADMIN']`;
- `' ORG_ADMIN'` (leading space).

**The 18 permission shapes:**
- absent;
- read;
- documents:*;
- register;
- `*`;
- `organizations:*`;
- `ORGANIZATIONS:REGISTER`;
- `' organizations:register '`;
- `Organizations:*`;
- `'* '`;
- read+register;
- the string `'organizations:register'`;
- nested `[['organizations:register']]`;
- `[null,'organizations:register']`;
- `[]`;
- an object;
- `'read organizations:register'`;
- `'read,organizations:register'`.

**The 18 organizationId shapes:**
- absent;
- own;
- own in upper case;
- own with surrounding spaces;
- own with tab and newline;
- foreign;
- foreign in upper case;
- `''`;
- `'   '`;
- a lone NBSP;
- own wrapped in NBSP;
- own prefixed with ZWSP;
- `null`;
- `12345`;
- `[own]`;
- `[foreign]`;
- `{id:foreign}`;
- `true`.

**Volume:** each run sends 6156 requests, plus 2 tenant-header probes, for **6158** in all. I ran it 4 times: head and develop, each in MT=false and MT=true.

**Classifier** (`evidence/tools/classify.js`): it judges each **stored row** with the head's own shared `isProvisioningCapable` and `normaliseOrgId`. `isProvisioningCapable` is the same predicate the gateway's `requireOrgProvisioner` (platform.ts:107) and `decideTenantAccess` (keyRevokePolicy.ts:298) grant on. Scopes reach the gateway unchanged: `parseJsonArray` (security converters.ts:94) passes arrays through as they are, and nothing on the path lower-cases, trims or flattens scopes (`git grep` over services/packages finds 0 such call sites).

### Results by classifier category

| category (classifier) | head MT=f | head MT=t | develop MT=f (control) | develop MT=t |
|---|---|---|---|---|
| FALSE PASS: non-platform 201 whose stored scopes are provisioning-capable | **0** | **0** | 451 | 451 |
| FALSE PASS: non-platform 201 stored under an org ≠ its own claim | **0** | **0** | 900 | 900 |
| stored org not in normalised form | **0** | **0** | 1422 | 1422 |
| non-platform with an org claim, stored NULL | **0** | **0** | 108 | 108 |
| 5xx | **0** | **0** | 0 | 0 |
| a row written on a refusal | **0** | **0** | 0 | 0 |
| FALSE REFUSAL (raw / after excluding claimless callers) | 130 / **0** | 130 / **0** | 0 | 0 |

- **The 130 raw entries:** these are ORG_ADMIN tokens with **no or a blank claim** naming A1, and every one is a 403 "organizationId must be your own organisation". A1 is not their organisation. This is the same verdict the security route gives (`caller has no organisation`). They are a classifier artefact, not a false refusal.
- **True legitimate set:**
  - ORG_ADMIN with claim A1, A1-UPPER or ws-A1, crossed with 13 non-provisioning permission shapes and 10 legitimate org shapes, gives 390 cases. All 390 returned 201 and stored canonical A1.
  - Every platform variant (5 role variants × 324 requests) returned 201 for every permission and org shape. That is 1620 cases.
- **Tenancy modes:** MT=false and MT=true give **identical** status and stored org on all 6158 rows, in both trees. Control: a one-row perturbation is detected (`matrix/compare.txt`).
- **Admission (requireRole, auth.ts:149-150):** only `SYSTEM_ADMIN`, `ORG_ADMIN`, `super_admin` and `SUPER_ADMIN` reach the handler. Nine variants are 403 at requireRole on 324 of 324 requests each: lower-case system_admin and org_admin, ADMIN, ISSUER_ADMIN, platform_admin, connector, dotless i, array role and space-padded role. `isPlatformRole` is true for exactly the three admitted platform spellings and false for ORG_ADMIN.

### Do the wildcards and case variants behave as the cells assume?

**TESTED:** yes. `hasScope` (scopes.ts:151) is exact-match plus `*` plus `<resource>:*`:
- `*` and `organizations:*` give 403 for ORG_ADMIN.
- `ORGANIZATIONS:REGISTER`, `' organizations:register '`, `Organizations:*`, `'* '`, a nested array and space- or comma-joined strings are **201 and stored verbatim**. Each is inert, because every grant site matches exactly (classifier: 0 provisioning-capable).
- `[null,'organizations:register']` gives 403 (the filter drops the null and the register scope is still seen).
- A string or object `permissions` falls back to `['read']`.

## 4. Sibling doors: writers of svc_api_keys (`evidence/writers_svc_api_keys.txt`)

Instrument: `git grep -i` for INSERT/UPDATE/COPY on `svc_api_keys` in non-test source. Control: 53 total `svc_api_keys` lines across services/packages.

- **Key-creating writers:** exactly two.
  - Security `apiKeyInsertStatement` (index.ts:420). It is reached only from `POST /api/keys` (:1161, :1394, behind decideMint, the KS-1584 hop-1 deny and `decideTenantAccess`) and from the revoke upsert (:1566, an existing row).
  - This route (adminConfig.ts:1004).
- **Migration:** 019 is a one-time legacy copy.
- **Other UPDATEs:** they only deactivate keys or record usage (adminConfig:1130, connectorOrganisationErasure:440, security :218/:224/:499).
- **Tenant-provisioning:** writes nothing to this table; it only mentions it in comments.
- **Validation path:** `security_find_api_key_by_hash` reads svc_api_keys only.

**Result: no third door.**

## 5. The c9b choice, and ADMIN against Kam's rulings

**c9b is accepted.**
- c9 and c9b are **one rule**: blank is absent (b), and absent falls back to the caller's own claim. The developer default, `body || claim`, already did that fallback.
- c9 stores NULL only because that SYSTEM_ADMIN token carries no organisation. Measured: SYSTEM_ADMIN(A1) with `'   '` stores A1 (`matrix/platform_and_orgless_rows.txt`).
- For an ORG_ADMIN, the result is the key **bounded to its own organisation**. That is what Kam's 11:47 ruling (explicit organisation scope) and 12:55 ruling ("bound … to the minting admin's own scope") point to, and it is stricter than the security route, which would store a tenant-level key.
- The PR body's sentence "a platform caller passing `'   '` stores NULL" is true only for an org-less platform token (i3).

**ADMIN** is refused by `requireRole` (324 of 324 requests), so this PR adds no ADMIN door. The 09:53 note ("needs to be changed before deployment") is untouched here and remains with KS-1570 and the security route (DEPLOY-BLOCKERS row `ks1533-admin-bounded`). This is consistent with that note.

## 6. Mutants (`evidence/mutants/`, `tools/mutants.py`)

**Method:**
- Each mutant edits the **scratch** head's adminConfig.ts.
- Each runs `tsc` first, then the 16 cells in MT=false. G4 also runs in MT=true.
- Each restore was asserted by sha256 (`46a0df1696b3eb12`).
- Every run loaded 16 of 16 cells.

| mutant | tsc | red cells | result |
|---|---|---|---|
| T1 (a) disabled | – | c1 c2 c4 c5 | KILLED (c3 survives: (c) refuses it on its own, as the author says) |
| T2 (a) platform test inverted | – | c1 c2 c4 c5 c14 | KILLED |
| T3 write not normalised | – | c8 c9 c9b c10 | KILLED |
| T4 (c) requested side raw | – | c8 | KILLED (the author reports c8–c10; that is a different spelling of the mutant) |
| T5 (c) disabled | – | **c6 only** | KILLED, matches the author |
| T6 (c) caller side raw | – | c15 | KILLED |
| G1 hasScope → exact `includes('organizations:register')` | 0 | c5 (+c13) | KILLED by c5 |
| G2 platform check on `user.tenantId` | – | c10 c14 | KILLED |
| G3 (a)'s 403 moved AFTER the INSERT | – | c1 c2 c4 c5 (row-count assert) | KILLED |
| G4 (c) only when MULTI_TENANCY_ENABLED=true | – | MT=f: c6 · MT=t: none | KILLED in MT=false only, which is why both modes are required |
| G5 blank body org stores NULL, not the claim | – | c9b | KILLED |
| G6 (c) nested under (a) | – | c6 | KILLED |
| **G7 (a) waived when the ORG_ADMIN names an organisation** | 0 | **none, 16/16 pass** | **SURVIVES** (m1, m3) |
| **G8 platform = literal `SYSTEM_ADMIN` only** | 0 | c13 only (a source-text guard) | **SURVIVES behaviourally** (m3) |
| G9 normalisation trims only (keeps case) | 0 | c8 c15 (+c13) | KILLED |
| X0 deliberate type error (tsc and harness control) | **2** | all 16 (load failure) | control |
| C0 comment-only | – | none | control, 16/16 |

**Note on first-batch load failures:** G1, G7, G8 and G9 first loaded as 16 of 16 red. That was a TS6133 unused-import load failure, which proves nothing. I re-spelled them so they compile (tsc rc 0) before reading the result (`mutants_run2.txt`).

## 7. Scope and paperwork

**Diff vs develop:** exactly 2 files.
- `adminConfig.ts` +49/−5.
- The new test file +291/−0.
- One commit, parent `026c2d16` (`scope_numstat.txt`).

**PR body:**
- `gh pr view` failed: no gh auth in the project's config, and I did not look for other credentials. **I did not read the live body.** I read the author's local copy, `5_Project_History/2026-10-13_seatV-8th/logs/pr_ks1594_body.md`.
- The body is accurate against the code and against my numbers, except for the c9 wording (i3) and the T4 red set (i7).
- It does **not** mention Kam's 12:55 "Allow it, but bound" ruling (m1).

**Closing keywords:** 0 in both the commit message and the body. Instrument: `close[sd]?|fix(e[sd])?|resolve[sd]?` followed by `KS-|#`. Control: a synthetic "Closes KS-1594" line gives 1. "Refs KS-1594" appears once in the commit and twice in the body.

**Linear linkKind:** **NOT read.** I had no read path within scope. The author reports `contributes` (attachment `1c2dd1ec…`). That is a claim, not verified.

**Brief's line reference:** the brief cites `requireRole` at ":38". At the head it is at **:45** (the import block grew).

## 8. Findings

### m1: Minor. Rule (a) is stricter than Kam's 12:55 ruling, and the PR does not say so

- **Where:** `adminConfig.ts:959`.
- **What happens:** ORG_ADMIN(A1) with a provisioning-capable set and `organizationId: A1` (its own) gets **403** (matrix, both modes).
- **Why it matters:**
  - Card `secuura-provisioning-scope-escapes-the-org-bound` was ruled **b, "Allow it, but bound the provisioning key to the minting admin's own scope"**. That ruling rejected rec a, "only platform roles", which is what (a) implements at this door.
  - The security route follows b. The same caller and request is admitted there with an organisation bound.
  - Wednesday's 09:05 plan confirmation approved (a) as written, so this is a ruled lane. But no artefact records that this door is deliberately stricter than Kam's word.
- **Risk:** fail-closed, and no in-repo caller loses anything (section 2).
- **Minimal fix:**
  - **Either** Wednesday tells Kam in one line that originate refuses provisioning mints from non-platform roles outright and the security route is the only door, and records it in the PR body.
  - **Or** relax (a) to `isProvisioningCapable && !platform && requestedOrg === null`, so the PR follows b. That relaxation is exactly mutant G7, which already passes all 16 cells.
- **Either way, pin the choice with a cell:** ORG_ADMIN(A1) + register + organizationId A1 → the intended status.

### m2: Minor. A non-string organizationId is silently treated as absent, which turns a malformed platform request into an UNBOUNDED provisioning key

- **Where:** `adminConfig.ts:971-972` and `:991`. `normaliseOrgId` returns null for any non-string.
- **Reproducing shape:** SYSTEM_ADMIN (no organisation claim), `permissions:['organizations:register']`, with `organizationId` set to `[A2]`, `{id:A2}`, `12345` or `true`.
  - **Head:** 201, `organization_id = NULL`. That is the org-less, platform-minted, unbounded provisioning-key shape (keyRevokePolicy.ts:290 treats it as unbounded).
  - **Develop:** stored the garbage string, for example `'{"…a2"}'`, a non-null value that bounds the key to a non-existent organisation.
- **For ORG_ADMIN:** `[A2]` gives 201, silently bound to its own A1 instead of being refused.
- **Severity:** platform-only reachability, and a platform caller can ask for an unbounded key outright. So this is Minor, not Major. It is still a fail-open on malformed input on the one key class whose unboundedness matters.
- **Minimal fix:** before normalising, `if (d.organizationId !== undefined && d.organizationId !== null && typeof d.organizationId !== 'string') return 400`. Add one cell (platform + register + `[A2]` → 400 and no row).

### m3: Minor. Two mutants survive the 16 cells

- **G7** (see m1): no cell has an ORG_ADMIN naming its *own* organisation with a provisioning set.
- **G8:** no cell uses `super_admin` or `SUPER_ADMIN`. A change that dropped them from the platform test would be caught only by c13's source-text guard, and only because the call name vanished. A spelling such as `isPlatformRole(role) && role === 'SYSTEM_ADMIN'` would pass all 16.
- **Context:** my matrix pins both today. Platform aliases give 201 in all 1620 cases, and G7's behaviour gives 403 on the head.
- **Minimal fix:** add the two cells.

### Info

- **i1. Tenant floor.** The route trusts `req.tenantId`; it is not a `decideTenantAccess` call. Probe with token tenant T and `x-tenant-id` T2, directly to originate: a read key is minted **in T2** on both head and develop, while the register probe is 403 on head. This is pre-existing and outside the diff. Through the gateway the header is set from the JWT, with an override only for super-admin roles (`api-gateway/src/middleware/auth.ts:514-523`). Originate strips unvouched trust headers only when `GATEWAY_VOUCH_SECRET` is set (fail-open when it is unset).
- **i2. KS-1591 (upper-casing `isPlatformRole`)** is **not reachable on this route**. `requireRole` matches exactly, and the dotless-i, array and padded roles are 403 there (324 of 324 each).
- **i3. PR-body wording on c9.** The NULL comes from the org-less platform token, not from a separate platform rule (section 5).
- **i4. ADMIN and ISSUER_ADMIN** never reach the handler, so the ADMIN note in DEPLOY-BLOCKERS is unaffected.
- **i5. No `validateScopes` here.** Inert spellings such as `ORGANIZATIONS:REGISTER`, padded strings and nested arrays are stored. This is pre-existing and harmless at every grant site measured; it is a hygiene item, not a door.
- **i6. ZWSP is not folded by `normaliseOrgId`.** For ORG_ADMIN this is fail-closed (403). A platform caller stores a ZWSP-prefixed organisation, which bounds the key to nothing real.
- **i7. Mutant spelling.** The author's T4 red set differs from mine because the mutant is spelled differently. Both are killed.
- **i8. Line reference.** The brief's ":38" is ":45" at the head.
- **i9. Unit suite.** It cannot see this behaviour (T3 passes it). The integration cells are the only pin.

## 9. NOT tested, and whether each could hide a Major

| not tested | why | could it hide a Major? |
|---|---|---|
| Hop 2 end to end (a key minted here then calling `register-connector` on a live gateway) | no Docker or stack, per the ruling | Low. The stored-scope classifier uses the exact predicate the gateway grants on, and scopes are passed through untransformed (read at source). |
| Schemathesis, Akto, Playwright, k6, preflight legs 3/4/8 | Docker down; Wednesday ruled no Docker | Low. The route is in no OpenAPI spec, so Schemathesis would not generate it anyway. |
| The gateway → originate path with real `GATEWAY_VOUCH_SECRET` and header stripping | no stack | Not for this diff. It bears on i1 (pre-existing tenant trust). |
| `perTenantDb=true` (a separate database per tenant) | harness runs a shared database | Low. The decision code runs before any database call, and the INSERT is the same statement. |
| Live or demo `svc_api_keys` nullability (c12 measured on my repo-built database only) | no live access, by rule | Not a Major in code. A failed 018 ALTER would make (b)'s NULL write a 500 (fail-closed). That is a deploy-seat check. |
| The live PR body, and the Linear linkKind | no gh auth; no Linear read path | Not for code. Paperwork only. |
| Production `express` body parsers other than JSON (for example a urlencoded array) | harness uses JSON | Low. Non-string shapes were tested directly (m2). |

**Gate verdict: GO WITH NOTE.** The note is m1, to acknowledge or align with Kam's 12:55 ruling. m2 and m3 are cheap follow-ups and can ride in this PR or the next one. This change deploys only in the KS-1570 round, never on its own. Merge only on Wednesday's head-bound GO for `a897f57e`.
