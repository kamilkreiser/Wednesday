---
date: 2026-09-07
type: pickup
scope: DATASEC ONLY — laptop seat. Secuura belongs to the Studio seat; do not touch it.
source: written at the 50% checkpoint by the laptop seat
status: live
supersede: replace wholesale at the next pickup; do not append
---

# NEXT PICKUP — Datasec laptop seat, ~10:5x AEST Monday 2026-09-07

**TWO WEDNESDAYS ARE RUNNING.** The Studio seat owns **Secuura** and is live on it. This seat owns
**Datasec**. We share one git repo, one dashboard and one chat panel. **Do not write the shared
handover files** (`NEXT-PICKUP.md`, the daily note, `_ledger.md`) — they are hers this session. This
file is the Datasec-scoped handover. Pull before every write.

## KAM'S RULINGS TODAY THAT BIND THIS SEAT
- **10:15** — *"Include the new projects in the analysis and run the full test, not just high level."*
  Supersedes the June brief's scope exclusions.
- **10:44** — **Vision is PARKED completely**, deliberately, until Datasec resolves its CRM approach
  and strategy. Also: **Vision is PRE-PRODUCTION** (corrects this seat's earlier "live production"
  framing, which was reasoned from the workspace CLAUDE.md rather than from him).
- **10:46** — **NexusAI is UNPAUSED** and is this laptop's responsibility. Supersedes his 2026-09-06
  17:01 pause ruling.
- **10:48** — objective for NexusAI: *"get Nexus to a state where it can be submitted to the Azure
  Marketplace."*
- **10:49** — ⚠️ **ROTATION BAND IS NOW 80–90%**, superseding the 2026-09-05 80–85% band.
  *"don't forget the Wednesday window is between 80 and 90% context. Use this as your rotation window."*
  **This is a W-tier operational rule affecting BOTH seats and it is not yet in `learnings/` or the
  ledger — those are the Studio seat's files this session. It must be filed at the next consolidation.**

## STATE — the security review re-run is DONE (first full pass)
All 8 reviewers reported. **219 findings stand across the estate: 31 June (27 unremediated, ZERO
fixed) + 188 new.** 15 new Criticals. Deliverables written, `.md` + branded `.docx` both current:
- `Deliverables/12_Rerun_Delta_2026-09` — the delta report (343 lines)
- `Deliverables/13_Consolidated_Findings_Register_2026-09` — the consolidated register
- `Deliverables/Components/` — 13 new component summaries
- `_Working/findings-seed-2026-09/` — 13 seed files + `_REVERIFICATION_19.md`
- `_Working/2026-09-07_METHOD_IMPROVEMENTS.md` · `_RERUN_DISCOVERY.md` · `_VISION_PARKED.md`
- `_Working/scan-artifacts-2026-09/` — gitleaks, semgrep, trivy, SBOM (per-component; syft panics on
  the combined tree), **each with its argv recorded**

## FLEET — one agent live
**`Datasec/NexusAI` pane `%2`**, launched 10:50, brief verified at `datasec-nexusai@agentmail.to`
@ 00:50:47Z. Commissioned: (1) file the 18 security findings as Jira tickets **under its own
identity** (Wednesday is READ-ONLY on RD), aggregated per Kam's 09-06 one-ticket-per-logical-path
rule, **grouping proposed to Wednesday before creation**; (2) categorise the **281 open RD issues**
and drive toward Marketplace submission readiness.
**Its plan confirmation will land for this seat — answer it.**

## WHAT THIS SEAT OWES NEXT
1. **Answer NexusAI's plan confirmation**, then its ticket-grouping proposal.
2. **`11_Assurance_Pack_Index.md` does not know documents 12 and 13 exist** — add them.
3. The **June deliverables 00/03/04/09/10** are now materially out of date (the register says 31; it
   is 219). Decide with Kam whether to re-issue or to let 12+13 stand as the current position.
4. **Two live checks named by reviewers**, both needing Kam's word: whether the OneTimePad demo
   exposes `/setup` unauthenticated, and whether Entra genuinely pins the EAM `sub`.
5. **The deferred live GitHub/Azure/Entra config pass** is still open from June, and the tenant
   conflict (`fc05dcdd-…` vs `0c57ab37-…`) must be settled before any `az`.

## STANDING NOTES FOR THIS SEAT
No `cd` (the hook refuses). Quote every grep glob — zsh `nomatch` makes an unquoted `--include=*.kt`
never run and read as a clean zero. **Every negative claim needs a positive control.** `send_brief.sh`
wants a literal `^PROVENANCE:` line with `- <fact> | <source> | read YYYY-MM-DD` entries and a
`SELF-CHECK: re-read end-to-end for contradictions | YYYY-MM-DD HH:MM` line — heading-style `##`
prefixes are REFUSED (cost two rounds today). The T9's `core.sshCommand` needed repointing from the
DevMASTER path at boot; check it after any sync.
