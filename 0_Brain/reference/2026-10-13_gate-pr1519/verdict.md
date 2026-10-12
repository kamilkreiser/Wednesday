# QA gate: Secuura PR 1519 (KS-1518 message half)

- Head under test: 0b0546e73d3873935386327e01df7e10153fa5bf (fetched from refs/pull/1519/head, equals the claimed 0b0546e73d38)
- Base: b2085e99ff1c; develop now 898a1ae11f3cf006cb27c45eb0aebaf562bd4632 (git ls-remote read by me)
- Tree method: scratch clone (git clone --shared, fetch of both refs), git archive of head and base into fresh dirs (g19/head, g19/base), node_modules shell of symlinks to the main checkout's deps (read-only), @secuura links relative so they resolve into the scratch tree, packages/shared built fresh in each tree.
- Tier: 3 (through-code only)

## VERDICT: GO

Majors: 0. Minors: 0. Notes: 1 (below).

## Findings

- Major: none. No accept/refuse decision changed (41-value sweep, 0 decision diffs). No new throw.
- Minor: none.
- Note (not a defect): the new text also changes for EVERY bigint, not only 1n: 0n now prints 0n, -1n prints -1n, 10n**30n prints a trailing n. This is the intended generalisation (typeof bigint) and the property cell covers 0n, -1n, 1n. Boxed Object(1n) and new Number(-0) still print 1 and 0 (typeof object); an unreachable-from-JSON edge, same class as the stated out-of-scope array/object ambiguity.
- Pre-existing, unchanged by the PR: Object.create(null) and Object(Symbol()) make String(value) throw a TypeError while building the message (old and new alike). A primitive Symbol does NOT throw in either path (prints Symbol(x)); the new code adds no Symbol throw.

## What I ran

1. Topology: git diff base..head is 2 files, +45 -6 (verification.ts +2/-1; the test file). git merge-tree --write-tree develop(898a1ae1) head is clean, tree a16cb63be4272fa6cce16999d1cf0e6d36a5ac36 (matches the builder's a16cb63be427). merge-base is b2085e99ff1c.
2. Product line read: shown = typeof value==='string' ? JSON.stringify : typeof bigint ? `${value}n` : Object.is(value,-0) ? '-0' : String(value). Table below was produced by extracting the real function from the base and head files and running both (script g19/tbl.js in my scratchpad).
3. Changed test file at head: 18 passed (18). Against the BASE product with the head test file copied in: 3 failed / 15 passed; the 3 are the two RED KS-1518 cells (1n, -0) and the property cell. Base test file restored afterwards.
4. Full api-gateway suite at head: 116 files / 1119 tests passed, 0 failed (once; includes the neighbouring ks1185 files). 
5. tsc --noEmit -p services/api-gateway: rc 0 at head and base. check:test-types for api-gateway: 35 errors, 35 in baseline, 0 new, 0 stale.
6. ESLint on verification.ts: 5 warnings, 0 errors at head (lines 652,1059,1178,1494,1570) and the same 5 at base (lines 651,1058,1177,1493,1569; shifted by the one added comment line). Pre-existing confirmed.
7. Mutants (head tree, verification.ts mutated then restored, sha256 of restored file equals original e8ca6c2f3e8f9245; script g19/mut.py), result = failing cells:
   - M0 no-mutation control: 18 passed.
   - M1 revert to String(value): 3 failed (1n, -0, property).
   - M2 n as prefix: 1 failed (1n cell only).
   - M3 bigint bare: 2 failed (1n, property).
   - M4 -0 prints 0: 2 failed (-0, property).
   - M5 zeros swapped (+0 prints -0): 2 failed (the "0" refused row, property); the -0 cell stays green because the swapped code still prints -0 for -0.
   - M6 strings not JSON.stringified: 2 failed (string '800' row, property).
   - M7 bigint test made typeof number: 9 failed.
   - M8 own: uppercase N suffix: 1 failed (1n cell).
   - M9 own: negative bigint unsuffixed: 1 failed (property cell only; the 1n cell cannot see it).
   - M10 own: -0 branch dropped: 2 failed (-0, property).
   - M11 own: refusal bound changed to >= 0: 3 failed (0 row, -0, property).
   All 12 non-control mutants killed; control exact.
8. Refusal decision: the sweep of 41 values (table below, includes 0/-0/0n/NaN/+-Infinity/2147483647/2147483648/strings/objects/undefined) shows identical accept/refuse and identical accepted return value old vs new.
9. Reachability: /usr/bin/grep -rl originateForwardTimeoutMs over api-gateway/src: product hits only routes/verification.ts, 3 test files (positive control: the grep finds them). index.ts has 0 hits (createVerificationRoutes appears 3 times there, so the file was read), so no running gateway passes an override.

## Old vs new print table (text inside "(got ...)"; ACCEPT = no refusal)

| value | old String() path | new path | diff |
|---|---|---|---|
| 1 | ACCEPT 1 | ACCEPT 1 | same |
| 0 | (got 0) | (got 0) | same |
| -0 | (got 0) | (got -0) | CHANGED |
| -1 | (got -1) | (got -1) | same |
| 1.5 | (got 1.5) | (got 1.5) | same |
| NaN | (got NaN) | (got NaN) | same |
| Infinity | (got Infinity) | (got Infinity) | same |
| -Infinity | (got -Infinity) | (got -Infinity) | same |
| 2147483647 | ACCEPT 2147483647 | ACCEPT 2147483647 | same |
| 2147483648 | (got 2147483648) | (got 2147483648) | same |
| 1e21 | (got 1e+21) | (got 1e+21) | same |
| 5e-324 | (got 5e-324) | (got 5e-324) | same |
| MAX_SAFE | (got 9007199254740991) | (got 9007199254740991) | same |
| 1n | (got 1) | (got 1n) | CHANGED |
| 0n | (got 0) | (got 0n) | CHANGED |
| -1n | (got -1) | (got -1n) | CHANGED |
| 10n**30n | (got 1000000000000000000000000000000) | (got 1000000000000000000000000000000n) | CHANGED |
| "1" | (got "1") | (got "1") | same |
| "" | (got "") | (got "") | same |
| "a\"b" | (got "a\"b") | (got "a\"b") | same |
| true | (got true) | (got true) | same |
| false | (got false) | (got false) | same |
| null | (got null) | (got null) | same |
| undefined | ACCEPT 15000 | ACCEPT 15000 | same |
| Symbol("x") | (got Symbol(x)) | (got Symbol(x)) | same |
| Symbol() | (got Symbol()) | (got Symbol()) | same |
| {} | (got [object Object]) | (got [object Object]) | same |
| [] | (got ) | (got ) | same |
| [1] | (got 1) | (got 1) | same |
| {toString} | (got T) | (got T) | same |
| Object.create(null) | Cannot convert object to primitive value | Cannot convert object to primitive value | same |
| throwing toString | boom | boom | same |
| new Number(5) | (got 5) | (got 5) | same |
| new Number(-0) | (got 0) | (got 0) | same |
| ()=>1 | (got ()=>1) | (got ()=>1) | same |
| new Date(0) | (got Thu Jan 01 1970 10:00:00 GMT+1000 (Australian Eastern Standard Time)) | (got Thu Jan 01 1970 10:00:00 GMT+1000 (Australian Eastern Standard Time)) | same |
| Object(1n) | (got 1) | (got 1) | same |
| Object(Symbol()) | Cannot convert a Symbol value to a string | Cannot convert a Symbol value to a string | same |
| 100 | ACCEPT 100 | ACCEPT 100 | same |
| 60000 | ACCEPT 60000 | ACCEPT 60000 | same |
| -5 | (got -5) | (got -5) | same |

Text diffs: 5 (-0, 1n, 0n, -1n, 10n**30n), all of them -0 or bigint. Decision diffs: 0.

## NOT TESTED

- A live gateway (no override reaches this message; not reachable from index.ts).
- Second full-suite run (ran once, 1119/1119; the builder's twice claim not repeated).
- Builder's M-numbering mutants beyond those I rebuilt (my M1-M7 map to the claim's classes; M8-M11 are mine).
- Refused arrays/objects ambiguity (declared out of scope), other Node versions (Node used here is the machine default).
- CI, preflight legs, other services' suites, frontend.
