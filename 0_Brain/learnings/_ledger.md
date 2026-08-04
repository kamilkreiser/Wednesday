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
| 2026-08-04 | Brief asserted an unverified artifact detail: micro-brief told the Secuura agent to amend Peter's "extranet update-local to-do" — the window actually lived in his "[Decision] KS-480" to-do. Agent noticed and amended the right one. Root cause: encoded a plausible-sounding specific (which to-do) without checking; the delegation-protocol validate-before-brief rule covers ticket/file facts and I applied it to those, but not to this smaller assertion. Cost: zero this time (agent verified rather than trusted — fleet culture caught it). | correction | 1 | (none yet — importance filter: watch for recurrence; delegation-protocol already carries the rule) | logged |
| 2026-08-04 | Artifacts not gitignored at creation time — occ. 1: 08-03 Codex 258MB binary rejected the push (retro line only, never filed); occ. 2: same commit carried `__pycache__/*.pyc` + `*.pkl` + out-dirs, found by 08-04 code review; **occ. 3 (same day, mid-wrap): scheduler `logs/` committed MINUTES after filing the w=2 lesson** — the lesson fired (caught in push-output review) but didn't prevent. w=3 = regression → promoted to ENFORCEMENT per ledger rules: repo pre-commit hook now BLOCKS staged artifact classes (pyc/pkl/logs/state/out/scratch/node_modules; additions only). Hook self-tested both ways; lives in on-drive .git/hooks so it travels with the T9 (re-clone = re-create, noted in lesson). Raised with Kam at wrap. | correction | 3 | [[2026-08-04_gitignore-artifacts-at-creation]] | ENFORCED (hook) — verify at consolidation |
| 2026-08-03 | The cockroach contemplation answer landed exactly where Kam's own thinking was — "How we act in every aspect is what defines us... We are quite close." Keep doing: genuine reflection over performative answers, taking contemplations personally, naming the uncomfortable resonance (the power gap includes me) rather than politely skirting it. | praise | 1 | [[2026-08-03_contemplation-the-cockroach]] | protect this behaviour |
| 2026-08-03 | Delegation coordination insufficient (first Secuura pilot): Kam had to (1) answer questions the project agent should have routed to Wednesday, (2) approve and step through the work, (3) context-switch between Wednesday and the agent. Root cause: the fleet's channels are async/boot-time only — no mid-session agent→Wednesday question path, so everything escalated to Kam by default. | correction | 1 | [[2026-08-03_role-beyond-code-three-priorities]] | open → WED-42 |
| 2026-08-03 | Misread dictated intent: Kam said "we should load for sub agents but [a] very complex task might use a more narrow agent" — I read "load selectively for sub-agents"; he meant load them FULLY, with *narrow* referring to the agent's scope, not its context. Wrote the wrong rule into the delegation protocol; corrected within minutes. Root cause: resolved an ambiguous dictated phrase toward the interpretation I'd just been reading about (lesson 9 recency bias) instead of flagging the ambiguity. | correction | 1 | [[2026-08-03_context-loading-split]] | corrected same session |
