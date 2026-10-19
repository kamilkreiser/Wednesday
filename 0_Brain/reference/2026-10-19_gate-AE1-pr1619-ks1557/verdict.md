VERDICT: GO WITH NOTE at head 894468de3dbb (tier 1, round 1 of 2; landing tree 9579105768a72cc8b7cdfd1873cf7e8f16d52d71 on develop 6ec1b7badb9b9fc1cd8d8cfe63b6cd61b8ce7b63; 0 blockers, 6 notes)

# GATE AE1: PR #1619 (KS-1557 write side), Opus, tier 1, round 1 of 2

Gate run 2026-10-19 08:45Z to 09:03Z. Nothing written under `!CODING`, nothing on GitHub or Linear. Every write verb ran in the scratch clone `.../scratchpad/ae1/repo`. The project repo was used only for `ls-remote`, `cat-file` and `config --get`. The scratch clone fetched from origin with the project's deploy key, read-only.

## Heads (read at start, re-read before the verdict)

| read | develop | #1619 head |
| --- | --- | --- |
| start (ls-remote) | `8323f2f70cd796219774f240184f777813c28aec` | `894468de3dbbce71bd36015d8465b5dc9a07033e` |
| before verdict, 09:00Z and 09:03Z | **`6ec1b7badb9b9fc1cd8d8cfe63b6cd61b8ce7b63`** (moved +2: `66faac9ae` KS-1629 #1617, `6ec1b7bad` KS-1642) | `894468de3dbb...` unchanged |

- **The author's predicted tree is CONFIRMED on the develop it named.** I ran `git merge-tree --write-tree 8323f2f70 894468de3` and got `45f61469230dc38aad5ae0792b43e6883bf91aef`, rc 0. A real `merge --squash` in scratch then `write-tree` gave the same tree.
- **That tree is now stale.** On live develop `6ec1b7bad`, `merge-tree` gives **`9579105768a72cc8b7cdfd1873cf7e8f16d52d71`**, rc 0, and the scratch squash's `write-tree` gives the same tree.
- **No file overlap with develop's move.** Develop moved 6 files: `routes/anchors.ts`, `utils/idNamespaceCollision.ts` and 4 tests. None is among the PR's 7 files. No package-lock, packages, prisma, migrations or docker file changed. Every suite below was re-run at the new landing tree.
- **The three-dot list (`develop...pr1619`, at both develop tips) is exactly the 7 files:** `routes/certifications.ts` plus `__tests__/` ks1213, ks1228, ks1508, ks1538 (unit), ks1557-lineage (new), ks1557-verify-trusts. The diff is +390 / -8.

## Q1: Is the identity guard exact? YES (measured both arms through the real route, both tenancy modes)

**Instrument:** a probe cell added to a scratch copy of the new suite, so it used the same harness (real routers, `secuura_app`, real PG). It ran with MT=false and MT=true and was then moved out of the tree.

- **Arm 1 (050 live).** `pg_trigger` showed `documents_id_namespaces_disjoint` enabled (count 1). An UPDATE that gave A's row X `external_id = B's row Y pkey` was refused with **`23505 document id namespace collision`**, in both modes.
- **Arm 2 (trigger disabled as superuser, collision planted).**
  - The check-path predicate (`external_id = $1 AND tenant_id = $2 LIMIT 1`) and the write-path sub-SELECT predicate both returned **X's pkey**, the attacker's own row.
  - Through the route:
    - A certifying with `parentDocumentId = Y.pkey` got **201** and linked **X**.
    - **Y's own owner got 403**: the check judged X, which is the row the write would link. That is the closed direction.
    - A stranger got **403**.
    - **Y gained 0 children.**
  - Cleanup: the trigger was re-enabled (`tgenabled = O`) and the collision census read 0. The planted collision itself was the non-zero control: the check path resolved Y's pkey to X.
- **Third resolution of "the parent": none that disagrees.** I read every place the request names the parent:
  - **The check:** `getDocument` query 1, keyed on `external_id` and tenant (`documentRepo.ts:240`).
  - **The cycle walk:** `assertNoCycle`, then `walkAncestors` with `WHERE d.external_id = cursor AND d.tenant_id` (`documentRepo.ts:781`). Same predicate.
  - **The write:** `saveDocument`'s `parent_document_id` sub-SELECT, `external_id` and tenant, in both insert tails (`documentRepo.ts:450, 476`). Same predicate.
  - **`saveCertification`:** stores no parent. I counted 0 `parent` hits in `certificationRepo.ts`, against a control of 4 `insert` hits in the same file.
  - **The anchoring POST body:** sends `documentId: id` and `certId: id`, which are the certification uuid. It carries no parent.
  - **`wasCreatedByConnector(document.id, ...)`** keys on the resolved row's `external_id`.
  - **Determinism:** `documents.external_id` is globally UNIQUE (`documents_external_id_key`, measured on the scratch schema; `docker/init/01-schema.sql:132`). So `LIMIT 1` cannot choose between rows.
  - The one non-resolution is a raw string copy. See note 3.
- **"A pkey-only match = no check, 201, links nothing" is TRUE.**
  - In code: if query 1 found nothing, then no row in the tenant has `external_id = P`. The write's sub-SELECT then folds to NULL.
  - Measured: the PKEY CORNER cell reads `parent_ext` NULL and B's child count unchanged, in both modes.
  - **The NULL-`external_id` case:** a row with a NULL `external_id`, addressed by its pkey, passes the guard and is checked even though nothing is linked. That over-refuses, which is the closed direction, and the author already names it.

## Q2: Ordering. DEFENSIBLE, not a weakening

- **The check is first.** It precedes `assertNoCycle`, the anchoring `fetch` and both saves (`certifications.ts:437-442`, then 443).
- **ks1228's 422 cell:** the status, code and "no row" assertion are unchanged. Only `wasCreatedByConnector` now answers true for `(doc-src-1228, connector:ks1228-conn)`, the suite's own source and connector. With the check first, a 422 can only come from an authorised caller, so the cell still tests what it says.
- **Not pinned:** see note 2. Mutant M3, the check moved after the cycle walk, survives every cell.

## Q3: The re-pinned cells. HONEST

**Instrument:** I ran develop's four unit-test files against the PR's route at landing. **Exactly 7 old cells red**, all of them named:

| old cell | count |
| --- | --- |
| ks1538 "a parentDocumentId ... does not run this check" | 1 |
| ks1228 "a lineage cycle: 422, no row" | 1 |
| ks1508 as connector: "RED versionedById dropped", "control rest of data kept" | 2 |
| ks1213 as connector: "control documentType equal", "control no documentType", "control KS-1229 accepted issue reaches /api/anchors" | 3 |

- **The 6 re-pins are fixture-only.** I read each diff. Not one assertion line changed. In each, the `wasCreatedByConnector` mock went from a blanket `false` to `documentId === 'doc-src-<suite>' && connectorUserId === <that suite's CONNECTOR.userId>`.
  - I checked the ids against each fixture: ks1213 and ks1508 both use `connector:ks1213-conn` as their CONNECTOR, and ks1228 uses `connector:ks1228-conn`.
  - The source owner is `ISSUER.userId` in ks1213 and ks1508, so the ISSUER and SYSADMIN principals pass through the real predicate.
  - A different connector, or a different document, still answers false. Note that no UNIT cell asserts that inverse; the integration "CREATING connector" control does.
- **The ks1538 cell encoded the defect.** Its old title and assertion were "201, `getDocument` not called" on the lineage path, which is exactly the open half of KS-1557. Its replacements:
  - owner gets 201 and `getDocument('doc-parent', TENANT, undefined)`;
  - a stranger gets 403 `FORBIDDEN` with no saves and no UPDATE;
  - a pkey-only resolution gets 201.

## Q4: Red-first and controls. REAL (reproduced)

- **Red-first:** develop's `certifications.ts` (0-line diff to develop) plus the new suite gave **6 failed / 7 passed with MT=false, and 6 / 7 with MT=true**.
  - The first failure is `Expected: 0 Received: 1` on the child count, so it names the defect as claimed.
  - The 6 that failed: RED user, RED connector, RED no-row, recipient control, creating-connector control, OWNERLESS DECISION.
- **Constraining controls:** UNCHANGED, PKEY CORNER, Stuart's S shape `c1712c38` and ITEM5c-open are **green at develop (both modes) and green at the PR head and both landing trees (both modes)**.
- **My mutants.** Each compiled (`tsc --noEmit` rc 0). Each ran in both modes. The green file was restored byte-identically every time (sha256 prefix `0c7a833daf0bb94f`).

  | mutant | result |
  | --- | --- |
  | M1: drop the identity clause (`if (parentDocument`) | reds **exactly PKEY CORNER**, in both modes |
  | M2: skip the check for `role === 'connector'` | reds **exactly 2**, RED connector and the creating-connector control, in both modes |
  | M3: check moved after the cycle walk | reds **0** of 13 in both modes, and 0 of 52 in the ks1228 and ks1538 unit suites. A survivor: note 2 |

## Q5: Landing. GREEN at both landing trees

- **DB:** scratch PostgreSQL 15.14 (Homebrew; no Docker) on 127.0.0.1:55410, TCP only.
  - Built from `docker/init/*` in lexical order. `00-init-platform-db.sh` was emulated by applying `docker/init-platform/01-platform-schema.sql` to `secuura_platform`, as the script does. `01-create-app-role.sh` was run as written.
  - Then the project's `scripts/run-migrations.sh` ran, copied only to move its error log into scratch. It printed **53 `[main] Applying` lines and 1 `[platform] Applying`**, ending `Summary: applied=54 failed=0 skipped=0`, rc 0.
  - 050, 051 and 052 all show an Applying line. Measured afterwards: both triggers enabled, and `secuura_app` has `rolsuper=f` and `rolbypassrls=f`.
- **Harness preconditions I had to add.** Both are pre-existing; see note 4:
  1. The suites insert into `tenants` in the TENANT database, so I also applied `003_platform_tenancy.sql` to `secuura`. Before that, 13/13 failed with `relation "tenants" does not exist`.
  2. I set the server timezone to UTC, as the docker image does. Under the inherited `Australia/Sydney`, ks1557-verify-trusts with MT=false reds 3 `certifiedAt` cells.
- **Suite counts at landing `9579105768a7` (live develop `6ec1b7bad`):**

  | suite | MT=false | MT=true |
  | --- | --- | --- |
  | ks1557-lineage-certify (new) | 13/13 | 13/13 |
  | ks1557-verify-trusts | 17/17 | 17/17 |
  | ks1538 integration | 10/10 | 10/10 |
  | originate FULL unit suite | 124 suites / 1497 tests / 0 failed, rc 0 | |
  | tsc **including tests** (scratch tsconfig extending the service's, tests included, jest typeRoots) | rc 0, 0 `error TS` | |
  | `tsc --noEmit -p services/originate` | rc 0 | |

  - **tsc positive control:** a planted wrong annotation in the new suite gives rc 2 with 1 `error TS`. The file was restored to the same sha256.
- **At the superseded landing `45f61469230d`:** 13/13 and 10/10 in both modes; verify-trusts 17/17 in both modes with the server on UTC; full unit suite **122 suites / 1483 tests / 0 failed**. This matches the author's 1483. Also at the PR head itself: the new suite 13/13 in both modes.

## Q6: Boxes. UNMEASURED

- **Which deployed boxes have migration 050 applied: UNMEASURED.** I cannot read the boxes and did not try.
- **The guard's exactness does NOT depend on 050.**
  - Arm 2 measured it with 050 disabled. Check and write agree because their predicates are identical and `external_id` is UNIQUE.
  - On the boxes, the unique index is inferred, not read: five `ON CONFLICT (external_id)` sites in originate would error (42P10) without it. `migrations/001_initial-schema.sql:31` declares the column without UNIQUE; `docker/init/01-schema.sql:132` declares it with UNIQUE.

## Blockers

None.

## Notes (non-blocking)

1. **The landing tree moved during the gate.** It is now `9579105768a7` on develop `6ec1b7bad`, not the predicted `45f61469230d`, which was correct at `8323f2f70`. There is no overlap, and everything was re-run at the new tree. Recompute the tree at merge time.
2. **The ordering is correct but unpinned.** Mutant M3 (403 after the cycle walk) survives all 13 integration cells and all ks1228 and ks1538 unit cells. KS-1656 already says the cycle arm cannot fire on this route, so the practical exposure is only the ancestor read. Still, nothing would catch a reorder.
3. **Pre-existing, measured identically on develop:**
   - The caller's `data.parentDocumentId` is spread AFTER the server's own value in the derived row's `data` (`certifications.ts`, derivedDoc `...dataWithoutVersionedById`).
   - So `GET /api/documents/<derived>` serves `data.parentDocumentId` = **a foreign document's id**, while the column links the caller's own parent. The foreign document gains 0 children.
   - The GET response has no top-level `parentDocumentId`, so this caller-controlled string is the only lineage claim GET shows.
   - It is display-only and outside this PR. It deserves a ticket next to KS-1656.
4. **Harness preconditions not stated in the suite headers, both pre-existing:**
   - The suites need a `tenants` table in the TENANT database.
   - ks1557-verify-trusts with MT=false reds 3 `certifiedAt` cells when the PG server's timezone is not UTC. The failing lines are not in the PR's hunk.
5. **The cell count is 7, not 6.** The PR changes 7 old cells: 6 fixture-only re-pins plus the ks1538 contract, replaced by 3 cells. The ks1228 mock comment says "(the 422 and the 503)", but the 503 cell sends no `parentDocumentId`.
6. **TOCTOU, already named by the author ("concurrency is not covered"):**
   - The check reads at t0. The write's sub-SELECT resolves at t1, after the anchoring POST, which can take up to 10 s.
   - If a parent that did not resolve at t0 gains that `external_id` in between, it would be linked unchecked.
   - Exploiting it means predicting a victim's future `external_id`. No cell covers it.

## NOT RUN

- Migration 050 state on any deployed box (UNMEASURED; no box access).
- The four platform suites (Schemathesis, Akto, Playwright, Performance/k6): need Docker, which the brief forbids.
- The push preflight hook. The ks1119 control suite.
- The author's mutant "refuse on a non-resolving parent". I ran my own M1, M2 and M3 instead.
- A develop-side red run of the re-pinned UNIT suites. I ran develop's unit files against the PR route instead.
- The full unit suite at the PR head itself (it ran at both landing trees).
- A cell-by-cell reconciliation of 1483 to 1497 (develop added 2 suites).
- Any concurrency or race exercise.
- Reading the PR body, the KS-1557 comment, or KS-1656 and KS-1647.
- A Docker-image PostgreSQL: Homebrew PG 15.14 was used instead; `02-seed-default-tenant.sql` was not applied, matching the init script.
- `.githooks` and the CI workflow.
SHA256: 985f3a50da69d6d7c882e4d8c229baf4b7e81b8ee8111f1d3ef323c2711ec3f3
