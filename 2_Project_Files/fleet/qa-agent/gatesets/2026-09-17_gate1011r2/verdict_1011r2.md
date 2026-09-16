SUBJECT: [QA -> Wednesday] TIER 1 GATE #1011 ROUND 2 (KS-871) 6dc825644 — GO WITH FINDINGS
FROM: CoAgent <coagent@agentmail.to>
TIMESTAMP: 2026-09-16T20:06:17.000Z
AUTH: {"spf": "pass", "dkim": "pass", "dmarc": "pass"}

VERDICT: GO WITH FINDINGS on 6dc8256448b50de6a15519001a4f7032ace1ae19, both as the delta over base 1125607e9 and on the merged tree 839294c16de1ec6392964daddd5d967132465abc (head + develop e0f41a8fa, local no-ff, never pushed).
QA agent (Testing Agent MAIN), findings-only. Run 2026-09-17 05:46:07 -> 06:05 AEST (clocks from date). The head was origin-verified at 05:47:07, 06:00:39 and 06:02:34; it never moved. Develop was e0f41a8fa throughout.
Report: /Volumes/DevMASTER/!CODING/Testing Agent MAIN/projects/secuura/reports/2026-09-17-ks871-1011-6dc825644-tier1-r2/report.md
(NOT-TESTED.written-first.md was written at 05:47, before any run.)

BLUF
- Round 1's three Majors are CLOSED on every measured instance, in both envs.
  - Census: 1115 requests / 119 routes, real app, 5 trees x 2 envs.
  - base vs head: REGRESSION 0. Every literal DIFF is a FIX toward canonical: test 256, production 574.
  - Head rows canonical: 1108/1108 (test), 1101/1101 (production).
- ONE NEW Minor test-quality finding (F-1011-6): SHIPS-WITH, ticketable.
- ONE §5f runtime-behaviour change: the audit trail's action / details.path changes for 256 test / 574 production rows, all toward canonical.
- No HTTP response change, so Schemathesis / Akto are NOT APPLICABLE.
- No rendered surface: the real-browser half of tier 1 does not apply.

CARRY-FORWARD (per the cap)
F-1011-1 (Major) CLOSED.
  - production: 25/25 refusal classes now gdpr.create / /api/gdpr/erasures, INCLUDING the named no-credential regression (base gdpr.create -> r1 v1.erasures -> r2 gdpr.create).
  - test: 7 CLOSED (//, //api//gdpr//, #x, absolute-form, /api/v1 x3), 18 already right, 0 open.
  - merged == head on every class.
  - Residue is pre-existing, NOT STILL OPEN: /api/GDPR/erasures -> GDPR.create and /API/GDPR/ERASURES unaudited (both -> R-4 ticket); GET clause no row (R-2, KS-871 acceptance note).
F-1011-2 (Major) CLOSED. Covers v1 / dbl / q / frag / abs / trail / canonical spellings, admitted and refused, test and production.
  - REGRESSION 0 in both envs.
  - Spelling-invariant routes: test 65 -> 118/119, production 109 -> 119/119.
  - The one split is POST /api/documents v1-user: a 5 s client timeout, pre-existing curio.
F-1011-3 (Major) CLOSED for every round-1 instance: absolute-form host (http / HTTP / v1), #frag, /api/v1/, //, v1-in-query.
  - Each -> logs.create /api/logs (or gdpr.create), replicated 2x.
  - Audit-entry probe: req.path is canonical at entry under the root mount, the v1 strip, //, #, absolute-form and the production 307 (finish shows /x, /verify trimming). Nested /gw fixture -> gate.create /api/gate/x.
  - Residue is base == head, pre-existing -> R-4 ticket (widened):
    - /api/LOGS 204 -> LOGS.create; /API/logs 204 -> NO audit row;
    - reaching gdpr spellings write caller text: gdpr/x/../erasures -> gdpr... ; ./ -> gdpr.erasures ; ;x=1 and %65 kept in the path;
    - unrouted 404s carry caller text.
F-1011-4 (TICKET KS-1187): reachability UNCHANGED (base == head == merged, statuses AND upstream lines, both envs, 2x).
  - The bypassing row now reads gdpr.create /api/gdpr/erasures.
F-1011-5 (Minor) CLOSED for its three rows.
  - G-NOMOUNT (index.ts audit mount removed) -> 3 red, so the rows come from the real app.
  - Round-1 blob f5a83ba2c -> 2 red, control green.
  - G-CTRL 3 red; G-NONGDPR 2 red.
F-1011-6 (NEW, Minor, test quality, target PR, SHIPS-WITH, ticket as a KS-871 follow-up): the production cell does not pin production mode.
  - Module-load witness, index.ts:387 csrf mount: X-CSRF-Token plus the csrf.ts:60 Secure cookie.
  - As committed: present on both production responses.
  - With vi.resetModules() removed: absent (index.ts stays test-mode), yet the file is 3/3 GREEN, because the 307 is a per-request read.
  - The "0 hits so the door" assertion also cannot tell the door from CSRF. The 403 IS the door (body INSUFFICIENT_SCOPE, measured; census boot: with-scope connector 307->200 with an upstream hit).
  - Fix-shape: assert the module-load witness and the INSUFFICIENT_SCOPE code.

ITEMS
1 Census.
  - Enumerator on head and merged: planted-mount control +2, commented plants absent; 119 routes / 1115 requests, unchanged.
  - Oracle from the request target alone, with planted controls: FIX, REGRESSION, BOTH-WRONG, SAME and missing-row all classed right. My own first control expected gdpr.erasures, wrongly; corrected in the open.
  - (a) base vs head: test literal DIFF 256 (non-gdpr 139 admitted / 91 refused; gdpr 3 / 23), SAME 859. Oracle-classed: FIX 256, REGRESSION 0, BOTH-WRONG 0.
        production literal DIFF 574 (non-gdpr 445 admitted / 91 refused; gdpr 11 / 27), SAME 541. Oracle-classed: FIX 574, REGRESSION 0.
  - (b) dev vs merged: identical counts.
  - (c) head vs merged: 0 diffs.
  - (d) head vs round-1 census_*_d3.json: 0 diffs, both envs.
  - Noise pair head vs head2: 0. base vs dev: 0 (the develop move is audit-neutral).
  - Changed fields: action / resource_type / details only. tenant, user, org, ip, ua and success: 0.
  - Wednesday's LITERAL criterion is met by 230 test / 536 production non-gdpr rows. All are oracle-FIX; the verdict rests on the oracle count, and you may overrule.
2 Refusal classes: see F-1011-1 above.
3 Canonical path: see F-1011-3 above.
4 Real-app cells: see F-1011-5 / F-1011-6.
  - NOPRODENV -> 1 red (expected 403 to be 307); R1BLOB -> 2 red; NORESET -> 0 red.
  - Curio: in the file's minimal boot, a with-scope connector gets 500 INTERNAL_ERROR with 0 hits (only ORIGINATE_SERVICE_URL stubbed). Undiagnosed; a slip against the drafter's prediction for that boot shape.
5 Tampers (whole suite, 50/417 on every row, tsc rc 0 on every row, restore sha-identical): all AS PREDICTED.
  T0 0 · R1 2 · R1P 2 · R1D 2 · TA 2 · TB 3 · G-NONGDPR 2 · TG 1 · TI 0 · G-CTRL 3 · G-NOMOUNT (QA) 3 · T0-after 0
  - TE and G-D3 are identities on this head: not run.
  - Blind to: module-load mode (F-1011-6) and a CSRF-caused 403.
6 Merge 22c0a51a8: parents 0a1f8900c + 1125607e9.
  - Tree e073733d12c8 = merge-tree of those parents. C5 CONFIRMED.
  - diff 0a1f8900c..22c0a51a8 is byte-identical to d067725ff..1125607e9 (#1010 content only).
  - Squash delta over develop e0f41a8fa: 4 files, +489 -4. Merged tree 839294c16de1ec6392964daddd5d967132465abc. For 79432c797 it would be 1429bc93f (matches the drafter).
7/11 Suites (sequential): base 47/408 · head 50/417 · dev e0f41a8fa 48/410 · merged 51/419, all green.
  - Project tsc rc 0 on all four.
  - Including tsc 30 lines / 10 files on all four; 0 in the 4 PR files; NEW 0 / GONE 0. listFilesOnly: all 4 PR files in the program on head and merged. Planted control +1.
  - eslint on the 4 files: 0 / 0.
  - shared not re-run (identical tree 89afd4b9d).
  - Correction in the open: my PARALLEL suite run showed 1 red on EVERY tree (db.retry.test.ts). Sequential and isolated reruns: all green, 12/12. Harness CPU load; curio, not #1011.
  - Disjointness: 18 other open PRs, 0 overlap, 0 touch any audit or census source file.
8 Linear (re-read 06:05:20): attachmentsForURL(pull/1011) = KS-871 [In Progress] contributes, only.
  - KS-843, KS-858 and KS-1187 (Backlog, 0 attachments) carry no #1011.
  - 0 closing phrases in the title, body, all 3 commits (including the merge) and the comment. Controls OK.
  - KS-871 stays In Progress on merge.
9 KS-1187: unchanged, see F-1011-4. D6 replicated and WIDENED (base == head, connector without subjects:erase, ENFORCED):
  - POST /api/gdpr/%65rasures -> 200; upstream "POST /api/gdpr/%65rasures" (prod 307 -> 200, "POST /api/v1/gdpr/%65rasures").
  - POST /api/gdpr/x/../erasures -> test 200, upstream "POST /api/gdpr/x/../erasures"; prod 307 -> 400.
  - NEW spellings that pass: /api/gdpr/./erasures and /api/gdpr/erasures;x=1 -> 200 with upstream hit, both envs; /api/v1/gdpr/%65rasures direct -> 200.
  - KS-858-class sibling, not KS-1187's mechanism. Whether originate routes these is UNMEASURED.
  - Escalation candidate only; nothing filed, nothing to Peter or Stuart.
10 Schemathesis / Akto: NOT APPLICABLE. 0 status diffs over 1115 x 2 envs x 3 pairs.
  - Production's 22 / 28 "product-caused" flags were timestamp-only after masking (controls OK). RETRACTED in the open; same artefact as round 1.
  - Not run (not commissioned).
12 Seat claims: C1-C9 CONFIRMED.
  - C2's "0 hits so the door" and C4's production mode are true but unpinned -> F-1011-6.
  - C1: originalUrl appears in 0 code tokens of head audit.ts.
  Records:
  - R-1 CLOSED for the fixture (the only mount is index.ts:570, root).
  - R-2 UNCHANGED.
  - R-3 MOVED: the login-429 is now auth.login in both envs; attemptedEmail is still never written (TICKET).
  - R-4 UNCHANGED and WIDENED (TICKET).
  - R-5 CLOSED by head.
  - R-6 and R-7 UNCHANGED.
  - R-8 CLOSED (the round-2 comment is measured true).
  - R-9 MOVED to 48/410 -> 51/419.

Prediction slips:
- READY: none.
- Drafter: "20 other open PRs" vs 18 at 05:58 (the count moved); with-scope 200 in the file's boot shape measured 500 (curio).
- Wednesday: the literal FAIL criterion vs the oracle-classed count.
- My own slips, all stopped loudly and re-run: an oracle control value, marker counts, zsh word-split and glob, one stray `cd /tmp` (touched nothing).

MERGE ADDENDUM
"squash 6dc825644 onto develop e0f41a8fa (merged tree 839294c16de1ec6392964daddd5d967132465abc); #1011 attaches to KS-871 only, linkKind contributes — KS-871 stays In Progress on merge (§5f: runtime behaviour — the audit trail's action / details.path change for 256 test / 574 production census rows, all toward canonical, 0 regressions); equality targets audit.ts 052131de0 / ks871 Part A 8d66dfaf7 / Part B f6bf4f9d4 / real-app ef19446f2; api-gateway 47/408 -> 50/417 at 1125607e9, 48/410 (develop e0f41a8fa) -> 51/419 merged (re-measured, sequential); Records: R-1 closed for fixture (root mount only), R-2 GET clause unmeetable via audit log, R-3 H29 attemptedEmail never written (TICKET; login-429 now auth.login), R-4 case-split / unaudited /API/ / dot-percent-; spellings / 404 caller text in action (TICKET, widened), R-5 closed (blast radius untested), R-6 seat including-tsc program root, R-7 KS-858 not in body, R-8 closed, R-9 48/410 -> 51/419; curio db.retry load-sensitive under parallel runs."
Test-quality finding: F-1011-6 (Minor, target PR, SHIPS-WITH, ticket as a KS-871 follow-up).

NOT TESTED (same prominence)
1. The §5f live sweep on a rebuilt stack (Sunday).
2. A real Postgres audit_logs write (RLS, UUID columns).
3. Deployed NODE_ENV, and whether clients call /api/v1/.
4. nginx / Container Apps / Caddy request-target rewriting (decides KS-1187 / D6 / R-4 reach).
5. Whether originate routes encoded, dot-segment or ;param paths, or re-checks subjects:erase.
6. Out-of-repo audit consumers (SIEM, dashboards): the blast radius of 574 production action changes.
7. Playwright / k6; Schemathesis / Akto runs.
8. Preflight legs 3/4/8.
9. H29 attemptedEmail fix-side.
10. packages/shared suite.
11. Sink-failure warning-log content.
12. Accessibility / browser: N/A, no UI.
docker info (run once, no container created):
docker_info_rc=0
