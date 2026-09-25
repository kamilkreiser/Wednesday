#1248 KS-1143 GF2CALLBACK: LEG F reads the guard from the parser's continuation
head 2b4960172644b5ef0414b94d46d11974012c2007

## What this changes

`routerParserAnalysis`'s guard walk ran over the **whole** wrapper body, so
`g(req, res, () => raw(req, res, next))` — guard first, parser inside its callback — read `guarded: true`
while the guard inspected an **unparsed** `req.body` and nothing ran after the parser. LEG F's own message
defines `true` as "the parser runs and something after it inspects the body", so the reading contradicted the
leg's stated meaning. It is the KS-800 class this file is named for, inverted.

The walk now starts at the parser call's **continuation**: the function-valued arguments of the parser call
inside that wrapper.

## Provenance

The change was **built and held** earlier today against a different base (stacked on #1215's pre-squash head,
never pushed). This PR is that single commit re-applied onto `develop` `6e2a00bfe`, and **every measurement
below was re-taken on this tree** — the earlier numbers are not restated anywhere, including in the commit
message, because they were taken on a tree this commit no longer sits on.

## Test Evidence

**Touched:** `Blockchain/Dev/packages/shared/src/__tests__/ks781-p3-3-body-parser-order.test.ts`. One file,
one commit. No `package.json`, no lockfile.

**Ran** (all by the author, on this head; node v24.7.0, vitest 4.1.11, macOS):

- `npm test` in `packages/shared` — **47 files / 930 passed / 0 failed**, rc 0, **0 timeouts**, at load 8.09
  falling to 7.45. Reported beside the run because the tree-walking guards in this package are a known load
  class.
- **BASE, measured not inferred**: develop's blob for this file put in place, the suite re-run, then restored
  and the restore verified by sha256 → **47 files / 928 passed / 0 failed**. So **928 → 930**, exactly the two
  new cells, with no pre-existing red on either side.
- `npm run build` (tsc) — rc 0 at base **and** at head.
- `npm run lint` — rc 1 at base **and** at head, and the finding sets are **byte-identical** (`diff` empty).
  The single error is the pre-existing `no-control-regex` at `:539`, which is red on `develop` too and is
  already on the backlog. A control was run to show the comparison can detect a difference.
- **Tamper matrix, 4 arms, all red** (`tamper1143.sh`, my own copy; restores from a saved byte copy with a
  sha256 assertion, never `git checkout`, and the runner redirects rather than pipes so the rc is the
  command's):

| arm | what it flips | reds |
|---|---|---|
| A1 | continuations accept **any** argument, not only a function expression | **W8 only** |
| A2 | revert the fix — walk the whole wrapper body | W7 **and** W8 |
| A3 | `parserContinuations` returns nothing (under-report) | W2, W3 **and** the undeclared-parser census |
| A4 | W7's expectation flipped to the old wrong answer | **W7 only** |

**A1 was run first, deliberately.** It is the arm that reddened *nothing* when this change was first built —
no fixture then distinguished "only a function expression" from "any argument", so the strictness was not
load-bearing and a later edit could have dropped it in silence. W8 exists because of that. Running it first
was the condition for trusting the rest of the matrix: it reds W8 here, so the matrix is **read**, not assumed.

**A3 reds three cells on this tree, not two.** The earlier run was filtered to the wrapper family; this one
runs the whole file, so the undeclared-parser census also catches it. Noted because the difference is in the
scope of the run, not in the product.

**NOT run / NOT covered:**

- **The indirect-invocation false negative is out of scope**, by the standing ruling on this ticket. The
  disclosed limit stands and is stated in the code: a continuation passed by **name**
  (`raw(req, res, afterParse)`) is not a function expression, so a guard inside it reads `false`. That
  **under-reports** — the safe direction.
- **GF-1 is already closed** by #1212 (`dd8f99cc7`) and is not touched here.
- This guard reads the whole `services/` and `packages/` tree by **text**, so a later merge from another lane
  can move its verdict. This result is stated at this head over develop `6e2a00bfe`.
- No environment, no docker, no database, no migration, no config. **Nothing deployed.**

## Which gate ran, and it is not a clean "preflight green"

This is a `Blockchain/Dev/` path, so `.githooks/pre-push` **did** run — unlike the three `systemTest/` PRs
raised alongside it, where the hook skips on path. The push took **7 minutes**. What it printed, verbatim:

```
PREFLIGHT INCOMPLETE — 12/15 legs ran, 3 SKIPPED. Nothing failed.
  legs 3 4 8 — local stack not up; you can clear this by starting it.
  This is NOT a pass. Do not quote it as one — say which legs ran.
```

So: **12 of 15 legs ran, nothing failed, legs 3, 4 and 8 were skipped** because the local stack is not up.
The preflight's own line forbids calling that a pass, and this PR does not.

**The fleet STOP count, read from the push output anchored to each suite's section header** (a first attempt
at this read grabbed the neighbouring suite's line and reported 15 for the fixture guard; the extraction is
now pinned to the header and has a control that returns NOT FOUND on a header that does not exist):

| suite | printed | expected |
|---|---|---|
| `pre_push_hook_base.test.sh` | **28 passed, 0 failed** | 28 / 0 |
| `pre_push_hook_base_fixture_guard.test.sh` | **6 passed, 0 failed** | 6 / 0 |
| shell suites | **60 passed, 0 failed, 0 skipped (of 60)** | 60 / 60 |

No line starting `FIXTURE BUILD FAILED`. `packages/shared` was **built before the push**, which is what makes
the shell-suite runner read 60/0 rather than 59/1 in a fresh worktree.

**Migrations + config:** none.

Refs KS-1143

