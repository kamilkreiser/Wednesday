REPORT_SHA256_16: d1d48d9c8fd56dd6

# Gate verdict: Secuura Platform K PR #1538 (KS-1009, public wallet status answers only { exists })

**VERDICT: GO WITH NOTE.** Major 0. Minor 3. (Sonnet tier 2, independent re-measurement. Not a deploy recommendation.)

Head under test: `5b4419bf96b39526e3001c8f9000bafdabf87434`, tree `539b048cd05265a7fa1544af7f84581a80cfd942` (asserted equal, `git rev-parse` in my own shared clone), parent `0026a43e6033...` (one commit directly on that develop). Develop at test: `2cdf1d7a9071e078bc3f3b3f4d44ce1fa4e50a6f` (asserted). Overlap between the PR's 4 files and develop's changes since the merge base: **0** (instrument: `comm -12` of the two `git diff --name-only` lists; control: develop's own list is non-empty, 12 files in migrations/049, services/security, packages/shared). `git merge-tree --write-tree develop pr1538` rc 0, tree `efa0aa07...` (clean).
Report sha256/16: see line 1 of this file (recipe in the last section).

Method: `git clone --shared` of 2_Project_Files into my scratchpad (push URLs disabled), remote `gh` fetched `refs/pull/1538/head` and `develop` with the project's `core.sshCommand`; two worktrees (head, develop), `node_modules` symlinked from the project (read-only use). Nothing written in the project folder. A throwaway PostgreSQL 15 was started and stopped (see 2).

## 1. New cells and the whole suite

| Run | Instrument | Result |
|---|---|---|
| New file on develop (copied in, scratch), run 1 and 2 | `vitest run` verbose | 4 failed (cells 1, 2, 5, 6) / 4 passed (3, C1, C2, C3), identical in both runs |
| New file on head, run 1 and 2 | same | 8/8 |
| Whole services/auth on head, 2 runs, idle | `vitest run` | 94 files / 1061 tests, 0 failed, both runs |
| Whole services/auth on develop (control, no new file) | same | 93 files / 1053 tests, 0 failed (1061 - 8 = 1053: the PR adds exactly 8 tests, 1 file) |
| tsc --noEmit (services/auth), eslint on wallet.ts + auth.openapi.ts | | rc 0, rc 0 |
| `generate-openapi --check` on head and on develop | `tsx scripts/generate-openapi.ts --check` | both CHECK PASS (so no drift pulled in); `check:spec-examples` 414 blocks OK |

Control for "red": the same file is green on head and red on develop in the same worktree layout, and C1/C2/C3 stay green on both.

### The ks949 flake: REPRODUCED and explained (not caused by this PR)
- What `ks949-platform-admin-seed-identity.test.ts` "the enumeration actually finds seed sites" does: `seedSites()` walks the WHOLE `Blockchain/Dev` tree (`devRoot = here/../../../..`), skipping node_modules/dist/build/coverage/.git/__tests__/__mocks__, and reads every .ts/.js/.mjs/.cjs/.sql/.sh file (about 975 files in the project tree; I measured 2120 files seen). It has no explicit timeout, so vitest's 5000 ms default applies, and two other cells in the same file call the same walk.
- Reproduction: whole suite under CPU contention (12 busy-loop node processes). **head: the cell failed with `Error: Test timed out in 5000ms` in run 1; in run 2 two ks949 cells failed with the same error. develop (the new file absent): the same ks949 cell failed in loaded run 1, and loaded run 2 failed at least four tests (output truncated at four) (ks949 again, plus ks1186 and ks728 timing out)**. Idle runs: 0 failures on both. Mechanism control: `--testTimeout=150` on ks949 alone makes the same 3 walk-dependent cells fail with "timed out in 150ms" (the walk is wall-clock bound); the walk measured 0.2 s warm, 2.0 s on a cold first read of the project volume, 0.24 s under the same CPU load.
- It does NOT depend on the new test file (fails on develop without it; the new file lives in `__tests__`, which the walk skips, and has no `INSERT INTO users`). Order dependence: none found. So the author's earlier failure (a full run alongside the `ks1000` tsc gate on the external volume) is explained as load/cold-cache timeout. Not established: which exact load the author had.
- Residual risk (Minor M1): the three ks949 walk cells can flake red on a loaded runner. Minimal fix (separate ticket, not this PR): give those cells an explicit timeout (for example 30 000) or hoist `seedSites()` into a `beforeAll`.

## 2. The response over the REAL route with a REAL database
What I ran: PostgreSQL 15.x (homebrew), throwaway cluster in my scratchpad; the project's real migrations `001_initial-schema.sql`, `002_verification-tiers.sql`, `030_auth_user_columns.sql` (real `users` table); the REAL `auth_find_user_by_wallet` SECURITY DEFINER function copied verbatim from `migrations/039_rls_fail_closed.sql` lines 218-222; role `secuura_app` (NOSUPERUSER, NOBYPASSRLS) with EXECUTE on the function only, RLS enabled and forced on `users`, direct `SELECT * FROM users` as that role = `permission denied` (control that the function is the only path), and the function returns the full row (id, role, created_at, ...) to it. The real `walletRoutes` and the real `db.query` (pg pool, `DATABASE_URL` as secuura_app) ran in an express listener; only logger, session, jwt, totp, events, userRepo, cip8 and the authenticate middleware were stubbed (as the author's harness). Same 25-request matrix sent raw over HTTP to develop and to head, bodies and headers compared (`evidence/real_compare.txt`).
Not run: migrations 002..049 in full, the gateway, nginx, Redis, the production image.

- Registered wallet (3 spellings that hit: exact, exact with trailing `/`, the mixed-case seeded address): develop answered `{"exists":true,"userId":"d8e83bf2-...","role":"ISSUER_ADMIN_SEED_1538","createdAt":"2026-10-13T02:01:20.153Z"}`; **head answers exactly `{"exists":true}` (15 bytes, one key)**; headers on head: x-powered-by, content-type, content-length 15, etag, date, connection, keep-alive; no id/role/date header.
- Unregistered / variant addresses: uppercased, trailing `%20`, leading `%20`, lowercased mixed-case, Cyrillic homoglyph `%D0%B0`, 9000-char address, `' OR '1'='1` (raw and encoded), `%25`, unknown wallet: **body and headers byte-identical to develop (status 200, `{"exists":false,"message":"Wallet not registered"}`)** except the date header (excluded). 20 000-char path: 431 on both. Matching is exact (case, whitespace, unicode do not collapse onto a registered row).
- Error paths: `%00`, `<registered>%00`, malformed `%E0%A4%A` produce 500 on BOTH develop and head with the identical body `{"success":false,"error":{"code":"INTERNAL_ERROR","message":"An unexpected error occurred"}}` (no row, no pg message echoed). `<registered>/extra` and `/status/` : 404 both.
- Public stays: all the above sent with no Authorization header and answered 200. Methods: POST, PUT, DELETE, PATCH = 404 on both; HEAD and OPTIONS (`Allow: GET,HEAD`) unchanged. HEAD differs in headers only through content-length/etag for the registered address (it is a HEAD of the trimmed body).
- Control for the matrix: the same script run against develop shows the leak (so the comparison can tell old from new).

## 3. Other routes returning the same fields
`git grep` over the whole PR tree (`evidence/grep_walletfind.txt`, `grep_walletstatus.txt`): in services/auth `wallet.ts` the routes are `POST /challenge` (touches no user row: returns challenge id/nonce/expiry only), `POST /verify` and `/authenticate` (return tokens and `user {id,email,role,verificationLevel,walletAddress}` only after a verified CIP-8 signature, i.e. not anonymous), `GET /status/:walletAddress` (this PR), `/link` and `/unlink` (behind `authenticate()`). The api-gateway's mock wallet endpoints (`/challenge`, `/authenticate`) are gated by `ENABLE_MOCK_ENDPOINTS` and echo only the caller's own input; there is no mock for `/status`. No `/api/wallet/status` handler exists in the repo (the e2e call at `tests/e2e/.../happy-path-wallet.spec.ts:255` asserts `< 500` only). Nothing else returns userId, role or createdAt keyed by a wallet address to an anonymous caller. Report only; scope not expanded.

## 4. The spec and its consumers
- Structural yaml diff (js-yaml walk, develop vs head): **exactly 4 differences** (`WalletStatusResponse.properties.userId`, `.role`, `.createdAt`, and the operation `description`); planted-difference control (one summary word changed) is detected as a 5th. The raw `git diff` agrees (15 lines in the yaml).
- `.passthrough()` remains on WalletStatusResponse (`auth.openapi.ts` ~1517), so Schemathesis cannot catch an added key. The ONLY thing pinning the trim at the handler is the new cell 1 (`Object.keys(...) == ['exists']`) and cell 2 (raw response text free of the seeded id, role and timestamp, including `2026-01-02`): it pins the BODY text, not the headers and not the error body (see Minor M2). Cell 5 pins the yaml property list exactly (`['exists','message']`); cell 6 pins the description.
- Consumers of the removed properties: `git grep` of the whole PR tree (frontends, mobile, sdk, connectors, e2e, e2e-v2, systemTest, MCP Deployment/openapi.yaml, services/mcp-server/openapi.yaml, docs): none read userId/role/createdAt from this route; the two MCP openapi copies carry no wallet-status entry; the website bundle hit was an unrelated minified match. The api-gateway serves the yaml from `docs/openapi/secuura-api.yaml` (a baked/mounted file), consistent with the PR body's deploy note. Gateway tests that read the spec (ks1359, ks1469, ks1470, ks733): 5 failed / 32 passed on BOTH head and develop with identical failing names (they need a real app boot unavailable in my scratch setup), so they are INCONCLUSIVE here, not evidence of a regression.

## 5. Mutants (cell names: 1 registered exact keys, 2 raw text, 3 unregistered, 5 yaml properties, 6 yaml description; C-cells controls)
Instrument: `evidence/mut.py` applies one substitution, runs the new file, restores the file (worktree diff empty afterwards). Killed BY CELL:
- M1 userId back: cells 1, 2. M2 role back: 1, 2. M3 createdAt back: 1, 2. M4 row spread: 1, 2. M5 unregistered message changed: 3. M6 yaml userId re-added: 5. M7 yaml description restored: 6. (author's 7 all re-derived and killed)
- Mine: N1 rename userId to uid: 1, 2. N2 id under key `ref`: 1, 2. N5 registered answers 201: 1. N6 `exists:'true'` string: 1. N7 yaml adds property `uid`: 5. N9 unregistered branch adds `userId:null`: 3. N12 extra key with padded name: 1.
- SURVIVED: N3 id in an `X-User-Id` response header with the body unchanged (no cell reads headers); N8 the error path echoing a message/param in a 500 body (no cell makes the query throw); N4 the TS description restored with the yaml untouched (the unit file does not read the TS, but `generate-openapi --check` FAILS on it: verified rc 1 "generated YAML differs", so a different gate kills it); N10 equivalent (SELECT left wide, answer narrow; behaviourally identical); N11 comment-only control (green, as it should).
- All files restored: sha256 of auth.openapi.ts identical before/after the N4 check.

## 6. Scope and PR body
`git diff --stat pr1538^ pr1538`: 4 files, +224/-35: wallet.ts (25), auth.openapi.ts (15), the regenerated yaml (15), the new test (204). Matches the stated list; no stray files. Handler logic read in full: unregistered condition `rows.length === 0 || !rows[0].id` is equivalent to the old `!userId`; only `id` is selected. The PR body (read from the local copy `5_Project_History/.../ks1009/pr1009_body.md`, NOT fetched live) states the client-visible change in the "Gate status" block, which is the first SUBSTANTIVE block, but the mandatory repo template block (merge warning, ack boxes, PII review) precedes it (Minor M3, cosmetic; the template says to keep it).

## Findings
- **Major: none.**
- **Minor M1** `services/auth/src/__tests__/ks949-platform-admin-seed-identity.test.ts:318` (and the two cells calling `seedSites()` at 293-316): whole-tree walk under vitest's default 5 s timeout flakes under load (reproduced on develop too). Not this PR's defect; do not block on it. Fix: explicit timeout or `beforeAll` for the walk.
- **Minor M2** `ks1009-...test.ts` cells 1-2 pin the body only: a leak through a response header (N3) or through an error body (N8) would pass the unit file. No such leak exists today (verified over the real route in section 2). Fix if wanted: add an assertion that the response header names are the Express defaults, and one error-path cell (stub `query` to throw, assert the 500 body has no seeded id).
- **Minor M3** PR body: the client-visible change is not in its first lines (template block comes first). Cosmetic.
- Note (external, not a code defect, not counted): Platform S's use of the route is still unknown (KS-1009 question dd3a7a2a to Stuart); the PR body says it must not merge as it stands if S reads any removed field. That decision is outside what a code gate can measure.

## NOT tested
Live GitHub PR body and check runs; the rest of the migrations (002-049 beyond 001/002/030) and any non-default RLS policy set on `users`; api-gateway with the baked yaml; nginx/ingress in front; Schemathesis, Akto (the HIGH NO_AUTH finding stays open by design), Playwright, k6; response-timing difference between the two branches (the PR says unexamined, I did not examine it either); behaviour with Redis/session stack up; Platform S.

## Cleanup
Throwaway PostgreSQL stopped (`pg_ctl stop`; no process on port 54938 afterwards) and its data directory and socket directory removed. Nothing pushed, no GitHub or Linear write, no remote box. Scratch clone and worktrees remain in the session scratchpad. Evidence: `evidence/` in this folder (cells_*, suite_*, real_*, mut_*, mutants.json, genopenapi_*, yamldiff_mine.txt, grep_*), plus the harness scripts `mut.py`, `real1538.test.ts`, `walk.mjs`.

## Hash recipe
`REPORT_SHA256_16` on line 1 = first 16 hex chars of sha256 over this file with line 1 and the blank line 2 removed (that is, the text from "# Gate verdict" to the end), computed with `shasum -a 256`.
