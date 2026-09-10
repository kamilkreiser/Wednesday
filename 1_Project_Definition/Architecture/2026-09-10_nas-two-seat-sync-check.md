---
date: 2026-09-10
type: design
source: Kam, panel 17:16 (view=tuesday) and 17:17 (view=wednesday); Tuesday s6
status: DESIGN — not built, not armed
---

# NAS two-seat sync check — design

**Commission, Kam verbatim (17:16):** *"With the sync to the NAS, please make sure that there's a good check as both you and Wednesday will be syncing at different times naturally. And you've been working on Datasec while Wednesday has been working on blockchain and Securo work."* He sent the same ask to Wednesday's tab at 17:17. Wednesday released it to Tuesday by mail at 09:19Z; nothing was started on her side.

**State:** Tuesday's 23:00 leg (`com.tuesday.nassync`) was **booted out at 19:19:19** so nothing runs unattended before this exists. Revert: `launchctl bootstrap gui/$(id -u) ~/Library/LaunchAgents/com.tuesday.nassync.plist`.

## 1. What exists today — measured 2026-09-10 19:1x on Tuesday's Mac

| Piece | Fact | Instrument |
|---|---|---|
| NAS | Live mount `//KAMILADMIN@192.168.20.221/Development` on `/Volumes/Development`; initialised 2026-05-18 from `/Volumes/DevMASTER` on the Studio ("partial force-sync aborted at ~65%") | `mount`; `.devnas-sync-state` |
| Engine (Kam's) | `!SYNC FILES/devnas-sync.sh`: bidirectional unison, drive root ↔ NAS. Lock is `/tmp/...lock.d`, so **per machine only**. Extra args: only `DEVNAS_IGNORE_NAMES` → `-ignore "Name X"`, **split on spaces** | read the script |
| Profile (Kam's) | `batch`, `auto`, `prefer = newer`, `copyonconflict`, `fastcheck`, **`confirmbigdel = false`**, backups kept on the machine that ran the leg, `.git` ignored | read `devnas.prf` |
| Wrapper (both seats) | `2_Project_Files/scheduler/nas_sync.sh`: DETECTS only — counts `Deleting` after the run, alarm at 50. Its report and logs are **gitignored**, so neither seat can see the other's last leg | read + `git check-ignore` |
| Legs | Tuesday 23:00 (`WED_AGENT=tuesday`, last exit 126 = TCC); Wednesday 03:30 on the Studio | `plutil`, `launchctl print`, installer |
| Wednesday's leg | **Running since 2026-09-09 03:30 — 40h at 14% (395 of 20,621 items, 6.57 of 44.13 GiB, 15.7 KiB/s, ETA 22 days); has never completed a run**, so its 2026-09-10 slot never fired. 315 `Copying`, **0 `Deleting`** — the deletion alarm is untested in real use. It is walking `!CODING/Datasec/ATTIO` and `!CODING/Datasec/NexusAI`, including `4_Credentials/.azure/telemetry/` | Wednesday's measurement on the Studio, mail 09:46Z (`launchctl list`, `ps`, its own log) |
| Existing damage | **33** `(conflict_on_…)` copies under `0_Brain/` in this tree — 23 dashboard, 4 daily, 4 projects_index, 2 learnings | `find`; positive control: a known copy is in the list |

## 2. The failure Kam named

Two drives, each the live working copy for a different client (T9 = Datasec, DevMASTER = Secuura and general), meet on one NAS at different times with `prefer = newer`. A change or deletion made on one drive reaches the NAS on that seat's leg and is carried to the other drive on the next. Neither leg knows the other ran, and the `/tmp` lock cannot stop two machines overlapping.

## 3. Proposed check — four parts

1. **PARTITION BY OWNER — the prevention.** Each leg ignores the trees the other seat owns, through the engine's existing `DEVNAS_IGNORE_NAMES`: Tuesday's leg `Secuura WEDNESDAY`, Wednesday's leg `Datasec TUESDAY`.
   **Tested (scratch, unison 2.54.0, own `UNISON` home):** with `-ignore 'Name X'` a deletion on one side is NOT propagated (a); a change on the other side is NOT pulled back (d); a nested folder of the same name is hidden too (c). **Control:** the same deletion WITHOUT the ignore IS propagated (e), so the harness can see the failure. Script: session scratchpad `unison_ignore_test.sh`. **`Name Datasec` matches the `!CODING/Datasec` directory itself** (basename, any depth — case c), so the ignore covers the CLIENT tree, not only a seat folder.
2. **CROSS-MACHINE LOCK ON THE NAS.** `mkdir /Volumes/Development/.devnas-seat-lock` with seat, host, pid and start time; the leg refuses while it is held. A lock older than a set age is reported on the panel, never broken silently. **DECIDED 19:5x, on Wednesday's measurement: ABORT-AND-REPORT, NEVER WAIT.** A leg that finds the lock held exits, writes its report and posts one panel line. With a live leg taking 40+ hours, a waiting leg would never run, and a collision is the normal night, not an edge case.
3. **PRE-FLIGHT REFUSALS.** This seat's brain tree is at origin and clean outside `dashboard/data`; the NAS is mounted; the conflict-copy count is recorded.
4. **POST-RUN.** The existing `Deleting` alarm; **the conflict-copy count must not rise** (Wednesday's input); and a NAS-side stamp `.devnas-last-leg-<seat>` so each seat can read when the other last ran and what it reported.

## 4. What it CANNOT do — stated, not implied

- **Inside a seat's own trees, unison still propagates deletions and overwrites.** Prevention there is Kam's one profile line, `confirmbigdel = true` (asked 2026-09-08, still open).
- **Folders with spaces in their names cannot be partitioned today** — `Notes (MASTER)`, `Setup and System`, `Daily Life`, `Meeting Notes and Transcripts`. Measured: the engine turns `Notes (MASTER)` into `Name Notes` + `Name (MASTER)`. They either stay synced by both legs, or the engine gains a path-based ignore. That engine is Kam's file.
- **A name ignore matches that name at ANY depth**, so a folder called `Datasec` or `Secuura` anywhere is hidden from the non-owning leg.
- **"Both replicas at origin" cannot be proven from one machine** (Wednesday's point). The partition narrows it to each seat's own tree, which that seat can check.
- **Throughput is unmeasured for a partitioned leg.** At 15.7 KiB/s a whole-drive leg cannot finish in a night; the partition shrinks each leg's set, but whether what remains finishes nightly is not known until one runs.
- **`fastcheck` compares size and time, not content.** In the first scratch run a same-size edit made within about a second of the previous sync was not seen; with a 2-second gap it propagated. Harmless for nightly legs, but real.

## 5. Decisions for Kam

1. **Who owns the shared trees** — everything that is neither Datasec nor Secuura (vault root, `Setup and System`, `Family`, `Daily Life`, `QA_AGENT`, the general `!CODING` projects)? Recommendation: Wednesday's leg, because general work is Wednesday's by his 2026-09-09 split. Tuesday's leg would then sync only Datasec and its own tree — which needs a path-based option in his engine, since only name ignores exist today.
2. **`confirmbigdel = true`** in his profile — the only prevention inside a seat's own trees.
3. **Credentials folders on the NAS.** `4_Credentials/` (and `3_Access_Keys/`) are gitignored everywhere and never committed, but they are inside the synced set: Wednesday's leg is copying `4_Credentials/.azure/telemetry/` today. Whether credentials belong on the NAS at all is Kam's call; neither seat has proposed or applied an ignore for them.

## 6. Build order (after Kam hears §3–§5)

Wrapper changes → red-proof every refusal in scratch with a stub engine and a scratch "NAS" → mail Wednesday the diff (her 03:30 leg runs the same wrapper) → reload Tuesday's job → watch the first leg by hand.
