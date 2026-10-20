# B374 drafter report (Tuesday's drafter, Sonnet 5.5, 2026-10-21 06:0x AEDT)

Brief: `2026-10-21_B374_SEAT-R12_nexusai-rd780-regex-anchors.md` (125 lines). Stamp slots: `@MAIN_SHA@` x3, `@STAMP_TIME@` x1. No `.pre-stamp` copy was written (outside the two permitted paths); Tuesday makes it before stamping.

## Key findings (all MEASURED, 06:0x)
- main = `115a775b6d5808629f493ef7a3f602d8c5853a22` (ls-remote). Open PRs: #102 `records/b362` @ 6dcbedb9, #101 `rd-874-875-test-guards-uat-port-r11` @ 48a17df8, #67 @ 94b288cc. No branch for RD-780.
- RD-780: To Do, High, no links, 0 comments. Alerts #244 (`scripts/propose-dark-retheme.js:184`) and #245 (`:214`), rule `js/regex/missing-regexp-anchor`, both open on main at 115a775b, created 2026-09-28T19:01:08Z.
- The ticket's suggested fix `/^(background|.*-bg)$/` is NOT behaviour-preserving (it stops matching `background-color`). The brief specifies `/^(?:background.*|.*-bg)$/`; node check on the 140 property names of dark-mode.css plus 9 planted names: 10 matched, 0 differences.
- No test references the script (`git grep` at main: only docs/scripts). No test is needed or wanted; proof of equivalence is byte-identical script output before/after (builder measures). No counts change, so no clash with PR #101.
- PR #101 file list (6) matches your partition list; B374 touches none; the brief names them as untouchable.
- Lock: `nexusai-jest.lock/` existed at 05:51 (held, probably B362); brief treats it as WAIT.

## Questions (each with a recommended answer)
1. Does the "no new test file" decision stand? Recommend YES (behaviour-preserving, no existing coverage, avoids the counts file that #101 edits).
2. Require a full `npm run verify` for a one-line change to a script no test loads (about 28 min under the lock, queued behind B362)? Recommend YES for READY-shape parity; drop to `node --check` plus equivalence proof only if the lock queue is long.
3. Use the exact-equivalence regex `/^(?:background.*|.*-bg)$/` rather than the ticket's form? Recommend YES.
4. Is the pane name `Datasec/NexusAI-R12` free? B360 is also "SEAT-R12" (an MPS brief); I did not check its pane name. Recommend confirming no live pane of that name before launch.
5. Land via C-190 same-commit fast-forward after QA; should the PR carry only this one file, opened after #101 lands or independently? Recommend independently (disjoint files).

## Could not verify
- Whether any other open alert sits in this file under a different rule (the all-rules path-filter `gh api` call errored in my shell).
- PR #102's file list (not read); the three lock-tool sha256s (B355 values relayed, not re-hashed).
- Whether CodeQL closes #244/#245 on the new regex, or raises a new alert (e.g. ReDoS on `.*-bg`); only the PR-ref scan shows that.
- That the script runs deterministically at the pin (the builder's Step 2 measures it).
- The ticket's "high" versus GitHub's `warning` rule severity (both recorded, not reconciled).
- C-numbers and line numbers for CLARIFICATIONS.md are relayed from B355, not re-read.
- No worktree, clone, jest or script run was made.
