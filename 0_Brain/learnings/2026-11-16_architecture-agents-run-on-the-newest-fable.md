---
date: 2026-11-16
type: preference
source: "Kam, Friday's terminal, 2026-11-16 ~14:5x, verbatim: 'I would like your help on a new version of an old project.  In a moment i will switch you to fable and I would like the architecture agents you use to analyse and design this project to also use the latest fable'"
status: live
supersedes: ""
tier: W
---

# Architecture agents for the new-version project run on the NEWEST Fable — the same level as the seat

**The lesson:** For the new version of the old project Kam brought to Friday on 2026-11-16, every agent Friday uses to ANALYSE or DESIGN it (architecture, discovery, design review) runs on the newest Fable, the same model Kam switches the Friday seat to. This is a named exception to the routing table (`fleet/specs/model-routing.md`), where Fable has no worker row: Kam's word is the authority, and the row it supersedes is the "Opus 5.5 for every agent" override, for this project's architecture work only.

**How to apply:**
1. The model ID is READ from `0_Brain/dashboard/data/models_latest.json` (`levels.fable.model_id`) at the moment of launch, never typed from memory. At 2026-11-16 14:46 it read `claude-fable-5-2` (source: docs models-overview page, warnings []). If the file names a newer Fable later, the newer one is used: Kam said "the latest".
2. In-session subagents: the Agent tool with `model: "fable"`. Cockpit panes: `/model <id from the file>` right after launch, and say so in the brief.
3. Scope is ANALYSIS and DESIGN for this project. Build, test and gate seats still route by model-routing.md unless Kam extends it; ask, don't widen.
4. Every launch names this file as the reason for the model choice.
