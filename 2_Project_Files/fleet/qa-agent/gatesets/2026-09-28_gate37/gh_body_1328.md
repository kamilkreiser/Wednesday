#1328 KS-1335: rotate the notify window on last_attempted_at, stamped on every attempt
head dbb70fa418afa13daeee5962f3d3bbdc2125e48f

## What this changes

`POST /api/teams/notify` ordered its window by `last_sent_at`, which is written **only after a
SUCCESSFUL send**. A webhook that always failed therefore kept a `NULL` and held the head of every
call, so with `MAX_ROWS` or more permanently-failing rows the starvation KS934 fixed came straight
back. The route's own KNOWN LIMIT comment named this ticket as the reason.

This adds a nullable **`last_attempted_at TIMESTAMPTZ`** to `svc_teams_webhooks`, orders the window
by it `NULLS FIRST`, and stamps it on every **attempt**.

`last_sent_at` keeps its meaning exactly — the last SUCCESSFUL send — and is still what the
published `lastSentAt` field returns. The column is not exposed in any response.

## The two design decisions, and why

**One stamp, not four.** The write goes immediately after the aggregate-deadline guard and **before**
`safeOutboundRequest`, as the first statement in the `try`. One write covers the guard-blocked,
non-ok, catch and success branches. The alternative — a write in each of the four branches — is the
exact structure that created this ticket: a write lived on the success branch alone and the others
were forgotten. A single pre-attempt stamp cannot be forgotten by a branch added later.

**A deadline-SKIPPED row is NOT stamped.** It was never attempted — the loop `continue`s before the
request is made. Leaving it `NULL` keeps it at the head of the next call under `NULLS FIRST`, which
is the priority a skipped row should have. Stamping it would push a never-tried row to the **back**
of the rotation and recreate this ticket's starvation inside its own fix. Cell **R5** pins this, and
an arm that deliberately stamps the skipped branch reds R5 and nothing else.

## Scope

`Refs KS-1335` — not `Closes`.

## Test Evidence

**Touched** (4 files, +87 / −27)
- `services/m365-integration/src/index.ts` (+16 / −7) — rotation key, the stamp, KNOWN LIMIT comment
- `services/m365-integration/src/__tests__/ks934-teams-notify-request-path-bound.test.ts` (+64 / −19)
- `services/api-gateway/src/startup-migrations.ts` (+6 / −1) — the CREATE and the guarded add
- `docker/init/06-m365-tables.sql` (+1 / −0) — the CREATE

**Ran** — in my own worktree detached at `63db8a38354c`, after `npm run build -w packages/shared`.

| step | result |
|---|---|
| RED, test-only (product file sha256 proven identical either side) | **2 failed / 7 passed / 9** — R3 and R5, **by `AssertionError`**, 0 Timeout, 0 Unhandled |
| GREEN, product applied | ks934 file **9 / 9**; `m365-integration` **6 files / 47 passed**; 0 Unhandled |
| `api-gateway` suite (the migration lives there) | **86 files / 781 passed** |
| `tsc --noEmit` | `m365-integration` rc 0, `api-gateway` rc 0 |

**Red first was real**: the rewritten R3 and the new R5 both failed at the untouched tip, by
assertion, with the product file's sha256 measured identical either side of the test-only apply.

**Controls — three arms, each line-exact, each `cmp`-checked non-inert, each restored by sha256**

| arm | predicted | measured |
|---|---|---|
| f — the OLD `ORDER BY last_sent_at` put back | R3 reds | **1 / 9**, R3 ✔ |
| g — the stamp line removed entirely | R3 + R5 red | **3 / 9** — see below |
| h — the deadline-SKIPPED branch ALSO stamped | R5 reds | **1 / 9**, R5 only ✔ |

**Arm g: my prediction was wrong, and the extra red is correct.** I predicted 2 and measured 3 — R2
reds as well. The reason is a real coupling worth stating: with no stamp, **no** row ever gets
`last_attempted_at`, so every row sorts `NULL` and the window falls back to `created_at ASC`. Call 2
then re-attempts exactly the rows call 1 attempted, which is precisely what R2 — an existing KS934
rotation cell — exists to catch. **So this change moves what R2 pins**: the KS934 rotation cell's
meaning is now carried by the new column, and a regression of the stamp is caught by R2 as well as
by R3 and R5. That is extra safety, but it is a change in an existing cell's dependency and it
should not be discovered later by someone wondering why R2 broke.

Arm h is the one that falsifies the skipped-stays-NULL decision: it reds R5 **and only R5**, so R5
discriminates that decision specifically rather than passing for any stamping scheme.

**Write cost, counted exactly; wall-clock NOT measured**
Per row, per call: a deadline-skipped row **0 → 0**; an attempted row that is blocked, non-ok or
throws **0 → 1**; a successful row **1 → 2**. Bounded by `TEAMS_NOTIFY_MAX_ROWS` (default 50; 25 in
the test env). **I did not measure the wall-clock cost against the 1500 ms aggregate deadline, and I
am not going to imply that I did**: the harness mocks `query`, so its cost here is not a real
database round-trip, and there is no real Postgres in this environment. The count above is exact;
the latency is not measured.

**NOT run**
- No real Postgres. The DDL is not executed anywhere in this evidence — only the TypeScript and the
  mocked `query` path are exercised.
- `check:openapi` not run.
- The `information_schema` guarded add-column block is not driven by any test; it is read-only
  reasoning that it matches the shape already used for `last_sent_at` beside it.
- **Push preflight: reported as a ratio below, not as a pass.**
- `m365-integration` has no lint script wired into this evidence; eslint was **run by hand**.

**Migrations + config**
This adds a **boot-migration column**, additive and nullable, at all three DDL sites. No env var, no
config key. It reaches production only through a normal deploy, which stays Kam's. Note for whoever
deploys: `run-migrations.sh` **exits 0 on a failed migration**, so a green runner is not evidence the
column exists — check the schema directly.

**KS 1054 (boot-migration stage order) has an open card, and I did not touch stage order.** Only the
column was added, inside the existing `DO` block, beside the existing `last_sent_at` add.

## Disclosures

- The ticket names `GET /api/teams/webhooks`. **That route does not exist** — `"/api/teams/webhooks'"`
  has **0** hits in `index.ts`. The field is returned by **`GET /api/teams/webhook-config`**
  (`index.ts:1161`, `lastSentAt: r.last_sent_at` at `:1172`).
- **`lastSentAt` is not in the published spec.** `M365TeamsWebhook` is `.passthrough()`, so the field
  reaches the wire only through passthrough, and it has no consumer in the tree besides `index.ts`.
- **This is a RUNTIME change on the Teams notify path, so a §5f live sweep is owed.**
- Prior-work check before editing: `git log -S last_attempted_at` over all history returns **2**
  commits, **both KS934's**, and both only because they wrote the KNOWN LIMIT comment that names this
  ticket. At `63db8a38` the symbol occurs **once**, in that comment. Board search by symbol
  (`last_attempted_at`, `svc_teams_webhooks`, `last_sent_at`) returns this ticket as the top hit and
  no other claimant; control term returns 0. No prior implementation exists.

## Push gate — read from the RAW hook log, not the wrapper's summary

Branch head `dbb70fa418afa13daeee5962f3d3bbdc2125e48f`, first push, confirmed at origin by
`ls-remote` after the push.

```
pre_push_hook_base.test.sh                   28 passed, 0 failed
pre_push_hook_base_fixture_guard.test.sh      6 passed, 0 failed
run_shell_suites.test.sh                     49 passed, 0 failed
shell suites: 60 passed, 0 failed, 0 skipped (of 60)
^FIXTURE BUILD FAILED: 0
OK — 13 code guards passed
VERDICT: MATCHES the declared fleet STOP condition
```

**PREFLIGHT INCOMPLETE — 12/15 legs ran, 3 SKIPPED. Nothing failed.** A ratio, not a pass: the 3
skipped legs are stack-dependent and no local stack was up on `http://localhost:6882`.
**12/15 is not 15/15.** `0` orphaned `login_stub` listeners were left by this worktree.

