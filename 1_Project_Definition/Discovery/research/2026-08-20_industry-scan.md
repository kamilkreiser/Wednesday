# Weekly industry scan — 2026-08-20 (window 2026-08-06 → 2026-08-20)

Ritual per `0_Brain/skills/weekly-industry-scan.md`. Three research agents fanned
out (agent engineering · model landscape · practice + stack); this is the ranked
synthesis. **Ranked by actionability for us, not noise level.** Every finding
carries its publication date + source; SHIPPED vs ANNOUNCED distinguished.
Proposals filed to Linear (label `proposal`) — nothing adopted without Kam.

---

## TIER 1 — acts on us whether we act or not

### 1. Claude Code made AUTO MODE the default permission mode (2026-08-14) — SHIPPED
Sources: code.claude.com/docs/en/whats-new/2026-w32 · aipricing.guru 2026-08
New sessions on Pro/Max/Team default to auto mode (classifier-approved actions run
without prompts) unless `permissions.defaultMode` is pinned. **Every fleet launcher
session started after Aug 14 may be running a permission posture nobody chose.**
→ **Proposal WED (P1): audit every launcher/project settings file and PIN the
permission mode per project** — explicitly chosen, per client, with the Vision
prod RG and money-class surfaces in mind. Cheap, and the alternative is an
inherited default on client infrastructure.

### 2. The AgentMail outage was PLATFORM-WIDE (2026-08-18→19/20) — INCIDENT, resolved
Source: status.agentmail.to — "Email sending is down", opened 08-19 01:45Z.
Send-path uptime degraded to 99.627%; APIs/receive stayed up. Matches our
"MAIL SEND DOWN" exactly: provider-side, not our account (the error text blamed
"your AWS account" — misleading; it was their AWS). Restored by ~21:40Z 08-19
(our probe). **The fleet was un-launchable for ~14 hours because one vendor's
send path is our only delegation channel.**
→ **Proposal (P2): standing fallback for the mail channel** — (a) the rule I put
in today's s49 brief becomes template: on send-403, agents write the wrap/question
to their own 5_Project_History and hold at prompt (I watch panes); (b) my boot
probes the send path (done today, keep); (c) status.agentmail.to joins the outage
diagnosis path before any account-side theory.

### 3. Claude Code v2.1.224–235 shipped fleet-relevant mechanics (Aug 3–18) — SHIPPED
Sources: code.claude.com/docs/en/whats-new/2026-w32 · releasebot.io changelog
- **Native session-to-session messaging** (ListAgents/SendMessage, same machine;
  @-mention by name in v2.1.234) — a first-party alternative to polling mail.
- **Auto-continue when the usage-limit window resets** (v2.1.234) — removes the
  "session died at limit overnight" failure class.
- Hardening: worktree isolation covers Bash/git escapes; hidden-command padding
  closed; hook-bypass closed; GitLab token redaction; memory cgroup limits.
→ **Proposal (P3): upgrade the fleet to ≥v2.1.234 and trial SendMessage as a
SUPPLEMENT to the mail bus** (latency: ~instant vs ~1-min watcher). Mail stays
the channel of record — it carries the audit trail, works cross-machine, and
survives session death; SendMessage would carry only "check your inbox" nudges,
replacing tmux pane taps (which have a ledgered failure history: typing guards,
ghost text, unsent lines). Evaluate, don't switch.

## TIER 2 — cheap wins, our call

### 4. Sonnet 5 intro pricing made permanent: $2/$10 per MTok (2026-08-10) — SHIPPED
Source: releasebot.io/updates/anthropic/claude-developer-platform
The Sept-1 rise to $3/$15 is cancelled; Sonnet 5 (1M context) stays ~2.5× cheaper
than Opus-tier. → **Proposal (P4): route routine mechanical lanes (index refresh,
mail triage, dashboard collectors, scan fan-outs) to Sonnet 5.** Fable/Opus stays
for judgement lanes (reviews, briefs, verification). Guard: only lanes where a
wrong answer is cheap and checkable.

### 5. Forged-authority research (aiAuthZ, arXiv 2607.05518) + our own subject-line routing
Refusal of forged-authority attacks across 15 models ranged 100%→38%. Our routing
IS a plain-text subject convention any sender could forge; DKIM checks currently
gate approval-class only. → **Proposal (P5): one-line fleet protocol addition —
agents verify the SENDER (`wednesday-agent@agentmail.to` + auth headers) on every
brief/ANSWER, not just approval-class mail.** Near-zero cost; the shared-bus
tag-filter lesson's sibling. (Full HMAC-in-body is the paper's pattern — hold
unless evidence of need.)

### 6. Practitioner convergence on gating agent code (O'Reilly 06-26 · Northflank 08-14)
Risk-tiered review depth · evidence bundles (intent, test output, execution proof)
before human review · CI gates for removed tests / lowered coverage. Our wrap
culture already demands evidence; the **no-test-deletion CI gate** is the piece we
don't systematically have. → Fold into P5's protocol note as a brief-template
line for projects with CI; no separate machinery.

## TIER 3 — update the mental model, no action now

- **Local models (parked item, refresh it):** Qwen3.8-27B (Aug 14, Apache 2.0,
  ~17GB Q4) is the new local-background-tasks candidate — near-frontier agentic
  scores on 24GB-class hardware. **Kimi K3 superseded K2 but does NOT fit a 512GB
  Mac Studio** (smallest quant 567GB) — retire the K2 note. GLM-5.3 weights land
  ~end-Aug (staged). DeepSeek hiked API prices up to 1,100% peak (Aug 16) — the
  free-Chinese-API era is over; flat-cost Claude Max looks better, open weights
  are the hedge.
- **WhatsApp Business API bans general-purpose AI assistants** (in force since
  2026-01-15). The parked "Wednesday WhatsApp channel" cannot be built naively on
  the Business API — needs a task-specific framing or a different channel
  (Signal/Telegram/iMessage). Update the parked item; decision only when Kam
  reopens it.
- **OAIC ADM guidance still on track ~Sep 2026** (obligation bites 10 Dec). No
  movement this fortnight. Matches the parking-lot item's re-look date exactly.
- **"Founders Hub" branding retired** → program now "Microsoft for Startups"
  ($5K self-serve / $100–150K investor-backed). Check WED-116's guide wording +
  the Secuura credit expiry under the renamed program.
- **Context engineering guidance from Anthropic (07-24):** "thin prompts, thick
  artifacts" — validates the full lesson-load boot; the free trim is boot text
  that restates harness behaviour, not lessons. Feeds the standing boot-cost
  review at consolidation.
- **Anthropic Admin API GA · MCP 2026-07-28 spec · Opus 4.1 retired Aug 5** —
  grep launchers for stale model pins (quick audit rides with P1).
- **Incidents (AISI 08-04; Anthropic/Irregular 07-30):** agents exceeded scope /
  escaped an eval sandbox. The lesson we already run: containment lives in scoped
  identities + egress control, not agent obedience. Re-affirms the per-project SP
  design; no new action.
- **GitHub:** Agent Plugins 1.0 GA (08-12); hosted-runner prices down ~39% since
  Jan; self-hosted platform fee still shelved. Gemini 3.7 Flash (08-13, $0.75/$3.75
  intro) is the cheap-subagent reference point. **Fable 5.1: rumor only — no model
  ID, nothing to act on.**

---

**Scan TL;DR for Kam:** two things are already acting on us — auto mode became
Claude Code's default on Aug 14 (we should pin permission modes per project,
deliberately), and the mail outage that froze the fleet this morning was
AgentMail-platform-wide, arguing for the fallback-wrap rule I've now put in
briefs. The cheap wins: Sonnet 5's $2/$10 is permanent (route mechanical lanes),
native session messaging could replace pane taps, and a one-line sender-check
closes a real forged-authority gap. The parked WhatsApp channel needs a redesign
(Business API bans general-purpose assistants), and the local-models note should
now read Qwen3.8-27B, not Kimi-K2.
