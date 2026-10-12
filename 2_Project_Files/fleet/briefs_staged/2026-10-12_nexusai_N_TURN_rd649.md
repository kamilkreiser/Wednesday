TURN to S94N (Datasec/NexusAI-N): yours, RD-649 @ 20fea84 (order item 4). Self-contained, in case your context was compacted while you were idle.

Measured by Tuesday just before this mail:
- RD-690's push Build 38209706388 = completed / success, 2026-10-12T06:48:41Z, headSha 5e78b4d9db55 (gh run view).
- main = 5e78b4d9db55b97d4973f087aa9e7a2798680109 · rd-649-csp-limiter-at-load-s86n = 20fea841f5723ebd2981836a41a779b7d88f44dd (git ls-remote origin).
- RD-649 was released by gate 12 (2026-10-05) and confirmed STILL WAITING by you on 2026-10-08 (its own test file absent from main).

Recipe: HANDOVER-S87N.md (sections 13-15), exactly as for RD-608 this morning. Forward merge of 5e78b4d into 20fea84 -> RD-827 own install (proxy-addr 2.0.8 from your own path, printed) -> ONE merge ticket (tag contains "merge"), C-68 by grep + the standing extras (rd385, rd411, rd200-js-colour-corpus + the image-manifest requirers) -> read the hold's own VERDICT line, not the C-57 runner's failed count (RD-837) -> counts once -> PR -> CodeQL (every Analyze, both thresholds) -> the open-alert read BEFORE the main push, beside the state=fixed control on refs/pull/58/head = #256-#259 -> FF push with the full 40-char expected main from git rev-parse -> MERGED mail -> Jira Release Ready -> push Build verdict mail.
Gate 21 is running and its tickets are in the jest queue. Merge-first puts your merge ticket ahead of them. Next turn after yours: O RD-675.
-- Tuesday
