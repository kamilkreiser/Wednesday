#1274 KS-934: bound POST /api/teams/notify with a LIMIT and an aggregate deadline
head 1a37bde12d55563f77e192519ca7db62461dbf6f

## What and why

`POST /api/teams/notify` looped over every active webhook **serially, inside the request handler**, with **no `LIMIT`** on the query and **no aggregate deadline**. The call site passed no `timeoutMs`, so each row rode `safeOutboundRequest`'s **10 s default** (`packages/shared/src/security/ssrf-guard.ts:486`).

**Measured against the unfixed route: 25 rows took 10048 ms** with the HTTP request held open throughout.

## Both bounds, because neither is sufficient alone

- A **`LIMIT`** bounds the row set and the memory one request costs — but still allows `LIMIT × 10 s` of wall-clock.
- An **aggregate deadline** bounds the wall-clock — but still loads an unbounded row set.
- **Paging is deliberately not added.** It puts *more* work on the request path, which is the opposite of the fix. The un-attempted remainder is **reported** (`skipped`, `deadlineExceeded`) rather than silently dropped, so a caller is never told a partial run was a complete one.
- Each call is given **`min(per-row timeout, time remaining under the aggregate)`**, so one hanging peer cannot consume time the aggregate has already spent.

The three numbers carry their reason in the source rather than being bare constants, and all three are env-overridable because the right values depend on how many webhooks a tenant registers:

| constant | default | why that value |
|---|---|---|
| `TEAMS_NOTIFY_MAX_ROWS` | 50 | bounds the row set and the memory one request costs |
| `TEAMS_NOTIFY_DEADLINE_MS` | 10 000 | **equals the guard's existing single-call default**, so this route's worst case becomes what ONE row already cost — no request gets slower than it could already be, and the N× multiplier is gone |
| `TEAMS_NOTIFY_PER_ROW_TIMEOUT_MS` | 2 000 | one hanging peer cannot starve the rows behind it; at this value at least five rows are still attempted inside the aggregate deadline even if every one hangs |

## Red proof

| cell | at develop `4db87c3e4b98` | with the fix |
|---|---|---|
| **N1** the query carries a `LIMIT` | **RED** — `'SELECT * FROM svc_teams_webhooks WHER…' did not match /LIMIT \s+\$\d+/i` | pass |
| **N2** a slow peer set cannot hold the request past the aggregate deadline, and the remainder is reported | **RED** — **`expected 10048 to be less than 3000`** | pass |
| **N3** no per-call timeout exceeds the budget remaining | **RED** — `expected 'undefined' to be 'number'` | pass |
| **CONTROL** a small fast set still delivers every row | green | green |

The control is green on **both** sides on purpose: the bound is not "skip everything". N1 and N3 also assert their own inputs (more rows available than the limit; calls actually made), so neither can pass vacuously.

## Why `safeOutboundRequest` is stubbed, stated plainly

It is the **SSRF guard** and refuses loopback by design, so a webhook pointed at `127.0.0.1` returns `blocked` in microseconds and no timing cell would measure anything. The stub models the guard's documented contract (`timeoutMs` is a total deadline on the whole operation) and **records the `timeoutMs` it is handed** — which is what makes N3 an assertion about **this route** rather than about the guard. That the guard honours its own deadline is `packages/shared`'s to prove, and it is not re-proved here.

## Test Evidence

**Touched**
- `services/m365-integration/src/index.ts` — the notify route and three new constants.
- `services/m365-integration/src/__tests__/ks934-teams-notify-request-path-bound.test.ts` — new.

**Ran**
- m365-integration **38/38 at develop `4db87c3e4b98` → 42/42 here**, `npx vitest run --no-file-parallelism`, `packages/shared` BUILT. Bare taken in a separate worktree detached at develop.
- The red proof above.
- **`packages/shared` 941/941** (48 files), identical to develop's 941/941. The **ks860 loopback guard was proven to see this new file**: tampering its listener to `0.0.0.0` turned that guard red naming this file by path and line (`…ks934-…test.ts:108`), and green again on restore.
- `npx tsc --noEmit`: **rc 0**.
- Push preflight: **PREFLIGHT INCOMPLETE — 12/15 legs ran, 3 SKIPPED (legs 3, 4, 8 — local stack not up). Nothing failed.**
- Fleet STOP counts — **this worktree does NOT contain `d7cdecf1d2ee`; base `4db87c3e4b98`**, so these describe that tree: `pre_push_hook_base` **28/0** · `pre_push_hook_base_fixture_guard` **6/0** · `run_shell_suites` **49/0** · shell suites **60 passed, 0 failed, 0 skipped (of 60)**. Zero `FIXTURE BUILD FAILED`. Each read from its suite's region, bounded between consecutive `=== <path> ===` headers.

**NOT run**
- No real Teams endpoint and no real `safeOutboundRequest` call — see the stub note above.
- **The `LIMIT` is not paged.** Beyond `MAX_ROWS`, rows are simply not attempted on that request and are reported as such. A caller needing all of them must call again; making that automatic is the "off the request path" design, which is **not** this change.
- **Observed and deliberately NOT changed:** `GET /api/teams/webhook-config` (`index.ts:1163`) also selects active webhooks with no `LIMIT`. It is a different exposure — it makes **no outbound calls**, so there is no `N × 10 s` wall-clock risk, only response size — and it sits behind `requireM365`, which the notify route does not. Out of KS-934's scope; named here rather than silently widened.
- Preflight legs 3, 4, 8. Nothing deployed.

**Migrations + config**
- None. No migration, no config file, no `package.json`, no lockfile, no `*.openapi.ts`. The three new constants read from `process.env` with defaults, so no environment must change for the bound to apply.

Refs KS-934

🤖 Generated with [Claude Code](https://claude.com/claude-code)
