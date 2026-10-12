# QA GATE PR #1480 (KS-1000) -- verdict: GO WITH NOTE
Head a9b39631a74094e83c64d8ccb2b7c88c0feef747 (branch feature/ks-1000-..., one commit on merge-base 8dcbddb5a).
Predicted onto develop 5bfa5a804f63 (later than 22668829b029; merge clean, 4188d5f in my scratch clone). Own clone, no shared-repo writes.
Not checked: preflight 12/15 legs (needs stack; seat log not re-run); Windows (static reading only).

## Diff (5 files, +291): Blockchain/Dev/package.json (+1 script check:test-types), scripts/typecheck-tests/{check.cjs,baseline-auth.txt},
services/auth/tsconfig.test.json, services/auth/src/__tests__/ks1000-...test.ts (7 cells). No CI, hook, preflight, tsconfig.json change.
Wiring: check:test-types is referenced ONLY in package.json:44. Not in preflight.sh, .githooks/pre-push, docs. It runs only as the REAL cell inside the services/auth vitest suite.

## My runs
- 7 cells green on head. Seat mutants M2 always-exit0, M3 no-test refusal removed, M4 update admits, M5 stale ignored: each reds exactly the expected cell(s) (M2 reds 3 cells incl. RED/admit/stale). M1 real plant in a real test file: checker rc1 names file:line, REAL cell reds, control (restored) green.
- Own mutants: B1 allow-one-extra (3 red), B3 examined-not-tests (1), B4 key-ignores-code (2), B5 update-not-lowered (1), B9 realpath removed (5 red). SURVIVED (all 7 cells green): B2 tsc-silent guard (check.cjs:63), B6 run.error (:52), B7 bad baseline line skipped (:84), B8 --init overwrite guard (:100).
- Behavioural (behavioural_probes.txt): baseline entry removed rc1; second same-code error rc1; hand-raised count rc1 (stale: baseline is exact, cannot be raised silently); count+1 in baselined file rc1; broken tsconfig rc1; empty include rc2; prod-file error rc1; missing baseline rc1; CRLF/dup lines ok.
- Recompute: tsc -p tsconfig.test.json = 42 errors, 27 file+code entries, IDENTICAL to baseline-auth.txt (sorted diff empty). 0 @ts-nocheck/ignore/expect-error in tests (88 test files, 88 examined; no tests outside src/__tests__). tsconfig.test.json only drops the __tests__ exclude.
- services/auth head: 88 files / 920 tests, twice. Merged tree: 89 / 926. tsc -p tsconfig.json rc0 (both). eslint 0 errors, 15 warnings (control: warnings printed). Checker on merged tree: 139 files, 89 tests, 42/0 new/0 stale rc0.

## Defects (no Major)
1. Minor, ratchet not run by any gate: package.json:44 only. ks1000 test header lines 15-16 say the pre-push gate runs the auth suite; .githooks/pre-push has no vitest and preflight.sh header says it does not replace service tests. It runs only when someone runs the auth suite (the merge gate does).
2. Minor, check.cjs:54-62: file-less diagnostics (TS5033, TS5xxx) are ignored whenever any file-level error exists (probe 5c rc0 while tsc printed TS5033). Only exit-2 path is "no parseable diagnostic" (:63).
3. Minor, check.cjs:73-75: keyed file+code+count, so fixing one error and adding another of the same code in the same file passes (probes 2b, 3). When a count is exceeded, :129 lists every error of that key, naming the old one (issuerCert.test.ts:46) not the new one.
4. Minor, narrowing is unratcheted: a tsconfig.test.json exclude/include narrowing or a // @ts-nocheck in a new test hides errors (probes 6b-6d rc0); only floor is ks1000 test:114 (>50 of 88).
5. Minor, test gaps: four surviving mutants above; no cell for --init, tsc-crash (:63), unparseable baseline.
6. Minor, spaces in a file path make baseline unreadable (rc2, fail-closed; probe 7c); Windows listFiles separators fail closed via exit 2 (unrun). No such paths in repo.
