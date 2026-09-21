# QA Agent Invocation Brief — Datasec/NexusAI, RD-518 Key Vault identity + loud fallback — THROUGH-CODE, round 2 of 2

**Written by Tuesday 2026-09-21.** Commissioned on the builder's READY FOR QA mail of 01:00Z.

## Charter
Read `fleet/qa-agent/QA_AGENT_CHARTER.md` in full first. You are an independent tester. You did not
build this and you owe it nothing. **Every sentence below that reports what the builder says is a
CLAIM, not a finding.** Where this brief quotes a measurement, it is quoting the seat that wants a GO.

## 1. Target
- **Branch `rd-518-kv-identity-r2-s75c` @ `9a7bc0c36d59c264040c9c6dce982c7576591ec1`** (short `9a7bc0c`), pushed to origin (verified at commission).
- Base **`1c4fcb0`** — the merge commit — **exactly ONE commit in range**, verified ancestor.
- The shape, verified at commission and not taken from the builder:
  - `9a7bc0c` parents `[1c4fcb0]` — the fix commit.
  - `1c4fcb0` parents `[6ea15a0 60c76d7]` — round 1's head merged forward with main (C-68, never rebased).
  - `6ea15a0` is the sha **round 1 gated and failed**.
- **Companion branch `rd-518-r2-runbook-fix-s75c` @ `c54d44cea9f2aea6090015118606cdc48ec6a71b`** (`c54d44c`), pushed. This is F-05's fix and it is **deliberately NOT in the head under test**. You need it to run, but judge it separately.
- **NOT on main. Nothing merges on your word or the builder's.**
- **No worktree is pinned for you.** Build your own scratch worktree from the object store at the sha
  (round 1's pattern). The repo is
  `/Volumes/KK_T9_External_HDD/!CODING/Datasec/NexusAI/2_Project_Files`.
  ⚠ Its working checkout is NOT at this sha and has uncommitted modifications — **pin everything to
  the sha above, never to `HEAD`, and never clean or stash that checkout.**

## 2. Why this is THROUGH-CODE and not a re-run of tier 1
Round 1 was TIER 1 and returned **🔴 NO GO** at `6ea15a0` with five findings: F-01 BLOCKER,
F-02 MAJOR, F-03 MAJOR (test design), F-04 MINOR, F-05 MINOR (obstacle).
Round 1's report is
`/Volumes/KK_T9_External_HDD/!CODING/Testing Agent MAIN/projects/nexusai/reports/2026-09-20-rd518-6ea15a0-tier1/report.md`
— **read it before you read the fix.** Your job is the five findings and what the fix disturbed,
carried through the code. The tier-1 weight was spent establishing the subject; do not spend it again.

The stakes are unchanged and they are why round 1 was tier 1: this decides whether customer secrets
are protected by a Key-Vault-managed key or a machine-derived one, and whether a broken deployment
says so out loud or looks healthy.

## 3. 🔴 THE TWO LIMITS THE BUILDER DECLARED — these are your first work, not your last
The builder put two limits in its own BLUF. **A declared limit is a place the evidence stops, and
the gate's job is to decide whether the verdict can stand on what is left.** Neither is a finding
yet. Neither is cleared by having been declared.

**L-1. STATE 2 of the four-state matrix (403 non-admin) was NOT driven this round.** It needs an
injected session. The builder re-drove the anonymous paths only, and says so: *"what I report is
three states plus a scanner control, not the gate's four."* Round 1's own M-A insisted on a control
that proves the instrument can see a refusal at all. **Decide explicitly: does F-02's fix rest on a
state nobody has driven since the fix landed?** If it does, that is a finding regardless of how
honestly it was declared.

**L-2. The C-57 id-superset shortcut is CONDITIONAL.** It holds only because nothing was
content-merged, which the builder says it checked rather than assumed. **Check the check.** The
claim is that every `__tests__` file in the merged tree is byte-identical by blob hash to one
parent's except the one file it edited. That is falsifiable by you in minutes and it is the whole
basis for `missing 0`.

## 4. The five findings — what to verify
Take each to source. The builder's account is in the READY mail and in the commit; neither is evidence.

**F-01 (BLOCKER) — claimed FIXED and red-proved before the fix.** The claim: `how` was hoisted out of
the `try` with a truthful initial value, so a throw from `buildKeyVaultCredential` itself still
reports honestly; R7/R8 failed with `ReferenceError: how is not defined` at `encryptionService.js:385`
before the fix. **The bar the builder itself set is CLEARS BASE:** at base `34ad321` the same catch
carried `logger.warn(... ${e.message} ...)`, so "no error" is not the bar — the SDK message AND the
identity are. Verify the diagnostic is at least as informative as base, not merely non-crashing.

**F-02 (MAJOR) — claimed FIXED at the boundary, blast radius claimed ENUMERATED not lower-bound.**
Round 1 could only call it a *lower bound* because it did not enumerate every route calling
`buildFullHealthDetails`. The builder now claims exactly three callers, with `/api/admin/health` the
only one serving the blob whole, and `publicKeyVaultState()` an allow-list so later fields are
withheld by default. **Enumerate them yourself.** A missed fourth caller is the finding.
Note the design decision to judge: source redaction was **rejected** on the grounds that it would
delete the operator diagnostic F-01 restores — the two would cancel. Is the boundary the right place?

**F-03 (MAJOR, test design) — claimed FIXED; M7 now reddens R7 and R8** (was 7 passed / 0 reddened).
Claimed: one lock hold, three runs, floor 0 at every one, RUN 2 (revert the hoist) the positive
control and it fired; R2 stays GREEN under M7 and is offered as the gate's own diagnosis confirmed.
**A mutation score is only as good as its control.** Verify the control fired and that the floor
claim is instrumented, not asserted.

**F-04 (MINOR) — claimed FIXED.** Comment corrected; `marketplace-api.js` claimed to have zero
occurrences of `keyVaultName`. One grep.

**F-05 (MINOR) — claimed FIXED on the separate branch `c54d44c`.** The runbook cost round 1 about a
third of its session. The trap it now documents: the misconfiguration listener binds the port and
answers `/api/health` with plausible JSON **from a process that is not the app**, so the runbook says
to identify the surface by the two boot lines. **You are the natural test of this fix — you have to
follow it. Report whether it actually works as written, and whether you were ever served by the
wrong process.**

## 5. The seven new cells
R7 · R7b · R8 · R9 · R9b · R10 · R10b — three are controls. The builder's reasoning: without R7b
"we are in the KV-access branch" is unfalsifiable (R2's exact hole); without R9b, R9 passes against a
deny-list stripping precisely `detail`, leaving the next operator-only field to ship; R10/R10b close
RD-555 F-2(a)'s other mode, where the projection is perfect and the call site stops using it. R10 is
a **source-level claim over the shipped file, labelled as one**. Judge whether the controls can fail.

## 6. Counts — C-57, claimed regenerated twice and never hand-edited
    parents: 6ea15a0 = 3709/210 · origin/main = 3772/214
    merge 1c4fcb0:  PASS — 3779/3779 across 215 suites   (3772 + rd518's 7)
    fix   9a7bc0c:  PASS — 3786/3786 across 215 suites   (3779 + 7 new cells)
215 is not fewer than the larger parent's 214. Reproduce the head count yourself. Arithmetic that
works is not the same as a suite that ran.

## 7. Drivable surface — LOCAL RUN, **NOT THE DEMO**
🔴 **The demo cannot test this** (RD-76, C-02: the demo's `/login` carries zero `<form>` and zero
`<input>`). Use a LOCAL RUN of `9a7bc0c` in open mode per `docs/runbooks/local-run-for-qa.md`
**as corrected on `c54d44c`** — read it with `git show`; it is off main.

## 8. 🔴 Floor discipline — three seats are live on this project
Every jest invocation goes through `session-tools/nexusai-lock.sh`. Hold the lock ONCE across a
multi-run measurement. Record the foreign `backend/server.js` count beside every result **by `ps`,
never by `EADDRINUSE`**. **A zero is reportable only if a control fired in the same window.**
Queueing behind another seat is the mechanism working, not a stall.
Run `bash -n` on any script you write before you run it — the builder lost a 910-second lock wait to
a quoting bug this round and said so.

## 9. What is HELD and must stay held
No merge to main. No deploy. No registry, no Partner Center, no production, no money, no external
comms. No real Azure, credential, vault, tenant or key. `wrappedDekPath`, the vault URL construction
and the wrapping key name untouched. `PRIVACY.md` / `TERMS` not edited (C-65). No `--no-verify`, no
force-push. **You are findings-only: do not commit, do not move any branch.**

The DEGRADED health flip is **design only, not in this commit**
(`5_Project_History/2026-09-21_S75C_rd518-degraded-flip-design.md`). Out of scope for your verdict —
but the builder flagged a trap in it worth your eye if you have time: the public `degradedReason` is
sanitised by a single GUID regex that catches an identity clientId and **does NOT catch a vault
hostname**, so reusing `detail` as the degradedReason would reintroduce F-02 on a more exposed
surface, permanently and publicly. Cell D3 is claimed to guard it.

## 10. Escalation
Round 2 of 2. **If you find a Major, C-62 says it is ticketed, not sent to Kam — a third round on
this class is Kam's own call, so say so and stop rather than assuming one.**
If you believe the delta justifies full tier-1 weight after all, STOP and mail Tuesday with the
reason rather than silently widening the scope.

## 11. Output
Write your report to:
`/Volumes/KK_T9_External_HDD/!CODING/Testing Agent MAIN/projects/nexusai/reports/2026-09-21-rd518-9a7bc0c-round2/report.md`

MAIL YOUR VERDICT to `tuesday-agent@agentmail.to` with the subject exactly:
`[QA/Datasec-NexusAI -> Tuesday] GATE VERDICT — RD-518 round 2 @ 9a7bc0c (through-code)`

The AgentMail key is `AGENTMAIL_API_KEY` in `/Volumes/KK_T9_External_HDD/TUESDAY/4_Credentials/.env`
— an absolute path; the QA project has no `4_Credentials` directory of its own.

**Rule 2 stands: what you did NOT test is first-class output.** Round 1's blast-radius gap became
this round's main question precisely because round 1 wrote it down.
