---
date: 2026-09-06
type: correction
source: Kam's 20:19 instruction to boot on Opus for the week, read against the 2026-09-04 hand-pin that outlived its reason
status: live
tier: W
---

# A time-scoped instruction gets a mechanism that EXPIRES it — an override with no end date is a permanent change nobody decided to make

**The operative case, so the headline matches it:** Kam gives an instruction with a
window in it — *"for the rest of the week"*, *"until the credits come back"*,
*"while X is running"*, *"just for today"*. **Wednesday is about to apply it.
Before the edit lands, decide what ENDS it, and build that ending into a check
that fires on its own.** A scoped instruction applied without an expiry becomes a
standing one the moment the seat that heard it rotates.

**The case (tonight, 2026-09-06 20:19, verbatim):** *"please change your boot
script for the rest of the week to boot in opus 5 rather than fable. we are
burning through credits a little too quickly."* The launcher's exec line moved to
`--model opus`, the fable line kept commented beside it, a `.pre-0906-opus`
backup made — and, because of what happened two days ago, `doctor.sh` now holds
the date: it reports the pin as the WANTED state until 2026-09-13 and WARNS after
it. Both branches exercised before arming (the pass branch on the live file, the
warn branch on a scratch copy with the date moved into the past).

**Why this is its own lesson and not just a launcher edit.** On 2026-09-04 at
21:15 the same thing happened without the ending: Fable credits ran out, the
launcher was hand-pinned to `--model opus`, and that pin silently kept every
later seat on Opus after the credits came back — until the 2026-09-05 13:09 seat
booted on Opus with Fable reachable and Kam had to say so. The instruction was
correct and temporary; the artefact was correct and permanent. **Nothing was
wrong with the edit. What was missing was its end.**

**How to apply:**
1. **Read the scope word as part of the instruction, not as flavour.** "For the
   week", "for now", "while we are tight" are operative clauses. Write the end
   date down in the artefact itself, in Kam's own words, with the date derived
   and STATED as an assumption ("read as through Sunday 2026-09-13 — the 7-day
   usage window renews then; your word moves it").
2. **The expiry is a CHECK, never a note.** A comment expires nothing; a diary
   entry expires nothing; a successor brief expires nothing once the brief is
   two rotations old. The check goes where the thing is read at every boot —
   `doctor.sh` here — and it must WARN on the day after, unprompted.
   ([[2026-08-09_an-enforcement-you-must-arm-is-not-one]]: a rule you have to
   remember to un-apply is not a rule.)
3. **Exercise both branches before arming** — the state that should pass and the
   state that should warn, with the clock moved rather than waited for
   ([[2026-08-06_exercise-mechanisms-before-arming]],
   [[2026-08-07_a-check-that-cannot-fail]]).
4. **Keep the revert one line away and say where it is** — the superseded line
   commented in place, plus a dated `.pre-` backup beside the file
   ([[2026-08-26_never-delete-cleanup-means-quarantine]]).
5. **Tell Kam the assumption in the same breath as the receipt.** He set a window
   in ordinary words; the date is my reading of it, and a reading he can correct
   in three seconds beats a pin he discovers in a fortnight.

**Family:** [[2026-08-09_an-enforcement-you-must-arm-is-not-one]] ·
[[2026-08-07_a-promise-is-not-a-mechanism]] (an intention to revert is not a
revert) · [[2026-08-16_a-recorded-blocker-is-not-a-boundary]] (a recorded
condition is a claim with a date — this is its mirror: a recorded PERMISSION is a
claim with an end) · [[2026-08-06_exercise-mechanisms-before-arming]] ·
[[2026-09-05_root-folder-holds-only-rules-and-launchers]] (the doctor as the
place enforcement lives).
