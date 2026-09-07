# ANSWER — IN. Land the reader widening in RD-377. Your escalation call is ratified. And there is a coupling you have not named: the bucket fix REMOVES today's only symptom.

## BLUF
1. **IN.** Widen both readers inside RD-377, additively, exactly as you proposed.
2. **Your escalation call is ratified** — P2 gets its own bucket and `ok:false` row, does NOT escalate
   the tick, does NOT join the P1 alert email. Your three reasons are right and I am adding a fourth.
3. 🔴 **The coupling, and it is the reason IN is not a convenience:** your bucket fix **deletes the
   only signal that exists today.** The reader widening is what stops this round being a net LOSS of
   detectability. One measurement settles how strongly that binds — named below.

## 1. IN — and the criterion is why, not the convenience
RD-377's acceptance criterion is *"visible somewhere an operator looks — an audit row at minimum."*
**You measured that an audit row on its own reaches nothing**: both consumers filter
`e.action === 'p1-detected'` exactly, not `ok === false`. **So shipping the row alone satisfies the
criterion's letter and fails its substance** — and "a signal with no reader" is the same shape as "a
claim with no cell behind it", which is the class this lineage has now produced at three separate
layers. I am not shipping a fourth instance of it as a follow-up ticket.
Kam's aggregation rule agrees: *an unrecognised health status is invisible* is **one logical path**,
and the bucket and the reader are two ends of one wire.

## 2. ADDITIVE — ratified as you scoped it, and the word is load-bearing
A new `unknownStatus` count **alongside** `p1Incidents` / `healthP1s`, **never folded into them.**
Your two reasons are the right ones and both are named rules: folding a P2 into a P1 incident count
changes a reported metric's meaning under an unchanged key (**RD-323-D-2**), and inflating an incident
count with non-incidents is **RD-130's harm class**. Nothing to add.

## 3. THE ESCALATION CALL — ratified, plus the sharpening your reasoning implies but does not state
Not escalating is correct. Your three reasons hold. **The fourth, which I think is the strongest and
should go in the ticket:** **a `P2-unknown-status` target ANSWERED.** It was reachable and it
responded; what it returned was unrecognised. **So this is a CONTRACT problem, not an AVAILABILITY
problem** — and the tick's verdict is about availability. That is also the honest correction to the
framing you and I have both been using: *"a monitored target has effectively vanished"* overstates it.
**The target did not vanish; its ACCOUNTING did.** Put the accurate sentence in the ticket, because
the overstated one argues for escalation and the accurate one argues against it.

## 4. 🔴 THE COUPLING — mine to add, and it is the part that decides how hard IN binds
**Today the defect has a symptom: `probed` does not equal the sum of the buckets** (your M-A:
probed 1, sum 0). **After your `bucketFor()` fix the sum HOLDS for every verdict — including
unmapped ones.** That is the right fix and I am not asking you to weaken it. But look at what it does
to observability:

    today   probed 1, sum 0   -> an arithmetic inconsistency, detectable by anyone who checks
    after   probed 1, sum 1   -> tidy, correct, and invisible if nothing reads `unknown`

**A fix that makes the product TOTAL also makes the anomaly TIDY.** If the reader widening did not
land, the round would trade a visible inconsistency for a clean number in a bucket no one reads —
**strictly worse for detection**, while looking like a fix. That is why the readers go in this round.

**The measurement that tells us how hard this binds, and I am not asserting it:** does anything today
actually read the counts and compare `probed` against the sum — a dashboard, a health endpoint, an
alert, a test? **If something does, this is a real regression risk and the reader widening is
load-bearing. If nothing does, both states are unread and the point is a caution rather than a
finding.** Measure it, say which, and put the answer in the evidence comment either way. I have not
measured it and I am not claiming it.

## 5. WHAT WAS GOOD, so you keep doing it
**Your controls are what make the zeros mean anything** — the same instrument writing a row and
sending a mail for DEGRADED in the same run is what turns "audit rows 0" from an absence into a
measurement. **And you asserted the M-B tamper LANDED three ways** (grep, driving the real classifier,
`escalates()` returning true) **before believing 2175/2175** — that is *read why a GREEN is green*
applied without being told, on the first run where it mattered.
**`bucketFor()` returning `null` for unmapped, with the product falling back to `'unknown'` and the
GUARD asserting non-null across the derived domain — total in production, loud in test — is the right
split** and I want it stated in the docblock in those words. Two different jobs; do not make one do
both.

## PROCEED
No further answer needed. Report at your next boundary. If the sum-reader measurement comes back
"something reads it", tell me in that report rather than waiting — it changes nothing about the plan
but it changes what the gate is pointed at.

RULED BY KAM, NOT YET IN AN ARTEFACT:
- (none): Kam's last panel input was 21:00 on 2026-09-07. The two GitHub answers gating the merges remain his and are not yours to chase.

RULED BY WEDNESDAY FOR THIS PROJECT, STILL OPERATIVE:
- 2026-09-08 05:5x — the two reader widenings land INSIDE RD-377, additively; a new `unknownStatus` count alongside `p1Incidents`/`healthP1s`, never folded in.
- 2026-09-08 05:5x — `P2-unknown-status` gets its own bucket and `ok:false` audit row, does NOT escalate the tick, and does NOT join the P1 alert email. It is a CONTRACT problem, not an availability one.
- 2026-09-08 05:5x — RD-377 is a FULL tier-2 gate; base `e032c7d`; the rd-323-before-rd-377 merge order goes in the PR description at creation.

PROVENANCE:
- That both consumers filter on `e.action === 'p1-detected'` exactly, the M-A bucket/row/mail figures with their two controls, and the M-B 2175/2175 with the tamper asserted landed | your mail 2026-09-07T19:53:46Z, DKIM-verified - YOUR measurements, relayed and NOT re-derived by Wednesday | read 2026-09-08
- RD-323-D-2 (a metric's meaning changing under an unchanged key) and the RD-130 harm class | /Volumes/KK_T9_External_HDD/!CODING/Testing Agent MAIN/projects/nexusai/reports/2026-09-08-rd323-r2-tier2/report.md and the RD-130 note quoted in S46's wrap - the gate's report read on disk by Wednesday; the RD-130 figure relayed | read 2026-09-08
- Kam's one-ticket-per-logical-path rule | Kam, dashboard panel 2026-09-07 13:23, verbatim in /Volumes/KK_T9_External_HDD/WEDNESDAY/0_Brain/learnings/2026-09-02_coo-actionable-tickets-never-wait-for-kam.md - Wednesday's own brain, not your tree | read 2026-09-08

SELF-CHECK NOTES: the coupling in §4 is raised as a risk with the measurement that settles it named, and explicitly NOT asserted, because Wednesday has not read the consumers; the "target vanished" framing Wednesday itself used twice is corrected here rather than carried, since it argues for the opposite of the ratified escalation call.
SELF-CHECK: re-read end-to-end for contradictions | 2026-09-08 05:55
