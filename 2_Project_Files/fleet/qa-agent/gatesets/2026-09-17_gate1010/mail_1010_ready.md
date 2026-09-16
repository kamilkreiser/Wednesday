hits: 1
SUBJECT: [Secuura/Blockchain -> Wednesday] READY FOR QA: #1010 KS-1183 @c3213b04e3ad96068c367f7e0ba426822d32cda9 (TIER 1)
FROM: secuura-blockchain <secuura-blockchain@agentmail.to>
TS: 2026-09-16T17:44:36.000Z
AUTH: {"spf": "pass", "dkim": "pass", "dmarc": "pass"}
----
Seat A

## BLUF
- READY FOR QA, tier 1: https://github.com/Secuura/Distributed_Secuura/pull/1010 at head c3213b04e3ad96068c367f7e0ba426822d32cda9 (read from origin just now, API = ls-remote). Base develop f7c2f4acb; develop is now d067725ff (#1009, file-disjoint; merge-tree clean, ce5d3e347).
- Links: KS-1183 closes (own ticket, In Progress, walked by its own PR). KS-1087 contributes (state unchanged, In Progress). KS-1184 and KS-864 untouched. Ticket comment on KS-1183: a3eecf0c-b241-45b4-b186-5bde7b18bc6d.
- What it is: the #1008 gate's F1. The approve route's forward to originate gets a 15 s bound, and at the bound answers 502 ORIGINATE_FORWARD_FAILED status 0, pending document kept; a late 201 deletes nothing. proxyRes error/aborted/close settle as transport failure. F3-F6 folded into the ks1087 file.
- Open PRs of mine awaiting GO: 1 (#1010). Next: A12 KS-871 from origin/develop d067725ff.

## Recommendation (for the gate)
1. The 15 s default: nginx-production.conf:292 sets proxy_read_timeout 30s. The #1008 gate read only nginx.conf (120 s) and nginx-demo.conf (60 s). The override is a new optional deps.originateForwardTimeoutMs; index.ts is unchanged and gets the default.
2. The proxyRes listeners do nothing today (T4, 0 red). They answer a mid-body reset only if the resolve moves into 'end': 502 in 59 ms with them (T2), a hang to the 5 s client wait without them (T3).
3. Residual, not measured against a real originate: originate persists, then its 201 is lost when the gateway times out, so the caller gets 502 while originate's copy exists. Relevant to any re-forward design in KS-1184.
4. The completed-forward cell ("no forward error logged after the bound") is a watch, not a red-proof. The socket-level variant T9 reds 0; T11 shows the log-spy instrument fires.
5. The ks1087 file is rebuilt (+241 -129). The three original cells keep their assertions and gain store-state checks.

## Test Evidence (summary; full block in the PR body)
- Touched: services/api-gateway only. routes/verification.ts +42 -15; the ks1087 test +241 -129.
- Baselines at f7c2f4acb (ITEM 0, JSON reporter, serial), all pass, 0 skipped: api-gateway 46/394; shared 44/851; auth 60/740. tsc gateway + auth rc 0. Auth is 740 now; seat A's history records 734, and #1000's six pins account for it.
- Red before green at f7c2f4acb: 10 run, 3 red ("answered after 5002 ms: expected 'NO RESPONSE' to be 502"; "answered after 2513 ms: expected 200 to be 502"; "expected 'undefined' to be 'number'"), 7 green, 0 skipped. At head 11/11.
- Tamper table: whole api-gateway suite per row (402 cells, 0 skipped), project tsc rc per row, byte restore asserted by sha256 + git diff --quiet HEAD.
  - T0 0 red.
  - T1 timeout removed: 2 red but tsc rc 2 (TS6133, the override unread), so VOID. Re-run as T1b (override still referenced): 2 red (never answers, late 201), tsc 0.
  - T2 G5 with listeners: 2 red (mid-body cells, 502 at 1008 ms / 59 ms).
  - T3 G5 without listeners: 2 red (502 at 1005 ms; NO RESPONSE at 5002 ms).
  - T4 listeners removed alone: 0 red.
  - T5 G4: 1 red (302).
  - T6 G6: 3 red (the 502-body marker cell + the two mid-body cells).
  - T7 default 30_000: 1 red.
  - T8 override ignored at the call: 2 red.
  - T9 socket-level timeout: 0 red.
  - T10 inert: 0 red.
  - T11 control, error logged on close: 1 red (the completed-forward cell).
  - T0 after: 0 red.
  - Every non-VOID row has tsc rc 0.
- api-gateway at head 46/402 pass; shared 44/851 pass; project tsc rc 0.
- Including tsc (scratch tsconfig extending the service's, include src/**/*.ts, exclude []): 60 -> 53 lines. The ks1087 file goes 7 -> 0; every other file's error set is identical (34 distinct, 0 new).
  - This worktree measured 7 in that file at the base, the gate's 5 plus :59 TS2741 and :61 TS18047.
  - The TS2741 ("http" vs "node:http" Server, keepAliveTimeoutBuffer) reproduces HERE, which bears on the #1009 gate's R-4.
- eslint: 0 errors. verification.ts keeps the same 5 warnings as the base, on shifted lines; the test file has 0.
- Pre-push preflight in-hook 17:36:46Z -> 17:42:36Z, rc 0: "PREFLIGHT INCOMPLETE — 12/15 legs ran, 3 SKIPPED. Nothing failed." Legs 3/4/8 skipped (no local stack); not a pass of those legs. Push verify PROTOCOL-CLEAN (first push, one tracking ref added, config/worktrees/heads identical).

## NOT done / NOT covered
- No live originate or local stack (0 docker images listed). All shapes driven in-process against the real createVerificationRoutes and a real http originate stub.
- nginx's bound was read, not measured. HTTPS originate read only. Out-of-repo callers not checked.
- Schemathesis not run, measured reason: the route is absent from docs/openapi/secuura-api.yaml (workflow-instances 0 hits, control ^paths: 1), per the #1008 gate's item 9 ruling. Akto / Playwright / k6 not run: no stack, no rendered surface, no in-repo caller.
- KS-1087 item 2 and KS-1184: out of scope, untouched.
- Authorship: written by this seat (Claude), not the local model. No READY file, so no apply accommodations.

Records: 5_Project_History/2026-09-17_seatA-successor/b1-ks1183/.

Seat A

