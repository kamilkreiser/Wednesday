Wednesday -> Seat B (Secuura/Blockchain-B)

## BLUF
**Kam ruled three of your row QUESTIONs at 18:31 AEST (panel):** mysql2 → override; ip-address → override; react-router rows 11+12 → commission the v7 migration AND date both rows to its planned landing. Two new PRs join your queue (both TIER 1); the react-router date waits for a sizing Wednesday commissions separately — **you do not re-date anything yet.**

RULED BY KAM, NOT YET IN AN ARTEFACT (post each on its ticket verbatim with its timestamp; mail the comment ids):
- `secuura-audit-row-mysql2-override-vs-prisma-pin` → override (18:31:30): "Override to mysql2 3.23.1 (recommended)" — lands on KS-763.
- `secuura-audit-row-ip-address-high-override` → override (18:31:18): "Override to ip-address 10.3.1 (recommended)" — lands on KS-729.
- `secuura-audit-rows-react-router-v7-migration` → migrate-and-date (18:31:25): "Commission the v7 migration AND date both rows to its planned landing (recommended)" — lands on KS-528.

## Recommendation
1. **PR-7 mysql2 override (row 3, Sep-24 — do it BEFORE PR-4 qs):** `"mysql2": "3.23.1"` in `overrides` of `services/originate/package.json` AND `Blockchain/Dev/package.json`; regen both locks in the bounded container; originate unit suites; `prisma generate` smoke in the container (allowed, no image build); remove row 3 once both gates read it gone. TIER 1. This is the first override that contradicts a declarer's exact pin — the PR body states Kam's ruling and that prisma's MySQL path is unused (the row's 09-06 measurement; re-measure imports = 0 with a positive control).
2. **PR-8 ip-address override (row 15, HIGH, Sep-30):** `ip-address: ^10.3.1` in `overrides` of `frontend/issuer/package.json` AND the root manifest; regen; the issuer build + unit suites; remove row 15. TIER 1 **with a real-browser pass on the issuer portal** (the gate drives it). Carry your tarball-diff finding as the evidence basis. A wallet flow needing a stack is stated NOT run.
3. Order now: #1022 (gate re-pinning) → PR-3 (js-yaml+vitest+bbm) → **PR-7 mysql2** → PR-4 qs → PR-5 react-router-dom → PR-6 row 14 → PR-8 ip-address. One root-lock PR open at a time.
4. **Rows 11/12 (react-router):** untouched by you. The migration (source work, 3 portals) goes to a separate Claude seat; its sizing sets the date, and the re-date then comes to you as its own instruction.
