STARTABLE: YES

# B774 DRAFTER REPORT: SEAT-R51, NexusAI records for PR #120 and PR #118

Drafted 2026-10-27 02:10-02:3x AEDT by the Tuesday kit drafter (Sonnet). Kit: `/Volumes/Laptop-DEV/TUESDAY/2_Project_Files/tuesday/briefs/2026-10-27_B774_SEAT-R51_nexusai-records-118-120.md` (216 lines; 63 fixed text parts; 9 lines hold the four-underscore pattern, control below). This report is the only other file I wrote.

## BLUF
Startable now. Both landings are as described and read from source: PR #120 merge commit `e553d340a565146c625fa973744d1945cf9a117b` (20:43:13 AEDT 26 Oct) and PR #118 merge commit `f4efe10f184ef99e8e8e8d1a93f29e52e2d4bb5b` (02:07:12 AEDT 27 Oct); main is `f4efe10f`; 0 open PRs; M16 is the only NexusAI seat live. The one thing not yet knowable is the push Build of `f4efe10f` (run 40346171619, `in_progress`, started 02:07:16, expect about 02:53); the kit starts a 75-minute background waiter and gates the RD-867 move on it. One correction to the brief you gave me: B728's "what to read after landing" says the Build pair is 5155/306, but PR #120 landed first, so the pair is now **5162/306** (measured in the `e553d340` Build job log); the kit says so.

## Facts re-measured (instrument, control)
| fact | value | instrument | control |
|---|---|---|---|
| PR #120 | merged true, `merged_at` 2026-10-26T09:43:13Z = 20:43:13 AEDT, head `882705bd...`, merge `e553d340...`, parents `cb8c8b19...` (the B727 records PR #119) and `882705bd...`, 9 files +81 -15, 3 commits | `gh api -X GET pulls/120`, `git/commits/<full sha>`, `pulls/120/files`, `compare/61154bba...882705bd` | `pulls/117` reads a different merge commit (`61154bba`) |
| PR #118 | merged true, `merged_at` 2026-10-26T15:07:12Z = 02:07:12 AEDT, head `610a8759...`, merge `f4efe10f...`, parents `e553d340...` and `610a8759...`, 1 file +30 -1 | same | `compare/e553d340...f4efe10f` ahead 2, one file |
| main | `f4efe10f`, `compare` identical; open PRs 0 | `commits/main`, `pulls?state=open` | closed list 120, 119, 118, 117, 116, 115 |
| push Build `e553d340` | run 40301734292 completed success, attempt 1, 45 min; log: expectation 5162/306, `Test Suites: 306 passed`, `Tests: 5162 passed`, `VERDICT: PASS` | `actions/runs?head_sha=`, job log with `--allow-escape-sequences` | nonsense token counts 0 in the log |
| push Build `f4efe10f` | run 40346171619 `in_progress`, attempt 1, started 15:07:16Z | same | its siblings Gitleaks, npm-audit, Push on main success; Deploy demo skipped |
| Deploy demo | `skipped` on both push runs | same | |
| analyses | 3 per commit (js 132, python 1, actions 0 results) at `f4efe10f`, `e553d340`, `cb8c8b19`, `61154bba`: same counts | `code-scanning/analyses?ref=refs/heads/main` | a count, not by alert number |
| open alerts on main | 133 (52 log-injection), 0 created since 2026-10-25T23:00Z | `code-scanning/alerts?state=open&ref=refs/heads/main` paginated | alert 95 `fixed`; `alerts/0` HTTP 400; 96-99, 116, 219, 222, 223 present |
| PR #118's own Build | run 40245881901 completed success at attempt 3; attempt 2 failed in 5 s (reason unmeasured); attempt 1 is the red one B728 read (unmeasured by me) | `actions/runs/<id>`, `.../attempts/2` | |
| ruling | status ruled, choice a, label "Land all three now; no demo deploy until part 2", ruled_ts 2026-10-26T20:23:37 AEDT | `decision_queue.sh show <exact id>` into a scratch file | |
| code lines | `backend/simpleDb.js:8` `RISK_RUN_MAX_ROWS = 1000`, `:805` the clamp; `backend/logSafe.js:43` the C1 class; `docs/SECURITY_AND_ARCHITECTURE_REVIEW.md:144` the old 10000 (and `:174` another, different function) | raw contents at `f4efe10f` | |
| HISTORY.md | 698274 bytes, blob `66ed6c0d`, 138 headings, last = the B727 entry; `PR #120` 0 hits | contents API | |
| CLARIFICATIONS.md | 2408 lines, 446481 bytes, sha `454b6b66...`, last C-223, last section `## 60.`; next C-224, `## 61.` | file read, `shasum` | `C-190` on 37 lines |
| Jira | RD-885 To Do 0 comments; RD-849 To Do 0; RD-876 To Do 1 (id 40133, the C-219 comment); RD-867 To Do 0; RD-573 To Do 1; RD-873 To Do 3 (M16's) | in-process GET via the project's `b727lib` | nonsense 0; `key = RD-876` 1 |
| duplicate searches | `B750`, `B746`, `B728`, `B713`, `e553d340`, `f4efe10f` all 0; `listen(0` 33, `reservePort` 14, `rows.slice` 11, `parseInt(limit` 2 (RD-876, RD-364) | `project = RD AND ( ... )` | same controls |
| seat name | `Datasec/NexusAI-R51` not in the pane list (live: tuesday, Datasec/Security-Composer-R51, HPSM-POC-G159, NexusAI-M16, MPS-G158, fleet-monitor) | `tmux list-panes -a -F '#{@cockpit_name}'` | M16 listed |
| ports 8680-8689 | `lsof` rc 1; 0 hits of `-w -E '868[0-9]'` in 69 non-`.pre-` SEAT kits of 26 and 27 Oct; neighbours 8640 (M16), 8650, 8660, 8670 | `lsof`, grep | python bind on 8685 showed 2 lines, freed rc 1; the same scan form finds `8640` in B770 (6 hits) |
| model | `claude-sonnet-5-5`, checked 2026-10-27 02:01:26; routing rows C2 `model-routing.md:92`, C7 `:97`; `brief_seat.sh` line 24 defaults to Opus | file reads | launch line carries `BRIEF_SEAT_LEVEL=sonnet` |
| stamp slots | the kit has 9 lines with the four-underscore pattern (8 slots and the last line); at-sign slot pattern 0; no non-ASCII byte in any text part; no backtick, no company name, no person's name in any text part | `/usr/bin/grep -c -E '_''_''_''_'` = 9; Python scan | the pattern finds the slot lines by line number |

The landing rule quoted in the kit: C-190 item 2 at `CLARIFICATIONS.md:2067` ("land the SAME commit. Never squash, never rebase"), C-218 at `:2362`. The ticket-state rule quoted: NexusAI `CLAUDE.md:300` and `:302` ("Code change -> Testing", owner's name elided), JIRA.md `:126-235` for the id 31 / id 51 trap; precedent B727 and B656.

## D-decisions (mine)
- **D1 Division of the records branch: copied from the B727 template exactly.** The seat pushes `records/b774` (HISTORY.md only) and stops at READY; Tuesday opens the PR and lands it through CodeQL as a merge commit. Your note said the seat "lands its own records branch"; the template and DRAFTER_RULES both say the seat pushes and Tuesday opens and lands, so I kept that and said so in the kit. (If you want the seat to open and land the PR, that is a change to the template division and a `gh` write; I did not make it.)
- **D2 Four creates, not five.** FALL (B750-1, the unpinned `|| 100` arm), LA (B750-7, Log Analytics path outside the clamp, a ruling), DOC (stale excerpt at the review document line 144), SIB (sibling host-less stands, from the builder and gate B728). The port-band collision (B728-10) is planned as a comment on **RD-573** (To Do; its description is the jest port band inside Linux's ephemeral range, which is this finding's cause; port 42842 is in that band), not a create. The seat reads RD-573 and rd412 hits at A3 and, if it is not on topic, posts nothing and lists it.
- **D3 Moves.** RD-885, RD-849 to Testing (id 31); RD-867 to Testing only if the `f4efe10f` push Build is `completed success` (a rare flake is not shown gone by a Build that has not finished; and the kit stops the move if the red cell is in `sustainability-logger-live`). RD-876 gets a comment only and stays To Do (the ruling's option text says it stays open). RD-573 comment only.
- **D4 No BACKLOG row.** The template says none; the file was last committed 2026-06-05 and Jira is the live tracker. Gate Minors became tickets.
- **D5 One C-entry (C-224, section 61)**, recording the product owner's 26 Oct ruling and the demo-deploy hold. The rename pairs (C-133 addendum, gate B750-8) go in the HISTORY entry, quoted by program from B746 STATUS `:116-120`.
- **D6 The hold is recorded in four places:** the RD-876 comment, the C-entry, the HISTORY entry, and FOR TUESDAY (so you quote it in any NexusAI deploy brief). I did not give the seat NexusAI `CLAUDE.md` or `HANDOVER-CURRENT.md` (outside the records lane; `HANDOVER-CURRENT.md` is the S36 file of 2026-09-05).
- **D7 Conditional wording by program.** Text parts that depend on facts I cannot know yet use a closed substitution set (`{BUILD120}`, `{BUILD118}`, `{MOVE120}`, `{MOVE867}`, plus the four ticket keys, `{READ-TIME}`, `{N1}`, `{RULING-TIME}`); the `{MOVE...}` forms say "stays To Do" when the Build is not green, so no comment claims a move that did not happen. The "no code-scanning alert was created after the landing" sentence is posted only after the seat re-reads the alerts by number (the baseline of 133 and the empty "since" list are in the kit).
- **D8 Partition.** M16's four test paths, `worktrees/b770-fix`, `session-tools/b770/`, branch `b770/nexusai-873-codeql-tests`, ports 8640-8649, RD-873 and alerts 96-99 and 116 are named NOT YOURS in the records kit; M16's own kit lists `HISTORY.md`, `CLARIFICATIONS.md`, `JIRA.md` and the counts file as not its, so the lanes share no path. The seat asserts at E3 that its diff is `HISTORY.md` alone.

## Q for Tuesday (each with a default)
- **Q1 RULING-TIME slot.** The card carries `ruled_ts` 20:23:37 AEDT. Default: stamp `20:23:37`.
- **Q2 Scope of the creates.** Four tickets, one Lowest (DOC). Default: keep all four; drop DOC if you want fewer writes.
- **Q3 Push Build `f4efe10f` red.** The kit never re-runs it; if it is red in a port-band suite the seat records it (RD-573 family) and does not move RD-867. B728 recommended a same-head re-run of the failed job as Tuesday's act. Default: you re-run once on a red in an unrelated suite, as for PR #118's own Build (which passed on attempt 3).
- **Q4 Launch timing.** Default: launch now; the waiter overlaps Jobs B and C and ends at the Build or 75 minutes.
- **Q5 Ports.** Default: keep 8680-8689 (B773 holds 8670-8679).
- **Q6 R-number.** `R51` is also in use for `Datasec/Security-Composer-R51` (B773, live): the pane names differ, and R50 is likewise used by two projects in the briefs directory, so I kept `Datasec/NexusAI-R51` as you named it. NexusAI's last records seat was R47.

## UNMEASURED
Conclusion of Build 40346171619; attempt 1 of Build 40245881901 and the cause of its attempt 2; the transitions available on RD-885, RD-849, RD-867 (not read); the bodies of every duplicate-search hit beyond summaries (only RD-573's description was read whole); the 9 host-less `.listen(` sites and the `backend/server.js` lines 21133, 21161, 21165 (relayed from the gates); whether the four new tickets already exist under words the searches did not catch; the rates of the RD-867 failure (the builder's, the gate did not re-measure); open alerts by number after the `f4efe10f` Build (the baseline is in the kit).

## Outside-the-fences disclosure
- I imported the project's own `b727lib.py` with `importlib` under `python3 -I` to make Jira GETs (it reads the project `.env` in-process; GET only; no token printed). My first script **printed the RD-876 and RD-873 comment objects whole** to my tool output, which carries a Jira author's name and address; nothing of it was written to any file or into the kit.
- `decision_queue.sh show <exact id>` ran once into `/private/tmp/claude-501/-Volumes-Laptop-DEV-TUESDAY/98188cbc-6bb8-43eb-82fe-bc7cdd63a28e/scratchpad/card120.txt`; I filtered it with a keyword `grep` that included the id prefix. No `list`.
- A brief python bind on 127.0.0.1:8685 as the port control (freed at once); `find` for the location of `decision_queue.sh` under `2_Project_Files`; a read-verb `git --no-optional-locks log` of `BACKLOG.md` on the shared checkout.
- Several greps were case-sensitive multi-word patterns (the hook warned); each returned hits, so none is a false zero, but I did not add a second control to those.
- Scratch files (`jr.py`, `js.py`, `rd573.py`, `alerts.json`, `simpleDb.js`, `logSafe.js`, `secdoc.md`, `kit-copy.md`) are in the session scratchpad only. No Artifact, Docs, mail, chat or publish tool; no `gh` write; no Jira write; no git write; no HTTP to any hosted site (GitHub and Jira APIs only); no `az`, ssh or docker. Only the two named files were written.
