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

