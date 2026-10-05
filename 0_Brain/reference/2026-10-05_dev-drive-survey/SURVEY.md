# DevMASTER dev-drive survey — 2026-10-05 (read-only)

Asked by Kam on 2026-10-05: find old or unused files that could be moved to `/Volumes/G-DRIVE/Scratch Files`. Nothing was moved, deleted or touched. The only writes were to this folder and the session scratchpad. Git was read-only (rev-parse, merge-base, diff, log, status, symbolic-ref, for-each-ref, ls-remote).
Drive: `/Volumes/DevMASTER` 1.8 TiB, 1.4 TiB used per `du` (1,436 GB), 366 GiB free, 58 M inodes in use. G-DRIVE has 3.8 TiB free (`df` only).

## BLUF — reclaimable by confidence (biggest first)

| Class | GB | What |
|---|---|---|
| **A SAFE** | **~167** | 181 Secuura worktrees whose HEAD is in `origin/develop` (53 ancestor + 128 squash-merged), all clean: 163.7 GB, 83.8 GB of it node_modules. Plus ~3.5 GB of non-Datasec regenerable dirs older than 14 days. |
| **B PROBABLY** | **~865** | QA-run scratch clones in Testing Agent MAIN: 291.5. Stale Docker Desktop disk image: 231.6. 242 unmerged-but-recoverable Secuura worktrees: 201.7. Duplicate Ollama model store: 127.8. Old Wednesday QA gatesets: 11.1. Small idle folders and quarantines: ~2. |
| **C KEEP** | — | Live Ollama store 268.7. KEEP worktrees ~34. Secuura main checkout 21.1. Records (`5_Project_History`) ~11. Datasec 56.1 (Tuesday's call). |

**Top 4 wins (~850 GB, about 60% of the drive):** QA scratch (291.5), Docker.raw (231.6), Secuura worktrees A+B (365), Ollama duplicate (127.8).
**Move-cost caveat:** roughly 50 M of the drive's 58 M files are node_modules. **Regenerate, don't move** (see MOVE COST).

## Class A — SAFE (regenerable, or provably merged and clean)

| Path | Size | Newest mtime | Why stale | How measured |
|---|---|---|---|---|
| `!CODING/Secuura/Blockchain/worktrees/` — 53 worktrees (list: `secuura_worktrees_classified.tsv`, class A, "ancestor") | 37.5 GB (nm 16.0) | none <3 d | HEAD is an ancestor of local `origin/develop` ef4901778; `status --porcelain` empty | `git merge-base --is-ancestor`; `du -sk`; `find -newer <2026-10-02 12:00>` excluding node_modules |
| same — 128 worktrees (class A, "squash-merged") | 126.2 GB (nm 67.8) | none <3 d | Every file the branch changed since its merge-base is byte-identical in develop. The content landed via squash merge. Clean. | `git diff --quiet HEAD origin/develop -- <files changed since merge-base>` |
| `!CODING/Agentic Coding` .venv ×7 + node_modules ×8 | 1.19 GB | 2026-08-03 | regenerable, idle 2 months | regen-dir scan (below) |
| `!CODING/Claude to Claude` node_modules ×2 + dist | 0.71 GB | 2026-03-24 | regenerable, idle since March | same |
| `!CODING/Secuura/Extranet` node_modules ×3 | 0.54 GB | 2026-08-03 | regenerable | same |
| Secuura `Blockchain/local-deploy`, `6_Tools/codex-cli` node_modules, `venv` | 0.92 GB | ≤2026-08-27 | regenerable, >14 d | same |
| `!CODING/Paperclip` node_modules | 0.09 GB | 2026-05-15 | regenerable | same |

## Class B — PROBABLY (old, needs a quick look before moving)

| Path | Size | Newest | Why | How / caution |
|---|---|---|---|---|
| `!CODING/Testing Agent MAIN/projects/secuura/reports/2026-09-2[2-9]*/{wt*,work*,clone*,scratch*,"spaced wt"}` — 57 dirs in 24 reports (`qa_report_scratch_dirs.tsv`) | **291.5 GB** | none <3 d (reports dated 09-22…09-29) | Per-run QA clones and worktrees, each carrying its own node_modules (221 GB). They are regenerable. `report.md`, `evidence/` and `mail/` are small and should STAY. | `du -sk` per subdir. **Only 6–13 days old, so under the 14-day bar.** Check that no open QA verdict still points into them. Worktrees there are linked to a `clone/.git` inside the same report, so nothing outside is orphaned. |
| `!CODING/Docker - Containers/DockerDesktop/Docker.raw` | **231.6 GB on disk** (994.7 GB apparent, sparse) | 2026-09-16 | **Not the live Docker disk.** The live one is `~/Library/Containers/com.docker.docker/Data/vms/0/data/Docker.raw` (mtime 2026-10-04). Docker `settings-store.json` has no custom data folder. Daily 2026-09-27 records that the Laptop-DEV copy was already removed. | `du -k` vs `stat %z`. **Copy with a sparse-aware tool** (`cp -c`, or `rsync --sparse`). A plain copy can write up to ~926 GB. |
| Secuura worktrees: 221 where the ks id is in the develop log but the files differ | 187.0 GB (nm 93.0) | none <3 d | Ticket landed in develop, but this worktree's files differ: superseded, or later edits on top. Clean. | develop log subject grep for `ks-?NNNN` (last 4,000 commits). **Unmerged diff may hold unlanded tweaks.** |
| Secuura worktrees: 21 unmerged, HEAD sha is a remote branch tip | 14.7 GB (nm 6.2) | none <3 d | Clean, and the commit exists on origin, so it is recoverable | `ls-remote --heads` sha match |
| `WEDNESDAY/2_Project_Files/local-model/models` | **127.8 GB** | 2026-09-15 | All 14 blobs (sha256-named) also exist in the live store `SYSTEM/ollama/models`. `launchd` and `start_ollama.sh` set `OLLAMA_MODELS` to SYSTEM. Separate inodes, so this is a real duplicate. | per-blob existence check. **`doctor.sh:162` still points `LM_MODELS_DIR` here**, so repoint doctor first or it will warn. |
| `WEDNESDAY/2_Project_Files/fleet/qa-agent/gatesets/` — 94 gatesets dated <09-21 | 11.1 GB (4.6 GB nm) | ≤09-20 | old gate runs | `du -d1`, age from folder-name date |
| `WEDNESDAY/2_Project_Files/**/_quarantine_*` | ~1.0 GB | 09-14…09-16 | already quarantined (0.66 GB overlaps gatesets above) | `du -sk` |
| `/Volumes/DevMASTER/tmp-qa962-mkwnwD` | 0.33 GB | 2026-09-13 | stray QA temp dir at drive root | `find -newermt` |
| `!CODING/Claude to Claude` (whole) 0.9 GB · `Paperclip` 0.56 GB · `Personal Projects` 0.02 GB | 1.5 GB | Mar–Jun 2026 | idle 90+ d (item 6) | `find -newermt 2026-07-07` returns no files |
| `Testing Agent MAIN` reports dated <09-21 (349 folders) + `.playwright-mcp` | 1.0 GB | ≤09-20 | old QA reports. Records-like, so low value to move. | `du -sk` |

## Class C — KEEP (listed only because big)

| Path | Size | Why keep |
|---|---|---|
| `SYSTEM/ollama` | 268.7 GB | **Live** Ollama store (`OLLAMA_MODELS`). Some 2025 blobs (phi-2 and others) may be unused; check with `ollama list`, not with this survey. |
| Secuura worktrees KEEP: 22 dirty, 4 changed <3 d (s-b55-*, s-d2-ks1404), 34 unmerged with HEAD not on any remote tip, `s-c21-ks1382` (parked), `s-b59-ks528/ks769` (live seat, created 11:06 mid-survey) | ~33.5 GB | rule. The 34 "unpushed" include the `s-*-batch` and `*-merge` worktrees. Their sha may exist under another ref; not proven. |
| `!CODING/Secuura/Blockchain/2_Project_Files` | 21.1 GB | main checkout + `.git` |
| `WEDNESDAY/5_Project_History` (incl. 6.67 GB `2026-09-25_copy_DevMASTER_to_Laptop-DEV.log`) | 7.5 GB | records (rule). The log is the single largest text file; Kam's call. |
| `Secuura/Blockchain/5_Project_History` (incl. `quarantine/` 2.2 GB) | 3.9 GB | records (rule) |
| `Family`, `Daily Life`, `Meeting Notes…`, `.app-source`, `.scripts`, `Cardano…`, `MultiAgent…`, `Security Testing Agent`, `Side Projects` | <0.1 GB each | idle 90+ d but personal or tiny. Nothing to gain. |

## Datasec — per-project totals and class sizes only (Tuesday's to decide)

Totals: NexusAI 30.0 GB · HPSM 15.0 · myPKI 4.1 · _archive 3.1 · CypherKey 2.0 · Security Review 1.1 · Vision_Sales_Portal 0.7 · all others <0.1. **Total 56.1 GB.**
Candidate classes, all older than 14 days:
- NexusAI: node_modules 16.8 GB (107 dirs). QA-worktree class 24.4 GB total (overlaps the node_modules figure).
- CypherKey: build output 1.4 GB.
- myPKI: node_modules 0.65 GB, build 0.31 GB.
- HPSM: node_modules 0.27 GB, .venv 0.05 GB. Also one 7.1 GB file under 1_Project_Definition, which is KEEP by rule.
- Vision_Sales_Portal: node_modules 0.20 GB.
- _archive: one 2.8 GB archive plus node_modules 0.08 GB.

**Tuesday's to decide.**

## Conflict copies, quarantines, Archive, `.pre-*` (low priority)

All projects: 453 `(conflict_on_…)` items (0.07 GB), 3,230 `*.pre-*` files (0.21 GB), 77 quarantine dirs (3.47 GB: Secuura records 2.2, Wednesday 1.0, TAM 0.34), 145 `Archive/` dirs (~0). By top folder: WEDNESDAY 1,667 (2_Project_Files) + 329 (0_Brain), TUESDAY 969 + 216, Secuura 352, Datasec 213, TAM 31. Not worth moving for space.

## MOVE COST — regenerate, don't move, node_modules

- One `Blockchain/Dev/node_modules` holds **161,048 files / 1.44 GB**. This was the same in a Secuura worktree (`s-b29-ks1129`) and in a QA scratch worktree (`batch1280-t1/work/wt/h1284`). npm, not pnpm: link count 1, no hard-link sharing, so the space is real.
- Worktree node_modules ≈ 240 GB ≈ ~160 such copies ≈ **~26 M files**. QA-report node_modules ≈ 221 GB ≈ **~23 M files**. The whole drive holds 58 M inodes. Moving ~50 M small files to G-DRIVE would take many hours to days.
- **Suggestion:** for A and B worktrees and QA scratch, either move the folder *excluding* node_modules and drop node_modules (it regenerates with `npm ci`), or move it whole only in overnight batches.
- The Docker.raw and Ollama blobs are a few huge files, which makes them fast to move (sparse caveat above).

## Git worktree orphan note

`Blockchain/2_Project_Files/.git/worktrees` has **487 admin entries**: 486 worktree dirs plus 1 that points into `5_Project_History/quarantine/2026-09-15-s233/worktree-ks679`. None are orphaned today. Moving folders off-drive would orphan:
- **181** entries for class A,
- **+242** for class B (**423** total).

Each moved worktree stays registered, so its branch shows as checked out and cannot be checked out elsewhere, until the Secuura agent runs `git worktree prune`. That is a write verb, so it belongs to Secuura's agent. The moved copies stop working as worktrees because `.git` holds an absolute `gitdir:`. The QA-report worktrees link to clones inside their own report folder, so moving whole report folders orphans nothing.

## FOUND / TESTED / HOW

- **Sizes:** `du -k -d 1` on the drive, `!CODING`, WEDNESDAY, Secuura and Blockchain, plus `du -sk` per candidate dir. "GB" means GiB of allocated blocks.
- **Regenerable dirs:** one `find`, pruning `.git` and stopping at the first match, over node_modules, .next, .turbo, dist, build, coverage, .pytest_cache, `__pycache__`, .venv and venv. It found 13,841 dirs. Each was measured with `du -sk`. Age is the newest mtime of the dir itself or its direct children; the 14-day cutoff is 2026-09-21. No .next, .turbo or coverage dirs exist.
- **Worktrees (484 at scan start):**
  - HEAD via `rev-parse`; branch via `symbolic-ref`.
  - Ancestor test against **local** `origin/develop` ef4901778. No fetch was run, and the remote develop is now 14d40d445, which is not present locally. This is conservative: some B worktrees are likely merged.
  - Squash test: file equality against develop. Remote branch and sha from one `ls-remote --heads` (730 heads).
  - Dirty = `status --porcelain` non-empty. Recent = any non-node_modules file newer than 2026-10-02 12:00.
- **Live cwds** (`lsof -d cwd`): `Secuura/Blockchain`, `WEDNESDAY`, `WEDNESDAY/2_Project_Files/dashboard`. None of them is inside a candidate.
- **Big files:** `find -size` over archives >500 MB, logs >100 MB, VM images >100 MB and anything >1 GB (20 hits). No .dmg, .iso or large .zip outside Datasec.

**NOT measured:**
- **/Volumes/Development (NAS):** `du -d 1` hit the 10-minute cap with no output, so it was skipped. `df` shows 1.8 TiB, 1.2 TiB used, 584 GiB free. Nothing recommended there.
- PR merge state via `gh`: not used (Secuura `gh` config not loaded). The squash test stands in for it.
- Whether the 34 "unpushed" KEEP worktrees' shas exist under non-tip refs.
- Which 2025-era blobs in `SYSTEM/ollama` are still referenced by a manifest.
- Contents of `.DocumentRevisions-V100`, `.Spotlight-V100` and `.Trashes`.
- Exact file counts beyond the 3 node_modules samples.
- Hidden tool caches under project `.claude/` dirs.
