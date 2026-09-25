--- comment 5827186405 by linear[bot] at 2026-09-25T05:14:31Z
<!-- linear-linkback -->
<details>
<summary><a href="https://linear.app/secuura/issue/KS-1128/the-platform-tenant-seeds-catch-logs-platform-tenant-seed-skipped-at">KS-1128 The platform tenant seed's catch logs `Platform tenant seed skipped` at debug — the KS-962 class on the platform-DB path: a seed that cannot seed reports into a level the demo does not read</a></summary>
<p>

## BLUF

`Blockchain/Dev/services/api-gateway/src/startup-migrations.ts`, inside `runStartupMigrations()`'s platform stage (`if (platformDbUrl)` → the `pSeedPool` block that inserts Secuura Co. + five client tenants + `tenant_config`): the seed's own catch is

```ts
} catch (seedErr: any) {
  log('debug', 'Platform tenant seed skipped', { error: seedErr?.message?.substring(0, 80) });
}
```

The main-DB user statement had the identical shape (`log('debug', 'User seed skipped', …)`) and it hid a statement that threw on every boot for as long as encryption had been live — KS-962's own words: *a defect that reports itself into a channel nobody is watching is indistinguishable from no defect.* The KS-950/KS-962 round raised the main-DB arm to warn and left this one alone by ruling (the platform seed does not move in that round).

## What is owed

* Raise the arm to `warn` with a message that names it a failure (`Platform tenant seed FAILED (platform DB)`), error text to 200 chars, in the same shape as the main-DB arm.
* A cell that proves it: boot the real `runStartupMigrations()` with `PLATFORM_DATABASE_URL` pointing at a database whose `tenants` table cannot take the insert, and assert the `[WARN]` line. The ks949 suite's boot driver (a mkdtemp `tsx` script importing `runStartupMigrations()` against a socket-only PostgreSQL) is the pattern; the platform path was **not** exercised in that round (`PLATFORM_DATABASE_URL` unset — stated in its PR's NOT run).

## Not this ticket

Whether the platform seed's `ON CONFLICT (slug) DO NOTHING` INSERT and the `tenant_config` upsert are themselves correct on the deployed platform schema — nobody has measured that on a real platform database in this round; KS-1055 covers the tenant-migration path.

## Provenance

Read from source at develop `0f69129b3` by s201, 2026-09-13 (ITEM 0 F3 in its plan confirmation; Wednesday ruled one Low ticket, 05:40:37Z). Board searched by `Platform tenant seed skipped`, `pSeedPool`, `platform seed` before filing: 0 hits.
</p>
</details>
<!-- linear-review-link -->
<p><a href="https://linear.app/secuura/review/ks-1128-seedwarn-a-failed-platform-tenant-seed-logs-warn-failed-200-87a172cc6fe5">Review in Linear</a></p>

