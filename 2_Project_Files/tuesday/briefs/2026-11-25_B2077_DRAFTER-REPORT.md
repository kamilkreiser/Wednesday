STARTABLE: YES

# B2077 DRAFTER REPORT: NexusAI lane NX-W2 (RD-1039), kit `2026-11-25_B2077_SEAT-N174_nexusai-nxw2-rd1039-status-text.md`

Drafter: an Agent-tool drafter for Tuesday (s326), commission `2026-11-25_B2077_NEXUSAI-NXW2-RD1039_DRAFTER_COMMISSION.md`. Read window: Wed 25 Nov 2026 from 08:51:23 AEDT (first `date`) to the `date` on the last line of this report. Scratch: `/Volumes/Datasec_DEV/TUESDAY/2_Project_Files/fleet/state/s326/d2077/`. Files written outside scratch: this report, the kit and the kit's `.measured` sidecar.

## SUMMARY (10 lines)
1. STARTABLE: YES, provided the STAMP accepts **Q-1** (two existing test files join the partition: a ticket row of this lane makes one existing cell red by design and breaks another's harness). Seat id N174 is free (a word scan of 32 non-`.pre-` SEAT kits of 24 and 25 Nov finds it in 0 files; controls N173 in 1, N172 in 1).
2. **BASE moved while I drafted:** origin main is `40df8493` (the merge of PR 253, NX-S2), not the commission's `4d8713e5`. The move touched `backend/server.js`, two new tests and the counts only; none of this lane's paths. I re-ran the whole chain on a scratch merge whose tree equals `40df8493`'s. Counts at BASE 6341 / 400; this lane adds 67 tests and 2 suites.
3. **The kit builds all of RD-1039:** 10 rows (5 in `static/js/index.js`, 5 in `static/js/first-run-setup.js`) written through the script's own `escapeHtml`, and the lookup at `azureOpenAIAdapter.js:307` reading `Object.hasOwn(executors, name)`. 15 lines added, 14 removed, ASCII. Every ticket line number is exact at BASE.
4. **Q-1 finding (the run's surprise):** the union green run (121 suites that read the changed files) read 2 failed of 2142 with only the product edits: `rd1008-endpoint-error-code-is-not-trusted` C4 pins the two status writes as raw (`statusWritesLeft: 2`; they are rows 3466 and 3478 of this ticket) and `rd395-ai-disabled-ui` UI2b lifts `askAIAssistantStreaming` without `escapeHtml`. The kit edits three lines in those two files; without Q-1 the lane cannot go green.
5. **Cells:** 67 in two new files (jsdom chat/setup file 44, adapter file 23). Red-first 38 failed / 29 passed; edited 67 of 67; red-proof (edits reverted) the same 38; green set 2142 of 2142 in 123 suites. `lane2077.sh` ran end to end twice (each base): all rc lines, three `JUDGE ... PASS`.
6. **Real browser proof (drafter's, not a cell):** headless Chromium, the 10 shipped statements x 6 values: BASE 19 elements with an `on*` attribute and a handler ran; edited 0 and 0.
7. **Full verify** at the prototype A: `VERDICT: PASS`, 6408 of 6408 tests across 402 suites, `EADDRINUSE` 0, 09:53:00 to 10:15:58 (23 min, load 3.1 to 3.5); the counts file went 6341 / 400 to 6408 / 402 (+67, +2, PREDICTED exactly). **K must carry 6408 / 402 at `40df8493`.** Local CodeQL at A and at K: rc 0 each, 29/29, KEPT 0, NEW 0, GONE 0.
8. **Two ticket premises are wrong at BASE (Q-5):** the setup script's escape already escapes both quotes (it is the attribute form), and `toString` does not throw (it returns `[object Undefined]`; `constructor` returns the model's arguments; 11 of 12 `Object.prototype` names fire the tool_call event, `__proto__` does not).
9. **27 unlisted rows have the same defect** (index.js 3044, 3750; first-run-setup.js 25 lines including 1502, three lines under a row this lane fixes): findings, Q-4 default report not build. NX-X (RD-1014) drop list is in the kit: first-run lines 1468, 1471, 1486, 4127, 4240 and the five chat lines.
10. Model: row C2 (Sonnet, line 92), gate G2 (line 109), Q-2; nothing deploys, a merge starts a skipped-by-variable `Deploy demo` run (Q-7). **Sequencing:** seat N173 (RD-1040) is live (pane `Datasec/NexusAI-N173`, STATUS `WORKING: B2076 plain (waiting for the lock, then the verify)` at 10:18) and held the jest lock while I ran; the kit's REFUSE 4(a) makes N173's `READY` a precondition, and its counts landing moves K's pair by +21 tests and +1 suite (HOLD 20).

## BLUF
Buildable now, one seat. Ten value writes get the script's own escape, one lookup line gets `Object.hasOwn`. The only wrinkle is two existing test cells that the ticket's own rows turn red or break; the kit includes the three-line fix for them and asks Tuesday to accept the wider partition (Q-1). The kit is dry-run end to end at the real BASE tree.

## FACTS RE-MEASURED (instrument; control)
- **origin main:** `gh api -X GET .../git/ref/heads/main` read `4d8713e5` at 08:51:41 and `40df8493` at 09:19:25 (merge of PR 253, tree `3bf46f17`, parents `4d8713e5` and `9d4ddb7f`, committed 2026-11-24T21:55:12Z). `compare/4d8713e5...40df8493`: ahead 3, behind 0, files `rd1017-...test.js`, `rd975-...test.js`, `backend/server.js`, `scripts/verify-expected-counts.json`. Counts at BASE 6341 / 400 (contents API, base64). Control: the five edited files' blobs read by `git rev-parse` are equal at `4d8713e5` and in the scratch merge, whose tree sha equals origin's.
- **Open PRs / refs:** 253 only at 08:51, 0 at 09:19; `matching-refs/heads/b2077` 0 (control `b2074` 1); `b2076` 0.
- **Jira GET** (`jwhole.py`, GET-only reader of the project `.env` in-process, nothing printed): RD-1039 To Do, Task, 5154 characters, 0 comments, created 2026-11-24T18:43:40+11:00, labels `records-pass-1124,security`; RD-1026 (Testing, 1 comment) and RD-1014 (To Do, 1 comment) read for the overlap. The three quoted ticket passages in the kit are substrings of the dump (a program printed True x3).
- **Every listed line is exact at BASE:** index.js 3466, 3470, 3474, 3478, 3569; first-run-setup.js 1468, 1471, 1486, 4127, 4240; adapter 307 (`apply2077.py` anchors printed by program). Both `escapeHtml` definitions, the csp-helpers delegate (line 70) and the server writers (7730, 7767, 7777, 7825, 7950 to 7953, 9985, 9993) printed by `awk NR==n` / `grep -n -F` at BASE.
- **Inherited-name run:** the real adapter with a scripted client for every own name of `Object.prototype` (12): 11 fire the event, `__proto__` does not; results as in finding 3 of the kit (`raw/inh.out`).
- **Deploy workflow:** lines 26, 29 to 32, 53, 91, 95 as quoted; last 20 runs of workflow 333076536 all `skipped`. Code scanning: 22 open, 13 at `backend/server.js`, 0 at the three product files.
- **Model routing:** C2 line 92, C3 line 93, G1 108, G2 109; `models_latest.json` line 23 `claude-sonnet-5-5`. Landing rule C-190 (`awk NR==2067`) holds "Never squash, never rebase".
- **Slots** (`slot.py`; controls `b2074-nodot/rf` 7, `b2076-nodot/rf` 16): `b2077-nodot/rf` 17, `work` 17, `vupd` 16, `chk` 5; `lsof` 0 listeners in the three bands (control 21 machine-wide). **Port scan** of non-`.pre-` SEAT kits: this lane binds no port; N173 (B2076) uses band 30240-30879 for its `rf` (slot 16), which equals this lane's `vupd` slot: sequential seats, named in the kit.
- **Lock base:** at 09:08 `b2076-lane` held it (my first acquisition waited 10 s); 09:20 to about 09:43 `b2076-verify-update` held it (my lane acquisition waited behind it, FIFO position 1). Panes at 08:55: `tuesday` only.
- **Browser proof** (finding 9): Playwright 1.62.1 from the B2042 drafter's `node_modules`, `about:blank`, no network: BASE 279 elements, 19 with `on*`, `window.ran` 1; edited 252, 0, 0. **Census** (finding 10): BASE 6 + 28 lines, edited 2 + 25 (control: 3 planted lines fire, a wrapped line does not).
- **Jest:** union of 121 suites (84 by `git grep -l -i -E` over eleven names, 58 by `readdirSync|glob` with `static`; the union is identical at both bases). Red-first, edited, red-proof and the judge controls as in the kit's HOW IT WAS DRY-RUN.
- **Full verify:** `npm run verify -- --maxWorkers=2 --update-counts` at the prototype A `914000d3` inside the lock: `Test Suites: 402 passed`, `Tests: 6408 passed`, `VERDICT: PASS`, jest exit 0, `EADDRINUSE` 0 (control: 1 `VERDICT` line), counts file changed in `_updated`, `tests`, `suites` only. Prototype K `d776fca4`: `STATIC K PASS` (13 OK), gitleaks clean, one path. CodeQL at A and at K both rc 0 (29/29, KEPT 0, NEW 0, GONE 0). **The plain verify at K was not run (PREDICTED equal).**
- **Static / leaks / names:** `static2077.py A` `STATIC A PASS` (28 OK lines; it caught three literal emoji in my first test file, a real fire); gitleaks `no leaks found` (control `leaks found: 2`); `node --check` rc 0 on the seven paths of A; name scan 0 on kit, messages, tests and scripts (control 1); kit card-id scan 0.
- **`stamp_check.py <kit>`:** 162 claims, 162 measured, rc 0 (the sidecar lines are real greps over the cited files or live read-only commands; where a literal is only a command or a placeholder the line says so). The four-underscore count in the kit is 5 (four slots and the last line).

## D-DECISIONS (the drafter's, overrulable)
- **D-1:** the escape per row is the script's own `escapeHtml` (the chat page's DOM escape for chat rows; the setup script's, which also covers quotes, for the table attribute). No new helper, no `textContent` rewrite (the minimal change, the RD-1026 form).
- **D-2:** two existing test files edited by `apply2077.py` (3 lines), counted in the revert so the red-proof is a full BASE.
- **D-3:** the judge's green set is the 121-suite union (the rule: every job whose tests read the changed files), not only suites that name the three files.
- **D-4:** the plain verify at K was not run (UNMEASURED, PREDICTED equal to the update run; saves 23 minutes of the shared lock); the K static check and CodeQL were run on the prototype K.
- **D-5:** the optional Chromium proof and census are frozen but not steps (Playwright is not in the seat's tree).
- **D-6:** a missing or null value now shows nothing instead of the words `undefined` or `null` (a stated change, cells N1 and N2).

## Q-QUESTIONS FOR TUESDAY (each with a default)
- **Q-0** (the escape per row, D-1). Default: accept.
- **Q-1** (partition widening: `rd1008-endpoint-error-code-is-not-trusted.test.js` lines 96 and 99, `rd395-ai-disabled-ui.test.js` line 139). Default: **include** (REFUSE 1 stops the seat if the STAMP does not accept it). Alternative: drop the chat rows 3466 and 3478 and the catch row 3569 from this lane (no existing cell red) and leave them to a lane that owns those two cells; I do not recommend it, the ticket lists them.
- **Q-2** (model). Default: **Sonnet builder, row C2 (line 92); G2 gate (line 109)**. G1 (line 108) if the seat widens past the listed rows; note the lookup guard sits on a tool-dispatch surface, a G1 reviewer would not be wrong.
- **Q-3** (the stated change of a missing or null value, D-6). Default: accept. Alternative: `escapeHtml(String(x))` to keep the old words (not recommended).
- **Q-4** (the 27 unlisted rows, above all first-run-setup.js 1502). Default: **report, do not build** (the commission's default); the records pass should add them to RD-1014's list.
- **Q-5** (ticket premises: the attribute form exists; `toString` does not throw). Default: the records pass corrects RD-1039's text; no build effect.
- **Q-6** (a real browser in a cell). Default: no cell; the drafter's Chromium proof stands as evidence, the review may re-run it.
- **Q-7** (deploy). Default: nothing deploys; the `Deploy demo` read at landing is Tuesday's (C-224 hold stands).

## UNMEASURED
The seat's clone and `npm ci`; the plain verify at K (PREDICTED equal to the update run); K's static check on a real K; the push; a hosted instance and its CSP; a real AI endpoint; the origin of a table name; Linux; the 27 unlisted rows; the real Playwright run in the seat's tree.

## CHAIN INPUTS (measured-literal rule 4: each input is made by an earlier step or exists at BASE)
| step | inputs | made by / exists |
|---|---|---|
| Step 0 | kit, frozen files, report, Jira | exist (this folder; Jira GET) |
| Step 1 | clone, BASE, node_modules | `git clone` of the project checkout, `npm ci` |
| 0 `trees` | BASE, frozen files | Step 1, Step 0 |
| 1 `quiet` | lock base | exists |
| 3 `lane` | `rf`, `work`, `suites2077.txt`, judge, apply | step 0; frozen files |
| 4 `astep` | `work`'s five edited files and the two new tests | step 3 |
| 5 `update` | `vupd` at A | step 4 |
| 6 `kstep` | `vupd`'s counts file | step 5 |
| 7 `plain` | `chk` at K | step 6 |
| 8 `mainmove-last` | origin | Step 1 |
| CQ | K | step 6 |
| PUSH | K, CQ rc 0 | steps 6, 8, CQ |

## OUTSIDE THE FENCES (disclosure)
- Read a sibling drafter's scratch (`fleet/state/s326/d2076/`: its clone, frozen scripts, `jwhole.py`) and cloned from it; read `s325/d2074/slot.py`, `namescan.py` and `s322/d2042/chromium-proof.js`; used the B2042 drafter's `node_modules` (Playwright) read-only. Git write verbs only inside my scratch clone (worktrees, branches, scratch commits with a scratch identity set in my clone's local config: `drafter-scratch`, never pushed). Fetched 9d4ddb7f INTO my clone FROM `.tools/b2074/clone` (a project seat clone, read only).
- Used the project's jest lock (`nexusai-lock.sh`, ticket files in its lock base); read N173's STATUS file tail and the B2069 STATUS `## Corrections` heading; `gh api -X GET` only under the project's `GH_CONFIG_DIR`; Jira GET with the project `.env` read in-process. No HTTP to any hosted host (the Chromium proof is `about:blank`).
- Hook refusals (each a STOP for that action, none worked around): `cd` once in a probe (refused; removed), `git -C $VAR checkout/worktree` three times (variable path; redone with literal paths in script files), `rm -f` of scratch logs once (refused; quarantined with `mv` under `laneT/_quarantine_*`). Killed my own aborted lane processes by pid at 09:20 (lock released).
- Not read: the card store, `fleet/briefs_staged/`, `scoreboard.md`, `_ledger.md`, any WEDNESDAY/FRIDAY tree or non-Datasec project.
date at the last read: Wed 25 Nov 2026 10:18:32 AEDT
