---
date: 2026-09-24
type: preference
source: Kam, terminal to Friday, 2026-09-24 ~11:3x AEST
status: live
tier: W
---

# Every decision Friday needs from Kam goes on the live board's Fleet activity panel, as a card, the moment it exists

**His words, verbatim:** *"please place decisions you need from me on the chat dashboard under fleet activity.  now and going forward"*

**The operative case, so the headline matches it:** Friday is about to write "decision for Kam", "your call", "waiting on you" or a
question with options into a terminal reply, a panel chat message or a STATUS summary. **Stop. Make it a card:**
`2_Project_Files/tools/decision_queue.sh add --json` (one JSON object on stdin). The script writes the local queue AND posts the card
to the live board, where it renders under **Fleet activity** (verified 2026-09-24: 11 HPSM-POC cards, each "posted to Friday (HTTP 201)").
Chat and terminal replies may POINT at the cards; they are not where the decision lives.

**How to apply:**
1. **One decision per card.** Fields: `id` (project-prefixed), `client_project`, `title`, `bluf`, ≥2 `options` (key, label, detail),
   `recommended`, `default_action` (what happens if he never answers, and who acts). Cards follow the ask-format lessons: action first
   when his hands are needed, the link on its own line.
2. **Do it the moment the decision exists**, not batched at the end of a turn: a seat's STATUS that lists "Decisions for Kam" is
   turned into cards in the same action as the review.
3. **The prior-ruling gate is a question, not an obstacle** ([[2026-09-07_a-prior-ruling-gate-refusal-is-a-research-prompt]]):
   read each match; if it is a different subject sharing generic words, re-add with `_override_prior` stating the measurement.
   **Never name another client's cards in the override text** (hard rule 2: a Datasec card carries no Secuura ids).
4. **Close the loop:** when he rules, `decision_queue.sh rule`, act, then `--delivered <artefact>`.

**Family:** [[2026-08-21_decision-queue-and-rotation-rhythm]] (the queue was already his preferred surface; this names WHERE it is read)
· [[2026-08-16_an-ask-without-a-default-is-an-indefinite-hold]] · [[2026-09-08_ask-format-action-first]] ·
[[2026-09-11_a-number-left-for-kam-in-a-handover-reaches-no-surface-he-reads]].
