STARTABLE: YES (after Tuesday's stamp; one timing condition, D-1)

# B1235 drafter report: SEAT-R161 (records), NexusAI, RD-922 landing of #163
Kit: `/Volumes/Laptop-DEV/TUESDAY/2_Project_Files/tuesday/briefs/2026-11-03_B1235_SEAT-R161_nexusai-records-rd922.md` (85 lines, C8 Sonnet, template B1210), `.pre-stamp` byte-equal (cmp ok), `2026-11-03_B1235_slots.json` (13 lines, valid JSON).

## BLUF
One comment (BLUF / Recommendation / Detail) on RD-922, one move to Testing (the `In Review` id 31 entry, as B1210 did for RD-917), C-235 in new section 71, a HISTORY.md entry on `records/b1235` pushed by the seat; Tuesday opens and lands the PR by merge commit (C-190). Slots: 11 four-underscore lines (grep -c prints 11; kit nonascii 0). Jira parts scanned with `scanlib1114.py` (controls true): BLUF, REC, DET 0 in every class; AUTH only the waived "Tuesday, the coordinating agent" (count 1); C parts 0 person, 0 card id, 0 at-sign, 0 banned ruling strings (planted fires).

## Facts re-measured (20:30-20:33 AEDT, from `date`)
- Main `f3ab00bd473d053a0f925616aebfe550aca3ba64`, parents `08352218...` + `5429e6dd...`; open PRs 0; control `pulls/99999` 404. `pulls/163` merged true 2026-11-03T09:28:34Z, 2 commits (98b00901, 5429e6dd), +212/-3: test +206, clear_db.js +3, counts +3/-3 (5299/315 -> 5301/316, from the patch). Merge tree = head tree `514ab3ce` (compare 5429e6dd...f3ab00bd: 0 files), unlike #160.
- Checks on the head: 8 check-runs all success, 7 DISTINCT names (audit-production-deps twice) = the relayed "7 of 7". Deploy demo 41611324246 skipped, jobs build and deploy skipped. Build 41611324299 and Push on main in_progress at 20:30 (UNMEASURED; the last Build took ~58 min).
- Raw GETs at the merge sha, `git hash-object` = contents-API sha: clear_db.js `18a96745` 55 lines (`:36` the added DELETE, `:40` VACUUM, `:43` message), rd922 test `cbfe1d0c` 206 (R1 `:146`, R2 `:183`), counts `649eb44a` 6, deploy-demo.yml `597b3487` 182, JIRA.md `e6e1be4b` 687. Wrong-line control `awk NR==99999` 0 bytes.
- Gates: B1219_STATUS.md:1 NO GO round 1 of 2, `:136` one Major (B1219-1), `:137-:144` 8 Notes; B1226_STATUS.md:1 GO WITH FINDINGS round 2 of 2, `:134` closed, `:174-:182` 9 Notes, `:186`, `:195` HOLD 1 (JSON stores), `:216` verdict; pair 5301/316.
- Jira (read helper, scratch copy of the b1210 lib with its heartbeat path in my scratchpad; controls: RD-99999999 404, nonsense text 0): RD-922 To Do, comment 40704 only, changelog 0, transitions include `In Review` (31) -> Testing; RD-917 Testing, comments 40699 + 40730, changelog 1; RD-902 To Do [40692]; RD-916 To Do [].
- CLARIFICATIONS 2496 lines, `## 70.` `:2490`, `**C-234.` `:2492`; C-235 and `## 71.` 0 (control C-234 1). HISTORY at main 9538 lines, B1210 heading `:9508`, B1235 0. Records #162 (B1210) is merged (08352218), `records/b1210` ref exists. Panes at 20:33: tuesday, Datasec/MPS-M91, Datasec/HPSM-POC-G325, fleet-monitor; NexusAI pattern 0. Ports 0; R161/B1235 kit scan 0 (control R156 1).
- Model: `model-routing.md:98` C8 (Sonnet first); `models_latest.json:23` claude-sonnet-5-5; `brief_seat.sh:24` default opus, so the level is in the launch quotes. Script hashes/lines printed by `shasum`/`wc -l` over `session-tools/b1210/`.

## Correction to the task text
C-234 is NOT an RD-922 scope entry: it is B1210's records entry for RD-917 (it mentions RD-922 as unblocked and the ruling as relayed, `:2494`). I found no C-entry that records the RD-922 ruling itself. So the next number is C-235, section 71.

## D-decisions (mine)
- D-1: Build is still running, written as UNMEASURED with a poll, widened from 45 to 75 minutes (B1210's Build ran ~58 min and its seat noted the window was too short); target 120 / hard stop 180 minutes.
- D-2: Detail lists 7 Note items (the 9 gate Notes, three grouped) as recorded not decided; "round 1 of 2" counts NO GO on the class, stated.
- D-3: The ruling is worded with the date only. B1210's kit typed 06:39 (board) while the store read 06:40:40; I typed neither.
- D-4: Wording ban strings widened to `ruled the move / chose the move / approved the move`, since here the product owner did rule on the CHANGE; only the move is the records step.
- D-5: RD-922 is not one of C-231's ten, so C-235 does not cite C-231 as authority; the move rests on `CLAUDE.md:302` and the relayed ruling.
- D-6: JSON-store question recorded as open in the comment (Recommendation), C-235 and HISTORY, with the relayed default, undecided. No card id anywhere.
- D-7: Hosted checks worded "eight runs, seven by name".

## Q-questions for Tuesday
- Q-1: Move RD-922 to Testing (default yes, per the project rule and B1210), not Done, though the relayed ruling says "RD-922 then closes"? Default: Testing; a person closes after verification.
- Q-2: Launch now with the Build running (default yes, 75 minute poll) or after it reads success?
- Q-3: The comment's AUTH says the ruling is "relayed by the coordinating agent"; confirm you may state it (default yes; no readable source file).
- Q-4: Should the open JSON-store question appear in the Jira comment at all (default yes, as one sentence in Recommendation)?

## UNMEASURED
Build 41611324299 and Push on main conclusions, CodeQL on the merge commit, the sha256 of CLARIFICATIONS, the ruling and the open question (relayed, the card store not read), whether the b1210 scripts run after renaming (nobody ran code), RD-922's comment 40704 beyond the portion printed.

## Outside the fences / disclosures
- Reads only: gh GETs, Jira GETs, tmux, lsof, raw files under `!CODING/Datasec/NexusAI/`. No `decision_queue.sh` call at all, no fenced trees. The scanlib imports `gh api user` (GET, login not printed).
- A `.pre-stamp` copy exists beside the kit (third file, as B1210 did); the first `cd` attempt of my first command was refused by the hook (no effect).
- Scratch: `/private/tmp/claude-501/-Volumes-Laptop-DEV-TUESDAY/e835675f-a717-4978-b50f-c7f6d7925838/scratchpad/` (raw reads, jl.py, j.py, scan.py).
