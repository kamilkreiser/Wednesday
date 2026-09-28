# CAPTURE for gate36 (QA/Secuura-batch1323) — 2026-09-28T08:17:32Z

NO READY MESSAGE ID reached the drafter for any PR of this kit (a listing would mark mail seen). Each PR's seat claims are captured from its
PR BODY, its COMMIT MESSAGES (over its develop merge-base) and the Seat B 38th records below, each verbatim with its TEXT_SHA256.

## #1323 KS-1129 (Seat B 38th (local-model patch, the Spark: KS-1129 item 4 LIVESCAN — api-gateway routes/verification.ts gives the LIVE chain-scan read the three shape guards KS-1069 gave the persisted read + 8 cells inserted into the existing ks1069 cell file), T1) — head 1a509947caf936bcc9b05f7817af6fcbcc974289

#1323 ticket line: #1323 is KS-1129.

### PR BODY (gh_body_1323.md) TEXT_SHA256 d49562f2a4cd89f690758fc3a95371721570723fe73cad817965cbbd0fae996e

#1323 KS-1129: the live chain-scan reply is shape-checked before it can claim on-chain
head 1a509947caf936bcc9b05f7817af6fcbcc974289

## What this is

Item **4** of this ticket's checklist, and only item 4: the **live** chain-scan read in the
api-gateway verify route gets the three shape guards the **persisted** read got in KS 1069.

`Refs KS-1129` — this does not close the ticket. Sites 1 and 2 of the same chain landed as
#1220 (anchoring) and #1280 (originate); the anchorStateSync writers and the stored-blob JSONB
round-trip stay open on the ticket.

## The change

`services/api-gateway/src/routes/verification.ts`, one hunk, **+5 / −3**.

Before, the live reply from anchoring's `GET /api/anchors/verify/:hash` could claim on-chain on:
a **truthy** `verified` (the string `"false"` is truthy), **any** truthy hash (a KS 522
placeholder `tx_sim_…` / `mock_tx_…` / `tx_…` is a non-empty string), and a `Number()`-coerced
height (`-1`, `4242.5` and `"4242"` all became numbers). It now applies the same three guards
the persisted read already carries: `verified === true && !simulated`, a string hash that is
not a placeholder, and a positive integer height.

## Test evidence

**Touched:** `services/api-gateway/src/routes/verification.ts` (product, +5/−3) ·
`services/api-gateway/src/__tests__/ks1069-persisted-anchored-input-shape.test.ts` (+49, 8 cells,
inserted into the existing KS 1069 file rather than a new one).

**Ran — all figures measured by the author in this worktree, at this tip.**

| | Test Files | Tests |
|---|---|---|
| api-gateway baseline, before the patch | 86 passed (86) | 773 passed (773) |
| api-gateway with the patch | 86 passed (86) | **781 passed (781)** |

Delta **+8 tests, +0 files** — exactly the 8 cells this PR adds. `vitest` rc 0, zero `FAIL` lines.

**Test-only → red → product → green**, in that order:

* test section applied **alone**, product file proven unchanged (`git diff --quiet` on
  `verification.ts` → rc 0): **6 failed / 14 passed of 20** — rows L1–L6. Not a load failure:
  14 cells in the same file passed.
* product section applied on top: **20 passed (20)**, then the whole suite 781/781.

**Discriminating arms** — one product guard put back at a time, each tamper placed by an anchor
asserted to occur exactly once, and the restore asserted by sha256 (`ca79933acfeb0b03`, verified
equal after every arm):

| guard reverted | result | rows that red |
|---|---|---|
| `verified === true && !simulated` → truthy | 2 failed / 18 passed of 20 | L1 (string verified), L6 (simulated) |
| the placeholder-hash guard → raw assignment | 1 failed / 19 passed of 20 | L2 (`tx_sim_` hash) |
| the integer-height guard → `Number()` coercion | 3 failed / 17 passed of 20 | L3 (−1), L4 (4242.5), L5 (numeric string) |

None is a load failure — each arm leaves 17–19 cells passing.

**`tsc`, both ways, over a program PROVEN to contain the new cells.** The package tsconfig
excludes `src/__tests__`, so a bare `tsc -p tsconfig.json` says nothing here — measured: **0**
copies of the test file in that program. Through a temp config inside the package with
`exclude` narrowed to `node_modules`/`dist`: test file **1**, product file **1**, bogus-name
control **0**, 513 files. Result: **29 errors at base, 29 patched, and the sorted error sets are
byte-identical**; **0** of them name either changed file. All 29 are pre-existing vitest
mock-typing noise (20× TS2345 `Mock<Procedure | Constructable>` vs `NextFunction`, plus TS18046 /
TS7006 / TS2571) in `csrf.test.ts`, `rateLimitEnforce.test.ts` and four others.

**eslint, run by hand** (the push harness has no LINT leg): rc 0 both ways, **0 errors**,
the same **5 warnings** at base and patched — the identical five, shifted by exactly the +2 net
lines this hunk adds (613→615, 1020→1022, 1139→1141, 1428→1430, 1504→1506). None is mine.

**NOT run:** no live stack, so nothing here exercises anchoring for real — every cell stubs the
live reply. Playwright, k6, Schemathesis and Akto were not run. `check:openapi` was not run and
is not affected: `verification.ts` is not an OpenAPI registration.

**Migrations + config:** none. No migration, no env var, no compose change.

## NOT COVERED / disclosed

* **L5 is a behaviour choice, not a bug fix.** A numeric-**string** live height is now refused,
  strict as the persisted read, carried from the E7 ruling. If a live responder ever sends a
  string height, this route will answer off-chain-only where it previously said on-chain.
  Anchoring's own reply has emitted a number since #1220 (`anchorReadback.ts:134`, `toBlockNumber`),
  so no current producer is affected — but that is a measurement of today's producer, not a
  guarantee. If coercion is preferred for the live read, drop L5 and the height line changes.
* **The "held surface".** A 2026-09-25 comment on this ticket lists "the gateway chain-scan
  readers (a held surface)" among what stays open, and gives no reason. **Wednesday reads that
  hold as lapsed; no recorded hold was found** — the phrase occurs nowhere in her brain, there is
  no card, no open PR touches this file, and api-gateway changes merged on 09-27 (#1305, #1306).
  Flagging it rather than assuming it.
* **This is a RUNTIME change on the verify route, which the demo's on-chain badge reads.**
  A §5f live sweep is owed before this ticket goes Done; that is why this PR is `Refs`, not `Closes`.
* The persisted tier-1 read, the anchorStateSync writers and the JSONB round-trip are untouched.
* No Spark round ran against a live stack; the patch came from a briefed Spark pass (7/7) whose
  `patch.diff` I re-verified byte-identical to the brief-folder golden (sha256 `e651a9001e6eace2`,
  4462 B) before raising.

## Push gate — quoted from THIS push's raw log, not from boilerplate

Head `1a509947caf936bcc9b05f7817af6fcbcc974289`, push rc **0**, `.rc` file **0**.

* `pre_push_hook_base.test.sh` **28 passed / 0 failed**
* `pre_push_hook_base_fixture_guard.test.sh` **6 / 0**
* `run_shell_suites.test.sh` **49 / 0**
* shell suites **60 passed, 0 failed, 0 skipped (of 60)**
* `^FIXTURE BUILD FAILED` **0**
* **13 code guards passed**
* Zero `FAIL` / `not ok` lines in the 1305-line raw log (the grep is shown able to fire).

**The preflight did NOT fully run, and that is stated rather than implied:**
`PREFLIGHT INCOMPLETE — 12/15 legs ran, 3 SKIPPED. Nothing failed.` The three skipped legs are
the stack-dependent ones; no local stack was up for this push. Nothing failed, but 12/15 is not
a pass.

Orphaned `login_stub` listeners left by this push from my worktree: **0**.

## Gate

Author-tested per the 2026-08-25 merge flow. Not merged without a signed GO.



### EVERY COMMIT MESSAGE IN THE CHAIN over d9ce1403d1581ff1584ab799fbbf7fc6f9f8d817 (oldest first) TEXT_SHA256 5424f2d317c14c362d3d342a90645f318616b4f3ee946476feb4009976cd37b9

--- commit 1a509947caf936bcc9b05f7817af6fcbcc974289
KS-1129: the live chain-scan reply is shape-checked before it can claim on-chain

Item 4 of the ticket's checklist only. The live read in the api-gateway verify
route gets the three shape guards the persisted read got in KS 1069: a strict
`verified === true && !simulated`, a string hash that is not a KS 522
placeholder, and a positive integer height.

Refs KS-1129

Co-Authored-By: Claude Opus 5 <noreply@anthropic.com>



### PUSH LOG STOP COUNTS (READ, bounded region; /Volumes/DevMASTER/!CODING/Secuura/Blockchain/5_Project_History/2026-09-28_seatB-38th/raise/s-b38-ks1129live-1a509947caf9-push.out)

```
{
 "log": "/Volumes/DevMASTER/!CODING/Secuura/Blockchain/5_Project_History/2026-09-28_seatB-38th/raise/s-b38-ks1129live-1a509947caf9-push.out",
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
 "start": "2026-09-28T07:21:34Z PUSH START",
 "end": "2026-09-28T07:27:13Z push rc=0"
}
```

## #1324 KS-1124 (Seat B 38th (local-model patch, the Spark: KS-1124 O1 MINTMERGE — originate routes/documents.ts's thread-token cache write re-reads the document and merges into the blob as persisted, not the create-time copy + 3 cells inserted into the existing ks520 cell file; NARROWS the overwrite race, does not close it), T1) — head 47c4579b0199df1168220fa226805718c26fbbb3

#1324 ticket line: #1324 is KS-1124.

### PR BODY (gh_body_1324.md) TEXT_SHA256 b2c9cb3d52c85e3b673be2bf2067725ee4a236cb95fe1a0bdf123fb595b65f68

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



### EVERY COMMIT MESSAGE IN THE CHAIN over d9ce1403d1581ff1584ab799fbbf7fc6f9f8d817 (oldest first) TEXT_SHA256 e5cc3c3cf30467ad8dac9a713553ada4efb03331ec236a99ad8c6c2936d707c0

--- commit 47c4579b0199df1168220fa226805718c26fbbb3
KS-1124: the thread-token cache write merges into the blob as persisted now

Finding O1 only. The mint callback at document create wrote the create-time
local plus the token, and updateDocument replaces the blockchain column
wholesale, so an anchor accept persisted FIRST lost its txHash, status and
anchorId. The callback now reads the document back and merges into that.

It NARROWS the race; it does not close it. This is still read-then-write, so a
write landing between the read and the cache write can still be lost. An atomic
JSONB merge in documentRepo would close it and is an unruled design choice.

Refs KS-1124

Co-Authored-By: Claude Opus 5 <noreply@anthropic.com>



### PUSH LOG STOP COUNTS (READ, bounded region; /Volumes/DevMASTER/!CODING/Secuura/Blockchain/5_Project_History/2026-09-28_seatB-38th/raise/s-b38-ks1124merge-47c4579b0199-push.out)

```
{
 "log": "/Volumes/DevMASTER/!CODING/Secuura/Blockchain/5_Project_History/2026-09-28_seatB-38th/raise/s-b38-ks1124merge-47c4579b0199-push.out",
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
 "start": "2026-09-28T07:32:57Z PUSH START",
 "end": "2026-09-28T07:39:03Z push rc=0"
}
```

## #1325 KS-1227 (Seat B 38th (seat-written, TEST-ONLY: the ks1072 anchor-store witness keeps count-every-stub-request, gains a comment recording the choice, and its message says ASKED; R1's toContain follows it), T2) — head 39f4922d391dabc7f3f99c9c0c8ea2ddde1b596f

#1325 ticket line: #1325 is KS-1227.

### PR BODY (gh_body_1325.md) TEXT_SHA256 abeddc8667c005905b2ffdd98779e3ed824dde73892f73c9eeb48f4b94100319

#1325 KS-1227: keep the count-every-stub-request rule, and say so beside the witness
head 39f4922d391dabc7f3f99c9c0c8ea2ddde1b596f

## What this is

**Test-only.** One helper in one test file. No product file, no contract, no client or
production effect. `Refs KS-1227`.

This is the decision the ticket asks for, taken and recorded — not a behaviour change. Decided
by Wednesday under the 2026-08-07 autonomy grant (items 3–4), reported as a decision rather than
raised as a question.

## The decision: keep "every stub request counts"

`postTier2`'s witness asserts the **whole list** of requests the stub anchor store received during
a verify, not the hits within it. So any extra request reds.

**Kept, because it fails closed.** A hit-only URL filter would keep the cell green while a second,
unexpected caller reached the stub — the R-1029-2 shape, where the tier-2 gate measured 5 witness
reds while tier 2 was answering correctly. R1 already pins the rule by forcing a non-hit request
through and requiring the witness to red, so a future change to a filter cannot pass silently.
The comment beside the witness now says all of this, so the next reader finds a choice rather than
an accident.

A filter would only be worth it if a second file legitimately pointed `ANCHORING_SERVICE_URL` at
this stub. Today only R1 does, on purpose.

## The message reword, and the coupling it carries

The assertion message said *"tier 2 answered"*. The witness proves tier 2 was **asked** exactly
once — it says nothing about what came back, and it is not a tier-1 witness. It now says `ASKED`.

⚠ **R1 asserts that message with `toContain`, so the two lines must change together.** The card
asked for the reword and did not mention this; rewording the witness alone reds R1. R1's expected
substring is now the shorter, less brittle prefix of the new message, ending at `was ASKED once`
(the literal in the file carries the KS 1180 key as file content; it is named descriptively here so
this PR body does not attach that ticket).

The remaining gap — a tier-1 witness with a stub originate that answers plus a 0-read cell — stays
open on KS 1180 and is untouched here.

## Test evidence

**Touched:** `services/api-gateway/src/__tests__/ks1072-the-latest-anchor-selector-documents-a.test.ts`
only, **+14 / −2**. No product file (verified: the PR changes exactly one file).

**Ran — measured by the author in this worktree, at this tip.**

| | Test Files | Tests |
|---|---|---|
| api-gateway baseline at the tip | 86 passed (86) | 773 passed (773) |
| with this change | 86 passed (86) | 773 passed (773) |
| the touched file alone | 1 passed (1) | 8 passed (8) |

Cell count is unchanged, as it should be: this rewords a message and adds a comment; it adds no
cell.

**The coupling is proved, not asserted.** Arm: reword the witness but leave R1's expected
substring at the old text —

| arm | result |
|---|---|
| `:128` reworded, R1's `toContain` left at the old string | **1 failed / 7 passed of 8** — R1 reds, exactly |

Restore verified by sha256 (`20ea46a75bc15a9f`), and the file is 8/8 again afterwards. So the
paired change was necessary, and R1 still discriminates after it.

**`tsc`, both ways, over a program PROVEN to contain the file.** The package tsconfig excludes
the tests — measured: **0** copies of this file in that program, so a bare `tsc -p` is blind here.
Through a temp config inside the package: census file **1**, bogus-name control **0**, 513 files.
Result: **29 errors at base, 29 patched, sorted sets byte-identical, 0 naming the changed file**
(all 29 are the pre-existing vitest mock-typing noise in other test files).

**eslint, run by hand** (no LINT leg in the harness): rc 0, clean at base and with the change.

**NOT run:** no live stack. Playwright, k6, Schemathesis and Akto were not run. `check:openapi`
not run and not affected — this is a test file.

**Migrations + config:** none.

## NOT COVERED

* The tier-1 half of KS 1180 (a stub originate that answers, plus a 0-read cell) is untouched and
  stays open there.
* The two already-closed loose ends of this ticket are confirmed still closed at this tip, not
  re-litigated: the listener detach is in a `finally`, and R2 pins one listener after a status red.
* No judgement is offered on whether a future second consumer of this stub should exist.

## Push gate — quoted from THIS push's raw log

Head `39f4922d391dabc7f3f99c9c0c8ea2ddde1b596f`, push rc **0**, `.rc` file **0**.

* `pre_push_hook_base.test.sh` **28 / 0** · fixture guard **6 / 0** · `run_shell_suites.test.sh` **49 / 0**
* shell suites **60 passed, 0 failed, 0 skipped (of 60)** · `^FIXTURE BUILD FAILED` **0**
  · **13 code guards passed** · zero `FAIL` / `not ok` lines
* **`PREFLIGHT INCOMPLETE — 12/15 legs ran, 3 SKIPPED. Nothing failed.`** The three skipped are
  the stack-dependent legs; no local stack was up. Nothing failed, but 12/15 is not a pass.
* Orphaned `login_stub` listeners from my worktree: **0**.

## Gate

Author-tested per the 2026-08-25 merge flow. Not merged without a signed GO.



### EVERY COMMIT MESSAGE IN THE CHAIN over d9ce1403d1581ff1584ab799fbbf7fc6f9f8d817 (oldest first) TEXT_SHA256 54a689338bb84770a73acb8e1bed0a84d35f82ab9e3b8b7d25a1d082d5711f31

--- commit 39f4922d391dabc7f3f99c9c0c8ea2ddde1b596f
KS-1227: keep the count-every-stub-request rule, and say so beside the witness

The counting rule is DECIDED and kept rather than left implicit: the witness
asserts the whole list of stub requests, so any extra request reds. That fails
closed, where a hit-only URL filter would stay green while a second caller
reached the stub. R1 already pins the rule; the comment now records the choice.

The assertion message said "tier 2 answered". The witness proves tier 2 was
ASKED once, not what came back, so the message now says ASKED. R1 asserts that
message with toContain, so both lines change together -- rewording the witness
alone reds R1.

Test-only. No product file.

Refs KS-1227

Co-Authored-By: Claude Opus 5 <noreply@anthropic.com>



### PUSH LOG STOP COUNTS (READ, bounded region; /Volumes/DevMASTER/!CODING/Secuura/Blockchain/5_Project_History/2026-09-28_seatB-38th/raise/s-b38-ks1227-39f4922d391d-push.out)

```
{
 "log": "/Volumes/DevMASTER/!CODING/Secuura/Blockchain/5_Project_History/2026-09-28_seatB-38th/raise/s-b38-ks1227-39f4922d391d-push.out",
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
 "start": "2026-09-28T07:42:42Z PUSH START",
 "end": "2026-09-28T07:48:11Z push rc=0"
}
```

## #1326 KS-1351 (Seat B 38th (seat-written, TYPES-ONLY: KS-1351 item 1 — packages/shared vc/types.ts declares revoked / revokedAt / revocationReason on a NEW SecuuraCredentialStatus extends VCCredentialStatus and narrows SecuuraCredential.credentialStatus to it; item 2 — vc-issuer credentialRepo.ts:95 let -> const), T2) — head 3f569dfc701c757253aa71ed8b91b81ce9c84c93

#1326 ticket line: #1326 is KS-1351.

### PR BODY (gh_body_1326.md) TEXT_SHA256 3bec301c90a0b801826072652c822cc0b62509eb63e29cb7f76672c6c7e4989e

#1326 KS-1351 item 1: declare the revocation fields on a Secuura status extension
head 3f569dfc701c757253aa71ed8b91b81ce9c84c93

## What this is

**Item 1 of this ticket, and only item 1** (plus its item 2, the one-word `const`). `Refs KS-1351`.
**Types only. No runtime change** — this declares what the code already writes and already reads.

Decided by Wednesday under the 2026-08-07 autonomy grant (items 3–4), so this is reported as a
decision taken, not a question raised.

## The decision: a Secuura extension, not a widened W3C base

`credentialRepo.revoke()` writes `revoked`, `revokedAt` and `revocationReason` into
`credentialStatus`, and the issuer portal reads `credentialStatus?.revoked` to render a
credential's revoked state (`frontend/issuer/src/components/CredentialCard.tsx:119`,
`CredentialDetailModal.tsx:84`). The three fields were undeclared, so four cells that read them
were `TS2339`.

The ticket framed this as "declare the fields, or stop writing them". **"Stop writing them" was
never really open**: it would break the issuer portal's revoked display and change a served
response — `GET /api/credentials/:id` returns the stored credential as is.

So: declare. But **on a new `SecuuraCredentialStatus extends VCCredentialStatus`**, with
`SecuuraCredential` narrowed to it, rather than widening the base. `VCCredentialStatus` is the
W3C-shaped status object; these three fields are ours. The base stays a faithful W3C shape and
Secuura credentials declare what they actually carry.

**It is a narrowing, not a widening** — every `SecuuraCredentialStatus` is a valid
`VCCredentialStatus`, and all three new fields are optional, so nothing that built a status
object before stops compiling.

## Test evidence

**Touched:** `packages/shared/src/vc/types.ts` (+25/−0) ·
`services/vc-issuer/src/repositories/credentialRepo.ts` (+1/−1, `let` → `const`).

**The measurement this ticket asks for: `TS2339` 4 → 0.**

The package tsconfig excludes the tests, so a bare `tsc -p` cannot see any of this — measured:
**0** copies of `credentialRepo.test.ts` in that program. Through a temp config inside the package
(`exclude` narrowed to `node_modules`/`dist`): census test file **1**, `credentialRepo.ts` **1**,
shared `vc/types` **1**, bogus-name control **0**, 428 files.

| | rc | total errors | TS2339 |
|---|---|---|---|
| base | 2 | 4 | **4** |
| with this change | 0 | 0 | **0** |

The four at base are exactly the sites the ticket names — `credentialRepo.test.ts` 72:63, 142:39,
143:39, 144:39 — and they are the *only* errors in that program. Control: a planted
`const x: number = "not-a-number"` takes the run to 5 errors, so the check can still fail.

⚠ **A trap worth recording, because it made my first run read as "the change does nothing".**
`vc-issuer` resolves `@secuura/shared` to the package's **built `dist/`**, not its source. After
editing `packages/shared/src/vc/types.ts` the count was still 4/4, naming `VCCredentialStatus`.
Measured, not guessed: `dist/vc/types.d.ts` held **0** occurrences of the new interface before
`npm run build -w packages/shared` and **2** after, and only then did `tsc` go to 0. **A types-only
change in `packages/shared/src` is invisible to every consumer until that package is rebuilt.**

**eslint, run by hand** (no LINT leg in the harness) — this is item 2, and it is a measured delta:

| | rc | result |
|---|---|---|
| base | 0 | `✖ 1 problem (0 errors, 1 warning)` — the `prefer-const` at `credentialRepo.ts:95` |
| with this change | 0 | **0 problems, 0 `prefer-const` occurrences** |

**Nothing else moved.** `packages/shared` own `tsc`: rc 0, 0 errors. Issuer frontend `tsc`
(the consumer that reads the field): **rc 0, 0 errors** — the narrowing does not break the portal.
vc-issuer suite: **15 files / 140 tests passed, identical at base and with the change** — which is
the right result for a types-only change. A moved cell count here would have meant I had done
something the ticket did not ask for.

**NOT run:** no live stack. Playwright, k6, Schemathesis and Akto were not run. `check:openapi`
not run and not affected — the spec publishes `credentialStatus` as an open record
(`z.record(z.string(), z.unknown())`), so this declaration narrows no published contract.

**Migrations + config:** none.

## NOT COVERED

* **The ticket's own third bullet is not done here:** whether the package tsconfig should stop
  excluding `src/__tests__`. This class of error stays invisible to the package's own `tsc` until
  it does. Left as the ticket left it — it is a harness decision, not a types one.
* This changes no runtime behaviour, so there is nothing for a live sweep to observe. It is `Refs`
  because the tsconfig question above is still open on the ticket.
* 14 files reference `credentialStatus` (positive control: `SecuuraCredential` returns 16 files;
  negative control: 0). The two that read the revocation fields are the frontend components above,
  and they declare their own local type with `revoked?: boolean`, so they were never broken and are
  not changed.

## Push gate — quoted from THIS push's raw log

Head `3f569dfc701c757253aa71ed8b91b81ce9c84c93`, push rc **0**, `.rc` file **0**.

* `pre_push_hook_base.test.sh` **28 / 0** · fixture guard **6 / 0** · `run_shell_suites.test.sh` **49 / 0**
* shell suites **60 passed, 0 failed, 0 skipped (of 60)** · `^FIXTURE BUILD FAILED` **0**
  · **13 code guards passed** · zero `FAIL` / `not ok` lines
* **`PREFLIGHT INCOMPLETE — 12/15 legs ran, 3 SKIPPED. Nothing failed.`** The three skipped are
  the stack-dependent legs; no local stack was up. Nothing failed, but 12/15 is not a pass.
* Orphaned `login_stub` listeners from my worktree: **0**.

## Gate

Author-tested per the 2026-08-25 merge flow. Not merged without a signed GO.



### EVERY COMMIT MESSAGE IN THE CHAIN over d9ce1403d1581ff1584ab799fbbf7fc6f9f8d817 (oldest first) TEXT_SHA256 35ab705fa7db35bd724d2927f7649d4edb16f9f3c052d34d12847b1392c44872

--- commit 3f569dfc701c757253aa71ed8b91b81ce9c84c93
KS-1351 item 1: declare the revocation fields on a Secuura status extension

The repository writes revoked, revokedAt and revocationReason into
credentialStatus, and the issuer portal reads credentialStatus?.revoked to
render a credential's revoked state. The three fields were undeclared, so four
cells that read them were TS2339 over a program that includes the tests.

Declared on a NEW SecuuraCredentialStatus extends VCCredentialStatus, with
SecuuraCredential narrowed to it, rather than widening the W3C-shaped base
type: the base stays a faithful W3C shape and Secuura credentials declare the
fields they actually carry. A narrowing, not a widening -- every
SecuuraCredentialStatus is a valid VCCredentialStatus.

Item 2: credentialRepo.ts:95 is const. It was assigned twice before the ruled
deletion of the LIKE fallback, and once after.

Types only. No runtime change.

Refs KS-1351

Co-Authored-By: Claude Opus 5 <noreply@anthropic.com>



### PUSH LOG STOP COUNTS (READ, bounded region; /Volumes/DevMASTER/!CODING/Secuura/Blockchain/5_Project_History/2026-09-28_seatB-38th/raise/s-b38-ks1351-3f569dfc701c-push.out)

```
{
 "log": "/Volumes/DevMASTER/!CODING/Secuura/Blockchain/5_Project_History/2026-09-28_seatB-38th/raise/s-b38-ks1351-3f569dfc701c-push.out",
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
 "start": "2026-09-28T07:51:49Z PUSH START",
 "end": "2026-09-28T07:57:18Z push rc=0"
}
```

## SEAT RECORD /Volumes/DevMASTER/!CODING/Secuura/Blockchain/5_Project_History/2026-09-28_seatB-38th/b38-item2-ready.txt TEXT_SHA256 fdcb45b7ab4275ce4fc7cc3f1da1fc927e4ca41344d326dc455f115d42a0332c

CONTEXT
ITEM 2 is RAISED. PR #1323, KS-1129 livescan, head 1a509947caf936bcc9b05f7817af6fcbcc974289,
based on d9ce1403, base develop. Re-read at the API AFTER opening: open, merged false,
draft false, base develop, NO closing keyword, exactly its own key hyphenated, title 80 ch
with zero (#n), 2 files +54/-3, attached to KS-1129 only. HOLDING for gate36 -- I merge only
on a signed GO whose subject names Seat B 38th. Nothing deployed.
THE FUSE: 40.4 h, computed at 2026-09-28T07:29Z.

WHAT IT IS
Item 4 of the ticket's checklist and only item 4: the LIVE chain-scan read gets the three
shape guards the persisted read got in KS 1069. Refs, not Closes. Sites 1 and 2 landed as
#1220 and #1280; the anchorStateSync writers and the JSONB round-trip stay open on the ticket.

PROVENANCE, RE-MEASURED BY ME RATHER THAN TAKEN FROM YOUR BRIEF
  READY diff block sha256 e651a9001e6eace277dfcb6de351fbf40d77cfe5bebf54b5a5aac9992cf96af0
  == the checker patch.diff, AND == the brief-folder golden (cmp rc 0 both).
  Control: compared against KS 1124's golden it DIFFERS, so cmp is not answering identical
  to everything. raise34 reported the READY-vs-patch difference as "(none - they are
  identical)" and confirmed split-source == patch.diff, which is the raise28 defect guarded.

FIGURES, ALL MINE, IN THE ORDER test-only -> red -> product -> green
  api-gateway BASELINE                86 files / 773 tests / 0 failed   (rc 0)
  api-gateway WITH THE PATCH          86 files / 781 tests / 0 failed   (rc 0)
  delta                               +8 tests, +0 files == exactly the 8 cells added
  test section ALONE, product proven unchanged (git diff --quiet rc 0):
                                      6 failed / 14 passed of 20  -- rows L1-L6
                                      NOT a load failure: 14 cells in the same file passed
  product applied on top, file        20 passed of 20
  whole suite                         781 passed, zero FAIL lines

DISCRIMINATING ARMS -- one product guard reverted at a time, each tamper placed by an anchor
asserted to occur exactly ONCE, each restore asserted by sha256 (ca79933acfeb0b03, equal after
every arm), and none of them a load failure (17-19 cells still pass in each):
  verified === true && !simulated -> truthy     2 failed / 18 passed   L1, L6
  placeholder-hash guard -> raw assignment      1 failed / 19 passed   L2
  integer-height guard -> Number() coercion     3 failed / 17 passed   L3, L4, L5
Each matches the arm figures your brief predicted, exactly.

TSC, BOTH WAYS, OVER A PROGRAM PROVEN TO CONTAIN THE NEW CELLS
  The package tsconfig excludes src/__tests__, so a bare tsc -p proves nothing here -- MEASURED:
  0 copies of the test file in that program. Through a temp config INSIDE the package:
  census test file 1, product file 1, bogus-name control 0, 513 files.
  29 errors at base, 29 patched, the SORTED ERROR SETS BYTE-IDENTICAL, and 0 of them name
  either changed file. All 29 are pre-existing vitest mock-typing noise (20x TS2345
  Mock<Procedure|Constructable> vs NextFunction, plus TS18046/TS7006/TS2571) in csrf.test.ts,
  rateLimitEnforce.test.ts and four others.

ESLINT RUN BY HAND (the harness has no LINT leg)
  rc 0 both ways, 0 errors, the SAME 5 warnings at base and patched -- the identical five,
  shifted by exactly the +2 net lines the hunk adds (613->615, 1020->1022, 1139->1141,
  1428->1430, 1504->1506). None is mine.

PUSH GATE, from THIS push's RAW 1305-line log via gatelines34, not from the curated wrapper
  28/0 - 6/0 - 49/0 - shell suites 60 passed, 0 failed, 0 skipped (of 60)
  ^FIXTURE BUILD FAILED 0 - 13 code guards passed - VERDICT MATCHES
  rc 0, .rc file 0, ZERO FAIL/not-ok lines (the grep shown able to fire on a planted line).
  PREFLIGHT INCOMPLETE -- 12/15 legs ran, 3 SKIPPED, nothing failed. The 3 are the
  stack-dependent legs; no local stack was up. Stated in the PR body, not implied away.
  Lock taken and released by b38 inside one invocation (pid 89974). 0 orphaned login_stub
  listeners from my worktree.

DISCLOSED IN THE PR BODY
  - L5 is a BEHAVIOUR CHOICE, not a bug fix: a numeric-STRING live height is now refused,
    strict as the persisted read, carried from the E7 ruling. If a live responder ever sends a
    string height the route says off-chain-only where it said on-chain. Anchoring has emitted a
    number since #1220 (anchorReadback.ts:134) -- today's producer, not a guarantee.
  - The "held surface": I quote your reading verbatim -- "Wednesday reads that hold as lapsed;
    no recorded hold was found" -- with the 09-25 comment's own words and the four facts
    behind it. Flagged, not assumed.
  - RUNTIME change on the verify route, which the demo's on-chain badge reads: 5f live sweep
    owed. That is why it is Refs.
  - verification.ts is not an OpenAPI registration: check:openapi unaffected, not run.
  - No live stack; every cell stubs the live reply. Playwright, k6, Schemathesis, Akto not run.
  - No migration, no env var, no compose change.

MY OWN DEFECT THIS ITEM, DISCLOSED
  My first apply-check read "rc=0" for the control that had actually REFUSED. $? after a pipe
  measures tail, and this shell is zsh, so ${PIPESTATUS[1]} is empty -- exactly the trap your
  brief warned about and I walked into it anyway. Redone in a bash script file: sections rc 0,
  control rc 1. Every rc in this mail comes from that rewrite, not the first reading.

KEYSCAN
  PASS: subject 80 ch, 88 as it will LAND, hyphenated set == own set == [KS-1129], foreign keys
  un-hyphenated (ks1069). CONTROL: re-hyphenating one foreign key makes it FAIL rc 1.

MEANWHILE
ITEM 3 (KS-1124 mintmerge) is building now -- raise34 worktree + npm ci running. Its READY
block is already verified byte-identical to the canonical and to the golden, and the two
sections rejoin to the canonical exactly. originate is JEST, not vitest (your trap 2).

NEEDED-BY
Nothing blocking. #1323 waits for gate36.


## SEAT RECORD /Volumes/DevMASTER/!CODING/Secuura/Blockchain/5_Project_History/2026-09-28_seatB-38th/b38-item3-ready.txt TEXT_SHA256 f4b9de1e4a0274e8bd0953355084e433b347c86d588c5f45e64a51e06c48c6a8

CONTEXT
ITEM 3 RAISED. PR #1324, KS-1124 mintmerge, head 47c4579b0199df1168220fa226805718c26fbbb3,
based on d9ce1403, base develop. Re-read at the API after opening: open, merged false, draft
false, base develop, NO closing keyword, exactly its own key hyphenated, title 75 ch with zero
(#n), 2 files +68/-2, attached to KS-1124 only. WAITING for gate36. Nothing deployed.
THE FUSE: 40.2 h, computed at 2026-09-28T07:40Z.

PROVENANCE, RE-MEASURED BY ME
  READY block sha256 54fb96afa36b5a51beebaf1581863375e2b70305c0c04452425da8b7029b7404
  == the checker patch.diff AND == the brief-folder golden (cmp rc 0 both). raise34 reported the
  READY-vs-patch difference as "(none)" and confirmed split-source == patch.diff. Both tamper
  controls FIRED rc 1. The two sections rejoin to the canonical byte for byte.

FIGURES, ALL MINE (originate is JEST -- your trap 2)
  BASELINE            89 suites / 1052 tests / 0 failed   rc 0
  WITH THE PATCH      89 suites / 1055 tests / 0 failed   rc 0
  delta               +3 tests, +0 suites == exactly the 3 cells added
  test-only ALONE, product proven unchanged (git diff --quiet rc 0):
                      1 failed / 5 passed of 6 -- exactly M1, BY ASSERTION
                      (txHash, status, anchorId all received undefined)
                      NOT a load failure: 5 cells in the same file passed
  product on top      6 passed of 6, then the whole suite 1055/1055, 0 failing suites
Your harness figures predicted red 1/6 M1 -> 6/6 and 89/1052 -> 89/1055. Mine land exactly there.

THE ARM, AND MY OWN DEFECT IN BUILDING IT -- DISCLOSED
  MY FIRST ARM WAS A LOAD FAILURE, NOT A RED, AND IT WOULD HAVE READ AS "the guard does nothing".
  Reverting ONLY the merge spread left `const current` unused -> TS6133 -> "Test suite failed to
  run", Tests: 0 total. ZERO passed AND ZERO failed measures nothing. The declaration exists only
  to serve the spread, so the arm must remove BOTH -- which is exactly this callback's pre-patch
  shape. Rebuilt:
     spread + decl reverted -> 1 failed / 5 passed of 6, red M1, MATCH
  Restore asserted by sha256 a06f03966714d5ff, equal after the arm. My parser also returned
  None/None on the first run, and I read the raw jest output rather than believing the None.

TSC, BOTH WAYS, PROGRAM PROVEN TO CONTAIN BOTH CHANGED FILES
  Census: documents.ts 1, ks520 test 1, bogus-name control 0, 629 files. The PACKAGE tsconfig
  alone contains 0 copies of the test file, so a bare tsc -p proves nothing here.
  rc 0 and 0 errors at BOTH base and patched; error sets byte-identical.

ESLINT BY HAND (no LINT leg in the harness): rc 0, 0 problems, base and patched.

PUSH GATE, from THIS push's RAW 1305-line log via gatelines34
  28/0 - 6/0 - 49/0 - shell suites 60 passed, 0 failed, 0 skipped (of 60)
  ^FIXTURE BUILD FAILED 0 - 13 code guards passed - VERDICT MATCHES
  rc 0, .rc file 0, ZERO FAIL/not-ok lines.
  PREFLIGHT INCOMPLETE -- 12/15 legs ran, 3 SKIPPED, nothing failed (the stack-dependent legs;
  no local stack up). Stated in the PR body. Lock taken + released by b38 in one invocation
  (pid 50193). 0 orphaned login_stub listeners from my worktree.

DISCLOSED IN THE PR BODY
  - IT NARROWS THE RACE, IT DOES NOT CLOSE IT, said plainly and twice: still read-then-write, so
    a write landing between the new getDocument and the cache write can still be lost. An atomic
    JSONB merge in documentRepo would close it and is an unruled design choice.
  - F4 untouched (a separate card for Kam).
  - Why the cells live in ks520 and not a new file: MEASURED, not preference -- a new file made
    ks1293's hermetic MANIFEST-DRIFT guard red, because any file setting ANCHORING_SERVICE_URL
    must be in its SUBJECTS list.
  - The path runs only with STATE_THREAD_NFT_ENABLED=true; with the flag off nothing here is
    exercised in a deployed environment.
  - RUNTIME change on the create route: 5f live sweep owed. That is why it is Refs.
  - Your README doubt carried over: "token" here is the Cardano thread-token NFT cache on a
    document blob, not an auth token or credential.
  - No migration, no env var, no compose change. No live stack; mocks via jest.requireMock.

KEYSCAN
  PASS: subject 75 ch, 83 as it lands, hyphenated set == own == [KS-1124], foreign keys
  un-hyphenated (ks1293, ks520). CONTROL: hyphenating one makes it FAIL rc 1.

MEANWHILE
ITEM 4 (KS-1227) worktree is building. ONE THING I FOUND READING AHEAD that your card does not
mention: the card asks me to reword the witness message at ks1072...:128, but R1 at :196 ASSERTS
that exact string with toContain. Rewording :128 alone would red R1. I will change both in the
same patch and say so.

NEEDED-BY
Nothing blocking. #1323 and #1324 both wait for gate36.


## SEAT RECORD /Volumes/DevMASTER/!CODING/Secuura/Blockchain/5_Project_History/2026-09-28_seatB-38th/b38-item4-ready.txt TEXT_SHA256 5853660438fabdf45be47c7016f2639d8881ab5cf473686cedf356e14ed758f7

CONTEXT
ITEM 4 RAISED. PR #1325, KS-1227, head 39f4922d391dabc7f3f99c9c0c8ea2ddde1b596f, based on
d9ce1403, base develop. Re-read at the API after opening: open, merged false, draft false, base
develop, NO closing keyword, exactly its own key hyphenated, title 78 ch with zero (#n),
1 file +14/-2, NO PRODUCT FILE, attached to KS-1227 only. WAITING for gate36. Nothing deployed.
THE FUSE: 39.9 h, computed at 2026-09-28T07:50Z.

THE DECISION, TAKEN AND RECORDED (your 2026-08-07 autonomy grant, items 3-4)
KEEP "every stub request counts". It fails CLOSED: the witness asserts the WHOLE list of stub
requests, so any extra request reds, where a hit-only URL filter would stay green while a second
caller reached the stub -- the R-1029-2 shape the tier-2 gate measured 5 reds on. The choice now
sits in the comment beside the witness, so the next reader finds a decision rather than an
accident. R1 already pins it, and still does after this change.

ONE THING YOUR CARD DID NOT MENTION, AND IT WOULD HAVE BROKEN THE BUILD
Your card asks for the :128 message reword. R1 at :196 ASSERTS THAT EXACT STRING with toContain.
Rewording :128 alone reds R1. I changed both in the same patch and then PROVED the coupling
rather than asserting it:
  ARM: :128 reworded, R1's toContain left at the old string -> 1 failed / 7 passed of 8,
       R1 reds, exactly. Restore verified by sha256 20ea46a75bc15a9f; file 8/8 again after.
R1's expected substring is now a shorter, less brittle prefix of the new message.
The message says ASKED, not "answered": the list proves tier 2 was QUERIED once, not what came
back, and it is not a tier-1 witness. The 0-read tier-1 half stays open on KS 1180.

FIGURES, ALL MINE
  api-gateway BASELINE at the tip   86 files / 773 tests / 0 failed   rc 0
  WITH THIS CHANGE                  86 files / 773 tests / 0 failed   rc 0
  the touched file alone            1 file / 8 tests / 0 failed
Cell count UNCHANGED, which is correct: this rewords a message and adds a comment; it adds no
cell. A +N here would have meant I had done something other than what the ticket asked.

TSC, BOTH WAYS, PROGRAM PROVEN TO CONTAIN THE FILE
  Census: ks1072 test file 1, bogus-name control 0, 513 files. The PACKAGE program contains 0
  copies of it, so a bare tsc -p is blind here.
  29 errors at base, 29 patched, sorted sets BYTE-IDENTICAL, 0 naming the changed file.
ESLINT BY HAND: rc 0, clean, base and patched.

PUSH GATE, from THIS push's RAW log via gatelines34
  28/0 - 6/0 - 49/0 - shell suites 60 passed, 0 failed, 0 skipped (of 60)
  ^FIXTURE BUILD FAILED 0 - 13 code guards passed - VERDICT MATCHES - zero FAIL/not-ok lines.
  rc 0, .rc file 0. PREFLIGHT INCOMPLETE -- 12/15 legs ran, 3 SKIPPED, nothing failed.
  Lock taken + released by b38 in one invocation (pid 7854). 0 orphaned login_stub listeners.

KEYSCAN REFUSED ME, CORRECTLY -- THE THIRD TOOL REFUSAL TODAY THAT FOUND MORE THAN A READ DID
My first PR body quoted the new assertion string VERBATIM, which put a hyphenated KS-1180 in the
body and would have ATTACHED that ticket on GitHub. keyscan34 FAILED it (MG-3 key set
[KS-1180, KS-1227] != own [KS-1227]). Named the row descriptively instead; re-scan PASS, and the
control (re-hyphenating one foreign key) still FAILS rc 1. I also checked all three commit
messages: each carries ONLY its own key.

STATE OF MY QUEUE
  #1323 KS-1129 livescan   1a509947  READY   waiting gate36
  #1324 KS-1124 mintmerge  47c4579b  READY   waiting gate36
  #1325 KS-1227            39f4922d  READY   waiting gate36
  ITEM 5 KS-1351 item 1    building now -- worktree up, npm ci running
Nothing merged, nothing deployed, no ticket moved.

MEANWHILE
ITEM 5 is the last of the queue. Design per your ruling: declare revoked / revokedAt /
revocationReason on a NEW SecuuraCredentialStatus extends VCCredentialStatus and NARROW
SecuuraCredential to it, rather than widening the W3C-shaped base; plus the one let -> const at
credentialRepo.ts:95. I will report the TS2339 count 4 -> 0 over an exclude-[] program as a
MEASUREMENT, with the census proving the program contains the test file.

NEEDED-BY
Nothing blocking. Three PRs wait for gate36; the fourth follows shortly.


## SEAT RECORD /Volumes/DevMASTER/!CODING/Secuura/Blockchain/5_Project_History/2026-09-28_seatB-38th/b38-queue-complete.txt TEXT_SHA256 b89bd17b84c7cf3e024e131866bb97d99b9e7ef27a2e68e372e879d57d587a3a

CONTEXT
QUEUE COMPLETE. ITEMS 1-5 all done; ITEM 6 does not exist (your ANSWER). Four PRs raised and
ALL FOUR WAITING for gate36. Nothing merged, nothing deployed, no ticket moved, no board state
changed except the one ticket ITEM 1 told me to file.
THE FUSE: 40.0 h, computed at 2026-09-28T07:59:05Z.

THE FOUR, each re-read at the API AFTER opening and re-swept just now
  #1323 KS-1129 livescan   1a509947caf936bcc9b05f7817af6fcbcc974289  2f +54/-3  title 80ch
  #1324 KS-1124 mintmerge  47c4579b0199df1168220fa226805718c26fbbb3  2f +68/-2  title 75ch
  #1325 KS-1227            39f4922d391dabc7f3f99c9c0c8ea2ddde1b596f  1f +14/-2  title 78ch
  #1326 KS-1351 item 1     3f569dfc701c757253aa71ed8b91b81ce9c84c93  2f +26/-1  title 75ch
All four: open, merged false, draft false, base develop, ZERO closing keywords, hyphenated key
set == own key set, zero (#n) in the title, every title <= 92 as it will LAND, ZERO reviews.
All four based on d9ce1403 (tree a87715ebff3e, equal to your declared END).

ITEM 1 -- filed as KS-1352 (P2), mailed separately at 07:06Z. Your prediction held and the
positive control did NOT discriminate: revoked verifies TRUE by BOTH routes, and verify answers
checks.status TRUE on a document whose own credentialStatus reads "revoked": true. No fix built.
NOTE: your own CARDS.md section 1 already carried this observation marked "Read from source, NOT
measured" and said it needed a measured red on a seat before it could become a ticket or a card.
That precondition is now satisfied BY MEASUREMENT, not by a code read.

ITEM 5 FIGURES -- the measurement KS-1351 actually asks for
  TS2339  4 -> 0   (total tsc errors 4 -> 0, rc 2 -> 0)
  The four at base are exactly the sites the ticket names (72:63, 142:39, 143:39, 144:39) and
  they are the ONLY errors in that program. Census: test file 1, credentialRepo.ts 1,
  shared vc/types 1, bogus-name control 0, 428 files; the PACKAGE program contains 0 copies of
  the test file. Control: a planted type error takes the run to 5, so the check can still fail.
  eslint prefer-const  1 problem -> 0   (item 2, a measured delta)
  vc-issuer suite 15 files / 140 tests, IDENTICAL base and patched -- correct for types-only.
  packages/shared own tsc rc 0. ISSUER FRONTEND tsc rc 0, 0 errors: the narrowing does not break
  the portal that reads credentialStatus?.revoked.

A TRAP WORTH A STANDING LINE, AND IT NEARLY COST ME THE ITEM
  vc-issuer resolves @secuura/shared to the package's BUILT dist/, not its source. After editing
  packages/shared/src/vc/types.ts the count was STILL 4/4, still naming VCCredentialStatus -- a
  result that reads exactly like "the change does nothing". MEASURED rather than guessed:
  dist/vc/types.d.ts held 0 occurrences of the new interface before
   and 2 after, and only then did tsc go to 0.
  A TYPES-ONLY CHANGE IN packages/shared/src IS INVISIBLE TO EVERY CONSUMER UNTIL THAT PACKAGE IS
  REBUILT. A successor measuring "4 -> 4" would wrongly conclude the change is inert. This is the
  inverse of the migrations-image trap and of the bind-mounted spec: same family, third surface.

FIVE OF MY OWN INSTRUMENTS CAME OUT WRONG BEFORE THEY CAME OUT RIGHT. ALL FIVE CAUGHT, NONE
REPORTED AS A RESULT.
  1. Store-membership control: bogus-sha arm only, BOTH arms fatal -- measures nothing.
  2. Auth smoke test: the mint had silently failed, so both arms were tokenless and both 401.
  3. 254 after a pipe measured tail, and this shell is zsh: an apply-check control that had
     REFUSED read as rc=0. Your brief warned me about exactly this and I walked into it anyway.
     Every rc I have reported since comes from a bash script file.
  4. KS-1124's first arm was a LOADFAIL, not a red: reverting the spread orphaned 
     -> TS6133 -> "Test suite failed to run", Tests: 0 total.
  5. A consumer grep returned 0 files on a wrong pathspec -- a false absence from my own tool.

THREE INHERITED TOOL DEFECTS, generation *34 (21 tools, censused 21-on-disk == 21-expected,
199 LIVE lines re-keyed, 6 prose lines preserved, the re-key tool in its own map)
  - bannercheck carried GEN = "33" AND NEITHER CONTROL RAN THROUGH GEN (control B asked my OWN
    folder for "34", which IS my generation, so it could only find zero). Fixed; both controls now
    derive from GEN. PROVED load-bearing by A/B on identical trees with only GEN differing:
    fixed = 16 checked / 0 stale / A,B,POPULATION all PASS; inherited = 0 checked and
    A=FAIL B=FAIL POPULATION=FAIL. Yours printed CLEAN. "0 checked" now fails by rule.
  - inbox_match lost "b 37th" and namecheck lost "b37" plus all four FOREIGN_FORMS -- the
    structural recurrence, THIRD generation running. COUNTERFACTUAL ON REAL MAIL: without the
    entry your "GO (Seat B 37th): merge 1321 1322 on gate35" classifies FOR ME. Both fixed;
    b 37th, b 36th and b 35th all present and proved on real subjects.
  - NEW, and bannercheck cannot catch it: rekey33.py's own module docstring opened
    "Seat B 36th - rekey32.py ... map (31 -> 32)". A docstring is prose, so the re-key cannot
    reach it BY CONSTRUCTION, and bannercheck checks self-naming OUTPUT lines, not docstrings.
    Mine states its own position.

keyscan34 REFUSED ME ONCE, CORRECTLY: my KS-1227 body quoted the new assertion string verbatim,
putting a hyphenated KS-1180 in a PR body, which ATTACHES that ticket. Named descriptively
instead. All four commit messages carry ONLY their own key, verified.

CONTAINMENT, measured at boot, after every push, and again now
  SHARED CHECKOUT NEVER WRITTEN: HEAD 3bad652d17cf and local develop 3bad652d17cf identical
  throughout, .git/config sha256 870a35e2163629ca... unchanged, 17 untracked / 0 tracked.
  refs 1506 -> 1510: EXACTLY FOUR ADDED, ALL FOUR CARRYING -b38-, ZERO foreign; plus ONE ref
  VALUE changed -- origin/develop 54f37d6399bd -> d9ce1403d158, the single refresh you authorised
  in Q3, taken and released under .push-lock-34 inside ONE invocation each time.
  Every push: lock taken and released by b38 in one invocation, 0 orphaned login_stub listeners.
  Four push gates, each read from its OWN raw 1305-line log via gatelines34, never the wrapper:
  28/0 - 6/0 - 49/0 - shell suites 60/60/0 - FIXTURE BUILD FAILED 0 - 13 code guards - VERDICT
  MATCHES - rc 0 - zero FAIL/not-ok lines. All four: PREFLIGHT INCOMPLETE, 12/15 legs, 3 SKIPPED
  (stack-dependent; no local stack up). Stated in every PR body, never implied away.

CARRY, listed not acted on
  The 16 orphaned login_stub listeners (8 s-b26-rc-head, 8 s-b26-rc-base, Seat B 26th's) -- your
  Q2 ANSWER says file them on the BOARD, not BACKLOG.md. I have NOT filed that ticket yet; it is
  the one item of your ANSWER still outstanding and I will do it next unless you would rather it
  waited for gate36. Not killed: not mine.

NEEDED-BY
Nothing blocking. All four wait for gate36, and I merge only on a signed GO whose subject names
Seat B 38th.


## SEAT RECORD /Volumes/DevMASTER/!CODING/Secuura/Blockchain/5_Project_History/2026-09-28_seatB-38th/b38-correction.txt TEXT_SHA256 2ab9713e34d21b5cf0cee6647cbd6b5d0f072481c2333f77efa90ca52c995b63

CORRECTION to my QUEUE COMPLETE mail of a moment ago. Two sentences in it are MANGLED, and the
cause is my own shell error, not a measurement error. Every figure in that mail stands; two
sentences lost words.

WHAT HAPPENED
I wrote that mail with an UNQUOTED heredoc so I could interpolate the fuse hours. An unquoted
heredoc body still performs command substitution, so the two backtick spans in my prose were
EXECUTED by the shell and replaced with their (empty) output. You can see the evidence in my own
terminal: an "npm error ENOENT ... could not read package.json" and a "command not found: const".
Those are not failures of anything I measured -- they are my prose being run as commands.

THE TWO DAMAGED SENTENCES, AND WHAT THEY SHOULD READ

1. The packages/shared rebuild trap, which is the whole point of that paragraph.
   AS SENT:     "dist/vc/types.d.ts held 0 occurrences of the new interface before
                  and 2 after, and only then did tsc go to 0."
   SHOULD READ: "dist/vc/types.d.ts held 0 occurrences of the new interface before
                 npm run build -w packages/shared, and 2 after, and only then did tsc go to 0."
   The missing words are the build command itself -- the one thing a successor needs.

2. The KS-1124 load-failure disclosure.
   AS SENT:     "reverting the spread orphaned
                  -> TS6133 -> Test suite failed to run, Tests: 0 total."
   SHOULD READ: "reverting the spread orphaned the const current declaration
                 -> TS6133 -> Test suite failed to run, Tests: 0 total."
   The missing words name the orphaned declaration.

NOTHING ELSE IS AFFECTED. I checked the whole file: 0 backticks survive, and those were the only
two spans. Every SHA, count, rc and verdict in that mail was written as plain text and is intact.

THIS IS THE SIXTH INSTRUMENT OF MINE TO MISFIRE TODAY, and the first that reached you rather than
being caught before it mattered. It belongs with the other five in my handover, and the rule is
simple enough to be worth a standing line: a mail body goes in a QUOTED heredoc, always; if a
value must be interpolated, substitute it afterwards in python, never by unquoting the delimiter.

The queue state is unchanged and correct as reported: #1323, #1324, #1325, #1326 all open, all
based on d9ce1403, all waiting for gate36. Nothing merged, nothing deployed.


## SEAT RECORD /Volumes/DevMASTER/!CODING/Secuura/Blockchain/5_Project_History/2026-09-28_seatB-38th/raise/s-b38-ks1129live-1a509947caf9-stubs.txt TEXT_SHA256 e3b0c44298fc1c149afbf4c8996fb92427ae41e4649b934ca495991b7852b855



## SEAT RECORD /Volumes/DevMASTER/!CODING/Secuura/Blockchain/5_Project_History/2026-09-28_seatB-38th/raise/s-b38-ks1124merge-47c4579b0199-stubs.txt TEXT_SHA256 e3b0c44298fc1c149afbf4c8996fb92427ae41e4649b934ca495991b7852b855



## SEAT RECORD /Volumes/DevMASTER/!CODING/Secuura/Blockchain/5_Project_History/2026-09-28_seatB-38th/raise/s-b38-ks1227-39f4922d391d-stubs.txt TEXT_SHA256 e3b0c44298fc1c149afbf4c8996fb92427ae41e4649b934ca495991b7852b855



## SEAT RECORD /Volumes/DevMASTER/!CODING/Secuura/Blockchain/5_Project_History/2026-09-28_seatB-38th/raise/s-b38-ks1351-3f569dfc701c-stubs.txt TEXT_SHA256 e3b0c44298fc1c149afbf4c8996fb92427ae41e4649b934ca495991b7852b855



