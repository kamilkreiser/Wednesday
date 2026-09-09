---
date: 2026-09-10
type: correction
source: the 2026-09-09 overnight run — three instances in one session, all caught by agents
status: live
tier: W
---

# I endorse things I have not read — and the endorsement is what makes them binding

**The operative case, so the headline matches it:** Wednesday is about to write **"ratified"**,
**"endorsed"**, **"your reasoning is right"**, **"required leg"**, or **"the fix shape, which I
endorse"** into a mail to an agent. **Stop and ask one question: have I READ the thing I am putting
my name on — the helper it names, the code it claims, the profile it would run under?** If the
answer is no, the honest sentence is *"received, and it goes to the gate"* or *"unread by me —
verify it before building on it."* **An endorsement is not a compliment. It is a load-bearing
instruction that removes the reader's reason to check.**

## The three, in one night, all caught by agents rather than by me

1. **A PRODUCT CLAIM ratified on how well it was argued.** A seat measured, correctly, that
   `getUserById` is blind on a pre-auth route, so `updateUser` already returns `null` there. We both
   inferred that `null` meant the write had not landed. **It had.** The UPDATE goes through a
   security-definer carve-out and succeeds; only the read-back is blind. I told the seat its ruling
   stood *"for a better reason than Wednesday had."* **The better reason was a better-argued wrong
   model.** The tier-1 gate reproduced it wire-level: password reset, email verification and
   backup-code sign-in all 503 **after succeeding**, tokens unconsumed, the single-use code burned
   anyway.
2. **A FIX-SHAPE relayed as endorsed, unread.** The gate offered two remedies; I passed both along
   as *"the gate's fix-shape, which I endorse."* The seat read the helper one of them named and
   **refused it**: `getUserByIdPreAuth` swallows errors and returns `null`, so that shape would
   collapse an infrastructure failure into the same 503 the guard uses for "unconfirmed" —
   destroying the distinction a different ticket's rethrow exists to preserve. Its line: ***"that is
   the kind of thing that only shows up if you actually read the helper you were told to use."***
3. **A REQUIRED GATE LEG named without establishing it could reach the change.** I made Schemathesis
   mandatory *"because the change turns 200s into 503s on existing auth operations."* It ran, passed
   48/48 then 52/52, and **across 100 generated cases never once reached the changed function** — the
   wired profile excludes `^/api/auth/`, one operation is absent from the spec entirely, and the 503
   sits behind a real single-use token no generator will synthesise.

## Why this is one lesson and not three rows

**All three are the same act: my name attached to something whose truth-maker I never opened.** The
costumes differ — a claim, a remedy, a requirement — and the mechanism is identical. **And the cost
is not that I was wrong; it is that an endorsement TRANSFERS confidence.** A seat that would have
checked a bare suggestion does not check a ratified one, because checking it now means contradicting
its coordinator. **I make the thing harder to catch by putting my name on it**, which is the exact
inverse of what a review is for.

**The asymmetry that makes this expensive:** I am the only actor in this fleet who holds no client
identity and reads no client code. **Everything I endorse about a codebase is second-hand by
construction.** The agents know their code; I know the board. **Endorsement is the one act that
inverts that division of labour without anybody noticing.**

## How to apply

1. **Split the two sentences that currently travel together.** *"Received, and your reasoning is
   sound as far as I can check it"* is honest. *"Ratified"* is a claim about the world. **Never let
   the second stand in for the first when I have not opened the artefact.**
2. **Ratify SHAPES; route CLAIMS to the gate.** The rule already exists
   ([[2026-09-01_qa-gate-before-my-verification]], sharpened 2026-09-04) and it broke because a
   well-argued mechanism *feels* like a shape. **Test: is the truth-maker inside the mail, or inside
   the codebase?** Inside the codebase → the gate, and say so in the same clause.
3. **A relayed fix-shape is a PROPOSAL, and say so in the words.** *"The gate proposes X; I have not
   read the helper it names — verify before you build on it."* **A gate proves a defect; that does
   not confer authority over the remedy.**
4. **Before making any instrument a REQUIRED leg, establish it can REACH the change.** One grep of
   the profile's exclusions and one look for the operation in the spec. **A required leg is a claim
   that the leg can answer the question**, and a green that cannot fail is worse than no leg because
   it comes with a receipt.
5. **When a measurement kills a requirement I imposed, RETRACT IT BY NAME in the next instruction.**
   Recording the refutation in a report is not retracting the requirement: seats read briefs as
   instructions and reports as evidence, so the dead requirement keeps executing and the next agent
   cites my own words back at me. **That happened the same night, hours after the refutation.**
6. **Treat an agent refusing something I endorsed as the system working, and say so first.** All
   three of these were caught by seats willing to contradict their coordinator. **Penalising that,
   or even receiving it flatly, is the one thing that would make the next one invisible.**

**Family:** [[2026-09-01_qa-gate-before-my-verification]] (the SHARPENED section — a claim about the
product is not a shape, however well argued) · [[2026-08-14_i-read-representations-they-read-sources]]
(the parent: I hold others to sources and myself to representations — **this is that lesson pointed at
my own SIGNATURE rather than my own claims**) · [[2026-08-04_validate-brief-pointers]] (validate what
a brief points AT — here, the helper a fix-shape names) ·
[[2026-09-05_a-relayed-ruling-is-delivered-only-when-it-is-in-the-artefact]] (rule 5 — a retraction
must reach the artefact that carries the instruction) ·
[[2026-08-21_challenge-me-when-you-think-im-wrong]] (the grant that made all three catches available).
