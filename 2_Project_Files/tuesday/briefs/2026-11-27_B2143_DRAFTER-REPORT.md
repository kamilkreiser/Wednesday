STARTABLE: YES

# B2143 drafter report: NexusAI lane 3 kit 1 (RD-1016, RD-1015; RD-1014 a Question), seat N184

Kit: `/Volumes/Datasec_DEV/TUESDAY/2_Project_Files/tuesday/briefs/2026-11-27_B2143_SEAT-N184_nexusai-lane3-kit1.md` (181 lines, 78713 bytes), sidecar `...N184_nexusai-lane3-kit1.md.measured` (143 claim lines, `stamp_check.py <kit>` exits 0: "143 claims, 143 measured, 0 not measured"; `grep -c _ _ _ _` on the kit prints 5: four slots and the last line). Drafted by an in-session read-only Sonnet drafter. **No jest, no verify, no playwright was run anywhere** (another seat holds the NexusAI jest lock); every red, green and mutant expectation is PREDICTED for jest and was only run under a 40-line stand-in for jest (plain node, jsdom 20.0.3, `describe`/`test`/`expect` with `toBe` and `toEqual`): marked MEASURED-BY-SHIM in the kit.

## BLUF
- STARTABLE: YES, with three disclosures the stamp should carry: (1) the lane script and its 14 mutation red sets have never run under jest (a judge FAIL under jest is a STOP and the kit says a failure traceable to the kit's own wording is a question to Tuesday, never the seat's to amend); (2) the NexusAI jest lock is held by the live erasure seat (`Datasec/NexusAI-N183`, kit B2142) until its READY: the seat's three acquisitions queue behind it (correct, said in the kit); (3) the counts pair after K is PREDICTED (6530 + 28 = 6558 tests, 411 + 2 = 413 suites): nobody ran the whole suite.
- Scope built: RD-1016 (one `escapeHtml` in `static/js/settings.js`, which escapes a non-string) and RD-1015 part (1) (the eight number cells of four CSV exports, through a new helper beside `csvCell`). Not built: RD-1014 (Q-2), RD-1015 parts (2) and (3) (Q-5). Three product/test files changed, two new test files, one existing test line turned, commits A, B, K on `b2143/lane3-kit1`.
- **One measured surprise that changed the design:** the existing `__tests__/rd835-csv-cells-are-not-formulas.test.js` lifts the export functions with an explicit helper list (`['escapeHtml', 'csvCell']`, line 100), so the moment the exports call any new function five of its cells (X1, X4, X5, X8, K3) read red (`csvNumberCell is not defined`). The kit turns that one list by a frozen program (Q-3) and the lane has a step that proves the need (`a2-835-before-turn-linux`, red exactly X1, X4, X5, X8, K3).
- **One existing defect found, not fixed:** the risk tables write the sheets figure with `toLocaleString()` (index.js 8903, 8953, 9003), so 1000 or more carries a thousands comma, and the anomalies exports write that cell raw: the row gains a column. Kept byte for byte (cell U2 pins it as "as before"); Q-9.

## Facts re-measured (instrument; control)
- BASE `279b22352dbcbd85664534395aeb366fec719a50` = main at 11:21:53 and again at 11:41:25 (`gh api -X GET .../commits/main --jq .sha`); open PRs `[]` and length 0 (`pulls?state=open`); `matching-refs/heads/b2143` 0 (control `heads/records` 58). Compare `e789995a...BASE`: ahead 19, files under `static/` 0.
- Nine blobs by `git hash-object` of the extracted BASE tarball vs `gh api ... contents?ref=BASE --jq .sha`: EQ in all 9 (settings.js `f82ca22d`, index.js `699b89c3`, rd835 test `7b975cd7`, rd861 test `702b2b5e`, rd778 test `3913596c`, counts `1067fa78`, build.yml `1abf0458`, verify-suite.sh `eb9731f5`, jest.config.js `fc1178d4`). The two new test paths answer Not Found (control: the settings.js path prints its blob).
- Tickets by Jira GET (own scratch helper reading `4_Credentials/.env` in process; no value printed; saved under `fleet/state/s333/d2143/jira/`): RD-1016 Low, To Do, 0 comments; RD-1015 Low, To Do, 0 comments; RD-1014 Medium, To Do, 2 comments (41437, 41493). Rulings: `ruled|ruling|decided by|approved by` over each text: 0, 0, 0 (control: `proposal` 1 in RD-1016). C-307 (`CLARIFICATIONS.md` line 3110) says no ruling is cited. **No card id is named in any of the three, so no card was read.**
- Code-scanning open alerts 22, 0 with a primary location in either script (control: `backend/server.js` 13).
- Seat id N184 free (1 file at the first read: the commission; N183 finds 6 files). Slots by the project's `worktreeSlot` (control: `b2133-nodot/run` 3, `mut` 16, `verify` 14 reproduced): `b2143-nodot/run` 7, `mut1` 6, `chk` 17; I renamed `mut` and `verify` to `mut1` and `chk` because the names `mut` and `verify` hash into slots 5 and 10 whose band edges appear in other kits (23200, 23839, 26400, 27039); the six edge ports of the chosen bands appear in 0 of 27 kits (control 22560: 5); `lsof` on the three bands prints nothing (control all listeners 16). Live panes: `tuesday`, `Datasec/OXPd2-X81`, `Datasec/NexusAI-N183`. No B2143 STATUS, no `.tools/b2143`, no `b2143-nodot`.
- Raw-cell census frame (a program over the `.join(',')` arrays of `static/js/index.js` at BASE; elements not starting `esc(` or `csvCell(`): the eight cells on lines 5874, 6124, 5957, 5958, 5977, 6145 plus the code-summed counters (5915, 5939, 6062, 6084), the sample-data writers and a fleet-health loop (named limits).
- Product hunks by program (`apply2143.py`, run on a scratch copy): `apply-1016 settings.js 179931 -> 179925 bytes` (numstat 6 16, blob `07c2d16b`), `apply-1015 index.js 476188 -> 476798 bytes` (14 6, blob `b60cdd12`), `apply-u835 ... 12898 -> 12915 bytes` (1 1, blob `968d6380`); a second apply refuses; the reverts restore the three BASE blobs (`cmp`); `node --check` of both heads rc 0. Sinks move to 1700, 1707, 1714, 1742, 2089 and the live function to line 2430 (grep -n of the head blob).
- No test file contains a removed line: 439 files scanned (`__tests__/*.js` and `tests/**`), 5 distinct removed/changed lines per script, 0 files each; control: the same 5 lines are found in the BASE scripts themselves.
- Shim runs (NOT jest): RD-1016 file 13 cells, BASE 9 red (E1, E2, E3, A1 to A5, O1), 4 green; head 13 of 13. RD-1015 file 15 cells, BASE 12 red (U1 to U3, X1 to X7, C1, C2), 3 green; head 15 of 15. rd835 22 of 22 at BASE and, after the turned line, at the head (control: 5 red before the turn); rd861 20 of 20 both sides; rd778 unreadable by the shim (15 of 17 red on both sides, for the shim's reasons). 14 mutations, red sets in the kit's LANE'S EXPECTED LINES.
- Dry run of `lane2143.sh` with a stand-in `jest.js` (shim -> jest-shaped JSON): 54 judge calls, `judge ... rc=0` 54, other rc 0; 14 `blob after revert` lines each equal to the head blobs. `static2143.py` over a scratch git repository: A, B, K each `STATIC <tag> PASS` (15 OK lines); gitleaks over the staged diff and the whole log: `no leaks found`; planted-key control: `leaks found: 2`. K's counts file in that repository was written by hand to check paths only.
- Cell counts (indented `^[[:space:]]+test\(`, column-1 `^test\(`, `test.each`): RD-1016 file 13, 0, 0; RD-1015 file 15, 0, 0. Selector check: describe and first test of each printed (kit).
- Linux-leg premise scan: `TMPDIR`, `localStorage`, `Date.now`, `toLocale`, `os.tmpdir`, `/tmp`, `process.env`, `chdir`, `listen(`, `spawn`, `execSync`, `mkdtemp` over both frozen test files: 0 each (control `readFileSync` 2 and 3). No cell depends on a platform path or env.

## Chain inputs (rule 4: each input is made by an earlier step or exists at BASE)
| step | inputs | made by |
|---|---|---|
| Step 0 | kit, frozen folder, neigh.txt, report, tickets | exist now (frozen files and neigh.txt read-only in the drafter's scratch) |
| Step 1 / 1b | BASE sha, clone, `npm ci`, scratch BASE copy | origin; step 1 |
| 0 trees | BASE, frozen files | Step 1, Step 0 |
| 1 quiet | lock base listing | exists |
| 2 lane | trees `run`, `mut1`; frozen files; `neigh.txt`; the two new test files (copied from the frozen folder inside the lane) | steps 0, 1; Step 0 |
| 3 commits | lane's verdict; frozen programs and messages | step 2 |
| 4 heads | head of B | step 3 |
| 5 linux-update | tree `chk` at B | step 4 |
| 6 kstep | counts file written in `chk` | step 5 |
| 7 plain | `chk` at K | step 6 |
| 8 cq | K sha, clone | step 6 |
| 9 mainmove-last | BASE | Step 1 |

## D-decisions (the drafter's; Tuesday can overrule)
- D1 The helper is `csvNumberCell`, built on `csvCell`'s own decision (it writes the cell csvCell would prefix; everything else is written exactly as before), so no second regular expression exists and no ordinary export changes by a byte. Refused alternative: `csvCell` for every cell (quotes numbers; turns rd835's X1, X4, X5, X8, K3; also turns `0` into an empty cell because `csvCell` does `(val || '')`).
- D2 The dead first `escapeHtml` is removed and the live second one is fixed (not the reverse): zero behaviour change for any string or scalar the page writes today.
- D3 Tree names `run`, `mut1`, `chk` (slot collision avoidance). D4 Neighbour list = every `__tests__/*.test.js` naming `static/js/settings.js` or `static/js/index.js` that does not boot or listen on a server: 35 files, 2 left to the whole-suite runs. D5 The frozen lane, versions script, judge, static check and messages are adaptations of B2133's (the judge is its copy byte for byte; `v2143.sh` differs by the name in its header).
- D6 No mutation of the "first definition came back" kind: E1 is held by the red-at-BASE itself (2 definitions), not by a mutant (named in the kit as a limit by omission).

## Questions for Tuesday (each with the kit's default)
- Q-1 one kit, two tickets, commits A (RD-1016), B (RD-1015), K: default yes.
- Q-2 RD-1014 in this kit? Default NO: kit 2 of lane 3 after this lands (it needs `escapeAttrValue` in settings.js (0 occurrences now), built on the function RD-1016 changes; its 72 index.js rows share a file with RD-1015's hunk; it has its own scope decision about the first-run error lines).
- Q-3 turn the one lifted-helper list of the RD-835 file (line 100): default yes (measured: five cells red without it).
- Q-4 RD-1015 shape: number cells stay bare unless formula-shaped (default) vs csvCell for all eight (quoted numbers; turns five existing cells).
- Q-5 RD-1015 parts (2) (leading space, look-alikes; needs a real spreadsheet) and (3) (negative amount): default not built; the ticket stays open for them.
- Q-6 `escapeHtml` of 0 and false: default still write nothing (as the live function); alternative prints `0`.
- Q-7 builder Sonnet (row C2, line 92), gate G1 Opus round 1 of 2 (line 108): default as stated; alternative Opus builder.
- Q-8 the seat commits K (the counts commit): default yes. Q-9 the thousands-comma row split of the anomalies exports: default a new ticket, not in this kit.
- Q-10 no Linux container run (the hosted build of Tuesday's PR is the first real Linux measurement): default yes. Q-11 launch timing: default launch now and queue behind N183's jest lock (its hard stop 14:30); alternative hold until N183's READY.

## UNMEASURED
Jest in any form; the lane script and judge on real jest `--json` (the judge is B2133's own file, which ran on real output there); the whole suite and the counts pair (6558 / 413 predicted); `static2143.py` and gitleaks on the real commits; CodeQL at the real head; the clone and `npm ci`; real Linux; a real browser and the dashboard's content security policy; a spreadsheet; the callers of `escapeHtml` in settings.js (35 other sites) were checked by reading the `grep -n` listing only; whether `rd778` stays green (the shim cannot read it).

## Outside the fences (disclosure)
- Wrote only: the kit, its sidecar, this report, and files under `fleet/state/s333/d2143/` (Jira text, a BASE tarball and trees, the frozen folder, shim, scratch git repository, logs, a `_quarantine/` holding two replaced sidecar drafts). A transient `.measured.bak` sat in the briefs folder for one command and was moved to my quarantine; no other stray file. No write to the NexusAI project folder, Jira, GitHub, cards, mail.
- Read-only reads beyond the commission list: the NexusAI `CLAUDE.md`, `CLARIFICATIONS.md`, `.tools/b2095/runlane.sh` and `cq/runcq.sh`, `session-tools/nexusai-lock.sh` header, B2142's and B2139's kits (OWNS blocks), the three NexusAI ticket texts via Jira GET, and B2133's drafter scratch (`fleet/state/s331/d2133/`: frozen judge, `v2133.sh`, `static2133.py`, `names4.txt` read by program and never printed, `node_modules` of the B2032 drafter used read-only for plain node and jsdom). Ran: `gh api -X GET` only (tarball download included) under the NexusAI `GH_CONFIG_DIR`, `tmux list-panes`, `lsof`, plain node, python, gitleaks, `git` in my own scratch repository only.
- Hook refusals during the work (no effect): an `rm -rf` of a scratch folder (refused: never delete), a `git init` through a variable path (refused; redone with the literal path), a typed `cd` (refused, not executed), `=====` words (refused).
- No `decision_queue.sh` call, no `fleet/briefs_staged/`, no scoreboard, no ledger, no WEDNESDAY or FRIDAY tree.

Drafting ended: Fri 27 Nov 2026 11:43:49 AEDT (stamp_check rc 0; kit 181 lines; no jest run).
