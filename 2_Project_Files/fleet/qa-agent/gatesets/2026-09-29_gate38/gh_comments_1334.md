--- comment 5873117241 by linear[bot] at 2026-09-28T15:24:44Z
<!-- linear-linkback -->
<details>
<summary><a href="https://linear.app/secuura/issue/KS-888/dbsaveapikey-swallows-a-failed-insert-post-apikeys-answers-201-for-a">KS-888 dbSaveApiKey SWALLOWS a failed INSERT — POST /api/keys answers 201 for a key that was never written; blast radius is ALL key persistence, not one column</a></summary>
<p>

## BLUF

`dbSaveApiKey` catches every error from its INSERT and only logs it (`services/security/src/index.ts:236-238`). **A key that fails to persist still returns 201 with live key material.** Pre-existing; KS-869 grew its blast radius by taking the statement from 14 columns to 15.

## Mechanism

```ts
} catch (err: any) {
  logger.error('DB save API key failed', { error: err?.message });
}
```

The route continues and answers 201. The key exists in `memApiKeys` and validates — until the process restarts, at which point it silently does not exist.

**KS-869's contribution:** on a schema lacking `connector_id` the 15-column statement raises `42703` where the parent's 14-column one succeeded. Likelihood measured **LOW** by the gate — every deployment path lands the column (migration 018 is a single commit, and the demo now carries it) — but the failure mode is the swallow, not the column.

## Fix shape

Either a **boot assertion** that the named columns exist (fail fast, loudly, at start), or **narrow the catch** so `42703` (undefined column) and other structural errors are re-raised rather than logged. A mint that cannot persist must not answer 201.

## Acceptance

With the column absent, `POST /api/keys` does **not** return 201. A driven test: point the service at a schema without `connector_id` and assert the response is a 5xx, not a 201 — the shape that would have caught this.
</p>
</details>
<!-- linear-review-link -->
<p><a href="https://linear.app/secuura/review/ks-888-pin-that-validate-logs-a-failed-usage-write-and-never-refuses-6ed5e7b6439f">Review in Linear</a></p>

--- comment 5873149195 by kksecura at 2026-09-28T15:26:26Z
**The `is_active` doubt named in the PR body: measured, and it is REAL. Filed as KS 1370 (High).**

Measured at `0d156d12`, from the control flow rather than inferred:

- `index.ts:1326` validate resolves the key from the **in-memory map first**.
- `:1328-1334` the code's own comment says that map is "populated **only at boot** from svc_api_keys".
- `:1335` the database is read **only** `if (!apiKey)`; `:1347` warms the cache.
- `:1358` the revoked check reads that **stale** copy.
- `:1369` → `:316-318` the upsert is `ON CONFLICT (id) DO UPDATE SET … is_active = EXCLUDED.is_active`, and `EXCLUDED.is_active` is the stale `true`.

So it is two things, and the first is worse than the write-back the brief asked about: a revoked key **keeps authenticating** in any process whose memory predates the revoke, and that process's usage write then **rewrites `is_active = true` over the persisted revoke**, losing it for everyone.

**Not fixed here and not touched here.** This PR is the log-only pin Kam ruled, and it neither causes nor hides the above. What is **not** done is a driven two-process run showing a persisted revoke actually lost — that is why KS 1370 is High rather than Urgent, and it is the first thing to do on it.

Board search before filing, with controls: `EXCLUDED.is_active`, `populated only at boot`, `security_find_api_key_by_hash`, `stale memory` all returned 0; positive controls returned `memApiKeys` 4, `dbSaveApiKey` 3, `is_active` 2; nonsense control 0. The four `memApiKeys` hits were each read and none covers this.

