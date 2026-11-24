STARTABLE: YES

# B2036 drafter report (Sonnet, read-only Agent-tool drafter), Datasec / Security Composer, records pass for pull request 133 (PCOMP-130)

Clock: `date` printed 12:07:31 at the start and 12:18:39 at the last check (AEDT, Tue 2026-11-24). Kit: `/Volumes/Datasec_DEV/TUESDAY/2_Project_Files/tuesday/briefs/2026-11-24_B2036_SEAT-R312_composer-records-pr133.md` (172 lines, 77269 bytes, 11 four-underscore lines = 10 slots + last line). Sidecar: `...composer-records-pr133.md.measured` (189 claims, `stamp_check.py <kit>` rc 0). Scratch: `/Volumes/Datasec_DEV/TUESDAY/2_Project_Files/fleet/state/s321/b2036/`.

## BLUF
The kit is startable. It copies the shape of B2007 (the kit that ran clean on 2026-11-23) with five deliberate differences: one C-entry (C-160 by program), NO create, one comment and one move on PCOMP-130 only, labels read `plan-comp-496` ALONE (no seed marker), and one BACKLOG row touched (#496). All facts were re-read live; every prototype STOP check passed with its control fired.

## Facts re-measured with instruments (each in the kit's THE FACTS)
- Code main = `d06508f8a69267542b92959a2048198055a7b473` (gh api -X GET, control pulls/9999 HTTP 404, zero-sha commit HTTP 422); PR 133 merged true, merged_at 2026-11-24T00:42:26Z = 2026-11-24T11:42:26+11:00 (python zoneinfo), head `7e10c623...`, 1 commit, 1 file, +10 -2, blob `09c3945d...`, 13123 bytes, `git hash-object` equal; squash parent `8b9ab200`, tree `32b3304b...` equal to the head's tree; check runs Analyze (csharp) and Analyze (javascript-typescript) completed success; open alerts on main 0; 0 open PRs; compare 8b9ab200...main ahead 1, one file.
- Four release blobs equal at 8b9ab200 and d06508f8; control at b4681297 reads unequal (b83e2e87, 7957c88f, b2e46ccb, 3ba29908).
- Test file at the squash (grep -n): `True|False` once at :88, `png|svg|jpg` once at :99 (it was :97 at the base: PCOMP-130's description says "line 97", so the comment and the entries say "now on line 99"), morePlants on 6 lines (:25 :31 :37 :216 :217 :222), the optional-space pattern at :123 (never copied into a text: the records rule bans the vendor initials).
- Gate B2035 VERDICT line 1 `GATE B2035: GO @ 7e10c62 on main 8b9ab20`; mutant lines `S1 GREEN / RED; S2 GREEN / RED; S3 GREEN / RED` and `T1d RED / RED; T1e RED / RED; T1f RED / RED` once each; Blocker 0, Major 0 (control Notes 1).
- Jira (GET, control PCOMP-9999 HTTP 404): PCOMP-130 Task, Backlog, labels exactly `plan-comp-496`, 0 comments, 0 changelog, transition 41 Done present, no Done-when line (control: live PCOMP-12 comment counts 1). Project: 130 issues, Done 54, not Done 76, held 19, seed marker 94, updated >= 2026-11-23 4. After the pass with comment and move: Done 55, not Done 75.
- Root records repo: main `413685b7...`, no remote, C-159 at :2981 (next C-160, no heading), row #496 at :492 (5 fields, ends `. |`), JIRA.md :64 `- B2007`, history :3 B2007; PR 133 / d06508f8 / B2033 / B2035 / B2036 count 0 in all four record files (controls PCOMP-130 and C-159 fire).
- Seat id R312: 0 files in 102 non-pre SEAT kits of 11-23 and 11-24 (control R307 1 file). Panes: no Composer pane at 12:09:28.

## D-decisions (mine, for Tuesday to veto)
- D1: No new ticket; Note N1 (optional-space pattern) goes into the C-entry's open list (FOR-RECORDS item 4 says "a candidate for a later pass only if wanted").
- D2: The comment states the line shift (88 stays, image pattern 97 -> 99) because PCOMP-130's description says "line 97"; the description itself is not edited.
- D3: The row #496 sentence says "the work of this row is on main" and does NOT say CLOSED (the row starts OPEN, NOT RULED).
- D4: AUTH-133 quotes the product owner's 2026-10-24 standing words from line 9 of the pickup file (RELAYED; the seat reads that one line only, because lines 12-13 name a decision card). The ticket's "Not ruled" is quoted and the call is called the coordinator's.
- D5: The record spans write "True or False" and "png, svg or jpg" without pipes; only the Jira text keeps `(True|False)` and `(png|svg|jpg)`.
- D6: Review reviewer's disclosure (two docker verbs before the lock, one hook-refused call) is relayed in REVIEW-133 as the gate wrote it.
- D7: The B2007 lesson C8 (deploy fragments are case-sensitive) and C1 (a control file must exist) are folded in as named corrections.

## Q-questions for Tuesday (each with a default)
- Q1: Ticket for Note N1 (optional-space pattern)? Default: no ticket, note only (D1).
- Q2: Slots to stamp. Default: JIRA WRITE, COMMENTS PCOMP-130, MOVES PCOMP-130, RECORDS WRITE, REC-MERGE MERGE, STATE-ROWS APPEND; BASE: root main 413685b7d8bd2c5bdf8d2ce3d4b2129fddbfd71f, code main d06508f8a69267542b92959a2048198055a7b473, PR 133 squash same sha, gate line 1 as above, PCOMP-130 0 comments.
- Q3: Move PCOMP-130 although its last sentence says "Not ruled"? Default: yes (FOR-RECORDS item 1 and the PCOMP-67 precedent; the entry says the call is the coordinator's).
- Q4: Seat id R312 and pane `Datasec/Composer-R312`. Default: keep (free).
- Q5: The stale PCOMP-130 and PCOMP-67 descriptions, and the PCOMP-31..35 comments. Default: not touched, listed in FOR TUESDAY.
- Q6: Hard stop and launch window are Tuesday's; the kit's READY target is Step 0 + 75 minutes.

## RAN (prototype STOP checks; scratch outputs proto2.out, proto_donewhen.out, spans.out)
- Jira text rule over TEXT-130, both variants: 0 hits, 29 of 29 project controls behave. Records rule and deploy-word check: 12 spans x 12 variants = 144 scans, 0 hits, 18 of 18 planted controls behave (including a capital "Nothing deployed", which fires). Scanner: B2007's copy of textscan_b1808.py, sha256 prefix 70b6bab8a80118f5 (original d517e19fce6b9f9f; differs only in the names.json path); the name list is B2007's names.json (8 tokens, not printed), not the one the seat will build: marked in the kit.
- Whole-kit name scan 0 (planted underscore name fired), non-ASCII 0 (planted 1), only card-id-shaped string composer-seed-1023.
- Done-when rows 1-6 all MET on live reads at 12:16:17 with controls (wrong blob, plants removed, b4681297 blobs, planted check name, planted phrase); text facts MET (including the squash-body sentence, which only reads 1 after line breaks are collapsed: a plain grep -c -F reads 0, and the kit says so).
- BACKLOG append check on a scratch copy: 1 changed line, 5 fields, strict prefix, planted extra-pipe row reads more fields.
- stamp_check sidecar: 189 lines. 14 of them are marked `NOT A LITERAL` (the checker pairs backticks across the text between two spans); the rest are python str.count lines over named corpora, with row/line pointers checked by awk NR==n (e.g. jira_write.py :10 :19 :81 :83 :116 :136 :137, jira_readback.py :30 :40 :41, CLARIFICATIONS :2981 :2995, BACKLOG :491). The sidecar is count-based for command and file literals (the same literal ran in B2007's kit); the substantive literals are measured by the prototypes above. Tuesday's five-line spot-measure should favour ids 8cffa50a, e641ee4b, 1d1897c4, dd0d2e3d, 7fe098b0.

## Chain-step inputs (MEASURED LITERALS 4)
| step | inputs | produced by |
|---|---|---|
| 0 | the kit, slots, root repo, `.tools/b2007/scripts` | exist at BASE (stamp) |
| PRIOR WORK | Jira GETs, gh GETs, record files | exist at BASE |
| 1 | gate files, B2033 STATUS, test file at squash, pickup line 9 | exist at BASE |
| 2 | slot values, span hashes | Steps 0 and 1 |
| 3 | spans, `names.json`, scanner copy | kit; `build_names.py` run in Step 0/3 (before the scans) |
| 4 | Step 1 reads, spans | `movechecks.json` and `jira_before.json` written in Step 4 itself |
| 5 | `payloads.json` (Step 4 order (1)), `movechecks.json` | Step 4 |
| 6 | C number (Step 0), comment id and move result (Step 5), date (Step 0) | Steps 0 and 5 |

## Span sha256 prefixes at drafting (unfilled markers, as extracted by spans_check.py)
TEXT-130 aac575edb5ffd328; TOPIC-133 7016d5a3287a1b35; AUTH-133 02d47fee496fc209; QUESTION-133 89f7f712caf9ce76; SETTLED-133 e9f1e81c4d33c2db; REVIEW-133 2307b1ea6976337f; TICKET-133 f23cf723f1814aaa; OPEN-133 06227186e721a17b; PERMITS-133 ad4b55f970dec77a; FORBIDS-133 7fd2414a9ecedc8d; SUPERSEDES-133 f112ebe282f8e1d1; LANES-133 3dc4eea9d2d0a803; ROW-496 c28fd7d163f47f3e. (Rebuild with spans_check.py if the kit is edited; the kit's own sentence says the seat reprints these and compares against this table.)

## UNMEASURED
What the demo runs (no hosted probe); the gate's mutant results and the build's runs (RELAYED, no test run here); the git diff --quiet instrument across the squash (the entry says the equal blobs are what was measured); the seat's own names.json; helper-copy edits, dry run, apply, read-back, records script, commit and merge (never run on a real output, marked in the kit); the tmux pane check (no Composer pane at drafting).

## Outside-the-fences disclosure
- Writes: the kit, its sidecar, this report, and scratch files under `/Volumes/Datasec_DEV/TUESDAY/2_Project_Files/fleet/state/s321/b2036/`. Nothing in the Composer folder, Jira or GitHub was written.
- Two Bash calls were refused by hooks before running (a `cp` whose destination hook-matched the project tree, and an `rm -f` of a sidecar I meant to regenerate); nothing ran, and I did not retry them in that form.
- Reads outside the commission's named files: the pickup file's lines 9, 12 and 13 by `grep -n` (line 12 printed the first 260 characters, which include a decision-card id; I did not use or copy it, and no card was read with `decision_queue.sh`); an earlier drafter's scratch scripts under `fleet/state/s318/d2007/` (read-only, for form); B2007's scripts and STATUS under the Composer project (read-only); `tmux list-panes -a` (names only); `lsof` listening-socket count only (13, no ports needed).
- No credential was printed; Jira auth went through the project's own `jira_lib` in-process.
