#1324 KS-1124: the thread-token cache write merges into the blob as persisted now
head 47c4579b0199df1168220fa226805718c26fbbb3

## What this is

Finding **O1** of this ticket, and only O1. `Refs KS-1124` — it does not close the ticket.
**F4 on the same ticket is untouched**; it is a separate card.

## The change

`services/originate/src/routes/documents.ts`, two hunks, **+5 / −2**.

The thread-token mint callback at document create built its write from the **create-time local**
`document` (which has no `blockchain` key) plus the token, and `updateDocument` replaces the
`blockchain` column wholesale. So an anchor accept that had persisted **first** lost its
`txHash`, `status` and `anchorId`. The callback now reads the document back and merges into the
blob **as persisted at write time**.

### It NARROWS the race. It does not close it.

This is still read-then-write: a write landing between the new `getDocument` read and the cache
write can still be lost. An **atomic JSONB merge in `documentRepo`** would close it, and that is
a design choice nobody has ruled. Stating it because the ticket's shape invites reading this as
the fix.

## Test evidence

**Touched:** `services/originate/src/routes/documents.ts` (product, +5/−2) ·
`services/originate/src/__tests__/ks520-anchor-fail-closed.test.ts` (+63, 3 cells).

**Why the cells went into `ks520` rather than a new file** — measured, not preference. A new file
made the whole originate suite go 1 failed: `ks1293-originate-suite-is-hermetic.test.ts`
MANIFEST-DRIFT. Any file that sets `ANCHORING_SERVICE_URL` must be named in that guard's
`SUBJECTS` list, and a create-route cell has to set it to stay off the network. `ks520` is
already a subject and already drives the create route with the same mocks.

**Ran — every figure measured by the author in this worktree, at this tip.** originate is jest.

| | Test Suites | Tests |
|---|---|---|
| originate baseline, before the patch | 89 passed (89) | 1052 passed (1052) |
| originate with the patch | 89 passed (89) | **1055 passed (1055)** |

Delta **+3 tests, +0 suites** — exactly the 3 cells this PR adds. rc 0, zero failing suites.

**Test-only → red → product → green:**

* test section applied **alone**, product file proven unchanged (`git diff --quiet` → rc 0):
  **1 failed / 5 passed of 6** — exactly M1, by assertion (`txHash`, `status`, `anchorId` received
  `undefined`). Not a load failure: 5 cells in the same file passed.
* product section on top: **6 passed (6)**, then the whole suite 1055/1055.

**Discriminating arm** — the merge reverted to the create-time local:

| guard reverted | result | red |
|---|---|---|
| `...(current?.blockchain \|\| document.blockchain \|\| {})` → `...(document.blockchain \|\| {})`, and the now-orphaned `const current` removed with it | 1 failed / 5 passed of 6 | M1 |

Restore asserted by sha256 (`a06f03966714d5ff`, equal after the arm).

⚠ **My first version of this arm was not a result and is disclosed as such.** Reverting only the
spread left `const current` unused → **TS6133** → `Test suite failed to run`, `Tests: 0 total`.
Zero passed **and** zero failed is a load failure, not a red. The declaration exists only to serve
the spread, so the arm removes both — which is exactly this callback's pre-patch shape.

**`tsc`, both ways, over a program PROVEN to contain both changed files.** The package tsconfig
excludes the tests, so a bare run proves nothing — measured: **0** copies of the test file in that
program. Through a temp config inside the package (`types: [jest, node]`): census documents.ts
**1**, ks520 test **1**, bogus-name control **0**, 629 files. Result: **rc 0 and 0 errors at both
base and patched**, error sets byte-identical.

**eslint, run by hand** (the push harness has no LINT leg): **rc 0, 0 problems** at base and
patched.

**NOT run:** no live stack. Playwright, k6, Schemathesis and Akto were not run. The `documents.ts`
create route is an OpenAPI-registered operation, but this hunk changes no request or response
shape — `check:openapi` was not run.

**Migrations + config:** none. No migration, no new env var, no compose change.

## NOT COVERED / disclosed

* **It narrows, it does not close** — see above. The residual is a real, reachable lost update.
* **This path runs only with `STATE_THREAD_NFT_ENABLED=true`.** With the flag off, the callback
  never fires and nothing here is exercised in a deployed environment.
* **RUNTIME change on the create route:** a §5f live sweep is owed before this ticket goes Done.
  That is why this is `Refs`, not `Closes`.
* **"Token" here is the Cardano thread-token NFT cache on a document blob** — not an auth token,
  not a credential. Carried from the brief's own open doubt, in case that distinction matters to
  whoever reviews the exclusion list.
* The cells reach `documentRepo` and the thread-token client through this file's own mocks via
  `jest.requireMock`; nothing talks to a real chain or database.
* F4 on this ticket, and the atomic-merge design question, are both untouched.

## Push gate — quoted from THIS push's raw log

Head `47c4579b0199df1168220fa226805718c26fbbb3`, push rc **0**, `.rc` file **0**.

* `pre_push_hook_base.test.sh` **28 / 0** · `pre_push_hook_base_fixture_guard.test.sh` **6 / 0**
  · `run_shell_suites.test.sh` **49 / 0**
* shell suites **60 passed, 0 failed, 0 skipped (of 60)** · `^FIXTURE BUILD FAILED` **0**
  · **13 code guards passed**
* Zero `FAIL` / `not ok` lines in the 1305-line raw log.

**The preflight did NOT fully run:** `PREFLIGHT INCOMPLETE — 12/15 legs ran, 3 SKIPPED. Nothing
failed.` The three skipped are the stack-dependent legs; no local stack was up for this push.
Nothing failed, but 12/15 is not a pass.

Orphaned `login_stub` listeners left by this push from my worktree: **0**.

## Gate

Author-tested per the 2026-08-25 merge flow. Not merged without a signed GO.

