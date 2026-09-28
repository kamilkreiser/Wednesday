#1338 KS-1370: validate answers on the stored revoke, and its usage write cannot revive one
head 42f8a5abc65ef9a6bc20c07797786089f2b9cd93

A revoked API key kept working, and using it un-revoked the key on disk.

`POST /api/keys/validate` resolved the key from `memApiKeys`, a map populated only at boot, so a revoke
performed in another process was invisible. Worse, validate's usage write went through the shared
`dbSaveApiKey` upsert, whose `is_active = EXCLUDED.is_active` then wrote the cached `true` back over the
persisted revoke — so merely *using* a revoked key restored it.

Driven on a real PostgreSQL 18.3 before the change: a stale instance answered `valid: true`, and after
its usage write the row read `is_active` false -> **TRUE** with `usage_count` 1 -> 2.

## Kam's rulings, quoted

`secuura-ks1370-revoke-undone-by-stale-process` = **(a)**, ruled 2026-09-29T07:11:50+10:00:

> **Fix both halves** — The usage write stops touching is_active (it records usage only), AND validate
> checks the stored revoke before answering valid, so a stale memory copy can neither honour nor
> restore a revoked key. A Secuura seat builds it with red-first cells for both halves, through the QA
> gate, no deploy. It re-pins #1334's validate cells, which bind the current upsert shape. It does not
> change your 20:22 ruling that a failed usage write is logged, never refused.

`secuura-ks1370-validate-when-the-revoke-check-cannot-read` = **(a)**, ruled 2026-09-29T08:05:30+10:00:

> Split: refuse on a failed read, memory-only mode answers from memory. A failed stored read with a
> database configured returns 503 'Unable to verify key'. ... A revoked key is never honoured.
> Memory-only deployments behave as today. The usage write stays log-only, as you ruled.

## What changed

**Half (i) — the usage write.** Validate now issues a usage-only
`UPDATE svc_api_keys SET last_used_at, usage_count`. Deleting `is_active` from the shared upsert is
**not** the fix: the revoke route persists its revoke through that same statement, and the KS 764
call-site guard pins exactly that shape, so removing it would stop a revoke of an existing row
persisting at all. Narrowing validate's own call site leaves revoke untouched. An `UPDATE` rather than
an upsert because every caller reaches it with a row that already exists — a usage bump must not
conjure a key.

**Half (ii) — the answer.** On a cache hit validate re-reads the stored row through the reviewed
pre-session carve-out `security_find_api_key_by_hash` (the KS 458 fail-closed carve-out, since this
route is unauthenticated and has no tenant GUC) and decides on that row, refreshing the stale cache
entry so it stops lying for later requests. The read has its own `try` and every exit from it is a
response, never a throw — this handler takes no `next`, so a throw would be an unhandled rejection.

## Two shapes, confirmed rather than assumed

Both follow from Kam's own words rather than new authority, and both were **confirmed as shapes by
Wednesday** (2026-09-28T22:28:36Z) before this was raised.

**1. A revoke is sticky in BOTH directions.** KS 888 (`secuura-ks888-revoke-validate-on-failed-save`,
option a) keeps the in-memory revoke when its save fails, so the key dies in that process while the row
still reads active. Refreshing blindly from the store would have **undone that and re-honoured a
revoked key**. So the two sources combine in the safe direction: revoked if *either* says revoked.
Stored-revoked beats cached-active (this ticket); cached-revoked beats stored-active (KS 888).
**Cell R2 of the KS 888 file is what caught this, and it now passes unchanged — the code was fixed,
not the test.**

**2. A vanished row** reads `Key not found` and the cache entry is evicted: a deleted row is a stronger
revocation than `is_active = false`. **This is a defensive path, not a live one** — grepped first,
nothing in `services/` or `migrations/` issues a `DELETE FROM svc_api_keys` outside migration 019.

## A measured cost, and a bound

`api-gateway middleware/auth.ts` re-read at this tip, not cited:
- `:229`/`:235` — a `!resp.ok` response **is** cached as a refusal for 30_000 ms, so a 503 from
  security refuses that key for up to 30 s past the fault. That is the cost of ruling (a)'s first limb.
- `:220` — a cached result is returned **without** re-validating. So half (ii)'s extra stored read fires
  **at most once per key per 30 s, not once per request.** The extra read is bounded by the gateway's
  own cache.

## Test Evidence

**Touched:** `services/security/src/index.ts`; `services/security/src/__tests__/ks888-failed-mint-save-issues-no-key.test.ts` (re-pinned); `services/security/src/__tests__/ks1370-validate-reads-stored-revoke.test.ts` (new). 3 files, +331/-8.

**Ran, on this head `42f8a5abc65ef9a6bc20c07797786089f2b9cd93`:**
- `services/security` whole suite — **26 files / 275 tests, 0 failed**
- KS 888 validate file — **19/19** (baseline **19/19** at the base tip; 7 executed cases failed mid-change, see the re-pin below)
- new KS-1370 cells — **9/9 green**, and **5/9 RED** against the unmodified `index.ts` at the base (W1, V1, V2, D1, F1)
- KS 764 revoke call-site guard (`packages/shared`) — **15/15, green and untouched**, as expected: revoke was not modified
- `tsc -p services/security` — rc 0
- `eslint` on both touched source files — rc 0
- **Real-PostgreSQL drill, 16/16 arms**, product file restored byte-identical (sha256 equal) after every tamper. PostgreSQL 18.3, unix socket only; my postmaster held **0 TCP listeners** (control: the native pg@15 held 2, so the check discriminates). Raw output is in `5_Project_History/2026-09-29_seatB-42nd/ks1370/`.
- Push preflight: **12/15 legs ran, 3 SKIPPED, nothing failed.** 12/15 is not a pass. The log reports the ratio but does not name which three skipped. Shell suites 60 passed / 0 failed / 0 skipped; 13 code guards passed.

**The re-pin, and why the count is both 5 and 7:** N-1334-1's figure of 5 counts `it`/`it.each`
*declarations* (R2, C3, V1, V2, V3); V1 is `it.each(INFRA)` with three cases, so **5 declarations = 7
executed cases**. R2 moved for the sticky-revoke interaction and now passes unchanged. C3, V1 x3 and V2
all failed for one root cause: the mock answered `rows: []` to every SELECT, so the new stored read read
`Key not found`. The mock now keeps a hash-keyed store the INSERT populates, which is *more* faithful —
a failed insert leaves the store active, which is precisely R2's state. V1 and V3 counted
`state.inserts`; validate's write is an `UPDATE` now, so they count `state.usageWrites`. Same claim, new
instrument. The two `state.inserts` counters that watch **mint** are deliberately untouched.
**V2's no-key/no-hash and one-error-line pins are unchanged**, and the usage-only write keeps the
byte-identical `'DB save API key failed'` message so V2 still binds this path. No pin was weakened.

**Only 5 of the 9 new cells are red-first, and I am not claiming 9.** The other four pin preserved
invariants: W2 (usage is still recorded), S1 (the KS 888 sticky revoke), M1/M2 (memory-only mode
unchanged by design, which keeps #1334's control C4).

**NOT run / NOT covered:**
- **RLS is not exercised by the drill, and it is the premise for the SECURITY DEFINER carve-out.** The
  drill runs as `postgres` (`rolsuper=t`, `rolbypassrls=t`), so every statement bypasses RLS.
  `svc_api_keys` genuinely is `relrowsecurity=t, relforcerowsecurity=t` with both `tenant_isolation`
  and `svc_api_keys_auth_lookup` present, but the drill **cannot** discriminate whether a direct SELECT
  would return zero rows. **The gate should drive the stored read as a non-superuser app role.**
- Two OS processes vs two module instances: two **module instances** with separate CJS caches were driven.
- `usage_count` written from a stale copy is a lost update. **Named as a candidate, not fixed, not filed.**
- The four platform suites (Schemathesis, Akto, Playwright, k6) were **not** run: this change is
  service-internal with no OpenAPI surface change.
- Nothing deployed. No migration run against any environment.

**Migrations + config:** none. No migration, no environment variable, no config change. The fixture
applied the existing migrations to a throwaway local database only.

**RUNTIME change on validate: §5f live sweep owed.**

Refs KS-1370


🤖 Generated with [Claude Code](https://claude.com/claude-code)

