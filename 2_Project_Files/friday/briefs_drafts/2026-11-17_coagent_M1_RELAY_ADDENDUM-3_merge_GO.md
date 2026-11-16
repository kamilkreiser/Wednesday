This addendum is from Friday (Kam's laptop coordinator seat). Client: General. Project: CoAgent. Report by appending a section "ADDENDUM 3 (merge)" to `coagent/5_Project_History/STATUS_M1_RELAY.md`; last line when done exactly `MERGED M1-RELAY`.

# M1 RELAY — rulings on your open points, and GO to merge `m1-relay` into `main`

## 0. Rulings (Friday)

1. **The five ignored gate tests: accepted as you left them.** Three assert limits addendum 2 told you to document, not fix (G1-r2a, G1-r2b, G1-r2d); two test the eviction mechanism addendum 2 told you to remove. They stay in the tree, failing when run with `--ignored`, each with its reason naming the owner decision or the removed premise. Friday compared the four gate files with the gate's originals with layout removed: three have identical content length; `gate_r2_state.rs` differs by the declared attribute lines, the lint line and the comment.
2. **Reservation rule, rotation dropping the old holder's buffered frames, the directory lock:** accepted as implemented and as documented in PROTOCOL.md.

## 1. Authority and basis for the merge

Merge authority: Friday's GO after QA gates, under Kam's overnight build grant (live board 2026-11-16 23:08:33; CoAgent only; no deploy, publish or spend). Gates: round 1 NO GO at 65fcc1b, delta gate GO WITH NOTES at 519d6f0, its list closed per your ADDENDUM 2 at head `4be8dde5a8d7c41a24759d340a2c5031918d9360` (Friday read `git rev-parse HEAD` = that SHA in your worktree, working tree clean). `main` has moved since you branched: it is now `129914b` (M1 CORE merged, plus an `env.sh` fix). Friday runs her own full check on `main` AFTER your merge lands; if it fails, the merge is reverted by a new commit and returned to you.

## 2. What to do

1. In your worktree, on `m1-relay` at `4be8dde` (if the head is anything else, stop and report): `git merge origin/main` (after `git fetch origin`). A merge commit, not a rebase. Expected conflict: `Cargo.lock` only. Resolve it by taking `main`'s `Cargo.lock` and letting cargo re-add what your crates need (`cargo update -w` or a plain `cargo check --workspace`, without `--locked`, once), never by hand-editing. If anything other than `Cargo.lock` and `BACKLOG.md` conflicts, stop and report. For `BACKLOG.md` keep both sides' entries.
2. After the merge, confirm no dependency VERSION changed for any crate that was already in `main`'s lock (diff the two lock files and list every changed version in STATUS; a changed version of a crate the CORE crates use is a stop-and-report).
3. `scripts/check.sh` in the worktree (no `COAGENT_TOOLS` export needed now): exit 0, with the CORE tests and yours all passing; report the counts. Run your red-control runner once more on the merged tree.
4. Push `m1-relay`. Then in `coagent/2_Project_Files`: `git merge --ff-only m1-relay` on `main`, `scripts/check.sh` there, `git push origin main`. Record `git ls-remote origin main`.
5. The CORE seat's test for "the relay binary has no CORE dependency" is yours (`coagent-cli` tree check): it must still pass on `main`.
6. Append a `5_Project_History/history.md` entry for M1 RELAY. Leave your worktree and branch in place. Do not remove temporary directories you create: quarantine or leave them.

## 3. Decisions you are NOT making

Not merging any other branch into `main`. Not touching the CORE, POLICY or AUDIT work. No force-push, no rebase, no tag, no release, no CI. Then stop: write the MERGED line and wait.
