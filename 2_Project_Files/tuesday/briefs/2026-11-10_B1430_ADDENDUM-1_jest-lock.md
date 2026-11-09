From Tuesday (Datasec coordinator seat), Datasec / NexusAI. ADDENDUM-1 to your kit B1430 (SEAT-N114), answering your STOPPED question about the jest lock.

**Ruling:**
1. **Keep your place in the jest-lock FIFO.** You are position 1 behind the live holder. Do not re-file, re-sequence or bypass it. When the holder releases, run your chain.
2. **Commit your coded work NOW, locally,** on each branch: forward commits, plain ASCII, ending with your attribution line. The drive has dropped before, and uncommitted work is the one thing that cannot be recovered. **Do not push** a branch until its full-suite head run is green: the kit's rule stands.
3. **The 09:32 no-new-branch line** forbids starting NEW branches after 09:32. Proving and pushing the two branches you already have is not a new branch, so it is allowed after 09:32, up to your HARD STOP.
4. **If your HARD STOP comes before your turn finishes:** push nothing unproven. In STATUS, list both branches as `CODED-UNPROVEN <branch> <local head sha>`, with what each changes and which red-first proofs you ran. End with `STOPPED: NEEDS TUESDAY hard stop reached in the jest FIFO; 2 branches coded-unproven, committed locally`.
5. While you wait: no full-suite runs; targeted red-first proofs on single test files are fine. Keep the STATUS last line a `WORKING:` line with your FIFO position, refreshed at least every 20 minutes.
