# WED-154 measurement: old Secuura/Blockchain (Platform K) files and old tests -- 2026-10-19 (read-only)

> **CORRECTION 2026-10-19 08:07 (Wednesday, from Seat D 20th's STOP at removal time):** the squash test spliced the changed-file list UNQUOTED, so a changed path with a space word-split and `git diff --quiet` compared nothing and exited 0. **27 of the 173 W worktree candidates were never proven merged** (each has the same two `Projects Documents/*.html` files differing from develop; develop's copies are newer). **Provable W candidates: 146** (53 ancestor + 93 squash). Tool fixed (`tools/storage_dryrun_secuura.sh`, backup `.pre-1019-quotepathspec`: NUL-safe quoted literal pathspecs, rc read three ways, stderr kept), arms (s)/(s2) added and red-proofed against the old tool. The 27 are round-2 material under a named predicate, Kam's to approve.

Measured 2026-10-19 ~06:30-07:30 AEDT. Nothing was removed, moved, renamed or written in any project. Only writes: this folder, the arms/tool files in Wednesday's tree, and the session scratchpad (`.../scratchpad/storage/`). Git on `!CODING` used read verbs only (rev-parse, symbolic-ref, merge-base, diff, log, status with `GIT_OPTIONAL_LOCKS=0`, ls-files). No fetch.

**Trees covered (every number below names its tree):**
- B = `/Volumes/DevMASTER/!CODING/Secuura/Blockchain/` (the project folder, `du -sk` allocated KiB, shown as GiB).
- LM = `/Volumes/DevMASTER/WEDNESDAY/2_Project_Files/local-model/` (Secuura run dirs, spark cache/work, hosted/work only; `models`, `omlx`, Ollama stores are out of scope).
- Drive context: `/Volumes/DevMASTER` 1.8 Ti, **1.6 Ti used, 91%, 178 Gi free** (`df -h`, 07:2x). The 2026-10-05 hygiene policy says "immediately when a drive passes 85% used". `/Volumes/G-DRIVE` is mounted: 11 Ti, 7.3 Ti used, **3.6 Ti free** (`df -h`; nothing written there).
- Candidate = passes the proposed "not needed" predicate in the tool. It is a PROPOSAL; nothing is authorised by this file.

## 1. Class table (FOUND / TESTED / HOW)

| Class | FOUND (count, size, tree) | Age (newest..oldest idle; >7d / >14d / >30d) | CANDIDATE (count, size) | "Not needed" predicate and how checked |
|---|---|---|---|---|
| **W** git worktrees + deploy clones | B/worktrees: 568 dirs (567 git checkouts + `.seat-claim-s158`, no .git), **602.1 GiB**, 416.3 GiB of it node_modules; B/deploy-clones: 10 clones, 6.3 GiB. Total 578 items, 608.4 GiB | worktrees 2.9d..42.2d; 554 / 484 / 118 older than 7 / 14 / 30d | **181 items, 200.4 GiB** (173 worktrees = 53 ancestor + 120 squash, + 8 deploy clones, all ancestor) | HEAD is an ancestor of the LOCAL `origin/develop` (5d1be7b, 2026-10-19 04:10, no fetch) OR every file the branch changed since merge-base is byte-identical in develop (squash test: `git diff --quiet HEAD origin/develop -- <changed files>`), AND `status --porcelain` empty, AND idle >= 7d (newest non-node_modules file, `stat -f %m`), AND not live. KEEP reasons seen: 368 UNMERGED (387.2 GiB), 22 DIRTY (10.4 GiB), 5 young <7d (9.4 GiB), 1 no develop ref (deploy-clone seatD18), 1 not a git checkout |
| **N** node_modules in working copies W kept | the same trees; 107 KEEP working copies hold node_modules idle >= 14d | idle 14.1d..107d | **107 dirs-sets, 166.2 GiB** (tool total 170,156 MB). Not double-counted with W | `node_modules` (find depth <=5, `du -sk`) in a working copy that is not live, idle >= 14d. Regenerable by `npm ci`, never in git. W candidates already contain ~139 GiB of node_modules (20.3 + 118.8), so W + N together = **~371 GiB** |
| **T** test artefacts | B/worktrees (+deploy-clones), dirs named coverage / test-results / playwright-report / allure-* / .nyc_output: **4 dirs, 2.7 MB** (seat-a, ks734). `*.log` > 512 KB under worktrees/deploy-clones/5_Project_History: **0 files** | 39.5d..41.4d | 4 dirs, 2.7 MB | untracked (`git ls-files` empty), idle >= 14d, not live. `reports/` dirs (12 found, e.g. `systemTest/akto/output/reports`) are excluded: tracked-looking output, not proven regenerable. **Old tests are not where the space is**: the weight is node_modules in the working copies that ran them |
| **E** 5_Project_History evidence | B/5_Project_History: 652 entries, **5.2 GiB** (quarantine/ 2.2 GiB; seatR-44th 0.4; seatD-4th 0.3; s232 0.3). Regenerable parts only: 6 items (clones / node_modules), 3.9 GiB | 3 young, 2 unmerged | **1 item, 1.4 GiB**: `quarantine/2026-09-15-s233/worktree-ks679/.../node_modules` | node_modules or a clean scratch clone with HEAD in origin/develop, idle >= 14d. The report files, evidence/, mail/, history.md, HANDOVER files are RECORDS and are never candidates (the rest of the 5.2 GiB: KEEP) |
| **P** seat scratch (B/scratchpad) | j7 10.9 GiB, j9 6.4, j8 4.3, j12 1.6 (+v9) = **23.1 GiB**, 43 items (clones, wt*, pg data, logs) | 33 young (<14d), **6 LIVE (<48h, all in j12)**, 4 unclassified | **0** | scratch clone (clean, HEAD in origin/develop, idle >= 14d) or node_modules; unclassified folders (no clone, no node_modules, e.g. pg data) are listed KEEP for the owner. Zero is real: nothing is 14d old yet (positive control: arm (y) reads a planted old merged scratch clone as CANDIDATE) |
| **R** local-model runs | LM/runs: 853 dirs, **19.1 GiB** (`ab_ornith15_2026-10-08` alone 15.2: cache 10.2 + clones 5.1). Regenerable parts: 12 clone/cache dirs, 18.1 GiB | 3 young (the ab_* run), 9 clones 31.8..32.0d old | **9 clones, 2.9 GiB** (`runs/*_pm.*/clone`, `next17d_*/clone`) | `clone/ clones/ cache/ work/` subdir of a run, idle >= 14d, not held by a process; the run's record files (out.md, checker, run.log) stay. `ab_ornith15` (15 GiB) becomes eligible ~2026-10-22 |
| **S** spark cache/work | LM/spark/cache/work: 127 per-round work dirs, **42.2 GiB** (~350 MB each, clone + quarantine); spark/cache/src 0.6 GiB (keep) | 1 live pid; 0 older than 14d; 42 older than 7d (13.9 GiB), 67 older than 2d (22.2 GiB) | **1 dir, 0.3 GiB** under the runner's own 4 guards | `prune_work.py` guards, read-only: marker `.spark_round_work`, run_dir has a verdict row in `spark/done.md`, marker pid dead, idle >= 48h. **126 of 127 fail guard 3 (no done.md row)**: aborted/control/r2 rounds and today's in-flight ones. 126 have a dead pid and an existing run dir (record is safe): **a proposed relaxation (pid dead + run dir exists + idle >= 7d) would release 42 dirs / 13.9 GiB now and ~22 GiB after 2 days.** That is a policy choice for Kam, not made here |
| **H** hosted work | LM/hosted/work: 146 dirs, **0.44 GiB** | all 9.5d or younger | **0** (all <14d) | idle >= 14d; zero is age, not a bug (control: same predicate fires for R and S) |

**Candidate total, de-duplicated (tool run): 371.3 GiB** (W 200.4 + N 166.2 + T ~0 + E 1.4 + R 2.9 + S 0.3). W+N alone is 366.6 GiB of that; against 178 GiB free on a 91%-full drive.

## 2. Policy classes already covered vs new (against `1_Project_Definition/Policies/2026-10-05_drive-hygiene-policy.md` and `SURVEY.md`)

Already covered by the 2026-10-05 policy (class names and predicates reused):
- **Class 1 "working copies whose work is merged, tree clean, > 7 days"** = W (also the clone parts of E, P, R). Reused: merged test = ancestor OR squash-equivalent (the survey's file-equality test); `gh pr list --state merged` (test a) is NOT used because the Secuura `gh` identity is not loaded here. Idle = newest non-node_modules file.
- **Class 2 "regenerable leftovers > 14 days"** = N, T, and node_modules in E/P.
- Never-moved list (`.git`, credentials, records, last 3 days, live holder, dirty/unpushed) = honoured. Tighter than the policy: live = modified in the last 48h (the brief's rule) AND candidates must be idle >= 7d; both fit inside the policy's 3-day rule.
- Policy class 3 (Docker.raw, Ollama duplicate) is not Secuura/Blockchain and was not re-measured.

NEW for Secuura/Blockchain (not in the 10-05 policy or survey):
- **S** spark/cache/work (42.2 GiB, did not exist as a class on 10-05; the runner has its own `prune_work.py` and 126 of 127 dirs slip past its guard 3).
- **R** run-dir scratch (clone/cache inside a record folder), **H** hosted/work, **P** `Blockchain/scratchpad` seat scratch (23.1 GiB, not in the 10-05 survey), **T** test output (tiny), and **E** regenerable parts inside the evidence folders (the survey said "records stay"; this splits record files from regenerable node_modules/clones).
- A **tool + scheduled mechanism** (dry-run on a cadence) rather than a survey; the 10-05 policy's "weekly re-run the survey" becomes `storage_dryrun_secuura.sh`.

Differences from the 10-05 survey worth knowing: it counted 181 squash+ancestor "SAFE" worktrees (163.7 GB); today 173 qualify (158.2 + 37.5 GiB incl. nm; the others since merged-cleanup or aged). The survey's "221 where the ks id is in the develop log but files differ" are KEEP/UNMERGED here (strict) and are not measured by PR state (see section 5).

## 3. Top 25 directories by size (B, project folder; DevMASTER numbers are `du -sk` GiB)

Whole-folder context: `B/worktrees` 602.1; `B/scratchpad` 23.1; `B/2_Project_Files` 21.4 (main checkout, never a candidate); `B/deploy-clones` 6.3; `B/5_Project_History` 5.2; `B/local-deploy` 0.4; `B/6_Tools` 0.3; `B/4_Credentials` 0.2 (credentials, never a candidate).

| # | GiB | Directory (under B) |
|---|---|---|
| 1 | 602.1 | worktrees/ (all 568 dirs; the folder itself) |
| 2 | 23.1 | scratchpad/ |
| 3 | 21.4 | 2_Project_Files/ (PROTECTED: main checkout) |
| 4 | 10.9 | scratchpad/j7 |
| 5 | 6.4 | scratchpad/j9 |
| 6 | 6.3 | deploy-clones/ |
| 7 | 5.2 | 5_Project_History/ |
| 8 | 4.3 | scratchpad/j8 |
| 9 | 2.9 | scratchpad/j9/ks1385 |
| 10 | 2.9 | scratchpad/j9/ks1114 |
| 11-25 | 2.7 each | worktrees/s-ra3-ks1136, s-ra4-ks1436, s-g7-ks1410-transfer, s-ra44-m1455, s-ra42-m1454, s-ra41-m1452, s-ra40-m1451, s-f13-b2, s-ra37-m1450, s-f14-c1, s-f15-c2, s-f16-d1, s-ra36-m1448, s-f12-ks591, s-ra35-m1449 (each ~2.7 GiB, 10-20 days idle; ~150+ other worktrees are the same size, all dominated by a 1.4-2 GiB node_modules) |

Next sizes: 5_Project_History/quarantine 2.2; scratchpad/j7/wt1119, wt759, wt1453, j8/dev405e, j8/pred1542 ~2.2 each; j7/iso1453 1.7; j12 1.6; deploy-clones/seatD18 1.0. Largest LM (first scan 06:2x): `spark` 39.2 GiB (of which `cache/work` 38.5), `runs` 19.1, `omlx` 2.0, `hosted` 0.56. The later tool run counts 42.2 GiB in `spark/cache/work` because the runner added ~30 work dirs in between.
Method: worktree sizes = per-dir `du -sk` (sum 602.06 GiB, equals the folder `du -sk` 631,305,144 KiB); other rows from `du -k -d 1/2`. The list ranks directories, so the 568 worktree dirs, which are all ~0.3-2.7 GiB, fill places 11+.

## 4. Live-seat exclusions found

- **Live Secuura seat:** tmux session `fleet`, window `main`, pane pid 41549 (zsh running `Launch_Claude.command`, echo marker `[cockpit] Secuura/Blockchain-R`, title "Blockchain session startup and daily plan"). Its claude process **pid 41551** has cwd `/Volumes/DevMASTER/!CODING/Secuura/Blockchain` (`lsof -a -p 41551 -d cwd`). Children: 41673 (`claude-bridge.js --mcp`) and 41674 (`npm exec @playwright/mcp`), cwd = the same project root. **None has a cwd inside `worktrees/`, `deploy-clones/` or `scratchpad/`**, so no worktree is excluded by cwd. Control: the tool's live detector (lsof cwd + ps command-line scan) is exercised by arm (c) for recency; the cwd path is checked by the same `is_live()` and reports no hit on any worktree in the real run.
- **Recency (<48h) exclusions:** worktrees: **0** (newest worktree file is 2.9d old; control: fixture arm (c) reads a fresh folder as LIVE; the real run shows 6 P rows LIVE, so the check fires). `B/scratchpad/j12/*` has 6 folders modified in the last 48h (redfirst, rf1568, ks1612, devbase, e2e, logs) -> KEEP.
- Other live processes found outside the project (not candidates, outside both trees): `watch_r49.py` and a postgres under `/private/tmp/claude-501/-Volumes-DevMASTER--CODING-Secuura-Blockchain/.../scratchpad/` (Seat R's session scratchpad, not touched). Seat R's active gate clones may live there; **not measured**.
- Always excluded: `2_Project_Files` (main checkout, 21.4 GiB), `1_Project_Definition`, `3_Access_Keys`, `4_Credentials`, `5_Project_History` record files, history.md, HANDOVER files, dirty and unmerged working copies.
- `.seat-claim-s158` inside `worktrees/` is a seat claim marker folder (no `.git`): KEEP (listed "not a git checkout").

## 5. NOT measured

- Remote boxes **kintsugi and demo (docker images, rollback sets, build leftovers): UNMEASURED** (no ssh, per the brief).
- PR merge state via `gh` (Secuura identity not loaded): the 368 UNMERGED working copies (387.2 GiB) include ones whose PR is merged but whose files differ from develop (the 10-05 survey estimated 221 such). Likely more is eligible than 181; needs `gh pr list --state merged` through the project identity, or a fetch by the project seat. Local `origin/develop` is as known at 04:10 today; no fetch was done in `!CODING`.
- `git worktree list --porcelain` was **refused by the workspace hook** (`pretooluse_no_cd.sh` treats any `git ... worktree` as a write verb for another project). Registration was therefore read from files: `B/2_Project_Files/.git/worktrees` has **557 admin entries** vs 567 worktree checkouts under `worktrees/` (10 not registered there: standalone clones or entries pointing elsewhere; not reconciled). Removing any worktree folder leaves its admin entry: pruning registrations is a write verb and belongs to the Secuura seat.
- Remote/unpushed check (`ls-remote`) not run; a clean working copy contained in local origin/develop is already pushed, but UNMERGED+clean ones are not tested for "sha exists on a remote branch".
- Docker images/volumes on this Mac, `/Volumes/Development` (NAS), `6_Tools`, `local-deploy` (0.4 GiB node_modules), `Backup`, `4_Credentials/.azure` caches: sized only at folder level, no class predicate.
- Hidden tool caches under `.claude/`, Ollama/omlx model stores (separate policy).
- LM `runs/` records themselves (0.9+ GiB of out.md/logs, 853 dirs): kept as records, not classified.
- A time series: this is one snapshot; growth rate (S gains ~29 work dirs/day, ~10 GiB/day) is inferred from dir dates, not measured over time.

## 6. Arms output (full run 2026-10-19, `tests/storage_dryrun_arms.sh`, pass=17 fail=0)

```
ARM PASS: (a) old merged clean working copy -> CANDIDATE
ARM PASS: (b) dirty working copy -> KEEP (DIRTY)
ARM PASS: (c) folder modified now -> KEEP (LIVE)
ARM PASS: (x) old unmerged working copy -> KEEP (UNMERGED)
ARM PASS: (x) node_modules inside a W candidate is not double-counted in class N
ARM PASS: (y) old merged clean scratch clone in scratchpad -> CANDIDATE
ARM PASS: (y) node_modules inside a candidate clone not listed twice
ARM PASS: (x) fixture files byte-identical before/after (tool wrote nothing but its report)
ARM PASS: (x) fixture report written
ARM PASS: (d) self-check refused the planted copy (rc=3, no report dir created)
ARM PASS: (d2) genuine script passes its own self-check
ARM PASS: (d3) planted 'mv /a /b' refused
ARM PASS: (d3) planted 'git worktree prune' refused
ARM PASS: (d3) planted 'find /x -delete' refused
ARM PASS: (d3) planted 'rsync -a --delete /a /b' refused
ARM PASS: (d3) planted 'git clean -fd' refused
ARM PASS: (e) real run rc=0, report written: .../dryrun_2026-10-19.md (208470 bytes)
ARMS: pass=17 fail=0
```

## 7. Files

- Tool: `/Volumes/DevMASTER/WEDNESDAY/2_Project_Files/tools/storage_dryrun_secuura.sh` (no removal/move/rename verb; self-check refuses to run otherwise; refuses if DevMASTER is unmounted; bash 3.2; absolute paths; stderr kept). The real run takes about 25 minutes (du over 600 GiB, six parallel probes), so schedule it off-hours.
- Arms: `/Volumes/DevMASTER/WEDNESDAY/2_Project_Files/tests/storage_dryrun_arms.sh` (set `ARMS_FIXTURE_ONLY=1` to skip the 25-minute real run (e)).
- First dry-run report: `/Volumes/DevMASTER/WEDNESDAY/0_Brain/reference/2026-10-19_storage-policy/dryrun_2026-10-19.md` (every candidate path with size, age, verdict).
- Raw measurements (scratch): `/private/tmp/claude-501/-Volumes-DevMASTER-WEDNESDAY/ff943889-d9ba-463a-a66e-300867d673bd/scratchpad/storage/` (`wt.tsv`, `lm_runs.tsv`, `du*.txt`).
- Not done on purpose: no commit, no Linear write, no mail, no artifact.
