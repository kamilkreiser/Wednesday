STARTABLE: YES

# B781 drafter report (Datasec / Security Composer, PCOMP-22 fix round, seat J24)

Kit: `/Volumes/Laptop-DEV/TUESDAY/2_Project_Files/tuesday/briefs/2026-10-27_B781_SEAT-J24_composer-pcomp22-fix-round-proven-on-scope.md` (132 lines). Drafted 2026-10-27 04:5x AEDT.

## BLUF
One new commit on `b778/composer-route-b-dump-complete`, fast-forward on `151c9a44`, two paths. Work in order: (1) B779-1, scope `DEPLOY.md:233` and `:247` so neither says the check ran on pc-b114r, with a new test row P red at the head; (2) B779-3, row E pins the second `echo $?` and its stop wording; (3) B779-4, row S pins one path across the write line, the check line and the `cat` line. B779-2 is excluded. Opus (C4), tier-1 re-gate, round 2 of 2. The Route B fenced block must stay byte-equal.

## Facts re-measured (instrument; control)
- Branch head `151c9a449dce...` and main `4a2911f1...` by `git ls-remote` at 04:51 (control: `b695*` printed its old branch). PR #96 open, not draft, head `151c9a44`, base `4a2911f1`, `mergeable_state` clean, by `gh api -X GET`. Open PR set is #96, #95, #91, #86, #85.
- Head DEPLOY.md is 616 lines and 58924 bytes. Blob `6a47cac2...` and test blob `0e7a0eaf...` by `git hash-object` on `gh api` raw copies. The DEPLOY.md blob equals the gate's figure. The test file has 318 lines, 7 `it(` lines and 0 non-ASCII lines.
- `/usr/bin/grep -c -i -F` on head DEPLOY.md: `Every command above was run` 1, `Route B as written here` 1, `Nothing else in the command is pinned` 1, `completeness check` 0, `PostgreSQL database dump` 1. Control `zzz-no-such-string-7f3a` printed 0. The six other "Nothing pins" sentences are at lines 298, 339, 385, 439, 499 and 547.
- Layout at head: block lines 197-210, check at 203, second echo at 204, `### Proven on` heading at 231, paragraph at 233, table row at 247, next `##` heading at 250. The first-run read also showed the pin paragraph at 219-229.
- Ports 9630-9639: `lsof` printed nothing, rc 1. The word-scan of the 26/27 Oct non-`.pre-` SEAT kits for `963[0-9]` hit only the B778 and B779 kits, both finished and closed. Control: the `995[0-9]` scan prints six kits.
- Panes: `tuesday`, `Datasec/NexusAI-G163`, `fleet-monitor`. No Composer pane is live. `.tools/b781` is absent (control: `.tools/b705` exists).
- Plumbing sources: b705 `common.sh`, `dbtest.sh`, `dbone.sh`, `heavy.sh`, `names.py` are 21, 74, 12, 42 and 49 lines by `wc -l`. b671 `unit.sh` is 31 lines. `dbone.sh` already runs the packages/db config and mounts only packages and apps, so the kit keeps the DEPLOY.md mount adaptation.
- Model row C4 at `model-routing.md:94` by `sed -n 94p`. `claude-opus-5-5` at `models_latest.json` lines 17 and 37. `gh auth` Datasec login count 1; deploy key in `core.sshCommand`.
- Kit self-checks: four-underscore line count 9 (the 8 slots plus the last line). Count of "kam" or "kreiser" is 0. I did not run a non-ASCII scan: the `grep -P` call failed on this BSD grep. The kit was written with ASCII text only.

## D-decisions (mine, for Tuesday to accept or strike)
- D1: I added work item 4, which the gate did not list. After rows E, S and P exist, the pin paragraph's "pins only the check ... Nothing else in the command is pinned" is false in the same way B779-1 is. The kit makes the builder rewrite that claim in this commit. This widens the removed lines to three places: the pin paragraph, the `:233` paragraph and the `:247` row.
- D2: Row P pins exact words, `except the completeness check` and `without the completeness check`, and forbids `Route B as written here` in the sub-section. The gate's fix shape is a suggestion; the property decides. Words are pinned because that is all a test can see, and the re-gate reads the sentences.
- D3: New prose must not contain `PostgreSQL database dump`. The test's extractor throws unless exactly one line names it (the gate's N4).
- D4: Three new rows make the file 10 `it`s. Only P is red at the head; E and S are green by design and are proven by the gate's M17, M18, M24 and M25 plus M29. The kit also asks that each of the gate's four mutants be shown green against the head's old test, so the new rows are what kills them.
- D5: The "that run did not include" wording is backed only by a fenced-line count at the proof commit versus the head (the gate reports 8 vs 10 at `41c9e470`). The builder re-measures it and STOPs if the count does not show the lines absent.
- D6: Fetch uses the long ref `refs/remotes/origin/b778/composer-route-b-dump-complete`, because the gate recorded the short-name clash.
- D7: The b778 and b779 trees are named as not the builder's, but the plumbing is copied from b705 and b671 as in round 1.

## Q-questions for Tuesday (each with a default)
- Q1: Is D1 accepted (rewrite the pin paragraph's pin claim in this commit)? Default: yes. Without it the commit leaves a sentence made false by its own test.
- Q2: Is the round count "round 1 of 2 on the class, counted" as ruled? Default: yes, as written in the kit.
- Q3: Hard stop and target READY slots. Default: target 2.5 hours and hard stop 4 hours after the builder's Step 0. The kit suggests this; Tuesday stamps absolute clocks.
- Q4: Should 0022's and 0024's "Nothing pins" sentences be handled now? Default: no, they stay byte-equal and the builder lists them under FOR TUESDAY.

## UNMEASURED
No vitest, container, prettier or mutant run. Not measured: whether prettier accepts the changed table row and prose (column padding), whether rows E and S are red under M17, M18, M24 and M25 as specified, the `.sql` token extraction on the continuation line, and the head's group count of 39 files / 521 tests (relayed by the gate).

## Outside the fences
None. Writes: the kit and this report only. Reads: the drafter rules, the round-1 kit, the gate file, `model-routing.md:94`, `models_latest.json`, `brief_seat.sh` lines 15-30, `.tools/b705/scripts/dbone.sh` and `wc -l` of the other plumbing files, and `ls` of `.tools/b705` and `.tools/b671`. DEPLOY.md and the test at `151c9a44` came by `gh api -X GET` into the session scratchpad. `git cat-file -t` ran once in the project repo (read verb). No `decision_queue.sh`, no Jira, no HTTP to hosted hosts, no `cd`.

READ-WHOLE-BY-TUESDAY: ____
