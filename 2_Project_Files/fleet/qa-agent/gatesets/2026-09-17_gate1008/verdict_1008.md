# [QA -> Wednesday] TIER 1 GATE #1008 (KS-1087) dd7086d5a — GO WITH FINDINGS
# 2026-09-16T17:09:58.000Z from=CoAgent <coagent@agentmail.to> auth={'spf': 'pass', 'dkim': 'pass', 'dmarc': 'pass'}

TIER 1 ROUND 1 GATE — Secuura/Blockchain PR #1008 (KS-1087 item 1) @ dd7086d5aa574285beffc515f9371a438621f25d

VERDICT: GO WITH FINDINGS. This covers dd7086d5a as the delta over base 93629700c, and the merged tree = head + develop 73d3fcb90 (#1006's squash on top of #1007's 0308b7a04). Develop was 73d3fcb90 at all four readings. The merged commit is local only (7821f9393), never pushed.

BLUF: every legitimate shape (L1-L5) is correct at head and merged. 2xx deletes; 3xx, 4xx, 5xx and transport errors answer 502 and keep the document. Auth is unchanged. The 502 body is a fixed literal plus an integer. The Ornith indentation doesn't change behaviour. The tampers red as predicted. Suites are green on base, head, develop and merged. Linear is `contributes` only.
No Blocker. The two findings with targets are F1 (a hang, Minor, new, SHIPS-WITH + TICKET) and F2 (the strand, Major product state, pre-existing cause, TICKET beside item 2).

GATE WINDOW: 01:19-01:42 and 03:03-(send time below) AEST. The API was unreachable 01:42-03:03 per your tap. Your tap said my last completed step was the parser proofs, but my record showed the static leg had also finished (qa_static.out, 01:34:18), so it wasn't re-run. The refs were re-read after the outage and hadn't moved. Work time was about 27 min of the 45-min box.

1. EVERY FORWARD OUTCOME (MEASURED; real createVerificationRoutes, stateful store, hit-counting originate stub on loopback; 35 cells per run, pending 0)
   - head and merged (the merged rows match head's exactly: 34 compared, 0 differ):
     - 200/201/204/299 -> 200, hits 1, delete 1.
     - 300/302/400/401/403/404/409/422/500/503, and 401 headers with a body that never ends -> 502, error.status = the code, delete 0, document kept.
     - socket destroyed before headers, or closed port -> 502 status:0, delete 0.
     - 201 headers then a mid-body reset, or a 201 whose body never ends -> 200 + delete 1, no crash.
     - accepts and never answers -> NO RESPONSE at 6 s and at 15 s, hits 1, delete 0, instance already 'approved'.
     - originate answers 201 at 3 s after the client gave up at 1 s -> the document IS created and the pending one deleted after the client left. Answering 401 late instead -> kept.
   - base: 200 + delete 1 on EVERY forward row, including the closed port with hits 0.
   - 0-hit controls: non-final step, no pending document, already-approved -> hits 0 on every tree.
   - Deleted without a completed 2xx BODY: the two mid-body rows (ruled correct in item 2).
   - Kept after a real success: none. The late-201 row is a success the caller is told is a failure (part of F1).

2. HEADERS vs 'end' (READ + MEASURED). Deleting on 2xx headers is RIGHT for this originate. originate documents.ts POST '/' persists with `await saveDocument` at :667, then answers `res.status(201).json` at :911, a single write after the persist. The idempotent 200 at :633 is only for an already-persisted row, and a throw becomes 500 at :932-934.
   G5 (resolve moved to 'end') is invisible to the 388 cells. On my harness it makes both mid-body rows HANG (there's no 'error'/'aborted'/'close' listener on proxyRes), so a naive "wait for end" fix would add a hang. Coverage gap: Record.

3. RETRY AND THE STRAND (MEASURED, stateful store). Head/merged/prod/dev:
   - Approve with originate 401 -> 502, delete 0, instance 'approved'.
   - Originate fixed, approve again -> 400 "Workflow already completed", originate hits 0.
   - Reject -> 400 "...cannot be rejected".
   The seat's stateless stub reads the same retry as 200 + delete. At base, the same input answers 200 and DELETES a document originate never created (silent loss).
   FEW HICCUPPS: Claims true; Purpose (item 1) met; History strictly better than base; User desires and Product consistency violated by the shared state (approved, no document, no re-forward path, kept document 403 PENDING_APPROVAL until its TTL; that last part RELAYED from the drafter's READ).
   Cause: verification.ts:970-972 persists 'approved' before the forward. That predates #1008.
   RULING: F2, Major product state, TICKET beside KS-1087 item 2 (persist 'approved' only after a 2xx, or add a re-forward path). Not a #1008 blocker.
   Reach is NOT ESTABLISHED: it depends on gated types existing, and originate's 401 today is RELAYED.

4. AUTH UNCHANGED.
   - Parser: the middleware args ["authenticateToken(true)","mockBodyParser"] are equal at base and head. The handler walked node by node with the forward span masked: 677/677 before, 44/44 after.
   - Controls: removing one `!` in the authz span -> DIFFERS; authenticateToken(false) -> DIFFERS.
   - My walker failed its own controls twice (blind to unary operators, then to nesting). Both were fixed, and the failing runs are kept.
   - Runtime, REAL authenticateToken with RS256 tokens from vitest.setup's in-process key:
     - no token -> 401
     - garbage bearer -> 401
     - wrong role -> 403
     - wrong user -> 403 FORBIDDEN
     - all four with originate hits 0 and deletes 0
     - POSITIVE CONTROL, right role -> 200, hits 1, delete 1
   - Identical at base, head and merged, and under production and development.
   - The ks1087 "401 cell" is ORIGINATE's 401: auth is stubbed to a pass-through there.

5. THE 502 BODY: {"success":false,"error":{"code":"ORIGINATE_FORWARD_FAILED","message":"Approved, but the document could not be created in originate; the pending document was kept","status":<code|0>}}.
   It's byte-identical under NODE_ENV test, production and development. There's no originate body marker, path or port in any of the 52 rows checked (13 non-2xx rows x 4 runs). Positive control: tamper G6 does put the marker in.
   Status-integer echo: Record (mild upstream-class disclosure to an authenticated approver). Nothing against #1008.

6. ORNITH HUNK. resolveStatus at :1003 sits inside ArrowFunction(arg of http.request), NOT inside proxyRes.on('end'). Positive control: the log('info') call is inside 'end'.
   - Head vs my re-indented copy: transpile IDENTICAL, AST IDENTICAL 5881/5881.
   - C2 (resolve moved into 'end'): both DIFFER.
   - C3 (type-only `: number` removed): transpile IDENTICAL, AST DIFFERS.
   - C4 (502 status key removed): both DIFFER.
   - The indentation does NOT change behaviour.
   - READY equality: READY -2 +10 vs applied -1 +9. After cancelling the one delete line removed and re-added: minus multiset EQUAL, plus multiset EQUAL, plus in-order EQUAL. Control (one trailing space): DIFFERS.
   - Wrapper leak paths: the executor never rejects. It has no timeout and no proxyRes error listener, so it can stay pending (F1). A synchronous throw (invalid x-user-id) gives NO RESPONSE at base AND head (parity); the escaped error text is unread.

7. TAMPERS (head, WHOLE api-gateway suite, serial; anchors by str.count = 1; markers asserted; parse-checked; sha256-asserted restore; porcelain 25/26/25):

   id        colour                     cells-run  failed  pending  reds
   T0        GREEN                      388        0       0        —
   S1        RED                        388        2       0        401 + unreachable ("expected 200 not to be 200")
   S2        RED                        388        2       0        401 ("survives a refused forward: expected 1 to be +0") + unreachable
   S3        RED                        388        1       0        control ("deleted once originate accepts: expected +0 to be 1")
   G1        RED                        388        1       0        401 only
   G2        RED                        388        1       0        control only ("expected 502 to be 200")
   G3        RED                        388        1       0        unreachable only
   G4 (3xx)  GREEN, invisible           388        0       0        my harness: 300/302 -> 200 + delete
   G5 (end)  GREEN, invisible           388        0       0        my harness: mid-body rows hang
   G6 (echo) GREEN, invisible           388        0       0        my harness: marker in the 502
   G7        GREEN                      388        0       0        —
   T0-after  GREEN                      388        0       0        —

   All rows as predicted. numFailedTestSuites is 2 per failed cell (file + describe).
   Red before green: the ks1087 file on base 93629700c -> 3 cells run, 2 fail (401 + unreachable, "expected 200 not to be 200"), control passes. It passes 3/3 on head and merged.

8. SUITES / TYPES / LINT / CALLERS / SCHEMATHESIS / LINEAR / MOUNT
   - api-gateway (serial): base 43/385 · head 44/388 · develop 45/391 · merged 46/394. All green, pending 0.
     Correction to my own first pass: I ran four suites in parallel, and that load pushed db.retry's first cell to 5,347 ms (vitest's 5 s default) -> red on all four trees. The serial re-run is green and db.retry alone is 7/7. My instrument, not the product. Record R4: that cell has little headroom under load.
   - packages/shared: base 44/842 · head 44/842 · merged 44/851. #1008 touches no shared file.
   - realpath(@secuura/shared) is IN TREE in all four trees.
   - Project tsc: rc 0, but it lists 0 __tests__ files.
   - INCLUDING tsc (exclude overridden; --listFilesOnly lists ks1087): base 30 error lines in 10 files -> head 35 in 11, verification.ts 0. The 5 NEW lines are all in the ks1087 test: :65 TS18047 'gateway', :66 TS18047 'originator', :119 TS6133 '_deadPort', :171/:172 TS18046 'body'. Plant control: +2 TS6133 and +2 eslint warnings, sha-identical restore. Grade: Polish; none hides a defect.
   - eslint: ks1087 test 0/0; verification.ts 5 warnings at base and at head (the same warnings, shifted by the diff).
   - Callers: no in-repo caller of POST .../approve. workflow-instances = 9 lines (issuer DocumentList.tsx:153 GET, mcp-server api-client.ts:106 GET); approve-caller pattern 3 (test + route). Control workflows/.*approve = 5. First-pass census controls were dead and were re-read with working ones.
   - Reach: nginx.conf:184 and nginx-demo.conf:410 location /api/ -> api_gateway_pool.
   - SCHEMATHESIS: NOT REQUIRED. The route is absent from Blockchain/Dev/docs/openapi/secuura-api.yaml (0; controls ^paths: 1, /api/documents 28), and Schemathesis can't reach an unpublished route. The behaviour is covered in-process. Stays not run: measured reason. Record R2: the route is missing from the spec (pre-existing).
   - LINEAR (re-read immediately before this mail, see the PRE-MAIL line at the end): attachmentsForURL(pull/1008) = 1 node, KS-1087, contributes, In Progress. Closing phrases in the PR body = [] and in the commit message = [] (regex control fires). No Major.
   - MOUNT: createVerificationRoutes at index.ts:891 sits in Block :883-896 with 0 ENABLE_MOCK_ENDPOINTS ancestors. Positive control: log('warn','Mock endpoints enabled') at :842 has 1. The only flag `if` spans :841-874. Mounted in every environment.

FINDINGS
- F1 (MEASURED; Minor; #1008 follow-up; SHIPS-WITH + TICKET). The forward has no timeout: an accepting, never-answering originate leaves the approve unanswered, and a late 201 creates the document after the caller got nothing (504 behind nginx at 120 s/60 s, which is READ). Oracle: History, Claims. Fix shape (owner's): a request timeout that destroys the request and resolves 0.
- F2 (MEASURED; Major product state; TICKET beside KS-1087 item 2). The strand, as in item 3.
- F3-F6 (Polish; #1008 tests; SHIPS-WITH):
  - F3: the stateless stub can't see the strand.
  - F4: G4/G5/G6 are invisible to all 388 cells.
  - F5: the 5 including-tsc lines.
  - F6: the dead deadApp/deadServer/_deadPort scaffolding (:87-120).
- Records:
  - R1: the 502 echoes originate's status integer.
  - R2: the route is absent from the published spec.
  - R3 (Open, pre-existing): a final approve with NO pending document answers "Document has been created." with 0 forwards, at base and head.
  - R4: db.retry's timeout headroom under load.
  - Checkout for-each-ref rose 889 -> 890 -> 891 during the gate. That's a neighbour's fetch; I ran only ls-remote.

ADDENDUM (merge seat)
"squash dd7086d5a onto develop 73d3fcb90 (the then-current develop at 03:05:56; file-disjoint from #1007's squash 0308b7a04 and #1006's squash 73d3fcb90, clean local merge 7821f9393; dependabot #649/#575 touch api-gateway package.json); #1008 attaches to KS-1087 only, linkKind contributes — KS-1087 stays In Progress for item 2; equality targets after the squash: verification.ts d0585dc34 / ks1087 test 7832724f3; api-gateway 45/391 -> 46/394 (both re-measured serial, green, pending 0), packages/shared unchanged by #1008 (44/851 on develop 73d3fcb90 via #1006); Records: R1 status-integer echo, R2 route absent from the published spec, R3 no-pending-document approve claims 'Document has been created', R4 db.retry near its 5 s timeout under load; checkout for-each-ref rose 889->891 during the gate (a neighbour's fetch)."
Test quality: F3 stateless stub, F4 invisible G4/G5/G6, F5 5 including-tsc lines, F6 dead deadApp scaffolding (Polish, SHIPS-WITH).
Strand (F2): TICKET beside item 2. Hang (F1): Minor, SHIPS-WITH + TICKET.

NOT TESTED
docker info rc (run once, a reading only; 0 containers; none created):
docker_info_rc=0
1. A live approve against a running originate, and KS-1087 item 2. Measured here: the forward carries no authorization header, only x-user-id.
2. Whether any environment has workflow-gated document types (decides whether F1 and F2 are reachable).
3. An HTTPS originate (L6): READ only.
4. A real Redis: the TTL of a stranded document. TTL.workflow's value was not read.
5. nginx's 120 s / 60 s bound on the hang: READ, not measured.
6. Out-of-repo callers.
7. A real browser or portal: there's no rendered surface, so the real-browser half of tier 1 does not apply.
8. The four platform suites:
   - systemTest/schemathesis: not run, measured reason; ruled NOT REQUIRED.
   - systemTest/akto: NOT COMMISSIONED (40% cap, KS-535 HOLD).
   - systemTest/playwright: NOT COMMISSIONED (same).
   - systemTest/performance: NOT COMMISSIONED (same).
9. Preflight legs 3/4/8 (the seat skipped them; a skip isn't a pass).
10. The unhandled-rejection text in the sync-throw row.
11. The downstream 403 PENDING_APPROVAL on a stranded document: RELAYED, not re-measured.
12. True concurrency on the final step (the in-process race interleaved serially).
13. #1006 / #1007 and their gates, and Seat A's worktree: not entered.

READINGS (checkout, read verbs only). At all four readings: porcelain 0, .git/config e0fa706f4bdae277, .git/worktrees 110, ks-597-b @ 355d82c8b, refs/pull/1008/head = branch = dd7086d5a, develop 73d3fcb90.
- start 01:20:31, for-each-ref 890
- mid 01:31:28, 891
- after outage 03:03:40, 891
- close 03:05:56, 891

REPORT: /Volumes/DevMASTER/!CODING/Testing Agent MAIN/projects/secuura/reports/2026-09-17-ks1087-1008-dd7086d5a-tier1-r1/report.md
(the evidence/ directory beside it holds the instruments, runs and JSON; NOT-TESTED.written-first.md was written before any run)

PRE-MAIL Linear/GitHub re-read: 2026-09-17 03:09:55 AEST — attachmentsForURL(pull/1008) = 1 node KS-1087 contributes In Progress; body/commit closing phrases []
SENT (date): 2026-09-17 03:09:57 AEST

