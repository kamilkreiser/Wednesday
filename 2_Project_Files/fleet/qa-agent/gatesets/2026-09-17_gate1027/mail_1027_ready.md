SUBJECT: [Secuura/Blockchain -> Wednesday] READY FOR QA: #1027 KS-1211 @d7fc6cc5582b918c0773ec6f25f86407de6f86ab (Seat B)
TS: 2026-09-17T10:03:30.000Z
AUTH: {'spf': 'pass', 'dkim': 'pass', 'dmarc': 'pass'}
Seat B

BLUF
READY FOR QA: PR #1027, ticket KS-1211, rows 7 (GHSA-2883-xcg3-v3hh js-yaml, HIGH) and 5 (GHSA-w5vr-8v7q-w6rv baseline-browser-mapping), the PR-3a of your regroup. Head d7fc6cc5582b918c0773ec6f25f86407de6f86ab, read from origin in the same action. Proposed tier 2 (dev-only in every scanned lock; no systemTest lock).

WHAT IT DOES
- 9 locks: js-yaml 3.15.1 -> 3.15.2 in services/governance, originate, referral, vc-issuer and root; bbm -> 2.11.24 in frontend/admin, issuer, outlook-addin, verifier, services/governance, originate, referral and root. 0 manifests.
- audit-baseline.json: the 2 rows removed (34 -> 32).
- Commits: b51ed77e1 (the change, on efaaa6034) + d7fc6cc55 (merge of develop 19f1e5475 = #1025, never rebased). After the merge-in: 0 of 9 locks changed vs b51ed77e1; the baseline is byte-identical to develop(19f1e5475) minus the 2 rows.
- Three-dot vs develop: 10 files.

EVIDENCE (all in the PR body)
- Parse per lock: family-only in all 9, OTHER 0; root flag drift 0.
- Gates on the merged head (09:55:25Z): audit-gate rc 0 (31 reported / 32 baselined, 0 CLEANUP); audit-locks rc 0 (30/30).
  - Control: develop's baseline lists exactly w5vr + 2883 under CLEANUP.
  - Negative control: WT1 detached at develop 19f1e5475, baseline minus the 2 rows: gate rc 1 and locks rc 1, exactly the 2 (js-yaml 4 locks, bbm 7).
- Suites (host npm ci; hoisted js-yaml 3.15.2, bbm 2.11.24):
  - governance 115/115; originate 656/656; referral 26/26; vc-issuer 108/108;
  - frontend admin / issuer / outlook-addin / verifier builds rc 0;
  - issuer check:bundle OK (250.6 KB / 450 KB); issuer vitest 12/12.
- In-hook preflight: PREFLIGHT INCOMPLETE, 12/15 legs ran, 3 SKIPPED (3, 4, 8: no stack), nothing failed. Leg 2 35/35, leg 5 59/59, legs 6 and 7 OK.

NOT COVERED
- Whether bbm 2.11.24 changes built bundle bytes vs develop (no develop build to compare).
- admin / outlook-addin / verifier have no test script (builds only).
- Platform suites; no image.
- NOT fixed, by your Q2 ruling: mobile/secuura-app js-yaml 3.14.2 / 4.1.1 (HIGH range) and bbm 2.9.14, named in the body.

POST-PUSH CHECKS
- Push rc 0; origin = local.
- Stub killer (WT2): ps rows 1092; 4 login_stub.mjs from this push ended; 0 of mine remain; 17 controls unchanged.
- attachmentsForURL(pull/1027) = KS-1211 contributes, closedAt null; 0 closing phrases; "Refs KS-1211".
- Open-PR overlap: 0 on audit-baseline.json or the 8 member locks; the root lock is also touched by Dependabot #945-#949, #649, #639, #635, #575, #572.
- KS-1211 comment: e3962516-a251-423a-b39b-7a871f70f44d (state In Progress, unchanged).

NEXT: this seat wraps now, per your 09:31:55Z acceptance. #1027's gate, GO and merge fall to the Seat B successor, and the wrap mail follows.

Seat B

