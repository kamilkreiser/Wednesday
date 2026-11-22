PR 2276: GO WITH NOTES (at head dca995028acd4dcdaee398b01d4ec6807417ad30; tier 1)

# Gate 402, tier 1 DELTA (Sonnet), PR 2276 round 2 (KS-2313), 2026-11-22 ~23:35-00:10 AEDT

The merge GO stays Wednesday's to hold until Kam rules card `secuura-dashboard-org-delete-same-rule-1122`. This covers the build of option a only. Findings-only.

## Pins (git ls-remote through the Secuura gh credential, read-only)
- develop c8fd1653a5dc9b79c41f752b29afb296910831a4 (unmoved); PR 2276 head dca995028acd4dcdaee398b01d4ec6807417ad30; PR 2159 head 7b54e7cbb6f0082a.
- gh pr view: OPEN, not draft, MERGEABLE, base develop, 7 files, +574 -16, 2 commits (13aa345653c0, dca995028acd), updatedAt 12:30:24Z. Head tree ec9b695a2c93 = `merge-tree origin/develop pr2276` (rc 0).
- My own clone `_work/g` (local clone of gate 400's, dissociated from nothing it needs; origin re-pointed to GitHub; PRs fetched). Worktrees h (head), x (mutants, red-first), d (develop). node_modules are APFS clones of gate 400's `h`. TMPDIR = `_work/tmp`. Node v26.8.1. No container, no database server started (the engine was PGlite inside the cells).

## Findings
No HIGH, no MEDIUM, no new defect in product code.

### LOW
**G402-2276-1: the PR body (and gate 400's own note) say the 9 ks1128b cells are "SKIPPED"; they are a FAILED SUITE.** Measured (`evidence/ks1128b_h.out`): the file's `beforeAll` throws `socket directory path too long for a unix socket (118 chars): set TMPDIR to a short path` (guard at line 75 of the test, threshold 88 chars on the socket directory, not the 104-byte limit the body names), so the 9 tests report as skipped and vitest exits rc 1 with `2 failed suites` in the whole-run JSON counters (the second counted suite is the same file's describe). The cause the PR body gives (long absolute TMPDIR under the gate's work path) is right; "skipped" and "104-byte" are loose. Environmental, the file is untouched by the PR, `git diff --name-only` shows it is not among the 7 paths. Not a defect of the PR.

**G402-2276-2 (carried, unchanged from gate 400): the "Test-types ratchet: OK (6 services). Ratchet leg test: 48 passed, 0 failed" and the body's auth-leg "41 errors, all in the baseline" are not reproduced here.** I did not re-run the ratchet (no auth install in any clone I may copy from). The PR body now says exactly that gate 400 could not reproduce them and why, which is honest. Unmeasured, not red.

### Info
- The commission says "the new file 26 cells". The new file holds 24 cells (all green); 26 is the two ks1868 files' remainder in the 50 of the three files. Not a PR issue.
- The PR body's "6 counted edits": the before/after diff of the seat's own record (7825 -> 9458 bytes) shows 4 diff hunks (lines 33, 38, 40-41, 44-47), some covering more than one edit. I cannot map hunks to six one-to-one; every changed sentence I read holds (see Q4). The live body is byte-equal to the seat's `pr2276_body_after_r2.md` (diff empty).

## The commission's questions

**Q1 SCOPE: holds.** `git diff --stat 13aa345653c0 dca995028acd` = exactly `services/api-gateway/src/__tests__/ks2313-gateway-organisation-delete-is-one-unit.test.ts`, 7 insertions, 4 deletions. `git diff --quiet` over admin.ts and index.ts between the two commits: rc 0 (byte-equal). The delta adds a `platformOfB` token (SYSTEM_ADMIN, organizationId = OID_B, tenantId = TENANT_B) and switches U2 and E2 (and their titles) to it; nothing else. The product files are unchanged since gate 400, so the delta is valid.

**Q2 G400-2276-1 CLOSED: yes.**
- Mutant G11, gate 400's exact spelling `String((req as any).user?.tenantId ?? (req as any).user?.organizationId ?? id)`: tsc 0, **KILLED on the round-2 cells by U2 and E2 (2 failed of 50)**; **SURVIVES on the round-1 cells (0 of 50)**, the control. For the control I wrote the round-1 test file (`git show 13aa345653c0:...`) over the head's in x, ran the same mutants, then restored it (x porcelain 0 after).
- Claim-family survivor hunt (my own variants, compiling, tsc 0 each), on the round-2 cells (U cells recording pool; E cells on PGlite as a non-owner NOBYPASSRLS role under the 027/039 policies read from the migrations):

  | mutant | round-2 cells failed | round-1 cells failed |
  |---|---|---|
  | C1 set_config from organizationId claim only | 2 (U2, E2) | 0 |
  | C2 set_config from tenantId claim only | 2 | 0 |
  | C3 organizationId then tenantId then id | 2 | 0 |
  | C4 rights_holders WHERE from the org claim | 2 | 0 |
  | C5 rights_holders WHERE tenant_id from the tenant claim | 7 | not run |
  | C6 user COUNT bound to the org claim | 1 (U2) | not run |
  | C7 FOR UPDATE lock bound to the org claim | 1 (U2) | not run |
  | C8 organisation DELETE bound to the org claim | 2 (U2, E2) | not run |
  | C9 set_config from the userId claim | 4 | not run |
  | C10 claim used only for a SYSTEM_ADMIN | 2 | 0 |
  | G11 | 2 | 0 |

  **No survivor in the claim family.** Note C6 and C7 (a bound statement taking the claim) are killed by U2 alone (the recording pool pins every statement's values); E2 does not see them (there the changed id would reach a no-op or a different row only if the claim differed in effect, and the PGlite fixture's answers do not depend on the count binding). That is a depth of one cell, not a survivor.
- I did not start the local postgres binary for this delta: the G11 real-database measurement of gate 400 (probe P2c, `secuura_app`: 200 with 2 orphaned rights holders) stands for the mutant's effect; the E2 PGlite cell now reproduces that effect by assertion and is what kills it.
- Full mutant re-run (the engine is gate 400's, re-pointed, plus C1-C10): **BASE 0 failed of 50; all 16 of the seat's compiling forms killed** (M1b 3, M2 3, M3 14, M4 6, M5 6, M6 6, M7 5, M8 6, M9b 1, M10 3, M11b 9, M12 16, M13 1, M14b 9, M15b 2, G11 2) plus gate 400's own G1b 10, G2 14, G3 6, G4a/b/c 2/2/3, G5 1, G6 6, G7 16, G8 9, G9 3, G10 6. My original M11 and G1 spellings fail tsc (2 errors each), as gate 400 recorded, and were superseded by M11b and G1b. Evidence: `evidence/mutants_run.out`, `evidence/mutants_r1cells.out`, `evidence/mut/*.json`.

**Q3 WHOLE (head dca995028acd):**
- **api-gateway vitest:** 2101 tests, 2092 passed, **0 failed assertions**, 9 skipped (the ks1128b file, G402-2276-1). 544 files, 542 passed, 1 file failed (that file, environmental). The new file: 24 of 24 green. Same arithmetic as gate 400's head (2092 + 9).
- **packages/shared vitest, develop c8fd1653a5dc and head:** 1730 tests, 1724 passed, 6 failed on BOTH arms. **The failing-name sets are IDENTICAL** (ks1536 G2; ks1725 F and J; ks727 corpus-2 x2; wallet-signature KS-278 valid-signature), 0 only on the head, 0 changed status. PR 2275 (KS-1536) is not merged: this is the six-red develop.
- **Red-first on develop's admin.ts and index.ts written over the head's** (restored, porcelain 0): 50 run, **19 failed, 31 passed, 0 suites failed to run**; the head arm 50/50. Of the new file, 17 red and 7 green (C4, C5a, C5b, C10, E0, E4, E5); every red is an assertion. **U2 red:** the statement log has 4 entries vs the expected 8 (`expected [BEGIN,…(3)] to deeply equal […(7)]`). **E2 red:** `rh: 2` left where `rh: 0` is expected after the organisation is gone. Plus the two inverted ks1868 C2 cells (`[Array(1)]` vs the five statements).
- tsc `--noEmit` (api-gateway, head): rc 0. eslint on the cell file: rc 0 (no output). Merge-tree: head vs develop rc 0; **head vs PR 2159 (7b54e7cbb6f0) rc 0, tree 030d5c1119dc**, equal to the seat's tree. (I did not re-run the planted conflict control or the census of other open PRs: the round-2 commit touches only a test file, and the waiver's two conditions were gate 400's measurement on admin.ts, which is unchanged.)

**Q4 WORDS:**
- **Facts comment 7f4a0237** (read-only through the Linear API): 3,406 B, still ONE comment on KS-2313 (In Progress, priority 2), updatedAt 12:30:26Z is after createdAt 11:39:00Z (edited, as stated). It now lists **all 5 residuals** (dashboard "Failed to delete", documents/members, concurrent insert without the FK, the rights_holders.tenant_id premise, no spec :id path), names the head and the round-2 line. Each sentence I checked holds: the U2/E2 token description (diff), G11 survived round 1 and is killed now (Q2), 24 cells (18 + 6), 17 red on develop, 16 mutants killed, same six shared reds. Two figures carry the same unreproduced items as the body: "2077/2077 on develop, 2101/2101 on branch" (in my tree 2092 passed + 9 skipped on the branch; the gap is the ks1128b environment) and "Static legs and the ratchet pair: clean" (auth leg unmeasured here).
- **PR body** (9,458 B; live equals the seat's after-file): it now says what gate 400 could not reproduce and why (ks1128b path length; auth ratchet leg), names the round-2 commit, G11 as a control and now killed, and the round-2 push. Every sentence I could check holds, with G402-2276-1 (skipped vs failed suite, 88 vs 104) and G402-2276-2 as the only looseness. "Four first forms failed the type-check (TS2367/TS6133)" is not something I can read off the PR's own state; gate 400 independently found M1, M9, M14 and M15's old forms do not compile, which fits.
- **Driver deviation** (existing-branch driver, 14 pushlock arguments, `OVL_IGNORE_PRS=[2276 2159]`): stated, and harmless on the record I read (`push/r2_real_launch.log`, `push/out_r2_real/status.txt`): precheck "ok: origin holds the branch at the gated head 13aa345653c0 (an ancestor of the tip), develop unmoved, no overlap: 20 open PRs, none touches any of 7 paths … ignored (mine, named): [2276, 2159]"; waiver condition 1 merge-tree vs 2159 rc 0 (tree 030d5c1119dc, which I reproduced), the planted control rc 1; condition 2 census reads admin.ts exactly [2159, 2276]; push 12:13:38Z-12:30:07Z rc 0; ls-remote VERIFIED at dca995028acd (my own ls-remote agrees). The ignore list names only the PR itself and the waived PR 2159, and was set by the driver only. Pre-push PREFLIGHT INCOMPLETE (13 of 16 legs, 3, 4 and 8 skipped) is stated in the body.

## Two-NO-GO cap
Not engaged (round 2, GO WITH NOTES).

## Faults, disclosed
- Two hook advisories (a case-sensitive grep with a multi-word phrase, and `$?` read after a pipeline); neither blocked, I re-read the results from the output of the commands themselves (the diff output was empty in both cases; its rc was not used).
- My first suites launch returned instantly because I had put the runner in the background inside a background call; the suites ran and finished (`evidence/suites.log: done`); I read their JSON.
- The ks1128b file was run once by itself to read the exact error (G402-2276-1).
- No mail, no `cd`, no `rm`, no write under `!CODING` (only reads: the seat's record folder, and gate 400's `_work` scripts and node_modules copied by APFS clone), no write on GitHub or Linear, no container, no deployed database.

## Not run
- The local postgres binary (gate 400's real-database probe) for G11 and the C-family; the E cells on PGlite stand in.
- The standalone ratchet (auth leg), check:openapi, fragments, the planted conflict control and the census of all open PRs: unchanged product files and a tests-only delta; gate 400's measurements stand.
- develop's api-gateway whole (gate 400: 2068 + 9 skipped, 0 failed; not re-run here).
- A booted gateway, any HTTP request, a browser, a container, Node 24.

## End state
h, x and d have 0 porcelain lines. Planted/mutated files in x were restored (the admin.ts, db.ts sha-checks inside the engine; the round-1 test file restored by `git checkout`).
