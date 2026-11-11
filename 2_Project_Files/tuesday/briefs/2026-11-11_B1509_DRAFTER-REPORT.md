STARTABLE: YES (after the Stamp; two decisions first: the seat id collision Q-1 and the second ruling's clock Q-2, both with a default that is safe)

# B1509 drafter report (kit: `2026-11-11_B1509_SEAT-R213_composer-records-124-and-route-b-lines.md`, 128 lines, 16 four-underscore lines: fifteen slots and the last line)

## BLUF
- Kit drafted on B1499's shape (R212) with B1486's standing rules. Writes: 5 comments, up to 5 moves to Done (PCOMP-21, 77, 15, 26, 27, each on its own slot), 1 new Task (label `plan-comp-479`), 3 C-entries (E1 = Composer PR #123 lane C, E2 = the Route B ruling and PR #124, E3 = PCOMP-77/15), 5 BACKLOG sentences plus one new row #479, one JIRA.md bullet, one history entry, one commit, one fold.
- **Two facts differ from the commission.** (1) The decision store's `ruled_ts` for the second card ("Singular for one, accept the speed") is **17:18:38 AEDT**, not 16:31 (the first, "Write the two-step way back", is 16:31:37). The B1506 kit and the builder's STATUS call both "16:31". The kit carries slot RULING-77-CLOCK (default 17:18:38). (2) **`R213` is already used** by B1500 (the NexusAI records kit) and mentioned in B1501; `R215` is free (Q-1).
- Every Jira text passed R209's scanner with 0 hits in 7 families and 21 controls firing; the builder's proposed texts could not be used as written (they hold "product owner", a branch name, short shas of unsquashed commits, the word "secret"), so they were rewritten from the rulings and the squash facts.
- The root repo has **no remote**, so there is no PR to open for the records branch; the kit follows B1499 (`records/b1509` -> `merge --no-ff` into root main under slot REC-MERGE). Said once here, as the commission asked "PR'd for Tuesday" (Q-5).
- Nothing was written outside the kit, this report and my work folder.

## Facts re-read at source (instrument, time AEDT; `date` printed 17:45:23, 17:45:34, 17:45:54, 17:46:22, 17:47:33, 17:49:23, 17:52:00, 17:52:30, 17:52:42)
| Fact | Instrument | Result | Control |
|---|---|---|---|
| PR #124 merged, squash `879facda441e4f7abccec51583916804f7770789`, `merged_at` 06:36:14Z (17:36:14), head `9d97328c`, one parent `5ad366c0`, tree `8a545518...` = tree of `git/commits/9d97328c` | `gh api -X GET` `pulls/124`, `commits/879facda`, `git/commits/9d97328c` (project `GH_CONFIG_DIR`) | all as the commission says | `pulls/9999` HTTP 404 |
| Files of #124: `DEPLOY.md` +117 -12, `Controls.tsx` +8 -1, web DOM test +3 -2, `b778` +316 -0 | `commits/879facda` `.files` | equal to the gate's list | |
| PR #123 merged, squash `5ad366c0074fefa0643d7b2eb0414d14e6ebf4a7` 05:26:02Z (16:26:02), head `311c69a1`, squash tree `f8d255d7` = head tree; commits `fbbbdf15`, `c5e77d10`, `311c69a1` | `pulls/123`, `pulls/123/commits`, `git/commits/*` | as stated | |
| PR #122 merged, squash `b14467e2...`, 04:07:19Z (15:07:19) | `pulls/122` | merged true | |
| Open PRs #91, #86, #85; newest PR is #124 | `pulls?state=all&per_page=6`, `pulls?state=open` | as stated | |
| Raw `DEPLOY.md` at `879facda`: 758 lines, sha256 `c76924a5177d...b65`; the lines the kit cites (20, 57, 85, 95, 169, 354-360, 372, 401-403, 626-627, 673-674, 687; headings 128, 191, 324, 374, 415, 494, 583, 643, 691) | `gh api ... contents ... Accept: raw`, `/usr/bin/grep -n -i -E 'route b|unmeasured'`, `awk NR==n` | all as the gate and the builder list; `- **roll forward** are as above` count 1 (line 169) | `- **Roll forward**` count 7 |
| 0020 section holds the drop line once, 0021 section 0 | `awk NR` range + `grep -c -F` | 1 and 0 | whole file 1 |
| `Controls.tsx:603` singular, `:604` plural template; label `Mark all secret fields local` at `:524` | raw copy, `grep -n` | as stated | |
| `scripts/ci.sh:112,113` the two new steps; `stack-diagnostics.sh` 3 mentions of the hint function (13 comment, 33 definition, 63 call); `up.sh:15`; both new test scripts exist (113 and 252 lines) | raw copies | as stated | `no-such-test.sh` 0 |
| Jira, the five keys: Backlog, 0 comments, 0 changelog entries, transition `41` -> Done, labels `composer-seed-1023` + `plan-comp-<row>`; `PCOMP-21` has parent PCOMP-2, the others none | python `-I`, `search`-free issue/comment/transition/changelog GETs via R209's `jira_lib` (token never printed) | as the kit says | `PCOMP-9999` 404 |
| Project counts: 127 issues, 42 Done, `held` 19, seed 94, Backlog 85; `labels = "plan-comp-479"` 0 | paginated `search/jql`, every JQL `project = PCOMP AND ( ... )` | as stated | `plan-comp-434` 1 |
| Duplicate search for the Task | `text ~ "Route B" AND status != Done` (PCOMP-9, 21, 25, 93), `summary ~ "DEPLOY.md" AND status != Done` (10, 21), `text ~ "UNMEASURED"` (7 keys), `text ~ "roll forward"` 0 | no duplicate | `text ~ "zzqxvbw"` 0, `UNMEASURED` 7 |
| Root repo: HEAD = main = `e62188105fe3913318b4f6a6bf6d7688ea5dd1b7` (B1499 fold), no remote, record files clean, no `records/b1509`, no `.tools/b1509`; CLARIFICATIONS 2,706 lines, highest `### C-142` at `:2692`, `### C-143` 0; JIRA.md 54 lines, `- B1499` at `:54`; BACKLOG 474 lines, 468 rows, highest #478; history 2,185 lines; BACKLOG rows #104/:108, #169/:163, #291/:287, #323/:319, #324/:320 each end ` |` | `git --no-optional-locks rev-parse/remote/status/log/config`, `grep -c`, `awk`, `wc -l` | as stated | `### C-142` 1, `- B1499` 1 |
| Not yet recorded anywhere: `PR #123`, `5ad366c0`, `B1504`, `PR #124`, `879facda`, `B1506`, `PR #122`, `b14467e2`, `B1495`: 0 in CLARIFICATIONS, JIRA.md, BACKLOG, history; `PCOMP-26/27/21/15` 0 in CLARIFICATIONS | `/usr/bin/grep -c -i -F` | the lane C landing (#123) is owed | `lane C` 8, `PCOMP-77` 7, `PR #121` 7 |
| Panes: no `Security-Composer-*` pane | `tmux list-panes -a -F` | 0 | |
| The two cards: both `status: ruled`, choice a, delivered with #124 / `879facda` | `decision_queue.sh show <exact id>` into my scratch, read through id filter | clocks 16:31:37 and 17:18:38 | |
| Gate B1506: line 1 `GATE B1506: GO WITH FINDINGS @ 9d97328 on main 5ad366c`, one Minor F1; `15 red` appears 3 times, the singular row sentence once | read whole, `grep -o -F | wc -l` | as stated | |
| B1495 STATUS has `9 extra queries`, `about 1.3 ms of 3.1 ms`, `about 10.1 ms of 12.6 ms` once each | `grep -c -F` | 1 each | |
| Seat id scan: `R213` in 4 files (B1500 kit + report, B1501 kit + report), `R215`/`R216`/`R217` 0 | word scan of the 221 non-`.pre-` `.md` briefs of 2026-11-10/11 | collision | `R212` 6 files |

## D-decisions (mine, with the reason)
- **D-1 Texts rewritten.** B1506 STATUS `FOR THE RECORDS SEAT` proposes texts holding "the product owner's ruling", a backticked branch name, the unsquashed commit shas `4a9c963` and `14b0ee2`, the phrase "secret field" and a "Close when the PR lands". None passes the text rule (product owner, backtick, `composer-...-` branch name, "secret"). I wrote TEXT-21/77/15 from the rulings and the squash facts instead, and cite the squash `879facda` (the shas of the branch commits are not on main).
- **D-2 PCOMP-15 numbers.** The builder wrote "about 1 ms ... 10 ms"; B1495 STATUS `:9` says about 1.3 ms of 3.1 ms (fixture) and 10.1 ms of 12.6 ms (50 groups, 2002 answers), 9 queries (the ticket says 8; the extra one is the version read, `:77`). TEXT-15 uses the measured figures.
- **D-3 Held-key rule.** The texts say "moved to Done"; so a key whose slot reads `COMMENT-ONLY` gets NO write (it HOLDS), instead of B1499's comment-only with a text that would then be false.
- **D-4 PCOMP-26/27 Done-when.** The tickets carry no Done-when (descriptions say `State: OPEN`). The only statement is B1504 STATUS `:64`/`:65` ("PROPOSED Done-when ... the records seat carries it"). The kit uses it, checked at main by program (`ci.sh` step lines, the two scripts at 200, the hint function counts). Separate slots MOVE-26 and MOVE-27 because PCOMP-27 has a recorded unruled edge (an empty root-owned volume prints no hint; gate Minor 3), which the text names.
- **D-5 PCOMP-26's registry facts** (resolves for amd64/arm64, an all-zero control did not resolve) are RELAYED from B1504 STATUS `:27`; the seat cannot re-measure them (no registry, no docker). TEXT-26 states them as "was checked", which is true of the lane's own evidence.
- **D-6 New Task = Task type, label `plan-comp-479` only, no parent,** after the seed-time rule (labels `plan-comp-<row>`, seed marker not applied) and PCOMP-116's shape; a BACKLOG row #479 is added only if the create read back (ROW-FORM `APPEND`). The description is 7 ADF paragraphs; its line numbers come from the raw file at `879facda` and the gate's re-print (`VERDICT.md:55`); the kit has THE LINE CHECK for the seat to re-print them.
- **D-7 Order of C-entries:** E1 (#123, 16:26) before E2 (#124 part 1, 16:31 ruling) before E3 (second ruling). E1 claims no product-owner ruling (authority: the coordinator's landing after the gate, plus the coordinator's ANSWER-1 allowing the measured-fact sentence).
- **D-8 Hard stop 21:30 AEDT, READY target 90 minutes after Step 0** (B1499 had 60; this pass has a create, two more keys and three entries). Sonnet, level inside the quotes, no ports, work folder `.tools/b1509/`.
- **D-9** Control strings in the kit say `_by_<a ban-list name>_`, never a real name (the first draft held two first names in the control list; the kit's name scan found 2 and both were removed).

## Q-questions for Tuesday (each with a default)
- **Q-1 Seat id.** `R213` collides with B1500's NexusAI kit; the commission named `R213`. Default: keep `R213` as ordered (the pane name `Datasec/Security-Composer-R213` is unique and the REFUSE check is per name). If you want the shared counter kept clean: `R215` is free; replace it in the kit text and the file name before the Stamp.
- **Q-2 The second ruling's clock.** Store `ruled_ts` 17:18:38; the B1506 kit and builder call it 16:31. Default: slot RULING-77-CLOCK = 17:18:38 AEDT (what the store prints). If 16:31 is right, the builder's W-77 words (taken at 16:44 on a "16:31" ruling) predate the store row and the store needs correcting, not the kit.
- **Q-3 The "Nothing pins Route B's command." lines** at `DEPLOY.md:372` (0022), `:413` (0023), `:641` (0026), `:689` (0027) are not on the B1506/gate list and are NOT in the new Task. Their truth was not checked by me. Default: leave out (the Task is exactly the gate's list plus F1). Adding them is one more sentence in TICKET-DESC-6; say so and I will not.
- **Q-4 PR #122 (PCOMP-77's action) has no landing record** either (0 hits for `PR #122`, `b14467e2`, `B1495` in the four record files). The kit names #122 as a fact inside E3 and TEXT-77 but writes no entry of its own. Default: no separate entry; a later records pass if you want one.
- **Q-5 "PR'd for Tuesday to land".** The root records repo has no remote (`remote -v` 0 lines), so there is nothing to PR. Default: B1499's mechanics (commit on `records/b1509`, `merge --no-ff` into root main under slot REC-MERGE, `MERGE` recommended); HOLD leaves the branch for you.
- **Q-6 PCOMP-27 close** with the edge unruled. Default in the kit: slot MOVE-27 is yours; I recommend CLOSE-IF-CHECKED because the Done-when as the lane stated it is met and the text names the edge.

## UNMEASURED (the kit says how the seat measures it, or that it cannot)
- The 0022 section's own two-step form (builder part M22 was not run; no one has run it). The Task records this; the seat does not measure it (no docker).
- Anything on the demo machine, `gawk`, `npm run build`, the whole `workspace` project (2014 rows) at the squash: the gate did not run them (VERDICT `NOT RUN`), the kit says so in TEXT-21 only for the demo machine and gawk.
- PCOMP-26's registry read and the facts of the B1504 Part 21b table (0022/0024/0025 refuse, 0023/0026/0027 restore) are RELAYED; one fixture, so a restore is one data shape.
- Whether the Jira workflow sets `resolution` on the move for these five keys: B1499 observed it for four keys; unmeasured for these five until the read-back.
- The `.pre-stamp` count (16) is the count of the kit as written: I counted 16 lines with `_{4}` in my copy (fifteen slots plus the last line); Tuesday's own `.pre-stamp` copy must read the same.
- No dry run of the create call was possible (not written; the kit tells the seat to write the create function behind the same guard, with a planted `HPSM` create and a planted second-label create as controls).

## Outside-the-fences disclosure
- Files written: the kit, this report, and in my work folder `/Volumes/Datasec_DEV/TUESDAY/2_Project_Files/fleet/state/s268/draft1509/` (`jget.py`, `jsearch.py`, `jcount.py`, `texts.py`, `texts2.py`, `payloads.json`, Jira JSON copies, the two card dumps and raw copies of seven code files under `main/`). Nothing else.
- Jira: GET only (issues, comments, transitions, changelog, `search/jql`); I imported R209's `jira_lib.py` read-only (it reads the project `.env` in-process; no token was printed). My first broad listing printed 100 issue summaries (read only; no content used except the keys listed above).
- GitHub: `gh api -X GET` only under the project `GH_CONFIG_DIR`.
- `decision_queue.sh show <exact id>` twice (the two exact ids), output to my scratch; I did not run `list`.
- One Bash call that began with `cd /tmp` was refused by the no-cd hook before it ran; nothing was executed.
- The rules file points its examples at `/Volumes/Laptop-DEV/...`; this machine's paths are `/Volumes/Datasec_DEV/...` (the same layout) and all my reads used those.
- No `git` write, no docker, no az, no ssh, no hosted host, no mail, no chat, no Artifact or Docs tool.
