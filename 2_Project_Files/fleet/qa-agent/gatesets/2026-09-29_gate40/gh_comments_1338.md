--- comment 5880008112 by linear[bot] at 2026-09-28T22:38:52Z
<!-- linear-linkback -->
<details>
<summary><a href="https://linear.app/secuura/issue/KS-1370/security-validate-reads-api-keys-from-a-boot-only-memory-map-so-a">KS-1370 Security: validate reads API keys from a boot-only memory map, so a revoked key keeps authenticating AND its usage write rewrites is_active = true over the revoke</a></summary>
<p>

**BLUF — measured from the source path at develop** `0d156d12`**, and it is worse than a multi-replica write-back concern: it is also a live authentication bypass on a single process.**

`POST /api/keys/validate` in `services/security/src/index.ts` resolves the key from an **in-memory map first** and reads the database **only on a cache miss**:

* `:1326` `let apiKey = Array.from(memApiKeys.values()).find(k => k.keyHash === keyHash);`
* `:1328-1334` the code's own comment states the map "is populated **only at boot** from svc_api_keys".
* `:1335` the DB fallback (`security_find_api_key_by_hash`) runs **only** `if (!apiKey)`, and `:1347` warms the cache.

So once a key is in memory, this process never re-reads its row. Two consequences follow, and the second is the one the KS-888 validate brief raised:

**1. A revoked key keeps authenticating.** `:1358` `if (!apiKey.isActive)` is evaluated against the **stale memory copy**. If the row is set inactive by anything this process did not do — the revoke route on another replica, an operator UPDATE, a future admin tool — this process answers `valid: true` until it restarts.

**2. The usage write then UNDOES the revoke for everyone.** `:1369` `await dbSaveApiKey(apiKey);` and the upsert at `:316-318` is `ON CONFLICT (id) DO UPDATE SET last_used_at = EXCLUDED.last_used_at, usage_count = EXCLUDED.usage_count, is_active = EXCLUDED.is_active`. `EXCLUDED.is_active` comes from the in-memory `k.isActive`, which is still `true`. So a validate on a stale copy writes `is_active = true` over a persisted revoke. The revoke is lost in the database, not merely missed locally.

**What is measured and what is not.** Every line above is read at `0d156d12` and quoted. The control flow is decisive on its own: memory-first, DB-on-miss-only, boot-only population, and the upsert asserting `is_active` from that copy. What is **NOT** done is a driven two-process run demonstrating the lost revoke end to end — that needs two memory maps over one database and is the natural first step for whoever takes this.

**Why it is not KS-888.** KS-888 is about what happens when the usage write *fails* (mint refuses, revoke answers 503, validate logs and continues — all shipped or pinned). This is about the write *succeeding* and carrying a stale field. The pin for validate's log-only behaviour is PR #1334; it does not touch this and must not be read as covering it.

**Board search before filing, with controls:** `EXCLUDED.is_active`, `populated only at boot`, `security_find_api_key_by_hash`, `stale memory`, `revoked key still validates` all returned **0**; positive controls on the same literal query shape returned `memApiKeys` 4, `dbSaveApiKey` 3, `is_active` 2, and the nonsense control 0. The four `memApiKeys` hits (KS-1174, KS-889, KS-888, KS-869) were each read and none covers this: they are the gateway's 401 collapsing, the connector_id backfill window, the KS-888 save-failure family, and connector_id persistence.

**Shapes worth considering (not a recommendation).** Narrowest: drop `is_active` from the upsert's SET list, so a usage write can never assert liveness. That closes consequence 2 and leaves consequence 1. Wider: re-read the row (or invalidate the cache entry) before answering, which closes both and costs a query per validate on a deliberately unauthenticated hot path.
</p>
</details>
<!-- linear-review-link -->
<p><a href="https://linear.app/secuura/review/ks-1370-validate-answers-on-the-stored-revoke-and-its-usage-write-3ebf6d875177">Review in Linear</a></p>

