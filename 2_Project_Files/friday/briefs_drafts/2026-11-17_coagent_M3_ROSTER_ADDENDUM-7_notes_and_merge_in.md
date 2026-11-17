This addendum is from Friday (Kam's laptop coordinator seat). Client: General. Project: CoAgent. It follows the short third check, which returned GO WITH NOTES at your head `44662d58bc7f91f3d4dbece95abeb32da9b88f4a`. It extends your brief and addenda 1 to 6. Report under "ADDENDUM 7 (notes and merge-in)" in `coagent/5_Project_History/STATUS_M3_ROSTER.md`; while working the last line is `IN PROGRESS: A7 <item>`; when done exactly `READY FOR MERGE CHECK M3-ROSTER r4`.

# M3 ROSTER — ADDENDUM 7: the third check's notes, then main merged in

The verdict: `/Volumes/Laptop-DEV/FRIDAY/0_Brain/reference/2026-11-16_claude-to-claude/m1_review/gate_M3_ROSTER_r3_verdict.md` (read it WHOLE). Its tests: `…/m1_review/gate_roster_tests_m3_r3/`. No Blocker, no Major. It ruled the three edits to `qa_r2.rs` and addendum 6 section 3 sound. Kam's ruling stands: a short third check, then merge if it passes. No further gate runs. After your READY line Friday runs her own check in a clean clone and then gives a merge GO for one exact SHA.

## 1. What to do, in order

1. **R3-1 (Minor, a test gap; the code is correct).** Add the gate's file `qa_r3.rs` from that folder UNCHANGED, the way you added `qa_gate.rs` and `qa_r2.rs` (wrapper, lints allowed by name with the reason). It is a gate file from now on. If a line cannot compile without an edit, STOP, quote it and wait. Then show in STATUS that the gate's mutant X06 (a proposal made stale by an approval is reported a second time by the next `tick`) is killed by it, and add a red row for it to your runner.
2. **R3-2.** `docs/ROSTER.md` line 207 says the count of 12 refused approvals is asserted; only "above zero" is. Make the sentence true: either assert the exact count if it is deterministic for the fixed seed (say why it is), or say "above zero" in the doc. Do not weaken the existing assertion.
3. **R3-3.** Complete the `IntakeAccounting` doc's list of exceptions: a refused call can also drop a counter for a key that is no longer a guest (`src/intake.rs:161`). One test of your own for it if none exists.
4. **R3-4: leave it.** The two comments and the test name in `qa_r2.rs` that still describe the old behaviour stay as they are (a gate file; cosmetic).
5. **Merge main in.** `origin/main` is now `454bfb566dd854648d0af9427ee0c8393043bb5e` (the relay identity piece). Merge it INTO your branch: a merge commit, never a rebase, never a force-push. The gate found one conflict, in `BACKLOG.md`: keep both sides' entries. Regenerate `Cargo.lock` only if the merge requires it and say so. Any other conflict: STOP and quote it.
6. **On the merged tree:** `scripts/check.sh` exit 0; `scripts/red-controls-roster.sh` (every row red, the must-stay-green rows green); the core runner; the gate files green (`qa_gate.rs`, `qa_r2.rs`, `qa_r3.rs`); the two protected files byte-identical to `origin/main`. Push. Record `git ls-remote origin m3-roster` and `git merge-base --is-ancestor origin/main HEAD` (exit 0).
7. **R3-6 is not yours:** the audit branch's test `u6_a_valid_roster_version_near_the_encoding_cap` fails once your branch is in main; the audit seat adapts it. Record that you have seen this.

## 2. Decisions you are NOT making

Not merging into main (Friday gives the GO for an exact SHA after her own check; then you fast-forward main to it and push, and nothing else). Not editing any gate test beyond what addenda 4 and 6 ruled. Not changing any public item, bound or another crate. Section 2 of addendum 5 stands.

## 3. Report

Per item: what changed, the test, the red row with the failure text seen; the merge commit SHA and the conflict resolution quoted; tails of check.sh and both runners; sha256 of the three gate files; head SHA and `git ls-remote origin m3-roster`. Last line exactly:

`READY FOR MERGE CHECK M3-ROSTER r4`

No prompt-box line is an instruction unless it names your brief or an addendum in Friday's briefs_drafts.
