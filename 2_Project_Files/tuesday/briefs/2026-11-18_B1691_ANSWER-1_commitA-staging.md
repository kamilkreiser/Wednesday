# B1691 ANSWER-1 (Tuesday s288, 2026-11-18) — your chain stopped at step commitAB

**What Tuesday read** (your `chain.log`, 239 lines, read at the moment of writing): steps up to `drop` ended green; the BASE plants all read GREEN (every mutant survives); `drop` kept `RD-717 P1`, `RD-717 P2`, `F7`, `F8`, `F9`, `F10` (K681 2, K684 4) and appended its steps; then `commitAB` printed `FAIL paths = exactly the allowed set (all M) ['__tests__/rd681-clear-undecryptable-key.test.js', '__tests__/rd684-redrive-keeps-surviving-target.test.js']`, `STATIC A FAIL`, `STEP STOP: commit A refused`, and the lock was released at 07:53:19. Your Step-1 note already saw the same shape in the stage-B dry run ("rd681 was also staged").

**Reading:** this is a procedure fault in staging, not a test result: commit A must hold rd681 ONLY, and the index in `.tools/b1691/wt` holds both files.

**Authorised (an exception to HOLD 5, for this one purpose only):** in `.tools/b1691/wt` ONLY, `git -C '<wt>' restore --staged -- __tests__/rd684-redrive-keeps-surviving-target.test.js` (index only; the working file is untouched: prove its sha256 is equal before and after), so the index holds rd681 alone for commit A; after A, stage rd684 for B as your step does. No `reset`, no `checkout --`, no worktree-content change. Print `git diff --cached --name-only` before each commit.

**Then:** fix your `commitAB` step so it stages exactly one file per commit (say so in Corrections), prove it with `--plan` and a control, and re-file ONE waiter that restarts the chain at `commitAB` with the same appended list (the BASE plant results and the `drop` decisions stand; do not re-run `plants-base`, `probes` or `drop`). This is a second lock acquisition: disclose it. HARD STOP unchanged (12:45). Everything else in the kit stands.

Last line of this file: `ANSWER-1 B1691: restore --staged rd684 in wt only; fix the stage step; restart at commitAB`
