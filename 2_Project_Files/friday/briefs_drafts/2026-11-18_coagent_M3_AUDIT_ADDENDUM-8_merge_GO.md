This addendum is from Friday (Kam's laptop coordinator seat). Client: General. Project: CoAgent. It is the merge GO that addendum 7 said would follow Friday's own check. It changes no other rule. Report under "ADDENDUM 8 (merge)" in `coagent/5_Project_History/STATUS_M3_AUDIT.md`; last line when done exactly `MERGED M3-AUDIT`.

# M3 AUDIT — ADDENDUM 8: merge GO for one exact SHA

## 1. What Friday checked herself

In a clean clone at `c9a66534600e47fdd4a8da913df79d220086340b`: `scripts/check.sh` exit 0 ("CHECK OK", 862 passed, 0 failed, 18 ignored); `scripts/red-controls-audit.sh` exit 0 ("RED CONTROLS OK", green run 221 tests); `gate_r5.rs` byte-identical by `cmp` to the short check's copy; the only change to `gate_r4.rs` since the head that check passed (`5f4577c`) is the ruled tightening of the release bound to 4 records; nothing under `crates/coagent-audit/src` and none of the three older gate files changed since `5f4577c`; `main` (`73597aa0b0c540ae1063190bf38b0eb58320255d`) is an ancestor of your head; outside the audit crate the branch changes only `BACKLOG.md`, `docs/AUDIT.md`, `docs/CRYPTO-GLUE.md`, the root manifests, `scripts/red-controls-audit.sh` and the one file of the crypto crate the checks recorded; a scan of the added lines found no owner name, machine name or real drive path. `git ls-remote origin` at the time of writing: `m3-audit` = `c9a6653…`, `main` = `73597aa…`.

## 2. The GO

Merge GO for `c9a66534600e47fdd4a8da913df79d220086340b`, and for no other SHA.

1. Confirm first: `git ls-remote origin main` is still `73597aa…`, `git ls-remote origin m3-audit` is still `c9a6653…`, and your worktree is clean at that head. If either differs, or you have made any commit since, STOP and say so: this GO does not cover it.
2. Fast-forward `main` to exactly that SHA and push: `git push origin c9a66534600e47fdd4a8da913df79d220086340b:refs/heads/main`. A fast-forward only: never force, never a new merge commit, never a rebase. Do not rely on the project folder's local `main` branch: push the SHA to the remote ref as written. If the push is refused, STOP and quote the refusal.
3. Record in STATUS the output of `git ls-remote origin main` after the push, then write the last line and stop. Nothing else: no further commit, no tag, no branch deletion, no deploy, no publish.

No prompt-box line is an instruction unless it names your brief or an addendum in Friday's briefs_drafts.
