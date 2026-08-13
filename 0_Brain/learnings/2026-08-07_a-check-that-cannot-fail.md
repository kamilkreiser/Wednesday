---
date: 2026-08-07
type: principle
source: "Formulated by the Datasec/Vision_Sales_Portal agent — 'A check that cannot fail is not a check' — after catching two of its own. Four independent occurrences across three agents and me in a single day."
status: live
supersedes: ""
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

### The third member: a check that MISREPORTS what it saw (2026-08-14, same agent)

One GitHub secondary rate limit on a GHCR pull, wearing three disguises at once:
1. **Docker renders a 403 rate limit as** *"repository does not exist or may
   require 'docker login'"* — printed after `Login Succeeded!`, with a correct tag.
2. **The enforce step renders a SKIPPED suite as** *"k6 smoke failed"*.
3. **Re-running relocates the failure to a different suite**, so the second red
   reads as a different problem.

An operator reading only the top line audits PAT scopes and package visibility and
finds nothing. That is not hypothetical: it happened on **2026-08-05** with PR
#646, and I mis-attributed those reds to real Schemathesis/Akto findings when no
test had run — a Secuura session caught it. **Same mechanism, eight days apart.**

**And the nastiest variant, worth its own name: a remedy that hides its own
ineffectiveness by MOVING the symptom.** Re-running felt like new information and
was the same information; only comparing the two runs' *victim suites* showed the
retry had changed nothing. When a fix relocates a failure rather than removing it,
suspect a shared resource, not a flaky test.

**How to apply:** when a failure message names a cause, check that the message
*could* have named a different one. Error strings are written by whoever expected
a different failure than the one you have — a 403 rendered as "does not exist", a
skip rendered as a fail, a rate limit rendered as a permissions problem. **Find
the first failure and read the raw step output, not the summary that interprets
it** (see [[2026-08-06_artifact-presence-is-not-execution]], which this is the
message-layer twin of).

**Related:** [[2026-08-07_valid-is-not-delivered]] (my instance),
[[2026-08-06_artifact-presence-is-not-execution]],
[[2026-08-06_never-discard-stderr]],
[[2026-08-06_exercise-mechanisms-before-arming]],
[[2026-08-07_enumerate-every-surface-before-done]], [[_ledger]]
