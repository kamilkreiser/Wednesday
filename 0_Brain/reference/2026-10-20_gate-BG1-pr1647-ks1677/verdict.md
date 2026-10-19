VERDICT: NO GO at head f9f425582bb20f8b01799f8d6b8daf3ab77cfdda (tier 1, round 1 of 2; landing tree 7aa017b89166288f9883ca30b2d6805ad0d5b06c on develop 937c7d10b7f83d2fa7e5e662ce46a9e8877186e3; 2 blockers, 11 notes)

## BLUF

The security core is right, and I measured it holding. A leaked state cannot complete, rebind, flip, burn, replay or race a sign-in on the route. On a REAL Postgres 18 (not PGlite), the exact `OAUTH_STATE_SQL.consume` gives exactly one winner in 50 rounds of 16 concurrent consumes, and a non-atomic control lets all 16 win. Migration 053 is idempotent on real PG. `/complete` is gone from the code and the spec. tsc is rc 0 on m365 and api-gateway. m365 goes from 148 to 194 cells, 0 failed, one rename. Gateway startup-migrations is 38/38 on both sides with identical names.

**Two blockers:**
- **B1:** the binding cookie is set on the ADMIN host, but every services.bicep deployment sends Microsoft back to the API host. On those deployments the real user's callback never carries the cookie, so every legitimate sign-in is refused.
- **B2:** the brief's own PKCE condition is not met. A fixed-verifier mutant survives the whole m365 suite, and so does a mutant where token-manager never passes the verifier to MSAL.

## Findings: blockers

**B1. On every Azure (services.bicep) deployment, every real m365 sign-in is refused (`invalid_state`).**
- **The cause:**
  - The admin wizard calls init with a RELATIVE fetch (`frontend/admin/src/services/api.ts:82`, `fetch(path, …)` from `M365SetupWizard.tsx:95`). So the request goes to `<prefix>-admin.<env domain>`, and admin nginx proxies it (`frontend/admin/nginx.conf:63-66`, `API_UPSTREAM` = `https://<prefix>-api…`, bicep :1515).
  - The browser therefore stores the host-only `m365_oauth_binding_*` cookie (no Domain attribute) for the ADMIN host.
  - But `ENTRA_REDIRECT_URI` is `${apiPublicUrl}/api/m365/callback`, which is the API host (`deployment/azure/services.bicep:1620`; live in `deployment/azure/env.dev.json:107` = `https://secuura02-demo-api.kindtree-935b2ded…/api/m365/callback`). FRONTEND_URL is the admin host (bicep :1627).
  - Microsoft redirects the browser to the API host, so the cookie is not sent, and `consumeOAuthState` is never reached.
- **Measured** with a browser cookie-jar model (tough-cookie 6.0.1, RFC 6265; `scratchpad/gate_bg1/scripts/jar.cjs`), using the exact Set-Cookie attributes init emits:
  - Cookie set via admin-host init, callback at the API host: `""`.
  - **Control:** the same callback path on the admin host: the cookie is present.
  - On the local single-nginx topology (`localhost:6882` serves both `/admin/` and `/api`), the cookie is present.
- **Why the author's probe could not see it:** the "cookie measured live" probe ran on that local single-host topology. On localhost the hostname matches, and cookies ignore ports.
- **This is not a security hole.** It fails closed. But the PR as landed makes the feature unusable on the deployed topology, and nothing in the PR, the deploy notes or the READY says so.
- **Fix options (for the ruling):**
  - (a) Point `ENTRA_REDIRECT_URI` at the admin host (`https://<prefix>-admin…/api/m365/callback`; admin nginx already proxies `/api/`), and register that redirect URI in the Entra app. That means bicep, env.dev.json and an Entra app-registration change.
  - (b) Otherwise, a deploy-round precondition that is named and verified.
  - Either way, it must be decided before landing, not discovered at deploy.

**B2. PKCE: the brief's condition "a mutant that sends no verifier or a fixed one must red" is half-met. The verifier's last hop to MSAL is unguarded.**
- **BG-M7:** `const codeVerifier = 'f'.repeat(43)` (one fixed verifier for every sign-in). tsc rc 0. **Survives all 18 files / 194 cells.**
  - R11 checks S256(verifier) == challenge within ONE sign-in, and a fixed verifier still satisfies that.
  - No cell compares two sign-ins.
  - Fix: one cell that inits twice and asserts the challenges (and verifiers) differ.
- **BG-M11b:** token-manager `...(codeVerifier === 'never-equal' ? { codeVerifier } : {})`, so MSAL never receives the verifier. tsc rc 0. **Survives 194/194.** `exchangeAuthCode` is mocked in every route suite, so "sent at the exchange" is only proven up to the mock's boundary.
  - Against real Entra, this mutant would break every sign-in, because a code issued with a challenge cannot be redeemed without the verifier.
  - Fix: a unit cell on `exchangeAuthCode` with a stubbed `msalClient.acquireTokenByCode` that asserts `codeVerifier` is in the request. msal-node 3.8.10's `AuthorizationCodeRequest` does carry `codeVerifier`.
- **The no-verifier mutant does red:** BG-M10 (callback passes `undefined`) is killed by R11.

## Findings: notes

- **N1. The documented fail-closed property has no cell.** `oauthState.ts` says "when [the DB] is up, the table is the ONLY authority for a consume".
  - BG-M4: on a DB miss, fall back to the memory map. tsc rc 0. **Survives 194/194, and also my four cells.**
  - Its effect would be a second completion across a DB blip, or across replicas: replica A minted the state, B completed it, and a replay to A succeeds while A's in-memory connection still reads `pending`.
  - The code is correct today; a regression would go unseen.
- **N2. BG-M3 (binding cookie value = the state) survives the author's suites.** With it, a leaked state IS the cookie. My cell BG1-X4 kills it.
- **N3. BG-M5 survives the author's suites.** In it, the refusal names its reason for the bound-but-refused cases (`connection_not_pending` / `organisation_mismatch` in the redirect). G1/G2 deliberately do not assert the wording, and R8 compares only unknown with unbound. My cell BG1-X1 kills it: it compares seven refusal kinds byte-for-byte against an unknown state (status, every header but Date, body): no cookie, wrong cookie, unknown-with-cookie, expired, org mismatch, not pending, consumed.
- **N4. KS-1673 A6 is now vacuous.** "as B, POST /api/connections/complete for A is 404" passes for everyone, because the route no longer exists. It no longer reaches the code it is named for. Retire or relabel it (R10 now owns the removal).
- **N5. The spec path count in the READY is off by one.**
  - A YAML parse (the repo's own `yaml` package) gives **312 -> 311 paths** and 347 -> 346 operations, not "311 -> 310".
  - The delta is exactly right: removed `/api/m365/connections/complete` (POST) and schema `M365CompleteConnectionRequest`, and nothing added.
- **N6. Stale references left behind:**
  - `services/m365-integration/SETUP.md:80` still documents `curl -X POST …/api/connections/complete`.
  - `systemTest/schemathesis/config/schemathesis-baseline.json:248,458` still carries two baseline keys for the removed operation. They are dead, not failing. I found no stale-key checker.
  - `packages/shared/src/crypto/encryptedField.ts` lists the encrypted-pair inventory as "22 pairs", and `code_verifier` is not in it.
  - The verifier's AAD string is `svc_m365_connections.code_verifier.<id>`, but the column lives in `svc_m365_oauth_states`. That is harmless (AAD is only a binding label), but it is misleading for whoever next re-derives that inventory.
- **N7. Hardening: cookie tossing.** The binding cookie cannot carry a `__Host-` prefix (that prefix requires Path=/).
  - Whoever controls a sibling host under the same registrable domain could plant their own binding cookie in a victim's browser. Combined with the attacker's own state, that restores the classic "victim's code into attacker's connection" attack.
  - On Azure, the siblings are the other Secuura apps on the environment's domain. On a custom domain, they are every subdomain.
  - Low; record it as residual risk.
- **N8. `initiated_by` (a user id) is now stored per sign-in.** Expired rows are purged only on the NEXT init, anywhere.
  - `userErasedSubscriber.ts` says per-user m365 state should be wiped there, and it was not touched.
  - Low (rows are short-lived in practice), but say so or wire it.
- **N9. `saveOAuthState` swallows a DB insert failure, and init still answers 201 with a URL.** With the DB up, that sign-in can never complete: it fails closed, but the user sees only a refusal. A UX/observability note.
- **N10. Outside the diff, already true before this PR:** nginx `log_format secuura_edge` / default access logs record `$request`, which includes the callback's `code` and `state`. After this PR a logged state is useless without the cookie, and a logged code is useless without the verifier. That is an improvement, so it is a note only.
- **N11. Process disclosure (mine):** my first m365 suite run used `npm --prefix <clone>/services/m365-integration exec -- vitest … --root <clone>` while the shell's cwd was /Volumes/DevMASTER/WEDNESDAY. That breaks the letter of the brief's npm-exec rule. I verified that nothing was written to WEDNESDAY (`git status` showed nothing new). Every later run invoked `node <clone>/node_modules/vitest/vitest.mjs --root <clone>/…` directly.
- **KS-1682:** NOT made worse. `exchangeAuthCode`'s refresh-token-from-shared-cache block is untouched; the only change is the verifier pass-through.

## Ruling input on the author's four beyond-plan items

1. **Binding in the consume key:** RIGHT, and race-safe on the real engine.
   - Real PG 18.3, 16 connections, 50 rounds: always exactly 1 winner.
   - Lock-ordered race: T2 blocks while T1's DELETE is open, and gets 0 rows after T1 commits.
   - Wrong and right bindings racing: only "right" ever wins.
   - A wrong binding first, then the right one: 0 rows then 1 row (no burn).
   - **Control:** non-atomic SELECT-then-DELETE gives 16 winners in all 50 rounds.
   - Accept.
2. **Third suite (memory branch):** worth keeping. It kills BG-M9 (the memory consume ignores the binding) via M-R3. Its gap is N1, which sits on the DB branch's fallback, not the memory branch.
3. **R16 (init refuses a token naming no user):** accept. It costs nothing for real tokens, and the state needs an initiator. (I did not re-mutate it; the author's X8b covers it.)
4. **No tenant_id / no RLS:** SAFE as built.
   - No code path reads the table except the consume, keyed by two 256-bit hashes.
   - Rows hold only hashes, an encrypted verifier and ids.
   - RLS in this repo is enabled per named table (009/012/013/039), so the table is reachable by the app role as `svc_m365_connections` is.
   - The organisation compare is pinned, but by ONE cell: BG-M1 (drop the compare) is killed by G1 only.
   - Accept, with G1 treated as load-bearing.

## FOUND / TESTED / HOW

**Setup**
- Clone: `git clone --shared` of the spark cache into `scratchpad/gate_bg1/repo`. The cache lacked the head, so I fetched the BRANCH ref and develop from GitHub, read-only, with the project's deploy key.
- Heads by ls-remote, at start and again before the verdict:
  - Branch = refs/pull/1647/head = `f9f42558…`.
  - Develop = `937c7d10…`.
  - Head tree = `merge-tree --write-tree` = `7aa017b8…`.
  - 17 files, +968/-234, matching the author's list.
- Develop baseline in a worktree that shares node_modules.
- Install: `npm ci --prefix <clone>/Blockchain/Dev` scoped to the workspaces (the full packages/* and services/* set for the spec check), `--ignore-scripts`. `packages/shared` built first.

**Q1 (attacker holding a leaked state)**
- The author's 23 route cells: all pass.
- My four cells (`gatebg1-route.test.ts`, appended to a copy of the route harness, scratch only): all pass at head, and all four red on develop.
  - X1: byte-identical refusals across seven kinds, 0 exchanges, and a success as a positive control.
  - X2: 5 concurrent right-cookie callbacks give exactly 1 exchange.
  - X3: no state, binding, verifier, code or state-hash on ANY of console.log/warn/error/info, process.stdout or process.stderr, across init, success, refusal and a failed exchange. Positive control: the capture sees the connection id.
  - X4: binding is independent of the state and the verifier.
- Expired: the clock was moved (`Date.now` spy, +10 min +1 ms), not waited out.
- Real-engine race: see ruling 1.
- Memory-branch race: the author's M-R4, run green.

**Q2 (PKCE)**
- R9 and R11 are green.
- BG-M6 (plain challenge labelled S256) is killed by R11.
- BG-M10 (no verifier) is killed by R11.
- BG-M7 and BG-M11b survive (B2).

**Q3 (retired route)**
- Census across the whole repo with `git grep -i` for `connections/complete|M365CompleteConnectionRequest|completeConnection`.
  - On develop (positive control): the index.ts route, the schema, both spec copies and the schemathesis files.
  - On head: only the tests (R10, KS-1673 A6), SETUP.md and the schemathesis baseline/data (N4, N6).
- No other route exchanges a raw code: `exchangeAuthCode` has one caller, the callback.

**Q4 (schema copies)**
- My own census (whole repo, case-insensitive `create table … svc_m365_connections`):
  - 5 creators: deployment/azure/migrate/init.sql, docker/init/04, docker/init/06, migrations/002, gateway startup-migrations.ts.
  - Creators of `svc_m365_oauth_states`: the same four live copies + 053 (+ the test file).
  - **Control:** the same grep for `svc_teams_webhooks` finds its known two creators + its test.
- The column sets are identical by inspection: the 06, gateway and 053 DDL is byte-equal, and the author's P2 is green.
- 053 on **real PostgreSQL 18.3** (Homebrew, throwaway cluster on 127.0.0.1:55432 in scratch, stopped after): first run CREATE TABLE/INDEX rc 0, second run "already exists, skipping" rc 0. **Idempotent.** `\d` shows 8 columns as intended.

**Q5 (logs)**
- Read every log call in the diff:
  - The refusal logs `{reason, connectionId}`.
  - init logs `{connectionId, organizationId}`.
  - The store logs `err.message` only.
  - `requestLogger` logs `req.path` (no query).
- X3 above measured it, and R13 is green.

**Q6 (existing cells not weakened)**
- m365 by cell name: develop 15 files / 148 / 0 failed; head 18 / 194 / 0. Vanished: exactly one (E10's rename). New: 47.
- **KS-1671:** BG-M12 (stringParam passes everything) is killed by K1-K4 and Q1-Q5, so K3/K4 are not vacuous. BG-M8 shows K5 reaches the exchange.
- **KS-1641:** BG-M13 (uncapped reflection) is killed by E1/E2/E5/E8.
- **tsc:** rc 0 for m365 and api-gateway. **Control:** a planted TS2322 in oauthState.ts gives rc 2, restored.
- **Gateway startup-migrations:** 7 files, 38/38 on head and on develop, cell names identical.

**Q7 (mutants)**
- 13 compile-safe mutants (BG-M1…M13), each type-checked (rc 0) before running, and each restored. `git status` on the clone was clean after every one. Not counted: BG-M11 (non-compiling, TS6133).
- Killed by the author's suites:
  - M1 (G1)
  - M2 (R5)
  - M6, M10 (R11)
  - M8, consume AFTER the exchange (13 cells)
  - M9 (M-R3)
  - M12, M13
- Survived the author's suites:
  - **M3, M4, M5, M7, M11b.**
  - My cells kill M3 (X4) and M5 (X1).
  - Nothing kills M4, M7 or M11b.

**Q8 (spec)**
- `npm run --prefix <clone>/Blockchain/Dev check:openapi`: rc 0 ("CHECK PASS: on-disk YAML matches generated"; check-spec-examples OK, 412 blocks).
- **Control:** one character changed in the on-disk YAML gives "CHECK FAIL: generated YAML differs", rc 1, restored.

## NOT RUN

- Preflight legs 3 (spec-auth conformance), 4 (path resolvability) and 8 (served-spec consistency). All three need a gateway on :6882, and there was no stack (no Docker).
  - By reading: the PR only removes one bearer-authed op and edits the callback's description. Leg 4 cannot gain an unroutable path from a removal. Legs 3 and 8 still need a stack to be measured.
- No real Microsoft sign-in, and no token POST to Microsoft. All exchanges were mocks.
- No browser end-to-end on the Azure topology. B1 rests on the cookie-jar model plus the bicep/env/nginx/frontend source, not on a live Azure run.
- The whole of docker/init/04, docker/init/06, azure init.sql and the full CORE_MIGRATIONS were not applied on real PG. Only 053 (twice) and the exact store statements were.
- Not run: the migrations runner/image, the four platform suites, the deploy.
- The PR body's 14-mutant table was not read (no GitHub API reads), so "not tried by the author" is judged from the READY text and the suites, not the table.
- Constant-time compare: not mutated. A timing-only mutant (`===` for `timingSafeEqual`) cannot be killed by a functional cell, and I did not build a timing harness.

## Wall-clock

20:40Z -> 20:58Z (2026-10-19 UTC; 07:40 -> 07:58 AEDT 2026-10-20). Heads re-read at 20:58Z: unchanged. `git -C /Volumes/DevMASTER/WEDNESDAY status --short`: no untracked paths outside 0_Brain/, 5_Project_History/, 2_Project_Files/local-model/ and 2_Project_Files/fleet/briefs_staged/.
1634ffa2082e33a79c495f2f6bcaaebbbb53814a6ab41e03fc19d4fdca717190
