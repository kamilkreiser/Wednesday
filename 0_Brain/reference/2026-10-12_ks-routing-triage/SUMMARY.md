# KS routing triage SUMMARY (2026-10-12, read-only, heuristic first pass)
Rows: 359 (Todo/In Review/Blocked/In Progress all; Backlog: 60 at p1/p2 + first 30 others). Fetched total 588 non-archived KS tickets.
Tiers: STALE=223, OPUS=58, SONNET=35, OWNED=18, SONNET+OPUS_GATE=12, CARD=8, SPARK=3, BLOCKED=2
States in scope: In Progress=222, Backlog=90, Todo=29, In Review=13, Blocked=5
Confidence by tier: BLOCKED/LOW=2, CARD/LOW=8, OPUS/LOW=58, OWNED/HIGH=18, SONNET/LOW=35, SONNET+OPUS_GATE/LOW=12, SPARK/LOW=3, STALE/LOW=223

## Controls
1. viewer query returned a user and teams KS, PS: auth path works.
2. Paginated fetch returned 588 total, matching Kam's stated 588; per-state counts (Backlog 240, Todo 29, In Progress 222, In Review 13, Blocked 5, Done 79) match exactly.
3. PR attachments are non-empty: 564 attachments (539 github) with metadata.status present (merged 510, closed 15, open 8, inReview 5, draft 1), so 'no open PR' is not an empty-query artefact.

## Area clusters (non-STALE, non-OWNED rows)
- ?: 23
- services/api-gateway: 13
- akto: 10
- schemathesis/systemTest: 8
- Blockchain/Dev/scripts: 8
- services/auth: 7
- Blockchain/Dev/docker-compose: 5
- Blockchain/Dev/tests: 4
All rows, top areas: ?=55, services/api-gateway=39, services/auth=30, services/originate=25, Blockchain/Dev/scripts=22, akto=21

## In Progress staleness: 222 rows; not updated 14+ days: 88; 30+ days: 0
10 oldest In Progress (id, last update):
- KS-1150 2026-09-14 (28d) PR:merged
- KS-973 2026-09-14 (28d) PR:inReview
- KS-968 2026-09-14 (28d) PR:merged
- KS-806 2026-09-13 (28d) PR:merged
- KS-801 2026-09-14 (28d) PR:merged
- KS-664 2026-09-13 (28d) PR:merged
- KS-741 2026-09-14 (27d) PR:open
- KS-1187 2026-09-17 (25d) PR:merged
- KS-1183 2026-09-16 (25d) PR:merged
- KS-1165 2026-09-16 (25d) PR:merged|merged
In Progress with every PR merged/closed: 212 of 222. PR merged, ticket open: each needs a live run or a Done decision.

## What I could not determine
- Tiers are keyword/regex heuristics on title, labels and description; I did not read every ticket body by eye. Treat all LOW rows as unverified.
- SPARK needs a runnable in-process test; I could not check that any ticket has one, so SPARK HIGH only means file:line plus an action sentence were quoted.
- Whether a merged PR actually completed the ticket: not verified at source (PR diffs not read, nothing deployed or run).
- OPUS is triggered by broad security/gate words (e.g. 'key', 'admin', 'audit'); some may be over-routed and fit SONNET.
- Assignees: Kam holds nearly all tickets; only Peter and Stuart rows are OWNED. 'Waiting on external' was only detected via Blocked state and text match, so BLOCKED-ON-EXTERNAL may be under-counted.
- Backlog beyond the p1/p2 plus 30 sample was not classified; priority 0 (none) sorted last in the 30-sample.
- Age counted from 2026-10-12 12:00 UTC; comment counts are in raw JSON only, not used in the tiering.
- Only 3 SPARK rows, all LOW: most open specs are 2-10 KB multi-file analyses, and the quoted line is the first regex match, not always the fix sentence (KS-638 is likely mis-tiered; read before launching).
