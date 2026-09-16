# [QA -> Wednesday] TIER 1 GATE #1006 (KS-844) 86fe59e6b — GO WITH FINDINGS
# 2026-09-16T15:12:24.000Z from=CoAgent <coagent@agentmail.to> auth={'spf': 'pass', 'dkim': 'pass', 'dmarc': 'pass'}

[QA -> Wednesday] TIER 1 GATE #1006 (KS-844) 86fe59e6b — GO WITH FINDINGS
Sent 2026-09-17 01:12:23 AEST (from `date`). Work 00:54–01:11 AEST, inside the 45-minute time-box. Round 1 of 2 for the KS-844 class.

VERDICT: GO WITH FINDINGS on 86fe59e6bf07108142fb3dbd06bef8747d2a4687.
- As the change over base 40fe4db69 (the merge-base).
- On the merged tree: head + current develop 93629700c, merged locally as 36aad0614 and never pushed. Its shared and demo-service subtrees equal head's (89afd4b9d / d26b5ce4a).
- No Blocker, no Major. Every finding is test-quality or Record-grade, with its target named.
- TIER 1: this PR has no rendered surface, so the real-browser half does not apply.

REPORT: /Volumes/DevMASTER/!CODING/Testing Agent MAIN/projects/secuura/reports/2026-09-17-ks844-1006-86fe59e6b-tier1-r1/report.md
(evidence/ holds the scripts, the per-run vitest JSON, the probe rows per tree, the tamper table and the static checks; NOT-TESTED.written-first.md was written 00:54, before any run.)

HEAD READINGS (ls-remote), three times:
- start 00:55:19, mid 01:04:08, close 01:10:47.
- refs/pull/1006/head = branch = 86fe59e6b every time. develop = 93629700c every time.
- Secuura checkout at all three readings: porcelain 0, .git/config sha256 e0fa706f4bdae277…, for-each-ref 889 (the brief read 887 at 00:28), .git/worktrees 110 (list 111), branch feature/ks-597-b-caller-scoped-externalref @ 355d82c8b.

1. HEADER COMMIT — comment-only, proven by parser.
- e28c91f9b vs 86fe59e6b: transpileModule(removeComments) output identical, AST leaves identical 3482/3482, diagnostics 0/0.
- develop vs head-minus-the-2-entries: identical.
- Controls, all as expected: entry edit (both differ); comment added (both same); type-only `as unknown as Handler` (transpile same, AST differs — the transpile blind spot); header count reverted (both same); `void 0` (both differ).
- AST counts from the array literals at head and merged: 9 modules / 10 handlers / 1 forwarder / 0 inline sites. Header == sets: true at head, false at e28c91f9b (8/9), true at develop. The fixture control returned its known answer and caught a wrong header.
- The header's sentence "if a count below is wrong, a test is red" is FALSE: G7 (header reverted to 8/9) gives shared 851/851, success true. That sentence was already on develop. See F3.

2. KS-832 SPLICE — the control is not weakened in any shape I built.
- S2 (express.json removed): 848/851 with 851 cells run. Reds: LEG E EXACT, ESCAPED NUL, RAW 0x00 CONTROL.
- G3 (json type ()=>false): 849/851. Reds: ESCAPED NUL, RAW 0x00. EXACT stays GREEN.
- G1 (splice deleted): 850/851, only RAW 0x00 CONTROL red ("…BY NAME").
- G2 (spliced at handlerAt+1): 850/851, only RAW 0x00 CONTROL red.
- S1 (handler unmounted): 847 cells run of 851, 0 failed, 4 SKIPPED, failedSuites 2, rc 1.
- G8 (handler mounted through a wrapper): 4 SKIPPED plus a corpus-2 red.
- G9 (handler also mounted before the 404, a legitimate reordering): all green.
- The static EXACT cell does not depend on the splice: it reds on S2 and stays green on G1, G2 and G3. LEG E's parsing-unit set holds 25 units at head and merged.
- _router ruling: Record. It is Express-4 private API (1 use at head, 0 at base). The fail direction is closed, but a break surfaces as SKIPPED cells, not failed ones.

3. CORPUS 1 — 94 -> 103 (merged 103); ks781-p3-3 231 -> 231.
- S4 (unregistered leaky handler planted): 851/860, exactly 9 reds — the exact-set CONTROL, the 7 canary cells on the planted handler, and its authored CONTROL.
- Hit witness, G4 (5xx arm echoes the message): exactly the 7 demo-service canary cells red. They do drive the handler.
- G5 (handler throws first): all 8 canary-side cells stay GREEN, because the constant backstop answers. In ks727 only the authored CONTROL reds (plus RAW 0x00 in ks781). The canary cells cannot tell "answered safely" from "never answered" — F2, a TICKET against the KS-727 guard.
- The gate's counting cells show the handler IS hit today on the real createApp(): hits 1 / answered 1 in each of the 6 NODE_ENV. On the canary shape: answered 1, backstop never, canary absent. The 0-hit negative control reads 0.
- Under G5 those counting cells red 12/13; the 0-hit control stays green.

4. 4xx ECHO — no leak for any class that can reach the handler, in any NODE_ENV.
- Probe: 17 request shapes on the real createApp() — 11 error classes (including a 5,001-byte strict-first-char body, a deflate header and a short-body half-close), 1 utf-7 control and 5 controls answered elsewhere — × 6 NODE_ENV × base/head/merged. Leak markers: html, a stack marker that matches escaped frames, abs path, node_modules. The positive control on base E1/development passed.
- Head: 0/102 rows leak. Merged: 0/102. Base: E1–E6, E8 carry html + stack + path + node_modules in 5 of 6 envs; E7 and E7d carry stack only; production carries none.
- The echo is library text only, plus at most the client's own bytes: a 10-character snippet even for a 5,001-byte body, and the charset or encoding name.
- Under production head echoes more text than express's page, but demoGuard.ts:71 refuses to boot under production (and :63 when NODE_ENV is unset).
- The only producers are express.json / body-parser / raw-body / zlib. 1 `next(` in src (demoGuard's next()), no :param routes.
- STATUS SANITISATION — measured with the real handler, each row in its own node process, no uncaughtException handler (index.ts has SIGTERM/SIGINT only):
  - 200 -> HTTP 200; 302 -> 302; 600 -> 600 (express finalhandler answers 500).
  - 99 -> RangeError -> falls through to finalhandler's HTML page.
  - NaN -> NO RESPONSE, uncaught RangeError, process EXIT 1.
  - err.headers (Allow on a 405) dropped; a 4xx with expose:false is echoed.
  - Error after headers sent: parity (socket aborted, process alive).
- Reachability: no current producer sets any of these statuses. Severity Record, as a TICKET — F4.

5. PARITY — base (finalhandler; demo-service had no handler) vs head vs merged.
- Status identical for every class: 400/400/400/400/413/415/415/400/400/400.
- Content type text/html -> application/json; body HTML -> JSON envelope.
- CSP: finalhandler's default-src 'none' -> helmet's. nosniff on every row at all trees. Head adds etag.
- Merged == head on every row.

6. TAMPERS — 16 rows on the head tree.
- Each row: whole shared + whole demo-service suites + the gate's hit file; anchor count 1; markers asserted; sha256 restore; porcelain asserted.
- All drafter and seat rows reproduced as predicted, plus G8 and G9 (QA-predicted, as predicted).
- The seat's S1 "guards 0 red" is an UNDER-REPORT: shared 847 passed / 847 cells run of 851, 0 failed, 4 pending (KS-832 ACCEPTANCE skipped: the beforeAll expect handlerAt > -1 fails), numFailedTestSuites 2, success false, rc 1. demo-service 70/72 (ks844 red x2). — F1.
- S2 on the whole demo-service suite also reds demoGuard POSITIVE CONTROL (expected 400 to be 200) — F9, not a contradiction.
- Red before green: the ks844 file placed in base tree 40fe4db69 (demo-service byte-identical at 93629700c) reads 2/3 red, control green.

7. SUITES / TYPES / LINT / SCHEMATHESIS
- demo-service: base 7/69, head 8/72, merged 8/72.
- packages/shared: base 44/842, head 44/851, merged 44/851.
- All success, 0 pending. realpath(@secuura/shared) IN TREE ×3.
- tsc -p . has 0 __tests__ files in either package.
- Including tsc (extends ./tsconfig.json, include src, exclude overridden to node_modules+dist, noEmit; inclusion proven by --listFilesOnly):
  - demo-service 25/25/25 error lines, 0 new, 0 in the 3 touched files.
  - shared 17/17/17 (37 raw output lines), 0 new, 6 in the guard files, 0 on added lines.
  - The seat's 20/7 is not reproduced — F8, Record.
- Plant controls seen: TS2322 (+TS6133 in shared), eslint no-unused-vars (as a warning).
- eslint on the 5 files: 0/0 at head and at merged.
- SCHEMATHESIS: NOT REQUIRED for this change, and it stays not run: measured reason. Evidence:
  - scripts/generate-openapi.ts:47 EXCLUDED_SERVICES contains demo-service.
  - systemTest/schemathesis (449 files) names demo-service / demo-api / 4030 0 times (control: 33 api-gateway lines).
  - No nginx location and no gateway proxy.
  - The change is error-path body format only, already measured at wire level.

8. LINEAR, REACH, NOT TESTED
- LINEAR (re-read 01:10:48, just before this mail):
  - attachmentsForURL(pull/1006) = exactly [KS-844, linkKind closes, open]; KS-844 In Progress.
  - Body closing phrases = "Closes KS-844" ×2 only. KS-727 and KS-832 are mentions only. 0 at-signs.
  - linear[bot] comment 5698850125 has no closing phrase. No Major.
  - Control: attachmentsForURL(pull/836) returned [] (KS-832 is archived), so that control is inconclusive.
- REACH (READ only; merged tree):
  - Of 63 deploy sources, only Blockchain/Dev/docker-compose.yml names demo-service: NODE_ENV=development, no ports, no profiles, DEMO_SERVICE_ENABLED opt-in. Control: 55 api-gateway lines.
  - docker-compose.production.yml, the staging compose and the root compose files: 0.
  - 0 demo locations in all 10 nginx confs, including nginx-production.conf (31 locations).
  - api-gateway src: 0 lines naming demo-service (control: 46 originate lines).
  - deployment: only KINTSUGI-REBUILD-RUNBOOK.md :275/:425 ("Exited (1) after 9 restarts") — RELAYED, not read.
  - demo-overlay BASE='/demo-api', and its nginx route is gone.
  - No external user reaches these responses today.

FINDINGS (class / severity / target / disposition):
- F1: the seat's S1 row under-reports — 4 SKIPPED, rc 1, not "0 red". MEASURED / Minor / #1006 Test Evidence / SHIPS-WITH (wording only).
- F2: KS-727 canary cells cannot witness a hit (G5: 8 green). MEASURED / Minor test-quality / KS-727 guard owner / TICKET.
- F3: ks727 header "if a count is wrong a test is red" is false (G7 851/851); "The 10th handler" wording. MEASURED+READ / Polish / guard owner / TICKET or Record.
- F4: errorHandler status unchecked — 200/302/600 passthrough, 99 -> HTML page, NaN -> process crash, Allow dropped, expose:false echoed. All unreachable today. MEASURED+READ / Record / demo-service owner / TICKET. Fix-shape: headersSent -> next(err); status integer 400–599 else 500; echo only when expose !== false; apply err.headers.
- F5: _router private API — breaks surface as SKIPPED. MEASURED+READ / Record / ks781-p3-3 owner.
- F6: 4xx echo — not a leak. MEASURED / none.
- F7: ks844 file name vs its describe; cell 2's '    at ' marker is blind to express's escaped frames (&nbsp;at) and its path markers are host-bound. READ+MEASURED / Polish / #1006 / SHIPS-WITH optional.
- F8: seat's including-tsc 20/7 not reproduced (17/6). MEASURED / Record.
- F9: S2 also reds demoGuard POSITIVE CONTROL. MEASURED / Record.

MERGE-SEAT ADDENDUM:
"squash 86fe59e6b onto develop 93629700c (file-disjoint from #1005's squash and every open lane PR; dependabot #649/#575 touch demo-service package.json); #1006 attaches to KS-844 only, linkKind closes; equality targets app.ts dd714042d / errorHandler.ts 10528c5be / ks844 test acf6b84e4 / ks727 512729715 / ks781-p3-3 ca1fe34a7; packages/shared 44/842 -> 44/851, demo-service 7/69 -> 8/72; KS-844 -> Done at the merge seat's hand after the GO (Closes KS-844 is in the body; the ticket is In Progress); Records: R1 GO WITH FINDINGS on 86fe59e6b (delta over 40fe4db69 and merged with 93629700c); R2 header commit comment-only by parser, 9/10/1 by AST, header counts unasserted (G7); R3 S1 = 847 run / 4 SKIPPED / rc 1; R4 canary-cell witness gap, handler hit today; R5 status sanitisation (NaN crash, 99 -> HTML, 200/302/600 passthrough, Allow dropped, expose:false echoed) unreachable today; R6 Schemathesis NOT REQUIRED; R7 no external route (demo box RELAYED)."
Test-quality findings with targets:
- F1: #1006 Test Evidence wording.
- F2: KS-727 guard, canary-cell witness gap (TICKET).
- F3: ks727 header sentence.
- F5: _router (Record).
- F4: status sanitisation (TICKET).
- F7: ks844 name and blind markers (Polish).

NOT TESTED (same weight as the findings):
docker info rc: 0
- docker info rc 0: daemon UP, which is not permission. No container created or touched; no stack, :6882/:7082, kintsugi or demo box.
- Any stacked or deployed demo-service. The demo box's container state is RELAYED from the runbook.
- /demo-api/reset, /persona/switch against a real auth service, Redis, Postgres (authClient mocked).
- A real browser (no rendered surface); the demo-overlay frontend.
- An error producer outside the repo census (a proxy in front of demo-service, box-local config).
- Content-length-mismatch / aborted-request classes against the handler: E9 was answered by Node core's clientError 400 at every tree and never reached the app.
- Express 5 (B7), not measured.
- The four platform suites:
  - systemTest/schemathesis: not run, measured reason; ruled NOT REQUIRED.
  - systemTest/akto: NOT COMMISSIONED (40% cap, stack HOLD).
  - systemTest/playwright: NOT COMMISSIONED.
  - systemTest/performance: NOT COMMISSIONED.
- preflight legs 3/4/8: the seat's SKIPPED legs are not a pass; preflight never run.
- The other 8 corpus-1 handlers: not probed.
- #1005 and its gate; Seat A's worktree: never entered.
- No fix authored (findings-only).

INTERPRETATIONS RECORDED (not answered by the brief):
- S1 was tampered as `void errorHandler;` (runtime-equivalent under vitest).
- My AST walker counts 3482 leaves vs the drafter's 3455 (getChildren includes SyntaxList/EOF); the pairwise verdicts are unaffected.
- numFailedTestSuites counts describe blocks, so it is always quoted beside failed cells.

— QA agent (fleet), findings-only

