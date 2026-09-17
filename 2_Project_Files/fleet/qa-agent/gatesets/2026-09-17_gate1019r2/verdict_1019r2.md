SUBJECT: [QA -> Wednesday] TIER 1 GATE #1019 ROUND 2 (KS-1187) 82f09c8bd — GO WITH FINDINGS
TS: 2026-09-17T07:50:33.000Z
AUTH: {"spf": "pass", "dkim": "pass", "dmarc": "pass"}

QA TIER 1 ROUND 2 gate (round 2 of 2, the cap) — Secuura/Blockchain PR #1019 (KS-1187) @ 82f09c8bd1bfab28e4d23c180cbaffea251685be
Run 2026-09-17 17:28–17:46 AEST (clocks from date). Findings-only. Report:
/Volumes/DevMASTER/!CODING/Testing Agent MAIN/projects/secuura/reports/2026-09-17-ks1187-1019r2-82f09c8bd-tier1-r2/

BLUF / VERDICT: GO WITH FINDINGS on 82f09c8bd as the delta over round-1 head 8b8996f8b (the round-2 commit 4d551f104) and over develop
f8c7aaa39, AND on the merged tree (develop f8c7aaa39; merged-tree OID 99df1503e4f18ac444baed015659fecbb912bbb0 = the head tree = drafter 99df1503e).
F-1019-1 (the round-1 NO GO) is CLOSED. F-1019-2 and F-1019-3 CLOSED. The findings are all Record-class, none a blocker.
ROUND 2 of 2 is the cap: this is NOT a NO GO — everything the fix round was commissioned to close is closed and no new Blocker/Major is opened,
so there is no closed-instances-ship / residue-ticket split to make. The Records SHIP WITH the PR into KS-1187's facts comment.

LEAD (item 1 + disagreements 1-3): F-1019-1 CLOSED for every spelling and mount I could build.
- My r1 harness column is BYTE-IDENTICAL to round 1's rows (rows_head.json sha ee8da0..., rows_origin_head.json sha 32a94464...; cmp -s IDENTICAL). The instrument IS round 1's.
- r1 -> r2: test 134 row diffs, prod 124 diffs, EVERY one a refusal gained, 0 hits gained. The W class (W01-W17, W07 abs) flips r1 200+1hit -> r2 400 NON_CANONICAL_PATH 0 hits, both mounts (/api/gdpr test AND /api/v1/gdpr production). D34 erasures/. and D35 erasures/abc/.. 403 -> 400.
- Refined FAIL-SCAN (door/W/undetermined, no-scope): 0 bad on r2/head/merged, both modes. head vs r2: 0 status/code/hits diffs. head vs merged: 0 diffs.
- Originate stage (REAL gdprRouter): no-scope getErasureStatusByExternalRef calls r1 16 -> r2 0 -> head 0 -> merged 0.
- My OWN hunt beyond round 1's census (264 rows/tree, 2 reps): at r1, 100 no-scope rows were forwarded; at r2/head every extra spelling whose RESOLVED path names the door flips to 400/0-hits (./erasures/.., consent/../erasures/.., ERASURES/%2e%2e, erasures/%2e%2e;x=1, erasures/..;a=b, erasures/..?x=, erasures/%2e, and odd mounts /API/GDPR/erasures/.., /api//gdpr/erasures/.., /api/gdpr/./erasures/..). The rows still forwarded resolve to a NON-erasure path (abc/.., ./abc, abc/., %2E->.) — PROBED on originate's REAL router: none reaches the erasure handler. Odd mounts /api/./gdpr, /api/gdpr;x, /api/%67dpr -> 404, 0 hits.
- Legit routes (17 originate routes + 26 not-door spellings): 200+1hit, r1=r2=head=merged, 0 diffs, 0 400s. Dotted refs (ref.v2, ..ref, a.b, abc., ref..v2) 403 without / 200+1 with the scope, unchanged. No real caller's route or reference refused.
- The WITH-scope dot-after-door flip the READY does not state (disagreement 2, L9/L10): r1 200+1hit -> r2 400. Ruled RECORD: no legitimate externalRef is . or .. (RFC 3986 5.2.4/6.2.2.2); clients normalise before sending; graded against L9/L10, not base.
- Why production 400 is the door's code (disagreement 3, item 4): detector runs by PATH PREFIX not NODE_ENV (proxyPaths has /api/gdpr not /api/v1/gdpr), matches literal ../ only; the 5 prod spellings have no ../. Neuter the ../ pattern -> whole suite 55/524 0 reds (unpinned, pre-existing), prod stage 0 no-scope door/W hits (the door refuses them alone), 13 tail-429 = the limiter instrument. NOT load-bearing. Record.

PLAIN STATEMENTS, items 1-10:
1. F-1019-1 CLOSED, both mounts, both modes, r2/head/merged; r1 column byte-identical to round 1's rows; no residual raw-match walk. MEASURED+PROBED.
2. No legitimate route or dotted reference refused. erasures/abc/.. 403->400 (refused either way, 0 hits). With-scope dot-after-door flip = Record.
3. F-1019-2 CLOSED (GHARDFALSE 1 red = the router cell; G-READOUTER 0 = cannot tell door vs factory router, Record latent). F-1019-3 CLOSED (GNORESTORE 2, G-RESTORE-UNDONE 1 red for the behavioural reason; G-RESTORE-PARAMS 1 = only the ks843 text pin, so the ;param class is unpinned, Record).
4. Detector NOT load-bearing (neutered -> door refuses the same rows, 0 hits, 0 whole-suite reds). Record.
5. Merge identity: git diff f8c7aaa39 82f09c8bd = exactly the 3 PR files; PR blobs byte-identical head==r2 (795ae7ca3 / 76c0137ee / 06b499605); develop blobs byte-identical head==develop; control fires; merged tree 99df1503e = head tree. head vs r2 = only X-RateLimit-Remaining (149 test / 139 prod rows; #1017 limiter via develop). Record.
6. Round-1 standing items: absolute-form bypass stays CLOSED; every named spelling refused; Tightening A a dot-after-door 400 IS undetermined by its words (ruled consistent); ONE canonicaliser (1 erasureDoorVerdict def, 1 decodeURIComponent in src, 0 in the test); grace door rows 1 line, W rows now 400/0-lines; x-user-email 500 unchanged (RELAYED); 400 before auth and during grace (Record).
7. Tampers at head (headT, 55/524, tsc rc 0 each, no VOID, all AssertionError): T0 0 / QWFIX 24 / GHARDFALSE 1 / GNORESTORE 2 / GONLYDOTDOT 1 / GCASEFOLD 2 / GWIDE 7 / TI 0 = the seat EXACTLY; G-READOUTER 0 / G-HARDTRUE 3 / G-RESTORE-UNDONE 1 / G-RESTORE-PARAMS 1 = the drafter EXACTLY. My own G-CHECKAFTERPOP (door check moved AFTER the pop): 23 reds — reopens F-1019-1 from a direction the seat's forms do not take, and the round-2 suite CATCHES it (round 1's Q-WFIX gave 0; the fix is now pinned). Red-proof at 8b8996f8b: 70 run, 46 green, 24 red, all AssertionError (the READY exactly). Round 1's 39-cell test over the round-2 proxy: 39/39 (no cell weakened).
8. Suites: r1 54/481 / r2 54/512 / head 55/524 / develop 54/454 / merged 55/524, all pass, pending 0, tsc rc 0 each; packages/shared 44/851 at head. Test-including tsc program: 31 lines / 11 files on r1/r2/head/develop, NEW vs r1 = 0, 0 in touched files; ks1187 test IN the including program, ABSENT from the project program (491 files); plant +1 TS2322. eslint proxy.ts 4 no-unused-vars r1=r2=head, NEW 0; ks1187 test 0; controls fire.
9. Linear/GitHub (17:41, GET/query only): attachmentsForURL(pull/1019) = KS-1187 contributes AND KS-843 contributes, no closes (controls pull/1017 -> KS-1195 contributes; pull/99999 -> 0). 0 closing directives in title/body/4 commits/comments (controls fire). 0 request-target spellings in title/description. KS-1187 stays In Progress.
10. Schemathesis/Akto NOT REQUIRED / NOT APPLICABLE (spec 122d3a2f8 already declares 400 on both erasure ops; #1019 adds refusals of the same 400; no status/schema/field change; fuzzers do not emit absolute-form or dot segments). Bounds: refs/pull/1019/head never moved from 82f09c8bd; develop unchanged f8c7aaa39; checkout porcelain 0, config sha + .vite unchanged (refs/worktrees moved by other sessions, not me). Listeners: 16 login_stub.mjs = the same 16 at start and close (#1020 sessions, not mine); none mine survives; docker info rc 0, no container. NOT TESTED: the edge, a real originate service, the four platform suites, preflight legs 3/4/8, real connector traffic, the real-browser half of tier 1 (no rendered surface change — N/A).

CLOSED / STILL OPEN / NEW:
- F-1019-1 (Major): CLOSED, SHIPS-WITH.
- F-1019-2 (Minor): CLOSED, SHIPS-WITH.
- F-1019-3 (Minor): CLOSED, SHIPS-WITH.
- NEW (all Record-class, informational, SHIPS-WITH): the WITH-scope dot-after-door flip (L9); F-1019-2's cell cannot tell door vs factory router (latent, both default); F-1019-3's ;param-only restore class unpinned; the production 400 is the door's code / detector not load-bearing; the merge adds only X-RateLimit-Remaining (#1017 limiter).
- Records carried: the 400 before authentication and during the grace; the ks843 pin is a text pin on a redundant collapse call; the x-user-email 500 (KS-744 class).

MERGE ADDENDUM (for the merge seat): squash 82f09c8bd onto develop f8c7aaa39 (then-current develop; f8c7aaa39 at draft close = the head's merge-base, an ancestor) (merged tree 99df1503e4f18ac444baed015659fecbb912bbb0; drafter 99df1503e = the head tree); #1019 attaches to KS-1187 and KS-843, both linkKind contributes, no closes (as read 2026-09-17 17:41 AEST) — KS-1187 stays In Progress on merge (5f: the edge's request-target handling is unmeasured); KS-843 unchanged; equality targets after the squash: proxy.ts blob 795ae7ca3 / ks1187 test 76c0137ee / ks843 scope-gate test 06b499605; api-gateway 54/454 at f8c7aaa39 -> 55/524 at head -> 55/524 merged (re-measured; drafter 55/524); packages/shared 44/851; dispositions: F-1019-1 CLOSED SHIPS-WITH, F-1019-2 CLOSED SHIPS-WITH, F-1019-3 CLOSED SHIPS-WITH; NEW (all Record, SHIPS-WITH): the WITH-scope dot-after-door flip, the F-1019-2 door-vs-factory-router latency, the F-1019-3 ;param restore class, the detector-not-load-bearing note, the merge X-RateLimit-Remaining header; Records for KS-1187's facts comment at merge: the 400 before authentication and during the grace, the ks843 text pin, the x-user-email 500 (KS-744 class), the merged-tree = head-tree identity.

NOT TESTED (same prominence): the edge (nginx/Caddy/Container Apps ingress — the reason KS-1187 stays In Progress, 5f); a real originate service (DB, real connectorContext, its own /api/v1 handling — the in-process mock mounts /api/gdpr); the four platform suites (schemathesis/akto/playwright/performance — NOT COMMISSIONED, 40% cap, KS-535 HOLD); preflight legs 3/4/8; real connector traffic and Platform S's real reference spellings; the real-browser half of tier 1 (no rendered surface change — N/A).

The real-browser half of tier 1 does NOT apply: #1019 round 2 changes no rendered surface.
Report: /Volumes/DevMASTER/!CODING/Testing Agent MAIN/projects/secuura/reports/2026-09-17-ks1187-1019r2-82f09c8bd-tier1-r2/
Mail built 2026-09-17 17:50:20 AEST.
