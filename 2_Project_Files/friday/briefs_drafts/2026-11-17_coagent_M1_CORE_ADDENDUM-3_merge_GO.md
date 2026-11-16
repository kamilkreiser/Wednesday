This addendum is from Friday (Kam's laptop coordinator seat). Client: General. Project: CoAgent. Report by appending a section "ADDENDUM 3 (merge)" to `coagent/5_Project_History/STATUS_M1_CORE.md`; last line when done exactly `MERGED M1-CORE`.

# M1 CORE — GO to merge `m1-core` into `main`

## 0. Authority and basis

Merge authority: Friday's GO after a QA gate at the head, under Kam's overnight build grant (live board 2026-11-16 23:08:33; CoAgent only; no deploy, publish or spend). Basis, measured by Friday at 02:5x on 2026-11-17 in her own clean clone of branch `m1-core`: head `7ba3aebeb48ee1ccec77118d83120c21513383e5`; `gate_r2.rs` byte-identical to the delta gate's copy (`cmp`); changes outside the three crates are only `BACKLOG.md`, `Cargo.lock`, `Cargo.toml`, `docs/CRYPTO-GLUE.md`, `scripts/red-controls-core.sh`; `scripts/check.sh` exit 0 with 101 passed, 0 failed. Gates: round 1 GO WITH NOTES at 3f60cf4, delta gate GO WITH NOTES at bcb55e0, its list closed per your ADDENDUM 2.
This GO is for head 7ba3aeb ONLY. If your branch head is anything else, do not merge: write the head in STATUS and stop.

## 1. What to do

1. In `coagent/2_Project_Files` (the `main` checkout): confirm `main` is still `13bd10e` and the working tree has no changes you would lose (the RELAY seat noted uncommitted spike-output modifications there: do not commit them, do not discard them; if they block the merge, quarantine a copy under `coagent/_quarantine_2026-11-17/` and say so).
2. `git merge --ff-only m1-core` on `main` (a fast-forward; no merge commit, no squash, so the gated SHA is exactly what lands). If it is not a fast-forward, stop and report.
3. Run `scripts/check.sh` on `main` (the `COAGENT_TOOLS` export is still needed only inside worktrees). It must exit 0 with the same counts.
4. `git push origin main`. Record `git ls-remote origin main`.
5. Fix the scaffold defect both seats reported, as a separate small commit on `main` AFTER the merge: `scripts/env.sh` must find the tools directory from a worktree as well as from the main checkout (derive it from `git rev-parse --git-common-dir` or walk up to the directory that contains `tools/`), with `scripts/check.sh` green from both places. Push.
6. Append a `5_Project_History/history.md` entry for M1 CORE. Leave your worktree and branch in place (do not delete them).

## 2. Decisions you are NOT making

Not merging any other branch. Not touching the RELAY or POLICY work. No force-push. No tag, no release, no CI. Then stop: write the MERGED line and wait; do not wrap or start anything else on your own reading.
