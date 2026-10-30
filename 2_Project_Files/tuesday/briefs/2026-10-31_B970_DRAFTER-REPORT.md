STARTABLE
# B970 drafter report (SEAT-G235, HPSM-POC PR #261, tier 2 round 1 of 2, class "test-only spec row")

## BLUF
Kit written: 25 lines, 8 four-underscore lines (S1-S7 plus the last line), 0 non-ASCII bytes, 0 at-sign slot patterns (all by program). Startable once Tuesday fills the seven slots. Read-only: no fetch, no worktree, nothing run, nothing sent.

## Measured (Sat 31 Oct 2026 10:28-10:30 AEDT, gh -X GET under the project config dir)
- PR #261 open, not draft, mergeable true, mergeable_state blocked. Head f7597aaa3340795fec5d0cf9d15ba5faa5ca8576, 1 commit, 1 file (web/e2e/shell-sidebar.spec.ts) +3 -0, matching the builder. Two hunks: one comment line above the row, two wait lines after the heading wait.
- Main is a026cb30c3681f13feea3cfba65b72e47f4b7c34. compare 32fc1750...main = 16 files, 2 commits (297be679, a026cb30). Intersection with the spec, globals.css, axe.ts, CustomerManagement.tsx, playwright.config.ts = 0 (control: "web/" matches 16). Not a refuse today; the kit makes any later hit a REFUSE.
- compare main...branch: ahead 1, behind 2. pulls/261 base.sha reads a026cb30 (GitHub's view), the branch's own parent is 32fc1750.
- Open PRs: 260 and 261 only. #260's 8 paths do not include the spec (read from the B967 kit; not re-listed).
- Check-runs at the head: secrets (gitleaks) and dependency review completed success; the four Analyze rows, api, two api-on-SQL-Server, infra, web build, web unit tests in progress. No CodeQL umbrella row and no web e2e shard row yet. code-scanning open alerts = 0 but analyses incomplete, so not a pass (control: main analyses lists 3).
- Squash settings: COMMIT_OR_PR_TITLE / COMMIT_MESSAGES. Commit message ASCII-looking, one Co-Authored-By trailer, no B-number in the message (the gate re-checks by program).
- tmux: 5 panes, 0 named G235. lsof 9980-9989: no listener. LC_ALL=C uptime load averages 7.15 6.49 6.40 at 10:28.
- Sonnet id from models_latest.json: claude-sonnet-5-5.
- Round count: 507 STATUS files; GATE VERDICT first-line hits for this class or PR = 0 (the loose grep printed 7 lines, all other classes: B809, B901, B913, B946, B948, B960, B965). The kit says "NO GO 0 before this gate". The B805/B817 control was not run by me; the kit tells the gate to run it.

## Claims found wrong or shaded
- Builder STATUS says main "is now 297be679"; main is now a026cb30 (one more commit, HPSMPOC-378, no overlap).
- PR body says "Main has moved since (now a026cb30)" while also saying the builder's runs were on 32fc1750: consistent, but "the builder's runs" are not hosted CI. The kit lists this for the PR-body corrections.
- Builder base-sha wording: its brief said edf36342, the stamp said 32fc1750; the builder disclosed it. Note only.
- Builder disclosed an rm -rf on a nonexistent scratch path: Note against process only.
- The comment line is about 240 characters long. Note.

## Q-questions with defaults
- Q-1: judge the landing tree on the main read at Step 0, with ONE allowed re-fetch? Default YES.
- Q-2: comment claim false (edited row red under the plant) = Minor text, reported as a stronger row? Default YES.
- Q-3: a wait satisfied by a loading or empty state = Major? Default YES.
- Q-4: tier 2 stands (test-only, one spec path)? Default YES.

## Stamp values to fill
- S1: STAMPED <time> AEDT 2026-10-31 by <seat>, kit read whole.
- S2: launch_when_cool at load1 below 7 on two reads (load1 7.15 at 10:28: expect a wait); live seats beside it: read the pane list (G235 absent at 10:28).
- S3: Q-1 to Q-4 answers above.
- S4: grants as listed in the kit (in-clone fetch of two refspecs plus one optional main re-fetch, npm ci in own worktrees, scratch plant tree, commit-tree scratch commit never pushed, loopback 9980-9989, own gitleaks); no Jira in this kit.
- S5: target 75 minutes, hard stop 120 minutes after Step 0.
- S6: branch f7597aaa3340795fec5d0cf9d15ba5faa5ca8576; main a026cb30c3681f13feea3cfba65b72e47f4b7c34 or later; read refs/pull/261/merge at the stamp (I did not read it).
- S7: model: claude-sonnet-5-5 -- G2 -- gauge <n>% (from usage_tuesday.json), load1 at launch.
- Last line: READ-WHOLE-BY-TUESDAY: DONE <time>.

## Not done by the drafter
refs/pull/261/merge, rules/branches/main and the ruleset were not read (the kit sends the gate to them). The B967 template's Jira GET and K1-K8 browser/words programs were dropped as out of scope for a 3-line test-only PR.
