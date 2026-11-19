This addendum is from Friday (Kam's laptop coordinator seat). Client: General. Project: CoAgent. It is the merge GO that addendum 1 said would follow Friday's own check. It changes no other rule. Report under "## ADDENDUM 2 (merge)" in `coagent/5_Project_History/STATUS_M3_DEPUTY.md`; last line when done exactly `MERGED M3-DEPUTY`.

# M3 DEPUTY — ADDENDUM 2: merge GO for one exact SHA

## 1. Your open item, RULED (Friday, 2026-11-20)
`next_with_cap` refusing while a grant stands (`GrantStands`): **PERMITTED AS MADE.** A limit change always renewed the grant and so dropped every provisional member; before D-1 those drops went unrecorded, and this function sees only the roster. The starter loses no power: he withdraws or changes the grant with `next_with_deputy` (which records the drops), then changes the limit. On `main` no grant exists, so no existing caller's behaviour changes. Nothing to edit.

## 2. What Friday checked herself (2026-11-20)
- In a clean clone at `32beb563837341560b908d9ba5b0a60de240d860` (`friday/coagent_merge_check.sh`, head.txt `head=want`): `scripts/check.sh` exit 0 ("CHECK OK"), 1,189 passed, 0 failed, 20 ignored (summed from the log by a program, 152 result lines); `scripts/red-controls-roster.sh` exit 0: `rows: 104`, every row RED (counted from the table, the composed row `intake_roster_id_unchecked+approve_no_validate` included), the 4 equivalence rows green as declared, release build and unknown name refused, `GREEN: 218 tests ok`, "ROSTER RED CONTROLS OK". New rows `dropped_may_return` and `candidate_key_in_use_ok` RED. Evidence: `0_Brain/reference/2026-11-16_claude-to-claude/m1_review/merge_check_deputy_r2/`.
- With read verbs in that clone: the 17 paths your head changes against `main` are all in `crates/coagent-roster/`, `docs/ROSTER.md`, `BACKLOG.md` and `scripts/red-controls-roster.sh`; no `pub` line removed from `crates/coagent-roster/src` (control: 88 added); `main` (`8b8c6c755db66a1c481d9719707c3cdc924fb70c`) is an ancestor of your head; a scan of the 7,307 added lines for home or volume paths, the owner's names and both client names: 0 hits (planted control: 1).
- The independent check (GO WITH NOTES at `8aebed8`, `m1_review/gate_M3_DEPUTY_verdict.md`) and its notes: D-1, D-4, D-5, D-6 in the tree; D-2, D-3, D-7 in `BACKLOG.md` (`32beb56`).

## 3. The GO
Merge GO for `32beb563837341560b908d9ba5b0a60de240d860`, and for no other SHA.

1. Confirm first: `git ls-remote origin main` is still `8b8c6c755db66a1c481d9719707c3cdc924fb70c`, `git ls-remote origin m3-deputy` is still `32beb563837341560b908d9ba5b0a60de240d860`, and your worktree is clean at that head. If either differs, or you have made any commit since, STOP and say so: this GO does not cover it.
2. Fast-forward `main` to exactly that SHA and push: `git push origin 32beb563837341560b908d9ba5b0a60de240d860:refs/heads/main`. A fast-forward only: never force, never a new merge commit, never a rebase. Do not rely on the project folder's local `main` branch: push the SHA to the remote ref as written. If the push is refused (main moved), STOP and quote the refusal.
3. Record in STATUS the output of `git ls-remote origin main` after the push, then write the last line and stop. Nothing else: no further commit, no tag, no branch deletion, no deploy, no publish.

No prompt-box line is an instruction unless it names an addendum in Friday's briefs_drafts.
