VERDICT: GO WITH NOTE at head 6b40e3a648f6608c0f7a05729c88a54936a2cb9f (tier 2, round 1 of 2; landing tree f16006646d5302a44052feb4684ecb87a41aec3e on develop 5ac66264b9ee10fe0c1d67b81951521a6a4a6dcf; 0 blockers, 3 notes)

## BLUF
The fix does what the ticket says. Every number in the author's claim reproduced: 8 of 13 new cells red at develop by assertion, 1555 to 1568 with 0 vanished, tsc rc 0, landing tree equal. My own reader census found no reader that trusts either field on the derived row, so there is no escalation to tier 1. Three notes, none blocking: one surviving mutant (log gate on falsy values), one display-only frontend reader outside the author's scope, and a behaviour change in the KS-1557 evidence path that is the intended direction.

Heads re-read at start (19:53Z) and before this verdict (20:01Z) by ls-remote: #1646 = 6b40e3a648f6608c0f7a05729c88a54936a2cb9f, develop = 5ac66264b9ee10fe0c1d67b81951521a6a4a6dcf. Unchanged.

## Findings
- B0 blockers: none.
- N1 (note, survivor): my mutant M7 changed both new log gates from `!== undefined` to truthiness. tsc rc 0, 13/13 cells stay green: it SURVIVES. Effect: a caller who supplies a falsy value (null, '', 0) still has the key dropped from the row, but no log line is written. The tests only plant truthy values (CALLER-CERT-ID, CALLER-TIME, an object, 1234567890). The PR's code uses `!== undefined` (same as the KS-1508 and KS-1660 lines), so the code is right; only a cell for a null or empty planted value is missing. Log-only, display-only fields: a note, not a blocker.
- N2 (note, outside the author's stated scope): frontend/issuer/src/components/DocumentDetail.tsx:203 reads `raw.certifiedAt || raw.data?.certifiedAt` and uses it at :89/:94 to draw a "Certified" timeline entry and its date. This is display only, no request or decision follows from it, and the fix makes it show the server's time. Not a trusted reader.
- N3 (note, behaviour change, from reading the code, not run): `claimedCertificationId` (verification.ts:266-274) reads `metadata.certificationId` of the derived row and requires the external id's 8-hex suffix to match it. Before the fix a caller-planted id usually failed that match, so the derived row was not counted as evidence; after it the row always carries the true id and is subject to rules 1 to 5 as designed. That is the intended direction (the caller can no longer make a genuine act fail to evidence itself), but it is a visible change in what verify can present for a request that plants the key. Worth one line in the PR if not already there.
- Observation, not a finding (explicit scope): the derived row's contentHash chain still hashes the caller's UNSTRIPPED `data`, so a planted certificationId or certifiedAt still feeds the hash. The ticket puts contentHash out of scope.

## FOUND / TESTED / HOW

### Q1 the fix does what the ticket says
- FOUND: the hunk (certifications.ts 646-659 at head) adds `certificationId` and `certifiedAt` to the destructure that already stripped versionedById and parentDocumentId, plus two `logger.info` lines whose meta is `{ tenantId, userId }` only. The server keys (`certificationId: id`, `certifiedAt: now`) are written before `...dataWithoutVersionedById`, as before.
- TESTED: the new file drives the REAL `certificationsRouter` over express with the KS-1508 mock shape (in-memory documentRepo, stub signer). At head: ks1679 + ks1293 = 23/23 green. At develop's certifications.ts: R1, R2, R3 (x2 principals, ISSUER_ADMIN and SYSTEM_ADMIN), R4, R5 = 8 failed, 5 controls (C1, C2 x2, C3) passed. The failures are assertions: `Expected "<uuid>" Received "CALLER-CERT-ID"`, `Expected "<iso>" Received "CALLER-TIME"`, and R3 object diffs. None is a load failure.
- Logs: R4 and R5 assert `JSON.stringify(all KS-1679 log calls)` does not contain the planted value and that the meta contains the tenant. I read the two log lines in the source as well: field names only.
- HOW: jest --config <clone>/services/originate/jest.config.js, run into the clone, with develop's certifications.ts copied over for the red run (restored byte-identically afterwards, `git status` of the clone clean).

### Q2 reader census (own, services/ and packages/ at head, non-test)
- `certificationId`: 108 lines in 16 files. Every one is one of: the route's own write (certifications.ts), the evidence resolver family (verification.ts:268 `claimedCertificationId`, which feeds `resolveTrustedCertificationEvidence` at :314 and re-checks the id against a real certification row in the row's tenant; presented id, type and time come from that real row, :339), the anchoring service's chain metadata (`chain.metadata?.certId || ...certificationId` at verification.ts:730, :1271, verificationV2.ts:242, written by the certification's own anchor request), request bodies (nft.routes.ts:26/146/636/656, thirdPartyVerifiers.ts:292/303), table columns (`certification_id`) in chargeEvents, billing, share_records, minting.service.ts, or type declarations.
- `certifiedAt`: 38 lines in 8 files. Reads of `certification?.certifiedAt` (verification.ts:814, :1019, verificationV2.ts:207) take `certification` from `buildCertification` (reads the `certification_metadata` COLUMN, server written) or from the trusted evidence map, not from the derived row's `metadata`. verification.ts:163 reads `certification_metadata` too. adminConfig.ts:1917 is a request body. No non-test reader of the derived row's `data.certifiedAt` in services/ or packages/.
- SQL: zero reads of either key through `->>`, `->`, `#>`, `jsonb_extract_path`, `json_extract`. Positive control: the same `->>` pattern finds 21 reads of other keys in services/packages (e.g. gdprService.ts:766 `certification_metadata->>'issuerId'`), so the zero is not a dead pattern.
- Bracket index `['certificationId']`: zero. Control: the same shape for any other key finds 307.
- Destructuring: three hits (certifications.ts:647, the PR's own, which is the control that the pattern fires; thirdPartyVerifiers.ts:303 and adminConfig.ts:1917, both `req.body`).
- Whole-object `metadata: r.metadata` passthroughs (adminConfig.ts:1885, gdprService.ts:270, others) return the blob for display or export; nothing in them decides on these two keys.
- Beyond the author's scope: whole-repo `*.sql`, `*.py`, `*.sh` grep for the two keys finds only the SDK and LibreOffice connector clients and migration 022 (shares). The frontend sweep found the display readers above (N2); no frontend decision on either key.
- Escalation rule: no reader trusts either field on the derived row for a decision or SQL read. No tier 1.

### Q3 red-first, no weakening, mutants
- Whole originate suite by cell NAME (file plus full name), develop vs head: develop 133 suites / 1555 tests / 0 failed; head 134 / 1568 / 0 failed. Vanished 0, new 13 (all in the new file), status flips 0. Control for the "vanished" comparison: run in the reverse direction it reports 13, so the comparison can see a difference.
- Manifest: with the new test file but develop's ks1293, ks1293 goes red on MANIFEST-DRIFT; with the manifest line it passes (23/23 together).
- Mutants, each applied to certifications.ts at head, type-checked first (`tsc --noEmit` on the originate program), then `jest ks1679`, then restored (cmp identical):
  - M1 drop the certificationId strip (rename the destructured key): tsc 0, red R1 R3 R4 (5 cells). Killed.
  - M2 drop the certifiedAt strip: tsc 0, red R2 R3 R5 (5 cells). Killed.
  - M3 remove the certificationId log: tsc 0, red R4. Killed.
  - M4 certifiedAt log leaks the value in its meta: tsc 0, red R5. Killed.
  - M5 certifiedAt log gated on the wrong variable: tsc 0, red R4 R5. Killed.
  - M6 reorder (spread first, server keys last, destructure and logs kept): tsc 0, 13/13 green. An EQUIVALENT mutant for stored values (server keys win either way), so green is correct. The author's M0 removes the strip and logs and is the version that reds R4 and R5.
  - M8 OWN: certificationId log drops `tenantId` from its meta: tsc 0, red R4. Killed.
  - M9 OWN: also strip an unrelated caller key (customNote): tsc 0, red C1 and C2 (4 cells). Killed.
  - M10 OWN: cross-wire the server key `certificationId: parentDocumentId`: tsc 0, red C1 R1 R3 (6 cells). Killed.
  - M7 OWN: truthiness gate on both logs: tsc 0, 13/13 green. SURVIVES (N1).
  - Two first attempts of M1 and M2 (deleting the variable and leaving references) failed to compile (TS2552, TS2304) and are not counted; I redid them as renames.
  - I did not re-run the author's nine by their labels (I do not hold their list); I ran six of the same kinds (M1 to M6) and four of my own (M7 to M10). Not claiming equality with their set.

### Q4 contentHash untouched
- The diff against the merge base is two hunks in certifications.ts (@@ -646 +646,2 and @@ -652,0 +654,6), both inside the destructure and log block. The `contentHash:` property of `derivedDoc` is the same four lines at develop (668-671) and head (675-678): `(data as ...)?.contentHash as string || generateDocumentContentHash(data || {}) || contentHash`. It still reads the unstripped `data`. Control: the grep for that property also matches line 1520/1527 `contentHash: certification.contentHash`, so the pattern fires.

### Q5 landing
- `git merge-tree --write-tree origin/develop pr1646` = f16006646d5302a44052feb4684ecb87a41aec3e, equal to the prediction. `git diff --stat pr1646 f16006646d53` shows exactly one file (docs/security/ROLES-AND-AUTHORIZATION-INVENTORY.md, #1645, docs only), so every source and test blob at the landing equals the head's; the tsc and jest results above apply to the landing's code. `git diff --stat origin/develop f16006646d53` = 3 files, +182/-1 (the PR).
- `tsc --noEmit -p services/originate/tsconfig.json`: rc 0 at head. Control: a planted `const zz: number = "x"` in certifications.ts reds it (TS2322). The new test file is excluded from that program (`exclude: src/__tests__`), so I type-checked it alone in a tsconfig of my own that extends the service's (files = the test): rc 0; a planted TS2322 reds it.
- `packages/shared` built first (tsc rc 0) in the clone, with real copies of the three node_modules trees.

## NOT RUN
- The four platform suites, any Docker, the stack, the pre-push preflight (the author's 13/16 with legs 3, 4, 8 skipped is theirs, not repeated).
- The author's exact nine mutants by label (see Q3).
- No live DB, no real certify request against a running service, no SQL against a real `documents` row; N3 is from reading verification.ts, not from running verify.
- Readers outside services/, packages/ and the frontend/ and whole-repo SQL/py/sh greps above (for example the docs, the website package, and deployed data in any environment).
- Landing built by tsc on a checkout of the landing tree itself: I relied on the diff showing the only landing difference is a docs file.
- merge-tree against develop was done on my clone's fetched develop (5ac66264b9ee); the head and develop shas were re-read from origin by ls-remote at the end.

## Wall-clock
About 9 minutes from 19:53Z to 20:02Z, including a 74 second copy of node_modules and two full originate suite runs (18 s and 15 s). Fetch of refs/pull/1646/head used the Secuura deploy key read-only (the cache clone did not hold the PR head). Nothing pushed, no GitHub or Linear writes, nothing written under !CODING or in WEDNESDAY other than this file. `git status --short` in WEDNESDAY shows only modified tracked dashboard data files under 0_Brain/dashboard/data/; no untracked path outside the allowed folders.
3dec6f2ca3b9c340f0a8014ce9144366319f7973454485da8b60148fc3390e7d
