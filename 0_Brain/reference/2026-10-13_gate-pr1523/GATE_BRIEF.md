# Gate brief: Secuura Platform K PR #1523 (KS-1351 item 3), OPUS tier 1 (changes every seat's pre-push gate)

Commissioned 2026-10-13 ~05:4x AEDT by the Wednesday seat.

## What you are gating
- Head `ff293fa0ac7e02bf4fcfeec86b65e0b73ffb5054` (Wednesday's ls-remote). Base develop 425ad3e0; develop is now b08ee6299e86 (KS-1512, api-gateway platform.ts + tests; the author says no file overlap and merge-tree clean; NOT merged in). Author: Seat V 5th.
- Change: services/vc-issuer goes under the test-file type-check ratchet at pre-push leg 16 and in the root `check:test-types`. Six files, author's list: services/vc-issuer/tsconfig.test.json (new); scripts/typecheck-tests/baseline-vc-issuer.txt (new, EMPTY, "floor 17"); scripts/preflight/test-types-ratchet.sh (default list gains vc-issuer); package.json (check:test-types); scripts/__tests__/preflight_test_types_ratchet_leg.test.sh; CLAUDE.md. GitHub: +41/-20.
- Author's claims (NOT evidence): a planted TS2322 in a vc-issuer test file reds this PR's leg 16 (rc 1, names the file) and passes develop's (rc 0); clean tree rc 0 "3 service(s)"; dropping vc-issuer from the default list reds 8 of 38 leg-16 cells; leg-16 suite 38/38; check:test-types rc 0 (vc-issuer 30 files / 17 tests, 0 errors); vc-issuer suite 160/160.

## How to get the code (READ-ONLY on the project)
- Project checkout `/Volumes/DevMASTER/!CODING/Secuura/Blockchain/2_Project_Files` is READ-ONLY. `git clone --shared` into YOUR scratchpad; fetch `refs/pull/1523/head` and develop there with the project's `core.sshCommand`, or use `/Volumes/DevMASTER/!CODING/Secuura/Blockchain/5_Project_History/2026-10-12_seatV-5th/bundles/ks1351-ff293fa0ac7e.bundle` (sha256/16 a44a650a7d6c29d8, verified). Assert the head first. No pushes, no GitHub/Linear writes.

## What to attack (every developer's push runs this)
1. The red-proof, yourself, through the REAL leg-16 entry point the hook calls (not the script alone): plant TS2322 in a vc-issuer test file -> refuses; clean -> passes; develop -> passes the plant.
2. tsconfig.test.json scope: does it include every vc-issuer test file (enumerate them, compare), and exclude nothing that should be checked? Does an error in a vc-issuer SOURCE file reached only through a test now red too, and is that intended?
3. The EMPTY baseline with "floor 17": what does floor mean in the ratchet, can a later push add baseline entries silently, and does an empty baseline make any existing vc-issuer error a hard refusal for every seat on their next push (it should be zero errors today: measure at the head AND at develop b08ee629 after a merge-tree).
4. Failure modes that would block EVERY push wrongly: vc-issuer deps not installed in a clone (what does the leg print and return?), tsc missing, a path with spaces, running from a linked worktree. The leg must not turn "could not run" into a pass or into a false refusal without saying why.
5. The mutant: drop vc-issuer from the default list -> the suite reds; also delete the new tsconfig -> what happens.
6. The other two services' ratchets unchanged (auth 42, api-gateway 35 baselined, 0 new).
7. CLAUDE.md text matches what the code does.

## Output
- `0_Brain/reference/2026-10-13_gate-pr1523/verdict.md` (this folder only, plus your scratchpad). Head under test; every number with its instrument and a control; FOUND / TESTED / HOW; NOT tested.
- VERDICT: GO / GO WITH NOTE / NO GO; Majors and Minors with file:line and the reproducing shape.
