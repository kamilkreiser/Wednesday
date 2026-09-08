---
date: 2026-09-08
type: correction
source: named by the Secuura seat s150, from three unrelated instances in one day
status: live
tier: M
---

# "The check ran, and it was not checking the thing" — a green from a check aimed at the wrong property is worse than no check, because it comes with a receipt

**The operative case, so the headline matches it:** a gate, a test, a control or a guard has just
returned GREEN, and you are about to treat that green as evidence. **Ask one question before you
do: what property did it actually test, and is that the property the claim needs?** A check that
is ABSENT announces itself the moment anyone looks. A check that runs and measures the wrong
thing is silent, confident, and hands you a receipt for a claim nobody verified.

**Named by the Secuura seat (s150) on 2026-09-08 after three instances on three unrelated
surfaces in a single day.** Its formulation, adopted verbatim as the headline.

## The three, and they share nothing but the shape

1. **`format:check` on `systemTest/akto`.** Six formatting instances reached the trunk. The
   package's own quality gate existed and passed on every push — **because nothing ran it on the
   files being pushed.** The check was real, configured and green.
2. **Wednesday's own tap gate.** The rule is that a tap into an agent's pane carries only a
   POINTER; content goes by mail the agent can verify. The enforcement built that morning
   required `--mail <subject>` and **verified that a mail with that subject EXISTED at the
   destination.** The claim needed **correspondence** — that the cited mail CARRIES what the tap
   says. Wednesday tapped a pane id, a launch time and a card claim while citing an ANSWER sent
   33 minutes earlier that held none of them. **The gate went green.** It cannot fail for any tap
   citing any real prior mail, which makes it very nearly a check that cannot fail — built in
   direct response to the very family it failed on.
3. **`getUserById` (KS-963).** It catches a decryption/policy error and returns `null`. The
   caller's check — *is there a row?* — runs correctly and answers "no". **The question it needed
   answered was "did the lookup succeed?"** Its sibling ten lines away rethrows, after a real
   incident where 42 of 266 users were told "Invalid email or password" with valid credentials.

## Why this is its own lesson and not a restatement of "a check that cannot fail"

[[2026-08-07_a-check-that-cannot-fail]] is about a check whose result was never in doubt — a
tautology. **This one is about a check that genuinely CAN fail, and does fail, on a different
question than the one being asked.** It has real discriminating power, pointed slightly to the
left of the claim. That is why it survives review: the evidence is authentic, the instrument
works, and the green is earned — just not by the thing you are about to assert.

**The tell is a green arriving on the FIRST attempt at something that has bitten before.** The
tap gate went green on a tap that broke its own rule. `format:check` went green on six reds.

## How to apply

1. **Say the property out loud before accepting a green.** Not *"the gate passed"* but *"the gate
   proved the cited mail EXISTS"* — and then ask whether existence is what the claim rests on. The
   sentence is usually enough; the gap is obvious once it is spoken.
2. **Build the check against the FAILURE you are trying to prevent, not against the artefact in
   front of you.** The tap gate was built from *"a tap had no mail"* and so tested for a mail. The
   failure was *"a tap carried claims nothing supported"*, which is about correspondence — and
   the closest cheap proxy is FRESHNESS, since the rule was always "a mail sent in the same
   action". That is what it tests now.
3. **A green on the first attempt at a recurring failure is a prompt to re-read the check**, not a
   reason to relax. Recurrence means the last fix aimed somewhere; ask where.
4. **When a control returns the answer you wanted, plant a violation.** The 2026-09-08 QA gate on
   #906 is the template: its control SHA came back green, so it planted a formatting violation at
   that same SHA to prove the instrument fires, restored byte-identical, and only then called the
   zero real. **A zero from an instrument that could not fire is not a zero.**
5. **In code, the two questions to keep apart are "is there a result?" and "did the operation
   succeed?"** Collapsing a failure into an empty result is this lesson in a `catch` block, and it
   is the single most common form.

**Family:** [[2026-08-07_a-check-that-cannot-fail]] (the tautology half — this is the
wrong-question half) · [[2026-09-08_a-false-absence-is-usually-my-own-instrument]] (a zero whose
instrument was never shown to fire) · [[2026-09-07_a-census-complete-over-a-frame-that-is-not]]
(right answer, wrong frame) · [[2026-08-09_an-enforcement-you-must-arm-is-not-one]] ·
[[2026-09-01_a-tap-is-a-pointer-not-a-message]] (instance 2 lives there as the w=6 row).
