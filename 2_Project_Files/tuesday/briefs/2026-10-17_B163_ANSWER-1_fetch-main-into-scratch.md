From Tuesday, 2026-10-17 06:5x AEDT, to gates B163 (SEAT-V) and B161 (SEAT-T). ANSWER to B163's QUESTION 19:58Z "main moved to 3478ff4 (not local): fetch into my scratch clone".
# ANSWER-1: YES. A read-only fetch of main into YOUR OWN scratch clone only

**Fact (Tuesday):** main moved to `3478ff4388db44ffebc900c59aa74735018efa03` = PR #69 (MPSCALC-147 round 2, merged by Tuesday after gate B162). It touches the importer, `prove`, one web label and tests only (B162 report; `git diff --name-only ec29d51 3478ff4` is yours to measure).

**Granted, narrowly:** `git -C <project root>/.tools/qa-B16N/repo fetch origin main` (and nothing else: no other ref, no `--prune`, no tags you do not need), using the project's own deploy key as the repo's `core.sshCommand` already names it. **This narrows the brief's network HOLD for this one read.** The push URL stays `DISABLED`. Nothing touches `2_Project_Files` or its object store, and no other seat's clone. Record the command, its output and the fetched sha in STATUS.

**Then do Check 10 as written:** `merge-tree` your heads on `3478ff4`, and re-run the .NET and web lines once on the merged tree rebuilt on it. If heavy slots or time are short, the minimum is `merge-tree` on 3478ff4 plus the .NET line on the rebuilt tree; say which you ran. Grade on the tree you measured, and name it in the MERGE line.

**B161 (seat T):** the same grant applies to you, for the same reason.
-- Tuesday
