# WEDNESDAY — session history (newest at TOP)

---

## 2026-08-04 — Rhythm day: wednesday-agent@ live, fleet convention switched, scheduler installed, two code reviews

**Accomplished**
- **First delegation SCORED:** Secuura 08-04 wrap closed the loop on my 08-03
  instruction email — brief executed end-to-end, scoreboard entry 1.0. Four
  wrap emails routed (Secuura + NexusAI × 08-03/08-04); the Step-2d feed works.
- **WED-8:** secure_test deleted (inspected first), wednesday@ taken platform-
  wide → Kam chose **wednesday-agent@agentmail.to**; created + round-trip
  verified both directions. Remaining: Kam's plan upgrade only.
- **Fleet convention switched** (Kam named go-ahead): workspace CLAUDE.md +
  vault Step 2d wraps → wednesday-agent@ (coagent@ fallback); vault 3c5f41f.
  My launcher checks both inboxes at boot.
- **Orchestrator-adws repo reviewed** (Kam's commission → WED-39): survey agent
  + source validation. 8 adoptions / 5 rejections;
  `0_Brain/reference/tac-course/orchestrator-adws-code-review.md`, mirrored to
  Wednesday Notes. WED-42 blueprint identified (summaries-firewall +
  completion-oracle monitoring). Their PASS/FAIL substring parse is buggy —
  ours uses a structured VERDICT line.
- **WED-16 daily rhythm BUILT + INSTALLED:** launchd pair (06:00 wake → normal
  launcher with morning-wake marker; 23:00 close → deterministic note-stamp +
  inbox snapshot + spoken good night), idempotent installer, PORTABILITY #12.
  All components verified; Mac never sleeps. **Supervised pilot: tonight 23:00
  + tomorrow 06:00.** Issue stays In Progress until evidence reviewed.
- **Coordination harness code-reviewed** (Kam's commission): 3 HIGH — uncaught
  verifier timeout (FIXED), seats cwd=drive-root context/secrets surface
  (FIXED → seat_scratch/), unsandboxed generated-code execution (accepted risk,
  precondition for break-glass use). Artifacts hygiene fixed (gitignore +
  untrack). Smoke re-verified green post-fix (gpt 1.0, 11.7s).

**Learning loop**
- Ledger w=2: artifacts-not-gitignored-at-creation (Codex binary 08-03 + pyc/
  pkl 08-04, same commit). Lesson filed incl. the meta-rule: retro candidates
  that matter become FILES same-session — un-filed candidates don't fire.
- Workflow candidates: self-review pass at wrap for code-shipping sessions;
  meta_prompt house format for briefs/skills.

**Next session:** WED-16 pilot evidence FIRST (scheduler logs), then WED-42
seamless integration v1 in a fresh window (blueprint on disk). Kam outstanding:
Agent Mail plan upgrade, RD-64 confirm, Secuura decisions, Release-Ready pile.

---

## 2026-08-03 — The compounding day: learning loop v2, TreeQuest→harness, first delegation, full TAC course

**Accomplished**
- **Learning loop v2 designed, Kam-approved, and implemented same day** — with
  Kam's own design change: frequency-weighted correction ledger (w=1 isolated /
  w=2 reinforced+diagnose / w≥3 regression+promote). Session retro in every
  wrap; weekly consolidation ("dreaming") + weekly industry scan rituals;
  `lesson` Linear label = async teaching channel. Ledger took its first two
  honest entries the same day.
- **Two-schools research** (Sakana AB-MCTS · Chinese iterate-over-scale) →
  synthesis: *repetition against a VERIFIER is the magic*. Four proposals
  (WED-20–23) — all approved by Kam.
- **TreeQuest: download → full core read → working multi-model coordination
  harness in ONE day** (`2_Project_Files/coordination/`: ABMCTSA over
  subscription seats gpt/claude/haiku, unittest verifier, checkpoints, priors).
  Day-3 finding, honestly reported: 4 runs, tree never branched — 2026 models
  one-shot well-specified katas; search = break-glass insurance, empirically.
  Coordination Protocol v1 (8 rules) + delegation-protocol skill + channel
  scoreboard shipped.
- **ChatGPT seat live** (Codex CLI on-drive, CODEX_HOME in 4_Credentials, Kam
  logged in, verified). `wednesday` terminal command registered.
- **First real delegation executed** (Secuura decisions-sitting + KS-538
  cross-model pilot): briefs Kam-reviewed, instructions delivered by EMAIL to
  the inbox their boot ritual reads, session launched by Wednesday via `open`
  — Kam removed from the relay by his own design. Their agent VERIFIED the
  email rather than trusting it and caught my stale DRAFT line (fleet culture
  working). **Email adopted as the fleet channel**: workspace CLAUDE.md fleet-
  comms section + vault end-of-session Step 2d wrap-email (commit 09dc86a).
- **Board awareness live** (WED-28): read-only grant recorded; first sweep of
  all trackers (Jira CPKEY/MYP/RD + Linear KS/PS/WED) → boards digest +
  aggregated Kam decision queue. Found: NexusAI aging security pair (RD-55/54),
  6-ticket Release-Ready stack, myPKI confirmed deliberately parked.
- **Entire TAC course (14 lessons) + all codebases captured and reviewed** via
  a self-built pipeline (DRM'd Mux video, but subtitle tracks = transcripts;
  documented in HOW-TO-HARVEST.md). Notes + adopt/reject verdicts filed both
  sides. Deployment plan → WED-29…38. Adopted: KPIs, work-class templates,
  health checks, ADW structure, orchestrator three-pillar spec, agent-expert
  mental-model discipline (Kam-endorsed). Refused: ZTE-to-prod, yolo
  workflows, dropping review, presence-to-zero as universal.
- **Kam's evening directive batch** → WED-39…46: 9-14 code deep-play, workflow
  lanes, Peter-testing bottling, seamless-integration v1 (Urgent), security+
  privacy+QC gatekeeper expertise models, stakeholder comms, visual fleet
  dashboard.

**Decisions Made**
- Daily rhythm: **wake 06:00, close 23:00** (WED-16, now Urgent) — *matches
  Kam's working day.*
- Ledger is frequency-weighted — *"frequency is reinforcement", Kam's design.*
- Email = fleet inter-agent channel for now; direct ping later — *works today,
  auditable, mount-independent.*
- Context loading: **full for Wednesday AND sub-agents** (tokens are not the
  constraint); "narrow" = agent SCOPE on complex tasks; selective loading is a
  situational lever — *corrected from my misread, ledger entry 1.*
- Brain = mental model, NOT source of truth — read → validate vs live source →
  act → fix model. *Kam-endorsed from TAC lesson 13.*
- No DB for expertise files (files-in-repo, 1000-line cap, self-improve
  pattern); DB belongs to the orchestrator runtime — *verified from source.*
- Role explicitly broader than code: personal, two kids, ideas-to-reality —
  *~60% of Kam's work is code; 0% of the relationship is only code.*
- myPKI deliberately parked; CoAgent app not extended internally (fleet feed
  instead); Anthropic-native preferred for integration approaches.

**State at End of Session**
- Operating system fully live: learning loop + ledger + retro (first one
  written tonight) + rituals; delegation protocol + scoreboard; fleet email
  channel wired both directions; board sweep mechanism; coordination harness
  tested; course knowledge base on both drives. One delegation in flight
  (Secuura — first wrap email expected). wednesday@ inbox blocked on a
  ten-second Kam decision (WED-8). No secrets committed (verified).

**Next Session** (2026-08-04)
- [ ] Boot: expect FIRST Step-2d wrap email from Platform K → score it
- [ ] Light consolidation pass (today created half the brain)
- [ ] WED-39 code deep-play (agent-experts + orchestrator, fresh context)
- [ ] WED-42 seamless integration design (Urgent; interim brief rule active)
- [ ] WED-41 Peter testing analysis
- [ ] Kam: WED-8 inbox decision; WED-16 scheduler now Urgent

**Suggested opening prompt for next session:**
> Launch via `wednesday` (new terminal command) or Launch_Wednesday.command.
> Boot ritual covers everything; expect the first project wrap-email in
> coagent@; then WED-39 (9-14 code deep-play) and WED-42 per the 08-03 handoff.


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
