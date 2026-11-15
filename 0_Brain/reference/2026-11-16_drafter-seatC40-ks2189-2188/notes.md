# Drafter notes: Seat C 40th, KS-2189 + KS-2188 kyc erasure (2026-11-16 02:3x AEDT)

Brief: /Volumes/DevMASTER/WEDNESDAY/2_Project_Files/fleet/briefs_staged/2026-11-16_seatC40_ks2189_2188_kyc_erasure.md (34,932 bytes)

## Measured
- Ordinal: `Seat C 40th` count 0, `Seat C 39th` count 1 in /Volumes/DevMASTER/!CODING/Secuura/Blockchain/5_Project_History/history.md (02:3x). Brief named C40.
- Precondition MET: PR 2231 merged 2026-11-15T07:12:59Z (240d1f664b52), PR 2236 merged 2026-11-15T09:41:29Z (9cbb9687021a); both ancestors of develop a5e13a242917 (ahead 26 / 16, behind 0). Develop unchanged 02:31 to 02:34.
- Tickets: both Backlog, P3 (2189) and P4 (2188), 0 comments, not updated since 2026-11-12.
- Open PRs: 71, 371 file rows, 0 API errors; services/kyc only in dependabot 575 and 649 (package.json); control services/transfer = 7. No PR doing this work.
- Code at develop (index.ts 1,434 lines, blob e2bef0b96435): dbDeleteUserData 374, read 223 (Promise.all inside the try), rowToVerification 417 (three undecodable causes incl. checks at 486), initiate schema 568, DELETE route 1274 with KS-2185 try/catch in place.
- services/kyc/tsconfig.json excludes src/__tests__; check:test-types script (package.json line 44) does not list kyc.
- load1 9.45 at 02:31, 4.91 at 02:34 (brief carries the gate of 8).

## Findings the brief carries beyond the ANSWER
1. The ANSWER's "fold the READ" collides with dbGetVerificationsByUser being shared with GET /user/:userId: brief defaults to erasure-only, folding the shared read is a plan QUESTION.
2. Kelvin cell: a GUID has no `k` (C 39th trap d), so the cell must run on a non-GUID id through the bus handler or the function; Postgres lower() on the column cannot be proven by a fake. Brief says so and tells the seat to report it vacuous rather than pad.
3. Honest red sets: on develop only P1, P5, P6 (and B1 via P1) are red for KS-2188; P2/P3/P4/P7 are already green (develop throws and keeps everything) and exist to kill mutants m6 to m9. A first draft said "all red"; corrected.
4. A per-row catch around rowToVerification also closes the third cause (checks) for the erasure read; the ANSWER files it, brief keeps it a filing.
5. Retry converges (idempotent, same kept row, throws again, dead-letter).
6. PR titles with two KS keys: flagged as known merge-tool case.

## Deviations / honesty
- Mutant red sets are labelled predictions; the seat corrects them at plan.
- A stray `cp ... /dev/null` in one of my commands was refused by the path guard (it named the C 37th HANDOVER as a destination); nothing written. No other write outside the two named files plus _work/.
- Brief was trimmed from 44.5 KB to 34.9 KB to meet the 35 KB cap; the plan-first, push and PR sections are compressed relative to the C 37th template.
- Scratch under /Volumes/DevMASTER/WEDNESDAY/0_Brain/reference/2026-11-16_drafter-seatC40-ks2189-2188/_work/ (index and sibling copies, ticket text, PR lists). No scratch clone was made (GitHub contents API only).

UNMEASURED
Every suite count (nothing run); whether existing cells assert the exact SQL text of changed lines (only ks1931 and ks2185 read); whether the fake can reach cause 3 and a non-vacuous Kelvin cell; Postgres lower() behaviour and table row counts on any box; originate's DEK destruction by canonical id; whether any caller sends an upper-case id; push queue and hook line numbers at the seat's push; the seat list at stamp time.
