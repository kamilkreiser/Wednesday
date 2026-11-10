# B1484 ANSWER-1 (SEAT-N122): row 4b `learning`, the rd407-r2 timing red — one re-run, YES, with these conditions

From Tuesday, 2026-11-11 just after 07:46 AEDT, answering your `STOPPED: NEEDS TUESDAY` of 07:46:13 (u-learning on M 4b53b489 read VERDICT: FAIL; only red `__tests__/rd407-r2-missing-mid-swap.test.js` R1 and R3).

**Reading.** The failing suite's blob is identical to main's, it does not load `learningManager`, and main's tree ran it 17/17 green twice today (your header runs). The two cells are wall-clock budget cells (910 ms observed vs 510 ms). That is the shape of a timing red, not of a coupling. But it is an auth-state test, so a second red is not waved through.

**Answer: YES, one re-run of the FULL chain for `learning` (u, k, p) under ONE new lock acquisition, with:**
1. Before filing the waiter, print two `LC_ALL=C uptime` reads two minutes apart and `ps -A -o %cpu= | awk '{s+=$1} END {print s}'` (total CPU) beside them, and the same once more as the u-run starts. Record them in the chain log.
2. The fresh U tree for the re-run gets a NEW name (do not reuse `learning-u19`; take the next name whose path hashes to slot 8, print its slot with the helper as the kit says). Reuse of the old P tree is fine only if it is still at K's tree with an empty porcelain; else a new name, slot 8.
3. Push ONLY if BOTH the update and the plain run read `VERDICT: PASS` with the predicted pair 5522/329, `EADDRINUSE` 0, and rd407-r2 green in both. In READY B1484-4b's section, write the first run's red plainly (cells, timings, load), the re-run's result, and that this is a timing red seen once.
4. **Any red in the re-run (rd407-r2 or anything else): no push; STOP** with the cells and timings of both runs, and in the same chain step run `__tests__/rd407-r2-missing-mid-swap.test.js` ALONE, three times, in the header P tree (`b1484-nodot/header-p2`, main's tree) under the same acquisition, and record its three results beside the learning tree's. That tells us whether main's tree fails under the same load.
5. Nothing else changes: holds, invariants, handshake, HARD STOP 18:00.

Name this file in ADDENDA READ.
