# Secuura board screen for parallel build lanes, 2026-11-15 (Sonnet screener, read-only)

Source of every claim: Linear KS team read 2026-11-15 ~14:3x; GitHub open PRs read live (85, with file lists); code read at develop `48883ba5976b` through the GitHub contents API (the local checkout is at `0e6479d7b`, 2026-11-10, and does not contain that sha). Method and gaps in notes.md.

## 1. Board picture (KS, team key)
| State | Count | Instrument |
|---|---|---|
| Todo | **37** | `board_count.sh` (returned 37, limit 250, real count) |
| Backlog | **480** | NOT from board_count.sh: the script refuses (more than 250 rows, `MORE PAGES EXIST`; its linear path cannot page). My own paginated query (100/page to hasNextPage=false, filter state type unstarted/backlog/started). Treat as a measured count by a non-standard instrument. |
| In Progress | **252** | same as Backlog (script refused) |
| (other open: In Review 6, Blocked 3) | 9 | same paginated query, not in scope |

Open PRs: 85 (GitHub, `gh pr list --state open --limit 500`, got 85 < 500 so not capped). Two of them (575 dependabot dotenv, 649 dependabot pg) touch package.json/package-lock in about 20 services; I treat them as a lockfile-only collision, not a code collision.

## 2. Candidate tickets (no open PR names them in title, branch or body; newest comment read)
Model rows are from model-routing.md v1.0 (C2 = multi-file build, Sonnet 1st; C3 = auth/credential/security/money DESIGN, Opus 1st; C4 = data-destroying path, Opus 1st; gate G1 = tier 1 Opus, G2 = Sonnet). The Spark column is "not available" (retired today). P2/P3 gauge check was not run (unmeasured), so every row assumes below 80%.

| Key | Title (short) | State | Pri | Paths it will touch (grep-measured at 48883ba5976b) | Size | Row | Why agent-actionable |
|---|---|---|---|---|---|---|---|
| KS-1934 | Billing: checkout.session.completed credits without checking payment_status 'paid' | Todo | 3 | `services/billing/src/routes/webhooks.ts` (case at :374; no `'paid'` check in that file) + one new test in `billing/src/__tests__/` | S | C3 (money), gate G1 | Fix shape stated in ticket; code confirmed absent at the ref; no comments, no PR |
| KS-1935 | Billing: addCertificationCredits optimistic lock is not a compare-and-set | Todo | 2 | `billing/src/services/stripeService.ts` (:226 loop, :244 retry) + tests | M | C3 (money), gate G1 | Mechanism read in ticket and in code; sibling `useCertificationCredits` has the same loop (:254), same file |
| KS-1910 | Billing: GET /invoices/:id and DELETE /payment-methods/:id make one extra Stripe lookup on refusal | Backlog | 4 | `billing/src/routes/billing.ts` + tests | S | C2 | Side-channel fix inside one file |
| KS-1897 | Billing: checkout routes read req.user.stripeCustomerId which nothing sets | Backlog | 3 | `billing/src/routes/billing.ts` (:477, :521 confirmed); the fix may need the gateway to set it (unmeasured) | M | C3 | Possible hidden decision: flag, last in lane |
| KS-2185 | kyc: DELETE /api/kyc/user/:userId/data has no try/catch | Backlog | 3 | `services/kyc/src/index.ts` (handler at :1273) + test | S | C2 | One handler; fix shape is plain |
| KS-2192 | kyc: owner check's two surviving mutants need two test cells | Backlog | 4 | `kyc/src/__tests__/` only (test gap, code correct per gate 338) | S | C2, G2 | Tests only; PR 2214 merged 2026-11-12 so no overlap |
| KS-2189 | kyc: upper-case userId row is not erased by DELETE route or user.erased subscriber | Backlog | 3 | `kyc/src/index.ts` (dbDeleteUserData :374, fold helpers :1131-1139) + subscriber + tests | M | C4 (erasure), G1 | Mechanism measured in ticket; build is read-first |
| KS-2188 | kyc erasure cascade: one undecodable row stops the whole erasure | Backlog | 4 | `kyc/src/index.ts` (dbDeleteUserData) | M | C4, G1 | Same function as KS-2189: ordering matters |
| KS-1900 | vc-issuer: re-revoke overwrites first revokedAt/reason | Backlog | 4 | `vc-issuer/src/repositories/credentialRepo.ts` (revoke at ~:546) + test | S | C2, G1 | One function |
| KS-1899 | vc-issuer revoke() has no ownership check of its own | Backlog | 4 | same file + `routes/credentials.ts` caller | S | C2, G1 | Defence in depth, spelled out |
| KS-1684 | vc-issuer: creator refused GET after revoke on the memory fallback | Backlog | 4 | same file (`memoryStore.set` at :552 stores no owner entry) | S | C2 | Mechanism in ticket |
| KS-1993 | vc-issuer revoke: memory-only credential answers 503 forever | Backlog | 4 | same file | M | C2 | Same function family |
| KS-1994 | vc-issuer: GET by id / by-hash answer from memory on a thrown SELECT | Backlog | 4 | same file (`getRecordById`, `getReadableByHash`) | M | C2 | Same file |
| KS-2030 | systemTest: two governance suites use the register route as it worked before PR 1947 | Todo | 3 | `systemTest/schemathesis/tests/test_get_by_id_object_authorization.py` (:151-156) + the KS 1762 suite | S | C2, G2 | Tests are stale, product code right (ticket says read not run) |
| KS-1914 | Schemathesis KS 1042 isolation fixture fails once a tenant is archived | Backlog | 3 | `systemTest/schemathesis/tests/isolation_tenant_fixtures.py` (:39 single PATCH) | S | C2, G2 | One fixture |
| KS-2003 | Schemathesis seed-demo-users: helper passes a seed where all 14 inserts failed | Backlog | 4 | `systemTest/schemathesis/tests/support/demo_seed_gate.py` (`parse_seed_counts` :101) | S | C2, G2 | One helper |
| KS-2044 | Schemathesis baseline: two accepted rows describe fixed defects | Backlog | 4 | `systemTest/schemathesis/config/schemathesis-baseline.json`, `scripts/runner/baseline_gate.py` | S | C2, G2 | Hygiene; expiry 2026-12-31 |
| KS-1749 | Retire the Schemathesis unexpected-methods suppression Kam ruled released (2026-10-27) | Backlog | 3 | `systemTest/schemathesis/docs/known-issues-and-baseline.md` (KS-406 text :207-225), config, three places | M | C2, G2 | Kam's ruling is on the ticket |
| KS-1372 | api-gateway failed-login lockout is inert: retire it | Todo | 2 | `api-gateway/src/middleware/security.ts` (createBruteForceProtection :221), `api-gateway/src/index.ts` (:456, :461 use), `api-gateway/src/config/services.ts` (:63 bruteForce), `api-gateway/src/__tests__/security.test.ts` plus brute-force tests ks1461/ks1868/ks1961, the doc line (path unmeasured) | M | C3-adjacent (deleting dead auth code, Kam named "tier 1" gate) | Ruled by Kam 2026-11-10, card option a, "separate seat's build" |
| KS-1694 | m365-integration tests import @electric-sql/pglite which no workspace member declares | Todo | 3 | `m365-integration/package.json`, `api-gateway/package.json` (comment of 11-04: api-gateway imports it too) + lockfile | S | C2, G2 | Fix shape is declared in the ticket comment; lockfile collides trivially with dependabot 649/575 |

## 3. LANES (5; 4 solid, 1 optional). Pairwise disjoint by directory root, check run by script
| Lane | Tickets in order | Path globs (write set) | Model |
|---|---|---|---|
| **A Billing** | KS-1934, KS-1935, KS-1910, KS-1897 (last, flag: may need a decision) | `Blockchain/Dev/services/billing/src/**` | **Opus 5.5**, row C3 (money surface); Opus gate G1 |
| **C kyc** | KS-2185, KS-2192, KS-2189, KS-2188 | `Blockchain/Dev/services/kyc/src/**` (all four share `index.ts`: strictly serial) | **Opus 5.5**, row C4 for the last two (erasure). Sonnet may do the first two if Wednesday splits; one seat recommended |
| **D vc-issuer** | KS-1900, KS-1899, KS-1684, KS-1993, KS-1994 | `Blockchain/Dev/services/vc-issuer/src/repositories/**`, `vc-issuer/src/routes/credentials.ts`, new files in `vc-issuer/src/__tests__/`. NOT `routes/presentations.ts` or `vc-issuer.openapi.ts` (PR 2131 owns them) | **Sonnet 5.5**, row C2; tier 1 Opus gate on the PR (security surface, G1) |
| **E schemathesis** | KS-2030, KS-1914, KS-2003, KS-2044, KS-1749 | `systemTest/schemathesis/**` | **Sonnet 5.5**, row C2; gate G2 (Sonnet) |
| **F gateway edge (optional)** | KS-1372, KS-1694 | `api-gateway/src/middleware/security.ts`, `api-gateway/src/index.ts`, `api-gateway/src/config/services.ts`, `api-gateway/src/__tests__/*brute*`, `security.test.ts`, `api-gateway/package.json`, `m365-integration/package.json` | KS-1372 by Opus 5.5 if C3 is read literally (it deletes auth-edge code), Sonnet is defensible because Kam ruled the result; PR gets the tier 1 Opus gate either way. Wednesday decides |

Pairwise check (script `scratch` run in-session, prefix test over every pair, 10 pairs): A-C, A-D, A-E, A-F, C-D, C-E, C-F, D-E, D-F, E-F all **disjoint**.
Open-PR collision check (every file of all 85 open PRs against each lane glob): A 0 hits, C 0, E 0, D 3 hits (all in the two paths excluded above, so 0 after exclusion), F 8 hits: PR 2129 and 2080 on `m365-integration/src/index.ts` (not in our write set), PR 575/649 on the two package.json files (lockfile-only collision). Seat AA 6th (`services/anchoring/**`) and Seat B 176th (PRs 2098, 2089, 2079, 2220-2224: auth, frontend, packages/shared, api-gateway enforcement/verification files) share no path with any lane. 2089 was not in the open list at 14:3x (merged or closed); I did not check which.

## 4. NOT NOW
| Ticket | Reason |
|---|---|
| KS-1699 | Waits on Kam (commission exclusion) |
| KS-2059 | Ruled 11-06 but "a separate seat takes it after KS-2058 lands, design returns to Kam before any migration" |
| KS-1948 | Needs an ownership model (a ruling), and overlaps PR 2067 (`staking/src/index.ts`) |
| KS-2092, 2093, 2105, 1732 (governance) | PR 2099 open on `governance/src/index.ts`, `services/governanceService.ts`, `db.ts`; KS-2093 is an authorization design |
| KS-757 | Ruled (atomic claim, no migration) but PR 2099 also edits `originate/src/services/gdprService.ts`: sequence after 2099 merges. Then it is a good C4 build |
| KS-2036 | `certifications.ts` (PRs 2228, 2160) and `adminConfig.ts` (2158, 2087) both under open PRs |
| KS-1936, KS-1545, KS-1632 | Overlap: `api-gateway/src/routes/admin.ts` (PR 2159), `routes/platform.ts` (2073), `originate adminConfig.ts` (2158, 2087), verification routes (2225, 2138). KS-1632 is ruled (remove the setting) and is a good build once those merge |
| KS-1200, KS-960 | Ruled "as recommended" but step one is a read of every environment's schema (production-adjacent, Kam), then aligning schema files; migration => QUESTION to Kam, flagged |
| KS-1777 | Ticket says no fix proposed; three systemTest files read the flat body: needs a ruling |
| KS-1882 | Asks for a stated authorization rule per route: a decision first |
| KS-1466 | Kam ruled "close it, measure first": measurement is a read on kintsugi and demo |
| KS-1392, KS-1076 | Premise is stale: GitHub Actions retired 2026-08-27; KS-1076 comment proposes re-framing as a local slot run |
| KS-1691, 1692, 2063, 1370, 619, 1937, 2038 | Auth/security paths: in Seat B's queue (PR 2223 area), already built in a branch or PR (619 -> 2128, 2038 -> 2048), or comment says built; not re-verified one by one |
| KS-607, 683, 735, 188, 135, 61, Peter/Stuart-assigned (8 + 7) | Waits on client humans or UAT/demo (KS-607 demo rows wait for a separate yes from Kam) |
| KS-1393, 1390, 725, 696, 651, 582 | Decisions or Akto/CI work in flux; not screened deeper |
