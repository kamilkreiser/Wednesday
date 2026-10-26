# Spark shadow gate, PR #1709 (KS-1554), head f1abd08594ecdc76fee9731be32459fc3f8ecd5f (UNSCORED; Wednesday scores against the Claude gate)
Spark verdict: **NO GO** (3 Major, 3 Minor, 1 Note). PR body: not supplied (gh not logged in). Review: 1 attempt, 105.5 s, 48541 prompt / 2041 completion tokens.
Deterministic half (no model), 36 s: 3 bash meta-suites, HEAD 36 passed 0 failed; BASE product code (head tests) 25 passed 11 failed in all 3 files (red on base, green on head). The 2 changed vitest files under services/security were NOT run (no install in the clone).
Spark Majors, in short: (1) empty baselines mean the ratchet now enforces zero errors (describes intended behaviour), (2) `__dirname` in an ESM-syntax test file would throw at runtime (not run; unverified), (3) m365-integration enrolment is outside the ticket (scope).
Checkable at source by Wednesday: the Spark Note says ks1513/ks1527 "are not run in the facts.json targeted runs" - facts.json lists all three suites (5, 4, 27 passed on HEAD), so that Note is wrong on the facts. All findings had quotes found in the input.
Raw: review.json, review/raw_attempt1.txt, facts.json.
