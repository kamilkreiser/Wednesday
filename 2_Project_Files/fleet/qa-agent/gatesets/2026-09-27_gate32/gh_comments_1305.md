--- comment 5853771186 by linear[bot] at 2026-09-27T07:23:26Z
<!-- linear-linkback -->
<details>
<summary><a href="https://linear.app/secuura/issue/KS-1090/api-gateway-originate-tsc-never-type-checks-951s-three-wiring-tests">KS-1090 api-gateway + originate: tsc never type-checks #951's three wiring tests, and the mint-scope test pins 2 of 17 non-originate keys</a></summary>
<p>

## BLUF

* **The type-check claim does not cover the tests (R2-2).** #951's Test Evidence says "`tsc --noEmit` rc 0 on both services", but that run never reads its 3 new test files.
  * Both services' tsconfigs exclude `src/__tests__`.
  * A type error planted in each test file returns rc 0; the same plant in `routes/proxy.ts` returns rc 2.
* **The mint-scope test pins 2 of 17 (R2-3).** `ks1041-vouch-mint-scope.test.ts` asserts "no vouch" only at analytics and auth. An allowlist widening that spares those two keys stays green.
* **Test-quality findings, not runtime defects.** They come from the round-2 tier-1 gate on #951 at `02a22f4bb`, and one test pass proves both.

## Recommendation

One change, one test pass:

1. **A type-check that includes the tests** (e.g. a `tsconfig.test.json`), run in the local gate, with a planted-error cell that must exit non-zero.
2. **A structural mint-scope guard:** derive every `proxy('<key>')` mount from the factory and assert, per mount, that only originate receives `x-gateway-vouch`, with a reach control on each. The gate's `evidence/harness/mounts.qa.ts` does this in 172 cells, in under 2 s.
3. **R2-4, record only:** quote tamper shapes that compile. `void stripTrustHeaders;` alone fails the gateway's tsc (TS6133, `req` unused); `void stripTrustHeaders; void req;` compiles and gives the identical red.

## Detail

* **R2-2, measured:**
  * Planted `const qa951r2Planted: number = 'qa951r2-not-a-number';` into each file.
    * 3 test files: rc 0.
    * Controls — `routes/proxy.ts` and `utils/gatewayProvenance.ts`: rc 2 (TS2322).
  * `--listFiles`: the gateway checks 33 `src` files and originate 51, with 0 under `__tests__` in each.
  * `api-gateway/tsconfig.json` excludes `src/__tests__`; `originate/tsconfig.json` excludes `src/__tests__` and `src/**/*.test.ts`. Both exclusions pre-date #951.
* **R2-3:**
  * V2 asserts absence at analytics and auth only.
  * The proxy has 18 service keys: 17 non-originate, on 16 hosts.
  * Example of a change that stays green: `VOUCH_RECIPIENTS.has(k) || k.startsWith('vc')`.
* **R2-4:**
  * C3a (`void stripTrustHeaders;`) — tsc rc 2, TS6133.
  * C3b (`… void req;`) — tsc rc 0.
  * Both redden the edge-strip C3 cell.
* **Source:** `Testing Agent MAIN/projects/secuura/reports/2026-09-11-ks1041-951-02a22f4bb-tier1-r2/report.md`, §R2-2, §R2-3, §R2-4.
* **Board searched before filing:**
  * literal match over the 7 KS issues and 12 comments created since 2026-09-10T22:40Z, for `R2-2`, `R2-3`, `R2-4`, `mint-scope`, `tsconfig.test`, `TS6133`, `void stripTrustHeaders`, `VOUCH_RECIPIENTS` and `noEmit`;
  * 0 hits, except `R2-2` on KS-1089 — that is #953's gate ID, read in context.
  * all-time `searchIssues`, matched literally and counting live tickets only: `type-check` 6, `__tests__` 12, `tsconfig` 7, `typecheck` 4, `mint-scope` 0.
  * The same tsconfig class is already filed per package elsewhere — KS-848 (services/kyc), KS-1000 (services/auth), KS-933 (packages/shared), KS-993 (systemTest/fixtures). None covers api-gateway or originate, and none covers the mint-scope pin.
* **Related:** KS-1041, PR #951, KS-1083.
</p>
</details>
<!-- linear-review-link -->
<p><a href="https://linear.app/secuura/review/ks-1090-r2-3-type-check-the-api-gateway-wiring-test-the-tsc-program-54094f1c14af">Review in Linear</a></p>

