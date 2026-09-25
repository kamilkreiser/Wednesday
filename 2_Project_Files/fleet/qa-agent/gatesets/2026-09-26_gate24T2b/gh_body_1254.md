#1254 KS-1155 WALKBUDGET: give the tree-walking guards a 60 s budget from config, and guard the list
head da0c94968a7423c340b3a3b76244bda536d1f6d2

## What this changes

Seven suites in `packages/shared` read the whole `services/` + `packages/` tree by design. The walk is the
cost, and it exceeds vitest's 5 s default when the box carries several seats at once. The assertions hold
every time — the same cells pass solo, with the timeout raised, or minutes later at a lower load — so a red
`Test timed out in 5000ms` in those files is a **load class**, not a product finding, and a merge seat
cannot tell the two apart without a solo re-run that costs a full suite.

The budget is set from `vitest.config.ts` through one setup file, **not in the guards**. No assertion is
touched, and every other cell in the package keeps the 5 s default, so a unit test that genuinely hangs
still fails fast. **Time, not truth.**

Three files: `vitest.config.ts`, a new `src/__tests__/support/walkTimeouts.setup.ts`, and a new
`src/__tests__/walkTimeouts.test.ts`. **Zero guard files touched**, which is what keeps this out of the way
of the ks781 and ks860 work in flight alongside it.

## Proven end to end, not asserted

The **same 6-second cell** appended to a walker (`ks860-…`) and to a non-walker (`ssrf-guard`) in one run:

```
✓  L6 PROBE — a 6 s cell   (ks860-test-listeners-bind-loopback.test.ts)
×  L6 PROBE — a 6 s cell   (ssrf-guard.test.ts)   Error: Test timed out in 5000ms.
```

So the raise applies exactly where intended and nowhere else. Both files were restored byte-exactly
afterwards (sha256 asserted). **That probe is not a standing cell** — a 6 s cell would be paid on every run
of this suite forever.

## The list is derived, not trusted

A hardcoded set of file names goes stale the moment someone writes the eighth tree-walker, and it goes stale
**silently**: the new guard gets the default budget and starts flaking under load, which is the state this
ticket exists to end. `walkTimeouts.test.ts` recomputes the set from the sources — a suite that reads the
tree cannot do it without `readdirSync`, `DEV_ROOT` or `WALK_ROOTS` — and fails on any difference, naming
the file.

The derived set and the configured set agree today at exactly the seven suites this ticket names.

## A gap I measured, and then closed

With only the list and predicate cells, **removing `setupFiles` from the config reddened nothing**. The
cells checked the list and the predicate; neither is evidence the setup file is ever *loaded*, so the budget
could have been unhooked in silence with the suite still green. There is now a cell pinning the wiring, and
its tamper arm reds. Written up here because the first version of this change would have shipped a budget
that nothing proved was connected.

## Test Evidence

**Ran** (all by the author, on this head; node v24.7.0, vitest 4.1.11):

- `npm test` in `packages/shared` — **48 files / 933 passed / 0 failed**, rc 0, **0 timeouts**, at load 5.57.
  Base, measured in this worktree before any change: **47 files / 928 passed / 0 failed** at load 7.67.
- `npm run build` (tsc) — rc 0.
- `npm run lint` — rc 1, finding set **identical to develop's** (`diff` empty; control run). The one error is
  the pre-existing `no-control-regex` at `:539`.
- **Tamper matrix, 6 arms, all red** (`tamper1155.sh`; restores sha256-asserted across all three files):

| arm | what it flips | reds |
|---|---|---|
| D1 | drop a real walker from the list | the equality cell, naming it |
| D2 | add a non-walker to the list | the equality cell + the predicate control |
| D3 | set the budget to the 5 s default | "the budget is a raise" |
| D4 | break the derivation's markers | the non-vacuity cell + the equality cell |
| D5 | match on the whole path, not the basename | the directory-name control |
| D6 | remove `setupFiles` from the config | the wiring pin |

⚠ **Two of those arms did not apply on their first run and printed a clean pass.** D4's anchor pointed at
the setup file when `WALK_MARKERS` lives in the test file, and D2's replacement was malformed; in both cases
the tamper's assertion failed, python exited, and the unguarded call let the arm report a green run —
**a tamper that silently does not apply reads exactly like a guard that cannot fail.** Both are fixed, every
arm now exits on a failed tamper, and the table above is from the corrected run.

**NOT claimed / NOT covered:**

- 🔴 **This ticket's "done when" is NOT met and I am not reporting it as met.** It asks for a full
  `packages/shared` run at **load ≥ 30** reading 0 timeouts. Tonight's load was **4.8–9.2**. The run is green
  with 0 timeouts at that load, which is a different measurement. I did not manufacture load 30, and the bar
  stays open on the ticket.
- The second "done when" — that a merge seat no longer needs a solo re-run — follows from the budget but is
  a claim about future runs, so it is stated as the intent, not as measured.
- **`threadToken.test.ts` is deliberately excluded.** Its 30 s cell is CPU-bound crypto, which this ticket
  calls a different shape with its own budget line; folding it in would hide that.
- The **vc-issuer `db.retry`** half of the class (from this ticket's comments) is a different package and is
  **untouched**.
- No assertion was loosened anywhere. No environment, no docker, no database. **Nothing deployed.**

## Which gate ran, and it is not a clean pass

```
PREFLIGHT INCOMPLETE — 12/15 legs ran, 3 SKIPPED. Nothing failed.
  legs 3 4 8 — local stack not up; you can clear this by starting it.
  This is NOT a pass. Do not quote it as one — say which legs ran.
```

Fleet STOP count, read anchored to each suite's section header with a control that returns NOT FOUND for a
header that does not exist: `pre_push_hook_base` **28/0**, fixture guard **6/0**, shell suites **60 passed,
0 failed, 0 skipped (of 60)**. No line starting `FIXTURE BUILD FAILED`.

Worth noting for this PR specifically: **the shell suites still read 60/0 with the new setup file in place**,
so wiring a `setupFiles` entry into this package has not disturbed the fleet count.

**Migrations + config:** no migration. The only config change is this package's own `vitest.config.ts`.

Refs KS-1155

