# QA Agent Invocation Brief — Secuura/Blockchain, s119's batch, THROUGH-CODE

## Charter (read first, in full)
`/Volumes/DevMASTER/WEDNESDAY/2_Project_Files/fleet/qa-agent/QA_AGENT_CHARTER.md`

## 1. Target
- **Client / Project:** `Secuura / Blockchain (Platform K)`
- **Running target:** **NONE — this is a STATIC pass.** Nothing is executed against the Secuura
  tree; every object is read by SHA. Do not start, stop or rebuild the stack.
- **Environment identity:** not applicable — no environment is touched.
- **Production?:** no environment is contacted at all. **No writes of any kind**, including to the
  repo. `git status --porcelain` must be empty at end and you should say so.

## 2. Spec / DoD being tested against
Three heads, all open, all clean, all requested from Peter, **none merged**, against develop
`7dd304b7c`:

**(a) #799 `04e9ef23d` — TWO TEST FILES ONLY, a light pass over the delta.**
The delta `124e98192..04e9ef23d` is one commit, three files: `keyRevokePolicy.ts` plus two test
files. **`keyRevokePolicy.ts` changed by COMMENTS ONLY** — that was measured twice by the builder
(strip comments and blanks then diff: 53 code lines both sides, no difference; raw patch filtered
for non-comment changed lines: 0) **with a control on a file whose code DID move in the same commit
returning 64**, and reproduced independently by Wednesday (43 added → 0 non-comment non-blank;
10 removed → 0). **Your scope here is the two TEST files.** If you find that the comments-only
claim is false, say so loudly — but it has two independent measurements and a control behind it.

**(b) #800 `033cb15dc` — the false clean, the unwired script, the narrowed all-clear.**
Claims to challenge: `get_value` now strips trailing whitespace then a MATCHED pair of surrounding
quotes, so a quoted or trailing-spaced shared literal is caught; **whitespace INSIDE quotes is
deliberately left alone** because a shell preserves it, with a control asserting exactly that;
a new 8-case fixture suite, 4 of them controls, which **reads the shared literals out of the script
rather than retyping them**; red-proof 4 failed / 4 passed against a COPY carrying the pre-fix
`get_value`; `check-app-db-password-default.sh` (164 lines, previously invoked by nothing) wired
into both start scripts honouring `SECUURA_STRICT_CREDENTIAL_CHECK` and verified exiting 0 in
today's held state; the all-clear narrowed to name the two literals it checks and point at the
script owning the third.

**(c) #804 `d494ff2b7` — KS-737, the platform-admin MFA bypass. Treat this as the highest-value
subject in the batch.**
Claims to challenge: `mfaCode` was part of the guard, so omitting it skipped the block and reached
`createSession()` + `generateTokenPair({…, role: platformAdmin.role})`; **TWO legs, not one** —
(1) no code supplied, (2) `mfa_secret` NULL while `mfa_enabled` is true — and a fix closing only
the first leaves the second; the branch now has the identical shape to its regular-user sibling;
red-proof three legs red at `expected 200 not to be 200` with **status and token asserted
SEPARATELY**, four controls green, 7/7 after the fix.

- **Source tree (read-only):** `/Volumes/DevMASTER/!CODING/Secuura/Blockchain/2_Project_Files`

## 3. Scope
- **Charter:** read the three deltas against the claims their PRs and tickets make, and hunt the
  CLASS behind each — the builder's own framing for the night was **"an assertion that cannot reach
  its subject"**, found in three separate places. Assume there is a fourth.
- **In scope:** the diffs, the tests added or changed, the fixtures those tests stand on, and
  whether each new assertion can actually reach the code it names.
- **Out of scope / do NOT touch:** any running stack, any container, any database, the demo/UAT VM,
  the four PRs themselves (no comments, no reviews, no state changes), and any file in the repo.

## 4. Credentials
**None needed and none supplied** — nothing authenticates in a static pass. If you believe a claim
can only be settled by running something, say so as a coverage gap rather than reaching for it.

## 5. State-mutation & cleanup
**Exclude-and-report-only.** No state is mutated. If reading requires a scratch copy, make it in
your OWN scratch directory, never in the Secuura tree, and say where.

## 6. Output boundary (fixed)
**Findings, reports and recommendations ONLY.** No code, no tests, no fixtures, no tickets, no
config, no PR comments. Describe the fix-shape and the regression test the owner should add, in
prose. The project's own agent authors and commits everything.

## 7. Known-fragile / known-changed areas — and the three classes to hunt
**Do NOT report these as new; they are recorded and owned:**
- 2 of 27 auth test FILES fail at import (`Missing "./utils/logger" specifier in "@secuura/shared"`
  — a mocked subpath the exports map does not publish). **Proven pre-existing against develop** by
  the builder, on a copy restored byte-identical. Filed in BACKLOG.md deliberately, so an unrelated
  shared-package fix would not widen the review on an auth-bypass PR.
- KS-780 records that two organisation-id normalisers exist in two layers; `@secuura/shared` cannot
  import from a service, so #799 could not have reused originate's. Named, not a finding.
- Platform sweeps were NOT run on #804 and the PR says so: no spec, route table, migration or
  gateway config changed.

**The three classes to hunt, each found in this tree TONIGHT — treat each as a hypothesis that
there is another instance you can find:**
1. **An assertion that cannot reach its subject.** `ks622-mfa-failure-lockout.test.ts` holds a
   **passing** case named *"CONTROL — a missing MFA code is MFA_REQUIRED"* that stubs
   `getPlatformAdmin` to return **null**, so every request in that file falls through to the
   regular-user branch — **the control never enters the branch its name claims.** Separately, a
   "sweep" case in #799 compares two literals in the same file while its comment claims it would
   have caught a finding it could not have. **Read what each fixture makes REACHABLE; never read a
   test's name as its coverage.**
2. **A control that does not control.** The builder's own KS-737 harness first failed both POSITIVE
   controls with 401 (a wrong mock path made it refuse everything) — without those controls, "leg 1
   returns non-200" would have reported a bypass that was never demonstrated. **For every red-proof
   in this batch, ask what would have happened had the harness been broken.**
3. **A guard whose corpus is narrower than its claim** — an all-clear, an exemption list, a
   baseline, or a checker whose message asserts more than its measurement covers. #800 is a fix for
   exactly this shape; check the fix did not reproduce it.

**Also worth a direct question:** #800's `check-app-db-password-default.sh` was 164 lines invoked by
nothing, inside the PR closing that same "does not reach" shape. **Is anything else in this batch
shipped-but-unreachable?** A whole-tree invocation search is cheap and it found the last one.

## 8. Logistics
- **Time-box:** one bounded pass. Depth over breadth — #804 first if you must cut.
- **Report to:** `projects/secuura-blockchain/reports/2026-09-03-s119-batch-through-code/SUMMARY.md`
  under your own tree, and mail Wednesday a summary. **Wednesday will read the FULL report, not the
  mail** — so put the load-bearing measurements in the report and do not compress them away.
- **Escalation:** back through Wednesday (`wednesday-agent@agentmail.to`, QUESTION subject).
  Approval-class items always pause for Kam. Priority on any finding is the humans' call.
- **Wednesday's standing ask, unchanged:** your NOT-TESTED list is first-class output and is read as
  carefully as the findings. Say plainly what you could not reach and why.

PROVENANCE:
- The three heads, their SHAs and the claim that all are clean/requested/unmerged | s119's Session wrap mail 2026-09-03T13:02:07Z in wednesday-agent@agentmail.to | read 2026-09-03
- #799's comments-only measurement (0 non-comment changed lines, control 64) | s119's CORRECTION mail 12:31Z, independently reproduced by Wednesday | read 2026-09-03
- #800's fix, its deliberate whitespace-inside-quotes limit, the 8-case fixture and the 4/4 red-proof against a copy | s119's STATUS mail 12:44:47Z | read 2026-09-03
- #804's two legs, the separate status/token assertions and the 7/7 | s119's STATUS mail 12:55:53Z | read 2026-09-03
- The ks622 control that stubs getPlatformAdmin to null, and the harness's first-run control failure | s119's STATUS mail 12:55:53Z | read 2026-09-03
- The 2-of-27 pre-existing import failures and their BACKLOG.md filing | s119's STATUS mail 12:55:53Z and its wrap 13:02:07Z | read 2026-09-03
- develop at 7dd304b7c | s119's wrap, confirmed by its own ls-remote rather than the merge API reply | read 2026-09-03
- The source tree path | /Volumes/DevMASTER/!CODING/Secuura/Blockchain/2_Project_Files, listed in this action | read 2026-09-03

SELF-CHECK: re-read end-to-end for contradictions | 2026-09-03 23:05
