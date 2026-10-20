VERDICT: GO WITH NOTE at head 97eaffe0d300... (tier 1, round 1 of 2; landing tree 5633c8d50584 on develop 108091b2e1c1; 0 blockers, 5 notes) - NO NEW AUDIENCE: the class PRE-EXISTS. The bare-connector control is readable on develop by same-tenant users exactly as the holder-less certification row is on the landing (200 / 200 / 404 / 200). The PR adds a new ROW TYPE to that class: a row that on develop could not exist (develop answers 400, 0 rows).

## BLUF
The fold is correct and well pinned, and every core claim BV1 made reproduces. I drove it on real Postgres 15 as `secuura_app` (NOSUPERUSER, NOBYPASSRLS), with the real certifications and documents routers and the real repositories.
- On develop, a connector certifying with no holder gets 400 "Certification payload contains values that cannot be stored", and no row is written.
- On the landing it gets 201 and writes a row with owner_user_id NULL and issuer_user_id NULL.
- That row is readable through GET /api/documents/:id by ANY same-tenant user, including a user of a DIFFERENT organisation in that tenant. Another tenant gets 404, and the issuing connector gets 200.
- Wednesday's control, a bare-connector POST /api/documents, is readable in exactly the same way on develop (and on the landing). So the reach is pre-existing. The PR extends it to one more row kind and does not widen it.

Two more things matter more than the PR itself:
1. GET /api/certifications/:id has no ownership check at all. A HUMAN-issued certification, which the documents GET does cloak (404), is served 200 to every same-tenant user of any organisation, through this path, on develop and on the landing alike.
2. The author's preferred remedy (fail the cloak closed on a falsy owner) would also cut the issuing connector off its own bare documents and holder-less certifications. A bare connector create writes no `action_provenance` 'create' row (measured: 0 rows), so the `wasCreatedByConnector` escape never admits it.

The READY claim "no reader admits on NULL" is false for the read path: documents.ts:1124 admits on the '' that documentRepo.ts:176 derives from NULL+NULL. The PR text should say so.

## Findings
- **N1 (note: the Q1 answer, class pre-exists).** At the landing, `documentRepo.ts:176` is `id: row.owner_user_id || row.issuer_user_id || ''`, and `routes/documents.ts:1124` is `if (userId && document.owner?.id && document.owner.id !== userId && !isAdmin && !isRecipient)`. With '' the conjunction is false, so the 404 cloak never runs. Measured audiences are below. (a) is a same-tenant ISSUER_ADMIN of the same organisation, (a2) is a same-tenant ISSUER_ADMIN of another organisation, (b) is another tenant, and (c) is the issuing connector.
  - Landing, connector certification with no holder, GET /api/documents/:id: a 200, a2 200, b 404, c 200. The 200 body carries `"owner":{"id":""}`, plus title, data and contentHash.
  - Develop and landing, bare-connector POST /api/documents (row owner NULL, issuer NULL), GET /api/documents/:id: a 200, a2 200, b 404, c 200.
  - Positive control: a human-issued certification with no holder (owner = issuer = the human's UUID) is 404 to a, a2, b and c on both trees, so the cloak works when the owner is non-empty, and the 200s above are not "everything is readable".
  - Develop, the same connector certification: 400, `{"success":false,"error":{"code":"BAD_REQUEST","message":"Certification payload contains values that cannot be stored"}}`. That is 0 rows for the id and 0 rows in the tenant whose metadata names the connector as issuer.
  - Audience: identical to the bare-connector class, which is the whole tenant, every organisation, all roles. The KS-1116 ruling ("owner-less rows readable by the row tenant's administrators") is narrower than what ships for BOTH row types.
- **N2 (note, pre-existing, wider than N1).** `routes/certifications.ts:956-1010` (GET /api/certifications/:id) calls `getCertification(id, tenantId)` and returns issuer, holder, data and blockchain with NO owner, holder or org check. Measured on both trees: the HUMAN certification (cloaked by the documents GET) is 200 to a and a2, and 404 to b. The new row is 200 to a, a2 and c, and 404 to b. On this path the new row has the same audience as every certification. The documents-GET cloak is therefore not the only thing guarding certification rows, so any remedy confined to documents.ts:1124 leaves this path open. List endpoints did not include the new id for (a), (a2) or (b): `documents.ts:321` filters on `d.owner?.id === userId`, and the certifications list filters on holder or issuer id. Only (c) saw it, in the certifications list.
- **N3 (note: a surviving mutant, coverage).** I added a mutant G1, `${cert.holder.id === cert.issuer.id ? null : cert.holder.id}::uuid`. It compiles (tsc rc 0) and is live: in the real-Postgres probe the human self-certification row was stored with owner NULL. Even so, ks1659 and ks564 stay 15/15 green. No cell pins "a HUMAN caller with no holder keeps owner_user_id = own UUID", because C1 uses distinct issuer and holder ids. On the documents GET it is masked by the `|| issuer_user_id` fallback (still 404 to all readers), but direct column readers (anchorOverwriteGuard custody, verification.ts:334, the GDPR owner selectors) would see NULL. Suggested cell: saveCertification(cert(HUMAN, HUMAN)) binds HOLDER_AT = HUMAN.
- **N4 (note: the remedy cost, Q4).** See Q4 below. The author's preferred shape strands the issuing connector unless it is paired with a 'create' provenance row or an org match.
- **N5 (note, confirms BV1).** certifications.ts:343 format-checks the holder only inside `if (req.body.holderId)`, so the :335 default `req.body.holderId || issuer.id` is never checked. :827 sits inside the foreign-key branch, so a 22P02 never reaches it. The develop 400 above comes from the KS-445 22P02 mapping at :858-868, not from :827.

## Q4: smallest remedy shapes (options, not a decision)
1. **Fail the cloak closed on a falsy owner at documents.ts:1124** (the author's preference): drop the `document.owner?.id &&` conjunct. It covers both row types in one line. Cost, measured: a bare connector create writes NO 'create' row in `action_provenance` (0 rows after the probe, against 12 documents in the database), and certify writes provenance only with onBehalfOf. So `wasCreatedByConnector` is false for the issuing connector, and (c) would go from 200 to 404 on its own bare documents and holder-less certifications. Per the KS-480 §6 comment at :1126, Platform S drives the whole lifecycle through that id. It needs a companion: record a 'create' row for bare connector creates and certifications, or admit `role === 'connector'` whose `organizationId` matches the row's organisation. It also does nothing for N2.
2. **Cloak an empty owner to admins plus the creating connector only** (the KS-1116 ruling shape). This is the same edit as option 1 plus a tenant-admin admit. It has the same provenance dependency and does not cover N2.
3. **Set the owner from the issuing connector's organisation or tenant administrator at write time.** This keeps reads unchanged, but it changes custody semantics (anchorOverwriteGuard), needs a lookup on the write path, and does nothing for the existing bare-connector rows.
4. **Refuse a holder-less connector certification** (400 HOLDER_REQUIRED). This is the smallest blast radius and returns to develop's "no row" state with an honest error instead of 22P02-as-payload. It is a client-visible contract change for Platform S, and the bare-document class stays as it is.
5. Separately, for N2: give GET /api/certifications/:id the same predicate as documents.ts:1124 (`callerMayCertifyDocument`-style). Without it, options 1 and 2 do not close certification reads.

## FOUND / TESTED / HOW
- **Heads:** ls-remote at start gave PR 97eaffe0d300 and develop 610570e5a757. At the end, develop had advanced to **108091b2e1c1** (#1660, one file under services/m365-integration, 0 overlap with the PR's 2 files).
- **Landing:** on 610570e5a757 the landing tree is 2ba4f69bfbd4 (equals the author's and BV1's). On live develop 108091b2e1c1 it is **5633c8d50584** (merge-tree rc 0). The originate subtree (7f33d677c55b) and the packages subtree (2865bfbdc718) are identical in both landing trees, so every run below applies to the live landing.
- **Q1/Q2 probe** (scratch file `gatebx1-reach-probe.integration.test.ts`): Postgres 15.14 on 127.0.0.1:55496, timezone UTC, migrations 001-054 plus 003_platform_tenancy. The SETUP cell asserts current_user is secuura_app, rolsuper=false and rolbypassrls=false. Same file on both trees, 4/4 passing, results in `logs/probe-{develop,landing}.json`.
- **Q3 suites, keyed by cell NAME:** develop 134 suites / 1568 tests, landing 135 / 1575. 0 vanished, 7 added (all ks1659), 0 non-passed on either side, 0 status changes. `ks564-certification-issuer-uuid` is 8/8.
- **Q3 fold** on 9 inputs, each paired with an idempotence check:
  - Kept as-is: a real UUID, and an UPPERCASE UUID.
  - Folded to NULL: a connector principal, null, undefined, '', 'not-a-uuid', a padded UUID, and the number 42.
  - 10/10 including a positive control showing the assertion can fail.
- **Q3 mutants:** each one passed tsc, the result came from a test assertion, and certificationRepo.ts was confirmed restored with `git diff --quiet` after every arm.
  - A1 (the author's revert to raw `cert.holder.id`): 3 red (R1, R2, R3).
  - A2 (the author's fold of `holder.did`): 2 red (C1, C2).
  - G1 (mine): 0 red, a SURVIVOR (N3). It was also driven through the probe, where it is masked on the read path.
- **Q3 type-check:** I built an own program, `tsconfig.bx1.json`, extending originate's with include = the ks1659 test only. `--listFilesOnly` shows the file. tsc rc 0. As a positive control, appending `const bx1Control: number = "not a number"` gave rc 2 with TS2322, and the file was then restored.

## NOT RUN
- No gateway or real JWT layer. The routers were mounted directly with the repo's own probe-user auth mock, so any scope gating at api-gateway is unmeasured.
- MULTI_TENANCY_ENABLED=true. A system_admin or recipient reader. An onBehalfOf connector certification. The derived lineage row (parentDocumentId).
- No anchoring stub: the routes ran with SIMULATE_ANCHORING=true and a closed anchoring port, NODE_ENV=test.
- No platform suites, originate integration suites, preflight, lint or format. No box, no Docker, no deploy.
- The remedies in Q4 were not built.

## Wall-clock
12:02-12:15 AEDT (about 13 min, of which about 6 min was runs). `git -C /Volumes/DevMASTER/WEDNESDAY status --short` before writing this file: empty, so there are 0 untracked paths outside the allowed directories. Scratch: /private/tmp/claude-501/-Volumes-DevMASTER-WEDNESDAY/4cf20ec9-03c1-4724-89c4-ae3e1635cfad/scratchpad/gate_bx1/ (the Postgres server is stopped).
sha256 of `sed '1d;$d' verdict.md | shasum -a 256`: d7b12fb87f270ffe6e1b25800b1f7f39c646d010ddbc0e9de12d4918abae3bec
