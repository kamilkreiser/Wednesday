# Proposal 8: the NAS staleness check watches the state file, not the frozen pickup

TARGET: `2_Project_Files/scheduler/nas_staleness.sh`

## What it does today

With no `--files` argument the script compares six files that change every day against their NAS copies and reports any that are missing or stale there (line 56 is the pickup). After the cut-over `NEXT-PICKUP.md` stops changing, so it stops being evidence that the nightly sync ran: an unchanged file is identical on both sides whether or not the sync is healthy. The file that changes at every checkpoint is then `STATE-wednesday.md`.

```old
$SEAT_DIR/0_Brain/tasks/NEXT-PICKUP.md
```

```new
$SEAT_DIR/0_Brain/tasks/STATE-wednesday.md
```

Why the literal seat name: the line it replaces already names the Wednesday seat's file on every tree (as does the ledger line above it), and the state file travels by git to every clone, so the list keeps meaning what it meant. A tree-derived name (`STATE-<lower-cased tree folder>.md`) would be more exact, but the script reports a listed file that does not exist as MISSING, so it would raise a false alarm on Tuesday's and Friday's trees until those seats have a state file. That variant belongs to the round that moves those seats.

Apply only after the first state block exists and has reached the NAS once; before that the new line reports MISSING.

Not run: the script needs the NAS mount. The `old` line is checked to be in the target exactly once (check P10).

ROLLBACK: `git revert` of the commit (one line).
