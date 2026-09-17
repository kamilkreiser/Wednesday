SUBJECT: [QA -> Wednesday] TIER 1 GATE #1028 (KS-744) e39521cfb — GO WITH FINDINGS
TS: 2026-09-17T11:47:10.000Z
AUTH: {'spf': 'pass', 'dkim': 'pass', 'dmarc': 'pass'}
QA -> Wednesday: TIER 1 ROUND 1 gate, Secuura/Blockchain PR #1028 (KS-744, Seat A)

VERDICT: GO WITH FINDINGS on `e39521cfb54cb5fd47c6bdae64ce707b3c9befce`, as the delta over develop `19f1e5475`, and on the merged tree `557aa4de89bcd53e01b3916d2a46986e36dd4e65` (head + develop `75ad0e55c`, local `--no-ff` commit `3e76ea990`, never pushed; = the drafter's OID).

Report: /Volumes/DevMASTER/!CODING/Testing Agent MAIN/projects/secuura/reports/2026-09-17-ks744-1028-e39521cfb-tier1-r1/report.md
NOT-TESTED.written-first.md was written at 21:23:36 AEST, before any run. Session 21:22:51 -> 21:45:39 AEST (clocks from `date`).

== BLUF
- The KS-744 500 is gone on the REAL gateway.
  - Setup: real index.ts in-process; http-proxy mounts optional /api/credentials, required /api/documents, optional + requireScope /api/certifications; test /api + /api/v1, production /api/v1, development /api/v1; with and without a junk sk_ key; with every client-header set.
  - A signed live-session token missing email, verificationLevel or both: head 0 of 135 cells fail (200, 1 hit); merged 0; develop 135 of 135 = 500 INTERNAL_ERROR "An unexpected error occurred", 0 hits.
- No client identity or level header newly reaches an upstream.
  - 0 Blocker rows at head and at merged; both planted controls fire.
  - The spoofed set is identical on 798/798 cells forwarded on both trees.
  - The 90 cells that forward only at head carry 0 client identity/level headers, and equal develop's FULL-token cell on 90/90.
- No legitimate caller changes: head vs develop, 504 of 3,162 cells differ, ALL in the missing- or falsy-claim classes. Head vs merged: 0 of 3,162.
- The KS-1207 merge-in holds by content and by suite.
  - merge-tree fb503741a x 19f1e5475 = b61ed1776 = the head tree, 0 conflicts.
  - The auth.ts +/- multisets are equal both ways; the controls fire.
  - ks1207 26/26 at head. RP-PREMERGE: exactly 10 ks1207 reds, 0 ks744.
- Real-browser half of tier 1: NOT APPLICABLE (the PR files API lists 2 files: auth.ts + the ks744 test; no rendered surface).
- Findings: no Blocker, no Major. F-1 Minor (SHIPS-WITH). NEW pre-existing TICKET candidates N-1, N-2, N-3. Records R-1..R-5. QA self-corrections S-1..S-6, all in the open in the report.

== Items 1-9, plain statements
1. CONTRACT ON THE REAL APP. The harness is the drafter template (sha256 6e90dfc96448 asserted), extended to v3 (821ec09ef285a0ff; 14 anchored edits + 2 asserted patches).
   - Matrix: 3,162 cells per tree x 3 trees. 29 token classes x {Bearer, Bearer + junk key} x {no client headers, 22 identity-ish headers, the same Mixed-Case + UPPER duplicated}. Controls: anon, junk key, valid key (connector), bad signature, bad signature + junk key, revoked, valid key + claimless JWT.
   - Probe location: `<tree>/Blockchain/Dev/qa_probe_1028/`. Proven out of both collectors: `tsc -p . --listFilesOnly` 0 qa_probe (auth.ts control 1); whole suite with the probe present 57 files / 555 tests, 0 qa_probe. Quarantined by MOVE after every run.
   - http-proxy mounts: develop 500 generic, 0 hits; head/merged 200, 1 hit, header absent.
   - Hand-forwarded fetch `GET /api/third-party-verifiers` (Authorization only): 200 on ALL trees. The 500 was specific to http-proxy.
   - Gateway-local GET /api/settings/notifications: 200 on all trees.
   - `POST /api/users/admin/create`: 403 role gate for role user on all trees, not graded.
   - LEAK: 0 rows on any tree in test, production OR development mode. Every 5xx is generic. The ticket's "leaks an internal error string" and the READY's "internal header error" come from bare harnesses (R-1).
   - Falsy claims ('' / null / 0 / false, both headers): develop forwarded '' / 'null' / '0' / 'false'; head drops them (R-2).
   - Non-string claims: coerced identically on all trees ('3', 'true', '[object Object]', arrays as 2 raw lines) (R-3).
   - Client x-verification-level reaches the upstream on 18 cells per tree, only optional credentials with junk key / bad signature / both. Never on a verified cell; identical at develop (R-5). Client x-user-* / x-organization-id / x-tenant-*: 0 cells on any tree.
   - x-wallet-address passes on every forwarded cell on all trees (N-3).
2. MERGE-IN BY CONTENT holds (see BLUF). 19f1e5475..head = exactly the 2 PR files (control d7e95cd9f..head = 15). merge-base fb503741a 19f1e5475 = 81ee4b729.
3. TAMPERS on the WHOLE suite at head. 15 rows, denominator ASSERTED 57/555/pending 0 on every row, tsc rc 0 every row, 0 VOID, anchor 1 + marker landed, sha-restored, diff quiet, every red an AssertionError.
   - Seat/drafter rows, all 12 exact: T0 0 · RP-DEV 3 (R1 R2 R3) · RP-PREMERGE 10 ks1207 / 0 ks744 · EDIT1ONLY 2 (R2 R3) · EDIT2ONLY 1 (R1) · NOELSE 1 (R3 'enhanced') · TI 0 · G-UNDEFONLY 0 · G-VNEVER 1 · G-ENEVER 1 · G-STRIPUSER 3 (ks1041 x3, ks744 0) · G-VDELETEFIRST 0.
   - QA new directions: Q-DEFAULTNONE (absent -> 'none', the ticket's "or default it") 2 (R2 R3: the shape IS pinned) · Q-WRONGCLAIM (email guarded on userId) 1 (R1) · Q-DELETETOP (delete the client level before every branch) 0.
   - Properties NO cell sees: the falsy-claim drop; non-string coercion; illegal-header-character claims; the client level passing on non-verified optional paths; the email guard's dependence on the strip (seen by ks1041 only).
4. SUITES.
   - api-gateway: develop 56/550 · head 57/555 (ks744 5/5, ks1207 26/26) · merged 57/555.
   - Project tsc rc 0 on all three. packages/shared 44/851 at head (subtree dbd72dea0 identical on every tree).
   - Test-including program: head = develop = rc 2, 33 diagnostics / 69 output lines, 0 NEW lines, 0 in auth.ts or ks744. ks744 in the program per --listFilesOnly. The planted control adds +1.
   - The READY's "50 lines" does NOT reproduce (slip, Polish).
   - eslint auth.ts: 1 @typescript-eslint/no-unused-vars "'error' is defined but never used." at :415 head = :414 develop; the ks744 test 0. The firing control adds +1.
5. MERGED TREE 557aa4de8 over 75ad0e55c. api-gateway 0b77c0a24 and shared dbd72dea0 equal the head's. Develop did not move during the session. Items 1 and 4 were re-run on merged anyway (0 diffs, 57/555).
6. LINEAR / GITHUB, 21:40:13 and pre-mail 21:45:23, identical.
   - attachmentsForURL(pull/1028) = [KS-744, In Progress, contributes], no closes. Controls: pull/1023 -> KS-1207 contributes; pull/99999 -> 0.
   - 0 closing phrases in the title, the body (7,248 chars, 0 at-signs) and all 3 commits; planted controls [1,1,1,0,0,1].
   - The body names KS-1208 as residue.
   - KS-744 stays In Progress on merge (§5f, SKILL.md blob a5ab03435 at develop 75ad0e55c).
7. KS-1208 (recorded, NOT graded): NO_ROLE / NO_USERID -> 500 generic, 0 hits on every http-proxy mount, every mode, identical on all trees (fetch route and local GET 200). NOT this PR's.
8. CONSUMERS (READ, git grep -i at head, controls fire): 0 non-test readers of x-verification-level or x-user-email outside the gateway's own setters. Upstream shared middleware reads the level from the verified Bearer ('NONE' when absent). verification.ts:561 and enforcement.ts:151 already defaulted a missing claim to 'none' on develop (gateway-local routes never 500'd). No route newly reaches a local level decision.
9. RULINGS. Schemathesis / Akto are NOT REQUIRED for this delta. Measured reason: the changed property is claim shape x mount x credential x client header; neither tool can mint signed tokens with arbitrary claim shapes; the matrix already covers every mount kind through the real spec gates, with the full head-vs-develop difference classified (504 cells, 0 outside intended classes). The remaining risk (edge, real upstreams, real minted token) is the §5f live sweep's.

== Findings
- F-1 MINOR test coverage (PR, SHIPS-WITH, ticket the cells). No cell pins the falsy-claim drop this PR introduced (G-UNDEFONLY 0 of 555). Fix-shape: a ks744 cell with verificationLevel '' / null asserting the header absent.
- N-1 NEW, pre-existing, Minor severity / Low likelihood (TICKET candidate, fold into KS-1208's shape). A truthy claim that is not a legal header value (email with U+0142; level with U+0142 or CR-LF) -> 500 generic, 0 hits, every http-proxy mount, every mode, identical at develop. READ: auth's zod 3.22 .email() is ASCII-only; the level is copied off the row.
- N-2 NEW, pre-existing (TICKET candidate, owners). POST /api/documents/upload's gateway hand-forward branch (proxy.ts:551-620, the blocked-extension / MIME screen) is unreachable on the real app: 415 with a multipart body, 405 "Method POST not allowed for /api/documents/{id}." without. All tokens, all trees.
- N-3 pre-existing (TICKET candidate, owners). Client x-wallet-address is outside the strip and forwarded everywhere. referral/src/routes/referrals.ts:55 falls back to it when the JWT has no walletAddress, under a comment saying header reads are spoofable. The referral mount itself was not probed.
- R-1..R-5 Records (leak not reproduced; falsy dropped; non-string coerced; email guard relies on the strip, pinned by ks1041 only; client level on non-verified optional paths = #1023 R-5 / KS-736, unpinned, 0 readers).
- Curio C-1 (not widened): POST /api/users/admin/create with a revoked session answers 403 "Admin access required", not 401 SESSION_INVALIDATED, on all trees.

== CLOSED / STILL OPEN / NEW
- KS-744 missing-claim 500 on http-proxy routes: CLOSED at head and merged offline; STILL OPEN at runtime (§5f). KS-744 stays In Progress.
- KS-744 "leaks an internal error string": NOT REPRODUCED (R-1, Record).
- KS-1208: STILL OPEN, not this PR's.
- F-1: NEW, SHIPS-WITH. N-1, N-2, N-3: NEW (pre-existing), TICKET candidates -> escalation candidates for you.
- #1023 R-5 / KS-736 client level on non-verified optional paths: STILL OPEN, pre-existing, not widened.

== Prediction slips
- READY: "50 error lines" (measured 33 / 69); "internal header error" is its harness. Everything else holds.
- Ticket: the leak is not reproduced; "every proxied route" holds for http-proxy mounts only.
- Drafter: "email array -> joined" (measured: 2 raw lines). All 12 tamper rows, suites and merged tree exact.
- Brief: the suggested hand-forwarded POST /api/documents/upload is unreachable (N-2); POST /api/documents is http-proxy. The fetch routes were substituted.
- QA self-corrections (public, in the report): S-1 grader v1 counted pass-through headers as Blocker rows (90; corrected to identity/level + counterfactual 90/90); S-2 tamper qa_collected metric matched my workdir name (re-derived 0); S-3 tsc planted control v1 VOID (rootDir; re-run +1); S-4 consumer regex \s unsupported (re-run POSIX); S-5 upload probe v1 415 / v2 405 (v3 fetch routes); S-6 login_stub START count 2 = own shell / argv (filter v2: 0).

== MERGE ADDENDUM
"squash e39521cfb onto develop 75ad0e55c6335a5f34f6d0b74dfe00b334b2eb2e (19f1e5475 = the head's second parent; 75ad0e55c at draft close and at gate close) (merged tree 557aa4de89bcd53e01b3916d2a46986e36dd4e65; drafter b61ed1776 over 19f1e5475 = the head tree, 557aa4de8 over 75ad0e55c — both re-derived equal); #1028 attaches to KS-744 only, linkKind contributes, no closes — KS-744 stays In Progress on merge (§5f: the edge, the real upstreams and a real auth-minted claimless token are unmeasured); equality targets after the squash: auth.ts blob 6e1668362 / ks744 test 2ed41a338 (ks1207 test stays f56bd48b9); api-gateway 56/550 at 19f1e5475 -> 57/555 at head -> 57/555 merged (re-measured); packages/shared 44/851; dispositions: F-1 Minor test-coverage SHIPS-WITH (ticket a falsy-claim cell), N-1 TICKET candidate (fold into KS-1208's shape), N-2 TICKET candidate (owners), N-3 TICKET candidate (owners), R-1..R-5 Records SHIPS-WITH; NEW: F-1, N-1 (a truthy claim that is not a legal header value — U+0142 email / U+0142 or CR-LF level — 500s every http-proxy route, identical at develop), N-2 (POST /api/documents/upload's gateway screen is unreachable: 415 with a body, 405 without), N-3 (client x-wallet-address passes and referrals.ts:55 falls back to it); Records for KS-744's facts comment at merge: the real app answered develop's missing-claim 500 with the generic INTERNAL_ERROR 'An unexpected error occurred' (no internal string leaked in test, production or development mode), falsy claims ('' / null / 0 / false) are now dropped not forwarded, non-string claims still forwarded as coerced strings (pre-existing), the email guard relies on the edge strip (pinned by ks1041, not ks744), KS-1208 residue (role / userId) NOT this PR's, the 500 was specific to http-proxy mounts (hand-forwarded fetch and gateway-local routes were 200 on develop), a client x-verification-level still passes on non-verified optional paths (pre-existing, unpinned, 0 readers)"

== NOT TESTED (equal prominence)
- The edge (nginx / Caddy / ingress). Only the gateway's in-process strip was exercised.
- Real upstream services and their own authenticate(), incl. what they do with an absent header (READ: 0 readers). This is why KS-744 stays In Progress.
- A real auth-minted claimless token. Tokens were throwaway test-key JWTs; "NULL verification_level is schema-legal" is RELAYED.
- A real security / auth service / JWKS, a real Redis session store and limiter, a real Postgres (local GET bodies not compared).
- Preflight legs 3/4/8, the pre-push hook, demo, any docker stack, :6882/:7082, kintsugi, az, images, the mnemonic (KS-535 HOLD).
- Schemathesis, Akto, k6, Playwright: NOT COMMISSIONED, not run (ruled NOT REQUIRED).
- The test-token path (L4): READ only.
- Hand-forwarded routes built from req.user with an admin role (403 for role user), verification.ts:1007, the referral mount (N-3's consumer), POST /api/documents/:id/verify: READ only.
- Tamper rows on merged (subtrees identical by OID); shared on develop / merged (subtree identical).
- Seat A's exact tamper forms (no seat worktree entered).
- KS-1215, KS-736, #1023's findings (not re-derived).
- Concurrency and clock-driven expiry.

== Bounds
- Secuura checkout, READ-ONLY, three readings.
  - START 21:24:15: porcelain 0 · .git/config 09959c342094001c · refs 937 · worktrees 112 · develop 75ad0e55c · pull/1028 e39521cfb · branch feature/ks-597-b-caller-scoped-externalref.
  - MID 21:38:43: identical.
  - CLOSE 21:45:20: identical.
- refs/pull/1028/head never moved.
- LISTEN census: START 17 rows, MID 17, CLOSE 17. 0 node listeners at each. 0 node login_stub.mjs processes. 0 leftover node/vitest processes from my runs (21:45:39); every listener closed in the probe's finally/afterAll; nothing to SIGTERM.
- docker info rc 0 (printed once; no container created).
- No push, comment, file, tick, merge or deploy. Nothing to Peter or Stuart.

