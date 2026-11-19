PR 2264: GO WITH NOTES (at head e4faf23efe05d7e594521e75cb700e9295f9d99e; tier 1)

# Gate 387, tier 1 (Opus), PR 2264 (KS-2277), 2026-11-20 ~09:26-09:45 AEDT

## Pins
- **gh api, twice:** at 09:26:57 (before the first measurement) and at 09:44:06 (before this file). Both reads gave the same values:
  - open, not merged, not draft;
  - head e4faf23efe05, base b75d89b3f29d, develop b75d89b3f29d;
  - 1 commit, 20 files, +591 -26, updated_at 2026-11-19T22:24:51Z.
- **The merged state is the PR head.** The head's only parent is b75d89b3f29d, which is develop's tip, so merging would be a fast-forward. Every "merged" figure below was measured on the head.
- **Closing keywords:** 0 in the PR body and 0 in the commit. "KS-2277" appears in the body, and the commit subject starts "Refs KS-2277:".
- **The PR body at source** (9,720 bytes, sha256 bc40d0350b15…) is byte-identical to the builder's drafts/pr_body_final.md.
- **Files the PR leaves alone:** `git diff develop..head` touches 0 lines of verification.ts, anchorStateSync.ts, tenant-guc.ts and db.ts. Control: verificationV2.ts shows +65 -26.
- **Develop between 718b15bb and b75d89b3:** 5 paths changed (auth issuerCertSweep and timestamping), none in originate or packages.

## How I measured
- **Clone.** My own clone `_work/g`, made from the GitHub URL with `--reference-if-able` pointing at the shared checkout and `--dissociate` (no alternates file is left).
  - Into my clone only, I fetched develop and refs/pull/2264/head.
  - Worktrees: `h` (the head, which is also the merged state), `d` (develop b75d89b3), `x` (mutants) and `p` (probes).
- **node_modules.** APFS-cloned (`cp -c`) from gate 386's own `_work/h` (a finished gate folder; no seat tree was touched). That source had 0 absolute links, and each of my trees has 0 absolute links (112 relative links each).
  - packages/shared/dist was built by me with tsc in every tree (rc 0).
- **Run conditions:** Node v26.8.1, jest 29 (originate's own config, cwd = originate), TMPDIR /private/tmp/g387t. load1 ran 5 to 17; the 17 was during my own whole-suite run.
- **Scripts:**
  - `_work/run_cwd_g387.py` sets the cwd, so no `cd` is needed;
  - `_work/suites_g387.sh`;
  - `_work/mutants_g387.py` (exact-count edits, restore, sha256 check);
  - `_work/probes/make_probe.py` with `probe_cells.ts`, which build a probe file from the PR's own harness plus a per-request ledger tag;
  - `_work/eslint_g387.mjs`.
- **Evidence:** `_work/evidence/`.
- **End state:**
  - h, d, x and p each show 0 porcelain lines.
  - verificationV2.ts in x after the mutants: sha256 963b9077cf20…, the same as h.
  - The planted files and the probe file are in `_work/_quarantine/{planted,probes,red_first}/`.

## Q1. Does the PR meet every clause of THE SPEC? YES (read at source, then measured)
| clause | where (head) | measured by |
|---|---|---|
| (1) v2 only; v1 unchanged | verification.ts diff empty; only verificationV2.ts changed | probes P1 and P2: v1 statements carry 0 bypass GUCs (control: v2 carries them); v1 does not name the other tenant's row |
| (2) every caller of the 3 entry points sees every tenant | `readAcrossTenants` at 402, 419 and 495; no caller test | probe P3: 8 caller shapes × MULTI off and on give counts hash 3, file 3, documentId 1 for every caller |
| (3) ONE helper = runWithPlatformScope around: row set + originals (S1/S2) | 300-302, 402 (`localRowsByHash` calls `readOriginalRows` inside it) | M1 is killed |
| (3) the evidence reads | 419 | M2 is killed |
| (3) the 2 documentId lookups + that row's evidence | 495-513 (one scoped block) | M9 is killed |
| (3) OUTSIDE: registry loop, chain fetch, eligibility, sort, buildMatch, heal | 403, 415, 426-433 | read at source; M5r, M7b and G6 are killed (heal under the scope); see G387-2264-1 for verify-file |
| (4) guard 1: the heal never runs under the scope | 431 runs after the awaited scoped calls return | P1, P2 and P3: every heal call has platformScope false |
| (4) guard 2: a foreign row reaches the heal only as `{...row, _tenantId: row.tenant_id}` | `rowForHeal` 310-314 | P3: in 16 runs no foreign row reached the heal with write true; M7, G1 and G4 are killed |
| (4) verification.ts unchanged | diff empty | – |
| (5) the public answer holds no person-derived value | buildMatch unchanged | probe P4 (Q4 below): 0 hits |

**A remark on clause (3).** The spec scopes "the evidence reads for rows WITHOUT `_tenantId`". The code wraps all of `resolveTrustedCertificationEvidence`, so registry rows (which carry `_tenantId`) also start inside the scope.
- This is safe. Their read goes through `runWithTenantId(tenant, …)`, which calls `scopeStorage.run({ tenantId })`. That REPLACES the store (tenant-guc.ts 93-98), so those reads run under their own tenant's GUC, not the bypass.
- The tenant is non-empty: it is the registry's tenant_id. An empty tenant would fall through to `fn()` under the bypass.
- I count this as compliant.

## Q2. The write path: ZERO writes inside the scope, and the heal can never write a foreign row
**Every statement reachable inside `readAcrossTenants`, read at source:**
- `localRowsByHash`: 1 `$queryRaw` SELECT.
- `readOriginalRows`: 1 SELECT.
- `resolveTrustedCertificationEvidence`, through `readForRow`:
  - `fetchParentHash`: SELECT;
  - `fetchCertificationRow`: SELECT;
  - for `_tenantId` rows, `queryWithTenantGuc`: BEGIN / set_config / SELECT / COMMIT.
- The documentId block: 2 SELECTs plus the evidence reads above.
- Logger calls.

**The wrapper's own statements:** under the scope, the GUC proxy issues one `SELECT set_config(...)` per statement inside a Prisma `$transaction` (db.ts 186-200).

**Ledger checks:**
- C10 checks that every statement under the bypass is a SELECT. Positive control: M1 and M2 make C10 fail.
- My probe ledger shows `bypassWrites 0` in all 16 P3 runs.
- A grep of verificationV2.ts finds no `$executeRaw`, UPDATE, INSERT, `.create(` or `writeAnchorBlobIf`. The only `.update(` hit is the crypto hash on line 555. Control: the same pattern hits verification.ts 6 times.

**The only write reachable from v2** is healVerifyRow → healAnchorForVerify → writeAnchorBlobIf (anchorStateSync.ts 596). It is gated twice:
- `if (!anchorId || !input.authHeader) return blob;` (line 569, quoted in the PR body). v2 passes `''` as the bearer at line 431, its only call.
- `if (input.write && input.tenantId)` (line 594).

So today v2 writes nothing. The PR adds two further guards on top of that.

**Probe P3:** /verify by hash, /verify-file and /verify by documentId, on 8 caller shapes, MULTI off and on, plus a planted tenant-less row.
- The caller shapes:
  - anonymous;
  - vouched tenant B (signed in);
  - vouched with A's id in upper case;
  - vouched with a leading space;
  - vouched with a malformed id;
  - unvouched with a forged B;
  - `req.tenantId` attached = B (the MULTI `extractTenantContext` arm);
  - attached B in upper case.
- In every run:
  - the heal is never under the scope;
  - no heal call carries a bearer;
  - the documentId path makes no heal call;
  - the tenant-less row and every row of a tenant other than the resolved one get write false.
- A row gets write true only when its tenant_id equals the RESOLVED request tenant exactly. That covers B's own row for a vouched B caller, and for an attached-B caller.

**Is "own" = `String(row.tenant_id) === req.tenantId` exact safe?** Yes, and it fails safe:
- Case, whitespace, a malformed id, or an empty or absent tenant make the row "not own", so it gets write false. That costs at most an own-row heal, which v2 cannot perform anyway (no bearer).
- A null tenant_id becomes `''` (not own) and gets `_tenantId: 'other-tenant'`, which is truthy, so write is false.
- `resolveRequestTenantId` always returns a non-empty string (the default tenant as a last resort), so the "absent" arm is unreachable in production.
- **The MULTI case.** With MULTI on, a caller who gets a raw `x-tenant-id` = B past the provenance strip makes B's rows "own" (write true). That is the KS-1032 trust model as it stands before this PR (requestTenant.ts 13-25), not something this PR introduces. Even then, no bearer reaches the heal, so nothing is written.

## Q3. Mutants (reproduced myself on x; 16 files = the new file + the 15 unit v2 files, 260 cells)
| mutant | failing cells |
|---|---|
| BASE | 260/260 pass |
| M1 no scope on S1 | C1×2, C3, C4, C5, C8, C9-signed-in, C10 |
| M2 no scope on S3/S4 | C3, C10 |
| M4 owner id in the match | C5 + 6 cells of ks590p |
| M5r router-wide scope on v2 | C8 |
| M7 heal gets the original row (my first edit failed to compile, TS6133; re-run with `void` references) | C2, C8, C9-signed-in |
| M7b heal inside the scope | C8 |
| M9 documentId block unscoped | C9 ext, C9 pkey |
| G1 copy's `_tenantId` falsy | C2, C8, C9-signed-in |
| G4 every row "own" | C2, C8, C9-signed-in |
| G6 the hash route's whole `matchesForHash` inside the scope | C8 |
| G7 bearer forwarded to the heal | ks1129 V2-NO-WRITE, ks1661 C2 and H2 (old cells) |
| G9 heal skipped for foreign rows | C2, C8, C9 |
| **G5 the verify-file handler's `matchesForHash` inside the scope (heal under the bypass on /verify-file)** | **none: SURVIVES 260/260** (G387-2264-1) |
| **G8 evidence for registry rows routed through the request db under the bypass (`_tenantId` stripped)** | **none: SURVIVES** (G387-2264-1) |
| G2 "own" when the request tenant is missing | none: survives. Unreachable: the request tenant is always set |
| G3 "own" compared case-insensitively and trimmed | none: survives. Benign, the same result for canonical ids |

**Red first:** the PR's cell file copied onto develop d (product untouched) gives 10 failed and 4 passed. The 4 that pass are C2, C6, C7×2, exactly as claimed. Each of the builder's named mutants I re-ran (M1, M2, M4, M5r, M7, M7b, M9) fails the cells the builder names.

**Concurrency and leakage (probe P1/P2, a ledger tagged per request by my own AsyncLocalStorage):**
- **P1, overlap.** The v2 anonymous request was stalled 150 ms inside its scoped read while these ran: a v1 anonymous request, a v2 request from a tenant-B caller, and a v1 request from a tenant-B caller.
  - v1 anonymous: 2 statements, 0 under the bypass.
  - v1 tenant B: 2 statements, both under B's GUC, 0 under the bypass.
  - Each v2 request: its row-set read was under the bypass (positive control).
  - All 6 heal calls: platformScope false.
  - 0 unattributed statements.
- **P2, keep-alive** (one socket, in order: v2, v1, v2, v1, verify-file, v1):
  - every request enters with `isPlatformScope()` false;
  - the 6 v1 statements carry 0 bypass GUCs.
- So the scope does not survive the response, and no concurrent request inherits it.

## Q4. Person-derived values for a FOREIGN tenant's row: NONE in any of the three answers (planted, measured)
**What I planted** on a third tenant's row (markers built at runtime):
- owner_user_id, tenant_id, issuer_organization_id and issuer_user_id;
- the org slug;
- `metadata.{issuerName (an email), ownerEmail, userId, createdBy, uploaderEmail}`;
- `certification_metadata.{issuerName (a local part), issuerId, holderId, userEmail}`.

**Answers read:** /verify by hash, /verify-file, /verify by documentId (external id), by documentId (pkey), and hash + documentId together.

**Result:**
- 0 hits in all 5 for every marker, for '@', and for B's planted user, tenant, org, slug and person values (case-insensitive).
- Control: every answer contains the foreign row's documentId and its company name "Gamma Pty Ltd".
- The match keys are exactly: blockchain, certifiedAt, checks, contentHash, createdAt, documentId, documentType, documentUuid, issuer, status, title.
- **Two residuals I confirmed:**
  - F6, stated in the PR: a person name typed into `metadata.issuedBy` with no org is presented.
  - The stored `blockchain` blob is presented verbatim (G387-2264-3).

## Q5. Suites, static checks, the overrides, ks1557
- **originate suite, whole:** d 2,868/2,868 in 234 files; merged (h) 2,882/2,882 in 235. 0 failed on both sides, so the failure-name sets are equal (both empty).
- **The 16 overrides were needed.** With all 16 lines removed on the head, the whole suite gives 2,771/2,882: 111 failures in exactly the 15 files named, and no other file goes red.
- **Each override is +1 -0** (numstat), with no assertion touched. In each file the added line is the ONLY mention of any platform-scope symbol. So no cell asserts on the scope, and the pass-through cannot weaken an assertion. Each file still tests what its name says. M4 and G7 show the old cells still fire on their own subjects.
- **tsc --noEmit (originate):** rc 0 on d and on h. Planted control: TS2322, rc 2.
- **eslint:**
  - all 18 changed .ts files: 0 errors, 0 warnings;
  - all of originate/src: 29 messages on d and on h, the same set, 0 new;
  - planted control: no-debugger error plus a no-unused-vars warning.
- **Test-types ratchet (check.cjs) on h:**
  - originate: 329 files, 268 tests, 0 errors, 0 new, 0 stale;
  - auth: 41 errors, all baselined;
  - api-gateway: 15 errors, all baselined;
  - vc-issuer, security and m365: 0 errors each;
  - planted originate test: rc 1, "1 new" TS2322.
- **docs-fragments check:** OK on h (301 new, against d's 300). The same 2 ADVISORY lines appear on both. Each fragment has 1 `<h2>`.
- **ks1557: the builder's call is right.**
  - Line 45 passes `{ ...jest.requireActual('@secuura/shared'), … }` as overrides to makeSharedMock.
  - makeSharedMock applies overrides last (`{ ...base, ...overrides }`, helpers/sharedModuleMock.ts), so its runWithPlatformScope is the REAL one.
  - A pass-through line there would make the cell less faithful.
  - It loads the v2 router at line 124.
  - ks1364 imports the real module with no shared mock, and it is green on h.

## Q6. The PR body and the KS-2277 comment
**PR body:** every factual sentence I could measure holds:
- the scope sites;
- outside-the-scope;
- line 569;
- 20 paths, +591 -26;
- 10/4 red first;
- 111 tests in 15 files;
- ks1557;
- the mutant cells I re-ran;
- 2,868 and 2,882;
- tsc 0, eslint 29/0 new, ratchet 0 new / 329;
- docs-fragments OK;
- `git diff --stat f8c15a52..b75d89b3 -- services/originate packages` empty (control: the whole diff is 3 files).

One loose sentence: G387-2264-4.

**Builder-only, NOT re-measured:**
- the PGlite RLS run;
- the pre-push hook (13/16 legs, 868 s);
- `preflight_test_types_ratchet_leg.test.sh` 48/0;
- M3, M4b, M5, M6 and M8 (I did not rebuild those five).

**KS-2277 comment 5aa86200: NOT read at source.** The Secuura Linear key lives only in the Blockchain project's `.env`, which that project forbids a session to read. Wednesday's own LINEAR_API_KEY answers "Entity not found" for KS-2277. I checked only the builder's draft (drafts/linear_comment.txt). Every factual sentence in it matches my measurements. Whether the posted text equals the draft is UNMEASURED.

## Findings
- **G387-2264-1 (LOW, test coverage; not merge-blocking).** Guard 1 (the heal never runs under the scope) is pinned only on /verify by hash.
  - **G5:** wrapping /verify-file's `matchesForHash` in `readAcrossTenants` runs the heal under the bypass, and all 260 cells stay green. C8 drives only /verify, and C1 checks only counts on /verify-file.
  - **G8:** routing registry rows' evidence through the request db under the bypass survives too. This is a read only, and its SQL pins tenant_id.
  - Neither mutant can write today: guard 2 still sends write false for foreign rows, and v2 forwards no bearer.
  - Suggested follow-up (Wednesday's call): repeat C8's heal assertions on /verify-file.
- **G387-2264-2 (LOW, docs).** The cheat fragment's "Checking it" line `npm --prefix Blockchain/Dev run check:test-types   # originate is gated` is false.
  - That npm script (package.json) runs auth, api-gateway, vc-issuer, security and m365-integration only, and NOT originate.
  - originate is gated by preflight leg 16 (`scripts/preflight/test-types-ratchet.sh` 53-54) or by `node scripts/typecheck-tests/check.cjs services/originate`.
- **G387-2264-3 (INFO, existing behaviour now across tenants).** `presentBlockchainHonestly` returns a non-simulated `blockchain` blob verbatim, so any key stored in it is presented. Probe P4: a planted `plantedOwner` user id inside it was presented.
  - The known writers (documentRepo seed, certifications.ts 601, documents.ts 905, confirmedBlobOf) store anchor and contract fields only, with no person-derived key.
  - The rule holds today on what is written. This PR widens the population to every tenant, not the filter.
- **G387-2264-4 (INFO, PR body precision).** "the one-line pass-through the 21 admin and GDPR cell files already carry": on develop, 21 originate test files MENTION runWithPlatformScope, but 18 carry an override key, and several are seed or log tests, not admin or GDPR. This does not affect the change.
- **G387-2264-5 (INFO, spec shape, compliant).** The evidence scope also covers `_tenantId` rows. They nest `runWithTenantId`, which replaces the store, so they read under their own tenant's GUC (Q1 remark).

## Not run / not measured
- Node 24, any live stack, container, database server or box. PGlite was not run (the builder's outside-the-suite run stands as the builder's).
- The two integration files.
- The four platform suites.
- The pre-push hook.
- Kintsugi or demo.
- The KS-2277 comment at source.

Nothing was written to GitHub, Linear or any !CODING path. No mail was sent, nothing was launched, no process was killed, and no sub-agents were used.
