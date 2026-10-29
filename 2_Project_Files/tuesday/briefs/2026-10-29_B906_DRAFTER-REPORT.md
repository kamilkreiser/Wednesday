STARTABLE: YES (with Q1-Q3 answered by Tuesday at the stamp; none blocks)

# B906 drafter report: SEAT-G205, NexusAI PR #143 (RD-869 / RD-870), TIER 1 gate, round 1 of 2

Drafted 2026-10-29 19:41-19:58 AEDT (clock from `date`). Kit: `/Volumes/Laptop-DEV/TUESDAY/2_Project_Files/tuesday/briefs/2026-10-29_B906_SEAT-G205_nexusai-143-rd869-roster-first-gate-tier1.md` (107 lines, long paragraphs). STATUS path in the kit: `/Volumes/Laptop-DEV/!CODING/Datasec/NexusAI/1_Project_Definition/Briefs/2026-10-29_B906_STATUS.md`.

## BLUF
- Kit is complete in the B892 NexusAI gate shape plus the tier-1 additions of B900 (own mutants, own corpus differential, real server on loopback through the repo harness). Model Opus `claude-opus-5-5` (`models_latest.json` line 17), routing row G1 (`model-routing.md:108`, cap `:111`), launch line carries `BRIEF_SEAT_LEVEL=opus` inside the quotes. Ports 9970-9979, pane `Datasec/NexusAI-G205`.
- PR #143 state at 19:5x: open, not draft, head `747f437b` = branch, merge ref `7620ebac` (parents `be13993a` then `747f437b`, tree `719ff517`, committer 19:51:11 AEDT) over CURRENT main `be13993a` (HISTORY.md only). The `build` check started 19:51:17, after the merge ref, so it judges the merge result. Analyze python and actions success (0 results); javascript-typescript and `build` still running; the CodeQL summary reads `neutral` (not a pass).
- The new reading of the code (not in the builder STATUS): five attack hypotheses the kit hands the gate: (1) PREEMPTION: the head collects all six pattern captures and picks the first ACCEPTED in order, so an earlier candidate that the roster now accepts can beat the later one that won at base (a "different user than before" route); (2) the sibling decides acceptance on `contextData.allLogs` but resolves on a fresh 1000-row read (two windows); (3) all six patterns now ALWAYS run (base stopped at the first valid capture) and `express.json` allows 50mb bodies (CPU); (4) in Azure Log Analytics mode the extra roster read is a workspace query per message, which the builder never measured; (5) the 130 re-indented lines of `server.js` can make CodeQL re-fingerprint OLD main alerts as new on the PR ref, so the kit makes the gate grade each server.js alert "moved" or "new in added code" against main's same-rule alert.
- M4: kit treats an M4-only red (hosted or local) as a base-rate Note with figures and re-runs nothing hosted.

## Facts re-measured (instrument, control)
| Fact | Value | Instrument | Control |
|---|---|---|---|
| main | `be13993a70cf...` | `git ls-remote` under `-C` shared repo | `refs/pull/143/*` printed the head and merge ref in the same call |
| PR #143 head, merge ref | `747f437b`, `7620ebac`; parents be13993a, 747f437b; tree 719ff517; 08:51:11Z | `gh api -X GET pulls/143`, `git/commits/<merge>` | head equals ls-remote value |
| 7e3d37e6..be13993a | status ahead, files `HISTORY.md` only | `compare ... --jq` | n/a |
| PR files | server.js 140/129, rd869 test 302/0, counts 3/3 | `pulls/143/files` | totals +445 -132 equal the pulls/143 fields |
| server.js blobs | base `312c352e...`, head `b6c3be29...` | `git hash-object` on raw `contents?ref=` (Accept raw), saved in scratchpad | base value equals the builder's quoted `312c352e` |
| counts file | main be13993a 5224/310; 7e3d37e6 5224/310 (via be13993a read); PR head 5250/311; #139 head 5223/310 | `contents?ref=` base64 | #139 does not list the file in `pulls/139/files` |
| #139 | open, 1 file `rd407-concurrent-settings-writers.test.js`, base be13993a, unstable | `pulls/139`, `pulls/139/files` | disjoint from #143's three paths |
| checks on head | CodeQL neutral; Analyze python, actions success; Analyze js-ts and build in_progress; scan, audit success | `commits/<sha>/check-runs --paginate` | analyses rows: python, actions at 747f437b, results 0 |
| Build base rate on main | 30 push runs since 10-24: 29 success, 1 failure (run 40834703321, 7e3d37e6) | `actions/workflows/201870215/runs?branch=main&event=push&per_page=30` | the failure is the run the task names; be13993a run 40838546809 success |
| Round count | 92 STATUS files, 31 GATE VERDICT first lines, 3 NO GO (B592, B647, B667), none this class | first-lines loop with `case`; NO GO subset | the known gates printed |
| Deploy switch | variables 0; environments [dev]; deploy-demo.yml blob 597b3487 | `actions/variables`, `environments`, `contents` sha | n/a |
| plumbing hashes | lock tool cf01bafb...971f; fence-preload 55eaafcb...b60 | `shasum -a 256` | equal to the B892 kit values |
| Ports | 9970-9979 no listener (lsof rc 1); unrestricted listing shows `*:7000` | `/usr/sbin/lsof -nP -iTCP:... -sTCP:LISTEN` | `*:7000` appeared |
| Port word-boundary scan | 49 non-`.pre-` SEAT kits of 10-28 and 10-29; one hit for 9970: B879 (closed other-project gate, text is "range scanned"), none live | `python3 -I` regex `(^|[^0-9a-fA-F])99(7[0-9])([^0-9a-fA-F]|$)` | `991x` hit 3 kits |
| G205 name | in no kit; no pane `Datasec/NexusAI-G205`; live panes tuesday, Datasec/HPSM-POC-H55, fleet-monitor; no b906 ref, tree or dir | python scan, `tmux list-panes`, `ls-remote 'refs/heads/b906*'`, `ls -d` | `G203` hit 4 kits; `session-tools/b895` exists |
| Code reading | `acceptUserCapture` 7972, `checkForCurrentUserQuery` 7985 (async), read at 8056, return `rosterLogs` 8071, caller 7268, reuse 7275, sibling 10145 using `contextData.allLogs`, resolver re-read 10161; `express.json` limit 50mb at 1362 | raw head copy, `sed -n`, `/usr/bin/grep -n -i` | the 5-hunk GitHub patch lines agree with these anchors |

## D-decisions made in the kit
- D1: tier 1 attacks in four ways beyond the tier-2 shape: an extractor + differential engine over a bounded-exhaustive corpus (C4), nine own mutants of the product (C5), a read counter / failure path / leak-key census / CPU timing (C6), and a loopback boot of the real server for the sibling (C7) and an answer differential on the gate's own corpus (C9).
- D2: the exposure grading is explicit (G-2): a skip-word capture equal to a roster account being answered with that account is the RULED behaviour and a Note with the list; a collateral user, a group question answered as one account, or a different user than base is Blocker/Major.
- D3: CodeQL "moved line" rule written into C3 and G-3 (an alert at a re-indented line that main also holds is reported, not this PR's).
- D4: M4 rule written once in FACTS, then referenced in C3, C10, G-3 and LANDING 1 (Note with figures; reproduce the cell alone once, local only).
- D5: landing order with #139 is stated as a measured consequence, not a ruling: paths disjoint, #139 moves no count, counts after both 5250/311, the second lander's merge ref and hosted checks rerun (C11).
- D6: hard stop suggested 210 / 300 minutes (opus gate, two installs, nine mutants, two boots, one 23-minute verify, up to 60-minute CodeQL wait).
- D7: no person's name and no decision-card id in the kit (the ruling is cited as "the product owner's 2026-10-29 ruling"); B-numbers appear only as file names / round-count frame / gate ids.

## Q-questions for Tuesday (each with a default)
- Q1: the kit says tier 1, round 1 of 2. Default: confirm ("0 of 2 before, this is round 1 of 2").
- Q2: the earlier in-repo gates on RD-863 ("gate 28/31", cited in `CLARIFICATIONS.md`, not in the B-numbered loop) count only if their NO GO was about which user an answer shows. Default: they do not count (the kit makes it a gate Q-question if a hit looks same-class).
- Q3: port block 9970-9979 despite one hit in the closed B879 kit (a range it scanned, not a claim). Default: keep 9970-9979; the alternative 9980-9989 was not scanned.
- Q4 (info, not a blocker): the gate may start before the hosted Build and the js-ts Analyze finish; the kit makes it wait (60 minutes beyond its last heavy job). Default: launch now.

## UNMEASURED by the drafter
Nothing was cloned, fetched, installed, run or booted. Not measured: any behaviour of the head (the five hypotheses are source readings, not runs); the 10 `server.js` hunks (the GitHub patch shows 5 context-diff hunks; the builder's 10 is `-U0` and RELAYED); the neighbour list of 15 suites; where the RD-864 and RD-871 cells live; blobs of rd856/857/863 (RELAYED from the builder, not re-read); the counts-file blob sha on main (`547eaef8` is the builder's value); main's open `server.js` CodeQL alerts (not counted); what `getAllPrinterLogs` throws and whether that message can carry a connection string; the middleware before `/api/chat` beyond `aiGate.requireAiEnabled` (route line seen, auth not read); Azure Log Analytics mode; the builder's differentials; the hosted `build` log (still running).

## Outside-the-fences disclosure
- Read only: DRAFTER_RULES.md, the B892 and B900 kits, the B895 STATUS, `model-routing.md` (lines 100-115), `models_latest.json` (grep for model ids), `CLARIFICATIONS.md` (grep by text for C-190, gate 28/31, M4, no content beyond cited lines), NexusAI Briefs STATUS first lines and a handful of grep hits (B338, B588, B894, B897 first lines).
- `gh api -X GET` only, under the NexusAI `GH_CONFIG_DIR`; one raw `contents` fetch of `backend/server.js` at base and head into the session scratchpad (`/private/tmp/claude-501/-Volumes-Laptop-DEV-TUESDAY/2f46e3cf-828a-43cc-877d-ab96bd9f9dfd/scratchpad/`: `head_server.js`, `base_server.js`, `server.patch`, `kits.txt`, `err.txt`); `git ls-remote` (read verb, `--no-optional-locks`) in the shared checkout; `lsof`, `tmux list-panes`, `shasum`, `ls -d`, `date`.
- NOT done: no `decision_queue.sh`, no Jira call, no fetch/clone/worktree, no az/ssh/docker, no HTTP to any hosted or demo host, no `cd`, no read of `fleet/briefs_staged/`, `scoreboard.md`, `_ledger.md`, any WEDNESDAY/FRIDAY tree or non-Datasec project. I used `sed -i` once on my own kit and `Write`/`Edit` only for my two files.
- One advisory from the grep-case hook fired (case-sensitive phrase greps); the counts it touched were re-checked case-insensitively. The slot count of the kit is 8 lines with the four-underscore pattern (control in the kit text), at-sign pattern 0, non-ASCII 0, person-name tokens 0.
