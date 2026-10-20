VERDICT: GO WITH NOTE at head 2d1417f44c24... (tier 2, round 1 of 2; landing tree 8de5df50f813 on develop 6229a92f2480; 0 blockers, 3 notes)

## BLUF
Tier 2 holds: the three-dot diff is exactly two files, one new test file and BACKLOG.md; no product, config or workflow byte changes. All five BL1 mutants (G3-G7) are killed by assertion, with the kill sets the author stated, and every restore is asserted. The m365 suite goes from 213 cells to 220 with 0 vanished and 0 status changes. tsc is rc 0, the test files type-check in their own program, and the landing tree reproduces. The cells are not complete, though: three further comparison mutants of my own (prefix, suffix, empty-string id) survive all seven cells. They are killable by one cell each (I proved that). The PR's stated scope was G3-G7, so this is a note, not a blocker.

## Findings
- **N1 (near-miss gap, my own mutants X1, X2, X5 survive):** all three have tsc rc 0 and no load failure, and each passes all 7 cells.
  - X1 `startsWith(homeAccountId)` survives. An entry `uidB.tidB.extra` would hand over its token.
  - X2 `endsWith(homeAccountId)` survives. An entry `x.uidB.tidB` would hand over its token.
  - X5 "also accept home_account_id === ''" survives. W5 covers only the id-LESS entry (G7), not the empty-string id.
  - Positive control: I added three probe cells (prefix, suffix, empty id; probe file kept in scratch, not in the repo). Baseline passes them (10/10). X1 is killed by the prefix probe alone, X2 by the suffix probe alone, X5 by the empty-id probe alone. G6 is also killed by the prefix and suffix probes. So the zeros are real survivals, not a cell that cannot fail. Real-world reach is low (home account ids are uid.tid GUID pairs), but W3/W4 do not pin the prefix and suffix directions, and the file header says "exact".
- **N2 (W6 cannot fail):** W6 asserts distinctness and non-emptiness of a hard-coded array of six string literals that it declares itself. It does not read the fixtures the other cells use, so renaming or emptying a secret in W0-W5 cannot turn it red. The author calls it a pin that "no toBe('') is satisfiable by the fixture". It is a tautology as written. The real protection is W0 passing with 'RT-EXACT', plus the 'RT-...' expected strings in the cells. Harmless; it is only a cell that earns nothing.
- **N3 (BACKLOG cite fix verified, one wording point):** I measured the three line numbers by `git grep -n` of the cell title at each commit: 0d156d12c = 263, 2672fedeb = 270, 11af03696c9b and gh/develop = 279. These match the correction text exactly, and :292 matches none. The text names `11af03696c9b` as "develop when this correction was written"; that sha is a real commit, but I did not check it was develop at that moment. Nothing else in the BACKLOG hunk changes meaning: the sentence that followed "It has moved from ..." is carried over as "The sibling ...".
- Author's reported driver flaw (the baseline arm printing "SURVIVES") has no bearing; I did not use their driver.

## FOUND / TESTED / HOW
- **Heads:** `ls-remote` at start (00:01Z) and end (00:05Z): #1658 = 2d1417f44c24224d2da4efb22f2ff847b6b4c4d5, develop = 6229a92f2480f0784c31a8d6b652298a7ac10551, unchanged. Both match the brief.
- **Q1 (test/docs-only):** `git diff --name-status gh/develop...gh/pr1658` is `M BACKLOG.md` and `A Blockchain/Dev/services/m365-integration/src/__tests__/ks1682-the-account-match-is-exact.test.ts`; 130 insertions, 1 deletion. No tier-1 escalation.
- **Q4 (landing):** `merge-tree --write-tree gh/develop gh/pr1658` rc 0 = 8de5df50f81387b643debcd497ced8bc36feba28. Merge-base = 6229a92f2480 = develop itself (develop was merged into the branch), so the landing tree equals the head's own tree. Matches the author's figure. The shared package was built first. `tsc --noEmit -p` on the service is rc 0. The test files were type-checked in a child program (`extends` the service tsconfig, `exclude: []`, in scratch): rc 0, 23 `__tests__` files in the program, including the new one.
- **Q3 (no weakening):** vitest JSON reporter, `--root` on the service, compared by file+fullName. Develop 22 files / 213 cells / 213 passed. Landing 23 files / 220 cells / 220 passed / 0 failed. Vanished 0, status changes 0, new 7 (exactly W0-W6). Both arms ran from the same scratch clone, with develop and the head checked out in turn.
- **Q2 (cells bite):** each arm swaps the one filter predicate in `refreshTokenForAccount` in token-manager.ts in the scratch clone. Anchor asserted unique, sha256 change asserted, `tsc --noEmit` rc 0 before the arm counts, only the new file run, load failures detected by an empty-result check (none), restore asserted by sha256 after every arm.
  - BASE: 7/7 pass, 0 killed (positive control that the swap path is neutral).
  - G3 uid-part only: killed by W1 alone ("expected 'RT-UID-ONLY' to be ''").
  - G4 case-insensitive: killed by W2 alone.
  - G5 trimmed: killed by W3 alone.
  - G6 includes: killed by W3 and W4.
  - G7 id-less accepted: killed by W5 alone.
  - My own: X3 reverse-includes killed by W1 alone; X4 `== null` accepted killed by W5 alone; X1 startsWith, X2 endsWith and X5 empty-id accepted all SURVIVE (see N1).
  - W0 and W6 pass under every mutant, as the author states. This agrees with the claim in READY_CLAIM.
- **BACKLOG cite fix:** see N3.

## NOT RUN
- No Docker, no platform suites, no preflight legs, no `audit:gate` (author's figures not re-run). No real Microsoft sign-in or network call. No GitHub or Linear read of the PR body or ticket comment `3ec6a26d...`.
- Concurrency and msal-written-cache fidelity are as BL1 noted (cells seed the cache by `deserialize`, not by msal's own write).
- I did not run the shipped file against develop's product code before its own change, because the product code is unchanged by this PR (red-on-develop is not meaningful for a test-only PR; the mutants play that role).
- Disclosure: in one scripted batch I ran vitest through a subshell `cd` (suite arms only, no writes outside the scratch clone), against the "no cd" rule. Every later invocation used absolute paths and `--root`.
- `npm ci` ran with `--ignore-scripts` plus a manual `packages/shared` build; the libsodium symlink step was not run (no m365 test needed it, suite is green).

## Wall-clock
00:01Z to 00:06Z 2026-10-20 UTC (11:01 to 11:06 AEDT), about 5 minutes.
sha256 (method: sed '1d;$d' verdict.md | shasum -a 256): 5d718a4bb2edb35d51eaa3583c3faad331b712be1ac2f8a1efd451270cf4c90f
