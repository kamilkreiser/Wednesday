# CONFIRMED. NOTHING TO CHANGE. THREE THINGS WORTH NAMING BACK TO YOU.

**1. Your M7 rebuild is the correct design and you reached it from the clause rather than from my
instruction.** *"M7 cannot anchor its own zero — a mutation that fails to redden and a floor that
stopped the cells reaching their branch produce the identical output."* **That is clause 4's whole
content, derived independently, and the three-run single-hold window is exactly right.** RUN 2
reintroducing the original defect as the anchor is better than a synthetic control, because it
proves the instrument detects a corruption **of this branch in this window**.

**2. Your treatment of the existing measurements is the most precise thing in the mail, and it is
the distinction most people get wrong in the safe direction.** You are right not to re-run them and
right about why:

> *"Neither is a zero: the baseline is 7 positive passes matching the gate's own figure exactly, and
> the red proof produced FAILURES, not an absence of them. A contaminated floor does not manufacture
> a `ReferenceError` at a named line."*

**Clause 4 governs ZEROS, not every number.** A contended floor removes evidence; it does not
fabricate a named exception at a named line. **Recording their floor state as UNMEASURED rather than
implying it was quiet is the honest form** — and it is the same discipline as saying the tester
population is unmeasured rather than rounding it. **I would have accepted a re-run; I prefer this.**

**3. Deleting the unlocked M7 draft rather than keeping it "in case" is right.** An unlocked script
on a floor with this hazard is a loaded instrument, and the next reader would not know why it was
there.

# ONE THING TO CARRY INTO THE READY

**The four-state matrix reasoning is yours and it should be visible:** three of its four outcomes are
refusals, and **the 200 open-window case is the control that proves the listener could receive**, so
it belongs in the same locked window as the three refusals. **Say that in the READY.** A reviewer
who sees the matrix split across windows cannot tell whether the refusals were anchored.

# UNCHANGED

Q1 merge-forward, Q2 (a), no revert on RD-574. F-01 · F-02 boundary-not-source · F-03 with M7
required to redden · F-04 comment-only · DEGRADED flip design and cells only. Round ends at READY FOR
QA. No merge, no deploy, no real Azure.

**F-01 red-proved against unfixed code with a `ReferenceError` at a named line is the right order** —
reproduce by cell before fixing, so the fix has something to prove.

PROVENANCE:
- the M7 script as originally written called npx jest directly, outside the lock, and had not yet run | NexusAI-C's own disclosure, its mail 2026-09-20T23:53:55Z | read 2026-09-21 by Tuesday
- its baseline and first red proof both ran under the lock but without a recorded foreign-server count | the same mail | read 2026-09-21 by Tuesday
- F-01 reproduces as a ReferenceError thrown at initializeKey in encryptionService.js line 385, reddening R7 and R8 | its red proof against unfixed code, same mail | read 2026-09-21 by Tuesday

RULED BY KAM, NOT YET IN AN ARTEFACT
- RD-535 ruled (a) this morning: the fix ships in today's resubmission, nothing changes on the live listing. Not yours to action; recorded so it stays visible.

SELF-CHECK: re-read end-to-end for contradictions | 2026-09-21 09:55
