STARTABLE: YES (after the stamp; Q1 to Q6 have defaults)

# B818 drafter report (Sonnet 5.5 drafter, 2026-10-27 about 12:45 to 13:10 AEDT)

Kit: `/Volumes/Laptop-DEV/TUESDAY/2_Project_Files/tuesday/briefs/2026-10-27_B818_SEAT-R62_composer-records-97-landing-b815-ticket.md` (185 lines). Seat `Datasec/Security-Composer-R62`, Sonnet (row C8, `model-routing.md:98`), `BRIEF_SEAT_LEVEL=sonnet` inside the launch line's quotes. No ports. Unstamped copy: 16 lines hold the four-underscore pattern (15 slot lines + the last line; control: a planted line counts 1).

## BLUF
- SEVEN Jira writes in a fixed order, PCOMP only: one create (Task, label `plan-comp-391`), then for PCOMP-99, -100, -101 each one facts-only comment followed by one transition `{"transition": {"id": "41"}}` (Done). Each key's comment and move are conditional on the seat's own Done-when check (Step 4a); a key whose Done-when the gate's text does not back is HELD with no comment and no move.
- My pre-read says all three Done-when texts are MET by what B815 measured (cites in Input 3 of the kit). PCOMP-99's "no row is loosened" rests on the gate's "test has 0 removed lines" (STATUS line 66), the 10 titles unchanged (179) and 29 of 29 regression (154-158); PCOMP-101's "nothing else on the row changes" rests on the gate (line 69) and my own raw cell compare (old row 250 vs new row 258: only the first cell differs).
- Records on `records/b818`: landing row #390 (PR #97), ticket row #391, OPEN-items row #392 (the gate's Decisions list, recorded NOT RULED, plus B815-5), State appends on #381 to #383, history, `JIRA.md`. `CLARIFICATIONS.md` untouched by default. One `merge --no-ff` into root main.
- Main has moved since the brief was commissioned: root `main` is `2474140f` (B812's fold, which created PCOMP-103 for row #389). Highest BACKLOG id is 389, so this kit uses #390 to #392 and the label `plan-comp-391`; Jira total is 103 (the kit expects 104 after).
- No Composer pane is live. B806's builder pane is gone, so there is nothing beside the seat in this project.

## Facts re-measured (instrument; control)
| Fact | Instrument | Control |
|---|---|---|
| PR #97: merged true; merged_at 2026-10-27T01:16:52Z = 12:16:52 AEDT; merge_commit_sha `8df52332e52bf520633317120c563a16387d1a13`; one parent `422ecf37`; tree `49e93d1a` = head `6f75c2d1`'s tree; 2 files +138 -6 (DEPLOY.md +14 -6, test +124 -0); 1 commit | `gh api -X GET pulls/97`, `commits/<squash>`, `commits/<head>` under the Composer `GH_CONFIG_DIR` | `pulls/9999` answered 404; `date -r` conversion offset +11 h |
| Check-runs on squash: Analyze (csharp) and (javascript-typescript) completed success 01:19:02Z / 01:19:51Z; open alerts on main 0 | `check-runs`, `code-scanning/alerts?state=open&ref=refs/heads/main` | `state=fixed` returned 20 rows |
| code repo main = `8df52332` at 12:5x | `git/ref/heads/main` | -- |
| Squash subject = "Deploy guide: name every pin of the 0021 Route B test; pin the stop line and the scoping words; fix a table cell (#97)" (the commit title), NOT the PR title the gate predicted | `commits/<squash>` `.commit.message` first line | PR title read from `pulls/97` differs |
| B815-4 resolved: PR body now says rows E and P are "strengthened" and the old-test sentence names the builder's shortened comment; closing line "Corrected 2026-10-27 ..." | `pulls/97` `.body` | the two old phrases were taken from the gate's quote at lines 303-306 |
| B815 STATUS: 436 lines; line 1 GATE VERDICT, GO WITH FOLLOW-UPS round 1 of 2; `^VERDICT:` count 1 (line 436); Findings 284-310; FOR TUESDAY 331-364 (checklist 336-342, Decisions 343-352, ticket text 353-363); Done-when claims at lines 65-66, 69, 137, 153-158, 179, 187, 245 | `/usr/bin/grep -n`, `sed -n` | `^VERDICT-ZZ:` pattern not run; count of real pattern = 1 |
| Evidence files `var-adv-report.txt`, `psql-probe.txt` exist (38 entries in the folder) | `ls` + grep | a made-up name matched nothing |
| DEPLOY.md at the squash: 628 lines; pin paragraph lines 222-233 hold the three pinned texts at 229 and 231; Proven-on row 258 reads "Route B with the one-step command of 0019 (...)", old row 250 "the command above it (...)"; second cell identical; a `diff` of the 12 table lines shows one differing line | `contents/DEPLOY.md?ref=<sha>` raw, `sed -n`, `diff` | `one-step command of 0019` count 1 new, 0 old |
| Test at the squash: 542 lines; `WRITES`, `DROPS`, `APPLIES` at 17-19; `findIndex` uses at 64, 84-90; 10 `it(` lines | `contents/...?ref=<sha>` raw, `sed -n`, `/usr/bin/grep -c` | -- |
| PCOMP-99/-100/-101: Task, Backlog, 0 comments by field and by endpoint; transitions 11/21/31/41 (41 = Done); labels `plan-comp-381/-382/-383` | `jira808.get`, `/transitions`, `/comment` | endpoint total vs field total both read |
| Jira: total 103, held 19, seed 94, owner-wait 2, `plan-comp-391` 0 (`-390`, `-392` 0), `plan-comp-389` 1 (PCOMP-103), `status = Done` 1 (PCOMP-30), composer 26, zzqxvbw 0, stemmer 42; PCOMP-95 1 comment, PCOMP-103 0 | `jira808.jql` (`project = PCOMP AND (...)`) | zero and positive controls both fired |
| Board search for the Route B substring pins: 16 terms; `b778-route-b-script-complete` -> PCOMP-100, -99, -22; `line.includes`, `substring`, `duplicate`, `|| true`, `A6a`, `A7c` -> 0; `first match` -> PCOMP-66 (unrelated). No ticket carries B815-1 to -3 | `jira808.jql` text/summary | `composer` 26 |
| Root main `2474140f532674832abf26b7a39eda8db72cd5ab`; no remote; status lines 1198; HEAD on main; no MERGE_HEAD/index.lock; BACKLOG highest id 389 (rows 390-393 absent on main); `records/b818`, `.tools/b818` absent | `git --no-optional-locks rev-parse/symbolic-ref/remote/status/grep/for-each-ref`, `ls` | `389` found, `.tools` b808 listing found |
| Panes: `%0 tuesday`, `%63 Datasec/HPSM-POC-D38`, `%62 Datasec/NexusAI-M21`, `%1 fleet-monitor`; no Composer pane or process; R62 unused in non-`.pre-` SEAT kits; ports 9750-9759 free | `tmux list-panes -a`, `ps`, `/usr/bin/grep -l -w`, `lsof` | `R60` finds the B812 kit |
| Model: C8 line 98; sonnet id `claude-sonnet-5-5`; `brief_seat.sh:24` `LEVEL="${BRIEF_SEAT_LEVEL:-opus}"` | `grep -n`, `python3 -I`, `sed -n` | -- |
| Kit hygiene: `B[0-9]{3}` in the 11 quoted ticket/comment lines (`^> `) and the LAND paragraph: 0 (control: planted `B815` = 1); name/client/card-slug terms in them: 0 | `grep -c`, `grep -o` | planted-line control fired |

## D-decisions
- D1: Done moves are CONDITIONAL on the seat's own check per ticket (Step 4a), not blanket. Reason: the project records no rule for when a merged ticket moves (JIRA.md, B808 text); the move rests on Tuesday's instruction on the gate's verdict, so the seat must prove each Done-when from the gate's lines. A ticket not proved is HELD with no comment.
- D2: Jira order is create, then per key comment, read back, transition, read back. Reason: a Done move without its evidence comment is the worst partial state; a create failing first stops before any move. The comments do not carry the new key (frozen before the create); they point at "BACKLOG row #391".
- D3: The gate's STATUS path holds a work number (`B815`), which the Jira text rule forbids. The comments say "the gate's STATUS file is named in BACKLOG row #390" and name no path; the records carry the path. (Q1.)
- D4: B815-5 (heavy.sh TZ quirk) goes in the OPEN-items row #392 as Note N-TZ, not in the ticket. Reason: it is seat tooling under `.tools`, not the guide or its test; the ticket's Done-when (A1 to A9 red or the paragraph says so) cannot cover it.
- D5: B815-4 resolved: recorded in landing row #390 only, after the seat re-reads the PR body at source. Nothing in Jira text.
- D6: Row #392 records the gate's Decisions list as OPEN, NOT RULED (precedent #385, #388). It decides nothing; stamp slot `DECISIONS-ROW` can drop it.
- D7: The follow-up ticket stays Backlog with the single label `plan-comp-391`; "Deferred" (the gate's word) is carried in text and State, not as a status or the `held` label (Q3).
- D8: Squash subject measured as the commit title, not the PR title the gate named. Recorded in row #390; no effect on any Jira text.
- D9: Ticket block 3 (the gate's ticket text) is copied BY PROGRAM from STATUS lines 353-363 with an equality assert; block 4 (the three findings with their fix shapes) is written in the kit from lines 284-302, with the `B815-n` ids turned into "the gate's finding n", and every token asserted by the seat.

## Q-questions for Tuesday (each with a default)
- Q1: You asked for the gate's STATUS path in the comments. The file name holds `B815`, and the Jira text rule bans `B<digits>`. Default: comments say "named in BACKLOG row #390" and carry no path (the B812 treatment of the evidence folder). Alternative: stamp that this one path may appear, and the seat adds it and exempts it from the `B[0-9]{3}` scan.
- Q2: A C-entry for the landing (C-104 was filed for PR #94's landing after a GO WITH FOLLOW-UPS gate)? Default: NONE; row #390 is the record, as row #380 was for PR #96. Stamp `FILE` for a C-107 in C-104's format.
- Q3: Should the follow-up carry the `held` label or a "Deferred" marker beyond text? Default: no; Backlog plus `plan-comp-391` only, like PCOMP-95 to -103 (the fence allows one label).
- Q4: Row #392 (the open decisions, NOT RULED)? Default: FILE. NONE keeps them in the STATUS only; the rows stay #390 and #391.
- Q5: Is "Done" right for tickets whose change is merged but not deployed? Default: yes as commissioned (the comment says Done means merged to main, not deployed); the tickets' own text already says "Not deployed". Stamp `MOVE` = NONE for comment-only.
- Q6: Hard stop and target READY: the drafter suggests target READY 100 minutes after launch (seven Jira writes, three Done-when checks, three records rows) and hard stop 3 hours. Default: accept.

## FOR TUESDAY items the seat only LISTS (the kit has it write no Jira for them)
From the gate's Decisions list (lines 343-352), each recorded in row #392 as OPEN, NOT RULED when slot `DECISIONS-ROW` is FILE:
1. The six "Nothing pins Route B's command." sentences: 310 (0022) and 397 (0024) stale, the other four true (same as row #385 O1).
2. A3x's boundary: "a reworded ... flag turns a row red" vs "a reworded flag that changes the pinned text".
3. Row 258: name `--exit-on-error` or not (the 88-character width allows it only by shortening).
4. The scanner's range gap (the 0021 section is outside the b616 scanner's heading range; PCOMP-98's lane; row #385 O2).
5. The test's +124 lines against the commission's 25 to 60 (the in-row controls carry most).
6. A11c: no row catches a demo-VM claim in the Proven-on scope sentence.
7. B815-5, the `heavy.sh` TZ log quirk: Note N-TZ in the same row (D4).
You will card or rule these; the kit decides none of them.

## UNMEASURED
Test, mutant and psql results (A1 to A9, M30 to M37, 10 of 10, 29 of 29, 12 of 12: RELAYED from the gate); the two evidence files' contents; whether the workflow's Done transition needs a resolution field (B532's PCOMP-30 move sent none; the transitions list shows `41 Done` for all three keys); the exact line numbers of the gate's Decisions items; main and Jira after about 13:00; the hosted site (out of fence).

## Outside-the-fences disclosure
None. Read-only throughout: Jira GETs via `.tools/b808/scripts/jira808.py` (scratch scripts `r818.py`, `s818.py`, `h818.py`, `o818.py` in the session scratchpad import its `get`, `jql`, `adf_text`, `OWNER_WAIT` only), `gh api -X GET` under the Composer `GH_CONFIG_DIR` (raw DEPLOY.md and the test file saved to the scratchpad only), git read verbs with `--no-optional-locks`, grep/sed/ls, tmux, lsof, uptime. No card store, no `decision_queue.sh`, no ledger, staged-brief or scoreboard read, no WEDNESDAY/FRIDAY tree, no mail/Artifact/Docs tool. The advisory case-sensitivity hooks fired on three of my greps; each result was paired with a control or re-run with `-i`. Two files written: the kit and this report.
