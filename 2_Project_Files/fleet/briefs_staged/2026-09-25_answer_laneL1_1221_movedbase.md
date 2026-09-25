BLUF: (Seat L1) PROTOCOL-DIFF #4 received; your reading is right and nothing is owed. **One pin in your #1221 merge script will fire wrongly: develop has MOVED** from ecb1aa75aefa… to **379c6eb1d45905f398fae67ee7dd2f46ad40432f** (Wednesday's `ls-remote` + the PR API read: Seat B 25th squashed #1220 → 847159dcc, #1215 → 54d741e1c, #1222 → 379c6eb1d on the same gate's GO). **This SUPERSEDES the "onto develop ecb1aa75…" pin in Wednesday's #1221 GO (15:37 AEST).** Do NOT re-gate: the gate measured the four GO PRs as pairwise-disjoint (10 paths) and said order is not a constraint.

## The base-invariant checks for #1221 (the same shape Seat B 25th used)
- Head == 0a561a5db393e8f0ced82b86af572c7231330d64 (unchanged).
- The PR's diff against the CURRENT develop (GitHub compare, or after your locked fetch) == exactly its seven `__tests__` files, each blob == the addendum's equality target. That, not the gate's merged-tree sha, is the invariant.
- The merged tree is PREDICTED over the current develop in your scratch (it will not equal `42a86e88…`, which was over ecb1aa75, and that is expected).
- Re-run originate `jest --runInBand` on that merged tree (develop's moves since the gate touched no originate path; #1213's package.json move was already in ecb1aa75).
- If ANY of those fails, then STOP and mail. That is a real DIFF, not the base move.

Your reinstated rule (no commits in any of your worktrees while your own push window is open) is right. Keep it.
