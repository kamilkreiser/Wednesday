From Tuesday (Datasec coordinator seat), Datasec / NexusAI. ADDENDUM-2 to your kit B1433 (SEAT-N117). Your kit, its ADDENDUM-1 and the ALL-LANES ADDENDUM-1 (non-dot verify) still bind you, except as this addendum changes them. HARD STOP 15:30 AEDT 2026-11-10.

## Why
Gate B1433 read GO WITH FINDINGS @ b7bafb8 (`tuesday/briefs/2026-11-10_B1433_verify/VERDICT.md`). Before landing, `scripts/verify-expected-counts.json` must read the branch's measured pair, 5513 tests / 327 suites, or the PR's Build check fails on stale counts. The sweep says that file is owned by no lane and is regenerated at landing, one branch at a time (`2026-11-10_nexusai_sweep/lanes.md:38`). The coordinator does not edit project files, so **for this one landing, the counts file is yours on branch `b1433/nexusai-b-csp-intake-edges-and-typed-fields` ONLY** (your kit's "you never write it on a branch" is lifted for that branch, for this one commit).

## Do (branch `b1433/nexusai-b-csp-intake-edges-and-typed-fields`, head b7bafb8d...)
1. In your clone, check out that branch at `b7bafb8d11cb8c228dc2d5384ef7eec5fe0ab6f3` (print it).
2. Regenerate the counts with the project's own tool, from a NON-DOT path as the ALL-LANES addendum requires: `verify-suite.sh --update-counts` (or the exact form your kit names). Take the jest lock through the FIFO as your kit says (one waiter; lane S holds it now; wait in the FIFO, no bypass).
3. The diff of your new commit must be EXACTLY `scripts/verify-expected-counts.json`, and it must read 5513 tests / 327 suites (print the file's two values). Any other value: STOP and say what you measured.
4. Then a PLAIN run (no `--update-counts`) from the same non-dot tree must read `VERDICT: PASS` with 5513/327.
5. ONE plain-ASCII forward commit (no amend; subject like "Expected test counts for this branch"), your attribution line; one plain push of that branch; `git ls-remote` sha after.
6. **Do not touch your other branch `b1433/nexusai-b-learning-manager-log-lines`** (725dcf0e): it lands after this one, with its own counts commit then.

## Prove it, under `## ADDENDUM-2` in STATUS
`git diff b7bafb8d HEAD --stat` = 1 file; the two count values; the update and plain VERDICT lines; the pushed sha.

**Last line:** `READY B1433-2: <head sha40 of the csp-intake branch>`, or `STOPPED: NEEDS TUESDAY <one question>`.
