--- comment 5825511923 by linear[bot] at 2026-09-25T02:08:15Z
<!-- linear-linkback -->
<details>
<summary><a href="https://linear.app/secuura/issue/KS-528/frontends-react-router-v6-v7-migration-3-moderate-client-runtime">KS-528 Frontends: react-router v6 → v7 migration (3 moderate client-runtime advisories — open redirect/XSS, constructor injection)</a></summary>
<p>

## Why

Three of the KS-493-baselined advisories sit on `react-router`/`react-router-dom` v6 in the three portal frontends (admin / issuer / verifier) and are **client-runtime** classes, not build tooling:

* GHSA-337j-9hxr-rhxg — arbitrary constructor injection via deserialization (moderate)
* GHSA-wrjc-x8rr-h8h6 — open redirect via backslash in `<Link>`/`useNavigate` (moderate)
* GHSA-jjmj-jmhj-qwj2 — open redirect leading to XSS (moderate)

npm marks the fix as `react-router-dom@7.18.2` with `isSemVerMajor: true` — a v6 → v7 migration, NOT a lockfile bump, so it cannot ride the KS-493 lock-regen wave.

## Scope

* Migrate `frontend/admin`, `frontend/issuer`, `frontend/verifier` from RRD v6 to v7 (route object/API changes, `RouterProvider` shape, relative-path semantics).
* Verify the three portals end-to-end on local + demo after the migration.
* Remove the three GHSA entries from `scripts/audit/audit-baseline.json` in the same PR (gate goes green on real fix, not suppression).

## Links

Parent register: KS-493 (Review H). Baseline entries expire **2026-08-19** — if this migration is not done by then, re-reason those three entries against THIS ticket with a new expiry instead of letting the gate lapse red.
</p>
</details>
<!-- linear-review-link -->
<p><a href="https://linear.app/secuura/review/ks-528-dompatch-react-router-dom-6306-in-four-locks-ghsa-jjmj-row-558d0a2d9562">Review in Linear</a></p>

