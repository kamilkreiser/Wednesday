GO WITH NOTES

# Gate 200 verdict - PR 2010 (KS-1504), tier 2, round 1. Subject: head e6ace3f0d06ff4e397847e60653d084c0fd0f1df on base/develop 5fc5569ed96ac61f64823cc9e1fa841899aa1f62 (ls-remote 18:2x AEDT; read twice, unmoved). A GO is about this SHA only.

BLUF: Scope is exactly 3 paths, product blob unchanged. O5 and O6 are real tests: all 6 mutants (the seat's X5, E1, Q4 plus three of mine) turn exactly the intended cell red; the old file stays green on X5/E1 and goes red only on O3 for Q4, as claimed. The count guard fails when a cell is removed. Eslint, docs-fragments and merge tree are clean. Notes: whole-suite comparison was only possible in a stale environment (not a clean pass), and the PR body text could not be read.

## Answers
1. Scope: diff stat 3 files, +76/-1 (pr.diff): ks1480 test (+47/-1), two KS-1504 html fragments (cheat, flow). rateLimitEnforce.ts blob cc5a35e681141e5620117f62b6cf9773e1723236 at base AND head (git rev-parse). PASS.
2. Mutants (ev_mut_*.log; mut script applies to the product file in my clone, restores, hash-checked "restored True"):
   - X5 (.trim() on logField): NEW file red on O5 only; OLD (base) file 14/14 green.
   - E1 (trim before JSON): NEW red on O5 only; OLD green.
   - Q4 (backslashes un-doubled): NEW red on O3 + O6; OLD red on O3 only (the indirect catch).
   - Mine OWN1 (tenant-only un-double): O6 red (proves the loneTenant leg bites). OWN2 (principal trimStart): O5 red. OWN3 (tenant trimEnd): O5 red.
   - Unmutated: new file 16/16, old base file green.
   Each cell has controls; O5 covers all four edge positions, O6 covers principal, tenant-end and the two-typed-vs-four case. PASS.
3. Count guard: planted (a) O6 it.skip -> COMPLETENESS red (14 pass/1 fail/1 skipped); (b) EXPECTED_CELLS reset to 13 -> COMPLETENESS red. 15 CELLS_RUN increments counted in source = 15. PASS (ev_PLANT1.log, ev_PLANT2.log).
4. Suites: ks1480 file passes 16/16 at head (14 at base). eslint on the changed file rc 0; planted `debugger` rc 1 no-debugger (ev_eslint_*.log). docs-fragments check OK at head (rc 0), and FAIL rc 1 on a planted unbalanced <div> (ev_docs_*.log); the two ADVISORY lines (flow l.6249, cheat l.6235) are identical at base, pre-existing.
   Whole api-gateway suite: NOT a clean pass. The shared checkout's node_modules are stale (packages/shared dist lacks zod3-compat; old zod; vitest 4.1.10 vs the seat's 4.1.12), so ~57 files fail on BOTH. Run 1: head 181 failed/1057 passed (1613), base 180 failed/1056 passed (1611); +2 tests as claimed. Failure-set diff: exactly one extra head failure, ks1215 STRUCTURAL "timed out in 5000ms" (the known load-flake class; I was running eslint/docs concurrently). Re-run alone: ks1215 fails the same 3 tests on head and base (environment), ks1480 green. Classification: same-on-base / load timeout, not caused by this PR. I could not reproduce the seat's 1625/0-failed figure (not commissioned for a rebuilt env; npm ci not attempted).
5. Merge tree (clone, merge-tree --write-tree base head): rc 0, tree fd38708c0b96a75a73d3474b3396d4df8a5e4cba, equal to head's own tree (develop = base, no drift).
6. Optional item 2: not built, and everything I could read says so (READY, the cheat and flow fragments both state "not built"/"optional"). The PR body itself was NOT read (gh unauthenticated in the Blockchain config dir: "gh auth login"), so a claim in the body is unchecked.

## Findings
- N1 (Low, info) Evidence class MEASURED AT RUNTIME for items 2-3; READ ONLY for item 6 PR body: whole-suite equivalence with the seat's 1625/0 is NOT confirmed here; environment stale (ev_fullsuite_head.log, ev_fullsuite_base.log, failset_*.txt). Same stale-node_modules candidate the seat already raised; suggest the owner confirm the suite on a fresh install.
- N2 (Low) PR body unread (ev_pr_body.json is the gh error). Owner/Wednesday should confirm the body does not claim item 2.
- N3 (Info) docs-fragments ADVISORY on the rendered page is pre-existing on base, not introduced.
- N4 (Info) O5 pins only the space character; a tab/other edge whitespace is escaped by JSON, so not at risk. Test file lines 124-166 (O5/O6), line 39 (count).

Not run: Node 24, the four platform suites, Docker push-hook legs, any box. Nothing posted to Linear/GitHub. Scratch quarantined in _quarantine_2026-11-05/ (planted copies, replaced node_modules symlinks); clone/ and base_wt/ are my own copies.
