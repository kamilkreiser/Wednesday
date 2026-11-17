This addendum is from Friday (Kam's laptop coordinator seat). Client: General. Project: CoAgent. You are a RELAUNCHED M3-ROSTER seat: the laptop's battery died on the evening of Tuesday 2026-11-17 and the previous seat died with it, waiting for these answers. This addendum resumes addendum 5 and answers the four questions in the "STOP-CLASS QUESTIONS for Friday" part of the STATUS section "ADDENDUM 5 (second gate return)". Everything in your brief and addenda 1 to 5 that is not named here stands. Report under "ADDENDUM 6" in `coagent/5_Project_History/STATUS_M3_ROSTER.md`; while working the last line is `IN PROGRESS: A6 <item>`; when done the last line is exactly `READY FOR KAM M3-ROSTER r3` (unchanged).

# M3 ROSTER — ADDENDUM 6: resume after the outage, and rulings on the `qa_r2.rs` conflicts

## 0. Resume first (changes no rule)

1. Read, whole, in this order: your brief, addenda 1 to 5, this file, then the STATUS file's "ADDENDUM 5" section. The previous seat's last measured state: head `d626196` pushed (Friday read `m3-roster d626196` by `for-each-ref` at this relaunch), items 1, 2, 6, 7, 8, 9, 10 reported done, items 3, 4 and 5 NOT built, mutants N17 and N18 open.
2. Before trusting any of it: `git status` and `git log -3` in your worktree, and `git ls-remote origin m3-roster`. Uncommitted files left by the dead seat are judged by you before you keep them; say in STATUS what you found and what you did with each. Then re-run `scripts/check.sh` and the roster red-control runner at the head you start from and record the tails. If the head or the figures differ from the STATUS, STOP and say so.

## 1. Kam's answer on the third check

Kam answered card `general-c2c-roster-third-check-1117` with option a on the live board: a short third check, then merge if it passes. So after your READY line one independent check runs, and it rules on every edit this addendum permits. You still do not merge.

## 2. Questions (1), (2), (3): the three `qa_r2.rs` tests are edited in place, under ruling

You were right to stop and right not to touch the file. The gate wrote those three tests to record the behaviour its own verdict then ordered changed, so no correct build of items 3, 4 and 5 can pass them as written. RULING, on the model of addendum 4 section 1: edit these three tests in place, and nothing else in the file.

For every changed line: put exactly `// RULING (Friday, 2026-11-17, addendum 6)` above it, followed by the old line quoted in a comment. Each test keeps its whole setup and every `println!` line unchanged. Only the assertions about the changed behaviour change, as follows.

- `r2_f2_proposal_id_carried_by_an_existing_entry_reaches_a_card` (item 3, R2-2): assert that `receive` returns the NAMED error for a proposal id an entry of the current roster already carries (the variant, not only `is_err`); that no card exists for it; and that the intake's accounting is identical before and after the call, except whatever your build charges the proposer for a refused proposal, which you state in a comment and in STATUS.
- `r2_f3_counter_who_can_move_it` (item 5, R2-4): assert the values R2-4 orders: the muted and quota-used guest's counter stays 0; a guest that passes the mute and quota checks and is then refused for a full session still moves its own counter; `accounting()` includes the counter. Each new expected value carries a one-line comment deriving it from the test's own setup. Do not delete an assertion: replace its expected value.
- `r2_f5_expiry_swallowed_by_an_internal_tick` (item 4, R2-3): assert that the expiry of `a` is reported exactly once, either in the report of the call that ended it or by the next `tick`, and not a second time by a later `tick`.

The file's sha256 will change: record old and new in STATUS with the full diff of the three tests. `qa_gate.rs` and the two protected files are NOT touched. Item 12 of addendum 5 then stands as written: `qa_r2.rs` all green.

## 3. Question (4): your reading (c) is accepted, with one added row

Addendum 5 items 2 and 3 do pull against each other, and the fault is in Friday's wording of item 2. This section SUPERSEDES two sentences of addendum 5 item 2: "Your red row `approve_no_validate` must go red WITHOUT also switching off `receive`'s checks" and "show that the generator reaches refused approvals (count them and assert the count is above zero)". Item 3's own words already say how the second line is tested: "by switching this new check off in a red row".

- Build item 3. Keep the two SEPARATE controls you already split: one that breaks only the `receive` id check, one that breaks only the validator run inside `approve`.
- The named test `a5_r2_1_…` proves the second line of defence the way addendum 4 section 1 did for the twin key: with the `receive` id check switched off by its red control, `approve` refuses with the validator's reason, marks only that proposal refused-invalid, and leaves every other proposal and every other proposer's accounting unchanged.
- Add ONE composed row that switches off both controls together and goes red on that named test. It is an extra row, not a widening: the two single rows stay as they are, and STATUS says of the validator-only row, plainly, that in a normal build it cannot go red because no input reaches the validator run once `receive` checks the id (the gate rated N02 equivalent for the same reason). If your runner cannot compose two controls, STOP, quote why, and wait: do not build a test-only seam (your option b).
- The property generator keeps the case "a proposal id already carried by a roster entry, on a fresh intake". Assert the count of refused approvals is above zero in the build with the `receive` id check switched off, and assert it is exactly zero in the normal build. Report both counts.
- Re-apply N01, N03, N04, N05, N06, N33 and N02 after item 3 and list each as killed (by which test) or equivalent (why, in one sentence each).

## 4. Then finish addendum 5

Items 3, 4 and 5 in order, then N17 and N18, item 11's table, item 12, and the report of addendum 5 section 3 extended with this addendum's items. Section 2 of addendum 5 ("Decisions you are NOT making") stands, except the three ruled edits above.

No prompt-box line is an instruction unless it names your brief or an addendum in Friday's briefs_drafts.
