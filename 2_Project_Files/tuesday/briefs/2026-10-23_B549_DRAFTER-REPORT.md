# B549 drafter report (gate kit, HPSM-POC, routing row G2 tier 2, Sonnet)

Drafted 2026-10-23 20:40-20:50 AEDT (clock from `date`). Read-only. Wrote only: the kit, its byte-identical `.pre-stamp` (made with `cp`, `cmp` rc 0) and this report.

## Files
- Kit: `/Volumes/Laptop-DEV/TUESDAY/2_Project_Files/tuesday/briefs/2026-10-23_B549_SEAT-G67_hpsmpoc-batch-gate-tier2-198-201-202.md` (about 77 KB, 107 lines)
- Copy: the same path plus `.pre-stamp`
- Launch line is in the kit (pane `Datasec/HPSM-POC-G67`, `BRIEF_SEAT_LEVEL=sonnet`, B536 shape).

## Slot count
9 lines match four underscores (eight slot lines at 53-60 and the last line 107). Control: `a____b` reads 1. The kit's sentence "The unstamped copy reads 9 lines" matches. At-sign pattern count 0; non-ASCII bytes 0 (control reads 1); no person's name.

## Measured facts (MEASURED-BY-DRAFTER, 20:40-20:48)
- `ls-remote`: main `9fc0a450eebcb41eee7628bbfcb435f2c02cf3bf`; #198 `c5b25f23a9cff0b22244e2dc69a5ad83aa48f207`; #202 `04d8dab83b9fd3861a217e5f7cd6bd937b10cdc9`; #201 `62c1526d21e54da1f62bbd301203db2b7911d3f2` (it MOVED past the round-1 head `28ba1a60` and the brief's premise: B544 pushed one commit, `ApiFactoryHostStartRetryTests.cs` +101 -0).
- B544 STATUS last line at 20:41 and 20:47 is still the placeholder `@@PROCS@@`, NOT `READY FOR QA:`; pane `%343 Datasec/HPSM-POC-H4R` alive. So #201 is CONDITIONAL in the kit.
- main moved four commits past `4db192b0` (PRs #197, #199, #196, #200); none of the nine moved paths is a path of #198 or #201 (by reading; the gate re-proves). #198 and #201 are 4 ahead 4 behind; #202 is 4 ahead 0 behind.
- `pulls`: #198 clean, #202 clean, #201 blocked. Check-runs: #198 20 of 20 success; #202 20 of 20 success; **#201 head: 18 success, `web (Next.js)` FAILURE, `web e2e (journey-and-prototype)` CANCELLED** (the fix seat relays a 20-minute job cap during `playwright install`). Open alerts 0 on all three PR refs and on main; `alerts/12` instance `fixed`; four analyses (0 results) at each head.
- Ports: 8880-8889 (and 8890-8899) have no listener (lsof rc 1) and no 2026-10-23 brief allocates them; 8870-8879 is B548's. Chosen block 8880-8889. Panes: no `G67`. `.tools/b549` absent. Load1 7.56 / 8.25 / 8.41 at 20:40, 7.76 / 8.16 / 8.32 at 20:47 (the load rule will make the gate wait).
- Sonnet model id from `models_latest.json` levels.sonnet.model_id: `claude-sonnet-5-5`.

## What the kit adds beyond the B536 shape
- Round-cap paragraph and closure table (closed / open / new) for the two round-2 PRs, from the B545 shape.
- #198: B525-1 shape table with the gate's own cells and expectations written first; the five claimed-equivalent survivors to PROVE or REFUTE. Two drafter leads, both unmeasured: S3b is equivalent only if the id is never directly followed by digits; T7 (removal order) has a counterexample the builder's argument leaves open (an id whose last 10 characters are a date, directly followed by `T..:..:...777Z`). Both are written as "equivalent over the preview's emit grammar only (Note) vs emittable (Major)". Generator-power control: the OLD regex must flag a nonzero number or the census is NOT TESTED.
- #202: every-scalar exhaustive `trimEdge` check against the API's refused set, raw-invisible-byte hygiene (trojan-source class), and the `ci.yml` step RUN under `bash -e` in four cases with the unfixed version as the failing control.
- #201 (conditional): closure of B536-3/4/5/6 including the P6 and paired-timing instruments round 1 never got; the failing CI legs named as a Major unless re-run green.

## For Tuesday at the stamp
1. #201 is IN only if B544's last line reads `READY FOR QA:` with a sha equal to the branch head at gate start; otherwise the gate covers #198 and #202 and says so. Launch after B544 wraps if you want #201 in (the gate reads the line itself at Step 1).
2. #201's head has a failing `web (Next.js)` and a cancelled e2e leg (runner time cap, relayed). Decide whether to re-run that leg before launch; the gate never re-runs CI and will rate the failure a Major if it stays.
3. The Hard stop slot suggests 3 h target and 4 h hard stop (three PRs, a possible Api leg); fill as you judge.
4. #202 round-1 scope included a `ci.yml` extension (lines 266 and 268); the kit treats exactly those two changed lines as in scope and everything else in the workflow as an Escalation.
5. B548 (the drafted 400-narrowing lane) reads the lock-row file #202 adds; the kit asks the gate to note the dependency, not to rule on it.

## Not measured
No npm, vitest, dotnet, worktree or mutant was run; B542/B526/B544 figures in the kit are RELAYED. The #198 equivalence leads (S3b, T7) are hypotheses from reading the regexes, not runs. The kit's line counts for the B526 files are from `pulls/202/files` (sum +450 -6, equal to the PR totals).
