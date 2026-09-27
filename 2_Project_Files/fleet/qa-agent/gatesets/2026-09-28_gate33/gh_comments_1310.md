--- comment 5856677570 by linear[bot] at 2026-09-27T14:22:50Z
<!-- linear-linkback -->
<details>
<summary><a href="https://linear.app/secuura/issue/KS-1348/originate-production-file-logs-are-a-column-of-undefined-the-file">KS-1348 originate production file logs are a column of `undefined` — the File transports carry no format</a></summary>
<p>

**BLUF: under** `NODE_ENV=production` **originate's two File transports write the literal string** `undefined` **on every line, so** `logs/error.log` **and** `logs/combined.log` **contain no usable information.** Found by the gate30T1 review; reproduced independently here.

## Measured

`services/originate/src/utils/logger.ts:45-46` constructs both File transports with **no** `format`:

```
new winston.transports.File({ filename: 'logs/error.log', level: 'error', maxsize: 10_000_000, maxFiles: 5 }),
new winston.transports.File({ filename: 'logs/combined.log', maxsize: 10_000_000, maxFiles: 5 }),
```

The logger-level format is `combine(errors({ stack: true }), timestamp(...))` — it has no `json()` and no `printf()`, so nothing renders the entry. The Console transport is fine because it is given its own format (`json()` in production, `colorize()+devFormat` otherwise); the File transports were never given one.

Rebuilding that exact logger and emitting one error:

* File transport **without** a per-transport format -> the file contains `undefined`
* the same transport **with** `format: combine(json())` -> `{"error":"boom","level":"error","message":"Admin config request failed (POST /api/admin/refresh-tenants)","service":"originate","timestamp":"..."}`

## Why it matters

Production is the only environment that creates these transports, so this is invisible in development and in tests. Every server-side error this service logs to file — including the `fail500` route context lines that KS-1341 and KS-1334 just routed there deliberately — lands as `undefined`.

## Fix shape

Give each File transport `format: combine(json())` (or hoist a shared `json()` into the logger-level format and let Console keep its override). Add a regression cell that builds the production logger against a temp directory, emits one error, and asserts the written line parses as JSON and carries `message` and `service`.

## Not covered

This is a reproduction of the mechanism, not a read of a real production log file on a deployed host. Scope is `services/originate`; other services' loggers were not examined.
</p>
</details>
<!-- linear-review-link -->
<p><a href="https://linear.app/secuura/review/ks-1348-redact-secrets-before-the-originate-file-transports-write-json-cbb593b69a74">Review in Linear</a></p>

