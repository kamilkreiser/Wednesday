# QA gate: Secuura Platform K PR #1491 (KS-811 second ask)

Head: f8abbdc747e4831643cb07541c36e2ef1b0da53c (branch feature/ks-811-post-documents-403-code-set-agrees)
Base: merge-base dd015e7358185feb2192719aa718161015846622; real origin/develop at gate time = 17e275adaf672dd5d642e0bfbe28da44ad599d2a (one commit ahead of the merge-base, KS-695 erase-connector; not touched by the PR).

## VERDICT: GO WITH NOTE

The claims hold: one commit, one new test file, no product file touched, the author's emitted set (FORBIDDEN + four enforcement codes) and published set match what I derived independently from source and spec, and the guard catches every mutation of the kinds it says it catches; the notes are blind spots the file already discloses, plus two small precision gaps.

## By my runs

1. `git clone --no-hardlinks` of the project repo into the scratchpad; origin set to Secuura/Distributed_Secuura with the project's core.sshCommand (key path not printed); `git fetch origin develop` ok (40ed3573b..17e275ada). Bundle: plain `git bundle verify` in the project repo reports the missing prerequisite dd015e73; in my clone the prerequisite exists (`cat-file -t` = commit, ancestor of origin/develop). `git fetch <bundle> feature/...:pr1491` ok; `rev-parse pr1491` = f8abbdc747e4831643cb07541c36e2ef1b0da53c. Bundle's only head = that sha.
2. Scope: `git log origin/develop..pr1491` = 1 commit (f8abbdc74). `git diff --name-status origin/develop...pr1491` = exactly one line, `A Blockchain/Dev/services/api-gateway/src/__tests__/ks811-post-documents-403-code-set-agrees.test.ts` (210 insertions, 0 deletions). No product file. (The two-dot diff shows develop's KS-695 files as deletions; that is develop being ahead, not the PR.) I merged origin/develop into my scratch clone to test against the current base.
3. Independent derivation (read verification.ts 1140-1397, enforcement.ts, originate documents.ts POST / 363-982, provenance.ts, originate.openapi.ts, shared responses.ts), before reading any result of the test:
   - Emitted 403: gateway handler = FORBIDDEN x4 (verification.ts 1222, 1272, 1282, 1296); enforcement.ts = DOC_TYPE_DISABLED (141), INSUFFICIENT_VERIFICATION_LEVEL (155), MFA_REQUIRED (163), AUTH_PROVIDER_NOT_ALLOWED (173), forwarded by `res.status(fail.status)...code: fail.code`; originate handler = FORBIDDEN (documents.ts 379 role/scope, 532 organizationUuid) plus resolveOnBehalfOf -> OnBehalfOfError(403,'FORBIDDEN') (provenance.ts 132). Set = {FORBIDDEN, AUTH_PROVIDER_NOT_ALLOWED, DOC_TYPE_DISABLED, INSUFFICIENT_VERIFICATION_LEVEL, MFA_REQUIRED}. Matches the author.
   - Published: the POST /api/documents 403 text (openapi.ts, after line ~958) names the same four enforcement codes in prose and says the list is "NOT exhaustive"; ErrorResponse code vocabulary in packages/shared responses.ts line 52-55 lists FORBIDDEN. Matches the author; the author's correction (sets DO agree once the shared schema is counted) is right.
4. `npm ci --ignore-scripts` in Blockchain/Dev: exit 0, 1937 packages. `tsc` in packages/shared (needed first): exit 0.
5. New file alone (`vitest run --root services/api-gateway <file>`): 1 file, 12/12 passed.
6. Whole api-gateway suite on the merged tree (PR + current develop): 111 files, 1053 tests, all passed, exit 0. (Author's 110/1047 was on the older base; the +1 file/+6 tests is not this PR's: PR adds 12 tests, develop's KS-695 adds the rest of the delta; I did not split it further.) Ran once, not twice.
7. `tsc --noEmit -p services/api-gateway`: exit 0, no output.
8. `npm run lint` (eslint src) in api-gateway: exit 0, 0 errors, 36 pre-existing warnings, none naming ks811 (positive control: the lint did run and report other files). A direct eslint call on the one file reports "ignored, outside base path", so the package script is the valid check.
9. `npm run check:test-types`: exit 0 (42 in baseline, 0 new) but it is wired to services/auth only; it does not examine this api-gateway file. `npm run check:openapi`: exit 0 (generator --check then spec-examples "413 example blocks OK").
10. Mutations (script in scratchpad, full output in `mutations.txt`; each restored from backup and a no-mutation control run first = 12/12 green):
    - A1 rename MFA_REQUIRED in enforcement.ts: RED (3 cells, including the agreement cell).
    - A2 new originate 403 code (organizationUuid refusal -> ORG_MISMATCH): RED (3 cells).
    - A3 drop `DOC_TYPE_DISABLED` from published text: RED (3 cells).
    - M3 keep the word but move MFA_REQUIRED from the 403 text to the 409 description: RED (2 cells, the 409 boundary holds).
    - M4 drop INSUFFICIENT_VERIFICATION_LEVEL from POST 403, add it to the GET /api/documents description: RED (wrong-operation move is caught).
    - M5 rename the provenance onBehalfOf 403 code: RED.
    - M8 remove FORBIDDEN from the shared ErrorResponse vocabulary: RED.
    - M9 rename AUTH_PROVIDER_NOT_ALLOWED in enforcement.ts: RED.
    - M1 gateway handler answers 403 through a helper function with a new code: GREEN (missed).
    - M2 gateway 403 whose code comes from a variable: GREEN (missed).
    - M7 enforcement 403 built via Object.assign (not an `ok: false` literal): GREEN (missed).
    - M6 a comment line containing `status(403)` and `code: 'OLD_RETIRED'` added in the gateway handler: RED (a false red, the scan reads comments).

## Findings

Major: none.

Minor
- M-1 The scan reads comments and strings. M6: a comment `// was: res.status(403).json({ code: 'OLD_RETIRED' })` inside the handler turns three cells red. Direction is safe (false red, not false green) but a future explanatory comment will fail the build with a confusing message. Evidence: mutations.txt, M6.
- M-2 `onBehalfOf403Codes` scans the whole provenance.ts, not just resolveOnBehalfOf, and `literal403Codes` takes the first `code: '...'` within 320 chars of any `status(403)`, so a 403 with a non-literal code followed soon after by another literal (e.g. a 404 or 502) would be attributed that other code. No such pattern exists in the two handlers today (I read both); it is a latent false attribution, not a present one.

Note (blind spots, already stated in the file header; mutants confirmed missed)
- N-1 A 403 through a helper (M1), a code held in a variable (M2) and a non-literal `ok:false` object (M7) are not seen. The header states the first two; the third (a spread or Object.assign) is within "a code built from a variable". The file's own wording that the guard fails on "a helper that answers 403 elsewhere" is accurate; the unit cells do not claim more.
- N-2 Global middleware ahead of the handler is out of scope by design, and it does emit unpublished 403 codes on this path: gateway csrf.ts answers 403 CSRF_ORIGIN_INVALID / CSRF_TOKEN_MISSING / CSRF_TOKEN_MISMATCH / CSRF_TOKEN_INVALID for a request that carries a cookie and no Bearer/x-api-key (csrf.ts 340-460, mounted index.ts 371-372). So "emitted = FORBIDDEN + four" is true for the handlers, not for every 403 a client can receive; the spec's "NOT exhaustive" wording covers this. The proxy scope check (INSUFFICIENT_SCOPE, proxy.ts 638) is NOT reached for POST /api/documents because createVerificationRoutes is mounted at index.ts 891, before createProxyRoutes at 1097 and the verification handler always responds. I did not run a live request to prove either point. Recommend the PR text say "handler-level" rather than "the set".
- N-3 Only the shared ErrorResponse vocabulary is trusted for FORBIDDEN; the second direction (published-but-not-emitted) is checked only for codes named in the 403 text, not for the vocabulary, which is correct for generic codes.

## NOT tested
- Live behaviour: no request was sent to a running gateway/originate (Docker is down); every claim about emitted codes is from source reading plus the source-scan itself, including the CSRF and proxy-ordering points in N-2.
- The author's "green twice" and exact 110/1047 on their base were not reproduced; I ran 111/1053 once on the merged tree.
- `check:test-types` does not cover api-gateway, so tests-type cleanliness of this file is covered only by the api-gateway tsc (exit 0), whose tsconfig may exclude `__tests__`; I did not verify that.
- No GitHub, CI or ticket state was read; PR metadata (title, body, checks) was not examined.
