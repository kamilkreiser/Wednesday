# ADDENDUM 1 to 2026-10-19_testing-agent-qa-scratch-cleanup.md (from Wednesday)

SUPERSEDES the brief's Step 1 rule "`.git` is a FILE → a worktree registered in another repository. Do not remove these."
That rule was written to protect ANOTHER project's repository. Wednesday measured the actual pointers read-only: every
`projects/secuura/reports/*/wt/*/.git` file's `gitdir:` points INTO a clone in the SAME report folder (38 into the
sibling `clone/.git/worktrees/`, the rest into another clone of that same report, e.g. `clone.50cv/repo/.git/worktrees/`).
None points into any other project. So you were right that the literal rule would keep almost all of the space.

The new rule:
1. A worktree whose `gitdir:` lies inside an in-scope clone of the SAME report folder is removed TOGETHER with that clone,
   as one unit (the worktree directories first, then the clone). Kam's card text covers it by name: "the regenerable QA
   clones and worktrees".
2. A worktree whose `gitdir:` points ANYWHERE outside its own report folder stays, and is listed with its gitdir line.
3. Every other test in Step 2 applies to the unit as a whole: older than 7 days, nothing open under any of its paths
   (re-checked just before removal), the report itself still present.
4. Do not run `git worktree remove` or `prune`: removing the clone removes its registrations with it.
Everything else in the brief stands, including the STOP conditions and the report.
