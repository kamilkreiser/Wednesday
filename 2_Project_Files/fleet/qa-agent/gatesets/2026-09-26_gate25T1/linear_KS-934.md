KS-934 m365 /api/teams/notify: a serial per-row loop with no LIMIT and no aggregate bound, inside the request handler — N rows x the guard's 10s default
state In Progress

## No aggregate bound over an unbounded row set, in a request handler

`POST /api/teams/notify` loops over every active webhook row **serially**, inside the request handler, with **no** `LIMIT` **on the query** and **no aggregate deadline** over the loop.

The gate confirmed the call site passes **no** `timeoutMs`, so each row rides `safeOutboundRequest`'s 10 s default. Worst case is `rows x 10s` with the HTTP request held open throughout.

KS-914 improved the per-row behaviour — before it, `fetch` was called with no signal at all — but the aggregate was never bounded and still is not.

### Fix shape

A `LIMIT` with paging, or an aggregate deadline over the loop, or move the dispatch off the request path entirely (which is the shape the webhooks dispatcher already uses). **Concurrency is not the fix on its own** — it changes the constant, not the bound.

Red-proof with N rows against a destination that never answers, asserting the handler returns within an aggregate bound rather than N x per-row.

*From the #868 round-1 gate (F4). Filed by s141, 2026-09-06.*
