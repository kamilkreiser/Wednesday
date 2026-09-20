---
date: 2026-08-07
type: principle
source: "Formulated by the Datasec/Vision_Sales_Portal agent — 'A check that cannot fail is not a check' — after catching two of its own. Four independent occurrences across three agents and me in a single day."
status: live
supersedes: ""
tier: MIXED
---

# A check that cannot fail is not a check

**The shape.** A verification runs, reports success, and could never have
reported anything else — because it measured the wrong thing, errored and
swallowed it, or asked a question whose answer was fixed in advance. It is worse
than no check, because it converts an open question into a settled one.

**Four occurrences on 2026-08-07 alone, across three agents and me:**

1. **Mine — the close-bell 403.** I verified the API key's value, length and
   byte-equality with a working one, and concluded it was valid. It was. The key
   was never reaching the process that used it (`source` without `set -a`).
   **Every check I ran was on the key at rest, and non-delivery is invisible to
   all of them.** Two nights of failure, and a wrong root cause reported to Kam.
2. **Vision — a private-key scan that errored and still printed "clean".** The
   shell scan of a mail for key material hit the `-----BEGIN` lines, read the
   leading dash as a flag, errored on exactly the two lines that mattered, and
   reported clean anyway.
3. **Vision — a print-layout check measuring a hidden element.** It measured
   `#quoteDoc` heights and got `0`, because the element is `display:none` on
   screen. Zero looked like a pass. Replaced with a real PDF render — which then
   found a customer-facing defect on page 2 that reading the source had missed.
4. **NexusAI — a `find` that timed out and read as a negative result.** A search
   for `pane_prompt_check.sh` silently timed out traversing an external drive and
   returned nothing; the agent came one step from reporting my evidence as
   fabricated on the strength of it. Their phrase: *"checking a premise badly is
   not checking it, and it fails in the direction that feels like diligence."*

**Why this is a distinct lesson and not just "verify properly".** All four
verifications were *performed*. The people running them were being careful —
that is the trap. `always-verify-and-check` fires on "did I check?", and every
one of these answers yes. The question it does not ask is **"could this check
have come out differently?"**

**How to apply — one question, asked of the check rather than the result:**

1. **"What would make this check fail?"** If there is no concrete answer, the
   check is decorative. For a credential: *what would show a valid key that
   never arrived?* — printing `len(key)` inside the failing process. For a
   layout: *what would show a broken page?* — the rendered artefact, not a
   hidden element's geometry.
2. **A zero, an empty result and a silent success are suspects, not evidence.**
   Zero rows, zero height, no matches, "clean" — each is equally consistent with
   "nothing is wrong" and "the check never ran". Distinguish them before
   reporting.
3. **Never let a non-zero exit be swallowed.** Occurrence 2 is
   [[2026-08-06_never-discard-stderr]] wearing a different hat: the error was
   printed *and ignored*, which is the same as discarding it.
4. **Prefer checking the artefact over checking the intent** — the rendered PDF,
   the served page, the value inside the failing process. Generating the real
   output beat reading the source twice in one day on the same project.
5. **When a check surprises you by passing, be as suspicious as when it fails.**
   Three of these four looked like good news.

**Meta-note:** the formulation is the Vision agent's, arrived at independently
while I was diagnosing my own instance of it. That is the second protocol
improvement the fleet handed me today. My job is to notice and propagate them.

<!-- tier: P-Secuura/Blockchain -->
## The concrete remedy, added 2026-08-13 (Secuura/Blockchain s28)

The rule above asks *"what would make this check fail?"* — good, but it is a
question you have to remember to ask. The Secuura agent found the **structural**
version, and it is cheap enough to be non-negotiable:

> **A negative-only test suite cannot distinguish "correctly rejecting" from
> "refusing everything". Every rejection suite needs a case that MUST succeed.**

**The case that taught it.** Its first HTTP matrix for the KYC callback guard
returned **401 for every probe — including the positive control.** Six rejections,
all "correct". Without the must-succeed case that reads as *"every rejection works,
confirmed"*, and it would have been reported that way. The logs showed why: the
route is JWT-gated, so **none of the six probes ever reached the guard being
tested.** Two real defects fell out of asking why the positive control failed
(the route Microsoft is told to call does not exist — registered URL 404, real
route 200; and the provider authenticates with an api-key and cannot hold a
Secuura JWT).

**Why this generalises past HTTP:** a blanket refusal, an empty result set, a
universally-failing parse and a permanently-down dependency all *look identical*
to a working negative test. The positive control is the only thing that
distinguishes "the guard is discriminating" from "nothing is getting through".

**How to apply:**
- Any suite that asserts things are rejected/blocked/filtered/denied carries at
  least one case that must be **accepted**, and it is a failure of the suite if
  that case does not pass.
- Same for absence checks: prove the search *can* find something before reporting
  that it found nothing. (My own `cycle` subcommand shipped its first draft with
  an unbound variable, so it searched for nothing and reported "no child" — the
  same defect, in the code written to fix a repeated failure.)
- A check that cannot fail and **a check that cannot see** are the same defect —
  their phrase, after a CI poll ran blind for ten minutes because a control
  character broke a strict JSON parse, and a status query used a short SHA and
  returned "0 runs, 0 failures".

<!-- tier: P-Secuura/Blockchain -->

## The cases — moved 2026-09-20, read on demand

The 27 case sections below were moved VERBATIM to `_cases_2026-08-07_a-check-that-cannot-fail.md` under Kam's ruling (b) (card `tuesday-boot-digest-outgrew-the-window`, 2026-09-20 16:41: *keep the whole read, shrink the corpus to fit*). **Nothing was deleted or summarised.** The headings stay here because a heading IS the retrieval handle (`weekly-consolidation.md` step 4: a merged lesson that cannot be grepped is a destroyed memory). **Open the cases file when you need the precedent behind a rule.**

- A failure-only log going quiet is not recovery (2026-08-22, Secuura s61)
- The third member: a check that MISREPORTS what it saw (2026-08-14, same agent)
- A test that cannot CLEAN UP starts asserting against live data (2026-08-15, Secuura s35)
- A positive control proves the suite it RAN IN, and nothing about its neighbour (2026-08-15, Secuura s35)
- The inverse: a REPRODUCTION that cannot reproduce (2026-08-15, Datasec/NexusAI)
- The refinement that makes the positive-control rule actually work (2026-08-16, Secuura s37)
- An indicator that can MISS its own event (2026-08-24, Datasec/NexusAI)
- The control needs its own control (2026-08-23, Datasec/NexusAI)
- The condition we had not stated: on a side-effecting system, the positive control IS an action (2026-08-14, Secuura s34)
- The mirror: an ABSENCE claim needs a positive control too (2026-08-14)
- Three "cannot see" members from one micro-session (2026-08-25, Datasec/NexusAI s5) — and a derivation lesson from its neighbour
- A test's NAME is not its coverage (2026-09-03, Secuura s119 — the member that let an AUTH BYPASS survive a suite that appears to test it)
- A census, a writer and a verifier that descend from ONE parse are one view rendered three times (2026-09-04, Datasec/NexusAI S29 — its own diagnosis, then its own correction to that diagnosis)
- THE ALL-FAIL RED-PROOF: a tamper that destroys the SUBJECT, so the failure set stops discriminating (2026-09-04, Datasec/NexusAI — self-caught and self-reported)
- A FIXTURE THAT CANNOT REACH THE PRODUCT'S PATH — the entry-point member (2026-09-04, Datasec/NexusAI RD-245; a BLOCKER found under a green suite the tester re-derived)
- A KEYWORD SEARCH OVER A CORPUS THAT CONTAINS THE SEARCH TERM AS VOCABULARY (2026-09-04 — three instances in one evening)
- `timeout N cmd | wc -l` PRINTS 0 WHEN THE COMMAND IS KILLED — and no `||` can catch it (2026-09-04, twice in one evening)
- CORRECTED the same session, by the same agent, and the correction is the better lesson
- A red-proof proves a check CAN fail; only a GREEN BASELINE proves it can pass for the right reason (2026-09-04, Secuura s120 — a guard defeated by its own doc comment)
- The AXIS a guard is blind on is not the axis it was designed for (2026-09-04, Datasec/NexusAI — a perfectly-implemented guard, green on a defect it could never see)
- THE OTHER END OF IT: a red-proof on a subject that did not COMPILE is not a red-proof (2026-09-04, Secuura s121 — the pair to the green-baseline rule above)
- A MULTI-CLAUSE guard red-proofed with a fixture that trips BOTH clauses has measured the pair and learned nothing about the parts (2026-09-04, Datasec/NexusAI S31 — the builder found its OWN guard was decoration)
- THE SECOND HALF, added hours later by the TESTER that verified the fix (2026-09-04, QA re-gate on `aad37da`)
- AN ELIMINATION SET THAT IS EXHAUSTIVE WITHIN ONE CATEGORY AND SILENT ABOUT THE OTHERS (2026-09-04, Datasec/NexusAI S32 — it disproved its OWN filed finding)
- A TEST HELPER THAT REIMPLEMENTS THE PRODUCT IS A MOCK THE MOMENT THE PRODUCT MOVES (2026-09-05, Secuura s128 — found by its own red-proof, not by reading)
- THE DELIVERY MEMBER, and it is the sharpest one yet because the failing check IS this family's own enforcement (2026-09-07, W-tier, agent-caught in two minutes)
- THE MEMBER THAT NAMES THE RIGHT PROPERTY AND OBSERVES THE WRONG WRITE (2026-09-08, Secuura s152 — twice in one seat, both caught by RUNNING)
