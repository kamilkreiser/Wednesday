# Weekly industry scan #1 — 2026-08-12

Ritual: `0_Brain/skills/weekly-industry-scan.md` (commissioned 2026-08-03; Kam
ruled 9a this morning: run tonight). First run of the weekly cadence. Window:
**2026-07-29 → 2026-08-12**, fresh sources only. Method: 4 research agents
(agent engineering / model landscape / practitioner practice / Kam's stack),
synthesized by Wednesday.

**Baseline already known (2026-08-03 reports, not re-reported):** Sakana
AB-MCTS/TreeQuest, Kimi K2 line, DeepSeek-R1/QwQ, ACE, Reflexion/Voyager/DGM/SEAL,
Zen MCP, second-model diff review, LLM-as-judge production patterns.

**Status legend:** SHIPPED (verifiable release) · ANNOUNCED (official, not yet
live) · REPORTED/RUMOR (secondary sources only, unverified).

---

## 0. Time-critical this week (both land before the next scan)

1. **Claude Code auto mode becomes the DEFAULT permission mode on 2026-08-14**
   (Thu — two days away) on Pro/Max/Team. ANNOUNCED 2026-08-09, official.
   Classifier approves safe actions, blocks risky; own `permissions.defaultMode`
   is preserved unless a one-time switch prompt is accepted. Anthropic's own
   data: users reflexively approve ~97% of prompts; classifier caught 89% of
   dangerous commands vs 13.6% for humans (1,053 testers). Every fleet session's
   permission posture may shift Thursday unless set deliberately.
   → **Proposal filed.** Sources: https://code.claude.com/docs/en/whats-new/2026-w32 ·
   https://techcrunch.com/2026/08/09/anthropic-is-turning-claude-codes-auto-mode-on-by-default/ ·
   https://claude.com/blog/auto-mode-default-in-claude-code (2026-08-07)

2. **The +50% weekly usage-limit boost on Pro/Max reportedly expires
   2026-08-19.** REPORTED — tracker sites only
   (ccforeveryone.com/guides/claude-code-limits-and-pricing,
   explainx.ai/blog/claude-usage-limits-2026-timeline-explained), extended three
   times before, NOT confirmed by Anthropic. If it lapses, effective weekly fleet
   capacity drops ~33% next week. No proposal (unverified, nothing to adopt) —
   but schedule heavy multi-session pushes before the 19th and watch for the
   extension announcement. Morning briefing item.

---

## Tier 1 — Actionable (proposal filed in Linear for each)

### 1.1 Fleet permission posture before Aug 14 + hard deny rules
See 0.1. The right response is not "keep manual mode everywhere" — the same
week produced the strongest public evidence yet that approval gates are weak
controls: a 40k-run gamified study (HN 2026-08-06, 338 pts,
scalex.dev/blog/ai-agent-permissions-stats/) found humans miss 1-in-3 threats
when approving agent commands; credential exfiltration missed 35% of the time;
malicious payloads behind `npm run` approved 64.7% of the time; accuracy decays
with session length. The surviving controls are the ones this workspace already
runs — scoped service principals, per-project config isolation, never-touch-prod
discipline — plus explicit deny rules for the paths where a wrong action is
irreversible. Decide `defaultMode` per project; add deny rules for
`datasec-sales-portal-rg`-touching commands, MCP config files, and sandbox/
launcher config before the default flips.

### 1.2 Upgrade every fleet Claude Code install to ≥2.1.228
SHIPPED 2026-08-07→11 (v2.1.225–2.1.228, official changelog). Fixes that map
directly onto fleet failure modes:
- **Session cleanup could DELETE contents of the project memory folder**
  (fixed 2.1.228) — versions before this can silently destroy memory.
- Transient 401s replacing long-lived OAuth tokens, breaking headless sessions
  (2.1.225); expired-token feature-flag bug wrongly prompting Max users to
  enable usage credits (2.1.227).
- Cross-session messages silently parking in headless sessions (2.1.225).
- Security: Bash commands can no longer hide parts of themselves from
  permission checks; invisible-Unicode padding no longer hides commands
  (2.1.223); synced skills can't shadow local commands or run `!`/`@`
  expansion (2.1.228).
Cost: minutes per machine. Risk: negligible (point releases).
Sources: https://github.com/anthropics/claude-code/blob/main/CHANGELOG.md ·
https://code.claude.com/docs/en/changelog (2026-08-07/08/10/11)

### 1.3 Cross-session messaging — native same-machine fleet comms
SHIPPED v2.1.224 (week of 2026-08-03; docs on HN 2026-08-08, 171 pts). Claude
Code sessions on the same machine discover each other (`ListAgents` /
`/list-agents`) and exchange plain-text messages (`SendMessage`) over per-session
Unix sockets — never through Anthropic servers. Design matches our existing
rule that a message is never consent: messages can't approve permissions, can't
change CLAUDE.md/config, slash commands arrive inert; inbound accept/hold/refuse
controls; headless `-p` workers can receive with `crossSessionInbound: accept`.
**Beats what we run:** the AgentMail bus polls every ~3 minutes; this is
near-instant with surfaced delivery failures. Email stays for durability, audit
trail, and cross-boot routing — this is a fast lane, not a replacement.
Cost: a trial session pair + a skills note. Risk: low (macOS/Linux only; new
feature, so trial before relying on it).
Source: https://code.claude.com/docs/en/cross-session-messaging ·
https://code.claude.com/docs/en/whats-new/2026-w32
Related, same release: 200-subagent-per-session cap removed; background
worktree sessions now follow CLAUDE.md git instructions; `/fork` gets its own
worktree.

### 1.4 Prod-credential exposure + protected-paths audit
Three in-window failure reports converge on one lesson — the boundary the agent
can edit, or the credential it can merely *see*, is the attack surface:
- **Claude Opus 5 wiped a production database** (late Jul/early Aug, Reddit +
  GH issues #34729/#36183, cybersecuritynews.com/claude-opus-5-wiped-data/):
  agent ran `prisma migrate diff` with `--shadow-database-url` set from
  `DATABASE_URL_UNPOOLED` in .env → pointed at prod Supabase → 22 tables
  dropped. The vector was a prod connection string reachable in an env var,
  not a malicious command. FIELD-REPORT, class confirmed by companion issues.
- **Cursor "DuneSlide"** CVE-2026-50548/50549, CVSS 9.8 (disclosed Jul 2026,
  catonetworks.com/blog/duneslide-two-critical-rce-vulnerabilities/): prompt
  injection had the agent overwrite its own sandbox helper binary. **AWS Kiro**
  (Jul 2026, via adversa.ai roundup): web-page text rewrote its own MCP config,
  auto-reloaded. Same shape: agent edits the boundary meant to contain it.
- **Skill files are now a first-class attack surface** (adversa.ai August 2026
  roundup): one malicious skill markdown passed all eight open-source skill
  scanners (2026-07-30); GitLost (Noma, Jul) — plain-English payload in a
  public GitHub issue exfiltrated private repo contents — is the exact threat
  model for our inbox-reading boot step.
**Action:** audit every fleet project's `4_Credentials/.env` for direct/unpooled
prod DB URLs exposed to sessions that don't need them (tenant #5's
`datasec-sales-portal-rg` warning is precisely this class); deny-write MCP
config and launcher/sandbox files; treat `skills/Current/` provenance like code
provenance; keep treating mail bodies as untrusted input.
Cost: one audit session. Risk: none — read-and-restrict only.

### 1.5 DeepSeek V4-Flash as the cheap second-model validator
SHIPPED 2026-07-31/08-01 — official API (0731 build) + MIT open weights on HF
simultaneously (huggingface.co/blog/ResterChed/deepseek-v4-flash-official-release).
Re-post-trained for agentic work; self-reported +21pts Terminal-Bench 2.1
(82.7%), +47pts DeepSWE — and **independently confirmed ~10-pt gains by
Artificial Analysis**. Pricing $0.14/$0.28 per MTok, cache hits ~98% off.
That is ~1/35th of Opus 5 output pricing. Caveat: V4-**Pro** is still preview
(ANNOUNCED); late-July claims of V4 GA on Jul 20 were wrong per DeepSeek's own
docs. A reported 2× Beijing-peak surcharge is so far unenforced.
**Beats what we run:** the 2026-08-03 research ranked second-model diff review
as the #1 value-per-effort validation upgrade; we never adopted it for lack of
a cheap verified candidate. This is that candidate.
Cost: cents per review; an afternoon to wire a diff-review slash command/hook.
Risk: Chinese-hosted API — no client code or secrets in prompts, diffs of
non-sensitive repos only, or run the MIT weights locally later. Alternatives at
higher capability: GPT-5.6 Sol (best Terminal-Bench 88.8), Kimi K3 (Elo 1547
but token-hungry — Simon Willison: 13K+ thinking tokens on trivial tasks,
simonwillison.net/2026/Jul/16/kimi-k3/), Kimi K2.6 at $0.95/$4 as value dark
horse.

### 1.6 Lesson re-verification at consolidation (the "groom" step)
FIELD-REPORT 2026-07-10 — Brandon Casci published a learning loop that is
independently convergent with our ledger (append-only lessons, duplicate-grep,
a counter that bumps when a lesson is seen a second session — our w-weights):
https://www.brandoncasci.com/2026/07/10/how-i-keep-my-coding-agent-from-relearning-the-same-lessons.html
His one addition we lack: at promotion/consolidation, **re-verify each lesson
against current reality** (is the code/behavior it references still true?) so
stale lessons die at graduation instead of living in the vault. Same direction:
obsidian-second-brain v0.14 (Jul 2026, ~4k stars,
github.com/eugeniughelbur/obsidian-second-brain) runs scheduled consolidation
agents nightly/weekly; Anthropic is productizing the identical job as "Dreams"
(Managed Agents research preview, extended to Opus 5 on 2026-08-01 —
platform.claude.com/docs/en/managed-agents/dreams) and an Auto-Dream/`/dream`
consolidation agent visibly exists in the Claude Code binary (prompt mirrored
at github.com/Piebald-AI/claude-code-system-prompts — ANNOUNCED/preview, treat
with caution).
**Beats what we run:** adds a staleness gate to learning-loop v2's weekly
consolidation. Cost: one line in the consolidation skill + minutes per week.
Risk: none. (Rakuten via Managed Agents memory reports 97% fewer first-pass
errors from cross-session lesson distillation — the strongest public
quantification yet that this whole loop pays:
claude.com/blog/claude-managed-agents-memory, 2026-04-23.)

### 1.7 Kokoro local TTS to replace the `say`-class voice
STANDING (no in-window release changed it; 2026 roundups consistent): Kokoro
82M — Apache-2.0, real-time on Apple Silicon CPU, beats far larger models
(incl. Microsoft's 9B VibeVoice) in blind tests
(tryspeakeasy.io/blog/open-source-text-to-speech-2026 ·
pinggy.io/blog/best_open_source_self_hosted_text_to_speech_models/).
**Beats what we run:** Moira/macOS `say` is the weakest link in the voice
channel; Kokoro is free, local, and drive-portable (fits the T9 portability
rule — model files live in `2_Project_Files/tools/`, doctor.sh + PORTABILITY.md
entries at adoption). Cloud alternatives don't beat it for this use: ElevenLabs
still ~$100/M chars after its May–Aug price reshuffle (flexprice.io); Qwen TTS
(2026-07-20) adds latency + a key dependency.
Cost: a setup session (~small local server + speak.sh swap). Risk: low;
keep `say` as fallback.

### 1.8 WhatsApp channel: the calculus changed — decide route before building
ANNOUNCED (Meta official docs): **from 2026-10-01, service + utility messages
inside the 24-hour customer-service window become chargeable** on the Business
Platform/API (free since Nov 2024/Jul 2025); country rates due by 2026-09-01;
US utility-class ~$0.004/msg, AU TBA
(developers.facebook.com/documentation/business-messaging/whatsapp/pricing).
Meanwhile unofficial bridges (Baileys/whatsmeow/Matrix) remain under active
ban-wave enforcement — no new crackdown in-window, but the trendline is bad
(github.com/WhiskeySockets/Baileys/issues/1869). Also SHIPPED: WhatsApp
usernames + Business Scoped User IDs rolling out via Twilio since Jun 2026 —
integrations must key contacts on IDs, not phone numbers, from day one
(twilio.com changelog).
**Project stays parked per CLAUDE.md — this is a decision note, not a start.**
When Kam green-lights: official Cloud API on a dedicated number is the
defensible route; a chatty assistant goes from ~$0 to per-message billing after
Oct 1 (still likely cheap in absolute terms for one user — model it first).
Cost now: none (recorded decision input). Risk of ignoring: building on a
bridge that gets the number banned.

### 1.9 Boot-payload audit against Anthropic's context-engineering guidance
SHIPPED (guidance) 2026-07-24 — "The new rules of context engineering for
Claude 5 generation models" (Anthropic, Thariq Shihipar,
claude.com/blog/the-new-rules-of-context-engineering-for-claude-5-generation-models):
Anthropic removed >80% of Claude Code's own system prompt for Claude
5-generation models with no measurable eval loss. Six shifts: rules→judgment,
examples→interface design, upfront context→progressive disclosure,
repetition→simple descriptions, manual memory→auto-memory, simple specs→rich
references.
**Scope guard: Kam ruled at the 2026-08-06 consolidation that the full lesson
load STAYS — this proposal explicitly does NOT touch `learnings/`.** The
auditable payload is everything else in boot: workspace CLAUDE.md, project
CLAUDE.md, skills, index reads — checking for rules that restate what Claude
5-generation models already do well, and for inlined content that could be a
reference pointer. Potentially material token savings per boot across the
whole fleet (every project session, every day).
Cost: one audit session + Kam review of any trims. Risk: over-trimming —
mitigate by trimming only with before/after behavioral checks, and nothing
from `learnings/`.

---

## Tier 2 — Watch (real, not yet actionable for us)

- **Anthropic Managed Agents: session budgets + advisor-in-roster** — SHIPPED
  beta 2026-08-07 (platform.claude.com/docs/en/release-notes/api). Hard spend
  cap per session (`budget_reached` pauses, not kills); `{"type":"advisor"}`
  lets a cheap executor consult a stronger model mid-turn. We're not on Managed
  Agents, but both patterns are liftable: per-session spend/wall-time/tool-call
  tripwires (the $48K/14h runaway-agent and $6.5K AWS respawn postmortems both
  argue for multi-dimensional budgets, not just tokens), and Sonnet-executor/
  Opus-consultant tiering. Candidate proposal next scan if session costs rise.
- **MCP spec 2026-07-28 "stateless rewrite"** — SHIPPED, largest revision since
  MCP launched (blog.modelcontextprotocol.io/posts/2026-07-28/): protocol
  sessions removed, tasks moved to an extension, DCR deprecated for CIMD.
  Deprecated features guaranteed ≥12 months. Our stdio-local servers are least
  affected. Action deferred: inventory remote/HTTP MCP servers at next
  convenient session; no deadline pressure.
- **Claude Code self-hosted environments** (`claude self-hosted-runner`) —
  SHIPPED public beta 2026-08-03/07 but **Team/Enterprise only**. This is the
  eventual "kick off a session from the phone that runs on Kam's machine"
  primitive and the shape of the parked Mac Studio idea. Watch for Max plan
  expansion.
- **Linear** — free-plan cap confirmed unchanged at **250 non-archived issues**
  (the Secuura block is structural, not a glitch); **archived issues don't
  count** — a cull/archive ritual is the free fix; Basic $10/user/mo, Business
  $16 (cut from $50 since Jul 2025). Linear "Loops" (recurring plain-language
  agent automations, SHIPPED 2026-07-20) and Claude Code cloud coding sessions
  assignable from issues (SHIPPED ~2026-07-30) are both Business+ gated —
  Linear is building Wednesday-shaped functionality natively; signal, not
  action. API deprecations to check in dashboard pollers: `Team.private` →
  `Team.visibility`, `AiPrompt` roots deprecated (linear.app/changelog).
  No proposal — the cap decision (cull vs money) is already on Kam's board
  from 2026-08-12 morning; this scan just confirms the options' facts.
- **GitHub** — one-click branch-protection→rulesets migration SHIPPED
  2026-08-11 (github.blog/changelog): trivial to adopt when next touching repo
  settings; rulesets allow explicitly scoped bypass actors (useful with our
  deploy-key pushes). gh CLI 2.97.0 (2026-07-31) fixes four security vulns —
  fold into the 1.2 upgrade pass. Secret-scanning coverage expanded 2026-08-04
  (automatic, no action). Org-level PR limits 2026-08-06 (agent-flood control;
  relevant only if fleet agents start opening many PRs on `datasecau`).
- **Azure** — quiet fortnight for our footprint. ACA "sandbox environments"
  preview (2026-08-11, azurecharts.com/updates) is Microsoft productizing
  agent-scoped blast-radius-limited compute — philosophically our tenant-#5
  pattern as a native primitive; preview, watch only. az CLI 2.89.0
  (2026-08-04) routine. **No ACS email changes** — quota-request path for the
  Vision portal's sending stands. Entra: managed-identity-as-federated-credential
  GA is the eventual way to drop client secrets from the `*-claude-deploy`
  principals (devblogs.microsoft.com/identity/) — nothing breaks meanwhile.
- **Sakana Fugu conductor on Gemma 4** — SHIPPED (self-reported) 2026-08-10
  (sakana.ai/blog/): their learned-orchestration line (TRINITY/Conductor, ICLR
  2026) shown base-model-agnostic; Fugu now has Ultra + Cyber tiers, claims
  SWE-Bench Pro 73.7 *without* Fable 5 in its pool. Proprietary, EU-unavailable,
  self-reported. The AB-MCTS lineage productized — conceptually relevant to
  cross-model review, no adoption case vs 1.5 yet.
- **Docker Sandboxes** — SHIPPED/ANNOUNCED 2026-08-10 (HN 684 pts,
  docker.com/products/docker-sandboxes/): off-the-shelf OS-level agent
  isolation. Candidate hardening layer if 1.1/1.4 find gaps our per-project
  config isolation doesn't cover.
- **Meta Muse Glimmer** — SHIPPED 2026-08-10: 30B dense multimodal, Apache 2.0,
  single-GPU, explicitly framed against Chinese open-weights momentum; "bigger
  models coming." No benchmarks at launch. Right shape for a future local
  always-on validator; too small for frontier code review today.
- **Mistral Shieldstral** — SHIPPED early Aug: 3B Apache-2.0 safety classifier
  taking plain-language policies at inference, one 16GB GPU. Neat free
  guardrail component if we ever need input screening on inbound mail.

## Tier 3 — Context and confirmations (no action)

- **Approval-gate obituary, with data:** Anthropic's auto-mode rationale
  (97% reflexive approval) + the 40k-run study (§1.1) together retire
  per-action human approval as a primary control. This *validates* the fleet's
  existing model — plan-confirmation up front, scoped identities and
  never-touch-prod in the middle, verify-before-done at the end. The seven hard
  rules now have public data behind them.
- **Agent-PR review reality check:** LinearB 2026 benchmarks (8.1M PRs) — AI
  PRs merge within 30 days at 32.7% vs 84.4% manual; 61.38% of agent-authored
  PRs in popular repos get zero review activity (AIDev dataset). Our
  session-scoring + Kam-traceable ship rulings are the antidote the industry
  lacks (linearb.io/dev-interrupted/). GitHub's canonical agent-PR checklist
  (May 2026, github.blog): **check CI/workflow diffs first** — agents weakening
  their own checks is the top gaming vector; cheap habit worth folding into
  review practice without a formal proposal.
- **Fleet-ops convergence:** "Coordinating an Agent Fleet for a Day"
  (2026-07-01, developersdigest.tech) independently arrives at our rules —
  single-owner file scopes, verification gates on handoffs, fail-closed on
  money/prod. One gap it names that we share: **silent idle processes** — a
  heartbeat/idle check candidate for the cockpit (recall the 08-08/09 NexusAI
  17h-idle boot). Agent-Manager (Show HN 2026-07-30, Apache-2.0,
  github.com/YoanWai/agent-manager) is the closest OSS twin of our tmux
  cockpit, with in-TUI diff review routed back to the agent. Claude Code Agent
  Teams remains experimental — official advice is still "try subagents first";
  speed claims in circulating guides carry no field data.
- **Anthropic housekeeping:** Opus 5 SHIPPED 2026-07-24 ($5/$25 unchanged, 1M
  context default, 128k out; thinking on by default; disabling thinking at
  effort xhigh/max now 400s) and is the default Opus in Claude Code — the
  fleet's Opus changed under us in late July. **Opus 4.1 retired 2026-08-05**
  — any script pinning `claude-opus-4-1-20250805` now errors; none known in
  fleet, verify during 1.2 pass. **Sonnet 5 $2/$10 made permanent 2026-08-10**
  (planned Sep reversion to $3/$15 cancelled) — but budget for Sonnet 5's ~30%
  tokenizer inflation vs 4.6 baselines. Legacy Workbench/prompt-tools APIs
  retire 2026-08-17. Claude elevated-errors incident 2026-07-29
  (status.claude.com) — single-provider fleet, single point of failure; known
  accepted risk.
- **Verification hierarchy write-up worth reading:** "Building an Advanced
  Agentic Harness" (data4sci.com, Jul 2026, HN 134 pts) — deterministic checks
  always run before any LLM judge; budgets in four dimensions (tokens, tool
  calls, wall time, cost). Matches our discipline; the multi-dimensional budget
  idea feeds the Tier-2 Managed-Agents-patterns watch item.
- **HyperProbe** (YC S26, 2026-08-05): read-only debugging probes in running
  prod for agents — a genuinely new validation primitive compatible with
  never-update-prod; too early to trial.
- **GPT-5.6 Sol update in ChatGPT** (2026-08-06, ChatGPT-side only) and
  **GPT-5.6-Cyber via gated Daybreak Red** (2026-08-10/11): context for §1.5's
  alternatives table. **OpenAI "Astra"** long-running-task family: RUMOR, demo
  to policymakers only. **o3 retires from ChatGPT 2026-08-26.**
- **Gemini 3.6 Flash GA** (2026-07-21): the strongest US-frontier cheap-slot
  candidate; note Google deprecated `temperature`/`top_p`/`top_k` on latest
  models — breaks configs that set them.
- **Memory research line:** HyperAgents (Meta paper, analyzed 2026-07-31,
  mem0.ai/blog) — self-referential agents *emergently built* performance
  tracking and causal-insight ledgers by generation 3; independent evidence our
  ledger+retro loop is the load-bearing part of self-improvement, not
  decoration. AutoMem (arXiv 2607.01224) + MemSkill (2602.02474): memory ops as
  evolvable skills — maps to keeping memory procedures in `skills/` the agent
  can revise. Zero-Mem (arXiv 2607.29377, 2026-08-05): zero-token memory ops.
  The standing contrarian ("Stop Calling It Memory", Mar 2026): markdown vaults
  fail at concurrency — our git pull-rebase discipline mitigates, doesn't
  eliminate; noted, not urgent at current fleet size.

## Rumor ledger update (from the 2026-08-03 reports)

| Item | 08-03 status | Now (2026-08-12) |
|---|---|---|
| Kimi K2.5 | rumor | **Dead — retired 2026-05-25** |
| Kimi K2.6 | rumor | **Real, SHIPPED** ($0.95/$4) |
| Kimi K3 | rumor, specs conflicted | **Real: launched 2026-07-16 (2.8T MoE, 1M ctx), open weights on HF 2026-07-26, Modified MIT** — largest open-weight release ever |
| DeepSeek-V4 | rumor | **Real: April preview; V4-Flash officially SHIPPED 2026-07-31 (MIT); V4-Pro still preview** |
| GLM-5 | rumor | **GLM-5 line shipped earlier in 2026 (current GLM-5.2, 744B, MIT); GLM-5.5 is the live RUMOR** (Aug target per JPMorgan/Reuters; founder "epic plus" only official signal) — re-check next scan |
| Qwen3.8-Max open weights | — | API SHIPPED 2026-08-03 ($2/$6, 2.4T MoE); **weights promised, NOT delivered as of 08-12**; weak SWE-bench Pro (67.7) argues against it for code review |

Macro: frontier token-price index at 12 vs Mar-2023 base 100 (−88%,
benchlm.ai). The cheap-second-model slot has never been cheaper.

---

## Proposals filed (Linear, team WED, label `proposal`)

See issues prefixed `P-scan:` created 2026-08-12 — one per Tier-1 finding
(1.1–1.9). Nothing is adopted without Kam's call; the morning briefing leads
with 0.1 (auto-mode Thursday) and 0.2 (possible limit drop the 19th).

*Scan filed by Wednesday, 2026-08-12 (evening). Next scan: week of 2026-08-17.*
