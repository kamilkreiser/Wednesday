STARTABLE: YES (once Tuesday stamps the nine slots and the last line; no Composer pane runs, root `main` and code `main` are as the kit says, and nothing in the kit needs a port)

# Drafter report, B1549 (SEAT-R227, Composer records for PR #126 and PR #127)
Drafter: a read-only Agent-tool drafter (Sonnet 5.5), 2026-11-13 06:34:17 to about 06:45 AEDT by `date`. Kit: `/Volumes/Datasec_DEV/TUESDAY/2_Project_Files/tuesday/briefs/2026-11-13_B1549_SEAT-R227_composer-records-126-127.md` (103 lines) and its sidecar `.measured` (109 lines). Work folder: `/Volumes/Datasec_DEV/TUESDAY/2_Project_Files/fleet/state/s274/d_comprec/` (`jget.py` Jira GET helper, `measure.py` sidecar writer, `textscan_draft.py` text scan).

## BLUF
- **Both dependency landings are in none of the four record files, and no Jira ticket exists for either.** So the kit has ZERO Jira comments and ZERO moves. It records PR #126 and PR #127 as two C-entries (expected C-146, C-147), two new BACKLOG rows (expected #480 landing, #481 open items), one `JIRA.md` bullet (B1549), one history entry, one commit, one merge into root `main`, in the form of C-127 (a landing with no ticket) and C-143 (the shape).
- **Item 1 (Composer #126): not recorded anywhere** (0 hits for `PR #126` and `9c8d2cdb` in all four files), so it is recorded. **Item 2 (#127): not recorded**, so it is recorded with its removal condition and the `npm ls` ELSPROBLEMS note (in the E2 sentence, row #481 and, if created, the watch ticket). **Item 3 (Jira): no ticket exists** for alert 28, minimatch, or the vitest bump (`text ~ "minimatch"` 0, `"vitest"` 0, `"Dependabot"` 0; control `"composer"` 66). The project records no rule that asks for a follow-up ticket (C-111 (3), C-112; precedent bullets `JIRA.md:49`, row #471: "recorded, not ticketed"), so the watch ticket is ONE optional CREATE, slot NEWTICKET, default HOLD, text fully drafted (summary plus 4 description paragraphs, label `plan-comp-481`).
- Facts are re-measured at source: PR #126 merged 2026-11-12T02:22:39Z (13:22:39 AEDT), squash `9c8d2cdb`; PR #127 merged 10:10:59Z (21:10:59 AEDT), squash `c2b231fa` = code `main` now; trees equal the heads; CodeQL, both Analyze runs success on both heads; alerts 5 to 12 and 28 read `fixed`; 15 open (fast-uri 8, undici 5, fastify 1, ip-address 1; 3 high).
- `stamp_check.py` exits 0 (109 claims, 109 measured).

## Facts re-measured, with instrument and control
| Fact | Instrument (time from `date`) | Control |
|---|---|---|
| PR #126: merged true, `merged_at` 02:22:39Z, `merge_commit_sha` `9c8d2cdb8a24...`, head `13bf95065519...`, base `5d3bf82d`, files 3 (+1-1, +147-147, +1-1) | `gh api -X GET repos/datasecau/Datasec-Security-Composer/pulls/126` and `/files` under the project `GH_CONFIG_DIR` (06:34:44) | `pulls/9999` HTTP 404 |
| PR #127: merged true, `merged_at` 10:10:59Z, squash `c2b231fada1a...`, head `b3d1a6f2c41e...`, base `9c8d2cdb`, files 2 (+58-16, +8-0) | same (06:34:44) | same |
| Squash parents and trees: `9c8d2cdb` one parent `5d3bf82d`, tree `ff517fca508a` = head `13bf9506` tree; `c2b231fa` one parent `9c8d2cdb`, tree `de561f6a2fad` = head `b3d1a6f2` tree | `gh api .../git/commits/<sha>` (06:37:21) | the two heads and squashes are different shas with equal trees (the read distinguishes them) |
| Code `main` = `c2b231fada1a9a7d44c3e6a3f9ad733a12ab2b9b`; open PRs #85 only; #86 and #91 closed unmerged (02:24:35Z, 02:24:37Z), one bot comment each; newest PRs 127, 126, 125 | `branches/main`, `pulls?state=open`, `pulls/86`, `pulls/91`, `pulls?state=all&per_page=3` (06:37:21) | list contains #85 and the expected numbers |
| Checks: head 126 `CodeQL`, `Analyze (javascript-typescript)`, `Analyze (csharp)` success 02:20:01Z to 02:21:31Z; head 127 same, 10:08:02Z to 10:10:01Z; squash `9c8d2cdb` Dependabot x2 + both Analyze success; squash `c2b231fa` both Analyze success; analyses `results_count` 0 on all 8 rows | `commits/<sha>/check-runs`, `code-scanning/analyses` (06:36:04, 06:37:21) | analyses listed for `refs/heads/main` and `refs/pull/126|127/head` (rows exist, not an empty list) |
| Alerts 5 to 10 vite, 11 and 12 @vitest/mocker: `fixed`, `fixed_at` 02:22:44Z/02:22:45Z; alert 28 minimatch GHSA-g3hv-75wg-m249 `fixed` 10:11:07Z; open 15 = fast-uri 8, undici 5, fastify 1, ip-address 1 | `dependabot/alerts/<n>`, `dependabot/alerts?state=open&per_page=100` (06:36:04, 06:36:22) | `dependabot/alerts/9999` HTTP 404; 15 rows summed per package = 15 |
| Open code-scanning alerts on `refs/heads/main` 0 | `code-scanning/alerts?state=open&ref=refs/heads/main` (06:37:21) | `state=fixed` returns 20 rows (the same 20 C-127 recorded) |
| Gates: B1534 `GO WITH FINDINGS @ 13bf950 on main 5d3bf82`, G2, dependency-bump, round 1 of 2, Minor 3 (F1 to F3); B1547 `GO WITH FINDINGS @ b3d1a6f on main 9c8d2cd`, G2, dependency-override, round 1 of 2, Minor 3, Info 2 | `sed -n` / `awk` over the two VERDICT files, `shasum -a 256` prefixes `335b69a37d3f52fe` (61 lines), `14a655964021e175` (48 lines) | line numbers printed by `awk NR==n`, not remembered |
| Builder statuses: B1534 STATUS 124 lines, `1770234cccbace94`; B1547 STATUS 112 lines, `c8a2b59e14139657`; ticket-text 15 lines, `e5c1de117c820364`; removal condition `:98`, npm reading `:68` | `shasum`, `wc -l`, `/usr/bin/grep -n -F` | grep of an absent phrase prints 0 |
| Root repo: HEAD `844c9a700af4...` = `refs/heads/main`; no remote; 4 record files clean; `user.email` `kamil.kreiser@datasec.com.au`; `records/b1549` absent (rc 1); `.tools/b1549` absent | `git -C ... --no-optional-locks rev-parse/remote -v/status --short/config` (06:36:42) | `records/b1509` resolves (rc 0); `.tools/b1509` exists; the code clone under `2_Project_Files` prints `origin` (2 lines) |
| Anchors: CLARIFICATIONS 2,754 lines, `### C-145` at `:2740`, `### C-146` 0; JIRA.md 55 lines, `- B1509` `:55`, `- B1549` 0; BACKLOG 475 lines, 469 data rows, `| 479 ` `:475`, `| 480 ` 0, `| 481 ` 0; history 2,193 lines | `wc -l`, `/usr/bin/grep -c -E`, `-n` (06:37:37) | `### C-142` 1, `- B1499` 1, `| 479 ` 1 |
| Not already recorded: `PR #126`, `PR #127`, `9c8d2cdb`, `c2b231fa`, `minimatch`, `alert 28`, `GHSA-g3hv`, `PR #91`, `B1534`, `B1547` print 0 in all four files; `vitest` 1/9/0/2 (CLAR/BACKLOG/JIRA/HIST, older test-runner mentions); `Dependabot` 2/13/0/4; `#91` 5/15/0/15, `#86` 5/16/0/14 (open-PR lists; row #448 at `BACKLOG.md:444` names the bot PRs, "not graded") | `/usr/bin/grep -c -i -F` per file (06:40, again in the sidecar) | `PR #124` prints 5/4/1/2, `C-145` 3/2/1/2 |
| Jira: 128 issues, 47 Done, `held` 19, seed marker 94, 81 Backlog, `needs-kam` 2, `created >= "2026-11-12"` 0, `labels = "plan-comp-480"` 0 and `"plan-comp-481"` 0; no ticket on minimatch, vitest, Dependabot; `PCOMP-128` Backlog, 0 comments, 0 changelog | `jget.py` (GET only, `project = PCOMP AND ( ... )`, token read in-process, never printed) (06:35 to 06:40) | `PCOMP-9999` HTTP 404; `labels = "plan-comp-479"` 1; `created >= "2000-01-01"` 128; `composer` 66; `zzqxvbw` 0 |
| Seat id: `R227` word-scan 0 in 79 non-`.pre-` briefs of 2026-11-12/13 (this kit excluded) | bash loop with `/usr/bin/grep -q -w -F` (06:44:02) | `R226` 2, `R225` 2 |
| Model: Sonnet; `models_latest.json:23`; routing `:97` row C7 and `:110` row G3 | `awk NR==97/110`, `/usr/bin/grep -n` | rows start `\| C7 ` / `\| G3 ` |
| Listeners: none needed; `lsof -nP -iTCP -sTCP:LISTEN` printed 12 lines overall (not ours) | `lsof` (06:38:22) | the 12 are other seats' |
| Jira text scan (summary + 4 paragraphs): ASCII, 0 hits for work number, seat code, internal words (incl. `lock`, `gate`, `status`), path, bracket/backtick, duration, deployed/live/production, host, 9 names (underscore-aware) | `textscan_draft.py` (06:43:29, re-run 06:43:50) | 13 planted phrases each fire (incl. `x_by_Kam_y`); clean phrase `PCOMP-98 NOT DEPLOYED Composer PR #121 package.json` reads 0. **A first run hit `lock` in `--package-lock-only`; DESC-2 was reworded ("a lockfile-only install") and re-scanned to 0.** |

## Corrections and findings in the sources (the kit says them)
- B1534 and B1547 as built: the product owner's ruling covers the re-push of the bot updates only; it does not name the minimatch override. E2's Authority says so and REFUSE 9 stops any line claiming otherwise.
- B1534 STATUS and the gate differ on one word only (F3: redundant, not conflicting); the kit follows the gate (a later, measured read).
- The pull request merge account is not recorded (precedent: C-127). Both squashes are `verified` true by the API.
- The kit's `.tools/b1509/scripts/records.py` does not hold `--no-ff` (0); the merge step is in `records2.py` (1). The kit now says so.

## Chain inputs (rule 4: each step's inputs come from an earlier step or exist at BASE)
| Step | Inputs | Produced by / exists at |
|---|---|---|
| 0 | the kit; `.env` names; B1509 helper scripts | BASE (exist now: kit, `4_Credentials/.env`, `.tools/b1509/scripts/` 13 files) |
| 0 | `refs-before.txt`, `status-all-before.txt` | made by Step 0 itself, before STATUS (absent now) |
| PRIOR WORK | PCOMP-128 and counts; PR list; record files; C-127 and C-143 | BASE (read-only) |
| 1 | gate files, builder statuses, PR/alert/check reads, anchors | BASE; the highest C-number and row number come from this step |
| 2 | decision table | Step 1 anchors |
| 3 | payload file under `Briefs/2026-11-13_B1549_evidence/runs/`, scanner copy, dry-run | the payload is built by Step 3 (1) BEFORE the scan (2) and the dry run (3) |
| 4 | the create (only if `CREATE`) and its key | Step 3 payload and dry run; duplicate search at that moment |
| 5 | C-entries, rows, bullet, history; the Task key in rows #481, both C-entries and the bullet | Steps 1 and 4 (the key comes from Step 4 before Step 5 writes it) |
| 5 | worktree `.tools/wt-b1549-rec`, `records/b1549` | made by Step 5's `worktree add` |
| 6 | STATUS | all earlier steps |

## D-decisions (mine)
- D-1: no Jira comment or move, because no ticket exists (C-127 and bullet `JIRA.md:49` are the precedent).
- D-2: two C-entries, one per PR (as C-131 to C-133), and two rows: #480 a landing record (as #470) and #481 open items, row only (as #471).
- D-3: the watch ticket is a CREATE slot with default HOLD; label `plan-comp-481`, not the seed marker. Row #479 and PCOMP-128 are not touched.
- D-4: no sentence is appended to older rows (#254, #448): "no earlier record is edited"; they are named as context in E1.
- D-5: the settled sentences carry a "RELAYED" removal condition with the builder's registry figures (381/20/415, dated 2026-11-12), because the seat has no registry access.

## Questions for Tuesday (each with a default)
- **Q-1 (slot NEWTICKET):** create the minimatch-override watch Task? Default HOLD (the project asks for no follow-up ticket; the condition is in E2 and row #481). If CREATE, text is fixed in the kit.
- **Q-2 (slot ROW-FORM):** APPEND (rows #480 and #481)? Default NONE per the kit's slot rule; I recommend APPEND, and without it the open items (15 alerts, the npm pin) have no home.
- **Q-3 (slot REC-MERGE):** MERGE into root `main`? Default HOLD; recommend MERGE as in B1509.
- **Q-4:** the 15 open alerts need their own update lane; B1534's stamp answered "Tuesday raises a separate bump lane". The kit only records them. Default: yes, a later brief.
- **Q-5:** E1's Authority names the product owner's "Re-push as our own, on all four projects" (verbatim from the B1534 kit line 7; the card id is left out). Default as written; change the wording if you prefer the clock only.
- **Q-6:** whether PR #122 (named inside C-145 only) needs its own landing entry was left open by C-143 and is NOT in this kit. Default: not in scope.

## UNMEASURED
- Any hosted state, deploy, or demo (outside the fences); "NOT DEPLOYED" is a repository fact only.
- The registry facts (eslint 10.14.0 `^10.2.6`, config-array 0.23.5 `^10.2.4`, estree 8.72.2 `^10.2.2`; 381/20/415 stable versions; alpha line) are RELAYED from the B1547 STATUS and dated 2026-11-12; I did not read the registry.
- `npm ls` ELSPROBLEMS under npm 10.9.8, the `--before` dates, `npm audit` 14 to 4, suite counts: RELAYED from the builder and gate files, not re-run.
- The Jira text search uses Jira's stemmer; zero hits for minimatch/vitest/Dependabot is read with the controls above, and the seat repeats it.
- Whether the seat's R209 scanner (`textscan.py`) agrees with my scan: not run (I did not execute another seat's helper).
- Nine sidecar lines (of 109) are backtick-pair artefacts of kit prose (an odd backtick in lines 7, 9 and 80 pairs the text between two literals); they are not literals a seat matches. They are marked as such in the sidecar; reword the three lines if you want them gone.

## Outside-the-fences disclosure
- Read-only everywhere except my files. Reads: the two template kits, the two STATUS files and evidence folder of B1534 and B1547, the two VERDICT files, the Composer record files and `JIRA.md`, `.tools/b1509/scripts/` (names and `grep -c` only), `brief_seat.sh` line 24, `model-routing.md`, `models_latest.json`, `4_Credentials/.env` (a `/usr/bin/grep -c` for the three JIRA variable NAMES and an in-process read by my `jget.py`; no value printed), tmux pane list, `lsof` listener count, `gh api -X GET` (about 45 calls) and Jira GET (about 60 calls, all `project = PCOMP AND ( ... )` or single-issue reads).
- **One stray write:** my first scan command redirected `> /tmp/none` (an empty file in `/tmp`, outside my folders). It holds nothing; I did not remove it (no delete). I also ran an unused `cd_unused=1` shell variable assignment (no `cd`).
- Harness side effect: tool outputs larger than the display limit were saved by the harness under `/Volumes/Datasec_DEV/TUESDAY/4_Credentials/.claude/projects/...tool-results/`; not my files.
- No `decision_queue.sh`, no brief staging, scoreboard, ledger, WEDNESDAY/FRIDAY tree, non-Datasec project, az, ssh, docker, npm, hosted host, mail, Jira write, GitHub write, or message to a human.

stamp_check final line: `stamp_check: 109 claims, 109 measured, 0 not measured (sidecar /Volumes/Datasec_DEV/TUESDAY/2_Project_Files/tuesday/briefs/2026-11-13_B1549_SEAT-R227_composer-records-126-127.md.measured)` (exit 0)
