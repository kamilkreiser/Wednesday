# B281 drafter report (2026-10-19)

Brief: `2026-10-19_B281_SEAT-G8_composer-gate-pr80-tier2.md` (gate on draft PR #80, tier 2 config/CI). Written with the Write tool only. Read whole: the B279 gate brief, the B280 builder brief, the B280 STATUS. I ran no command (no git, gh, docker, HTTP), so every fact in the brief is either from your task text (MEASURED by Tuesday) or from the B280 STATUS (RELAYED), and the brief marks them that way. Not read: shared fleet folders, `compose.yaml`/`ci.sh` themselves.

## Slots (8; each appears in the brief, split-pattern REFUSE check at the top)
| Slot | Default / source |
|---|---|
| MODEL | `claude-sonnet-5-5` (launched with BRIEF_SEAT_LEVEL=sonnet; `brief_seat.sh` pins Opus, so switch with `/model` or let STATUS say which ran) |
| STAMP_TIME | `date` at stamping, AEDT |
| PANE | `Datasec/Security-Composer-G8` |
| PANE_SUFFIX | `G8` |
| PORT_BLOCK | `18210-18219` (B280 used 18200-18209; confirm free with `lsof` and that no other seat claimed it) |
| CODE_MAIN_SHA | `230f9fab122d7335d838a173e21aec195f01860f` (re-read by `ls-remote` at stamp) |
| HEAD_SHA | `fddb799b0ea3cbc3ffe93671c73308053137fb47` (re-read at stamp) |
| B_NUMBER_CONFIRM | `B281`, after confirming 0 hits for B281 in `briefs/` and both projects' `Briefs/` |

Self-check recipe: copy `.pre-stamp` first; the REFUSE grep on the stamped file must print 0 and on `.pre-stamp` must print >= 1 (STAMP_TIME appears twice, HEAD_SHA and CODE_MAIN_SHA several times, so use a global replace for each).

## Design notes
- Structure copied from B279: REFUSE, LOAD, PINS, CLAIMS with traps (T-a to T-e), r0-r7 each with FAIL-first, own instrument, control, VERDICT, HOLDS, NOT TESTED. Your r0-r7 map one to one (r0 scope + merge-tree, r1 byte identity, r2 ci.sh, r3 R4/R7, r4 old-volume, r5 override, r6 CodeQL, r7 gitleaks + prior work).
- Added from B280 STATUS: the empty `DOCKER_CONFIG` needs `DOCKER_HOST` set (Correction 3); load can read over 6 seconds after a "below 6" gate (Correction 1); ci.sh runs its own `down -v` on its own `pc-ci-*` project (excepted from the never-delete hold, named); `compose.demo.yaml` is not in the repo, so the gate may only test stand-ins and must grade the "cannot reach the demo" claim as RELAYED.
- r4 is conditional on the old pin being cached (builder F-8: cached as `minio/minio@sha256:14cea493…`, arm64). Never pulled.

## Top doubts
1. **`PC_E8_SOW_TEXT`.** ci.sh run from a worktree needs this var, which B280 pointed at a file under `1_Project_Definition/Source_Documents/`. The standing HP-Restricted hold forbids opening it, but ci.sh reads it. I wrote "pass the path, do not read it; else NOT TESTED + STOPPED". Tuesday should decide before launch whether that file is safe for ci.sh to read, or give the gate a non-restricted path.
2. Load: three gates share the Mac and B280's ci.sh load hit 13.6; r2 may sit waiting a long time.
3. B280 STATUS says +8/-1; your measurement says +5/-1 and +3/-0 (= +8/-1, consistent). The brief quotes your numbers.
4. I did not check whether `cockpit.sh add Datasec/Security-Composer-G8` name or port block 18210-18219 collide with anything live.
