---
date: 2026-09-10
type: principle
source: Kam adopting Peter's PR verification protocol, panel 2026-09-10 20:27:50 + 20:29:36
status: live
tier: W
---

# A reviewer's protocol is not a checklist we run — it is the acceptance criteria for everything we hand them, and reading it as a to-do list is the failure

**The lesson:** Kam adopted Peter's 624-line PR verification protocol as our process. The obvious
reading is *"here are the steps; run them."* **That reading is wrong and it is expensive.** The
document is written from the REVIEWER's chair — his machine, his checkouts, his slot, his
authorisations. Almost none of its steps are ours to execute. What binds us is the **author side it
assumes**: the state a PR must already be in before his protocol can be run against it at all.

His own document says so three times — *"the gate is the reviewer's APPROVAL plus a Test Evidence
block … filled from LOCAL runs by the author"*, *"the AUTHOR merges, not the reviewer"*, *"ticket and
review must not sit with the same person."* **The obligations are in the assumptions, not in the
numbered steps.**

**Why it matters:** read as a to-do list, it produces an agent burning hours running six suites it
was not asked to run, using authorisations (§2c ticket creation, §2d PR comments) that were granted
to *his* verification run and not to us. Read as acceptance criteria, it produces PRs that pass on
the first look — which is the actual goal, since the reviewer is the scarce resource.

## The general rule

**When a counterparty hands you their process, find the sentence that says what they assume is
already true when they start. That sentence is your contract; the rest is their business.**

The same shape appears wherever two parties meet across a document: a QA gate's brief, a client's
onboarding form, a vendor's security questionnaire. **The obligations that bite are the preconditions,
not the procedure.**

## How to apply

1. **Before adopting any external process, split it in two:** what THEY do, and what must be TRUE
   when they start. Write the second half down as acceptance criteria. Hand only that half to the
   agents.
2. **Never inherit their authorisations.** A pre-authorisation inside someone's protocol is scoped to
   their run of it. Peter's §2c/§2d let *him* create tickets and post one PR comment during *his*
   verification. Adopting the protocol does not transfer that to us. **Check the scope sentence —
   his is explicit: *"Creating and commenting on tickets is pre-authorised ONLY for failures produced
   by a test run during this verification."***
3. **Do not quote their machine-local rules back at anyone.** His §4 says it in terms, and it applies
   to us: their environment specifics are not policy for other developers.
4. **Read the whole thing before acting on any of it.** 624 lines, and the operative constraint for
   us (§10's "would it BITE?" — revert, confirm RED, restore, confirm GREEN) sits two-thirds of the
   way down, after nine sections of their-side procedure. **A skim would have found the procedure and
   missed the contract.**
5. **Check their stated premises against what you have measured.** A protocol is a representation of
   the world at the time it was written. Peter's says *"GitHub Actions is RETIRED, so there is no CI
   to read"*; we measured the same day that Actions is back and its security gates fail on
   essentially every PR. **Correcting a premise is a gift to the author; silently working around it
   is how two teams end up with different models of the same repo.** The correction goes to the
   human via Kam — never agent-to-client.

## Related

[[2026-09-07_a-classification-list-is-a-representation-not-an-instruction]] — the list layer of the
same failure. [[2026-08-16_a-recorded-blocker-is-not-a-boundary]] — a record is a claim, not a rule.
[[2026-09-05_handovers-to-peter-and-stuart-are-test-blocks]] — what Peter wants to receive.
[[2026-08-03_mental-model-not-source-of-truth]] — validate the stored fact before acting on it.
[[2026-09-08_a-safety-claim-names-the-property-it-checked]] — "would it BITE?" is that rule applied
to a test.
