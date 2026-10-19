VERDICT: GO WITH NOTE at head 260115f9b481... (tier 2, round 1 of 2; landing tree aa6f52d2ac5464461695b5ce8c48f13585f991e9 on develop a4187f0f66228603df211628d6d8ae239d6147d0; 0 blockers, 3 notes)

## BLUF

#1641 does what it says and nothing else: it strips only the caller's `data.parentDocumentId` from the derived certification document and keeps the route's own value in both the `data` blob and the `parent_document_id` column. Every instrument agrees with the author's claim: 20/20 declared cells, 129 files / 1,536 of 1,536 across the whole originate suite, landing tree `aa6f52d2ac54...` reproduced, and the new test file type-checks. All three mutants I was asked to run (M1, M5, M6) are killed by the cells the author named, plus M2, M3, M4, M7 and the ks1293 manifest removal, with no false kills (no `TS####` in any failure).

**Tier stays 2.** Q2 answer: pre-fix, the caller's value could name any string, including another organisation's or another tenant's document id, but **nothing reads it**. Every lineage walk, verify route, v2 verify route, erasure walk and derive route reads the `parent_document_id` COLUMN, which `saveDocument` resolves tenant-scoped. This is a display-only fix, not a tenant-isolation fix. Details below.

0 blockers. 3 notes (one of them about the same bug class on other keys, which Wednesday will want to decide on).

## Findings

**N1 (note, real, not for this PR) - the same bug, other keys, still open.** The spread at `certifications.ts:666` still lets the caller overwrite three more server-written things on the derived row. I ran it (probe test, 201): with `data = {certificationId:'CALLER-CERT-ID', certifiedAt:'CALLER-TIME', contentHash:'sha256:bbbb...'}` the stored derived `data.certificationId` and `data.certifiedAt` are the CALLER's, and the derived row's top-level `contentHash` is the caller's `data.contentHash` (line 669, by design of the existing `||` chain). The control run (no such keys) stored the server's UUID and ISO time. `parentDocumentId` and `versionedById` are the only two keys now protected. Mitigation already present: `verification.ts` `resolveTrustedCertificationEvidence` (KS-1557 read side, header comment at :238-258) treats the derived row's metadata as caller-chosen and re-checks `certificationId` against a real certification row in the same tenant, the id8 in the external id, the owner and the parent's hash. So the exposure is display of a caller-chosen `certificationId`/`certifiedAt` in a plain document read, not a trust decision. I could not read Linear (barred), so I do not know whether a ticket covers this; if none does, one should.

**N2 (note) - forward-only.** The fix stops new rows being poisoned. Rows written before it keep whatever `data.parentDocumentId` the caller planted; there is no backfill and the PR does not claim one. Since nothing reads that key, this is cosmetic, but a read of an old derived row can still show a foreign id.

**N3 (note, about my instrument, not the PR).** The cache clone's three `node_modules` are absolute symlinks into the read-only project tree, so a naive copy resolves `@secuura/shared` to the PROJECT's stale `packages/shared` and 9 originate suites then fail to compile (`isProvisioningCapable` not exported; 19 cells). I caught it, replaced them with real copies, rebuilt shared in the clone and reran: 129/129, 1,536/1,536. The first 9-suite red was my environment, not the PR. Anyone repeating this gate from the same cache should know.

Also seen, no action: the certification record itself (`buildCertification`, `certifications.ts:487`, echoed at :781 and :979) stores and returns the caller's `data` as given, including any `parentDocumentId` inside it. That is the caller's own declared data, no server value sits beside it, and the PR says it is untouched. Not the bug in KS-1660.

## FOUND / TESTED / HOW

**Q1 - the fix.** READ `routes/certifications.ts` at head `260115f9b481` lines 639-676 (instrument: Read + `cat -n`). Line 646 destructures `parentDocumentId: droppedParentDocumentId` out of `data` beside the existing `versionedById`; the rest goes to `dataWithoutVersionedById`, spread at :666 AFTER the server's `title`, `certificationId`, `certifiedAt`, `parentDocumentId` (:660-665). The server's value (`parentDocumentId`, the route const from `req.body.parentDocumentId`, :415) is written at :665 and is no longer overwritten. The drop is `!== undefined`, so `null`, a string and an object are all dropped. Log line (:650-652) carries `tenantId` and `userId` only. Other keys: enumerated by reading the spread and PROVED by the probe above - `certificationId`, `certifiedAt` and `contentHash` can still overwrite (N1). `title` is `data.title` by construction, so no loss.

**Q2 - cross-organisation reach.** Pre-fix the caller's `data.parentDocumentId` was never resolved or authorised: only the route-level `parentDocumentId` goes through `getDocument` + `callerMayCertifyDocument` (KS-1557, :439-444), so the blob key could name any document id. Readers, by `git grep` across the whole repo (all services, frontend, mobile, sdk, mcp-server) for `parentDocumentId` outside tests/docs: the only files are `originate.openapi.ts`, `documentRepo.ts`, `certifications.ts`, `documents.ts`, `verification.ts`, and none reads `data.parentDocumentId` / `metadata.parentDocumentId` (a SQL-form grep for `metadata ->>'parent...'` also returns nothing, with a positive control: the same grep for `versionedById` finds the three erasure lines). Every lineage reader uses the column: `documentRepo` ancestors (:780, tenant-scoped LEFT JOIN), descendants (:852), `verification.ts` `fetchParentHash` (UUID + tenant predicate), v2 routes, `connectorOrganisationErasure.ts` (:375, :400). `saveDocument` (:423-461) resolves the column from the external id with `AND tenant_id = ...`, "no cross-tenant lineage". The sibling derive routes (`/version`, `sign-cert`, `sign-wallet`, `documents.ts` ~2332, 3071, 3266) spread the source's `data` and then write `parentDocumentId: id` last, so a planted value does not propagate. Conclusion: display-only. Not run: any live DB or deployed read; the readers were read, not driven.

**Q3 - cells can fail.** Own harness `scratchpad/gate_bb1/mutate.py` (python3 -I): asserts each line's exact pre-image before planting, runs the two test files with ts-jest (type errors are real compile errors), restores by writing the original back, scans each failure text for `TS\d{4}`. Control M0 (unmutated): rc 0, 20 cells, 0 failed.
- **M1** (:646, fix undone, variable still declared and used): rc 1, 4 failed = R1 and R2 for both principals. (The author's M1 also kills R3; mine keeps the log call, so R3 correctly stays green. Same fix undone, different log shape.)
- **M5** (:666, `data` not spread): rc 1, 4 failed = C1, C2 for both principals.
- **M6** (:666, re-plants only a NON-STRING value): rc 1, 2 failed = **R2 alone**, both principals. R2 is not a restatement of R1.
- M2 (log guard `!== null`): C3 only. M3 (log loses tenantId): R3 only. **M4 (log carries the dropped VALUE): R3 only** - the log line carries no dropped value in the real code. M7 (server's `parentDocumentId` removed at :665): R1, R2, C1 for both principals.
- All 7 mutants compile (no `TS####` in any failure message); the file was restored byte-identical after each run (`restored True`, `git status` of the clone clean).

**Q4 - ks1293 manifest line.** Removed `'ks1660-a-caller-s-data-parentdocumentid-overwrites.test.ts',` from `SUBJECTS` in `ks1293-originate-suite-is-hermetic.test.ts` (pre-image asserted present): rc 1, 1 of 20 red = `MANIFEST-DRIFT: no file this config runs touches the key without being a SUBJECT`. Restored. Load-bearing.

**Q5 - landing.** `merge-tree --write-tree` of develop `a4187f0f6622` and head `260115f9b481` in my clone = `aa6f52d2ac5464461695b5ce8c48f13585f991e9`; the head commit's own tree is the same, `merge-base` = develop (one commit on tip). Heads re-read via `git ls-remote origin` at start and again immediately before this verdict: develop `a4187f0f6622...` and `refs/pull/1641/head` = `260115f9b481...`, unchanged. Three-dot diff = 3 files, +154/-1. Full originate suite on this tree (jest, `--rootDir` my clone, real copied `node_modules`, shared rebuilt): **129 suites passed / 129, 1,536 tests passed / 1,536, rc 0** (the author's number exactly). New test file + ks1293 type-checked in a separate program (`tsconfig.tests.json`: extends originate's, `include` both files, `typeRoots` to the clone's `@types`, `types: [jest,node]`): rc 0, empty output; positive control (a file with two assigned-type errors and an unused local added to the include) printed three TS errors, so the program does check test files.

## NOT RUN

- No Docker, no database, no live originate, no deployed environment, no Playwright. The preflight's 3 skipped legs (3, 4, 8: stack not up) are not mine and remain unrun.
- Baseline suite at develop (1,526) was not rerun by me; I took the +10 from the author. My 1,536 stands on its own at the landing tree.
- GitHub, Linear and the PR body/comment readbacks were not read (barred); the claim's push/preflight/readback facts are the author's, unverified by me.
- No eslint, no `npm run build` of originate, no other service's suites.
- Whether a ticket exists for N1: unknown, Linear barred.

## Wall-clock

About 9 minutes from first command (16:48Z) to this verdict (about 16:57Z), including a 75 s node_modules copy and one wrong-instrument detour (N3).
b8c36438c413c5764abb04269f1d415098cfd5187ebbc5ce7ca25e11f7084ea8
