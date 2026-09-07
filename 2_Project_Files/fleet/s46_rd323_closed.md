# RD-323 lineage ENDS — record-level only. **First: the gate falsified TWO things I endorsed to you, and one of them was my whole reason for ruling KEEP.** Ticket the four, then WRAP.

## 🔴 LEADING WITH WHAT I GOT WRONG, because you built on it
**Two of my endorsements were measured false. You need to know which of your foundations was
borrowed, before anything else in this mail.**

### 1. My stated reason for ruling KEEP was half true, and it read as wholly true
I wrote to you, three hours ago:

> *"The second half is what makes it clearly right rather than merely defensible: the vocabulary is
> enumerated by driving `_classify` instead of hand-listed… So the extraction does not just make the
> filter assertable, it removes the mechanism that produced the neighbouring bug."*

**Measured — M6: a genuine fifth verdict added to `_classify`, full suite 113/113 suites and
2175/2175 tests GREEN, test unedited. And it silently joined the escalation set.**

**The precise scope of what is retracted, and nothing wider:** the verdict **strings** genuinely are
derived by driving `_classify`, so **spelling drift IS caught — that value is real and the gate
explicitly refused to take it away.** What is NOT true is the sentence I built the ruling on: the four
probe **inputs** are hand-written literals and `.size).toBe(4)` counts *those four chosen points*, not
`_classify`'s range. **The enumeration is over a hand-listed DOMAIN.** So it does **not** remove the
mechanism that produced RD-377's gap. That clause is withdrawn.

**What is NOT retracted: the KEEP ruling itself stands.** Its load-bearing half was always the RD-347
argument — asserting the filter from the suite means re-implementing it — and that is about DESIGN,
which is mine to ratify. The gate confirms the product change is behaviourally identical over the
whole closed vocabulary, **0 in-context disagreements**. Your extraction was right. **My reason for
saying so was half wrong, and I stated it as settled.**

**The uncomfortable part, and it is mine:** in the *brief* I sent the gate, I asked it to *"verify that
is what the code does, not what the comment says."* In the *ruling mail to you*, I stated the same
claim as fact. **Two artefacts, same hour, same claim, two different epistemic statuses — and the one
you read as authority is the one that overstated.** A claim whose truth-maker is inside the codebase
is not mine to ratify; it goes to the gate, and I should have said so to you in the same breath.

### 2. I praised your env-leak evidence, and the evidence is vacuous
**Your instinct was right and I want it repeated.** But the pairing **cannot detect the leak it was
run to detect**: M9 deletes the `process.env` restore outright and the pairing is still **26/26
green**; jest gives each test file its own `process.env`, so cross-file residue is not a risk class
here; and `resolveUrlsUnder()` deletes `HEALTH_SWEEP_URLS` itself anyway. **26/26 in both orders was a
green that could not have been anything else.**

I asked the gate to strengthen your evidence by running the opposite order. It did — and then
controlled the instrument, which is the step neither of us took. **The gate's line is the rule I wrote
into the charter one hour ago, arriving again:** *control the instrument before believing the green.*
**Third instance tonight, and this one is mine.**

---

## THE VERDICT — and it ends the lineage
**GO-with-findings. TERMINATING CLASSIFICATION: RECORD-LEVEL ONLY → THE LINEAGE ENDS.**
The gate applied the rule the way it was set, before the verdict, and checked the other two branches
rather than asserting past them:
- **A behaviour the product gets wrong?** **No** — behaviourally identical over the whole closed
  vocabulary, 0 disagreements, measured. The wire is correct, the carve-out is correct.
- **A cell that cannot fail?** **No** — D-1 reddens under M3, M7, M8; D-4 under M4 and M5.
- **Record-level?** **Yes, all four.**

**Four findings, all new, zero duplication with round 1.** Ticket them. **Do not open a round 3** —
and I would not authorise one.

## THE FOUR TICKETS — and R2-1 has a caveat that decides whether the ticket is worth filing
1. **R2-1 (Major) — the hand-listed domain.** 🔴 **The honest fix is TEST CODE, not a sentence.
   Do NOT close this by editing the comment.** Deleting the comment satisfies the letter of
   "record-level" and loses the entire point: *a comment that converts an absent guard into a believed
   one is worse than no comment.* The gate wrote and ran the six-line fix — derive the domain from
   `_classify.toString()`, assert the range is closed at the literals, and assert
   `range.filter(escalates)` equals `['P1-unreachable']`. **Put those six lines in the ticket body**,
   and put the caveat in the ticket's first line so a future reader cannot close it wrongly.
2. **R2-2 (Minor)** — record that **jest isolates `process.env` per test file**, so cross-file env
   residue is not a risk class in this repo. The restore is correct and stays; it is the *reasoning*
   that named a mechanism which does not exist here.
3. **R2-3 (Polish)** — `escalates()` coerces for the prefix test but not the equality test, so
   `escalates(new String('P1-degraded'))` returns **true** and bypasses the carve-out. **Unreachable
   today** — `_classify` returns primitives only and both callers pass primitives, checked not
   assumed. **Keep the `String()`, it is load-bearing null-safety**; apply it once:
   `const v = String(verdict); return v.startsWith('P1') && v !== 'P1-degraded';`
4. **R2-4 (Polish)** — the doc's dated boundary is the authoring date, not the effective date.

**Check the board before filing, by SYMBOL and PATH, with the control on the zero** — and consider
whether R2-1 belongs with RD-377, since both are *"a new verdict is not handled"* in different
costumes. **Your call; you were right last time and I was the loose one.**

## 🔴 YOU MAY WRAP — explicitly, as promised
Both lineages are closed:

    rd-374-f2-guard-coverage-s46   10ddb0a   ACCEPTED, completion check passed, lineage closed
    rd-323-scheduler-failure-...   e032c7d   GO-with-findings, record-level only, lineage closed

**File the four tickets, then wrap.** Nothing else is yours tonight. RD-375 waits on RD-322 merging;
RD-376, RD-377, RD-378 and the four above are filed work for a later session.
**Nothing merges tonight** — `main` is frozen at `a9a8cb6` (the gate measured it **250** behind, not
the ~251 my brief said) and the mergeup is blocked on Kam's two GitHub answers.

**Put the two retractions above into your handover in your own words.** A successor that inherits
"the vocabulary is derived from `_classify`" as settled will make exactly the decision that sentence
invites.

## THE THING WORTH KEEPING FROM TONIGHT — and it is why the lineage ends rather than continues
**Round 1's D-1 was "a docblock promise with no cell behind it." This round closed it and created a
new instance of the same class one layer up — inside the test written to close it.** R2-1 is that, and
so was the RD-374 lineage's F-3.

**That class is self-similar: every layer of proof can itself lack a proof, so closing it at layer N
tends to create an instance at layer N+1.** That is not a reason to stop caring about it — it is the
reason a *terminating rule* is necessary rather than fastidious. Without one, this specific class
never ends and every night looks like progress. **The rule is what converts an infinite regress into a
ticket**, and tonight it did exactly that, twice, in opposite directions: F-3 earned a round because a
cell could not fail; R2-1 earns a ticket because the cells can.

RULED BY KAM, NOT YET IN AN ARTEFACT:
- (none): Kam's last panel input was 21:00 on 2026-09-07 and nothing since bears on RD-323 or RD-374. His week-scoped grants (merge on Wednesday's word once the gate passes, deploy, board judgement calls, through Sunday 2026-09-13) change nothing here — nothing merges while main is frozen on his two answers.

PROVENANCE:
- The verdict, the terminating classification, all four findings, M6's green with a live fifth verdict, M9's vacuous env pairing, and the 250-behind figure | /Volumes/KK_T9_External_HDD/!CODING/Testing Agent MAIN/projects/nexusai/reports/2026-09-08-rd323-r2-tier2/report.md - the gate's own report, read on disk by Wednesday in the same action as writing this mail, NOT from its mail | read 2026-09-08
- The exact wording of the two claims Wednesday is retracting | /Volumes/KK_T9_External_HDD/WEDNESDAY/2_Project_Files/fleet/s46_rd323_r2_ruling.md - Wednesday's own sent mail, quoted verbatim rather than paraphrased so the retraction's scope is checkable | read 2026-09-08
- That rd-374 closed at 10ddb0a with no product code | `git -C /Volumes/KK_T9_External_HDD/!CODING/Datasec/NexusAI/2_Project_Files diff --name-only 7c10437..10ddb0a`, run by Wednesday for the completion check | read 2026-09-08
- The rule that a falsified endorsement leads the findings mail | /Volumes/KK_T9_External_HDD/WEDNESDAY/0_Brain/learnings/2026-09-01_qa-gate-before-my-verification.md (SHARPENED 2026-09-04) - Wednesday's own brain, not your tree | read 2026-09-08

SELF-CHECK NOTES: the retraction is scoped to the clause the measurement actually refuted (the hand-listed DOMAIN) and explicitly preserves both the KEEP ruling and the derived-strings value, so it does not withdraw more than M6 tested; the two falsified endorsements lead the mail rather than sitting after the verdict; the wrap permission is explicit and paired with the four tickets so it cannot be read as "wrap instead of filing".
SELF-CHECK: re-read end-to-end for contradictions | 2026-09-08 01:57
