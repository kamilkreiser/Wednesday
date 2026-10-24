# B610 drafter report (SEAT-R34, MPS records for the 24 to 25 Oct landings), written 2026-10-25 about 00:40 AEDT

Brief: `/Volumes/Laptop-DEV/TUESDAY/2_Project_Files/tuesday/briefs/2026-10-25_B610_SEAT-R34_mps-records-107-108-109.md` (103 lines, 49,551 bytes). No `.pre-stamp` copy was made (fence: two files only); take it before stamping. Template: B583 (SEAT-R30), the latest MPS records brief, read whole with its stamp and its `.pre-stamp`; B605's head read for the newest wording.

## BLUF
- The brief is ready to stamp: records seat, Sonnet, pane `Datasec/MPS-R34`, no port, no heavy slot, 4 Jira creates (T-A to T-D) and 14 comments (one per ticket the three landings touch), a coordinator section, 13 BACKLOG rows, 2 history entries, 1 JIRA.md section, the B589 Correction line committed on `records/b610`, and the seat fast-forwards root main itself (the convention B583 and B556 used).
- **Decision for you before stamping: the "move closed tickets to their done-state" instruction resolves to NO TRANSITION under the project's own rule.** `JIRA.md:174, :185, :208, :243` say "no project rule moves a ticket on merge or deploy (R-R13-1)"; the 14 Done tickets in MPSCALC are all question or early-build tickets from 2026-10-01 to 10-13; B583 posted evidence comments on 71 landed tickets and moved none. So the brief gives each landed ticket one evidence comment and slot DONE-TRANSITION defaults `no`. A `yes` needs a quoted grant in the stamp.
- **#109's push run on main was still `in_progress` (web and dotnet) at 00:15:44.** The brief tells the seat to re-read it, not to stop on it, and to record a failure by job name.

## Stamp decisions (slot -> default -> recommendation)
1. DONE-TRANSITION: default `no`. Recommend `no` (above). If the product owner wants Done, quote his line; MPS statuses are Backlog / Selected for Development / In Progress / Done, so there is no Testing state as in NexusAI.
2. LABELS-REMOVE: default `no`. Recommend `no` (no line of `JIRA.md` allows a records seat a label edit). `needs-ruling` stays on -204 and -316, both already ruled (C-62, C-64); carry the question in FOR TUESDAY.
3. B589-COMMIT: default `yes` (you asked for it). Note: `B589_STATUS.md` is untracked WHOLE, so the commit tracks the whole 344-line file, not just the Correction line at `:338`. 349 Briefs files are tracked and 647 are not, so there is no clean rule. Recommend `yes`, as asked; `no` is the alternative if you would rather track no builder file.
4. FF-MAIN: default `yes` (B583 and B556 convention; Tuesday may not write another project's `.git`). Recommend `yes`.
5. EVENING-RULINGS: default `none`. I cannot read the decision store. If the product owner ruled anything since 12:00 on 24 Oct (C-65 is the highest on file), paste each with board time and `ruled_ts`; the seat writes C-66 onward. Recommend you check the day's rulings list before stamping.
6. Hard stop: suggested target 90 minutes and hard stop 3 hours after Step 0 (18 Jira writes, no bulk driver).
7. Launch line carries `WED_USAGE_STOP=100` copied from the B583 template (the 2026-10-20 Datasec grant); re-confirm it is still the live setting.

## Ticket plan (dedupe result)
- **Create (4), each with a search-first list and a zero control; no twin was found by the drafter:** T-A the 15 governed-validate server errors (B585 candidate, B594 fact 1; neighbours -53, -50, -319, -190, -166 to be read whole); T-B store reopen follow-ups B594-1, B594-2 plus the no-store hold (neighbours -323, -324; `NoStore`, `vanished`, `StoreReopen` all 0 hits); T-C draft-save refusal-order pins B604-1, B604-4, B604-6 and B591-10's order gaps, aggregated as one path (neighbours -204, -213, -322); T-D web stub and e2e leftovers (stub unit-test file, `bom.spec.ts:180`, `check-bundle.mjs`; neighbours -313, -118, -297).
- **Comment instead of file:** B606-1 on -330, B606-2 on -329, the focus-width question N9 on -321, the OpenAPI sentence on -290, the `maxLength` and `:1424` words items on -316.
- **14 comments, one per key:** #108: -323, -324, -326, -327 (the PR body names them); #107: -204, -316, -290; #109: -328, -329, -330, -218, -221, -321, -313 (the gate B606 clause-by-clause reading and the builder table). Shape: BLUF, FOUND, TESTED, HOW, ending `[B610]`; no name, no card id.
- Not filed (BACKLOG only): Notes B594-3 to -7, B604-2, -3, -5, -7, -8, B606 N1 to N11 not ticketed, B591-1 to -9 (closed or carried).

## MEASURED (instrument, time; AEDT, clock `date`)
- Latest MPS records brief is B583 SEAT-R30 (`ls -t` of the briefs folder, 00:12:36). Its `.pre-stamp` reads 9 lines with four underscores; B610's reads 9 (grep -c with the split pattern, control `a____b` 1).
- Root repo (git read verbs, 00:12:58): HEAD `a5b95c5eee1897025cb9cec8ea0f0ebb20a489b9` on `main`; CLARIFICATIONS 1275 lines, highest `### C-65` at `:1219`, last coordinator heading `:1228`; BACKLOG 2712, JIRA.md 247, history 1115; `records/b610`, `.tools/b610`, `.tools/wt-b610-records`, `.tools/.git-lock` absent; `numstat` on CLARIFICATIONS empty.
- Code repo (`gh api -X GET` under the project's `GH_CONFIG_DIR`, 00:13:22 to 00:15:44): #107, #108, #109 `closed`, `merged` true, merged_at 12:44:18Z, 09:58:11Z, 13:11:36Z on 2026-10-24; squash shas, heads, file/line/commit counts, parents as in the brief; one `merged_by` account for all three; main `93e1cab5...`; open PRs 0; `compare e027ebd0...93e1cab5` ahead 12, behind 0; check-runs #108 8/8 and #107 8/8 success, #109 7 total, 5 success, 2 in progress. Squash messages and PR bodies read whole: no squash names a key; the #108 body names 323, 326, 327, 324.
- Jira GETs (00:13 to 00:14, credentials read in-process, never printed): highest key MPSCALC-330; `created >= "2026-10-24"` is -321..-330; `labels = mpscalc-b610` 0 (control `mpscalc-b583` 3); zero control 0; `QA gate B354` 6; status, labels and comment counts of 20 keys; 45 `text ~` terms; 14 Done keys listed.
- Gate and builder STATUS sections read as listed in the brief's SELF-CHECK; the line numbers cited were taken from `grep -n '^#'` headings in the same read.
- Panes (00:15): `tuesday`, `Datasec/HPSM-POC-G91`, `fleet-monitor`; no clash with `Datasec/MPS-R34`. load1 2.52. `lsof` 9620 to 9700 listing empty; no port is bound by the brief.
- Self-checks on the brief (python and grep, with controls): four-underscore lines 9 (control 1); `@[A-Z_]+@` 0 (control 1); non-ASCII bytes 0 (control 2); names 0 (control 1); decision-card ids 0 (control 1).

## UNMEASURED
Jira descriptions, Acceptance text and existing comments of the 14 targets and of every neighbour (the seat reads them whole); whether any neighbour is a twin; lane labels beyond -204 and -313; whether the hosted showcase moved (no probe; the B583 record says `e027ebd0`); the end state of #109's push run; whether the C-64 string is at `docs/API.md:425` and `openapi.json:369` at `5fe35a05`; whether `bom.spec.ts:180` reproduces; the evening's rulings; Linux CI for the new store rows; the `.tools/b583/` helper contents (names only).

## Fences kept
Wrote only the two files above (and a scratchpad Jira GET helper and two query scripts under the session scratchpad). No `decision_queue.sh`, `fleet_ack.sh`, `briefs_staged/`, `scoreboard.md`, mail, chat, Artifact or Docs call. Git in the project repo: `rev-parse`, `log`, `status`, `diff --numstat`, `ls-files`, `branch --list`, `worktree list`, `check-ignore` only (no fetch, no worktree add). `gh` GET only. Jira GET only, every JQL beginning `project = MPSCALC AND`. No build, test, HTTP to a hosted host, az or docker. No `cd`.
