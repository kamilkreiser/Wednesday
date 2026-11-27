---
date: 2026-11-27
type: instruction
source: Kam, Wednesday terminal 2026-11-27 (stamp 10:31 at capture), right after /login on a new account and his own /model to Fable 5.2
status: live
tier: W
---

# Fleet-structure project (Kam's priority beside Secuura): Fable for Wednesday and its agents; Postgres-backed brain, tiered project briefs, specialist skill loads

**The operative case.** Wednesday is choosing what to work on, launching an agent for this project, or designing boot/brief/skill loading for any seat. **This project is prioritised alongside Secuura, and Wednesday and every agent working on it run on the newest Fable.**

## Kam's words, verbatim

"In addition to working on Secuura I have a new project I would like you to prioritise.  Use fable for yourself and agents working on this project.  1)I would like to review and improve the structure for you Tuesday and Friday.  2) I saw that using a postgress datavase is a more efficient and better than .md files.  recently we revised the learning brain files but this would be a much better improvement.  Please look at this video and structure mentioed in it.  Anything else along the same line and improve the setup we use.  https://youtu.be/eNhiHP7t5bo?si=uWXQJ4MuXn3sRS0u  3)for each project, I would like to create a structure where, you, tuesday and friday can load the full project brief and info.  As you spin up worker agents for each task, the agents go through a cut down version of the brief on load, that includes project intent, architecture and key info (high level for context.  4) in addition to the before context, specialised agents will load specialised skills.  E.g. security review agent will load security skills including NIST guidelines, essential 8 for australia, GDPR, etc.  Each load it checks if they have been updated and reviews against these.  5)Please review the following skills and apply.  general ones to all loaders, specific ones to specialised agents https://www.linkedin.com/posts/yrebryk_12-github-repos-for-founders-to-ship-secure-share-7531386388663975936-agWC/?utm_source=social_share_send&utm_medium=ios_app&rcm=ACoAAAB0lV0BkPTMAUZBwf7qDXkSIFyZLethBus&utm_campaign=copy_link"

## Wednesday's reading (told to him on the panel, bf-6bfcb92a1ea4e355)

1. Review and improve the structure of Wednesday, Tuesday and Friday.
2. Study the video's Postgres-backed memory structure (and similar work) against the markdown brain; improve the set-up.
3. Per project: coordinators load the FULL brief; worker agents load a CUT-DOWN brief (intent, architecture, key info).
4. Specialist agents also load specialist skills (security: NIST, Essential Eight, GDPR and so on), with a check on each load that the source has not been updated.
5. Review the twelve repos in the LinkedIn post; general ones to all loaders, specific ones to specialists.

## Boundaries (Wednesday's, stated)

- "Use fable" is scoped to THIS project: Secuura seats keep routing by fleet/specs/model-routing.md. Kam set this pane's model himself; a seat's model is still set at launch, never by /model from Wednesday.
- Research and a design come to Kam before anything is rebuilt: the brain, launchers and boot path are shared by three seats (claim with the sister seats before touching shared tooling).
- Datasec project briefs are Tuesday's to write; the STRUCTURE is shared and client-neutral.
- Third-party skills and repos are read before adoption; nothing external is installed into a loader unread.

## RULED 2026-11-27 (live board, after the design was shared)

- 11:43:30, a note, verbatim: "thank you.  I like your recommendations.  Please put this into action for you.  Each external drive will now also hold the dB.  once you finish and test, prepare instructions and send to Tuesday and Friday"
- 11:43:40 tap: card wed-fleet-structure-v2-where-postgres-runs-1127 = **c, Local index only**.
- 11:43:52 tap: card wed-fleet-structure-v2-go-steps-1-3-1127 = **a, Go, steps 1 to 3 in that order**.

**Wednesday's reading (told to him on the panel):**
- Build and test on Wednesday's own seat FIRST. Tuesday's and Friday's seats change only after that, by written instructions Wednesday sends them.
- Postgres is LOCAL. Its data directory lives ON each seat's external drive (DevMASTER for this seat), so the drive still holds everything. It is a REBUILDABLE INDEX only (tap c): no hosted database, no spend; row records stay in files and the union tools.
- This lifts PORTABILITY.md item 25's "never start a service on it" for this ONE use. The rule "never store project state off-drive" stands, and is why the data directory is on the drive.
- Still Kam's: any hosted database, any spend, any change to another seat's boot before the instructions step.
