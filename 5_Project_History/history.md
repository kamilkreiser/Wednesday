# WEDNESDAY — session history (newest at TOP)

---

## 2026-07-31 (later) — Setup complete: voice, GitHub, Linear, index feed

**Accomplished**
- Voice: Kam auditioned macOS voices, chose **Matilda (Premium)** (en_AU neural);
  speak.sh switched with fallback chain; protocol + PORTABILITY updated.
- GitHub live: private `kamilkreiser/Wednesday`, write deploy key verified
  (fingerprint-checked; first attempt was read-only, redone), main pushed +
  tracking. Every session now commits + pushes.
- Linear live: Kam created account "Wednesday" (kreiser.org+wednesday@me.com),
  workspace `wednesday-agent`, team WED. API key in 4_Credentials/.env. Task
  board migrated: 11 issues (WED-5…15), onboarding samples archived. TASKS.md
  demoted to pointer — **Linear is the task source of truth**.
- WhatsApp research: dedicated real SIM is the ONLY viable path (Cloud API can't
  join user-created groups; no number-free registration). Plan: ALDI $2 PAYG SIM
  (~$15/yr), old phone on Wi-Fi permanently, mautrix-whatsapp/Baileys bridge.
- **Cross-project index feed implemented (Kam-approved):** Step 2c added to vault
  `skills/Current/end-of-session.md` — every project wrap-up writes its index
  card to `0_Brain/projects_index/entries/`; mount-tolerant. Smoke-tested with
  Secuura__Blockchain.md from real history. Vault commit 8287668 pushed. WED-12
  Done.
- Discovery round 1 recorded (portability, delegation, Linear, mail, WhatsApp);
  3 new learnings: one-question-at-a-time, manage-don't-do, fully-portable-drive.

**Decisions Made**
- T9 SSD = fully portable master copy — *Kam travels; everything on-drive.*
- Wednesday manages/delegates, never edits other projects' files — *management
  agent stays a management agent.*
- One question per voice turn — *Kam answers carefully one at a time.*
- Matilda over Moira — *natural beats Irish; Irishness lives in the writing.*

**State at End of Session**
- Fully operational backbone: brain, launcher, voice, git+GitHub, Linear, index
  feed. Deploy key on-drive (portable by design). No secrets committed (verified
  each commit).

**Next Session** (Sunday 2026-08-02 or Monday 2026-08-03, per Kam)
- [ ] Re-ask the daily-rhythm question (asked twice, unanswered) — then WED-6 queue
- [ ] WED-5 architecture doc once enough discovery answers accumulate
- [ ] WED-7 full projects sweep (good autonomous block)

**Suggested opening prompt for next session:**
> Launch via Launch_Wednesday.command (it does everything). If launching manually:
> you are Wednesday at /Volumes/KK_T9_External_HDD/WEDNESDAY — read CLAUDE.md,
> 0_Brain/ (all learnings), check Linear team WED, then pick up the daily-rhythm
> discovery question and the WED-6 queue.

---

## 2026-07-31 — Founding session

**Done:**
- Created the full project structure at `/Volumes/KK_T9_External_HDD/WEDNESDAY`
  (numbered folders per workspace convention + `0_Brain/` Obsidian vault).
- Brain seeded: routing `CLAUDE.md`, `identity/persona.md` + `voice-protocol.md`,
  `people/kam.md`, first learning (`parent-child-learning-model`), templates,
  `tasks/TASKS.md`, `projects_index/` (INDEX + feed spec).
- `Launch_Wednesday.command` — standalone adaptation of the standard launcher
  (per-project az/gh isolation, statusline, Fable 5 pin, full-brain boot ritual,
  spoken greeting).
- Voice v1: `2_Project_Files/voice/speak.sh` (Moira en_IE, non-blocking, logged,
  mutable, single seam for future TTS upgrade).
- Research (2 agent passes) filed in `1_Project_Definition/Discovery/research/`:
  Jared Rhodes' Jarvis system; 2025–26 second-brain/agent-memory best practices.
- Discovery pack: verbatim prompt log, distilled brief, 20 discovery questions.

**Open / next:**
- Kam to answer `1_Project_Definition/Discovery/02_discovery-questions.md` (by
  voice; Wednesday records answers inline).
- Draft architecture doc from the answers.
- First read-only sweep of DevMASTER projects to populate `projects_index/INDEX.md`.
- Decisions pending Kam: git repo or local-only; end-of-session skill change for
  the index feed; Agent Mail inbox model.
