# PROPOSAL (not a brief) — raise the UNRAISED held passes — 2026-10-10

Source: `0_Brain/reference/2026-10-10_spark-hold-census/CENSUS.md` (tip `785cb671557a`, unmoved start to end). 52 runs censused; 33 already on develop; **15 strict UNRAISED** (patch applies strict at the tip, absent from develop and every PR ref), 1 IN-A-PR-REF (KS-1426 = #1450), 1 lenient-only REJECT (KS-723 anchors-get, excluded). Pass-patch overlap with live seats #1448 / #1450: **0 of 15** (but see Q1). Patch path for each: its READY `CANONICAL PATCH =` line, or `runs/<run>/out.md.checker/patch.diff` for done.md-only runs. Not run: no tests at this tip (UNMEASURED).

## Bundles (file-disjoint from each other on pass files; max 4 PRs each)

**Bundle A — KS-591 (+ the one KS-1364 that shares its file), 3 PRs, all contract-only `requestBody.required` / param flags**
- A1 (tier 2): anchors-post-thread-mint (`anchoring.openapi.ts`) + stake-complete-unstake (`staking.openapi.ts`) + transfer-delegation-posts (`transfer.openapi.ts`). Three distinct files, REVIEW "security-adjacent: no", handlers untouched.
- A2 (tier 2): billing-customers-bundle (KS-591) + billing-credits-use-r4 (KS-1364); both edit `billing.openapi.ts`, A-then-B-check rc 0. Must ride one PR because they share the file. Billing is money, hence Q3.
- A3 (tier 1 guess): platform-tenants-create-status + platform-tenant-id-uuid; both edit `tenant-provisioning.openapi.ts`, A-then-B rc 0. Platform-admin tenant surface; the create-status REVIEW says "security-adjacent: yes by surface note, cannot alter any auth decision". platform-tenant-id-uuid was never reviewed.

**Bundle B — KS-1364 contracts, 2 PRs**
- B1 (tier 1 guess): originate-share-system-errors (`originate.openapi.ts`; one of its 3 operations is `POST /api/documents/{id}/share`; REVIEW "borderline only by name").
- B2 (tier 2): analytics-exports-r4 (`analytics.openapi.ts`) + teams-webhook-notify (`m365-integration.openapi.ts`) + apigw-batch-certify-delegate (`api-gateway.openapi.ts`). Three distinct files.

**Bundle C — code and dev tooling, up to 4 PRs**
- C1 (tier 1): KS-1432 apigw ks529 guard (`api-gateway/src/routes/verification.ts` + test) — a behaviour change to the `POST /api/documents` body guard on the gateway; the only non-contract product change among the 15. Patch is byte-identical to the drafter's golden.
- C2 (tier 2): KS-1355 dev-reload-slot-container-r2 (`dev-reload.sh` + test).
- C3 (tier 2, REVIEW FIRST): KS-948-r3 mixed-backtick (`check_shared_relink.test.sh` + `ks948_…test.sh`); r1/r2 were a FAIL and a REJECT, r3 never reviewed. Note ornith KS-937 landed in `check_shared_relink.test.sh` (40ed3573b); r3 still applies strict.
- C4 (tier 2, REVIEW FIRST): KS-865-r2 header-lists-checked-files (`check-no-latest-tags.sh` + test); r1 was a REJECT, r2 never reviewed.

Raisable now without a review step: A1, A2, A3, B1, B2, C1, C2 (7 PRs, 11+ passes). Needing a review first: C3, C4. Total bundles: 3.

## OPEN QUESTIONS for Wednesday

1. **Shared-file collision at raise time.** Every historic raise also edited the two `Projects Documents/*.html` docs, and every openapi raise `secuura-api.yaml` (checked on 1fba82ddb, 3d570510b, 4eaf7741a, 8a7b7ece0, 785cb6715, 1e7f90e26). #1448 holds the yaml + both docs, #1450 holds both docs. Bundles A and B (11 openapi passes) therefore serialise on the yaml and all seven PRs on the docs, whatever the pass files say. Should raise seats wait for #1448/#1450, or rebase onto them? (Textual collision only: UNMEASURED by trial rebase.)
2. **PR state of #1450.** I measured its head (76 of 79 KS-1426 lines present) but not whether it is open. Treat KS-1426 as not-mine either way?
3. **Tier calls.** Are billing (A2), tenant-provisioning (A3) and the document-share operation (B1) tier 1 or 2, given the passes are spec-only and each REVIEW says the gateway gate reads only methods + `security`?
4. **Reviews.** C3, C4 and platform-tenant-id-uuid (in A3) have no REVIEW HOLD. Who reviews, or do they drop out?
5. **KS-723 anchors-get** (REVIEW = REJECT, brief-class; applies only with `--recount --ignore-whitespace`, 14/67 lines on develop): confirm excluded.
6. **Held READY files that already landed** (33 of 52, e.g. KS-1274, KS-1139, KS-1410 x4, KS-1345, KS-1346, KS-1417, KS-1456, KS-591 nft pair): should their READY files be marked landed so the next census does not recount them?
7. **Freshness.** Most of these passes (drafted 10-05 to 10-07) were drafted against older tips; strict-apply passes at 785cb671557a, but tests were not run. Does the raise seat re-run the checker's red-first/green steps before opening each PR?
