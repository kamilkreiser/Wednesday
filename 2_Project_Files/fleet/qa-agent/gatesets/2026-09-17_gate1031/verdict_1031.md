auth: {'spf': 'pass', 'dkim': 'pass', 'dmarc': 'pass'}
QA -> Wednesday: TIER 1 ROUND 1 (of 2) gate on Secuura/Blockchain PR #1031 (KS-1213, Seat A). Composed and sent 2026-09-17 23:11:49 AEST (clock from `date`). Findings only.

## VERDICT
GO WITH FINDINGS on `be8596a29af15477cb0cbf4b8684e35e63c38e9f`, as the delta over develop `75ad0e55c`, AND on the merged tree `007cca4290fb313744e4c076116241f2a00538eb`.
- The merged tree is head x develop `27e53ec3aa010b50cd9b2e4a1d15cbb34605ba7d`. develop moved before my first reading (#1028, #1030, #1029), and the move touches no originate / shared / openapi / eslint path.
- No Blocker. D1 is Minor and pre-existing: TICKET. The D2 and Q test gaps are Minor: SHIPS-WITH optional cells, else TICKET. L01 is a Record; L03 stays STILL OPEN (ruled).
- Real-browser half of tier 1: does not apply. #1031 changes two originate route handlers and one jest file; there is no rendered surface.

Report: /Volumes/DevMASTER/!CODING/Testing Agent MAIN/projects/secuura/reports/2026-09-17-ks1213-1031-be8596a29-tier1-r1/report.md (NOT-TESTED.written-first.md written 22:46, before any run; evidence/ beside it)

## ITEMS 1-10
1. CONTRACT (MEASURED AT RUNTIME, real routers in-process; 506 rows per tree x develop / head / merged).
   - Principals: ISSUER_ADMIN (level none), SYSTEM_ADMIN, a docs connector, a certs connector, a plain user.
   - Harness: one loopback upstream counting sign / users/stub / anchors, with AUTH_SERVICE_URL and ANCHORING_SERVICE_URL both pointed at it; parsers as index.ts (json + urlencoded).
   - Head: 278 caller-type refusals (400 BAD_REQUEST) with 0 derived rows, 0 saveCertification, 0 sign calls, 0 users/stub, 0 anchors, 0 verifyMessageSignature and 0 events. Provenance 1 (D1).
   - develop, same rows: 278 derived, 54 certifications, 74 sign calls, 3 stubs, 54 anchors.
   - Head 201 stored != served: only the ruled legacy inheritance (L03, its in-memory twin D01, 2 chain steps); none has a caller type.
   - merged = head on every value column. FAIL condition: not met.
   - D1 row `V-OBO` (docs connector, /version + onBehalfOf + PROPERTY_DEED): head 400, provenance 1; develop 201, provenance 1.
   - holderEmail row `I-I14`: head 400, users/stub 0, anchors 0, saveCertification 0; develop 201, stub 1, anchors 1, served PROPERTY_DEED.
   - I-OBO (issue + onBehalfOf): head 400, provenance 0.
   - D1 RULING: Minor, pre-existing class, NEW finding, TICKET. `V-OBO-404` and `V-OBO-HASH` record provenance 1 on develop AND head (handleOnBehalfOf `documents.ts:1951` precedes every later refusal); #1031 adds one more trigger and does not widen the class. It writes an action_provenance row for the SOURCE id, action version:watermark, for an action that never happened. The READY's C1 ("before any write") needs this qualifier.
2. HUNT: no caller-supplied path relabels at head.
   - Census re-derived with git grep -P and controls run through git grep. The only `...metadata` spreads are the 3 guarded writers; saveLineageDocument appears only at the guarded issue path.
   - NEW READ: api-gateway `startup-migrations.ts:678-686` also writes `documents` (tenant_id only). That is a slip against the drafter's "no other service".
   - Shapes all refused or benign: non-string (incl. true / false), NBSP, combining mark, ZWSP, Cyrillic, full-width, `__proto__` / `constructor` raw keys, duplicate / escaped keys, and FORM-ENCODED `metadata[documentType]` / `data[documentType]` (urlencoded is mounted).
   - text/plain and merge-patch+json bodies: body {}, no relabel.
   - Principals: single-scope connectors 403 cross-wise, plain user 403, SYSTEM_ADMIN = ISSUER.
   - Legacy: L01 400 (was 201), L02 201, L03 201 stored CERTIFICATE served DEGREE (ruled). Untyped / '' sources (D01-D05) are in-memory only; Postgres reads type as `document_type || 'document'`.
   - Chains: issue-derived -> version -> sign-cert are all guarded. L03 propagates along version / sign chains with no caller type; sign-wallet + the stored type repairs it.
   - Legacy issue `documentId` path: caller data.documentType lands in certification_metadata (`$executeRaw` 1) but is never served (fromDbRow READ). Record.
   - Postgres READ: a derived row round-trips stored = served for any non-legacy source.
3. TAMPERS on the whole originate suite: 21 / 21 as predicted, 0 VOID, every row tsc 0, 64 / 741 pending 0, 0 reds outside the file, 0 load failures, restored sha + diff rc 0.
   - The seat's 11 EXACT forms, read from its tamper.py (not rendered): T0 0, RP-DEV-DOCS 12/12/12, RP-DEV-CERTS 9, TN-VERSION 12, TN-SIGNCERT 12, TN-SIGNWALLET 12, TN-ISSUE 9, CASEFOLD-VERSION 6, SOURCEDATA-VERSION 3 (controls), NB-CASEFOLD 2, TI 0.
   - The drafter's 6, each 0 reds, consequence re-measured on the tampered tree:
     - X-SIGNCERT-AFTER-UPSTREAM: sign 1 on a refusal;
     - X-ISSUE-AFTER-HOLDER: users/stub 1;
     - X-ISSUE-AFTER-ANCHOR: anchors 1;
     - X-ISSUE-LOOSE: 7 / array / object / true -> 201 served the non-string;
     - X-VERSION-TRIM: served 'DOCUMENT ';
     - X-SIGNWALLET-SERVED: legacy + DEGREE -> 201 served DEGREE.
   - Mine, one per writer, each 0 reds:
     - Q-VERSION-TRUTHY: null / '' / false -> 201, stored = served, benign;
     - Q-SIGNCERT-UNTYPED-SOURCE-SKIP: an untyped source + DEGREE -> 201 served DEGREE, in-memory only;
     - Q-SIGNWALLET-AFTER-VERIFY: verifySig 1 on a refusal, CPU only;
     - Q-ISSUE-AFTER-OBO: provenance 1 on a refused issue (the D1 class, unpinned on issue).
   - D2 RULING: the users/stub (it mints an INVITED user in auth) and anchors side effects on a refused request are load-bearing for tier 1. Cells are recommended SHIPS-WITH. Not a Blocker: the runtime at head is correct.
4. MERGE-IN (my clone): merge-tree `450e3429d` x `75ad0e55c` = `75ed56fb4` = head tree.
   - File sets 14 = 14, per-file patch-id mismatches 0, whole-delta `a990435d0` both.
   - Nothing under originate/src; the only originate path is package-lock.json (#1027). The 3 files are byte-identical fix = head.
   - C5: my farm (the checkout install) differs from develop's lock: js-yaml 3.15.1 vs 3.15.2, baseline-browser-mapping 2.10.29 vs 2.11.24. Neither is on the guard's path. Record.
5. SUITES: originate develop 63/656, head 64/741, merged 64/741; tsc -p rc 0 x3.
   - Test-including tsc program (config outside the service root): head rc 0, 0 errors, ks1213 in program True / project False, __tests__ 68 (develop 67). The plant gives 2 errors.
   - eslint by rule + message: 0 / 0 / 0 on the 3 files. The same-file plant fires @typescript-eslint/no-unused-vars.
   - Probe placement: outside the service root. At head, jest --listTests 64 files / 0 qa_probe (ks1213 listed); tsc --listFilesOnly 0 qa_probe (documents.ts listed).
6. OPENAPI: 400 is declared on all four (`originate.openapi.ts:1137 / 1202 / 1272 / 2179`); generate-openapi --check CHECK PASS at head.
   - R-a (Polish): sign-wallet's 400 description names only VALIDATION_ERROR / INVALID_WALLET_SIGNATURE, not BAD_REQUEST.
   - Residual census (READ): 0 in-repo callers of sign-wallet, sign-cert, the /version route or parentDocumentId in frontend / sdk / connectors / mobile / api-gateway src / mcp-server / tests / packages (controls fire in originate). certifications/issue callers (portal, SDKs, connectors, e2e, perf) send no parentDocumentId.
   - Residual Record: an out-of-repo caller sending a differing type, or a legacy served label (L01), now gets 400.
7. MERGED TREE: `007cca4290fb313744e4c076116241f2a00538eb` (head x develop `27e53ec3a`; commit-tree `ae716c9c9` in my clone), 0 conflicts. newdev..merged = the 3 PR files at their blobs. Items 1 and 5 were re-run on it: equal to head.
8. LINEAR / GITHUB, at 23:00-23:01 and pre-mail 23:09:51 / 23:10:09, equal:
   - attachmentsForURL(pull/1031) = KS-1213 contributes only (pull/1024 -> KS-1202; pull/99999 -> 0);
   - 0 closing phrases in title, body and both commits (planted controls 1/1/0);
   - KS-1213 In Progress, stays In Progress on merge (§5f); KS-1203 Backlog, no #1031 attachment, not widened.
   - R-e: open PR #1033 (new since drafting) touches originate package.json + lock (merge-order note).
9. SCHEMATHESIS / AKTO: NOT REQUIRED (not run, not commissioned).
   - Contract unchanged: 400 already declared, CHECK PASS.
   - The class needs a type differing from a server-side stored type on an EXISTING source plus a later GET; random {id}s answer 404 before the guard (measured N01).
   - The Schemathesis baseline already ACCEPTS positive_data_acceptance for all four ops (KS-591), so the new rule falls in an accepted class.
   - Akto: no auth / scope / route change; the principal matrix was measured develop = head.
10. CARRY-FORWARD: the table below.

## CLOSED / STILL OPEN / NEW
- KS-1213 /version (#1024 N-A): CLOSED - MEASURED - PR - SHIPS-WITH
- KS-1213 /sign-cert: CLOSED - MEASURED (loopback upstream) - SHIPS-WITH
- KS-1213 /sign-wallet: CLOSED - MEASURED (signature stubbed) - SHIPS-WITH
- KS-1213 issue + parentDocumentId: CLOSED - MEASURED - SHIPS-WITH
- #1024 N-B: CLOSED for the case + array cells (NB-CASEFOLD 2 reds); legacy / untyped controls READ present - SHIPS-WITH
- D1 (/version provenance before the guard): NEW, pre-existing class - MEASURED - Minor - TICKET
- D2 (drafter's 6 unpinned properties): NEW test gap - MEASURED - Minor - SHIPS-WITH optional cells (stub / anchors recommended), else TICKET
- Q-ISSUE-AFTER-OBO / Q-SIGNCERT-UNTYPED-SOURCE-SKIP / Q-VERSION-TRUTHY / Q-SIGNWALLET-AFTER-VERIFY: NEW test gaps - MEASURED - Minor / Polish - SHIPS-WITH optional, else TICKET
- D3 L01 (legacy served label echoed -> 400): Record - MEASURED - SHIPS-WITH (facts comment)
- D3 L03 (legacy inheritance, no caller type): STILL OPEN (ruled) - MEASURED in memory + READ Postgres - TICKET (§5f live census)
- KS-1203 / N-4: STILL OPEN, untouched - READ + RELAYED - TICKET (KS-1203)
- #1024 D4 (create does not string-check type): STILL OPEN, untouched - READ - Record / TICKET
- R-a sign-wallet 400 description: NEW - READ - Polish - SHIPS-WITH optional, else Record
- R-b legacy documentId path -> certification_metadata: NEW Record (not served) - MEASURED + READ
- R-c api-gateway startup-migrations writes documents.tenant_id: NEW Record - READ
- R-d farm != develop lock (C5): Record - MEASURED
- R-e open PR #1033 touches originate package.json + lock: Record for the merge seat

## NOT TESTED (equal prominence)
- A real Postgres round-trip (KS-535). The live census of rows already served != stored (C9 / §5f).
- The api-gateway stage and gateway verify gate. A real issuer-certs upstream, real CIP-8 signature, real anchoring, real auth users/stub (one counting double; verify stubbed true).
- What recordActionProvenance really writes (READ `provenance.ts:215-218`; resolveOnBehalfOf stubbed null).
- #1024 G-TRIM / Q-DOCTYPEONLY create tampers vs the new N-B cells. rejectNulBytes not mounted.
- Schemathesis / Akto / Playwright / k6 (not commissioned). A real browser (n/a). Platform suites beyond originate; preflight legs 3/4/8.
- Out-of-repo callers (NOT PREDICTABLE). Concurrency / replay. A clean npm ci from develop's lock. The launcher's develop-moved arm (judged by content, launcher not run).

## PREDICTION SLIPS
- READY (seat) C1: "before any write" is false for /version + connector onBehalfOf (D1). All other seat counts matched.
- Drafter: "no other service writes documents" (api-gateway startup-migrations, tenant_id only). Seat forms rendered, not read (TI is above the guard, not after; counts equal). All drafter counts matched, 204 / 204 rows identical per tree.
- Mine, kept:
  - the first census used git grep -E (no \s / \b), and its control did not run through git grep;
  - the probe placeholder assert said 36 (19), which left the head collector proof to a separate run before the tampers;
  - the residual census crashed once;
  - the analyzer counted 279 refusals (one is the human-OBO refusal on both trees: 278);
  - one "control" tsc line ran after the plant was removed and controls nothing;
  - the start listener census counted my own tool shell as 1 process.

## BOUNDS / LISTENERS
- Checkout (22:47:56 / 23:01:47 / 23:09:06): porcelain 0 / 0 / 0; .git/worktrees 112 x3 (setup before = after 112); config sha `f9ef2cb7e4b9fa5a` x3; refs 941 / 942 / 942 (other sessions; not attributed); branch feature/ks-597-b-caller-scoped-externalref x3; originate .vite ['vitest'], 0 newer x3; refs/pull/1031/head `be8596a29` x3; origin develop `27e53ec3a` x3.
- docker info rc 0, run once; no container.
- Listeners: start 22:48:01 = 18 LISTEN rows, 0 node, 0 login_stub.mjs. Close 23:09:06 = 17 rows, 0 node, 0 login_stub.mjs, 0 processes naming my workdir.
- Each of my 13 probe runs bound 127.0.0.1:0 x2 and closed both: 0 LISTEN rows on the recorded ports after exit. No kill needed.

## MERGE ADDENDUM
"squash `be8596a29` onto develop `27e53ec3aa010b50cd9b2e4a1d15cbb34605ba7d` (then-current at 23:09:06; `75ad0e55c` at draft close) (merged tree `007cca4290fb313744e4c076116241f2a00538eb`; drafter `75ed56fb4` = head tree while develop was an ancestor); #1031 attaches to KS-1213 only, linkKind `contributes`, no closes; KS-1213 stays In Progress on merge (§5f: live census of rows already served != stored owed); KS-1203 not widened into; equality targets after the squash: `documents.ts` e3eeb5a68 / `certifications.ts` 20934ee94 / ks1213 test 808282689; originate jest 63/656 at develop -> 64/741 at head -> 64/741 merged (re-measure); dispositions: KS-1213 four writers CLOSED SHIPS-WITH; #1024 N-B CLOSED SHIPS-WITH; D1 Minor TICKET; D2 Minor SHIPS-WITH optional cells (users/stub 0 + anchors 0 on a refused issue recommended; non-string data.documentType on issue) else TICKET; L01 Record; L03 STILL OPEN TICKET; KS-1203/N-4 STILL OPEN TICKET; #1024 D4 STILL OPEN Record; NEW: Q-ISSUE-AFTER-OBO, Q-SIGNCERT-UNTYPED-SOURCE-SKIP, Q-VERSION-TRUTHY, Q-SIGNWALLET-AFTER-VERIFY (Minor test gaps, SHIPS-WITH optional else TICKET), R-a sign-wallet 400 description omits BAD_REQUEST (Polish), R-b legacy documentId path copies data.documentType into certification_metadata (not served, Record), R-c api-gateway startup-migrations writes documents.tenant_id (Record), R-d farm != develop lock (Record), R-e open PR #1033 touches originate package.json + lock (merge order); Records for KS-1213's facts comment at merge: the exact rule (case / whitespace / NBSP / combining / confusable / non-string incl. null, '', true, false, arrays, objects, and form-encoded carriers -> 400 BAD_REQUEST before any derived row, certification, sign call, holder stub or anchor), L01 (a caller echoing a legacy source's served label is now 400), L03 (legacy inheritance with no caller type is still served as the legacy label and propagates along version / sign chains), the out-of-repo caller residual (0 in-repo callers), D1 (a connector's refused /version with onBehalfOf still writes an action_provenance row for the source; pre-existing ordering, also on 404 / bad hash; TICKET), and the same provenance-before-guard class unpinned on issue (Q-ISSUE-AFTER-OBO)."

Escalation candidates (for Wednesday, not actioned by QA): a D1 ticket (provenance after the derived save on /version); optional cells on #1031 for the refused-issue users/stub and anchors side effects.

