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
| Secuura agent | project delegation + AGENT TEAMS lead | 5 | 1.00 | 1.0 ×5 | **08-05 ruling execution 1.0:** KS-561 shipped+verified (matrix green), KS-560 closed 11/11 (untouched tests greened on platform fix alone = root-cause proof), #646 correctly HELD when green never came (real GHCR infra block, diagnosed not bypassed — exactly the verify-culture we protect). |
| (pilot row) Secuura agent | Agent Teams pilot | 4 | 1.00 | 1.0, 1.0, 1.0, 1.0 | **08-04 night: WED-54 Agent Teams pilot 1.0** — DoD 11/11 verdicted (ALL one root cause: KS-561 real platform bug since 07-11, curl-proven), harness PR #645 merged 8/8 demo-green, fix #644 DRAFT proven-local held for Kam (deploy hold honored ALL night incl. expanded scope), packet+KS-559 (7/11 patched, PR #646) done, KS-562 side-find A/B-cleared. Teams mechanics: 4 Sonnet teammates, contract-first, 4/4 accepted via gates, 0 escalations; adversarial-honest teammates killed 2 lead hypotheses (feature!). Friction filed: teammates lacked task tools; notification race; teammate bg-tasks die silently on lead Docker restarts. |
| (prior row) Secuura agent | project delegation | 3 | 1.00 | 1.0, 1.0, 1.0 | 08-04 session 3 (consent+deploy brief, v1.1 routing): all in-window DoD items done — merges+deploy demo-verified, KS-555/556/557 closed w/ receipts, Peter nudge posted. FOUND a real coordination gap (EOD-08-04 window never communicated to Peter) and fixed it in-flight. Routing: 1 QUESTION mail, ANSWERed ~2 min, 0 Kam pauses. Prior: 08-04 WED-20 pilot brief end-to-end (5 tickets, codex pilot honest KEEP); verified my email instead of trusting it. Protocol caveat stands: prompt fidelity is the WED-20 lever. |
| VSP agent | project delegation | 1 | 1.00 | 1.0 | 08-04 dependabot+handoff brief: deploy-wiring verified FIRST (two ways), supply-chain check on new transitives, 144 tests green locally, LEAD_BOT confirmed NOT completed w/ multi-source evidence, refused prod firewall change, refused wrong gh identity (honest CI caveat instead). Used the 15-min fallback correctly when MY side swallowed their question (my defect, not theirs — ledger). |
| NexusAI agent | project delegation | 1 | 1.00 | 1.0 | 08-04 board-actions micro-task: 10/10 tickets moved/commented, post-change JQL verification, REST fallback self-applied, round cap respected. ~25 min brief→receipts. |
| Tokenomics agent | project delegation | 2 | 0.50 | 1.0, 0.0 | 08-04 rebrief EXEMPLARY: cross-verified my facts vs 2 sources before writing, both files fixed grep-clean + bonus own-folder stale ref, DELIBERATE DEVIATION flagged intelligently (brief said mirror Blockchain wording, but that wording itself fails grep-clean — worded DEAD warnings w/o old identifiers instead). First attempt 0.0 (session died, no work; my circular brief the likely stall — ledger w=2 mine). |
| CypherKey agent | project delegation | 1 | 1.00 | 1.0 | 08-04 rulings brief incl. keyed-digests one-way door: key handled exactly right (openssl→4_Credentials only, secretref not literal), pinned-digest roll, LIVE e2e ceremony pass + DB proof of old/new coexistence, honest residual stated, temp firewall rule self-cleaned. Held plan-confirmation for the env change (good judgment). ~15 min confirm→receipts. |

Seeded 2026-08-03 from the day-3 harness runs (see
`1_Project_Definition/Architecture/2026-08-03_treequest-study-notes.md`).
