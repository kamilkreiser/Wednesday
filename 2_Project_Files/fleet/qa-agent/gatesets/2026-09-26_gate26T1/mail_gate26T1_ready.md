# CAPTURE for gate26T1 (QA/Secuura-batch1280) — 2026-09-26T00:56:47Z

NO READY MESSAGE ID reached the drafter for any PR of this kit (the seat records carry none; a listing would mark mail seen). Each PR's seat
claims are captured from its PR BODY, its head COMMIT MESSAGE and the seat HANDOVER files below, each verbatim with its TEXT_SHA256.

## #1274 KS-934 (Seat L8 (round 2 by B 30th), T1) — head 8e94f5fb3e6d8ef21ba2007fde92d3ea0b5c942d

#1274 ticket line: #1274 is KS-934.

### PR BODY (gh_body_1274.md) TEXT_SHA256 b44fe8f8854a1df2e5d72edd10ab584d067e27deb9ff0a30e320915442af611f

#1274 KS-934: bound POST /api/teams/notify with a LIMIT and an aggregate deadline
head 8e94f5fb3e6d8ef21ba2007fde92d3ea0b5c942d

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


### HEAD COMMIT MESSAGE TEXT_SHA256 9bf2d17e894d389ea0bc11b6842171a09d70bf1af26bc8a0c0d903612db8c4eb

KS-934: rotate the notify window and report a truncated run

Fix round 1 for #1274, on the gate's blocking finding F-1274-1. The author of the
branch has wrapped, so this is a fast-forward commit by another seat; the history
before it stays its author's.

MEASURED, through the real route: with more rows than the limit, the answer was
{sent: MAX_ROWS, skipped: 0, total: MAX_ROWS, deadlineExceeded: false}. Rows past
the limit were neither attempted nor reported, and because the order was a fixed
created_at ASC, calling again re-notified exactly the same rows for ever. The
newest webhooks were starved permanently and silently. That contradicted the PR's
own obligation 4, its body and its code comment, all three of which said the
remainder was reported.

Two changes, one per half of the defect:

  * fetch MAX_ROWS + 1. The extra row is a PROBE, never a recipient: it is sliced
    off before the loop, and read only so the body can carry `truncated`. An exact
    remaining count would need a second COUNT(*) on the request path, which is the
    work this bound exists to avoid.
  * order by last_sent_at ASC NULLS FIRST, created_at ASC. This rotates the window,
    so a repeat call reaches the rest. NULLS FIRST keeps never-notified rows at the
    head, so a newly registered webhook is served first rather than last.

The column was verified before being relied on: last_sent_at exists in BOTH DDL
sources and has an information_schema-guarded backfill for existing deploys, and
the route already writes and reads it. No migration is added.

KNOWN LIMIT, pinned rather than left implicit: last_sent_at is written only after a
SUCCESSFUL send, so a permanently failing row keeps a NULL and stays at the head of
every call. Cell R3 asserts that current behaviour, and says in the file that it is
a pin and not a fix. Tracked on KS1335, whose Done-when requires R3 to be rewritten
in the same change. Fixing it here would mean either changing the meaning of the
published lastSentAt field or adding a column in two DDL sources plus a backfill,
which is wider than a fix round.

Also in this round: F-1274-4, boot() moves from beforeEach to beforeAll(boot,
60_000), so the first cell no longer pays the module import under vitest's 10 s
hook budget.

The comment that said "Paging is deliberately NOT added ... the un-attempted
remainder is reported instead of being silently dropped" is corrected in place
rather than silently contradicted: the first half still holds, the second was false
as written.

Refs KS-934

Co-Authored-By: Claude Opus 5 <noreply@anthropic.com>



### PUSH LOG STOP COUNTS (READ, bounded region; /Volumes/DevMASTER/!CODING/Secuura/Blockchain/5_Project_History/2026-09-26_seatB-30th/raise/s-b30-ks934-ff-8e94f5fb3e6d-push.out)

```
{
 "log": "/Volumes/DevMASTER/!CODING/Secuura/Blockchain/5_Project_History/2026-09-26_seatB-30th/raise/s-b30-ks934-ff-8e94f5fb3e6d-push.out",
 "lines": 1296,
 "pre_push_hook_base": "28/0",
 "fixture_guard": "6/0",
 "run_shell_suites_region": "49/0",
 "run_shell_suites_prefixed": "49/0",
 "shell_suites": "60 passed, 0 failed, 0 skipped (of 60)",
 "CONTROL_absent_header": "NOT FOUND",
 "fixture_build_failed_lines": 0,
 "verdict_line": "PREFLIGHT INCOMPLETE \u2014 12/15 legs ran, 3 SKIPPED. Nothing failed.",
 "preflight_ran": true,
 "rc": "0",
 "start": "2026-09-26T00:13:17Z PUSH START",
 "end": "2026-09-26T00:20:25Z push rc=0"
}
```

## #1280 KS-1129 (Seat B 29th, T1) — head 12c197a9215e3156d48cf47fbcec09292619cb68

#1280 ticket line: #1280 is KS-1129.

### PR BODY (gh_body_1280.md) TEXT_SHA256 7f8350f441201188afd496115a47868eb7a02cc49836e968954615bfbdf78b6b

#1280 KS-1129: coerce chain.blockNumber so the heal persists a number
head 12c197a9215e3156d48cf47fbcec09292619cb68

## What

`block_number` is a `BIGINT`, and `pg` returns int8 as a **string** by default with no int8 parser anywhere in `Blockchain/Dev`. #1220 fixed anchoring's verify body to report a number; the heal path in originate must not depend on that, because whatever the heal composes is handed to `persistHealedAnchor`, which **writes** it to the document blob — and the gateway's tier-1 read refuses a string (`typeof persistedBlockHeight === 'number'`), so a healed document answers off-chain-only for a document that **is** on chain.

## 🔴 Two persisting sites, not one — and a cell found the second

The ticket, its gate report, and my own first measurement all name only `verification.ts:338`. There is a **second**: v2 heals through its own `healBlobWithChainFact` (`verificationV2.ts:143`), a near-duplicate of `confirmStalePendingAnchor`'s tail carrying the identical `chain.blockNumber ?? blob.blockHeight ?? 0`, whose result goes to `persistHealedAnchor` at `:191` — **a persisted write on the v2 verify path.**

It was not found by reading. It was found by a cell: the cell drove v2, asserted the write was reached, and **read back `"4242"` as a string after the v1 site had already been coerced.** Both sites are coerced here.

The complete sweep of originate's heal compositions, with each traced to its write:

| site | function | reaches a persisted write? | this PR |
|---|---|---|---|
| `verification.ts:368` | `confirmStalePendingAnchor` | **yes** — `persistHealedAnchor` at `:688`, `:1118` | **coerced** |
| `verificationV2.ts:143` | `healBlobWithChainFact` | **yes** — `persistHealedAnchor` at `:191` | **coerced** |
| `verification.ts:607` | chain-first branch | no — `res.json` only | untouched |
| `verification.ts:1058` | chain-first branch | no — `res.json` only | untouched |
| `verificationV2.ts:235` | chain-first branch | no — `res.json` only | untouched |

The three response-only sites each parse their **own** anchoring reply, so there is no single `chain` parse point to coerce at — which is why the coercion is at the sites rather than "once where `chain` is parsed". Typing the published `blockchain` block is ruled out (`secuura-ks1019-blockchain-block-untyped` = a), so those three stay as they are.

**Also measured and NOT in this PR:** `services/anchorStateSync.ts:231`, `:266`, `:346`, `:380` write `blockHeight: anchor.blockNumber || 0` and all four persist. They read `GET /api/anchors/:id`, which is a different endpoint from the one #1220 fixed, so whether they carry the same defect is **unmeasured**. Raised for a ruling rather than folded in silently — those four are KS-1074's writers and a different claim from this ticket's.

## `toBlockHeight`

Mirrors anchoring's `toBlockNumber` (#1220) deliberately, including its two refusals: an **empty** string becomes `null`, never `Number('') === 0` — a zero height is a claim, absence is not; and an unconvertible value becomes `null`, never `NaN`. A real `0` is preserved, and both call sites keep `??` rather than `||`, so a zero height still means zero.

**Behaviour change, stated:** before, `chain.blockNumber = ''` or `'abc'` was persisted verbatim (neither is null, so `??` kept it). Now each falls through to the stored height. That is the intended fix, not a side effect.

## Why the cell file matters more than usual here

**No test file in this suite names `persistHealedAnchor`**, and the closest sibling (`ks584-p3-verify-list.test.ts`) **cannot reach the write**: its row fixture carries no `tenant_id`, so `persistHealedAnchor` returns at `if (!docId || !tenant) return;` before calling `updateDocument`. That is why its incomplete `documentRepo` mock never blows up — and a cell copied from it would assert a property of **a write that never happened**, and pass for that reason.

So every cell asserts the write was **reached** before asserting anything about its content, and one cell is the control for exactly that: with `tenant_id` removed, `updateDocument` is called **0** times while the response still presents `confirmed`. That is what makes "called exactly once" load-bearing rather than decorative.

## Test Evidence

**Touched:** `services/originate/src/routes/verification.ts`, `services/originate/src/routes/verificationV2.ts`, and a new `services/originate/src/__tests__/ks1129-heal-persists-a-number.test.ts`.

**Base:** this worktree contains develop `d7cdecf1d2eef7dde26dd23120e80c9db3f0e4a9`. (develop has since moved to `df5e9f5da6d2`; this worktree does not contain that.)

| arm | result |
|---|---|
| originate BARE — both sources restored **and the new cell file moved aside** | **878 passed / 878, 74 suites**, rc 0 |
| originate PATCHED | **883 passed / 883, 75 suites**, rc 0 (+5 cells) |
| `packages/shared`, `npx vitest run` | **941 passed / 941, 48 files**, rc 0 |
| `tsc --noEmit` in `services/originate` | rc 0 |

Both source restores asserted by sha256 after the bare arm.

**Five red arms, one per conjunct, each reddening exactly the named cells:**

| arm | conjunct falsified | cells that red |
|---|---|---|
| R1 | v1's coercion reverted, `verification.ts` only | V1PERSISTSANUMBER |
| R2 | v2's coercion reverted, `verificationV2.ts` only | PERSISTSANUMBER + FALLTHROUGH |
| R3 | `toBlockHeight` becomes the identity | both PERSISTS cells + COERCION + FALLTHROUGH |
| R4 | the empty string becomes `0` instead of `null` | COERCION + FALLTHROUGH |
| R5 | `persistHealedAnchor` stops requiring a tenant | CONTROL-REACHED |

R1 and R2 are separate arms **because the two compositions are separate functions** — a cell on one proves nothing about the other, and my first version of this suite drove v2 only, so reverting v1 would have reddened nothing.

⚠ **R2 and R3 proved nothing in their first form**, and the runner caught it rather than scoring it. Reverting v2's site left `toBlockHeight` **imported and unused**, which `tsc` refuses; and R3's early `return` left the rest of the function **unreachable**. Both are compile-breaking tampers: the suite never runs, reds nothing, and looks exactly like an inert tamper if only the failed set is read. The runner's `LOADFAIL` verdict (0 passed **and** 0 failed) is what distinguished them. R2 now also removes the import; R3 replaces the whole body.

**NOT run / NOT covered:**
- **Legs 3, 4 and 8 NOT run** (local stack not up): `12/15 ran; legs 3, 4, 8 NOT run (local stack not up)`. No spec moves, so no LEG-8-PORT reading.
- The four `anchorStateSync.ts` writers are **not** covered — see above; they are raised, not fixed.
- The gateway's own tier-1 read is not exercised here; this PR fixes what originate persists, and the gateway is a held surface.
- The JSONB round-trip item on this ticket stays open.

Refs KS-1129

🤖 Generated with [Claude Code](https://claude.com/claude-code)



### HEAD COMMIT MESSAGE TEXT_SHA256 60d009b289f5f353a00eaf1c1ab0d71cb838f766bcb8d57c4189626b4fae625c

KS-1129: coerce chain.blockNumber so the heal persists a number

block_number is a BIGINT and pg returns int8 as a STRING by default, with no
int8 parser anywhere in Blockchain/Dev. #1220 fixed anchoring's verify body to
report a number; the heal path in originate must not depend on that, because
whatever the heal composes is handed to persistHealedAnchor, which WRITES it to
the document blob — and the gateway's tier-1 read refuses a string, so a healed
document answers off-chain-only for a document that IS on chain.

TWO PERSISTING SITES, NOT ONE. The ticket, its gate report and my own first
measurement all name only verification.ts:338. There is a second: v2 heals
through its own healBlobWithChainFact (verificationV2.ts:143), a near-duplicate
of confirmStalePendingAnchor's tail carrying the identical
`chain.blockNumber ?? blob.blockHeight ?? 0`, and its result goes to
persistHealedAnchor at :191 — a persisted write on the v2 verify path. It was
found by a cell: the cell drove v2, asserted the write was reached, and read back
"4242" as a string after the v1 site had already been coerced. Both are coerced
here.

The two response-only sites (verification.ts:607 and :1058, and
verificationV2.ts:235) are deliberately untouched: each builds an honestChain for
res.json with no write, each parses its own anchoring reply, and typing the
published blockchain block is ruled out.

toBlockHeight mirrors anchoring's toBlockNumber, including its two refusals: an
empty string becomes null rather than Number('') === 0, and an unconvertible
value becomes null rather than NaN. A real 0 is preserved, and the call sites
keep ?? rather than ||, so a zero height still means zero.

WHY THE CELL FILE MATTERS MORE THAN USUAL: no test file in this suite names
persistHealedAnchor, and the closest sibling cannot reach the write — its row
fixture carries no tenant_id, so persistHealedAnchor returns before calling
updateDocument. That is why its incomplete documentRepo mock never blows up, and
a cell copied from it would assert a property of a write that never happened.
Every cell here asserts the write was REACHED first, and one cell is the control
for exactly that: with tenant_id removed, updateDocument is not called at all.

originate 878 -> 883, 74 -> 75 suites. Five red arms, one per conjunct, each
isolating one of the two compositions or one refusal of the coercion.

Refs KS-1129

Co-Authored-By: Claude Opus 5 <noreply@anthropic.com>



### PUSH LOG STOP COUNTS (READ, bounded region; /Volumes/DevMASTER/!CODING/Secuura/Blockchain/5_Project_History/2026-09-26_seatB-29th/raise/s-b29-ks1129-12c197a9215e-push.out)

```
{
 "log": "/Volumes/DevMASTER/!CODING/Secuura/Blockchain/5_Project_History/2026-09-26_seatB-29th/raise/s-b29-ks1129-12c197a9215e-push.out",
 "lines": 1305,
 "pre_push_hook_base": "28/0",
 "fixture_guard": "6/0",
 "run_shell_suites_region": "49/0",
 "run_shell_suites_prefixed": "49/0",
 "shell_suites": "60 passed, 0 failed, 0 skipped (of 60)",
 "CONTROL_absent_header": "NOT FOUND",
 "fixture_build_failed_lines": 0,
 "verdict_line": "PREFLIGHT INCOMPLETE \u2014 12/15 legs ran, 3 SKIPPED. Nothing failed.",
 "preflight_ran": true,
 "rc": "0",
 "start": "2026-09-25T20:51:01Z PUSH START",
 "end": "2026-09-25T20:58:07Z push rc=0"
}
```

## #1281 KS-1074 (Seat B 29th, T1) — head c3374e3129ccaca29a9beeafe2d0098ffc86796d

#1281 ticket line: #1281 is KS-1074.

### PR BODY (gh_body_1281.md) TEXT_SHA256 cf46ba53a56705bdb7217c3dcaf16726bcb8216257255c7f8ccf44f6ac69c219

#1281 KS-1074: carry threadToken forward through every anchor rebuild writer
head c3374e3129ccaca29a9beeafe2d0098ffc86796d

## What

`updateDocument` replaces the `blockchain` column **wholesale** — measured at source, not taken from the comment: `documentRepo.ts` builds `const updated = { ...doc, ...updates }`, a **top-level** spread, so `updates.blockchain` replaces `doc.blockchain` entirely and every key not restated is destroyed.

KS-1058 fixed exactly **one** writer, the failure path. **Four more** rebuild the blob as a literal with no `threadToken`, and **two of those are on the SUCCESS path** — so a document that mints a thread token at create and then anchors *normally* lost the cache dashboards read. `state_thread_registry` stays the canonical truth; the blob field exists to avoid that lookup, which is the whole point of KS-1058.

| writer | path | before |
|---|---|---|
| `anchorStateSync.ts:182` (`markDocumentAnchorFailed`) | failure, fail-closed | carried it, but by a **truthy** guard |
| `:229` poller, real txHash | **SUCCESS** | erased |
| `:266` poller, simulated declaration | success | erased |
| `:346` reconcile, heal-to-confirmed | success | erased |
| `:382` reconcile, heal-to-simulated | success | erased |

The ticket's line numbers (`~:191 ~:226 ~:299 ~:327`) are stale; the above are at `d7cdecf1d2ee`. The ticket also cites `documentRepo.ts:480` for the shallow spread — at this base it is `:541`.

## The repro came first, as the ticket requires

**Against the unfixed code, 6 of the 8 cells are RED**, and the two that pass are the two that should: the fail-closed writer (already fixed by KS-1058) and the cell asserting an absent token is not invented. That is the erasure *measured* before the fix rather than argued from the source — which is what this ticket asks for ("Verify at runtime first — this ticket is a source read").

## Three decisions this ticket asks for, each asserted by a cell rather than left to a reader

1. **`!= null`, not truthiness** (the MINOR-2 item). `threadToken` is typed `unknown`, so an empty string or `0` would be discarded by the very write that exists to stop a value being lost. Theoretical for a real hex token, and exactly what a rewrite reintroduces — so it is pinned, and a red arm reverts the guard to truthiness and reddens only that cell.
2. **Carried explicitly, never by spreading `prior`.** A blanket spread would also carry `anchoredAt`, which the blob's own contract says is *"Absent in the KS-520 fail-closed state — nothing was anchored"*. That reasoning is KS-1058's and is preserved.
3. **`simulatedTxRef` is NOT carried.** The two simulated writers already spread `...simFields`, reconstructed from the anchor being read, so nothing needs inheriting; and carrying a simulated marker onto a write that has just recorded a **real confirmed** txHash would assert something false. A cell asserts that a real confirmed write does not inherit a prior `simulatedTxRef`.

## One implementation detail worth reading

In the poller, the prior blob is read **per write**, not once before the loop. The thread-token mint is fire-and-forget at document create and can land **mid-poll**, so a blob read earlier would not carry a token that exists by the time the write happens — and that race is the actual mechanism by which the token goes missing on a normal anchor. In the reconcile path no extra read is needed: `bc` is already this document's prior blob.

## Test Evidence

**Touched:** `services/originate/src/services/anchorStateSync.ts`, plus a new `services/originate/src/__tests__/ks1074-every-rebuild-writer-carries-threadtoken.test.ts`.

**Base:** this worktree contains develop `d7cdecf1d2eef7dde26dd23120e80c9db3f0e4a9`. (develop has since moved to `df5e9f5da6d2`, which this worktree does not contain.)

| arm | result |
|---|---|
| originate BARE — source restored **and the new cell file moved aside** | **878 passed / 878, 74 suites**, rc 0 |
| originate PATCHED | **886 passed / 886, 75 suites**, rc 0 (+8 cells) |
| `packages/shared`, `npx vitest run` | **941 passed / 941, 48 files**, rc 0 |
| `tsc --noEmit` in `services/originate` | rc 0 |

The source restore after the bare arm was asserted by sha256.

**Six red arms, one per writer plus the guard, each reddening exactly its own cell:**

| arm | writer whose carry is removed | cell(s) that red |
|---|---|---|
| A1 | the fail-closed writer | W1 + FALSYTOKEN (both drive that writer) |
| A2 | the poller SUCCESS writer | W2 + NOSIMULATEDTXREFONREAL |
| A3 | the poller SIMULATED writer | W3 |
| A4 | reconcile heal-to-confirmed | W4 |
| A5 | reconcile heal-to-simulated | W5 |
| A6 | the guard reverted to truthiness | FALSYTOKEN only |

Per-writer arms exist **because the repro's six simultaneous reds measure the SET and say nothing about the PARTS** — which is how four writers survived KS-1058.

⚠ **Two arms proved nothing in their first form.** Dropping a spread left `const priorBlob = …` **declared and unused**, which `tsc` refuses: the suite never compiles, reds nothing, and is indistinguishable from an inert tamper unless the runner separates "0 passed **and** 0 failed" from "nothing reddened". It does, and that verdict has caught this class **four times in this session**. Each arm now removes the declaration in the same tamper.

**NOT run / NOT covered:**
- **Legs 3, 4 and 8 NOT run** (local stack not up): `12/15 ran; legs 3, 4, 8 NOT run (local stack not up)`. No spec moves, so no LEG-8-PORT reading.
- These cells drive the writers through their exported functions with `getDocument`/`updateDocument` mocked. **No database is involved**, so this does not prove the column round-trips the value — the JSONB round-trip is a separate open item on KS-1129.
- **`blockHeight: anchor.blockNumber || 0` at these same four sites is NOT touched here.** It is the KS-1129 class on a *different* anchoring endpoint and is filed as **KS-1333**, to be built after this merges — on a ruling that being in the file does not put it in scope.

Refs KS-1074

🤖 Generated with [Claude Code](https://claude.com/claude-code)



### HEAD COMMIT MESSAGE TEXT_SHA256 06ef665e0fd1061e3bdaab80103590b109b6f3c46d63491a7763ae15177feafd

KS-1074: carry threadToken forward through every anchor rebuild writer

updateDocument replaces the blockchain column WHOLESALE — measured at source, not
taken from the comment: documentRepo builds `{ ...doc, ...updates }`, a top-level
spread, so updates.blockchain replaces doc.blockchain entirely and every key not
restated is destroyed.

KS-1058 fixed exactly ONE writer, the failure path. Four more rebuild the blob as
a literal with no threadToken, and TWO of those are on the SUCCESS path — so a
document that mints a thread token at create and then anchors normally lost the
cache dashboards read. state_thread_registry stays the canonical truth; the blob
field exists to avoid that lookup, which is the whole point of KS-1058.

The repro came first, as the ticket requires. Against the unfixed code, 6 of the
8 cells are RED, and the two that pass are the two that should: the fail-closed
writer (already fixed by KS-1058) and the cell asserting an absent token is not
invented. That is the erasure measured before the fix rather than argued from the
source.

Five writers, one cell each, because five separate object literals are five
separate claims — which is how four of them survived KS-1058.

The guard is `!= null`, not truthiness (the MINOR-2 item on this ticket):
threadToken is typed `unknown`, so an empty string or 0 would be discarded by the
very write that exists to stop a value being lost.

The token is carried EXPLICITLY, never by spreading the prior blob — a blanket
spread would also carry anchoredAt, which the blob's own contract says is absent
in the KS-520 fail-closed state. That reasoning is KS-1058's and is preserved.

In the poller the prior blob is read PER WRITE, not once before the loop: the mint
is fire-and-forget at document create and can land mid-poll, so a blob read
earlier would not carry a token that exists by the time the write happens. In the
reconcile path no extra read is needed — `bc` is already the prior blob.

simulatedTxRef is deliberately NOT carried, and that decision is asserted by a
cell. The two simulated writers already spread ...simFields, reconstructed from
the anchor being read; and carrying a simulated marker onto a write that has just
recorded a REAL confirmed txHash would assert something false.

originate 878 -> 886, 74 -> 75 suites. Six red arms, one per writer plus the
truthiness guard, each reddening exactly its own cell.

Refs KS-1074

Co-Authored-By: Claude Opus 5 <noreply@anthropic.com>



### PUSH LOG STOP COUNTS (READ, bounded region; /Volumes/DevMASTER/!CODING/Secuura/Blockchain/5_Project_History/2026-09-26_seatB-29th/raise/s-b29-ks1074-c3374e3129cc-push.out)

```
{
 "log": "/Volumes/DevMASTER/!CODING/Secuura/Blockchain/5_Project_History/2026-09-26_seatB-29th/raise/s-b29-ks1074-c3374e3129cc-push.out",
 "lines": 1305,
 "pre_push_hook_base": "28/0",
 "fixture_guard": "6/0",
 "run_shell_suites_region": "49/0",
 "run_shell_suites_prefixed": "49/0",
 "shell_suites": "60 passed, 0 failed, 0 skipped (of 60)",
 "CONTROL_absent_header": "NOT FOUND",
 "fixture_build_failed_lines": 0,
 "verdict_line": "PREFLIGHT INCOMPLETE \u2014 12/15 legs ran, 3 SKIPPED. Nothing failed.",
 "preflight_ran": true,
 "rc": "0",
 "start": "2026-09-25T21:11:18Z PUSH START",
 "end": "2026-09-25T21:17:54Z push rc=0"
}
```

## #1282 KS-730 (Seat B 29th, T1) — head 34a67a9e48057a0d4939527a4b721a7a5605e4ab

#1282 ticket line: #1282 is KS-730.

### PR BODY (gh_body_1282.md) TEXT_SHA256 2c700c6eaf2c0c6cb4b246ce0b6a90fc45d5367516b90183f5a9b32085077b8b

#1282 KS-730: stop returning the thrown message from systemErrors 500s
head 34a67a9e48057a0d4939527a4b721a7a5605e4ab

## What

**First of three PRs by file**, on the ruling to split KS-730's originate half per file with `systemErrors.ts` first.

Four inline handlers in `routes/systemErrors.ts` returned `err.message` verbatim unless `NODE_ENV === 'production'`, so **`development`, `demo`, `test` and an UNSET `NODE_ENV`** all answered an admin route with raw internal text. KS-727 fixed the two *shared* handlers the same way; these are part of the per-route remainder it enumerated rather than folded in.

| route | site at `d7cdecf1d2ee` |
|---|---|
| `GET /api/system-errors/stats` | `:140` |
| `GET /api/system-errors` | `:162` |
| `PATCH /api/system-errors/:errorId/resolve` | `:172` |
| `POST /api/system-errors/resolve-by-service` | `:188` |

## 🔴 The fix is NOT subtractive here, and that measurement shaped it

KS-727 could simply delete its ternaries because the shared handlers **already logged** `err.message` and `err.stack` at entry — the change lost nothing. Across the three originate files this ticket enumerates, **0 of 65 sites log the error before returning it.** Measured by walking back from each match to its enclosing `catch` and looking for `logger.error|warn|info` in between, against a control that finds **23** `logger.*` calls in a sibling file and 0 for a nonsense pattern.

So deleting the ternary alone would **destroy the diagnostic at every site**. The ticket anticipates this ("where a site does not log, add the log in the same change") but reads as if it were a handful; it is all of them. The log is added in the same change, through **one small local helper** — the ticket's own suggested shape ("a small local helper rather than 67 edited ternaries"), and the only one in which 65 such edits stay reviewable.

Each call site passes **its own context string naming the route**, so a log line is attributable without trusting the caller about which handler produced it. The cells assert that context as a **value**: a helper logging one constant string would satisfy a looser check and make every route's log indistinguishable.

## #1182's two ingest routes are deliberately NOT refactored

They already log inline with their own context strings — verified at source: **2** inline `logger.error` calls, **4** `fail500` call sites. Rewriting an already-merged fix to share a helper is a change with no defect behind it. A red arm confirms the asymmetry rather than leaving it implied: removing the helper's log reds **all four** new log cells and **neither** of #1182's.

## Re-swept to zero

**0 live response-side `NODE_ENV === 'production'` sites remain in this file**, excluding comments and log lines, with the excluded mentions counted separately (1) so the sweep is shown to be able to see lines at all.

## Test Evidence

**Touched:** `services/originate/src/routes/systemErrors.ts` and `services/originate/src/__tests__/ks730a-ingest-500-never-answers-err-message.test.ts` (an existing cell file extended, not a new one added).

**Base:** this worktree contains develop `d7cdecf1d2eef7dde26dd23120e80c9db3f0e4a9`.

| arm | result |
|---|---|
| originate BARE (both files restored pre-edit, sha256-verified) | **878 passed / 878, 74 suites**, rc 0 |
| originate PATCHED | **889 passed / 889, 74 suites**, rc 0 (+11 cells) |
| `packages/shared`, `npx vitest run` | **941 passed / 941, 48 files**, rc 0 |
| `tsc --noEmit` in `services/originate` | rc 0 |

**Five red arms, each isolating one thing:**

| arm | what is reverted | cells that red |
|---|---|---|
| R1–R4 | the original ternary at **one** site | exactly that route's A5 + A6 (15 passed / 2 failed each) |
| R5 | the helper's `logger.error` call | all four A6 cells (13 passed / 4 failed), and **neither** of #1182's |

Four site arms rather than one, because four call sites are four claims — and the whole reason KS-730 exists is that KS-727 fixed the shared handlers and left the inline ones behind. A single arm reverting all four would measure the helper, not each route's wiring to it.

⚠ **R5 took three attempts, and the class is worth naming.** Deleting the log line orphaned **three** identifiers in turn — `logger`, then `context`, then `err` (TS6133) — and each time `tsc` refused the file, so the suite never ran, reds nothing, and looks exactly like an inert tamper. Voiding them one at a time just moved the error; the reliable form is to reference **every** identifier the deleted line used. The runner's `LOADFAIL` verdict (0 passed **and** 0 failed) is what kept this from scoring as a pass. **Sixth instance of this class in this session.**

⚠ **And R5's first expectation was wrong, not the code.** It expected #1182's two ingest cells to red as well; they did not, because those routes log inline. The expectation was corrected and the fact corroborated at source, rather than the arm being loosened.

**NOT run / NOT covered:**
- **Legs 3, 4 and 8 NOT run** (local stack not up): `12/15 ran; legs 3, 4, 8 NOT run (local stack not up)`. No spec moves, so no LEG-8-PORT reading.
- **This is one file of three.** `gdpr.ts` (15 sites) and `adminConfig.ts` (46) follow as separate PRs; the api-gateway and tokenisation sites are held surfaces and not in this round.
- The cells drive the router on a loopback listener with the service layer mocked. They prove the **response and the log**, not that any real error path produces these particular throws.

Refs KS-730

🤖 Generated with [Claude Code](https://claude.com/claude-code)



### HEAD COMMIT MESSAGE TEXT_SHA256 16d0d13a3ec3391f62e14cba5aa8ff7aaed70b809415985ab67965b95d45aa88

KS-730: stop returning the thrown message from systemErrors 500s

The first of three PRs by file. Four inline handlers in routes/systemErrors.ts
returned err.message verbatim unless NODE_ENV === 'production', so development,
demo, test and an UNSET NODE_ENV all answered an admin route with raw internal
text. KS-727 fixed the two SHARED handlers the same way; these are part of the
per-route remainder it enumerated rather than folded in.

THE FIX IS NOT SUBTRACTIVE HERE, and that is the measurement that shaped it.
KS-727 could simply delete its ternaries because the shared handlers already
logged err.message and err.stack at entry. Across the three originate files this
ticket enumerates, 0 of 65 sites log the error before returning it — walked back
from each match to its enclosing catch, against a control that finds 23 logger
calls in a sibling file. So deleting the ternary alone would destroy the
diagnostic at every site. The log is added in the same change, as the ticket
requires, through one small local helper — the ticket's own suggested shape, and
the only one in which 65 such edits stay reviewable.

Each call site passes its own context string naming the route, so a log line is
attributable without trusting the caller about which handler produced it. The
cells assert the context as a VALUE: a helper logging one constant string would
satisfy a looser check and make every route's log indistinguishable.

#1182's two ingest routes are deliberately NOT refactored to use the helper. They
already log inline with their own context strings (verified at source: 2 inline
logger.error calls, 4 fail500 call sites), and rewriting a merged fix to share a
helper is a change with no defect behind it. A red arm confirms the asymmetry
rather than leaving it implied: removing the helper's log reds all four new log
cells and neither of #1182's.

Re-swept to zero, excluding comments and log lines: 0 live response-side
NODE_ENV === 'production' sites remain in this file.

originate 878 -> 889, 74 suites both (an existing cell file was extended rather
than a new one added). Five red arms: the original ternary restored at each of
the four sites separately, each reddening exactly that route's two cells, plus
the helper's log removed.

Refs KS-730

Co-Authored-By: Claude Opus 5 <noreply@anthropic.com>



### PUSH LOG STOP COUNTS (READ, bounded region; /Volumes/DevMASTER/!CODING/Secuura/Blockchain/5_Project_History/2026-09-26_seatB-29th/raise/s-b29-ks730a-34a67a9e4805-push.out)

```
{
 "log": "/Volumes/DevMASTER/!CODING/Secuura/Blockchain/5_Project_History/2026-09-26_seatB-29th/raise/s-b29-ks730a-34a67a9e4805-push.out",
 "lines": 1305,
 "pre_push_hook_base": "28/0",
 "fixture_guard": "6/0",
 "run_shell_suites_region": "49/0",
 "run_shell_suites_prefixed": "49/0",
 "shell_suites": "60 passed, 0 failed, 0 skipped (of 60)",
 "CONTROL_absent_header": "NOT FOUND",
 "fixture_build_failed_lines": 0,
 "verdict_line": "PREFLIGHT INCOMPLETE \u2014 12/15 legs ran, 3 SKIPPED. Nothing failed.",
 "preflight_ran": true,
 "rc": "0",
 "start": "2026-09-25T22:10:18Z PUSH START",
 "end": "2026-09-25T22:17:16Z push rc=0"
}
```

## #1283 KS-730 (Seat B 29th, T1) — head f92b7c19e98d888b39674eb0b39461ed214a37d3

#1283 ticket line: #1283 is KS-730.

### PR BODY (gh_body_1283.md) TEXT_SHA256 190534665c71c0c89c63d5bb57f88990d6211f5b06f0941350f1c9162898278f

#1283 KS-730: stop returning the thrown message from gdpr 500s
head f92b7c19e98d888b39674eb0b39461ed214a37d3

## What

**Second of three PRs by file.** Fifteen inline handlers in `routes/gdpr.ts` returned `err.message` verbatim unless `NODE_ENV === 'production'`, so **`development`, `demo`, `test` and an UNSET `NODE_ENV`** all answered a GDPR route — consent, DSRs, exports, erasure, retention, the deletion log — with raw internal text.

All fifteen now go through one local `fail500(res, context, err)` that logs first and returns the constant body, each call site passing **its own context naming the route**. Re-swept to zero, excluding comments and log lines: **0 live ternaries, 15 helper calls, 15 distinct contexts.**

## 🔴 A constraint in this file had to be measured before it could be set aside

A comment in `gdpr.ts` states there is **deliberately no logger import**, because `utils/logger` pulls in `config.ts`, which throws at module load when `DATABASE_URL` is unset — and that importing it kills three unit suites before a single test runs ("an import-throw reads as a clean zero"). My fix needs to log, so that constraint was directly in the way.

**The constraint was real. Its stated mechanism is not true at this commit.**

| claim | measurement |
|---|---|
| `utils/logger` pulls in `config.ts` | **False.** `utils/logger.ts` imports `winston` and nothing else. |
| importing it throws with `DATABASE_URL` unset | **False.** Importing it with `DATABASE_URL` **and** `JWT_SECRET` both deleted **succeeds**. |
| importing `routes/gdpr` unmocked throws | **True** — `DATABASE_URL environment variable is required`, from its own graph reaching `config.ts` by another path. Unchanged by adding a winston-only import here. |

The only thing that could have refuted this is the suites that import this router. **All six run and pass: 78/78** (`ks754`, `ks694`, `ks444-gdpr-dsr-update-withdraw-guards`, `ks431`, `ks445`, `ks1029`) — none of which sets `DATABASE_URL` itself.

**The comment is corrected in place rather than contradicted silently**, so a reader who finds the import also finds the measurement that licensed it.

## Two kinds of cell, and the difference is stated rather than blurred

- **Four behavioural cells** drive routes end to end over a loopback listener and read the real 500 body and the real log call. They are the strong evidence, and they cover **four of fifteen**.
- **One source cell** pins all fifteen by construction — zero live ternaries, fifteen helper calls, fifteen **distinct** contexts. It is **weaker**: it reads the file rather than the behaviour, and it exists because driving fifteen routes would need fifteen service mocks for no additional discrimination.

## ⚠ My first four routes were measuring my own fixtures

`POST /consent` and `PATCH /dsr/:dsrId` validate a zod body and a UUID **before** calling the service. My fixtures did not satisfy them, so each was refused **400** and the service never threw — the cells were grading my test data, not the handler. Replaced with four routes that reach their service with nothing to satisfy first, verified at source: `GET /dsr/pending`, `GET /retention`, `GET /deletion-log`, `GET /consent/check`.

## Test Evidence

**Touched:** `services/originate/src/routes/gdpr.ts` and a new `services/originate/src/__tests__/ks730b-gdpr-500-never-answers-err-message.test.ts`.

**Base:** this worktree contains develop `d7cdecf1d2eef7dde26dd23120e80c9db3f0e4a9`.

| arm | result |
|---|---|
| originate BARE (`gdpr.ts` restored, the new cell file moved aside) | **878 passed / 878, 74 suites**, rc 0 |
| originate PATCHED | **890 passed / 890, 75 suites**, rc 0 (+12 cells) |
| the six suites that import `routes/gdpr`, run together | **78 passed / 78, 6 suites**, rc 0 |
| `packages/shared`, `npx vitest run` | **941 passed / 941, 48 files**, rc 0 |
| `tsc --noEmit` in `services/originate` | rc 0 |

The `gdpr.ts` restore after the bare arm was asserted by sha256.

**Five red arms:**

| arm | what is reverted | cells that red |
|---|---|---|
| R1–R4 | the original ternary at **one** driven site | that route's B1 + B2, **plus the source cell** (9 passed / 3 failed each) |
| R5 | the helper's `logger.error` call | all four B2 cells (8 passed / 4 failed) |

The source cell reds on every site arm too, and that is listed in each expectation rather than left as an unexplained extra red.

⚠ **R5's anchor found 0 matches on the first run and the runner STOPPED rather than tampering something else** — `gdpr.ts` indents with two spaces where `systemErrors.ts` used four. That is the unique-anchor rule doing its job; a runner that fell back to a fuzzy match would have tampered a line I did not choose.

**NOT run / NOT covered:**
- **Legs 3, 4 and 8 NOT run** (local stack not up): `12/15 ran; legs 3, 4, 8 NOT run (local stack not up)`. No spec moves.
- **Eleven of the fifteen routes are covered by the source cell only**, not behaviourally. Stated above rather than implied by a single count.
- The cells prove the response and the log. They do not prove that any real error path produces these particular throws.
- `adminConfig.ts` (46 sites) follows as PR 3. The api-gateway and tokenisation sites are held surfaces and not in this round.

Refs KS-730

🤖 Generated with [Claude Code](https://claude.com/claude-code)



### HEAD COMMIT MESSAGE TEXT_SHA256 b8131749539acf1c473927b8a85b2cb6f5267699704a11ddb1b30cc282146aad

KS-730: stop returning the thrown message from gdpr 500s

Second of three PRs by file. Fifteen inline handlers in routes/gdpr.ts returned
err.message verbatim unless NODE_ENV === 'production', so development, demo, test
and an UNSET NODE_ENV all answered a GDPR route — consent, DSRs, exports, erasure,
retention, the deletion log — with raw internal text. All fifteen now go through
one local fail500 helper that logs first and returns the constant body, each with
its own context naming the route. Re-swept to zero, excluding comments and log
lines. Fifteen helper call sites, fifteen distinct contexts.

A CONSTRAINT IN THIS FILE HAD TO BE MEASURED BEFORE IT COULD BE SET ASIDE. A
comment here states there is deliberately no logger import because `utils/logger`
pulls in config.ts, which throws at module load when DATABASE_URL is unset, and
that importing it kills suites before a single test runs. The constraint was real;
its stated MECHANISM is not true at this commit. Measured: utils/logger.ts imports
winston and nothing else, and importing it with DATABASE_URL and JWT_SECRET both
deleted SUCCEEDS. What does throw is importing routes/gdpr itself unmocked — its
own graph reaches config.ts by another path, which a winston-only import here does
not change. All six suites that import this router are run and pass (78/78), which
is the only thing that could have refuted it.

The comment is corrected in place rather than contradicted silently: a reader who
finds the import must find the measurement that licensed it.

TWO KINDS OF CELL, and the difference is stated rather than blurred. Four
behavioural cells drive routes end to end over a loopback listener and read the
real 500 body and the real log call; they are the strong evidence and they cover
four of fifteen. A source cell pins all fifteen by construction — zero live
ternaries, fifteen helper calls, fifteen distinct contexts — and is weaker because
it reads the file rather than the behaviour.

MY FIRST FOUR ROUTES MEASURED MY OWN FIXTURES. POST /consent and
PATCH /dsr/:dsrId validate a zod body and a UUID before calling the service; my
fixtures did not satisfy them, so each was refused 400 and the service never
threw. Replaced with four routes that reach their service with nothing to satisfy
first, verified at source.

originate 878 -> 890, 74 -> 75 suites. Five red arms: the original ternary
restored at each of the four driven sites separately, each reddening exactly that
route's two cells plus the source cell, and the helper's log removed reddening all
four log cells.

Refs KS-730

Co-Authored-By: Claude Opus 5 <noreply@anthropic.com>



### PUSH LOG STOP COUNTS (READ, bounded region; /Volumes/DevMASTER/!CODING/Secuura/Blockchain/5_Project_History/2026-09-26_seatB-29th/raise/s-b29-ks730b-f92b7c19e98d-push.out)

```
{
 "log": "/Volumes/DevMASTER/!CODING/Secuura/Blockchain/5_Project_History/2026-09-26_seatB-29th/raise/s-b29-ks730b-f92b7c19e98d-push.out",
 "lines": 1305,
 "pre_push_hook_base": "28/0",
 "fixture_guard": "6/0",
 "run_shell_suites_region": "49/0",
 "run_shell_suites_prefixed": "49/0",
 "shell_suites": "60 passed, 0 failed, 0 skipped (of 60)",
 "CONTROL_absent_header": "NOT FOUND",
 "fixture_build_failed_lines": 0,
 "verdict_line": "PREFLIGHT INCOMPLETE \u2014 12/15 legs ran, 3 SKIPPED. Nothing failed.",
 "preflight_ran": true,
 "rc": "0",
 "start": "2026-09-25T22:30:28Z PUSH START",
 "end": "2026-09-25T22:37:55Z push rc=0"
}
```

## #1284 KS-730 (Seat B 30th, T1) — head dfc2468a547f0bb3d4995404942736312384539b

#1284 ticket line: #1284 is KS-730.

### PR BODY (gh_body_1284.md) TEXT_SHA256 f0a6eb38aeac955f6c59da0d347cc00a3f80a76648a1432b147de6c3d890dd07

#1284 KS-730: stop returning the thrown message from adminConfig 500s
head dfc2468a547f0bb3d4995404942736312384539b

## BLUF
The third and last of KS-730's three files. `routes/adminConfig.ts`'s **46** inline handlers returned
`err.message` verbatim unless `NODE_ENV === 'production'`; all 46 now go through one small local
`fail500` helper that logs the message server-side under a distinct per-route context and answers the
constant body. No product behaviour changes beyond those 46 sites.

**Authorship:** the source change was built by the previous build seat, which has since wrapped. This
seat adopted the branch and worktree unchanged, diagnosed and fixed the failing cell, and raised the
PR — so the PR is this seat's, and the history before this commit is its author's.

## The cell was failing 9 of 12, and the cause was the cell's own fixture
This was re-measured here rather than inherited: `9 failed / 3 passed / 12 total`, reproduced exactly.

All four GET routes the cell drives open their catch with a **pre-existing benign branch**:

```ts
if (err?.message?.includes('does not exist') || err?.code === '42P01') {
  return res.json({ success: true, documentTypes: [] });   // 200
}
fail500(res, 'Admin config request failed (GET /api/admin/document-types)', err);
```

The cell threw `'relation admin_settings does not exist ks730c-private-detail'`, which **contains that
substring**. Every route took the benign branch, answered **200**, and **never reached `fail500`** —
the code this ticket is about never ran. Changing **only** that string, and nothing else, took the
cell from 9/12 to **12/12**. One variable, one outcome.

Worth stating because three cells were *passing* at 9/12 while the fix was never exercised: a fixture
that routes the subject down a different branch yields green cells asserting a property of a code
path that did not run.

Four things now stop that returning silently:
- the trap is written into the file at the `LEAK` definition, naming the branch and why the string
  must not match it;
- **C1 asserts the catch was REACHED** — `mockLoggerError`'s last call must be
  `[route.context, { error: LEAK }]`. A clean body is also what the benign branch and a mock-shaped
  crash produce; only `fail500` logs that pair. **This is the load-bearing assertion in the file.**
- **new `control KS-730 C0`** pins the benign branch: a `does not exist` error still answers 200 and
  never calls `fail500`. Same routes, same mechanism, different message, different answer;
- the `describe` was narrowed from *"the admin-config routes never..."* to *"the 46 converted
  admin-config sites never..."*, which is what is actually proved — see NOT COVERED.

## Test Evidence
Base this worktree **CONTAINS**: `d7cdecf1d2ee` (`merge-base --is-ancestor` YES). `node_modules` and
`packages/shared/dist` present. originate is jest, run **BARE and SERIAL** (`--runInBand`).

**Touched**
- `services/originate/src/routes/adminConfig.ts` (+69 / −46)
- `services/originate/src/__tests__/ks730c-adminconfig-500-never-answers-err-message.test.ts` (new)

**Ran**
| suite | command / cwd | result |
|---|---|---|
| the cell | `npx jest <cell> --runInBand`, `services/originate` | **14 passed / 14** |
| originate, full, BARE | `npx jest --runInBand`, at base, cell absent | **74 suites / 878 tests / 0 failed** |
| originate, full, PATCHED | `npx jest --runInBand` | **75 suites / 892 tests / 0 failed** |
| `packages/shared` | `npx vitest run` | **48 files / 941 tests / 0 failed** |
| `tsc --noEmit` | `-p tsconfig.json`, `services/originate` | **rc 0, 0 output lines** |

Delta is exactly **+1 suite / +14 tests** — this cell and nothing else.

**Red proofs — 4 arms, `arms730c.py`.** Each asserts the tamper APPLIED (byte diff), reads the verdict
from `jest --json`, restores, and asserts the restore is **byte-identical**. **LOADFAIL is graded
separately from PASS**: 0 passed AND 0 failed is never read as "inert".

| arm | tamper | result | named reds |
|---|---|---|---|
| arm0 | none | 14/0 GREEN | — |
| **base** | `adminConfig.ts` restored to `d7cdecf1` | **5/9 RED** | C1 ×4, C2 ×4, C3 |
| **nobenign** | delete `/document-types`' benign branch | **13/1 RED** | **C0 only** |
| **fifthsite** | add a 5th unconditional `err.message` site | **13/1 RED** | **C4 only** |
| **wrongcontext** | `fail500` logs `context + ' TAMPER'` | **6/8 RED** | C1 ×4 **and** C2 ×4 |
| armfinal | none | 14/0 GREEN, source byte-identical to arm0 | — |

Zero LOADFAIL. `fifthsite` only adds, and `wrongcontext` keeps `logger` and `context` referenced, so
no arm could orphan an identifier.

**`packages/shared`'s 941/941 is a statement about this file, not silence about it.** Proved rather
than assumed: binding the cell's listener to `0.0.0.0` makes the ks860 loopback guard go
**1 failed / 24 passed, naming this file at `:78`**; restored byte-identical, **25/25** on both sides.

**NOT run**
- No local stack, so preflight legs 3, 4 and 8 are **NOT run**.
- No database. No integration cell here, and the merged ks1263 integration file was not run — it
  refuses any DSN outside `127.0.0.1:55410-55419`, which is not this seat's range.
- No deploy of any kind. No demo, no UAT.
- The other **42** of the 46 converted sites are covered by the **source** cell (C3), not driven end
  to end. Four are driven. That trade is stated in the file's own header.

**Migrations + config:** none. No migration, no `package.json`, no lockfile, no config file.
**No `withTenant(` call is touched** — `git diff` contains zero such lines (control: 9 exist in the
file), per the KS1304 ruling.

## NOT COVERED — and it is a real gap, now owned
Four handlers in **this same file** return `err.message` in a 500 body with **no `NODE_ENV` guard at
all**, so they leak in **production** too: `:113` `POST /refresh-tenants`, `:1859`
`POST /backfill-certification-metadata`, `:2031` `POST /seed-demo-users`, `:2158`
`POST /migrate-tenant-data`.

They are **pre-existing — 4 at the base `d7cdecf1d2ee`, 4 at this head** — and are a different, worse
class than this ticket's off-production ternary, which is why they are **not fixed here**: KS-730
enumerated 46 ternary sites and this PR converts exactly those.

Filed as **KS1334** (High). `KS-730 C4 SOURCE` pins all four **by enclosing route name** so a fifth
reds — and so that **fixing one also reds**, forcing the list to be updated as part of the fix rather
than drifting. KS1334's Done-when says so explicitly.

## For the gate
The fixture trap above is worth checking in any cell that asserts a catch body: an error string that
happens to match a benign early-return routes the request away from the code under test, and the cell
then passes or fails for reasons unrelated to the change. **C1's REACHED assertion is the load-bearing
one here**; a body-shape assertion alone would not have caught it.

Refs KS-730



### HEAD COMMIT MESSAGE TEXT_SHA256 99f290873488e6685160023dc7e4d670ade2f37d8ef790ddbaff6bc28a57288d

KS-730: stop returning the thrown message from adminConfig 500s

The third and last of KS-730's three files. Forty-six inline handlers returned
`err.message` verbatim unless NODE_ENV === 'production', so development, demo,
test and an UNSET NODE_ENV all answered an admin-configuration route with raw
internal text. All forty-six now route through one small local `fail500` helper
that logs the message server-side against a distinct per-route context and
answers the constant body.

The cell that proves it was failing 9 of 12 when this seat adopted it, and the
cause was the cell's own fixture, not the product code. All four driven routes
open their catch with a pre-existing benign branch that answers 200 for an error
whose message contains 'does not exist' — and the fixture threw exactly such a
message, so no route ever reached the helper. The fixture is now a message that
does not match that branch, the trap is written into the file at its definition,
and three things stop it returning silently:

  * C1 asserts the catch was REACHED (the logger call for that route), not only
    that the answered body looks clean;
  * control C0 pins the benign branch itself — a 'does not exist' error still
    answers 200 and never calls the helper;
  * C4 pins, by enclosing route, the four sites in this file that return
    err.message with no NODE_ENV guard at all. Those are pre-existing (four at
    the base, four here) and are a different, worse class than this ticket's
    off-production ternary, so they are named rather than silently left.

No product behaviour changes beyond the forty-six sites. No `withTenant` call is
touched, per the KS-1304 ruling.

Refs KS-730

Co-Authored-By: Claude Opus 5 <noreply@anthropic.com>



### PUSH LOG STOP COUNTS (READ, bounded region; /Volumes/DevMASTER/!CODING/Secuura/Blockchain/5_Project_History/2026-09-26_seatB-30th/raise/s-b29-ks730c-dfc2468a547f-push.out)

```
{
 "log": "/Volumes/DevMASTER/!CODING/Secuura/Blockchain/5_Project_History/2026-09-26_seatB-30th/raise/s-b29-ks730c-dfc2468a547f-push.out",
 "lines": 1305,
 "pre_push_hook_base": "28/0",
 "fixture_guard": "6/0",
 "run_shell_suites_region": "49/0",
 "run_shell_suites_prefixed": "49/0",
 "shell_suites": "60 passed, 0 failed, 0 skipped (of 60)",
 "CONTROL_absent_header": "NOT FOUND",
 "fixture_build_failed_lines": 0,
 "verdict_line": "PREFLIGHT INCOMPLETE \u2014 12/15 legs ran, 3 SKIPPED. Nothing failed.",
 "preflight_ran": true,
 "rc": "0",
 "start": "2026-09-25T23:49:35Z PUSH START",
 "end": "2026-09-25T23:56:24Z push rc=0"
}
```

## SEAT RECORD /Volumes/DevMASTER/!CODING/Secuura/Blockchain/5_Project_History/2026-09-26_seatL8/measurements/fleet-measurement-RESULT-d7cdecf1.md TEXT_SHA256 a4c421c21ef366bfca8c8c580c187edd16433d0f2bf2d5e306d162fe6de7f576

# FLEET MEASUREMENT — preflight on the COMBINED tree d7cdecf1 (Seat L8, 2026-09-26)

Run at Wednesday's request (19:30Z ANSWER), because her 19:27Z declaration's line
"the first seat to push over it is the measurement" was wrong — a push measures its own
WORKTREE's base. This is the first tree that actually contains the merge.

**Base, stated per the new rule:** `merge-base --is-ancestor d7cdecf1d2ee HEAD` = **YES**.
HEAD = `d7cdecf1d2eef7dde26dd23120e80c9db3f0e4a9`, detached, throwaway worktree, **no push**.

## The four named counts — ALL MATCH the declaration

| count | measured | declared | |
|---|---|---|---|
| `pre_push_hook_base` | **28 / 0** | 28/0 | MATCH |
| `pre_push_hook_base_fixture_guard` | **6 / 0** | 6/0 | MATCH |
| `run_shell_suites` | **49 / 0** | 49/0 | MATCH |
| shell suites | **60 passed, 0 failed, 0 skipped (of 60)** | 60 of 60 | MATCH |

Zero lines starting `FIXTURE BUILD FAILED`. Preflight rc **0**;
`PREFLIGHT INCOMPLETE — 12/15 legs ran, 3 SKIPPED. Nothing failed.` (legs 3, 4, 8 — local stack
not up). That verdict is not a pass and is not quoted as one.

**The expectation is now a measurement.**

## The tree is proven to be the combined one, not a stale checkout

Three independent signs, each measured rather than assumed:

1. `merge-base --is-ancestor d7cdecf1d2ee HEAD` = YES.
2. The two suites the merge modified are the POST-merge copies:
   `run_migrations_failure_exit_code.test.sh` **180 lines** (105 pre-merge) and
   `no_tracked_credentials_root.test.sh` **352 lines** (324 pre-merge) — matching the compare's
   +77 and +31 exactly.
3. Their CELL counts moved with the content — **both of them**:
   `run_migrations_failure_exit_code` **5/0 -> 7/0** (+2 cells, from +77 lines) and
   `no_tracked_credentials_root` **15/0 -> 16/0** (+1 cell, from +31 lines).
   So the new content really RAN; the suites were not merely present in the tree.

That third point is what makes the four unchanged counts meaningful rather than vacuous: the
preflight demonstrably executed changed content and still produced the same quadruple.

## Method notes
- `d7cdecf1` was ABSENT locally, so one `git fetch origin develop` was taken **under
  `.push-lock-25`** — the lock honoured this seat's own 90 s cool-off first, and was held
  **3 seconds** (19:48:39Z -> 19:48:42Z).
- The fetch disturbed nothing another session owns: shared checkout HEAD and the **local `develop`
  branch both still `3bad652d17cf`** (only `origin/develop`, a remote-tracking ref, advanced);
  working tree still 17 untracked / 0 modified; shared `.git/config` sha unchanged.
- Counts read by **bounded region** between consecutive `=== <path> ===` headers, because the log
  carries two summary forms and either parser alone under-reports.


