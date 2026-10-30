STARTABLE: YES - kit B959 is unstamped (8 four-underscore lines: 7 slots + last), 0 non-ASCII, seat G226 is free (no pane, 0 listeners on 9880-9889); the only live caveats are three still-running `api` jobs and the Q-answers below.

DRAFTER REPORT B959 (gate kit, seat G226, PR #255, tier 2, round 1 of 2). 17:44-18:0x AEDT 2026-10-30.

BLUF: PR #255 head 7f70cba4 (4 commits, 5 files +413 -50) is mergeable against main 332dcc6f; hosted CI is green except 3 `api` jobs in progress; CodeQL and 4 Analyze success, 0 open alerts. The kit's risk is NOT the words but three layout/behaviour trades the builder made and the PR body omits: Devices/Sites hidden at 1280 and 1440 (2xl instead of the brief's xl), three table cells wider than main at 390/768 (HPSMPOC-401 clause), and a script-placed menu that closes on any scroll. The unlanded branch b929 changes ui/Table.tsx and customer/parts.tsx, both rendered by the lists.

KIT: /Volumes/Laptop-DEV/TUESDAY/2_Project_Files/tuesday/briefs/2026-10-30_B959_SEAT-G226_hpsmpoc-255-lists-gate-tier2.md (66 lines). Shape copied from B958 (sections, REFUSE, Stamp with underscore slot lines, final READ-WHOLE line, Launch line form); ports 9880-9883 e2e, 9884 main, 9885 comb; worktrees/tools under .tools/b959.

MEASURED (instrument; control):
- Time/load: `date` Fri 30 Oct 17:44:03 AEDT; `LC_ALL=C uptime` 10.38 10.18 10.32 (above the 7 threshold; the kit says wait for it).
- main: `gh api -X GET commits/main` = 332dcc6f3324158cc6b2d7297aa9ef47cfd33f94 (as expected, committed 06:14:30Z).
- PR 255: `pulls/255` open, draft false, head 7f70cba482b257cad51df857d2bd1c3ecce40f8c, base.sha 332dcc6f, mergeable true, mergeable_state blocked, commits 4, changed_files 5, +413 -50, created 06:31:44Z. `pulls/255/files`: A CustomerManagement.restyle.test.tsx 206/0, M CustomerManagement.test.tsx 1/1, M CustomerManagement.tsx 99/30, A EngagementsList.restyle.test.tsx 78/0, M EngagementsList.tsx 29/19.
- merge ref: `git/commits/6ab62f2d...` parents 332dcc6f + 7f70cba4, tree be9fe57e07b6f984d5fe782d010064e3fae3e79c (fresh against current main).
- compare 7365165d...7f70cba4: ahead 4, behind 0, merge base 7365165d (control: a non-existent ref in `contents?ref=000...0` errors with "No commit found").
- compare 7365165d...main: ahead 4, 36 files (wc -l of the filenames file = 36). Intersection with #255's 5 paths by `/usr/bin/grep -c -x -F -f` = 0; control (the 5 against themselves) = 5.
- Main moved files that the lists sit next to: shell/GlobalNav.tsx, shell/CustomerShell.tsx, web/e2e/playbook.ts, web/e2e/shell-sidebar.spec.ts, web/e2e/playbook-event-states.spec.ts, server/auth/returnPath.ts, plus playbook/*, readiness/*, screens/*, admin, training. NONE is imported by CustomerManagement.tsx or EngagementsList.tsx (import lists printed from the head files; 25 + 11 import lines read), none of ui/Table, ui/Progress, customer/parts. So the gate STOP list is: moved GlobalNav (sidebar around the pages) and the three e2e helpers are named, not refused.
- Other open PRs (248, 250, 251, 252, 253, 254) file lists intersected with #255's 5: 0 each (253 has 36 files, 254 has 4).
- Branches without a PR vs the 5: b928, b929, b930, b931, b934, b949 = 0 shared. By rendering: b929 (2 commits dated 29 Oct, ahead 2 behind 5) changes ui/Table.tsx (2/2), ui/Table.test.tsx, customer/parts.tsx (1/1), customer/parts.restyle.test.tsx; b928 changes shell/CustomerShell.tsx; b930 and b949 change shell-sidebar.spec.ts (b930 also playbook.ts). No b95* branch pushed (matching-refs b9 list printed).
- Checks on head (`commits/7f70cba4/check-runs --paginate`, counted): completed success 16 incl. CodeQL, Analyze x4, gitleaks, dependency review, infra, web build, web unit, web (Next.js), 5 web e2e shards; in_progress 3 (api ASP.NET Core, two api on SQL Server). Code scanning: alerts open for refs/pull/255/head = 0; analyses for the PR head = 4 rows (csharp, javascript-typescript, python, actions) at 7f70cba4, results_count 0 each; control analyses for refs/heads/main = 30 rows.
- `rules/branches/main` --jq of required contexts returned no names (empty output): the kit tells the gate to read it itself and say so.
- Repo squash settings: allow_squash_merge true, title COMMIT_OR_PR_TITLE, message COMMIT_MESSAGES.
- tmux list-panes: 14 panes, no Datasec/HPSM-POC-G226 (H74 and G224 are new vs the B958 list). `lsof -nP -iTCP:9880-9889 -sTCP:LISTEN | wc -l` = 0 (no listener lines; note this count has no positive control run).
- Routing: model-routing.md:108 G1, :109 G2 (quoted in kit), :111 G-cap; models_latest.json line 23 model_id claude-sonnet-5-5.
- Source read: head files of the 2 screens, the 2 new tests and the changed existing test fetched via `gh api contents?ref=`; base files of the 3 existing files at 7365165d; main tarball extracted under my scratchpad (not inside any project .git). Diff of the existing test = line 57 only (selectOptions on the Stage combobox -> click on "Assessment in progress"), matching numstat 1/1. Non-ASCII line counts base vs head: CustomerManagement.tsx 9/9, EngagementsList.tsx 1/1, both new tests 0 (LC_ALL=C grep -c '[^ -~]'; no planted control run for this one, so treat as unverified until the gate runs it).
- e2e census (main tarball, `/usr/bin/grep -r -l -i -E '/customers|/engagements|CustomerManagement|EngagementsList' web/e2e`): 37 files (live-API ones among them); zero control (`zzz-no-such-b959` pattern) = 0.
- Kit hygiene by program: non-ASCII lines 0; four-underscore lines 8; at-capital-at tokens 0; person-name pattern 0; "C-n" hits 9 but all are ticket keys HPSMPOC-373/-399/-401/-402 (no entry numbers, no card ids).

INPUT CLAIMS FOUND WRONG OR SHADED:
1. Your note "4 visible strings added, all existing app words": the diff shows two of them are NEW on the Customers page only: the column head "Progress" (an existing Engagements head) and the figure "N of M steps" (existing on Engagements). Also the chips reuse "Stage"/"All stages"/stage labels from the select. So "all existing app words" holds as app words, but not as Customers-page words; the kit grades these as the proved list and asks the gate to reconcile the builder's "4".
2. Builder STATUS says "0 behind" (true on 7365165d) while main is 4 commits/36 files ahead; builder corrections say the stamp's main was stale at its start. Note-level.
3. PR body says "Tests (the builder's runs on 7365165d)": honest, but it omits the 2xl breakpoint choice, the table-width cells (3 wider + 1 px), the Customers "Progress" head and the close-on-any-scroll menu. Kit puts replacement sentences in FOR TUESDAY.
4. The B944 brief's default was `xl:` for the wide columns (D-5); the builder shipped `2xl:` with measurements (table 1136 in a 962 region at 1280 under xl). That is a deliberate deviation, disclosed in STATUS but not in the PR body.
5. Builder says "removed 1 existing test line" and strings removed 0 visible; my diff of the Customers screen shows the Select (label "Stage", value, onChange, options) removed and replaced by the chip group: the kit counts this as a control-type change with the same words.

D-DECISIONS (taken in the kit; stamp accepts or strikes):
- D-1 Judge the landing tree on the Step-0 main, one allowed re-fetch (same as B958).
- D-2 The 3 disclosed wider table cells (Customers 768 689->903 in 678; Engagements 390 415->455 in 324; Engagements 768 678->707 in 678) and the 1 px Engagements overflow at 1024 are MINOR if the gate's numbers match the builder's within 2 px and the page does not scroll (the builder brief's own D-5: "a finding to state, not a failure, unless the PAGE scrolls"); any undisclosed wider cell is a Blocker; the HPSMPOC-401 clause reading goes to FOR TUESDAY for the product owner.
- D-3 Devices/Sites hidden at 1280/1440 (2xl) is a Minor layout change listed for veto, provided the table fits at 1280/1440/1536.
- D-4 The menu: a script-placed fixed menu is new behaviour; clipped/covered/off-window in any of four viewports, or lost Tab order = Blocker; closes immediately on a real click/keyboard open (>=10 opens per cell) = Major; close-on-any-scroll as briefed = Note + ticket.
- D-5 Unlanded branch b929 (Table.tsx, parts.tsx) is named, with what cannot be tested; it is not a Blocker by itself.
- D-6 Plants: re-make p1-p8, added p9 (equivalent green), p10 (2xl pin), p11 (bar value without *100), p12 (scroll-close listener), p13 (role=group), p14 (Progress th scope); p15 is a note that directory.ts (Status filter) is out of scope.
- D-7 Names program is the gate's own (the builder's AST program and scratch spec are read-forbidden); chip-vs-select row sets compared for all 6 stage states.
- D-8 Jira GET set widened to HPSMPOC-373, -399, -401, -402 (401 is the width clause).

Q-QUESTIONS FOR TUESDAY (each with default):
- Q-1 Is the landing tree judged as merge onto Step-0 main with one allowed re-fetch? Default YES.
- Q-2 How are the 3 disclosed wider cells + 1 px graded? Default Minor under the builder brief's D-5, product owner decides the HPSMPOC-401 reading; strict reading would be Major/NO GO.
- Q-3 How is Devices/Sites hidden at 1280/1440 graded? Default Minor, listed for veto.
- Q-4 Menu closing on any scroll: graded Note + ticket unless a real click/keyboard open closes it. Default as stated.
- Q-5 Does unlanded b929 change the verdict? Default: no, named and untested.
- Q-6 CodeQL neutral/queued at verdict: Condition. (At drafter read it is already success, so this is moot unless it changes.)
- Q-7 What does NO GO mean? Default: parks at round 1 of 2; Tuesday writes the round-2 fix kit.
- Q-8 Is tier 2 (G2, Sonnet) right? The G2 row's text is "tests-only, spec-only, docs, config/CI, tooling and follow-ups whose mechanism a prior gate already measured"; this PR changes product markup, a scripted menu placement and a filter control type, so a strict reader would put it nearer a product-code gate. No security/auth surface found, so G1 is not triggered. Default: keep tier 2 as you instructed, the kit escalates to G1 on any role/auth/session/storage find.

OTHER NOTES:
- Builder-preview main count: it reported 224 files / 3363 passed on main plus its files, so main alone should be 222 files / 3350; the kit marks this as a hypothesis, not measured.
- Load is 10.4 at the drafter read, so the launch should wait (launch_when_cool handles it).
- I did not open HP Reporting and Docs, any SOW, Source_Documents or inbound; nothing written outside the scratchpad except the two output files; no fetch/worktree-add inside any project .git; python only -I -B (one in-place edit of the kit).

RECOMMENDED STAMP SLOT VALUES:
- S1: STAMPED <time> AEDT 2026-10-30 by Tuesday <seat>: kit read whole (1-66) with this report; D-1 to D-8 accepted.
- S2: from the stamp until about 20:30 30 Oct (90-minute target + 150-minute hard stop, plus a CI wait), launch_when_cool at load1 below 7 on two reads (load1 10.38 at drafter read), one waiter at a time; live beside you: HPSM-POC builders and gates (pane list at Step 0).
- S3: Q-1 YES; Q-2 Minor per D-2; Q-3 Minor per D-3; Q-4 Note + ticket unless a real open closes it; Q-5 named, not a Blocker; Q-6 Condition; Q-7 NO GO parks at round 1 of 2 with a round-2 fix kit; Q-8 tier 2 stands, escalate on any auth/role/session/storage finding.
- S4: Tuesday, under the product owner's 2026-10-30 commission and his 2026-10-16 merge-once-tested grant; each YES: in-clone fetches (2 refspecs + 1 optional re-fetch of main), npm ci in own worktrees, untracked names file and scratch plant tree (never committed/pushed, restored byte-equal), commit-tree scratch combined commit (never pushed), loopback servers 9880-9889, own gitleaks run, Jira GETs of HPSMPOC-373/-399/-401/-402. Nothing else.
- S5: target verdict 90 minutes and HARD STOP 150 minutes after the Step-0 date (absolute AEDT clocks written at Step 0).
- S6: per `ls-remote` at stamp: branch 7f70cba482b257cad51df857d2bd1c3ecce40f8c; main 332dcc6f3324158cc6b2d7297aa9ef47cfd33f94 (or later, say which); refs/pull/255/merge 6ab62f2d (parents 332dcc6f, 7f70cba4); PR #255 open draft=false head 7f70cba4; check-runs on the head (success n, in_progress n; CodeQL, Analyze x4 status); open PRs 255, 254, 253, 252, 251, 250, 248; b929 and any b95* branch.
- S7: model: claude-sonnet-5-5 -- G2 -- gauge <n>% (from usage_tuesday.json) -- load1 <n> at launch.
- READ-WHOLE-BY-TUESDAY: DONE <time> (<seat>; kit 1-66 and this report).
