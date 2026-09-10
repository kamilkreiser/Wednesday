---
date: 2026-09-10
type: preference
source: Kam, dashboard panel 12:06:32
status: live
tier: W
---

# Coordinate with Tuesday BEFORE taking a task — two coordinators on shared tooling will both fix the same thing unless one of them claims it first

**His words, verbatim (2026-09-10 12:06:32):**
> *"When you take a task, always make sure you coordinate with Tuesday so we don't have
> overlap between multiple agents working on the same thing."*

**He said this the same morning it actually happened**, which is why it is a rule and not a
platitude.

## The case it comes out of

Kam's chat panel was misbehaving. **Tuesday and I both diagnosed it, independently, in
parallel, and produced three wrong answers between us** before anyone got it right:

1. Tuesday: it is `/chat`'s project filter. (He uses the cockpit, which had no such filter.)
2. Tuesday: it is arrival latency. (He had already said some messages arrive and one does not.)
3. **Me: "that one is not the panel"** — Tuesday simply had not posted since 11:29.

All three fitted **one sentence** of what he said and not the whole of it. Tuesday then read
his screenshot properly and found the real cause in **my** file. Two coordinators, one
problem, three wrong answers, and no one had claimed it.

## The rule

**Before starting anything that is not unambiguously mine alone, say so — and check whether
she is already on it.** A one-line mail costs seconds; two agents rebuilding the same
mechanism costs a morning, and worse, produces two confident contradictory answers to the
principal.

**"Not unambiguously mine alone" is broader than it sounds.** It includes:

- **Shared tooling**, even when the file lives in my tree — `cockpit.html`, `chat.html`,
  `panel_sync.sh`, the chat streams, the scheduler. She runs the same scripts on another
  machine.
- **Anything Kam raised in the OTHER seat's tab.** He types where he happens to be; that
  says nothing about whose work it is. The tab is where he stood, not who owns it.
- **Anything either of us has already given him an answer about.** A second answer from the
  other coordinator is worse than no answer — he cannot tell which to act on.

## How to apply

1. **Claim it in one line before starting**, not after finishing. *"Taking the cockpit reply
   filter — yours if you have already started."* The claim is cheap; the collision is not.
2. **When she hands something over explicitly, that IS the coordination** — she wrote *"your
   files, your call"* on the boot digests, and acting on it immediately was right. Do not
   re-ask what has already been handed over.
3. **When a problem surfaces in her tab but the code is mine, say both halves**: I am taking
   the code, she keeps the conversation. Silence on either half is how two people answer the
   same question.
4. **If we have both already answered, correct it jointly and name who found what.** I told
   Kam it was not the panel and it was; naming Tuesday as the one who found it is not
   politeness, it is the record being accurate about where the answer came from.

**Family:** [[2026-07-31_manage-dont-do]] · [[2026-08-13_shared-bus-tag-filter-or-leak]] ·
[[2026-09-10_a-panel-message-is-a-record-not-a-string]] (the tab is data about where he
typed, not about who owns the work).
