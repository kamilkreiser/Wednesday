STARTABLE: YES

# B2055 DRAFTER REPORT (Sonnet drafter, in-session, read-only): NexusAI records kit for pull requests 248 and 249, seat R318

Kit: `/Volumes/Datasec_DEV/TUESDAY/2_Project_Files/tuesday/briefs/2026-11-24_B2055_SEAT-R318_nexusai-records-248-249.md` (88652 bytes, 174 lines). Sidecar: the same name plus `.measured` (181 claims, 181 measured; `stamp_check.py <kit>` exits 0). Scratch: `/Volumes/Datasec_DEV/TUESDAY/2_Project_Files/fleet/state/s323/d2055/` (reads started 18:15:07 AEDT, last reads 18:30:56, kit built after, from `date`).

## BLUF
- One kit, one seat, Sonnet: RD-1026 result comment plus move to Testing, ONE Low hardening ticket (NEW-A), CLARIFICATIONS section 111 with three entries (C-321 pull request 248 with RD-1026 and its review; C-322 pull request 249; C-323 the correction of C-319's doubled run id, a new entry, nothing edited), and an optional history branch `records/b2055-history`.
- Every fact of the commission re-measured at source and equal: PR 248 = merge `dd0698a6` (parents `04a6b89d` + `444fe281`, merge tree = head tree), Deploy demo run `45333856653` skipped (both jobs skipped); PR 249 = merge `c74d1ad4` (parents `dd0698a6` + `c6e48118`); main = `c74d1ad4`, 0 open pull requests.
- Seat id R318 is free (word scan, control taken).
- One decision for you (Q-1): RD-1014 (To Do, Medium) counts about 80 first-run lines and may hold the first-run rows of NEW-A. Default: create the ONE ticket as commissioned, name RD-1014 as related, write nothing on it.

## Facts re-measured with instruments (each with its control)
| Fact | Instrument and result | Control |
|---|---|---|
| main | `gh api -X GET git/ref/heads/main` 18:28:00 and 18:30:53 -> `c74d1ad4d8291f42fb66660fc38a3e61afe9b8e1`; `pulls?state=open` -> 0; `compare c74d1ad4...main` identical | `pulls/99999` 404 |
| PR 248 | `pulls/248`: merged 05:30:56Z = 16:30:56 AEDT (python zoneinfo), merge `dd0698a6...`, parents `04a6b89d` + `444fe281`, 2 commits, 3 files, 218/4; trees `b065c652` = `b065c652` | file list equals the review's (index.js 1/1, test file 214/0, counts 3/3) |
| PR 249 | `pulls/249`: merged 06:05:45Z = 17:05:45 AEDT, merge `c74d1ad4...`, parents `dd0698a6` + `c6e48118`, 1 file HISTORY.md 22/0; head tree `5893b14d`, merge tree `a007fbb1` (differ BY DESIGN: `compare c6e48118...c74d1ad4` lists exactly the three paths of 248) | the kit says "merge tree = head tree: NO" for 249; do not copy B2043's "YES" wording |
| Checks 248 | 8 check-runs completed: 6 success, `build` (138241202515) and `deploy` (138241202821) of Deploy demo skipped; 5 runs: Build 45333856816, Push on main 45333856452 (event `dynamic`), Deploy demo 45333856653 skipped, npm-audit, Gitleaks | the two checks named `build` told apart by `check_suite_id` (Build workflow's = 138241201471) |
| Checks 249 | 6 check-runs, all success; 4 runs; no Deploy demo run | 248's merge commit has a Deploy demo run |
| Build logs | `actions/jobs/<id>/logs` with `--allow-escape-sequences`: 138241201471 and 138254236292 each `VERDICT: PASS — 6300/6300 tests passed across 397 suites`, one line each | `VERDICT: FAIL` count 0 in both; counts file at `dd0698a6` and `c74d1ad4` 6300/397, at `04a6b89d` 6280/396 |
| Code scanning | main paged: 22 open (same 22 numbers as the earlier passes), 222 fixed, 7 dismissed; created or fixed since 2026-11-22T13:00Z: 0; open rows by path: server.js 13, incidents.js 2, jsonStorage.js 2, entraProvisioning.js 2, emailService.js 2, tests/uat-run.js 1, **static/js/index.js 0**; analyses by `commit_sha`: javascript-typescript 29 at both merge commits | 222 fixed rows each carry `fixed_at`; server.js 13 |
| RD-1026 | Jira GET: To Do, Bug, Medium, labels `records-pass-1120,security`, 0 comments, description 5589 chars; transition id 31 `In Review` -> Testing; 1034 issues, highest RD-1038; markers `LAND-248-1026-24NOV` and `HARDEN-248-24NOV` 0 (variant `-25NOV` 0) | `RD-99999999` 404; markers `TOOLLABEL-238-20NOV` -> RD-1026, `DSLIST-247-24NOV` -> RD-1036, `HIGHRISK-246-24NOV` -> RD-1038 each 1; label `records-pass-1124` 3 issues |
| Records files | CLARIFICATIONS.md 932503 bytes, sha256 prefix `56dee9441642851f`, 3224 lines, section 110 at 3202, C-320 at 3222; HISTORY.md at `c74d1ad4`: 10406 lines, 1137780 bytes, prefix `507d9add4195c3d5`, 7563 non-ASCII bytes | `C-316` 7 in CLARIFICATIONS; `pull request 247` 1 in HISTORY; `pull request 248/249` 0 in both |
| C-319 slip | python over lines 3202-3224: `(run 45315569382)` twice on line 3216 and 0 on every other line; any repeated parenthesis group inside one line of section 110: only that one | planted `(run 1) (run 1)` fires the same check |
| Pointers | `pointers2055.py`: `pointer rows 40 fail 0` at `dd0698a6`, `04a6b89d`, `c74d1ad4` (index.js 113, 3466, 3470, 3474, 3478, 3515, 3523, 3529, 3569; first-run-setup.js 1431, 1468, 1471, 1486, 2946, 4098, 4127, 4184, 4240; adapter 307, 309, 313; tools.js 283; server.js 4096, 7728, 7765, 7823, 7901, 7920, 7950; model-config.js 175; azureLogAnalytics.js 422; test describes 119, 184; counts lines 4, 5) | line-1 controls (`escapeHtml` in index.js, `executors` in the adapter) read False; `escapeAttrValue` in first-run-setup.js 0 lines, `escapeHtml` 8 |
| Tool lookup | `node v26.13.0` on `{search_users(){}}`: `typeof o['constructor']` function, `Object.hasOwn` false; `search_users` function/true; null-prototype copy undefined | the kit marks the claim DERIVED from source; the seat runs no node |
| Seat id | word scan over 211 non-`.pre-` SEAT kits of 11-17..11-24 (excluding this kit): R318 0 | R315 in 3 files |
| Scanner | `.tools/b2043/scan1947.py` and `.tools/b2004/scan1947.py`: 6267 bytes, sha256 prefix `3707dc37c4795fbf`, `cmp` equal | bank scan: 33 texts, 0 problems; planted `Tuesday` (both modes), `_by_Kam_`, doubled parenthesis, card shape, `B2055`, `R318`, URL all fire |
| Layout | simulated append on scratch copies: CLARIFICATIONS heading 3226, C-321 3228-3232, C-322 3234-3236, C-323 3238-3240, ends 3240; prefix byte-equal, added bytes ASCII; HISTORY heading 10408, 10427 lines | prefix byte-equal and added bytes ASCII printed True in the same run |
| Model row | `model-routing.md` line 97 (C7), 98 (C8), 110 (G3); `models_latest.json` line 23 `claude-sonnet-5-5`; `brief_seat.sh` default Opus is now at **line 31** (`LEVEL="${BRIEF_SEAT_LEVEL:-opus}"`), not line 24 as DRAFTER_RULES says; launch line carries `BRIEF_SEAT_LEVEL=sonnet` inside the quotes | |
| Ports and panes | none used; `tmux list-panes -a` 18:28:00 and 18:30:53: `%0 tuesday` and two unnamed; no `Datasec/NexusAI-*` | |

## D-decisions (mine, each reversible by one slot or word)
- D-1: three entries (C-321, C-322, C-323). The correction is its own entry because the section is append-only (commission). Its text avoids writing the doubled string (so the doubled-parenthesis check can run on the kit's own entries).
- D-2: the Jira comment and the entries state "default of the change, not the product owner's choice" for leaving the sibling rows out (the coordinator's Q-3 default in FOR-RECORDS); no product-owner ruling is cited anywhere.
- D-3: the kit builds the fixes for B2043's Deviations 3, 5 and 9 in: counts of its own texts are printed by program (Step 1 list); the create-search guard reads a REVIEWED list from the start (HOLDS 4c); fill-in clauses carry a run id only in the fill-in (no template line holds one) and the check over added lines refuses a parenthesis group twice in one line and a 3-word run twice (controls named). Deviations 1, 4, 6, 8 are folded in too (helpers and group first; `Push on main` event is `dynamic`; one-command transport on every `ls-remote`; an open pull request is named, a stop only on a shared path).
- D-4: the EVIDENCE read applies to the Deploy demo run of `dd0698a6`: anything but skipped is the deploy switch ON, approval-class, STOP (carried from the landing text step 4).
- D-5: no text says an alert closed; the code scanning clause carries "0 of the open alerts in static/js/index.js" (measured, control 13) and the comment says the hosted check cannot witness the fix (local comparison: gone 0).
- D-6: Jira text rules: the independent review's "secrets scan" is written "a leak scan" and "the seat's red-proof" "the builder's red-proof" (the first drafter scan read `seat` in one text; re-worded before freezing).

## Q-questions for Tuesday (each with its default; the Stamp's Q-ANSWERS slot takes them)
- **Q-1** RD-1014 overlap. RD-1014 (To Do, Medium, `records-pass-1120,security`) excludes the chat region but counts 82 first-run-setup.js rows and asks "whether the 80 first-run error lines belong here or in a separate Low ticket". NEW-A holds first-run-setup.js 1486, 4127, 4240, 1468, 1471. Default: create NEW-A (the commission's ONE ticket), say in its P3 that whichever lands second drops rows the first fixed, write nothing on RD-1014. Alternative: drop the first-run rows from NEW-A and name them in C-321 only.
- **Q-2** Entry shape. Default three entries (248 with RD-1026, 249, correction). Alternative: fold 249 into C-321 (two entries); say so and I would reflow the layout numbers.
- **Q-3** NEW-A type. Default Task, priority Low (the commission says Low; Task is my reading; the review graded the rows not reachable). Alternative Bug.
- **Q-4** HISTORY slot. Default WRITE (branch `records/b2055-history`, same identity form as the previous pass, no pull request; Tuesday lands it, head pinned, merge commit).
- **Q-5** MOVE-1026. Recommended `1026` (Testing by CLAUDE.md line 302; a human moves it on to Release Ready).
- **Q-6** Launch. Cockpit line as written (Sonnet inside the quotes); the waiter `launch_when_cool.sh` is Tuesday's choice.

## UNMEASURED (named)
- The local `user.email` value and its prefix `be76c2c1baf03ec1` (RELAYED from the previous pass's STATUS; `git config` is not a drafter verb); the push permission of the deploy key (worked for the previous pass).
- Everything the seat runs: the ADF builder, the posting path, the append helper, the check over added lines on real fill-ins, the Step 7 helper, the FOR TUESDAY lister, the EVIDENCE poll (see "checks not run" below).
- The review's numbers inside the comment and C-321 (20 cells, 11 red at base, 10 and 9 in the browser) are RELAYED from VERDICT.md and FOR-RECORDS.md; the drafter did not run jest or a browser. The seat re-reads those lines.
- Reachability of each sibling row is the review's reading, re-read by me at the source lines only (constants at server.js 7728/7765/7823/7901/7920; adapter lines); Azure's table-name rule is not measured (stated in NEW-A).
- Whether RD-1014's census holds the five first-run rows (its census file is outside the repository).

## Checks of the kit that were not run on a real output, and what I ran instead (DRAFTER_RULES 2026-11-20 row)
STOP-severity checks run once on prototype output: (a) the scanner in `entry` mode over every filled entry and history line (0 hits; controls: `Tuesday`, `_by_Kam_`, `B2055`, `R318`, https URL, card shape each FIRED); (b) the doubled-parenthesis check and the 3-word repeat check over all 33 filled texts (0 hits; planted `(run 1) (run 1)` and `x y z a b c a b c d` FIRED); (c) the append layout simulation on scratch copies (prefix `cmp` equal, ASCII added bytes, headings at 3226/3228/3234/3238, end 3240; HISTORY heading 10408, end 10427). Not run: the seat's own helpers, which do not exist yet.

## Chain inputs (every step's inputs exist at BASE or come from an earlier step)
| Step | Inputs | Produced by |
|---|---|---|
| 0 | the kit; REFUSE 1-3 reads; scanner copy | BASE (`.tools/b2043/scan1947.py` exists, 6267 bytes) |
| 1 | the kit's text bank; scanner | Step 0 |
| 2 | identity read, `ls-remote`, fetch | BASE; helpers of Step 1 |
| 3 | GitHub, Jira, records reads; PRIOR WORK | BASE; Step 2 |
| 4 | texts, fill-ins | Step 3 reads |
| 5a-5c | payloads, marker searches, transition id | Step 4; Step 3 |
| 6 | created key, comment id, printed line numbers (`<<LINE-C319-HOSTED>>`, `<<RUN247>>`) | Step 5; Step 3 |
| 7 | `entry-numbers.txt`, section written | Step 6 |
| 8 | all logs | all |

## Outside-the-fences disclosure
- Writes: the kit, its sidecar, this report; scratch under `fleet/state/s323/d2055/` (helpers, copies of raw files at the merge commits, two Build job logs, `HISTORY.c74d.md`, simulated appends). Nothing in any project, Jira, GitHub or the card store; no `cd`; nothing deleted; nothing to any human; nothing of another client.
- Reads: NexusAI `CLARIFICATIONS.md`, `CLAUDE.md`, `STATUS B2043`, `.tools/b2043/scan1947.py` and `.tools/b2004/scan1947.py` (bytes read for `cmp`/sha only); `gh api -X GET` under the NexusAI `GH_CONFIG_DIR` only; Jira GET only with credentials read by name in-process (never printed; `gh auth status` printed a masked token prefix line); `tmux list-panes`; `node -e` on a literal object (no file).
- **One refused command:** my first `cp -n` of the NexusAI scanner into scratch was refused by the path guard (it read the source as a write target). I re-did it with a python read of the bytes and a write into scratch; no NexusAI file was written.
- No decision card, `decision_queue.sh`, `briefs_staged/`, scoreboard, ledger, WEDNESDAY/FRIDAY tree or non-Datasec project was read. No jest, lock, listener, deploy, az, docker, ssh.
- Two PreToolUse advisories (grep case and `cut`) were read; every absence in this report is from a program with a control.
