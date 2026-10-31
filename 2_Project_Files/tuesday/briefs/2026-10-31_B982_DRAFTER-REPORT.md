STARTABLE: yes - kit B982 (SEAT-G239, tier 2, round 1 of 2, class "infra binding rule rows") is complete and unstamped; stamp S1-S7 and launch.

# B982 drafter report (read-only; nothing run beyond reads, nothing sent)

## BLUF
Kit `/Volumes/Laptop-DEV/TUESDAY/2_Project_Files/tuesday/briefs/2026-10-31_B982_SEAT-G239_hpsmpoc-264-binding-rule-rows-gate-tier2.md`, house style of B977 (template) with the infra toolchain and mutant method of B961. Unstamped copy reads 8 lines with the four-underscore pattern (7 slots plus the bare last line `READ-WHOLE-BY-TUESDAY: ____`), 0 non-ASCII, 0 `@X@` tokens (all by program, `/usr/bin/grep -c`; control = the 8). Tier 2 stands: test-only, mechanism measured by B961.

## Measured by the drafter (13:18-13:20 AEDT, `gh api -X GET`, read-only)
- PR #264 open, not draft, mergeable true / blocked, head `8222af61...`, base `8ce48527...` (= main now, ahead 0 behind 0), 1 commit, 1 file +15 -2; created 02:17:35Z.
- Open PRs: #263 (web only, 5 files) and #264; shared paths 0 (control: #264 files vs the path reads 1).
- Checks at the head: gitleaks and dependency review success; `CodeQL` completed neutral; 4 `Analyze`, api, 2 SQL Server, infra, web build, vitest in progress.
- Panes: no `G239`; `tuesday`, `MPS-G237`, `HPSM-POC-H81`, `HPSM-POC-H80`, `MPS-M52`, `fleet-monitor`. Load `LC_ALL=C uptime` 13:18: 2.09 3.28 4.58.
- Sonnet id `claude-sonnet-5-5` (`models_latest.json` line 23). Round count for PR #264: 0 hits (loop over `Briefs/*_STATUS.md` first lines; control B961 file reads 1); neighbours B943 (NO GO r1) and B961 (GO WITH FINDINGS r2) are PR #251, a different class.
- Diff of main vs head test file (my own `diff` of both blobs, 2758 -> 2771 lines): the 2 changed lines are exactly the trailing comment (main 1240) and the whole-line comment (main 1628); everything else is the one new method; the neighbour mutant, anchor and tuples match the commission. Tuples read: `MODULE_CALL_BINDINGS` 3 (rbac, keyvault, appservice), `PREFIX_CALL_BINDINGS` 2 (monitoring, identity), `NAME_CALL_BINDINGS` 3 (storage, sql, openai); the rule loop (line 1210) iterates all three. The new comments name all 8.
- Finding for the gate to weigh: the instruction said "every call MODULE_CALL_BINDINGS holds"; that tuple holds only 3, the comments name 8. The kit grades this as correct (superset, the loop reads 8) - see Q-3.
- PR body ends with a non-ASCII generated-by line (Minor, never in the squash); its figures are the builder's local runs.

## Q-questions (defaults applied in the kit)
- Q-1: edge-case grading. Default: neighbour surviving = Major; equivalent mutant red = Major; vacuous row = Blocker (as the task stated).
- Q-2: landing tree built by `merge-tree` and `commit-tree` in the gate's clone, compared with the merge-ref tree. Default YES (if main is still `8ce48527` the tree equals the head's).
- Q-3: comments naming 8 calls vs the commission's 3-call tuple wording. Default: accepted as correct (rule reads 8); a wrong or missing call = Minor.
- Q-4: tier 2 stands. Default YES; escalate to tier 1 only on a rule/template/module byte.

## Stamp values to fill
- S1 STAMPED <time> AEDT 2026-10-31 by <seat>, brief and this report read whole, Q-1..Q-4 as above.
- S2 window until about 16:30 31 Oct, launch_when_cool at load1 below 7 (2.09 at 13:18); live beside: MPS-G237, HPSM-POC-H80, MPS-M52, H81 parked.
- S3 the reading seat, Q-1..Q-4 answers.
- S4 launch authority: the product owner's 2026-10-31 keep-going words on HPSM-POC tickets, 2026-10-16 HPSM-POC grant, 2026-09-13 as-many-agents rule, 2026-10-24 every-boot-works-tickets, Datasec CodeQL policy, 2026-10-22 Sonnet-first grant; yes to: in-clone fetch of 2 refspecs, scratch mutant tree, commit-tree scratch commit, local bicep compile, gitleaks.
- S5 target verdict 75 minutes, hard stop 120 minutes after Step-0 `date` (absolute clocks written at Step 0).
- S6 branch `8222af615a06a633fe167f706d49f5c310c69b02`, main `8ce485275455e07eaa39c46a50e62e7f7f2b3c83` (re-read at launch), merge ref and check table at launch; open PRs #263, #264.
- S7 `model: claude-sonnet-5-5 -- G2 -- gauge <n>%` from `usage_tuesday.json`, load1 at launch.
- Last line: `READ-WHOLE-BY-TUESDAY: DONE <time> (<seat>; kit and drafter report)`.

## Not done / unmeasured
No test, build, worktree or clone was run (read-only). The CI rows will move; the gate re-reads them last. `.tools/b979/` was not opened.
