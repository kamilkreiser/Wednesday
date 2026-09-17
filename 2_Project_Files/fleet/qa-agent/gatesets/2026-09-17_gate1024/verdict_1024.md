SUBJECT: [QA -> Wednesday] TIER 1 GATE #1024 (KS-1202) d1a328088 — GO WITH FINDINGS
TS: 2026-09-17T09:03:57.000Z
AUTH: {'spf': 'pass', 'dkim': 'pass', 'dmarc': 'pass'}
QA -> Wednesday — TIER 1 GATE #1024 ROUND 1 of 2 (KS-1202) — composed 2026-09-17 19:02:18 AEST (clock from `date`)

VERDICT: GO WITH FINDINGS on d1a3280880d85ff31fd409aa1b5a16c428c4bb9a, as the delta over develop 581c9db0d, AND on the merged tree ccd3f281977eb0ddda4af2e555c074d30fddd3db = head + develop 81ee4b729e86a645fc9098aafa1aaf39035a9950 (#1021's squash; develop unchanged 18:39:29 -> 18:53:27 -> 18:58:51; drafter merged tree ccd3f2819 = mine).

Report: /Volumes/DevMASTER/!CODING/Testing Agent MAIN/projects/secuura/reports/2026-09-17-ks1202-1024-d1a328088-tier1-r1/report.md (evidence/ beside it; NOT-TESTED.written-first.md written 18:38:48, before any run)

== BLUF ==
- The create writer is CLOSED, end to end, for every carrier (MEASURED AT RUNTIME).
  - Stage A: originate in-process, 4 principals x 45 carriers. Head and merged: 0 creates served as a type other than the stored one. Develop: 54 (positive control).
  - Stage B: the REAL api-gateway app in front of a LIVE loopback originate (not a stub), 5 principals x 34 carriers. Head and merged: 0. Develop: 42.
  - Through the gateway: forwarded bodies byte-identical on every row; originate's status piped through on every row.
- No legitimate create is refused. 0 in-repo callers send `data.documentType`. The portal, Python SDK, add-in and legacy shapes answer the same on develop and head.
- Another writer is still open (NEW N-A, Major, pre-existing, not widened, NOT a Blocker against #1024).
  - `POST /api/documents/:id/version` with `metadata.documentType` stores DOCUMENT and serves PROPERTY_DEED, on develop = head = merged.
  - MEASURED through the real gateway: a `['DOCUMENT']`-restricted connector gets 201 and is served a type its allow-list refuses. No allow-list or enforcement applies to /version.
  - `sign-cert`, `sign-wallet` and `certifications/issue` + `parentDocumentId` follow the same pattern (READ ONLY).
  - The READY's C6 is create-only. Disposition: TICKET, carried on KS-1202 (stays In Progress).
- Tampers: 15/15 as predicted. The seat's 5 re-derive exactly: T0 0 / NOCHECK 10 / LOOSE 1 / WRONGSIDE 3 / TI 0. Every row: tsc 0, 63/656, pending 0, sha-restored.
- NEW N-B, Minor (test gap): I measured what each 0-red tamper lets through.
  - G-CASEFOLD silently reopens served != stored for 6 carriers (case variants, arrays, 7 vs '7').
  - Q-DOCTYPEONLY (mine) silently refuses 6 legitimate shapes, e.g. legacy `{type DEGREE, data.documentType DEGREE}`.
  - Disposition: SHIPS-WITH optional, else TICKET.
- Real-browser half of tier 1: does not apply. #1024 changes an originate route and a jest file; no rendered surface.

== Plain statements, items 1-10 ==

(1) CLOSED on the real create path — MEASURED AT RUNTIME.
- Stage A (seat harness + originate index.ts's json/urlencoded parsers; connector documents:write, ISSUER_ADMIN none, SYSTEM_ADMIN, plain user):
  - develop -> head: 54 mismatch rows 201 -> 400 BAD_REQUEST saved 0. The carriers: case, null, '', array, object, ZWSP, Cyrillic, duplicate data key last-mismatch, escaped key documentTyp\u0065, documentType over type, duplicate top-level documentType/type last-mismatch, untyped + data DEGREE, 7 vs '7', FORM data[documentType].
  - 6 null/'' rows 201 -> 400 (these served = stored at develop: R-1).
  - Legit 48 rows 201 = 201. The plain user is 403 on every row.
- Stage B (restricted ['DOCUMENT'] and ['DEGREE'] sk_, unrestricted sk_, Bearer ISSUER_ADMIN none, NONE human role issuer):
  - Head and merged: FAIL-1 (201 with served != stored) = 0.
  - FAIL-2 = 2: the ['DEGREE'] connector's untyped bodies, stored = served DOCUMENT. That is #1014r2 N-4, not a `data.documentType` carrier.
  - Mismatch carriers from a restricted connector: allow-list key DOCUMENT, enforcement resolved DOCUMENT, forwarded byte-identical, originate 400.
  - FORM and text/plain: 415 at the gateway. `type` arrays: 403 (restricted) or 400 VALIDATION_ERROR.
  - Head vs merged row diffs: 0.

(2) No legitimate caller refused.
- READ census: portal api.ts:303 and DocumentUpload.tsx:236, Python SDK client.py:207-220, add-in api.ts:112-126. None sends `data.documentType`. The other hits are verify-response readers.
- MEASURED 201 stored = served on develop = head = merged: portal, SDK, add-in, legacy CERTIFICATE, legacy matching, '' || type, untyped + data DOCUMENT, filled, lower-case equal, FORM matching. LEGIT refused at head: 0.
- Platform-S: NOT PREDICTABLE, not tested.
- Legacy mismatched rows (D2): GET 200 and list 200 for all principals, served PROPERTY_DEED on all trees. Versioning inherits it.
- R-3 Record (pre-existing): through the gateway, the add-in (application/pdf) and legacy CERTIFICATE are 400 UNKNOWN_DOCUMENT_TYPE on develop AND head, with the seed catalogue.

(3) Writer census (served = data.documentType || type).
- create: CLOSED.
- /:id/version: OPEN.
  - MEASURED Stage A: W01 PROPERTY_DEED on DOCUMENT, W03 DEGREE on CERTIFICATE.
  - MEASURED Stage B: the gateway mounts /api/documents/* behind authenticateToken + requireScope(documents:read OR documents:write), no allow-list, no enforcement. A restricted connector gets 201, served PROPERTY_DEED on GET and list.
  - A documents:read-only key passes the gateway and is refused only by originate RBAC 403 (R-4).
- sign-cert (:2705-2725), sign-wallet (:2800-2921), certifications/issue + parentDocumentId (certifications.ts:486-520): OPEN, READ ONLY.
- updateDocument callers and raw UPDATEs: no caller-set type (READ).
- Verify gate end to end: NOT TESTED. My instrument's POST /:id/verify returned 404 for the target AND the control, so the precondition failed.
- Ruling: not a Blocker against #1024. N-A Major, TICKET, carried on KS-1202.
- Fix-shape (prose): refuse `metadata.documentType` != source.type in each derived writer, or serve the stored type. Q-READSIDE shows the read-side closes every writer and turns the create cells red 10/656.

(4) Tampers (my head tree; whole originate suite 63/656, pending 0, tsc rc per row, anchor 1 + marker asserted, sha-restored + git diff --quiet on every row).
- Seat forms, verbatim from Seat A's tamper_1202.py (read only; D5 resolved):
  - T0 0; NOCHECK `!== dataDocumentType` 10; LOOSE 1; WRONGSIDE `!== rawType` 3; TI = inert comment 0.
- Drafter forms: D-NOCHECK `&& false` 10; D-TI swap 0; G-CASEFOLD 0; G-TRIM 0; G-TRUTHY 0.
- Mine:
  - Q-DOCTYPEONLY (`!== documentType`) 0.
  - Q-AFTERFILL (the check after :586 on the filled data.documentType) 0: an equivalent mutant.
  - Q-READSIDE (guard off + readers serve type) 10.
- VOID control (the seat's `if (false)`): tsc rc 2, TS6133 documents.ts(574,13) -> VOID.
- Red-proof (documents.ts = develop bytes): ks1202 19 run, 10 red (all toEqual), 9 green; whole suite 656, failed 10.
- Tamper x Stage A (what the 0s let through, MEASURED):
  - G-CASEFOLD: 8 rows change, 6 reopen served != stored, 1 goes to 500.
  - G-TRIM: 2 arrays reopen, 4 go to 500.
  - G-TRUTHY: null/'' admitted with served = stored (benign).
  - Q-DOCTYPEONLY: 6 legitimate shapes 201 -> 400.

(5) Suites, tsc, eslint.
- originate jest: develop 581c9db0d 62/637 · head 63/656 · merged ccd3f2819 63/656. 0 failed, 0 pending.
- tsc --noEmit -p .: rc 0 on all three trees.
- Test-including program (scratch tsconfig, quarantined after):
  - rc 0, 0 errors: develop 692 files / 66 __tests__; head and merged 693 / 67.
  - The ks1202 test is in it. Control: the project program (626 files) excludes it.
  - Plant -> 2 errors (TS2322 + TS6133), restored sha-equal.
- eslint: documents.ts 0 (develop, head); ks1202 test 0. The firing control hits @typescript-eslint/no-unused-vars on both.
- The PR's 2 files are byte-identical fix = head = merged: de9b5ae25 / ada07f053.

(6) OpenAPI: POST /api/documents already declares 400 (originate.openapi.ts:915). `npm run generate-openapi -- --check` at head: CHECK PASS. No spec entry needed; naming the condition in the 400 description is a Record at most.

(7) Persistence (READ ONLY; a real Postgres is NOT TESTED).
- saveDocument writes document_type = doc.type and metadata = {...data minus blockchain/signatures/walletAddress}, so data.documentType persists.
- fromDbRow spreads metadata over `documentType: row.document_type`.
- At head, every create has metadata.documentType absent or === type, so a round-trip serves the stored type.
- A legacy mismatched row, and any /version relabel, is served as its metadata type.

(8) Linear / GitHub, read 18:51:32 and again 19:02:08 (immediately before this mail):
- attachmentsForURL(pull/1024) = KS-1202 [In Progress] contributes only. Controls: pull/1019 -> 2 (KS-843, KS-1187), pull/99999 -> 0.
- 0 closing phrases in the title, the body (4,658 chars, 0 at-signs, KS-1202 x2) and all 3 commits. Planted regex controls [1,1,1,0,0].
- PR head = pin; 0 reviews; compare develop...head: merge_base 581c9db0d, diverged, ahead 3, behind 1, files 2.
- KS-1202 STAYS In Progress on merge (§5f: live sweep + N-A).

(9) Schemathesis / Akto: NOT REQUIRED.
- The only contract change is an already-declared 400 (CHECK PASS).
- The carrier census covered every value class a spec generator would produce, plus the ones it cannot (duplicate/escaped keys, __proto__, FORM), with 0 served != stored at head.
- `type` is not in DocumentCreateRequest, so a generator would not reach the legacy-key carriers.
- 0 auth or gateway files changed (api-gateway subtree 663f4555a on all trees), so Akto has nothing new to fuzz.
- Not run (NOT COMMISSIONED).

(10) Table below.

== CLOSED / STILL OPEN / NEW ==
- KS-1202 @ create: CLOSED. MEASURED (Stage A + B, head + merged). SHIPS-WITH #1024.
- N-A NEW: /:id/version stores X and serves Y; through the gateway a restricted connector is served a type its allow-list refuses. sign-cert / sign-wallet / certifications/issue + parentDocumentId READ.
  - Pre-existing (develop = head = merged); MEASURED + READ ONLY. Major.
  - TICKET, carried on KS-1202. Not a Blocker against #1024.
- N-B NEW: G-CASEFOLD / G-TRIM / Q-DOCTYPEONLY are 0 reds while measurably reopening served != stored (6 carriers), producing 500s, or refusing 6 legitimate shapes. MEASURED. Minor. SHIPS-WITH optional (owner), else TICKET.
- #1014r2 N-4: STILL OPEN, untouched. The untyped body from a restricted connector is stored = served DOCUMENT, even for a ['DEGREE'] connector. MEASURED. Minor. TICKET.
- R-1 Record: fail-closed exact equality; case variants, non-strings AND null/'' now 400.
- R-2 Record (D4, pre-existing): originate stores and serves non-string `type` (array, 7). The gateway refuses them, so they are reachable only directly to originate.
- R-3 Record (pre-existing): add-in and legacy CERTIFICATE are 400 UNKNOWN_DOCUMENT_TYPE at the gateway on develop = head.
- R-4 Record (pre-existing): a documents:read-only key reaches /version past the gateway scope; only originate RBAC refuses.

== PREDICTION SLIPS ==
- READY (seat) C6 "can no longer be served as a type other than the one stored": create-only (N-A).
- READY (seat) C1 "a non-string value is refused": true for data.documentType; a non-string top-level `type` is still stored and served (R-2).
- Wednesday's brief, item 1: "every mismatch carrier 201 served as the data type at develop (incl. null, '')". At develop null/'' serve DOCUMENT = stored. The drafter's C05 table row is correct.
- Drafter, forms only (counts equal): its NOCHECK (`&& false`) and TI (swap) are not the seat's forms (`!== dataDocumentType`; inert comment).
- Drafter Q2, "add-in / legacy 201 develop = head": true at originate; 400 at the gateway on both trees (R-3).
- #1014r2 N-1 relay "201 for every principal incl. the NONE human": with a real originate, the NONE human (role issuer) is 403 at originate for every body.
- Mine (kept, renamed, not deleted):
  - setup.out printed the develop test blob as 581c9db0d (a rev-parse echo); cat-file -e rc 128 proves it absent.
  - stageb_compare.py crashed twice before its table (a print format; a JSON-dropped undefined key).
- No slip on any measured count: red-proof 10/19, seat tampers 0/10/1/3/0, drafter G-* 0/0/0, suites 62/637 -> 63/656, plant 2 errors, eslint 0, OpenAPI PASS, merged OID ccd3f2819.

== MERGE ADDENDUM ==
squash `d1a328088` onto develop `81ee4b729e86a645fc9098aafa1aaf39035a9950` (merged tree `ccd3f281977eb0ddda4af2e555c074d30fddd3db`; drafter `ccd3f2819` — equal); #1024 attaches to KS-1202 only, linkKind `contributes`, no closes — KS-1202 stays In Progress on merge (§5f: live sweep owed; writers other than create: NOT closed — `/:id/version` MEASURED through the gateway (restricted connector served a type its allow-list refuses, develop = head = merged), `sign-cert` / `sign-wallet` / `certifications/issue`+`parentDocumentId` READ; carried on KS-1202 as N-A Major, not a Blocker against #1024); equality targets after the squash: `documents.ts` blob `de9b5ae25` / ks1202 test `ada07f053`; originate jest 62/637 at develop -> 63/656 at head -> 63/656 merged (re-measure); dispositions: KS-1202-create CLOSED SHIPS-WITH; N-A Major TICKET (carried on KS-1202); N-B Minor SHIPS-WITH optional else TICKET; #1014r2 N-4 STILL OPEN TICKET; R-2 (D4) Record; NEW: N-A, N-B, R-3 (add-in / legacy CERTIFICATE 400 at the gateway, pre-existing), R-4 (read-only key reaches `/version` past the gateway scope); Records for KS-1202's facts comment at merge: the fail-closed exact-equality rule (case variants 400), also `null` / `''` / non-string `data.documentType` 400 (served = stored at develop for `null`/`''`); the create guard does not cover `/version`, `sign-cert`, `sign-wallet` or `certifications/issue`; legacy mismatched rows stay readable and served as their data type; G-CASEFOLD / Q-DOCTYPEONLY 0 reds (regression cells owed: case variant, array carrier, legacy `{type X, data.documentType X}` -> 201, untyped + data DOCUMENT -> 201).

Escalation candidate (for Wednesday; nothing pushed by me): N-A. Kam may want to rule whether /version relabelling is carried on KS-1202 or split into its own ticket, before or after the merge.

== NOT TESTED (same prominence) ==
1. A real Postgres (KS-535). Item 7 is READ ONLY; all stored/served rows are in-memory.
2. The verify gate end to end on a relabelled document (my row 404'd on the control too).
3. sign-cert, sign-wallet, certifications/issue + parentDocumentId: READ ONLY.
4. A live Platform-S create: NOT PREDICTABLE.
5. Originate's real JWT verification in Stage B (a declared decode double); the real auth service, connector-token mint and Redis (fallback + stub).
6. The edge, nginx / Container Apps, any live stack, deploy.
7. Schemathesis / Akto / Playwright / k6: NOT COMMISSIONED (ruled NOT REQUIRED).
8. Preflight legs 3/4/8 and the real pre-push hook.
9. Platform suites beyond originate (api-gateway suites, shared, auth, frontend, SDKs).
10. A real browser (not applicable).
11. Concurrency / replay; a production catalogue shape.
12. How a real Postgres binds a non-string `type`.

== BOUNDS ==
- Checkout, 18:39:29 / 18:53:27 / 18:58:51 (each value identical at all three):
  - pull/1024/head d1a328088 (OK); develop 81ee4b729.
  - porcelain 0; .git/config d7e7298b02c45f52...; refs 925; .git/worktrees 112 (list 113).
  - branch feature/ks-597-b-caller-scoped-externalref @355d82c8b.
  - originate .vite ['vitest'], 0 entries newer than my marker.
- Listeners: 17 LISTEN rows at start, 19 at close.
  - The +2 are node pid 95956, cwd another session's gate1023 clone: NOT MINE, left alone.
  - My 3 originate hosts (127.0.0.1:49423-49425, pids 61155-61157, cwd my clone) exited rc 0 and closed their listeners; recount 0. 0 of my processes alive. 0 login_stub.mjs.
- docker info rc:
0
- No container created or touched.
- Nothing written to Linear, GitHub or the checkout. No push, no preflight.

