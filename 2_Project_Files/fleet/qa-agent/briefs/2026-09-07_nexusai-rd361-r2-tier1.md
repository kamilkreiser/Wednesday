# QA GATE — Datasec/NexusAI RD-361 (`rd-361-fail-closed-unknown-s43` @ `1149d1c`), TIER 1. **Round 2 of 2 under Kam's cap.**

**Charter first, in full:** `/Volumes/KK_T9_External_HDD/!CODING/Testing Agent MAIN/CLAUDE.md`
(this seat runs from the **T9**; DevMASTER is not mounted — every path in this brief is a T9 path.)

**TIER 1, ruled by Wednesday.** The change decides **whether an unauthenticated caller reaches 175
routes** when the auth subsystem cannot read its own state. It is the fail-closed boundary of a
Marketplace offer. Round 1 was **NO GO**: the fix closed **1 of 4** failure modes, and the Azure Files
case named in the builder's *own* rationale survived it.

**ROUND 2 OF 2 UNDER THE CAP** (Kam, 2026-09-05 20:19): a second NO GO **ships what is closed and
tickets the residue**. There is no round 3 without Kam's word. So your verdict must separate
*"this specific claim is false"* from *"this is not the shape I would have chosen"* — only the first
blocks.

## 1. Target — the four SHAs, and they are four different facts
- **Branch under test:** `rd-361-fail-closed-unknown-s43`
- **Head:** `1149d1c332b6ebaac68393ba0afdeb8c65ebdd29`
- **Round 1 head (the red-proof baseline):** `e4d9147`
- **Base / merge-base / `origin/main` head:** `a9a8cb6e3fc62b8c08e1f3aadecb08519f1f6ddc` —
  **all three coincide today**; the branch is not behind. Re-derive this rather than trusting it.
- **NexusAI's mainline is `main`, NOT `develop`.** (Secuura uses `develop`; do not carry that across.)
- **Diffstat round 1 → round 2:** 6 files, +313 / −41 —
  `__tests__/auth-gate-fail-closed.test.js`, `backend/jsonStorage.js`,
  `backend/routes/entraProvisioning.js`, `backend/server.js`,
  `backend/services/authEnforcement.js`, `scripts/verify-expected-counts.json`.
- **Repo:** `/Volumes/KK_T9_External_HDD/!CODING/Datasec/NexusAI/2_Project_Files`
- **Work in your OWN worktree/clone.** Do not write into the builder's checkout.
- **NON-PROD. NO DEPLOY on this round. Do not touch any Azure resource or any live box.**
  Kam's production lift of 2026-09-07 12:07 is **Secuura only** (his 12:10: *"Only secure"*).
  **Datasec production is not in scope for anything, at any point in this pass.**

## 2. 🔴 THE CENTRAL QUESTION — are the two newly-load-bearing signals actually correct?
Round 2 closes the holes using **two flags that already existed in `jsonStorage` and were being used
by nothing**: `dataDirFallbackActive` and `persistenceSentinelPreexisting`.

**A field that exists and is unused is the fingerprint of an intention that was never finished.**
Before accepting either as a discriminator, establish independently:
1. **Is each flag SET on every path where its meaning holds, and only there?** Enumerate every
   assignment and every early return that skips one. A discriminator that is silently `false` on a
   path fails **open** — which is the entire defect class this ticket exists to close.
2. **`persistenceSentinelPreexisting`** exists because `checkPersistenceSentinel()` *creates* the
   sentinel, so presence at read time proves nothing. **Prove the pre-existing flag is captured
   BEFORE the create, on every ordering**, including a crash between read and create.
3. **`dataDirFallbackActive`** is claimed to close D (data dir unusable → fell back to `/tmp`).
   The builder says `emergencyBackupStatus` could not serve because it is set to `'unavailable'` at
   three sites for three reasons. **Check that claim** — and check whether the new flag has the same
   ambiguity in a different costume.

## 3. RE-DERIVE THE FOUR-SCENARIO TABLE YOURSELF, on both heads
The builder reproduced the gate's round-1 table against its own round-1 worktree and reports:

    A  corrupt file            r1: deny   r2: deny
    B  settings ABSENT         r1: OPEN   r2: deny
    C  authEnforced clobbered  r1: OPEN   r2: deny
    D  data dir unusable       r1: OPEN   r2: deny   <- the Azure Files case
    genuine first run          r1: open   r2: open   <- negative control
    CONTROL enforced+readable  r1: require-session  r2: require-session

**Run it yourself, on real `JsonStorage` and real directories, on BOTH heads.** The negative control
and the positive control are what stop *"round 2 denies everything"* from satisfying the table — so
**both controls must be exercised, not assumed**, and a green baseline matters as much as the red.

## 4. 🔴 THE F-2 GUARD — the builder's own metric moved the WRONG WAY, and it says so
Round 1's guard counted `authGateDecision` calls. The mutation that removes the fix **adds** such a
call, so **the guard's metric went UP while the fix was being removed.** That is a guard that cannot
fail on the thing it guards.

Round 2 renames the shape to `mustHaveSession()` so the mutation must **delete** a counted call.
- **Red-proof the new guard yourself**, by performing the revert on a copy and asserting the tamper
  actually happened before asserting the count drops.
- **A multi-clause guard red-proofed with a fixture that trips every clause has measured the pair and
  learned nothing about the parts.** If the guard has more than one clause, prove each clause
  **individually**.
- Then prove the **green baseline**: it passes for the right reason on untampered code.

## 5. THE SIX-SITE CLAIM — and why the count is the suspect
The builder's round-1 claim *"every deciding site routes through `authGateDecision`"* was **false as
written**: `serverCode()` read `server.js` only, so `backend/routes/` was invisible. A sixth site
(`backend/routes/entraProvisioning.js:107`) existed; it failed closed, so there was no live exposure.

The guard now reads **two files** and asserts **six sites**.
- **Enumerate the deciding sites across the WHOLE tree, not across the two files the guard reads.**
  An enumeration's **file set and extension list are part of its claim** — an omitted path is a
  silent scope reduction that looks exactly like a complete answer.
- Say what your own sweep covered and what it did not.

## 6. WHAT THE BUILDER SAYS IT DOES **NOT** CLOSE — adjudicate the boundary, do not re-litigate it
Verbatim: *a persistent volume **wiped between deploys** presents with no sentinel, no settings and no
artefacts — byte-identical to a genuine first deploy from inside the volume. **It still opens.***
`jsonStorage` fires `persistenceWiped` at error severity for that shape; the durable fix is the
platform layer (**SEC-01 remediation 3 / RD-363**). Denying there would brick every legitimate first
deployment, which a Marketplace offer cannot do.

**Wednesday's position: that is a judgement, honestly disclosed, and it is very likely right.**
Your job is narrower and answerable:
1. **Is the residue genuinely unreachable from inside the volume?** Is there any signal (mount
   metadata, inode/ctime, a platform env var, image digest, deployment id) that *does* discriminate
   and was not considered?
2. **Does `persistenceWiped` actually fire** on that shape, and does it reach an operator?
3. **Is the residue actually on a ticket** — RD-363 or another? **Search the board by SYMBOL, PATH and
   ERROR STRING before concluding it is unfiled**, and say what you searched and what you found.
   (*"Pre-existing" and "unfiled" are two different questions and only the first has a control.*)

## 7. F-7 / F-8 — the status code and the audit event
- 503 + `Retry-After: 5` replaces 401 on the deny path. The builder **retracted its own round-1
  reasoning** (it had argued 401 invites an unsuccessful retry; 503 is the retryable one, RFC 9110
  §15.6.4). Conclusion endorsed by Wednesday; **verify the header is actually emitted**, not just set.
- The deny path used `logger.error` only, so **a total auth outage produced no record at
  `/api/admin/audit-log/export`** — the one incident an operator most needs evidence of. Verify the
  audit event now lands there, and that **auditing can never turn a deny into a 500**.

## 8. EVIDENCE RULES — mandatory on every cell you count
1. **For every cell, state what it MOCKS and therefore what it cannot prove.** A cell that mocks the
   store proves statement text and bindings, never behaviour under a real constraint.
   (Same-week precedent in the sibling repo: a green cell stood over a live hole because the test
   double could not enforce a unique index.)
2. **A zero, an empty result and a silent success are suspects, not evidence.** Distinguish "nothing
   is wrong" from "the check never ran" before reporting either.
3. **Capture `rc` on its own line** for any bounded command; a `0` from a killed command is not a zero.
4. **Never delete anything.** Cleanup means quarantine.
5. **Findings-only. You never fix.**

## 9. Verdict shape
**GO** · **GO-with-findings** (say which findings are Majors and which are advisory) · **NO GO**.
Severity is yours; **priority is Wednesday's**. If NO GO, name explicitly **which closed instances
could ship** and **what the residue's ticket should say** — because under the cap that is what happens
next.

Report by mail to `wednesday-agent@agentmail.to`, subject
`[QA -> Wednesday] Datasec RD-361 round 2 (@ 1149d1c, tier 1)`.

PROVENANCE:
- branch head `1149d1c332b6ebaac68393ba0afdeb8c65ebdd29` | `git ls-remote origin refs/heads/rd-361-fail-closed-unknown-s43` run by Wednesday in the same action as writing this brief | read 2026-09-07
- base = merge-base = `origin/main` `a9a8cb6e3fc62b8c08e1f3aadecb08519f1f6ddc` | `git ls-remote` + `git merge-base`, same action | read 2026-09-07
- round-1 baseline `e4d9147` | `git cat-file -t`, same action | read 2026-09-07
- diffstat 6 files +313/−41 | `git diff --stat e4d9147 1149d1c`, same action | read 2026-09-07
- round-2 claims (the four-scenario table, the two flags, the F-2 metric inversion, the sixth site, the not-closed statement) | the builder's own mail `[Datasec/NexusAI -> Wednesday] READY FOR RE-GATE round 2`, 2026-09-07T06:36:08Z, re-read from the inbox in this action | read 2026-09-07
- round 1 verdict NO GO 1-of-4 | Wednesday's mail 2026-09-07T06:21:18Z | read 2026-09-07
- tier cap "two NO GO rounds per class" | Kam, 2026-09-05 20:19 *"Let's go ahead with your recommendation."* | read 2026-09-07
- production lift is Secuura-only | Kam, panel 2026-09-07 12:07 + 12:10 *"Only secure"* | read 2026-09-07

SELF-CHECK: re-read end-to-end for contradictions | 2026-09-07 17:24
