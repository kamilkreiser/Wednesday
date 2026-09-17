Wednesday -> Seat A (Secuura/Blockchain), 5th successor

## BLUF
One small queue item, inserted AFTER KS-1207's push + READY (not before): **file ONE Backlog ticket for the #1019 round-2 gate Record on F-1019-2** — the router `caseSensitive` read has no cell that tells the door router from the factory router (the gate's tamper G-READOUTER reds 0; latent, both default today). Test-only pin; it is a local-model candidate, so do NOT build it.

## Recommendation
1. Search first (by `caseSensitive`, `erasureDoorVerdict`, `F-1019-2`, `KS-1187`) and state the terms + hit counts in the ticket.
2. Ticket: ours, Backlog, related KS-1187, NOT linked to any PR. Body BLUF: the property (the door must read its OWN router's caseSensitive option), the gate's measurement (G-READOUTER 0 reds at 82f09c8bd; report `/Volumes/DevMASTER/!CODING/Testing Agent MAIN/projects/secuura/reports/2026-09-17-ks1187-1019r2-82f09c8bd-tier1-r2/`), the fix shape = a test-only cell that mounts the door on a case-sensitive router while the factory router stays default (and the inverse), red under G-READOUTER.
3. Mail the ticket id in your next STATUS.

## Detail
- Why a ticket: the local model's builder refuses a finding that lives only on a PR, and KS-1187 is In Progress (§5f), so it cannot carry it.
