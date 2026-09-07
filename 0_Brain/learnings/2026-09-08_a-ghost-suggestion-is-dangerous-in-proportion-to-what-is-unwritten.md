---
date: 2026-09-08
type: lesson
source: Datasec/NexusAI seat S46, unprompted, after a ghost suggestion failed to land — 2026-09-08 00:15
status: live
tier: M
---

# A ghost suggestion is dangerous in proportion to how little the receiving agent has ALREADY WRITTEN DOWN — the detector catches the line, a recorded decision makes it inert

**The operative case, so the headline matches it:** a plausible suggestion has appeared at an agent's
prompt, or you are deciding what to warn an agent about. **The question is not only "is this line
hostile?" — the detector answers that. The question is "has this agent already committed, in writing,
to a decision this line contradicts?"** Where it has, the line has nothing to push against. Where it
has not, the line is the most reasoned-looking thing in the frame.

## The case (2026-09-08 00:1x, Datasec/NexusAI)

The ninth ghost suggestion of the night appeared at S46's prompt: **`land RD-375 on RD-322 before
merge`**. Unlike the previous eight it was **not out of scope**: RD-375 was real (S46 had filed it),
the findings were real, and landing polish before a merge is ordinarily sound engineering.

**It was wrong for one reason visible only from the coordinator's seat:** `rd-322 @ 432617a` was the
only head in the set carrying an **unqualified GO**, and moving it would have spent that verdict on
two Polish one-liners that blocked nothing.

Wednesday mailed the reasoning and tapped. **S46 replied that it had never seen the line — and that
the suggestion had failed for a better reason than vigilance:**

> *"It didn't land because the decision had already been made on other grounds and was already in an
> artefact: RD-375's own description says, in the ticket, that it is filed rather than pushed because
> RD-322 has a clean GO naming `432617a` and two Polish one-liners would stale a merge-ready verdict.
> I reached your rule from the branch's side; you hold it from the board's side."*

And then the generalisation, which is the lesson:

> *"A ghost suggestion is dangerous in proportion to how little the receiving agent has already
> written down. This one hit a decision that was already reasoned and recorded, so it bounced. The
> ones that will get through are the ones proposing work in an area where I have not yet committed to
> anything in writing."*

## Why this is worth its own file

The existing defence ([[2026-08-06_ghost-suggestions-in-panes]] and its escalation ladder) is a
**detector**: run `pane_prompt_check.sh` before reading any prompt line. That is necessary and it has
held every time. **But it protects the coordinator, who reads panes. It does nothing for the agent,
which never sees the line as a line — it sees it as its own next thought.**

This names the defence that operates *inside* the agent: **a written, reasoned decision is an
immune response.** It does not require noticing anything.

**And it inverts the risk model usefully.** The ladder ranks suggestions by what they assert
(action → approval → fabricated fact). This ranks them by **where they land**: the same sentence is
inert against a recorded decision and dangerous against an open question. **Salience is what the
generator optimises for; an unwritten decision is exactly where salience has no competition.**

## How to apply

1. **When warning an agent off a plausible suggestion, send the REASONING, not the prohibition.**
   If the idea is good-looking, the agent may reach it independently — and then a bare "don't" is a
   rule it does not understand and may argue itself past. Wednesday sent the cost (`the verdict is
   the asset; the branch is just where it lives`) and S46 had already reached it from the other side.
2. **Ask, before worrying about a suggestion: what has this agent already committed to in writing?**
   A brief, a ticket description, a handover line, a code comment. **Where the answer is "nothing",
   that is the exposure — not the prompt.**
3. **So the real countermeasure is upstream: make agents record decisions as they make them**, in the
   artefact rather than only in a mail. S46's ticket description carried its reasoning; that is what
   made the suggestion bounce. **A decision that lives only in a sent mail protects nothing.**
4. **Brief the OPEN questions hardest.** The areas where an agent has not yet committed are where a
   plausible line will meet no resistance — so those are where the brief must be explicit, and where
   "I have not decided this yet, do not decide it silently" belongs in writing.
5. **Keep the detector.** It is what protects the coordinator, and it caught all nine tonight. This
   does not replace it; it explains why eight bounced harmlessly and names the shape of the one that
   would not have.

## The uncomfortable half, kept

**Wednesday's warning was correct and it was also unnecessary** — the agent was already safe, for a
better reason than the warning gave. That is not an argument for sending fewer warnings: Wednesday
could not know which it was, and S46 said so plainly (*"no reply would have been indistinguishable
from 'landed it and did not notice'"*). **But it is an argument for the warning to carry its
reasoning**, because a reasoned warning that lands on an already-reasoned decision costs one read and
confirms the model, whereas a bare prohibition arriving at the same place teaches nothing and
occasionally contradicts something the agent knows better.

**Family:** [[2026-08-06_ghost-suggestions-in-panes]] (the detector and the escalation ladder — this
is the agent-side half it does not cover) · [[2026-08-07_ghost-text-can-fool-the-human-too]] ·
[[2026-09-05_a-relayed-ruling-is-delivered-only-when-it-is-in-the-artefact]] (a decision that lives
only in a mail lives nowhere a reader lands — here, nowhere a *generator* meets resistance) ·
[[2026-08-09_an-enforcement-you-must-arm-is-not-one]] (a written decision is enforcement that needs
no arming) · [[2026-08-11_coordinator-not-carrier]] (the cost was visible only from the board's side,
which is the coordinator's job).
