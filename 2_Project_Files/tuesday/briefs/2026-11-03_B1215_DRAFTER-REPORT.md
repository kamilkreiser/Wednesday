STARTABLE: YES (after your stamp; 9 four-underscore slots, none filled). REVISED after Tuesday's answer to Q-1: TABLE ONLY.

# B1215 drafter report - SEAT-N95, NexusAI RD-922, reset script also wipes the risk rules

Kit: `/Volumes/Laptop-DEV/TUESDAY/2_Project_Files/tuesday/briefs/2026-11-03_B1215_SEAT-N95_nexusai-rd922-reset-wipes-risk-rules.md`. Drafted by a sub-agent under row C8. Clock: `date` printed 15:14 AEDT at the first read and 15:18 AEDT at the last measurement; the kit carries no typed clock.

## BLUF (revised)
- Tuesday ruled Q-1: TABLE ONLY (the ruled option's own detail and C-234 both say "adds the sixth table"; wiping the JSON stores is wider than ruled and is not built). The kit was rewritten in place; the "build BOTH" paragraph is replaced by the ruling and its reason.
- Design: ONE step in `scripts/clear_db.js` (`DELETE FROM risk_conditions` before the `VACUUM`), bound 6 added lines, no `require`, no new string; the JSON stores, the three settings keys, the re-add route (`server.js:21099`) and the four JSON twins are recorded as measured findings in HOLD 1 and D8, not built.
- Test: ONE new file, ONE cell R1 (six-table counts 1,1,1,1,1,2 before, all 0 after; the sixth table is seeded with an active AND an inactive row), run on a temp tree with a COPY of the script and a symlinked `backend`; containment controls in the same body (child `HOME` stays empty, so the logger was not loaded; the repo `data/` listing is unchanged). Counts +1 test / +1 suite from the base the seat reads (drafted base 5299/315 -> 5300/316); the counts diff is three lines.
- Mutants: MA (remove the DELETE) and MB (`WHERE is_active = 1`, the one wrong shape a single DELETE can take, which is why R1 seeds an inactive row). No third named; the kit says so.
- Step 5 kept short: on a realistic fake tree only `printer_logs.db` changes; every JSON file and the backups are byte-equal.
- Model row re-checked: stays **C4 / Opus** (`model-routing.md:94` lists "delete" and "blank"; G1 `:108` lists "data destruction"; neither row exempts a single DELETE on a developer script's own database), `claude-opus-5-5` (`models_latest.json:17`), launch line `BRIEF_SEAT_LEVEL=opus`, gate tier 1 (G1) under G-cap (`:111`). Landing: head-pinned merge commit, never squash (C-190 `:2062`, item 2 `:2067`); the seat never deploys; Tuesday re-reads `CI_DEPLOY_ENABLED` and the environments before any merge. Target READY 90 / hard stop 150 minutes (smaller than the first draft's 150 / 210).

## Facts re-measured (instrument; control)
- Repo variables `total_count` 0 (`gh api -X GET .../actions/variables`; control `variables/zzqxnonexist` answers 404 Not Found); environments `["dev"]`; org variables UNMEASURED (not read). Open PRs length 0 (control `pulls/99999` 404). `matching-refs/heads/b1215` length 0 (control `heads/b1183` length 1).
- Deploy workflow lines at main (each `awk NR==n`): `:26 on:`, `:27 push:`, `:28 branches: [main]`, `:29 paths-ignore:` (`'**.md'`, `'docs/**'`, `'tests/**'`: `scripts/` and `__tests__/` NOT ignored, so a merge starts the workflow), `:33 workflow_dispatch:`, `:53` and `:91` the `vars.CI_DEPLOY_ENABLED == 'true'` ifs, `:95 environment: demo`. Blob `597b3487` (same as the B1195 kit).
- CI predicate: `build.yml:29` node 24, `:84` `npm run verify -- --maxWorkers=2`; `verify-suite.sh:258 :343 :354 :366` each printed by `awk NR==n`. Counts file blob `031d4b17`: `tests` 5299 (`:4`), `suites` 315 (`:5`); C-234 text agrees.
- Blobs at main (`git hash-object` of the tarball files): `scripts/clear_db.js` `fb277a16`, `backend/jsonStorage.js` `bba3742b`, `backend/simpleDb.js` `572b4e0d`, `rd904-906-...test.js` `f9f9bca0`.
- Every `file:line` in the kit was printed by `grep -n` / `awk NR==n` over a tarball of main `08352218` (fetched with `gh api -X GET .../tarball/<sha>` into my scratchpad, extracted in its own directory, read only with grep/sed). Clarification headings by `grep -n -i`: C-68 `:665`, C-190 `:2062` (item 2 `:2067`, ADDENDUM `:2076`), C-224 `:2412`, C-231 `:2467`, C-234 `:2492`.
- C-234 (read whole): RELEASED the counts file to RD-902 then RD-916, "each rebasing on the committed pair"; it "Unblocked: RD-922 ... a builder adds the sixth table to the reset with a test, through a review". RD-922 is NOT one of the two named for the counts file: the kit makes the seat read the base at Step 1 and says Tuesday orders landings (Q-6).
- RD-922 (Jira GET, in-process, no token printed): To Do / Low, labels `ai-assistant`, `b1100-finding`, `b1114-2026-11-02`; one comment id 40704 (the landing comment, "Measured at main c8f361aa ... risk_conditions occurs on no line of the file (control: printer_logs occurs on 3 lines)"). Done-when quoted in the kit.
- Card `nexusai-rd922-reset-keeps-risk-rules-1102` read via `decision_queue.sh show` (path `2_Project_Files/tools/decision_queue.sh`, the fleet/ path does not exist) into a scratch file; ruled choice `a` at 2026-11-03T06:40:40+11:00. NOTE the card's option-a detail still reads "adds the sixth table", amended premise in the BLUF only.
- Ports: `lsof -nP -iTCP:8500-8599 -sTCP:LISTEN` empty (rc 1 on its own run). Word-bounded scan of 139 non-`.pre-` SEAT kits of 2-3 Nov for `NexusAI-N95`, `N95`, `b1215`, `B1215`: 0 each; control `NexusAI-N94`: 5 files. Live panes: `tuesday`, `fleet-monitor`. `worktrees/b1215-n95`, `session-tools/b1215`, `.tools/b1215` all absent (ls rc 1 each).
- Slots: `grep -c -E '_''_''_''_'` over the kit prints 9 (control for the unstamped state); no person name (`grep -c Kam` 0), no at-capitals-at token.
- Neighbour frame: 9 test files name `low_risk_conditions|addRiskCondition|risk_conditions` at main (listed in the kit as "at least these").

## D-decisions (mine, for you to veto)
- D1. Opus / C4 kept (see BLUF).
- D2. Table only, per your answer. HOLD 1 carries the JSON-store facts (re-printed by the seat at its clone) for the product owner.
- D3. The test runs a COPY of the script in a temp tree (the script hard-codes `<its dir>/../data`), `HOME` of the child = a temp folder; an empty `ROOT/home` after the run is the proof the script still does not load the logger.
- D4. R1 seeds two `risk_conditions` rows (one inactive) so a `WHERE is_active = 1` DELETE is red (MB).
- D5. New branch off main, plain create-push; REFUSE if `refs/heads/b1215*` exists. Counts: +1 test, +1 suite (new test file), three changed lines.

## Q-questions for Tuesday (each with a default)
- Q-3. Size bound 6 added lines on `scripts/clear_db.js` (the statement plus an optional comment). Default: 6.
- Q-5. Footprint: your commission said `.tools/b1215`; every prior seat uses `session-tools/b<n>` and `.tools` does not exist in the project root. I used `session-tools/b1215` and the REFUSE check reads all three paths. Default: `session-tools/b1215`.
- Q-6. Counts-file order: C-234 queued RD-902 then RD-916 and does not name RD-922; if either lands first the seat's base moves (it reads the base at Step 1 and STOPs at Step 8 if the pair moves). Default: you order the landings.
- Q-7. Launch line is the B1195 template form (`launch_when_cool.sh ... BRIEF_SEAT_LEVEL=opus ...`), not the `cockpit.sh add` form in DRAFTER_RULES.md. Default: template form.
(Q-1, Q-2, Q-4 of the first draft are closed or void: table only means no R3 plant and no `jsonStorage` require.)

## UNMEASURED
- Nothing ran (fences). Not run: the script, the child process, jest. R1's red at main is predicted from reading the script (`risk_conditions` occurs on no line); Step 3a makes the seat measure the unchanged script first.
- Org-level Actions variables; hosted Build/CodeQL on the future head; node 24 on hosted runners; whether anyone runs the script or `fix_risk_conditions.js`; the backup-restore behaviour for the wiped stores (the kit reports the previous two backup generations keep the old rules and calls it out as HOLD 1).
- Findings carried as HOLD 1 / D8 (read from code, not run): the script clears four SQLite tables (`settings`, `cost_centers`, `user_cost_center_assignments`, `quick_questions`) whose JSON twins the product actually uses; it does not touch them, so after this change "All tables are now empty" is still not true of the product's other configuration. Read from the code, not run. You may want a card for it.

## Outside-the-fences disclosure
- Read-only, outside my two files: raw files and one tarball of main via `gh api -X GET` under the project's `GH_CONFIG_DIR` (extracted into my scratchpad, its own directory); `decision_queue.sh show` for the one named card (stdout to a scratch file, printed whole: 13 lines); Jira GET in-process through `b774lib.py` (`issue`, `comments`; a `count_line` call of mine raised a TypeError on a `search` result I misused, no write); `CLARIFICATIONS.md`; `model-routing.md`; `models_latest.json`; the B1195 kit, its report and its addendum answer; `DRAFTER_RULES.md`; `tmux list-panes`; `lsof`; `ls` of the briefs folder and the project's `worktrees/` and `session-tools/` names (names only).
- Not used: `decision_queue.sh list`, `fleet/briefs_staged/`, scoreboard, `_ledger.md`, any WEDNESDAY/FRIDAY tree, git write verbs, HTTP to a hosted host, az/ssh/docker, `cd`, Artifact/Docs/mail. One `git ls-remote` with the literal SSH URL from the wrong cwd failed with "Repository not found" (no credentials; harmless, nothing written); the correct `ls-remote origin` from the project checkout answered.
- Case-sensitive grep advisories fired on several of my greps; each count I relied on is paired with a positive control above, or came from a program that printed the line itself.
