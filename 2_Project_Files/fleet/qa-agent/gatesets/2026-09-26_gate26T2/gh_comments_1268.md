--- comment 5838129147 by linear[bot] at 2026-09-25T19:11:49Z
<!-- linear-linkback -->
<details>
<summary><a href="https://linear.app/secuura/issue/KS-1318/ks781-j2-the-combined-default-shapes-control-asserts-the-count-of">KS-1318 ks781 J2: the combined default-shapes control asserts the COUNT of shapes, not which shapes</a></summary>
<p>

## BLUF

Non-blocking finding from the tier-2 gate on PR #1249 (KS-1144, merged `8b666a33a2b4`). J2's **combined** control cell asserts the **number** of default-export shapes found, not **which** shapes they are, so it would pass if two shapes were detected under one another's name.

## Detail

`defaultShapesOf()` returns tagged strings — `'export default function'`, `'export default <Kind>'`, `'export { x as default }'`. The per-shape rows each assert the exact tag, and they are the strong cells. The combined fixture, which carries all three at once, asserts only `toHaveLength(3)`.

So a change that made the `export default function` branch emit the `export { x as default }` tag (or made one branch fire twice and another not at all) would leave the combined cell green. The per-shape rows would catch *that* particular swap — but they are fed one shape each, so they cannot see an interaction between branches, which is the only thing the combined fixture is there to test.

## Why it is Polish and not a defect

The walk is correct at the merged tree and the per-shape rows do pin the labels. What is missing is that the **combined** cell, the one cell whose job is the interaction, checks the weakest property available.

## Done when

- ☐ the combined cell asserts the **set of tags**, not the count — e.g. `toEqual([...])` against the three expected strings in source order

## Board search before filing

Literal match over **1,307 issues (includeArchived) and 3,684 comments**: `LENGTH-ONLY` -> 1 (KS-1144, this finding's own record) · `defaultShapesOf` -> 1 (same). **Searched those two terms, 0 open hits outside KS-1144 itself.** Controls: `readYaml` -> 10 hits, fires; `qqx7-fresh-control-never-written-anywhere` -> 0.

⚠ Control note: the nonsense token used earlier today stopped being a control once it was written into two ticket bodies — it then returned 2 hits, itself. A control token has to be one that has never been recorded. This search uses a fresh one.

## Provenance

Tier-2 gate `QA/Secuura-batch1249`, non-blocking (N-1249-a), recorded at the merge of #1249.

Refs KS-1144
</p>
</details>
<details>
<summary><a href="https://linear.app/secuura/issue/KS-1316/ks781-leg-f-a-guard-defined-but-never-called-inside-the-parser">KS-1316 ks781 LEG F: a guard DEFINED but never called inside the parser continuation still reads guarded true (over-reports)</a></summary>
<p>

## BLUF

Pre-existing limit of LEG F's guard walk, recorded by the tier-2 gate on PR #1248 (KS-1143 GF-2, merged `fa25c9b10fb4`). **A guard that is DEFINED but never CALLED inside the parser's continuation still reads** `guarded: true`**.**

This **over-reports**, which is the **unsafe** direction: the leg says something inspects the parsed body when nothing does. It is the same asymmetry KS-1143's own GF-1 was about, one step further in.

## Mechanism

GF-2 moved the walk's start from the whole wrapper body to the parser call's **continuation** — the function-valued arguments of the parser call. Inside that continuation the walk still hits on a **call node whose callee name is a known guard**. It does not establish that the call is reached: a guard call sitting in a branch that never executes, or bound and shadowed, is indistinguishable from one on the path.

Not introduced by #1248 — the predicate it replaced had the same property over a wider region, so GF-2 narrowed the region without changing this. Recorded so the remaining looseness has a name.

## Relationship to what is already open on KS-1143

KS-1143 stays In Progress for the **indirect-invocation false negative**, which is the *opposite* direction (under-reports: a continuation passed by NAME is not followed, so a genuinely mounted guard reads unguarded). **This one over-reports.** Two different directions, two different risks; they are not the same defect and should not be closed by one change without saying which each fix addresses.

## Done when

- ☐ a fixture where the guard call inside the continuation is unreachable reads `guarded: false`, **or**
- ☐ a line in the file records why reachability is deliberately out of scope for a text-level walk, so the limit is stated rather than latent

## Board search before filing

Literal match over **1,305 issues (includeArchived) and 3,677 comments**: `CONT-DEFERRED` -> 1 (KS-1143, this finding's own record) · `parserContinuations` -> **0** · `defined but never` -> 1 (KS-1143) · `never called` -> 17 total / 5 open, each read and none this subject (KS-1291 a stale comment, KS-1185, KS-843, KS-1143 itself). **Searched those four terms, 0 open hits for this defect.** Controls: `readYaml` -> 8 hits, fires; `zzz-nonexistent-token-l6-control` -> 0.

## Provenance

Tier-2 gate `QA/Secuura-batch1243`, non-blocking, recorded at the merge of #1248.

Refs KS-1143
</p>
</details>
<details>
<summary><a href="https://linear.app/secuura/issue/KS-1142/entrypoint-corpus-is-pinned-by-two-hand-maintained-literals-in-two">KS-1142 Entrypoint corpus is pinned by TWO hand-maintained literals in two files — K1's 27-package presence set (`entrypoint-corpus.test.ts`) and ks781's 25-file `CORPUS` (`:1839-1865`) — a package add/remove now moves both; `services/blockchain` + `services/shared` are guarded by K1 alone</a></summary>
<p>

## BLUF

PR #980 (KS-924 + KS-901, merged 2026-09-13) closed the cardinality-floor blind band by pinning every contributing package BY NAME (K1) and made the three blind-spot shapes visible (P1–P3 + the census). The tier-2 gate's class hunt (R-3) found that the same walk is now pinned by a SECOND hand-maintained literal in another file: `ks781-p3-3-body-parser-order.test.ts`'s `CORPUS` — the 25 entrypoint files, asserted `toEqual` and `toBe(25)`. Two literals over one walk drift independently; a package add or remove now moves two files. Fix shape is the GATE'S PROPOSAL, not ratified — the builder's call. One file family, one test pass.

Report: `/Volumes/DevMASTER/!CODING/Testing Agent MAIN/projects/secuura/reports/2026-09-13-ks924-901-980-9c620f890-tier2-r1/report.md` — Records R-3 (class hunt), R-2 (K1 reds on ordinary growth by design). Line numbers are the gate's at `9c620f890`; note the ks781 file on develop is #975's blob (`ad0afd7cb`, +21 −7 above the `6beacc935` this PR was cut against) and #981 moves it again — locate by symbol (`const CORPUS = [`), not by number.

## Items (one test pass)

1. **R-3 — two literals over one walk.** `entrypoint-corpus.test.ts` K1 (`:395`, "every package that contributed a walked file at this SHA still does — pinned BY NAME") pins the 27 contributing packages (incl. `services/blockchain` `:416` and `services/shared` `:429`, which have no entrypoint file). `ks781-p3-3-body-parser-order.test.ts:1839-1865` `const CORPUS = [ 'connectors/whatsapp-bot/src/index.ts', 'services/analytics/src/index.ts', … 'services/wallet-connector/src/server.ts' ]` pins the 25 files that ARE entrypoints; `:1897` `expect(guarded).toEqual(CORPUS);` and `:1916` `expect(CORPUS.length, 'the declared corpus size — update deliberately').toBe(25);`. A new service with an entrypoint reds BOTH (K1 by package, CORPUS by file); a new package without one reds K1 only; a removed entrypoint reds CORPUS only — each red is correct, but the two literals are maintained by hand in two files with no assertion tying them together. **Proposal (the gate's):** one literal imported by both (K1's package set derived from CORPUS's paths ∪ the two entrypoint-less packages, or the reverse), OR a cell in `entrypoint-corpus.test.ts` asserting CORPUS's package set ⊆ K1's literal — so the two cannot drift apart silently. Regression: swap one CORPUS path's package for a package K1 does not list → the new cell reds.
2. **R-2, for context (no change asked):** K1 reds on ORDINARY GROWTH by design — a new package under either root, or a `.ts` appearing under `connectors/libreoffice-extension/src/`, reds K1 until the literal moves; the file's comment `:404-406` says so; K1's title names only the "still does" direction while its body checks both (an under-claim). Whatever shape item 1 takes should keep that property and say it in the title.

## Dedupe (searched before filing)

By symbol over 1,131 KS issues + 908 comments (includeArchived): `CORPUS` and `toEqual(CORPUS)` → KS-831 (Done, archived — the KS-800 guard-side ticket where the literal was pinned; named here, not related) and KS-1141 (another subject — the ks727 CORPUS section); `ks781-p3-3` → 12 hits, none about the CORPUS literal (KS-802 the parser regex, KS-905 the IIFE clause, KS-953 line pins, KS-828/KS-900 the #981 lane, the rest archived); `entrypoint-corpus` / `sourceFilesUnderRoots` → KS-924, KS-901, KS-1140, KS-899/KS-857 (archived), KS-917 (archived). No home; filed new.
</p>
</details>
<!-- linear-review-link -->
<p><a href="https://linear.app/secuura/review/ks-1318-ks-1142-ks-1316-ks781-tag-set-corpus-containment-guard-66b5b59b7399">Review in Linear</a></p>

--- comment 5841576010 by kksecura at 2026-09-26T00:36:46Z
## FIX ROUND 1 of 2 — THE READER RULE, new head `5ac42fafeee11dec596e7e7d833ac82b8b478790`

Fast-forward on this branch; the author has wrapped, so this round is another seat's work and the
history before this commit stays its author's. **No merge-in** — the base this worktree **contains**
is still `4db87c3e4b98`.

**KS-1318's and KS-1142's proven work is untouched, verified rather than asserted:**
`entrypoint-corpus.test.ts` is **byte-identical by blob** to this branch's previous head
(`8a4ce36a3a96…` both sides), and **zero** changed lines in `ks781-…` mention KS-1318 or its tag set.
Only the walk and the new cells moved.

### The cause
`collectInvoked` recorded only `name(...)` — a **direct identifier call**. Every other way of running
a bound function expression left the name out of the set, so the binding read as a definition the
walk would not enter. Nine shapes flipped correct → wrong, all **under**-reporting, which is the
direction that makes LEG F claim nothing inspects the parsed body when something does — including the
alias shape **this file's own comment named while asserting it read `true`**.

### Three rules, each proved independently load-bearing
1. **A bound function expression is a DEFINITION only when its binding is REFERENCED NOWHERE ELSE** in
   the continuation. The decidable question is not "is it called" — that needs control flow — but "is
   it referenced at all". Referenced anywhere else, we cannot say it does not run, so we keep the old
   answer and descend. Same when-in-doubt direction W12 already states.
2. **`NewExpression` arguments are treated like call arguments.** A `NewExpression` is not a
   `CallExpression` to the compiler, so its callback fell through to the generic descent with
   `invoked=false`.
3. **A function expression RETURNED from an invoked one escapes**, so it descends.

### ⚠ Rule 3 is BEYOND the gate's two stated shapes, and it is here because of a measurement
With rules 1 and 2 only, **W14–W17 pass and W18 (`mk()()`) still read `false`** — measured, not
predicted. The returned arrow has **no binding**, so rule 1 cannot see it. The gate's own regression
set requires W18 to read `true`, so a third rule is needed to satisfy the cells as specified. It is
flagged here rather than presented as part of the ruled shape, and it is the narrowest form that
works: only a **returned** function expression, in both return shapes (a concise arrow body and an
explicit `return`).

### The limit is held where it was
`W9` still reads `false`, and **new `W19`** pins that an arrow merely **stored** in an object and
never called still reads `false` — so rule 3 cannot quietly widen until every nested arrow reads
`true`. The `overwide` arm reds **exactly W9 and W19**, so both are live controls rather than cells
that would pass whatever happened.

The code comment asserting the alias shape read `true` is **corrected in place**, not silently
contradicted by the code beneath it.

### Test Evidence
Base this worktree **CONTAINS**: `4db87c3e4b98` (`merge-base --is-ancestor` YES), no merge-in. Fresh
worktree: `npm ci` (1936 packages) and `packages/shared` built.

| suite | result |
|---|---|
| `packages/shared` **BARE** at `a8e0fca70ed4` | **48 files / 947 tests / 0 failed** |
| `packages/shared` **PATCHED** | **48 files / 953 tests / 0 failed** |
| `tsc --noEmit` | **rc 0, zero `error TS`** (the one output line is an npm workspace-config warning) |

Delta **+6 cells**: W14–W19.

**Red proofs — 5 arms, `arms1318.py`, ALL BEHAVED, zero LOADFAIL. Each arm's red set is asserted
EXACTLY, not merely "contains".**

| arm | tamper | reds (exact) |
|---|---|---|
| **noref** | revert ONLY rule 1 | **W14, W15, W16** |
| **nonew** | revert ONLY rule 2 | **W17** |
| **noescape** | revert ONLY rule 3 | **W18** |
| **base** | all three reverts = the walk exactly as at `a8e0fca70ed4` | **W14, W15, W16, W17, W18** |
| **overwide** | descend into EVERY nested function expression | **W9, W19** |

Each rule reds its own cells and no others, so none is carrying another's weight. `base` reproduces
the previous head's behaviour exactly — the five cells the gate identified, and nothing else.

### NOT covered
- **K1b (K1B-SOURCE-TEXT) is NOT built** — non-blocking, not pinned, reach 0, per the gate and the
  coordinator's ruling.
- **W13 remains undecided by design**: a guard inside `if (false)` still reads `true`. Reachability of
  a *statement* is control flow; this change is about whether a *function expression* runs.
- The object-property / array-element case is deliberately **not** covered by rule 3 — that is W19.
- No local stack, so preflight legs 3, 4 and 8 NOT run. No database. No deploy.

