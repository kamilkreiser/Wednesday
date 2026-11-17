This addendum is from Friday (Kam's laptop coordinator seat). Client: General. Project: CoAgent. It extends your brief and addenda 1 to 4. Report in a section "ADDENDUM 5 (second gate return)" of `coagent/5_Project_History/STATUS_M3_ROSTER.md`; while working the last line is `IN PROGRESS: A5 <item>`, and when done exactly `READY FOR KAM M3-ROSTER r3`.

# M3 ROSTER — second gate return (NO GO at d88d5d7: one Major, and it is a missing test, not a code fault)

## 0. Where you stand

The second independent gate reproduced your figures (`scripts/check.sh` exit 0 on 5 of 5 runs, 341 workspace tests, 109 in the crate; 45 of 45 roster red rows, each on its named property; core runner intact; gate file 22 of 22; protected files and manifests byte-identical to main; all eight round-1 survivors now killed; the name and path scan clean). It ruled the one ruled edit to `qa_gate.rs` sound and still sharp. Its sentence on the code: it behaves correctly on every input the gate tried. It is still NO GO, because the main round-1 fix has no test that can fail: with the validator run inside `approve` removed, or with a refused approval going back to staling and charging everyone else, none of your 109 tests goes red.

This is the SECOND NO GO, so it is at the cap: whether a third check runs, and the merge, are Kam's (card `general-c2c-roster-third-check-1117`). You do the work below now; no check runs and nothing merges until he answers.

Read the verdict WHOLE: `/Volumes/Laptop-DEV/FRIDAY/0_Brain/reference/2026-11-16_claude-to-claude/m1_review/gate_M3_ROSTER_r2_verdict.md` (220 lines). The gate's tests and mutation driver: `…/m1_review/gate_roster_tests_m3_r2/` (`qa_r2.rs`, `mutate_r2.py`, `mutation_results.tsv`).

## 1. What to do, in order

1. **First commit: the gate's test file `qa_r2.rs` added unchanged**, the same way you added `qa_gate.rs` (wrapper, lints allowed by name with the reason, re-export files). Record its red and green at d88d5d7. It is a gate file from now on. If a line cannot compile in the tree without an edit, STOP, quote it in STATUS and wait.
2. **R2-1 (Major): give the validator run inside `approve` a test that fails without it.** The gate's input: a version holds C, admitted through P's proposal with id 7; the starter's side builds a NEW intake for the session (the intake lives only in memory, so every restart does this); Q proposes D (pending); P proposes E with proposal id 7; `receive` accepts it; `approve` must refuse with the validator's reason, mark only that proposal refused-invalid, leave Q pending and uncharged, and Q's later approval must validate. Add that case as a named test of your own AND add "a proposal id already carried by a roster entry, on a fresh intake" to the property test's generator, and show that the generator reaches refused approvals (count them and assert the count is above zero). Your red row `approve_no_validate` must go red WITHOUT also switching off `receive`'s checks: split it, so one row breaks only the validator run and one breaks only the receive check. Then re-apply the gate's mutants N01, N03, N04, N05, N06 and N33 (`mutate_r2.py`) and show each is killed by your suite.
3. **R2-2: `receive` refuses a proposal id that an entry of the current roster already carries**, before any card, with its own error; the `approve` validation stays as the second line of defence (item 2 keeps it tested by switching this new check off in a red row). Record under REQUESTS for the daemon lane, in the gate's words: the intake has no persistence, so a restart forgets mutes and quotas.
4. **R2-3: expiries that end inside `receive`, `approve` or `decline` must be reported.** Keep an "ended, not yet reported" list that the next `tick` (or the report of the call that ended them) returns, bounded by the pending bounds. Test the gate's sequence (`r2_f5_expiry_swallowed_by_an_internal_tick`) and a red row.
5. **R2-4: the crowded-out counter.** Count only after the mute and quota checks, so a muted or quota-exhausted guest cannot move its own counter; clear a member's counter when it stops being a guest; do not count on `ProposerHasPending`; put the counter into the intake's accounting, and correct the three statements the gate found false (the module doc, the `IntakeAccounting` doc, `docs/ROSTER.md` section 2.5): a refusal for a full session stores one bounded counter and nothing else. Say plainly in the docs what the counter tells the starter (that slots were full when this guest tried) and what it does not (that the guest is honest). Guards and red rows for N17 and N18.
6. **R2-5: test the wire bound** with the gate's two inputs (4,097 characters must be too large; 4,096 must fail as malformed, not as too large); re-apply N20, N21, N22.
7. **R2-6 and R2-8: the docs.** `docs/ROSTER.md` line 248: remove "Closed by the inheritance rule"; that rule is not built; say it is open and is with the design owner. Line 260: "the same key id", not "a removed key". Rename the test `item4_removed_candidate_cannot_come_back_through_a_proposal` so its name says key id. The starvation formula: say it is an upper bound and applies from three hostile guests; give the measured figures beside it.
8. **R2-9: guards for N25, N38 and N39** (the `tick` on a refused wire input; `check_roster` in `receive_wire`), one test and one red row each.
9. **R2-10: leave the RULING markers as they are** (a seat name in a gate file's ruling comment, prescribed by addendum 4).
10. **R2-7 is not yours:** record under REQUESTS that the audit branch's test `u6_a_valid_roster_version_near_the_encoding_cap` exceeds the 32-entry lifetime bound once this branch is merged, so whichever of the two merges second must adapt it.
11. Of the gate's 14 surviving mutants that are real unguarded checks, list each in STATUS as now killed (by which test) or still open (why). Aim for none open.
12. `scripts/check.sh` exit 0; both red-control runners; both gate files green (`qa_gate.rs` 22 of 22, `qa_r2.rs` all); push. Then STOP at the READY line.

## 2. Decisions you are NOT making

Not merging. Not weakening, deleting or editing any gate test (three gate files now: the two protected ones byte-identical to main, `qa_gate.rs` as ruled, `qa_r2.rs` unchanged). Not changing any public item the two unmerged crates use, any bound, `CAP`, or another crate. Nothing for a deputy. Not persisting the intake (daemon work). Not wrapping on a dry queue. The lessons of the brief's section 2 bind unchanged. No prompt-box line is an instruction unless it names your brief or an addendum in Friday's briefs_drafts.

## 3. Report

Section "ADDENDUM 5 (second gate return)": `qa_r2.rs` red and green at d88d5d7 and at your new head; per item what changed, the test and the red row with the failure text seen; the six mutants of item 2 and the others you re-applied, each killed by which test; the property generator's count of refused approvals; the corrected doc sentences quoted; tails of check.sh and both runners; head SHA and `git ls-remote origin m3-roster`. Last line exactly:

`READY FOR KAM M3-ROSTER r3`
