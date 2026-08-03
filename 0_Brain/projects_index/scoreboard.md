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
| Secuura agent | project delegation | 0 | — | — | no scored delegations yet |
| CypherKey agent | project delegation | 0 | — | — | no scored delegations yet |

Seeded 2026-08-03 from the day-3 harness runs (see
`1_Project_Definition/Architecture/2026-08-03_treequest-study-notes.md`).
