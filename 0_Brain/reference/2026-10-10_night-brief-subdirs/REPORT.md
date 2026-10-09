# Night runner: subdirectory briefs (2026-10-10)

## BLUF
- `night/build_input.sh` now resolves a brief from a subdirectory (Spark shape: `briefs/<dir>/<TICKET>.md`), in this order: `brief_dir=` pin, flat `briefs/<T>.md`, exactly one `<T>-*/` subdir (logged), more than one with no pin (REFUSED rc 2, names them all).
- `night_run.sh` forwards the new `brief_dir=` queue pin. 12 arms in `tests/night_brief_subdir_arms.sh` all PASS. The same arms run against the OLD builder FAIL 9 of 12, so they discriminate.
- Not tested: a full build or model run (no dry mode exists; it always reads Linear and git). Incidental finding: the live develop tip is not in the local object store and `tip_override.txt` is stale, so a real build would currently REFUSE at the tip check (see NOT tested).

## Findings that differ from the brief
- The brief inside each subdir is named `<TICKET>.md` (e.g. `KS-1410.md`), NOT `brief.md`. The Spark convention (`spark/queue.md` header: "holds exactly one KS-<n>.md brief"; `spark/round.sh` line 23 sets `NIGHT_BRIEFS_DIR=<brief_dir>`) is what I reused. Setting `NIGHT_BRIEFS_DIR` to the subdir makes the three existing readers work unchanged.
- Line numbers confirmed in the original: 218 (`_early_brief`), 435 (`_bp`), 683 (`brief_path`), 689 (bare-ticket message). All three read `$NIGHT_BRIEFS_DIR/<ticket>.md`.
- Stale header comment CONFIRMED wrong. Original line 22-23: "the service is not on vitest (the checker runs `npx vitest run`; originate and governance are jest)". Code contradicting it: original lines 261-269 (`# jest services (originate, governance — ts-jest) are IN`, `elif "jest" in test_script: runner_kind = "jest"`, refuse only when neither: "the checker runs vitest or jest only"). Header rewritten.

## What changed
Files (live backups beside them, exec bits kept: build_input.sh is 755, night_run.sh was and is 644, it is run via `bash`):
- `night/build_input.sh` (backup `build_input.sh.pre-1010-briefsubdir`): +~45 lines.
  - Header: jest line corrected; BRIEF RESOLUTION block added.
  - After the KS-id check, before any `.env` or network read: the resolver. It exports `NIGHT_BRIEFS_DIR=<winning dir>` and prints `build_input: brief resolved — <path> (<why>)`. The python `prompt source: WEDNESDAY BRIEF <full path>` line then states the file used, as before.
  - `BUILD_INPUT_RESOLVE_ONLY=1` prints the resolution plus `NIGHT_BRIEFS_DIR=...` and exits 0 (used by the arms only).
  - The python is untouched, including the bare-ticket message.
- `night/night_run.sh` (backup `night_run.sh.pre-1010-briefsubdir`): 2 lines. The pin allow-list gained `brief_dir`, and the header QUEUE comment documents it. Without the allow-list change the pin would have been dropped silently, as `test_file=` once was.
- `tests/night_brief_subdir_arms.sh`: new.
- NOT edited: `night/queue.md` (the real queue; owed header doc line, see below), `hold_ready.py`, `tests/hold_ready_*`.

Queue usage: `KS-1410 brief_dir=KS-1410-transfer-process-expired-500 product=... ` (relative to `night/briefs/`, or absolute).
Resolver behaviours beyond the spec:
- A pin naming a dir that lacks `<T>.md` is REFUSED rc 2.
- A subdir only counts if it holds `<T>.md`.
- The glob is `<T>-*/` plus `<T>/`, so KS-141 can never match KS-1410-*.
- When `NIGHT_BRIEFS_DIR` is already a brief dir (the Spark path), the flat step matches, so Spark is unchanged.

## Arms
Run: `bash 2_Project_Files/local-model/tests/night_brief_subdir_arms.sh` (args: new builder, old builder). Fixtures live under the scratchpad `briefsubdir/fx_*`; the real briefs dir is only read.
Mechanism: resolver via `BUILD_INPUT_RESOLVE_ONLY=1`. The python 5c block is extracted verbatim from the script under test and run in isolation to get the real `prompt source:` line.

| Arm | Expected | Actual | Fails if |
|---|---|---|---|
| B1 flat fixture `KS-777.md` | rc 0, dir = root, "(flat file)", `prompt source: WEDNESDAY BRIEF <root>/KS-777.md` | PASS | flat file stops resolving or the path changes |
| B1b real flat (KS-1009, read-only) | resolves to the briefs root | PASS | same, on real data |
| B2 `brief_dir=KS-1410-transfer-process-expired-500` (fixture, with two decoys) | `prompt source` = that subdir's `KS-1410.md`, "named by the brief_dir= pin" | PASS | pin ignored, or a decoy picked |
| B2b same on the REAL dir | `NIGHT_BRIEFS_DIR` = real subdir | PASS | |
| B2c pin to a dir without the brief | rc 2 REFUSED | PASS | pin silently falls through |
| B3 two KS-1410-* subdirs, no pin | rc 2, both names in the message, no `NIGHT_BRIEFS_DIR` line | PASS | it picks one |
| B3b three subdirs | rc 2, "3 brief subdirectories" | PASS | |
| B3c REAL dir (4 KS-1410 subdirs) | rc 2 naming them | PASS | |
| B3d exactly one subdir, no pin | used, "the ONLY brief subdirectory" in the log | PASS | silent or refused |
| B4 OLD script's 5c block, B2 input | `prompt source: the ticket description` | PASS | old script already resolves subdirs |
| B4b OLD has no `brief_dir` consumer | true | PASS | |
| B5 no brief anywhere | bare-ticket warning, byte-identical OLD vs NEW | PASS | message changed |

Discrimination: with the OLD builder in the NEW slot, 9 of 12 arms FAIL (B2/B2b/B3*/B1/B1b/B5 fail; B2c, B4, B4b pass). Final run with the new builder: `ALL ARMS PASS`, rc 0.

## Night job schedule + running-process check
- `pgrep -fl 'night_run|build_input'` at the start: no output. Re-run just before the swap: the only hit was a zsh wrapper of my own earlier backgrounded `grep -r` (its command text contains "night_run"), not a runner. No runner or builder was executing, so the in-place swap was safe.
- `launchctl list`: `com.wednesday.ornith-night` (last exit 3) and `com.wednesday.ornith-loop` (last exit 3) loaded. `ornith-night.plist`: `StartCalendarInterval` 23:30 daily, `RunAtLoad` false, runs `/bin/bash .../night/night_run.sh`. I did not read the ornith-loop plist schedule. Both loaded jobs pick up the new scripts on their next start.

## NOT tested
- A full `build_input.sh` run or any model run for a subdir brief. build_input has no dry mode (it always reads Linear and runs `git ls-remote`). Hence the resolver and the extracted 5c block are tested separately: the join between `NIGHT_BRIEFS_DIR` and the python's three reads is by construction (all three read `$NIGHT_BRIEFS_DIR/<ticket>.md`) and by the Spark path already relying on it, not by an end-to-end run.
- Incidental, when the OLD builder ran in the NEW slot: `build_input: REFUSED — develop tip 4aa5cb38... is not in the local object store`, and `tip_override.txt` is verified against `df5e9f5d...`, which is no longer origin's tip. A real build tonight would refuse here unless the coordinator refreshes the override or a Secuura seat fetches. Not mine to fix; read-only observation.
- `night_run.sh` forwarding was checked by diff and `bash -n`, not by running a queue line.
- Owed: add a `brief_dir=` line to the `night/queue.md` header (left alone as the live queue). The `spark.pins` files in the subdirs are not read by the night path (Spark only).

## Instrument errors I made and caught
- My first `pgrep -fl -i 'ornith|...'` matched an unrelated wake-watcher process and then my own grep command, which looked like a runner. Narrowed to `night/(night_run|build_input)` and read the command lines: no real runner.
- A `grep -rl` over all of `local-model` timed out (the runs dir is huge) and ran in the background. Re-ran with explicit file globs.
- The brief said the brief file is `brief.md`; listing the real dirs showed `KS-1410.md`. I followed the real shape.
- An `echo =====` in a zsh command failed (`=` expansion) and hid the output of two `sed` prints. Re-ran with `printf`.
- Draft test had a leftover no-op line (`rm_unused=1`, removed) and mixed a 3-dir fixture with the stated 2-dir B3; added a dedicated 2-dir root so B3 matches the spec.
