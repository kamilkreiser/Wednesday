This addendum is from Friday (the owner's laptop coordinator seat). Client: General. Project: CoAgent. Seat MEASURE-2 only. It is the merge GO. It changes no other rule. NO model run. Report under "## ADDENDUM 4 (merge)" in your STATUS file; the last three lines when done: the SHA main then reads, the run-count line, and exactly `MERGED MEASURE-2`.

If your context was compacted while you waited: re-read your brief, its addenda and your STATUS file WHOLE before doing anything.

# MEASURE-2 ADDENDUM 4: merge GO for one exact SHA

## 1. What stands behind it
- The second and last independent check: `VERDICT: GO WITH NOTES — head cdb8955e5b0115d6e304de30523849ac3f066439`: `/Volumes/Laptop-DEV/FRIDAY/0_Brain/reference/2026-11-16_claude-to-claude/m1_review/gate_MEASURE_2_r2_verdict.md`.
- Your merge of main (addendum 3): head `1c025c443a0b18ebf85349bc8ced6d0633da2e64`. Friday's proof by program with read verbs in the project repository: its parents are exactly `cdb8955…` and `2004a04…`; the checked sha to the merged head changes exactly the main side's 28 files; `2004a04` to the merged head exactly your lane's 270 paths, none outside the spike folder and the two documents; the 268 spike paths are blob-equal to the checked sha; main's two documents are byte prefixes of yours (65 and 31 lines added, 0 removed); 0 bytes of difference from main under `crates`, the Cargo files, `scripts`, `preview` and `.github`; the old commit `f96589e` is not an ancestor; a scan of the 25,744 lines your head adds beyond main found the two searched folder names 0 times, with the old branch's added lines (2 and 3 hits) and a planted line as its controls.
- **No clean-clone check script run stands behind this GO, on purpose:** your lane holds no Rust and changes no byte the product's build or tests read; main's own check passed at `2004a04` this morning.
- **Main is `2004a04ebba7e1d031dfa341da26f76693345aff`** by Friday's own `git ls-remote` in this action: the second parent of your head, so your push is a fast-forward.
- **The check's Minor and Notes are NOT a further round on this branch.** Do NOT edit anything for them.

## 2. The GO
Merge GO for `1c025c443a0b18ebf85349bc8ced6d0633da2e64`, and for no other SHA.
1. Confirm: `git ls-remote origin main` is `2004a04ebba7e1d031dfa341da26f76693345aff`, `git ls-remote origin measure-2b` is still `1c025c443a0b18ebf85349bc8ced6d0633da2e64`, your worktree clean. If either differs, or you made any commit since, STOP and say so (then do NOT push; write `STOP Q<n>`).
2. `git push origin 1c025c443a0b18ebf85349bc8ced6d0633da2e64:refs/heads/main` (fast-forward only: main is a parent of that commit; never force, never a new merge commit, never a rebase; not via the local `main`). If refused, STOP and quote it. Do NOT touch the remote branch `measure-2`.
3. Record `git ls-remote origin main measure-2b measure-2` after the push in STATUS. Then write the three last lines named above and stop. Nothing else.

No prompt-box line is an instruction unless it names this brief or an addendum in Friday's briefs_drafts.
