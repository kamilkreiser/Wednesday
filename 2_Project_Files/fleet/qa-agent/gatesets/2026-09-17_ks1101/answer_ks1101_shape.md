Wednesday -> Seat A 7th successor (Secuura/Blockchain)

## BLUF
**RULED: O-SURFACE, your default.** Every aggregate body carries `degraded` (generic, for every probed service that answers 2xx with JSON `status: 'degraded'`). No HTTP status and no readiness changes: `/health/ready` and `/status/simple` keep their current 200/503 rules, with degraded counted as not-down.
**Reason:** O-FAIL changes readiness on paths your read shows are load-bearing: the api-gateway compose healthcheck, mcp-server's `service_healthy` start, and the CI boot action's `/health/deep` wait. Anchoring's own code keeps chain reachability out of liveness on purpose. The ticket asked that degraded never shows as `up`; O-SURFACE does exactly that without redefining readiness. Generic scope rather than anchoring-only: it is one mechanism (reading a body field that three services already emit), so it does not widen what the ticket commissions.
**One condition added:** `degraded` is a NEW enum value in these response bodies, so census in-repo consumers first (item 2).

## Recommendation
1. **Order unchanged:** finish KS-1204 (push, PR, READY) first. KS-1101 builds after it, inside the cap.
2. **Before building KS-1101, census every in-repo consumer** of the three bodies' `status` / `overallStatus` / `checks.*.status` / `summary`. Cover the admin and portal dashboards, the frontends, mcp-server, systemTest, scripts and CI. **A consumer that switches on these values and has no branch for `degraded`** (e.g. `status === 'up' ? green : red`, or an exhaustive switch) is either fixed in the same PR, if it is one line in a file no open PR touches, or reported as a finding in the READY. Out-of-repo consumers are UNMEASURED: say so in the PR body.
3. Build it as you specified in O-SURFACE items 1–5. Spec update with `generate-openapi` + `check:openapi`; tier 1; no Schemathesis (the earlier A11 answer); `Refs KS-1101`. Regression cells:
   - a stub anchoring answering 200 `{status:'degraded'}` shows `degraded` in `/health/deep`, `/status` and the dashboard, never `up`;
   - `/health/ready` stays 200;
   - `/status/simple` stays 200;
   - a `down` service still gives 503.
   Add one tamper where readiness counts degraded as down: the readiness cells must go red.
4. Put the ruling on KS-1101 as a facts line when the item starts ("shape O-SURFACE ruled by Wednesday 2026-09-17: surface degraded in bodies, readiness unchanged; reason: compose / mcp-server / CI depend on readiness").

## Detail
- The file partition you measured holds: KS-1101 needs `health.ts`, `system-status.ts` and `health-dashboard.ts` (+ spec/tests), and none of #1032, #1033, #1034 or your KS-1204 PR touches them. Re-read the open PR file lists right before the push.
- O-FAIL is recorded as the rejected alternative, with the reason above. If a later need arises for readiness to track chain reachability, that is a separate decision with deploy consequences (compose restart loops), not this ticket.
- Holds unchanged: nothing to Peter or Stuart, no deploy, never Done (§5f), Refs never Closes, never delete.
