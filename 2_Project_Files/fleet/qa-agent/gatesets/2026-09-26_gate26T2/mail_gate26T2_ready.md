# CAPTURE for gate26T2 (QA/Secuura-batch1245) — 2026-09-26T00:58:48Z

NO READY MESSAGE ID reached the drafter for any PR of this kit (the seat records carry none; a listing would mark mail seen). Each PR's seat
claims are captured from its PR BODY, its head COMMIT MESSAGE and the seat HANDOVER files below, each verbatim with its TEXT_SHA256.

## #1245 KS-1313 (Seat L6 (round 3 by B 29th), T2) — head cb31a58c190f86aad49b402c1c001429c037ed24

#1245 ticket line: #1245 is KS-1313.

### PR BODY (gh_body_1245.md) TEXT_SHA256 82f0f39bbedb5194e51e6aba79d43dd01e9a710c7290170ef82249df0cb3dd85

#1245 KS-1313 SUMMARYREAD: read the vitest summary by label set and sum, not by requiring passed
head cb31a58c190f86aad49b402c1c001429c037ed24

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



### HEAD COMMIT MESSAGE TEXT_SHA256 4a983089269845953c529cd821540faa0bc570301af0ced99f5e2072f9e39a7c

KS-1313 round 3: refuse a killed child, and anchor the summary on vitest's own block

gate24T2c measured what round 2's anchor costs. A child whose test printed a
COMPLETE summary-block lookalike to stdout and was then KILLED — status 143,
signal null, error ETIMEDOUT, 6007 ms, no summary of vitest's own — read
{ passed: 7, failed: 0 } through readChildOutput and end to end through
childSuiteCounts. A clean pass for a run that never finished, which is the worst
direction for this reading to be wrong in.

THE ANCHOR MOVED, and the exit code is not the discriminator. S15, S17, S18 and
S19 all exit 1 and are legitimate runs with real summaries that must still be
read. What the killed child lacks is vitest's own `   Start at` line — the gate's
own independent oracle. A test can print ' Test Files ' as easily as it can print
`Tests`, so that anchor cannot tell vitest's block from a fixture's imitation of
it. `Start at` can be printed by a test too, but not in the right PLACE: vitest
prints it immediately after the `Tests` line of its own block, and only once the
run reached the end. So the read anchors on the last `Start at` and walks
backwards to the nearest `Tests` line, refusing any foreign line in the gap.

Verified before changing the anchor, because it would otherwise have bought H1 by
breaking everything else: all four captured stdout fixtures carry exactly one
`Start at`, and a cell asserts that so the move cannot silently invalidate them.

childSuiteCounts additionally refuses a child that did not END NORMALLY before it
reads stdout at all — a signal, a spawn or timeout error, or a status outside
vitest's own 0 and 1. A killed run's stdout can contain anything its tests
printed, and no parsing makes that output trustworthy. Two independent refusals
for H1, each red-provable on its own.

H1b and H1c already read null in round 2, for the accidental reason that their
lookalikes were incomplete, so only H1 discriminates the two anchors. They are
cells anyway, to prove round 3 did not buy H1 at their expense — and they stay
green in every red arm.

One guard clause was INERT until a fixture was written for it: removing the
refusal of a foreign line between `Tests` and `Start at` changed nothing, because
no fixture exercised it. A tamper that finds nothing is a statement about the
corpus, so the fixture now exists and the clause reds without it.

systemTest/performance unit suite 1115 -> 1120, 63 files both. The round-2 anchor
restored reddens exactly H1 and the two cells that depend on the new anchor, with
H1b and H1c green.

The round-3 commit is mine because the author (Seat L6) has wrapped.

Refs KS-1313

Co-Authored-By: Claude Opus 5 <noreply@anthropic.com>



### PUSH LOG STOP COUNTS (READ, bounded region; /Volumes/DevMASTER/!CODING/Secuura/Blockchain/5_Project_History/2026-09-26_seatB-29th/raise/s-b29-pr1245-ff-cb31a58c190f-push.out)

```
{
 "log": "/Volumes/DevMASTER/!CODING/Secuura/Blockchain/5_Project_History/2026-09-26_seatB-29th/raise/s-b29-pr1245-ff-cb31a58c190f-push.out",
 "lines": 7,
 "pre_push_hook_base": "NOT FOUND",
 "fixture_guard": "NOT FOUND",
 "run_shell_suites_region": "NOT FOUND",
 "run_shell_suites_prefixed": "NOT FOUND",
 "shell_suites": "NOT FOUND",
 "CONTROL_absent_header": "NOT FOUND",
 "fixture_build_failed_lines": 0,
 "verdict_line": "NONE",
 "preflight_ran": false,
 "rc": "0",
 "start": "2026-09-25T21:39:57Z PUSH START",
 "end": "2026-09-25T21:40:04Z push rc=0"
}
```

## #1261 KS-1293 (Seat B 28th (round 2 by B 30th), T2) — head 0b2fdbb1b8195d4f73467508f8eb6a4c3781b81a

#1261 ticket line: #1261 is KS-1293.

### PR BODY (gh_body_1261.md) TEXT_SHA256 b4d697a5ad6fb60b3fb296513dd7f335aa07bd46eb8e96c839a7fe39ca62ddb3

#1261 KS-1293: pin the originate unit suite's hermeticity, in the suite itself
head 0b2fdbb1b8195d4f73467508f8eb6a4c3781b81a

## BLUF
KS-1266 stopped the anchoring-touching unit files reaching the network, and **nothing in the suite would have noticed if that regressed** — the property was proved by an out-of-band probe, so once #1221 merged it was protected by nobody. The tier-2 gate measured exactly that: revert one file's env line and the suite stays green. Pinned here, in the suite, with two cells and five red arms.

## Why TWO cells, measured rather than assumed
The ticket has two acceptance criteria and one instrument cannot serve both. Measured on node 24 while writing the cells:

| base | `cause.code` | what actually happened |
|---|---|---|
| `http://127.0.0.1:2` | `ECONNREFUSED` | a socket **was** attempted and refused — the closed port happened |
| `http://127.0.0.1:1` | *undefined* | a **Fetch bad port**: refused *before* any socket, so the closed port never happened |
| a loopback literal | — | **0** `dns.lookup` calls |
| the product default | — | **1** lookup for its non-loopback host — the regression shape |

So a DNS spy **cannot** tell `:1` from `:2`: both are loopback and both produce zero lookups. That is precisely the erosion the ticket's second criterion names.

| cell | carries | how |
|---|---|---|
| `CONFIGPINNED` (static) | **criterion 2** — a drift back to a bad port | every anchoring-touching file in this config sets a loopback host on a port not in the Fetch bad-port list |
| `NODNS` (probe-backed — the ticket's preferred shape) | **criterion 1** — hermeticity itself | with a `dns.lookup` spy installed: zero non-loopback lookups **and** a socket-level `ECONNREFUSED` |

Both assert non-vacuity **before** the property: `CONFIGPINNED` refuses a scan finding fewer than 8 bases, and `NODNS` proves its own spy can fire by first showing the product default *does* produce a lookup.

## Test Evidence

**Touched:** `services/originate/src/__tests__/ks1293-originate-suite-is-hermetic.test.ts` (new). 1 file, +157. Test-only.

**Ran (all on this head, base `fa25c9b10fb4`):**
- `npx jest --runInBand` (originate): **bare 869 / 869, 74 suites** with the file moved aside, **patched 871 / 871, 75 suites** with it in place — both rc 0, same commit. +2 cells, +1 suite, fully accounted.
- **Five red arms.** Every restore verified by `sha256`; untampered re-run clean afterwards:

  | arm | cell(s) red |
  |---|---|
  | C1 a subject file points at a non-loopback host | `CONFIGPINNED` only |
  | C2 a subject file drifts to a Fetch bad port (`:1`) | `CONFIGPINNED` only |
  | C3 non-vacuity: a subject file stops setting it at all | `CONFIGPINNED` only |
  | N1 the configured base becomes a non-loopback host | `CONFIGPINNED` + `NODNS` |
  | N2 the configured base becomes a Fetch bad port (`:1`) | `CONFIGPINNED` + `NODNS` |

  **The two N arms necessarily redden both cells**, because this file is itself one of `CONFIGPINNED`'s subjects — stated rather than presented as single-cell arms. The three C arms tamper a **different** file and redden only `CONFIGPINNED`, so both cells are shown independently reachable.
- `npm run lint` (= `eslint src`): rc 0.
- `npx tsc --noEmit`: rc 0. Re-run with `exclude: []` and this file asserted present in the program (706 files, `--listFilesOnly`): rc 0.
- `npm test -w packages/shared`: 47 files / **930 tests**, rc 0 — rebuilt first, since `packages/shared` moved in this base.
- Push: rc 0. `pre_push_hook_base` 28/0, `pre_push_hook_base_fixture_guard` 6/0, shell suites 60/0/0 of 60. No `FIXTURE BUILD FAILED`.

**Three errors of mine that only running caught**, recorded because each would have shipped a cell that proved less than it claimed:
1. The static cell first counted **7** bases where the suite has 8 — `ks1213` assigns a **constant**, not a literal, so a literal-only reader would have reported the one file that is *more* readable than its siblings as an offender. It now resolves the constant's own declaration.
2. The probe cell had **no configured base**, because this file did not set one — so it was measuring the regression shape rather than the pinned one. Fixed by making this file hermetic like the other eight, which is also correct in its own right: it runs in the same config.
3. `import * as dns` yields a namespace object whose `lookup` is **getter-only**; assigning it throws `Cannot set property lookup ... which has only a getter`. The mutable exports come from `require('dns')`. A standalone probe of mine had used `require` and worked, which is exactly why the import form's failure was surprising.

**NOT covered:**
- **`*.integration.test.ts` is not scanned.** It runs only under `jest.integration.config.js`, and `ks1263-multi-write-rolls-back.integration.test.ts` currently sets the base to `127.0.0.1:1` — **a bad port, the very shape criterion 2 names.** Correcting it was ruled into the KS-1310/KS-1311 PR, where that file is already open; widening this scan to the integration config belongs with that change, not ahead of it. Both facts are written into the file's own footer so the next reader finds them.
- These cells pin the suite's **configuration** and the configured base's **behaviour**. They do not prove that every anchoring call site in the product routes through that base.
- **Preflight INCOMPLETE — 12/15 legs, 3 SKIPPED** (legs 3, 4, 8 — local stack down). A skip is not a pass.

**Migrations + config:** none.

Refs KS-1293

🤖 Generated with [Claude Code](https://claude.com/claude-code)



### HEAD COMMIT MESSAGE TEXT_SHA256 ee12e39b43982bf69cc6de5765b7a7ccf44a1335b01c1f79bdc7a7bc065cdbfa

KS-1293: derive the hermeticity subjects from a manifest, not from mentions

Fix round 1 for #1261, on the gate's blocking finding B-1261-1 REVERT-SKIPS. The
author of the branch has wrapped, so this is a fast-forward commit by another
seat; the history before it stays its author's.

The subject set was derived from "which files MENTION the key", which is
circular: deleting the env line the cell exists to catch also deletes the file
from its own subject set. The gate measured three real files going green that
way, and two of the nine subjects carry no second mention at all, so for them one
deleted line is the whole of it.

TWO halves, and each is needed -- proved by an arm that restores one at a time:

  * an EXPLICIT nine-file manifest. A subject that stops pinning is an offender
    NAMED BY FILE, whether the line was deleted, the assignment nested, or the
    file renamed. Restoring the circular rule alone reds RS1 and RS2 exactly.
  * the base must come from an IMPORT-SCOPE assignment, read from the TypeScript
    AST rather than from text. ks1213 assigns the key inside finally blocks as
    well as at the top level, so deleting the top-level line left a text reader
    still finding a base -- but a nested assignment runs during a test, not at
    module load, and does not pin the phase this cell is about. Restoring the
    text reader alone reds RS3a exactly.

The AST is used rather than a column-0 regex because indentation is a formatting
accident and prettier is free to change it; the language's own notion of a
top-level statement is not.

MANIFEST-DRIFT closes the other direction: a new anchoring-touching file that
nobody added to the manifest is an offender too, so the list cannot silently
cover less of the suite than its name implies as the suite grows.

RS1, RS2 and RS3a drive the scan against COPIES in a temp directory rather than
tampering the real files, so they reproduce the gate's revert exactly without
touching a tree another seat may be reading. Each has a paired CONTROL on the
same untouched file, because a cell that reds on a stripped fixture also reds for
a scan that calls everything an offender.

Also in this round, N-1261-a NODNS-EGRESS: the dns spy answered non-loopback
names by delegating to the real resolver, so the pin itself sent a live
getaddrinfo off-host on every run -- and inside the compose network, where the
name resolves, it made a real request to a live service and the arm failed. The
spy now answers non-loopback names itself. Loopback still reaches the real
resolver, because the second arm's ECONNREFUSED must be a genuine socket-level
refusal rather than something the spy invented.

Refs KS-1293

Co-Authored-By: Claude Opus 5 <noreply@anthropic.com>



### PUSH LOG STOP COUNTS (READ, bounded region; /Volumes/DevMASTER/!CODING/Secuura/Blockchain/5_Project_History/2026-09-26_seatB-30th/raise/s-b30-ks1293-ff-0b2fdbb1b819-push.out)

```
{
 "log": "/Volumes/DevMASTER/!CODING/Secuura/Blockchain/5_Project_History/2026-09-26_seatB-30th/raise/s-b30-ks1293-ff-0b2fdbb1b819-push.out",
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
 "start": "2026-09-26T00:45:27Z PUSH START",
 "end": "2026-09-26T00:51:59Z push rc=0"
}
```

## #1268 KS-1318 + KS-1142 + KS-1316 (Seat L7 (round 2 by B 30th), T2) — head 5ac42fafeee11dec596e7e7d833ac82b8b478790

#1268 ticket line: #1268 is KS-1318 + KS-1142 + KS-1316.

### PR BODY (gh_body_1268.md) TEXT_SHA256 e9c852d621e2100fc862303cf740a7e1e0a5ccb565abb7f470dd2402c13d33d1

#1268 KS-1318 + KS-1142 + KS-1316: ks781 tag set, corpus containment, guard reachability
head 5ac42fafeee11dec596e7e7d833ac82b8b478790

## BLUF

**Test-only, three findings, one PR** — KS-1318 and KS-1316 are the same file and KS-1142 reads it, so sequential PRs would each need a merged-blob equality target on a file all three touch. Every claim below is measured; the interesting results are that **the old KS-1318 cell was green under a permutation of the whole file**, and that **KS-1316's own control caught a defect in my first walk**.

`Refs KS-1318` · `Refs KS-1142` · `Refs KS-1316`

---

## KS-1318 — the combined cell asserts the set of tags, not the count

`toHaveLength(3)` is green under any permutation and under any relabelling that keeps the cardinality. Replaced with `toEqual` of the three tags **in source order** — the order confirmed by measurement, not assumed.

| arm | with the new assertion | with `toHaveLength(3)` |
|---|---|---|
| **A** — `return shapes.slice().sort()` | **1 red — the combined cell ALONE**, 0 per-shape rows | **0 red — the whole file green** |
| **B** — the `export default function` branch emitting another branch's tag | 2 red — combined cell **and** 1 per-shape row | 1 red — per-shape row only; **the combined cell stayed GREEN** |

Arm B is the finding verbatim: *"it would pass if two shapes were detected under one another's name."* Arm A is the stronger one — it is the case where **only** the combined cell can see the change, because the per-shape rows are fed one shape each and cannot see order at all.

---

## KS-1142 — one literal, two readers

K1's 27-package literal is hoisted to module scope. The new **K1b** cell in `entrypoint-corpus.test.ts` reads ks781's `CORPUS` **from source text** — ks781 is a test file, and importing it would execute its suites — locates it **by symbol** (`const CORPUS = [`), and asserts its package set is a **subset** of K1's.

**Subset, not equality, and the cell says why.** `CORPUS` is a FILE list and K1 a PACKAGE list; `services/blockchain` and `services/shared` are guarded by K1 alone. An equality assertion would red at the tip for that reason and would push someone to "fix" it by widening `CORPUS` — the opposite of the pin. **R-2 is kept and named in the cell title: K1 still reds on ordinary growth by design.**

| arm | result |
|---|---|
| swap one `CORPUS` path's package for one K1 does not list | **K1b reds** |
| rename the `CORPUS` symbol so the parse finds nothing | **K1b reds** |
| restored | 0 red |

The second arm is not decoration: `[]` is a subset of everything, so both sides assert non-empty first or the containment passes vacuously.

---

## KS-1316 — the gate's syntactic fix, not a recorded limitation

A guard **defined** inside the parser continuation but never **called** read `guarded: true`. That over-reports, which is the unsafe direction.

**Why this is decidable, having first argued it was not.** General reachability is control flow and a text-level walk cannot decide it. But the finding is narrower: whether a **nested function expression** is invoked *in the continuation's own body* is syntactic — it is immediately invoked, handed to a call, or bound to a name that is called there. The walk no longer descends into an uninvoked nested function expression. The continuation itself is always entered, because the parser invokes it.

| cell | shape | reads |
|---|---|---|
| **W9 🔴** | `const later = () => g(req,res,next); next();` | `guarded: false` (was `true`) |
| W10 CONTROL | the same arrow, `later();` | `guarded: true` |
| W11 CONTROL | `(() => { g(...); })();` | `guarded: true` |
| W12 CONTROL | `[1].forEach(() => { g(...); });` | `guarded: true` |
| W13 | `if (false) { g(...); }` | `guarded: true` — **STILL NOT DECIDED**, pinned as such |

**Under develop's walk with these cells present: exactly ONE red, W9.** Every control is green at **both** ends, so none of them is satisfied by a walk that merely stopped entering nested arrows.

**W11 caught a real defect in my first version of the walk.** An IIFE parses as a call whose callee is a `ParenthesizedExpression`, so the `invoked` flag did not survive the parentheses and the arrow read as a definition. **W9 alone would have passed over it** — which is the whole argument for building the controls rather than only the red cell.

**What is NOT closed:** W13's class. Reachability of a *statement* is control flow. KS-1143's indirect-invocation false negative is the opposite direction and stays out of scope, as ruled.

---

## Test Evidence

**Touched**
- `packages/shared/src/__tests__/ks781-p3-3-body-parser-order.test.ts` — the J2 combined assertion, the LEG F guard walk, and cells W9–W13.
- `packages/shared/src/__tests__/entrypoint-corpus.test.ts` — K1's literal hoisted, cell K1b added.

**No product file is touched.** Both files are under `src/__tests__`.

**Ran**
- `packages/shared`: **941/941 bare → 947/947 patched**, 48 files, **+6 = exactly these cells** (W9–W13 and K1b). `npx vitest run --no-file-parallelism` in `s-l7-ks781`, at develop `4db87c3e4b98`, load average **17.67** bare / **10.00** patched. Baseline taken before any edit on a clean tree.
- `npx tsc -p . --noEmit` → **rc 0**. `npm run build` → rc 0.
- Every arm above, each asserting its anchor was found **and** that bytes changed, so a tamper that did not apply could not read as a clean pass.
- **Push gate:** `PREFLIGHT INCOMPLETE — 12/15 legs ran, 3 SKIPPED. Nothing failed.` — legs 3, 4, 8, local stack not up. Not quoted as a pass.
  Fleet STOP count with `packages/shared` **built**: `pre_push_hook_base` **28/0** · `fixture_guard` **6/0** · `run_shell_suites` **49/0** · shell suites **60 passed, 0 failed, 0 skipped (of 60)**.

**NOT run**
- Legs 3, 4 and 8 — local stack not up, per the standing verdict.
- **The LEG F walk change is exercised by fixtures, not by a running Express app.** W9–W13 are source strings fed to `routerParserSites`; nothing here proves runtime behaviour of any route.
- **No product behaviour changes.** The guard walk is a test-side analyser; tightening it changes what the leg *reports*, not what any service does.
- W13's class (statement reachability) and KS-1143's indirect-invocation false negative are open by design.
- KS-1318 arm A uses `.sort()` as the permutation vehicle; no other permutation was enumerated.

**Migrations + config**
- **None.** No migration, schema, runtime config, `package.json`, lockfile, Dockerfile, route or OpenAPI surface.

## Note for the reviewer

If the gate NO-GOes one of the three, the other two are held with it — that is the accepted cost of the one-PR vehicle, agreed before building.


---

## Fix round 1 of 2 — a rule beyond the two the round was scoped to

The blocking finding was that the walk read `guarded: false` on shapes that do run the guard. Two
rules close most of it: a bound function expression is a DEFINITION only when its binding is
referenced nowhere else in the continuation, and `NewExpression` arguments are treated like call
arguments.

**A third rule was needed, and it is here because of a measurement, not a preference.** With the two
above only, four of the five regression cells pass and **W18 (`mk()()`) still reads `false`** — the
returned arrow has **no binding**, so a rule phrased in terms of a binding cannot reach it. The third
rule is the narrowest form that closes it: a function expression **RETURNED** from an invoked one
escapes and is descended, in both return shapes (a concise arrow body and an explicit `return`).

**Its boundary is pinned, not assumed.** It deliberately does **not** cover the object-property /
array-element case, so an arrow merely *stored* and never called still reads `false` — a row this PR
itself fixed and must not undo. **W19** asserts exactly that, and the `overwide` arm (drop the
narrowing entirely) reds **exactly W9 and W19**, so both are live controls rather than cells that
would pass whatever happened.



### HEAD COMMIT MESSAGE TEXT_SHA256 418ee40b37f40ee73e0d53735972feff4fb2c2319652e6e540d10592e535aa56

KS-1316: the walk reads an indirectly invoked guard as invoked

Fix round 1 for #1268, on the gate's blocking finding (THE READER RULE). The
author of the branch has wrapped, so this is a fast-forward commit by another
seat; the history before it stays its author's. KS-1318's and KS-1142's proven
work is untouched: entrypoint-corpus.test.ts is byte-identical to the adopted
head by blob, and no changed line in ks781 mentions KS-1318's tag set.

MEASURED: the shape this file's OWN comment named -- "a bound arrow invoked only
through an alias ... still read true" -- read guarded: FALSE. So did .call,
.apply, .bind()(), a callback handed to new Promise(...), and an arrow returned
and then invoked. Nine shapes flipped correct to wrong, every one of them
UNDER-reporting, which is the direction that makes LEG F claim nothing inspects
the parsed body when something does.

The cause was the invoked-name set: it recorded only name(...), a DIRECT
identifier call, so every indirect way of running a bound function expression
left the name out and the binding read as a definition the walk would not enter.

THREE rules, each proved independently load-bearing by its own arm:

  * a bound function expression is a DEFINITION only when its binding is
    REFERENCED NOWHERE ELSE in the continuation. Referenced anywhere else, we
    cannot say it does not run, so we keep the old answer and descend -- the same
    when-in-doubt direction W12 already states.
  * NewExpression arguments are treated like call arguments. A NewExpression is
    not a CallExpression to the compiler, so its callback fell through to the
    generic descent and read as a definition.
  * a function expression RETURNED from an invoked one escapes, so it descends.

THE THIRD RULE IS BEYOND THE GATE'S TWO STATED SHAPES, and it is there because
the gate's own regression cell W18 (mk()()) was MEASURED to still read false with
only the first two: the returned arrow has no binding, so the binding rule cannot
see it. Recorded here rather than presented as part of the ruled shape.

The limit is held where it was. W9 still reads false and W19 -- new -- pins that
an arrow merely STORED in an object and never called still reads false, so the
escape rule cannot quietly widen until every nested arrow reads true. The
overwide arm reds exactly W9 and W19, so both are live controls.

The code comment that asserted the alias shape read true is corrected in place
rather than silently contradicted by the code beneath it.

Refs KS-1316

Co-Authored-By: Claude Opus 5 <noreply@anthropic.com>



### PUSH LOG STOP COUNTS (READ, bounded region; /Volumes/DevMASTER/!CODING/Secuura/Blockchain/5_Project_History/2026-09-26_seatB-30th/raise/s-b30-ks1318-ff-5ac42fafeee1-push.out)

```
{
 "log": "/Volumes/DevMASTER/!CODING/Secuura/Blockchain/5_Project_History/2026-09-26_seatB-30th/raise/s-b30-ks1318-ff-5ac42fafeee1-push.out",
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
 "start": "2026-09-26T00:29:22Z PUSH START",
 "end": "2026-09-26T00:35:50Z push rc=0"
}
```

## #1275 KS-1179 (Seat L7, T2) — head d852e56b912f8a14b8f2cf01639dc37f9c9ff6a2

#1275 ticket line: #1275 is KS-1179.

### PR BODY (gh_body_1275.md) TEXT_SHA256 ebcba3b222023efbb9c05fc0cdbd7c4eae2d3b41a3833c29990f5217d24e3dd4

#1275 KS-1179: N1 reachability overclaim, N2 contract pin, and the one type error that fixes cleanly
head d852e56b912f8a14b8f2cf01639dc37f9c9ff6a2

## BLUF

KS-1179's residue: **N1** (a comment claiming a reachability it does not have), **N2** (a cell pinning a throw the module's contract disclaims), and **TYPECHECK-DEBT**, of which exactly one error fixes cleanly. **The emitted JavaScript is byte-identical to base** — no runtime behaviour and no emitted string moved, which is the constraint this change was held to.

`Refs KS-1179`

> **Base:** this branch is cut from `4db87c3e4b98`. develop is now `d7cdecf1d2ee`, which this worktree does not contain — so the STOP counts below describe `4db87c3e4b98 + this change`, not the combined tree.

## N1 — the comment claimed a live path that does not exist

It said the DNS-timer cleanup was *"a live path, not a defensive one"* because an `isIP` throw rejects the resolve race.

**`net.isIP` does not throw.** Measured on this node — `'x'`, `''`, `null`, `undefined`, `123` — each returns `0`, none throws. The rejecting exit is reachable **only** by mocking `net`. So the `finally` is **defensive**. It stays, because it costs nothing and is correct for any future arm of that race that *can* reject; what it no longer does is overstate how reachable it is. The next reader sizes a bug here on that claim.

## N2 — the cell pinned a throw the contract disclaims

The module's docblock: *"Returns the guard's error rather than throwing it"*, and KS-931 made that literally true even for a synchronous throw out of `http.request`. The cell asserted `.rejects.toThrow(SEAM)` — enshrining, as behaviour, a throw that exists **only because `net` is mocked**.

The rejection is now the **vehicle, not the claim**: it is caught and asserted only to *be the seam*, so the cell still reaches the exit F-6 is about without pinning a path no real input takes. A new **CONTRACT** cell pins what actually holds — on a real input the guard returns `{ ok: false, reason: 'blocked' }` with its error in the returned value, and does not throw.

**Red-proof for the contract cell:** tampering `return { ok: false, … }` to `throw` reds it, together with CALIBRATION and the settling CONTROL, which take the same return. **The F-6 cell stays green there**, because it leaves through the rejecting seam — exactly the separation the two cells are meant to have. Product restored byte-identical.

## TYPECHECK-DEBT — one fixed, one recorded

`tsc -p .` returns **rc 0** and always did: `tsconfig.json` excludes `src/__tests__`, so the package's own check never sees a test file. **That exclusion is the debt.** Under a test-inclusive program (method and controls in the ticket) there are **10** errors across 6 files.

**TS7006 (`(res)` implicitly any) — fixed** with an annotation; annotations erase, so the emit is untouched.

**TS2349 (`mod.request` not callable) — RECORDED, NOT FIXED.** Four shapes measured; each **relocated** the error:

| attempt | result |
|---|---|
| no change | **TS2349** not callable |
| cast the callee | **TS2769** no overload matches (`agent` is `https.Agent \| http.Agent`) |
| callee cast + cast at the call site | errors 10 → 8, **but the emit changes** (`agent,` → `agent: agent,`) |
| callee cast + assertion on the declaration | emit identical, **TS2352** types do not overlap |

The only shape left is `as unknown as https.Agent`. **Refused:** in an SSRF guard, a type the compiler stops checking is the risk to avoid, not the tidiness to buy. Carried into the follow-up ticket as a measured item.

## The emit proof, and why it is the one that matters here

`ast_equiv` (transpile with `removeComments`, compare output) — **pristine vs head: EQUIVALENT, 12,137 vs 12,137 bytes, 0 diagnostics.**

**Control on the same instrument:** change one character of the deadline error `(connect, transfer and drain)` → `(…drained)` and it reads **DIFFERENT**, naming the line. So the instrument can see precisely the string that had to stay fixed, and it says nothing moved.

**Why that string is load-bearing:** `services/originate/src/__tests__/ks914-deliver-webhook-blocked-vs-failed.test.ts:76` and `:86` assert it as an exact string, and `services/originate/` is **not in this lane**. Changing it would have reddened another seat's suite mid-round. **ks914's own cells: 16/16 green at this head.**

**F-5 needed no change** — its docblock correction shipped in an earlier round, and the only remaining element was that runtime string.

## Test Evidence

**Touched**
- `packages/shared/src/security/ssrf-guard.ts` — the N1 comment, and the TS7006 annotation.
- `packages/shared/src/__tests__/ks1179-dns-timer-cleared.test.ts` — N2.

**Ran**
- `packages/shared`: **941/941 bare → 942/942 patched**, 48 files, **+1 = the contract cell**. `npx vitest run --no-file-parallelism` in `s-l7-ks1179`, at base `4db87c3e4b98`, load **7.71** bare / **12.77** patched.
- `npx tsc -p . --noEmit` rc 0; `npm run build` rc 0.
- `ks914-shipped-path` + `ks914-pinned-address`: **16/16**.
- The contract-cell red-proof, and the emit comparison with its control.
- **Push gate:** `PREFLIGHT INCOMPLETE — 12/15 legs ran, 3 SKIPPED. Nothing failed.` (legs 3, 4, 8 — local stack not up; not quoted as a pass). STOP count with `packages/shared` built: `pre_push_hook_base` **28/0** · `fixture_guard` **6/0** · `run_shell_suites` **49/0** · shell suites **60 of 60** — on the base named above.

**NOT run**
- Legs 3, 4, 8.
- **The defensive `finally` is not exercised by any real input** — by construction, since nothing real rejects that race. The F-6 cell reaches it through a mock and now says so.
- **TS2349 and the other 8 type errors are not fixed** and are carried to the follow-up ticket.
- **No behaviour change of any kind.** The emit proof is the evidence, not a claim.
- ks914's cells were run to show the string survived; **this PR does not touch `services/originate/`**.

**Migrations + config**
- **None.**



### HEAD COMMIT MESSAGE TEXT_SHA256 254731f392c35135186545ba90b3e6e208873257d3e3cc54713608a4adfe512f

KS-1179: N1 reachability overclaim, N2 contract pin, and the one type error that fixes cleanly

N1 -- the comment claimed the DNS-timer cleanup was "a live path, not a
defensive one" because an isIP throw rejects the race. MEASURED: net.isIP
does not throw. On this node 'x', '', null, undefined and 123 each return
0 and none throws. The rejecting exit is reachable ONLY by mocking net.
The finally is DEFENSIVE. It stays -- it costs nothing and is correct for
any future arm of that race that can reject -- but the comment no longer
claims a reachability it does not have.

N2 -- the cell asserted .rejects.toThrow(SEAM) while the module's own
contract says its error is RETURNED, never thrown ("Returns the guard's
error rather than throwing it", made literally true for a synchronous
http.request throw by KS-931). It pinned, as behaviour, a throw that
exists only because net is mocked. The rejection is now the VEHICLE, not
the claim: it is caught, and asserted only to be the seam, so the cell
still reaches the exit F-6 is about without enshrining a path no real
input takes. A new CONTRACT cell pins what actually holds -- on a real
input the guard returns { ok: false, reason: 'blocked' } with its error
in the returned value and does not throw.

Red-proof for the contract cell: tampering `return { ok: false, ... }` to
`throw` reds it, together with CALIBRATION and the settling CONTROL,
which take the same return. The F-6 cell stays GREEN there, because it
leaves through the rejecting seam -- which is exactly the separation the
two cells are supposed to have. Product restored byte-identical.

TYPECHECK-DEBT, Q2 = (a) as ruled: TS7006 ((res) implicitly any) is fixed
with an annotation. TS2349 is RECORDED, NOT FIXED. Four shapes were
measured and each RELOCATED the error rather than removing it:

  no change                                  TS2349 not callable
  cast the callee                            TS2769 no overload matches
  callee cast + cast at the call site        clean, but the emit CHANGES
                                             (agent, -> agent: agent,)
  callee cast + assertion on the declaration TS2352 types do not overlap

The only shape left is `as unknown as https.Agent`, a double assertion.
Refused: in an SSRF guard a type the compiler stops checking is the risk
to avoid, not the tidiness to buy.

EMIT BYTE-IDENTICAL, which is the requirement this change was held to:
ast_equiv pristine vs head, 12,137 vs 12,137 bytes, 0 diagnostics -- so
no runtime behaviour and no emitted string moved. In particular the
deadline error at :605 is untouched, because Seat B 29th's
ks914-deliver-webhook-blocked-vs-failed.test.ts:76 and :86 assert it as
an exact string and that file is not in this lane. Control on the same
instrument: changing one character of that string reads DIFFERENT and
names the line. ks914's own cells: 16/16 green at this head.

F-5 needed no change -- the docblock correction shipped in an earlier
round and only the runtime text remained, which stays byte-identical.

packages/shared 941/941 bare -> 942/942 patched (48 files, +1 = the
contract cell), vitest run --no-file-parallelism in s-l7-ks1179, at
develop 4db87c3e4b98, load 7.71 bare / 12.77 patched. tsc -p . --noEmit
rc 0. npm run build rc 0.

Refs KS-1179

Co-Authored-By: Claude Opus 5 <noreply@anthropic.com>



### PUSH LOG STOP COUNTS (READ, bounded region; /Volumes/DevMASTER/!CODING/Secuura/Blockchain/5_Project_History/2026-09-26_seatL7/raise/s-l7-ks1179-d852e56b912f-push.out)

```
{
 "log": "/Volumes/DevMASTER/!CODING/Secuura/Blockchain/5_Project_History/2026-09-26_seatL7/raise/s-l7-ks1179-d852e56b912f-push.out",
 "lines": 1300,
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
 "start": "2026-09-25T19:52:07Z PUSH START",
 "end": "2026-09-25T19:58:58Z push rc=0"
}
```

## #1276 KS-794 (Seat B 29th, T2) — head 737a4069c6316b10a89fa9c499fac6c2cb20f619

#1276 ticket line: #1276 is KS-794.

### PR BODY (gh_body_1276.md) TEXT_SHA256 f45d2d77e8a5744fd58adb31d95e85da60312091228be08ef78d2960132833cd

#1276 KS-794: declare fileSize and fileHash on the verify schemas
head 737a4069c6316b10a89fa9c499fac6c2cb20f619

## What

Both verify-file handlers return `fileSize` on every 200, and the v1 one also returns `fileHash`, while neither response schema declared any of them. Both bases are `.passthrough()`, so the responses validated and nothing went red — the contract was simply narrower than the behaviour.

**Option (1) from the ticket:** optional fields on the two BASE schemas. No new schema, no new example, no allowlist entry. The alternative — `.extend()` into new registered schemas — copies the base `example` across, and the E8 identifier-literal guard correctly refuses the copies; an allowlist entry for a schema just created would carry a justification that is false of it, which is the failure the guard exists to catch.

## Two corrections to the ticket, both measured before building

**1. `fileHash` is declared on `VerifyResponse` ONLY.** The ticket's comment says "`fileHash` needs the same treatment as `fileSize`". Measured at source: v1 verify-file returns `fileHash`; the **v2** handler computes the same sha256 over the same bytes and returns it as **`hash`**, never a `fileHash`. Declaring `fileHash` on `V2VerifyResponse` would publish a field no v2 operation emits. Neither name is being renamed — a published field rename is a breaking change and is not proposed — so the divergence is documented in both response descriptions **and asserted by a cell**, so a later reader cannot "tidy away" the asymmetry as an oversight.

**2. FIVE operations' published schemas move, not two**, because both bases are shared. Confirmed by walking the regenerated yaml (not only the source), with controls:

| schema | operation | returns `fileSize`? | returns `fileHash`? |
|---|---|---|---|
| `VerifyResponse` | `POST /api/documents/{id}/verify` | no | no |
| `VerifyResponse` | `POST /api/verification/verify` | no | no |
| `VerifyResponse` | `POST /api/verification/verify-file` | **yes** | **yes** |
| `V2VerifyResponse` | `POST /api/v2/verification/verify` | no | no |
| `V2VerifyResponse` | `POST /api/v2/verification/verify-file` | **yes** | no — it returns `hash` |

Three of the five return neither field. "Optional and absent" is an honest description of those three, and that trade is exactly what the ticket's option (1) proposes — but the ticket names only the two verify-file operations, so the other three are named here. Controls on the yaml walker: a nonexistent schema returns **0** references; `ErrorResponse` returns **2666**.

Nothing here types the published `blockchain` block (the `secuura-ks1019-blockchain-block-untyped` ruling).

## Why a cell file, when `check:openapi` is green

`check:openapi` proves the committed yaml matches what the generator emits. **It cannot prove the generator declares any particular field** — delete the two lines from the schema, regenerate, and `check:openapi` is green again on a spec that has silently lost them. That blindness is recorded on KS-811. So the properties an integrator depends on are asserted in `ks794-verify-file-fields-are-published.test.ts`.

## Test Evidence

**Touched:** `services/originate/src/originate.openapi.ts`, `docs/openapi/secuura-api.yaml` (regenerated, per the OpenAPI rule), and a new `services/originate/src/__tests__/ks794-verify-file-fields-are-published.test.ts`.

**Base:** this worktree **contains** develop `d7cdecf1d2eef7dde26dd23120e80c9db3f0e4a9` (`git merge-base --is-ancestor` → yes), so unlike my two earlier PRs this round, **these counts measure the combined tree**, not a pre-merge base.

**Ran** — `worktrees/s-b29-ks794`, `packages/shared` BUILT (88 dist files):

| arm | result |
|---|---|
| originate BARE (both files restored pre-edit, sha256-verified) | **878 passed / 878, 74 suites**, rc 0 |
| originate PATCHED, before the cell file existed | **878 passed / 878, 74 suites**, rc 0 |
| originate PATCHED, with the cell file | **881 passed / 881, 75 suites**, rc 0 (+3 cells) |
| `packages/shared`, `npx vitest run` | **941 passed / 941, 48 files**, rc 0 |
| `tsc --noEmit` in `services/originate` | rc 0 |
| `npm run check:openapi` | **rc 0** — `CHECK PASS: on-disk YAML matches generated`, and `check-spec-examples`: 405 example blocks, every published example resolves to the fixture set |

The schema-only arms reading 878 either side is the point: adding optional fields to a shared base breaks no existing cell. `packages/shared` is run because its guard suites read originate sources by TEXT.

**Planted-drift control, two-sided.** A **one-character** change to a published description in the on-disk yaml, with nothing regenerated → `check:openapi` **rc 1**, `[gen-openapi] CHECK FAIL: generated YAML differs from on-disk version`. Restored by content, sha256 identical (`bc67c11bec447622`) → **rc 0**. So the green above is a check that can fail.

**Red-proved one conjunct per arm, six arms, each reddening exactly the named cell:**

| arm | conjunct falsified | cell(s) that red |
|---|---|---|
| R1 | `fileSize` removed from `VerifyResponse` | V1PUBLISHESBOTH + NOTONLYPROSE |
| R2 | `fileHash` removed from `VerifyResponse` | V1PUBLISHESBOTH + NOTONLYPROSE |
| R3 | `fileSize` removed from `V2VerifyResponse` | V2PUBLISHESFILESIZEONLY + NOTONLYPROSE |
| R4 | the asymmetry "tidied away" — `fileHash` **added** to `V2VerifyResponse` | V2PUBLISHESFILESIZEONLY |
| R5 | v1 `fileSize` typed as a string | V1PUBLISHESBOTH |
| R6 | v1 `fileHash` made **required** | V1PUBLISHESBOTH |

**R6 is worth reading, because its first version proved nothing.** Dropping `.optional()` alone gives **TS2769 at the schema's own `.openapi({ example })`** — the published example carries no `fileHash`, so a required field makes that example fail the inferred input type, and **the suite never compiles**. A compile-breaking tamper reds with nothing having run. The runner's `LOADFAIL` verdict caught it instead of scoring it, and the arm was rewritten to fix the example too, so the file compiles and the cell is the only thing that reds. **The fact that fell out is worth keeping: optionality here is enforced by the example block at compile time, independently of any cell.**

Every tamper asserts its anchor before applying. `fileSize: z.number().int().optional().openapi({` occurs **twice** — once per schema — so those arms tamper **by line number with the surrounding content asserted**, located from a unique description line at a fixed offset; a wrong offset aborts the run rather than guessing an occurrence. Restores are by content with sha256 asserted.

**NOT run / NOT covered:**
- **Legs 3, 4 and 8 NOT run** (local stack not up): `12/15 ran; legs 3, 4, 8 NOT run (local stack not up)`. **Leg 8 is the served-spec-vs-yaml check and it is the leg closest to this change**, since this PR moves the yaml — its absence is the most significant gap here and is named rather than waved through. The yaml *is* proven to match the generator by `check:openapi`; what is unproven is that the **gateway serves** the regenerated document.
- No runtime behaviour is exercised, because none changes: the handlers already returned these fields. The claim is about the published contract.
- The v1/v2 naming divergence is **documented and asserted, not fixed**. Renaming a published field is out of scope here.

Refs KS-794

🤖 Generated with [Claude Code](https://claude.com/claude-code)

## Push gate — and this is the fleet's first measurement of the quadruple ON `d7cdecf1`

`pre_push_hook_base` **28/0** · `fixture_guard` **6/0** · `run_shell_suites` **49/0** · shell suites **60 passed / 0 failed, 0 skipped (of 60)** · `^FIXTURE BUILD FAILED` **0 times**. Preflight **INCOMPLETE — 12/15 legs ran, 3 SKIPPED (legs 3, 4, 8 — local stack not up)**. That is not a pass and is not quoted as one.

Unlike a pre-merge worktree, **this one contains the new develop**: my head's parent is `d7cdecf1d2eef7dde26dd23120e80c9db3f0e4a9` exactly. And the quadruple is attributable to that base rather than to this change — of the three files this PR touches, **0** are under `Blockchain/Dev/scripts/{__tests__,preflight,audit}/` or `.githooks/`, which is where every counted suite and everything those suites read by text lives (control: 2 of the 3 are under `services/originate/`). So the expected figures the 19:27Z fleet declaration carried as UNMEASURED are now measured.



### HEAD COMMIT MESSAGE TEXT_SHA256 0d37ff694c9c98c3313b8957d21a34929c79cb2f46b70f6205141140df6543ab

KS-794: declare fileSize and fileHash on the verify schemas

Both verify-file handlers return fileSize on every 200, and the v1 one also
returns fileHash, while neither response schema declared any of them. Both bases
are .passthrough(), so the responses validated and nothing went red — the
contract was simply narrower than the behaviour.

Option (1) from the ticket: optional fields on the two BASE schemas. No new
schema, no new example, no allowlist entry. The alternative — .extend() into new
registered schemas — copies the base example across, and the E8
identifier-literal guard correctly refuses the copies; an allowlist entry for a
schema just created would carry a justification that is false of it.

fileHash is declared on VerifyResponse ONLY, which corrects the ticket's "same
treatment" wording. Measured at source: v1 verify-file returns fileHash; the v2
handler computes the same sha256 over the same bytes and returns it as hash, and
never a fileHash. Declaring fileHash on V2VerifyResponse would publish a field no
v2 operation emits. Neither name is being renamed — that is a breaking change —
so the divergence is documented in both response descriptions and asserted by a
cell, so it cannot be "tidied away" by a reader who takes it for an oversight.

FIVE operations' published schemas move, not two, because both bases are shared.
Confirmed by walking the regenerated yaml: VerifyResponse is referenced by POST
/api/documents/{id}/verify, POST /api/verification/verify and POST
/api/verification/verify-file; V2VerifyResponse by POST
/api/v2/verification/verify and POST /api/v2/verification/verify-file. Three of
the five return neither field; "optional and absent" is an honest description of
those, and that trade is what the ticket proposes.

The two 200 descriptions no longer claim the fields are undeclared, because they
no longer are.

A cell file is added because check:openapi cannot see this: it proves the
committed yaml matches what the generator emits, not that the generator declares
any particular field. Delete the two lines, regenerate, and check:openapi is
green again on a spec that has silently lost them.

originate 878 -> 881, 74 -> 75 suites. check:openapi rc 0 with a planted-drift
control that fires.

Refs KS-794

Co-Authored-By: Claude Opus 5 <noreply@anthropic.com>



### PUSH LOG STOP COUNTS (READ, bounded region; /Volumes/DevMASTER/!CODING/Secuura/Blockchain/5_Project_History/2026-09-26_seatB-29th/raise/s-b29-ks794-737a4069c631-push.out)

```
{
 "log": "/Volumes/DevMASTER/!CODING/Secuura/Blockchain/5_Project_History/2026-09-26_seatB-29th/raise/s-b29-ks794-737a4069c631-push.out",
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
 "start": "2026-09-25T20:00:21Z PUSH START",
 "end": "2026-09-25T20:07:14Z push rc=0"
}
```

## #1277 KS-1319 (Seat L7, T2) — head 702171eaadbeb0a9d830237ec6fd86219311477c

#1277 ticket line: #1277 is KS-1319.

### PR BODY (gh_body_1277.md) TEXT_SHA256 f7d813a2963a0acfbed0d1eaa1c3df3265e75efcce06d6b936da9d6b645cf2d7

#1277 KS-1319: the wiring check survives a comment-out, the derivation misses nested and async walkers
head 702171eaadbeb0a9d830237ec6fd86219311477c

## BLUF

Test-only, one file. **The wiring check could be satisfied by a commented-out line** — that is item 1, and the proof that matters is the second arm: under the same tamper, the old check stays **fully green**. Item 2 widens the derivation and proves the new coverage on a fixture, because neither shape exists in this package yet. Item 3 is **recorded as accepted**, not resolved, with the measurement.

`Refs KS-1319`

> **Base:** branched from `4db87c3e4b98`; develop is now `d7cdecf1d2ee`, which this worktree does not contain. The STOP counts below describe that base plus this change.

## Item 1 — a `//` does not remove a string

The cell read the config's **source text**: `expect(config).toContain('setupFiles')`. Comment the setting out and the strings are still there, so unhooking the budget left the cell green. The config is now **imported** and its resolved `test.setupFiles` read, which no comment can fake.

| arm | result |
|---|---|
| `setupFiles` commented out, **my check** | the wiring cell **REDS** |
| `setupFiles` commented out, **the old check alone** | **7/7 fully green** |

**My first version of that second arm was worthless** — I left my own assertions in the cell beside the old ones, so it reddened either way and proved nothing about the old check. Re-run with the old substring check in isolation; that is the row above.

## Item 2 — nested and async walkers were invisible, and the fix had to be provable

The derivation was `readdirSync(TESTS_DIR)` — one level — with three synchronous markers. It is now recursive and carries async markers.

**Measured before building, and it changed the shape of the work:**
- recursion finds **nothing new** today — `support/` is the only sub-directory and holds no walker;
- the async markers match **nothing** — **zero** files under `src/__tests__` use `readdir(`, `opendir`, `fs.promises`, `node:fs/promises`, `glob(` or `globSync`.

So neither could be proven against the real corpus. **A marker that has never matched anything is a marker nobody has shown to work.** The coverage is therefore proved on a **fixture tree** — a nested sync walker, a top-level async one, and a non-walker — where the derivation must return exactly the two walkers. Removing the recursion reds that cell **and only that cell**.

A second new cell **names what is still not covered**, with the first of the three pinned on a fixture:

1. a walk reached through a **helper in another module** — not seen (pinned);
2. a walk built from a **computed string** — not seen;
3. a marker appearing only inside a **comment** — over-reports, which is the safe direction.

Closing (1) and (2) means parsing, which is a larger change than a timeout list justifies.

## Item 3 — TS1343 recorded as accepted

`import.meta.url` at `:27` is TS1343 under the package's own commonjs program. **It is not this file's problem:** 9 TS1343 across the package, 4 of them in `ks256-spec-example-contract.test.ts`, 1 here. It is invisible to `tsc -p .` for the same reason as everything on **KS-1329** — `tsconfig.json` excludes `src/__tests__` — and "fixing" it here alone would mean dropping `import.meta` in one file while eight others keep it. Carried on KS-1329.

## Test Evidence

**Touched**
- `packages/shared/src/__tests__/walkTimeouts.test.ts` — the wiring cell, the derivation, and two new cells.

**Ran**
- `packages/shared`: **941/941 bare → 943/943 patched**, 48 files, **+2 = the fixture cell and the disclosed-limits cell**. `npx vitest run --no-file-parallelism` in `s-l7-ks1319`, at base `4db87c3e4b98`, load **8.50** bare / **9.44** patched.
- **Zero `Test timed out in 5000ms`** in the run; `walkTimeouts` re-run **solo** afterwards at load 7.59, green — per this ticket's own rule about reading a timeout as a load class.
- `npx tsc -p . --noEmit` rc 0; `npm run build` rc 0.
- Both red-proof arms above; config and test file restored **byte-identical** after each.
- **Push gate:** `PREFLIGHT INCOMPLETE — 12/15 legs ran, 3 SKIPPED. Nothing failed.` (legs 3, 4, 8 — local stack not up; not quoted as a pass). STOP count with `packages/shared` built: `pre_push_hook_base` **28/0** · `fixture_guard` **6/0** · `run_shell_suites` **49/0** · shell suites **60 of 60**.

**NOT run**
- Legs 3, 4, 8.
- **The end-to-end budget proof is not a standing cell** — a 6 s cell would be paid on every run forever. The wiring is pinned by the imported config instead, which is the honest scope of what a test here can assert about its own runner.
- **The async markers are not exercised by any real suite** — by construction, since none exists. The fixture is what proves them.
- **TS1343 is not resolved**, and the three named blind spots are not closed.
- Nothing outside `src/__tests__/walkTimeouts.test.ts` is touched; `vitest.config.ts` is read, never modified.

**Migrations + config**
- **None.**



### HEAD COMMIT MESSAGE TEXT_SHA256 2b1a6a2ae1b267ca9dd0ae7b9e9bff4737a5319a340a0e83596d43c5a6d9489a

KS-1319: the wiring check survives a comment-out, the derivation misses nested and async walkers

Test-only, one file.

ITEM 1 -- the wiring check could be satisfied by a COMMENTED-OUT line. It
read the config's SOURCE TEXT with toContain('setupFiles'), and `//` does
not remove a string. So unhooking the budget left the cell green. The
config is now IMPORTED and its RESOLVED test.setupFiles read, which no
comment can fake.

Proved BOTH sides, and the second arm is the one that matters:

  setupFiles commented out, MY check      -> the wiring cell REDS
  setupFiles commented out, the OLD check -> 7/7 FULLY GREEN

The first version of that second arm was worthless: I left my own
assertions in the cell alongside the old ones, so it reddened either way
and proved nothing. Re-run with the old substring check ALONE.

ITEM 2 -- the derivation was `readdirSync(TESTS_DIR)`, one level, with
three synchronous markers. A walker in a sub-directory, or one using an
async spelling, got the default budget and nothing said so. It is now
recursive and carries the async markers.

Measured first, because it changes what the guard can catch: recursion
finds nothing new today (`support/` is the only sub-directory and holds
no walker) and the async markers match NOTHING -- zero files under
src/__tests__ use readdir(, opendir, fs.promises, node:fs/promises,
glob( or globSync. So neither could be proven against the real corpus. A
marker that has never matched anything is a marker nobody has shown to
work.

So the coverage is proved on a FIXTURE tree instead: a nested sync walker
plus a top-level async one plus a non-walker, and the derivation must
return exactly the two walkers. Removing the recursion reds that cell and
only that cell.

A second new cell NAMES what the derivation still does not cover, with
the first of them pinned on a fixture: a walk reached through a helper in
another module is NOT seen. The other two -- a computed string, and a
marker appearing only inside a comment -- are recorded in the same place.
The comment case over-reports, which is the safe direction; the other two
do not. Closing them means parsing, which is a larger change than a
timeout list justifies.

ITEM 3, TS1343 -- RECORDED AS ACCEPTED, not resolved. `import.meta.url`
at :27 is TS1343 under the package's own commonjs program. It is not one
file's problem: 9 TS1343 across the package, 4 of them in
ks256-spec-example-contract.test.ts, 1 here. It is invisible to
`tsc -p .` for the same reason as everything else in KS-1329 --
tsconfig.json excludes src/__tests__ -- and "fixing" it here alone would
mean dropping import.meta in one file while eight others keep it.
Carried on KS-1329 with the rest.

packages/shared 941/941 bare -> 943/943 patched (48 files, +2 = the
fixture cell and the disclosed-limits cell), vitest run
--no-file-parallelism in s-l7-ks1319, at base 4db87c3e4b98, load 8.50
bare / 9.44 patched. Zero `Test timed out in 5000ms` in the run;
walkTimeouts re-run solo afterwards at load 7.59, green. tsc -p . --noEmit
rc 0, npm run build rc 0.

Refs KS-1319

Co-Authored-By: Claude Opus 5 <noreply@anthropic.com>



### PUSH LOG STOP COUNTS (READ, bounded region; /Volumes/DevMASTER/!CODING/Secuura/Blockchain/5_Project_History/2026-09-26_seatL7/raise/s-l7-ks1319-702171eaadbe-push.out)

```
{
 "log": "/Volumes/DevMASTER/!CODING/Secuura/Blockchain/5_Project_History/2026-09-26_seatL7/raise/s-l7-ks1319-702171eaadbe-push.out",
 "lines": 1300,
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
 "start": "2026-09-25T20:07:56Z PUSH START",
 "end": "2026-09-25T20:14:35Z push rc=0"
}
```

## #1278 KS-1314 (Seat L7, T2) — head c321bcce2a9ae7e2c3d5da65f3c1d64fc3295de9

#1278 ticket line: #1278 is KS-1314.

### PR BODY (gh_body_1278.md) TEXT_SHA256 74c901dccba556c35172d02d21192724df1e748aa94cd202f8772d59ca295325

#1278 KS-1314: a prettier-wrapped parser import evaded the routing check; pin the loaders; record the canary spawn
head c321bcce2a9ae7e2c3d5da65f3c1d64fc3295de9

## BLUF

Test-only, two files. **A parser import that prettier has wrapped evaded the routing check entirely** — and the fixture proving it is *captured from this package's own prettier*, because my first attempt at writing one by hand didn't wrap at all. Plus a cell pinning the product loaders, and the canary's spawn recorded with its measured cost.

`Refs KS-1314`

> **Base:** branched from `4db87c3e4b98`. This is a `systemTest/` path, so **no preflight ran** and **no fleet STOP count was executed or is quoted**.

## Item 1 — a wrapped import hides the specifier from every line-anchored pattern

`parserImportSites()` matches line by line. When prettier wraps a statement the first line is `import {` and the module name only appears on the **last** line, `} from '<parser>';`. No pattern sees it.

**Measured before the fix:** `parserImportSites(PRETTIER_WRAPPED_IMPORT)` → `[]`, while the **identical single-line import was caught**.

**The fixture is captured, not typed**, and this mattered: my first candidate was a 99-character import, and **prettier left it on one line** — `printWidth` here is 120. A hand-written "wrapped import" can be wrapped at the wrong column and pin a shape prettier never emits. The real shape came from `npx prettier --stdin-filepath` on a 136-character import: 12 lines, `tabWidth: 4`.

Multi-line `import`/`export` statements are now collapsed onto one logical line before matching, **bounded at 40 lines** so an unterminated statement cannot swallow the file.

**Controls in the cell:** a wrapped import of *something else* is not a hit; an unterminated statement yields at most one.

## Item 2 — nothing pinned the thing the property is about

The routing cells read only **this suite's own source**. The suite could be perfectly routed while `runner/config_loader.ts` parsed the file itself. A new cell pins that every product loader calls `readYaml()` and imports no parser.

**Its control is the load-bearing part:** `utils/yaml.ts` is asserted to be the **one** module that *does* import the parser. If that ever reads `[]`, the instrument has stopped seeing real imports and every other assertion in the cell is vacuous.

## Item 3 — the spawn stays, recorded with its cost

**Measured: 193 ms of the file's 220 ms.** Each alternative is worse:

- **import the parser in-process** — it would (correctly) trip the routing cell, so the only way is a computed specifier: deliberately evading this suite's own guard in order to test it;
- **capture the raw error once as a fixture** — it stops being a live witness the moment js-yaml changes its message, which is exactly how the original canary was lost;
- **drop the raw half** — the claim is comparative ("the raw parser prints the file, `readYaml` does not"), and half a comparison proves nothing.

193 ms is the cheapest honest form, and the file now says so rather than leaving it to be re-litigated.

## Red-proof, re-run against the FINAL bytes

The first pass predated prettier reformatting both files, so it was re-run rather than quoted from a draft.

| arm | result |
|---|---|
| collapse removed | the **wrapped-import cell reds, alone** |
| a loader imports `js-yaml` | the **loaders cell reds** |
| a loader drops `readYaml()` | the **loaders cell reds** |
| restored | **0 red** |

`runner/config_loader.ts` restored **byte-identical** after each arm.

## Test Evidence

**Touched**
- `tests/unit/support/readYamlRouting.ts` — the collapse, and `PRETTIER_WRAPPED_IMPORT`.
- `tests/unit/config/sheddingCeiling.test.ts` — two new cells, and the canary's recorded rationale.

**No product file is in this PR.**

**Ran**
- `npm run test:unit` in `s-l7-ks1314/systemTest/performance`, at base `4db87c3e4b98`: **1104/1104 bare → 1106/1106 patched**, 63 files, **+2 = exactly these cells**. Load **9.01** bare / **7.65** patched.
- `npm run lint` → **rc 0** (both tsconfigs and eslint). It caught three things I had not: two prettier wraps and a missing `curly` brace.
- All four red-proof arms above.
- Push: **12 s**, `[format-gate] 1 package(s) checked, 0 skipped, 0 failed`.

**NOT run**
- **No preflight, no fleet STOP count** — `systemTest/` path.
- **KS-1300 item 1 (READYAML-UNGATED) is deliberately out of scope**: wiring this suite into a gate touches the push gate, which is not in this lane. So these cells are still executed only by hand.
- **The collapse is text-level, not a parser.** A parser import assembled from a computed string still evades it, as does one reached through a helper in another module.
- The canary's 193 ms is measured on this box at this load; it is a cost, not a budget.

**Migrations + config**
- **None.**



### HEAD COMMIT MESSAGE TEXT_SHA256 d6fd91c676cc069342a180d7076eb965c57ef0ba6a9fe3f03852a1d76c5b0961

KS-1314: a prettier-wrapped parser import evaded the routing check; pin the loaders; record the canary spawn

Test-only, two files.

ITEM 1 -- parserImportSites() is line-anchored, so a statement prettier
has WRAPPED hides the module name from every pattern: the first line is
`import {` and the specifier only appears on the last, `} from '...';`.

The fixture is CAPTURED from this package's own prettier, never typed.
The wrap point is a property of prettier.config.js (printWidth 120,
tabWidth 4), not of anyone's memory -- a first attempt at 99 characters
did NOT wrap, which is exactly the way a hand-written "wrapped import"
pins a shape prettier never emits. A 136-character import wraps to 12
lines, and that is what PRETTIER_WRAPPED_IMPORT holds.

Measured before the fix: parserImportSites(PRETTIER_WRAPPED_IMPORT)
returned [] while the identical SINGLE-LINE import was caught.

Multi-line import/export statements are now collapsed onto one logical
line before matching, bounded at 40 lines so an unterminated statement
cannot swallow the file. Controls: a wrapped import of something ELSE is
not a hit, and an unterminated statement yields at most one.

ITEM 2 -- nothing asserted the thing the property is actually about. The
routing cells read only THIS SUITE's own source, so the suite could be
perfectly routed while runner/config_loader.ts parsed the file itself. A
new cell pins that every product loader calls readYaml() and imports no
parser, with utils/yaml.ts asserted to be the ONE module that does import
it -- if that ever reads [], the instrument has stopped seeing real
imports and every other assertion in the cell is vacuous.

ITEM 3 -- the canary's per-run child spawn STAYS, recorded not removed.
MEASURED: 193 ms of the file's 220 ms. The alternatives are each worse:
importing the parser in-process would correctly trip the routing cell, so
the only way is a computed specifier -- deliberately evading this suite's
own guard in order to test it; a captured fixture of the raw error stops
being a live witness the moment js-yaml changes its message, which is how
the original canary was lost; and dropping the raw half leaves half of a
comparative claim, which proves nothing.

Red-proofs, RE-RUN against the final bytes after prettier reformatted
both files (the first pass predated that):

  collapse removed          -> the wrapped-import cell reds, alone
  a loader imports js-yaml  -> the loaders cell reds
  a loader drops readYaml() -> the loaders cell reds
  restored                  -> 0 red

runner/config_loader.ts restored byte-identical after each arm; no
product file is in this PR.

systemTest/performance 1104/1104 bare -> 1106/1106 patched (63 files, +2
= the wrapped-import cell and the loaders cell), `npm run test:unit` in
s-l7-ks1314, at base 4db87c3e4b98, load 9.01 bare / 7.65 patched.
`npm run lint` rc 0 -- both tsconfigs and eslint. Lint caught three
things I had not: two prettier wraps and a missing `curly` brace.

KS-1300 item 1 (READYAML-UNGATED) is deliberately NOT here: wiring this
suite into a gate touches the push gate, which is not in this lane.

Refs KS-1314

Co-Authored-By: Claude Opus 5 <noreply@anthropic.com>



### PUSH LOG STOP COUNTS (READ, bounded region; /Volumes/DevMASTER/!CODING/Secuura/Blockchain/5_Project_History/2026-09-26_seatL7/raise/s-l7-ks1314-c321bcce2a9a-push.out)

```
{
 "log": "/Volumes/DevMASTER/!CODING/Secuura/Blockchain/5_Project_History/2026-09-26_seatL7/raise/s-l7-ks1314-c321bcce2a9a-push.out",
 "lines": 11,
 "pre_push_hook_base": "NOT FOUND",
 "fixture_guard": "NOT FOUND",
 "run_shell_suites_region": "NOT FOUND",
 "run_shell_suites_prefixed": "NOT FOUND",
 "shell_suites": "NOT FOUND",
 "CONTROL_absent_header": "NOT FOUND",
 "fixture_build_failed_lines": 0,
 "verdict_line": "NONE",
 "preflight_ran": false,
 "rc": "0",
 "start": "2026-09-25T20:22:50Z PUSH START",
 "end": "2026-09-25T20:23:00Z push rc=0"
}
```

## #1279 KS-1306 (Seat B 29th, T2) — head dabde931df5e02e45272b70f2fe75fb3dab6ed38

#1279 ticket line: #1279 is KS-1306.

### PR BODY (gh_body_1279.md) TEXT_SHA256 06b2a59926cac94e9f66eb68281056270ba2266dbbb5a6b761156f52eba217dd

#1279 KS-1306: assert rolsuper alongside rolbypassrls on both DSNs
head dabde931df5e02e45272b70f2fe75fb3dab6ed38

## What

The KS-980 D1 cell asserted `rolbypassrls` alone. A Postgres **SUPERUSER bypasses RLS regardless of `rolbypassrls`**, so a role with `rolsuper = true, rolbypassrls = false` satisfied the cell while being exactly the thing the cell reads as *"a role RLS constrains"*.

`rolsuper` is now asserted alongside it — as a **value** on the `platform_bypass` path, where `false` is the property under test, and as a **type** on the `bypassrls` path, where either setting is a legitimate way to provision an admin role. Pinning a value there would refuse a valid instance; asserting the type still fails if the column stops being read, which is the failure mode that matters.

## The blind spot is measured, not argued — and the ticket's own framing is confirmed

On a disposable Postgres built the documented way (`docker/init` + `scripts/run-migrations.sh`; **49 migrations applied / 0 failed**, with the tracker table read **independently** of the runner's own `Summary` line, and `048` present), I created a role with `SUPERUSER NOBYPASSRLS` and pointed the `platform_bypass` path at it. Role shape asserted before use: `s_b29_super_nobypass super=true bypassrls=false`.

| arm | result |
|---|---|
| **PRE-EDIT `D1` cell**, blind role | **PASSES** — the blind spot is real and reachable, not theoretical |
| **PRE-EDIT `D2`** GUC cell, same role | **FAILS** — the consequence was caught by a *different* cell, exactly as this ticket states |
| **PATCHED `D1`**, same role | **REDS**, and the failure names `rolsuper` |
| **PATCHED `D1`**, the honest app role | **passes, 6/6** — the new conjunct is not a blanket refusal |

The first version of that first arm asserted the pre-edit **suite** passed, and it failed — because a superuser also breaks `D2`. The claim is about `D1`, so the instrument had to read `D1`; a suite-level exit code cannot. Verdicts come from `--json` `fullName`.

Also measured on this instance, and it is why the ticket matters here rather than in the abstract: the admin role `docker/init` provisions is `rolbypassrls = true, **rolsuper = true**`.

## The widening, recorded as one

**Before this, the suite performed no host, port or disposability check at all.** It required both DSNs to be *set* (throwing at the two gates) and would otherwise connect to a shared or remote Postgres without complaint — **and it INSERTs rows**. The #1262 precedent is that a test which writes to a database must be unable to reach a shared one.

It now refuses a **non-loopback host** and refuses the **shared-stack ports**. The compose stack port is **READ from `docker-compose.yml`'s own default** (`POSTGRES_EXTERNAL_PORT:-6432`, proven to match at `6432`) rather than pasted, so the guard cannot drift away from the stack it protects. `5432` is refused as Postgres's own default. If the compose file cannot be read, `6432` is still refused — it fails closed.

**A seat's port RANGE was deliberately not used, unlike #1262.** That cell installs a **trigger**, so its range is part of a DDL containment argument. This suite writes only INSERTs, and a hardcoded range would refuse every runner outside it — a later formal test pass, or a gate on another seat's ports. Loopback plus shared-port refusal are the two properties that actually protect the row writes, and neither is brittle. **If the range is wanted anyway, say so and it is a one-line addition** — I did not want to narrow who can run this suite on my own judgement.

## Test Evidence

**Touched:** `services/originate/src/__tests__/ks597-issuer-organization-id.integration.test.ts` (test-only).

**Base:** this worktree **contains** develop `d7cdecf1d2eef7dde26dd23120e80c9db3f0e4a9`.

| arm | result |
|---|---|
| `ks597` integration BARE, `--config jest.integration.config.js --runInBand` | **6 passed / 6**, rc 0 |
| `ks597` integration PATCHED, same command | **6 passed / 6**, rc 0 |
| originate unit, `npx jest --runInBand` | **878 passed / 878, 74 suites**, rc 0 |
| `packages/shared`, `npx vitest run` | **941 passed / 941, 48 files**, rc 0 |
| `tsc --noEmit` in `services/originate` | rc 0 |

**`No tests found` matched 0 times** in the integration runs, checked explicitly — a `No tests found` exit 1 is a zero-executed run, not a pass, and this was neither.

**Eight arms, 0 failed**, counted from a tally file rather than shell variables: the four in the table above, plus the DSN guard — a remote host refused with the host named; port `6432` refused (and `6432` proven to have been *read* from `docker-compose.yml`); port `5432` refused; and a **control** that my own `127.0.0.1:55412` is accepted, so the guard discriminates rather than refusing every port.

**My disposable Postgres:** container `s-b29-pg-ks1306`, image `postgres:15-alpine` **read from `docker-compose.yml`** with the script refusing any `:latest`, bound to `127.0.0.1:55412` only, anonymous volume created with `-v` so it can be proven gone, password generated fresh and **asserted different from the compose default read from the file** (so no credential literal enters the tree). Port proven free immediately before binding, against a control showing 3 listeners on `5432`. **55419 was read and left alone** — it is reserved for the #1262 gate.

**NOT run / NOT covered:**
- **Legs 3, 4 and 8 NOT run** (local stack not up): `12/15 ran; legs 3, 4, 8 NOT run (local stack not up)`. No spec moves, so no LEG-8-PORT reading.
- The `SUPERUSER NOBYPASSRLS` role exists only in my throwaway instance and is **not** created by the committed cell — the cell writes no DDL, which is why the #1262 DDL-refusal rule does not bind it.
- The guard checks host and port. It does **not** verify the database is genuinely disposable (empty, or freshly migrated); that is not decidable from a DSN, and the docblock says so rather than implying a stronger property.

Refs KS-1306

🤖 Generated with [Claude Code](https://claude.com/claude-code)



### HEAD COMMIT MESSAGE TEXT_SHA256 b81669069c755685ed4a87920f3ee7f2e25048f328d5857e5ab2194352d38a6d

KS-1306: assert rolsuper alongside rolbypassrls on both DSNs

The KS-980 D1 cell asserted rolbypassrls alone. A Postgres SUPERUSER bypasses RLS
regardless of rolbypassrls, so a role with rolsuper=true and rolbypassrls=false
satisfied the cell while being exactly the thing it reads as "a role RLS
constrains".

Measured rather than argued, on a disposable instance built the documented way
(docker/init + run-migrations.sh, 49 migrations, tracker read independently of the
runner's own summary). With a SUPERUSER NOBYPASSRLS role on the platform_bypass
path, the PRE-EDIT D1 cell PASSES — the blind spot is real and reachable, not
theoretical — while the D2 GUC cell FAILS on the same role, which is this
ticket's own observation that the case was caught by a different cell than a
reader of D1 would assume. After the change, D1 reds on that role and names
rolsuper, and the honest app role still passes 6/6, so the new conjunct is not a
blanket refusal.

rolsuper is asserted as a VALUE on the platform_bypass path, where false is the
property under test, and as a TYPE on the bypassrls path, where either setting is
a legitimate way to provision an admin role — pinning one there would refuse a
valid instance, while asserting the type still fails if the column stops being
read.

Also, a WIDENING recorded as one: the suite performed no host, port or
disposability check at all. It required both DSNs to be SET and would otherwise
connect to a shared or remote Postgres without complaint — and it INSERTs rows.
It now refuses a non-loopback host, and refuses the shared-stack ports. The
compose stack port is READ from docker-compose.yml's own default rather than
pasted, so the guard cannot drift away from the stack it protects.

A seat's port RANGE was deliberately not used, unlike the #1262 precedent: that
cell installs a trigger, so its range is part of a DDL containment argument. This
suite writes only INSERTs, and a hardcoded range would refuse every runner outside
it — a later formal test pass, or a gate on another seat's ports. Loopback plus
shared-port refusal are the two properties that actually protect the row writes.

Refs KS-1306

Co-Authored-By: Claude Opus 5 <noreply@anthropic.com>



### PUSH LOG STOP COUNTS (READ, bounded region; /Volumes/DevMASTER/!CODING/Secuura/Blockchain/5_Project_History/2026-09-26_seatB-29th/raise/s-b29-ks1306-dabde931df5e-push.out)

```
{
 "log": "/Volumes/DevMASTER/!CODING/Secuura/Blockchain/5_Project_History/2026-09-26_seatB-29th/raise/s-b29-ks1306-dabde931df5e-push.out",
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
 "start": "2026-09-25T20:24:23Z PUSH START",
 "end": "2026-09-25T20:31:34Z push rc=0"
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


## SEAT RECORD /Volumes/DevMASTER/!CODING/Secuura/Blockchain/5_Project_History/HANDOVER-seatL7-2026-09-26.md TEXT_SHA256 9e6169ace278af641bb1a92ce34161a371c573e4712b17dbddd3d2252d78119b

# HANDOVER — Seat L7 (2026-09-26, round 25). Written to be read COLD.

## 1. WHERE THINGS STAND

**Queue COMPLETE: 7 of 7 items, 7 PRs, all READY FOR QA. Nothing merged. Nothing deployed. No ticket state moved by me.**

| PR | key(s) | head | family | gate |
|---|---|---|---|---|
| #1263 | KS-1140 | `3c33f936fe39` | packages/shared | preflight 12/15 · STOP 28/0 6/0 49/0 60/60 |
| #1265 | KS-1315 | `87ef6a1b0887` | systemTest/performance | **no preflight** · format gate only |
| #1268 | KS-1318 + KS-1142 + KS-1316 | `a8e0fca70ed4` | packages/shared | preflight 12/15 · STOP all match |
| #1271 | KS-1164 | `c9ea1dc1705f` | systemTest/performance | **no preflight** |
| #1275 | KS-1179 | `d852e56b912f` | packages/shared | preflight 12/15 · STOP all match |
| #1277 | KS-1319 | `702171eaadbe` | packages/shared | preflight 12/15 · STOP all match |
| #1278 | KS-1314 | `c321bcce2a9a` | systemTest/performance | **no preflight** |

**Every one is branched from `4db87c3e4b98`.** develop is `d7cdecf1d2ee` and no worktree of mine contains it, so **every STOP count above describes `4db87c3e4b98` + that change** — not the combined tree. Mailed as COUNT ATTRIBUTION 19:4xZ.

**Ticket filed: KS-1329** — "packages/shared does not type-check `src/__tests__`, hiding 10 errors". Carries the full error table, the probe method, every control note, and the three ks781 errors marked "after #1268 merges".

**Shared checkout `2_Project_Files`: HEAD `3bad652d17cf`, 17 `??` / 0 non-`??` at boot AND at wrap, byte-identical.** No pull, no fetch, no commit there all session. Shared `.git/config` carries **0** lines with my token `l7r25`.

## 2. THE THING TO INHERIT — my harness failed the same way the code does, four times

Every one was caught by a control, never by reading the code. **The pattern: an arm that can only come out red proves nothing. You need the arm that comes out GREEN.**

1. **A control that reds for the wrong reason.** KS-1319's second arm was meant to show the OLD wiring check stayed green under a comment-out. I left my new assertions in the cell beside the old ones, so it reddened either way. Re-run isolated, the old check was **7/7 fully green** — which is the entire finding.
2. **An instrument that cannot see its subject.** A regex extracting "string literals" matched backticks **inside comments**, reporting 138 -> 155 literals for a comment-only edit. Replaced by an emit comparison (`removeComments`, compare bytes).
3. **A probe whose config invented the answer.** The typecheck probe reported 24 errors, then 2, then 10 across three configs. Only a **planted** error settled which was real — and my first read of that control grepped for the VARIABLE NAME when tsc prints the FILE and LINE.
4. **A control that never fired.** A `sed`-based syntax check used GNU syntax on BSD sed, so the tamper never applied and "rc 0" meant nothing.

## 3. A GUARD THAT COULD NOT FAIL, AND HOW IT LOOKED FINE

KS-1319's wiring cell read the config's **source text** for `setupFiles`. `//` does not remove a string. The budget could be unhooked entirely and the cell stayed green. It now **imports** the config and reads the resolved value.

**The general shape: any check that reads source TEXT for a setting is satisfied by that setting commented out.** Grep the repo for `toContain('` against a config file and you will find the next one.

## 4. MEASURE BEFORE BUILDING — three tickets were wrong about their own subject

- **KS-1179 / F-5:** the ticket and the ruling both asked me to correct a docblock. **It was already correct**, fixed in an earlier round with the record left in the file. I changed nothing.
- **KS-1179 / N1:** a comment claimed an `isIP` throw made a cleanup path "live". **`net.isIP` does not throw** — `'x'`, `''`, `null`, `undefined`, `123` all return 0. The path is reachable only under a mock.
- **KS-1314 / item 1:** my first "wrapped import" fixture was 99 characters and **prettier left it on one line**. `printWidth` here is 120. A hand-written wrapped import pins a shape prettier never emits — capture it.

## 5. WHAT I RECORDED INSTEAD OF FIXING, AND WHY

- **TS2349 in `ssrf-guard.ts`.** Four shapes measured, each **relocated** the error: no cast -> TS2349; cast the callee -> TS2769; cast at the call site -> clean but the **emit changes**; assertion on the declaration -> TS2352. Only `as unknown as https.Agent` remained. **Refused:** in an SSRF guard a type the compiler stops checking is the risk to avoid. On KS-1329.
- **TS1343** (`import.meta`): 9 across the package, 4 in one other file. Fixing it here alone would drop `import.meta` in one file while eight keep it. On KS-1329.
- **The canary's per-run spawn** (KS-1314): **193 ms of the file's 220 ms**, and each alternative is worse — in-process needs a computed specifier (evading the suite's own guard to test it), a captured fixture stops being a live witness, and dropping the raw half leaves half a comparative claim.

## 6. THE CROSS-LANE CATCH

KS-1179's F-5 wanted the deadline error text at `ssrf-guard.ts:605` changed. Repo-wide search found **three** hits; two are **exact-string assertions in Seat B 29th's lane** (`services/originate/src/__tests__/ks914-deliver-webhook-blocked-vs-failed.test.ts:76` and `:86`). Changing it would have reddened another seat's suite mid-round. Ruled (c): docblock only, runtime string byte-identical.

**The proof that it stayed identical is the emit comparison, not a diff read:** pristine vs head **12,137 vs 12,137 bytes, 0 diagnostics**, with a control that reds on **one character** of that string. ks914's own cells: **16/16 green at my head**.

## 7. FOR WHOEVER SITS HERE NEXT

- **`ast_equiv.cjs` (copied from B 28th's folder) is the right instrument for "type-only" or "comment-only".** Type assertions and annotations erase at emit, so byte-identical output proves no runtime change AND no string change at once. Its control must red at an **identical emit size** — that is the case a token counter misses.
- **Re-run red-proofs after lint/prettier touches your files.** I had to on KS-1164 and KS-1314; the first pass was against bytes that no longer shipped.
- **`git merge-base --is-ancestor <sha> HEAD` fails identically for "not an ancestor" and "object not in the store".** If the sha is not local, the sound argument is the absence itself.
- **A `?? Blockchain/Dev/packages/shared/None/` directory** came from a python arm reading `os.environ.get('R')` with no default: `None` became a plausible PATH rather than an error. Check `git status` after any scripted run that writes a report.
- **Tools:** `2026-09-26_seatL7/raise/` — `lock25.sh` (10/10), `push25.sh` (8/8), `push25_ff.sh` (18/18), `seatreq25.sh` (8/8, my own LOCK_SEAT change), `containproof25.sh` (7/7, both sides + the read-back), `merge25.py` (never used — no GO arrived).
- **`merge25.py`'s `merge_note` is now REQUIRED** with no default. B 28th made `--seat` required and left the note optional, then omitted it and the inherited default asserted the opposite of their case. **A parameter whose default makes a factual claim is a hardcoded claim with extra steps.**

## 8. 🔴 THE FUSE — unchanged, and it is Kam's alone

**Both audit rows lapse `2026-09-30T00:00Z`, four days out.** From then `audit:gate` and `audit:locks` refuse **every** `Blockchain/Dev` push, from every author — that is #1263, #1268, #1275 and #1277 of mine. Legs 6 and 7 passed on all four. **It needs Kam's own word** — his typed line or mail with `dmarc=pass header.from=me.com`. A relay does not substitute. No open PR names KS-729. Nothing this round averted it.

## 9. RECORDS

`5_Project_History/2026-09-26_seatL7/raise/` — every tool, proof matrix, tamper arm, captured output, push log (named by head sha per KS-1323) and probe config.


