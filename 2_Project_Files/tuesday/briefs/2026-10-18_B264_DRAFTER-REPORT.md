# B264 DRAFTER REPORT (HPSM-POC hosted deploy of the PR #159 squash)

**Brief:** `/Volumes/Laptop-DEV/TUESDAY/2_Project_Files/tuesday/briefs/2026-10-18_B264_SEAT-F_hpsmpoc-hosted-deploy-pr159.md`, 124 lines, UNSTAMPED: placeholder `@MAINSHA@` on 29 lines (39 occurrences). sha256 `9ecbd521c9c498b6a4379453de07e97ac828aa497f1716d4bad45b24c509ea67` before this report was written.
**B number:** B264 was free in both folders (`tuesday/briefs/` and `HPSM-POC/1_Project_Definition/Briefs/`: 0 `B264` names).
**Template:** the B260 brief, its ANSWER-1 and ANSWER-2 and its DRAFTER-REPORT, all read whole. Also read whole: `B260_STATUS.md` (384 lines), `B262_STATUS.md` (170), `B263_STATUS.md` (355, read in two parts). I read C-112 (records `CLARIFICATIONS.md:1344-1422`) from a scratch copy.

## Tuesday must stamp / decide
1. **Stamp `@MAINSHA@`** after the merge, once `git/commits/<sha>` reads tree `5180070b0f314adf2da47c445cdba25bfbb07a57` with one parent `d1fca809…`. Keep the `.pre-stamp` copy, which is the refusal control.
   - **PR #159 is not mergeable yet** (04:57Z): `mergeable_state` blocked, and `ci` 39098487912 is in progress (`api (ASP.NET Core)` and both SQL Server shards running).
   - CodeQL "PR #159" 39098486613 is already `success`, as are the check-runs `CodeQL` and `Analyze` ×4.
2. **RULED, start-up pair 3213 + 3211.** Recommend YES: ANSWER-2's five conditions become the B264 brief's rule, as step 7 is written.
   - C-112 records ANSWER-2 as *"for this deploy only … not a standing acceptance"*, so it does not carry over by itself. B264 needs its own ruling.
3. **RULED, guard chunks and auth traces.** Recommend STRICT.
   - The guard chunks (`src_077gfht._.js`, `src_0fsk14j._.js`) and the 4 auth `route.js.nft.json` traces should be byte-equal, because `guard.ts`, `bff.ts` and `entra.ts` are not in the range. Any difference is a STOP.
   - I did not measure whether Turbopack's cross-chunk references can change these files when only `_1dnntxr._.js` changes. STRICT may cost a round, as B260 round 1 did.
4. **RULED, Pkcs expectations.** Recommend UNCHANGED: `2 · 2 · 2 · 121`, and `deps.json` equal to `d1fca80`'s `92eb15a7…`.
5. **RULED, B263-1 (Minor).** The BFF does not count a file part named by a MIME encoded-word, and -276 adds 49 spellings to that. Recommend it DOES NOT BLOCK the deploy:
   - the gate verdict is GO WITH FINDINGS, with 0 Blocker and 0 Major;
   - the API's own total still refuses the form (422, measured by B263);
   - the BFF's 21 MiB cap bounds the extra to about 1 MiB.
6. **RULED, no POST to hosted.** Recommend YES, as in B260's stamp. -276's counting and `Connection: close` stay NOT TESTED on hosted.
7. **Completion check location:** a slot is left in the stamp.

## Measured (my own reads, UTC 2026-10-18T04:57–05:00Z)
All GitHub reads were GETs (`gh api`, project `GH_CONFIG_DIR`, `kamilDatasec`).
- **Target tree:**
  - `git/commits/094602f…` has tree `5180070b0f314adf2da47c445cdba25bfbb07a57`, which starts with `5180070b0f31` as B263 `:17` says. Its parent is `78df292…`.
  - Control: `rev-parse 094602f^{tree}` in `.tools/b263/repo` gives the same tree.
  - PR #159's test merge `98695bcd…` has the same tree, with parents `d1fca80` and `094602f`.
  - `d1fca80`'s tree is `a083966f…` (= B260).
- **Refs:** main is `d1fca809…` and the branch is `094602f…`. PR #159 is open, `merged=false`, base `main`.
- **Range** (`compare/d1fca80...094602f`, files fit on one page):
  - `ahead_by` 10, `behind_by` 0; 12 files, +741 −62. `git diff --shortstat` in B263's clone agrees.
  - Classified: 1 web server file (`formGate.ts` +22 −10); 1 api code file (`ImportEndpoints.cs` +4 −1); 3 web tests; 6 api test files (2 added); 1 infra test.
  - 0 scripts, migrations, settings, `.csproj`, `package*.json`, `.github`, `.bicep` and start-up files.
- **Risky pathspec over `d1fca80..094602f`:** exactly `M infra/tests/test_deploy_hpsmpoc208.py`. Control: the same pathspec over `787d159..d1fca80` gives 2 lines.
- **Other range checks:**
  - Migrations 84 = 84 (diff 0).
  - Start-up files in the range 0. Control: 5 under `api/src` (B260 counted 7 "in the tree", a wider scope).
  - Added config-pattern lines in non-test `api/src` + `web/src`: 0. Control: 4 in `api/tests`.
  - The `appsettings.json` blob is `f10fcc8c…` at both commits; `:17` is `"ImportsEnabled": false`.
- **Import gates:** `ImportEndpoints.cs:425` at tip (`:422` at `d1fca80`) and `AssessmentModule.cs:123` at both. The new catch is at `:137-140` at tip (verified by `git show | sed -n`).
- **NEW WORDS (from the compare patches):**
  - The literals on added non-comment code lines are `";"`, `"="`, `"name"` and `"files"`, all in `formGate.ts`.
  - The number of lines holding each in `formGate.ts` is 2/1/1/3 at both commits.
  - `ImportEndpoints.cs` adds 0 literals.
- **formGate importers at tip:** only `web/src/server/bff.ts:14`. `guard.ts:12` names it in a comment only.
- **d1fca80 packages** (in `wt-B260/out/…`, sha256 and Python `zipfile`, read-only):
  - api.zip `54dbc813…`: 121 files, Pkcs at 2 paths. web.zip `e4580b17…`: 1,874 files. Both equal `B260_STATUS.md:125`.
  - 7 `route.js.nft.json` files.
  - The formGate literals ("the files are over their total", "the upload was too slow", "latin1") appear ×1 each, only in `.next/server/chunks/_1dnntxr._.js`. `content-disposition` appears ×2 in that chunk, and the token `complete` ×1.
  - The guard literals and `form-data[ \t]*(;|$)` appear only in `src_077gfht._.js` and `src_0fsk14j._.js`.
  - The 787d159 packages: 121 / 1,874 files.
- **Worktrees** (`git --no-optional-locks`):
  - `wt-B260` HEAD `d1fca809…`, `wt-B256` HEAD `787d159…`, `wt-B253` HEAD `72073da…`; each has 0 tracked changes.
  - `.tools/b264`, `.tools/wt-B264` and `.tools/.git-lock` are absent.
  - `.tools/b260/` has 99 entries, including `webid260.py`, `nftcmp260.py`, `class3260.py`, `rollback260.zsh` and `postmerge255.sh`.
  - `id.zsh` sets `SHA=d1fca80` and `OLDSHA=787d159`. `rollback260.zsh` moves into `wt-B256` and deploys `$OLDSHA`, so the second fallback runs unchanged from `.tools/b260/`.
- **CI runs and artifacts:**
  - `d1fca80`: `ci` 39077252343 and "Push on main" 39077252179, both success, attempt 1.
  - Way back, run 39077252343: web 12117378517 (15,359,012 B, expires 2026-10-24T23:08:02Z) and api 12117432659 (49,629,101 B, expires 2026-10-24T23:14:33Z), both `expired=false`.
  - Second fallback, run 39001143811: web 12089850327 (expires 2026-10-24T04:11:54Z) and api 12089267777 (expires 04:12:30Z), both `expired=false`. That run now shows `run_attempt` 2; the deploy artifacts are attempt 1's (B256).
  - `72073da`, run 38974522883: web expires 2026-10-23T22:21:13Z. I did not put it in the brief.
- **Code scanning:** 0 open alerts on main; control: 1 in any state.
- **Records:**
  - `HPSM-POC-analysis` main is `5d45352a4b324c20f6cde86f2822ff41c2cbb7ce` ("Records: B261 … (#119)", 01:26:02Z).
  - `CLARIFICATIONS.md` has 1,422 lines. C-105 is still at `:1235`, and the highest entry is C-112 at `:1344`.
- **Ports:**
  - `lsof` LISTEN across 6800–7299 shows only 7000 (`ControlCe`). Control: 10 listeners in total.
  - `lsof -iTCP:7160-7169` gives rc 1.
  - From the B258–B263 briefs: 6980–6989 (B258, B262), 6990–6999 (B260), 7140–7149 (B259), 7150–7159 (B263); B261 none.
  - **I assigned 7160–7169.**
- **Pane:** `cockpit.sh status` lists `tuesday`, `QA/NexusAI-gate25`, `QA/NexusAI-gate26`, `Datasec/NexusAI-O` and `fleet-monitor`, so `Datasec/HPSM-POC-F6` is free. Two NexusAI QA gates are live; the brief tells the seat to keep local work light.
- **`brief_seat.sh`:** the exports are at lines 25-26. `PLAYWRIGHT` has 0 hits (control: `AZURE_CONFIG_DIR` 1).

## Could not measure (UNMEASURED in the brief)
- The merge, `@MAINSHA@`, its CI, packages and artifacts.
- PR #159's final `ci`.
- The real web differences at `@MAINSHA@`. My prediction is 14 same-path files: 9 build-id, 3 key, plus `_1dnntxr._.js` and the `v1/[...path]` trace. The `complete` count at tip is also unmeasured.
- Whether the guard chunks stay byte-equal.
- Anything hosted, including today's state, runtime and the start-up pair. I ran no `az` and sent no HTTP to the hosted site.
- Tuesday's completion-check record, and Jira.

## Conflicts / tensions found
1. **ANSWER-2's scope.** ANSWER-2 and C-112 say "THIS deploy only … not a standing acceptance". The task asked for its conditions as "the brief's standing rule for this deploy". The brief writes them as Tuesday's rule for B264 only and leaves a RULED slot, so Tuesday re-rules rather than inheriting.
2. **B260's template line "3211/3213/3214 0/0/0"** is superseded in B264 by the five conditions (B260 Open 3).
3. **`startscan.py`.**
   - B260 `:222` and Open 2 say it reads 0 on the StartupLogs format.
   - B260 `:279` says it fits the app docker log and agreed with grep in round 3.
   - The brief therefore uses the docker log with grep as the primary reader, and `startscan.py` only as a second reader on that format.
4. **Old vs new reader.** B260's step-5 comparison of the two live-check readers is dropped. `scripts/` is unchanged in this range, so the brief replaces it with a `git diff --quiet … -- scripts/` proof.
5. **The way back now runs from `wt-B260`.** That needs a new `rollback264.zsh` and `b264/id.zsh` (`OLDSHA=d1fca80`). `.tools/b260/` must stay unmodified so that `rollback260.zsh` still works as the second fallback.
6. **`RetryLimitExceededException` string count.** B260 used it as evidence (`:135`, `d1fca80` 1 vs `787d159` 0). The type is already referenced at `d1fca80`, so it cannot prove -274's new catch. The brief says not to use it.
7. **Records sha.** B262 F-8 and B263 cite records main `5d45352a`; that matches today's read. The B260 brief cited `2e284455`, which is now superseded.
8. **Gate findings carried, not blocking.** B263-2 (the Feedback context's migrations lock still waits only 30 s) means main's CI can still flake on the `__EFMigrationsLock` class. The brief keeps "a red main ci is Tuesday's to re-run".

## Not done
- No `az`, docker, HTTP to hosted, git fetch, pull, worktree or checkout, Jira or mail.
- Git use was `--no-optional-locks` read verbs only, in `.tools/b263/repo` and the worktrees.
- A guard hook refused my first attempt to list the zips with `unzip -Z1`, so I used Python `zipfile` instead.
- Scratch copies of `compare.json` and `CLARIFICATIONS.md` are in the session scratchpad. Nothing was written outside the two output files.
