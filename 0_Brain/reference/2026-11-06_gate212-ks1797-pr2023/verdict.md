GO WITH NOTES

# Gate 212: Secuura / Blockchain, PR 2023 (KS-1797 POST half), tier 1, round 1 of 2

Covers SHA 5c828fa98931d605e69beec75565d0f548ee1377 only. Base is develop 1b1b65c7415f (worktree `base/`).

Head readings (develop read 1b1b65c7415f at the start and the end, from my clone's local origin):
- start, 23:36Z: 5c828fa98931, detached at the PR head
- mid-run: the clone is a detached checkout, so it cannot move; `oauth.ts` read sha256 21e0baec after the mutants (equal to the start)
- end, 23:49Z: 5c828fa98931

Dependencies are symlinks to gate 204's install. Its lockfiles and packages/shared tree are identical to this head's (hashes compared). Node v26.8.1 (not LTS), vitest 4.1.12.

**BLUF:** The guard does what Wednesday ruled. It is byte-equal to the GET guard and sits right after the destructure, so nothing runs before it. On the real route over real HTTP, with collaborators doubled:
- All 5922 non-string rows answer the same 400 with every call count 0.
- All 2619 string or absent rows are identical to base.

Two things need your eye:
- The refusal also covers `null`, numbers and booleans, which base accepted. The READY does not list this (N1).
- The seat's "8 of 8 mutants killed" does not reach that part of the predicate. Two mutants of mine survive the seat's file (F1).

Nothing here blocks a GO on this SHA.

## Answers

1. **Scope: confirmed.** The diff has exactly 4 paths, +223/-0. `oauth.ts` is +7/-0 in one hunk: a 3-line comment, the 3-line guard and a blank line.
   - The GET guard is untouched: head and base lines 503-505 have the same sha256.
   - The guard is at lines 663-665. Between the destructure's end (line 658) and the guard there are only a blank line and the comment.
   - The first later calls are `action === 'deny'` (679), `resolveAuthorizeClient` (680 and 739), `enforcePasswordLoginGates` (781) and `createAuthorizationCode` (798). None of them runs before the guard.
   - `git merge-base` prints develop's tip.
   - Evidence: evidence/q1_q2_q8b.txt.

2. **Ruling conformance: confirmed.** The guard is a copy, not a shared function. `cmp` of 503-505 against 663-665 gives rc 0, sha256 d2c0e68a. So there is no divergence, and the status, envelope and description are the same. The lines:
   ```
   if ((state !== undefined && typeof state !== 'string') || (code_challenge !== undefined && typeof code_challenge !== 'string')) {
     return res.status(400).json({ success: false, error: { code: 'BAD_REQUEST', message: 'invalid_request', description: 'state and code_challenge must each be a single string' } });
   }
   ```
   Status is 400, `code` is BAD_REQUEST, `message` is invalid_request. Measured: no Location and no Set-Cookie on any refusal. Only the destructure runs before the guard. `null` IS refused, because it is not undefined and not a string (see N1).

3. **Behaviour table: 8541 rows run on BASE and on HEAD.** Harness: gate212-table.test.ts, the seat's seam plus the urlencoded parser, with the real route and resolver and the real login gate. The dimensions were action x client (public, confidential, unregistered) x credentials (valid, wrong, missing) x MFA (4 variants) x JSON and form shapes, with `code_challenge` with and without a method, plus XHR rows.
   - **Non-string at head: 5922 of 5922** give the same 400 body. That is 1 distinct body whatever the client or credentials, so no enumeration. No Location, no Set-Cookie, and getAppByClientId, the user lookup, password verify, lockout, recordFailure and createAuthorizationCode all at 0 calls.
   - **String or absent at head: 2619 of 2619** identical to base on status, body, Location, cookie, content type, 6 call counts, mint argument and lookup argument.
   - **Every seat claim about develop reproduced on base:**
     - array state on deny: `state=a%2Cb`
     - array state on approve: a code with `state=a%2Cb`
     - array `code_challenge`: a code, with `codeChallenge: ["a","b"]` reaching mint
     - object state: `%5Bobject+Object%5D`
     - form-encoded repeated state: `a%2Cb`
   - **Base minted 396 codes across the non-string rows; head mints 0.**
   - **Beyond the READY, on base:** a truthy non-string `code_challenge` (`[]`, `{}`, `123`, `true`, an array) satisfied the public-client PKCE rule and minted a code. Head closes that. What the code exchange would then do with such a row is not measured (mocked storage).
   - Evidence: evidence/table_base.jsonl, evidence/table_repo.jsonl, evidence/q3_q4_analysis.txt, evidence/q3_counts.txt, analyse.py.

4. **Other POST parameters: 336 rows, 0 differ from base, 0 are a 500.** Nothing got worse. See N3 for two follow-up notes. Evidence: evidence/q4_condensed.txt.

5. **Mutants: 8 run, 6 killed, 2 survived (F1).** All compile (tsc rc 0). oauth.ts restored sha256-equal (21e0baec). Every prediction was stated first and held.

   | Mutant | Seat file passes | Red cells |
   |---|---|---|
   | S1 guard on approve only | 9 of 12 | P1, P4, P6 |
   | S2 `Array.isArray` for `typeof` | 11 of 12 | P5 |
   | S3 state clause dropped | 7 of 12 | P1, P2, P5, P6, P7 |
   | S4 `\|\|` to `&&` | 5 of 12 | P1 to P7 |
   | G1 guard after the deny branch | 9 of 12 | P1, P4, P6 |
   | G2 guard after the client lookup | 6 of 12 | P1 to P6 (the approve cells do see the getAppByClientId count; P7 asserts only status) |
   | G3 `!= null`, admits null | 12 of 12 | none, SURVIVED |
   | G4 `typeof === 'object'`, admits numbers and booleans | 12 of 12 | none, SURVIVED |

   Evidence: evidence/q5_mutants.txt, evidence/q5_survivors_admit.txt, mutants.py.

6. **Suites, in my clones, no stack:**
   - **New file on base product:** 7 failed, 5 passed; the 7 are by assertion (302 where 400 is expected). **On head:** 12 of 12. With `ks1797-authorize-get-refuses-a-repeated-state-or-code-challenge.test.ts`: 22 of 22.
   - **The 12 named files:** 187 of 187 on both base and head. List confirmed by `/usr/bin/grep -l -i "authorize"` (positive control: the PR's own file listed). A 13th file with POST authorize lines, `ks799-consent-script-csp-and-execution`, also passes: 194 of 194 with it, on both.
   - **Whole auth suite:** base 1712 of 1714, head 1725 of 1726. Totals equal the seat's. The failures are ks949-platform-admin-seed-identity timeouts: 2 on base, 1 on head. The seat read 3 and 2, so the count varies with load. Alone it is 31 of 31 on BASE and on HEAD. **Classified SAME-ON-BASE; 0 NEW.** The ks1868 C1 timeout did not occur: ks949 is the only failing file on either side.
   - **Static:** tsc rc 0. test-types: 197 files, 41 errors, 41 in the baseline, 0 new; a planted TS2322 gives rc 1 with 1 new. eslint on both files: rc 0; a planted `debugger` gives rc 1.
   - **Instrument note:** my first whole-suite run used `--root` from the wrong working directory, and ks1009 and ks1467 failed because they resolve paths from the process's working directory. I discarded it (evidence/q6_whole_*.json, without `cwd`). The figures above are from runs with the working directory set to the service, by a Python subprocess, not a shell `cd`. One earlier table launch had no output path set, ended on its own before any measured run, and wrote nothing; none of its data is used.
   - Evidence: evidence/q6_*.log, evidence/q6_whole_summary.txt, evidence/q6b.txt, evidence/q6c_q7_q8.txt.

7. **Docs: confirmed.** `docs-fragments.mjs check` at head gives OK with the ADVISORY lines at flow 6249 and cheat 6235, the same as base. Flow goes 165 to 166 new, cheat 165 to 166 new. A planted unbalanced div plus a second h2 in the PR's flow fragment gives FAIL with 2 findings, rc 1. Restored sha256-equal; rc 0 again. Evidence: evidence/q6c_q7_q8.txt.

8. **Merge onto develop: clean.** `merge-tree` rc 0, tree bba50f3d, equal to the head's own tree, because the merge base IS develop's tip. So the range from base is empty and 0 paths are shared. Planted control: a real develop path added to the four is printed by the intersection.
   - **PR 2022 (1a0fa7c23b24):** 12 files, 0 shared, no `oauth.ts`. Gates 211 and 212 are independent by path.
   - **Open PRs: UNMEASURED.** I did not touch GitHub (no external network). My clone's origin is the local checkout, which holds 0 `refs/pull/*`, so I cannot say which refs are open. Among its 988 local branch refs (841 distinct unmerged tips, 0 missing objects), 16 other tips touch `oauth.ts` on a merge-base diff. Most are from September, one is October's GET half, and the newest, 587db03ce183 (KS-1150, 11-05), merges onto this head with a tree equal to the head's, so it adds nothing here. The other 15 were not merge-tested. The instrument that closes this is a `git ls-remote` against GitHub plus a head diff, or the merge driver at merge time (the seat's driver read no overlap with 19 open PRs at 13:51Z).

## Findings

- **F1 (Low): two predicate mutants survive the seat's test file. The behaviour at head is correct; only the pin is missing.** No cell sends `null`, a number or a boolean. `routes/oauth.ts:663`, test file `ks1797-authorize-post-refuses-an-array-state-or-code-challenge.test.ts`.
  - G4 (`typeof === 'object'`) is the one that matters. It would admit `code_challenge: 123` or `true`, and a public client would again mint with a non-string challenge: 16 rows on the table, 8 of each value.
  - G3 (`!= null`) admits `null`, which minted only where base did.
  - Fix shape, for the owner: one `null` cell and one number or boolean cell per field, on approve.
  - Evidence class: **MEASURED AT RUNTIME** (the seat's file plus my table against each mutant). Evidence: evidence/q5_mutants.txt, evidence/q5_survivors_admit.txt.

- **N1 (Note, required naming): a behaviour change the READY does not list.** The READY's "string or absent is unchanged" is exact (2619 of 2619) but incomplete. These values were accepted on base and are refused 400 at head:

  | Field and value | Base |
  |---|---|
  | `state: null`, `0`, `false` | treated as absent: redirected or minted with no state param |
  | `state: 123`, `true` | echoed as `state=123`, `state=true` |
  | `code_challenge: null`, `0`, `false` | confidential client: minted with that value stored in `codeChallenge`. Public client: 400 PKCE, now 400 with the guard's description instead |
  | `code_challenge: 123`, `true` | minted on both client types |

  This is a declared consequence of the ruled predicate, not a defect. The ruling says "array (non-string)", and the GET guard refuses the same values. It also matches the published contract (`z.string().optional()`, auth.openapi.ts). In-repo callers: the consent form sends only strings (FormData) and the Python SDK only builds the GET URL. **READ ONLY** for callers; external clients that send `state: null` are not known. If anyone wants the `null` case softened, that is a ruling for Wednesday, not this gate. **MEASURED AT RUNTIME** for the behaviour. Evidence: evidence/q3_q4_analysis.txt.

- **N2 (Info): the cheat fragment understates the guard.** `fragments/cheat/KS-1797-...html` says "An array or object `state`, or an array `code_challenge`". The guard refuses any non-string, including an object `code_challenge` and the N1 scalars. The flow fragment says "present and not a string", which is exact. **READ ONLY.**

- **N3 (Note, follow-up ticket candidates, pre-existing and unchanged from base, 0 of 336 rows differ):**
  - `action` as an array or object never equals `'deny'`. So `action: ["deny"]` with valid credentials takes the approve path and mints a code. The caller holds the credentials, so nothing is gained over a plain approve, but a "deny" that mints is wrong. **MEASURED AT RUNTIME.**
  - A one-element array `client_id` passes the charset regex by coercion and reaches `getAppByClientId` as an array. With a permissive lookup double it reaches mint with `clientId: ["client-conf"]`; with a strict double it answers invalid_client. **MEASURED** for the route; what the real database function does with it is **READ ONLY** (the query passes it as a parameter), not run.
  - `redirect_uri`, `response_type`, `scope`, `code_challenge_method`, `email`, `password` and `mfaCode` as arrays all answer a 400 on the approve path. On deny, the credential fields are not read at all.
  - Evidence: evidence/q4_condensed.txt.

- **N4 (Info): the form-encoded cells guard only the service layer.** The gateway's `contentType.ts` comment and the OpenAPI text say a non-JSON body to this endpoint is refused 415 at the gateway. So P6 and my form rows are reachable only by a direct call to the service. The cells stay useful as defence in depth. **READ ONLY**; the gateway was not run.

- **N5 (Info, commission):** Q8 names `git ls-remote origin` while the same commission says no external network. I took the stricter reading and did not reach GitHub. See answer 8.

## Not covered

- The real database: collaborators are mocked, so what pg would store for a non-string `code_challenge` on base, and what the exchange would do with it, is not measured.
- A browser on the consent page; a booted service; the gateway and CSRF layers.
- An MFA account reaching mint with an accepted code. The MFA-enabled rows ended in a refusal before mint on both sides, and the guard precedes them all.
- The wildcard-redirect app with an array `redirect_uri`.
- The four platform suites; pre-push legs 3, 4, 8; `npm ci`; any LTS Node.
- Scope dedupe and cap; the other POST parameters except as probed in Q4.
- The PR body on GitHub, and open-PR overlap (answer 8).

The clones are clean against HEAD apart from the dependency symlinks. My test copies are in `_quarantine_2026-11-06/`. No process of mine is left running. Nothing was posted.
