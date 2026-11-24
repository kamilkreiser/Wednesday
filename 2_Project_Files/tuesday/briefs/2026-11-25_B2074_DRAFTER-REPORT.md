STARTABLE: YES

# B2074 DRAFTER REPORT: NexusAI lane NX-S2 (RD-1017, RD-975), kit `2026-11-25_B2074_SEAT-N172_nexusai-nxs2-audit-action-business-hours.md`

Drafter: an Agent-tool drafter for Tuesday (s325), commission `2026-11-25_B2074_NEXUSAI-NXS2-SERVER-BUNDLE_DRAFTER_COMMISSION.md`. Read window: Wed 25 Nov 2026 from 06:05:14 AEDT (first `date`) to the `date` on the last line of this report. Scratch: `/Volumes/Datasec_DEV/TUESDAY/2_Project_Files/fleet/state/s325/d2074/`. Files written outside scratch: this report, the kit and the kit's `.measured` sidecar.

## SUMMARY (10 lines)
1. STARTABLE: YES, provided the STAMP accepts Q-0 (the new key `SETTINGS_CHANGE`). Seat id N172 is free: a word scan of 203 non-`.pre-` SEAT kits from 18 to 25 Nov finds N172 in 0 files (control: N171 in 2, N170 in 5).
2. BASE is `11149d3f` (the merge of PR 251). Counts 6323 / 398, `backend/server.js` blob `6d8e51390547`. Open PRs: 0 at 06:05; at 06:43 there is 1, #252 (records/b2073-history, `HISTORY.md` only, which HOLD 20 allows).
3. **The kit builds 2 of the 5 keys:** RD-1017 and RD-975. `backend/server.js` gets 4 lines added and 1 removed, plus two new test files and the counts file.
4. **RD-974 is out.** I applied the smallest fix in scratch and 2 of the 65 rd798 cells turned red (`C-BODY-HOURS LIVE`, `OUT 190`). The seeded rows have no `Job_Start_Time`, and that suite pins the clock-dependent paragraph. **RD-893 is out:** its own text says to measure first and build the type checks under a separate ticket. **RD-896 is out** (measure only). **RD-577 is not built** (records only).
5. **Cells:** 18 tests (RD-1017: 10; RD-975: 8). Red-first fails exactly 9 named cells, red-proof fails the same 9, and the 28-suite green passes 509/509 (rd798 and rd994 included).
6. **Full verify** at prototype A: `VERDICT: PASS` 6341/6341 across 400 suites, EADDRINUSE 0, 06:17:08 to 06:39:05. K must carry 6341 / 400.
7. **Local CodeQL** at prototype K (`--base 11149d3f`): rc 0 PASS (29/29, KEPT 0, NEW 0, GONE 0). The frozen `lane2074.sh` ran end to end and all three judges read PASS. All 4 of my jest acquisitions ran inside the project's jest lock.
8. **The sweep pointed at the wrong function.** Its RD-975 pointer (line 13411) is in `generateUserCountReport`. The ticket's function is `generateBusinessHoursReport`, line 13775. That is the line the kit edits; 13411 stays as it is (Q-5).
9. Model: row C2 (Sonnet, line 92), gate G2 (line 109), both per the commission's framing (Q-1). Nothing deploys; a merge starts a skipped-by-variable Deploy demo run (Q-6).
10. **Questions:** Q-0 new key; Q-1 Sonnet C2 / G2; Q-2 RD-974 out; Q-3 RD-893 out; Q-4 RD-896 out; Q-5 the other created_at readers left alone; Q-6 no deploy; Q-7 BASE `11149d3f`. Defaults are below.

## FACTS RE-MEASURED (instrument; control)
- **origin main** `11149d3f38b0dacab95b2397aea6bca64f0c819f`: `gh api -X GET .../git/ref/heads/main` at 06:05:58 and again at 06:43:35. The commit GET:
  - message `Merge pull request #251 from datasecau/b2069/rd1036-viewer-data-sources-list`
  - tree `0a0f0a4a...`, parents `e2911754` and `c1a99d4b`
  - committed 2026-11-24T16:43:50Z
- **Refs and PRs:**
  - `matching-refs/heads/b2074` returns 0 (control: `b2069` returns 1).
  - Open PRs: 0 at 06:05:58 and 1 at 06:43, #252 `records/b2073-history` (`pulls/252/files`: `HISTORY.md`).
  - `compare/11149d3f...records/b2073-history`: ahead 1, behind 0.
- **The drafter's tree:** `git clone --no-hardlinks --no-checkout` of the project checkout `2_Project_Files`, which holds `11149d3f` (`cat-file -t` reads commit), detached at BASE itself. So, unlike B2069, the cells ran at the merge commit.
- **Jira GET**, whole, comments paginated (`jwhole.py`, a copy of the B2069 drafter's GET-only reader; it prints key, character counts and status only):
  - RD-1017: To Do, 4409 characters, 0 comments.
  - RD-975: To Do, 1214 characters, 0 comments.
  - RD-974: To Do, 1467 characters, 0 comments.
  - RD-893: To Do, 2926 characters, 2 comments.
  - RD-896: To Do, 2741 characters, 0 comments.
  - RD-577: To Do, 2153 characters, 2 comments.
  - Every ticket sentence quoted in the kit: `grep -c -F` reads 1 in the dump.
- **`CLARIFICATIONS.md`** (954114 bytes; never read whole):
  - `awk NR==2067` holds "Never squash, never rebase" (C-190, count 1).
  - `grep -n -i` finds RD-1017 and RD-975 on Related lines only (2605, 3113, 3134, 3146, 3168). No entry decides the tag or the order.
- **Source facts at BASE** (`grep -n -F`, `awk`, and a program over `backend/server.js`):
  - `AUDIT_ACTIONS` has 18 keys; the file reads 17 distinct names in 39 places; the only undefined name is `SETTINGS_CHANGE` (writers at 17366 and 17616).
  - Line pointers: export filter 2128; `auditLog` 306 and its log line 318; buffer load 339.
  - Business hours: report at 13740 with its list at 13775. The user-count report is at 13357 (list 13411), and `getStatsFromLogs` at 6090 (list 6121).
  - Literal-kind writers: `DATA_SOURCE_ALLOWLIST_REJECT` on 3 lines, `DATA_SOURCE_ENDPOINT_REJECT` on 1.
  - `seedDemoData.js` line 34 lists `Job_Start_Time_UTC` and no `Job_Start_Time`.
  - `simpleDb.js` line 67 is `Job_Start_Time_UTC TEXT`; `azureLogAnalytics.js` line 1138 writes ISO strings.
- **rd994 census:** cell C3 at line 287 holds `SETTINGS_CHANGE` 2 (line 70) and R12 (line 75). A new key leaves it true; the green run confirms.
- **deploy-demo.yml at BASE:** lines 26, 29 to 32, 53, 91 and 95 as quoted. The runs GET reads total 266, last 20 skipped.
- **Code scanning:** 22 open; 13 at `backend/server.js`, none in the edited spans.
- **Model routing:** line 92 is C2 and line 109 is G2; `models_latest.json` line 23 is `claude-sonnet-5-5`.
- **Slots** (`slot.py`, the project's rule; controls `b2042` rf 0 / work 7 and `b2069` rf 11):
  - `b2074-nodot/rf` 7, `work` 7, `vupd` 16, `chk` 15.
  - `lsof` showed 0 listeners in each band at 06:18:32 (control: 12 machine-wide).
- **Port word scan** over the 30 non-`.pre-` SEAT kits of 24 and 25 Nov (5-digit numbers inside the three bands):
  - 38 numeric hits; 2 have port context, both in B2042's REFUSE 7 (band 24480-25119, its `work` slot 7).
  - B2042 is finished (`READY B2042`), so nothing is live in the band.
- **Lock base:** `queue-docker queue-jest released`, `queue-jest` 0 tickets, at 06:09 and 06:43. Panes: `Datasec/NexusAI-R321` (records; STATUS `READY B2073`) and `tuesday`.
- **NexusAI STATUS files 22 to 25 Nov:** 16 (15 `READY`, 1 `DEPLOYED`).
- **apply2074.py:**
  - `apply` prints `bytes 1140305 -> 1140567 lines 22819 -> 22822 nonascii 3913`, blob `a7426b07a963`.
  - A second apply and a second revert each give `AssertionError`, rc 1.
  - `revert` gives back `6d8e51390547`.
- **Jest** (all inside `nexusai-lock.sh jest`):
  - rf: 9 failed of 18 (exactly the 9 named).
  - green (28 suites): 509/509 in 45 s.
  - redproof: the same 9.
  - Judge controls each read FAIL: green-as-rf, green-as-redproof, rf-as-green.
- **RD-974 probe** (`t/x974`; one line of the off-hours filter skips a job with no `Job_Start_Time`): rd798 read 2 failed of 65 (`C-BODY-HOURS LIVE`: the `out.paragraph` it expects true read false; `C-BODY-HOURS OUT 190`: its hash changed).
- **The frozen `lane2074.sh`** (scratch T/RF/W), 06:15:45 to 06:16:32: every expected rc line, `lock-wrapper rc=0`, and three `JUDGE ... PASS`.
- **Full verify** 06:17:08 to 06:39:05 at A `92cc03c4248c`:
  - `Test Suites: 400 passed, 400 total`, `Tests: 6341 passed, 6341 total`, `VERDICT: PASS`, EADDRINUSE 0.
  - The counts went 6323/398 to 6341/400, with `_updated` the only other key that moved.
- **Prototype commits** A `92cc03c4248c` and K `51b1be10e89c` (scratch identity, never pushed):
  - `STATIC A PASS` (14 OK lines) and `STATIC K PASS` (13 OK lines).
  - gitleaks: staged A, staged K and `log -p` all read `no leaks found` (control pair: `leaks found: 2`).
  - `node --check` of the three files: rc 0.
- **CodeQL** (base `11149d3f`, head `51b1be10`), 06:39:27 to 06:40:30: `diff pack: 4 files with added lines, 5 ranges`, results 29/29, KEPT 0, NEW 0, GONE 0, rc 0, `cq.err` 0 bytes.
- **Name scan** (underscore-aware, the four names of scanlib1114.py line 20, via `namescan.py`; "drafter's list, not the project's"): kit, msg-A, both test files and apply2074.py each read 0; control `_by_<name>_` fires (1). The kit holds 0 card ids (`grep -c -i 'datasec-nexusai-|decision_queue'` reads 0).
- **`stamp_check.py <kit>`:** 133 claims, 133 measured, rc 0. The four-underscore count in the kit is 5.

## D-DECISIONS (the drafter's, each overrulable)
- **D-1: two keys, not five.** RD-974, RD-893 and RD-896 each fail the build-now test at source:
  - RD-974: measured, a fix turns rd798 red.
  - RD-893 and RD-896: by their own text.
  - A kit that stays inside the commission's partition (`backend/server.js` plus new tests) can only build RD-1017 and RD-975.
- **D-2: RD-1017 adds a key rather than retagging.** This keeps rd994's census true without touching that test, and the value follows the object's own pattern (name = value). The commit message says it is a new tag, as the ticket asks.
- **D-3: RD-975 moves created_at to the end** of the report's one list, giving the exact order of the sibling readers (line 10101). Only the ticket's own function changes.
- **D-4: RD-975's cells lift the shipped function** (brace-balanced, `new Function` with a stub store and logger), as RD-1036 and RD-1026 lifted page functions. Times carry no zone, so the cells are zone-independent.
- **D-5: RD-1017's wire cells use the inventory boot** (`bootServer` with `inventory.PRELOAD` and `serverEnv`; outbound refused), as RD-1036 did. Each run boots once.
- **D-6: three lock acquisitions, dot-free trees, one commit A for both tickets** (one product file), then K, as in B2069.

## Q-QUESTIONS FOR TUESDAY (each with a default)
- **Q-0 (RD-1017's tag).** Add the key `SETTINGS_CHANGE: 'SETTINGS_CHANGE'`, or point both writers at an existing tag such as `CONFIG_CHANGE`.
  - Retagging would make rd994's census false and widen the lane into that test.
  - **Default: the new key.** REFUSE 1 stops the seat unless the STAMP accepts it.
- **Q-1 (model).** **Default: builder row C2 (line 92), Sonnet, `BRIEF_SEAT_LEVEL=sonnet`; gate G2 (line 109).**
  - Alternative: Opus under the 2026-11-21 model rule (Opus "or lower by the routing table").
  - The audit-trail key is labelled security on the board. If you read it as G1, the gate is Opus; the build stays C2.
- **Q-2 (RD-974).** Any fix changes route 190's night answer, so rd798's `C-BODY-HOURS LIVE` and `OUT 190` must be re-pinned.
  - It also needs a design choice: does `Job_Start_Time_UTC` count as a start time? (The seeded rows have only that field.) If not, the demo's off-hours paragraph disappears at all hours.
  - **Default: out of this seat. It becomes the next NexusAI seat after this lands, with rd798 in its partition and the choice stated.**
- **Q-3 (RD-893).** Its text says measurement (1) (the Log Analytics path) comes first and the type checks get "their own build ticket and gate". Its comment 2 confirms they are still open.
  - **Default: out of this seat. The records pass may note that `generateKQLQueryForCondition` (line 5316) calls `conditionText.toLowerCase()` (read, not run).**
- **Q-4 (RD-896).** **Default: out (measure only), as the commission proposed.**
- **Q-5 (the other created_at readers, lines 6121 and 13411, the ones RD-975 lists as "Not examined").** **Default: not changed. The records pass names them on RD-975.**
- **Q-6 (deploy).** A merge starts `Deploy demo`, because `backend/**`, `__tests__/**` and `scripts/**` are not ignored. It is gated on `vars.CI_DEPLOY_ENABLED`, and the last 20 runs were skipped. **Default: nothing deploys; the landing read is Tuesday's; the C-224 hold stands.**
- **Q-7 (BASE).** **Default: launch on `11149d3f`.** PR 252 (`HISTORY.md` only) may land first, which HOLD 20 allows. A move of `backend/server.js` or the counts file is a STOP.
- Also for the next records pass (not a question): RD-577 is "built, records only" (per the sweep). RD-1040 was created by B2073 for the plain data-source routes (RELAYED from B2073's READY line). This kit does not touch those routes.

## UNMEASURED
- The seat's own clone, `npm ci`, the push and the seat's lock acquisitions.
- The plain verify at K: its pair is PREDICTED equal to 6341 / 400.
- My `node_modules` is a symlink to the B2032 drafter's `npm ci` (same lockfile sha256).
- Not tested: the first-run (open) window, the audit buffer's disk round trip, the winston line text, a non-string start field reaching the report, Log Analytics rows, the chat routes that call the report, a hosted instance and Linux.

## CHAIN INPUTS (every step's inputs are produced by an earlier step or exist at BASE)
| step | inputs | made by |
|---|---|---|
| Step 0 | the kit, the frozen files, Jira | Tuesday's stamp; the drafter's folder; Jira |
| Step 1 | the project checkout, the deploy key, origin | BASE |
| Step 1b | the clone at BASE, `apply2074.py` | Step 1, Step 0 |
| 0 `trees` | BASE, the two frozen test files, `apply2074.py` | Step 1, Step 0 |
| 1 `quiet` | the lock base | Step 1 |
| 3 `lane` | `rf`, `work`, `lane2074.sh`, `judge2074.py`, `suites2074.txt`, `apply2074.py` | step 0, Step 0 |
| 4 `astep` | `work`'s three paths, `msg-A.txt`, `static2074.py` (reads `apply2074.py` beside it) | step 3, Step 0 |
| 5 `update` | A, `v2074.sh` | step 4 |
| 6 `kstep` | `vupd`'s counts file, `msg-K.txt` | step 5, Step 0 |
| 7 `plain` | K | step 6 |
| 8, CQ, push | K, origin | step 6 |

## OUTSIDE-THE-FENCES DISCLOSURE
- **Lock writes.** As the commission requires, every jest run and the full verify ran inside `nexusai-lock.sh jest` with tags `d2074-proto1`, `d2074-proto2`, `d2074-lane-scratch` and `d2074-verify-update`.
  - Each acquisition wrote and moved aside the lock's own ticket and owner files under `!CODING/Datasec/NexusAI/session-tools/locks-laptop-1017/`. That is the only write under `!CODING`.
  - No other holder was present, and each lock was acquired after 0 s.
- **Writes in my own scratch clone (never pushed):**
  - a repo-local scratch identity `drafter-scratch@invalid.test`
  - branch `proto2074`
  - commits A and K
  - worktrees `t/rf`, `t/work`, `t/wt`, `t/x974` (holds the RD-974 probe edit) and `t/vupd`
- **Reads only toward the project:**
  - `git clone` read `2_Project_Files`.
  - `cat-file` / `config --get` (lengths only) on `.tools/b2069/clone` and other trees.
  - gh `-X GET` and Jira GET.
  - `cat`, `sed`, `awk` and `grep` of project files.
  - No card was read (the commission named none; the open card on the plain routes was not needed). No az, ssh, docker or HTTP to any hosted site.
- **Hook refusals:**
  - four Bash calls (two `git -C $var` write verbs the hook could not resolve; one `=====` separator; one `set -- $x` word split). I re-issued each with literal forms.
- **A zsh modifier fired in one read** (`$B:scripts`), the very fault the kit's HOLD names. Nothing was written; I re-ran it with the sha typed.
- **Never deleted:** the sidecar was written by `--init` and then filled by `os.replace`.

Read load for Tuesday (wc -c before this report): kit about 59.9 KB, sidecar about 14.3 KB, this report about 15.3 KB.

Last `date` of the drafting: Wed 25 Nov 2026 06:45:00 AEDT
