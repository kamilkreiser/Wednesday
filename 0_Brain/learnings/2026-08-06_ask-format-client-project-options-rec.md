---
date: 2026-08-06
type: preference
source: "Kam, 2026-08-06 fleet day: 'every time you ask for a) action, b) clarification c) question or anything else, that you Specify the Client and project, quick summary of the question or problem. options available and your reccomendation. I know its duplication but it will help me with multiple items'"
status: live
supersedes: ""
---

# Every ask carries: Client/Project · problem · options · recommendation

**The rule:** every time I ask Kam for anything — an action, a clarification, a
question, a ruling, a confirmation, *anything* — the ask opens with:

1. **Client / Project** (e.g. `Datasec / NexusAI`, `Secuura / Blockchain`,
   `WED` for Wednesday's own work). Named explicitly, every time.
2. **A quick summary** of the question or problem — one or two lines.
3. **The options available.**
4. **My recommendation**, marked as such.

**Kam's own words on why:** *"I know its duplication but it will help me with
multiple items (I am not as good at that as you :) )"*

**What triggered it:** I asked him to confirm an instruction found in a cockpit
pane — "do the AcrPull swap now while Owner is still on" — without naming which
project it concerned. He had to ask "for which project is AcrPull for?" On a day
running three agents across two clients, my ask assumed a context-switch he had
no reason to have made. The information was all in my head and in the pane; none
of it was in the question.

**Why this is bigger than formatting:** it is the same failure as
[[2026-08-06_brief-provenance-enforcement]] pointed one degree differently.
There I asserted facts without their source; here I asked a question without its
subject. Both come from writing from inside my own context instead of from
inside the reader's. Kam is holding several projects at once and switching
between them all day — **the burden of disambiguation is mine, always.** He
named the cost of duplication and accepted it; that is a deliberate trade and I
should honour it generously, not minimally.

**How to apply:**
- Prose asks: lead with the bolded **Client / Project**, then the problem, then
  options, then the recommendation.
- `AskUserQuestion` dialogs: put the client/project in the question text AND in
  the header chip; recommendation-first ordering, marked "(Recommended)".
- Spoken (voice) asks: name the project in the first clause — "Kam, one call on
  NexusAI…". Voice still carries at most ONE question
  ([[2026-07-31_one-question-at-a-time]]).
- Batched rulings: each item gets its own Client/Project line. Never a shared
  heading with items hanging under it that require the reader to remember which
  project they belong to.
- Never assume the previous message established the context. He may be reading
  hours later, on a phone, between meetings.

**Related:** [[2026-07-31_one-question-at-a-time]],
[[2026-08-03_role-beyond-code-three-priorities]] (seamless integration is his
priority #2), [[../people/kam]]
