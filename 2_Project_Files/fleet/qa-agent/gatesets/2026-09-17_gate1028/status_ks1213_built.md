SUBJECT: [Secuura/Blockchain -> Wednesday] STATUS: KS-1213 built and red-proofed locally @450e3429d (11/11 tampers); KS-1180-P1 into the free slot
TS: 2026-09-17T10:46:43.000Z
AUTH: {'spf': 'pass', 'dkim': 'pass', 'dmarc': 'pass'}
Seat A

## BLUF
STATUS: **KS-1213 built and red-proofed locally at `450e3429ddd66a479231d259cd201fcddbe2b5a4`** (branch `feature/ks-1213-derived-document-writers-still-relabel-the-served-type-post`, parent develop `19f1e5475`). Not pushed. **Tamper table: 11 / 11 as predicted, 0 VOID**, whole originate suite 64 suites / 741 tests on every row. Originate 741 / 741 green, tsc rc 0, eslint 0 on the three files. It pushes (tier 1, `Refs KS-1213`) when a slot frees, after develop is merged in. Your veto on the comparison target (my 10:33:13Z STATUS) still stands open. Next: **KS-1180-P1 takes the slot #1018 freed.**

## Recommendation
No action needed unless you veto the certifications comparison target. If you do, I rework before its push.

## Detail
- **The change** (+25 in routes, +226 test):
  - `documents.ts`: in `/:id/version`, `/:id/sign-cert` and `/:id/sign-wallet`, right after the source 404 (and, for sign-cert, before the issuer-certs upstream call), `if (metadata.documentType !== undefined && metadata.documentType !== source.type)` answers 400 BAD_REQUEST `metadata.documentType must equal the source document type`.
  - `certifications.ts`: right after body validation, before the holder stub and `saveCertification`, `data.documentType` present and ≠ `type || 'verification_certificate'` with `parentDocumentId` set answers 400 BAD_REQUEST.
  - The comparison is exactly the KS-1202 create guard's.
- **Cells** (`ks1213-a-derived-writer-relabel-is-refused.test.ts`, 85, the real routers over one in-memory store, served type read back as SYSTEM_ADMIN):
  - per document writer × {ISSUER_ADMIN, SYSTEM_ADMIN, connector}: 4 RED (PROPERTY_DEED on DOCUMENT, DEGREE on CERTIFICATE, case variant, array) + 3 controls (equal type, no metadata, legacy source keeps its own served label);
  - issue-with-parent × 3 principals: 3 RED (incl. the parent's-type-not-cert-type shape and a case variant; `saveCertification` never called) + 3 controls (equal type, no data.documentType, no parent → not refused);
  - the #1024 N-B four on the create guard (case variant RED, array RED, legacy `{type X, data.documentType X}` 201, untyped `data.documentType DOCUMENT` 201).
- **Harness facts:**
  - `@secuura/shared` goes through `makeSharedMock` (KS-1061's guard caught my first draft's `requireActual` spread: 1 red, fixed before the commit). The routes' own shared imports (`hasNulByte`, `runWithTenantId`, `encryptField`, `decryptField`, `lookupHash`) pass the real implementations; only `verifyMessageSignature` is stubbed true.
  - The issuer-certs upstream is a loopback stub.
- **Red-proof and tampers** (`5_Project_History/2026-09-17_seatA-6th/ks1213/tamper/tamper.json`, 20:44:00 → 20:46:08 AEST; anchors 1, tsc per row, restore by sha + `git diff --quiet HEAD`):

| Row | Form | Reds in ks1213 (pred = measured) |
|---|---|---|
| T0 | none | 0 |
| RP-DEV-DOCS | documents.ts = develop bytes | /version RED 12, /sign-cert RED 12, /sign-wallet RED 12 |
| RP-DEV-CERTS | certifications.ts = develop bytes | issue RED 9 |
| TN-VERSION / TN-SIGNCERT / TN-SIGNWALLET | that writer's guard prefixed `Date.now() < 0 &&` | 12 each, only that writer |
| TN-ISSUE | the issue guard never fires | issue RED 9 |
| CASEFOLD-VERSION | /version compares `String(…).toUpperCase()` | /version RED 6 (case variant + array) |
| SOURCEDATA-VERSION | /version compares the merged `{...source.data, ...metadata}.documentType` | /version control 3 (the legacy-source control) |
| NB-CASEFOLD | the KS-1202 create guard case-folds | N-B RED 2 |
| TI | inert comment | 0 |

  0 reds outside the file on every row, 0 load failures.
- **Slips (both caught, recorded):**
  - **Guard insertion:** my first two edits targeted line numbers off by one. The scripts' content assertions refused before any write (`git diff` empty after each), and the third run anchored by route instead of line.
  - **Tamper run 1:** 3 rows VOID. `if (false && …)` made tsc answer TS18047 `'source' is possibly 'null'` and 12 suites fail to load. Kept as `tamper.run1-3-rows-VOID-false-and-unreachable`; the re-run uses `Date.now() < 0 &&`.
- **NOT run:** the gateway in front of originate, a real `sign-cert` upstream, a real CIP-8 signature, a live DB (legacy rows served ≠ stored are not censused), Schemathesis / Akto / Playwright / k6 (no stack). N-4 / KS-1203 untouched, as ruled.

