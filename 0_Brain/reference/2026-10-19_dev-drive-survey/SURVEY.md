# DevMASTER dev-drive survey — 2026-10-19 (read-only re-run)

Trigger: DevMASTER passed the 85% line in the drive-hygiene policy (`1_Project_Definition/Policies/2026-10-05_drive-hygiene-policy.md`). Template: `0_Brain/reference/2026-10-05_dev-drive-survey/SURVEY.md`.
Read-only. Nothing was moved, deleted or renamed. No git write verbs, no `cd`. The only writes were this file and the session scratchpad `.../scratchpad/drivesurvey/` (scripts and raw `.tsv`/`.txt`).
**Scope:** `/Volumes/DevMASTER/WEDNESDAY`; `!CODING/Secuura` (Blockchain top-level total only); general top-level folders that belong to no client. Datasec gets one total per top-level folder and nothing inside.
**Frames.** "GiB" = allocated blocks from `du -sk` ÷ 1,048,576. Drive figures are `df`. "Age" = the directory's own mtime unless stated. The "<48 h" test is `find -name node_modules -prune -o -type f -mmin -2880`, which looks for any non-node_modules file changed in the last 48 h. Survey time: 2026-10-19 about 07:50–09:30 AEDT.

## Drives

| Drive | Used / size | % | Free | Frame |
|---|---|---|---|---|
| `/Volumes/DevMASTER` | 1.7 TiB used of 1.8 TiB (1,691 GiB of 1,863 GiB) | **91%** | 171.5 GiB (178 Gi at start of the survey; the drive is still filling) | `df -h` / `df -k`, 82 M inodes in use |
| `/Volumes/G-DRIVE` | 7.3 TiB used of 11 TiB | 67% | 3.6 TiB | `df -h` |

**10-05 comparison:** DevMASTER then showed 1,436 GB used per `du`, 366 GiB free (about 1.5 TiB used by `df`). It now has **about 195 GiB less free**, even though 359 GiB was removed in between (below). G-DRIVE `Scratch Files` holds 158.1 GiB (`du -sk`), including `2026-10-05_DevMASTER_cleanup/WEDNESDAY_local-model_models_duplicate/models` at 127.8 GiB. The 10-05 BLUF said "move": that ran for the Ollama duplicate.

## Where the drive's bytes are (top-level `du -sk`, GiB)

| Folder | GiB | Whose |
|---|---|---|
| `!CODING/Secuura/Blockchain` | **658.9** | Secuura. Top-level total only; see the pointer below |
| `!CODING/Testing Agent MAIN` | **294.9** (Secuura QA projects: 294.6; `projects/hpsm` 0.10 and `projects/nexusai` 0.15 are Datasec, totals only) | general / Secuura |
| `WEDNESDAY` | **305.5** | Wednesday |
| `SYSTEM` (`ollama`) | **268.7** | general (live Ollama store) |
| `!CODING/Datasec` | 98.8 (10-05: 56.1) | Datasec. **One line only; Tuesday's seat, not read** |
| `TUESDAY` | 1.3 | Datasec coordinator. One line only |
| `Agentic Coding` 1.3 · `Claude to Claude` 0.87 · `Paperclip` 0.55 · `.fseventsd` 0.55 · `Secuura/Extranet` 0.55 · `tmp-qa962-mkwnwD` 0.32 · `.pnpm-store` 0.26 · `Family` 0.07 · `Notes (MASTER)` 0.03 · rest under 0.03 | | general |

Sum of everything measured: 1,632.7 GiB, against `df` used of 1,691 GiB. **About 58 GiB is unaccounted for.** Possible causes: the drive grew during the run, and unreadable system folders (`.Trashes` returned "Operation not permitted"; `.Spotlight-V100` and `.DocumentRevisions-V100` were not measured). No claim is made about what fills the gap.

**Secuura/Blockchain: 658.9 GiB (top-level `du -sk`) and nothing deeper.** Its worktrees, clones and test artefacts are being measured by another sub-agent for the separate storage policy: `/Volumes/DevMASTER/WEDNESDAY/0_Brain/reference/2026-10-19_storage-policy/` (`MEASUREMENT.md`, `dryrun_2026-10-19.md`). The 10-05 survey gave no Blockchain total, so there is no top-level comparison. Its worktree classes then summed to about 365 GB (A+B).

## Exclusions (live use and the 48 h rule)

- **Live Secuura seat:** tmux `fleet:main.1`, `@cockpit_name = Secuura/Blockchain-R`. Its claude is pid 41551; with its children (41673, 41674, 41845) it has `cwd` = `!CODING/Secuura/Blockchain` (`lsof -d cwd`). A live postgres has `cwd` `Blockchain/scratchpad/j7/pg/data`. Nothing under Blockchain is a candidate here.
- **Wednesday's own live use:** cwd `WEDNESDAY` and `WEDNESDAY/2_Project_Files/dashboard`. A running Spark round (`round.sh ... ks_1620_info --control`) has a `tsc` process inside `local-model/spark/cache/work/spark_secuura_2026-10-19_ks_1620_info-control_*`. That makes the 66 work folders from the last 2 days (22.1 GiB) live or excluded.
- **rsync** pid 45463, started 03:30, runs with cwd `/Volumes/DevMASTER` and `--backup-dir=/Volumes/Development/_nas_push_overwritten/...`. Not examined further. Nothing recommended below touches its backup target.
- **Anything modified in the last 48 h:** excluded per class (the test is stated in each row).
- The positive control for the 48 h test is in "Controls".

## Reclaimable classes (biggest first)

Policy classes: 1 = merged and clean working copies older than 7 days; 2 = regenerable leftovers older than 14 days; 3 = superseded images, duplicate models, large archives that no tool references; NEVER = `.git`, credentials, records, anything changed in the last 3 days, anything live.

| # | Class (policy class) | Size | Count | Age | Verdict | GB a move/removal would free |
|---|---|---|---|---|---|---|
| 1 | **`Testing Agent MAIN/projects/secuura/reports/*/{wt*,work*,clone*,scratch*,tmp*}`**: per-run QA clones and worktrees (2). Includes each run's own `node_modules`. | **284.7 GiB** (55 dirs under 55 of 302 reports; the 302 reports total 294.5 GiB) | 55 dirs | 20.2–26.5 d. **Past the 14-day bar this time** (10-05 it was 6–13 d). No non-node_modules file changed in the last 48 h (0 of 55). | **Regenerable.** Drop the clones and worktrees; keep each report's `report.md`, `evidence/` and `mail/` (about 9.9 GiB across all reports). The 10-05 caution stands: confirm no open QA verdict points into these. Moving a whole report orphans nothing, since the worktrees link to a clone in the same report. 10-05 reference: 57 dirs, 291.5 GiB. **Regenerate, do not copy:** roughly 23 M small files. | **284.7** |
| 2 | **`WEDNESDAY/2_Project_Files/tools/omlx/models/`**, oMLX model folders, new since 10-05 (3). Qwen3.8-Flash-Next-oQ4e-mtp **99.0** · Qwen3.5-122B-A10B-4bit **64.8** · Ornith-1.5-35B-A3B-MLX-8bit 34.3 | 198.2 GiB (237 files) | 3 folders | Created 2026-10-08 (11 d), no file changed in 48 h (`find -mtime -2` empty) | **Keep Ornith-1.5**: `doctor.sh:245` checks that exact path and it is `night_run`'s default backend. **Qwen3.8-Flash (99.0): class-3 candidate.** Only `omlx_setup_and_download.sh` mentions it. It is not served; no omlx process is running and `lsof +D` on the models folder is empty. It re-downloads from Hugging Face. **Qwen3.5-122B (64.8): probable.** Only `omlx_serve.sh` mentions it (the generic serve script) and the `runs/ab_qwen122_2026-10-08` test was the use. The model choice is **Kam's call.** | **163.8** (99.0 sure; +64.8 on his word) |
| 3 | **`SYSTEM/ollama` (live store 268.7 GiB, 13 manifests)**: models whose names appear in none of the 35 Wednesday tooling files checked (see Controls): qwen3:32b-fp16 **61.0** · qwen3-coder-next 48.2 · qwen3-coder:30b 17.3 · codellama:13b 6.9 · phi3 2.0 · llama3.2:3b 1.9 · phi2 1.7 | 139.0 GiB | 7 models | Manifests 2025-09 to 2026-03 (7–13 months), none newer | **Probable (class 3, needs one check).** The check covered only Wednesday's scripts, doctor, PORTABILITY and fleet specs. It did not cover Secuura, Datasec or other agents, so run `ollama list` and ask first. Removal is `ollama rm`, not a move. Blob dedup between manifests was not measured, so 139.0 is an upper bound. Kept: ornith (referenced in 9 files), gpt-oss:120b/20b (60.9/12.8, referenced in 1 file), nomic-embed-text. 0 unreferenced blobs exist on disk (267.0 GiB, all manifest-referenced), so there is no loose-blob cleanup. | up to **139.0** |
| 4 | **`WEDNESDAY/2_Project_Files/fleet/qa-agent/gatesets/`**, old QA gate runs (1/2) | 27.9 GiB, of which `node_modules` 16.2 | 206 gatesets: **173 older than 14 d = 11.2 GiB**; 33 at 7–14 d = 16.7 GiB | 0 of 206 hold a non-node_modules file changed in the last 48 h | 173 older than 14 d: **class 2, regenerable** (all of it, not just `node_modules`; the gate verdicts sit in `0_Brain/reference/<date>_gate-*` folders, which this survey did not open). 33 at 7–14 d: wait for the 14-day mark. 10-05 reference: 94 gatesets before 09-21, 11.1 GiB. Merged-proof (class 1) was not run. | **11.2** now; +16.7 within 7 d |
| 5 | **`WEDNESDAY/2_Project_Files/local-model/runs/ab_ornith15_2026-10-08/`**: the Ornith-1.5 A/B test (1) | 14.9 GiB (cache 9.9, clones 4.9); all `runs/` = 19.1 GiB over 866 dirs | 1 dir; `runs/` aged: <2 d 74, 2–7 d 40, 7–14 d 111 (15.3 GiB), >14 d 642 (3.7 GiB) | 11 d; 0 of 753 `runs` dirs older than 7 d hold a non-node_modules file changed in the last 48 h | **Probable.** Experiment output, results are small (`tasks/` 27 MB). The cache and clones are regenerable. The ab_qwen122 run next door is 0.35 GiB. Keep the tasks and logs. Not proven merged. | **14.9** (+3.7 for the 642 old dirs) |
| 6 | **`local-model/spark/cache/work/`**: Spark work clones (1) | 42.2 GiB, 134 dirs: <2 d 66 = 22.1 (**live**, excluded) · 2–7 d 25 = 8.3 · **7–14 d 43 = 14.2** · >14 d 0 | | 0 of 68 dirs older than 2 d hold a non-node_modules file changed in the last 48 h | The 7–14 d slice is class 1 once merged-proof runs (`gh pr list --head <branch> --state merged` through the Secuura identity, or a tree comparison). Not run here: read-only, no `gh`. >14 d is empty because the 10-05 move already sent clones to G-DRIVE `2026-10-05_WEDNESDAY_spark-work-clones`. | **14.2** after proof |
| 7 | **`WEDNESDAY/2_Project_Files/fleet/state/t9_to_devlocal_2026-10-09.log`**, one sync log (3) | 3.86 GiB (4,146,753,564 B) | 1 file | Last written 2026-10-11 (8 d). No process has it open (`lsof` empty). | **Probable.** It is not in `5_Project_History/` (the records folder). The grep of `*.sh` and PORTABILITY for its name found nothing. Kam's call, like the 6.67 GiB 09-25 log below. | **3.9** |
| 8 | **Small regenerable dirs older than 14 d outside Blockchain/Datasec** (2) | 3.3 GiB: Agentic Coding 1.19 · Claude to Claude 0.70 · Extranet 0.55 · `tools/` (codex-cli etc.) 0.54 · Wednesday other 0.21 · Paperclip 0.09 | 69 dirs (node_modules, .venv/venv, dist, build) | Idle since Mar–Aug (newest files: Extranet 2026-08-04, Agentic Coding 2026-08-05) | **Regenerable.** Agentic Coding, C2C and Paperclip are idle, so their own agents or Kam can remove them. **Extranet is the coupled sibling of the live Secuura seat**, so ask that agent. 10-05 reference: about 3.5 GiB. | **3.3** |
| 9 | **Idle folders and strays (3)**: `Claude to Claude` whole 0.87 (newest file 2026-07-04) · `Paperclip` 0.55 (2026-05-19) · `tmp-qa962-mkwnwD` 0.32 (2026-09-13, drive-root stray) · `Personal Projects` 0.02 | 1.8 GiB | 4 | 6–5 months idle | Low value. Tiny gains. `tmp-qa962` is a stray QA temp and a safe tidy. | 1.8 (overlaps row 8 by about 0.8) |
| 10 | **Quarantines** in Wednesday (`_quarantine_*`) | about 0.4 GiB (`coordination/seat_scratch/_quarantine_2026-09-16` 0.33) | 25 dirs | 09-06 to 10-18 | Already quarantined. Not worth the churn. | about 0.4 |

**Summed (no double counting between rows 1–7 and 10; row 9 overlaps row 8):** about **637 GiB** at most, **about 299 GiB without a model decision from Kam** (rows 1, 4's 11.2, 8: 284.7 + 11.2 + 3.3). If everything lands the drive goes from 91% to about **57%**; the sure items alone bring it to about 74%.

### KEEP (listed because big)

| Path | Size | Why |
|---|---|---|
| `SYSTEM/ollama` — the 6 referenced models (ornith, gpt-oss, nomic-embed-text) | about 129.7 GiB | live store, referenced |
| `tools/omlx/models/Ornith-1.5-35B-A3B-MLX-8bit` | 34.3 GiB | `doctor.sh:245`; default night backend |
| `WEDNESDAY/5_Project_History` (incl. `2026-09-25_copy_DevMASTER_to_Laptop-DEV.log` **6.67 GiB**, 7,160,026,449 B; backups tarball 0.66) | 7.5 GiB | records (rule). The log is still the largest text file on the drive; Kam's call, unchanged since 10-05 |
| `local-model/spark/cache/work` entries from the last 2 days | 22.1 GiB | live |
| `Notes (MASTER)` 0.03, `0_Brain` 0.36 | | records |
| `Secuura/Blockchain` | 658.9 GiB | live seat; separate policy |

## Datasec (one line per top-level folder; not read)

`!CODING/Datasec` 98.8 GiB (10-05: 56.1 GB, so about +43 GiB; **Tuesday should look**) · `TUESDAY` 1.3 GiB · `Testing Agent MAIN/projects/hpsm` 0.10 GiB · `…/nexusai` 0.15 GiB. Nothing inside any of them was listed or read. Whether Tuesday has re-run its own survey is unknown.

## Comparison with 2026-10-05

| Class on 10-05 | 10-05 | Now | Note |
|---|---|---|---|
| Docker.raw (stale Docker Desktop image) | 231.6 GB | **gone** (`Docker - Containers/DockerDesktop` holds only `.DS_Store`) | Where it went is not recorded; it is not at depth 3 under G-DRIVE `Scratch Files`. Positive control: `find -type f` on that folder returned exactly 1 file. |
| Duplicate Ollama store (`local-model/models`) | 127.8 GB | **gone from the drive** | Now on G-DRIVE `Scratch Files/2026-10-05_DevMASTER_cleanup/…` (127.8 GiB). `local-model/models` no longer exists. |
| QA-run scratch clones (Testing Agent MAIN) | 291.5 (57 dirs) | **284.7** (55 dirs) | Same pile, now past the 14-day bar |
| Secuura worktrees A+B | 365 | not re-measured by this survey | Another sub-agent has it |
| Gatesets | 94 × 11.1 | 206 / 27.9 total, 173 older than 14 d = 11.2 | Grew; the oldest portion is unchanged in size |
| Regenerable older than 14 d (non-Datasec) | about 3.5 | 3.3 (plus gatesets 4.6, already in row 4) | |
| oMLX models | not there | **198.2** | New since 10-08, the biggest new Wednesday block |
| Spark work clones | (moved to G-DRIVE) | 42.2 (22.1 live) | 14.2 at 7–14 d |
| Ollama store | 268.7 | 268.7 (267.0 blobs) | unchanged |
| Datasec | 56.1 | 98.8 | +42.7; Tuesday's |
| Wednesday tree | not stated | 305.5 | of which tools/omlx 200.6, local-model 61.6, fleet 31.9, 5_Project_History 7.5 |

Net since 10-05: 359 GiB removed from the drive, yet free space fell 195 GiB. New growth: oMLX models 198, Spark work and runs 61, Datasec +43, Blockchain (not measurable here). The drive does not stay under 85% on moves alone: it needs a rule on what Spark and oMLX leave behind.

## Move-cost note (unchanged from 10-05)

QA scratch, gatesets and Spark clones are mostly node_modules (about 160,000 files each copy). The drive holds 82 M inodes. **Remove or regenerate; do not copy** to G-DRIVE. The oMLX models and the Ollama blobs are a few huge files: fast to move, and `rm`-free to delete. Worktree registrations (`git worktree prune`) are the owning project's agent's job, as before.

## Controls (every zero and every "empty")

- **"No file changed in 48 h" (rows 1, 4, 5, 6).** `recent.sh` reported 0 hits for 55 QA scratch dirs, 206 gatesets, 753 old `runs` and 68 old Spark work folders. **Positive control:** the same script on 5 `runs` dirs less than 2 days old returned 5 hits of 5 (4,264 KB). An earlier control on the 2 newest QA reports returned 0, correctly, because their newest dir mtime is 8 days.
- **"Not referenced" (rows 2, 3, 7).** `refs.sh` greps 35 files: `local-model/*.sh`, `spark/*.sh`, `night/*.sh`, `doctor.sh`, `PORTABILITY.md`, `IMPROVEMENTS.md`, `fleet/specs/*`. Positive controls from the same run: `ornith:35b` found in **9** files, `omlx/models` in 3, `gpt-oss:120b` in 1. An earlier run printed 0 for every name including the control, because zsh did not expand the globs; it was discarded and the loop re-run under `/bin/bash`. The zeros are therefore not from the first run.
- **"No process serves oMLX".** `ps` for omlx/mlx/ollama/vllm showed none (control: the same `ps | grep` matched the Spark `round.sh` and `ssh` tunnel lines); `lsof +D` on `tools/omlx/models` was empty (it takes the same `lsof` that listed 50-odd cwds earlier).
- **"No file over 500 MB" outside Wednesday (non-Datasec folders).** The find over Agentic Coding, Claude to Claude, Paperclip, Personal Projects, `.pnpm-store`, `tmp-qa962`, Family, Extranet and `platform-s-main` returned nothing at the 200 MB mark. Control: the same `find ... -size +500M` shape over `WEDNESDAY` returned 3 files (7.16 GB, 4.15 GB, 0.69 GB).
- **"Docker.raw gone".** `find -type f` on the folder returned 1 file (`.DS_Store`); the 10-05 survey had `Docker.raw` there.
- **Seat resolution.** `tmux show-options -p -t fleet:main.1` printed `@cockpit_name Secuura/Blockchain-R`; the process tree and `lsof -a -p <pid> -d cwd` are in the scratchpad (`seat_cwds.txt`, `all_cwds.txt`).

## NOT measured

- Anything inside `Secuura/Blockchain` (the storage-policy sub-agent's) and anything inside Datasec (Tuesday's).
- The node_modules share of the QA scratch (10-05 had 221 of 291.5 GiB). The 55 dirs were sized whole.
- **Merged state** of any working copy (rows 5 and 6): no `gh`, no git calls at all here. Both are labelled "after proof".
- Whether other agents use any Ollama model or any oMLX model (rows 2 and 3): only Wednesday's tooling was grepped.
- `/Volumes/Development` (the NAS), `.Trashes`, `.Spotlight-V100`, `.DocumentRevisions-V100`, APFS snapshots, `~/Library/Containers/com.docker.docker` (the live Docker disk, outside the drive). The 58 GiB gap to `df` stays unexplained.
- Conflict-copy and `.pre-*` counts: Wednesday only (2,158 files, negligible); not re-run for other folders.
- What the running rsync (pid 45463) is syncing.
