## QA GATE - TIER 1, round 1: GO WITH NOTES
(Filed by the Wednesday seat from gate 37's returned text, 17:4x AEDT. Probes in `probes/` beside this file, on disk, gitignored.)

**Subject:** PR #1834 (Secuura/Distributed_Secuura), KS-1797 GET half only, author Seat T 8th (built by T 7th). GET /api/oauth/authorize answers 400 invalid_request, not 500, for a repeated state or code_challenge.
**Head:** `d261b3cfa9c7074ab436b1140ed9b74a5e50db59`, equal at 17:34:18 and 17:43:48 AEDT; develop a8c554659cb3 both reads; feature 7fed298b9 on 530f091120d5. merge-tree conflicts ONLY in the two Projects Documents html (section 124). Net diff vs 85cd24d = exactly the 4 files; 530f091..85cd24d touches nothing under services/auth.
**Gate:** 37, tier 1. Clone `repo/` (toplevel asserted, push URL no_push_qa_gate, clean at end). Nothing pushed/commented/merged; nothing under !CODING written.

### Verdict
Correct, safe, strict improvement. 51-shape hunt through the real router: 20 answered 500 at base; 18 of those answer the exact 400 envelope at head (repeated, [], [a], [50], [0]/[1], __proto__, [length], x30, empty-repeated, public app, XHR); the other 2 are latent wildcard cases (F2). 15 controls byte-identical base vs head (status, content-type, Location, CSP, body sha). This GET never redirects (0/51 Location; M5 produced 22, so the instrument sees them). 400 description constant, no raw values. Red-first R1/R2 500 at base, 6/6 at head. Whole auth at head 1332/1332 (one ks949 5008 ms load timeout re-run alone 31/31, KS-1053).

### Findings
- **F1 Minor — FOLLOW-UP (cheap; recommended before merge).** 6 of 10 mutants survive the author's 6 cells: M2a/M2b (`Array.isArray` guard: `state[a]=x` -> 500 again, qs gives an object), M6 (values JSON.stringified into the description = reflection leak), M9 (error.code -> INTERNAL_ERROR), M8 (empty `state=` refused), M3 (check after the resolver; safety-equivalent). Killed by the author's file: M1, M4, M5, M7. Cells to add: `state[a]=x` and `code_challenge[a]=x` with toEqual on the whole envelope; a repeated marker state with body not containing the marker; `state=` (empty) still 200. Evidence `probes/runs/mut-*-{author,assert}.log`.
- **F2 Minor — FOLLOW-UP (same class, not this PR's claim).** On an app registering '*', an array redirect_uri still answers 500 at head (H16 repeated, H17 `redirect_uri[]=https://evil.example/cb`): `includes('*')` lets it through, `new URL(array)` stringifies, escapeHtml throws in generateConsentPage ("s.replace is not a function"). Nothing unsafe emitted (no Location, no consent page, nothing minted). Latent: the code comment says 0 of 21 apps register a wildcard (not re-measured). Fix shape: add redirect_uri (or every resolver field) to the typeof guard, or one typeof loop over all seven query fields.
- **F3 Info (disclosed).** The early return masks the resolver's more specific refusal for a repeated state: unknown client, unregistered redirect, response_type=token, javascript: redirect on a wildcard app now read invalid_request (all JSON 400, no redirect; RFC 6749 4.1.2.1 respected). Docs state it.
- **F4 Info, PRE-EXISTING.** `client_id[]=client-1` passes the charset regex (String(array)) and reaches getAppByClientId as an array; consent page under mocks at base and head; real pg would give '{"client-1"}' -> no row -> invalid_client (inferred, no DB run).
- **F5 Info.** The "docs-only merge-in" d261b3c brings in develop's #1823/#1824 code (gdpr.ts + 3 tests); the net diff is still the 4 files — label only.

### NOT TESTED
POST half of KS-1797; a real DB (F4 inferred); the real logger and helmet/CSP; the api-gateway proxy's own query parsing; a browser, a running stack, Node 24, platform suites; tsc/eslint not re-run; the live wildcard-app count.

### Instrument faults
First ls-remote without the deploy key: "Repository not found" (re-run via the clone's core.sshCommand). Hook refused a variable-path merge-tree (re-issued literal). First whole-suite run from the WEDNESDAY cwd gave 4 false reds (cwd-dependent tests), re-run via `npm run test --prefix <auth>`. M3's red is a client-lookup assertion, recorded as safety-equivalent.
