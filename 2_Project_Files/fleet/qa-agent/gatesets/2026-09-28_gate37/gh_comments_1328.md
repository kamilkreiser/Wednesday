--- comment 5868238110 by linear[bot] at 2026-09-28T10:36:51Z
<!-- linear-linkback -->
<details>
<summary><a href="https://linear.app/secuura/issue/KS-1335/post-apiteamsnotify-a-permanently-failing-webhook-is-never-rotated">KS-1335 POST /api/teams/notify: a permanently failing webhook is never rotated past, because last_sent_at is written only on success</a></summary>
<p>

## BLUF

`POST /api/teams/notify` now bounds its row set and **rotates** it, so a repeat call reaches rows the
previous call did not (#1274, F-1274-1). The rotation key is
`ORDER BY last_sent_at ASC NULLS FIRST, created_at ASC`.

`last_sent_at` **is written only after a SUCCESSFUL send.** A webhook that always fails — a dead peer,
or one the SSRF guard blocks — keeps a NULL `last_sent_at` for ever and therefore sorts to the **head**
**of every call**. With `TEAMS_NOTIFY_MAX_ROWS` or more permanently-failing rows, the starvation
F-1274-1 identified **returns in full**: the healthy rows past the limit are never reached by any
number of calls.

This is a **known, pinned limit of the F-1274-1 fix**, not a regression it introduced. Before that fix
the order was a fixed `created_at ASC` and *nothing* rotated.

## Where

`services/m365-integration/src/index.ts`, the notify route. The write is inside the success branch:

```ts
if (resp.ok) {
  sent.push(wh.id);
  await query('UPDATE svc_teams_webhooks SET last_sent_at = NOW() WHERE id = $1', [wh.id]);
} else {
  failed.push(wh.id);       // <- no write, so last_sent_at stays NULL
}
```

The `!result.ok` branch (guard-blocked or request-failed) likewise does not write.

## It is already pinned in code

`R3` in `src/__tests__/ks934-teams-notify-request-path-bound.test.ts` asserts the CURRENT behaviour:
with `MAX_ROWS` permanently-failing rows, a second call attempts **exactly the same set** and never
reaches the last five. **R3 is a pin, not a fix.**

⚠ **When this ticket is built, R3 WILL RED. That is the intended signal, not a breakage** — it must be
rewritten to assert the new behaviour in the same change.

Red-proved: writing `last_sent_at` on a failed attempt too (one of the fix shapes below) reds **R3 and**
**only R3** — 1 of 8 cells. So R3 discriminates today rather than passing vacuously.

## Why it was not fixed in #1274's fix round

Both available shapes reach past a fix round's declared scope:

1. **write** `last_sent_at` **on every ATTEMPT.** This changes the meaning of a **published** field —
   `lastSentAt` is returned by `GET /api/teams/webhooks` (`index.ts`, the list route) — so "last sent"
   would start meaning "last tried". A consumer cannot tell the difference and is not warned.
2. **add a** `last_attempted_at` **column.** DDL in **two** places (`docker/init/06-m365-tables.sql` and
   `services/api-gateway/src/startup-migrations.ts`) plus an `information_schema`-guarded backfill for
   existing deploys, then order by it.

Shape 2 is the honest one — it leaves the published field alone — but it is a schema change and
belongs in its own pass with its own review.

## Done means

1. A rotation key that advances on an ATTEMPT, not only on a success, by whichever shape is chosen.
2. A cell: `MAX_ROWS` permanently-failing rows, two calls, the second REACHES the rows past the limit.
3. `R3` rewritten in the same change (it pins the behaviour being replaced).
4. If shape 1 is chosen, the published `lastSentAt` field's meaning is documented where it is
   returned, or renamed.

## Search before filing

`searchIssues`, KS team, `includeArchived: true`, every page literal-matched client-side:
`last_sent_at`, `last_attempted_at`, `svc_teams_webhooks`, `teams/notify starvation`,
`permanently failing webhook`, `NULLS FIRST`, `teams notify rotation` — **0 literal hits each**.
Controls: `webhook` **43**, `adminConfig` **19**, `teams` **11** (the matcher fires); a nonce token
never written anywhere **0**. Noted for a later reader: KS-934's own description contains neither
`svc_teams_webhooks` nor `last_sent_at`, so those zeros are a property of the corpus, not of the
matcher.

Refs KS-934
</p>
</details>
<!-- linear-review-link -->
<p><a href="https://linear.app/secuura/review/ks-1335-rotate-the-notify-window-on-last-attempted-at-stamped-on-every-a9e317ee8ea5">Review in Linear</a></p>

