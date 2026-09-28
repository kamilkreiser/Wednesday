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

