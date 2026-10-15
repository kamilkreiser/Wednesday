VERDICT: PR #1555 (KS-1114) head c85cc28d0232e5641901bfd12ca6960a9711e783: NO GO (round 1 of 2). One MAJOR needs a ruling: the title answer gives away far more than whether the document exists. Apart from that the code does what it claims, measured.
SHA256/16: 66116dda9da0a126

# Gate: PR #1555, KS-1114 anonymous title lookup in one tenant (Opus tier 1, FULL)

Commissioned by Wednesday, 2026-10-15. This gate reports findings only and fixed nothing. All work ran in `/private/tmp/claude-501/gate1555-1792045119/` (my own clone, `--shared` from the checkout, fetched from origin there). In `!CODING` I used only `ls-remote`. Nothing was pushed, written or deleted. Evidence is in `evidence/` (scripts in `evidence/scripts/`, outputs in `evidence/runs/`).

## Heads (re-read by me)
- `refs/pull/1555/head` = `c85cc28d0232e5641901bfd12ca6960a9711e783` (matches the brief). The base is develop `53b429ed6b4bf4d23c0721bf573b9df1c858bc06`, which is the merge-base.
- **Live develop has moved to `0bb4f17ca5010baa3ad9d91b790522e87b8c9dc1`.** That is three commits since the base: #1549 `8cbadd8d4`, #1554 `18de4b7ce`, #1552 `0bb4f17ca`. See `runs/lsremote.txt` and `runs/merged_tests.txt`.

## Severity summary
| # | Sev | What | Where |
|---|---|---|---|
| F1 | **MAJOR** | A title hit returns the full documentId answer: `contentHash`, external `documentId`, `issuer`, `status`, the `certification` block, `lineage[]` (ancestors' ids, dbIds and hashes) and `newerVersions[]` (descendants' ids, dbIds and hashes). That is more than existence. The `contentHash` turns a guessed title into a full `verified:true, integrityVerified:true` answer through `{hash}`. Kam's option (b) on the card read: *"A stranger can still learn whether a given title exists, even if the reply hides the details."* The reply does not hide the details. | `services/originate/src/routes/verification.ts:1456-1459` calls `respondExistenceOnly` (`:1021-1093`; `contentHash` `:1066`, `issuer` `:1067`, `lineage` `:1079`, `newerVersions` `:1086`). Spec text "EXISTENCE answer" is at `originate.openapi.ts:555-556`. The shape was Wednesday's ruling inside Kam's, per the test header at `ks1114-…integration.test.ts:11`. |
| F2 | MINOR | Drafts and revoked documents can be found by title (`status:"draft"` plus their `contentHash`). Nothing filters by status, so a document that was never certified becomes discoverable by guessing its title. This is part of the F1 ruling. | `verification.ts:1444-1455` (no status predicate) |
| F3 | LOW | The spec says "the default tenant for an anonymous caller". That is false under `MULTI_TENANCY_ENABLED=true` with `NODE_ENV=production`: every anonymous verify answers 400 `Missing tenant context`. This predates the PR and affects every strategy. | `originate.openapi.ts:2008`, `packages/shared/src/db/tenant-context.ts:68` |
| F4 | LOW (test only) | The T9 golden is not hermetic. **(a)** It assumes the DB TimeZone is UTC: it measured red with the server on Australia/Sydney (`certifiedAt` shifted by +11h) and green under UTC. **(b)** It goes red when any other row shares its guessable fixture hashes (`'a1'.repeat(32)`): my own probe seed collided and T9 went red, then green once my rows were re-hashed. | `ks1114-…integration.test.ts:63,66`; `runs/it_h_st_super.log`, `runs/clean_m_dbg.log` vs `clean_m_dbg2.log` |
| F5 | LOW | The `!tenantForTitle` guard is dead code. `resolveRequestTenantId` always returns a value, so my mutant o3 survives. Harmless, but the comment implies a reachable branch. | `verification.ts:1442` |
| F6 | INFO | The author's mutation count is off by one. The PR table has 13 rows: 10 killed, 3 survived. The text says "11 killed". | author's PR body |
| F7 | INFO | `{contentHash:"", title}` and `{documentId:"", title}` now reach the title strategy; on develop they got 400. This is consistent with "empty means absent". | probe P11d/P11e |
| F8 | INFO | A vouched upper-case `x-tenant-id` finds nothing: the SQL predicate is lower-cased, but the RLS GUC is set from the raw value. This fails closed and predates the PR. | probe P16b |

## FOUND / TESTED / HOW

**1. Hunks.**
- verification.ts, behaviour: `title` is destructured; `titleToFind` counts only when `trim().length>0`; the 400 text adds "or a title"; `respondExistenceOnly` is hoisted out of strategy 2 verbatim (the byte-identity of the documentId answer is proven by T9); strategy 3 is new.
- originate.openapi.ts, spec: field and request descriptions, the corrected precedence text, the 400 text.
- yaml: generated. `generate-openapi --check` at head PASS, and `check-spec-examples` OK. **Control:** a one-word change planted in `KS1114_TITLE_SEMANTICS` gives `CHECK FAIL` with rc=1; the file was restored with an empty diff. On the predicted merge with live develop, `--check` also PASSES.
- ks1103 test: cell E3 inverted (400 becomes 200, no integrity claim); MSG_MISSING widened.
- Two new test files and one fixture (the golden).

**2. Does it do exactly (b)?** Probed on the REAL originate app (`src/index.ts` booted with tsx, with the real provenance middleware and `GATEWAY_VOUCH_SECRET` set). Postgres 18 is my own, on port 55731, schema from `docker/init` plus `migrations`, `secuura_app` role with `NOBYPASSRLS`, and `documents` under FORCE RLS. Every reply body is in `runs/probe_h_st_final.json`, with `probe_h_mt.json` and `probe_h_mt_prod.json` alongside.
- Anonymous hit in the default tenant: 200, with the full body (F1).
- A title that exists only in tenant B: 200, not found, **byte-identical** to a missing title. Also identical are the erasure sentinel `[erased]`, `[erased] ` and `[ERASED]`. All four not-found bodies share one body (timing run, `distinct_bodies` 1 each, `identical:true`).
- Empty, whitespace, `\t\n` and NBSP-only titles: 400, which now names title.
- `%`, `100% off__`, a bare `%`, `' OR '1'='1` and `…' OR title <> '`: not found. The exact titles with `%_` and with quote/backslash: found. So there is no LIKE semantics and no injection.
- Titles of 500 characters hit; 501 characters and 100k characters miss with a 200 and no error leak. NFC hits, NFD misses. A NUL is refused with 400.
- Precedence: documentId+title gives the documentId's document; unknown documentId+title gives the documentId not-found, with no fall-through to title; hash+title, unknown hash+title and documentData+title all take the hash strategy.
- Shared title: the newest in the caller's tenant wins (the default tenant's older row for an anonymous caller; B's row for a vouched B caller).
- Both tenancy modes: single-tenant and MT-dev give identical bodies on all 47 probes, with verifiedAt normalised. **Control:** the same comparator shows 41 of 47 differing for MT-prod.
- Develop app against head app: 39 of 47 probes differ (the title bodies), 8 identical (the non-title bodies).
- The T9 golden **re-recorded by me on develop 53b429ed** equals the PR's fixture byte for byte. Control: the head's cells run on develop give 10 red and T8+T9 green.

**3. Leaks beyond existence.** The body is F1. Headers: helmet, CORS, `Content-Length` and a weak `ETag`; none of them is data-bearing beyond the body.
- **Escalation chain, measured** (`runs/chain_h_st_final.txt`): title gives `contentHash`; `{hash}` then gives `verified:true, integrityVerified:true`, issuer "Acme Private Issuer Pty". `newerVersions[0].contentHash` (a document never guessed) gives `verified:true`, and its id gives its title.
- **Timing** (`runs/timing_h_st_summary.json`), 400 interleaved samples per class after 20 warm-ups:
  - absent vs other-tenant: medians 0.574 / 0.572 ms, Mann-Whitney p=0.72, so indistinguishable.
  - absent vs absent2: p=0.41.
  - Controls that fire: hit 2.00 ms (p≈1e-132), and the sentinel 0.18 ms, since it short-circuits before the query (p≈1e-132). The sentinel difference depends only on the input, not on stored data: INFO.

**4. Mutants at head** (`runs/mutants_r2.txt`, `runs/mutants2.txt`). The clean baseline is 12/12 under both roles, and the worktree was clean afterwards.
- Author's mutants:
  - m1 (app role, FORCE RLS) SURVIVES in both MT=false and MT=true; m1 (superuser) is KILLED by T2 and T3.
  - m2 KILLED by T2b, m3 by T4, m4 by T4b, m5 by T5, m7 by T6, m8 by T7, m9 by T1, T2b and T9, m10 by T3.
  - m6a and m6b each SURVIVE alone, and both removed together (m6c′, compile-valid) is KILLED by T6. m6c exactly as written in the author's tool is a TS6133 compile break, which I recorded as a LOAD FAILURE and did not score; the author disclosed and re-ran the same.
  - **"Survives by design" is honest:** m1 survives only where RLS is the first line, and m6a/m6b are two-line defence in depth with the pair pinned.
- My own:
  - o1 (title wins over documentId): KILLED by T8 and T9.
  - o2 (title matched trimmed): KILLED by T5.
  - o3 (null-tenant guard dropped): SURVIVES; this is F5.
  - o4 (existence-only body with no hash, issuer or lineage): KILLED only because T1/T2b/T4/T4b assert `documentId` and `title`. **No cell pins whether `contentHash`, `issuer` or lineage appear on a title hit.**
  - o5 (no tenant predicate, superuser, MT=true): KILLED by T2 and T3.
  - o6 (sentinel lines and tenant predicate all removed): KILLED by T2, T3 and T6.
- Comment-only control: SURVIVES (0 red).

**5. Caller tenant for an anonymous caller.** `callerTenantOf` (`verification.ts:351-357`) returns `req.user.tenantId`, else `req.tenantId`, lower-cased. `req.user` is never set on `/api/verification` (the connector promotion is scoped to `/api/metering`, metering.ts:80). `req.tenantId` comes from `resolveRequestTenantId` (`utils/requestTenant.ts`): attached, else the header (only when vouched), else DEFAULT.
- Single-tenant: unvouched always gives DEFAULT.
- MT: `extractTenantContext` reads the raw `x-tenant-id`, but the provenance middleware has already stripped it (pattern `^x-(user|tenant|…)`) on an unvouched request. So DEFAULT in dev, and 400 in production.
- **No header, query parameter or body field chooses the tenant.** Measured: forged `x-tenant-id`, `x-tenant-override`, `x-tenant-slug`, a wrong vouch, forged `x-user-*`, `?tenant=` / `?tenantId=`, and `tenantId`/`tenant_id` in the body all give not-found for B's title. Only a request carrying the correct vouch secret reaches tenant B (P16).

**6. Merge.**
- `merge-tree` of the head onto live develop `0bb4f17c`: clean, tree `17365488a704…`. Overlap is 0: develop's three commits touch none of the PR's 7 files.
- **Control:** a planted develop-side edit of verification.ts:850 (the destructuring line) gives `CONFLICT`, rc=1.
- On the predicted merge commit `9cf95dc4` (built locally): verify integration 47/47 (MT=false app, MT=true super), originate unit 110/110 suites and 1373/1373 tests, check:openapi PASS.
- Cross-lane: #1552 (`762d044b0`) touches only preflight.sh and its test. #1554 (`3c15af569`) touches `api-gateway/src/routes/verification.ts` and its test. **Neither touches `secuura-api.yaml` or `originate.openapi.ts`.** Both are already merged into develop, so merge order does not matter.
- KS-1543 (R lane) is local commit `7b7d4032`, which is not on origin and not readable from my clone. Per Wednesday's daily note it is api-gateway only (ESLint and api-gateway suites). **Not measured** (see below).

**Author's claims, checked:**
- Originate unit 108/1342: **reproduced** (develop 107/1337).
- Verify integration 47/47: **reproduced** in MT=false/app and MT=true/super. In MT=true/app one ks1557 cell is red, and in MT=false/super five ks1119 cells and one ks1557 cell are red. **Those reds are identical on develop 53b429ed**, so they predate this PR (`runs/verifymatrix.txt`).
- ks1114 12/12 in all four role×mode combinations, with the platform DB set so MT really engages ("TenantPoolManager enabled=true").
- Note: without `PLATFORM_DATABASE_URL`, MT=true silently falls back to single-tenant (`ks1119…:164`). My first "MT" runs were exactly that, and were re-run.

## NOT tested
- The path through api-gateway: no gateway was booted. Gateway behaviour was read from source only (the inbound strip, optional auth, and the per-IP limiter at `api-gateway/src/index.ts:559`: 60/min in prod, 600 in non-prod).
- KS-1543's diff, which is not on origin.
- Timing was measured only on a small local table: a large tenant-B dataset, a title index, or network jitter were not measured. The full originate integration suite (other suites need DB fixtures and ports outside this gate's setup); only the three verify suites were run.
- No Docker and no remote box.

## For the ruling (F1/F2)
For Wednesday, and Kam if needed: is the title answer the documentId shape (current), or existence only (for example `documentExists` plus no `contentHash`, `issuer`, `certification` or lineage), as the card text Kam tapped implied? Does a title hit include drafts and revoked documents? Either way, a cell should pin the answer: no current cell distinguishes the two (mutant o4).
