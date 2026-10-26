STARTABLE: YES

# B793 drafter report (SEAT-G166, NexusAI PR #125 gate, tier 2, round 1 of 2)
Drafted 2026-10-27 06:52-06:57 AEDT by a Sonnet kit drafter. Kit: `/Volumes/Laptop-DEV/TUESDAY/2_Project_Files/tuesday/briefs/2026-10-27_B793_SEAT-G166_nexusai-125-887-row-gate-tier2.md` (74 lines, 8 four-underscore lines: 7 slots plus the last line, `grep -c` = 8; at-sign slot tokens 0; non-ASCII bytes 0).

## BLUF
- Startable now. The G166 name and the B793 file were unused. Head, main and PR #125 read exactly as commissioned. One thing differs from the commission's framing: PR #125 already exists and its CodeQL analyses are still running, so Check 7 is built to be read LAST and to cope with "analyses pending".
- The kit re-measures the named defect both ways (M1 under the BASE file green 33 of 33, under the HEAD file red with the three new keys at 101), M2, M3, M4 (default-only, both files), plus per-key mutants that prove each new key is alive, the zero-limit probe (report only), counts, the verify at the head (head tree = GitHub's merge-ref tree, behind 0), and CI/CodeQL last.
- Port block 8780-8789. Pane `Datasec/NexusAI-G166`. Launch line carries `BRIEF_SEAT_LEVEL=sonnet`.

## Facts re-measured (instrument, control)
| Fact | Reading | Instrument | Control |
|---|---|---|---|
| main | `e24f16f5f41203ceb701b3578e80e2a9b1b616f6`, a merge of PR #122 (parents `6e58ddf7`, `4558a53a`) | `git --no-optional-locks ls-remote` (06:52) and `commits/e24f16f5` | `branches/main` agrees |
| branch/PR head | `0980ab451afefbfa0e2911bc1b772ff37a081e29`; `refs/pull/125/head` the same | ls-remote | `refs/heads/b790*` prints one line; `b793*` none |
| delta | ahead 1, behind 0, status `ahead`, one path `__tests__/rd774-risk-sql-templates.test.js` +7 -1; PR 1 commit 1 file, +7 -1 | `compare`, `pulls/125`, `pulls/125/files` (three agree) | `compare e553d340...e24f16f5` answers ahead 8, 7 files (the instrument sees changes) |
| commit | parent `e24f16f5`, tree `7def5bce14f0...`, unverified (unsigned), message read whole, no person name, no card id | `commits/0980ab45` | n/a |
| diff shape | 3 comment lines, 3 keys (`NaN`, `'abc'`, `null`), one `.toEqual` line replaced by itself plus 3 pairs; six old pairs unchanged by eye | `pulls/125` with the diff Accept header, read whole | the gate re-does it by program (kit Check 1) |
| file blobs | head `86262442ca76df52...`; counts `9712206a584fff80...` at BOTH main and head | `contents/<path>?ref=` `.sha` | two shas for one path differ for the test file (`dfc7a448` base vs `86262442` head) |
| merge ref | `refs/pull/125/merge` = `7180d56f`, parents main and head, tree `7def5bce` = the head's tree | `commits/7180d56f` | main's tree is `8f91f4b7`, different |
| clamp | `backend/simpleDb.js:797` `limit = 100`, `:805` `parseInt(limit, 10) \|\| 100` | raw contents at main | n/a (builder's `\|\| 100` count 1 is RELAYED) |
| open PRs | #125 (this) and #124 `records/b788` (HISTORY.md only per the builder; I did not read #124's file list) | `pulls?state=open` | n/a |
| ruleset | `code_scanning`: `alerts_threshold` errors, `security_alerts_threshold` high_or_higher; `required_status_checks` list EMPTY; `non_fast_forward`, `deletion` | `rules/branches/main` | n/a |
| head runs 06:52 | `npm-audit` push success; PR: `Gitleaks Scan` success, `npm-audit` success, `Build` in_progress, `PR #125` dynamic in_progress; check-runs: `CodeQL` neutral, `Analyze (actions)` success, `Analyze (javascript-typescript)` and `Analyze (python)` in_progress | `actions/runs?head_sha=`, `commits/<sha>/check-runs` | pending is not pass (kit says so) |
| PR code scanning 06:52 | analyses for `refs/pull/125/head` = 2; open alerts = 0 | `code-scanning/analyses`, `code-scanning/alerts` | `alerts/0` answers HTTP 400 (instrument answers); the zero is a suspect until the analyses complete (kit says so) |
| main push runs at `e24f16f5` | `Build` success, `Deploy demo` push completed skipped, `Gitleaks Scan` success, `npm-audit` success | `actions/runs?head_sha=` | n/a |
| routing | row G2 at `model-routing.md:109`, G-cap at `:111` | `sed` of lines 105-112 | the table header shows column S55 = Sonnet "1st" for G2 |
| model | `levels.sonnet.model_id` = `claude-sonnet-5-5` at `models_latest.json:23` | grep | n/a |
| ports | 8700-8799 no listener (rc 1); 8780-8789 free; word-boundary scan of the 88 non-`.pre-` SEAT kits of 26-27 Oct: 0 hits in 8780-8789 (hits at 8700, 8709, 8710, 8715, 8719, 8727, 8730, 8739, 8748, 8760, 8765, 8769 and 9640/9641/9649/9680/9681/9689) | `lsof -nP -iTCP:... -sTCP:LISTEN`; python scan | a python listener on 8785 was listed by `lsof -iTCP:8780-8789`, then freed (rc 1); `x 8700 y` matches the scan and `a8700` does not |
| panes | `tuesday`, `Datasec/MPS-M39`, `fleet-monitor`; no `NexusAI-G166` (count 0), no `NexusAI-M18` | `tmux list-panes -a` | `MPS-M39` counts 1 |
| G166/B793 free | no SEAT kit of the two days names G166; no B793 file before this one; highest earlier NexusAI gate suffix G161 (B776), highest of any repo G165 | python scan, `ls` | n/a |
| lock | `nexusai-lock.sh` sha256 `cf01bafb...971f` (equals the builder's and B776's); `queue-jest/` empty (`total 0`); load 5.30 5.12 4.77 | shasum, `ls -la`, `uptime` | n/a |
| landing rule | C-190 `:2062`, merge path `:2067`, never-dismiss `:2068`, wait line `:2073`, C-68 `:665`, C-209 `:2270`; main's last landing is a merge commit (PR #122) | grep of `CLARIFICATIONS.md` with line numbers | positive hits on every id |
| K-mutant shapes | `parseInt(limit,10) \|\| (Number.isNaN(limit) ? 101 : 100)` moves only NaN; `limit === null` moves only null; `'abc'` needs its own equality | a node one-liner (NaN 101, abc 100, null 100; null mutant: null 101, abc 100, NaN 100) | the other inputs stay 100 (a mutant that moved everything would show the wrong row) |

## D-decisions
- D1. Round count and class: "zero NO GO rounds on this branch or PR". Class named `a pinned row that does not turn red under the defect it names, or turns red for another reason`. Source: no earlier gate on PR #125 or `b790/...` exists in `tuesday/briefs` (scan by G166/B793/branch name). Tuesday may rename.
- D2. Added per-key mutants K-NaN, K-abc, K-null and two test mutants (delete the keys under M1 gives green; `defaultAtNull: 99` gives red at that key) to prove no new key is dead. The builder did not run these. M3 is "record what you see" (builder says it errors with `SQLITE_MISMATCH`, not red).
- D3. The head is the tree Tuesday lands (`behind 0`; GitHub merge ref tree equals the head tree), so the verify runs at the head itself and the gate's own `merge --no-ff` in its clone is a recorded "Already up to date" check, not a combined-tree build. No `merge-tree --write-tree` anywhere (fence 3).
- D4. CodeQL and CI are read LAST (Check 7), with the PR's alert read tied to completion of every `Analyze (<language>)` run. If the analyses are still pending at the verdict, the best token is GO WITH FINDINGS naming "CodeQL PENDING at <time>"; the landing hold tells Tuesday to re-read before the merge. I did not make a pending analysis a NO GO.
- D5. Zero limit: the gate probes `0` and reports, never pins; reported as a question for the product owner (the accepted D-ZERO). The probe is jest-free; the kit says to say whether it used a lock ticket.
- D6. Verify ticket cap 45 minutes (builder: 1441 s), other tickets 20 minutes. The B776 kit's Q-2 form, which Tuesday ruled YES; the S4 slot asks Tuesday to rule again.
- D7. Intersection set B includes #124 (`HISTORY.md`); expected empty with the one test path.
- D8. The Jira helper is mentioned only as optional, in-process, read-only (the builder used `b774lib.py`); no Jira call is required by any check. No race-script re-run (it was struck on B776 and is irrelevant here).
- D9. Port block 8780-8789 chosen because 8700-8709 (the block of the previous gate) is named in 17 hits across today's kits. Kit text and the 8780 scan agree.

## Q-questions for Tuesday (each with a default)
- Q1. The class name on the verdict line (D1). Default: as written.
- Q2. The ruleset has an empty `required_status_checks` list and `mergeable_state` reads `blocked`; the drafter's guess is pending CodeQL under the code-scanning rule. Default: the gate quotes both and Tuesday does not rely on the guess; the landing waits for every `Analyze (<language>)` run to COMPLETE regardless.
- Q3. Whether to hold the launch until `Analyze (javascript-typescript)`, `Analyze (python)` and `Build` complete (they finish while the gate does Checks 1-6). Default: launch now; Check 7 reads last.
- Q4. Verify ticket 45 minutes (D6). Default: YES.
- Q5. The zero-limit question for the product owner and whether to file a ticket. Default: the gate reports, Tuesday files after the verdict.

## UNMEASURED
- Everything the gate measures: the mutants, the verify, titles, the probe, `node --check`, the sentence classes, #124's file list (RELAYED from the builder), `parseInt` behaviours under node 26 and 24 (K-mutant shapes were checked on this machine's node only).
- CodeQL result on the head (pending), the PR's `Build` conclusion (in progress), the Linux runner/node 24, the em dash context line being absent from added lines (read by eye from the diff, the gate re-does it by program), and whether `mergeable_state` `blocked` is the CodeQL rule or something else.
- The kit's line-count and number claims for the builder STATUS ("250 lines", "lines 194-215") come from the file as read in this session; the STATUS may have grown since.
- I did not run a pre-stamp copy; Tuesday copies to `.pre-stamp` per habit.

## Outside-the-fences disclosure
- Read: DRAFTER_RULES, the B776 template kit, the B790 kit and STATUS, `model-routing.md` lines 105-112, `models_latest.json` (grep), `brief_seat.sh` (grep), `CLARIFICATIONS.md` (grep with line numbers), the project lock script hash, raw `backend/simpleDb.js` at main (lines 797-806), `contents/<path>` shas, GitHub GETs (`pulls`, `compare`, `commits`, `check-runs`, `actions/runs`, `code-scanning` analyses and alerts, `rules/branches/main`) all `-X GET` under the NexusAI `GH_CONFIG_DIR`. One call in the batch of GETs near the end printed `gh: This API operation needs the "admin:repo_hook" scope`; stderr order hid which call it was (every value I use printed). The NexusAI token lacks that scope: if a gate call hits it, that is the boundary working, report it and do not widen anything. I did not read `fleet/briefs_staged`, the scoreboard, `_ledger.md`, any decision queue, any WEDNESDAY/FRIDAY tree, any other project.
- Wrote only the two files named. One loopback listener on 127.0.0.1:8785 (python, 4 seconds) as the port control, freed; one node one-liner with no file or network. No Artifact, Docs, mail, chat, Jira, git write, clone, fetch, az, ssh, docker, npm or jest.
- Typed the builder's brief number (B790) and PR/ticket numbers in the kit; no person's name and no decision-card id appear in the kit text.
