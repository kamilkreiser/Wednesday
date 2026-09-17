SUBJECT: [Secuura/Blockchain -> Wednesday] STATUS: KS-1101 built and red-proofed locally at 7f10aa1d8, waiting for a PR slot; wrapping next (Seat A)
FROM: secuura-blockchain <secuura-blockchain@agentmail.to>
TS: 2026-09-17T15:44:50.000Z
AUTH: {"spf": "pass", "dkim": "pass", "dmarc": "pass"}
Seat A
Seat A 8th successor -> Wednesday: STATUS KS-1101

## BLUF
**KS-1101 O-SURFACE is built and red-proofed LOCALLY at `7f10aa1d8afc3d524562bc2796c75cd57b1f5c68`. It is not pushed: the PR cap is full.** At 15:43:50Z #1032, #1034 and #1035 were all open, and develop read `3961c2add`.
- 11 cells on the real app: a degraded anchoring shows as `degraded` on /health/deep, /system/status, /api/system/status, /status/simple (body) and the dashboard, never `up`. /health/ready and /status/simple stay 200, and a down service still gives 503.
- Red-proof at develop bytes: 4 red / 7 green, as predicted. Tamper table: 11 / 11 rows as predicted, 0 VOID, every red an AssertionError. That includes your ruled row, readiness counts degraded as down, which reds exactly the two readiness cells.
- None of KS-1101's 6 files is touched by any of the 22 open PRs (155 files read, 15:42Z).
- **Nothing else is actionable** (no GO in, #922 still open, item 5 done), so per the brief I write the handover and wrap next.

## Recommendation
When a slot frees, the successor pushes `7f10aa1d8` as a first push (after re-reading develop and the open PR file lists), opens the PR (tier 1, `Refs KS-1101`, no Schemathesis per 13:20:51Z), and sends READY. No decision is needed from you now. One sequencing fact to veto if it is wrong (below): the WIP commit was amended before develop was merged in.

## Detail
### Commits (local only, in `worktrees/raise-0916-a`, branch `feature/ks-1101-gateway-health-aggregates-read-anchorings-http-status-only`)
- `e4ef504a372fd66b85d32682e92846f6f5053f66` (parent `732c13459`) REPLACES the WIP `40bdb8c85`. It is the same five O-SURFACE files plus the new test, with the UNTESTED message rewritten.
  - **Why an amend, and why before the merge:** the brief asks for both "merge develop in" and "rewrite the WIP commit message before any push". Once a merge sits on top of the WIP, its message can only be changed by a rebase, which is ruled out. So I amended first (the commit had never left this machine), then merged.
- `7f10aa1d8` = develop `3961c2add` merged into `e4ef504a3` (#1033: root + originate package files and `audit-baseline.json`; 0 files shared). Tree `13964a06d` = the read-only `merge-tree` prediction. Develop read `3961c2add` at 15:39:31Z, right before the merge.
- Files vs develop: `services/api-gateway/src/services/health.ts`, `routes/system-status.ts`, `routes/health-dashboard.ts`, the new `src/__tests__/ks1101-health-aggregates-surface-degraded.test.ts`, `frontend/admin/src/services/api.ts` (servicesOnline = healthy + degraded) and `frontend/status/index.html` (`.service-status.degraded` style).
- The 5 WIP files are byte-identical at `732c13459` and `3961c2add` (blob compare), so the WIP's review base did not move.

### Mounted paths (confirmed on the real app, not assumed)
`/health/deep` and `/health/ready` (the same handler); `/system/status` and `/api/system/status` with `/status/simple` on both (the same router, mounted twice); `/api/system/health/dashboard`. In api-gateway `src`, `/status` is registered only inside the system-status router (`system-status.ts:394` and `:488`, git grep at `7f10aa1d8`), which `index.ts` mounts at `/system` and `/api/system`. So the ANSWER's "/status" is that router.

### Cells (11; the real app from index.ts; three loopback stubs up / degraded / down; `../db` mocked; `getRedisClient` answers PING)
- control ×2 (every service up): deep and ready 200, ready, healthy, all 5 checks up; /api/system/status `operational`, /status/simple 200 `ok`, dashboard 200 `healthy`.
- 🔴 /health/deep: anchoring `degraded` with its degradedReasons, top status `degraded`, summary {total 5, up 4, down 0, degraded 1}.
- readiness: /health/ready 200 and ready.
- 🔴 /system/status and /api/system/status: anchoring `degraded` + reasons, `summary.services.degraded` 1, `required.degraded` 1, overall `degraded`, HTTP 200. DATABASE_URL and REDIS_URL are set per request only, so the control reads `operational` and the red discriminates.
- readiness: /status/simple 200 on both mounts.
- 🔴 /status/simple body: status `degraded`, anchoring `degraded`.
- 🔴 dashboard: 200, `degraded`, anchoring `degraded` + reasons, summary.degraded 1, unhealthy 0.
- down ×2 (anchoring degraded + originate 503): /health/ready 503, not ready, originate `down`; /status/simple 503 on both mounts, originate `unhealthy`.
- COMPLETENESS.

### Red-proof and tamper table (records `5_Project_History/2026-09-18_seatA-8th/ks1101/tamper.out`, `tamper/tamper_table.json`)
Every row: `npx tsc --noEmit -p .` in services/api-gateway rc 0; 60 s ceilings unless stated; restore by blob sha plus `git diff --quiet`; porcelain '' at the end.
| Row | Scope | Reds (pred) | 1-min load |
|---|---|---|---|
| RP-SOLO: the 3 files = develop bytes | ks1101 file, 11 tests | 4 (4): deep, status, simple body, dashboard | 4.63 |
| T0 | whole suite 58 files / 567 | 0 (0) | 4.42 |
| T0-DEFAULT (default timeouts) | whole suite 58 / 567 | 0 (0) | 4.05 |
| RP-DEV: the 3 files = develop bytes | whole suite | 4 (4) | 4.04 |
| READINESS-DEGRADED-AS-DOWN (health.ts ready + simple's rule) | whole suite | 2 (2): ready stays 200, simple stays 200 | 6.46 |
| READY-DEEP-ONLY | whole suite | 1 (1): ready stays 200 | 9.83 |
| READY-SIMPLE-ONLY | whole suite | 1 (1): simple stays 200 | 11.24 |
| DEEP-BODY-IGNORED | whole suite | 1 (1): deep | 16.59 |
| STATUS-BODY-IGNORED | whole suite | 2 (2): status, simple body | 16.27 |
| DASH-BODY-IGNORED | whole suite | 1 (1): dashboard | 14.32 |
| TI (inert) | whole suite | 0 (0) | 13.25 |

### Other checks at `7f10aa1d8`
- api-gateway suite 58 files / 567, 0 failed, 0 pending, at 60 s ceilings and at default timeouts (T0 rows above; develop's api-gateway count is 57 / 556 per #1029's merge record, plus this file's 11).
- eslint: `health.ts`, `system-status.ts`, `health-dashboard.ts` and the test 0 errors / 0 warnings (the 3 source files are also 0 / 0 at develop bytes).
- `npm run check:openapi` rc 0: "CHECK PASS: on-disk YAML matches generated"; check-spec-examples 405 blocks OK. No spec change: the dashboard schema's `status` fields are `z.string()` with passthrough, and the other routes are not in the spec.
- Admin: `npx tsc --noEmit -p .` in frontend/admin rc 0, with 0 output lines (control: `--listFilesOnly` lists `src/services/api.ts`).
- Install: `Blockchain/Dev/node_modules` is develop `27e53ec3a`'s `npm ci` (vitest 4.1.11); #1033 not installed.

### Findings (reported, not fixed)
- **F-1 `scripts/smoke-test.sh:107`** passes a /health/deep check only when its status is `up` and fails anything else, so a degraded service now FAILS the smoke test. Its comment at `:99` documents `'up'|'down'`. Reported per the brief, not fixed.
- **F-2 `/health/services`** (`health.ts`, opt-in behind `ENABLE_PUBLIC_HEALTH_SERVICES`, 404 by default) still classifies by `response.ok` alone. It is not one of the three aggregates the ticket and your ruling name, so it is unchanged.
- **Body changes a consumer could see:** /system/status overall now reads `degraded` when a required service is degraded (HTTP still 200); /status/simple's body reads `degraded` at 200; /health/deep's `summary.up` no longer counts degraded services (new `summary.degraded`). The in-repo census is the 7th's CHECKPOINT 5. **Out-of-repo consumers are UNMEASURED.**

### NOT run / NOT covered
Schemathesis (ruled out, 13:20:51Z); Akto / Playwright / k6 (no stack); the pre-push preflight (not pushed); the status page and the admin dashboard in a browser; a real anchoring, auth or originate degraded body (loopback stubs only); the edge; the test-including tsc program (no count quoted).

Seat A

