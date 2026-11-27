# Proposal 7: doctor's stacked-pickup warning stops firing once the handover is the state file

TARGET: `2_Project_Files/doctor.sh`

## What it does today

Lines about 1109 to 1123 (added 2026-09-18) warn when `0_Brain/tasks/NEXT-PICKUP.md` holds more than one `## ` block or is over 15,360 bytes. It has warned at every launch for weeks: the file holds 110 blocks and about 290 KB. After the cut-over nobody writes that file again, so the warning would fire at every launch for ever, about a file that is frozen on purpose. A warning that is always on teaches the reader to skip the preflight.

## The change: retarget, not retire

Once `STATE-wednesday.md` exists, the one-block property is checked on the state file by `handover.sh check` (proposal 4), which can also see a block appended by hand. The legacy check then prints one quiet OK line. Before the cut-over nothing changes: the `elif` keeps the old check exactly as it is. The check has always been about the Wednesday seat's pickup (the path is `NEXT-PICKUP.md`, not a per-seat name), so the state file named here is the Wednesday seat's on every tree; the file travels by git, so the line reads the same on Tuesday's and Friday's machines.

```old
NP="${WED_PICKUP_FILE:-$PROJECT_DIR/0_Brain/tasks/NEXT-PICKUP.md}"
if [ -f "$NP" ]; then
```

```new
NP="${WED_PICKUP_FILE:-$PROJECT_DIR/0_Brain/tasks/NEXT-PICKUP.md}"
# WED-170 step 1 (2026-11-27): once the Wednesday seat's handover is the one-block state file, this
# legacy file is FROZEN on purpose and the one-block rule is checked on the state file instead
# (handover.sh check, in the wake-pack block above). Before that cut-over this check is unchanged.
if [ -z "${WED_PICKUP_FILE:-}" ] && [ -f "$PROJECT_DIR/0_Brain/tasks/STATE-wednesday.md" ]; then
  ok "NEXT-PICKUP.md is frozen: the handover is 0_Brain/tasks/STATE-wednesday.md"
elif [ -f "$NP" ]; then
```

The `WED_PICKUP_FILE` test seam still reaches the old check, so that check's own selftest keeps working.

Apply together with proposal 4, and only after the first state block is written.

This changes what doctor prints on Tuesday's and Friday's machines too, once `STATE-wednesday.md` reaches them by git: a warning about the Wednesday seat's pickup becomes one OK line. That is intended (the warning was never about their file), and it is still a change to their doctor output, so it is claimed with them like the launcher.

Not run inside doctor; the two shell lines were syntax-checked in a scratch harness (check P13).

ROLLBACK: `git revert` of the commit; the old check returns as it was.
