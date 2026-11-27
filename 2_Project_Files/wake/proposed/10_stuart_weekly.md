# Proposal 10: the weekly Stuart run stages the STATE block, not the frozen pickup's top block

TARGET: `2_Project_Files/tools/stuart_weekly/stuart_weekly.sh`

Round 4 (the second checker's N10). Proposal only: the build seat did not edit or run the script.

## What it does today

Line 137 stages "where the seat is" for the weekly run by cutting the first `## ` block out of `0_Brain/tasks/NEXT-PICKUP.md` into `$STAGE/next_pickup_top.md`; line 138 fails the stage only when that file comes out empty. After the cut-over the Wednesday seat writes its handover through `handover.sh` into `STATE-wednesday.md` and adds nothing to `NEXT-PICKUP.md`. The pickup's top block is then frozen at the day of the cut-over. It is not empty, so line 138 passes, and the script stages a stale picture every Monday without complaint.

```old
  awk '/^## /{n++} n==1{print} n>1{exit}' "$PROJECT_DIR/0_Brain/tasks/NEXT-PICKUP.md" | head -60 > "$STAGE/next_pickup_top.md"
  [ -s "$STAGE/next_pickup_top.md" ] || fail stage "NEXT-PICKUP.md top block is empty or unreadable"
```

```new
  bash "$PROJECT_DIR/2_Project_Files/wake/handover.sh" show | head -60 > "$STAGE/next_pickup_top.md"
  [ -s "$STAGE/next_pickup_top.md" ] || fail stage "the STATE block (handover.sh show) is empty or unreadable"
```

`handover.sh show` prints the seat's one block without its header and writes nothing; with no state file it prints nothing on stdout (rc 1, the reason on stderr, which goes to the run's log), so line 138 then fails the stage loudly instead of staging old text. The staged file keeps its name, so nothing downstream has to be renamed; the research prompt that reads it may describe it as "the pickup's top block", and that wording was not checked here.

Apply after the first STATE block exists (order step 2), and before the pickup is a week stale: the script runs on Mondays.

Not run: the script needs Linear and a headless session. The `old` lines are checked to be in the target exactly once (check P10).

ROLLBACK: `git revert` of the commit (two lines).
