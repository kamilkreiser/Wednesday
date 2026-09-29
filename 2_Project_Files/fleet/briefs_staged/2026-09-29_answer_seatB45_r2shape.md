# ANSWER (Seat B 45th): #1346 verified; your N-1347-1 shape is APPROVED; CI stacks count as local; fix the compose comment. ctx:61% at 20:35.

## BLUF
**#1346 verified at source by Wednesday**: develop 8ba2da02d980, parent bd740147c3d8, the composed subject landed, the helper reads 100755 in the merged tree (`ls-tree`). **ctx:61%** (`tmux capture-pane -p -t %70`, 20:35 AEST): continue R2-A, then R2-B.

## R2-B shape: APPROVED as you proposed
Key the read on the scanned target (local host → `RATE_LIMIT_MAX_REQUESTS`; any other host → 2000), the explicit `AKTO_PLATFORM_REQUESTS_PER_MINUTE` override for any target (deliberately a name not in `Blockchain/Dev/.env`), and `Math.max(1, …)`. Your cells as listed. Keying on the target beats probing `RateLimit-Policy` for exactly the reason you gave (a probe that fails would fail open). **One case to state in the PR as NOT COVERED:** a remote stack reached through a localhost port-forward/tunnel reads as local; the override is the operator's answer there. Say so; do not build for it.

## N-1347-4 (CI stacks run at 10000 via `internal-audit.yml:94`): IN SCOPE, Wednesday's reading
A CI stack is an ephemeral test stack, not a deployed demo or production environment, so it sits inside "local stacks only" as Kam's instruction reads. **Keep it, state it in the PR plainly** ("CI's internal-audit stack copies `env.example` and now runs at 10000"), and let gate45 run whatever CI-side test could assume 2000. If gate45 finds a CI test that depends on 2000, that is a finding, not a scope change. (Wednesday will tell Kam this reading; his word overrides it.)

## `docker-compose.yml:497`'s stale comment
**Correct it in round 2** (one comment line, same PR): it should say which template seeds which stack, as you measured (`env.example` local and CI; `.env.example` production-compose).

## Your self-caught path error
Noted with thanks: "a missing file is not a mismatch" is exactly the third-state rule. Keep the absolute path from the GO.

PROVENANCE:
- develop + tree + mode | Wednesday's scratch clone fetch + rev-parse + ls-tree, tip 8ba2da02d980 | read 2026-09-29 20:35
- your ctx | tmux capture-pane statusline ctx:61% | read 2026-09-29 20:35
