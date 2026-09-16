---
date: 2026-09-16
type: audit
scope: every Datasec project's instruction files
requested_by: Kam, 2026-09-16 ~20:50 — "For the last week, HPSM and nexus were running without you. I told them to comment out the sections that required them to hold everything unless it was from you. please check all projects and make sure the instructions work" + "will be working through you"
status: findings only — NOTHING EDITED (hard rule 1: this seat never edits another project's files)
---

# Datasec coordinator-instruction audit — 2026-09-16

## BLUF

**28 instruction files across 15 Datasec projects were checked. Two projects were paused, exactly the
two Kam named: HPSM and NexusAI. Thirteen are clean.**

**But a verbatim restore of NexusAI would be WRONG twice over**, and that is the finding that matters:
its pre-pause text names **Wednesday** as the authorising coordinator, which was true before Kam's
2026-09-07 seat split and is false now — Datasec is Tuesday's. And the pause week *added* work Kam
asked for (RD-399's boot review and `pending_plan_<date>.md`) which a revert would silently delete.
**The restore is a merge, not a revert.**

Separately, **3 lines in 2 projects mail the wrong coordinator** and have done since before the pause.

## Method

`find -maxdepth 3` for `CLAUDE.md` and `Launch_*.command` under `!CODING/Datasec/` → 28 files
(`_archive` and `.pre-*` excluded). Each searched for pause markers, commented-out blocks, coordinator
holds, GO-gating, and both agent mail addresses. Positive control on every count.

**One false positive excluded deliberately:** Feedback_System, Vision_Sales_Portal and the Datasec root
`CLAUDE.md` all match "coordinator" — that is a *software component* (Feedback_System's coordinator
service, port 4900, `/api/feedback/coordinator-state`), not the agent. No action.

## 1. HPSM — one banner, and it carries its own expiry

`HPSM/CLAUDE.md:5-7`, added 2026-09-14. Verbatim:

> **COORDINATOR PAUSED — Kam, 2026-09-14 … Do not wait for Tuesday, do not expect briefs, ANSWERs or
> GO mails from Tuesday, and do not run inbox pollers for her … This stays in force until Kam says
> Tuesday is back.**

**Kam has now said it.** The condition the banner wrote for itself has fired, so the banner goes.
It was an *addition*, so removal is clean and no backup is needed. Once removed the file is
self-consistent: line 219 already reads *"Coordinator for Datasec is now **Tuesday**
(`tuesday-agent@agentmail.to`)"*.

The banner's third line is **not** pause-related and must survive: *"Standing rule (Kam, 2026-09-14):
use as many subagents as the work needs, without asking first."*

## 2. NexusAI — two files, restorable, but NOT verbatim

Pre-pause copies exist and are intact: `NexusAI/quarantine/2026-09-14-tuesday-pause-before/`
(both files) and `Launch_Claude.command.bak.20260914` (24,556 B).

- `CLAUDE.md` — 10 changed lines: the protocol v1.3 delegation wrapped in `<!-- PAUSED (RD-399) … -->`
  (lines 271-283), a banner at 269, a live line changed from *"deploy only on Wednesday's GO"* to
  *"deploy only on Kam's GO"* (line 329) with its note at 330, and a checklist line at 386.
- `Launch_Claude.command` — 44 changed lines: the TURN DISCIPLINE mail-first rule commented out
  (277-290), its replacement note (351-355), and the boot steps re-pointed from mail to in-session.

### Why a verbatim restore is wrong — two independent reasons

**(a) It would point NexusAI at the wrong seat.** The pre-pause text names Wednesday five times as
the authorising coordinator (`CLAUDE.md` 269, 271, 273, 275, 323). That was correct before Kam's
**2026-09-07 split**; since then *"you will work on ONLY datasec projects … Wednesday will work on
Secuura and general tasks."* Restoring it verbatim would tell a Datasec project to seek GO mails from
the seat that does not answer for Datasec.

**(b) It would delete work Kam asked for during the pause.** The diff shows the pause week added
RD-399's step 7 — boot review of wrap-ups, backlog and needed work, saved as
`5_Project_History/pending_plan_<date>.md`. That is Kam's own 2026-09-14 instruction and is
independent of who coordinates. A revert would remove it with no trace.

### The merge, concretely
1. Un-comment the v1.3 delegation block and the TURN DISCIPLINE block.
2. **Replace Wednesday with Tuesday** in every restored authorisation line, and the GO line back to
   a coordinator GO — Tuesday's.
3. **Keep** step 7 and the `pending_plan_<date>.md` habit.
4. Resolve the open question the pause note itself records at line 330: *"who commissions the testing
   agent's gate"* — that returns to the coordinator.

## 3. Pre-existing misroutes — NOT caused by the pause

Three lines send Datasec mail to the Secuura/general seat. They predate the pause and would have
misrouted all week regardless:

| file | line | what it says |
|---|---|---|
| `HPSM/CLAUDE.md` | 446 | wrap mail to `wednesday-agent@agentmail.to` |
| `HPSM/CLAUDE.md` | 451 | plan confirmation BY MAIL to `wednesday-agent@` |
| `Vision_Sales_Portal/Launch_Claude.command` | 263 | turn never ends unmailed → STATUS/wrap to `wednesday-agent@` |

HPSM contradicts itself: line 219 names Tuesday, lines 446/451 name Wednesday. All three should read
`tuesday-agent@agentmail.to` per the workspace rule that Datasec projects tag `-> Tuesday`.

## 4. The thirteen clean projects

ATTIO · Commercial Readiness · CypherKey · Feedback_System · HPAM · Lead_Bot · Marketing_Collateral ·
myPKI · RESEARCH · Security Review · Task_Dispatcher · Vision_Sales_Portal (instructions clean; only
the launcher mail line above) · Websites. No pause markers, no commented-out holds.

Note: Commercial Readiness, HPAM and RESEARCH have **no `CLAUDE.md` at all** — they are document
folders rather than agent projects. Recorded as a fact, not flagged as a fault.

## What this seat did NOT do

**Nothing was edited.** Every file above lives in another project, and this seat manages rather than
edits (workspace hard rule 1). The changes need each project's own agent, briefed by this seat, or
Kam's own hand.
