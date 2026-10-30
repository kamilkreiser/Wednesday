## QA GATE - TIER 1, round 1: GO WITH NOTES

**Subject:** PR #1830 (Secuura/Distributed_Secuura), KS-1792, author Seat T 7th. GitHub sign-in adapter refuses a 200 token answer that has no usable access_token.
**Head:** `8c4dcba109f8555f8074e34a2bc13d3e0ad9c652`. ls-remote at start and at end (15:00:51 AEDT) gave the same value, so the head did not move.
**Base:** merge-base `530f091120d5`. origin/develop is `85cd24d81cb9`. The moved range `530f091..85cd24d` touches nothing under `services/auth` (the `git diff --stat` is empty).
**Gate:** QA gate 33, tier 1 (authentication surface), findings only. Clone at `0_Brain/reference/2026-10-30_gate33-1830/repo`. Nothing was pushed or commented, and nothing was written under `!CODING/`.

### Verdict in one paragraph
The fix is correct. It refuses every shape I tried of a 200 token answer with no usable `access_token` before any `/user` call: missing, null, `""`, number, boolean, object, array, an error field (even next to a valid token), an array body and a string body. Nothing else changes: routes/auth.ts, the sibling providers and the `/social/link` mapping are the same as at base. The refusal log carries only the error code, cut to 80 characters, never the token. I confirmed the user-visible message change through the real routes, so the author's read-only claim is now a run fact. The red-proof holds: at base R1-R3 are red and C1-C2 green, and at head all 5 pass. The whole auth suite is green, the type ratchet has 0 new errors and eslint is clean. The one thing to fix before merge is cheap. Two of the four mutants in the brief, plus one more of mine, **survive the PR's own 5 cells**: accepting an empty string, dropping the error clause, and logging the token. The cells cover fewer shapes than the code refuses.

---

### Findings (ranked)

**F1 - Minor - FIX BEFORE MERGE (cheap: 2-3 cells). Coverage: mutants on the empty-string clause and the error clause survive the PR test file.**
- **M4** (accept an empty string: remove `|| tokenBody.access_token === ''`) gives 5/5 green on the PR file. No cell sends `{"access_token":""}`. The brief lists this mutant by name, and a survivor counts as a coverage finding.
- **M5** (remove `|| tokenBody.error !== undefined`) gives 5/5 green. R1 carries an error but no token, so it is refused by the typeof clause whatever the error clause says. No cell sends an error next to a string token.
- Fix: add a cell for `{"access_token":""}` and a cell for `{"access_token":"x","error":"bad_verification_code"}`. Each should expect the token-exchange message and `calls == [token endpoint]`. My probe cells P2 and P6 kill M4 and M5 respectively (see the mutant table).

**F2 - Note (recommend adding with F1). No cell pins "the refusal log never carries the token".**
- **M7** (log the whole `tokenBody` in the warn) gives 5/5 green on the PR file. The test mocks the logger silently and never inspects it.
- The code at head is correct. Probe P14 confirms that the only log line is `["GitHub token endpoint answered 200 without an access token", {"provider":"github","error":"bad_verification_code"}]`, with no token in any logger channel. P15 confirms the error string is cut to 80 characters.
- An assertion over `silentLogger.*.mock.calls` that excludes the token value would kill M7.

**F3 - Note. A JSON `null` body or a non-JSON 200 body is refused before `/user`, but as a raw TypeError or SyntaxError whose text reaches the client.**
- P10 (`null`) gives `TypeError: Cannot read properties of null (reading 'access_token')`.
- P11 (form-encoded) gives `SyntaxError: Unexpected token 'e', "error=bad_"... is not valid JSON`.
- The login callback echoes `OAuth authentication failed: <message>` to the client. **This is not a regression.** At base, destructuring `null` and `json()` on a form body throw the same classes. GitHub sends JSON because the request sets `Accept: application/json`, so this is theoretical. It is a possible follow-up: wrap the body read so that any unparseable or non-object answer becomes the same token-exchange refusal.

**F4 - Note. Shapes the guard deliberately does not judge.** All of these reach `/user` and fail there, which is safe:
- a whitespace-only token (P12),
- `token_type` other than bearer (P13). GitHub only issues bearer, and the RFC does not require the client to check it here.
- Separately, P7 (`{"access_token":"x","error":null}`) is **refused**, because `null !== undefined`. This is over-strict but harmless, since GitHub never sends `error: null`.

**F5 - Note (out of scope, follow-up candidate). The sibling adapters keep the unchecked read.**
- google.ts:87, facebook.ts:82, linkedin.ts:85 and microsoft-personal.ts:87 still take `access_token` unchecked.
- apple.ts:86 takes `id_token` unchecked, so a missing one becomes a TypeError on `.split`.
- These providers answer errors with non-2xx, as RFC 6749 §5.2 requires, so the GitHub-specific "200 with error" case does not apply to them. Their defensive posture is still weaker. None of them is touched by this PR.

**F6 - Note (evidence of value, not a defect).**
- My route probe used the ks1240b harness, whose `/user` stub answers 200 whatever the bearer.
- At **base**, `GET /social/github/callback` with a token answer of `{}` answered **200**: a sign-in completed on `Bearer undefined`. The base guard against that was GitHub's own 401 and nothing in our code.
- At head the same call answers 400 with the token-exchange message.

**Not a finding (as briefed):** the docs entry section 122 collides with develop. Renumber at merge prep.

---

### Q1 - Is the refusal correct and complete?

The guard is at `github.ts:88-92` (head):

```ts
if (typeof tokenBody.access_token !== 'string' || tokenBody.access_token === '' || tokenBody.error !== undefined) { ... throw new Error('GitHub token exchange failed (no access token)'); }
```

It sits after the `!tokenRes.ok` branch and before the only `/user` fetch (line 94). The `/user/emails` fetch comes after `/user`. Both callers go through `exchangeCode` → `exchange`: `routes/auth.ts:1076` (the login callback) and `routes/auth.ts:1361` (`POST /social/link`).

| Shape (HTTP 200) | Refused before /user? | PR cell | My probe |
|---|---|---|---|
| error + description, no token (`bad_verification_code`) | yes | **R1** | - |
| `{}` (token missing) | yes | **R2** | - |
| access_token is a number | yes | **R3** | - |
| access_token `null` | yes | - | P1 |
| access_token `""` | yes | **none (M4 survives)** | P2 |
| access_token boolean, object or array | yes | - | P3, P4, P5 |
| error field next to a valid string token | yes | **none (M5 survives)** | P6 |
| `error: null` next to a valid token | yes (over-strict) | - | P7 |
| JSON array body `[]` or string body `"x"` | yes | - | P8, P9 |
| JSON `null` body | yes, as a raw TypeError (F3) | - | P10 |
| non-JSON (form-encoded) body | yes, as a raw SyntaxError (F3) | - | P11 |
| whitespace-only token | no, so /user is called and GitHub 401s | - | P12 |
| `token_type: "mac"` | no (not checked) | - | P13 |
| non-2xx | unchanged (HTTP-status message) | **C2** | - |
| good token | signs in with `Bearer <tok>` | **C1** | - |

### Q2 - Does anything else change?

- **Files:** github.ts (+8/-2), the new test file and two Projects Documents html files. `routes/auth.ts` is unchanged, as are the other five provider adapters and the errorHandler.
- **User-visible message:** I ran this through the real routes and errorHandler (ks1240b harness copy). The token answer was `{}` and `/user` answered 401, as real GitHub does for `Bearer undefined`.

  | Route | Base | Head |
  |---|---|---|
  | `GET /api/auth/social/github/callback` | `400 BAD_REQUEST "OAuth authentication failed: Failed to fetch GitHub user profile"` | `400 BAD_REQUEST "OAuth authentication failed: GitHub token exchange failed (no access token)"` |
  | `POST /api/auth/social/link` | `500 INTERNAL_ERROR "An unexpected error occurred"` | the same (plain Error, generic 500, unchanged) |

  So the author's claim, which they read from the code but did not run, is **confirmed by a run**.
- **Consumers of the old string:** a `git grep` over frontend, mobile, sdk, api-gateway and tests found none outside the providers. ks1240b:115 uses `'Failed to fetch GitHub user profile'` as the `/user`-401 path with a good token, which still holds, and its suite is green. The ks795 fingerprint pin hashes only the `emailVerified` lines, which this PR does not change, and it is green.
- **Logging:** one new `logger.warn` with `{provider, error: <code, cut to 80 characters>}`. **No token is logged** (P14). The existing `!ok` branch still logs a 200-character slice of the non-2xx body, as before.

### Q3 - Red-proof and mutants

**Red-proof** (spark_gate.sh, which runs the test file alone on BASE product code and on HEAD):
- At BASE: R1, R2 and R3 are red, each with `expected 'Failed to fetch GitHub user profile' to be 'GitHub token exchange failed (no access token)'`. C1 and C2 are green.
- At HEAD: 5/5 green. I reproduced this in my own clone: 5/5.

**Mutants:**
- Each mutant was applied to github.ts by anchor replacement with anchor count 1.
- Each was checked to parse with `ts.transpileModule`, giving 0 diagnostics.
- The file was restored from a copy, and the restore was asserted by sha256 `7697077f78a27e37cf8a5e949c01d04d85ae301aebd86cfa5243898a86bb8f91` after every mutant. The clone's `git status` was clean at the end.
- The script is kept at `mutate.py.txt`.

| # | Mutant | Parses | PR file (5 cells) | + gate probe | Verdict |
|---|---|---|---|---|---|
| M1 | drop the check (`if (false)`) | yes | **R1, R2, R3 red** | P1-P9, P15 red | killed |
| M2 | check only `access_token === undefined` | yes | **R3 red** (1/5) | P1-P7 red | killed (by R3 only) |
| M3 | guard moved after the /user call | yes | **R1, R2, R3 red** | P1-P9 red | killed |
| M4 | accept an empty string | yes | **5/5 green** | P2 red | **SURVIVES the PR file (F1)** |
| M5 (extra) | drop the `error !== undefined` clause | yes | **5/5 green** | P6, P7 red | **SURVIVES the PR file (F1)** |
| M6 (extra) | drop the typeof clause (undefined/'' only) | yes | **R3 red** | P1, P3-P5 red | killed |
| M7 (extra) | log the whole token body | yes | **5/5 green** | P14, P15 red | **SURVIVES the PR file (F2)** |

### Q4 - Suite, types and lint at the head

| Check | Result |
|---|---|
| auth suite, `vitest run --maxWorkers=3`, ks949 excluded, cwd = services/auth | **110/110 files, 1300/1300 tests pass** (53.7 s, load around 17-20) |
| ks949 run separately (KS-1053) | default 5 s timeout: 30 pass, 1 fails ("the enumeration actually finds seed sites…", timed out at 5004 ms under load 20). With `--testTimeout=30000`: **31/31 pass**. This is the known load timeout, unrelated to this PR. |
| tsc with tests in the program (`node scripts/typecheck-tests/check.cjs services/auth`, the KS-1000 ratchet) | examined 162 files, 111 of them under `__tests__` (floor 105). **42 errors: 42 in the baseline, 0 new, 0 stale.** |
| tsc build (`tsc -p tsconfig.json --noEmit`) | 0 errors |
| eslint on the 2 changed .ts files | 0 errors, 0 warnings. A JSON-format positive control confirms both files were linted and not ignored. |

### Q5 - Spark gate

- **Deterministic half run** (`spark_gate.sh` with the test file and `--node-modules`, rc 0, 31 s). It agreed on the head (tip mode), the merge-base and the diff (4 files, +109/-2). Targeted HEAD: 5 passed, 0 failed. Targeted BASE: 2 passed, 3 failed. facts.json is in the scratchpad (`sg_work/out/`).
- **LLM half (`spark_review.py`) NOT RUN.** `spark/state/round.lock` was held by another operator, `ks_1544c_originate_paged_lists_total_order`: first the control round from 14:49:54, then the rebrief round from 14:59:46. That operator's queue looked set to hold the box past the ~20 min wait limit.

---

### What I did NOT test
- Live GitHub. Every answer was stubbed, either as a recording `fetch` stub or as the ks1240b local HTTP stub.
- The `/user/emails` path and profile mapping, beyond what the existing suites cover. This PR does not touch them.
- The sibling providers' token handling, beyond reading the code (F5).
- The frontend's rendering of the new callback message. No frontend consumer of either string was found by grep.
- The Projects Documents html changes (docs, not the auth surface). The section 122 renumber is deferred as briefed.
- The full repo preflight (`preflight.sh`). I ran only the auth ratchet leg.

### Instrument errors (mine, corrected)
1. **First whole-suite run had the wrong cwd.** `vitest --root` does not change `process.cwd()`, so the run was rooted at `/Volumes/DevMASTER/WEDNESDAY`. ks1009 and ks1467 (path-relative reads) failed, and auth.integration hit a `beforeAll` hook timeout at load 20. The result was 3 failed files and 2 failed tests. I re-ran with cwd = services/auth (a Python subprocess with `cwd=`, since the hooks forbid `cd`): 110/110 and 1300/1300. I used the cwd-correct run for every later check.
2. **Console output from the probe cells** was suppressed by the test setup in the route probe. I switched to appending results to a scratch file through an env-named path.
3. **ls-remote:** one end-of-run `ls-remote` without the deploy key answered "Repository not found". That was an auth instrument error, not a moved head. I retried through the clone's repo-local `core.sshCommand` and got the same head.
4. **Clone assertion:** `rev-parse --show-toplevel` was asserted right after `git clone` into the non-existent path, before the PR-ref fetch. The clone is itself the first network read.

### Artefacts
- `repo/`: the clone, clean at the head (`git status` empty). It has node_modules installed and `packages/shared` built.
- `gate33-probe.test.ts.txt`: probe cells P1-P15, adapter level.
- `gate33-route-probe.test.ts.txt`: the route probe (copy of ks1240b plus the GATE33 cells).
- `mutate.py.txt`: the mutant runner.
