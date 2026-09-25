#1245 KS-1313 SUMMARYREAD: read the vitest summary by label set and sum, not by requiring passed
head 65eb964271b0d6895e90fe8f5ffcbbbb9a484050

## Round 2 of 2 — the cap round. What round 1 got wrong, and how.

**Round 1 was NO GO on B-1245-1 (LIVE-SHAPE WRONG), and the gate is right.** The rule was *the last
`Tests`-shaped line of stdout and stderr joined*. That is not the summary. Captured from real vitest
4.1.11, here are two ordinary ways a `Tests`-shaped line reaches **stderr**, both landing **after** the real
summary in that join:

| capture | how the lookalike gets there | round 1 read | vitest actually said |
|---|---|---|---|
| **S17** | a test calls `console.error('      Tests  5 passed (5)')` | `{ passed: 5, failed: 0 }` | `1 failed \| 1 passed (2)` |
| **S18** | an ordinary **multi-line string diff** prints its *unchanged context lines*, so a fixture whose middle line is `      Tests  9 passed (9)` puts that on stderr — **with no console call at all** | `{ passed: 9, failed: 0 }` | `1 failed \| 1 passed (2)` |

Neither needs anything unusual. **A failing child reporting a clean run** is the whole cost, and that is
exactly the case this reader exists to survive.

## The rule now

`readChildOutput(output)` takes the `Tests` line that follows the **last ` Test Files ` line**. vitest
prints that block once, at the end, so anything a *test* emitted — on either stream — is before it.

`childSuiteCounts` passes **`result.stdout` alone**, so stderr cannot reach the reader at all. The anchor is
*also* measured to hold on the **joined** text, because the round-1 defect was precisely someone joining the
streams — belt and braces rather than one or the other.

**I looked for the adversarial case against my own new rule before writing it**, which is the thing round 1
did not do. **S19** is a test that logs **both** a ` Test Files ` line *and* a `Tests` line to **stdout**.
vitest's own block still comes last, and the rule still reads the real summary. Measured across **14**
captured shapes in total.

## The fixtures are whole runs, not lines

Round 1 was proven against summary *lines*, and the defect lived in *which line of a whole run gets picked* —
a class of defect that fixture shape cannot reach. `tests/unit/support/capturedChildOutput.ts` carries the
**complete streams** of real runs, stdout and stderr kept apart so a cell can feed either or both. It is
**generated from the captured bytes, not retyped**; the originals and the fixtures that produced them are
archived at `5_Project_History/2026-09-25_seatL6/evidence/vitest-capture-round2/`.

## Test Evidence

**Touched:** `systemTest/performance/tests/unit/utils/unitSuiteSlotIndependence.test.ts` and a new
`systemTest/performance/tests/unit/support/capturedChildOutput.ts`. No `package.json`, no lockfile.

**Ran** (all by the author, on this head; node v24.7.0, vitest 4.1.11):

- `npm run test:unit` — **63 files / 1115 passed / 0 failed**, rc 0, at load 5.79. Base at develop
  `6e2a00bfe`: **63 / 1089 / 0**.
- `npm run lint` — **rc 0**, across **both** tsconfigs plus eslint. (`tsconfig.node.json` is the only one
  that type-checks this file at all — `tsconfig.json` excludes `tests`.)
- `npm run format:check` — rc 0.
- **Tamper matrix, 4 arms, all red**, restores sha256-asserted:

| arm | what it flips | reds |
|---|---|---|
| E1 | round 1's rule restored in full (last `Tests` line, no anchor) | **S17 JOINED, S18 JOINED, and the anchor control** |
| E2 | the call site reads the joined streams again | the call-site pin |
| E3 | anchor on the **first** ` Test Files ` line | **S19** — the logged-anchor case |
| E4 | no anchor → fall back to the whole text instead of `null` | the anchor control |

E1 reds the two **JOINED** cells and not the stdout-only ones, which is the defect stated precisely: round
1's rule only breaks once stderr is in the text.

⚠ **My first E1 applied cleanly and tampered nothing** — it changed the `anchor` initialiser, which the loop
immediately overwrites. My `|| exit` guard could not see that: the guard catches a tamper that does not
*apply*, never one that applies and is **inert**. The only thing that caught it was expecting a **named**
red and not getting one. E1 now replaces the whole body, and that note is in the script.

**The call-site pin is now behavioural**, as the gate asked — the pure `readChildOutput` is fed the real
captured output of the same kind of child and the answer asserted. The text pin is kept **beside** it, not
instead of it: a text pin passes for a call site that calls the function and ignores its answer, and the
behavioural cell cannot see an inline regex creeping back.

**Also in this round:** the ticket's `      Tests  2 failed | 3 passed (5)` row, captured byte-exact as
S10, reads `{3,2}`. Title set to the gate's proposed ≤92-char subject.

**NOT run / NOT covered:**

- The **JSON-reporter** alternative the gate offered was not taken: the anchor on the default reporter's own
  block is measured to hold on all 14 shapes, and adding a reporter file would change what the child writes.
  Stated as a choice, not an oversight.
- A **TTY** child (colour codes present) is not captured — the caller pipes, and ANSI is stripped
  unconditionally, so the difference cannot reach the parse.
- A vitest other than **4.1.11**: the label set and the ` Test Files ` block are read from this version.
- `npm run knip` / `npm audit` not run. No docker, no k6, no environment. **Nothing deployed.**

**Which gate ran:** repo-root `systemTest/` path, so `.githooks/pre-push` skipped its 15-leg preflight; the
push took 12 s and printed only `[format-gate] 1 package(s) checked, 0 skipped, 0 failed`. The fleet STOP
count was **not executed** on this branch and nothing here quotes it.

**Migrations + config:** none.

Refs KS-1313

