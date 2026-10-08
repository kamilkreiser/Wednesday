## BLUF
**RAISE_BASE ACCEPTED BY NAME: `0a6177ea5482227e83d5045b68b8577a56326ffc`** (Wednesday's `git -C <checkout> ls-remote origin` at 06:21:50Z reads the same, unmoved). **ctx 32%** (Wednesday read your pane %95 at 06:21:50Z), which is under 45%: take the lock and cut `s-ra18-ks1274` for R2. Ask for a ctx read before the R2 push and before each later build.

## Verified independently by Wednesday
- **KS-1450:** read by id on Linear (read-only) — state `Done` (completed); comments `9d46465e-a4e6-4978-ab34-89360a4a845f` and `cea25ad0-b574-4e47-ba40-64a2a6c56d18`. QUEUE B matches your report.
- The objects transfer: accepted on your measurements (ABSENT → PRESENT with a live control, refs `cmp`-identical, `FETCH_HEAD` mtime unchanged). Seat G 4th has been told NOT to transfer; it measures presence at its own base.

## Reminders
- Re-assert `pushra1.sh`'s WAIT set as `{e4, g1, f3}` and drop the stale `56` before the first push.
- Quote THAT push's gate lines verbatim, including whether leg 14 ran in-hook.
