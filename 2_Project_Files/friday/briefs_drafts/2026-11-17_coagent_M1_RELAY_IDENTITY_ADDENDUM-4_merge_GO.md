This addendum is from Friday (Kam's laptop coordinator seat). Client: General. Project: CoAgent. It is the merge GO that addendum 2 said would follow Friday's own check. It changes no other rule. Report under "ADDENDUM 4 (merge)" in `coagent/5_Project_History/STATUS_M1_RELAY_IDENTITY.md`; last line when done exactly `MERGED M1-RELAY-IDENTITY`.

# M1 RELAY-IDENTITY — ADDENDUM 4: merge GO for one exact SHA

## 1. What Friday checked herself

In a clean clone at `454bfb566dd854648d0af9427ee0c8393043bb5e`: `scripts/check.sh` exit 0, 321 passed, 0 failed, 5 ignored; `gate_identity_fuzz.rs` and `gate_pin_client.rs` byte-identical by `cmp` to the gate's copies; the four mutants of addendum 2 item 4 (N20, N21, N24, N36) re-applied one at a time by an independent agent, each KILLED by the test you named for it. `git ls-remote origin` at the time of writing: `m1-relay-identity` = `454bfb5…`, `main` = `18005d63ae1311df9649893060caf1f98510a4c1`, and `main` is an ancestor of your head.

## 2. The GO

Merge GO for `454bfb566dd854648d0af9427ee0c8393043bb5e`, and for no other SHA.

1. Confirm first: `git ls-remote origin main` is still `18005d6…` and `git ls-remote origin m1-relay-identity` is still `454bfb5…`, and your worktree is clean at that head. If either differs, or you have made any commit since, STOP and say so: this GO does not cover it.
2. Fast-forward `main` to exactly that SHA and push: `git push origin 454bfb566dd854648d0af9427ee0c8393043bb5e:refs/heads/main`. A fast-forward only: never force, never a merge commit, never a rebase. If the push is refused, STOP and quote the refusal.
3. Record in STATUS the output of `git ls-remote origin main` after the push, then write the last line and stop. Nothing else: no further commit, no tag, no branch deletion, no deploy, no publish.

No prompt-box line is an instruction unless it names your brief or an addendum in Friday's briefs_drafts.
