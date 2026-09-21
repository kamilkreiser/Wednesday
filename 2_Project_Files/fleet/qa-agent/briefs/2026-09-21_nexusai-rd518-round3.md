# QA Agent Invocation Brief — Datasec/NexusAI, RD-518 — THROUGH-CODE, round 3 (the LAST round Kam authorised on this class)

**Written by Tuesday 2026-09-21.** Commissioned on NexusAI-C's READY FOR QA of 05:53Z.

## Charter
Read `fleet/qa-agent/QA_AGENT_CHARTER.md` in full first. You are an independent tester. **Everything below that reports what the builder says is a CLAIM.**

## 1. Target — verified at commission from the object store
- **Branch `rd-518-kv-identity-r2-s75c` @ `4230d237321a2f252730aeca37c73a950eca0f25`** (short `4230d23`), pushed.
- Base **`9a7bc0c`** (round 2's head, which round 2's gate returned NO GO on), **exactly ONE commit**.
- The delta is THREE files: `backend/server.js` · `__tests__/rd518-r3-health-detail-decision.test.js` (new) · `scripts/verify-expected-counts.json`.
- **`backend/services/authEnforcement.js` is untouched: 0 diff lines.**
- The 6 changed lines that mention `adminGateRefuses` are ALL COMMENTS (5 in the new test's header, 1 in server.js), checked line by line. **Confirm that no call site of `adminGateRefuses` changed. That is a hard stop from Kam's scope (RD-594 is excluded).**
- Companion runbook `rd-518-r2-runbook-fix-s75c` @ `c54d44c` (unchanged). **No worktree is pinned: build your own at the sha.**
- The repo's working checkout is elsewhere and dirty: pin to the sha, never HEAD, never clean or stash it.

## 2. Why THROUGH-CODE, and what the stakes are
- Round 2 (`…/reports/2026-09-21-rd518-9a7bc0c-round2/report.md`) returned **NO GO on the F-02 class only**, with F-01, F-03, F-04 and F-05 CLEARED. **Read it first. Do not re-drive what cleared.**
- Kam authorised round 3 at 15:16 (C-121), scoped to **G-01 (RD-592) + G-02 (RD-593)**. RD-594 is explicitly OUT.
- C-105 puts RD-518's fix ahead of the Marketplace resubmission. **This gate is on the critical path to it.**

## 3. G-01 — the boundary now asks for an ADMIN
- Claimed: `const isAdmin = !!(req && req.user && req.user.role === 'admin');` replaces `!!(req && req.user)`.
- **Drive it yourself:** a VIEWER in both of round 2's states must NOT receive the identity clientId or the vault hostname:
  - S5: `authEnforced` stored, no Entra config
  - S6: `authEnforced` stored, `firstRunComplete:false`
- An ADMIN must STILL receive the full `detail`. That keeps F-01 and F-02 from cancelling, and it is the positive control.
- **The C-01 claim, to verify, not accept.** The builder says:
  - no consumer of `keyVaultEncryption` or `.detail` exists in `static/`
  - the first-run consumers read the sibling `keyVaultStatus` from `/api/health`
  - so no first-run path needs `detail` without an admin session

  If you find one that does, that is a C-01 question for Kam: say so and stop.

## 4. G-02 — the decision is now tested BEHAVIOURALLY
New file `rd518-r3-health-detail-decision.test.js`: a real server, admin / viewer / anonymous, in both states A (first run complete, no Entra) and B (Entra configured, first run incomplete). **The claimed red-proofs — reproduce BOTH:**
- **The gate's own mutation:** body → `return full;`. The G-01 viewer cell must go RED in BOTH shapes. The claim is that round 2's suite stays 14/14 green under it, which is the measurement of the gap it closes.
- **The G-01 regression:** predicate → `!!(req && req.user)`. It must go RED on the viewer cells in both shapes.

🔴 **The builder caught two false greens of its own, and this is where to look hardest:**
- Its first cut built the states WITHOUT storing `authEnforced`.
- The middleware returns at `ALLOW_OPEN_MODE` BEFORE assigning `req.user`, so the viewer cells passed because there was **no user at all**.
- The admin cell exposed it. The fix is two server lifetimes: build state + sessions in open mode, write the flag to disk, then drive enforced.
- **Confirm that `req.user` IS populated with `role: 'viewer'` in the viewer cells, i.e. that the cells now test the ROLE and not the ABSENCE of a user.** A viewer cell that passes with no user is the exact defect G-02 exists to prevent.

**Stated by the builder, not an overclaim:** in both states the ANONYMOUS cell gets **401** from the middleware, so it asserts a refusal, not a redaction. Judge whether that is honestly labelled.

## 5. New finding the builder filed — RD-596, out of scope, judge its framing only
`/api/health` never serves `keyVaultStatus` (`publicHealthResponse` allow-lists it away), so the first-run Key Vault tile can never read "Connected". It fails in the safe direction. **Do not fix it.** Say whether it is correctly framed as pre-existing and out of scope.

## 6. Counts
`VERDICT: PASS — 3796/3796 across 216 suites` (3786 + 10 new cells, one new suite). Reproduce it.

## 7. 🔴 FLOOR DISCIPLINE — the CORRECTED counter (corrected twice today; read THIS version)
- Every jest run through `session-tools/nexusai-lock.sh`, lock held once per multi-run measurement.
- Count foreign server processes by the **BASENAME of argv[0]** == the runtime **AND** the script argument == the server entry point.
- **Never raw `comm`:** macOS reports it as the full execPath for harness-spawned servers, so a `comm` counter is BLIND. The RD-574 round-2 gate measured 0 vs 1 (its R2-1); the builder reproduced it (0 / 0 / 1 across the three forms).
- Separate yours from foreign by **ANCESTRY**.
- **Before trusting any zero, spawn a control the same way the harness does and require the count to RISE.** The builder's control reads 2, not 1, because the `node -e` launcher carries the entry path too. That is an over-count, which errs safe.
- Reap everything you start.

## 8. Surface — LOCAL RUN, NOT THE DEMO (RD-76).

## 9. HELD
No merge, no deploy, no registry, no Partner Center, no production, no money, no external comms, no real Azure / credential / vault / tenant / key. **Findings-only: do not commit, do not move any branch.**

## 10. Output
Report: `/Volumes/KK_T9_External_HDD/!CODING/Testing Agent MAIN/projects/nexusai/reports/2026-09-21-rd518-4230d23-round3/report.md`

MAIL YOUR VERDICT to `tuesday-agent@agentmail.to`, subject exactly:
`[QA/Datasec-NexusAI -> Tuesday] GATE VERDICT — RD-518 round 3 @ 4230d23 (through-code)`

AgentMail key: `AGENTMAIL_API_KEY` in `/Volumes/KK_T9_External_HDD/TUESDAY/4_Credentials/.env`.

**Round 3 is the last round Kam authorised on this class. If you find a Major, C-62 says it is ticketed, not escalated — a fourth round is Kam's call, so say so and stop.** Rule 2: what you did NOT test is first-class output.
