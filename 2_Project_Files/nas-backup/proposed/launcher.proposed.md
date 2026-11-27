# PROPOSED lines for the seat launcher (`Launch_Wednesday.command`, shared by all three seats). Nothing here is applied.

The launcher is shared: per the WED-170 design, a change to it is claimed with Tuesday and Friday first.

## 1. In the preflight section, beside the `doctor.sh` call (it must run at EVERY boot, whether or not the backup job ever fired)
```
# Nightly NAS backup, three-day flag (WED-170, Kam 2026-11-27: "Flag it with me if backup not done for 3 days").
# Prints one status line; when overdue it prints the ONE decision-card command, once per gap. It never runs it.
if [ -x "$PROJECT_DIR/2_Project_Files/nas-backup/nas_backup_watch.sh" ]; then
  bash "$PROJECT_DIR/2_Project_Files/nas-backup/nas_backup_watch.sh" --flag 2>&1 | tee -a "$PREFLIGHT_LOG"
fi
```
(`$PREFLIGHT_LOG` stands for whatever file the launcher already collects its preflight lines in; use that name.)

Rollback: remove the five lines (take `Launch_Wednesday.command.pre-<date>-nasbackup` first).

## 2. One sentence in the boot prompt, where preflight warnings are handled
```
If the preflight printed a line starting "CARD-COMMAND:" from nas_backup_watch.sh, the NAS backup has not completed for three days: run that exact command (it adds ONE card for Kam, default "wait for tonight's window"), then run `nas_backup_watch.sh --mark-raised <the card id>`. Do NOT run a backup outside the window unless Kam rules option a; if he does: `nas_backup.sh --run --out-of-sequence <the card id>`.
```
Rollback: remove the sentence.

## Why the command is printed and not run by the tool
The brief for this round forbids any `decision_queue` write. Beyond this round it is still the safer split: the tool has no board credentials and cannot double-post; the coordinator that adds the card is the one that will read Kam's answer. The price is named: a printed command nobody reads is a flag nobody raised (2026-09-10 lesson). Three things cover that: the watch keeps exiting 3 and printing a reminder line at every boot until `--mark-raised` is recorded; doctor warns on the same condition; the state file shows `flag.raised: false`.
