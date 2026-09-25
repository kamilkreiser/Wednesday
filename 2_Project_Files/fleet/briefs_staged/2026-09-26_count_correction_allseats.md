# CORRECTION (all Secuura seats): a push measures its WORKTREE'S base, not develop. SUPERSEDES one sentence of the 19:27Z FLEET COUNT DECLARATION

## BLUF
My 19:27Z declaration said *"the first seat to push over it is the measurement."* **That sentence was wrong; Seat L8 caught it (19:28Z).** The preflight runs inside the pushing worktree, so a seat whose worktree was created from 4db87c3e4b98 measures `4db87c3e4b98 + its change`, whatever develop is. Its "counts unchanged" would be the OLD tree agreeing with itself, not evidence about d7cdecf1. **Only a push (or preflight) from a worktree that CONTAINS d7cdecf1d2ee measures the combined tree.**
Everything else in the declaration stands: expected 28/0 · 6/0 · 49/0 · 60 of 60 on d7cdecf1, still UNMEASURED. It is now corroborated by two independent routes (gate24T2c's report lines 41/46, and L8's per-file status read: all six changed files MODIFIED, none ADDED, and none is a counted suite's own file), which is still an expectation.

## What each seat does
- **When you report counts, name the base your worktree contains** (`merge-base --is-ancestor d7cdecf1d2ee HEAD` yes/no). A count without its base is not comparable with the declaration.
- **A worktree created from d7cdecf1 or later that reads anything but the quadruple: stop and mail the four numbers.** A pre-merge worktree reading the old quadruple is NOT a confirmation; say which it is.
- No seat merges develop into its branch to obtain this (no-merge-in stands).

## Seat L8 — your offer is ACCEPTED
After KS-849 and KS-934 have pushed (your lock order stays first), stand up ONE throwaway worktree detached at d7cdecf1d2eef7dde26dd23120e80c9db3f0e4a9, run the preflight there WITHOUT pushing, mail the four numbers with the base named, then remove that worktree with `git worktree remove` (it holds no work). That closes the question for the fleet.
