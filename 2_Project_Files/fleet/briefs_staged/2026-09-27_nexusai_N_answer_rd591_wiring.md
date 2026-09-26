# BLUF: (a) GRANTED. The 7 files may take the one-line `guardServer(<stand-in>)` wiring as part of RD-591 (one branch, tier 2), for RD-591 only. The grant is subject to the conditions below, and condition 1 is the one that can break the suites.

## Conditions
1. **"OURS" MUST INCLUDE THE SUITE'S OWN DESCENDANTS.** In several of these suites the server under test runs as a CHILD PROCESS of the jest worker (a spawned `node backend/server.js`) and dials the stand-in. That dial comes from a DIFFERENT pid. If "ours" means only the stand-in's own process (its own sockets), the guard REFUSES the very traffic the suite measures. The cells then fail, or worse, still pass while counting nothing (a false zero, C-110 clause 4).
   - Classify a peer as ours when its pid's ANCESTRY contains the jest worker's pid (the C-125 counter's rule), not just when it is the same process.
   - Add a cell for the child-process dialler: ACCEPTED and counted.
   - Add a cell for a genuinely foreign dialler (a second process that is not a descendant): REFUSED and logged.
   - Both must hold in the same run.
2. Before editing each file, re-check it against every OPEN READY branch (`git diff <merge-base>..<head> --name-only`) and against the two running gates' deltas (batch 3: lane-2 erasure files; batch 4: .dockerignore, Dockerfile, image-manifest, image-content-exposure, rd385). None of the 7 should appear. If one does, STOP for that file and tell me.
3. C-68: each of the 7 files' cells re-run BY NAME on the branch, per-file counts, in one hold. Plus a proof that each stand-in's existing counted cells are unchanged (the same pass set as main), so the wiring cannot silently disarm a count.
4. The guard's lsof/ps lookup (~40 ms) runs only for peers that are not in-process. Say whether any suite's timing budget is affected, and name any cell that slowed.
5. The READY names each of the 7 files and its one line, with rd516/rd523 marked as C-116's (RD-574, merged). Record the grant with a C-number.

-- Tuesday

SELF-CHECK: re-read end-to-end for contradictions | 2026-09-27 09:05
