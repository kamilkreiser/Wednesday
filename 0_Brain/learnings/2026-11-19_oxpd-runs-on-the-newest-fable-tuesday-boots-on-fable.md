---
date: 2026-11-19
type: instruction
tier: W
source: Kam, typed into the Tuesday terminal, 2026-11-19 (s292, about 15:47 AEDT by the statusline read beside it)
status: superseded (by 2026-11-21_no-fable-unless-flagged-opus-is-the-default.md, Kam 2026-11-21)
---

# OXPd runs on the newest Fable, and the Tuesday seat now boots on Fable

**Kam's words, verbatim:** *"Friday has been working on a claude to claude agent while away and also on an oxpd projects. she is backing up now.  once ready, she will send you notes to claim and start on the oxpd project.  i would like you to switch to latest fable and use fable agents when working on this project"*

## The rule
- **Datasec/OXPd:** every agent Tuesday starts for this project (drafters, builders, gates, analysts) runs on the NEWEST Fable, read from `0_Brain/dashboard/data/models_latest.json` at the launch (`claude-fable-5-2` on 2026-11-19), set AT LAUNCH (`SEAT_MODEL_ENV` for a cockpit seat, `model` on an in-session agent); never `/model` into a pane. This overrides the model-routing table's Sonnet/Opus rows for OXPd only, by Kam's word.
- **The Tuesday seat itself** boots on the `fable` alias with `opus` as the availability fallback: one line in `Launch_Wednesday.command` beside Friday's (commit 2026-11-19, backup `.pre-1119-tuesdayfable`), tested by arms (tuesday fable, friday unchanged, wednesday opus). It takes effect at the next rotation; the rung-5 check reads the pane's model field after it.
- **The OXPd handover:** Friday holds the project under her own grant (EXPIRING-GRANTS, Friday's OXPd row: analysis, architecture document, plan and questions; NOT a build). When Friday's notes arrive in tuesday-agent@, Tuesday reads them at source, claims `Datasec/OXPd` (WED-OWNERSHIP, check then claim), and starts. What Tuesday may do there is what the notes and Kam's words cover: the Friday row's NOT-covered list (no build, no library change, no Azure, GitHub or HP portal action, no message to HP or any human, no spend) is read as still standing until Kam widens it.

## Why
Kam chose Fable for architecture and design work on OXPd (his 2026-11-18 brief to Friday said "keep latest fable running for you and the sub agents used for this task"); this carries that choice to the seat that inherits the project.

## Exception and failure direction
The fallback to Opus exists so an unavailable Fable never stops a rotation; a seat that comes up on Opus after a rotation is told on the board, not silently accepted. Datasec work that is NOT OXPd keeps the routing table.
