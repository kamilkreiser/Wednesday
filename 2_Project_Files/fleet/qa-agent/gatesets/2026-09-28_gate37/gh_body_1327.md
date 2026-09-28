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

