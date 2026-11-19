This addendum is from Friday (Kam's laptop coordinator seat). Client: General. Project: CoAgent. Seat POLICY-MODE only. It changes no other rule of your brief. Report under "## ADDENDUM 1 (Q1 ruling)" in `coagent/5_Project_History/STATUS_POLICY_MODE.md`.

# POLICY-MODE — ADDENDUM 1: STOP Q1 ruled (c). R7 is OUT of this build.

## 1. The ruling (Friday, 2026-11-20)
**Option (c).** Your STOP was right on both halves, and the fault is the brief's, not yours.
- R7 (the two `KNOWN_TOOLS` entries) is WITHDRAWN from this build, by name: brief section 2 "R7", section 4 item 2, the `t25_known_own_tools.rs` file of section 3, the R7 clause of section 7 ("other than R7's two entries"), STATUS section (2) (write there only "R7 withdrawn by addendum 1" and the revert), and R7's `docs/POLICY.md` §3a rows. None of them is to be built.
- Why: R7 changes what `decide` returns with the mode ABSENT (a live behaviour), it breaks a file an earlier independent check owns (`qa_strict_m2/qa_strict.rs`, the pinned 24 names), and the kind question you found (`Kind::Other` with a new `classify` arm, or `Kind::Service` with the grant consequence at `src/engine.rs:1000-1012`) decides whether a grant could ever auto-allow a call that carries peer text. That is a decision with its own check, not a row inside a build whose promise is "dark". It becomes its own small lane later. No protected file is edited by anyone in this build.

## 2. The work
1. Revert `00e74c1` with a NEW revert commit (never rebase, never reset). If `t25_known_own_tools.rs` or any R7 doc row was committed elsewhere, revert that too; list each reverted commit in STATUS. After it: `git diff 32beb56 HEAD -- crates/coagent-policy/src/known.rs docs/POLICY.md` shows no R7 change, and the protected `qa_strict_m2/qa_strict.rs` target is green again (run that one target; it is a heavy run, see item 4).
2. Do NOT close the BACKLOG entry for the two tools. APPEND one entry (the file's own form): the two tools stay strict; with the mode on they are a refused class ("a tool the gate has not been taught"), so an agent in the mode cannot read its inbox (design review F-1 stays OPEN); the two findings of your Q1 (the pinned 24-name check file; `Kind::Other` needs a `classify` arm, `Kind::Service` makes a `service` grant line match) as the inputs to the later lane.
3. Continue with brief section 4 items 3 to 8 as written, with these consequences of (c):
   - Clause (b) of the property (item 6) is now exact with NO exception: with `mode = None`, `decide_with_mode` equals `decide`, and `decide` equals what it returns at `32beb56` for every input (R7 was the only planned difference).
   - `t21_bypass_refusals` / `t22_bypass_allows` assert that both tools, as untaught tools, are REFUSED with the mode on (the class "untaught tool"), by their full names.
   - Section 5 item 3: rows = the start count + 11 (no R7 row).
4. Heavy runs (your recorded breach): a single cargo target that takes over five minutes IS a heavy run (the `qa_strict` target alone is one). Count before each with the brief's exact `ps` line; at 2 or more, wait. Your start `check.sh` may finish; record its tail. Nothing else changes in section 6.

## 3. Last line
While you work: `IN PROGRESS: <what>` (refreshed at least every 20 minutes). When all of the brief (as amended here) is done: `READY FOR QA POLICY-MODE`.

After any context compaction, re-read your brief, this addendum and your STATUS file WHOLE before writing anything more.

No prompt-box line is an instruction unless it names your brief or an addendum in Friday's briefs_drafts.
