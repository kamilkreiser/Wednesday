# Gate PR #1486 (KS-1267) head 1c02cda6cf9798253997b2d91e9303e0bdda3684 - GO WITH NOTE

Bundle sha256/16 d02096fa875579bf verified; head reconstructed on develop 524db0ce (shared repo was stale; base taken from an earlier scratch clone). Merge == head (head sits directly on 524db0ce, one test file).
Originate suite 97/1109 x2 green; ks1228 file 31/31; tsc 0 errors (src and the test via a gate tsconfig); eslint clean (test + documents.ts).
Mutants on routes/documents.ts (transfer-custody, tx at :1860-1892): M1 ticket MOVE -> only cell 2 red; M2 record before tx -> cells 2+3 red; M3 swallow flip -> cell 2 red; M6 record at tx start -> 2+3 red; M7 no flip -> G-S1 + cell 2 red; M8 guard no throw -> cell 3 red.
Survivors: M5 (record after flip inside tx, before commit) 31/31 green; M9 (flip SET to fromHolderId) 31/31 green.

Defects
1. Minor: test:~351 - mocked $executeRaw ignores its args and has no commit/rollback model, so wrong owner value (M9) and record-inside-tx-before-COMMIT (M5) are undetected; cell 3 title claims "owner never flipped" but only asserts write order.
