---
date: 2026-09-05
type: preference
source: "Kam, dashboard panel 2026-09-05 13:55 (verbatim): 'The team is not using the extranet much. I mentioned this yesterday. If anything needs to be escalated, please tell me and I'll send a WhatsApp message. Otherwise, everything has to be done through the tickets.' — the re-ask of his 2026-09-04 08:32 note; the shape goes back to 2026-08-19 ('by having the detail in that ticket, the message can actually be short')"
status: live
supersedes: ""
---

# Client-facing communication goes ON THE TICKET — the extranet is not a channel, and the only escalation path is a short WhatsApp that KAM sends

**The operative case, so the headline matches it:** Wednesday or an agent has something Peter, Stuart or any client human needs to read — a status document, a warning, a question, a PR's state, a finding. **It goes as a BLUF comment on the ticket they will read (Linear for Secuura, Jira for Datasec). Never the extranet. Never a document "posted" or "sent" anywhere else.** If it is urgent enough that a ticket comment might sit unread, that is an ESCALATION: Wednesday tells Kam, with a copy-pasteable one-or-two-line WhatsApp text that points at the ticket, and Kam sends it. Nobody else messages the humans.

**The lesson:** Kam's team works from tickets and from Kam's WhatsApp; the Secuura extranet is a surface they barely look at. Everything the team must act on lives in a ticket comment; escalation is a short pointer Kam sends; the detail is never in the message, it is in the ticket.

**Context (why w=2, and the diagnosis w=2 requires):** on 2026-09-04 08:32 Kam wrote on a card: *"it does not look like the guys are watching the extranet. If all communication needs to be through tickets or if you want me to escalate, please give me the text to post in whatsapp."* The seat treated that as a TASK (draft the WhatsApp text — done, sent by Kam 09:02) and never filed it as a RULE. So on 2026-09-05 the successor briefs still carried "extranet posted" and "Peter's five extranet replies" as if the extranet were a live channel, and Wednesday's own 13:39 panel line framed the PR-status document (#811) as a thing to be "sent" — when the rule already said: put it on the ticket, and hand Kam a pointer if it needs a push. **A ruling that arrives inside a drafting task is still a ruling; the task is the instance, the sentence is the rule.** The same shape as [[2026-08-04_gitignore-artifacts-at-creation]] rule 3 and the 08-06 consolidation rule: a candidate that changes behaviour gets a file the same session, or it does not fire at the next boot.

**How to apply:**
1. **Every deliverable for a client human is a ticket comment, BLUF-first** ([[2026-08-06_bluf-write-for-the-reader]]), posted by the project's own agent under its board authority. A document in a repo or on a branch (the #811 status document) is delivered by a comment that carries its content or its link ON THE TICKET the human reads — the review-stream parent for Peter, the S↔K stream for Stuart ([[2026-09-02_coo-actionable-tickets-never-wait-for-kam]]).
2. **The extranet is INPUT ONLY.** Read replies there if they exist; never post there; never count an extranet reply as "the human has been told" in the other direction. A brief that says "post to the extranet" is wrong.
3. **Escalation = Wednesday → Kam → WhatsApp.** When a ticket comment is not enough (a security hold, a merge the team must not do, a question blocking a rotation), Wednesday tells Kam on the panel with the WhatsApp text ready: one or two lines, the ticket id, nothing that is not already on the ticket (his 2026-08-19 rule: "by having the detail in that ticket, the message can actually be short"). Kam decides and sends; external comms stay his signature class ([[2026-08-07_protocol-v1.3-signed-delegation]]).
4. **Wednesday does not nag him with escalation candidates.** Tell him when one exists, with the text; the default if he is silent is that the ticket comment stands on its own.
5. **Briefs carry this as a standing line** in the HOLDS section for every client project: "Client-facing communication = ticket comments only; the extranet is not a channel; anything needing a push goes to Wednesday as an escalation candidate for Kam's WhatsApp."

**Related:** [[2026-08-06_bluf-write-for-the-reader]] · [[2026-08-06_ask-format-client-project-options-rec]] · [[2026-08-07_protocol-v1.3-signed-delegation]] · [[2026-09-02_coo-actionable-tickets-never-wait-for-kam]] · [[2026-08-04_gitignore-artifacts-at-creation]] (file it at creation) · [[../people/kam]]
