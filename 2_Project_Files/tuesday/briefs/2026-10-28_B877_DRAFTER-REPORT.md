STARTABLE: YES (two paths, no open PR, no live branch on either, ports 9800-9809 free, seat name M53 unused; one REFUSE wait: main's push Build on 79addb5a read in_progress at 07:2x and must read success first)

# B877 drafter report (SEAT-M53, NexusAI, RD-897, retire the dead anomaly filter)

## BLUF
Kit written: `/Volumes/Laptop-DEV/TUESDAY/2_Project_Files/tuesday/briefs/2026-10-28_B877_SEAT-M53_nexusai-rd897-retire-dead-anomaly-filter.md` (106 lines, B862 shape). Authority re-read with `decision_queue.sh show nexusai-rd897-dead-anomaly-filter-1028`: status ruled, choice `b` "Retire the dead code in a gated PR", ruled_ts 2026-10-28T07:15:15 (the board click was 07:14). One commit, deletion only, with **TWO paths, not one**: `static/js/index.js` (82 lines removed, 0 added: base 9223-9264 and 9421-9460) AND `__tests__/fixtures/rd200-js-brand-debt.json` (two counts, `index.js #27ae60` and `#f39c12`, 6 to 5). The fixture is forced: the removed `executeAnomalyFilter` holds the only two colour literals in the ranges, and the rd200 `NO ROT` cell fails when the source count drops below the manifest. RD-733 (`ed4c1bfd`) is the project's own precedent for exactly this pairing. No test count moves (5223 / 310). Model Sonnet `claude-sonnet-5-5`, routing P4 (line 50) then C2 (line 92).

**Demo deploy:** the branch push fires nothing. **A merge to main WOULD START a `Deploy demo` run** (`paths-ignore` excludes only `**.md`, `docs/**`, `tests/**`), but both jobs skip while `CI_DEPLOY_ENABLED` is unset. `actions/variables` read `total_count 0` (HTTP 200). The last 100 of 194 runs all read skipped, including the run for #132, a `static/js` change. So it would **not deploy** today. The kit treats the switch or a `demo` environment appearing as a STOP. It also tells the coordinator to re-read both right before the merge.

## Facts re-measured (instrument, control)
- Main `79addb5a3cecca31ffe18a34fc53b5334372b7c3` (ls-remote). Open PRs 0 (control: closed lists #129-#136). All `b8*` branches and `records/b854` read `ahead_by 0`. No `b877*` and no `records/b875`. The shared checkout is stale (it holds none of the last four main shas).
- **RD-894 landed:** PR #134, merge `3a1ac7f2`, 2026-10-27T18:11:20Z, two paths (`__tests__/rd891-probe-name-race.test.js`, the counts file). DELTA 753 said "RD-897 step 2 only if a caller is found, after RD-894 lands". That wait existed for the counts file under a GUARD design. A retirement adds no cell, so the wait no longer binds anything. Since `f4ea31c9`, main has moved only by those two test files, `rd407` and the counts file (control compare listed 4 paths). No open PR and no branch touches `static/js/index.js` or the fixture. `index.js` is blob `59aca9df`, unchanged since `7d21711d`, last edited by `3047ae92` on 10-18.
- No-caller census, run over the whole tree. Frame: 960 files from ONE tarball GET at `79addb5a`, of which 876 read as text.
  - **Literal names:** `executeAnomalyFilter` appears in 2 lines (the definition at 9224 and HISTORY prose). `displayFilteredAnomalies` appears in 3 (the call at 9257 inside the filter, the definition at 9421, HISTORY).
  - **Parse tree (acorn):** both are top-level declarations, so they are reachable through `window[name]`. Neither has any reference apart from 9257. Controls fired: `displayRiskLevelResults` at 9215, `clearAnomalyTables` at 9242.
  - **Attribute dispatch:** 333 `data-csp-fn` literals (186 distinct values) and none names either function (control: `handleFilterChange` found 9 times). There are 2 `setAttribute` sites, both with literal values. `CSP.register` appears only for `saveSettings`. There are 0 templated attributes and 0 string timers. Inline `on*=` attributes appear only in docs and scripts. `eval` and `new Function` appear only in tests.
- **Correction to the 06:00 sweep:** it reported 3 lines for `executeAnomalyFilter`, counting line 9261 ("Failed to execute anomaly filter"). A literal grep -i matches only 2.
- Scratch simulation of the deletion: 9482 lines become 9400. `node --check` passes. The parse finds neither name, and `clearAnomalyTables` is left with 0 references. A diff shows 82 lines removed and 0 added.
- Test pins:
  - Nothing pins the `index.js` blob.
  - No `index.js:<line>` pin sits at line 9200 or above (control: 11 pins below that line).
  - No test names either function.
  - Open CodeQL alerts: 124 on main. Two are in `index.js` (#79 and #80, at lines 10 and 11), outside both ranges.
- Ports 9800-9809:
  - `lsof` empty (control: listeners exist on other ports).
  - Word-boundary scan of 110 kits from 27 and 28 Oct: 0 hits (control: 9840-9849 is named in 7 kits).
  - Live panes: tuesday, fleet-monitor, NexusAI-R79, HPSM-POC-D40.
  - The name `M53` appears in 0 kits (control: M52 appears in 23 files).
- Lock tool sha256 `cf01bafb...4971f`, unchanged. load1 was 6.01.

## D (decisions in the kit)
- D-1: exact ranges, each taking the one blank line that follows, so no blank lines pile up. The second range shifts to 9379-9418 after the first edit.
- D-2: the fixture is lowered, not removed (5 occurrences of each value remain). The red-proof runs the deletion alone first and must show NO ROT red naming exactly the two entries.
- D-3: absence is proven by four censuses (literal, parse tree, string dispatch, substring), each run at base and head with a planted control.
- D-4: no new cell (see Q-4).
- D-5: the deploy switch is read at REFUSE and again before the push. The coordinator re-reads it before the merge.
- D-6: model Sonnet, row C2. A launch line with `BRIEF_SEAT_LEVEL=sonnet` is in the kit.

## Q (each with its default)
- Q-1: accept the second path (the fixture), which the commission's "nothing else" did not foresee? Default: YES (without it the suite is red; RD-733 precedent).
- Q-2: `clearAnomalyTables` loses its only caller. Default: leave it and record it as newly dead. **This is the default I am least sure of.** C-18 says dead code is removed, so the coordinator may prefer to add it (7 lines, no colours) under the same ruling, and avoid a follow-up ticket for the same dead code. The ruling's words name only the filter and its display helper.
- Q-3: the stray comment `// Display filtered anomaly results` at base 9265. Default: leave.
- Q-4: add an rd733-style absence pin cell? Default: no. The ruling asks the gate to prove absence, and a cell would move the counts.
- Q-5: gate tier. Default: tier 2 (G2), round 1 of 2, following B853, which gated #132's `static/js` product byte at tier 2. Tier 1 would apply only if the coordinator counts "the merge starts Deploy demo" as "anything deploying" (G1).
- Q-6: ports 9800-9809 and pane M53. Default: taken; recheck at launch.

## UNMEASURED
Every jest run and the verify. Whether the page loads in a browser. CodeQL on the new head. A function name arriving from data at runtime. Whether `CI_DEPLOY_ENABLED` can be read at org level (only the repository level was read).

## Finding for the coordinator (not in the lane)
The `demo` environment does not exist (`environments` lists only `dev`), while `deploy-demo.yml` relies on its required reviewer as the gate. If the switch were ever set, a merge would deploy with no reviewer. C-220 already ties the switch to "a demo environment with a reviewer".

## Outside-the-fences disclosure
- I read Tuesday's `0_Brain/tasks/NEXT-PICKUP-TUESDAY.md` and `daily_tuesday/2026-10-28.md` through a grep filtered on DELTA 753, RD-897 and anomaly, to find the DELTA 753 plan. They are Tuesday files, not on the forbidden list.
- I downloaded one tarball through `gh api -X GET` into my scratchpad and extracted it there.
- I ran node with the project's own `acorn` from a scratch script. It parsed only; nothing from the tarball was executed.
- Jira: GET only (RD-897, RD-894).
- No list call on the decision queue, no writes, and no HTTP to any hosted host.
