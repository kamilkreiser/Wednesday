STARTABLE: YES

# B746 drafter report (NexusAI N-CHAIN: RD-885, RD-849, RD-876 part 1), 2026-10-26 14:52-15:00 AEDT

Kit: `/Volumes/Laptop-DEV/TUESDAY/2_Project_Files/tuesday/briefs/2026-10-26_B746_SEAT-M15_nexusai-885-849-876-chain.md` (150 lines). Read-only drafter (Sonnet sub-agent); wrote only the kit and this report.

## BLUF
- One seat, `Datasec/NexusAI-M15`, Opus (`BRIEF_SEAT_LEVEL=opus`, `claude-opus-5-5`), three commits in series on `b746/nexusai-885-849-876-chain`, red-first, ends READY FOR QA (PARTIAL pushes the proven prefix of the chain). Ports 9880-9889 (probably unused). Gate default tier 1.
- **Two corrections to the sweep that change what the seat does:** (1) the RD-876 clamp is `backend/simpleDb.js:802`, NOT `backend/server.js` (server.js only passes the limit through, `:21133`, `:20917`); (2) RD-885's git-environment failure (B714-3) sits in `__tests__/helpers/dockerfile-stages.js:133/:154` (no `env` on `execFileSync('git', ...)`), because `rd848-no-redundant-copy.test.js:61` already strips `GIT_`. Both are written as the drafter's reading, to be reproduced by the seat first.
- Main has not moved since the 14:30 sweep: `61154bba6ae745b0749d804a4b14def45875d785`; counts file 5155 tests / 306 suites. Open PRs: #118 (logger-live test), #119 (`HISTORY.md`): disjoint from YOURS.
- Deploy on landing: `Deploy demo` is NOT path-ignored for `backend/**` or `scripts/**` (unlike test-only B713), so it starts, but every job is gated by `vars.CI_DEPLOY_ENABLED == 'true'` and the repo has 0 Actions variables; main's own push run read `skipped`. Build, Gitleaks, npm-audit and CodeQL also run. CI is paused per the sweep's relay of the 12:35 ruling.

## Facts re-measured (instrument and control)
| Fact | Instrument | Control |
|---|---|---|
| main = `61154bba...`, merge commit, parents `8ae0a87f` and `f1d23b25` | `git ls-remote`, `commits/<sha>` | the other refs print lines; `b713*` exists, `b746*` does not |
| Open PRs #118 (1 file), #119 (1 file) | `pulls`, `pulls/<n>/files --paginate` | `pulls/117/files` returned its 5 files incl. the counts file |
| `b703/...` ahead 0 behind 1; `b713/...` ahead 1 (logger-live file); `records/b727` ahead 1 (`HISTORY.md`) | `compare/main...<branch>` | `19b7106b...6e076b29` returned 6 files |
| Counts file 5155 / 306; depth-1 `__tests__/*.test.js` = 306 | `contents` raw; `git/trees?recursive=1` filtered | the `.zz` extension count = 0 |
| Clamp `simpleDb.js:802` (`...,10000)`), second `10000` at `:305` is another function | raw file read by line | `grep` hits both lines |
| `logSafe.js` C0 class `/[\x00-\x08\x0B-\x1F\x7F]/g`, no C1 | raw file read whole (47 lines) | the ticket's U+2028/9 and separators lines read |
| B667 appears on 4 rd777 lines: 55, 97, 171, 211 (ticket says 80, 86, 91, 97: stale) | `grep -n B667` on the raw file | count 4 |
| `dockerfile-stages.js:133,154` run git without `env`; `rd848...:61` strips `GIT_` | raw file read | `grep -n GIT_` printed the one stripping site |
| Existing rd774 cells call `executeRiskTemplate(...,10000)` at `:119 :128 :166` | raw file read | cell list printed |
| `deploy-demo.yml` push to main with `paths-ignore` `**.md`, `docs/**`, `tests/**`; `if: vars.CI_DEPLOY_ENABLED == 'true'`; variables `total_count` 0; main push run: Deploy demo skipped, Gitleaks success, npm-audit success, Build success | workflow raw read, `actions/variables`, `actions/runs?head_sha=` | the five runs listed exist |
| Landing convention: PR #117 bundled five tickets in one PR, merge commit with 2 parents; C-190 `:2067`, C-68 `:665`, C-218 `:2362` | `commits/<sha>.parents`, `CLARIFICATIONS.md` grep | line hits printed |
| RD-876 ruling is on the ticket as comment 40133 (2026-10-25 12:05 +1100) quoted in the kit; its scope is lower the clamp to 1,000 + notice + button; no words approved | Jira GET of RD-876 whole | JQL control `key in (RD-zzz)` = 0 |
| Seat name: highest NexusAI builder seat in 134 non-`.pre-` kits of 25/26 Oct = M14 (B713, finished) | `NexusAI-M[0-9]+\b` scan | `NexusAI-M99` control line matched |
| Ports: `lsof 9880-9889` empty; scan hits 6 kits (B638, B639, B693, B728, B729, B730); every decade of 9800-9899 is named by 6-12 kits, 9870-9879 and 9880-9889 the lowest | `lsof`, word-boundary scan | python listener on 9885 listed; `x 9887 y` matches, `x a9887 y` does not |
| Lock tool sha256 `cf01bafb...`; `queue-jest/` empty; load1 8.94 | `shasum`, `ls -la`, `uptime` | hash equals B713's recorded value |
| No `*B746*` file existed in `tuesday/briefs/` or the NexusAI `Briefs/` before writing | `ls | grep` (0 and 0) | n/a |
| Stamp slots: 9 lines match four underscores; 0 at-sign patterns; 0 names | `grep -c` | per the B713 REFUSE controls |

## Model routing (read, `model-routing.md:85-112`)
RD-885 = row C2 (`:92`, Sonnet first); RD-849 = row C3 (`:93`, Opus first, security surface); RD-876 part 1 = a small product edit (C2 would cover). One seat runs all three, so its level is the highest needed: **Opus**. The launch line carries `BRIEF_SEAT_LEVEL=opus` explicitly. Gate row G1 (`:108`) by default, G2 (`:109`) possible (Q-4).

## D-decisions
- D1: One branch, one PR, three commits (all three touch the counts file; PR #117 set the precedent for a multi-ticket PR landing as a merge commit).
- D2: RD-876 is ordered LAST so that Tuesday can cut at a commit boundary if it will not land a silent 1,000-row ceiling before part 2's words are approved.
- D3: Counts are computed by program (`jest --json` before and after per ticket) and the file is regenerated only by the project's own `--update-counts` command, once per commit; a mismatch is a STOP, not an edit.
- D4: Added a property the other kits lack: no brief-number token (B plus digits) in added lines or commit messages, because that is exactly RD-885's finding.
- D5: A partial chain may push its proven prefix (the tickets are independent), unlike B713 where a PARTIAL pushed nothing.
- D6: Lock hold limits: 35 minutes for a verify ticket, 20 for others (the queue was empty at 14:55 and load was 8.94).
- D7: Time budget: target READY 4 h, HARD STOP 6 h after Step 0 (four verifies of about 25-30 minutes plus waits).

## Q-questions for Tuesday (each with a default)
- **Q-1: RD-878 (non-string `risk_level` answers 500).** Measured COMPLETABLE with no new words (existing 400 text at `backend/server.js:21234`, throwing line `:21233`; the ticket's fix reuses that text). It is in the same counts chain. Default: OUT of B746 (per commission); a later seat or a follow-up kit.
- **Q-2: RD-870 (`generateUserActivityAnalysis` capture).** Measure-first and "or name why not" (ruling-shaped). Default: OUT.
- **Q-3: Level.** One Opus seat for all three (the RD-849 security surface sets it). Default: Opus single seat; the alternative is two seats (RD-885 on Sonnet, then RD-849 and RD-876 on Opus), which breaks the counts-file serial share.
- **Q-4: Gate tier.** Commit 2 is a security-surface sanitiser and commit 3 is a user-reachable ceiling. Default: tier 1 (Opus) at the branch head; tier 2 is defensible only for commit 1.
- **Q-5: Landing RD-876 part 1 before part 2.** After part 1 the run endpoint truncates silently at 1,000 rows; the ruling also asks for a "limited" notice and a show-all button, whose words are not approved. Default: build it as commit 3; Tuesday decides at the gate whether the PR lands with it (a subset is a new head and a new gate).
- **Q-6: Port overlap.** 9880-9889 was chosen from 9800-9899 while other drafters choose for B744 and B745. Default: Tuesday checks those two kits' blocks at the stamp; the seat probably binds nothing.
- **Q-7: CI is paused (sweep relay).** Default: the seat pushes its branch and stops; the landing waits for CI to resume.

## UNMEASURED
No install, jest, clone, fetch or workflow run was made. Not measured: the three rd848 failures (cause is a reading), C4/C5 survival (ticket's figure), the raw C1 pass-through (read from source), the seed's row count at this main, whether any existing risk cell returns more than 1000 rows, anyone relying on more than 1000 risk rows or on a "10,000" sentence in a UI or document, the full-verify wall time, CodeQL on the new head, node 24 on Linux.

## Outside-the-fences disclosure
- Read-only throughout. Jira: GETs and POSTs to the search endpoint through the HPSM-POC helper (credentials read in-process, never printed); the helper's output includes a commenter's display name, which was read and not copied into the kit. The kit names no person and no decision card.
- GitHub: `gh api -X GET` only, under the NexusAI `GH_CONFIG_DIR`, including 3 `search/code` calls. Raw file copies were written to the session scratchpad (`/private/tmp/claude-501/-Volumes-Laptop-DEV-TUESDAY/a4b8b0d7-c5c4-4870-a000-03dec8ba3ee1/scratchpad/k/`), not into any project.
- Local reads: `CLARIFICATIONS.md` greps (line hits only), `session-tools/nexusai-lock.sh` header (first 40 lines, not invoked) and its sha256, `ls` of the lock directories and the NexusAI `Briefs/` folder, `git status --porcelain | wc -l` on the shared checkout (34). One `python3` listener bound on 127.0.0.1:9885 for six seconds as the lsof control, then released.
- Did not read `decision_queue`, `briefs_staged`, the scoreboard, `_ledger.md`, or any WEDNESDAY/FRIDAY tree. Did not use Artifact, Docs, mail or chat. No git write in any project repo. Edited only the kit (two small post-write fixes) and wrote this report.
