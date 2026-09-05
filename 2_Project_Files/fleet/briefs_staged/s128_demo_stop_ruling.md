## BLUF

**KAM RULED (panel 14:53:51 AEST) on card `secuura-demo-service-crash-loop`: STOP — "docker stop it."** This is his demo-class word, first-party on his own panel, and it authorises exactly ONE action on the LIVE DEMO: `docker stop` of the `secuura-demo-service` container. Nothing else on the demo is touched. Do it at your next boundary (before or after the KS-386 board writes, your call — it is one command), and report.

## THE ACTION — bounded
1. **Before:** read the container's state on the demo VM (`docker inspect` — `RestartCount`, `Status`, `RestartPolicy`) and the container count; copy the numbers from the output.
2. **Act:** `docker stop secuura-demo-service` — the one container, by name. **No `rm`, no compose changes, no env changes, no recreate.** `restart: unless-stopped` honours an explicit stop, so it stays stopped across the daemon's restarts; say whether the policy holds by reading it, not by assuming.
3. **After:** `docker inspect` again — `Status: exited`, `Restarting: false`, `RestartCount` unchanged from the pre-read; the container count unchanged minus nothing (a stopped container is still listed by `-a`); the other 32 containers untouched (count them). Curl the demo's public health and the portal once — both as before.
4. **Record on KS-641:** Kam's ruling (time), the before/after readings, and that persona switching stays off (the enable path — `DEMO_SERVICE_ENABLED` + `DEMO_SERVICE_KEY` — was NOT chosen).
5. **Mail Wednesday** `STATUS: demo-service stopped on Kam's ruling` with the readings.

## HOLDS
Only this container, only `stop`. If anything on the demo looks different from s127's 04:21Z reading before you act (a healthy demo-service, a different restart count by orders of magnitude, other unhealthy containers), STOP and mail Wednesday a QUESTION instead — the ruling was made on that reading.

PROVENANCE:
- Kam's ruling `stop` on `secuura-demo-service-crash-loop` | `0_Brain/dashboard/data/chat_log.json` 2026-09-05T14:53:51+10:00 and the ruled card — Wednesday's project, not yours | read 2026-09-05 14:54
- The crash-loop reading (RestartCount 2856 since 2026-09-03T04:04Z, FATAL `DEMO_SERVICE_ENABLED must be exactly "true"`, policy `unless-stopped`, host load 0.18, only unhealthy container) | s127's mail 2026-09-05T04:21:15Z — s127's read | read 2026-09-05 14:54

SELF-CHECK: re-read end-to-end for contradictions | 2026-09-05 14:54
(checked: "demo is Kam's" against "you act" — Kam's first-party ruling on his panel is the authorisation, and the action is bounded to the one command he named; "stays stopped across daemon restarts" is stated as something to READ from the policy, not asserted.)
