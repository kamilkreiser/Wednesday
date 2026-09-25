# CONTINUE (Seat B 28th): you are at 56%. Keep working your queue in THIS seat; the handover is for ~80%

## BLUF
**Do not hand the rest of the queue to a next seat yet.** Your pane (read by Wednesday at 01:1x AEST) says "Remaining queue for the next seat: KS-1293, then KS-1310/KS-1311 with the disposable Postgres, then the KS-1160 residual report", and the statusline reads **ctx:56%**. Your brief's WRAP section says **"Wrap cold at ~80% context"**. The 51% watcher wake is a CHECKPOINT (keep the handover current; start nothing that will not fit), not a wrap order. Overnight is working time (Kam's standing rule).

## Do, in order
1. Finish item 4 (KS-1159): when its push lands, open the PR and send its READY FOR QA, as you planned.
2. **Then take KS-1293 in this seat**, then KS-1310/KS-1311 (your own disposable Postgres, per the brief's Q6 base `33ccff807eb2`), then the KS-1160 residual report, exactly as your brief orders them.
3. Keep the handover current at each boundary. Wrap cold at ~80%, per the brief's WRAP section (fetch + `cat-file -t` the tip, destroy your Postgres and prove it gone).

## Your wake
Your push is a background job; the harness wakes you when it exits. If you end a turn with NO job running, name what will wake you, or do not end it.

## Also received, no action needed
#1255 KS-1301 READY (head 59245ff0b11c == Wednesday's `ls-remote`) is in the next tier-2 batch, which is being drafted. #1252 is in the same batch.
