# CAPTURE for gate37 (QA/Secuura-batch1327) — 2026-09-28T10:56:38Z

NO READY MESSAGE ID reached the drafter for any PR of this kit (a listing would mark mail seen). Each PR's seat claims are captured from its
PR BODY, its COMMIT MESSAGES (over its develop merge-base) and the Seat B 39th records below, each verbatim with its TEXT_SHA256.

## #1327 KS-888 (Seat B 39th (a local-model golden, section-applied by the seat: KS-888 REVOKE — security index.ts: DELETE /api/keys/:id opts into dbSaveApiKey's rethrow inside its own try, answers 503 (infrastructure: SQLSTATE 08/53/57, socket and pool errors, the mint's classifier) or 500 (other) on a failed save, and KEEPS the in-memory revoke; mint and validate unchanged; the existing ks888 cell file edited IN PLACE — header :5-7 and describe :98 reworded, C2 replaced by R1-R4), T1) — head e1c94f60a786e2404a77268118e4687137a01d5a

#1327 ticket line: #1327 is KS-888.

### PR BODY (gh_body_1327.md) TEXT_SHA256 42cd097c3e6e1008b95cd5fe9d5f4003127be049da38e43c22e20a2202d3585f

#1327 KS-888: a revoke whose save fails answers 503 or 500 and is not acknowledged
head e1c94f60a786e2404a77268118e4687137a01d5a

## What this changes

`DELETE /api/keys/:id` opted into `dbSaveApiKey`'s log-only swallow, so a revoke whose INSERT never
landed still answered `200 "API key revoked"`. The key read as active again after a restart, and the
caller had been told the opposite.

The revoke call now opts in with `{ rethrow: true }` **inside the handler's own `try`**, because the
handler takes no `next` and an uncaught throw would end the process. On a failed save it answers
**503 `SERVICE_UNAVAILABLE`** for an infrastructure fault (the mint's classifier: SQLSTATE 08/53/57,
a lost socket, a pool timeout) or **500 `INTERNAL_ERROR`** for anything else, and **the in-memory
revoke is KEPT** — the key stops working in this process even though the row did not persist.

Contract source: the DEFAULT of card `secuura-ks888-revoke-validate-on-failed-save`, option a, acted
on from 18:00 AEST 2026-09-28 because it went unruled. **That card is still OPEN: Kam's word
overrides this contract up to the merge.** It follows his 2026-09-28 06:58 ruling on
`secuura-ks888-failed-key-save-design` ("fix all three routes"); the mint shipped as #1322.

**Mint code is byte-unchanged.** Hunk 1 rewords only the comment *inside* `dbSaveApiKey` that said
"only the mint opts in", which this change makes false.

Two edits in this PR are **hand-written, outside the model pass**, and are marked as such below.

## Scope

`Refs KS-888` — deliberately **not** `Closes`. This closes the **revoke third only**. The validate
third is held pending card `secuura-ks888-validate-usage-write-failure` (open). KS-888 stays
In Progress.

## Test Evidence

**Touched**
- `Blockchain/Dev/services/security/src/index.ts` (+19 / −4)
- `Blockchain/Dev/services/security/src/__tests__/ks888-failed-mint-save-issues-no-key.test.ts` (+32 / −7)

**Ran** — all figures measured by me, in my own worktree detached at `63db8a38354c`, after
`npm run build -w packages/shared` (that package is consumed as built `dist/`, so a baseline taken
before it is not a baseline).

| step | result |
|---|---|
| baseline, untouched tip | `services/security` **26 files / 265 passed**, rc 0 |
| test hunk ALONE (product file sha256 proven identical either side) | **4 failed / 10 passed / 14**, exactly the 3 R1 cases and R4, **by assertion** (`status: 200` received where 503/500 expected), **0 Unhandled, 0 TimeoutError** |
| product applied | ks888 file **14 / 14**; suite **26 files / 270 passed**; 0 Unhandled |
| after both hand edits | ks888 file **14 / 14**; suite **26 files / 270 passed**; 0 Unhandled |
| `tsc --noEmit -p services/security` | rc 0 |
| eslint | rc 0 over **37 files linted** |

**Falsifiability.** Five tamper arms, each a line-exact edit to the **revoke** occurrence only, each
`cmp`-checked as non-inert before the run and each restored with a sha256 equality assertion after:

| arm | predicted | measured |
|---|---|---|
| a — revoke's `{ rethrow: true }` removed | R1 ×3 + R4 red | **4 / 14** ✔ |
| b — `infra` forced false | R1 ×3 red, R4 green | **3 / 14** ✔ |
| c — `infra` forced true | R4 red, R1 green | **1 / 14** ✔ |
| d — **message** alternation dropped, code half kept | only the no-code case reds | **1 / 14**, `pool timeout with no code` ✔ |
| e — **code** alternation dropped, message half kept | the two code-matched cases red | **2 / 14**, `SQLSTATE 08006` + `socket ECONNREFUSED` ✔ |

Arms d and e are one per conjunct of the two-alternation guard, and they name which term carries
which case: the code alternation carries `SQLSTATE 08006` and `socket ECONNREFUSED`; the message
alternation carries `pool timeout with no code`.

Both anchors occur **twice** in the file — the mint's at `:1141`/`:1144` and the revoke's at
`:1293`/`:1295`. The first version of the arm runner matched on substring and silently selected
both; it refused on its own count assertion and the arms were re-cut to line-exact equality. The
mint's lines are untouched in every arm.

**Controls that had to be shown capable of failing**
- `git apply --check --whitespace=error`, per section, no `--recount`, no fuzz: both sections rc 0.
  A one-context-line mutation of **each** section was refused (rc 1). Without that, "it applies" is
  not a measurement. The section split was proven lossless — `sec1 + sec2` is byte-identical to the
  canonical patch.
- eslint rc 0 is **not** vacuous: it linted 37 files, and a planted `var` + `debugger` took it to
  rc 1. (A clean rc 0 from outside the base path would have meant "ignored every file".)

**NOT run**
- No real Postgres. The fault is planted at the mocked `query`; the production path, where
  `dbGetApiKey` returns a fresh DB object, is reasoned, not driven.
- `check:openapi` not run, and **no 503/500 is declared for revoke** in the published spec.
- The gateway's handling of a revoke 503/500 was not read.
- Multi-replica behaviour not exercised.
- **Push preflight: see the ratio printed below — it is reported as a ratio, not as "passed".**
- `services/security` has **no lint script at all**. eslint above was **run by hand** from
  `Blockchain/Dev`; this is not a lint-gate pass.

**Migrations + config**: none. No migration, no env var, no config key. Nothing to deploy-order.

## NOT COVERED — read this before approving

1. **The kept revoke is in-process only.** Other replicas, and this process after a restart, still
   see the key as **active in the database**. The 503/500 tells the caller the revoke was not
   stored, and **nothing retries it**. That is the card default as written, but it was never
   measured against more than one replica.
2. Hunk 1 rewords a comment #1322 added inside `dbSaveApiKey`. If "the mint must stay unchanged" is
   meant to cover that comment too, drop hunk 1 — and the comment then goes stale.
3. **This is a RUNTIME change on the revoke route, so a §5f live sweep is owed.**
4. Whether any other open PR touches these two files: **measured, none.** All 20 open PRs were
   checked through the pulls/files API; 0 overlap. Control: 16 of the 20 touch `Blockchain/Dev/`,
   so the instrument reads files and can return non-zero.

## The two hand-written edits

Neither came from the model pass; both are mine, and both fix a claim this patch falsifies.

1. **Header comment `:5-7`.** It said the file covers the mint route only and that "revoke and
   validate keep the swallow", naming controls C2 and C3. After this patch that is false for revoke
   (C2 has become red cell R4). Rewritten to: the file covers the **mint and revoke** routes;
   **validate** keeps the swallow, pinned by C3 alone.
2. **The `describe` title `:98`**, which still read "revoke and validate are unchanged". Reworded to
   "validate is unchanged". **This renames every `fullName` in the file**, because `describe` is the
   first segment of each. Measured before doing it: the old string has **0** occurrences anywhere
   outside this file, and `KS-888 A4`/`A5` are referenced nowhere else, so nothing pins those names.

## Provenance

The code change is a local-model (Spark) pass. Its READY block, the brief-folder golden and the
checker's canonical `patch.diff` are all **byte-identical**, sha256 `278cbc4558018ca3985bde8d8e1da0f391874c186093a0e495023923f0d065ac`,
5,852 B — verified three ways at raise time, so there was nothing to reconcile.

**The READY was held BY HAND, not by the hold tool**, which refused it: its product-only assumption
does not fit a brief that edits an existing test file in place.

**Both checker passes are disclosed**: the first pass **FAILED** at A3c — a harness class, since
fixed — and the re-check **PASSED 7/7**, with a one-line-dropped mutation proven to fail.

One measurement to flag, because the numbers differ and both are right: the brief predicts
`+29 / −4` on the test file and git's `numstat` reports `+28 / −3`. The patch contains one empty
`-` line immediately followed by an empty `+` line, which git collapses to "unchanged". The brief
counted the patch's raw lines; git counts the minimal diff of the result. Same tree.

## Push gate — read from the RAW hook log, not the wrapper's summary

Branch head `e1c94f60a786e2404a77268118e4687137a01d5a`, first push, confirmed at origin by
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

**PREFLIGHT INCOMPLETE — 12/15 legs ran, 3 SKIPPED. Nothing failed.** Stated as a ratio, not as a
pass: the 3 skipped legs are stack-dependent and no local stack was up on `http://localhost:6882`.
**12/15 is not 15/15.**

`0` orphaned `login_stub` listeners were left by this worktree.



### EVERY COMMIT MESSAGE IN THE CHAIN over 63db8a38354c2f153a4d947c6b6203013c293d7e (oldest first) TEXT_SHA256 1337de189c26a2ff0f2c5106559a94be51b4674fc1f9045cea6f6e4f9732a01f

--- commit e1c94f60a786e2404a77268118e4687137a01d5a
KS-888: a revoke whose save fails answers 503 or 500 and is not acknowledged

DELETE /api/keys/:id opted into the log-only swallow in dbSaveApiKey, so a revoke whose
INSERT never landed still answered 200 "API key revoked". The key then read as active again
after a restart, and the caller had been told otherwise.

The revoke call now opts in with { rethrow: true } inside the handler's own try, because the
handler takes no next and an uncaught throw would end the process. On a failed save it answers
503 SERVICE_UNAVAILABLE for an infrastructure fault (the mint's classifier: SQLSTATE 08, 53,
57, a lost socket, a pool timeout) or 500 INTERNAL_ERROR otherwise, and the in-memory revoke
is KEPT, so the key stops working in this process even though the row did not persist.

Mint code is byte-unchanged. Hunk 1 rewords only the comment inside dbSaveApiKey that said
"only the mint opts in", which this change makes false.

Refs KS-888

Co-Authored-By: Claude Opus 5 <noreply@anthropic.com>



### PUSH LOG STOP COUNTS (READ, bounded region; /Volumes/DevMASTER/!CODING/Secuura/Blockchain/5_Project_History/2026-09-28_seatB-39th/raise/s-b39-ks888revoke-e1c94f60a786-push.out)

```
{
 "log": "/Volumes/DevMASTER/!CODING/Secuura/Blockchain/5_Project_History/2026-09-28_seatB-39th/raise/s-b39-ks888revoke-e1c94f60a786-push.out",
 "lines": 1305,
 "pre_push_hook_base": "28/0",
 "fixture_guard": "6/0",
 "run_shell_suites_region": "49/0",
 "run_shell_suites_prefixed": "49/0",
 "shell_suites": "60 passed, 0 failed, 0 skipped (of 60)",
 "CONTROL_absent_header": "NOT FOUND",
 "fixture_build_failed_lines": 0,
 "verdict_line": "PREFLIGHT INCOMPLETE — 12/15 legs ran, 3 SKIPPED. Nothing failed.",
 "preflight_ran": true,
 "rc": "0",
 "start": "2026-09-28T10:13:47Z PUSH START",
 "end": "2026-09-28T10:19:21Z push rc=0"
}
```

## #1328 KS-1335 (Seat B 39th (seat-written: KS-1335 — m365-integration POST /api/teams/notify rotates its window on a NEW nullable last_attempted_at, added at all three DDL sites (docker init 06, the CORE_MIGRATIONS CREATE, the guarded information_schema add-column block), stamped ONCE after the deadline guard and before safeOutboundRequest (Wednesday's ruling, placement A); the DEADLINE-SKIPPED row is NOT stamped; ks934 R3 rewritten, R5 added), T1) — head dbb70fa418afa13daeee5962f3d3bbdc2125e48f

#1328 ticket line: #1328 is KS-1335.

### PR BODY (gh_body_1328.md) TEXT_SHA256 7e9dc4d430165cb69e8f8741d76b226ee7415d0935be2f84b0f74a608dfc422a

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



### EVERY COMMIT MESSAGE IN THE CHAIN over 63db8a38354c2f153a4d947c6b6203013c293d7e (oldest first) TEXT_SHA256 a6315bc0c325f9f63599b8a8d4106d27bd5943864b35ff413681cb2e8b43099a

--- commit dbb70fa418afa13daeee5962f3d3bbdc2125e48f
KS-1335: rotate the notify window on last_attempted_at, stamped on every attempt

POST /api/teams/notify ordered its window by last_sent_at, which is written only after a
SUCCESSFUL send. A webhook that always failed therefore kept a NULL and held the head of
every call, so with MAX_ROWS or more permanently-failing rows the starvation KS934 fixed
came straight back.

Adds a nullable last_attempted_at TIMESTAMPTZ to svc_teams_webhooks at all three DDL sites
(both CREATEs and the guarded information_schema add-column block), orders the window by it
NULLS FIRST, and stamps it ONCE per row immediately after the aggregate-deadline guard and
before the outbound request. One write covers the guard-blocked, non-ok, catch and success
branches: this ticket exists because a write lived on the success branch alone, so a single
pre-attempt stamp is deliberately not repeated per branch.

A row the aggregate deadline SKIPPED is NOT stamped. It was never attempted, and leaving it
NULL keeps it at the head of the next call under NULLS FIRST, which is the priority a
skipped row should have; stamping it would push a never-tried row to the back and recreate
this ticket's starvation inside its own fix.

last_sent_at keeps its meaning exactly - the last SUCCESSFUL send - and is still what the
published lastSentAt field returns. The migration is additive and nullable.

Refs KS-1335

Co-Authored-By: Claude Opus 5 <noreply@anthropic.com>



### PUSH LOG STOP COUNTS (READ, bounded region; /Volumes/DevMASTER/!CODING/Secuura/Blockchain/5_Project_History/2026-09-28_seatB-39th/raise/s-b39-ks1335-dbb70fa418af-push.out)

```
{
 "log": "/Volumes/DevMASTER/!CODING/Secuura/Blockchain/5_Project_History/2026-09-28_seatB-39th/raise/s-b39-ks1335-dbb70fa418af-push.out",
 "lines": 1305,
 "pre_push_hook_base": "28/0",
 "fixture_guard": "6/0",
 "run_shell_suites_region": "49/0",
 "run_shell_suites_prefixed": "49/0",
 "shell_suites": "60 passed, 0 failed, 0 skipped (of 60)",
 "CONTROL_absent_header": "NOT FOUND",
 "fixture_build_failed_lines": 0,
 "verdict_line": "PREFLIGHT INCOMPLETE — 12/15 legs ran, 3 SKIPPED. Nothing failed.",
 "preflight_ran": true,
 "rc": "0",
 "start": "2026-09-28T10:30:01Z PUSH START",
 "end": "2026-09-28T10:36:06Z push rc=0"
}
```

## SEAT RECORD /Volumes/DevMASTER/!CODING/Secuura/Blockchain/5_Project_History/2026-09-28_seatB-39th/raise/ks888rv.section_1.diff TEXT_SHA256 24e3ea2eb8977ce6ae85a7e49a1396b703cfc7b1222cfc570f342213e9011580

--- a/Blockchain/Dev/services/security/src/index.ts
+++ b/Blockchain/Dev/services/security/src/index.ts
@@ -330,8 +330,9 @@
     ));
   } catch (err: any) {
     logger.error('DB save API key failed', { error: err?.message });
-    // KS-888: only the mint opts in. Revoke and validate keep this log-only swallow: their handlers
-    // take no next, so a throw from here would be an unhandled rejection that ends the process.
+    // KS-888: re-throws only for a caller that opts in, and each caller that opts in catches it in its own try.
+    // Any other caller keeps this log-only swallow: a throw into a handler that takes no next is an unhandled
+    // rejection, and that ends the process.
     if (opts.rethrow) throw err;
   }
 }
@@ -1285,4 +1286,18 @@
   apiKey.isActive = false;
-  await dbSaveApiKey(apiKey);
-  
+  // KS-888 (card secuura-ks888-revoke-validate-on-failed-save, option a, the default from 2026-09-28 18:00):
+  // a revoke whose save did not persist is not acknowledged. The in-memory revoke above is KEPT, so the key
+  // stops working in this process, and the caller is told the revoke was not stored: 503 for an infrastructure
+  // fault (the mint classifier: SQLSTATE 08, 53, 57, a lost socket, a pool timeout), 500 for anything else.
+  // The try is required: this handler takes no next, so an uncaught throw would end the process (KS-888 r2).
+  try {
+    await dbSaveApiKey(apiKey, { rethrow: true });
+  } catch (saveErr: any) {
+    const infra = /^(08|53|57)|^(ECONNREFUSED|ECONNRESET|ETIMEDOUT|EHOSTUNREACH|ENETUNREACH|EPIPE)$/.test(String(saveErr?.code)) || /connection terminated|timeout exceeded when trying to connect|connection timeout|pool is draining|client has encountered a connection error/i.test(String(saveErr?.message));
+    log('error', 'KS-888: API key revoke not stored, the key is revoked in this process only', { keyId: apiKey.id, code: saveErr?.code, infra });
+    return res.status(infra ? 503 : 500).json({
+      success: false,
+      error: { code: infra ? 'SERVICE_UNAVAILABLE' : 'INTERNAL_ERROR', message: 'The API key revoke could not be saved, so it may not survive a restart' },
+    });
+  }
+
   log('info', 'API key revoked', { keyId: apiKey.id });


## SEAT RECORD /Volumes/DevMASTER/!CODING/Secuura/Blockchain/5_Project_History/2026-09-28_seatB-39th/raise/ks888rv.section_2.diff TEXT_SHA256 644aabddb5ea2d3fe332f224f60fce6b2503402ab013bce38d576d79a78f3d3f

--- a/Blockchain/Dev/services/security/src/__tests__/ks888-failed-mint-save-issues-no-key.test.ts
+++ b/Blockchain/Dev/services/security/src/__tests__/ks888-failed-mint-save-issues-no-key.test.ts
@@ -122,8 +122,33 @@
   });
-
+
+  it.each(INFRA)('RED KS-888 R1 %s: a revoke whose save hits an infrastructure fault answers a retryable 503', async (_label, fault) => {
+    const minted = await mint('ks888 revoke infra');
+    state.fault = fault;
+    const res = await fetch(base + '/api/keys/' + minted.body.data.id, { method: 'DELETE', headers: { Authorization: 'Bearer ' + PLATFORM() }, signal: AbortSignal.timeout(3000) });
+    const json = (await res.json()) as { success?: boolean; message?: string; error?: { code?: string } };
+    expect({ minted: minted.status, status: res.status, success: json.success, code: json.error?.code, message: json.message }).toEqual({ minted: 201, status: 503, success: false, code: 'SERVICE_UNAVAILABLE', message: undefined });
+  });
+
+  it('control KS-888 R2: the in-memory revoke is kept when its save fails, so validate answers Key revoked', async () => {
+    const minted = await mint('ks888 revoke kept in memory');
+    state.fault = STRUCTURAL;
+    await fetch(base + '/api/keys/' + minted.body.data.id, { method: 'DELETE', headers: { Authorization: 'Bearer ' + PLATFORM() }, signal: AbortSignal.timeout(3000) });
+    const res = await fetch(base + '/api/keys/validate', { method: 'POST', headers: { 'Content-Type': 'application/json' }, body: JSON.stringify({ key: minted.body.data.key }), signal: AbortSignal.timeout(3000) });
+    const json = (await res.json()) as { data?: { valid?: boolean; reason?: string } };
+    expect({ minted: minted.status, status: res.status, valid: json.data?.valid, reason: json.data?.reason }).toEqual({ minted: 201, status: 200, valid: false, reason: 'Key revoked' });
+  });
+
+  it('control KS-888 R3: a revoke whose save lands answers 200 API key revoked, and the save was issued', async () => {
+    const minted = await mint('ks888 revoke saved');
+    const before = state.inserts;
+    const res = await fetch(base + '/api/keys/' + minted.body.data.id, { method: 'DELETE', headers: { Authorization: 'Bearer ' + PLATFORM() }, signal: AbortSignal.timeout(3000) });
+    expect({ minted: minted.status, status: res.status, message: ((await res.json()) as { message?: string }).message, inserts: state.inserts - before }).toEqual({ minted: 201, status: 200, message: 'API key revoked', inserts: 1 });
+  });
+
-  it('control KS-888 C2: revoke still answers 200 while the same INSERT fails (the swallow is unchanged there)', async () => {
-    const minted = await mint('ks888 revoke control');
+  it('RED KS-888 R4: a revoke whose save fails structurally (42703) answers 500 INTERNAL_ERROR, not API key revoked', async () => {
+    const minted = await mint('ks888 revoke structural');
     state.fault = STRUCTURAL;
     const res = await fetch(base + '/api/keys/' + minted.body.data.id, { method: 'DELETE', headers: { Authorization: 'Bearer ' + PLATFORM() }, signal: AbortSignal.timeout(3000) });
-    expect({ minted: minted.status, status: res.status, message: ((await res.json()) as { message?: string }).message }).toEqual({ minted: 201, status: 200, message: 'API key revoked' });
+    const json = (await res.json()) as { success?: boolean; message?: string; error?: { code?: string } };
+    expect({ minted: minted.status, status: res.status, success: json.success, code: json.error?.code, message: json.message }).toEqual({ minted: 201, status: 500, success: false, code: 'INTERNAL_ERROR', message: undefined });
   });


## SEAT RECORD /Volumes/DevMASTER/!CODING/Secuura/Blockchain/5_Project_History/2026-09-28_seatB-39th/raise/s-b39-ks888revoke-e1c94f60a786-stubs.txt TEXT_SHA256 e3b0c44298fc1c149afbf4c8996fb92427ae41e4649b934ca495991b7852b855



## SEAT RECORD /Volumes/DevMASTER/!CODING/Secuura/Blockchain/5_Project_History/2026-09-28_seatB-39th/raise/s-b39-ks1335-dbb70fa418af-stubs.txt TEXT_SHA256 e3b0c44298fc1c149afbf4c8996fb92427ae41e4649b934ca495991b7852b855



