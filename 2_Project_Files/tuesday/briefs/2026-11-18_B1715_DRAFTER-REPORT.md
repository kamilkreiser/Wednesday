STARTABLE: YES

# B1715 drafter report (SEAT-R272, NexusAI records pass for pull requests 219 to 223)
Drafter reads of `date`: first 16:45:43 AEDT, last 17:09:58 AEDT, 2026-11-18. Kit `2026-11-18_B1715_SEAT-R272_nexusai-records-221-223.md` (215 lines, 100734 bytes, 12 four-underscore lines, last line `READ-WHOLE-BY-TUESDAY: ____`), sidecar `.measured` (142 lines: 104 literal lines + 37 sentence-to-source match lines (who-* and row-*) + 1 comment line). `stamp_check.py <kit>` exits 0 (104 of 104 claims measured). All 31 Jira text strings re-extracted from the written kit: sha256 labels equal, my scan over each text with sample fill-ins (and over each Detail with its landing string filled) reads 0 problems, controls fire (list in the kit's JIRA TEXT RULES). Entry and history blocks scanned for names, B-numbers, seat codes, at-sign, URL, non-ASCII: 0.

## BLUF
Startable. One records seat, Sonnet, pane `Datasec/NexusAI-R272`, one wait (the hosted Build of the newest merge commit `d4048bfa`, run 44246382733, `in_progress` at 17:04:37; earlier Builds today took 39 to 63 minutes, so expect about 17:25 to 17:50). Writes: up to 6 comments (RD-689, RD-980, RD-717, RD-749, RD-1003, RD-425), up to 4 moves to Testing (689 980 717 749), 1 move to Done (RD-1003), 1 create (follow-up of the picomatch review's F1 to F3), one section 100 / entry C-302 in CLARIFICATIONS.md, one history branch `records/b1715-history`. The seat writes no code, makes no pull request, sends no mail, runs no `decision_queue.sh`.

## Corrections to the facts in the commission (all verified at source)
1. **#223's merged head is NOT the reviewed head.** The review (B1700) read `50e6db9a` (counts 5876/377); the merged head `71a170e6` is that head + one merge of main (`3aa747ca`) + one counts regeneration. The two test files have the same blob ids at both heads (`362052d5`, `04f6164d`); merge tree = merged head tree (`6d0651b8`); the merged tree was not reviewed again (B1714 STATUS NOT TESTED). T-LAND-223 says so in words. #220, #221, #222 merged exactly their reviewed heads.
2. **RD-425 is Release Ready** (8 comments, newest 38545): comment only, no move; RD-689 is To Do (2 comments, newest 38932).
3. **RD-1003 goes to Done, not Testing**: CLAUDE.md line 303 "Decision / docs / non-code -> straight to Done"; precedent in the project's own records (C-253 line 2711, C-264 line 2799: decision tickets "MOVED TO DONE"; the 2026-11-16 ruling on RD-992 ended with RD-992 moved to Done). Code changes go to Testing (line 302, quoted by CLARIFICATIONS.md at lines 2485, 2493, 2501).
4. **#219's merge started no Deploy demo run at all** (HISTORY.md only; the commit has 4 workflow runs, none Deploy demo); #221, #220, #222, #223 each have a Deploy demo run `completed/skipped`. #223's Build was still running at 17:04:37, so "nothing deployed" holds but its hosted Build is not yet read.
5. Everything else in the commission matched: merge ids 078e7b3d / 5b3ca950 / 832bf2d9 / 50fab597 / d4048bfa; gates B1704, B1685, B1690, B1700; counts 5881/378 on main until #223, 5887/378 after; picomatch card ruled `a` "Narrow, dated exception", delivered 14:13:21; RD-1003 card ruled `a` "Record it, no code change" at 08:36:17, not yet delivered.
6. Merge-id naming trap (Q1): the full ids of the 222 and 223 merge commits hold hexadecimal runs (`b5970` inside `50fab5970e...`, `b341` inside `...b341de...`) that the project's case-insensitive B-number scan fires on, so those two are written as 7 and 8 character prefixes (`50fab59`, `d4048bfa`) in every Jira text and in the entry; the other three ids pass in full.

## Facts re-measured (instrument; control)
- PRs 219 to 223: `gh api -X GET pulls/<n>`, `git/commits/<sha>`, `pulls/<n>/files`, `/commits` (merged true; parents; trees; paths; adds/dels; 219: 1 path +21; 220: 3 paths +11 -17; 221: 4 paths +235 -15, trees equal; 222: 2 paths +34 -26; 223: 3 paths +165 -15, trees equal, 5 commits). Control `pulls/99999` -> 404. Merge times (AEDT = UTC+11): 12:04:45, 14:12:15, 14:12:29, 14:50:36, 16:44:52.
- Hosted Builds: job logs of 134495738812, 134548268490, 134548359754, 134563048391, each 1 `VERDICT: PASS` line, 5881/5881 across 378 (em dash bytes between PASS and the figures, `od -c`). Counts file by `contents?ref=<sha>`: 5881/378 four times, 5887/378 at d4048bfa. Check-run tables per merge commit (6/8, 6/6, 6/8, 9/11, 6/8 expected after the wait; the 11 is a Scheduled run's second set of Analyze rows).
- Code scanning on main (paged, `ref=refs/heads/main`): 22 open, 222 fixed, 7 dismissed (142 143 144 147 148 149 150); newest open created 2026-11-08T21:39:52Z; newest fixed_at 2026-11-16T22:06:02Z; all open alerts' latest instance at d4048bfa; javascript-typescript analysis 2193094962 (29 results). None of the six keys names an alert (description lines with the word: RD-980 1 = the sentence about moving RD-798/799/800; others 0; control RD-1002 1).
- Jira (own GET-only reader, credentials by name in-process, never printed): GET RD-1003 200, RD-99999999 404; states in BLUF 5 of the kit; transitions Testing id 31 and Done id 41 on all six; the seven markers each 0 (controls: LAND-218-1002-18NOV -> RD-1002, ACTIONAUTH-216-18NOV -> RD-1003); duplicate searches picomatch / GHSA id / dated exception / audit-prod.js each 0 (control `npm audit` 162); 999 issues, highest RD-1003.
- Records: CLARIFICATIONS.md 752293 bytes, sha256 `eb95fd62...`, section 99 at line 3041, C-301 at line 3043, ends with newline; next = section 100, C-302 (0 hits for every prior-work literal, controls C-301 and `pull request 218` present). HISTORY.md at d4048bfa: 10185 lines, last heading line 10166, ends with newline. Identity prefix `be76c2c1baf03ec1` (with newline `4123cf83d812afdc`). `/Volumes/Laptop-DEV` absent. `records/b1715*` 0 refs (control b1684 1). Panes: `%0 tuesday`, `%1 fleet-monitor`, two unnamed; no NexusAI pane. Disk 1074 GiB.
- Rulings at source (`decision_queue.sh show <exact id>`, three ids, no list): picomatch card and RD-1003 card and the 2026-11-16 RD-992 card all `ruled`, client_project Datasec/NexusAI, option details quoted in the kit equal the printed text. Every who-decided phrase and every gate-finding sentence is matched to its row in the sidecar (`who-*`, `row-*` lines).

## D-decisions (defaults; Tuesday approves at the stamp; none is written as the product owner's)
- D1 one create only: the follow-up of #221's F1 to F3 plus the 2026-12-18 calendar step (Task, Medium, labels dependencies / records-pass-<MMDD> / security). No ticket for #220's Advisory, #222's Minor, #223's five Minor (they travel in comments and the entry).
- D2 moves: Testing for RD-689, RD-980, RD-717, RD-749; Done for RD-1003; RD-425 comment only; RD-798/799/800 untouched (RD-980's own text says their move waits for the CodeQL read of main).
- D3 one entry C-302 (landings + the RD-1003 ruling + the picomatch ruling as relayed), not two.
- D4 the posted sentence "pull request 217 landed between the review and the merge" is corrected by one sentence in the new entry and the new history entry only; the earlier comments are not edited.
- D5 texts avoid `live`, `deployed`, `gate`, `complet` etc. by wording ("the run's own push", "put on a host"); the fourth rd684 cell (title prefix F10, a seat-code shape) is never named by its title.

## Q-questions for Tuesday (each with a default)
- Q1 Merge-id naming (see correction 6). Default: 7 and 8 character prefixes for 222 and 223; alternative: loosen the scan to a boundary form `(?<![0-9a-f])b\d{3,4}(?![0-9a-f])` and print full ids. Default stands unless you change the project scan rule.
- Q2 Create or not, and priority. Default: NEW at Medium (the production audit goes red on 2026-12-19 Sydney unless done or ruled). Alternative: Low, or NONE.
- Q3 RD-1003 to Done. The card's option detail asks for the record on the ticket and in the clarifications; the Done move rests on CLAUDE.md line 303 and the RD-992 precedent, and the ticket's own proposed option (a) also mentioned the route's row note, which the card detail does not ask for (the kit changes no table). Default: DONE `1003`; label `needs-decision` is not edited. Alternative: DONE NONE (comment only).
- Q4 RD-717 to Testing although two of its four mutants (M-A1, M-A3) have no cell (the review judged them equivalent through HTTP and accepted; the comment says so and tells the verifier what a cell would need). Default: move. Alternative: drop 717 from MOVE.
- Q5 One entry or two (landings; ruling in the C-253 form). Default one.
- Q6 Hard stop 19:30 AEDT (wait limit 18:30), launch now (the seat waits on the Build). Default as proposed.
- Q7 NOTE425 WRITE (the RD-425 note: its identifier guard now has no entry marked known). Default WRITE.

## UNMEASURED
The Build of d4048bfa; the Jira create payload (priority name Medium, labels, ADF) and the Done transition screen were not exercised (no write); that the key file in the transport string exists (copied from B1684, whose STATUS shows it worked); Node 24 / Linux beyond hosted CI; the B1704 review's real-clock lapse (only injected clocks); the Scheduled run's reason for the extra Analyze rows on 50fab597 (the CHECKS fill-in property covers it).

## Chain inputs table (every step's inputs come from an earlier step or exist at BASE)
| step | inputs | made by |
|---|---|---|
| 0 | the stamped kit, `df`, the pane | BASE |
| 1 | `.tools/b1715/` | 0 |
| 2 | `.tools/b1715/`, the kit | 0 |
| 3 | helpers, identity log, `snap_before.json` | 2, 1, 3 itself (baseline helper) |
| 3b | wait helper, the run id and merge sha in the kit | 2, BASE |
| 4 | texts in the kit, facts of 3 and 3b, the dry table | BASE, 3, 3b |
| 5 | dry payloads, markers, ticket states of 3 | 4, 3 |
| 6 | `snap_after.json` and comment ids of 5, CLARIFICATIONS.md before-copy | 5, BASE |
| 7 | `entry-numbers.txt`, identity prefix, `origin/main`, the kit's history text | 6, 1, BASE |
| 8 | all logs | 0 to 7 |

## Outside-the-fences disclosure
- Ran `decision_queue.sh show <exact id>` three times (never `list`); printed each single-card file whole (not filtered). The glob `card*.txt` in one `wc -l` also matched two other sessions' card files in the scratchpad (names and line counts printed; not read).
- Wrote the kit and sidecar with `cp` from a generator in the scratchpad (the sha256 labels are computed), not with the Write tool; the report was written with Write. One `rm` of my own sidecar was refused by the no-delete hook and nothing was deleted (the generator overwrites the file).
- Read-only reads outside the briefs folder: NexusAI Briefs STATUS files B1679, B1683, B1684, B1691, B1714 (whole), B1687 and B1694 (headings), CLARIFICATIONS.md and CLAUDE.md lines, `git config --get user.email` in the project's 2_Project_Files (value never printed), `tmux list-panes` and `tmux display -t %0`, today's daily note (grep only, for lane status: no DROPPED/HELD line concerns these keys), `fleet/specs/model-routing.md` lines 97 and 110, `models_latest.json` line 23.
- Jira: GET only through my own scratchpad reader reading the project `.env` by name. GitHub: `gh api -X GET` only under the project's GH_CONFIG_DIR. No az, ssh, docker, mail, push, PR, deploy.
- Two zsh-word-split hook refusals (`====` separators) and several advisory hook notes; no effect on results.
- Scratchpad files (reader, generator, scans, fetched sources, fetched HISTORY and JIRA.md copies) are in `/private/tmp/claude-501/-Volumes-Datasec-DEV-TUESDAY/7d54115b-162a-4248-9923-2b718612d52b/scratchpad/`.

## Model row
Sonnet (records): `fleet/specs/model-routing.md` line 97 row C7 and line 110 row G3; model id `claude-sonnet-5-5` (`models_latest.json` line 23). Launch line carries `BRIEF_SEAT_LEVEL=sonnet` inside the quotes. Ports: none.
