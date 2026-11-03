STARTABLE: YES (after Tuesday's stamp; no Jira, git or file blocker found; one timing condition, D-1)

# B1210 drafter report: SEAT-R156 (records), NexusAI, RD-917 landing of #160
Kit: `/Volumes/Laptop-DEV/TUESDAY/2_Project_Files/tuesday/briefs/2026-11-03_B1210_SEAT-R156_nexusai-records-rd917.md` (83 lines, C8 Sonnet, template B1200 + its ADDENDUM-1).

## BLUF
One comment (BLUF / Recommendation / Detail) on RD-917, one move to Testing, C-234 in new section 70, a HISTORY.md entry on `records/b1210` pushed by the seat; Tuesday opens and lands the PR. All 11 slot lines are four underscores (grep -c prints 11 on the kit and on the byte-equal `.pre-stamp`; planted `x ____` counts 1). Jira text scanned with `scanlib1114.py` (its controls true): AUTH, BLUF, REC, DET all 0 in every class, ASCII; the five C-parts ASCII, 0 card ids, 0 at-signs, 0 banned ruling strings.

## Facts re-measured (command + control; clocks from `date`)
- Clocks: first read 13:26:59 AEDT, Jira/raw reads 13:27 to 13:31, kit written before 13:32:03.
- Main: `gh api -X GET repos/datasecau/Reporting_Dashboard_Au/commits/main` = `682a7b019be70f290ad25b2ff33df9aab99d8bf0`, parents `1ab39907`, `6fcab38a`. Control `pulls/99999` 404.
- `pulls/160`: merged true, merge sha as above, head `6fcab38a10bc80b49bfce3e10d5090ca24fdafc1`, merged 2026-11-03T01:54:16Z; `git/commits/<sha>` tree `c9a2da90...`, parents `1ab39907f81f48a61718e371936ccd4724e75d70` + `6fcab38a...`. `pulls/160/files`: test +490/-0, `backend/dataExport.js` +61/-9, counts +3/-3 (matches the brief). `compare 6fcab38a...682a7b01`: `HISTORY.md` +64/-0 only, so the tree is NOT the head's.
- Open PRs 0 (`pulls?state=open --jq length`). `matching-refs/heads/records/b1210` 0; control `records/b1200` 1 (merged as #161, commit `1ab39907`).
- Runs `actions/runs?head_sha=682a7b01`: total 5: Deploy demo push completed skipped 41562736152; Build 41562736062 **in_progress** (re-read 13:28:34 still in_progress); Gitleaks success; npm-audit success; Push on main success. Control all-zero sha total_count 0. `workflows/deploy-demo.yml/runs` top 3: 41562736152, 41505248380, 41447110873 all skipped.
- Raw GETs at the merge sha with `git hash-object`: `dataExport.js` 456 lines blob `0c9b960b` (equals the contents API sha); rd917 test 490 lines `283c5fd4` (equals); counts file 6 lines `031d4b17` ("tests": 5299, "suites": 315); `deploy-demo.yml` 182 lines `597b3487`; `JIRA.md` blob `e6e1be4b`, heading at `:620`. `awk NR==99999` on the file prints 0 bytes (wrong-line control). Pointers printed by `grep -n`/`awk NR==n`: `:212`, `:233-:238`, `:420-:423`, `:447-:452` (`:451` the reject line), test cells D 137, V 241, W 281, X 341, Y 430.
- Gate files: B1191 `:1` NO GO round 1 of 2 at 559e426, `:129` Blocker, `:130` Major, `:131` B1191-3, `:137` B1191-9; B1201 `:1` GO WITH FINDINGS round 2 of 2, `:93` C5, `:137-:145` findings (8 Notes), `:144` "this lane lands first on the counts file", `:157` plain verdict, `:21` census (class NO GO count 1). G315 kit `:70` PARTITION says RD-902 then RD-916 queue behind the counts file.
- Jira (GET through a scratch copy of `b1200lib.py` whose heartbeat path I pointed at my scratchpad): RD-917 To Do, 1 comment 40699 (text read, Authority paragraph names the 2 November delegation and the veto), one `In Review` -> `Testing` transition; RD-922 To Do 1 comment 40704; RD-902 To Do 1 comment 40692; RD-916 To Do 0. Searches (list lengths): `( key = RD-917 )` 1; `( text ~ "zzqxnonexist" )` 0; `( text ~ "B1210" )` 0; `( text ~ "B1200" )` 0. I did not read RD-917's changelog (my call failed on a tuple return); the kit has the seat read it at Job A.
- CLARIFICATIONS (`1_Project_Definition/CLARIFICATIONS.md`): 2488 lines, `## 69.` `:2482`, `**C-233.` `:2484`, C-231 `:2467` (quote re-read); `C-234` 0, `## 70.` 0, `C-233` 1 line-hit (control `C-231` 6). So C-234 in section 70, not the C-233/section 69 of the template. Sha256 of the file not asserted in the kit (seat records it).
- HISTORY.md at main: 9506 lines, B1200 heading `:9476`, `B1210` 0, `B1200` 1 (so Job F's tail check works).
- Panes: `tmux list-panes -a -F '#{@cockpit_name}'` = tuesday, Datasec/MPS-G316, Datasec/HPSM-POC-G313, fleet-monitor. `^Datasec/NexusAI-[A-Z][0-9]+$` 0 (planted R999 -> 1); `^Datasec/NexusAI-G[0-9]+$` 0. Job F gate check: no NexusAI-G pane live now.
- Ports: `lsof -nP -iTCP:9800-9999 -sTCP:LISTEN | wc -l` 0; SEAT kits (non-`.pre-`) of 11-02/11-03 matching `R156|B1210` 0 (control `R153` 1).
- Model: `model-routing.md:98` is the C8 row (Sonnet 1st); `models_latest.json:23` `claude-sonnet-5-5`; `brief_seat.sh:24` default opus, so the level is inside the launch quotes.
- Decision store: `decision_queue.sh show nexusai-rd922-reset-keeps-risk-rules-1102` read to a scratch file: status ruled, choice `a` ("Wipe the risk rules too"), `ruled_ts=2026-11-03T06:40:40+11:00`; planted nonexistent id rc 2, 0 hits. The kit carries no card id.

## D-decisions (mine)
- D-1: The Build for the merge was still running at drafting; I wrote it as UNMEASURED with a Job A poll (every 3 min, up to 45 min) and made `Build success` a Job E predicate clause, and a STOP on failure/cancel. The Jira Detail states "Build ... concluded success", which the seat may only post after reading it. Launch after the Build ends removes the wait.
- D-2: Test pointer table uses 5 cells (D, V, W, X, Y); the comment names them one clause each; Notes go in Detail as "recorded from the review, not decided" (non-ENOENT warning shape, finalize catch without a cell, x and x-backslash key, directory at by-name sites, manifest.json last); hosted node 24, CodeQL and a hand-closed download are "Not measured".
- D-3: No RD-922 / RD-902 / RD-916 text in the Jira comment (the Jira text rules ban lane/seat words, and those keys are read-only). They appear in the C-entry only, as words, and in the HISTORY closed list as "not touched" rows (each GET-asserted unchanged at Job E).
- D-4: The RD-922 ruling is recorded in C-234 as "the product owner's ruling of 2026-11-03 06:39 AEDT, option a" without the card id and without the word "ruled" (the wording rule's banned strings). I used 06:39 as you gave it; the store timestamp is 06:40:40 (board time vs store time, the C-231 pattern).
- D-5: Detail says the tree differs from the head's only by HISTORY.md (measured +64/-0); I did not claim equality.
- D-6: Quoted CLAUDE.md:302 with "[name omitted]" for the person, as C-233 did.
- D-7: Tooling: copies from `session-tools/b1200/` (it exists, hashes printed in the kit with 16-hex prefixes and line counts, measured with `shasum -a 256`/`wc -l`). Note `figures1200.py` and `append-c1200.py` have 143 and 181 lines (the B1200 kit cited the B1187 line counts). The seat must rework `figures` for one comment.

## Q-questions for Tuesday
- Q-1: Should C-234 carry the RD-922 ruling as relayed (default, one sentence, no card id) or should a separate seat record it as its own entry? Default: as written in `<C234-SETS>`.
- Q-2: Launch now with the Build running (default: yes; the seat polls up to 45 min) or after the Build reads success?
- Q-3: Is "released to RD-902 then RD-916 in that order" from B1201's PARTITION still the order you want (default: yes)?

## UNMEASURED
Hosted Build conclusion (running at drafting), CodeQL on #160, the sha256 of the CLARIFICATIONS file, RD-917's changelog, the contents of the B1201 evidence folder, whether the seat's scripts from `b1200` run unchanged after renaming (nobody ran code).

## Outside the fences / disclosures
- Reads only: gh GETs, Jira GETs (scratch library copy, no write), tmux, lsof, raw files under `!CODING/Datasec/NexusAI/` (read-only), one `decision_queue.sh show <exact id>` (no `list`). I did not read the fenced trees.
- A `.pre-stamp` copy of the kit exists beside it (byte-equal, `cmp` clean) because the kit's REFUSE refers to it; this is a third file against "exactly two". I could not remove it (the no-delete hook refused, correctly); you may stamp or quarantine it.
- One failed attempt: `sed -i` on the kit failed on macOS (no change made); I used the Edit tool instead. One zsh glob error on a `gh api` URL with `?` (no effect).
- Scratch files in `/private/tmp/claude-501/-Volumes-Laptop-DEV-TUESDAY/8ade374d-0a0f-45f0-bf14-6cca67fc2a0e/scratchpad/` (raw reads, `jl.py`, scans, `card.out`).
