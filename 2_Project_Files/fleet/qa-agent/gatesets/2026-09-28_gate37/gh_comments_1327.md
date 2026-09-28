--- comment 5868013987 by linear[bot] at 2026-09-28T10:20:29Z
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
<p><a href="https://linear.app/secuura/review/ks-888-a-revoke-whose-save-fails-answers-503-or-500-and-is-not-5f6357d94a07">Review in Linear</a></p>

