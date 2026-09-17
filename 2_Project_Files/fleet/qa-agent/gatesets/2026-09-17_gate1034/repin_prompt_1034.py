#!/usr/bin/env python3
"""repin_prompt_1034.py — RE-PIN the #1034 prompt fd81a75f0 -> e4624218b by ASSERTED substitutions (count per old string). Backup .pre-0918-repin.
Asserts after: byte size <= 19,800 (the pane-paste bound this family keeps), no fd81a75f0 left except named history, no Kam's-tap merge condition, no NUL."""
import hashlib, re
P = '/Volumes/DevMASTER/WEDNESDAY/2_Project_Files/fleet/qa-agent/briefs/2026-09-17_secuura-1034-ks1215-tier1.prompt.txt'
s = open(P).read(); assert s == open(P + '.pre-0918-repin').read()
def sub(old, new, n=1):
    global s
    c = s.count(old); assert c == n, (old[:90], c, n); s = s.replace(old, new)
H = 'e4624218bc29cda4c07b2d31ca18bba422cfbc3e'
sub("""You are the fleet QA agent running ONE TIER 1 ROUND 1 gate (round 1 of 2 under the cap) over Secuura/Blockchain PR #1034 (KS-1215, Seat A) at
head fd81a75f0688f6cbe1e5f79b061bb1369c88f477.""", """You are the fleet QA agent running ONE TIER 1 ROUND 1 gate (round 1 of 2 under the cap) over Secuura/Blockchain PR #1034 (KS-1215, Seat A) at
head e4624218bc29cda4c07b2d31ca18bba422cfbc3e (RE-PINNED from fd81a75f0; no gate ran there).""")
sub("""STRUCTURAL direct-call cells per Wednesday's 11:59:12Z ruling). fd81a75f0 merged develop 27e53ec3a in; tree 6339c404c. No rendered surface changes:
say in one line whether the real-browser half of tier 1 applies. A GO is a gate verdict, NOT a merge authorisation: the merge waits for Kam's tap.""",
"""STRUCTURAL direct-call cells). fd81a75f0 merged develop 27e53ec3a; 96d859467 merged develop 3961c2add; e4624218b = the PRE-GATE FIX (Wednesday
13:51:51Z): routes/platform.ts authHeaders forwards req.headers.authorization, never rawAuthorization, +4 register-connector cells (20). Tree 6f912843b.
No rendered surface changes: say in one line whether the real-browser half of tier 1 applies.
A GO is a gate verdict: #1034 then merges on WEDNESDAY'S signed GO naming the head (the TESTED grant), NOT on Kam's tap (that is #1032's condition).""")
sub("""Its last section, RULE BEFORE LAUNCH, says how the register-connector forward is graded: grade it as that section says.""",
"""Its RE-PIN section (near the top) wins wherever a number differs; its last section, RULE BEFORE LAUNCH, grades the register-connector forward.""")
sub("""- the seat's READY (gatesets/2026-09-17_gate1034/mail_1034_ready.md) and Wednesday's receipt (receipt_1034.md);""",
"""- the seat's READY (gatesets/2026-09-17_gate1034/mail_1034_ready.md), Wednesday's receipt (receipt_1034.md), the pre-gate ruling
  (answer_pregate_register_connector.md) and the seat's HEAD MOVED mail (mail_1034_headmoved.md);""")
sub("""- gatesets/2026-09-17_gate1034/DRAFTER_REPORT.md;""", """- gatesets/2026-09-17_gate1034/DRAFTER_REPORT.md (at fd81a75f0) and the re-pin outputs under out_repin/;""")
a = s.index("Head (git ls-remote 23:03:08"); b = s.index("Repo:    /Volumes/DevMASTER")
s = s[:a] + """Head (git ls-remote 01:38:08 + 01:40:22 AEST 2026-09-18 and the PR API 01:38:38 agree; the launcher re-asserts it):
  #1034 e4624218bc29cda4c07b2d31ca18bba422cfbc3e = refs/pull/1034/head = feature/ks-1215-api-gateway-a-revoked-session-jwt-plus-a-valid-key-whose
  A fast-forward: 6c6fdc94e (the change) -> fd81a75f0 (merge 27e53ec3a) -> 96d859467 (merge 3961c2add, tree 92256f2df) -> e4624218b (the fix).
  develop 3961c2add8e1637b32e638f8f0952c328c00833e = origin develop = the merge-base: compare develop...head = ahead 4, behind 0, files 3. Blobs:
  auth.ts 6e1668362 -> bf09d315a; platform.ts 4550401f8 -> b80a8cd8d; ks1215 test absent -> 75006b5cf. Merged tree over 3961c2add = the head tree
  6f912843b (develop is an ancestor), and develop's api-gateway + shared subtrees equal 27e53ec3a's. If develop moves, merge it onto e4624218b in YOUR
  clone, name the OID, judge the move by content, and re-run items 1, 3 and 6 on the merged tree if it touches services/api-gateway/ or packages/shared/src/.
""" + s[b:]
sub("""  - The seat's records (Blockchain/5_Project_History/2026-09-17_seatA-7th/ks1215/) are READ-ONLY files: parse build/tamper_1215_r2.py's ROWS literal,
    never execute that runner (it hard-codes the seat worktree).""",
"""  - The seat's records (Blockchain/5_Project_History/2026-09-17_seatA-7th/ks1215/) are READ-ONLY files: parse r1-pregate/tamper_1215_r3_{auth,platform}.py's
    ROWS literals, never execute them (they hard-code the seat worktree, now on KS-1101). Pattern: GS/repin_tamper_1034.py.""")
sub("""  - Record the checkout's porcelain count and .git/worktrees count before and after: they must be equal (drafter 0 / 112).""",
"""  - Record the checkout's porcelain count and .git/worktrees count before and after: they must be equal (re-pinner 0 / 112).""")
sub("""  - the real-app probe at <tree>/Blockchain/Dev/qa_probe_1034/ (template GS/src/qa1034-drafter-probe.template.ts, __GW_SRC__ = the tree's api-gateway
    src),""", """  - the real-app probe at <tree>/Blockchain/Dev/qa_probe_1034/ (template GS/src/qa1034r-repin-probe.template.ts: the drafter's + JWT-only SYSTEM_ADMIN
    register-connector cells; __GW_SRC__ = the tree's api-gateway src),""")
sub("""  58 files) and `tsc -p . --listFilesOnly` lists 0 qa_probe""", """  58 files) and `tsc -p . --listFilesOnly` lists 0 qa_probe""")
sub("""What Wednesday requires (brief items 1-9; each carries drafter predictions marked predicted-by: drafter):
""", """What Wednesday requires (brief L0 + items 1-9; predictions marked drafter (fd81a75f0) or re-pinner (e4624218b)):

L0. THE PRE-GATE ROUND (the LEAD). On the REAL gateway, does POST /api/platform/organizations/register-connector with a REVOKED (or LIVE) Bearer + a
   valid key still send the caller's Authorization to /api/tenants, /api/keys (the mint) or /api/audit? Drafter at fd81a75f0: 24 (= develop); expected
   at e4624218b: 0. Re-run the whole 3,258-request census per tree (develop 3961c2add, head e4624218b; merged = head). Must hold: a JWT-only
   SYSTEM_ADMIN still 201 with its OWN Bearer; a key-only connector still connector-jwt; 0 status changes. Re-measure O1 (re-pinner: 2 STRUCTURAL
   reds only). The cache-get HANG and the no-timeout exchange fetch stay TICKET leads unless you MEASURE them reachable. Numbers: brief RE-PIN.
""")
sub("""   Drafter (measured, 3,258 cells per tree): develop 558 such cells; head 24, ALL on POST /api/platform/organizations/register-connector (platform.ts
   authHeaders prefers rawAuthorization captured at index.ts:345-350 before auth), on EVERY exchange outcome including OK, to /api/tenants, the security
   key mint /api/keys and /api/audit; develop has the same 24. 534 cells differ head vs develop, all user:<session> -> absent (or '' on the two fetch
   routes); 0 status differences; 0 on NOKEY/JUNK keys or Bearer-less callers. /api/batch/*: 401 to every caller, 0 hits, both trees.""",
"""   Drafter (3,258 cells per tree): develop 558 such cells; fd81a75f0 24, ALL on register-connector (authHeaders preferred rawAuthorization); 534 cells
   user:<session> -> absent (or '' on the two fetch routes); 0 status differences. /api/batch/*: 401 to every caller, 0 hits, both trees.""")
sub("""   denominator asserted 58 / 572 / pending 0;""", """   denominator asserted 58 / 576 / pending 0;""")
sub("""   - The seat's 8 rows from its ROWS literal EXACTLY. Drafter (measured): T0 0 · T0-DEFAULT 0 · RP-DEV 9 · DELETE-REMOVED 9 · O1 2 (STRUCTURAL only) ·
     AFTER-AWAIT 2 · NOSET 6 (ks1215 x4 + ks480 x2) · TI 0 = 8 / 8, 28 reds, all AssertionError.
   - The drafter's 7: X-DELETE-CASED 9, X-REQUIRED-ONLY 5, X-ONPROXYREQ-RAW 9, X-EMPTY-NOT-DELETE 3 (controls) and X-BEARER-PREFIX-ONLY, X-FETCH-RAW,
     X-PLATFORM-NO-RAW each 0 reds, with the consequence measured on the tampered real app (lower-case bearer forwarded; signatories forwards the
     caller's Bearer even on exchange OK; register-connector forwards none).""",
"""   - The seat's 11 r3 rows EXACTLY. Re-pinner at e4624218b: T0 0 · T0-DEFAULT 0 · RP-DEV 10 · DELETE-REMOVED 10 · O1 2 (STRUCTURAL) · AFTER-AWAIT 2 ·
     NOSET 9 · TI 0 · platform T0 0 · RAW-BACK 2 (register revoked, live) · TI 0 = 11 / 11, 35 reds, all AssertionError.
   - Drafter/re-pinner rows: X-DELETE-CASED 10, X-REQUIRED-ONLY 5, X-ONPROXYREQ-RAW 9, X-EMPTY-NOT-DELETE 3 (controls); X-BEARER-PREFIX-ONLY 0 and
     X-FETCH-RAW 0 (consequence on the real app: lower-case bearer forwarded; signatories forwards the caller's Bearer even on exchange OK);
     R-PLATFORM-RAW-FALLBACK (header || rawAuthorization) 1 red (register revoked only).""")
sub("""5. MERGE-IN: merge-tree --write-tree 6c6fdc94e x 27e53ec3a = head tree 6339c404c; brought files = develop's own delta 0a2b1603f..27e53ec3a (drafter
   44 = 44, blobs = develop's); 27e53ec3a..head = exactly the 2 files; patch-id 0a2b1603f..6c6fdc94e = 27e53ec3a..head (drafter 975abd867785); auth.ts
   6e1668362 at 0a2b1603f = 27e53ec3a. The merged tree over the CURRENT develop (drafter 92256f2df over 3961c2add).""",
"""5. MERGE-IN: both merges (drafter: 6339c404c = merge-tree 6c6fdc94e x 27e53ec3a, 44 brought = develop's; re-pinner: 92256f2df = merge-tree
   fd81a75f0 x 3961c2add, 8 brought = develop's own delta 27e53ec3a..3961c2add, blobs = develop's); 3961c2add..head = exactly the 3 files; auth.ts
   patch-id 0a2b1603f..6c6fdc94e = 3961c2add..head (70144bde53f1). Merged tree over the CURRENT develop (re-pinner: = head tree 6f912843b).""")
sub("""6. CHECKS: api-gateway develop 57/556 · head 58/572 at DEFAULT ceilings AND at 60 s on vitest 4.1.11 (drafter measured, 0 failed, load 7-9), load""",
"""6. CHECKS: api-gateway develop 57/556 · head 58/576 at DEFAULT ceilings AND at 60 s on vitest 4.1.11 (re-pinner measured, 0 failed), load""")
sub("""   eslint by rule AND message on auth.ts (both trees) and the test with a firing control (drafter: 1 pre-existing no-unused-vars warning :415 -> :424;
   test 0/0; the control fires).""", """   eslint by rule AND message on auth.ts + platform.ts (both trees) and the test with a firing control (re-pinner: no-unused-vars auth.ts :415 -> :424,
   platform.ts :980 -> :983; test 0/0; the control fires).""")
sub("""LEAD WITH item 1 and item 2:""", """LEAD WITH L0, then item 1 and item 2:""")
sub("""/Volumes/DevMASTER/!CODING/Testing Agent MAIN/projects/secuura/reports/2026-09-17-ks1215-1034-fd81a75f0-tier1-r1/""",
    """/Volumes/DevMASTER/!CODING/Testing Agent MAIN/projects/secuura/reports/2026-09-18-ks1215-1034-e4624218b-tier1-r1/""")
sub("""Verdict: ONE line — GO, GO WITH FINDINGS, or NO GO — on fd81a75f0688f6cbe1e5f79b061bb1369c88f477, as the delta over develop 27e53ec3a, AND on the""",
    """Verdict: ONE line — GO, GO WITH FINDINGS, or NO GO — on e4624218bc29cda4c07b2d31ca18bba422cfbc3e, as the delta over develop 3961c2add, AND on the""")
sub("""Give the merge seat its MERGE ADDENDUM line: "on Kam's tap only: squash fd81a75f0 onto develop <then-current develop; 3961c2add at draft close>
(merged tree <OID>; drafter 92256f2df); #1034 attaches""", """Give the merge seat its MERGE ADDENDUM line: "on Wednesday's signed GO naming the head: squash e4624218b onto develop <then-current; 3961c2add at
re-pin> (merged tree <OID>; re-pinner 6f912843b = head tree); #1034 attaches""")
sub("""equality targets after the squash: auth.ts bf09d315a / ks1215 test 5b7431af0; api-gateway
57/556 at develop -> 58/572 at head""", """equality targets after the squash: auth.ts bf09d315a / platform.ts b80a8cd8d / ks1215 test 75006b5cf;
api-gateway 57/556 at develop -> 58/576 at head""")
sub("""[QA -> Wednesday] TIER 1 GATE #1034 (KS-1215) fd81a75f0 — <GO | GO WITH FINDINGS | NO GO>""", """[QA -> Wednesday] TIER 1 GATE #1034 (KS-1215) e4624218b — <GO | GO WITH FINDINGS | NO GO>""")
# trims to hold the byte bound (content kept in the brief)
sub("""2. THE CACHE-GET-THROWS HANG (Wednesday's LEAD). (a) Can a production request make authenticateToken / getConnectorBearer reject (READ every statement
   outside a try on the connector branch and in clientRateLimit, with a positive control; then try what a request controls: key shape, duplicated
   x-api-key, validate / exchange response shapes)? (b) At develop too? (c) Did #1034 create, widen or only expose it? (d) On a REAL process, not vitest
   (which intercepts process.exit), per UNHANDLED_REJECTION_MODE unset (default exit) and survive: exit, hang, or later requests refused? Name which
   deployments run which mode (READ).""", """2. THE CACHE-GET-THROWS HANG (a TICKET lead, L0). (a) Can a production request make authenticateToken / getConnectorBearer reject (READ every
   statement outside a try, positive control; try key shape, duplicated x-api-key, exchange response shapes)? (b) At develop too? (c) Did #1034 create,
   widen or only expose it? (d) On a REAL process (vitest intercepts process.exit), per UNHANDLED_REJECTION_MODE unset (exit) and survive? Name which
   deployments run which mode (READ).""")
sub("""- A scripted edit that appends a comment to a Python line can comment out the rest of that line (the drafter's own slip): assert the written file.
""", """- A scripted edit can comment out the rest of a Python line (the drafter's slip); a phrase your guard greps must stay on one line: assert the file.
""")
sub("""4. LEGITIMATE CALLERS: a valid key + a live JWT is unchanged on exchange OK and loses the user's Bearer on exchange failure. Census (READ, case-insensitive
   git grep, positive controls) of upstream readers of the inbound Authorization beyond verifying it (drafter: originate re-forwards it to anchoring;
   tenant-provisioning to security) and of in-repo clients sending key AND Bearer together (drafter: the JS and Python SDKs send either, else-if: 0).
   A legitimate flow that breaks = a finding with its class.""", """4. LEGITIMATE CALLERS: a valid key + a live JWT is unchanged on exchange OK and loses the user's Bearer on exchange failure; a JWT-only platform
   admin keeps its Bearer on register-connector. Census (READ, case-insensitive git grep, positive controls) of upstream readers of the inbound
   Authorization and of in-repo clients sending key AND Bearer together (drafter numbers: brief item 4). A legitimate flow that breaks = a finding.""")
sub(""" Drafter at 23:34:33: 17 rows, 0 node
listeners, 0 stubs.""", """ Re-pinner at 01:47:28: 18 rows, 0 node
listeners, 0 stubs.""")
sub("""   Drafter (measured, tsx harness, head AND develop x test AND production): unset -> the throwing request's socket closes, the process exits 0, the next
   request and /health ECONNREFUSED; survive -> that request never answers, the process keeps serving (200, /health 200); head = develop on all 8 arms.
   Reachability PREDICTED none (Map caches, every fetch inside try; 0 unhandled-rejection lines over 6,516 real-app cells). A REAL request-reachable
   hang: an exchange that never answers leaves the request hanging (no fetch timeout), both trees.""",
"""   Drafter (tsx harness, fd81a75f0 AND develop; auth.ts + index.ts blobs unchanged at e4624218b): unset -> the process exits 0, next requests refused;
   survive -> that request never answers, the process serves on. Reachability PREDICTED none. The exchange with no fetch timeout hangs a request, both trees.""")
bad = [l for l in s.split('\n') if re.search(r'fd81a75f0', l) and not re.search(r'fd81a75f0 \(merge|from fd81a75f0|fd81a75f0 merged|drafter|Drafter|DRAFTER_REPORT|x 3961c2add', l)]
print('fd81a75f0 lines outside named history:', bad)
assert not bad
assert not re.search(r"waits for Kam.s tap|on Kam.s tap only", s) and "WEDNESDAY'S\nsigned GO" not in s
assert '\x00' not in s
n = len(s.encode()); print('prompt bytes', n, 'sha256', hashlib.sha256(s.encode()).hexdigest()[:16]); assert n <= 19800, n
open(P, 'w').write(s)
