# B1492 ANSWER-2 (SEAT-N123): old-slow liveness by an in-realm probe: accepted

From Tuesday, 2026-11-11 just after 13:21 AEDT, answering your `STOPPED: NEEDS TUESDAY` of 13:21:52. Supersedes ANSWER-1 items 2 and 3 for step 1; ANSWER-1 items 1, 4 and 5 stand.

**Yes.** An in-realm probe is the right proof that the shim is live (a check run where the code under test runs; Tuesday's ledger now requires exactly that). Do it this way:
1. In the scratch tree `mut24` only, write an untracked one-cell jest file (no product file, nothing committed) whose single cell times `Atomics.wait(new Int32Array(new SharedArrayBuffer(4)), 0, 0, 200)` with `process.hrtime.bigint()` inside the test, and asserts nothing but prints the elapsed ms (write it to a JSON file you read by program).
2. In the SAME acquisition as old-slow: run the probe once UNDER the same `--setupFiles` shim (required: at least 600 ms) and once WITHOUT it (control: under 600 ms). Print both.
3. old-slow is then judged only on: all 3 runs have exactly M2, R1, R3 FAILED and the other 14 passed.
4. For step 4 (`new-slow`, the NEW cells), keep the kit's 1500 ms per-cell bar AND run the same probe pair once in that step's acquisition window too (cheap, and it proves the shim for those 20 runs by the same method).
5. Afterwards move the probe file into `.tools/b1492/_quarantine/` (never delete) and show `git status --porcelain` of `mut24` empty before the mutation step.
6. Your 13:20 and 13:21 old-slow runs are evidence (the control fires twice), not counted runs. Name this file in ADDENDA READ and re-file the chain.
