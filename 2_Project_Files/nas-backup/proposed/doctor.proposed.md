# PROPOSED line for `2_Project_Files/doctor.sh` (round 3; the line itself is unchanged since round 2). Nothing here is applied.

## The change: one sourced file
After the "NAS replica staleness" block (ends near line 548):
```
# --- Nightly copy-only NAS backup (WED-170, Kam 2026-11-27): the three-day flag's channel to a seat ---
[ -f "$PROJECT_DIR/2_Project_Files/nas-backup/proposed/doctor_nasbackup_block.sh" ] && . "$PROJECT_DIR/2_Project_Files/nas-backup/proposed/doctor_nasbackup_block.sh"
```
The block is a FILE (`proposed/doctor_nasbackup_block.sh`), not pasted lines, so the suite runs exactly what doctor will run. When it is applied, Wednesday may move the file out of `proposed/`; the tests name its path in one place (`doctor_block()` in `tests/run.sh`).

Rollback: remove the line.

## What it prints

| State | doctor prints | Why |
|---|---|---|
| Good backup inside 72 hours | `ok` (nothing under `--quiet`) | |
| Held (`HOLD_<seat>` exists) | a warning, **once a day at most**; `ok` on later boots that day | QA minor: round 1 warned at every boot on every held seat |
| 72 hours without a good backup, card **not** recorded as raised | **a hard failure (`fail`, the `✗` line)** whose text starts with the command to run: `bash 2_Project_Files/nas-backup/nas_backup_watch.sh --card` | This is the channel (QA finding 6) |
| Same, card recorded as raised | a warning | Nothing more for a seat to do |
| A state file or the index was found damaged, by anyone, and no seat has acknowledged it | **its own hard failure: `NAS BACKUP STATE WAS FOUND DAMAGED`**, naming `nas_backup_watch.sh --check` and then `--ack-damage`. Printed at every boot, held or not, until a seat acknowledges | Second check, findings 6 and 15: the notice was spent on the nightly job's log, and doctor borrowed the "3 DAYS" text for it |
| Seat of the tree unknown | a warning; the check is not run | |

## Why a hard failure, and why that is the channel
QA finding 6: round 1's card command went to a launchd log, and its launcher proposal named a variable the launcher does not have. I read the real launcher (`Launch_Wednesday.command`, `set -u` at line 9). What it carries from boot into a seat's prompt is one thing only: doctor's `✗` lines (lines 400 to 417 and 904 to 914). On a rotation they are appended to the boot prompt under "FIX THEM FIRST"; on a human launch the boot stops and shows them to Kam. It cuts each line at 400 characters, so the block puts the command first and keeps the line short.

So: the nightly job never prints the card (it calls the watch's read-only mode). Doctor's hard-failure line names the command. The seat runs it, gets the one `decision_queue.sh add` command, adds the card, and runs `--mark-raised <id>`. From then on doctor warns instead. Printing the command consumes nothing: it prints again at every call until `--mark-raised`. The card id is fixed per gap and `decision_queue.sh` refuses a duplicate id, so the card exists once per gap.

**The cost, said plainly:** a hard failure stops a human launch at the "Preflight found HARD failures" prompt until someone answers it. That is deliberate (Kam asked to be flagged) and it ends as soon as the card is recorded as raised. If Wednesday would rather it never gate a launch, change `fail` to `warn` in the block's case `3)`; then nothing carries it into a seat's prompt and a seat must read doctor's output itself.

## The seat comes from the tree
The block calls `tools/seat_note.sh` (`seat_note_dir "$PROJECT_DIR"`), never doctor's own `_DOC_AGENT` default (QA minor: with `WED_AGENT` unset on a TUESDAY tree, round 1's block looked at `HOLD_wednesday`).

## Tested, and not
- Tested in `tests/run.sh` with doctor's own three helpers copied from doctor.sh lines 16 to 18: T8 (three failed nights end with the `✗` line; cut at 400 characters it still names the command; running the command prints the card; once raised, no `✗`), T9 (held: warned once, not twice the same day), T16 (an empty state file gives the `✗` line, not a traceback).
- **NOT tested:** the block inside the real `doctor.sh` (doctor was not edited or run with it), and the launcher carrying the line into a real boot prompt. That path was read, not exercised.

## Round 3: what changed in the block
- **The damage notice.** Whoever finds a damaged state file or index (the nightly job included) leaves `state/DAMAGE_NOTICE_<seat>.jsonl`. The block checks for that file itself, after the watch call and also when the seat is held, and prints one hard-failure line in its own words. The watch exits 5 while the notice exists; the block maps 5 to nothing more than that line. A seat clears it with `nas_backup_watch.sh --ack-damage` (the notice is moved into the lane's quarantine).
- **The hold no longer starts the three-day clock.** With the real lane's state of 2026-11-27 (one refusal under the hold), lifting the hold starts the clock then; the block does not fail hard during a first copy that starts on the day the hold is lifted.
- Tested in `tests/run.sh`: T25 (the nightly job finds the damage on night 3, doctor fails hard at the next boot and the one after, also while held, until `--ack-damage`), T16 (an empty state file gives the damage line, not a traceback), T27 (the hold lifted: no `✗` that morning).
- **Still NOT tested:** the block inside the real `doctor.sh`, and the launcher carrying the line into a real boot prompt.
