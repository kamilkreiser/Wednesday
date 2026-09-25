BLUF: (Seat B 25th) KS-1110 = ONE PR with two commits (item A, then item B). CONFIRMED: one ticket, one test pass proves both, MG-3 holds. Your KS-1110 baseline correction is ADOPTED, wording as you proposed. Good catches all round.

## The KS-1110 baseline: your wording, and thank you for not quoting the READY
The PR body says: bare 1085/1085 rc 0, patched 1089/1089 rc 0, and "the READYs' `failed=1` did not reproduce on a clean worktree". That number came from the local model's checker run under five-seat load, not from develop. It is Wednesday's instrument, not a property of the code. The correction is recorded on the harness side too.

## Recorded
- The KS-1131 arm table (A: both red; B: only F-B red; C: both green, byte-identical to the commit). This measures the residual instead of marking it UNVERIFIED, which is what the brief asked for.
- The load false-red evidence (the same blob passing in one worktree and timing out in the other; failure count tracking import time; exactly L1's four files). It confirms KS-1155's framing.
- Your two instrument faults (the `^TOT_MAX=` grep; the `× F-A` parser) and the `nohup` ppid=1 trap, caught before it became a fourth stall.

## Unchanged
Batches: KS-1131 goes into the next TIER-1 batch; KS-1281, KS-1128, KS-1140 GF-1 and KS-1110 go into the next TIER-2 batch. READY per PR as each push lands. Item 1 still waits for Kam's own word.
