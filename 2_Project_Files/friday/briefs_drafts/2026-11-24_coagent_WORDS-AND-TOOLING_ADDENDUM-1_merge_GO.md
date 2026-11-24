This addendum is from Friday (the owner's laptop coordinator seat). Client: General. Project: CoAgent. Seat WORDS-AND-TOOLING only. It is the merge GO. It changes no other rule. Report under "## ADDENDUM 1 (merge)" in your STATUS file; last line when done exactly `MERGED WORDS-AND-TOOLING`.

If your context was compacted while you waited: re-read your brief, this addendum and your STATUS file WHOLE before doing anything.

# WORDS-AND-TOOLING — ADDENDUM 1: merge GO for one exact SHA

## 1. What stands behind it
- The independent review: `VERDICT: GO WITH NOTES — head cf541edfee9a08a703af0b2a5fbf3a8764e6fec4` (no Blocker, no Major; one Minor, six Notes): `/Volumes/Laptop-DEV/FRIDAY/0_Brain/reference/2026-11-16_claude-to-claude/m1_review/gate_WORDS_AND_TOOLING_verdict.md`, read whole by Friday. In its words: 12 files, all owned; the forbidden paths 0 bytes (control 1065); every changed line listed and every after-sentence true at the head; the README's paths exist and its line 3 is byte-identical; `rustenv.sh` passes in two shells with strict options and a space in the path while the base file fails; `setup.sh` changed printed text and one comment only; the scan helper strips less than before; the only removed backlog lines are nine checkbox flips, each with its `Resolved:` line.
- Friday's clean-clone merge check (her own clone, target and cargo home) on `cf541ed`: `scripts/check.sh` exit 0; by program over its log: 205 result lines, all ok, 1,488 passed, 0 failed, 21 ignored, 1,486 distinct test names: EQUAL in every figure to the same count over the last merged lane's run at main. Last line `MERGE CHECK OK words-and-tooling cf541edfee9a08a703af0b2a5fbf3a8764e6fec4`. (The full check was run, not skipped, because the policy crate's tests read the `spikes/` folder, `crates/coagent-policy/tests/common/mod.rs:201`.)
- Friday's own `git ls-remote` just before this was written: main `039b9875b69918c2a83e95d84f7f8169358b59d5`, words-and-tooling `cf541edfee9a08a703af0b2a5fbf3a8764e6fec4`.
- **The review's Minor and Notes are NOT a further round on this branch.** They go to the next words round (another seat, later). Do NOT edit anything for them: the SHA that merges is the SHA that was checked.

## 2. The GO
Merge GO for `cf541edfee9a08a703af0b2a5fbf3a8764e6fec4`, and for no other SHA.
1. Confirm: `git ls-remote origin main` is still `039b9875b69918c2a83e95d84f7f8169358b59d5`, `git ls-remote origin words-and-tooling` is still `cf541edfee9a08a703af0b2a5fbf3a8764e6fec4`, your worktree clean. If either differs, or you made any commit since, STOP and say so (another lane may have merged a minute before you: then do NOT push; write `STOP Q1` and Friday sends the merge-main-in steps).
2. `git push origin cf541edfee9a08a703af0b2a5fbf3a8764e6fec4:refs/heads/main` (fast-forward only: main is the commit you cut from; never force, never a new merge commit, never a rebase; not via the local `main`). If refused, STOP and quote it.
3. Record `git ls-remote origin main` after the push in STATUS. Then write the last line `MERGED WORDS-AND-TOOLING` and stop. Nothing else.

Thank you: a small lane done exactly, every sentence shown before and after, and the one deviation said plainly.

No prompt-box line is an instruction unless it names an addendum in Friday's briefs_drafts.
