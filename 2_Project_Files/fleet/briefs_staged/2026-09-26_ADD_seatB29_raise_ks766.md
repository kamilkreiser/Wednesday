# ADD (Seat B 29th): one more item at the END of your queue — RAISE KS-766 from a held local-model READY (a Spark PASS)

## BLUF
**Add as the LAST item of your queue** (after your lane items and the #1261 fix round): raise **KS-766** as ONE PR from the held READY.
- **The patch:** `/Volumes/DevMASTER/WEDNESDAY/2_Project_Files/local-model/night/READY_KS-766-BASEIMAGEWATCH_spark-dsv4_SELFTEST-PASS_2026-09-26.diff.md` (the diff block inside it). One file: `Blockchain/Dev/scripts/base-image-watch.sh`, 3 hunks, written by the Spark local model, checked by Wednesday's harness (strict apply at d7cdecf1; red with the test hunk alone (exit 12), green with all three (exit 0), 20→22 PASS lines). Wednesday read it line by line: identical to the verified golden.
- **Base:** it was checked at d7cdecf1. develop is now df5e9f5da6d2, and the move touched 0 files under `Blockchain/Dev/scripts/` (GitHub compare, read by Wednesday). Apply it strict (`git apply --check` with no recount) on a worktree at the current develop tip. If it does not apply strictly, STOP and mail; do not recount.
- **Your own proof, not the harness's:** run `bash Blockchain/Dev/scripts/base-image-watch.sh --self-test` at the tip (expect 20 PASS) and at your head (expect 22 PASS, exit 0). Reproduce the red: the test hunk alone gives exit 12. Put all three in the Test Evidence block and name the base your worktree contains.
- **Partition:** `Blockchain/Dev/scripts/` belongs to no live seat (L5 has wrapped). This is a new worktree on your own namespace token (`-b29-`), under `.push-lock-25`.
- **PR body:** "Refs KS-766". No closing keyword. Credit the patch's origin plainly ("patch produced by the local model under a Wednesday brief, re-verified by this seat").
- It then goes to the next gate. Tier: by its diff. It is a host-script change, so the gate decides.
