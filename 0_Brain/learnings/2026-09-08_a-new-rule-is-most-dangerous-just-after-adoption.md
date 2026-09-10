---
date: 2026-09-08
type: principle
source: the Secuura/Blockchain seat (s151), after its retraction caught a rule Wednesday had shipped into the brief path ten minutes earlier
status: live
tier: W
---

# A new rule is at its most dangerous immediately AFTER it is adopted — one worked example, a persuaded author, and nobody has met its exception yet

**The operative case, so the headline matches it:** you have just written a rule from something that
happened today, and you are about to put it somewhere that binds — the brief path, a standing line,
a launcher, `CLAUDE.md`. **Stop. Ask what its exception looks like, and whether anyone has met one.**
A rule is never more confident, never better argued, and never less tested than in the hour it is
adopted.

## The case, measured, and it took ten minutes

The Secuura seat reported a mechanism: its push had been orphaned by a nested `&` and killed at leg 2
while the harness reported exit 0. **Wednesday shipped it into `fleet/specs/brief-standing-lines.md`
within ten minutes**, as standing rule *"never nest backgrounding"*, with the seat's mechanism as its
justification — so every future brief in the fleet would have carried it.

**Fourteen minutes later the seat retracted: the push had never failed. It was IN FLIGHT.** A 14-leg
preflight takes ~4 minutes and the ref only moves at the very end, so a short log and an unmoved
remote ref are exactly what a *healthy* push looks like at minute three. Its own words: *"I invented
a mechanism to explain an outcome I had misread."*

**And the rule Wednesday had shipped in the same breath — *"read the destination, not the exit
code"* — is what CAUSED the seat's error.** It is complete about one failure direction (a green
trusted too readily) and silent about the other (a healthy operation declared dead because its
destination has not changed *yet*). **The rule produced its own opposite failure within ten minutes
of being written, by the person it then caught out.**

## The seat's formulation, adopted verbatim

> *"A new rule is at its most dangerous immediately after it is adopted, because it has a single
> worked example behind it, its author is persuaded, and nobody has met its exception yet. **Ours got
> its exception in ten minutes. Most will not be so lucky.**"*

And on how it got through: *"Nothing in that path required it to be true — **it only required it to
be well-told. My account was well-told. That is what made it dangerous.**"*

## Why this is its own lesson and not go-slow rule 4 restated

[[2026-08-03_go-slow-earn-autonomy]] rule 4 says a new mechanism pilots before it stands. **It says
what to do and not why the failure is structural.** Three properties coincide only at adoption:

1. **Exactly one worked example**, and the rule was reverse-engineered from it — so it fits that case
   perfectly and has never been asked about another.
2. **The author is maximally persuaded**, having just done the reasoning. A rule you argued yesterday
   is easier to doubt than one you argued ten minutes ago.
3. **No exception has been met**, so the rule looks complete. **Completeness and untestedness are
   indistinguishable from the inside**, which is the same shape as
   [[2026-08-07_a-check-that-cannot-fail]] pointed at a rule instead of a check.

**A rule built against ONE failure direction is not neutral about the other — it actively recommends
the opposite mistake.** That is the transferable half.

## How to apply

1. **Before a rule enters a binding path, write its EXCEPTION** — the case where following it gives
   the wrong answer. If you cannot construct one, you do not yet understand the rule's scope; say so
   in the line itself rather than omitting it.
2. **A mechanism reported by one party, once, is a HYPOTHESIS.** It may go in a ledger row the same
   day. **It does not enter the brief path until something verifies it or it recurs.** (Wednesday's
   own [[2026-08-03_frequency-weighted-reinforcement]]: w=1 is *could be noise*.)
3. **Every standing line carries its evidence basis** — how many instances, verified by what, or the
   honest `SINGLE UNVERIFIED INSTANCE — pilot only`. **A path that accepts a well-told line is a path
   with no gate**, and prose quality is not evidence.
4. **State the direction a rule was built against.** *"Built from a green trusted too readily; says
   nothing about a slow operation mid-flight"* is one clause, and it is the clause that would have
   prevented this.
5. **Treat the first exception as a dividend, not an embarrassment.** Ours arrived in ten minutes and
   cost nothing because the seat retracted unprompted. **The rules to fear are the ones whose
   exception arrives in three months, to someone who was not there.**

**Family:** [[2026-08-03_go-slow-earn-autonomy]] (rule 4 — this is its mechanism) ·
[[2026-09-01_qa-gate-before-my-verification]] (SHARPENED 09-04: a mechanism claim goes to the gate,
not to ratification — the rule broken here) · [[2026-08-09_an-enforcement-you-must-arm-is-not-one]]
(the brief path IS enforcement, so writing to it is arming something) ·
[[2026-08-14_i-read-representations-they-read-sources]] (the SHARPENING: a compression propagates with
perfect fidelity — so does a well-told wrong rule) · [[2026-08-07_a-check-that-cannot-fail]].

## EXTENSION 2026-09-10 — the FILE-level twin: a just-REPAIRED file is least defended, and repairing it is what makes you fast enough to break it

**Tuesday's formulation, adopted (she named the twin; I had written only the instance):** *"Same
clock, different object: a rule is least tested in the hour it is adopted; a file is least defended
in the hours after it is repaired, because the repair consumes the attention that would have noticed
the next change."*

**The case, and it is mine.** `wake_watch.sh` had two agent-blind defects — a hardcoded inbox and a
hardcoded pane name — remediated the same morning under Kam's `parameterise` ruling (`a66e3793`,
card marked **delivered**). **Four hours later I proposed a fix for that same file whose gate read
`~/.claude/projects/…` — a third hardcoded, seat-specific location.** It would have re-introduced the
closed family into the file that had just been cleaned, past a card whose whole purpose was to catch
exactly that and which had already been told the job was done.

**The compounding part, which is the reason this is not just "be careful":** I was the author of the
fix, in a file I had read, hours earlier. **Being the person who repaired it is not protection — it
is what makes you confident enough to change it quickly.** The card being marked delivered is not
protection either; it is the mechanism standing down.

**How to apply:** before changing a file that was repaired in the last day, **read what the repair
CHANGED, not what the file now says** — the constraint the fix introduced is invisible in the final
text, and a delivered card is evidence the guard has stopped looking. Standing line for every builder
brief: `2_Project_Files/fleet/STANDING_LINES.md`.
