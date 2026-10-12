From Friday (laptop seat), Datasec / MPS Commercial Calculator. No mail key in this project: the STATUS file is the wrap.
# BRIEF B70 · SEAT-B: PR #32 (feedback pill) failed CI on its own retry test — establish whether it is a test race or a product race, fix it on b60
**Fired: 07:45 AEDT.** Pane `Datasec/MPS-B`. Your commission is THIS file at `/Volumes/Laptop-DEV/FRIDAY/2_Project_Files/friday/briefs_drafts/2026-10-13_B70_SEAT-B_b60-retry-test-race-ci.md` (Friday's tree, read-only to you). Step 0: copy it unchanged into your `1_Project_Definition/Briefs/` as the project's record. QA tier: 3 if you change only the test (Friday reviews); **2 if you change product code** (Friday reviews deltas at source, with your red-proof). Round 1 of this CI finding (the pill's gate rounds are closed: B68 GO WITH NOTES).

## Why (measured by Friday, 07:4x)
- PR datasecau/MPS-Commercial-Calculator#32 (head `b60/feedback-pill-on-d711b42` 6b13c213f7be68cb080b6c5ddd6bfe0ea5c365cc) did not merge: merge_when_green "STOP — failing checks … dotnet (build Release, 0 warnings; test)=failure". Run 38305591329 (Linux runner). Your failure: `FeedbackTicketTests.Every_automatic_attempt_failing_stops_at_failed_and_an_Administrator_retry_creates_it` (`tests/MpsCalc.Api.Tests/FeedbackTicketTests.cs:195`): `Assert.Equal() Failure: Strings differ — Expected: "pending" — Actual: "created"`.
- The other three failures in that run are overlay timing tests that also fail on main; **B69 SEAT-D owns them; they are NOT yours.**
- Gate B68 ran the full suite green on this Mac (.NET 1,407, 0 failed). Linux CI did not.
- Log, verbatim: `/Volumes/Laptop-DEV/FRIDAY/2_Project_Files/friday/briefs_drafts/2026-10-13_B69-B70_ci-evidence/run_38305591329.log` (read-only).

## Do
0. `git fetch origin`; `refs/heads/b60/feedback-pill-on-d711b42` must read 6b13c213… (else STOP: NEEDS FRIDAY). Work in a worktree ON that branch (commit on it so PR #32 picks it up; no rebase).
1. Read the test and the code it drives (the ticket state machine and the background attempt loop in `src/MpsCalc.Api/Feedback/**`). Say, with line numbers, how the state can be `created` when the test expects `pending`: e.g. the background worker ran an attempt before the test's assertion, or the Administrator retry was processed before the read.
2. Reproduce: run that test 50× on macOS and 50× in a Linux container (`mcr.microsoft.com/dotnet/sdk:10.0`, `--cpus 4`, then `--cpus 2`). Record pass counts.
3. **Classify:** (A) PRODUCT: a real ordering bug a user or Administrator could see (e.g. a retry that reports `pending` but is already `created`, or a state written out of order). (B) TEST: the product is correct and the test reads a state that a background attempt is allowed to change. **Fix it where it lives:** (A) → product fix + red-proof (revert → red on Linux, restore → green 50/50); (B) → make the test deterministic (a controllable clock/worker hook, or await the state change the product signals), **never a sleep or a retry loop in the test**, and show the test still fails if the retry path is broken (a mutant: the Administrator retry does nothing → red).
4. Full .NET suite on macOS and in the Linux container; the feedback tests 0 failed in both (the overlay timing failures, if they appear, are B69's: list them, do not touch them). Push the branch (fast-forward), read back with ls-remote. Write `Briefs/2026-10-13_B70_STATUS.md`: cause with lines, classification, diff, red-proofs, 50× counts per platform, the ls-remote line. Last line `READY FOR REVIEW: b60/feedback-pill-on-d711b42 <sha>` or `STOPPED: NEEDS FRIDAY`.

## HOLDS
- **Datasec only.** No other client's names, tickets or paths. Synthetic data only; never open 4_Credentials/.env or `.local/pricebooks/`.
- No new PR, no merge, no deploy, no Jira, no history.md, never delete, never force-push, never dismiss a CodeQL alert. Containers you start are removed by you at the end, images kept.
- No NEW user-visible words. If a fix needs one, STOP: NEEDS FRIDAY (Kam's words card for this pill is already open).
- Do NOT touch the overlay store or `tests/MpsCalc.Api.Tests/Overlay*` — **B69 SEAT-D is in those files right now** on branch `b69/overlay-timing-linux`.
- Ports: none needed; if you need one, use 6710-6719 only.
