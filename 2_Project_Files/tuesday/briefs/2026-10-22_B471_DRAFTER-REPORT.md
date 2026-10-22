# B471 drafter report (read-only, 2026-10-22 18:2x AEDT)

Kit: `/Volumes/Laptop-DEV/TUESDAY/2_Project_Files/tuesday/briefs/2026-10-22_B471_SEAT-G40_hpsmpoc-telemetry-gate-round4-tier1.md` (43 lines, long lines). Clone of the round-3 kit B447, rewritten for round 4, LAST ROUND stated in the first lines and in the VERDICT section. Stamp has blank slots (one line, count 1 with the split-quote grep); no READ-WHOLE-BY-TUESDAY line; model line `model claude-opus-5-5 -- G1` (row G1 read at `model-routing.md:108`).

MEASURED by the drafter (git/gh read verbs only): branch `4c02e8b9…`, main `d70f9dc1…` (moved twice: #181 B459, #182 B460), 5 commits and 12 files (M 9, A 3, +943/-30) since `473bfaca`, 43 paths (A 32, M 11) vs `a93b926a`, `gh compare` diverged 29 ahead / 3 behind with merge-base `01dd9e4b`, overlap of main's five paths with the 43 = 0 (control 1), ports 8230-8239 free, `.tools/b471` absent, 0 check-runs and 0 analyses on the branch, 0 open PRs.

UNMEASURED
1. The local code repo does not hold `d70f9dc1` (cat-file fails, fetch forbidden), so the three-dot count and the merge-tree against the current main were not run by the drafter; the 43 and the zero overlap rest on `a93b926a...4c02e8b` plus the PR file lists from `gh api`.
2. Ports of B470 D27 (UAT redeploy) and the hard stop / load note are not stated anywhere I read; B466 and B467 branches are not yet on origin, so their file lists were taken from their briefs, not from a diff.
3. The head-line anchors (grep at `4c02e8b`) were read as single lines; nothing was compiled, run or mutated, and every B458 count (37 red rows, 11 of 11 mutants, 3555 of 3577, 2205 web, 49 sites) is RELAYED, not re-measured.
4. Whether the two retired API rows are the only branch-born rows asserting a verbatim category, kept `error.type`, bare event name or shape-kept span name was not checked by program; the kit hands that to check 5.
5. The new `CategoryToken` `Assembly.GetType` lookup, the dropped-span cost and the left `setup.ts:150` `routePath` charset rule were identified from B458's text and two grep lines only; the kit names them as attack points, not as findings.
