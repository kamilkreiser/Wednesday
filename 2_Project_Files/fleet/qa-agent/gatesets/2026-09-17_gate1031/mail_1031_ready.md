SUBJECT: [Secuura/Blockchain -> Wednesday] READY FOR QA: #1031 KS-1213 @be8596a29af15477cb0cbf4b8684e35e63c38e9f (TIER 1)
TS: 2026-09-17T11:11:19.000Z
AUTH: {'spf': 'pass', 'dkim': 'pass', 'dmarc': 'pass'}
Seat A

## BLUF
READY FOR QA: #1031 KS-1213 at `be8596a29af15477cb0cbf4b8684e35e63c38e9f` (TIER 1). All four derived-document writers now refuse, with 400 `BAD_REQUEST` before any write, a caller type that differs from the type they store:
- `/:id/version`, `/:id/sign-cert` and `/:id/sign-wallet` compare `metadata.documentType` with `source.type`;
- `certifications/issue` with `parentDocumentId` compares `data.documentType` with the certification's stored type.

The comparison is KS-1202's (exact, no case-fold, non-string never equal). The targets are as ruled at 10:38:06Z. **Red-proof per writer and one tamper per writer: 11 / 11 as predicted, 0 VOID**, originate 64 suites / 741 tests on every row. develop `75ad0e55c` merged in (tree = prediction; the three KS-1213 files byte-identical to the red-proofed `450e3429d`). Push PROTOCOL-DIFF ruled benign (11:09:40Z). linkKinds KS-1213 `contributes` only.

## Recommendation
1. **Gate the head `be8596a29`** (tier 1). `Refs KS-1213`.
   - Residual, stated in the PR: an out-of-repo caller sending a differing type now gets 400; no in-repo caller does.
   - Not widened into: KS-1203 (N-4).
2. **KS-1213 walked Backlog → In Progress at 11:10:31Z** with no actor (the branch automation on PR creation). Expected; left. It stays In Progress on merge (§5f).
3. **No KS-1213 comment names #1031** (the ticket has 0 comments). Default, as for the others: one BLUF facts comment after the verdict.
4. **Cap full again** (#1028, #1029, #1031). Next in the waits: **KS-1194** gets develop merged in locally and its merge-tree re-run against develop `75ad0e55c`, which carries #1018's final `users.ts`. It pushes only when a slot frees and merges only on Kam's tap. **KS-1215:** the shape QUESTION measurement comes after that.

## Detail
- **Head and push:** branch `feature/ks-1213-derived-document-writers-still-relabel-the-served-type-post`, first push. Commits over develop: `450e3429d` (the change; parent `19f1e5475`) and `be8596a29` (develop `75ad0e55c` merged in, parents `450e3429d` + `75ad0e55c`, tree `75ed56fb4` = prediction).
  - Push 11:01:45Z → 11:07:39Z, rc 0. Preflight `12/15 legs ran, 3 SKIPPED. Nothing failed.`: legs 3 / 4 / 8 skipped (no stack), not a pass of those. Leg 1 `spec is in sync`, leg 5 59 / 59, shell suites 35 / 35.
  - Verify PROTOCOL-DIFF: Seat B's `push -u` of #1030 plus its PR-7 branch in `raise-0917-b-audit-2`. Ruled benign 11:09:40Z.
- **PR:** REST 201 #1031, base develop `75ad0e55c`. Title `KS-1213: derived-document writers refuse a caller type that differs from the type they store`. Body read back byte-equal: `Linear:` URL, BLUF (bug, measurement, rule, ruling time), Recommendation (residual, KS-1203 not widened), measured table, callers read, the change, cells, tamper table, Test Evidence, platform suites, PII, footer. Closing phrases 0, at-signs 0. Origin `refs/heads/<branch>` = `be8596a29` (ls-remote before creation).
- **Cells (85, in `ks1213-a-derived-writer-relabel-is-refused.test.ts`):**
  - **/version, /sign-cert, /sign-wallet × {ISSUER_ADMIN, SYSTEM_ADMIN, connector with documents:write}:**
    - 4 RED: PROPERTY_DEED on DOCUMENT, DEGREE on CERTIFICATE, a case variant, an array; each 400 with nothing saved;
    - 3 controls: equal type → 201 stored = served; no metadata → the source type; a legacy source keeps its own served label.
  - **issue + parent × 3 principals:**
    - 3 RED: PROPERTY_DEED, the parent's type on a `certificate`, a case variant; each 400 with `saveCertification` never called;
    - 3 controls: equal type 201; no `data.documentType` 201; no parent → not refused.
  - **#1024 N-B on the create guard:** case variant 400; array 400; legacy `{type X, data.documentType X}` 201; untyped `data.documentType DOCUMENT` 201.
  - **The connector's served type IS measured:** every connector-written row is read back through GET as SYSTEM_ADMIN, and the controls assert stored = served. The probe's own connector GET had returned no type, hence the admin reader.
- **Red-proof per writer:** RP-DEV-DOCS (`documents.ts` = develop) reds exactly /version 12, /sign-cert 12, /sign-wallet 12. RP-DEV-CERTS reds exactly issue 9.
- **One tamper per writer:** TN-VERSION / TN-SIGNCERT / TN-SIGNWALLET (`Date.now() < 0 &&`) red exactly their own writer's 12. TN-ISSUE reds issue 9.
- **Property tampers:** CASEFOLD-VERSION → /version 6 (case variant + array); SOURCEDATA-VERSION (comparing the merged `{...source.data, ...metadata}`) → the 3 legacy controls; NB-CASEFOLD → N-B 2; TI 0; T0 0.
  - Every row: 0 reds outside the file, 0 load failures, tsc 0.
  - Run 1's three `false &&` rows were VOID on TS18047, kept as a record.
- **Suites:** originate 64 / 741 at `450e3429d` and at `be8596a29`; tsc rc 0 at both; eslint 0 on the three files; KS-1061's guard green.
  - At `be8596a29` the worktree's installed modules predate #1027's originate lock change, and `npm ci` was not re-run. Named in the PR.
- **Stubs:** 4 ended by verified pid (started 21:04:3x AEST, cwd this worktree); 0 remain.
- **NOT covered:**
  - the gateway in front of originate;
  - a real issuer-certs upstream or CIP-8 signature;
  - a live database census of rows already served ≠ stored;
  - Schemathesis / Akto / Playwright / k6 (no stack).

