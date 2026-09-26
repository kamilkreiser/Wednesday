--- comment 5841261954 by linear[bot] at 2026-09-25T23:57:51Z
<!-- linear-linkback -->
<details>
<summary><a href="https://linear.app/secuura/issue/KS-730/security-71-inline-handlers-still-return-errmessage-verbatim-off">KS-730 Security: 71 inline handlers still return err.message verbatim off-production — KS-727's enumerated remainder (api-gateway leaks it TWICE, at the edge)</a></summary>
<p>

## BLUF

**71 response-side sites still return** `err.message` **verbatim unless** `NODE_ENV === 'production'`**.** KS-727 fixed the two *shared* handlers — `packages/shared/src/errors` (mounted by 12 services) and `services/auth`'s own — which was the high-leverage half. These 71 are per-route **inline** handlers: the same defect, a mechanical change, but 5 files across 3 services with their own test surface, so they were enumerated rather than folded into [#767](<https://github.com/Secuura/Distributed_Secuura/pull/767>).

**Do api-gateway first.** It is the edge, and it is the worst of them.

## The remaining surface, measured 2026-09-01 after #767

| file | sites |
| -- | -- |
| `services/originate/src/routes/adminConfig.ts` | 46 |
| `services/originate/src/routes/gdpr.ts` | 15 |
| `services/originate/src/routes/systemErrors.ts` | 6 |
| `services/api-gateway/src/index.ts` | 2 |
| `services/tokenisation/src/index.ts` | 2 |
| **total** | **71** |

## Why api-gateway is the priority

`services/api-gateway/src/index.ts:1065` and `:1072`:

```ts
const errorMessage = NODE_ENV === 'production' && statusCode >= 500
  ? 'An unexpected error occurred'
  : err.message;
res.status(statusCode).json({
  success: false,
  error: {
    code: errorCode,
    message: errorMessage,
    ...(NODE_ENV !== 'production' ? { details: { details: err.message } } : {}),
  },
});
```

It returns `err.message` **twice** — once as `message` and again as `details.details`. Because this is the edge handler, a caller can receive internal text **even where the downstream service handler was careful**. It also makes the `details` leak survive any fix that only touches `message`.

`:1063` includes `err.stack` in the **winston log**, not the response. That one is correct and must stay — noted because a naive grep counts it as a leak (it counted mine).

## The shape of the fix

The two shared handlers were fixed by deleting the ternary, because **they already log** `err.message` **and** `err.stack` **at entry** — the change was subtractive with no information loss. **Check that per site here**: an inline handler that returns the message *without* logging it would lose the detail entirely if the return were simply removed. Where a site does not already log, add the log in the same change.

The three affected services are consistent within themselves, so a per-service pass is likely cleaner than a per-file one.

## Done when

- ☐ `services/api-gateway` — both sites, including `details.details`. Separate, first, and worth its own review.
- ☐ `services/originate` — `adminConfig.ts` (46), `gdpr.ts` (15), `systemErrors.ts` (6). Consider a small local helper rather than 67 edited ternaries; that is a judgement call for whoever does it.
- ☐ `services/tokenisation` — 2 sites. Note it *also* mounts the shared handler, so it is already partly covered by #767.
- ☐ A test per service in the shape of KS-727's: assert a 500 body does not contain the thrown message across `development` / `demo` / `test` / unset, with a control that a typed client error still carries its own text.
- ☐ Re-run the sweep to zero — **excluding comments and logging lines**, which the naive grep counts (73 naive → 72 code → 71 response-side on the measurement above).

## Refs

* KS-727 / [#767](<https://github.com/Secuura/Distributed_Secuura/pull/767>) — the shared handlers, fixed. This ticket is its enumerated remainder.
* KS-658 — the demo runs `NODE_ENV=development`, which is what makes every one of these the always-executing branch rather than a dev convenience.
* KS-703 / [#757](<https://github.com/Secuura/Distributed_Secuura/pull/757>) — the thread that surfaced the class, with the two measured leaks (`invalid byte sequence for encoding "UTF8": 0x00` and `role.split is not a function`).

*Filed 2026-09-01 (session 94) from KS-727's platform-wide sweep. Every count read off this tree in-session; no code written here.*
</p>
</details>
<!-- linear-review-link -->
<p><a href="https://linear.app/secuura/review/ks-730-stop-returning-the-thrown-message-from-adminconfig-500s-2a9f5086093e">Review in Linear</a></p>

