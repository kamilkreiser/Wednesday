STARTABLE: YES (after Tuesday stamps the 21 slot lines and the last line; unstamped copy reads 22 lines with the four-underscore pattern, MEASURED by `/usr/bin/grep -c -E '_''_''_''_'`; control: the REFUSE line in the kit splits the pattern and does not match itself)

# B756 drafter report | SEAT-R49 (records) | HPSM-POC records for #225, #221, #223, #226, #227, the B749 deploy and six rulings

Kit: `/Volumes/Laptop-DEV/TUESDAY/2_Project_Files/tuesday/briefs/2026-10-26_B756_SEAT-R49_hpsmpoc-records-221-227-and-rulings.md` (148 lines). Drafted 2026-10-26 about 20:00 to 20:30 AEDT, read-only.

## BLUF
- Records main is `7ed1398a` (B701 landed as PR #143, C-188 highest). Nothing of 26 Oct is recorded: 0 hits for #221 to #227, B729, B733, B734, B747, B749, B753, and for the ruling phrases (control `B607-1` found). Default numbering C-189 to C-200 (six ruling entries, five landings, one deploy), re-derived by the seat's scan.
- Code main is `1e3ea8a9` (#227). **The push run on #225's squash `1523cd2d` is completed failure (13 of 15 check-runs failure, 2 skipped)**; #221, #223, #226 squash runs are completed success; **#227's run was in progress at 20:18**, so any Done move that depends on it holds.
- Residue tickets: none exist for B729, B733, B734, B738, B747 (all `text ~` searches 0; controls fired). Proposed: two tickets (B733-1/-2/-3 Minors; B734-2 Minor plus the named doubts), none for Notes-only gates.
- No decision-card id and no person's name in the kit (grep over the kit: 0 hits for the name classes, after one fix, see D-6).

## Facts re-measured, with instruments
- Records main sha, open PRs 0, branches: `gh api -X GET branches/main`, `pulls?state=open` length 0, `matching-refs/heads/records/b756` 0, control `.../b701` 1.
- File sizes at records main: CLARIFICATIONS 3,468 lines, BACKLOG 1,787, history 2,455, JIRA.md 17 (`wc -l` of raw `contents`). Highest heading C-188 at `:3399` (`/usr/bin/grep -n -i '^### C-'`, last 6 lines printed).
- Records tree: 14,113 entries, `truncated` false; 0 paths match `2026-10-26_B7..._STATUS`; control: 6 of 6 `2026-10-25` STATUS files present.
- Five PRs: `pulls/<n>`, `commits/<sha>` (one parent each; #224 `merged` false, closed_at 06:51:07Z, same head `0413f25c` as #226); AEDT = UTC+11 derived by hand from the Z times (#225 14:00:10, #221 15:58:03, #223 15:58:07, #226 18:10:18, #227 20:11:09); the seat re-derives by program.
- Check-run and run counts per squash and per head (`check-runs?per_page=100`, `actions/runs?head_sha=`); branch protection `enforce_admins` true, 5 contexts.
- STATUS files: `wc -l`, `stat -f`, `shasum -a 256` (first 16 hex) for 17 files; `HP Restricted` count 0 each (control file holding the phrase = 1).
- Jira: `.tools/b701/search.py` (header read first): `created >= 2026-10-25` 8 keys, newest HPSMPOC-354; B729/B733/B734/B738/B747 text searches 0; zero control `qxv9k2zzprobe` 0; positive control `UatOpenTests` 21; `PkcsInPackageTests` 8 hits (all Done except 271; none names B733-1/-2/-3).
- Panes: `tuesday`, `Datasec/MPS-M34`, `Datasec/MPS-G153`, `fleet-monitor`; no HPSM-POC pane. `.tools/b756`, `.tools/wt-b756` absent; the kit's REFUSE check controls with `.tools/b701`.
- Register: one inclusion-filter call; HPSM-POC rows at 26, 28, 30, 31, 40, 41, 42, 49, 50, 54, 59; none dated 26 Oct; 13 `RECORDED` marks in the file (count only).
- Cards: `decision_queue.sh show <exact id>` for the three ids named, into scratch files; each read back through an inclusion filter on the id (1 hit each); all three `ruled`.

## D-decisions
- D-1 C-SCOPE slot with three values (`TWELVE`, `SIX-LANDINGS-DEPLOY`, `RULINGS-ONLY`); ruling entries first because they precede the landings in time.
- D-2 Model row C8 (Sonnet), `fleet/specs/model-routing.md:98`, id `claude-sonnet-5-5` from `models_latest.json` line 23 (read lines 20-24). Launch line carries `BRIEF_SEAT_LEVEL=sonnet` inside the quotes. Ports none.
- D-3 Records branch `records/b756`, merge-commit landing by Tuesday (PR #143 precedent, 2 parents, read); code PRs were head-pinned single-parent squashes (read); the kit tells the seat to quote the source of the squash rule from the gates' FOR TUESDAY lines and `CLARIFICATIONS.md:1545`. The project CLAUDE.md states no landing rule (grep 0): disclosed.
- D-4 Rulings entries cite board times as relayed; the 17:21:09 ruling is written with "a client stakeholder" in place of the name (the name is not in the kit).
- D-5 HP-tools standing line carried (HOLDS 9, verbatim, plus the short form).
- D-6 One correction during drafting: the kit first named the project's GitHub account login in the REFUSE line; replaced with "the project account, active; its handle is not written here". A second text fix replaced a muddled Done-rule sentence.
- D-7 Catch-up copies: STATUS files of 16 briefs (B708, B716, B718, B723, B725, B726, B729, B730, B733, B734, B735, B738, B739, B747, B749, B753), B741 only if C-191 cites it. No evidence folders, no SEAT briefs or ADDENDUM files.
- D-8 No HPSMPOC-343-style trace in this kit (not in scope); the trace helper is named only to be marked unused.

## Q-questions for Tuesday (each with a default)
- Q-1 Residue tickets: TWO (one per gate area: Pkcs assertions; shard-reader docstrings/doubts) or ONE larger ticket? The kit asks the seat to cite the product owner's "one larger ticket" rule from B653's Part 3 A, which the drafter did not re-read. Default: TWO.
- Q-2 HPSMPOC-353 to Done? B734 leaves "Done plus a new ticket, or stays open" to you; #221 is test-only, its squash run is completed success. Default: DONE on the Part 3 C checks (strike to NOT-DONE if you want the residue ticket first).
- Q-3 Your instruction said Jira writes are only the residue tickets and the status moves the template permits. The template also permits landing comments. The kit has slot `COMMENT-KEYS` (HPSMPOC-353, -343, -271). Default: LANDING-KEYS; set NONE to write only tickets and the transition.
- Q-4 The three cards' store processing stamps (09:21:02, 09:21:16, 13:32:17 +11:00) differ from the board times you gave (08:45, 08:58, 13:31). The kit cites only your board times. Default: your times; say if the store stamp is the one to quote.
- Q-5 Board verbatim text: only the 09:47:44 instruction is verbatim in the kit (from the B723 kit `:9`); the others are option labels and fragments as you gave them. Paste the rest into slot `BOARD-WORDS`, or leave `AS-GIVEN-IN-BRIEF`. Default: as given.
- Q-6 Should the record say that #225's own push run is completed failure? The kit states it as read and relays the gates' billing reading. Default: yes, facts only.
- Q-7 Fields outside the eight (action plan title/phase, evidence source) and the web sentence B747-2 are recorded as open product decisions. Default: open, nothing ruled.

## UNMEASURED
The cause of the failed push run on `1523cd2d`; the `1e3ea8a9` run's end; the 61 new rows on SQL Server; who merged each PR (`merged_by` present, login unread); whether the user guide v0.3 reached HP; the hosted state after 19:07:28; the verbatim board text of rulings 1, 2, 4, 5, 6; the trailers of the five heads (only the tail line of each squash read); the contents of builder files beyond the lines named; whether HPSMPOC-343's open comment thread holds anything after B701's comment.

## Outside-the-fences disclosure
- Wrote exactly two files: the kit and this report. Scratch files only in the session scratchpad (raw copies of the records files, card reads, the tree list).
- Ran `decision_queue.sh show` on the three ids named (no `list`); `.tools/b701/search.py` (Jira GET, after reading its header) and the register inclusion call, as the task allowed. No `git` command in the project repo at all; `gh api -X GET` only, under the project config. No HTTP to any app host, no az, ssh, docker.
- Read `B747_ADDENDUM-1`, the B718, B723, B741 kits and the B701 kit (Tuesday-owned or project files) for ruling text; read no fleet/briefs_staged, scoreboard, `_ledger.md`, WEDNESDAY/FRIDAY tree or non-Datasec project. One `ls` listing of `tuesday/briefs` file names only for B-number and live-kit census.
- `gh auth status` printed the project account handle in my tool output; it is not in either file.
