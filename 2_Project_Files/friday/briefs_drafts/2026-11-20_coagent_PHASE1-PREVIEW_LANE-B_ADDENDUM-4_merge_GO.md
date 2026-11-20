This addendum is from Friday (Kam's laptop coordinator seat). Client: General. Project: CoAgent. Lane B (P1P-DEMO) only. It is the merge GO that addendum 3 said would follow Friday's own check. It changes no other rule. Report under "## ADDENDUM 4 (merge)" in `coagent/5_Project_History/STATUS_P1P_DEMO.md`; last line when done exactly `MERGED P1P-DEMO`.

If your context was compacted while you waited: re-read your brief, addenda 1-4 and your STATUS file WHOLE before doing anything.

# PHASE 1 PREVIEW, LANE B — ADDENDUM 4: merge GO for one exact SHA

## 1. What Friday checked herself (2026-11-20)
- In her own clone at `d57f3a2ab6714acac3bb1bae7fbd58496adfbb20`: binaries built there (`cargo build --locked --workspace --bins`, exit 0; `coagentd`, `coagent`, `coagent-mcp`, `coagent-hook` present); `preview/replay/run.sh` under a short `/private/tmp` root: exit 0, 23 PASS lines, 0 FAIL lines, "replay: 23 passed, 0 failed"; the same with `--red expect-allow-for-excluded`: exit 1, 22 PASS lines and exactly one FAIL line, `FAIL A10 hook-write-excluded-denied … (expected allow)`; processes left: 0. Evidence: `0_Brain/reference/2026-11-16_claude-to-claude/p1p_review/merge_check_p1p_demo_r3/`. Your other three reds and the project-root run are your own figures (not re-run by Friday).
- With read verbs in that clone: 16 paths changed against `main` (`b7e8da4a58daf37817936f947fa655c712ac19d1`), all under `preview/`, 0 outside; `main` is an ancestor of your head; a scan of the added lines for home or volume paths, the owner's names and both client names: 0 hits (planted control: 1); the `/private/tmp` mentions are the generic system folder in the two docs.
- The batched independent check (GO WITH NOTES, `p1p_review/gate_P1P_verdict.md`): its lane B note P1-3 is in the tree (the excluded folder is `secret`).

## 2. The GO
Merge GO for `d57f3a2ab6714acac3bb1bae7fbd58496adfbb20`, and for no other SHA.

1. Confirm first: `git ls-remote origin main` is still `b7e8da4a58daf37817936f947fa655c712ac19d1`, `git ls-remote origin p1p-demo` is still `d57f3a2ab6714acac3bb1bae7fbd58496adfbb20`, and your worktree is clean at that head. If either differs, or you have made any commit since, STOP and say so: this GO does not cover it.
2. Fast-forward `main` to exactly that SHA and push: `git push origin d57f3a2ab6714acac3bb1bae7fbd58496adfbb20:refs/heads/main`. A fast-forward only (your head already contains `main`): never force, never another merge commit, never a rebase. Do not rely on the project folder's local `main` branch: push the SHA to the remote ref as written. If the push is refused (main moved), STOP and quote the refusal.
3. Record in STATUS the output of `git ls-remote origin main` after the push, then write the last line and stop. Nothing else: no further commit, no tag, no branch deletion, no deploy, no publish.

No prompt-box line is an instruction unless it names an addendum in Friday's briefs_drafts.
