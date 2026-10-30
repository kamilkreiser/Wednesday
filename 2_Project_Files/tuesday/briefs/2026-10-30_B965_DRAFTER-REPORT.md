STARTABLE: YES - kit is complete and measured at 21:36-21:40 AEDT 2026-10-30; two things must be true at launch: the three `api` CI jobs finished (they were in progress) and main still `fc59b575` (else the kit's REFUSE names the moved paths).

# B965 drafter report (round 2 of 2, cap, tier 1, PR #253, seat G232)

## BLUF
- The round-2 delta is FOUR TEST FILES, one commit (`963f718d..df07688c`, +40 -3): `SecurityAssessments.test.tsx`, `Sidebar.mode.test.tsx`, `security.routes.test.ts`, `customer-nav.test.ts`. No product byte by file list. `useSecurityData.ts` (the B953-1 blocker line 97) is untouched, so B953-1 closes only if the new rows kill plant p18: the kit makes that R1.
- 0 of the 36 paths are in the 31 paths main moved since `37bc6323` (8 commits). 0 overlap with open PRs #257-#260. But main moved things #253 renders around (CustomerShell, GlobalNav, shell-sidebar.spec): judged by running on a landing tree, not by path lists.
- GitHub's merge ref is stale (`dd0e7e6b`, parents `2d0f0a17` + `df07688c`, before #251). The gate builds its own landing tree.
- Round count: one NO GO on this class (B953). A second NO GO = the cap.

## Measured (all `gh api -X GET`, project GH_CONFIG_DIR, clocks from `date`)
- main `fc59b5754bccaf8f7de943d75c2e91364661a103`, tree `74d0f955` (21:35). `compare 37bc6323...main`: ahead 8, 31 paths. Round 1 judged on `7c353747` (its STATUS first line), the builder's base is `37bc6323`.
- PR #253: open, not draft, mergeable true, state `blocked`, head `df07688c`, 6 commits, 36 files, +1519 -27 (round 1 +1479 -27).
- Delta compare: ahead 1 behind 0; files and counts as above; commit title names the held customer's reviewed count, page titles, the mode line, an encoded route id.
- Intersection of the 36 with the 31 moved: 0 (control: the 36 against themselves = 36). Open PRs #257 (9 files), #258 (8), #259 (8), #260 (8): 0 with the 36 and 0 with the moved set.
- Checks at the head: 19 check-runs, 16 completed success, 3 in progress (`api (ASP.NET Core)`, `api on SQL Server` x2). CodeQL and 4 of 4 Analyze success. Open alerts on the branch ref 0 (analyses list empty at the branch ref).
- Round count: first lines starting `GATE VERDICT` over Briefs/*_STATUS.md: B953 is the only NO GO for this class; B963 and B964 PENDING (other classes).
- Panes: no G232 (G233 G231 G230 H75-H77 H74 H68 exist). `lsof 9940-9949` empty, 9900-9999 lists 6 lines (control answers). `.tools/b965` and `wt-b965-comb` absent. Load1 8.25 at 21:35.
- Routing rows G1 (`model-routing.md:108`), G2 (`:109`), G-cap (`:111`) read. Opus id `claude-opus-5-5` (`models_latest.json` line 17).

## Input claims found wrong or needing care
- Brief said "main fc59b575 or later: read it": it is `fc59b575` now; the PR base is `37bc6323` and round 1's landing tree was `7c353747`: the kit states all three.
- Brief expected "merge ref": it is stale and not usable as the landing tree.
- Brief lists #250 as "globals.css @source not lines": confirmed (3bec6da8), and #256's two e2e one-word lines confirmed in the moved list (`shell-sidebar.spec.ts`, `playbook-partner.spec.ts`).
- The kit's C-style check labels were avoided (R1-R7) to dodge C-number tokens; round 1's STATUS uses C1-C10, so the gate must not confuse them.
- Not read whole: the middle (long lines 3-24) of the round-1 kit and the B962 body; I used structure plus the round-1 STATUS first line and FINDINGS headings. The addenda were sampled (ADDENDUM-4 whole; ADDENDUM-3 and B953 addenda not re-read: the kit cites them as data). Say if you want a re-draft with them read in full.

## D-decisions (taken in the kit; strike any at stamp)
- D1: R1 control = run the round-1 versions of the four test files on the same tree and require p18 to stay GREEN there (proves the gap and that the rows are what kills it).
- D2: STOP on any merge conflict, and on any moved path in the 36 or the shell/server/e2e set (same list as round 1, re-based on `fc59b575`).
- D3: B953-3 is graded only as "unchanged and named DEFERRED", not as a finding that counts toward NO GO.
- D4: Cut order under load keeps R1, R3, R4, R5 returnPath/auth, R6 and cuts the 132-cell width matrix to a 6-cell spot, the 22 plants to five plus a green control.
- D5: Hard stop 150 minutes (target 100), shorter than round 1 (210/150), because it is a delta gate.
- D6: Verdict line carries a `CAP:` sentence when NO GO.

## Q-questions (each with a default)
- Q1: Judge the landing tree on the main read at Step 0 (fc59b575 or later, named)? Default YES.
- Q2: If the 3 `api` jobs are still running at launch, launch anyway and read CI last? Default YES (the gate's R6 is conditional if still in progress at the verdict).
- Q3: What a NO GO at the cap means: Tuesday ships the closed instances, tickets the residue with the tester's cells attached, and a round 3 needs the product owner's word (G-cap row). For this PR that means: do not land #253 as it stands; ticket the open item(s), keep B953-3 as its own proxy ticket. Default: park the PR, no round 3 without the owner.
- Q4: Is the 8-commit-behind head squashed head-pinned at `df07688c` after a GO? Default YES (a squash onto the current main; if main moves first the pin still names the head).
- Q5: Is the stale merge ref worth a note to the builder? Default NO (the gate builds its own).

## Recommended stamp slot values
- S1: `STAMPED <clock from date> AEDT 2026-10-30 by Tuesday`, D1-D6 accepted.
- S2: launch_when_cool, load1 below 7 on two reads; load was 8.25 at the draft; live seats G233 G231 G230 beside.
- S3: Tuesday seat; Q1 YES, Q2 YES, Q3 as above, Q4 YES.
- S4: yes to in-clone fetch, npm ci in own worktrees, scratch plant tree, commit-tree (unpushed), loopback 9940-9949, gitleaks, Jira GET; no to anything else.
- S5: target 100 minutes, hard stop 150 minutes after the gate's Step-0 `date`, written as absolute clocks by the gate.
- S6: the section values in the kit (head `df07688c`, main `fc59b575`, 3 api jobs to re-read).
- S7: `model: claude-opus-5-5 -- G1 -- gauge <n>%` read from `usage_tuesday.json` at launch, and load1 at launch.

## Hygiene
Kit: 42 lines, 28.6 KB, 0 non-ASCII by program, 8 four-underscore lines (7 slots plus the last line), no placeholder clock, no person name, no decision-card id, no C-number. Nothing run in any project; no fetch, no message sent. One scratchpad dir used for gh output only.
