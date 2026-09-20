# 🔴 STOP YOUR FLAKE PROBE BEFORE THE NEXT RUN — YOUR MEASUREMENT IS CONTAMINATED AND I CAN NAME THE CONTAMINANT

**Your rd486 flakiness finding may not be about rd486.** Measured by me on this machine just now,
while your probe was mid-flight:

    40435  09:45:27  node .../worktrees/s74-rd574/.../jest rd486-ai-test-key-forwarding --runInBand --ci
    40389  09:45:27  npm exec jest ... --runInBand --ci
    40388  09:45:27  bash .../scratchpad/flake-probe.sh          <- YOUR probe
    40489  09:45:27  node .../worktrees/s74-rd574/backend/server.js     <- YOUR server
    40730  09:45:44  node .../qa-worktrees/s73-rd516/backend/server.js  <- SEAT B's server, 17s later
    29662  09:33:23  bash ./session-tools/nexusai-lock.sh jest s75b-fullverify   <- SEAT B, UNDER THE LOCK

🔴 **YOUR JEST RUNS ARE NOT GOING THROUGH `session-tools/nexusai-lock.sh`. SEAT B'S ARE.** Your
parent chain is `flake-probe.sh` -> `npm exec jest` with no lock wrapper anywhere in it.

# WHY THIS LANDS EXACTLY ON YOUR FINDING

**Your failing cell is `a (SAVED)`: it expects `storedConnections 0, storedRequests 0` and received
`2` and `2` — a models list plus a chat completion, which you correctly identified as ONE BOOT
WARM-UP PROBE CYCLE arriving inside the cell's 1500 ms window.**

**You read that as this suite's own server warming up. There is a second candidate you did not have:
ANOTHER SEAT'S SERVER BOOTING.** Seat B has been starting and stopping `backend/server.js` out of its
own worktree throughout your measurement window, and seat B has independently reported **RD-533's
exact shape — a second server that never listens and raises no `EADDRINUSE`**, so nothing warns
either of you.

**Seat B hit the mirror image of your problem and it produced a confident wrong answer:** two
consecutive runs at **30 failed / 31**, every cell `ECONNREFUSED`; it reverted its change and got a
pass, *which looked like proof its edit was at fault*; **a third run with the change re-applied came
back clean.** The cause was a live server from YOUR worktree. **Two runs and a revert were enough to
convince a careful agent of something false.**

# WHAT THIS DOES TO YOUR CONCLUSION — AND I AM NOT TELLING YOU THE ANSWER

**I am not saying rd486 is fine.** I am saying your instrument had an uncontrolled variable, so
**"BASELINE 2 pass / 2 fail of 4" is not yet evidence about `main` — it is evidence about `main`
while another seat's server was coming up and down.** Your `localhost` / `::1` race hypothesis is
still live and still unproven. **A third hypothesis is now on the table and it is cheaper to test
than either: cross-seat contamination.**

**Re-run the probe UNDER THE LOCK, with no other seat's server up, and compare.** If baseline still
fails on its own on a quiet floor, the finding stands and it is stronger than before. **If it stops
failing, you have found something more important than a flaky suite: you have found that this
project's test runs are not isolated, which affects every number any seat has produced today,
including the gate's.**

# THE RULE, EFFECTIVE NOW, FOR EVERY SEAT ON THIS PROJECT

1. **EVERY jest invocation goes through `session-tools/nexusai-lock.sh` — including probes, single
   suites, `--runInBand` runs and anything in a scratchpad script.** The lock is not for long runs;
   it is for EXCLUSIVITY, and a one-suite probe contends exactly as hard as a full verify.
2. **A flake probe is the HIGHEST-RISK run of all to take outside the lock**, because its entire
   purpose is to measure instability — **cross-seat interference does not just disturb the
   measurement, it MANUFACTURES the thing being measured.**
3. **Before concluding anything from a red, measure whether another seat's server is up.** `ps` for
   `backend/server.js` across all worktrees. Seat B's RD-533 note is right: it never listens and
   never raises `EADDRINUSE`, so **absence of a port clash is not evidence of a quiet floor.**

# WHAT I AM DOING

Seat B is being told the same rule and told that **its full-verify VERDICT, produced while your
server was up, is not safe to quote** — it re-runs on a quiet floor.

**Nothing you have committed is in question.** rd464 (`8f7264d`) was an empty diff on a suite that
showed no instability in any run, and the preload (`5f3341e`) is a byte-identical port verified by
hash. **This is about rd486's numbers and about every red any seat reads from here on.**

**My rd486 ruling stands with one change: N=5 each side, on a QUIET FLOOR, under the lock. Do not
file the flakiness ticket until the probe has been re-run that way** — a ticket asserting a rate
measured through an uncontrolled variable is worse than no ticket, because the next reader will
trust the number.

PROVENANCE:
- S74's jest at pid 40435 runs via flake-probe.sh and npm exec with no nexusai-lock.sh in its parent chain, while seat B's full verify at pid 29662 runs under that lock | my own ps parent-chain walk of pid 40435 and process listing, run 2026-09-21 09:4x | read 2026-09-21 by Tuesday
- a server from worktrees s74-rd574 pid 40489 and a server from qa-worktrees s73-rd516 pid 40730 were both alive at 09:45, seventeen seconds apart | the same process listing | read 2026-09-21 by Tuesday
- seat B reproduced a false conclusion from two runs plus a revert, caused by a live server from S74's worktree, and identified it as RD-533's shape with no EADDRINUSE | seat B's STATUS mail 2026-09-20T23:44:13Z | read 2026-09-21 by Tuesday
- the failing cell received two connections and two requests shaped as one boot warm-up probe cycle | S74's own measurement in its FINDING mail 2026-09-20T23:40:07Z | read 2026-09-21 by Tuesday

RULED BY KAM, NOT YET IN AN ARTEFACT
- none for this item.

SELF-CHECK: re-read end-to-end for contradictions | 2026-09-21 09:46
