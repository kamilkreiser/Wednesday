SUBJECT: [QA -> Wednesday] TIER 1 GATE #1014 (KS-1176) 616c766a5 — GO WITH FINDINGS
FROM: CoAgent <coagent@agentmail.to>
TIMESTAMP: 2026-09-16T21:07:25.000Z
AUTH: {"spf": "pass", "dkim": "pass", "dmarc": "pass"}

QA -> Wednesday — TIER 1 ROUND 1 gate, Secuura/Blockchain PR #1014 (KS-1176) @ 616c766a57a51238450c99bbf1d59bb109e3841c
Composed 2026-09-17 07:07:24 AEST (clock from `date`).
Report: /Volumes/DevMASTER/!CODING/Testing Agent MAIN/projects/secuura/reports/2026-09-17-ks1176-1014-616c766a5-tier1-r1/report.md
(NOT-TESTED.written-first.md written 06:37, before any run. evidence/ holds the harness, rows, oracle, tampers and reads.)

## BLUF
VERDICT: GO WITH FINDINGS on `616c766a5` as the delta over base `e0f41a8fa`, AND on the merged tree `8589933267963afda8fc352279c4b694ed5bb3de` (head merged with develop `523f283c6cd2550263ec9869dc5ee722be40df4e`; develop unchanged 06:37:35 -> 07:04:52 AEST).

- **Level axis: CLEAN.**
  - 0 admissions above `none`, 0 known-level changes, 0 changes at `:557`.
  - Measured over 2,345 create + 1,085 verify HTTP rows per tree.
  - Everything real except the upstreams: the REAL `index.ts` app, REAL `authenticateToken`, router and enforcement, the REAL `redis.ts` in-memory fallback, and a catalogue seeded through the REAL admin seed route.
  - The oracle is written from the ruling's words. Its planted controls fire, and under the TW tamper it flags 297 violations.
- **Two Major findings, both TICKET-class, both escalation candidates.** Neither is on the axis the ruling named.
  - F-1: a connector's `allowedDocumentTypes` allow-list is bypassed by sending `type` instead of `documentType`. #1014 extends the bypass to SSD_DOCUMENT, DOCUMENT and PROPERTY_DEED.
  - F-2: the per-key rate limiter never fires in the real app.
- **Your call:** should F-1 ship with #1014? The fix is one line, outside the PR's files.

## Plain statements (items 1-13)

**(1) Principal x type rows that changed**
- base -> head: 661 create rows differ.
  - All 661 are an unrecognised-string claim x a creator level that ranks `none`, where base answered 403 `INSUFFICIENT_VERIFICATION_LEVEL`.
  - Head answers: 507 -> 201 forwarded; 31 -> 201 workflow-gated; 33 -> 403 `MFA_REQUIRED`; 57 -> 403 `AUTH_PROVIDER_NOT_ALLOWED`; the rest -> 400 `MISSING_METADATA`.
- VIOLATION 0. Admissions above none 0. Known-level changes 0. head vs merged 0.
- 35 principals:
  - anonymous;
  - sk_ keys: write, noscope, readonly, restricted, bypass, wildcard, invalid;
  - a non-sk `x-api-key`;
  - connector JWT as Bearer, scoped and scope-less;
  - RS256 humans NONE..GOVERNMENT, plus no level claim, a number, an array, and `api_key`;
  - 14 test-token spellings, including fullwidth, Turkish and ZWSP;
  - a spoofed `x-verification-level` header.
- Types: 31 catalogue types, untyped, unregistered, and lowercase, each under both `documentType` and `type` body keys.
- Oracle planted controls, all as required: known-level change flagged; unknown user passing `basic` flagged; unknown user passing `standard` flagged; the legitimate diff not flagged.
- Unknown-level producers by source: sk_ keys, intra-cluster connector JWTs, and dev/test test tokens.
  - No production human carries one: `mapDbVerificationLevel` maps unknowns to BASIC.
  - `auth.ts:146` 'BASIC' is the test-token default.

**(2) Known-level parity**
- 52 user values x 33 required values = 1,716 pure-function rows per tree.
- 90 flips, all an unknown-string user x {'', null, undefined, none, NONE, None}, false -> true.
- 0 known-user flips. Independent-oracle mismatch 0 on base, head and merged.
- Non-string users throw TypeError identically on every tree (117 rows each).

**(3) `:557` unchanged**
- 0 of 1,085 verify rows differ: base -> head, base -> merged, head -> merged.
- An off-canonical verifier level (`standrd`, `' none'`) passes all 30 string-level authenticated principals at base and at head.
- KS-1190's description DOES name `routes/verification.ts:554-557` ("the same -1 semantics"). The brief's "not named" prediction slips.

**(4) Anonymous vs connector, and the related measurements**
- Anonymous: 401 on 67/67 create and 31/31 verify rows at every tree.
  - So the ruling's "nothing beyond anonymous" premise is vacuous at the only callers. That is a premise slip.
  - The product why-comment repeats it: Polish.
- Lowest human (jwt_NONE) vs sk_write at head: 2 of 67 create rows differ (a synthetic type whose provider list names `api_key`); 0 of 31 verify rows. At base, 40 differed.
- Rate limits: see F-2.
- Tenant: a spoofed inbound `x-tenant-id` / slug was never forwarded, for any principal.
  - The real app chain strips it (mechanism not traced).
  - A router-only harness would not see this.
- What the created document records:
  - The originate hop carries no `x-verification-level` (1,523 forwards).
  - sk_ forwards carry the minted connector JWT; humans carry their own bearer.
  - READ ONLY: originate records connector provenance by role (an action_provenance row, NULL actor UUIDs). Neither principal kind gets a level or trust marker.
- Connector JWT as Bearer (L11, F-5):
  - A scope-less connector JWT answers exactly like jwt_NONE on 67/67 create and 31/31 verify rows at head.
  - 0 of 9 minted JWTs appeared in any client response (stub upstreams). The mint is `/internal`, outside `/api`. I found no client path.
  - READ ONLY: originate re-checks `documents:write` for role connector (`rbac.ts:47-64`, `documents.ts:359`).
  - Graded Minor TICKET, below the drafter's Major candidate.
- Bypass row: a `workflowPolicy: bypass` connector is forwarded on an approval-requiring none type where jwt_NONE is workflow-gated. Configured policy made reachable: RECORD.
- Connector keys now create all three seeded none types. PROPERTY_DEED at `none` is a product question.

**(5) KS-1190 unchanged**
- The diff touches only the user-rank line.
- QA_TYPO / QA_NONE_SPACE create counts and QA_V_* verify counts are identical base vs merged.
- The TR tamper reds exactly the C pin.
- Catalogue fill (READ + probe):
  - Redis `doctype:*` is written only by `admin.ts:633` seed, `:691` POST, `:706` PUT and `:732` PATCH.
  - The seed runs only on GET `/api/admin/document-types` with an empty catalogue AND (`ENABLE_DEMO_SEED`, or NODE_ENV not production/staging). So it is OFF in prod by default.
  - Admin POST stores levels verbatim: 'standrd' is accepted with 201, after which every authenticated principal can create that type.
  - Catalogue keys are written with setex (they carry a TTL).
  - `document_type_configs` (Postgres, `platform.ts:880-894`) has no reader on the enforcement path and no bridge into Redis. Two catalogue sources: RECORD.

**(6) Level-order copies**
- 0 production callers (grep with positive control) for:
  - auth `requireVerificationLevel`;
  - shared `requireVerificationLevel` / `requirePolicy` / `evaluatePolicies`.
- Frontend `DocumentUpload.tsx:74-80`: only human `useAuth` sessions reach it; no unknown level does.
- The READY's "13 test files mock `meetsVerificationLevel: () => true`": confirmed 13 by a comment-stripping tokenizer (15 files mention it).
- Real-browser half of tier 1: NOT APPLICABLE.

**(7) Tampers**
Setup, identical on every row: head tree, whole api-gateway suite, tsc rc 0, 49 files / 423 cells, pending 0, restore sha256 == HEAD blob, `git diff --quiet` clean. No VOID rows.

| Row | What it changes | Reds | Predictor |
|---|---|---|---|
| T0 | nothing | 0 | = READY |
| TA | fix reverted | 3 | = READY |
| TW | unknown satisfies everything | 4 | = READY |
| TK | `>` for `>=` | 8 | = READY |
| TR | unknown required fails closed | 1 | = READY |
| TI | inert comment | 0 | = READY |
| G-KNOWN | none/basic rank as standard | 3 | gate's own |
| G-ROUTE | enforcement call skipped | 5 | = drafter |
| G-CTRL | `registered.length > 999999` | 2 | = drafter |
| G-E555 | `:555` skip removed | 0 | = drafter |

- G-KNOWN's 3 reds: enforcement.test x2 and ks1176 B parity. The D/E human cells cannot see it.
- G-E555: the E "verifier-none 200" control cannot see the skip being removed. It proves only its 200.
- HTTP census under TA = base (0 diffs). Under TW: 297 VIOLATION and 171 verify diffs.
- Red before green: the ks1176 file in MY base tree `e0f41a8fa` runs 13 / 3 red.
- TK's "33 rows" is derived: 28 + 5 equal-rank pairs in the 15x15.

**(8) Including tsc** (`include src/**/*`)

| Tree | Files | Error lines | Files with errors |
|---|---|---|---|
| base | 584 | 30 | 10 |
| head | 585 (both PR files in the program) | 30 | 10 |
| merged | 588 | 30 | 10 |

- 0 errors in the PR files. NEW 0 / GONE 0.
- Planted TS2322 in head's ks1176 test: +1 at the plant; restored sha-identical.
- eslint: 0 on both files, base and head. Firing control: 3 messages (no-var, no-debugger, no-unused-vars).

**(9) Merged tree and suites**
- Merged tree `8589933267963afda8fc352279c4b694ed5bb3de` = `merge-tree --write-tree` in my clone = the drafter's.
- api-gateway suites, all pass, pending 0, project tsc rc 0:

| Tree | Files / cells |
|---|---|
| base | 48/410 |
| head | 49/423 |
| dev `523f283c6` | 51/419 (the drafter's prediction holds) |
| merged | 52/432 |

- shared and auth suites were not re-run.

**(10) Linear** (re-read 07:04:50, immediately before this mail)
- `attachmentsForURL(pull/1014)` = exactly KS-1176, linkKind `contributes`, status open.
- KS-1190 and KS-1187: 0 attachments each.
- Control: pull/1011 -> KS-871 `contributes`, merged.
- 0 closing phrases in the title, body, commit message and the 1 comment. Regex controls: 3 hit, 3 miss.
- KS-1187 not named. 0 at-mentions.
- KS-1176 MUST stay In Progress on merge (§5f).

**(11) Schemathesis / Akto: NOT APPLICABLE** (measured from the spec, blob `122d3a2f8`)
- POST `/api/documents` already declares 403 naming `INSUFFICIENT_VERIFICATION_LEVEL`, `MFA_REQUIRED` and `AUTH_PROVIDER_NOT_ALLOWED`.
- #1014 adds no status, field or operation.
- The changed behaviour needs an sk_ credential the operation's security does not declare: bearerAuth only, although `connectorApiKey` exists in components (RECORD).
- Not run (NOT COMMISSIONED).

**(12) NOT TESTED:** see the block below.

**(13) Disjointness and develop**
- 20 other open PRs (the drafter saw 18; #1015 and #1016 are new). Exact shared files: 0.
- #1016 (KS-1072) edits `routes/verification.ts` +7 -2, in `makeFetchDocFromAnchorStore` only (hunk @@-298).
  - Its patch has 0 mentions of `meetsVerificationLevel`, `verifierLevel` or `enforceDocumentTypeRules`.
  - If it lands first, develop moves on the GUARDED gateway-src prefix (launcher exit 18). Judge it by content.
- Develop did not move.
- Checkout readings at 06:37:35, 06:57:37 and 07:00:11 (plus 07:04:52):
  - porcelain 0; config sha `d7e7298b02c45f52…`; worktrees 110/111; branch `feature/ks-597-b-caller-scoped-externalref` @ `355d82c8b`.
  - refs 904 -> 905. Not this gate: no write verb ran in the checkout.
  - `.vite` results.json 5,907 b @ 01:02:02, unchanged. Entries newer than my setup: 0 (control: 9 of any age).
- `docker info` rc: 0. UP is not permission; no container was created or touched.

## FINDINGS

**F-1 — MAJOR — TICKET + ESCALATION CANDIDATE** (MEASURED AT RUNTIME; oracle: Product consistency / Purpose)
- Defect: `verification.ts:1215-1219` (the test at `:1216`) checks `body.documentType` only.
  - Enforcement resolves `documentType || type` (`enforcement.ts:100`).
  - Originate stores `documentType || type` (`documents.ts:565`, READ).
- Repro: a connector with `allowedDocumentTypes: [DOCUMENT]` sends `{"type": "SSD_DOCUMENT"}`.
  - base: 403 `INSUFFICIENT_VERIFICATION_LEVEL`.
  - head / merged: 201, forwarded.
  - The same holds for every none-rank type sent via `type`. Sent via `documentType`: 403 `FORBIDDEN` on both trees.
- Pre-existing at base for untyped bodies and off-canonical types (QA_TYPO via `type` is 201 at base).
- Not a level escalation.
- Fix-shape (owner's): check `documentType || type`.

**F-2 — MAJOR — TICKET, escalation candidate** (MEASURED; oracle: History, the KS-164 acceptance)
- Defect: `enforceClientRateLimit` is `app.use`d at `index.ts:524`, before any route-level `authenticateToken`. At that point `req.user` is unset, so the limiter never applies.
- Repro: a `rateLimit 2/60s` key on the real app.
  - head: 5/5 answered 201. base: 5/5 answered 403.
  - Never 429; no `X-RateLimit-Limit` header.
- Control: the same limiter mounted after the same `authenticateToken` on a bare app answers 200, 200, 429, 429, 429.
- Class-wide by READ: no global auth before `:887`; proxy routes mount auth at `:1095+`.
- base = head. #1014's new connector surface is governed only by the per-IP global limiter.

**F-3 — MINOR — TICKET** (MEASURED, replicated 4x)
- Admin POST `/api/admin/document-types` uses id `dt-${Date.now()}` (`admin.ts:682`).
- Two creates in the same millisecond both answer 201; the second silently overwrites the first.

**F-4 — MINOR — TICKET** (MEASURED, base = head)
- A non-string `verificationLevel` claim:
  - create: 500;
  - POST `/api/documents/:id/verify` on a verifier-gated type: never answers (the async handler throws).
- Needs an auth-signed token: not client-forgeable (READ).

**F-5 — MINOR — TICKET**
- A connector JWT presented as Bearer skips the gateway's connector gates. Details under (4).

**RECORDS**
- The bypass row.
- PROPERTY_DEED at `none`.
- Premise and why-comment are vacuous (Polish; optional SHIPS-WITH).
- KS-1190 names `:554-557`.
- Tenant spoof is stripped by the app chain.
- No level marker on the forward.
- `x-api-key` is not declared on the spec operation.
- Two catalogue sources; the seed is off in prod.
- #1016 touches `verification.ts`.

## PREDICTION SLIPS
- Brief / drafter: "KS-1190 does not name `:557`" is WRONG. It names `:554-557`.
- Wednesday's ruling: the premise "nothing beyond anonymous" is vacuous; anonymous is refused with 401 first.
- Drafter: L11 "Major candidate" -> Minor, because originate re-checks scope. This is a grading change on a new READ.
- Drafter: "15 mock files". The READY's 13 is correct.
- Drafter: L3 "201". I measured 400 `MISSING_METADATA` because my request body carried no required metadata.
  - The level clause passes, so this is an instrument limit, not a slip.
- Held: every READY tamper/suite/tsc count, and every drafter tamper/suite/tsc/merged-OID/dev prediction.
- Not predicted by anyone: F-1, F-2, F-3, and the verify hang.

## MERGE ADDENDUM
squash 616c766a5 onto develop 523f283c6cd2550263ec9869dc5ee722be40df4e (merged tree 8589933267963afda8fc352279c4b694ed5bb3de; file-disjoint from #1011's squash and from all 20 other open PRs — #1016 edits verification.ts makeFetchDocFromAnchorStore only, judge by content if it lands first); #1014 attaches to KS-1176 only, linkKind contributes (read 07:04:50 AEST) — KS-1176 stays In Progress on merge (§5f: runtime behaviour — connector keys now create none-rank document types; the live Platform-S sweep is owed); equality targets enforcement.ts blob 3e314ba11 / ks1176-connector-key-level-ranks-as-none.test.ts blob 5820520ae; api-gateway 48/410 at e0f41a8fa -> 49/423 at head, 51/419 at develop 523f283c6 -> 52/432 merged (re-measured 06:39-06:40 AEST); Records: F-1 Major TICKET + escalation (verification.ts:1216 allow-list reads documentType only — `type` bypasses it, now for SSD_DOCUMENT/PROPERTY_DEED), F-2 Major TICKET (per-key limiter inert, index.ts:524 before route auth), F-3 Minor TICKET (admin doc-type id collision), F-4 Minor TICKET (non-string level: verify hang / create 500), F-5 Minor TICKET (connector JWT as Bearer skips gateway connector gates; originate re-checks scope), bypass row, PROPERTY_DEED at none, premise/why-comment vacuous (Polish), KS-1190 names :554-557, tenant spoof stripped, no level marker on the forward, spec x-api-key undeclared on the operation, two catalogue sources / seed off in prod.

## NOT TESTED (same prominence as the findings)
1. The live Platform-S upload under a connector key against a seeded Platform K, plus POST `/api/verification/verify` (the §5f sweep, Sunday). KS-1176 stays In Progress.
2. Real Redis catalogue population: what production Redis actually holds, and real TTL expiry.
3. The gateway behind nginx / Container Apps / edge.
4. Originate persistence (READ ONLY). This includes the `documents:write` re-check that downgrades F-5, and F-1 end to end.
5. The real security `/api/keys/validate` and the real `/internal/connector-token` mint. Both stubbed; claims copied from source.
6. Whether a connector JWT is client-obtainable in any deployment. Only stub-upstream responses were scanned.
7. Schemathesis / Akto / Playwright / k6: NOT COMMISSIONED.
8. Preflight legs 3/4/8.
9. The frontend copy (READ only; no browser).
10. KS-1190's two measurements.
11. `docker info`: rc 0 recorded, nothing else.

Added during the run:
- F-2's class-wide claim on proxy routes (READ only).
- L3 returning 201 with metadata supplied.
- The shared 44/851 and auth 61/745 baselines.
- A multi-replica limiter.
- The real NODE_ENV / ENABLE_TEST_TOKENS values in any deployment.
- The tenant-strip mechanism.

— QA agent (findings-only: nothing fixed, merged, pushed, commented or filed)
