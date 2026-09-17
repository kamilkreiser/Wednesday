SUBJECT: [Secuura/Blockchain -> Wednesday] READY FOR QA: #1037 KS-1101 @f87506f476ce83fbbc006e9f84d22454053126ad (TIER 1)
FROM: secuura-blockchain <secuura-blockchain@agentmail.to>
TS: 2026-09-17T16:18:14.000Z
AUTH: {"spf": "pass", "dkim": "pass", "dmarc": "pass"}
Seat A
Seat A 8th successor -> Wednesday: READY FOR QA #1037 KS-1101

## BLUF
**READY FOR QA: #1037 KS-1101 at `f87506f476ce83fbbc006e9f84d22454053126ad` (TIER 1)** (origin refs/pull/1037/head and the branch both read f87506f47 at 16:18:10Z, in the same action as this send; develop 34cdcfb26).
- Shape O-SURFACE, as ruled at 13:30:57Z. `/health/deep`, `/system/status` + `/api/system/status` (with the `/status/simple` body) and `/api/system/health/dashboard` show a probed service that answers 2xx `{status:'degraded'}` as `degraded`, never `up`.
- `/health/ready` and `/status/simple` keep their 200 / 503 rules, with degraded counted as not-down.
- Consumers fixed in the same PR: admin servicesOnline (healthy + degraded) and the status page's degraded style.
- KS-1101 comment `ee2bc417` names the PR. attachmentsForURL pull/1037 → KS-1101 `contributes` only; 0 closing phrases.
- No Schemathesis (13:20:51Z); the reason is in Test Evidence.

## Recommendation
Gate `f87506f47`, tier 1. Findings for the gate (in the PR body, NOT fixed):
- **F-1** `scripts/smoke-test.sh:107` passes a `/health/deep` check only when it reads `up`, so a degraded service now FAILS the smoke test.
- **F-2** `/health/services` (opt-in, 404 by default) still reads `response.ok` only.
- Out-of-repo consumers of these bodies are UNMEASURED.

## Detail
### Head and history
- `e4ef504a3` (the O-SURFACE edits + the 11-cell test, on `732c13459`; the amended WIP) → `7f10aa1d8` (develop `3961c2add` merged in) → `f87506f47` (develop `34cdcfb26` merged in).
- Both merge trees equal the read-only `merge-tree` prediction (`13964a06d`, `4f7ce40b4`); 0 shared files each time; never rebased.
- Develop read `34cdcfb26` at 16:05:11Z (before the merge) and at 16:07:15Z (in the push script).
- Files vs develop: `services/api-gateway/src/services/health.ts`, `routes/system-status.ts`, `routes/health-dashboard.ts`, the new `src/__tests__/ks1101-health-aggregates-surface-degraded.test.ts`, `frontend/admin/src/services/api.ts`, `frontend/status/index.html`.
- 0 overlap with the 21 open PRs (153 files, re-read right before the push).

### Test Evidence (as in the PR body)
- **At `f87506f47`:** RP-SOLO 4 red / 7 green at develop bytes, as predicted. Whole api-gateway suite 59 files / 576, 0 failed, 0 pending, at 60 s ceilings (load 17.77) and at default timeouts (load 20.71). tsc rc 0.
- **At `7f10aa1d8`** (the tamper table; the merge after it is disjoint): 11 / 11 rows as predicted, 0 VOID, every red an AssertionError, 1-min load 4.0–16.6.
  - RP-DEV 4;
  - READINESS-DEGRADED-AS-DOWN 2 (the ruled tamper: exactly the two readiness cells);
  - READY-DEEP-ONLY 1; READY-SIMPLE-ONLY 1;
  - DEEP-BODY-IGNORED 1; STATUS-BODY-IGNORED 2; DASH-BODY-IGNORED 1;
  - T0 / T0-DEFAULT / TI 0 (58 / 567).
- eslint 0 / 0 on the 3 source files and the test (the source files are also 0 / 0 at develop bytes).
- `npm run check:openapi` rc 0 (no spec change; 405 examples), at `7f10aa1d8`.
- `npx tsc --noEmit -p frontend/admin` rc 0 (control: `--listFilesOnly` lists `src/services/api.ts`).
- Install: `Blockchain/Dev/node_modules` = develop `27e53ec3a`'s `npm ci` (vitest 4.1.11); #1033 not installed (api-gateway has no mysql2 reference).
- **NOT run / NOT covered:**
  - Schemathesis (ruled out 13:20:51Z); Akto / Playwright / k6 (no stack);
  - the status page and admin dashboard in a browser;
  - real degraded bodies (loopback stubs only); the edge;
  - out-of-repo consumers; the test-including tsc program (no count quoted).

### Mounted paths (confirmed on the real app)
- `/health/deep` = `/health/ready` (one handler).
- The system-status router mounted at `/system` and `/api/system` (`/status`, `/status/simple`).
- `/api/system/health/dashboard`.

### Push (16:07:18Z → 16:14:00Z, rc 0)
- Preflight: `PREFLIGHT INCOMPLETE — 12/15 legs ran, 3 SKIPPED. Nothing failed.` Legs 3, 4 and 8 skipped (no stack). Leg 1 spec in sync; leg 2 locks clean; leg 5 59 / 59; legs 6 and 7 no advisories outside the baseline; leg 14 shell suites 35 / 35; leg 15 21 / 21 guards.
- Verify: PROTOCOL-DIFF, config CHANGED = only the 3-line upstream section my `git push -u` wrote for this branch. Ruled benign by your 16:16:26Z ANSWER; kept, no restore; recorded in the PR body. Future first pushes: no `-u` (handover corrected).
- 4 stubs ended by verified pid (68447, 68529, 68611, 68710; control 1089 ps rows; 17 non-node listeners before and after; 0 remain).

### PR #1037
- POST 201 at ~16:17:25Z. The readback body is byte-equal; draft false; 6 files; 3 commits.
- Test Evidence block, Linear URL, `Refs KS-1101`, the Claude Code footer.
- KS-1101 was moved Backlog → In Progress by the PR/branch automation (read 16:17:35Z) and stays In Progress (§5f).

Seat A

