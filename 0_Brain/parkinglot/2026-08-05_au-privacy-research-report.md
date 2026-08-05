# Australian Privacy Reform (Dec 2026), AI-Agent "Reporting", and Microsoft Purview — Verification Report

**Date:** 2026-08-05
**Prepared by:** Wednesday research agent (web research, read-only)
**Claim under test:** *"Australian privacy regulation changes in December; organisations will need to report when AI agents are interacting with client data; Microsoft has already added this capability to Purview."*

---

## Verdict at a glance

| Claim component | Verdict |
|---|---|
| "Australian privacy regulation changes in December [2026]" | **TRUE** — new APPs 1.7–1.9 (automated decision-making transparency) commence **10 December 2026**; the Children's Online Privacy Code must also be registered by that date. |
| "Organisations will need to report when AI agents are interacting with client data" | **INACCURATE as framed.** There is **no reporting, logging, or recording obligation** for AI-agent interactions with personal/client data. The real obligation is a **privacy-policy disclosure** about automated decision-making (ADM) that could significantly affect individuals' rights or interests. Nothing is reported to the OAIC or to individuals. |
| "Microsoft has already added this capability to Purview" | **PARTLY TRUE, but not for this law.** Purview now audits/observes AI-agent interactions (DSPM AI Observability + Insider Risk Management for agents reached GA mid-June–end-July 2026; the unified audit log captures agent prompts/responses). But this is a general AI-governance capability — it was not built for, and is not required by, the Australian ADM obligation. Its Compliance Manager AI assessments target EU AI Act / NIST AI RMF / ISO, not APP 1.7. |

---

## 1. What exactly changes in December 2026

### Instrument and commencement

- **Act:** *Privacy and Other Legislation Amendment Act 2024* (Cth), No. 128 of 2024 ("POLA Act") — the **first tranche** of the Privacy Act Review reforms (implementing 23 of the 116 review proposals). Royal Assent **10 December 2024**. It amends the *Privacy Act 1988* (Cth). [legislation.gov.au C2024A00128]
- **The December 2026 piece:** **Schedule 1, Part 15 — "Automated decisions and privacy policies"** — commences **10 December 2026** (24 months after Assent, per the commencement table). It inserts **new Australian Privacy Principles 1.7, 1.8 and 1.9** into APP 1 (open and transparent management of personal information), plus s 13K(1)(b)(iia) making non-compliance a civil-penalty matter.
- Everything else in the POLA Act is already in force — notably the **statutory tort of serious invasion of privacy (from 10 June 2025)**, tiered civil penalties (up to A$50M / 3x benefit / 30% adjusted turnover for serious interferences), anti-doxxing offences, and expanded OAIC enforcement powers.
- **This is NOT a new "tranche 2".** Tranche 2 (fair-and-reasonable test, removal of the A$3M small-business exemption, right to erasure, expanded "personal information" definition, DPO-style role) was confirmed as "progressing" by Attorney-General Michelle Rowland at Senate estimates in **February 2026**, but as of August 2026 **no Bill exists and no date is set**. The Productivity Commission has been publicly critical of parts of it.

### Who is covered

- **APP entities only**: Commonwealth agencies and private organisations with **annual turnover above A$3 million**, plus always-covered categories regardless of turnover — health service providers, businesses trading in personal information, Commonwealth contractors, and (since **1 July 2026**, via the separate AML/CTF Tranche 2 expansion) 100,000+ newly captured reporting entities (real estate agents, lawyers, conveyancers, accountants, dealers in precious metals/stones) for their AML/CTF-related data handling.
- **The small business exemption (< A$3M) still stands** for the ADM obligation — it does not by itself pull exempt small businesses into the Act.
- The obligation applies to ADM systems **already deployed before 10 December 2026** — the privacy policy must be accurate on day one.

### Also landing 10 December 2026

- The OAIC's **Children's Online Privacy Code** (required to be registered by 10 Dec 2026; exposure draft consulted through mid-2026).
- (Separately, the DTA's whole-of-government AI policy hits full mandatory compliance for Commonwealth agencies in December 2026 — public sector only.)

## 2. The actual "AI agent" obligation — ADM transparency (APPs 1.7–1.9)

### What it is

A **transparency-only** measure: certain information about ADM must appear in the entity's **privacy policy**. Three-limb trigger (APP 1.7):

1. **Responsibility:** the entity has *arranged for* a computer program to make, or do a thing *substantially and directly related to* making, a decision. ("Arranged for" pins the obligation on the deploying entity, not the SaaS/tool vendor.)
2. **Materiality:** the decision could reasonably be expected to **significantly affect the rights or interests of an individual** (adverse or beneficial — e.g. benefits eligibility, contractual rights such as insurance, access to significant services; potentially targeted ads causing differential pricing).
3. **Personal information** about the individual is used in the operation of the program.

If triggered, the policy must disclose (APP 1.8): the **kinds of personal information** used; the **kinds of decisions made solely** by such programs; and the **kinds of decisions the program substantially and directly contributes to** (assisted decision-making — a human in the loop does NOT automatically take you out of scope; OAIC's Issues Paper even uses a pre-programmed Excel triage formula as an in-scope example).

### What it is NOT

- **No reporting to the OAIC or any regulator.** No register lodgement, no filing.
- **No obligation to log or record AI-agent interactions with data.** Nothing in the Act requires interaction-level auditing.
- **No direct notification to affected individuals**, no right to contest a decision, no right to demand an explanation of a specific decision (unlike GDPR Art 22, and unlike WA's *Privacy and Responsible Information Sharing Act 2024*, which commenced 1 July 2026 for WA public sector with notification and human-intervention rights).
- **Not AI-specific.** It covers any "computer program" — AI models, rule engines, even spreadsheets. Conversely, an AI agent that merely *touches/reads* client data but makes no rights-affecting decision is **not** caught.

### Who must do what, from when, penalties

- **Who:** APP entities meeting the three-limb test. **What:** update the privacy policy. **From:** 10 December 2026 (ongoing accuracy thereafter). 
- **Penalties:** failure to include the required policy content is a civil-penalty provision under **s 13K(1)(b)(iia)** — up to **200 penalty units** (≈ A$66,000 at the current A$330 unit; corporate multiplier of 5 takes the ceiling to ≈ A$330,000), enforceable via OAIC **infringement notices** (~A$66,000 tier) and **compliance notices** without court proceedings. This sits in the new low/mid-tier penalty regime created by the POLA Act.
- **Guidance timeline:** OAIC Issues Paper released **18 May 2026**, submissions closed **15 June 2026**, final OAIC guidance expected **September 2026**. OAIC has signalled a **broad reading** (Bird & Bird and Allens both flag this) and readiness for compliance-review activity from commencement day.
- **Practical burden:** the real work isn't the policy edit — it's the **internal inventory of ADM/AI systems and data flows** (including third-party SaaS features that quietly add AI), the significance assessments, and ongoing governance so the disclosure stays true. This is where the claim's "report on AI agents" intuition has a kernel of truth: you need to *know internally* what your automated systems do with personal information, even though you *report* nothing.

### Where the "report AI agent interactions" framing likely came from

A conflation of three real things: (a) the 10 Dec 2026 ADM disclosure rule; (b) OAIC/industry commentary telling entities to *audit and monitor* their AI/ADM usage (incl. third-party tools) to be able to comply; and (c) Microsoft's Purview-for-agents marketing wave (Ignite Nov 2025 onward). No Australian law requires reporting/recording AI-agent interactions with client data. The mandatory AI guardrails proposal (Sept 2024), whose Guardrail 9 did require record-keeping, was **shelved** — the National AI Plan (2 Dec 2025) opted for existing laws + voluntary guidance (the Oct 2025 "Guidance for AI Adoption"/AI6) + an AI Safety Institute. On **15 July 2026** the PM announced an Office of AI in PM&C and plans to legislate "Australian Standards for AI" in **early 2027** (initial focus includes large AI data centres); National Cabinet considers it August 2026 — announced, not law, and not an interaction-reporting duty.

## 3. Microsoft Purview — what actually exists for AI agents

### GA (verified)

- **Purview for agents — DSPM "AI Observability" + Insider Risk Management for agents:** public preview rolled out from **December 2025**; **GA worldwide mid-June to end-July 2026** (Message Center MC1280556, dated 15 Apr 2026). Requires **Microsoft 365 E7 or Agent 365** subscriptions. Gives inventory of agents, activity monitoring, risk levels/patterns, guided remediation, and IRM policies applied to agents like users.
- **Unified Audit Log:** agent/Copilot **prompts and responses are captured as audit records** ("Auditing and AI interactions", learn.microsoft.com) — searchable for investigations and compliance. This is the closest real thing to "reporting when AI agents interact with data", and it long predates any Australian obligation.
- **Broad capability matrix for Agent 365 agents** (learn.microsoft.com/purview/ai-agent-365): auditing, data classification, sensitivity labels, DLP, IRM, Communication Compliance, eDiscovery, Data Lifecycle Management, Compliance Manager — supported for AI interactions; agent instances are auto-enabled for audit and sensitive-data detection at creation.
- **DSPM for AI** (the earlier product) has been GA since 2024/2025 for Copilot, Copilot Studio, ChatGPT Enterprise, Entra-registered AI apps, and even browser-detected third-party AI (ChatGPT consumer, Gemini, DeepSeek) — including **Anthropic Claude (Enterprise)** as a tracked Enterprise AI app.

### Announced / preview (do not treat as deployed reality)

- **Agent 365 as the "control plane" for agents** — announced at **Ignite, 18 November 2025**, with Purview protections extended to it (DLP on agent actions, Communication Compliance for human-agent interactions, Purview SDK embedded in the Agent Framework SDK, Purview-Foundry integration, automated AI compliance assessments in Compliance Manager against **EU AI Act, NIST AI RMF, ISO/IEC** — note: no Australian APP 1.7 template found).
- **Fabric data-agent interaction auditing** — still **preview**.

### Gaps vs the claim

- Purview's deep observability (risk levels, remediation) currently applies to **Microsoft-ecosystem agents** (M365 Copilot agents, Copilot Studio, Foundry); third-party agents get inventory but not full risk treatment. Agents outside the Microsoft stack (e.g. a local Claude Code fleet on a Mac) are essentially invisible to it unless traffic is proxied/registered.
- Licensing: the agent-observability GA is gated on **E7/Agent 365** — premium SKUs.
- Most importantly: **Purview does not perform APP 1.7 compliance.** The Australian obligation is a legal analysis + privacy-policy drafting task; Purview helps with the *discovery/inventory* substrate (which systems, which data, which agents), not the disclosure itself.

## 4. Practical implications

### (a) Datasec — Australian cybersecurity company

- **Compliance-product/service angle is real and time-boxed.** Every APP entity using rights-affecting ADM must complete a system/data-flow audit before 10 Dec 2026; law firms are openly telling clients to start now, and OAIC guidance lands ~September 2026 — a natural Q4 demand spike for: ADM/AI system discovery audits, privacy-policy uplift support, and **Purview DSPM-for-AI / Purview-for-agents deployment services** (E7/Agent 365 positioning fits Datasec's Microsoft partner posture, incl. Marketplace). An "ADM readiness assessment" packaged offer maps cleanly onto the three-limb test + OAIC guidance.
- **Own compliance:** if Datasec (or NexusAI demo workflows, lead scoring in Lead_Bot, etc.) uses programs that substantially inform decisions significantly affecting individuals (e.g. hiring shortlisting, credit/eligibility screening for clients), Datasec's own privacy policy needs the disclosure.

### (b) Secuura — blockchain document-verification platform

- The APP 1.7 duty sits with whoever **"arranged for"** the program — i.e. **Secuura's clients**, not Secuura as vendor, when the platform's automated verification outcome substantially drives a decision that significantly affects a person (document/credential authenticity feeding employment, finance, identity decisions is squarely the kind of example regulators cite).
- Expect **procurement pressure**: OAIC explicitly tells entities to "actively identify, assess and keep oversight over how a [third] party product/service uses ADM." Secuura should prepare a **client-facing ADM disclosure pack** (what the platform decides vs assists, what personal information its programs/agents use, where humans intervene) — that becomes a sales asset, not just paperwork.
- If Secuura itself is an APP entity (>A$3M turnover or trades in personal information), its own privacy policy needs the APP 1.7–1.9 content by 10 Dec 2026.

### (c) Small business running an internal fleet of AI coding/ops agents

- **Mostly out of scope.** Agents reading client project data to write code, run ops, or draft documents are not making decisions that "significantly affect the rights or interests of an individual" — no APP 1.7 disclosure arises from that activity alone. And a business under A$3M turnover is generally not an APP entity anyway (unless health/PI-trading/Commonwealth-contractor/AML-captured).
- **Real exposures instead:** (1) the **statutory tort** (since 10 June 2025) applies to everyone regardless of size — reckless exposure of someone's private information by an agent is suable; (2) **client contract flow-down** — APP-covered clients must manage downstream ADM/privacy risk, so expect security/AI-usage questionnaires; (3) if any agent starts scoring, triaging, or making eligibility-style calls about *people* using their personal information, re-assess immediately.
- **Cheap insurance:** keep the agent inventory + interaction logging discipline already emerging in the fleet (aligns with the voluntary AI6 guidance and with where Tranche 2 / the 2027 "Australian Standards for AI" may head). No legal duty today; strong direction of travel.

## 5. Key dates table

| Date | Event | Status |
|---|---|---|
| 10 Dec 2024 | POLA Act Assent; most provisions live Dec 2024 | In force |
| 10 Jun 2025 | Statutory tort of serious invasion of privacy | In force |
| 2 Dec 2025 | National AI Plan — no mandatory AI guardrails "at this time" | Policy |
| Dec 2025 | Purview-for-agents public preview rollout begins | Done |
| 1 Jul 2026 | AML/CTF Tranche 2 → 100k+ small businesses partly Privacy-Act-covered; WA PRIS Act commences (WA public sector) | In force |
| 15 Jul 2026 | PM announces Office of AI + planned "Australian Standards for AI" (legislation early 2027) | Announced only |
| mid-Jun–end-Jul 2026 | Purview DSPM AI Observability + IRM for agents GA (E7/Agent 365) | GA |
| ~Sep 2026 | OAIC final ADM guidance expected | Pending |
| **10 Dec 2026** | **APPs 1.7–1.9 ADM transparency commence; Children's Online Privacy Code registered** | Legislated, fixed |
| Early 2027 | Australian Standards for AI Bill expected | Speculative |
| TBD | Tranche 2 (fair-and-reasonable test, small-biz exemption removal, erasure) | No Bill, no date |

## Sources

**Legislation / regulator (primary):**
- Privacy and Other Legislation Amendment Act 2024 (Cth) — https://www.legislation.gov.au/C2024A00128/asmade/text (commencement table: Sch 1 Pt 15 → 10 Dec 2026)
- POLA Act Sch 1 Pt 15 text (APPs 1.7–1.9, s 13K amendment) — https://classic.austlii.edu.au/au/legis/cth/num_act/paolaa2024377/sch1.html
- OAIC ADM Issues Paper (18 May 2026) — https://www.oaic.gov.au/__data/assets/pdf_file/0027/263925/ADM-Issues-Paper.pdf
- OAIC consultation page — https://www.oaic.gov.au/engage-with-us/consultations/consultation-on-guidance-for-transparency-in-automated-decision-making
- Privacy Act 1988 (current compilation) — https://www.legislation.gov.au/current/C2004A03712
- Mandatory guardrails proposals (not proceeding) — https://consult.industry.gov.au/ai-mandatory-guardrails
- National AI Plan, "Keep Australians safe" — https://www.industry.gov.au/publications/national-ai-plan/keep-australians-safe
- Guidance for AI Adoption implementation guidance — https://www.ai.gov.au/staying-safe-and-responsible/essential-ai-practices/guidance-ai-adoption-implementation-guidance

**Law-firm analyses (secondary, consistent with each other):**
- Allens (10 Jun 2026) — https://www.allens.com.au/insights-news/insights/2026/06/automated-decision-making-transparency-what-app-entities-need-to-know-about-the-app-1-amendments/
- Hamilton Locke (4 Jun 2026) — https://hamiltonlocke.com.au/transparency-in-automated-decision-making-what-regulated-entities-need-to-know-and-do-before-december-2026/
- McCullough Robertson (18 Mar 2026, penalties detail) — https://mccullough.com.au/2026/03/18/automated-decision-making-transparency-requirements-new-obligations-for-businesses-with-ai-systems/
- Maddocks (16 Jun 2026) — https://www.maddocks.com.au/insights/beyond-compliance-preparing-for-the-new-app-regime
- Bird & Bird (2026) — https://www.twobirds.com/en/insights/2026/australia/australias-new-adm-transparency-obligation-oaic-signals-a-broad-reading-ahead-of-december-2026
- Pinsent Masons on Tranche 2 (29 Jul 2025) — https://www.pinsentmasons.com/out-law/analysis/privacy-act-reforms-australia
- Biztech Lawyers reform status — https://www.biztechlawyers.com/legal-articles/australias-privacy-reform-shaping-the-future-of-data-protection
- ComplyAU small-business guide (30 Jun 2026) — https://complyau.com/does-privacy-act-apply-small-business-australia/
- ScaleSuite SME guide (18 Jul 2026) — https://www.scalesuite.com.au/resources/privacy-act-changes-for-smes
- SafeAI-Aus legal landscape (22 Jul 2026, Office of AI / Standards) — https://safeaiaus.org/safety-standards/ai-australian-legislation/
- Mamba Strategic AI regulation guide (10 Jul 2026) — https://mambastrategic.au/australian-ai-regulation-2026/

**Microsoft (vendor — GA vs announced flagged in text):**
- MC1280556 GA notice (15 Apr 2026): Purview for agents GA mid-Jun–end-Jul 2026, E7/Agent 365 — https://mc.merill.net/message/MC1280556
- Ignite announcement (18 Nov 2025): Agent 365 + Purview for GenAI agents — https://techcommunity.microsoft.com/blog/microsoft-security-blog/announcing-new-microsoft-purview-capabilities-to-protect-genai-agents/4470696
- Purview + Agent 365 capability matrix / audit of AI interactions — https://learn.microsoft.com/en-us/purview/ai-agent-365
- Purview protections for Copilot & GenAI apps (incl. Claude Enterprise tracking) — https://learn.microsoft.com/en-us/purview/ai-microsoft-purview
- Fabric data-agent auditing (preview) — https://learn.microsoft.com/en-us/fabric/data-science/data-agent-purview-governance
- DSPM for AI deployment blog — https://techcommunity.microsoft.com/blog/microsoft-security-blog/how-to-deploy-microsoft-purview-dspm-for-ai-to-secure-your-ai-apps/4397714

*Verification note: legislative facts cross-checked against the Federal Register of Legislation and OAIC primary sources; law-firm pieces used for interpretation only where mutually consistent; Microsoft claims separated into GA (Message Center) vs announced (Ignite blog).*
