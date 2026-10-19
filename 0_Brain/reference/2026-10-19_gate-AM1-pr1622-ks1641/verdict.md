VERDICT: NO GO at head e065dc9e06d2b52b50944584e9505b95c897dee6 (tier 1, round 1 of 2; landing tree 40a3bc836b0b0e2d4dd2a5f8a62e2eb3bd23dee4 on develop 115797747cb60009e781d80e9059dbbed69e1ac3; 1 blocker, 6 notes)

Gate AM1, PR #1622 (KS-1641 finding 2), Opus, round 1 of 2. Clone: /private/tmp/claude-501/-Volumes-DevMASTER-WEDNESDAY/08573273-0b69-4d9e-abf5-9b213ac8c2f2/scratchpad/am1/repo. Heads re-read by ls-remote at start and before this verdict: develop 115797747cb6, refs/pull/1622/head e065dc9e06d2, unchanged.

## BLOCKER

B1. services/m365-integration/src/index.ts:465 - the new `.slice(0, 200)` cuts by UTF-16 code unit, so it can split a surrogate pair. `encodeURIComponent` then throws `URIError: URI malformed` on the lone high surrogate. Express 4.22.3 does not catch errors from an async handler, and m365 sets no `process.on` handler and does not use gracefulShutdown (grep of index.ts for `process\.on` = 0; positive control `process\.exit` = 1 at :1581). Result: a single UNAUTHENTICATED GET kills the service process. This PR introduces it; develop does not have it.
- Input: `GET /api/callback?error=x&error_description=` + encodeURIComponent('A'*199 + U+1F600 + 'zz'). That is valid UTF-8, so qs decodes it intact.
- Real process (tsx src/index.ts, NODE_ENV=development, Node v24.7.0, driver /private/tmp/claude-501/-Volumes-DevMASTER-WEDNESDAY/08573273-0b69-4d9e-abf5-9b213ac8c2f2/scratchpad/am1/live.js):
  - LANDING tree 40a3bc83, measured twice: control 'A'*198 + emoji gives 302 (Location 269). Split input: socket dropped (UND_ERR_SOCKET), then /health gives ECONNREFUSED, child exit code 1.
  - DEVELOP 11579774: the same split input gives 302 (Location 272), /health gives 200 afterwards, and the child is still alive.
- In-suite probe (vitest, the PR's harness): landing records rejection `URIError: URI malformed` and the request hangs to timeout. Develop records 302 and no rejections.
- None of E1-E4 can see this: every cell is ASCII. The cap needs to be surrogate-safe (or the encode guarded), plus a cell for it.

## Questions

Q1 Cap bounded? Yes, apart from B1. Worst case, measured: 200 code units of U+0800..U+FFFF encode to 1800 chars, astral to 1200, '%' to 600, ASCII to 200. With FRONTEND_URL http://frontend.test the Location is 1859 at most (measured, case bmp3_200). On develop the same input gave 9059. The pre-PR bound was only Node's 16 KB request-header limit (a 45K/60K request returns 431). The `error`-only fallback and a repeated `error_description` array are both capped too (Location 259 / 261; develop 5059 / 362).
Reflection sites in m365-integration. Case-insensitive grep for `res\.redirect|error_description|req\.query|location`. Positive control: :465 and 5 redirects hit.
- :464 log `error` + `error_description` uncapped (unauthenticated).
- :474 log `connectionId` = raw `state` uncapped (unauthenticated). NOT disclosed in the claim.
- :465 redirect (capped).
- :469 and :477 constant text.
- :508 `connectionId` interpolated UNENCODED, but only after a memConnections hit, so `state` must equal a server-issued id. `tenant` is encodeURIComponent'd and uncapped (MSAL/Graph source).
- :515 MSAL `err.message`, which can carry AAD error text. Encoded, uncapped, needs a valid state. Disclosed.
- :742 body `details: err?.message` and :1026 body Graph `error.message`: both authenticated, uncapped.
The log calls use JSON.stringify, so there is no newline injection.

Q2 Scope: the claim says finding 2, 1 of 3 sites, and the diff agrees: exactly 2 files, +76/-1, only :465 changed. Finding 1 says 5 redirects target /admin/integrations, and I counted 5 (:465, :469, :477, :508, :515), none changed. The KS-1641 ticket text itself is NOT in the author's mail (only R's paraphrase), so I could not check the claim against the ticket wording.

Q3 Cells can fail. Measured on the landing tree:
- head: 4/4.
- no-cap mutant: E1 and E2 red, 2 failed / 2 passed.
- `.slice(-200)` mutant: E2 red only, 1 failed / 3 passed.
- E3 and E4 green in both mutants.
- index.ts restored by checkout after each run.

Q4 Injection: none. With `%26` (`a&m365=success&connectionId=evil`), `#frag`, CRLF + `Set-Cookie`, `//evil.example/@x`, a 60K value and the split case, every 302 has host frontend.test, path /admin/integrations, query keys exactly [m365, message] and an empty hash. The decoded message equals the literal. Oversize requests get 431 from Node before the handler. The only escape is B1: a crash, not a redirect change.

Q5 Landing:
- `merge-tree --write-tree` origin/develop origin/pr1622 gives 40a3bc836b0b0e2d4dd2a5f8a62e2eb3bd23dee4, rc 0, which equals the author's prediction.
- Merge-base is 6ec1b7ba.
- Three-dot list: exactly the PR's 2 files.
- m365 vitest on the landing tree: 68 passed / 68 in 10 files, rc 0.
- At develop: 64 / 64 in 9 files, rc 0. My probe file was excluded and its absence from the log checked (0).
- Type-check including the test file (scratch tsconfig.am1.json extends the service tsconfig; listFilesOnly shows ks1641 = 1, probe = 0): rc 0, no output. Positive control: the same config with a deliberate TS2322 gives rc 2.

## Notes

N1. The author's "npx tsc --noEmit rc 0" does NOT cover the test file: the service tsconfig excludes src/__tests__ (listFilesOnly: ks1641 = 0, index.ts = 1). My including-check passed, so this is not a defect, but the claim overstates what was checked.
N2. :474 logs the unauthenticated `state` uncapped. It is missing from the PR's "does not fix" list, which names only :464 and :515.
N3. The services/auth precedent this PR cites (auth.ts:1015-1016) caps the LOG and never echoes ("Logged, never echoed"). This PR caps the echo and leaves its own log (:464) uncapped, so it does not match that precedent.
N4. :508 interpolates `connectionId` without encoding. Not exploitable today (it has to match a server-issued Map key) but fragile.
N5. :742 and :1026 reflect provider/internal error text into JSON bodies uncapped (both authenticated). Out of this PR's scope; candidates for the :515 decision.
N6. The cells cover only ASCII. A cell with a multi-byte character at index 199/200 would have caught B1.

## NOT run

- No Docker, DB or stack; Linear and the KS-1641 ticket not read; the GitHub PR body not read.
- No preflight legs; no other services' suites; no deployed environment.
- The live crash was shown with tsx in NODE_ENV=development, not with the built dist under the production Dockerfile. The image is node:24-alpine, the same major as the measured v24.7.0.
sha256 52d3a6d53fb26e65b484094951c93bcc41dad43975447a93cd6826c71470fc4b
