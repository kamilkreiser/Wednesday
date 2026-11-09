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

5. **The FRIDAY tab, and check it where Kam looks** (Kam, same day: *"You posted the fleet activity under Tuesday, not Friday… going forward, use the Friday board."*). Friday's cards are stored in the Friday partition. Until live-board commit `a3fe28e5e` is deployed, the page routed them by project name (Datasec → Tuesday). After any change to how cards are posted, confirm on the page which TAB shows them. The post's `HTTP 201` is a receipt for the store, not a view of his screen.

6. **Answered cards come OFF the board** (Kam, same day: *"Once answers are submitted through the fleet activity, please remove the tiles."*). `decision_queue.sh rule` on a friday-seat card now hides it on the live board (reversible and audited: `dashboard-cloud/seat/hide_message.py --card --id <id>`, and `--unhide` to restore). This needs the server's `kind=card` (commit 6741602c0, deployed by Wednesday). If the hide fails, it says so loudly; re-run the hide by hand. The ruling itself lives on the local card + the artefact, not on the tile.

**Family:** [[2026-08-21_decision-queue-and-rotation-rhythm]] (the queue was already his preferred surface; this names WHERE it is read)
· [[2026-08-16_an-ask-without-a-default-is-an-indefinite-hold]] · [[2026-09-08_ask-format-action-first]] ·
[[2026-09-11_a-number-left-for-kam-in-a-handover-reaches-no-surface-he-reads]].

## EXTENSION 2026-11-10 (ledger w=2): a 201 proves STORAGE, not that Kam can SEE the card

**What happened.** Kam, live board 2026-11-10 02:48:13: *"I cannot see any cards on fleet activity"*. The same words came on 2026-11-06 20:42; that seat listed the cards in chat and left the cause "unmeasured". Thirteen cards were open and every post had returned HTTP 201. His screenshot (IMG_0044) showed the footer `0 need you · 0 ruled today · 915 cards synced · 30 synthetic hidden`, the key unlocked, and the `× clear` chip on screen. In index.html, `× clear` renders only when a filter is saved in the browser's localStorage, and "need you" counts only cards passing that filter and the active agent tab. He tapped clear and ruled twelve cards in four minutes.

**Rules.**
1. When Kam says he cannot see something on the board, ask for the footer line (or a screenshot) FIRST. It separates three causes in one read: `cards synced 0` = API or auth; synced > 0 with `need you 0` = a filter, the agent tab or the key on his screen; `🔒` titles = the key is locked.
2. A post's HTTP 201 is never evidence that a card "is on the board" in a sentence to Kam. It proves the server stored it, and nothing more.
3. A "can't see" report gets its cause measured in the same session. Leaving it "unmeasured" is how the 11-06 recurrence happened.
4. Mechanism owed (WED's own dashboard; deploying the live app needs Kam's word): the footer should say `N open hidden by your filter` whenever a saved filter hides open cards.
