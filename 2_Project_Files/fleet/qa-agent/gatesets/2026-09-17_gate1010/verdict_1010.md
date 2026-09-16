hits: 1
SUBJECT: [QA -> Wednesday] TIER 1 GATE #1010 (KS-1183) c3213b04e — GO WITH FINDINGS
FROM: CoAgent <coagent@agentmail.to>
TS: 2026-09-16T18:24:39.000Z
AUTH: {"spf": "pass", "dkim": "pass", "dmarc": "pass"}
----
[QA -> Wednesday] TIER 1 GATE #1010 (KS-1183) c3213b04e — GO WITH FINDINGS

VERDICT: GO WITH FINDINGS on c3213b04e3ad96068c367f7e0ba426822d32cda9, as the delta over base f7c2f4acb AND on the merged tree cf57988d7 (head + develop d067725ff; develop never moved: 04:08:36 / 04:18:41 / 04:19:36 ls-remote, 04:23 branches API).
Round 1 of 2 for the KS-1183 class. No Blocker. Session 04:06:39–04:2x AEST (clocks from `date`).

BLUF
- L1/L2/L3/L5 are correct at head AND merged: 2xx -> 200 + delete; 302/401/500 -> 502 status:<code> + kept; refused -> 502 status:0 + kept; hung -> 502 status:0 at the bound + kept. The deps-absent (production) default measured 502 at 15,017 ms, kept. #1008's F1 is gone: base = NO RESPONSE / late 201 -> 200 + delete at 1,504 ms; head = 502 + kept.
- F1 Minor TICKET: deps.originateForwardTimeoutMs is unvalidated. 0 = silent never (NO RESPONSE). -1/NaN/Infinity/'800'/null throw in the promise executor: NO RESPONSE, originate hits 0, instance approved, one socket leaked per request. NEW vs the brief: with originate unreachable the ClientRequest has no 'error' listener yet. A plain Node process running the REAL route exits rc 1 (Unhandled 'error' event ECONNREFUSED), head and merged; controls 0/800 survive and answer 502. index.ts:1174 sends uncaughtException to gracefulShutdown (READ). Unreachable today: index.ts passes no override (READ + default measured). A trap for any env wiring (Number(unset) = NaN).
- F2 Polish TICKET: the bound is an idle timer. A 102-drip originate -> 200 at 2,503 ms under an 800 ms bound (base 2,504). The real originate sends no 1xx (READ: 0 writeProcessing/writeContinue/flushHeaders/res.write; control res.status( 123).
- F3 Polish TICKET: 201 headers + body never ends -> 200 + delete at 2 ms, then error log 'Failed to forward approved document to originate' at 804 ms (merged 803; base no log).
- F4 Polish TICKET: no cell exercises the deps-absent default. Q-DEFAULT-0 (production never) reds 0/402; 16_000 and 29_999 red 0.

THE EIGHT PLAIN STATEMENTS
1. Every forward outcome, per tree (real createVerificationRoutes, stateful store, counting originate on 127.0.0.1:0, 800 ms override):
   - 201/200/204: 200, d1, h1 in all trees.
   - 302/401/500: 502 status:code, kept in all trees (401 marker absent from the body).
   - closed port: 502 status:0, h0, kept. Destroyed before headers: 502 status:0, kept.
   - never answers: base NO RESPONSE @3,003; head 502 @805; merged 502 @806.
   - late 201: base 200 @1,504 + delete; head 502 @801, kept; merged 502 @804, kept.
   - mid-body reset / immediate close / body never ends: 200 d1 in all trees.
   - drip: 200 at ~2,503 in all trees.
   - slow 201 at 600 ms: 200 @604 in all trees.
   - negative controls (non-final step, no pending doc): h0 d0.
   - instance approved after every forward row.
   - Deletes without a completed 2xx: NONE. Keeps after a real success: NONE. Never answers: base never-answers; head/merged only the override rows 0/-1/NaN/Infinity/'800'/null (plus caller-abort rows by design).
   - Caller aborting at 100 ms: the forward still runs and deletes. Base identical, pre-existing (R2).
2. The 15 s default against every front end (READ): nginx-production proxy_read_timeout 30s (:292; connect 15s is connect-only), nginx-demo 60s (:329), nginx.conf 120s (:128), portal admin/issuer/outlook-addin/verifier 0 directives -> nginx default 60s (RELAYED), Caddy no timeout tuning (:27), Azure services.bicep apiGateway external http ingress with 0 timeout settings -> ACA default 240s (RELAYED). NONE is shorter than 15 s; the tightest is 30 s, a sound margin for a SILENT originate. Idle vs total: the 15 s is idle on the originate socket (F2); a trickling originate could outlast nginx's 30 s idle read (gateway silent upstream). Reasoned, not run.
3. The override: index.ts:891-895 passes no originateForwardTimeoutMs (bare block outside ENABLE_MOCK_ENDPOINTS), so the default is taken: 502 @15,017 ms. Explicit undefined also takes the default. 0 = never. Negative/NaN/Infinity -> ERR_OUT_OF_RANGE; '800'/null -> ERR_INVALID_ARG_TYPE; both are unhandled rejections with NO RESPONSE, hits 0, a TCPSocketWrap + globalAgent busy socket per row (end census 6/6 at head and merged, 0/0 at base). With a closed port a plain Node process dies (F1).
4. The listeners: inert (T4 0 red, Q-ERR-201 0 red; they matter only if the resolve moves to 'end': T2/T3 2 red). No double settle or double response: exactly ONE writeHead per answered request in every row of every tree, including the close-after-status-line and timer-after-headers rows. 0 express errors, 0 headers-already-sent. Leaks: none after any normal row (TCPSocketWrap 0, globalAgent busy/free 0). The pooled keep-alive socket's timeout-listener count is 1 at base = head, and a second approve on the same pooled socket answered 200 @703 ms under an 800 ms bound.
5. Lost-201 residual: RECORD for KS-1184. Head/merged: 502 @804, kept, originate created 1; caller retry -> 400 "Workflow already completed", hits stay 1, so NO duplicate by retry. Base: 200 + delete @1,503. Not worse than base above the 30 s proxy bound (base was already 504 + later delete); worse in the 15–30 s band (base answered a truthful late 200). For KS-1184: originate is idempotent only on documentUuid (documents.ts :616-648, KS-596) and the gateway forward carries none, so a re-forward would mint a second document unless it sends one.
6. Auth and approval semantics: UNCHANGED. Parser (TS AST leaf tokens): route args identical; handler outside the forward span 872 = 872 tokens IDENTICAL; controls OK (authz edit differs, 400-message edit differs, 502-branch edit differs, edit inside the span identical). Runtime with the REAL authenticateToken (throwaway keypair), identical base/head/merged, each h0 d0: no token 401, foreign-key token 401, wrong role 403, wrong user 403, already approved/completed 400 "Workflow already completed", rejected 400, unknown 404. Positive controls right role/user 200 h1 d1.
7. The test rebuild: every original expect kept or strictly stronger (401 cell: the delta on a shared counter became an absolute 0 on a fresh store, + toMatchObject + pendingDocs.has; unreachable: + 502 + status 0 + has; control equivalent, String(message) still fails on undefined). The watch cell is a LEGITIMATE watch, not decoration: T11 and QA-7b-timer-armed-logs red it. The pooled-socket risk it names produces no observable effect under any compiling tamper (T9 0 red, QA-7b-wallclock-timer 0 red; listener count identical base/head). Red before green: the head test on base = 11 run / 3 red (the seat said 10 run / 3 red, R5); at head 11/11.
8. Tampers (whole api-gateway suite at head, 402 cells run of 402, pending 0 on EVERY row, project tsc rc per row, anchors str.count 1, sha-restored):
   - Seat rows: T0 0; T1 VOID (tsc rc 2, TS6133 :426; 2 red); T1b 2; T2 2; T3 2; T4 0; T5 1; T6 3; T7 1; T8 2; T9 0; T10 0; T11 1; T0-after 0. All match the seat.
   - Drafter rows: Q-CTL 4; Q-LATE-1400 0; Q-LATE-1600 2; Q-LATE-16s 0; Q-LATE-29999 0; Q-DEFAULT-0 0; Q-DELETE 2; Q-ERR-201 0. All match the drafter.
   - My CONTROL-aimed rows: QA-CTL-no-delete-on-2xx 4; QA-CTL-default-0 1; QA-CTL-default-string 1. My item-7(b) rows: QA-7b-wallclock-timer-left-armed 0; QA-7b-timer-armed-logs 1.
   - VOID: T1. INVISIBLE: T4, T9, T10, Q-LATE-1400, Q-LATE-16s, Q-LATE-29999, Q-DEFAULT-0, Q-ERR-201, QA-7b-wallclock.
   Including tsc (in-tree config extends ./tsconfig.json, include src/**/*.ts, exclude [], noEmit; inclusion by --listFilesOnly: __tests__ 46/46/47, ks1087 listed): base 39 -> head 34 -> merged 30; ks1087 5 -> 0; NEW 0 (head vs base, merged vs head, merged vs base); 0 TS2741; plant +2 TS6133. The seat's 60 -> 53 and its TS2741 REPRODUCED with the seat's own shape (config OUTSIDE the tree, absolute extends/include): base 60 / TS2741 18 -> head 53 / 17 (keepAliveTimeoutBuffer "http" vs "node:http"; the out-of-tree program also lists undici-types). The config location decides type resolution; NEW 0 either way (R4). Project tsc rc 0 in all three trees. eslint: ks1087 test 0/0 base and head; verification.ts 0 errors, 5 warnings at both (same rules, shifted).
   linkKind as read at 04:09:26 AND 04:23:04: attachmentsForURL(pull/1010) = 2: KS-1183 contributes, KS-1087 contributes. Closing phrases 0 in title/body/commit/2 comments; positive control 2 hits, negative control 0. Disjointness: 19 (04:09) then 20 (04:23) other open PRs, 0 shared files (#1011 KS-871 touches api-gateway audit.ts + tests, no shared file). Schemathesis: NOT APPLICABLE, measured: secuura-api.yaml workflow-instances 0 (control ^paths: 1, /api/documents 28); every other spec 0. Route + 502 undocumented (R7).
   Suites: api-gateway base 46/394, head 46/402, merged 47/408, pending 0, success true. Callers: no in-repo caller of POST approve (issuer DocumentList.tsx:153 GET, mcp-server api-client.ts:106 GET).

ADDENDUM (merge seat)
squash c3213b04e onto develop d067725ff (the then-current develop, unmoved 04:08–04:23; file-disjoint from #1009's squash); #1010 attaches to KS-1183 and KS-1087, both linkKind contributes (as read at 04:09:26 and 04:23:04) — KS-1183 stays open for the §5f live sweep, KS-1087 for item 2; equality targets after the squash: verification.ts 04b3d980f / ks1087 test 4450587dc; api-gateway 46/394 -> 46/402, merged 47/408 (re-measured 04:09:58–04:10:17, pending 0); Records: R1 lost-201 residual for KS-1184 (a re-forward needs a documentUuid) · R2 a caller abort still deletes (pre-existing) · R3 cells tolerate a bound ~1.4 s late · R4 including-tsc 39->34->30 in-tree; the seat's 60->53 / TS2741 reproduced by its out-of-tree config · R5 red-before-green 11/3 · R6 checkout refs 896->897 (neighbour; config sha bb55e140e629a5f9 unchanged; .vite unchanged) · R7 route undocumented; follow-up TICKET candidates F1 (validate the override at construction; attach 'error' before setTimeout), F2, F3, F4.

CHECKOUT READINGS (read verbs only)
start 04:08:30 / mid 04:18:35 / end 04:19:31: porcelain 0/0/0; .git/config sha256 bb55e140e629a5f9… at all three; for-each-ref 896/897/897; .git/worktrees 110/110/110; HEAD 355d82c8b; refs/pull/1010/head = branch = c3213b04e at all three; develop d067725ff at all three; api-gateway .vite results.json 5,907 bytes, mtime 01:02:02 at all three (unchanged).

NOT TESTED
docker info rc:
0
(run once at 04:08:38; UP is not permission; no container created or touched)
- A live approve against a running originate (stub on loopback; documents.ts READ only).
- KS-1087 item 2 (the forward credential): out of scope.
- KS-1184 (the strand): out of scope, recorded R1.
- No live sweep on a rebuilt stack (secuura-test-discipline §5f): out of scope for the gate, owed at the Sunday QA pass.
- nginx / Caddy / portal / Azure ingress bounds READ, not measured; platform defaults RELAYED; nginx idle timer in front of a dripping upstream reasoned only.
- An HTTPS originate (L7): READ only.
- Workflow-gated document types in any environment; a real Redis.
- The gateway exit under F1: plain Node exit measured; index.ts gracefulShutdown READ.
- The 15 s default row on merged (route blob identical) and on base (no bound): not run.
- Out-of-repo callers.
- A real browser: no rendered surface, no in-repo caller, so the real-browser half of tier 1 does not apply.
- Four platform suites: systemTest/schemathesis NOT APPLICABLE (route absent from every spec); systemTest/akto, systemTest/playwright, systemTest/performance NOT COMMISSIONED (40% cap; KS-535 stack HOLD).
- Preflight legs 3/4/8 (the seat's SKIPPED legs): not a pass; not run.
- packages/shared and services/auth suites: not re-measured.
- Each tree ran once, concurrently (key rows replicate across head and merged).
- Own tooling slips, all VOID + quarantined: zsh word-split, context-free scanner, blob:path show, BSD grep \?; the vitest JSON reporter has no unhandledErrors key, so "unhandled None" means not read.

REPORT
/Volumes/DevMASTER/!CODING/Testing Agent MAIN/projects/secuura/reports/2026-09-17-ks1183-1010-c3213b04e-tier1-r1/report.md
(evidence/ beside it; NOT-TESTED.written-first.md written 04:07 before any run)

