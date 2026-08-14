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

### The family, completed overnight 2026-08-13/14 (Secuura/Blockchain s28–s32)

One agent produced five more members in five sessions. Kept together because the
shared property is what matters: **the check failed in a way that looked like the
answer.** None of them involved the code under test.

- **cannot see** — a status query with a short SHA returned "0 runs, 0 failures".
- **cannot parse** — a strict JSON load died on a control byte and reported zero
  matches; a CI poll ran blind for ten minutes the same way.
- **cannot receive input** — a `docker exec` heredoc with no `-i`, so psql silently
  never ran and the empty result read as clean.
- **runs before its own setup** — a test setting `process.env` after ESM had
  hoisted its imports.
- **run by the WRONG RUNNER** — vitest against a jest suite: "38 files failed, no
  tests", which reads as the code being broken when nothing ran at all.

Their generalisation, adopted verbatim: **a check that cannot parse, cannot receive
input, or runs before its own setup is the same defect as a check that cannot fail.**

**The inverse, done right, belongs here too:** when two auth test files showed red,
the agent stashed its own changes and re-ran clean before attributing them — they
were pre-existing and unrelated. *Blaming your own change for someone else's red is
the same error as missing your own.*

**And the measurement that makes the positive-control rule concrete**, taken three
times on different code: with the guard set to refuse everything, **24 of 35 tests
still passed** (image validation), **9 of 16** (token encryption), **7 of 10**
(billing idempotency). Every survivor was a rejection case. A suite without a
must-succeed case cannot tell you which of those numbers you are looking at.

### The condition we had not stated: on a side-effecting system, the positive control IS an action (2026-08-14, Secuura s34)

The rule above says *always prove the search can find something before trusting that it
found nothing*. Three separate catches today came from it. **Secuura s34 found its limit.**

**The case.** Verifying KS-472's control-byte guard needs both directions. The negative half
— a document title containing U+0000 — returned **400** and created nothing, free of charge.
**The positive half, the identical payload without the NUL, returned 201 and originate
auto-anchored it on the real Cardano preview testnet within seconds** — a permanent
transaction, `simulated=false`.

**And it did NOT clean it up, correctly.** The chain write cannot be un-made and the local
row is the only thing linking it to a document; deleting the row would manufacture **an
on-chain proof with no local record — exactly the KS-587 defect the same deploy was shipping
the fix for.** It relabelled the artefact instead and wrote the behaviour into the runbook.

**The generalisation, now standing:** the negative half of a validation test is usually
free; **the positive half writes.** Before running a positive control, ask what the success
path DOES — a chain write, an email, a webhook, a payment, an audit row, a notification. If
it commits something, either run it where those effects do not land, or run it knowingly and
**label the artefact so the next reader knows it was a probe.**

**Never skip it** — an unproven negative is still worthless, and that is the whole lesson
above. **Just stop treating it as free.**

### The mirror: an ABSENCE claim needs a positive control too (2026-08-14)

The family above is about checks that cannot report a failure. This is its mirror —
**a search that could not have found the thing, reported as evidence the thing is not
there.**

**The case.** A Secuura session flagged that a claim in its own previous wrap was
false: an entry it said had been written to `BACKLOG.md` was in neither backlog file
nor Linear. It had grepped, found nothing, and disclosed it. **I amended my scoreboard
on the strength of it.** Then it retracted: the entry existed all along, committed on
an unmerged branch, and its grep had run from a tree that forked before that commit.
Its own formulation:

> an artefact-claim needs the same check as any other, and that includes the claim
> that an artefact is **missing** — before reporting "nothing matches", prove the
> search can find something

**Why this is harder than the errors above, and worth its own entry:** diligence was
performed. The agent did search, the search ran cleanly, and the negative was real
*for the tree it ran in*. Nothing errored, nothing was swallowed. The defect was
entirely in the **scope** of the search, which is invisible from inside its result.

**This is the same class as my own w=4 slip the night before**, mirrored: I claimed
something was "absent from every document" without opening the one document that
disproved it. Mine was an absence asserted without looking; theirs was an absence
asserted after looking somewhere that could not have contained it.

**How to apply:**
1. **Every "X does not exist" carries the corpus it was measured against** — the file
   set, the command, the count, and for a repository, **which ref**. `git log --all
   -S` would have settled this in one command; a working-tree grep never could.
2. **Prove the search can find something before trusting that it found nothing** —
   run it against a case you know is present. This is the positive control, applied
   to absence.
3. **Distinguish "I could not find why this still matters" from "here is what
   replaced it."** In a list of closed tickets those look identical and are not the
   same claim.
4. A bulk triage is a pile of negative claims — dozens of "is this still real?"
   judgements, each able to fail exactly this way. That is where this rule earns most.

**The meta-note worth keeping:** the disclosure AND the retraction were both
unprompted, and the churn is left visible in the scoreboard rather than tidied away.
A record that quietly returns to its original wording hides that a correction cycle
happened — and the cycle is the evidence the loop works.
