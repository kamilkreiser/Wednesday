auth: {'spf': 'pass', 'dkim': 'pass', 'dmarc': 'pass'}
Seat A

## BLUF
**READY FOR QA: PR #1035 (KS-1204) @ `4b1fb0621e58ff00bba096751130bc6e53df4714`, TIER 1.** The head was read from origin (`git ls-remote refs/pull/1035/head`) at 13:34:20Z; develop was `732c13459` in the same read.
- **N-2:** a connector `allowedDocumentTypes` that is configured but not an array (a string, an object, an empty string) now refuses every create with 403 FORBIDDEN before enforcement. A string used to substring-match. An absent, null or `[]` allow-list is unchanged (no restriction).
- **N-3:** two precedence cells pin `documentType` over `type`.
- **Tamper table at THIS head (58 / 565): 8 / 8 as predicted, 12 reds, all AssertionError.** RP-DEV 4, NOGUARD 4, STRING-ONLY 1 (object), FALSY-OPEN 1 (empty string), G-REV 2 (precedence), T0 / T0-DEFAULT / TI 0. Red-proof at develop: 4 red / 5 green as predicted.
- Push PROTOCOL-CLEAN; 4 stubs ended, 0 remain. Ticket comment `4ba94ee5-32a3-4a74-b984-bca7f9a12db1`; attachmentsForURL(pull/1035) = [KS-1204 contributes In Progress].
**Open PRs of this lineage: #1032, #1034, #1035 (cap 3 of 3).** Next: KS-1101 per your 13:30:57Z ruling. I start with its facts line and the consumer census, then build locally; it pushes when a slot frees.

## Recommendation
Gate #1035 at `4b1fb0621` (tier 1). **Veto points (my defaults inside your #1014 ruling):**
1. The refusal is 403 `FORBIDDEN`, matching the route's existing allow-list refusal.
2. An empty string counts as configured-but-not-a-list (refused), where it used to read as absent.
3. An untyped body is refused too under a non-array list (fail closed).

## Detail
- **File overlap** (PR files API, 13:2x): #1032 auth users.ts + ks1194 test; #1033 root + originate package files + baseline; #1034 api-gateway middleware/auth.ts + ks1215 test. #1035 = `services/api-gateway/src/routes/verification.ts` + the ks1204 test: no overlap.
- **The change:** commit `4b1fb0621` on develop 732c13459 (branch = Linear's name). `verification.ts` +11 −1: read `rawAllowedTypes`; not undefined / null / array → 403 FORBIDDEN "Connector document-type allow-list is not a list; refusing until it is corrected"; else `(rawAllowedTypes || []) as string[]` as before.
- **Cells (9)**, on the ks1176 harness (the real verification router and the real `enforceDocumentTypeRules` over the seeded catalogue; the workflow gate is a spy):
  - 🔴 string "SSD_DOCUMENT" vs DOCUMENT;
  - 🔴 ×3 non-array (string / object / empty string), each with the named type AND an untyped body;
  - control: array admits and refuses as before;
  - control: absent / null / [] unrestricted;
  - precedence ×2 (both directions; the admit cell also asserts enforcement resolved SSD_DOCUMENT; the refuse cell asserts the message names "DOCUMENT");
  - COMPLETENESS.
- **At `4b1fb0621`:**
  - tsc rc 0.
  - eslint: the test 0 / 0; `verification.ts` 0 / 5, equal to develop's 0 / 5.
  - Suite 58 / 565 at 60 s and at default; ks1204 9 / 9.
  - Runner `ks1204/build/tamper_1204.py` (per row: anchors pre-asserted against HEAD, tsc, denominator == T0, restore by blob sha + git diff --quiet; porcelain '' at the end; load 5–15).
- **Push:** 13:26:40Z → 13:32:55Z, rc 0. Preflight `12/15 legs ran, 3 SKIPPED. Nothing failed.` (legs 3, 4, 8 = no stack: NOT a pass of those); leg 1 spec in sync; leg 5 59/59; shell suites 35/35. verify PROTOCOL-CLEAN. Stubs: ps rows 1100, 4 targets (pids 2849, 2927, 3001, 3080), SIGTERM ×4, 0 alive, node listeners 4 → 0, non-node controls 17 → 17.
- **NOT covered / NOT run:** the admin settings write (`PUT /api/admin/settings` still stores any shape); a real Redis / platform-settings; the workflow-bypass config read on the same route (a string equality, no list semantics); Schemathesis / Akto / Playwright / k6 (no stack); the test-including tsc program (not measured).
- **Slip, none skipped:** the test file keeps the ks1176 harness's unused stub-originate route (serves a verify lookup no ks1204 cell calls). It is inert. I trimmed the unused `HUMAN_STANDARD` / `createDocument`, and the lint `prefer-const` it raised was fixed before commit.

