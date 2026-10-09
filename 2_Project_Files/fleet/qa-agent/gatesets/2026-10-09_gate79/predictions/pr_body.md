Refs KS-1402 — https://linear.app/secuura/issue/KS-1402

## What changes

`POST /api/documents/:id/transfer-custody` with `newHolderEmail` used to forward the caller's credential to auth's `GET /api/users/lookup`. Auth refuses a connector token there, so every Platform S transfer by email answered **403**: Stuart measured 7 of 7 on 2026-10-05.

Kam ruled on card `secuura-ks1402-s-key-cannot-carry-users-read-1006`, option **a** (2026-10-06T09:58:21+11:00): *"a: Originate resolves the holder with its own service credential (Stuart's option 2)."* Detail: *"No scope change and no re-mint of any live key. Keeps 'on-behalf-of resolution is K-side'. A K build round, then the QA gate, then a merge. The cross-tenant guard must be proved by the gate."*

**Mechanism.** Originate resolves the holder with one bound read on its own database, and sends no token at all: it validates the email with auth's own zod schema (`users.ts:233`, `z.string().trim().email().min(3).max(320)`), normalises the value as sent with auth's `toLowerCase().trim()` (`documents.ts:1728-1730`), hashes it with `lookupHash`, and reads `SELECT id FROM users WHERE email_lookup_hash = $hash AND (tenant_id IS NULL OR tenant_id = $tenant::uuid) LIMIT 1` on the request's db. Choosing a DB read for "its own service credential" is a reading of the ruling, confirmed by Wednesday (2026-10-09 03:07:58Z send amendment). The id path already reads `users` inside originate (`documents.ts:1799-1805`), so this is not a new kind of access for the route. Auth is unchanged, and the act gate (`documents:transfer-custody`) is byte-unchanged and still runs first.

**The headline (cell C2): the tenant guard is NEWLY load-bearing for connectors.** At base, auth refused the connector before its own tenant compare ever ran. Now the connector resolves, and the bound tenant predicate is the only thing between it and another tenant's user. C2 pins that a cross-tenant email answers the same 404 as no user. C2b pins the interactive caller, green at both base and head.

**The ruled mechanism is STRICTER than auth's path.** `users.ts:306` skips the tenant compare when either side is falsy (`callerTenantId && user.tenantId && …`). Here the request's tenant is bound in the WHERE clause on every call.

**RLS, stated honestly:** the bound predicate is the enforcement. The tenant GUC is belt-and-braces, and this PR does not claim two working layers.

**Failure-mode change (deliberate, accepted by Wednesday 04:01Z):** a database failure during resolution now lands in the route's existing outer catch, `500 INTERNAL_ERROR 'Failed to transfer custody'`, which is where the id path's own `users` read already lands. Before, the only failure on this path was auth being unreachable (502).

**Deploy requirement:** originate needs `PII_LOOKUP_HMAC_KEY` (already declared for it at `docker-compose.yml:601`). Registration takes TWO conditions: `index.ts:370` loads the keyring only when `PII_ENCRYPTION_KEY` is set, and `encryptedField.ts:632-633` registers the lookup key only when `PII_LOOKUP_HMAC_KEY` is also set. Nothing refuses to start without the second. Without it every email transfer answers a labelled 502 (cell C9).

## Test Evidence

**Touched (8 files):** `routes/documents.ts`; `originate.openapi.ts` (descriptions only) and the regenerated `docs/openapi/secuura-api.yaml`; a NEW `ks1402-transfer-custody-resolves-holder-email-in-originate.test.ts`; `ks739-…-lookup-4xx-mapping.test.ts`; `ks697-…-holder-existence.test.ts` (one key-registration statement plus its comment); both `Projects Documents/*.html` (flow `44.`, cheat-sheet `KS-1402`, in this same commit per SKILL §4).

**Ran — by Seat K 1st (the build seat), on these bytes** (tied by patch sha256 `ab8e9e441864e05c…`, 88593 B):
- New file, 11 cells on the real router, with the real `rbac` unmocked. **BASE red C1, C2, C9; HEAD 11/11.** C1's base red is `expected 201 received 403`, which is auth's own answer: the base fetch spy re-implements auth's three decisions (gate `users.ts:285`, schema `:233`, tenant compare `:306`). The db mock EVALUATES each query's predicates. Tenant B is originate's `DEFAULT_TENANT_ID`, so a bind-the-default tamper is caught.
- Tamper matrix, 14 rows, each 11/11 executed, HEAD restored by sha256: tenant conjunct dropped → C2 C2b; bind default → C1 C2 C2b C4 C8; skip the gate → C3; restore the caller-header fetch → C1 C2 C9 (= base); normalisation ×3 → C8; cross-tenant answers 403 → C2 C2b; hash conjunct dropped → C2 C2b C5 C7 C8 C10; NULL tolerance → C7; no catch → C9; no format check → C6. No all-green row; one red arm per conjunct.
- KS 739 file: 20 definitions / 25 executed → **17 retired (21 executed) + 3 re-pointed (4 executed)**, plus a 13-row guard asserting 0 lookup calls whatever auth would answer. HEAD 17/17, BASE 0/17.
- KS 697 file: 16/17 without the key line (the red reads 502) → 17/17 with it; the cell text is byte-identical.
- Whole originate suite (`jest`): 96 files 1093/1093 → **97 files 1096/1096**. tsc: service program rc 0 and a separate test program rc 0, each with a planted rc 2 control.
- `check:openapi` rc 1 before regenerating (the control), rc 0 after; the yaml moved in 3 hunks.

**Ran — by Seat K 2nd (this PR's author seat), before the commit:** ks1402 **11/11**, ks739 **17/17**, ks697 **17/17** (jest JSON, the named binary), `npm run check:openapi` rc **0**. The patch sha256 was identical before and after.

**NOT run:** the four platform suites (Schemathesis, Akto, Playwright, k6), because there is no local stack this round; no S↔K pair run; live sweep owed.

**Migrations / config:** no migration, no config change, no scope change, no new secret or env var (`PII_LOOKUP_HMAC_KEY` already exists; see the deploy requirement above).

## Sequencing (SEQUENCED-AFTER)

- This branch is on base `81d2e5f4c415`, and develop has moved since. **The merge seat merges develop IN (keep-both on both docs) and REGENERATES `secuura-api.yaml`**; neither is hand-merged here.
- `secuura-api.yaml` lands after **#1429** (KS 1449), the only other open PR that touches it.
- Both `Projects Documents/*.html` docs are touched by eight open PRs: **#1383, #1429, #1430, #1431, #1432, #1433, #1434, #1436**. gate77 has given a GO to the seven gated rows, and a merge seat will land them. #1427 (KS 1274) is already merged. Every overlap is a doc block; no open PR touches `documents.ts`, `originate.openapi.ts` or any of the three test files.

## NOT COVERED

- live sweep owed.
- No S↔K pair run: Stuart's `PS 992` cell can go green only after a Kintsugi deploy, which is Kam's call.
- Q-LEGACY: a user with a plaintext email and no lookup hash resolved at base through auth's legacy fallback, and 404s at head. The count of such users is unmeasured.
- The KS 1406 class (a tenant-less connector on auth's `/lookup`) is not addressed; `/lookup` is unchanged.
- The four platform suites were not run (above).

## Project rules walked (quoted at base `81d2e5f4c415`)

- SKILL `secuura-test-discipline` (blob `b59b74a592e9`): §4 both docs in the same commit as the test change; §5d WHY + ticket + prior behaviour (in each doc block) and the ticket URL here; §5e this round makes ONE branch and ONE PR; §5f `live sweep owed`, and the ticket does not move.
- Repo `CLAUDE.md` (blob `ff426ce6097d`): `:167-175` no cross-organisation references (none here); `:255-256` the Linear URL (first line); `:285-286` Test Evidence (above); `:296` never push to `develop` (this is a feature branch).
- Merge: the author merges once TESTED on Wednesday's GO, and not in this round.

🤖 Generated with [Claude Code](https://claude.com/claude-code)
