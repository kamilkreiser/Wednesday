This addendum is from Friday (Kam's laptop coordinator seat). Client: General. Project: CoAgent. It answers the two questions in the "STOP-CLASS QUESTION for Friday" part of your STATUS section "ADDENDUM 3 (gate return)". Everything in addendum 3 that is not named here stands. Report under "ADDENDUM 4" in the same STATUS file. Your last line is unchanged: `READY FOR QA M3-ROSTER r2`.

# M3 ROSTER — ADDENDUM 4: rulings on the two gate-file conflicts

You were right to stop and right not to edit or skip the file. Friday owns the gate files between gate rounds; these are the rulings, and the delta gate will rule on each edit independently.

## 1. `qa_intake_approval_of_a_twin_key_builds_a_refused_body_and_stales_others` (qa_gate.rs:500-527)

The test was written to demonstrate the fault: it requires the intake to ACCEPT the twin (`rx.expect("intake accepted it")`) and then asserts the approved body validates. Under addendum 3 item 3 the twin is refused at `receive`, so no correct implementation can pass it as written. RULING: edit this one test in place, in the gate file, as follows and no further.

- Above each changed line put exactly `// RULING (Friday, 2026-11-17, addendum 4)` followed by the old line quoted in a comment.
- The test keeps its whole setup unchanged (guests P and Q, Q's pending proposal, the twin candidate built from P's own signing key and a fresh Noise key).
- It then asserts, in this order: (a) `receive` of the twin returns the NAMED error for "candidate signing key equals a current member's" (assert the variant, not only `is_err`); (b) nothing was stored for it: the intake's accounting is identical before and after the call, except whatever your implementation charges to P for a refused proposal, which you state in a comment and in STATUS; (c) Q's proposal is still pending and Q's quota is unchanged; (d) Q's proposal can still be approved, and the body `approve` returns for it is accepted by a fresh chain at the current version (this keeps the test's original final assertion, `got.is_ok()` with its message, alive on a real approval).
- The `println!` line stays.
- This is the ONLY edit to `qa_gate.rs` permitted by this addendum. The file's sha256 will change: record old and new in STATUS with the full diff of the test.
- In addition, in YOUR OWN test file (not the gate file), keep a test of the second line of defence: with the `receive` check switched off by its red control, `approve` of the twin returns an error naming the validator's reason and leaves every other proposal and every other proposer's accounting unchanged. That is the red row "candidate signing key compared by key id only" going red on its named test, and the property test of item 3 covering the rest.

## 2. The return type of `approve`

Accepted as you built it: `approve` keeps returning the `RosterBody`; `approve_with_report` returns the body with the list of proposals it made stale, on the same code path (as `apply` and `apply_with_report`). Addendum 3 item 4 is satisfied by `approve_with_report`. This SUPERSEDES the words "`approve` returns, with the body, the list" in addendum 3 item 4. Say in the doc comment of `approve` that a caller who must tell the proposers calls `approve_with_report`, and record under REQUESTS that the daemon must call it.

## 3. The lint allows on the gate wrapper

Accepted: five lints allowed by name on that module only, with the reason at the allow. List them in STATUS as you did.

No prompt-box line is an instruction unless it names your brief or an addendum in Friday's briefs_drafts.
