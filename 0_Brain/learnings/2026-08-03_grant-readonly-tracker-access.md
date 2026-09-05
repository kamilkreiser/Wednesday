---
date: 2026-08-03
type: principle
source: "Kam, 2026-08-03, explicit grant: 'yes, approved - go ahead and run the first sweep'"
status: live
supersedes: ""
tier: W
---

# Autonomy grant: read-only tracker access across all projects

**The grant:** Wednesday may source each project's API keys from its own
`4_Credentials/.env` for **read-only queries against that project's task
tracker** (Linear workspaces, Jira instances) — for board sweeps, decision-queue
aggregation, and situational awareness.

**Hard limits (unchanged by the grant):**
1. **READ-ONLY, ever.** No comments, no state changes, no ticket creation on
   any other project's board from Wednesday's hands. Writes remain with each
   project's own agent under its own identity.
2. Keys are sourced transiently for the query — never copied into Wednesday's
   own files, notes, or .env; never logged or echoed.
3. Output lives in Wednesday's brain (boards digest, decision queue) and in
   briefings to Kam — never pushed back into project spaces.

**Context:** Granted for the standing board-sweep mechanism (WED-28) whose
core product is the aggregated Kam-decision queue at the morning briefing.
Per [[2026-08-03_go-slow-earn-autonomy]] rule 5, this grant is recorded
explicitly so the autonomy boundary is written down, never vibes.

**Related:** [[2026-08-03_go-slow-earn-autonomy]], [[../projects_index/INDEX]]
