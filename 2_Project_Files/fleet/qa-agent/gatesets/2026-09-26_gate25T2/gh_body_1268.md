#1268 KS-1318 + KS-1142 + KS-1316: ks781 tag set, corpus containment, guard reachability
head a8e0fca70ed41ef061cc99a325b610d27f08c7fb

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

