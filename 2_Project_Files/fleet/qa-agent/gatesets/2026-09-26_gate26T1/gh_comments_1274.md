--- comment 5838576287 by linear[bot] at 2026-09-25T19:48:05Z
<!-- linear-linkback -->
<details>
<summary><a href="https://linear.app/secuura/issue/KS-934/m365-apiteamsnotify-a-serial-per-row-loop-with-no-limit-and-no">KS-934 m365 /api/teams/notify: a serial per-row loop with no LIMIT and no aggregate bound, inside the request handler — N rows x the guard's 10s default</a></summary>
<p>

## No aggregate bound over an unbounded row set, in a request handler

`POST /api/teams/notify` loops over every active webhook row **serially**, inside the request handler, with **no** `LIMIT` **on the query** and **no aggregate deadline** over the loop.

The gate confirmed the call site passes **no** `timeoutMs`, so each row rides `safeOutboundRequest`'s 10 s default. Worst case is `rows x 10s` with the HTTP request held open throughout.

KS-914 improved the per-row behaviour — before it, `fetch` was called with no signal at all — but the aggregate was never bounded and still is not.

### Fix shape

A `LIMIT` with paging, or an aggregate deadline over the loop, or move the dispatch off the request path entirely (which is the shape the webhooks dispatcher already uses). **Concurrency is not the fix on its own** — it changes the constant, not the bound.

Red-proof with N rows against a destination that never answers, asserting the handler returns within an aggregate bound rather than N x per-row.

*From the #868 round-1 gate (F4). Filed by s141, 2026-09-06.*
</p>
</details>
<!-- linear-review-link -->
<p><a href="https://linear.app/secuura/review/ks-934-bound-post-apiteamsnotify-with-a-limit-and-an-aggregate-728a64b7b5ce">Review in Linear</a></p>

--- comment 5841445466 by kksecura at 2026-09-26T00:21:00Z
## FIX ROUND 1 of 2 — F-1274-1 (LIMIT-TRUNC), new head `8e94f5fb3e6d8ef21ba2007fde92d3ea0b5c942d`

Pushed as a **fast-forward** on this branch. The author has wrapped, so this round is another seat's
work; the history before this commit stays its author's. No merge-in of develop — the base this
worktree **contains** is still `4db87c3e4b98`.

### The finding, reproduced at source before choosing a shape
`ORDER BY created_at ASC` is a **fixed** order with no cursor, so "call again" re-selected the same
first `MAX_ROWS` for ever and rows past the limit were never reached by any number of calls. The gate
offered three shapes; measured before choosing:

| shape | measured | verdict |
|---|---|---|
| 1 — drop the LIMIT | re-opens the unbounded row set this PR exists to bound | rejected |
| 2 — fetch `MAX_ROWS + 1`, report truncation | reports it, but the order is still fixed, so a second call still re-sends the same rows | **necessary, not sufficient** |
| 3 — order by `last_sent_at ASC NULLS FIRST` | **the column exists and is maintained** | **necessary, not sufficient** |

**Option 3's column was verified rather than assumed** — the gate could not confirm it existed.
`last_sent_at TIMESTAMPTZ` is declared in **both** DDL sources, `docker/init/06-m365-tables.sql:63`
and `services/api-gateway/src/startup-migrations.ts:361`, **and** there is an
`information_schema`-guarded backfill for existing deploys at `startup-migrations.ts:526-527`. The
route already writes it (`index.ts`, after a successful send) and reads it (the webhook list route).
**No migration is added.** A `migrations/`-only grep finds nothing — this table is created by the two
sources above, which is the trap.

**Both 2 and 3 are shipped**, because each fixes a different half: 2 makes a bounded run *legible*, 3
makes the next call *reach further*. Either alone fails half of the gate's own regression cell.

### The `+1` row is a probe, never a recipient
It is sliced off before the loop, so at most `MAX_ROWS` are ever notified. `N1` asserts both halves —
the LIMIT parameter is `MAX_ROWS + 1` **and** `outbound.calls.length <= MAX_ROWS` — because a LIMIT of
`MAX_ROWS + 1` that also *notified* `MAX_ROWS + 1` would be a regression of the bound itself.

### Cells: 4 → 8
- **R1** a bounded run reports `truncated: true`, `total === MAX_ROWS`, and the probe row is not notified.
- **R1b CONTROL** a complete run reports `truncated: false`. Without it, R1 passes for a route that
  hardcodes `true`.
- **R2** the gate's regression cell: a **second** call attempts the rows the first never reached, and
  attempts them **first** (NULLS FIRST serves a newly registered webhook before older ones).
- **R3** pins the KNOWN LIMIT — see below.

The mock now models the `ORDER BY` **only when the SQL asks for it**, and models the
`UPDATE ... SET last_sent_at = NOW()` write-back. Both matter: a mock that sorted regardless would let
R1/R2 pass for a route that ordered any way at all, and without the write-back a second call could not
observe the rotation, so R2 would be vacuous.

### KNOWN LIMIT, pinned, not smuggled — KS1335
`last_sent_at` is written **only after a successful send**. A permanently failing webhook keeps a NULL
and therefore stays at the head of **every** call; with `MAX_ROWS` or more such rows the starvation
returns in full. **R3 asserts that current behaviour and says in the file that it is a pin, not a fix.**
Fixing it needs either a change to the meaning of the **published** `lastSentAt` field or a new column
in two DDL sources plus a backfill — wider than a fix round. Filed as **KS1335**, whose Done-when
requires R3 to be rewritten in the same change.

### Also in this round
**F-1274-4**: `boot()` moves from `beforeEach` to `beforeAll(boot, 60_000)`, so the first cell no
longer pays the module import under vitest's 10 s hook budget — the timeout the gate saw.
**F-1274-2 is NOT built and NOT filed**, per the gate's TICKET disposition and the coordinator's ruling.

### A comment corrected in place
The route's comment said *"Paging is deliberately NOT added ... The un-attempted remainder is reported
instead of being silently dropped."* The first half still holds. **The second was false as written**,
and is exactly what the gate measured. It is corrected where it stands rather than silently
contradicted by the code beneath it.

### Test Evidence
Base this worktree **CONTAINS**: `4db87c3e4b98` (`merge-base --is-ancestor` YES) — unchanged, no
merge-in. Deps installed and `packages/shared` built in this worktree.

| suite | result |
|---|---|
| ks934 cell | **8 passed / 8** (was 4) |
| m365-integration, BARE at `1a37bde12d55` | **6 files / 42 tests / 0 failed** |
| m365-integration, PATCHED | **6 files / 46 tests / 0 failed** |
| `packages/shared` | **48 files / 941 tests / 0 failed** |
| `tsc --noEmit` | **rc 0, 0 output lines** (both arms) |

**Red proofs — 5 arms, one per new cell, all behaved, zero LOADFAIL.** Each asserts the tamper
APPLIED, reads the verdict from vitest's JSON, restores, and asserts the restore byte-identical. Every
arm is also checked to red **only** the cells it names.

| arm | tamper | reds |
|---|---|---|
| **base** | index.ts at `1a37bde12d55` | N1, R1, R1b, R2 (4 of 8) |
| **noorder** | revert ONLY the ORDER BY | **R2 alone** |
| **noprobe** | revert ONLY the `+1` | N1, R1, R2 |
| **hardcode** | `truncated` reported unconditionally | **R1b alone** |
| **ks1335fix** | write `last_sent_at` on a FAILED attempt too | **R3 alone** |

`noorder` reds R2 alone, so the ordering change is independently load-bearing. `ks1335fix` reds R3
alone, so R3 is a live pin rather than a cell that would pass whatever happened.

**NOT covered:** no local stack, so preflight legs 3, 4 and 8 NOT run. No database. No deploy.
`safeOutboundRequest` is stubbed, as the file's header already explains. The OpenAPI spec is
**not** touched and does not need to be: this operation's 200 response is the generic
`M365Success` `.passthrough()` envelope, which enumerates no `data` fields — the same reason the
original round could add `skipped` and `deadlineExceeded` without a spec change.

