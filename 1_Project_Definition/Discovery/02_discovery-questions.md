# Discovery questions — scoping & architecture

Date: 2026-07-31. Informed by the founding brief + both research reports in
`research/`. Answer by voice in any order; Wednesday records answers inline under
each question and marks it ✅. Nothing gets built from an unanswered question.

## A. Daily operation & rhythm

1. **What does a normal day look like?** When do you start, when do you want the
   morning briefing, what timezone(s) do you live in? Should Wednesday have a
   scheduled morning wake-up (cron) or only run when you launch her?
2. ✅ **Where do your tasks live today** — Linear (Secuura-PK), the extranet portal,
   the vault `tasks/` + `To Do`, Apple Reminders, email, your head? Which of these
   is Wednesday allowed to *write* to, and which should become the single source
   of truth?
   **Answer (2026-07-31):** A NEW, dedicated Linear account/workspace just for this
   project. Every action item and task recorded in Linear; the launcher checks
   Linear at session start and builds the day's plan from it (critical in early
   phases, less so once agent tooling matures). Kam will create the account;
   Wednesday guides setup.
3. **What counts as an "intermediate task/answer/query"** (duty #2)? Examples of
   the last three so I understand the shape — research questions? Waiting-on-reply
   trackers? Draft answers held for your approval?

## B. Delegation & other agents

4. ✅ **Delegation mechanics:** when you say "delegate to other agents", is the model
   (a) Wednesday writes a briefing file the project's own Claude session picks up
   at launch, (b) Wednesday spawns headless Claude sessions in project folders
   herself, or (c) both, trust-gated over time? (b) has real blast-radius —
   where's your comfort line today?
   **Answer (2026-07-31):** Very high comfort. Wednesday may spin up sessions,
   write notes/briefs, paste into input boxes — but MUST NOT modify files inside
   coding projects. Manage and delegate; the target agents execute. Everything
   else, Wednesday can control. (Learning: `0_Brain/learnings/2026-07-31_manage-dont-do.md`)
5. **Projects index:** the proposed design keeps other projects' wrap-ups writing
   one entry file each into `0_Brain/projects_index/entries/` via a single change
   to the vault `end-of-session` skill (spec: `projects_index/README.md`). OK to
   implement? And is the interim read-only sweep (Wednesday reads each project's
   `history.md` at startup) acceptable until then?
6. **Which projects should Wednesday watch first?** All of `!CODING/`, or a
   shortlist (e.g. Secuura Blockchain, NexusAI, Sales Portal)?

## C. Email, WhatsApp, comms

7. ✅ **Agent Mail:** own inbox for Wednesday (e.g. wednesday@agentmail.to) or the
   shared coagent@agentmail.to? What may she do unprompted: read+summarize only,
   draft-for-approval, or send within defined limits? Which of YOUR mailboxes (if
   any) is in scope for triage, and what's firmly out of bounds?
   **Answer (2026-07-31):** Dedicated wednesday@agentmail.to — "perfect". Early on
   also monitor the shared coagent@ inbox; over time Wednesday develops her own
   identity. (Send-permission limits still to be defined — remains open.)
8. ◐ **WhatsApp:** which discussions will she be added to, and what's the expected
   behaviour — silent observer building context, active participant, or
   summarizer-on-demand? Any hard rules for family chats?
   **Partial answer (2026-07-31):** Kam leans toward a dedicated old phone + new
   SIM/number for Wednesday, added to selected groups. He does NOT want Wednesday
   seeing his own WhatsApp.
   **Research verdict (2026-07-31):** Kam's plan is the ONLY viable one — no
   number-free path exists, and the official Cloud API cannot join user-created
   groups. Recommended build: old phone + ALDI $2 PAYG SIM (~$15/yr), phone
   permanently on home Wi-Fi, account aged 1-2 weeks, Mac paired via
   mautrix-whatsapp or Baileys. Ring-fenced ban risk accepted. Full report:
   `research/2026-07-31_whatsapp-channel-options.md`. Still open: which groups,
   and observer-vs-participant behaviour per group.
9. **Interrupt policy:** when may Wednesday proactively ping you (voice, WhatsApp,
   email) vs. hold things for the next session?

## D. The brain & learning loop

10. **Promotion gate:** research strongly recommends one-off remarks NOT become
    permanent rules immediately (over-personalization risk). Proposal: corrections
    land in `learnings/` at once, but only change `identity/` (who Wednesday IS)
    after recurring or on your explicit "make that permanent". Agreed, or do you
    want every lesson binding immediately?
11. **"Dreaming" consolidation:** a scheduled job that distills daily notes into
    the brain, flags stale/conflicting facts, and writes an audit summary for your
    review. Want this (nightly/weekly), or manual wrap-up-only consolidation for
    now?
12. **Contemplation tasks:** when you set one, do you want Wednesday's written
    reflection delivered back to you (next briefing?) or just stored?
13. **Cross-brain boundary:** Wednesday reads the DevMASTER vault for context.
    Anything in it (or on the system) that is out of bounds — `Family/`,
    `Daily Life/`, financials?

## E. Voice

14. ✅ **Voice check:** is Moira (macOS Irish voice) acceptable for now? Comfortable
    volume/speed? (Rate is tunable in `speak.sh`.)
    **Answer (2026-07-31):** Yes — Moira confirmed acceptable at default rate 175.
15. **Chattiness:** current protocol speaks at session start, task completion,
    blockers, and important changes — 1-3 sentences. More or less than you want?
16. **Later: full voice loop** (Rhodes-style push-to-talk: whisper.cpp → agent →
    neural TTS, family can phone it). Ambition for phase 2/3, or keep
    Whisperflow + `say` indefinitely?

## F. Scope, trust & safety rails

17. **Autonomy ladder:** what may Wednesday do TODAY without asking (read
    everything? send email? create Linear issues? spend money—never?), and what
    does she have to earn? A short written ladder becomes her operating policy.
18. **Failure etiquette:** when she breaks something or gets it wrong, what do you
    want beyond fix-and-verify — e.g. a written post-mortem into `learnings/`?
19. ✅ **Git:** should WEDNESDAY become a git repo (private GitHub under which
    account?) with brain versioned, or stay local-only on the T9 for now?
    **Answer (2026-07-31):** Yes — Kam's PERSONAL GitHub account, access via a
    deploy key with read+write, step-by-step setup guided by Wednesday. Also:
    the T9 SSD is the master copy — fully portable, everything on the drive
    (learning: `2026-07-31_fully-portable-drive.md`).
20. **Name check:** happy with "Wednesday" spoken aloud in the house / on calls?
    (Siri-style accidental-trigger considerations, family hearing it, etc.)

---

## Answers

*(recorded here as they come)*
