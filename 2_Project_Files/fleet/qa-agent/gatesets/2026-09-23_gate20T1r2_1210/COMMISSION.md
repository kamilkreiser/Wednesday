# COMMISSION — DRAFT the round-20 TIER-1 RE-GATE for #1210 KS-1239 ALONE (round 2 of 2) — do NOT launch

Written by Wednesday (the 17:0x seat of 2026-09-23). **Copy the shape, discipline and file set of `../2026-09-23_gate20T1_seatB/`**
(its README is the file map; its repin script, launcher generator, controls and prompt are the template) — reduced to ONE PR.

## Authority
Kam, live board 2026-09-23 14:24:05 (*"…merge, push, and deploy what you can"*); the 90% usage cut is lifted for THIS lane only
(0_Brain/tasks/EXPIRING-GRANTS.md round-20 row) — this re-gate is part of it.

## The PR
**#1210 KS-1239 RAWAUTHDEAD, round 2** — head `6b572240fc31e564a6d0c516fdff66814bb856c6` (Seat B 22nd's READY round 2, 10:17Z in
wednesday-agent@; read it WHOLE; Wednesday's `ls-remote` agrees). 3 files: api-gateway `src/index.ts` (+0/-18), the new
`ks1239-…test.ts`, and `packages/shared/src/__tests__/ks781-p3-3-body-parser-order.test.ts` (+17/-8 — KS-781 LEG D's three
line pins moved 845/858/891 → 827/840/873, plus comments and a read-back note).
**Round 1** (`gate20T1_seatB` report, 09:54:43Z): NO GO on Major **LEGD-LINEPIN** only — the re-gate's first job is that finding:
is it CLOSED (shared green at the head AND merged over develop), and did the fix introduce anything new. Grade the +17/-8 on
the shared file for scope (the seat asks whether the comments/note exceed "the three pins").
**Develop moved:** now `dd8f99cc75b9b753172a40379eaab2b6c1026180` (tree `b3ba2cb87ac0…`, six tier-1 merged incl. #1212 in the SAME
shared file). The launcher READS develop and the head at launch; the gate grades the merged tree over THAT develop and asserts
LEG D's hunk is disjoint from #1212's (the seat reports 2022-2052 vs 2327/2550). Expected: shared 918/918 merged, api-gateway 746/746.
0 bytes under `services/auth/`. Expected GO string: `GO: merge #1210 batch`.
**Under the two-NO-GO cap:** a NO GO here is final for this round — say which parts are closed so they can ship and what to ticket.

## Deliver (do NOT launch, send, tap, commit or push)
The gate-set files in THIS directory, a `repin_and_launch_*.sh` that refuses unless it re-reads develop + the head at launch,
its controls run (a stale head must refuse), the routing line to add (Wednesday adds it), and your report as TEXT in your final
message. Opus 5.5 by the configured default (no `--model`). Never `cd`; no `timeout`; never discard stderr; read verbs only in
the Secuura checkout (write verbs only in your own scratchpad clone); never delete; Secuura content only.
