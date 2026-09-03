# QA Agent Invocation Brief — Secuura/Blockchain, #799's MAJORS LANDING, STATIC THROUGH-CODE

## Charter (read first, in full)
`/Volumes/DevMASTER/WEDNESDAY/2_Project_Files/fleet/qa-agent/QA_AGENT_CHARTER.md`

## 1. Target
- **Client / Project:** `Secuura / Blockchain (Platform K)`
- **Running target:** **NONE — STATIC pass, read by SHA.** Do not start, stop or rebuild the stack;
  do not run compose; do not contact the demo/UAT VM.
- **Environment:** none contacted. **Zero writes to the Secuura tree.** Expect `git status` to show
  two untracked `(conflict_on_2026-07-03)` snapshots on arrival — **they pre-date this session by
  two months; report the tree as UNCHANGED BY YOU rather than as clean.**
- **Production?:** nothing is deployed and no finding of yours triggers a deploy.
- **Source tree (read-only):** `/Volumes/DevMASTER/!CODING/Secuura/Blockchain/2_Project_Files`

## 2. Subject and the claims to falsify
**PR #799, the landing that closes Peter's Majors 1 and 2, at `b36757f7a`** (previous head
`4cb07b79f`), against develop `492152a81`. **Derive the changed-file set yourself from the range
`4cb07b79f..b36757f7a`** rather than from any list in this brief — if the set differs from
"two new test files, no production code", that difference is itself a finding.

**Every claim below is the BUILDER's (Secuura agent s121). Falsify them.**

- **"15 cases across two new files, NO PRODUCTION CODE TOUCHED."** The second half is the
  load-bearing one: a landing that closes a reviewer's Majors with tests only is claiming the
  product was already correct. **Check the range, not the sentence.**
- **Counts:** security **124/124 across 11 files** (Peter's 118/118 plus 6); originate
  **470/472 across 44 suites** (his 461/463 plus 9); **`tsc --noEmit` rc 0 on both**; preflight 8/8.
  **The 2 failures are claimed to be the pre-existing KS-650 pair in an untouched file** — verify
  that attribution rather than accepting it; a failure blamed on a neighbour is a claim.
- **The mock surface, which is the part the builder itself called the keeper:** `requireRole` comes
  through `jest.requireActual` so the role gate is the product's own; **only `authenticate()` is
  stubbed**; the principal is set under **BOTH** `_secuuraUser` and `user` *"exactly as the real
  `setUser` does"*. **Read the real setter and confirm the equivalence** — the builder's own
  sentence is *"a stub setting one silently disables half the chain."*
- **The load-bearing control asserts `decideKeyRevoke` is NOT a jest mock** — because mocking
  `@secuura/shared` wholesale would have replaced the SUBJECT with a stub and left a green suite
  testing nothing. **Prove that control CAN fail**: would it actually redden if the subject were
  mocked? A control that cannot fail is the thing this fleet has bled on all week.
- **The red-proof discipline claimed for the landing:** the hoisted-`UPDATE` proof reddened
  **CASE 2 and CASE 4 on `not.toHaveBeenCalled()` while their 403 status still PASSED**, and the
  allow-path cases failed `toHaveBeenCalledTimes(1)` receiving **2**. **Confirm the assertions in
  the committed file still have those properties** — an ordering assertion that an end-state
  assertion sails through is exactly the value being claimed, and it is checkable statically.

## 3. Scope — and the standing hypothesis
**Charter:** judge whether Peter's two Majors are genuinely closed, and hunt the CLASS rather than
the instances. **The standing hypothesis, which has paid every time it was used on this project:
assume one more instance exists.**

**The three questions that matter most, in order:**
1. **DOES EACH OF THE 15 CASES ENTER THE BRANCH ITS NAME CLAIMS?** A test's NAME is not its
   coverage. Read what each fixture makes REACHABLE — a stub returning `null` for a discriminator
   routes every case in the file elsewhere and the suite still goes green. This exact class let an
   auth bypass survive a suite that appeared to test it (s119, 2026-09-03).
2. **GREEN BASELINE, THEN THE COUNT.** For any assertion you judge: would it pass on unmodified
   known-good code (a red there is a defect in the assertion), and on a tamper does the **number of
   cases EXECUTED** match the baseline? **`1 failed / 0 tests` is a build failure wearing a
   red-proof's clothes** — this is the builder's own catch from tonight, and the reason it is in
   this brief is that it is now the fleet's rule: **check the test COUNT, not the verdict, and
   confirm the SPECIFIC cases that reddened are the ones the tamper should hit.**
3. **IS THERE A THIRD SURFACE?** The F-764-01 shape on this very repo was **a second revoke surface
   that never calls `decideKeyRevoke`**. Ask what else resolves the same relationship and whether
   this landing's cases reach it. If the answer is "nothing else", say how you established it and
   against which corpus — an absence claim carries the corpus it was measured against.

**Do NOT re-report, but DO check:** findings **6(b)** and **6(c)** on #799 are **deliberately
unfixed and named on the PR**, because touching the head would have voided the review request just
issued. That was the right call. **Confirm they are in fact named on the PR** and say plainly if
either is **worse than the PR describes it** — a deferral is a claim too.

**Explicitly OUT of scope:** the status document (`8919a9007` on `docs/open-pr-status-2026-09-04`)
and its counts. Its figures are a **snapshot with a settle point**, and re-measuring them now would
measure a different board and generate false findings. Also out: the running stack, any container,
any PR state change or comment, and any file in the Secuura tree.

## 4. Credentials
**None, and none needed.** **Never read a real `.env`.**

## 5. State-mutation & cleanup
**Exclude-and-report-only.** Scratch in YOUR scratchpad; nothing copied back. If you run any suite,
run it from a copy by SHA in your own scratchpad, never in the Secuura tree.

## 6. Output boundary (fixed)
**Findings, reports and recommendations ONLY.** No code, tests, fixtures, tickets, config or PR
comments. Fix-shapes and regression tests in prose.

## 7. Known-fragile / known-changed — do NOT re-report as new
- **The two `(conflict_on_2026-07-03)` snapshots** — two months old, not this session's.
- **2 of 27 auth test files fail at import** (`Missing "./utils/logger" specifier`) — proven
  pre-existing, filed in BACKLOG.md deliberately so an unrelated shared-package fix would not widen
  an auth-bypass PR's review.
- **The KS-650 pair** in an untouched originate file — claimed pre-existing; verify, do not re-file.
- KS-784 records an orphan Schemathesis failure on `POST /api/teams/webhook-config`, unrelated.

## 8. Logistics
- **Time-box:** one bounded pass. Depth over breadth — question 1 (fixture reachability) first if
  you cut.
- **Report to:** `projects/secuura-blockchain/reports/2026-09-04-799-majors-landing-through-code/SUMMARY.md`
  under your own tree, then mail Wednesday a summary. **Wednesday reads the FULL report, not the
  mail.**
- **Escalation:** `wednesday-agent@agentmail.to`, QUESTION subject. Approval-class pauses for Kam.
- **Your NOT-TESTED list is first-class output. State the counting UNIT and SETTLE POINT for any
  population figure.**
- **CONTEXT FOR YOUR SEVERITY CALLS, not a reason to soften them: #799 is in front of PETER right
  now, review requested at this exact head.** A finding here reaches a human reviewer's desk before
  he spends his time, which is worth more than a finding after. **Report what you find at the
  severity you find it** — the routing to Peter is Wednesday's problem, not yours, and you make no
  contact with him.

PROVENANCE:
- Head `b36757f7a`, previous head `4cb07b79f`, develop `492152a81`, the 15 cases / two files / no-production-code claim, the four count claims, the review re-request at head, and findings 6(b)/6(c) deferred | s121's Session wrap mail, `wednesday-agent@agentmail.to`, 2026-09-03T16:57:55Z | read 2026-09-04
- The mock surface (requireActual `requireRole`, both principal properties), the NOT-a-mock control, and the hoisted-UPDATE red-proof's per-case behaviour | s121's STATUS mail, same inbox, 2026-09-03T16:52:58Z | read 2026-09-04
- The `1 failed / 0 tests` TS6133 catch and the count-not-verdict rule | s121's STATUS + wrap mails, same inbox | read 2026-09-04
- The F-764-01 second-revoke-surface class and the test-NAME-is-not-coverage class | /Volumes/DevMASTER/WEDNESDAY/0_Brain/learnings/2026-08-07_a-check-that-cannot-fail.md | read 2026-09-04
- The two pre-existing auth import failures and the tree's two-month-old snapshots | s120's STATUS mail, same inbox | read 2026-09-04

**NOT re-derived by Wednesday:** every SHA above is copied from s121's mail, a channel with an
author, and was NOT verified against the repository from Wednesday's seat. **Verify each as an
object on your own seat and say so if any does not resolve.**

SELF-CHECK: re-read end-to-end for contradictions | 2026-09-04 03:08
