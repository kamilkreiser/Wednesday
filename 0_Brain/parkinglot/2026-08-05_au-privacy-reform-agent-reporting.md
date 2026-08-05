---
date: 2026-08-05
mode: research      # Kam-confirmed 2026-08-05 at wrap: research, IN A NEW SESSION
status: open        # open | promoted | dropped — RESEARCHED 2026-08-05 (session 2), awaiting Kam read
source: "Kam, in-session (parking lot founding item)"
promoted_to: ""
---

# AU privacy regulation changing Dec 2026 — agent/client-data reporting

One-liner: Australian privacy regulation changes in December; organisations
will need to report when AI agents are interacting with client data;
Microsoft has already added this capability to Purview.

Facets:
1. What exactly changes in the Dec reform (which schedule/act, thresholds).
2. The agent-interaction reporting obligation — scope, who must report, when.
3. Microsoft Purview's new coverage — what it detects/reports, gaps.

Why it matters here: directly touches Datasec (compliance product angle?),
Secuura (agents on Platform K touch client documents), and Wednesday's own
fleet (agents interacting with client data is literally our architecture).

Research (run 2026-08-05, session 2 — full report w/ sources:
[[2026-08-05_au-privacy-research-report]]; first live run of the park-vs-research flow):

**Verdict on the one-liner: half right.**
- **TRUE — the date and the reform.** 10 December 2026: APPs 1.7–1.9 (from the
  *Privacy and Other Legislation Amendment Act 2024*, Sch 1 Pt 15) commence,
  plus the OAIC Children's Online Privacy Code.
- **FALSE — the "report when AI agents touch client data" framing.** There is
  NO reporting/logging obligation to anyone. The real duty is a
  **privacy-policy disclosure** of automated decision-making (any computer
  program, not just AI) that uses personal information and could significantly
  affect an individual's rights/interests. APP entities only (>A$3M turnover;
  small-business exemption survives — its removal is tranche 2: no bill, no
  date). Penalties via s 13K civil-penalty tier. OAIC guidance ~Sep 2026.
- **PARTLY TRUE — Purview.** DSPM AI Observability + Insider Risk Management
  for agents went GA mid-June–end-July 2026 (needs M365 E7 / Agent 365); the
  unified audit log captures agent prompts/responses. But it's generic AI
  governance, Microsoft-ecosystem-deep only, and its compliance assessments
  target EU AI Act/NIST/ISO — not the Australian rule.
- Adjacent: statutory privacy tort live since 10 Jun 2025 (applies at ANY
  size); mandatory AI guardrails shelved Dec 2025; "Australian Standards for
  AI" announced 15 Jul 2026 for early 2027 — announced, not law.

**Implications:**
- **Datasec — real product angle, deadline-driven.** ADM/AI discovery audits,
  privacy-policy uplift, Purview-for-agents deployments before 10 Dec 2026;
  demand spike expected after the OAIC guidance lands (~Sep). Datasec must
  also self-check its own tools (lead scoring, NexusAI flows) against the
  three-limb test.
- **Secuura — client-facing asset, not a vendor duty.** The obligation falls
  on Secuura's CLIENTS; OAIC expects entities to oversee third-party ADM →
  a disclosure pack (what Platform K decides vs assists, what personal data
  its agents touch) becomes a sales asset. Secuura's own policy needs the
  update only if it's an APP entity itself.
- **Wednesday's fleet — not caught.** Internal coding/ops agents make no
  rights-affecting decisions about individuals; small-business exemption
  likely applies anyway. Real exposures: the statutory tort (any size) and
  client contract flow-down. The fleet's agent inventory + logging discipline
  = cheap insurance, not a current legal duty.

**Proposed next step (Kam's call):** park until ~Sep 2026 (OAIC guidance),
THEN decide whether Datasec productises. If he wants the Datasec angle
explored sooner, promote to a ticket on their board via their agent.
