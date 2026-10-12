# QA gate: Secuura Platform K PR #1496 (KS-1496)

- Head: 3470818891032c490112f1317a6affb880acf965 (merge commit; parents a9eca364 author's commit, 3fd441aa develop). Confirmed from the bundle.
- Base used: origin/develop 1158045e52b834d2a6cda5e2160c1d3d412a3526 (fetched today). Merge-base with the head is 3fd441aa.
- Gate seat: Sonnet tier, independent clone in the session scratchpad. Nothing in !CODING was written.

## VERDICT: GO WITH NOTE

The change is exactly what it claims (one test file, +149/-2, no product change), all five pins are real and each goes red under its own mutation, and every number reproduced; the notes are gaps in what M1/M2 can see, none of which the claim promised to cover.

## By my runs

1. `git diff --stat origin/develop...pr1496` (three-dot, so it ignores develop's own movement): 1 file, `services/api-gateway/src/__tests__/ks1480-no-allowance-warning-fields-are-escaped.test.ts`, +149/-2. `git diff pr1496^2 pr1496 -- <that file>` shows the two `-` lines are the `lines` helper getting `(c: unknown[])` and `(l: string)`. `rateLimitEnforce.ts` is byte-identical between pr1496 and origin/develop (the api-gateway stat against develop lists only the test file). CONFIRMED. A two-dot diff against current develop lists 17 files only because develop moved past the merge parent; none of them is in api-gateway.
2. `npm ci --ignore-scripts` in Blockchain/Dev, rc 0. The first full-suite run failed 74 files on `Failed to resolve entry for @secuura/shared`, so I ran `npm run build` in packages/shared (rc 0), which is the build tsc/vitest need here.
3. The file alone: vitest 4.1.11, 14 passed / 14 on the head.
4. Full api-gateway suite on the head (after the shared build): 111 files / 1058 tests passed, rc 0. Matches the author.
5. Same suite on develop 1158045e with only the PR's test file checked out onto it: 111 files / 1058 tests, rc 0. So the claim holds on the real current develop.
6. Type-check: api-gateway `tsconfig.json` EXCLUDES `src/__tests__`, so `npm run build` never sees this file. `check:test-types` is hard-wired to `services/auth` and covers nothing in the gateway. I wrote a temp `tsconfig.gate.json` (extends the gateway config, strict, noUnusedLocals) including the test file: tsc rc 0. Planted-error control (`const zzbad: number = 'x'`) gave TS2322 and TS6133, rc 2. So the clean result can fail. CONFIRMED.
7. eslint on the test file and rateLimitEnforce.ts by absolute path: rc 0, zero warnings. `eslint src` (the package `lint` script) rc 0, 36 warnings, none from this file.
8. Mutation runs, all against rateLimitEnforce.ts, restored from a pristine copy after each (full table in mutation-results.txt, script in mut.py.txt). Result is the failing test titles; a run counts red if the vitest rc is 1.
   - NEGATIVE CONTROL N1 (comment-only edit): rc 0, nothing red.
   - P1: DEL not escaped (A1) red P1 only; class starting at U+007E so the tilde is escaped (A2) red P1 only; DEL written as `\x7f` (X7) red P1 only.
   - P2: range ends U+009E (A3), starts U+0081 (A4), runs to U+00A0 (A5), runs to U+00A1 (A6), only NEL (A7), a hole at U+0090 alone (A8): each red P2 only. Uppercase hex (E3) red P1+P2.
   - P3: quote not escaped (Q1) red P3 only; quote escape that doubles the backslash (Q2) red P3 only; typed-equals-real collapse, a regex folding `\+"` to `\"` (X6) red P3 only, and that one is only reachable through the last assertion of P3, so that assertion has teeth.
   - M1: set loses oauth_app (S2), gains `Api_Key` (S4), `Oauth_App` (S5), a member with a newline (S6), has() lower-cases (S12), has() trims (S13), gate widened to any string (X4): each red on M1 (and M2 where the declaration changed).
   - M2: gains `sso` (S1), gains `oauth` (S3), spread of a defined array (X1), `as const` argument (X2), computed template member (S8, X8), `Set<string>` generic (S15), built from Object.keys (S16), inner-scope second declaration (S17), a live declaration under a commented-out copy (S14), rename plus alias (X9): each red on M2 only. S7 (spread of an undefined name) fails the module load, rc 1.
   - Pre-existing cells also trip where they should: no JSON escaping at all (Q3) red 7 cells; escape-before-JSON (E2) red P1+P2.
   - MUTANTS THAT STAYED GREEN (findings below): S9, S10, S11, X3, E1, X5.
9. AST reader controls: 6 controls inside M2 all pass (comment copy invisible, added member seen, spread refused, template member refused, two declarations refused, no declaration refused). Count of outsiders in M1 re-counted by hand: 10 + 10 + 5 + 7 = 32. CONFIRMED.

## Findings

Major: none.

Minor
- m1. M2 and M1 pin the DECLARATION and a fixed list of 32 outsiders, not the runtime membership. These stay green: `MACHINE_AUTH_METHODS.add('evil')` after the declaration (S9) and `(... as Set<string>).add('evil')` (S10), an extra condition in the gate `|| user.authMethod === 'sso'` (S11), and a widened copy of the set in the gate with the declaration untouched (X3: `new Set([...MACHINE_AUTH_METHODS,'oauth']).has(...)`). Any of them admits a value that `warnNoAllowance` writes into the log UNESCAPED (rateLimitEnforce.ts line 123 `(${authMethod}, ...)`), which is the exact reason M1/M2 exist. The claim ("members read from the AST") is literally met, but the protection stated in the file header (safe only because the gate admits only the fixed tokens) is weaker than it reads. Cheapest fix: have the warning path escape `authMethod` with `logField`, which removes the dependency; or add to M1 an outsider carrying a newline plus a `.add` / extra-condition mutation. Not blocking for a test-only PR.

Note
- n1. 'oauth' omission is RIGHT, and I find no hole created by it. auth.ts line 160 takes `authMethod` from the signed JWT payload (default 'email') and line 321 sets 'api_key'; the 'oauth' label is used in scopes.ts. If KS-1156 adds 'oauth' to the set, M2 fails by design and forces the exact-members edit; if someone renames oauth_app to oauth, M2 also fails. Pinning 'oauth' as a non-member in M1 would fail the day KS-1156 lands. The one cost: an 'oauth' admitted OUTSIDE the set (X3-style) is invisible, which is m1 again.
- n2. A final `.trim()` on `logField` (X5), or a trim before the JSON step (E1), stays green: trailing whitespace on an id is silently dropped, so the KS-1480 promise "ordinary ids are written byte for byte" is not pinned for edge whitespace. This is a pre-existing gap in the KS-1480 O cells, not something the five new pins claim; safety is unaffected (a trimmed newline is gone, not forged).
- n3. Backslash not escaped while quote is (my Q4) leaves P3 green, because typed and real still differ. Other cells (E4, O3) catch it. P3 pins the quote, not injectivity.
- n4. M2 reads the product source by `resolve(__dirname, '../middleware/rateLimitEnforce.ts')`. A move or rename fails closed (readFileSync throws), not green. `__dirname` works under vitest 4.1.11 here; if the package ever goes ESM-only it must be revisited.
- n5. M2 is deliberately brittle: `as const`, a `Set<string>` generic, or a built-from-constants set all fail it. That fails closed and is the right direction.
- n6. The test file adds the `typescript` import at runtime in the test; it resolves from the workspace root (installed). No package.json change was needed.
- n7. The PR title/branch reuses number 1496 for ticket and PR; not an issue, just keep them apart in the record.
- n8. P1/P2/P3 and M1 give distinct buckets per probe (tenant/connector include the code point or a counter), so the 30 s warning throttle cannot hide a second probe. Checked by reading, and every P2 iteration asserts exactly one line.

## NOT tested

- Docker, a real Redis, or any deploy (down / out of scope); the limiter ran on the test's fake Redis only.
- The author's own tamper record and its 11 mutations were not replayed one for one; I ran 40 mutations of my own that cover each pin, so a single-line match to their list is not claimed.
- `check:test-types` was run only as a read of its scope (auth only); I did not execute it.
- Windows or non-Node-24 runtimes; vitest was 4.1.11 on node v24.7.0 darwin-arm64.
- Whether other gateway files write other claims unescaped (out of this PR's scope).
- GitHub CI status of the PR itself (no GitHub access).
