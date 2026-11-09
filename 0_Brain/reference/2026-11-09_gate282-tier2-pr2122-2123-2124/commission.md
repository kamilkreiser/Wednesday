# Gate 282, tier 2 BATCH: PR 2122 (KS-2130, E6), PR 2123 (KS-1902, E7) and PR 2124 (KS-1794 item 3, E8). All three are Seat T 21st's (held Spark READYs raised by a Claude seat). Commissioned 2026-11-09 14:4x by the 13:5x Wednesday seat.

Common rules: /Volumes/DevMASTER/WEDNESDAY/0_Brain/reference/2026-11-07_gate_tier1_common.md, read whole, applied at TIER 2 depth (through code: read the diff, check the words are true, re-run the cells with a planted defect of your own). STOP LINE per PR: a byte in a PRODUCT file (a service's src, a migration, a deployed config) means NEEDS TIER 1 for that PR. A dev/ops tooling script under Blockchain/Dev/scripts is tier 2: say which each changed file is.

Pins (Wednesday's ls-remote at 14:4x AEDT; RE-READ at start and end, and say whether each moved):
- develop 4d6b7bb17fd3be7b3fde8a3babc5d59c91c959b8 (PR 2110 squash)
- PR 2122 head f5a9a878ef4376eb2d925c663a6ca69f81c6f494 (KS-2130, bash suite only +5/-0; READY /Volumes/DevMASTER/!CODING/Secuura/Blockchain/5_Project_History/2026-11-09_seatT-21st/evidence/e6/mail/ready_ks2130_body.txt)
- PR 2123 head 3e8265bae0a1189e82b5e4826a206ace98e14727 (KS-1902, a declared +2 byte in a tooling script plus +19 suite; READY /Volumes/DevMASTER/!CODING/Secuura/Blockchain/5_Project_History/2026-11-09_seatT-21st/evidence/e7/mail/ready_ks1902_body.txt)
- PR 2124 head b2853fcf9274a6c06dc60cce330e864254bd5c36 (KS-1794 item 3 only, +2/-1 in smoke-test.sh plus +12 suite; READY /Volumes/DevMASTER/!CODING/Secuura/Blockchain/5_Project_History/2026-11-09_seatT-21st/evidence/e8/mail/ready_ks1794_body.txt)

Questions:
1. For each PR: which files, and is any byte in a product file (stop line)?
2. PR 2122: the cells pin a phrase rather than the whole abort text: re-run the suite, plant your OWN mutant of the code under test, show which cell goes red, restore by sha. Are the cell names true? The seat says 12 sibling suites (338 cells) are byte-identical: check one.
3. PR 2123: the script change and its six new flag cells: red-first claims as the READY states; plant your own mutant of the script change (revert each added byte in turn) and show which cell goes red. Is the script change exactly what KS-1902 asks for, and nothing more?
4. PR 2124: item 3 only (the 'Smoke target:' line no longer prints credentials). Re-run the suite and the seat's mutants with your own. THE KEY QUESTION: the seat measured that the two skip warnings have 15 call sites (about lines 283 to 432, after the --quick branch ends near line 176) that still print the base URL on a FULL run, and that the sed scrub misses a raw '@' inside a password and a scheme-less URL. Verify each of those three gaps by reading the code (and a fixture run if cheap; NEVER run the script against a real host). Then: does the PR body's NOT-covered statement state ALL of them, truly? A body that names fewer than exist is a finding.
5. Merge tree of each head on develop 4d6b7bb17fd3: rc and tree for each and for all three together. Shared paths with each other and with any open PR (planted control).
6. Words: PR bodies and ticket comments (9ee4e4c6, e96bc82f, 6d565175) true at the heads; NOT TESTED if you cannot read them (read the seat's saved copies in its record and say so).

Constraints: clone on the boot volume /private/tmp/g282 (no rm; state its size at the end); never cd; no git write verb in any /Volumes/DevMASTER/!CODING checkout; load1 under 8; df DevMASTER at start and end.

Output: /Volumes/DevMASTER/WEDNESDAY/0_Brain/reference/2026-11-09_gate282-tier2-pr2122-2123-2124/verdict.md (if your Write is refused, put the whole verdict in your final message). Line 1 exactly: 'PR 2122: <V>; PR 2123: <V>; PR 2124: <V>' with V one of GO | GO WITH NOTES | NO GO | NEEDS TIER 1. Then FOUND / TESTED / HOW (instrument, controls), NOT TESTED, and findings with ids G282-<PR>-<n> and a severity. Findings only; post nothing; mail nothing.
