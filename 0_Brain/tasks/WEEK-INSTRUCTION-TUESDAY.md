---
date: 2026-09-21
type: week-instruction
status: live
valid_until: 2026-09-27
given: "Perfect, thank you. Keep going, and if you need anything from me, post it to the live dashboard. I'll be traveling, but we'll be checking this dashboard." — Kam, typed into the Tuesday terminal, 2026-09-21 18:02:30 AEST (transcript 4c844a00, 08:02:30Z)
source: seat-scoped copy created 2026-09-16; made live 2026-09-21 18:2x by the post-rotation Tuesday seat (previous version kept at WEEK-INSTRUCTION-TUESDAY.md.pre-0921-1820-live)
---

# The week's standing instruction (read at every boot — the launcher names this file)

**status: live — Kam is travelling. He reads and types on the LIVE dashboard (https://wednesday-dashboard-e42e.azurewebsites.net).**

## His words, and the ones it stands on (verbatim)
- **18:02:30 (terminal):** "Perfect, thank you. Keep going, and if you need anything from me, post it to the live dashboard. I'll be traveling, but we'll be checking this dashboard."
- **~08:3x (panel):** "Don't worry about the usage gate. I will log in as a new account as we get close to 100%. Please do everything you can to get Nexus AI ready for resubmission."
- **~15:2x (terminal):** "It's okay, let's keep working through it and email me the zip when it's ready to upload and resubmit."

## valid_until — a READING, stated to Kam on the live board, his word corrects it
He gave no return date. On 2026-09-15 he said he would be away "next week", leaving Monday night (2026-09-21). **Read as through Sunday 2026-09-27** (weekday derived: `date -j -f %Y-%m-%d 2026-09-27 +%A` = Sunday). If he comes back or restates earlier or later, this date moves.

## Scope (Tuesday's reading of his words)
1. **Priority: NexusAI ready for Marketplace RESUBMISSION.** It is the agreed fix for a measured live data-exfiltration finding (RD-549). The work runs through the NexusAI agent(s). Tuesday commissions the work, gates it, checks it and reports.
2. **The deliverable Kam asked for:** the resubmission zip, once it has **passed its own package QA gate**, emailed as an attachment to **kamil.kreiser@datasec.com.au**. The mail says what the zip contains, the commit it was built from, which gates it passed, and every known residual. **Kam uploads and resubmits. We never touch Partner Center.**
3. **Asks go on the live board** as `chat_reply.sh` messages or `decision_queue.sh add` cards (BLUF first, with a default). A message counts as delivered only on HTTP 201. His replies reach this seat only through the live poller (`fleet/cockpit/live_chat_poll.sh --seat tuesday`), so keep it armed and re-arm it after any reboot.
4. **Unchanged, and NOT granted by this file:** the v1.3 signature classes (production, money, external comms to humans, anything irreversible) still pause for him. The QA gate comes before every score and every merge. **A merge to NexusAI main triggers `deploy-demo.yml`. The harness classifier has refused that tap unless Kam says it in the terminal** (2026-09-21 05:4xZ), so a merge release while he is travelling needs his word via the live board. That word arrives in this pane as a poller tap. Whether the classifier accepts that is UNTESTED. Say so when the moment comes; never route around it.
5. **Usage:** his ~08:3x lift of the 95% stop still holds (EXPIRING-GRANTS). Re-ask if the gauge passes ~99% with no new account.
6. **Other Datasec projects** keep their standing state. Nothing new starts on them on this file's authority.

## On or after valid_until, or if status is not live
Stop acting on this file's authority and card Kam (learnings/2026-09-06_a-scoped-override-carries-its-own-expiry.md). `doctor.sh` warns on a lapsed file at every launch.
