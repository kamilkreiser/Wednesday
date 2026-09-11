## BLUF
- **SUPERSEDES, for #954 only, the brief's item-1 clause "If it landed as a merge commit (two parents), STOP and mail".** It did land as a merge commit. That is accepted, and it is not a stop.
- **Measured by Wednesday** (GitHub REST API on Secuura/Distributed_Secuura, Secuura key, read-only, 17:5x AEST):
  - #954 merged at 07:49:56Z by `kksecura` — Kam, who wrote "done" on his panel at 17:50 — as merge commit `2600229efedae9682339064d8127ccf035b90afc`;
  - its parents are `19cc900695cc699d3f916c6a6066bf35efe6db5d` (develop's tip before it) and `355d82c8b02792a2d25992db9ec0e2bdc636f318` (the gated head);
  - its diff against the first parent is exactly #954's 9 files.
- **develop moved twice after the brief's figures:** Peter merged #899 (KS-971) at 07:46:46Z as `19cc90069`, then Kam merged #954. develop read `2600229ef` at 17:5x (`ls-remote`). Neither merge touches #953's 2 files.

## What changes for you
1. **#954 — verify, do not merge.** Check all three:
   - second parent == `355d82c8b…`;
   - `git diff --stat 19cc90069 2600229ef` lists exactly the PR's 9 files;
   - `git merge-tree --write-tree 19cc90069 355d82c8b` gives the same tree as `2600229ef`.

   If any one differs, STOP and mail. Otherwise do step (e) for KS-597: the comment says Kam merged it as a merge commit whose second parent is the gated head.
2. **Do not revert, re-merge or rewrite anything about #954's history.** The squash convention (`CONTRIBUTING.md:107`) still applies to every merge YOU make, #953 included.
3. **#953 is unchanged** — re-read develop's tip T immediately before it. It is no longer `38a919d40`.
4. **Kam, panel, 17:50:39:** *"you also have my approval to merge anything that has been finished and tested"*. It does not widen your round: you merge #953 and verify #954; the census still merges nothing; Wednesday GOs census rows one at a time.

## Unchanged
Everything else in the brief stands.
