# Channel scoreboard — per-channel, per-work-class track record

Feeds routing decisions (delegation-protocol R5) and the harness `priors` hook.
Score = verifier score in [0,1]. Update at every task close-out. Retirements
(w≥3 failures on a class) recorded in the notes column with date + reason.

| Channel | Work class | Attempts | Mean | Recent scores (new→old) | Notes |
|---|---|---|---|---|---|
| gpt (GPT-5/Codex) | small verified coding | 2 | 1.00 | 1.0, 1.0 | one-shot both; ~14–34s; $0 marginal (sub) |
| haiku | small verified coding | 2 | 1.00 | 1.0, 1.0 | one-shot both incl. trap task; ~135–144s |
| claude (Sonnet) | small verified coding | 0 | — | — | wired; never selected before early-stop |
| gpt-low (effort none) | small verified coding | 0 | — | — | wired; untested in anger |
| Secuura agent | project delegation | 3 | 1.00 | 1.0, 1.0, 1.0 | 08-04 session 3 (consent+deploy brief, v1.1 routing): all in-window DoD items done — merges+deploy demo-verified, KS-555/556/557 closed w/ receipts, Peter nudge posted. FOUND a real coordination gap (EOD-08-04 window never communicated to Peter) and fixed it in-flight. Routing: 1 QUESTION mail, ANSWERed ~2 min, 0 Kam pauses. Prior: 08-04 WED-20 pilot brief end-to-end (5 tickets, codex pilot honest KEEP); verified my email instead of trusting it. Protocol caveat stands: prompt fidelity is the WED-20 lever. |
| NexusAI agent | project delegation | 1 | 1.00 | 1.0 | 08-04 board-actions micro-task: 10/10 tickets moved/commented, post-change JQL verification, REST fallback self-applied, round cap respected. ~25 min brief→receipts. |
| CypherKey agent | project delegation | 1 | 1.00 | 1.0 | 08-04 rulings brief incl. keyed-digests one-way door: key handled exactly right (openssl→4_Credentials only, secretref not literal), pinned-digest roll, LIVE e2e ceremony pass + DB proof of old/new coexistence, honest residual stated, temp firewall rule self-cleaned. Held plan-confirmation for the env change (good judgment). ~15 min confirm→receipts. |

Seeded 2026-08-03 from the day-3 harness runs (see
`1_Project_Definition/Architecture/2026-08-03_treequest-study-notes.md`).
