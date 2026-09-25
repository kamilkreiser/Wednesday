# Wednesday — reserved local ports

**Policy (Kam directive, 2026-08-05):** Wednesday services must never sit on
common ports — other projects' stacks use those by default (Secuura and
Datasec both run Docker services on the usual 3000/5000/8000/8080/5432/etc.
range, and 8787 is RStudio's default). Wednesday owns a dedicated block:

## Block 47780–47789 (127.0.0.1 only, never exposed)

Chosen because it is unassigned by IANA, far from every common dev default,
and BELOW the macOS ephemeral range (49152–65535) so the OS never hands it
out dynamically.

| Port | Service | Since |
|---|---|---|
| 47787 | Day Dashboard — `dashboard/serve.sh` → `server.py` (static site + WED-only write API) | 2026-08-05 |
| 47780–47786, 47788–47789 | unassigned — claim here BEFORE binding | |

Rules:
1. Any new Wednesday service takes its port from this block and registers it
   in the table above in the same change that binds it.
2. Override via `WEDNESDAY_DASHBOARD_PORT` (and equivalents) is possible but
   the default in code must stay inside the block.
3. Never bind 0.0.0.0 — remote access is Phase 4 (Tailscale) with auth.
4. If a block port is ever found held by a foreign process, do NOT kill it —
   report and pick the next free port in the block (then update the table).
