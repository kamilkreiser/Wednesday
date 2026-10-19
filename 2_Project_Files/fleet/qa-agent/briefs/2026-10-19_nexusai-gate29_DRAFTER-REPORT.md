# Gate 29 (RD-774 + RD-836, PR #97 @ 4c9b0d3) — DRAFTER REPORT, for Tuesday

Drafted 2026-10-19 from 16:27:21 AEDT (first `date` reading) to ~17:00 AEDT by a read-only drafting agent (Opus 5.5). I only read and measured. I wrote the three files in §1 plus this report, and scratch copies in my session scratchpad. Nothing was launched, mailed, published or pushed. I did not edit `inbox_routing.conf`.

## 0. BLUF

- **The kit is drafted as TIER 1 with a browser leg.** It has 20 rows: r0-r14, r7S, r12b and b1-b3. It also has a T0-T10 ruling set and the two verdict lines (RD-774+RD-836, and LANDING CHECKLIST).
- **Mode 0 applies today: the head already contains main.** Main is `7700caf`, and `4c9b0d3` is 3 ahead and 0 behind it. So in mode 0 the gated tree is the head itself. Nothing is merged and no counts are regenerated.
- **Main is about to move.**
  - Gate 28 finished (~16:55 AEDT).
  - At 16:56 S101O took the jest lock as `s101o-rd856land`, i.e. RD-856 is landing.
  - At 16:58 main was still `7700caf`.
  - If you stamp a moved main, T0 mode (a) applies: the gate rebuilds the merge in its own store and runs C-57.
  - I measured PR #97 against all three gate-28 heads. Each conflicts in the counts file only.
- **The launcher passes every content guard.** `bash -n` gives rc 0. On a scratch copy:
  - with the kit still slotted, it refuses at **32S** (19 slots) and **40** (route line);
  - a stamped copy passes (exit 0);
  - a wrong stamped tree refuses (exit 18);
  - a planted `qa-g28-*` lock holder refuses (exit 33).
- **The drafter found four things that change the gate. The kit makes each one a row:**
  1. **RD-836 does not cover the Settings page's own add/remove path.** `settings.js:1878` and `:1482` POST to `/api/settings/risk-definitions`. That route has no role check, and it syncs rows into the risk-condition store (add, delete, update). `POST /api/validate-condition {saveToDatabase:true}` also writes a row with no role check. And `GET /api/risk-conditions` auto-syncs from settings for any reader, which makes the gated `POST /sync` moot. None of these routes is changed by PR #97, so they are pre-existing siblings, not regressions. **T6 asks you to rule** whether they count against RD-836's "admin-only writers" claim (default) or become notes.
  2. **The builder's "planted UNION" is not a UNION.** `PLANTED_SQL` is a marker-alias SELECT. The kit has the gate plant its own UNION, ATTACH, PRAGMA, chained and comment shapes (T3).
  3. **The demo seed stamps one `created_at` on all 1445 rows.** That means T5, T6, T9 and T10 cannot fail on the seed. T2 adds a spread-date substrate.
  4. **Verify names are not "LOST 0".** RD-774 rewrites F-10: 13 old names are removed and 14 new ones added. r12 accounts for each lost name. This is a branch-side rewrite, not a C-215 rename.
- **Also found:**
  - **#221**, main's raw test-custom-query log line at `server.js:21592`, is removed by the head. The READY does not list it among the alerts expected to close at the land. It is on the landing checklist now.
  - **PUT has no text validation**, and neither does the risk-definitions route. So a CR/LF condition text can be planted over HTTP. The READY says "a stored record is the reachable source". r10 drives the HTTP sources.

## 1. Files written

| file | what | sha256 |
|---|---|---|
| `/Volumes/Laptop-DEV/TUESDAY/2_Project_Files/fleet/qa-agent/briefs/2026-10-19_nexusai-gate29-rd774-rd836.md` | the kit (250 lines, 116,977 bytes) | `0efe6a52e0d9048068f54b9bddfe120d08132cf4ace8a605fbe5d6a7dc6e2e3e` |
| `/Volumes/Laptop-DEV/TUESDAY/2_Project_Files/fleet/qa-agent/launchers/launch_qa_nexusai_gate29.sh` | the launcher (792 lines), copied from gate 28's with names, pins and paths changed, plus gate 27's browser checks | `c6b7da0e4a9f4e74956acf1bbf3379375600a43bf47d2dafbb8b63e8862bf320` |
| `/Volumes/Laptop-DEV/TUESDAY/2_Project_Files/fleet/qa-agent/briefs/2026-10-19_nexusai-gate29-READY-pr97.txt` | the READY mail copied whole (8,841 bytes: the FROM and AUTH header lines plus the body) | `ee6d589c74cdcc8a2dc87503c58c6d7808f94a75096eb31ff5ca035954e8acae` |
| this report | — | — |

- **READY copy.** `cmp` against your scratchpad file `ready97.txt` says IDENTICAL. The builder's `session-tools/s101/mail-31-ready-rd774.txt` is not byte-equal to the delivered body. The kit names the delivered copy as the one to read.
- **Launcher mode.** It is mode `-rw-r--r--`. I did not chmod it. It runs as `bash '…'`.

## 2. What I read (with refs)

- **Templates, read whole:**
  - gate 27's kit (amended, 243 lines);
  - gate 28's kit (stamped, 251 lines);
  - `2026-10-19_nexusai-gate28_AMEND-REPORT.md`;
  - gate 28's launcher (all 815 lines);
  - `BRIEF_TEMPLATE.md`;
  - `QA_AGENT_CHARTER.md`.
- **Templates, read in part:** gate 27's launcher (the browser-guard lines :82, :113-:114, :164, :376-:377, :395-:430); the gate-28 `.pre-stamp` kit (slot tokens only).
- **Commission inputs:** the READY (`ready97.txt`, whole); Tuesday's ANSWER-20, -21, -23 and -24 (`tuesday/briefs/2026-10-19_S101O_ANSWER-2{0,1,3,4}_*.md`, whole).
- **NexusAI source at `4c9b0d3`, read verbs only:**
  - `backend/services/riskSqlTemplates.js` (whole);
  - `backend/server.js`:
    - :2525-:2830 (requireAuth and the middleware order);
    - :4640-:4650 and :4920-:4945 (the scheduler executor);
    - :5030-:5060 (`ensureRiskCondition`);
    - :6945-:7060 (validate-condition);
    - :18780-:18810 (`requireAdminFor`);
    - :20670-:21330 (the risk block);
    - :21408-:21424 (run-now);
  - `backend/simpleDb.js` :125-:135 and :780-:873;
  - `backend/services/authEnforcement.js` around `adminGateRefuses` (:609-:660);
  - `backend/validators.js` :40-:75 and :220-:240;
  - `backend/logSafe.js` header;
  - `backend/services/riskAlertScheduler.js` :52-:125;
  - `static/js/settings.js` :1455-:1500 and :1840-:1900;
  - the rd774 test :1-:60 and :150-:441;
  - the spy preload (whole);
  - the F-10 diff in `security-fixes.test.js`.
- **Main `7700caf`:** the lines behind #220 (:21290), #221 (:21590) and #70 (`simpleDb.js:855-860`).
- **CLARIFICATIONS** (435,914 bytes, mtime 2026-10-18 22:35): the C-01, C-02, C-203, C-211, C-215 and C-216 headings at source. Every quote the launcher greps was checked with `grep -F`: each is found in CLARIFICATIONS and in the kit.
- **gh GETs** (NexusAI's `GH_CONFIG_DIR`, account `kamilDatasec`, 16:32 AEDT):
  - PR #97;
  - analyses on `refs/pull/97/head`;
  - open alerts on that ref;
  - #70, #220 and #272 with their instances on both refs;
  - main's open `js/sql-injection` and `js/log-injection` alerts;
  - PR #58's alerts;
  - the check runs on `4c9b0d3`.
- **Builder evidence (method only, hashed):** the listings of `rd774-char/` and `rd774-runs/`, and `rd774-char/main-888203c.txt` (whole, 13 lines).

## 3. Premises the kit rests on, with sources

All of these are MEASURED unless marked otherwise.

1. **Pins.**
   - Origin read by `ls-remote` at 16:28:10 and 16:58:04 AEDT (rc 0, 1 attempt each): main `7700cafd33ca8a329e1e7905081d869e83c6ccb5`; `refs/pull/97/head` = `refs/heads/rd-774-risk-sql-templates-s101o` = `4c9b0d36993f1e78c8f23cd9e1216200550324b8`.
   - Trees: head `26f5dd7e…`, `360cd82` `a02a8755…`, `63bef65` `2b20a25e…`, main `ba9581ab…`.
   - Parents: `360cd82` = `63bef65` + `7700caf`.
2. **Commit counts.**
   - `7700caf..4c9b0d3` = 3, left-right `0 3`.
   - `888203c..4c9b0d3` = **5**, because the merge brings in `3047ae9` and `7700caf`. First-parent = 3.
   - My first draft said "3 over 888203c". The scratch `--check` caught it (exit 8). The kit and launcher are corrected, and the kit records the correction.
3. **Conflicts.** I used the legacy stdout-only merge-tree four times. `.git/objects` held 90 files before and after.
   - PR #97 against `f9649dc` (RD-476), `1da0bd4` (the RD-856+857 stack) and `f15217c` (the C-170 delta): conflict markers only in `scripts/verify-expected-counts.json`.
   - `888203c 63bef65 7700caf`: one changed-in-both, the counts file.
4. **Counts.** `7700caf` is 4676/292; the head is 4700/293 (blob `ff5f5d7…`). The F-10 rename set comes from `git diff` of `security-fixes.test.js`: 13 names removed, 14 added.
5. **Census.** These come from `git grep` plus source reads at the head. They are WRONG 7 and 8 in the kit.
   - **Writers:**
     - POST, PUT and DELETE on `/api/risk-conditions`, and POST `/sync` (all gated);
     - `/api/settings/risk-definitions` (ungated);
     - `/api/validate-condition` save (ungated);
     - the GET list's auto-sync;
     - `ensureRiskCondition`;
     - the KQL-regeneration writes.
   - **Executors:** `runRiskConditionOnDatabase`, reached from `executeRiskConditionRows` (the scheduler and run-now), from `/:level?execute=true` and from `/:id/execute`. The only SQL text that reaches sqlite is `executeRiskTemplate`'s.
   - **The ungated-writer reading is READ-ONLY-INFERRED.** I booted no server; r7S measures it.
6. **CodeQL.**
   - The head's analyses are `1978185235`, `1978176566` and `1978176513`, all with results 0. Open alerts on the PR ref: 0.
   - `360cd82`'s js/ts analysis `1977664006` had results 1. That is the firing control.
   - #272's instance is `fixed@360cd82`. Its top-level `state` reads empty.
   - #70, #220 and #221 are open on main. #172 is the KQL sibling line (raw at the head's :5411).
   - The PR #58 control shows 4 alerts, all fixed.
7. **Floor.**
   - Tool sha256s are unchanged: lock `3c33f5ae…`, c57 `1ae84a10…`, c133 `6f938bfc…`.
   - T9 is unmounted. Node is v26.8.1, gitleaks 8.30.1, Chrome 155.0.8059.84, Playwright 1.62.1 in lock `19477a9`.
   - `models_latest.json` gives `levels.opus.model_id` = `claude-opus-5-5`.
   - Load was 6.73 at 16:31 and 10.89 at 16:56.
8. **The seed's single date** (READ-ONLY-INFERRED consequence): the last line of `main-888203c.txt` gives `"lo"` = `"hi"` = `2026-10-18 20:19:32`.
9. **The configured-deployment harness** comes from the rd774 test: local users, placeholder Entra, complete-first-run, CSRF, and a TEST-constant `SESSION_SECRET` in the child environment only.

## 4. Launcher verification (on scratch copies; the real launcher was run only through `bash -n`)

- `bash -n launch_qa_nexusai_gate29.sh` gives rc 0.
- **Why the checks ran on scratch copies.** The real launcher's guard 70 greps four `fleet/briefs_staged/` ruling files, and my commission fences me off that folder. So every `--check` ran on a scratch copy with that one block removed:
  - `/private/tmp/claude-501/-Volumes-Laptop-DEV-TUESDAY/f5b4105d-8dec-44c0-9b32-e05d9c0a2a47/scratchpad/g29_nostaged.sh`;
  - the control copies are under `/private/tmp/claude-501/-Volumes-Laptop-DEV-TUESDAY/f5b4105d-8dec-44c0-9b32-e05d9c0a2a47/scratchpad/g29ctl/`.
- **The removed block is carried verbatim from gate 28's launcher**, plus gate 27's driver-ruling grep. It passed `--check` for those drafters. **Tuesday's own `--check` on the real launcher is the first run of that block for gate 29.**
- **Slotted kit** (16:58): all content guards passed (`9 40 18T 18 6 18M 7 8 90 91 22 93 96 70 70N 31 10 17 11 12 13 14 15 20 41 82 19 24 53 71 76 77 78 79 38R 86`), then `REFUSING (32S): 19 at-sign SLOT placeholder(s)` and `REFUSING (40)` (no route line). EXIT=40.
- **Stamped-path controls** (scratch kit, scratch routing file):

  | test | result |
  |---|---|
  | positive (main `7700caf`, tree `ba9581a`, landed `none`, T0-T10 `default`, date 2026-10-19) | `all guards pass`, EXIT=0, report path `…/reports/2026-10-19-gate29-rd774-rd836/report.md`, MODE 0 |
  | wrong stamped tree | `REFUSING: M0 7700caf's tree is 'ba9581ab6d77', not the stamped tree '111111111111'`, EXIT=18 |
  | gate-28 holder planted in a scratch lock base | `REFUSING (33L): the jest lock is HELD by gate 28 ('qa-g28-C9')`, EXIT=33 |

- **Not exercised:** the mode-(a) branch of guard 18M. It needs a real main past `7700caf`, and none existed at 16:58. That branch does three things:
  - it NOTEs what landed;
  - it requires `landed` ≠ `none`;
  - it runs the legacy merge-tree of the head onto M0, which must show conflict markers in the counts file only.
  The function behind it is the same one the 360cd82 check (guard 22) proved.
- **Negative-control seats.** On this machine the launcher derived `78171` (Datasec/NexusAI-O) and `98361` (tuesday).

## 5. Slots left for Tuesday (19 occurrences, 17 names)

| slot | where | fill with |
|---|---|---|
| `SLOT:MAIN_SHA` ×2 | MAIN-STAMP line; PIN-HEADS MAIN row | origin main at stamp (the same sha in both places) |
| `SLOT:MAIN_TREE` | MAIN-STAMP line | `git rev-parse <sha>^{tree}` (`ba9581ab6d779e867edc066895f8481e5580691a` if it is still `7700caf`) |
| `SLOT:MAIN_LANDED` | MAIN-STAMP line | `none` if main is `7700caf`; otherwise what landed (e.g. the RD-856 land) |
| `SLOT:REPORT_DATE` ×2 | T9 and §11 | the same `YYYY-MM-DD` in both; recommended `2026-10-19` |
| `SLOT:RULING_T0` … `SLOT:RULING_T10` | TUESDAY'S RULINGS | `default` or your ruling (options and recommended defaults below) |
| `SLOT:SELF_CHECK_STAMP`, `SLOT:SELF_CHECK_NOTE` | top of the kit | LAST, by hand; keep the form `SELF-CHECK: re-read end-to-end for contradictions | …` |

The MODEL line is NOT a slot. It is `claude-opus-5-5`, and the launcher refuses unless it equals `models_latest.json`'s `levels.opus.model_id`.

**T-options, with the recommended default for each (full text in the kit):**
- **T0, the mode.** Default: mode 0 if main is `7700caf`. If main moved, (a): the gate rebuilds the merge, counts-only plus C-57, which is gate 27's route. (b) asks S101O to forward-merge first, which means a new head and a kit amendment.
- **T1, C-57/C-133 (mode (a) only).** Default (a): run the copy of the runner. Expect the 13 F-10 names to show as "missing". They are accounted for in r12 and named to you.
- **T2, the characterisation substrate.** Default (a): the demo seed plus a spread-date copy. (b), seed only, leaves T5, T6, T9 and T10 VOID.
- **T3, the SQL plant shapes.** Default (a): inert, marker-only UNION, ATTACH, PRAGMA, chained, comment and CTE forms, and nothing that writes. THE MODEL RULE may bite here.
- **T4, the CDN.** Default (a), as your gate-27 T5 (a) ruling.
- **T5, the configured deployment.** Default (a): the rd774 harness shape, with a per-boot random child `SESSION_SECRET` generated in-process; the host stays UNSET. (b) is open mode only, which leaves RD-836 PROVISIONAL.
- **T6, the sibling writers.** Default (a): they count against RD-836's claim, as a Major, never as a regression. (b) makes them N29 notes plus a candidate ticket. **This is the ruling that most changes the verdict.**
- **T7, the scheduler executor.** Default (a): drive it through POST `/api/notifications/run-now`, with mail enabled to an `.invalid` host under the belt. (b) is NOT RUN, relying on the code-identity read.
- **T8, the network.** Default (a): no npm audit.
- **T9, where the gate lives and Node.** Default as written.
- **T10.** None.

**Route line.** Add this exact line to `/Volumes/Laptop-DEV/TUESDAY/2_Project_Files/fleet/inbox_routing.conf`. The file has 234 lines and its last line is gate 28's, so this becomes line 235. I did not edit the file.

```
QA/NexusAI-gate29|tuesday-agent@agentmail.to|no
```

## 6. Unmeasured, and what I could not do

- **No server, jest, browser or lock ticket.** So every behavioural expectation in the rows is the drafter's reading or the builder's claim (RELAYED). That covers the viewer writing through the siblings, the PUT hostile values, the differential, the characterisation numbers and the browser outcomes.
- **I did not read Jira** (the RD-774 and RD-836 ticket text). "RD-836's scope" is taken from ANSWER-20 (*"POST /api/risk-conditions stores a client-sent sqlQuery with no role check"*) and from PR #97's title.
- **I did not read any `fleet/briefs_staged/` file.** The carried rulings (m), (n), (o), (u) and gate 19's RELEASE are quoted from gates 27 and 28's kits. One disclosure against that fence: I once ran `ls … | grep -c .` on `fleet/briefs_staged/` and saw only a filename count (3723). I opened no file there.
- **Not read:** gates 22-26's §3a (carried by reference, as in gates 27 and 28); gate 28's live `inst/` and its report body (only line 3, the status); the builder's `characterise.js` body (the gate must not read it before writing its references).
- **Whether `adminGateRefuses` lets a locally constructed S4 (sign-in unproven) state be reached** is unknown. The kit allows S4 to be NOT RUN, named.
- **The mode-(a) path of guard 18M was not exercised** (§4).

## 7. Hard limits kept

- **NexusAI repo:** read verbs only, with `--no-optional-locks`, plus the legacy stdout-only merge-tree. No fetch, pull, worktree, checkout, merge or `--write-tree`. `.git/objects` held 90 files before and after.
- **gh:** GETs only. **AgentMail:** not used. **HTTP:** none to any app, demo or production host.
- **Datasec paths only.**
- **Writes:** the four files in §1 (via Write and Edit), plus scratch files in my session scratchpad. Those are `git show` copies, merge-tree outputs and the `--check` scratch copies of the launcher and kit.
