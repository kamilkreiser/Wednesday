STARTABLE: YES (after Tuesday answers or accepts the defaults of Q-1 to Q-4; none blocks the launch)

# B1318 drafter report (lane R-N1, seat R181, NexusAI records, Sonnet), drafted 2026-11-06 10:27 to 10:37 AEDT

## BLUF
- Re-measured, not copied: **all 69 code scanning alerts listed by the nine alert-bearing tickets read `fixed` on `refs/heads/main`, none dismissed** (RD-782 7, RD-783 10, RD-784 2, RD-785 2, RD-786 26, RD-787 14, RD-788 6, RD-789 1, RD-774 1). Control: alert 174 reads `open`, alert 999999 answers 404. So every one of RD-782 to RD-789 and RD-774 meets the done-when as this kit reads it; each is movable.
- **RD-786's "family" is not a family of To Do tickets:** RD-873, RD-874 and RD-875 are already Testing. They are read-only in the kit. RD-873 itself says RD-786's done-when is 26 alerts; all 26 read fixed (21 at the PR #98 analysis, five later: 95, 96, 97, 98, 99).
- RD-836 has no alert and no done-when line. The kit gives it a read-at-source rule (six gated writers at main `server.js` lines printed by program, PR #97 an ancestor, two describes present) and a not-moved text if any clause fails. Default: move (Q-1).
- The product owner's 6 Nov 10:12:54 words are recorded verbatim as C-239 in a new section 75 (highest now C-238 at `CLARIFICATIONS.md:2525`).
- Partition: N101 (`backend/server.js`, branch) and this seat share nothing; the seat reads server.js only as the raw file at the pinned main sha. Records-PR gate check: no live NexusAI gate pane at drafting (panes: wednesday, HPSM-POC-H127, fleet-monitor, three unnamed); Job G re-checks at A5 and before the push.

## Files
- `/Volumes/Laptop-DEV/TUESDAY/2_Project_Files/tuesday/briefs/2026-11-06_B1318_SEAT-R181_nexusai-records-pr98-pr97-pass.md` (11 `____` slots, counted by `grep -c -E '_{4}'`)
- `/Volumes/Laptop-DEV/TUESDAY/2_Project_Files/tuesday/briefs/2026-11-06_B1318_slots.json`
- this report

## Facts re-measured (instrument; control)
- main `ffb6715230d1f5533746343f997e00b9854434f9`, open PRs 0 (`gh api -X GET commits/main`, `pulls?state=open --jq length`, 10:33:32; control `pulls/99999` 404 and `pulls?state=all` earlier in the sweep).
- PR #98 merged true, `d463f8817fba925dee7e78c5216df3d5ea8ad073`, 2026-10-20T11:16:38Z, compare to main ahead 192 behind 0. PR #97 merged true, `115a775b6d5808629f493ef7a3f602d8c5853a22`, 2026-10-20T17:12:04Z, ahead 184 behind 0 (10:28:03).
- Alerts: one `code-scanning/alerts/<n>` GET per number (10:28:03 to 10:28:58), numbers parsed from each description by regex, counts equal the stated N, the 69 parsed equal the 69 read; planted 999 makes the sets differ. `fixed_at`: 21 of RD-786's 26 and all of RD-782 to RD-789's others at 2026-10-20T11:20:31Z; 95 at 10-24T20:26:13Z; 96, 98, 99 at 10-26T18:42:37Z; 97 and RD-787's 116 at 10-27T08:38:55Z; 70 at 10-20T17:16:01Z; twin 274 fixed.
- Jira (GET, scratch copy of b1308lib.py, 10:31 to 10:33): statuses, comment ids, transitions as pinned in the kit; no comment on RD-774 or RD-836 after the PR #97 merge; no literal "done when" in any of the ten descriptions (control: RD-873 has one); `Fix as one change ... Never dismiss` present in the nine alert tickets.
- RD-836 pointers at raw `backend/server.js` blob `c04a0f4e` (22428 lines): 6841, 20718, 20984, 21004, 21014, 21081, 21279, 21294, 21331; test file describes at 340 and 522; all printed by `grep -n`.
- `CLARIFICATIONS.md` 2530 lines, sha256 `e3289a40...`, C-239 and `## 75.` 0; HISTORY.md blob `998703da...` 9679 lines, B1308 at :9645, B1318 0, `records/b1318` 0 refs.
- Ports: `lsof -nP -iTCP:9800-9999` 0; scan of 21 non-`.pre-` SEAT kits for `R181`/`B1318` 0 (control R175 5 files).

## D-decisions
- D-1: no new Jira text mentions any decision-card id or person; ruling cited as "the product owner's ruling of 29 October" (C-227 line printed).
- D-2: the 28 other To Do `codeql-baseline` tickets (RD-762 to RD-815 by key) are explicitly out of the fence; the kit makes the seat list them, not touch them.
- D-3: the product owner's words go in C-239 verbatim and the kit refuses to read them as approval of any move (wording rule); the question the "yes" answers is declared unknown.
- D-4: records-branch landing follows C-190 (merge commit, never squash), quoted from `CLARIFICATIONS.md:2067`.
- D-5: slot values for AUTH-RULINGS are worded "RULED ... at the stamp and not before", so the pre-written line is not an attestation of a read Tuesday has not done.

## Q-questions for Tuesday (each with a default)
- **Q-1:** RD-836 has no alert; may the seat move it to Testing on a read-at-source of the six admin gates (no test run), or comment only? Default: move if all six gate lines, PR #97 ancestry and the two describes re-print; else comment only (kit text V / VN).
- **Q-2:** Is "every alert in the ticket's own list reads fixed on main, none dismissed" the done-when for RD-782 to RD-789 and RD-774, given none carries a literal done-when line? Default: yes (RD-873 states RD-786's done-when is 26 alerts).
- **Q-3:** Sonnet for a records seat rests on precedent (B1235 to B1308), not on a model-routing row (C8 at :98 names no records job). Default: Sonnet.
- **Q-4:** Is the move of In Progress tickets RD-774 and RD-836 inside the same records-step grant as the To Do ones (the project's rule text says To Do-era "Code change -> Testing"; the transition list offers `In Review` -> Testing from In Progress)? Default: yes, same pattern as RD-916 on 5 Nov.
- **Q-5:** Record the 6 Nov words in NexusAI's `CLARIFICATIONS.md` (they name four projects)? Default: yes; other projects' seats record theirs.
- **Q-6:** Do the 28 other To Do `codeql-baseline` tickets deserve their own pass (not examined here)? Default: a later kit, not this one.

## UNMEASURED
- Whether N101 has a branch or pane (none at drafting); whether the tests in the PR #98 and #97 still prove what they proved (not run); the hosted build of main; any deployment; the question the product owner's "yes" answers; the words' source (RELAYED by Tuesday only); RD-902 to RD-907 current statuses (RD-868's comment names them, not read by status).
- The scripts in `session-tools/b1308/` are read for sha256 and line counts only (not opened whole); the seat adapts them and reads them whole first.

## Outside-the-fences disclosure
- Read-only: Jira GETs (RD-774, 782 to 789, 836, 868, 873, 874, 875, 879 and four searches) through a scratch copy of `session-tools/b1308/b1308lib.py` (heartbeat path changed) in the scratchpad `.../scratchpad/d/`; `gh api -X GET` under the project `GH_CONFIG_DIR` (commits, pulls 97 and 98, compare, 69+ code-scanning alert numbers, contents raw of HISTORY.md, JIRA.md, backend/server.js and the rd774 test, `gh api user` login test, git/matching-refs); local reads of `NexusAI/CLAUDE.md`, `1_Project_Definition/CLARIFICATIONS.md`, `ls` and `shasum` of `session-tools/b1308/` and `Briefs/`, `tmux list-panes`, `lsof`, `model-routing.md`, `models_latest.json`, `brief_seat.sh`.
- One misquoted zsh URL produced `no matches found` errors and one repeat; no write resulted. A first `cd_=1` variable assignment was typed by mistake (no `cd`). No decision_queue, no staged-briefs, scoreboard, ledger, WEDNESDAY or FRIDAY tree, no az, ssh, docker, no HTTP to any hosted host, no git verb in a project repo. Scratch files only in the session scratchpad. Wrote exactly the three files above.
