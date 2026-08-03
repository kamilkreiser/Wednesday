# Correction ledger — frequency-weighted reinforcement

Design per Kam (2026-08-03, voice): *"similar to when people learn, frequency is
used for reinforcement — if a mistake happens once, that could be isolated; if it
happens more than once, an increased weight is given."*

## The weight scale

Weight = number of occurrences. Each recurrence escalates the response:

| w | Meaning | Required response |
|---|---|---|
| 1 | **Isolated** — could be noise | Log it. Write a lesson file only if it would change future behaviour (importance filter). |
| 2 | **Reinforced** — a pattern, not noise | Lesson file mandatory. If one existed and didn't fire, diagnose *why* (wrong file? too abstract? bad retrieval handle?) and fix the lesson, not just the mistake. |
| ≥3 | **Regression** — the system is failing to learn | Treat like a failing test (no-skip rule). Automatic promotion candidate: move the rule into `identity/` or into *enforcement* (launcher check, hook, CLAUDE.md line). Raise it with Kam at the next briefing. |

Rules:
- Same *underlying* mistake in a new costume still increments the weight — match
  on root cause, not surface form.
- Weights never decay automatically. They are only retired at weekly
  consolidation, with the reasoning written in the audit note.
- Positive reinforcement counts too: when Kam explicitly praises a behaviour,
  log it as `praise` — repetition there tells us what to *keep* doing.

## Ledger (newest at top)

| Date | What happened (root cause) | Type | w | Lesson | Status |
|---|---|---|---|---|---|
| 2026-08-03 | Delegation coordination insufficient (first Secuura pilot): Kam had to (1) answer questions the project agent should have routed to Wednesday, (2) approve and step through the work, (3) context-switch between Wednesday and the agent. Root cause: the fleet's channels are async/boot-time only — no mid-session agent→Wednesday question path, so everything escalated to Kam by default. | correction | 1 | [[2026-08-03_role-beyond-code-three-priorities]] | open → WED-42 |
| 2026-08-03 | Misread dictated intent: Kam said "we should load for sub agents but [a] very complex task might use a more narrow agent" — I read "load selectively for sub-agents"; he meant load them FULLY, with *narrow* referring to the agent's scope, not its context. Wrote the wrong rule into the delegation protocol; corrected within minutes. Root cause: resolved an ambiguous dictated phrase toward the interpretation I'd just been reading about (lesson 9 recency bias) instead of flagging the ambiguity. | correction | 1 | [[2026-08-03_context-loading-split]] | corrected same session |
