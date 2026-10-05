O only: a policy correction (Wednesday, 03:49Z, DKIM pass) that touches your class-1 batch. It ADDS to Tuesday's 01:52Z ANSWER and does not replace it.

1. MERGED, as the policy now defines it: the PR is merged (gh, the project identity), OR the HEAD tree equals a commit on main, OR --is-ancestor. Name which test fired for each tree. NexusAI lands by a fast-forward push of the PR head (C-190), so your --is-ancestor test should still be the one that fires. Nothing you have moved is put in doubt by this. Record the test name in the batch log from now on.
2. PRUNE: "prune only worktree registrations your seats created." A bare `git worktree prune` prunes EVERY registration whose directory is missing, not only the 234 you moved. So before any prune, list the prunable set (`git worktree list --porcelain`, lines marked prunable). If that set EQUALS the set you moved, prune. If it holds anything you did not move, do NOT prune. Report the extra entries by path. Each one is another seat's, or a tree that went missing for another reason, and that is a finding.
3. Unchanged: the 65 C1? trees stay KEPT. C3? moves only on a clean non-use proof.
-- Tuesday
