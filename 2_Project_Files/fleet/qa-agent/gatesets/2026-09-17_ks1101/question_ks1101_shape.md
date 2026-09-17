auth: {'spf': 'pass', 'dkim': 'pass', 'dmarc': 'pass'}
Seat A

## BLUF
**KS-1101 is decision-shaped. Measured by read at develop `732c13459`: "map degraded to a state other than up" changes READINESS unless the shape says otherwise.**
- `/health/ready` is the SAME handler as `/health/deep` (`services/api-gateway/src/services/health.ts:166-167`). It answers 503 whenever any check is not `up`.
- **api-gateway's compose healthcheck is `/health/ready`** (`docker-compose.yml`), and **mcp-server `depends_on` api-gateway `service_healthy`**.
- **The CI boot action waits for `/health/deep` 200** (`.github/actions/boot-platform-stack/action.yml:136-142`).
- **auth and originate ALSO answer `status: 'degraded'`** in their health bodies: auth `routes/health.ts:30,50,96` (Redis or DB on the in-memory fallback), originate `routes/health.ts:37`. Anchoring does it on chain trouble (`anchoring/src/index.ts:340-358`, HTTP 200 on purpose).
So "degraded counts as down" would make the gateway container unhealthy, block mcp-server's start and fail the boot action whenever the chain is unreachable. With a generic body read, it would do the same whenever auth runs on in-memory Redis.
Meanwhile: continuing with the KS-1204 push, PR and READY. Nothing is built for KS-1101.

## Recommendation
Rule the shape. **DEFAULT (O-SURFACE, veto):** surface `degraded` in every aggregate body WITHOUT changing any HTTP status or readiness.
1. `health.ts` deep/ready: a probed service whose response is 2xx with JSON `status: 'degraded'` becomes `checks.<name>.status: 'degraded'`, plus its `degradedReasons` when present. `ready` and the HTTP status still count only `down`, so `/health/ready` stays 200 and the compose healthcheck, mcp-server and CI are unchanged. The top-level `status` reads `degraded` when any check is degraded or down.
2. `system-status.ts` `checkServiceHealth`: a new `'degraded'` value. `/status`'s `overallStatus` is `'degraded'` when a required service is degraded (a body field; it already has that value). `/status/simple` keeps its HTTP rule, with degraded counting as healthy for the 200/503.
3. `health-dashboard.ts`: service `status: 'degraded'`, plus an additive `summary.degraded` count; it is not counted as healthy.
4. Scope: every probed service's body (generic), not anchoring only, since three services emit the value. The spec is updated where these bodies enumerate status, then `generate-openapi` + `check:openapi`.
5. Tier 1, no Schemathesis (the 3rd successor's A11 answer (a)), `Refs KS-1101`. Regression cell per the ticket: a stub anchoring answering 200 `{status:'degraded'}` never shows as `up` in `/health/deep`, and `/health/ready` stays 200.
**Alternative O-FAIL:** degraded counts as down (readiness 503). The consequences are above. **Alternative O-ANCHOR:** O-SURFACE for anchoring's body only.

## Detail
- **The ticket** (KS-1101, filed by s188 from the kintsugi deploy gate F-2): "make each aggregate read anchoring's body status and map degraded to a state other than up". It names `health.ts:132`, `system-status.ts:333` and `health-dashboard.ts:59`; at develop 732c13459 these read `response.ok` only (health.ts `probeService`, system-status `checkServiceHealth` :306-343, health-dashboard `checkService` :43-60). The ticket does not address readiness.
- **Compose** (parsed with yaml at 732c13459): healthchecks on `/health/ready` for api-gateway (:8080), originate (:4000) and auth (:4003). `depends_on` api-gateway `condition: service_healthy`: mcp-server.
- `system-status.ts` `/status/simple` (≈:466-492) answers 503 unless every required service is `healthy`, so O-FAIL there would also flip an HTTP status.
- Anchoring's own comment explains why it keeps 200 on degraded: a non-200 makes the compose healthcheck restart-loop the service, and "Liveness and chain reachability are different questions". O-SURFACE keeps that separation one level up.
- **File overlap with open PRs:** KS-1101 needs `services/api-gateway/src/services/health.ts`, `routes/system-status.ts`, `routes/health-dashboard.ts` (+ spec/tests). #1032 (auth users.ts), #1033 (root/originate package files + baseline), #1034 (api-gateway middleware/auth.ts + ks1215 test): no overlap. The KS-1204 PR (being pushed) touches `routes/verification.ts` + its test: no overlap.

