VERDICT: GO WITH NOTE at head d7c2e296c909... (tier 1, round 1 of 2; landing tree 9497977aaa7a on develop f01ba49da56d; 0 blockers, 5 notes)

## BLUF
- **The bound is correct and complete on the three GETs.** It holds on the real router over the REAL `certificationRepo.getCertification` / `fromDbRow` SQL, run against an in-process Postgres (PGlite). Every reader that is not the issuer, the holder or a platform admin gets 404 on `GET /:id`, `/:id/lineage` and `/:id/evidence-bundle`. That covers same-tenant readers of the same organisation (a) and of ANOTHER organisation (a2), i.e. every same-tenant user of ANY organisation. The issuing connector (c) keeps 200 on its own holder-less certification on all three routes. Another tenant (b) gets 404.
- **The refusal is byte-identical to the unknown-id 404 on each of the three routes.** A refused reader causes no expiry save, no share lookup, no lineage read, no charge read and no `evidence_export` charge.
- **None of my break attempts got through:** prefix, suffix and case variants of the ids; an empty, missing or non-string userId; no `req.user`; odd admin spellings.
- **Heads unchanged start to end. The landing reproduces. The suite is +23 by name with 0 vanished.** I re-ran 5 of the author's mutants and added 2 of my own (7 built, 7 killed). Both of mine **survive the author's 23 cells** (N3).
- **Notes, not blockers:**
  - (N1) `POST /:id/verify` and `/:id/recertify`, which this PR does not touch, still give a refused reader the record's existence, its issuer and (through recertify) its holder.
  - (N2) Platform roles `SUPER_ADMIN` and `platform_admin` lose the by-id read.
  - (N3) Two gaps in the author's suite.
  - (N4) The legacy E2E transfer cell would go red.
  - (N5) Platform S non-issuer reads are still reported, not measured.

## Findings

**Q1 scope and product diff (read whole).**
- Three-dot against live develop: 2 files, **+398/-3** (`routes/certifications.ts` +65/-3 and the new `__tests__/ks1695-…test.ts` +336). No migration, config or dependency changes.
- The admit rule is `callerMayReadCertification` (`certifications.ts:154-162` at the head):
  - It admits a role in exactly `system_admin | SYSTEM_ADMIN | super_admin`.
  - Otherwise, `userId` is the string `req.user.userId` or `''`, and `''` returns false.
  - Then it admits `userId === issuer?.id` or `userId === holder?.id`.
  - This is exactly `platform admin || (userId !== '' && userId === issuer.id) || (userId !== '' && userId === holder.id)`. The admin set equals the list route's `isAdmin` (`:947`).
- Refusal: all three routes return through one `certificationNotFound(res)`, the same function the unknown-id branch now uses. The body is `{"success":false,"error":{"code":"NOT_FOUND","message":"Certification not found"}}`, asserted literally in G6.
- Ordering:
  - On `GET /:id` the check (`:1017`) precedes the expiry `saveCertification` (`:1022-1025`).
  - On lineage (`:1477`) it precedes `getSharesByCertification` (`:1482`).
  - On evidence-bundle (`:1564`) it precedes every read and `createChargeEvent('evidence_export')` (`:1575`).
- The 22P02 catch on `GET /:id` (`:1052`) still writes the same body inline. It is byte-identical today but outside the helper.

**Q2 audience, measured.**
- **What the author's harness proves:** it runs the real router and real handler logic over a mocked `getCertification` that honours the tenant in JS. It pins the handler's decisions, not the SQL or the row mapping.
- **What my file adds:** `gatecf1-pglite.test.ts` (scratchpad, not in the PR). It runs the real router plus the REAL `getCertification` SQL (`WHERE id = $1::uuid AND tenant_id = $2::uuid`) and the REAL `fromDbRow` against PGlite. It seeds rows shaped as the repo writes them:
  - a human cert (UUID columns set);
  - a KS-1659 holder-less connector cert (UUID columns NULL, `certification_metadata.issuerId = holderId = 'connector:platform-s:…'`);
  - a bare `document` row (all actor fields NULL);
  - an expired cert.
- **G0 (control):** the real mapper yields the connector principal for both ids, and `''`/`''` for the bare row.
- Measured on all three routes:
  - Human cert: a = 404, a2 = 404, issuer = 200, holder = 200 (G1). b (other tenant) = 404, and so is the issuer itself when calling from the other tenant, because the tenant wall comes first (G2).
  - Holder-less connector cert: c = 200, a = 404, a2 = 404, and a DIFFERENT connector id = 404. c on the human cert = 404 (G2).
- The audience was every same-tenant user of ANY organisation (a and a2 both 200, as in BX1's N2 rows). It is now issuer, holder and platform admin only.
- **Still not proven:** a real gateway, a real JWT, or real role and organisation claims. a and a2 are distinguished only by id here, because the handler reads no organisation.

**Q3 break attempts (all on the real SQL, all three routes, each zero with a positive control):**
- **Id variants:** `ISSUER[0:8]`, `ISSUER` minus 1 char, `ISSUER+'a'`, `ISSUER.toUpperCase()` and `' '+ISSUER` → 404. Connector-id variants `connector:platform-s`, an upper-cased connector id, `+':x'` and a truncated id → 404. Control: the exact issuer → 200 (G3).
- **Bare row (issuer = holder = `''`):** userId `''`, `undefined`, `null`, `0`, `false` or `[]`, a user with no `userId` key, no `req.user` at all, and reader a → 404 on all three. Control: a platform admin with `userId: ''` → 200 (G4).
- **Role spellings:** `system_admin`, `SYSTEM_ADMIN` and `super_admin` → 200. `ORG_ADMIN`, `SUPER_ADMIN`, `Super_Admin`, `platform_admin`, `admin`, `ADMIN`, `system-admin`, `' system_admin'`, `ISSUER_ADMIN`, `OWNER` and `connector` → 404 (G5; see N2).
- **Refused reader on lineage and evidence-bundle:** 0 calls each to the share lookup, lineage events, charge read, charge write and expiry save. Control: the issuer's same calls hit every spy (G7). The refused lineage body equals the unknown-id body, so it carries no recipient data (G6).
- **Other by-id routes in the file:**
  - `grep -n "getCertification(" certifications.ts` → 7 sites (`:1009 :1086 :1150 :1232 :1332 :1469 :1556`). Control: the same grep finds the 3 bound GETs.
  - The other 4 are revoke (issuer-only 403 check, `:1093`), and verify, share and recertify, which have no per-record check.
  - The router has 9 routes. It is mounted once (`originate/src/index.ts:258`) behind `authenticate()` (`:65`).
  - See N1 for the addendum question.

**Q4 regression risk.**
- **nft-certificate** (`minting.service.ts:148,:173`, source-read): `fetch` sends no Authorization header. originate's `authenticate()` returns 401 when the bearer is missing (`middleware/auth.ts:87-89`), so this caller already fails, and the bound changes nothing for it. Inference: not run.
- **Human UI** (source-read):
  - `certificationApi.get` has 0 call sites. Control: the same grep finds `getLineage` (`LineageViewer.tsx:108`) and `getEvidenceBundle` (`:353`).
  - The viewer is reached from `DocumentDetail` → `/documents/:id/lineage`. The issuer and the holder (= `owner_user_id`) keep both routes.
  - Inference: a user whom the documents GET admits as a recipient (`data.recipientEmail`, `documents.ts:1123`) or via `wasCreatedByConnector`, but who is neither issuer nor holder, can open DocumentDetail and then gets 404 on lineage and evidence-bundle. Not measured.
- **SDK** (`sdk/javascript/src/modules/certifications.ts:122`, source-read): a non-party SDK caller now gets 404. That is intended.
- **Share recipients** (source-read):
  - The share route sends no `viewUrl` in `notifyDocumentShared`.
  - `isRecipient` on the documents GET reads `data.recipientEmail`, not `share_records`.
  - So nothing found depends on a share recipient reading `/:id`. Inference.
- **Transfers:** see N4.
- **Platform S:** see N5.

**Q5 red-proof.**
- **Suite by cell name** (`jest --json`, unique `path + fullName`):
  - 7e3b9362e08b: 135 files / 1575.
  - develop f01ba49da56d: 135 / 1576.
  - landing (real `git merge` of develop into the head; tree `9497977aaa7a…`): **136 / 1599 / 0 failed / 0 runtime-error suites**.
  - develop → landing: +23, all in the new file, **0 vanished**. base → landing: +24 (adds `ks1659-a-connector-certifying-with-no-holder` from develop), 0 vanished.
  - Lockfile, `package.json` and prisma are identical across all three trees.
- **Develop's `certifications.ts` swapped in** (sha256 `6abd05c5ea2f25f1`): the author's file goes **14 failed / 9 passed**, as claimed. Mine goes 7 of 8 red; G0, the mapper control, stays green, so this is not a load failure. Every failure carries an `expect(` assertion. Restored to `b0ea5cc5f1f90195`, sha-asserted.
- **Mutants** (each `tsc --noEmit -p originate` rc 0 first; anchor count = 1; failures parsed from JSON, all by assertion; restore sha-asserted each time; final restore True):
  - M1 drop the holder arm → C2, G1.
  - M2 drop the `''` guard → R13, G4.
  - M3 move the check after the expiry write → R6, G7.
  - M4 admit `ORG_ADMIN` → R14, G5.
  - M7b give GET `/:id` its own refusal body → R4, G6. My first M7, which changed the shared helper's text, was not a valid identity mutant (refusal and unknown-id both change) and is not counted. Only G6, through its literal-body assertion, catches it.
  - **X1 (mine):** move the lineage check after `getSharesByCertification` → killed **only by G7**. The author's R12 checks the body only, so it survives all 23.
  - **X2 (mine):** case-insensitive issuer compare → killed **only by G3**. It survives all 23 of the author's cells.
  - Total 7 built, 7 killed.
- **The new test file type-checked in its own program** (a tsconfig extending originate's, `files: [the test]`, `types: jest,node`; `--listFilesOnly` shows it included): rc 0, 0 diagnostics. Positive control: the same program over a copy with `const TENANT: number = "not-a-number"` → rc 2 with TS2322 at the injected line. Originate program `tsc --noEmit` at the landing: rc 0.
- **merge-tree** on live develop f01ba49da56d: `9497977aaa7a159922089b2e6b1abd2cd8927850`, equal to the claim. develop's tree is `38200e78045e`.
- Note: the head is NOT a descendant of f01ba49 (`merge-base` = `3a6f1810981e`). The claim's "develop is an ancestor" refers to 3a6f, which is accurate. The PR is not a fast-forward onto current develop.

**Q6 (for Wednesday, not the verdict).** The claim's control is sound as designed. It compares this PR against develop's own heads `f01ba49da56d` and `3a6f1810981e`, which carry the identical 6 `conclusion: failure` runs with `steps=0`. Same signature on GO'd commits means a "not this PR" attribution. I could not read the runs, because gh is not allowed. This is unverified by me.

## Notes
- **N1 (addendum; source-read plus measured on the real router; NOT a blocker).** Verify, share and recertify do not give a refused reader the record's content, its share recipients, its lineage or its evidence bundle: the bound itself is not bypassed. They do leak around its non-disclosure:
  - **verify (S1, measured):** a2, refused 404 on all three GETs, gets **200** from `POST /:id/verify`. The body has `checks.exists:true`, `issuer.id` = the issuer's UUID plus did, `status` and the `blockchain` block, and a `verification` charge row is written for a2. An unknown id gives 404. So verify is an **existence oracle** that undoes the "not yours = no such id" property, and it reveals the issuer. The holder id is absent from that body (asserted).
  - **share (S2, measured):** a2 gets 201 sharing the record to any address. Share and charge rows are written, the share email goes out with the title, and a2's share appears in the issuer's lineage. Afterwards a2 is still 404 on all three GETs, because the bound consults no share table. That is source-read: `isRecipient` uses `data.recipientEmail`.
  - **recertify (S3, measured up to the save):** a2 gets 201. The saved verification certificate has `issuer.id = a2`, `holder` = the ORIGINAL holder, and `data.originalIssuer` and `data.originalType` = the original's. Inference, not run because the save was mocked: a2, now that row's issuer, passes the bound on `GET /:newId`. They would read the original holder's id, name and did plus the original issuer and type, which is identity the refused GET withholds. It is not the original `data`.
  - All three predate this PR and are untouched by it. The author is filing a separate ticket. The UI calls share and recertify (`ShareDialog.tsx:87`, `RecertifyDialog.tsx:54`), so binding them is a product decision.
- **N2 (regression, source-read; not measured through a JWT).**
  - The admit set copies the list route, as PLAN 1-A prescribed. originate's own `requireRole`/`hasAnyRole` aliases `SUPER_ADMIN` to SYSTEM_ADMIN (`middleware/auth.ts:149,:170`), and `packages/shared/src/security/keyRevokePolicy.ts:171` says "JWTs in this repo carry both casings". The gateway also treats `platform_admin` as a platform role (`api-gateway/src/middleware/auth.ts:515`).
  - Effect: a platform admin whose token says `SUPER_ADMIN` or `platform_admin` was 200 on develop and is now 404 on another party's certification (G5 measured on the handler).
  - The list route already hides those rows from them, so this is consistent, not a widening. It is still a loss someone may notice.
- **N3 (test gaps, measured by X1 and X2).** The author's 23 cells do not pin that the lineage check precedes the share lookup (R12 asserts only the body), and they do not pin exact-match comparison (no case or prefix cell). G7 and G3 are the killing cells; worth adding if there is a round 2.
- **N4 (E2E, source-read):**
  - `tests/e2e/tests/integration/full-certification-flow.api.spec.ts:178-183` expects the verifier to get 200 on `GET /api/certifications/:id` after `/api/transfers` approve.
  - The transfer service never writes `documents.owner_user_id` (`git grep -i "owner_user_id|UPDATE documents" services/transfer/src` → 0 hits; control: 278 "transfer" hits in `services/transfer/src/index.ts`). So under the bound that cell would go 404.
  - The spec is already stale: its step 3 calls `/api/certifications/:id/audit`, which does not exist on this router. It runs only in `deploy-demo.yml` (workflow_dispatch, legacy Container Apps path, guarded by KS-552).
  - originate's own custody transfer (`documents.ts:2113-2118`) does flip `owner_user_id`, and therefore `holder.id`, so that path keeps the new holder at 200 (source-read).
- **N5 (Platform S): REPORTED, NOT MEASURED.** "S never reads certifications by id with a non-issuer key" is Stuart's word from S's code. Our token cannot read S's repo. A non-issuer S key now gets 404, which G2 measured for a different connector id.

## FOUND / TESTED / HOW
- **FOUND:** the bound matches the brief's rule exactly, comes before both side effects, and its refusal body is identical across all three routes.
- **TESTED:**
  - The author's 23 cells (23/23 at the landing; 14 red / 9 green on the develop file).
  - My 11 cells: G0-G7 on the bound and S1-S3 on the addendum; G1-G7 red on the develop file.
  - 7 mutants.
  - Three full suites by name.
  - Separate test-file tsc with a positive control.
  - merge-tree plus a real merge.
- **HOW:**
  - `git clone --shared` of the spark cache into `scratchpad/gate_cf1/src`.
  - Fetched `refs/pull/1667/head` and `develop` from GitHub over the Blockchain deploy key (read).
  - `npm ci --prefix <clone>/Blockchain/Dev --ignore-scripts --workspace=packages/shared --workspace=services/originate --include-workspace-root`, then `npm run build --prefix …/packages/shared` and `npm run generate --prefix …/services/originate`.
  - Tests via `npm test --prefix …/services/originate` (runs in that dir). Mutant runs used `subprocess cwd=<originate>`.
  - **PGlite:** `@electric-sql/pglite@0.4.1` resolved from the clone's hoisted root `node_modules` (lockfile-installed, not declared by originate). It needed `NODE_OPTIONS=--experimental-vm-modules` for its dynamic WASM import. `prisma.$queryRaw` tagged templates were translated to `$n` parameters and run on PGlite. Only saves, shares, lineage events and charge events were spies.
  - My test files lived in `scratchpad/gate_cf1/tools/` and were moved out of the clone's `__tests__` before every full-suite run. Clone `git status` was clean at the landing tree afterwards.
  - Mutant runner: `scratchpad/gate_cf1/tools/mutants.py`.

## NOT RUN
- No real gateway, real JWT, real Postgres server, Docker, or the four platform suites.
- No `services/auth` run.
- No OWNER, `MULTI_TENANCY_ENABLED=true`, recipient-by-`recipientEmail` or `onBehalfOf` connector-cert reader (the same gaps the author lists).
- No E2E.
- No GitHub, Linear, gh or push.
- Nothing under `!CODING` was written. The only use of `!CODING` was reading the deploy key path for a fetch into the scratchpad clone.
- The `GET /:newId` read after recertify (N1) is inferred, not run.

## Housekeeping
- **Heads:**
  - Start (02:54:34Z): PR `d7c2e296c9099ec9a0efd8db4d2f51210381ffc4`, develop `f01ba49da56d3d55204caa02ab3348f94d63b9c0`.
  - End (03:03:45Z): identical.
- `git -C /Volumes/DevMASTER/WEDNESDAY status --short` before writing this file: every untracked path is under `0_Brain/`, `2_Project_Files/local-model/` or `2_Project_Files/fleet/briefs_staged/`. None is outside the allowed set. This gate's only write in WEDNESDAY is this `verdict.md`.

## Wall-clock
- 02:54:20Z start → 03:04Z verdict written (about 10 minutes).
- Suites: about 15 s each.
- Mutant batch: about 3 minutes.
sha256 (sed '1d;$d' verdict.md | shasum -a 256): 1379e2bd461e3f658cf1eb5b21aae137f04db9528fd16e6d92be91b48ca352ea
