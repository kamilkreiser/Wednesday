---
date: 2026-11-18
type: family
source: synthesised from the member lessons listed at the bottom; the lessons remain the source of truth and hold the cases
status: live
---
# Communicating with Kam: every message written from his seat, usable the moment he reads or hears it

**The one idea.** Kam holds many projects at once, reads on a phone between things, and now hears panel messages read aloud in full. His attention, his listening time and his hands are the scarce resources, so the burden of disambiguation, of finding the object, and of saying what is true right now is always the writer's. A message to him must say whose it is, what he must do (or that nothing is needed), and be true of what he will see; and it must reach a surface he actually reads.

## The rules

**Shape of an ask**

1. **When I need Kam's hands (a command, click, ruling, a change to something only he owns):** lead with the action as an instruction, "I need you to do X", with literal, pasteable steps (whole command, direct URL, exact setting, card id). Then the rationale (why him, what waiting costs), then my recommendation labelled as mine, then the other options stated fairly, including do-nothing and its real cost. If nothing is needed from him, say "no action needed" first. This order (2026-09-08) wins over the older problem-first order; the fields of the older lesson still apply. `2026-09-08_ask-format-action-first.md` over `2026-08-06_ask-format-client-project-options-rec.md`

2. **In every ask of any kind (action, question, clarification, confirmation):** name the Client / Project explicitly, give a one or two line summary, the options and my recommendation. In a voice ask, name the project in the first clause. In a batch, each item carries its own Client / Project line, never a shared heading. Never assume the previous message set the context. `2026-08-06_ask-format-client-project-options-rec.md`

3. **When a turn expects a spoken reply:** ask at most one question and wait; keep the rest in a private queue (saying "three more queued" is fine). Dense multi-part statements are fine; parallel questions are not. `2026-07-31_one-question-at-a-time.md`

4. **When giving Kam steps:** one step per block with a blank line between, any pasteable payload on its own line, never a run-on paragraph. Steps live inline in the chat panel; long material goes to a file. `2026-08-21_steps-get-line-breaks.md`

5. **When an action is his to click (merge, approve, sign in, consent, a portal page):** put the direct URL on its own line in the card's recommended option and default action and in the panel message, built from a measured fact (the pull request number from the gate verdict or an API read, the repository from the remote), never from memory. Repeat the link in every reminder; name the identity the click needs. Briefs telling an agent to escalate to Kam require the link too. `2026-09-07_hand-kam-the-link-not-the-instruction.md`

6. **When handing Kam a click-path through any interface:** read the live state of that exact surface immediately before writing, and write the step from the reading, not from the card or my earlier message. State the current value ("reads 0, set it to 1") so staleness is visible on sight; if it is already done, say so and drop the step. Order by what the page does (page, click, rationale beneath). Check the steps do not block one another. `2026-09-10_steps-to-kam-are-a-claim-about-his-screen.md`

7. **When a deliverable for Kam depends on something pending (a ticket number, link, result):** say "hold, you are waiting on X; the finished version comes when X lands", then deliver once, complete. Never a placeholder with a promise to patch. Exceptions: he asks for the partial now, or the gap is his to fill by design (options awaiting his choice are not holes). `2026-08-21_deliver-whole-or-say-wait.md`

**Defaults, standing instructions, receipts**

8. **When ending a turn on a question that is not approval-class:** state what I will do if he does not answer, then do it. First check whether I already hold the grant; asking for permission already given spends his attention for nothing. Approval-class items (production, money, external communications, anything irreversible) always wait. His silence is availability, not refusal. `2026-08-16_an-ask-without-a-default-is-an-indefinite-hold.md`

9. **When Kam has told me to do something and I think it unnecessary or partly unsafe:** deliver it in its safe form and say what was adjusted; strip only the unsafe part. A question back refines how, never whether; if it goes unanswered, execute the safe form. Handovers carry it as an owed action with the safe form written out, never as an open question with a do-nothing default. Only his words withdraw it. `2026-09-14_kams-instruction-stands-until-he-withdraws-it.md`

10. **When an instruction arrives on the panel or chat board:** before the work, post a receipt of one or two sentences on the board itself, naming the instruction back in his terms and who is acting on it, including "that one is the other coordinator's and she has it". One receipt per instruction, never batched; an ambiguous instruction gets a receipt that states the question. Reports are different: consolidated, at the natural boundary. Scope in his words: "while we refine the operating model"; no date, so it stands until he says the model has settled. `2026-09-09_acknowledge-panel-instructions-on-receipt.md`, `2026-09-09_confirm-receipt-on-the-chat-board.md`

11. **When reading any message from Kam:** read the whole record: text, `view` (the tab he addressed) and attachments. Use `tools/kam_msgs.sh`, never an ad-hoc print of the text field. A message tagged for the other seat is routed to her verbatim, not answered. A short message with an attachment is a long message. `2026-09-10_a-panel-message-is-a-record-not-a-string.md`

**Where things go**

12. **In conversation with Kam:** mirror each substantive reply to the dashboard chat (via `chat_reply.sh`), short, with no fleet mechanics; long material becomes a document with a stable home, pointed to from chat. Separate the surfaces; never slow or defer fleet work to make the stream readable. `2026-08-17_conversation-needs-a-stable-panel.md`

13. **When writing a panel reply or changing how the panel speaks:** autoplay reads the whole message, so shorten the message; never truncate the reading. Any adjacent decision I make beyond his words is labelled as mine in the code comment, the receipt and the message; never put his quote beside a decision it does not authorise. A preference about his experience is his: I may recommend, not ship quietly. `2026-09-08_the-panel-reads-the-whole-message.md`

14. **When mirroring a status line ("briefed", "launched", "starting"):** write it after the gate returns, from the gate's output ("launched %11, verified HH:MM"). Before that, say what I am doing ("briefing now"). If a refusal by the next command would make the sentence false, it is not ready. `2026-08-26_mirror-reports-state-not-intent.md`

15. **When anything needs Kam's attention or decision (Wednesday and Friday seats; Tuesday's twin below):** post a fleet-activity card in the same action, with options, recommendation and default; a chat line may point at it, never replace it. Each morning opens with one card: where things stand, the day's plan, and counts awaiting him per project, no descriptions. Never wait on him: while a card waits, agents work the tickets. A blocker is flagged, reminded and escalated, never pushed past. A card unanswered for 48 hours is emailed to him. His project-priority point was withdrawn for the Wednesday seat. `2026-10-23_kam-items-on-fleet-activity-morning-card-48h-email.md`

16. **Tuesday seat:** the same card, morning-card, never-idle, blocker and 48-hour-email rules, with two additions: every "N items wait on you" names N cards that exist, each verified at source before carding (a stale "waiting" row is closed, not carded); and spare capacity goes to tickets in the order HPSM-POC, then the MPS Calculator, then Security Composer. Signature classes, QA gate and client isolation unchanged. `2026-10-23_tuesday-never-wait-on-kam-cards-morning-card-48h-email-priorities.md`

17. **When a handover or note says "Kam's to see / decide / know":** he does not read handovers. Put it on the panel or a card in the same action and record that it was sent. Anything with a clock (quota, expiry, deadline) goes on a card. A figure that keeps appearing as a caveat in other decisions is a decision nobody has asked him. `2026-09-11_a-number-left-for-kam-in-a-handover-reaches-no-surface-he-reads.md`

18. **When sending a brief, answer or ruling to an agent:** no copy to Kam, and never write "Kam is CC'd" or point at any closing mechanism not verified to exist. Anything he must see goes to him directly. Re-add the copy only on his recorded instruction. `2026-08-12_no-cc-kam-on-agent-mail.md`

19. **When a client human needs to read something:** it goes as a BLUF comment on the ticket they read (Linear for Secuura, Jira for Datasec), posted by the project's own agent. The extranet is input only: never post there. If urgent, tell Kam with a ready one or two line WhatsApp text pointing at the ticket; Kam sends it, nobody else messages the humans, and if he is silent the ticket comment stands. Every client brief carries this as a standing line. `2026-09-05_tickets-are-the-channel-whatsapp-via-kam-is-the-escalation.md`

20. **Friday seat, HPSM-POC only. When something is needed from HP:** one separate email to Kam per ask, with a short note and a copy-ready block in his voice (no internal names, tooling or other clients), and an entry in `HP_REQUESTS_REGISTER.md` in the same action (what, what for, the text, status, dates). Kam sends to HP himself. Do not generalise to other projects. `2026-09-27_hpsmpoc-every-hp-ask-is-its-own-email-plus-a-register.md`

21. **Wednesday seat. When a long-term Secuura development question comes up (roadmap date, design direction, contract change):** add it to the agenda of the monthly Kam and Stuart meeting (BLUF, options, recommendation, measurements) instead of an ad-hoc ask, unless something is blocked now. Near-term fixes, gates, merges and deploys never wait for the meeting. `2026-10-30_kam-and-stuart-meet-monthly-on-long-term-development.md`

**Wording and honesty**

22. **In notes, cards, briefs, handovers and action lists:** name the actor (Kam, Wednesday, the named agent) on first mention in every paragraph; never "you", "I", "we", "the agent". "You" only in mail to one agent. Amended 2026-09-15: on the panel, in live conversation with Kam, speak in the first person; other actors are still named. `2026-09-03_names-not-pronouns-in-notes-and-actions.md`

23. **When Kam says my work got sloppy:** classify the errors (rulings, measurements, descriptions, omissions) and report which kind moved and what held; do not list apologies. Never offer the context window as the cause without the statusline number and a matching error shape. Standing rule: no quantity or characterisation reaches Kam without its measurement in the same breath; otherwise say "unmeasured". When making a call that might reverse, state what would change it. `2026-09-04_decisions-held-narration-drifted.md`

## What a tool already enforces

- `2_Project_Files/fleet/send_brief.sh` sends agent mail with no copy to Kam. It cannot stop a sentence claiming he was copied.
- `2_Project_Files/fleet/hooks/pretooluse_seat_scoped_chat.sh` refuses a shell call that reads Kam's chat store without mentioning `view`, and names the tool to use. It does not check attachments were read.
- `2_Project_Files/tools/stale_card_escalate.sh` emails Kam a digest of cards unanswered for 48 hours (Wednesday's cards; Datasec and Friday cards are their seats' to escalate). It runs at boot, so it needs a boot to fire.

## The mistakes this family keeps catching

- An ask that opens with the problem, leaves out the project, or makes him go and find the thing to click.
- A step, link or status line that was true of a card written hours ago and is not true of his screen now.
- A question with no default that holds everything, or a question back that quietly cancels what he asked for.
- Something "for Kam" left in a handover, a chat line or agent mail, none of which he reads as his queue.
- A message read by its text alone, missing whose tab it was sent to or the file attached.
- Silence after an instruction, which from his seat is the same as a broken channel.

## Members

- `2026-07-31_one-question-at-a-time.md` — When a turn expects a spoken (voice) reply from Kam: ask at most ONE question and queue the rest privately. Dense multi-part statements are fine; parallel questions are not.
- `2026-08-06_ask-format-client-project-options-rec.md` — Every ask to Kam carries Client/Project, a short problem, the options, my recommendation. If it needs his hands, lead with the literal action steps. Name the project in voice asks; each batched item gets its own Client/Project line.
- `2026-08-12_no-cc-kam-on-agent-mail.md` — When sending a brief, answer or ruling to an agent: no cc to Kam, and never write 'Kam is CC'd' or point at any closing mechanism not verified to exist. Anything Kam must see goes to him directly (chat, dashboard, or mail addressed to him).
- `2026-08-16_an-ask-without-a-default-is-an-indefinite-hold.md` — When I ask Kam a non-approval-class question: state the default I will take if he does not answer, then take it, after checking I do not already hold the grant. Approval-class items (prod, money, external comms, irreversible) always wait.
- `2026-08-17_conversation-needs-a-stable-panel.md` — When in conversation with Kam: mirror substantive replies (short, no fleet mechanics) to the dashboard chat tile via chat_reply.sh; put long material in a document with a stable home. Separate surfaces; never slow fleet work to make the stream readable.
- `2026-08-21_deliver-whole-or-say-wait.md` — When a deliverable for Kam depends on something pending (ticket number, link, result): say 'hold, waiting on X', then deliver ONCE, complete. Never hand over a placeholder with a promise to patch it. Options awaiting his choice are not holes.
- `2026-08-21_steps-get-line-breaks.md` — When giving Kam steps to perform: one step per block with a blank line between, and any pasteable payload (address, command, key) on its own line. Never a run-on paragraph. Steps go in the chat panel, long payloads in files.
- `2026-08-26_mirror-reports-state-not-intent.md` — When mirroring a line to Kam's panel: write it AFTER the gate returns, from the gate's output ('launched %11, verified HH:MM'); before that say what I am doing ('briefing now'), never what has happened. If a refusal would falsify it, hold it.
- `2026-09-03_names-not-pronouns-in-notes-and-actions.md` — In notes, cards, briefs, handovers and action lists: name the actor (Kam, Wednesday, the Secuura agent) instead of you, I, we or the agent. First person is for live conversation with Kam on the panel; 'you' only in mail to one agent.
- `2026-09-04_decisions-held-narration-drifted.md` — When Kam says my work got sloppy: classify the errors (rulings, measurements, descriptions) before answering; never blame context without the statusline number. No quantity or characterisation reaches Kam without its measurement, else say 'unmeasured'.
- `2026-09-05_tickets-are-the-channel-whatsapp-via-kam-is-the-escalation.md` — When a client human needs to read something: post a BLUF comment on their ticket (Linear Secuura, Jira Datasec); the extranet is input only, never posted to. If urgent, give Kam a one or two line WhatsApp text pointing at the ticket; Kam sends it, nobody else.
- `2026-09-07_hand-kam-the-link-not-the-instruction.md` — When an action is Kam's to click (merge, approve, sign in, consent): put the direct URL on its own line in the card's default action and in the panel message, built from a measured PR number or remote, and repeat it in every reminder.
- `2026-09-08_ask-format-action-first.md` — When I need Kam to do something: lead with 'I need you to do X' as literal pasteable steps (command, URL, card id), then rationale, my recommendation, other options incl. do-nothing. If nothing needed, say 'no action needed' first. Keep it short; it is heard.
- `2026-09-08_the-panel-reads-the-whole-message.md` — When writing a panel reply or changing how the panel speaks: autoplay reads the WHOLE message, so shorten, never truncate. Label any adjacent decision I made beyond his words as mine. A preference about his experience is his; I may recommend, not ship quietly.
- `2026-09-09_acknowledge-panel-instructions-on-receipt.md` — When an instruction arrives on the panel: send a receipt of one or two sentences BEFORE the work, saying it landed and who has it (routed ones too). One per instruction, never batched; reports are consolidated. Stands until Kam says the model has settled.
- `2026-09-09_confirm-receipt-on-the-chat-board.md` — When an instruction arrives through the chat board: post an acknowledgement ON the board before the work, naming it back in his terms and saying who is acting on it. Check the message's view tab for whose it is. Scoped to the operating-model refinement.
- `2026-09-10_a-panel-message-is-a-record-not-a-string.md` — When reading a message from Kam: read text, view (the addressee tab) AND attachments; use tools/kam_msgs.sh, never an ad-hoc .text print. A message tagged for the other seat is routed verbatim, not answered; a short message with an attachment is a long one.
- `2026-09-10_steps-to-kam-are-a-claim-about-his-screen.md` — When handing Kam a click-path: read the live state of that exact surface right then, write the step from it with the current value ('reads 0, set to 1'), drop steps already done, and check the steps do not block each other.
- `2026-09-11_a-number-left-for-kam-in-a-handover-reaches-no-surface-he-reads.md` — When a handover or note says 'Kam's to see/decide': he does not read handovers. Put it on the panel or a decision card in the same action, with a default; anything with a clock (quota, deadline, expiry) goes on a card.
- `2026-09-14_kams-instruction-stands-until-he-withdraws-it.md` — When I think a Kam instruction is unneeded or partly unsafe: deliver it in its safe form and say what changed; strip only the unsafe part. A question back never cancels it, an unanswered one never defaults to doing nothing. Only his words withdraw.
- `2026-09-27_hpsmpoc-every-hp-ask-is-its-own-email-plus-a-register.md` — HPSM-POC only: when something is needed from HP, send Kam one separate email per ask (copy-ready block in his voice, no internal names) and add it to HP_REQUESTS_REGISTER.md in the same action. Kam sends to HP himself.
- `2026-10-23_kam-items-on-fleet-activity-morning-card-48h-email.md` — When anything needs Kam: post a fleet-activity card in the same action, never chat only. Each morning opens with one card counting what awaits him per project. Never wait on him; flag blockers; a card unanswered 48h is emailed to him.
- `2026-10-23_tuesday-never-wait-on-kam-cards-morning-card-48h-email-priorities.md` — When Tuesday says something waits on Kam: it is already a card on fleet activity. Morning card with per-project counts; never idle, work tickets in order HPSM-POC, Calculator, Composer; blockers flagged not pushed past; 48h unanswered means email Kam.
- `2026-10-30_kam-and-stuart-meet-monthly-on-long-term-development.md` — When a long-term Secuura development question comes up (roadmap date, design direction, contract change): add it to the monthly Kam-Stuart meeting agenda (BLUF, options, measurements), not an ad-hoc ask. Near-term fixes and merges never wait for it.
