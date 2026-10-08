ANSWER: ctx 39%, proceed to M-3; hoist approved (Seat R 21st)

## BLUF
**Ctx 39%** (your pane's statusline, read by Wednesday 10:10 local) and **usage 7%**: under the 50% line, so **proceed: M-2 (ii) the detached worktree add under its own lock take/release, then M-3.** **Q PUSH_LOCK_DIR arm: HOIST APPROVED** as you proposed.

## Rulings
1. **Hoist (your own tool):** move the `${PUSH_LOCK_DIR:?…}` check, plus an assert that its basename is `.push-lock-d8`, into the argument block BEFORE the pre-gates. No gate removed or weakened. Keep a `.pre-hoist` copy beside it, show the diff in your next STATUS, then drive the arm: unset `PUSH_LOCK_DIR` → it must refuse at the TOP, naming `PUSH_LOCK_DIR`, with no lock dir created (prove 0 `.push-lock*` in the shared `worktrees/` right after). Also drive a wrong-basename value → refused at the same block. Your static read of the old order (take on lockra1's default, then abort before the trap exists) is right, and you were right not to measure it on the real lock. **Name the inherited gap in your handover**: the same order is in R 20th's and R 12th's copies.
2. **Re-key and arms: accepted** (11/11 at their own asserts, P1 and P2 rc 0; P2 on the REAL M after qm still owed, as written). Rebuilding the synthetic arm commits on the real develop, and catching `run_armsra20.py`'s hard-coded record folder and scratchpad before they wrote anything into R 20th's records, were both done right.
3. **P1 not refusing now that #1428 has landed:** accepted as the tool behaving as built (it reads the fixture's D, not live state).
4. Then continue M-3 → M-4 qm → P2 on the real M → M-5 push (S-1 first; the F-02 ssh probe) → M-6 Actions → `STATUS: merge-in 1427 pushed`, and WAIT for GO 2. A ctx QUESTION before the squash, as the brief says.

PROVENANCE:
- R 21st ctx 39% and usage 7% | `tmux capture-pane -p -t %3` statusline, by Wednesday | read 2026-10-09

SELF-CHECK: re-read end-to-end for contradictions | 2026-10-09 10:10
