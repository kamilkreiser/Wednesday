KS-1334 adminConfig: four admin routes return err.message in a 500 body with no NODE_ENV guard (production info leak)
state In Progress

## BLUF

Four handlers in `services/originate/src/routes/adminConfig.ts` put the thrown error's `message`
straight into a 500 response body **with no** `NODE_ENV` **guard at all**, so they leak internal text in
**production** as well as everywhere else. This is a different and worse class than KS-730, which is
about the off-production ternary shape (`NODE_ENV === 'production' ? constant : err.message`).

Found while finishing KS-730 PR 3 of 3. **Not fixed there**: KS-730 enumerated 46 ternary sites and
converted exactly those; these four were never in its list, and folding four unlisted admin routes
into a tier-1 fix round would widen it well past its declared shape.

## The four sites, measured at base `d7cdecf1d2ee`

| line | route |
| -- | -- |
| `:113` | `POST /api/admin/refresh-tenants` |
| `:1859` | `POST /api/admin/backfill-certification-metadata` |
| `:2031` | `POST /api/admin/seed-demo-users` |
| `:2158` | `POST /api/admin/migrate-tenant-data` |

Each is the same shape:

```
res.status(500).json({ success: false, error: { code: 'INTERNAL_ERROR', message: err.message } });
```

(`:113` is `message: err?.message || 'Refresh failed'`, the same leak with a fallback.)

**Pre-existing, not introduced:** the count is **4 at the base** `d7cdecf1d2ee` **and 4 at the KS-730 PR 3**
**head**. KS-730 PR 3 neither added nor removed any of them.

## Why it was invisible to KS-730's own guard

KS-730 PR 3's source cell asserts `liveTernaries: 0` and `helperCalls: 46`. Both are TRUE with these
four present, because the cell counts the `NODE_ENV === 'production'` shape — which these four do not
have. A green KS-730 cell therefore says nothing about them, which is exactly why they are pinned
separately rather than left to be rediscovered.

## The regression guard that already exists

`KS-730 C4 SOURCE`, in
`services/originate/src/__tests__/ks730c-adminconfig-500-never-answers-err-message.test.ts`, pins these
four **by enclosing route name**. A fifth site reds it. **Fixing one of these four will also red it** —
that is deliberate: the list is then updated as part of the fix rather than drifting silently.
**Whoever builds this ticket must update that cell's** `KNOWN` **list in the same change.**
Red-proved: adding a fifth unconditional site reds C4 and nothing else (1 of 14).

## Done means

1. The four sites answer the constant body and log the message server-side, as KS-730's 46 do
   (`fail500` already exists in this file and is the obvious vehicle).
2. `KS-730 C4 SOURCE`'s `KNOWN` list is emptied, or the cell retired with its reasoning recorded.
3. A cell drives at least one of the four end to end and proves the thrown text is absent from the
   body **under** `production` — which is what separates this class from KS-730's.

## Search before filing

`searchIssues` with `includeArchived: true` over the KS team for: `refresh-tenants`,
`backfill-certification-metadata`, `seed-demo-users`, `migrate-tenant-data`, `adminConfig`,
`unconditional err.message`, `err.message 500 no NODE_ENV guard`, `adminConfig production info leak`.
Every page literal-matched client-side, because `searchIssues` ranks fuzzily.
**0 tickets name two or more of the four routes together with** `err.message`**.**
Controls: `adminConfig` returns **18** literal hits (the matcher fires), a nonce token never written
anywhere returns **0**. Open PRs also searched: **24 non-dependabot PRs' file lists read, 0 touch**
`adminConfig.ts`**.**

Refs KS-730
