# The seat launcher: NO change is proposed (round 2)

Round 1 proposed five lines for `Launch_Wednesday.command` that piped into `tee -a "$PREFLIGHT_LOG"`. QA finding 6: the real launcher has no such variable and runs under `set -u`, so every boot of every seat would have printed `PREFLIGHT_LOG: unbound variable` and lost the line. That proposal is withdrawn (kept at `round1/launcher.proposed.md.round1`). My slip: I wrote a placeholder name into a proposal without reading the file it was for.

## Why nothing is needed
I read the real launcher this round. It already does the one thing required:

- Line 9: `set -u`.
- Lines 400 to 417: it runs `2_Project_Files/doctor.sh --quiet`, captures the output in a `mktemp` file, and collects doctor's `✗` lines into `PREFLIGHT_HARD` (each cut at 400 characters).
- Lines 904 to 914: on a rotation, `PREFLIGHT_HARD` is appended to the boot prompt under "FIX THEM FIRST". On a human launch the boot stops and shows them.

The three-day flag now reaches a seat through that existing path: the doctor block (`proposed/doctor.proposed.md`) prints a `✗` line that names `nas_backup_watch.sh --card` while a card is due and not recorded as raised. No launcher line, no new variable, nothing that can break a boot.

## What a seat does when it sees the line
```
bash 2_Project_Files/nas-backup/nas_backup_watch.sh --card
```
It prints one line starting `CARD-COMMAND:`. Run that command (it adds ONE card for Kam, default "wait for tonight's window"), then:
```
bash 2_Project_Files/nas-backup/nas_backup_watch.sh --mark-raised <the card id>
```
Do not run a backup outside the window unless Kam rules option a. If he does: `bash 2_Project_Files/nas-backup/nas_backup.sh --run --out-of-sequence <the card id>`.

## Not tested
The launcher carrying the line into a real boot prompt: read in the launcher's source, not exercised (no launcher was run).
