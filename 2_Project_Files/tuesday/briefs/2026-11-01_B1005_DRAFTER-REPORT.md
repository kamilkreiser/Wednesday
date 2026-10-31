STARTABLE: YES

# B1005 drafter report (SEAT-G246, gate of branch b1002/hpsmpoc-422-423-anchor-pin-blank-evidence)

## BLUF
Kit written at `/Volumes/Laptop-DEV/TUESDAY/2_Project_Files/tuesday/briefs/2026-11-01_B1005_SEAT-G246_hpsmpoc-422-423-gate-tier2.md` (34 lines, B1003 shape). Tier 2, Sonnet (row G2 line 109, G-cap line 111, G1 line 108 for contrast), `claude-sonnet-5-5`, NO ports, round 1 of 2, no PR (so the gate writes PR and squash text as data files and a LANDING CHECKLIST). Six checks: diff by program, own Unicode sweep under Node 24 and Node 26, rows red at main plus 16 own plants, local CI predicates plus whole suite at base and head, the known consequence shown by running, messages and gitleaks. Nothing was started; Tuesday stamps.

## Facts re-measured (instrument, control)
- Branch head `0c3c42daad92f7acbb7bc5e7d6a3d9b8592a4661`, main `d0eff4ca637b8959dd205adc0b77e8111b60280a`, both by `git ls-remote origin` at 01:10:29 AEDT (control: `refs/heads/b984*` returned its line). `gh api -X GET compare` main...head: ahead 2, behind 0, total_commits 2, files remediation-store.test.ts 32/0, remediation-store.ts 2/1, AssessmentScreen.restyle.test.tsx 38/0 (control: main...main lists 0 files; `c364caf0...main` lists remediation-store.ts, count 1).
- Commit subjects 3f38b9ca and 0c3c42da read; no ticket key, no B-number, ASCII (`LC_ALL=C grep -c '[^ -~]'` over the two bodies read 0 for the first body-join check; the gate re-does it with a planted control).
- Diff read by `git diff` (read verb): remediation-store.ts hunk `@@ -19,7 +19,8 @@`: the removed line is main line 22; added are a comment line (new line 22) and the class (new line 23); the old class is a prefix of the new, tail `\u{85}\u{FFF0}-\u{FFF8}\u{1D173}-\u{1D17A}\u{E0080}-\u{E0FFF}`. The builder's phrase "line 22" is true for main only; the kit says so.
- `QuestionBlock.tsx` at the head holds `id={anchor}` at lines 45 (not-applicable return, `className="rounded-md border border-dashed`) and 53, so the anchor text for P13 is unique only with its className context.
- Node: `.tools/node24/bin/node` v24.21.0 ICU 78.3 Unicode 17.0; machine node v26.8.1 ICU 78.3 Unicode 17.0 (both `node -p`). CI pins node 24 (`ci.yml` web-build and web-unit `node-version: 24`).
- CI steps read at main `d0eff4ca` (`git show`): web-build line 371 (lint 396, typecheck 409, build 413, `--check-shards` 426), web-unit line 450 (`npm test` line 478). package.json: lint `eslint --max-warnings=0`, typecheck `next typegen && tsc --noEmit`, test `vitest run`, build `node scripts/build.mjs`.
- Round count: first lines of `Briefs/*_STATUS.md` starting `GATE VERDICT`, filter `b1002|hpsmpoc-42[23]|anchor-pin|blank-evidence`: 1 hit (B989, different PR and class, GO WITH FINDINGS); control `B981` pattern 1. NO GO 0 before on this class.
- Open PRs: #266 only (`pulls?state=open`); PRs for the branch (state all): 0. Panes (`tmux list-panes -a -F '#{@cockpit_name}'`): tuesday, Datasec/HPSM-POC-G245, Datasec/MPS-M53, Datasec/HPSM-POC-H85, fleet-monitor; no G246, no H87.
- Ports: `lsof -nP -iTCP:9470-9529 -sTCP:LISTEN | wc -l` read 0. No port assigned; the kit tells the gate to bind none (jsdom vitest, build, `--check-shards` = Playwright list). Not word-boundary-scanned (no block needed); no positive lsof control run by me.
- Tool paths present: launch_when_cool.sh, `.tools/b198/lock.sh`, `.tools/b267/waitload.sh`, `.tools/node24/bin/node`, `/opt/homebrew/bin/gitleaks`, `.tools/bicep` dir. `.tools/b1005*` and `.tools/wt-b1005*` do not exist (shell glob "no matches").
- Kit self-checks: four-underscore line count 8 (7 slots plus last line), non-ASCII 0, `@X@` 0, the word "kam" 0, launch line carries `BRIEF_SEAT_LEVEL=sonnet` inside the quotes.

## D-decisions
- D1: PARTITION: gate names B998 (H85, ports 9470-9479) and B1003 (G245, no ports) from both sides; builder B1002 trees READ-FORBIDDEN.
- D2: Plants: 16 own plants (P1-P16): every new range edge both ends, a mid-range split (proves the loop walks every code point), add U+1BCA0, add U+FFFC, blank-test-on-every-state, a `\p{Default_Ignorable_Code_Point}` shape, three QuestionBlock id plants, one equivalent (reorder). Cap 16 runs.
- D3: The sweep runs under BOTH Node 24 (the CI runner's major) and Node 26 (the builder's); the builder's own STATUS flags Node 24 as unmeasured by it, and its Corrections note a |B|/A-minus-B discrepancy against B989 (4203 vs 4199) that the gate should explain by running, not assume.
- D4: Check 5 asks the gate to SHOW the HPSMPOC-424 consequence by a throwaway scratch test at main and head, since the builder only read it; not-worse test: `saveEntry` still refuses; only an older build's stored value can hit it.
- D5: If main moves only on non-lane paths (e.g. #266 lands), the gate builds a comb tree via merge-tree in its own clone, as the B981 gate did.
- D6: The 2026-10-31 "Verified complete only" scope is described as the coordinator's stamp answer, not a ruling, per the B1002 stamp; the PR/squash text files must cite no ruling for it.
- D7: Data files: pr-title/pr-body plus squash-subject/squash-body, each checked by program with a planted `B123` control. Hosted CI, CodeQL and e2e shards are NOT TESTABLE and say so.

## Q-questions for Tuesday (default in force unless the stamp says otherwise)
- Q-1: May the PR title and squash subject carry `HPSMPOC-422` and `HPSMPOC-423`? Default YES (main d0eff4c subject reads "HPSMPOC-411 -415 -408: ..."); the commit messages and bodies carry none.
- Q-2: Tier 2 stands? Default YES (one regex line in a browser-held register, tests; escalate to tier 1 on any byte outside the class line and comment).
- Q-3: Plant cap 16? Default YES; more are NOT RUN by design.
- Q-4: Is a throwaway scratch test (never committed) allowed for check 3b and 5b? Default YES.
- Q-5: Is the double Node sweep wanted? Default YES (cheap, and CI runs Node 24).

## UNMEASURED
- Whether the head's tests pass, whether the rows are red at main, whether lint/typecheck/build pass: not run (drafter fence: no worktree, no test).
- Builder's suite counts (3649 -> 3661) are RELAYED.
- The gate's heavy-job duration (target 90 / hard stop 135 minutes is an estimate from B981 and B1003).
- Whether `launch_when_cool.sh` accepts the pane name (copied from the B1003 kit, whose stamp shows it used).
- Hosted CI, CodeQL, e2e shards, Chromium drawing of U+1BCA0.

## Outside-the-fences disclosure
- One slip: my first Bash call to read `model-routing.md` began with a `cd` and the hook refused it before it ran; no effect. Reran without it.
- Read verbs only in the project repo (`ls-remote`, `diff`, `show`); `gh api -X GET` under the project GH_CONFIG_DIR; `tmux list-panes`, `lsof`, `node -p`, `ls`, `grep`. No `decision_queue`, no Jira, no read of briefs_staged, scoreboard, `_ledger.md`, any WEDNESDAY or FRIDAY tree, HP Reporting and Docs, SOW, Source_Documents or inbound. I read the three template/builder briefs and the B1002 STATUS (a Briefs file in the project, as the task directed). One advisory hook note about case-sensitive grep appeared on two of my greps; those were count checks on my own file with a controlled expectation.
- Written: only the kit and this report.
