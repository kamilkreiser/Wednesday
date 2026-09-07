# BRIEF — Datasec / Security Review · Step 2 delta reviews, the REMAINING FIVE components

## BLUF
**Kam, panel, 2026-09-07 21:00 (verbatim): _"keep working on security review and I will review in
the morning when I wake."_** This is that work. Finish Step 2 of the 2026-09-07 re-run by producing a
delta review for the **five components that have a June baseline and no 2026-09 output**.

**Nothing here is merged, deployed, deleted or ticketed. Static, read-only, findings only.**
Kam reads the result in the morning.

## THE FRAME, NAMED — because the previous seat's list was complete over a smaller frame
Wednesday enumerated `Deliverables/Components/*.md` (the June baselines) and diffed it against
`_Working/delta-review-2026-09/*.md` + `_Working/verification-2026-09/*.md`:

    32  components with a June baseline summary
    15  have a 2026-09 DELTA review
    10  have a 2026-09 VERIFICATION pass
     2  PARKED by Kam 2026-09-07 10:44 (vision_datasec-sales-portal, vision_hpas-quickquote)
     5  REMAIN  <- this brief

**🔴 The predecessor handover named FOUR of these five. `hpsm-main` was missing from it.** It has a
June baseline (`Deliverables/Components/hpsm-main.md`) and no 2026-09 file in either directory.
Wednesday found it only by enumerating the frame rather than trusting the list — which is exactly
the failure family filed tonight as *a census complete over a frame that is not*.
**If you find a defensible reason HPSM is out of this engagement's scope, say so and skip it —
do not force it in to satisfy a count. Wednesday's inclusion of it is an inference from the
baseline's existence, not a Kam instruction.**

## THE FIVE, in the order to run them
Kam's standing preference for this workstream is **three at a time** (his overrule of Wednesday's
recommendation to drop them: *"yes, queue the eleven three at a time"*).

**BATCH A — the HP Auth Suite client-side family, run these three first:**
1. `Source_Code/CypherOneDrive-main` → `cypheronedrive-main.md`
2. `Source_Code/Teams-main` → `teams-main.md`
3. `Source_Code/CommonValueLibraryCypher-master` → `commonvaluelibrarycypher-master.md`

**BATCH B — run when A is written:**
4. `Source_Code/Cyphercard-Enrolment-App-main` → `cyphercard-enrolment-app-main.md`
5. `Source_Code/HPSM-main` → `hpsm-main.md` (read the scope caveat above first)

**One note carried from the June characterisation, so you do not re-derive it:**
`Cyphercard-Enrolment-App` is the **enrolment app (KMP, iOS + Android)** — it is **NOT** HPSA.
HPSA mobile source is a recorded `[GAP]`; do not report its absence as a finding.

## READ FIRST, in this order — all four bind you
1. `_Working/findings-seed-2026-09/_AGENT_RULES.md` — the engagement's non-negotiables and the
   instrument discipline.
2. `_Working/delta-review-2026-09/_DELTA_RULES.md` — what a delta review IS, and the two honest
   constraints you must restate in your output (no git history; scanners already rerun).
3. `Deliverables/03_Findings_Register.md` — the June register, for YOUR components only.
4. `Deliverables/Components/<component>.md` — June's summary. It names the trust boundaries, which
   is where to look.

Your question is **not** "what is wrong with this component". It is **"what is here NOW that is not
in the June register"** — with the value concentrated in what scanners cannot see: authorisation
(not authentication), identity and trust decisions, fail-open paths, cross-component seams, and
configuration that ships.

## OUTPUT
One file per component at `_Working/delta-review-2026-09/<slug>.md`, in the shape `_DELTA_RULES.md`
§Output specifies: new findings (severity + CVSS vector, Confirmed/Suspected, `file:line` + quoted
code, why it matters, remediation, variant-of-June-id or not) · changes vs the June summary · what
improved · coverage.

**PLUS, per Kam's standing instruction of 2026-09-07 18:56:36 (verbatim: _"where there is analysis,
make notes of what was found, what was tested, and how"_), every component file carries three
explicit fields — not implied, not woven into prose:**
- **FOUND** — the claim.
- **TESTED** — the scope: what you exercised and what you did not.
- **HOW** — the instrument, the exact command, and the CONTROLS. A positive control proving the
  instrument fires; and where you report a zero, a negative control so the zero is one Kam can
  vouch for. *A method without its controls is a story about what someone did.*

## NAME THE FRAME — the rule filed tonight, and it is the one most likely to bite this work
Before you write *"the only caller"*, *"every occurrence"*, *"three writers"*, *"no hardcoded
endpoint remains"* — **state what you searched over, in the sentence.** *"Three writers **in
`app/src/main/`**"*, not *"three writers"*. Six instances of this landed across the fleet today in
one day, two of them Wednesday's own. Both usual controls pass and the number really is read from
the source — the source is just smaller than the question. **A stated frame is one somebody can
widen; an unstated one is invisible to you and to the reader.** Language and directory boundaries
are the commonest and least visible: a Kotlin grep will not see the Java caller; an `app/` sweep
will not see the library module.

## HOLDS — none of these is negotiable, and none is waived by anything
- **READ-ONLY on `Source_Code/`.** No modify, refactor, build, run or "fix".
- **STATIC ONLY.** Nothing may reach a production, demo or customer system, or any Azure/Entra
  tenant. No `az`. No network testing.
- **READ-ONLY on Jira.** No ticket created, edited or transitioned.
- **NEVER copy a secret value** — file, line, variable, value LENGTH, credential class. Never the
  value and never a prefix of it.
- **Never delete anything — quarantine** (rename into a dated folder and say where it went).
- **🔴 Datasec has NO production grant.** Kam lifted the production ban at 12:07 today and narrowed
  it at 12:10 to *"Only secure[Secuura]"*. **It does not reach this project.** Anything
  production-affecting stops and comes to Wednesday.
- **Signature classes still pause for Kam:** production, money, external communication to any human,
  anything irreversible.

## REPORT BACK — this project has NO fleet inbox, so the FILE is the channel
`Datasec/Security Review` is deliberately absent from `2_Project_Files/fleet/inbox_routing.conf`, so
`send_brief.sh` refuses mail to it and Wednesday will not receive one. **Do not rely on mail.**

Write your coordinator report to a file at exactly this path:

    /Volumes/KK_T9_External_HDD/!CODING/Datasec/Security Review/_Working/delta-review-2026-09/_BATCH2_REPORT.md

containing, per component: new-finding count by severity · the single most important new finding ·
what improved · whether the June component summary is still accurate · **what you did not examine**
· and for HPSM, your scope verdict. Then update `_Working/PROGRESS.md` with what is now complete.

If `AGENTMAIL_API_KEY` is available in this project's own `4_Credentials/.env`, you MAY additionally
mail `wednesday-agent@agentmail.to` with subject
`[Datasec/Security Review -> Wednesday] Step 2 delta batch 2 — <n> components complete`. That is a
convenience, not the deliverable. **The file is the deliverable.**

## IF YOU GET BLOCKED
Wednesday is live and coordinating overnight. Write the blocker into `_BATCH2_REPORT.md` under a
`## BLOCKED` heading with what you tried and what you need, and continue with the next component.
**Do not stop the whole batch on one component.** Kam is asleep; nothing here is worth waking him.

## PROVENANCE
- Kam's 21:00 instruction | dashboard chat_log.json, entry ts 2026-09-07T21:00 | read 2026-09-07
- Kam's 18:56:36 "what was found, what was tested, and how" | tools/kam_rulings_today.sh output | read 2026-09-07
- Kam's 12:07 production lift, narrowed 12:10 to "Only secure" | tools/kam_rulings_today.sh output | read 2026-09-07
- Kam's 10:44 Vision park | _Working/2026-09-07_VISION_PARKED.md | read 2026-09-07
- Kam's "queue the eleven three at a time" | NEXT-PICKUP-DATASEC-LAPTOP.md, Security Review section | read 2026-09-07
- The 32/15/10/2/5 split | `ls Deliverables/Components/*.md` vs `ls _Working/delta-review-2026-09/*.md` and `_Working/verification-2026-09/*.md`, counted by hand | read 2026-09-07
- Cyphercard is the enrolment app, not HPSA | _Working/PROGRESS.md:19 | read 2026-09-07

SELF-CHECK: re-read end-to-end for contradictions | 2026-09-07 21:0x
