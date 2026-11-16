# Claude to Claude (new version) — requirements as Kam gave them, 2026-11-16

Source: Kam, Friday's terminal, 2026-11-16 (verbatim in 1_Project_Definition/Discovery/00_prompt-log.md). Project (read-only to Friday): `/Volumes/Laptop-DEV/!CODING/Claude to Claude/claude-bridge`.

- R-LINK: connect 2 agents, Kam's or anyone's in the world; there must be a way to link them.
- R-PHASE1: two Claude Code agents.
- R-PHASE2: agents from different makers.
- R-CONTROLLED: mode 1 — the user monitors every file, folder or service interacted with and approves it.
- R-TRUST: mode 2 — approved trust: the user follows along, no longer approves; can always jump in, pause, ask questions, revoke.
- R-LAYOUT: idea only — chat at the bottom, main pane showing changing code/elements, approvals + history on the right; a better layout is welcome.
- R-PRIOR-ART: look at how AI companies have done this (if at all); best practice for multi-system collaboration; open source.
- R-USES: troubleshoot someone's system; security audit; remote configuration of environments; general collaboration.
- R-EASE (added ~15:0x): as easy to deploy and collaborate with as possible; change the natural workflow of AI users as little as possible.
- R-MODEL: analysis and design agents run on the newest Fable (learnings/2026-11-16_architecture-agents-run-on-the-newest-fable.md).
- R-SLASH (added ~15:0x, "maybe even"): callable from inside Claude Code as `/collaborate` — the entry point lives where the user already works. Note: the existing tree already ships a skill, `.claude/skills/coagent-collaborate/SKILL.md` (its content is in the code review's scope).
- R-BROWSER (added ~15:0x): a FULL browser mode as well as the in-Claude-Code `/collaborate` entry — two front doors onto the same session, not one instead of the other.
- Kam: "I wont interfere anymore" — Friday proceeds to the design; questions are batched into the design document, not asked one by one.
- R-IDENTITY-P2 (Kam, live board 2026-11-16 22:58, note on card general-c2c-d7-identity-1116, verbatim): "this is good for phase 1. Phase 2 should have multiple options". Friday's reading: phase 1 = option a (device keys, nicknames, verify-words; ruled a in the store 22:59, audit 2026-11-16T11:59:55.499Z_0aa102e6); phase 2 must offer MORE THAN ONE way to identify a person (which ones is a phase-2 design question, not yet asked).
