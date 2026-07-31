# WEDNESDAY — project definition

**One-liner:** Kam's personal AI chief-of-staff ("Jarvis-like"): task manager,
delegator to all other agents, comms handler — with a dedicated second brain and
an explicit learning loop so the relationship improves over time.

**Started:** 2026-07-31 · **Phase:** Discovery / Architecture
**Home:** `/Volumes/KK_T9_External_HDD/WEDNESDAY`

## Phase plan (draft — refine after discovery answers)

| Phase | Contents | Exit criteria |
|---|---|---|
| 0. Foundation ✅ | Folder structure, brain, launcher, voice script, research | Kam launches via `Launch_Wednesday.command`, Wednesday boots with brain + persona + voice |
| 1. Discovery ⟵ NOW | Q&A (`Discovery/02_discovery-questions.md`), architecture doc, autonomy ladder | Kam signs off architecture + autonomy ladder |
| 2. Core loops | Daily briefing, task board live, projects-index feed (end-of-session skill change), learning loop proven over ≥1 week | Wednesday demonstrably applies ≥3 captured learnings; index fresh without manual sweeps |
| 3. Comms | Agent Mail inbox; WhatsApp channel | Wednesday triages mail + participates in WhatsApp per agreed policy |
| 4. Delegation | Briefing-file handoffs to project agents; then (trust-gated) spawning sessions | A real task delegated end-to-end through Wednesday |
| 5+. Later | Neural voice loop, dedicated Mac Studio, local models (Kimi-K2), "dreaming" consolidation job | — |

## Key design decisions (log — newest at top)

- **2026-07-31 · Index feed shipped:** one Step 2c in the vault end-of-session
  skill (not 15 launcher edits); mount-tolerant; entries/ is the only place other
  agents write in Wednesday's brain.
- **2026-07-31 · Linear = task source of truth:** dedicated workspace
  `wednesday-agent` (account IS "Wednesday"), team WED; TASKS.md is a pointer.
- **2026-07-31 · Portability:** T9 is the master copy; on-drive deploy key chosen
  deliberately over keychain (travels with the drive); PORTABILITY.md tracks the
  few machine-local deps.
- **2026-07-31 · Voice = Matilda (Premium):** Kam auditioned; natural beat Irish.
  Persona's Irishness lives in the writing, not the synthesizer.

- **2026-07-31 · Brain layout:** three-tier memory in `0_Brain/` (daily=episodic,
  learnings+people=semantic, identity=procedural); full `learnings/` read at boot
  (Kam accepted token cost); index-first pattern deferred until scale demands it.
- **2026-07-31 · Coordination:** other agents feed `projects_index/entries/` via
  ONE change to the vault end-of-session skill (pending Kam approval); Wednesday
  never writes into other projects.
- **2026-07-31 · Voice v1:** macOS `say` + Moira (en_IE) behind `speak.sh` (single
  swap-seam for future TTS); inbound via Whisperflow. Full research on the
  Rhodes-style voice loop filed in `Discovery/research/`.
- **2026-07-31 · Persona:** Wednesday, Irish, playful, direct; persona lives in
  the brain (`0_Brain/identity/`), not hardcoded in the launcher.
