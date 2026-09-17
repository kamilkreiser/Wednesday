=====MSG 2026-09-17T00:56:33.000Z {'spf': 'pass', 'dkim': 'pass', 'dmarc': 'pass'} chars 10150
QA TIER 1 ROUND 1 gate — Secuura/Blockchain PR #1019 (KS-1187) @ 8b8996f8b290ef55c35721c30f8671f982fa5a91
Run 2026-09-17 10:01–10:54 AEST (clocks from `date`). Findings-only. Report:
/Volumes/DevMASTER/!CODING/Testing Agent MAIN/projects/secuura/reports/2026-09-17-ks1187-1019-8b8996f8b-tier1-r1/

BLUF / VERDICT: NO GO on 8b8996f8b as the delta over base fa887f382 AND on the merged tree(s) — graded against the door's own oracle.
Reason: #1019 CLOSES everything it was commissioned to close (the absolute-form bypass + every named spelling, both modes, all merged trees),
but it OPENS a new walk-around of the very door it hardens — F-1019-1, the dot-segment-after-`erasures` class — which no cell and no tamper covers.
This is a NO GO candidate against the KS-843 oracle; blast radius is narrow, so Wednesday/Kam decide SHIPS-WITH vs TICKET. If the humans judge the
blast radius acceptable and ship with an immediate follow-up ticket, the residual is GO WITH FINDINGS (the door-fix itself is correct and clean).

Develop = fa887f382 (unchanged throughout; PR parent). refs/pull/1019/head never moved from 8b8996f8b. refs/pull/1017/head at my start = a067d4e3e
(its round 2; I merged both cbe29597d and a067d4e3e). Merged-tree OIDs: over develop = head tree 3bc12a363; over develop + #1017 cbe29597d =
1ed8d64dd; over develop + #1017 a067d4e3e = 269fd78e9 (all reproduced exactly, merge-tree rc 0, 0 conflicts; squash trees 135b07468 / 35974a2ff).
docker info rc 0 (no container created).

LEAD FINDING — F-1019-1 (MAJOR, NEW, widened BY #1019; target: the PR; NO GO candidate): a connector WITHOUT subjects:erase (ENFORCED), and an
`email` user, sending GET /api/gdpr/erasures/.. (also .../%2e%2e, .../.%2e, .../%2e., .../%2E%2E, .../..;x, .../%2e%2e%2fabc, .../..%2f,
.../%2e%2e%2fconsent, .../.%2e;x, ERASURES/.., //erasures/.., erasures//.., erasures/..?x=1, erasures/../ ) — 16 origin-form spellings — is REFUSED
403 with 0 hits at BASE and FORWARDED 200 with ONE upstream hit at HEAD, in test AND production, head = merged17 = merged17r2. Cause:
erasureDoorVerdict('/erasures/..') pops `erasures` -> not-door canonical '/', so the gateway forwards the RAW path; express routes the RAW
/api/gdpr/erasures/.. to originate's /erasures/:externalRef. PROBED on originate's REAL gdprRouter + requireRole (in-process, DB/logger mocked): the
status handler getErasureStatusByExternalRef is invoked with externalRef `..`, `..;x`, `../abc`, `../consent`; originate re-checks only the connector
ROLE (not the scope), so a no-scope connector reaches the handler; an `email` user is refused 403 FORBIDDEN at originate's requireRole. Under the
GRACE (flag unset) the same request is admitted at head with NO grace line (base logged one). Control W18 `erasures/%2e%2e%3bx` is judged `door` and
refused — pinning the class to the bare dot-segment forms. Blast radius (READ): a STATUS READ of a `..`-prefixed ref, tenant/org-scoped by originate,
connector-role-gated. Fix-shape (owner's): make erasureDoorVerdict fail-closed against the raw express match too — undetermined for any `..`/dot
segment once the raw first segment names the door — so /erasures/.. is refused 400. Regression cells: GET /api/gdpr/erasures/.. (+%2e%2e, .%2e, ..;x,
%2e%2e%2fabc) by a no-scope connector -> refused, 0 hits, both modes. My fix-shaped tamper Q-WFIX gives 0 whole-suite reds -> the fix direction is
UNPINNED by the existing suite. Replicated 2x.

PLAIN STATEMENTS, items 1-10:
1. Absolute-form bypass CLOSED (MEASURED): base 32 test / 28 prod no-scope door/undet rows answer 200+hit or 500; head + both merged trees 0. Every
   absolute-form variant (any host, HTTP://, https://:443, userinfo, #frag, /api/v1) flips base 200 -> head 403, 0 hits, test AND production. WITH-scope
   absolute-form admitted, forwarded origin-form. Unversioned prod -> 307. head == merged17 == merged17r2, 0 row diffs.
2. Every named spelling refused, 0 hits, both modes (403 door / 400 NON_CANONICAL_PATH). Production `../` forms answer 400 BAD_REQUEST from security.ts
   FIRST (base = head). The class hunt found exactly F-1019-1 (the dot-segment-after-erasures disagreement between the canonical verdict and express's
   raw match).
3. Tightening A: 403 = canonical names the door; 400 = undecodable first segment / `..` climbs out; forwarded = plainly not the door. All 17 originate
   gdpr routes + 26 not-door spellings -> 200 + 1 hit, base = head, both modes; 0 400s on a legitimate path. No widened refusal.
4. Tightening B: caseSensitive read from the router (undefined -> false, express default; READ). Upper-case cells refused 403; originate routes ERASURES
   case-insensitively too (READ; no caseSensitive in originate). BUT G-HARDFALSE (read replaced by constant false) = 0 whole-suite reds -> the READ is
   pinned by NO cell (F-1019-2, Minor). G-HARDTRUE 3, G-ROUTERCS 5.
5. ONE canonicaliser (erasureDoorVerdict defined once; 1 decodeURIComponent in api-gateway src; 0 in the test). normalisePath's collapse is not a second
   door canonicaliser. req.url restored (setter spy on a bare app): admitted requests forwarded as sent, absolute-form -> origin-form, //erasures ->
   collapsed. G-NORESTORE reds only the ks843 text pin; the "restored" control stays green with the restore removed (F-1019-3, Minor; behaviour correct).
6. WITH-scope connector admitted in both forms, forwarded as sent (200 + 1 hit, every tree/mode); non-erasure gdpr paths unchanged vs base. L1-L10
   unchanged; L11 = the W class (F-1019-1).
7. ks843 pin CORRECTED, not weakened. Red-proof: ks1187 over base proxy = 39 run / 7 passed / 19 TypeError / 13 AssertionError (= the READY exactly);
   new ks843 over base proxy 9/10; old ks843 at c1 9/10; old over old 10/10. Full tamper table, every row tsc rc 0 (no VOID), 54/481 pending 0, sha-
   restored: T0 0 / T739 7 / TC 8 / TW 4 / TI 0 / G-HARDFALSE 0 / G-HARDTRUE 3 / G-ROUTERCS 5 / G-NOCOLLAPSE 1 / G-NORESTORE 1 / G-NODECODE 6 /
   G-NOPARAMS 3 / G-DOTS 2 / G-CLIMB 3 — EVERY seat/drafter prediction reproduced exactly. Gate's own: Q-WFIX 0 reds (W-fix unpinned), Q-WPOPFIRST 4
   (pins climbing, not the W walk). packages/shared 44/851.
8. x-user-email 500: pre-existing (KS-744 class), base = head where the door admits, not gdpr-specific (anchors/documents 500 too). At base the no-email
   absolute-form bypass read as a 500/0-hit refusal-lookalike -> D03 abs noemail_noscope base 500 -> head 403. My tokens carry email, so item-1 counts
   are honest. Record.
9. Merge interplay clean: suites base 53/442 -> head 54/481 -> merged17 55/489 -> merged17r2 55/493, all pass, pending 0, project tsc rc 0 each;
   packages/shared 44/851. Items 1-2 on both #1017-merged trees: 0 row diffs vs head. #1017 per-key limiter (ONE api_key principal): Remaining 99->98->
   97->96 (a refused 403 consumes allowance)-> [400 not counted]->95->94 (the W-class erasures/..)->93. Including tsc: 31 lines / 11 files on base/head/
   both merged, NEW 0, plant +1, ks1187 test in the head/merged program (absent base). eslint proxy.ts 4 no-unused-vars base = head = merged17r2;
   ks843/ks1187 tests 0; controls fire.
10. Linear (query, re-read 10:54:45 immediately before this mail): attachmentsForURL(pull/1019) = KS-843 contributes + KS-1187 contributes, NO closes;
    controls pull/1017 -> KS-1195 contributes, pull/99999 -> 0. 0 closing phrases in title/body/both commits/the issue comment (regex controls fire).
    0 request-target spellings in title/body (controls 6/6). KS-1187 stays In Progress on merge (§5f). Schemathesis/Akto NOT APPLICABLE / NOT REQUIRED:
    the spec (blob 122d3a2f8, identical base=head) already declares 400 on both erasure ops, so the NON_CANONICAL_PATH 400 is not a spec divergence;
    #1019 changes no status/schema/field; spec fuzzers don't generate absolute-form or dot segments. NOT RUN (40% cap, not commissioned).

RECORDS (rule, not blockers): F-1019-2 (Minor, Tightening B read unpinned), F-1019-3 (Minor, req.url-restore control cannot fail for its stated
reason), the 400-before-auth and 400-during-grace order, the ks843 pin is a text pin on a redundant collapse call.

NOT TESTED (same prominence): the edge (nginx/Caddy/Container Apps ingress — the reason KS-1187 stays In Progress, and the reason F-1019-1's real-world
production reachability is UNDECIDED: if the edge normalises erasures/.. -> erasures, F-1019-1 never fires); a REAL originate (F-1019-1's upstream reach
is PROBED on originate's real router with DB/logger mocked, and its production /api/v1 handling is untested — my mock 404s the v1 path); the four
platform suites (schemathesis/akto/playwright/performance — 40% cap, KS-535 stack HOLD); preflight legs 3/4/8; real connector traffic; the real-browser
half of tier 1 (no rendered surface change — N/A).

MERGE ADDENDUM (for the merge seat): squash 8b8996f8b onto develop fa887f382 (then-current develop; fa887f382 at draft close = the PR parent) (merged
tree 3bc12a363 over fa887f382; 1ed8d64dd over fa887f382 + #1017 cbe29597d's squash; 269fd78e9 over fa887f382 + #1017 a067d4e3e's squash); #1019
attaches to KS-1187 and KS-843, both linkKind contributes, no closes (as read 2026-09-17 10:54:45 AEST) — KS-1187 stays In Progress on merge (§5f: the
edge's request-target handling is unmeasured); KS-843 unchanged; equality targets after the squash: proxy.ts blob db1534753 / ks843 scope-gate test
06b499605 / ks1187 test 389e51e1d; api-gateway 53/442 at fa887f382 -> 54/481 at head -> 55/489 (merged17, #1017 cbe29597d) / 55/493 (merged17r2, #1017
a067d4e3e) (re-measured; drafter 54/481 / 55/489 / 55/493 agree); packages/shared 44/851; Records: F-1019-2 (Minor, PR), F-1019-3 (Minor, PR), and
F-1019-1 (MAJOR — the gate's NO GO; target the PR; SHIPS-WITH or TICKET is the humans' call).

Listener census: start (10:01:59) 16 LISTEN, 0 node, 0 login_stub.mjs; close (10:53:56) 16 LISTEN, 0 node, 0 login_stub.mjs, 0 procs with cwd in my
workdir — no leak; I SIGTERM'd nothing (nothing of mine survived a run). Checkout READ-ONLY: porcelain 0 / worktrees 111 / .vite unchanged, start=mid=
close; all writes in my --shared clone from script files; scratch quarantined by rename, never rm.
