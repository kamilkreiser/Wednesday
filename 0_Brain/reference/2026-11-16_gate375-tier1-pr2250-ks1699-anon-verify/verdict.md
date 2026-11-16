PR 2250: GO WITH NOTES (at head 9ec3e460b68dc3df7404ce5946df69f027807a86; tier 1)

Gate 375, tier 1, findings only. Opus 5.5. 2026-11-16 12:29-12:48 AEDT. Nothing was posted, pushed, merged or written to GitHub or Linear, and nothing was written under !CODING.
Clone: scratch/repo (`git clone --shared` of s-a20-base, origin = GitHub over https, refs fetched by gh credential). Worktrees: scratch/head (PR head) and scratch/dev (develop 72aeaec533dd). Deps: `npm ci` at Blockchain/Dev plus services/originate in my own tree; shared built in my tree. TMPDIR /private/tmp/g375t.

## Pins (gh api)
- First read 01:29:21Z: PR 2250 head 9ec3e460b68d (1 commit, 12 files, +734 -205, base develop 72aeaec533dd); PR 2249 head 10057c4f63c3; PR 2160 head b02bd2716cc2.
- Re-pin before the verdict, 01:47:24Z: PR 2250 is UNCHANGED at 9ec3e460b68d (open, not merged). Develop moved to **6f5ac0ec59ad** (one commit, KS-2125: a packages/shared role-list baseline, a test, and two fragments; 0 files shared with PR 2250, control 12 files). PR 2249 moved to **d04080d7a523**. PR 2160 is unchanged at b02bd2716cc2. PR 2225 is at 7d4a82f27063.

## Merge-tree (`git merge-tree --write-tree`, my clone)
- Against develop 6f5ac0ec59ad: clean in both orders (identical tree d630ad8d141e).
- Against PR 2249 at d04080d7a523 (its current head): clean in both orders (c31a543df990). Also clean at its earlier head 10057c4f63c3. The file sets are disjoint.
- Against PR 2160 at b02bd2716cc2: clean in both orders (8570ec05f0f2).
- Planted controls, each fired in both orders:
  - (A) a develop-side edit of the JSDoc line PR 2250 rewrites conflicts in certifications.ts.
  - (B) a 2250-side edit of the exact line PR 2160's hunk replaces (`const msg = ...`) conflicts with 2160.
  - (C) a 2250-side edit on PR 2249's first verification.ts hunk conflicts with 2249.

## Q1. What an anonymous caller gets back, read from the write side
Handler at head: certifications.ts `verifyCertificationHandler`. Row: `getCertification` runs `SELECT * FROM documents WHERE id AND tenant_id`, and `fromDbRow` maps it.

| field | source (write side) | holds | personal? |
|---|---|---|---|
| verified | computed: status=='issued' && !expired && hashValid | boolean | no |
| certificationId | documents.id (uuidv4 at issue) | random UUID | no |
| status | documents.status mapped | enum | no |
| checks.* | computed from status, expires_at, content_hash vs hash of certification_metadata.certificationData, and blockchain presence | booleans | no |
| issuer.id | documents.issuer_user_id, else certification_metadata.issuerId (issue writes `req.user.userId`) | **the certifying user's id** | **yes: null for anonymous** (measured: V-A10 green; my mutant g2 reds it) |
| issuer.did | certification_metadata.issuerDid | the certifier's DID | **yes: null for anonymous** (V-A10; my mutant g3 reds it) |
| issuer.verified | constant `true` | constant | no |
| blockchain | certification_metadata.blockchain, else metadata.blockchain. Issue writes {anchorId, txHash, blockHeight, anchoredAt, confidence, anchoringStatus, status}. Document paths can add threadToken {policyId, scriptAddress, mintTxHash, network}, error (an anchoring error message), failedAt, createAttempts, retryClaim, retryClaimedAt, retryPostUnknownToken (crypto.randomUUID) | chain and anchor metadata; no email, user id or owner id written into it (read across every writer in originate) | no (see F4) |
| verifiedAt | new Date() | timestamp | no |
| chargeEventId | null when there is no req.user | null | no |

- The 404 body is `{verified:false, error}` and the 400 body is the express-validator errors. No email, no local part of an email, no user id, owner id, DID or IP reaches an anonymous answer. **Nothing for Kam on personal data.**
- issuer.name (the email local part) is not in this route's answer for anyone.
- Signed-in answers are unchanged. V-C7 (issuer exactly as on develop) and V-C1 (whole charge argument list) are green at head. Whole originate suite: 2741/2741.

## Q2. Charges
- Anonymous: the `principal ? createChargeEvent(...) : null` branch means no call is made. Measured by V-A3 and V-A9 x2 green, and by my mutants:
  - g1 (always charge): red V-A3 and V-A9 x2.
  - g4 (charge an anonymous call to `certification.issuer.id`, i.e. the owner): red on the same 3 cells.
- Signed-in: exactly one call with the same five arguments as on develop (V-C1). V-A6 (a token with no userId) is still charged.
- Charging someone else: an anonymous call never reaches createChargeEvent. A signed-in call charges the caller's own tenant (`getReqTenantId`), and lookup is in that same tenant, so another company's certification answers 404 with no charge (V-C2, V-D1).
- A lowercase `bearer <valid JWT>` is anonymous at both the gateway and originate (`startsWith('Bearer ')`), so it is not charged and is counted by the limiter.
- **No anonymous charge and no charge leak.**

## Q3. The limiter (`skip: req.user`)
Measured on the real app with the cap at 3 (my probe, scratch/tools/zz-gate375-probe.ran.ts; log runs/probe_log.txt). After 3 anonymous calls, each of these was 429 with 0 forwarded, so each is counted as anonymous:
- an expired JWT
- a 3-segment junk JWT
- an HS256 JWT
- an sk_ key that fails validation
- `Bearer ` with an empty token
- a Basic auth header
- W33's cells, green: lowercase bearer, junk Bearer, junk key

Not counted:
- a signed-in caller: G-A4, 5/5 forwarded
- a valid sk_ key: G-A4c, 5/5 forwarded

My mutants:
- g5 (count a valid sk_ key): red G-A4c and the placement pin.
- g6 (skip on any Authorization header): red G-A4b x2 and the placement pin.
- g7 (never skip): red G-A4, G-A4c and the placement pin.
- A no-op control stayed green (109/0).
- Every product file was restored by content; the sha256 values are equal.

429 answer: status 429, body `{"success":false,"error":{"code":"RATE_LIMIT_EXCEEDED","message":"Too many certification verify requests, slow down."}}`, with standard RateLimit headers (limit 3).

Audit rows:
- One audit INSERT per 429 (G-A9 green).
- The audit middleware logs every POST (audit.ts: only GETs are skipped), so a forwarded anonymous POST also writes one row. A 429 therefore adds no amplification: rows stay at most one per POST, bounded by the global 300/min/IP, the same as any POST route.

IP keying (`trust proxy` 1, index.ts:113):
- Behind nginx (`$proxy_add_x_forwarded_for`, real_ip on the demo conf), a spoofed leftmost XFF with a constant rightmost hop shares one bucket: 3x200 then 429 (measured).
- A client that reaches the gateway directly and picks the RIGHTMOST XFF gets a fresh bucket each time: 5/5 forwarded (measured; see F3).

## Q4. Nothing else opened
At the gateway, anonymous callers got 401 and 0 forwarded on:
- GET /:id, GET /, POST /issue
- GET /:id/evidence-bundle, GET /:id/lineage
- POST /:id/share, /:id/revoke, /:id/recertify
- PUT, DELETE, PATCH and GET on /:id/verify
- POST /:id/verify/x, POST /:id/verify%2Fx, `/:id/VERIFY;x`
- v1 and upper-case share
- `verify/../share`, `x/../<id>/share`

Other measured answers:
- POST /api/certifications and POST /api/certifications/verify answer 405.
- `/<id>%2Fshare/verify` and `/verify?x=/share` are forwarded as verify. That is still the verify route at originate; `%2F` is not a separator.

At originate (head certifications.ts):
- The only registration above `certificationsRouter.use(authenticate())` (line 78) is POST `/:id/verify` (line 68).
- issue, list, get, revoke, share, recertify, lineage and evidence-bundle all sit below it.
- The V-C3 cells (8) are green.

m-V4: the share handler does not itself refuse an anonymous caller; only the blanket guard does. The blanket is intact at head, so **share is NOT reachable anonymously** (originate V-C3, gateway G-A3 and my probe).

## Q5. Tests
**Red first.** My run puts develop's bytes of the 4 product files into the head tree:
- originate ks1699v: **9 of 25** red, all AssertionError (V-A1, V-A2, V-A3, V-A5, V-D1, V-A8, V-A9 x2, V-A10). This matches the READY.
- gateway: **16 of 37** in the READY's three files (ks1699v 15 of 20, ks1628 G-C2 1, ks815 0), all AssertionError. This matches.
- ks570 also reds one cell ("public allowlist has no stale entries") on develop bytes, because it is the forced PUBLIC_BY_DESIGN entry. That is 17 of 55 across four files, all expected.

**Mutants.** I did not rerun W33's 17. My own 7 mutants plus the control:

| mutant | red |
|---|---|
| anonymous charged | 3 |
| anonymous charged to the owner | 3 |
| issuer.id leaking only to a no-header anonymous caller | 1 (V-A10) |
| issuer.did leaking to anonymous | 1 (V-A10) |
| limiter counting a valid sk_ key | 2 |
| header-text skip | 3 |
| never skip | 3 |
| no-op control | 0 |

**Whole suites,** one at a time, load1 at or below 8 at each start (runs/suites.log):

| suite | develop 72aeaec533dd | head |
|---|---|---|
| gateway | 173 files / 1962, 0 failed | 174 / 1979, 0 failed |
| originate | 227 suites / 2716, 0 failed | 228 / 2741, 0 failed |

Both equal the READY.

**Static checks:**
- tsc on both services' tsconfig: 0 errors. A planted TS error is reported (rc 2, 1 error).
- `check:test-types`: rc 0. api-gateway: 174 test files examined, 25 errors, all baseline, 0 new.
- eslint, run from Blockchain/Dev on the 9 changed .ts files: 0 errors. Warnings: index.ts 2 and proxy.ts 4, identical on develop. A planted `var` plus an unused expression gives 2 errors.
- docs-fragments check: OK. A planted unclosed `<div>` gives "FAIL — 1 finding(s)". After restore: OK.

## Q6. PR body
Correct as written:
- The rulings are stated as facts (09:16:45 b, 09:59:15 a, 11:12:46 a).
- The OVL_IGNORE_PRS line is present (2225 2160 on the STAMP 10:49, W33-R4).
- The NOT-run list is honest:
  - Schemathesis, Akto, Playwright and k6 are listed as NOT run.
  - Preflight legs 3, 4 and 8 are SKIPPED with the reason (no local stack).
  - The hook's final line is quoted.
- No self-hold sentence (the only "hold" hit is "the pin holds ten lines").
- No closing keyword: 0 hits in the body, title or commit message; a planted "Closes KS-1699" counts 1.

Gaps are in F6. On the skipped preflight legs: legs 3 (spec-auth conformance) and 4 (path resolvability) are exactly what would exercise a NEW public route on a live stack. Neither ran, so the "live stack answers anonymous" claim stays UNMEASURED: production and the demo stack were never hit.

## Findings (none blocking; none for Kam)
- **F1 LOW (defence in depth, new reach):** the gateway's `/originate/` passthrough (proxy.ts ~1282, no auth, no scope) reaches the route this PR opens at originate, and does NOT pass the anonymous limiter. Measured: with the cap at 3, 6 of 6 anonymous POSTs to `/originate/api/certifications/<id>/verify` were forwarded.
  - At the edge, nginx closes `/originate/` with a 404 in all three confs (KS-1041), and api-gateway publishes no port. So this is reachable only from the compose network or a direct gateway hit.
  - Candidate filing: retire or guard the gateway's `/originate/` mount (the KS-1041 second step).
- **F2 LOW:** a VALID sk_ key whose connector-token exchange fails gets req.user at the gateway, so the limiter does not count it. It is forwarded with no Authorization, and originate answers it as anonymous: 200, no charge, issuer null. Measured: 3/3 forwarded, Authorization null.
  - On develop the same call got a 401.
  - It is not a charge leak, and it is still under the global limit and the per-key limit.
- **F3 LOW (inherited):** the limiter keys on req.ip with `trust proxy` 1. It is correct behind nginx, which appends the hop. A client that reaches the gateway directly can choose its bucket with the rightmost XFF. This is measured, and the same holds for every gateway limiter.
- **F4 LOW (reading):** the answer returns the raw `blockchain` blob, not `composeHonestBlockchainBlob`. It can carry an anchoring error message, a placeholder or simulated txHash, and the re-anchor claim UUIDs.
  - Signed-in callers already see it. It is now world-readable, but it holds no personal data.
  - Also by reading: `getCertification` does not filter on document_type, so any default-tenant `documents` UUID verifies. That is an existence and status oracle for unguessable UUIDs.
- **F5 LOW (reading, not run):** a non-UUID id makes the `::uuid` cast throw, which gives a 500 INTERNAL_ERROR plus a logger.error. Anonymous callers can now trigger it, bounded by the limiter. Signed-in callers could already.
- **F6 NOTE (PR body and docs):**
  - "tier 1" is not named in the body (0 hits, case-insensitive), although the commission asks for it.
  - The door table's header names develop `553c0f8ab334`, which is stale; the base is 72aeaec533dd.
  - The flow fragment says "11 of 32 fail on develop's product bytes", where 16 of 37 is measured and the PR body says 16 of 37.
  - A one-line body edit and a fragment edit fix all three; none is a code change.

## Needs Kam
None. No personal value reaches an anonymous answer (issuer.id and issuer.did are null, and the other fields carry no person-derived value), and no charge goes against his 09:59 ruling.
