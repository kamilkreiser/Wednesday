# QA gate, round 5 (delta): Secuura Platform K PR #1497 (KS-695 part ii, the organisation erasure), head dc488c46

- **Head under test:** `dc488c460f794dc476ce3460eabd44c9d6e138fe`. Develop: `425ad3e00ae40ddbce6ead62c127c610e2e67a16`.
  - **How I got it:** a `git clone --shared` of the Blockchain `2_Project_Files` into my scratchpad, with push URLs set to `DISABLED`. I then fetched `refs/pull/1497/head` and `develop` from GitHub over the project's `core.sshCommand` (read-only, at 05:17 AEDT), as the brief allows. Both shas match the brief.
  - **Why I fetched instead of using the bundles:** the project checkout lacks the bundles' prerequisite commits, so the bundles cannot be applied there. They do verify in my clone, and both sha256/16 match the brief (full `1379e0d584d363fd`, delta `bf766f1f934e0c25`).
  - **Head is the merged tree:** `merge-base(head, develop)` = `425ad3e0`, so the head already contains the develop tip and its tree is the merged tree. Every run below is on that tree.
  - **Nothing written in the project:** no git write verb and no file write under `!CODING`. No push, and no GitHub or Linear write.
- **Database:** my own throwaway PostgreSQL 15.14, on 127.0.0.1:55471 and then :55417, with its data directory in my scratchpad.
  - I moved the port because `ks1263` refuses any port outside 55410-55419. That refusal caused 3 environment-only failures per mode on the first all-8 run; see the suites evidence.
  - Init SQL 11/0, migrations 49/0, plus platform tenancy.
  - `secuura_app` has rolsuper f and rolbypassrls f. FORCE RLS is t on documents, organizations, svc_api_keys and action_provenance.
  - The database is now stopped (`pg_isready` rc 2). I touched no Kintsugi, demo or remote box.
- **Modes:** F = `MULTI_TENANCY_ENABLED=false`, T = `true` with `PLATFORM_DATABASE_URL` set.
  - **Fallback-warning grep** (`grep -c -i 'falling back to single-tenant'`): 0 in every F and T log.
  - **Positive control:** with the platform URL unset, the bounds file gave 2.
  - My file's setup line prints `poolBranch=true` in T.
- **Gate:** independent Opus delta gate, round 5, Tier 1 (destructive, GDPR-class), 2026-10-13.

## VERDICT: NO GO

The collision guard does what the author built it to do for the case it names: two keys whose `connector_id` strings are byte-equal.
- That case is re-proved on real Postgres in both modes: 403, and the database is byte-identical afterwards.
- Every round-4 item still holds. The trigger rewrite still reddens on the defects it guards. Both develop merges are clean.

It does **not** close M-1 path 2, which the PR body claims ("Path 2 (a shared connector id) IS closed here").
- **The cause:** the selector matches the authenticated *principal* (`connector:` + `connectorId || 'api-key'`), but the guard compares the *stored column*.
- **The consequence:** every key with a NULL or empty `connector_id` authenticates as `connector:api-key`. An organisation whose own key carries the literal connector id `api-key` passes the guard and erases those keys' documents, which belong to other organisations.
- **Exposure:** Kintsugi has 10 of its 13 keys with a NULL `connector_id` (the author's own read-only probe, `kin_collision_out.txt`). The probe's `WHERE connector_id IS NOT NULL` excluded exactly these keys.

That is a new **Major (M-2)** under the brief's rule ("any path that erases data it should not").

The merge is held for Kam's card regardless. I recommend neither merging nor deploying.

## Majors

### M-2. The guard compares `connector_id` values, but the selector matches the principal, and NULL, `''` and `'api-key'` collapse to one principal (path 2 is still open)

**Where the mismatch comes from:**
- **The principal.** The gateway and auth build it as `` `connector:${meta.connectorId || 'api-key'}` `` (`services/api-gateway/src/middleware/auth.ts:392`, `services/auth/src/services/jwt.ts:289`).
- **The validate result.** The security validate returns `connectorId: apiKey.connectorId || null` (`services/security/src/index.ts:1350`).
- **What a mint accepts.** The mint schema is `connectorId: z.string().optional()` (`index.ts:491`). It accepts `'api-key'` and `''`, and an omitted id is stored as NULL.
- **The route.** It strips the prefix: `connectorId = userId.replace(/^connector:/, '')` (`routes/platformOrganizations.ts:56`).
  - A key stored as `connector_id = 'api-key'` therefore passes `resolveOrganisationErasureTarget` (`connectorOrganisationErasure.ts:126`, `key.connector_id === ctx.connectorId`).
- **The guard.** It reads `WHERE tenant_id = $t AND connector_id = 'api-key'` (`connectorOrganisationErasure.ts:317-320`). That finds only A's own key: not NULL, and not `''`.
- **The selector.** Arm (b) and the lineage arm (`:328`, `:353`, `:259` `connectorUser`) match `versionedById = 'connector:api-key'`. After KS-1508 that value is written by the server, as `user.id`, for every version, sign-cert or sign-wallet made by a NULL-connector or empty-connector key, of any organisation and also org-less ones.

**Reproducing shape (cell K1, my file, REAL `/api/documents` and `/version` routes, then the REAL erase route, as `secuura_app`, both modes):**
1. Org A has a key with `connector_id='api-key'`.
2. Org B has a key with `connector_id NULL` and another with `''`. There is also an org-less key with `connector_id NULL`.
3. B's connector (principal `connector:api-key`, org B) creates "B payroll 2026.pdf" (issuer B), then `/version`s it. The result is a NULL-issuer row with `versionedById='connector:api-key'`.
4. The org-less key `/version`s the same document.
5. A B human `/version`s B's connector derivative.
6. A erases.

**The FAIL condition I stated first:** A answers 200 and B's derivative is `[erased]`. The PASS condition was a 403 with nothing written, or B's rows kept.

**Measured (F and T identical):**
- The guard's view of keys per connector_id is `{"api-key":1, NULL:2, "":1}`.
- A erase returns **`200 completed, documentsBlanked:4`**:
  - A's own document is `[erased]`.
  - **B's connector derivative is `[erased]`.**
  - **The org-less key's derivative is `[erased]`.**
  - **B's human child of it is `[erased]`.**
  - B's issued source is kept.
  - B's name and all of B's keys are untouched.
- Evidence: `evidence_runs.txt` (r5_false, r5_true).

**Who can do it:**
- Anyone who can put a key with connector id `api-key` into their OWN organisation, for example an org-scoped admin through `/api/security/keys` (free string).
- KS-1533's "organisation arm on mint" does not stop this, because the mint is for the attacker's own organisation.
- The victims are every NULL-issuer connector derivative made by a NULL-connector or empty-connector key in the tenant, and those rows' non-connector descendants. KS-869 notes that before KS-869 *every* connector collapsed to `connector:api-key`, so legacy rows of this shape are expected too.

**Minimal fix (owner's choice), inside this PR:**
- (a) Refuse (403, nothing written) when `ctx.connectorId` is `api-key` or the key row's `connector_id` is NULL, `''` or `api-key`. The fallback principal is never a connector identity.
- (b) And/or make the guard compare the principal: `COALESCE(NULLIF(connector_id,''),'api-key') = $connectorId`. Also decide whether the selector should ever match `connector:api-key`.

**Regression test to add:** the K1 shape, in both modes, through the real routes. It should assert a 403 and a byte-identical database. Add a mutant that drops the NULL/`''` arm.

**Also falsified by this:** the qualified N2 sentence ("holds only while connector ids are distinct"). Here the ids are distinct by value, yet another organisation's connector derivative is erased.

## Minors

**m-1. A key and document minted between the guard read and the blanking UPDATE are erased (measured; the author documents "not bounded").**
- **Cell R1:** A has 100,000 issued documents (ANALYZEd), so that the count statement makes a window.
  - While A's count statement was visible in `pg_stat_activity`, a second session committed B's key `connector_id = X` (A's id) plus a B NULL-issuer root with `versionedById='connector:X'`, within 20 to 27 ms.
  - Result: **200, `documentsBlanked:100001`, B's document `[erased]`** in F (2,959 ms) and in T (3,454 ms).
- **Why the window exists:** READ COMMITTED gives the UPDATE a fresh snapshot.
- **Why Minor:** it needs B to mint a key with A's exact id AND create a version within seconds of A's erasure, and it is disclosed in the PR body.
- **Cheap fix:** re-run the guard query immediately AFTER the blanking UPDATE (`:363`) and throw on a collision, so the transaction rolls back. A key committed before the UPDATE's snapshot is then always seen.
- **Side observation:** the count and the UPDATE use different snapshots, so `documentsBlanked` can exceed the 150,000 bound by the race. With N=150,000 in T the count saw the racing row and answered 503 `ORGANISATION_TOO_LARGE`, nothing written.

## Notes

- **N-1. Test gap: the guard's inactive-key arm is unguarded.**
  - Mutant G1 (`AND is_active IS DISTINCT FROM false` added to the guard) **survives the unit file (39/39) and bounds 25/25 in both modes**. Only my C2 (an inactive org-less key) kills it.
  - **Why it matters:** a revoked key of another organisation leaves its documents in place, and those documents must still block the erasure.
  - Mutant G2 (org-less keys ignored) is killed by unit only (1 cell). Bounds survives it.
- **N-2. Deleted-key reuse (C5, both modes).**
  - Shape: B's key X made B's NULL-issuer connector root and derivative, B's key row was DELETEd, A then holds a key X, and A erases. Result: **200, `documentsBlanked:2`, B's root and derivative `[erased]`.**
  - No app path hard-deletes `svc_api_keys`. The only DELETE is the one-off migration `019:145`. So this is reachable only by DBA action.
  - The guard reads live key rows, not history.
- **N-3. Statistics dependency.** Without `ANALYZE` after a bulk load, 150,000 flat issued documents ran past the budget: 500 at 25,082 ms (F) and 25,233 ms (T), rolled back, nothing written. With ANALYZE it took 5.2 s. That is data-safe, but a just-loaded organisation is a retry loop until autovacuum analyses.
- **N-4. Pre-existing liveness gap.** A key whose `connector_id` is NULL can never use erase-connector: its principal `api-key` is not equal to its NULL row, so the request is refused 403, which is terminal. On Kintsugi's counts that is 10 of 13 keys.
- **N-5.** The live PR body was not fetched (no `gh`). I read the author's local copy, `5_Project_History/2026-10-12_seatJ-4th/evidence/round5/pr1497_body_v5.md`.

## The author's claims, re-measured

| Claim | Result | Instrument and control |
|---|---|---|
| (1) Collision guard, path 2 | **Partly.** Byte-equal ids: C1 403 with diff `[]`. Org-less, active and inactive: C2 403 with diff `[]` (both modes). r4's P6 is now 403, with all five B rows kept. **Not closed for the NULL/`''`/`api-key` class (M-2).** | Snapshot = md5 of every row of documents, organizations and svc_api_keys in both test tenants, plus `count(*)` of every public table. Control: C3 (a successful erasure) shows the same snapshot changing (`diff=["documents","organizations","svc_api_keys"]`). |
| (1) Same-org rotation must not refuse | **Holds.** C3: older inactive key, sibling active key, and a key with org id stored `' UPPER\t'` give **200 completed, blanked 1**. Only the named key is revoked; the sibling and odd keys stay active. | Mutant G3 (raw compare, no normaliser) turns C3 red, and bounds m1/N-B too. |
| Spellings | **Consistent.** C4: case, lead and trail space, TAB, U+200B, NFD vs NFC, extended and prefix ids on B's key are not refused (200). B's root carrying the variant **kept** in every case. B's issued document claiming A's exact id **kept**. Exact `=` both sides. | Both modes. |
| Other tenant | C6: the same id in another tenant is not a collision (200), and that tenant's document is untouched. | Mutant G4 (no tenant filter) is killed by unit (5 cells). |
| 403 writes nothing | **Holds:** C1/C2 diff `[]`, including every table's row count (so no audit row either). The route logs ids only (`erase-connector: refused 403 ...`, seen in the T log). | Control as above. |
| (2) N2, (3) m-C wording | Present: `originate.openapi.ts:3726-3730`, service header `:182-190` and `:221-225`. `check:openapi` CHECK PASS, 414 example blocks. **The N2 qualification is still too strong (M-2).** | Read, plus `check:openapi` rc 0. |
| (4) G8 cells | **Hold.** Mutant G8 reddens unit (1) and the bounds N-a (G8) cell, F and T. | `mut.py` |
| (5) "M-1 PATH 1 IS NOT CLOSED" stated | **Stated** (body v5 line 19, service `:186-188`, openapi `:3727`). **True:** my P8 and r4's P8 still give **200 completed, B name and doc `[erased]`, B's own key true**, in both modes. | |
| Author numbers | **Reproduced:** unit **39/39**. Bounds **25/25** F and T. Older integration **15/15** F and T. All 8 integration files `--runInBand` **88/88** F and T (on port 55417). Originate jest **103 suites / 1254 tests**, twice. packages/shared vitest **49 files / 954**. tsc originate rc 0 with 0 lines. eslint on the 9 PR TS files rc 0 with 0 lines. | `evidence_suites.txt`. The first `check:openapi` rc 1 was my own mistake: I ran it in the originate workspace ("Missing script"). The re-run from the repo root gives rc 0. |

## Item 3: the round-4 attack file on this head (fast cells, both modes)

- **12 passed, 4 skipped (slow), 1 failed.**
  - The failure is P6, whose assertion pins round 4's *defect*. It now returns 403 with nothing erased, which is the fix.
- **P1:** 11/11 rows `consistent:true` in both modes.
- **P1b:** cancelled at 16 ms (F) and 12 ms (T).
- **P4:** N2 matrix unchanged.
- **P5a, P5b, P5c, P5f, P7:** as in round 4.
- **P5d/P5e (m-C):** committed at 2,505 and 2,537 ms (F), and 2,505 and 2,507 ms (T). This is still true and is now disclosed.
- I did not re-run the slow cells Q1 to Q4, B1 to B4, or scale. The budget code is unchanged since round 4 (blob-identical except the guard insertion); see NOT tested.

## Item 4: the trigger rewrite (AFTER statement triggers with transition tables)

The cells can still fail. Each mutant was applied alone and restored byte-identical (sha256 `7c55baba95d7` after every one). tsc rc 0 for every mutant.

| Mutant | Unit | Bounds F | Bounds T | My file |
|---|---|---|---|---|
| CTL | 39/39 | 25/25 | 25/25 | K1 red only (the finding) |
| G8 (commit check before the revoke) | **1 red** | **N-a red** | **N-a red** | - |
| M2a (commit check removed: m-2) | 3 red | **4 red** (m-2 outlives, m-A x2, N-a) | **4 red** | - |
| M2b (Prisma timeout back to 5 s: m2) | 1 red | **m2 red** | green (expected: the pool branch has no Prisma timeout) | - |
| G0 (guard removed) | 3 red | 2 red | 2 red | K1, C1, C2 red |
| G1 (guard ignores inactive keys) | **0** | **0** | **0** | C2 red only (N-1) |
| G2 (org-less keys ignored) | 1 red | 0 | 0 | C2 red |
| G3 (no normaliser in the guard) | 1 red | 3 red | 3 red | C3 red |
| G4 (no tenant filter in the guard) | 5 red | 0 | 0 | - |
| N3 (proposal, below) | 1 red | 1 red (M1+m3: count 4 to 3) | 1 red | N3 red; **K1 still erases** |

## Item 5: the develop merges

- **No evil merge.** `merge-tree --write-tree` reproduces both merges exactly:
  - `f4d4152b7` + `b2085e99`: tree `bfbda5b2`.
  - `df2c279bb` + `425ad3e0`: tree `35aad4ec`.
- **The PR's 10 files are blob-identical across both merges.** Fix vs head is identical except the bounds file, and that file's only change is the tests-only `df2c279bb`.
- **No develop commit in `551dc980..425ad3e0` touches the 10 files** (the log is empty). Control: the same log over `services/originate/src` lists `b2085e99`.
- **But develop DID change what the PR reads.** `b2085e99` (KS-1508) changed `documents.ts` and `certifications.ts`, which are the writers of `metadata.versionedById` that arms (b) and (c) select on.
  - Effect 1: a create or certification-derived row can no longer carry a caller value. My K1 and N3 cells ran on that code through the real routes.
  - Effect 2: the version routes now always stamp `user.id`. That is exactly what makes M-2 a server-made collision rather than a caller plant.

## N-3 premise: FAILS

The proposal is to add `AND d.parent_document_id IS NOT NULL` to arm (b) in both SQL copies. The premise is "every ROOT row carrying versionedById was caller-planted; the three version routes that set it also set a parent".

### Writer table (every writer at head, by grep over services, packages, migrations, scripts and docker, excluding tests)

**`metadata.versionedById`:**

| Writer | Value written | Parent column |
|---|---|---|
| POST `/:id/version` (`routes/documents.ts:2118`) | `user.id`: `connector:<connector_id>`, `connector:api-key` (NULL or `''` connector id), or a human user UUID. Set after the caller's metadata, so it is never caller-chosen and never NULL. | Sets `parentDocumentId: id` (`:2109`). The **column** is resolved `WHERE external_id = id` (`repositories/documentRepo.ts:450/476`), so it is **NULL when `:id` is the pkey UUID**. |
| POST `/:id/sign-cert` (`documents.ts:2853`) | As /version. | As /version (`:2845`). |
| POST `/:id/sign-wallet` (`documents.ts:3048`) | As /version. | As /version (`:3040`). |
| POST `/api/documents` create (`documents.ts:607`) | Drops any caller value (KS-1508). Writes none. | Create sets no parent. |
| POST `/certifications/issue` derived row (`certifications.ts:512`) | Drops the caller value. Writes none. | Parent from the body (`:521`), resolved by external_id. |
| `updateDocument` (`documentRepo.ts:612`) and `saveDocument` ON CONFLICT (`metadata = EXCLUDED.metadata`) | Carry forward the stored value. All 13 `updateDocument` callers pass system fields only (blockchain, status, signatures). | No parent write. |
| GDPR subject erasure (`gdprService.ts:735`) | Overwrites metadata with `{"anonymized":true}`, removing the key. | - |
| Seed (`documentRepo.ts:1079`), migrations, SQL scripts | None. | - |
| Rows written before KS-1508 deploys | Any caller value, root or derivative. | - |

**`parent_document_id` (column):**

| Writer | What it writes |
|---|---|
| `saveDocument` INSERT only (`documentRepo.ts:450/476`) | The parent resolved by `external_id` in the tenant, else NULL. The ON CONFLICT tail never updates it. Callers: the three version routes, the certification-derived row, and create (none). |
| FK `ON DELETE SET NULL` (`migrations/021:37`, mirrored in `api-gateway/src/startup-migrations.ts:592`) | NULL, fired by the admin organisation delete `DELETE FROM documents WHERE issuer_organization_id = $org` (`routes/adminConfig.ts:861`). |
| Any `UPDATE ... SET parent_document_id` | None exist. |

### Why the premise fails

The API hands clients the pkey as `documentUuid` whenever `external_id` is not UUID-shaped (`documentRepo.ts:172`, which says "the pkey UUID serves ... a working lookup key"). `getDocument` accepts it. KS-1278's own comment (`documentRepo.ts:602`) records that external_id-keyed writes silently miss UUID-addressed ids.

**Measured, cell N3, real routes, both modes:**
1. A's connector creates a document. The response's `documentUuid` is the pkey (`apiDocumentUuidIsPkey: true`).
2. `/version` by external id gives `parent` set.
3. **`/version` by `documentUuid` gives `parent: null`, `versionedById: 'connector:platform-s:<A>'` (server-set), issuer NULL, and `metadata.parentDocumentId` = the pkey.**

That is a **legitimate, server-written ROOT row carrying versionedById**. Further root rows of the same kind come from a source whose `external_id` is NULL (certificationRepo rows) and from children of an admin-deleted organisation's documents.

### What the predicate would stop reaching

Mutant N3, both modes: A's erasure leaves **A's own connector derivative "A board minutes 2026.pdf (watermarked)" un-erased**, because it has no parent and is now excluded from arm (b). That is under-erasure of the erased organisation's own titles.

The mutant also reddens the author's bounds cell M1+m3 (count 4 to 3).

It does **not** stop M-2: K1 still erases B's derivatives under N3, because they have parents.

**Recommendation for the ruling:** do not build N-3 as proposed. If root-planted legacy rows are the target, a data-scoped heal is the safer route: KS-1508's N-3 rows created before the KS-1508 deploy timestamp. Separately, fix the parent resolution so it also matches the pkey (the same class as KS-1278).

## What I did NOT test

- **The security-service and gateway halves at runtime:** minting a key with `connectorId: 'api-key'` or `''`, validate, the JWT exchange and the erase door's scope check. M-2's principal mapping is read from code (cited lines). The originate half is measured through the real routes with that principal injected by the gate's auth mock, which is the same harness as rounds 3 and 4.
- **Kintsugi data:** whether Kintsugi or production actually holds `connector:api-key` NULL-issuer rows. Not queried; no remote access was allowed.
- **sign-cert and sign-wallet addressed by `documentUuid`:** read only. They share the `saveDocument` parent resolution that /version uses.
- **Round-4 slow cells (Q1 to Q4, B1 to B4, R5) and the 149k scale cell:** not re-run. The budget code is blob-identical to round 4 apart from the inserted guard.
- **Mutants:** the author's 28 were not re-run. I ran 9 of my own plus a control.
- **Parallel (non-runInBand) integration runs:** not run. The author says they are not parallel-safe.
- **Other tooling:** the pre-push preflight and hook legs, Schemathesis, Akto, Playwright and k6 were not run.
- **Real environment conditions:** real NTP steps, Azure commit latency and pgbouncer were not tested.
- **The live PR body on GitHub:** not fetched.
- **Concurrency:** R1 is one timing shape (the insert committed during the count). Inserts during the UPDATE itself were not separately probed. By READ COMMITTED semantics they are not touched.

## Evidence in this folder
- `evidence_topology.txt`
- `evidence_suites.txt`
- `evidence_runs.txt` (K1, C1-C6, R1, N3, P8 and the r4 file, both modes)
- `evidence_mutations.txt`
- `gate1497r5-attack.integration.test.ts.txt`
- `mut.py.txt`
