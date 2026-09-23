# KS-1143 R18-GUARDMENTION TIGHTEN LEG F's GUARD WALK SO A *MENTION* OF A GUARD-BOUND LOCAL IS NOT READ AS A MOUNT — item 1 (GF-1) of the ks781 LEG F guard walk — Wednesday's task for Ornith, CODE_PATCH, **ONE file, MODIFIED IN PLACE, two hunks** (written 06:20:51 AEST on 2026-09-23 by the feed18 drafter)

File: `Blockchain/Dev/packages/shared/src/__tests__/ks781-p3-3-body-parser-order.test.ts`
Tip: `2bc5ccf63b8c40911afb568b03cace066238ffcf`
Runner: `vitest`

Written from develop `2bc5ccf63b8c40911afb568b03cace066238ffcf` (`git ls-remote origin refs/heads/develop` at 06:1x, read verbs only; the object is in the local store, no fetch). The subject file is **5425 lines**; its `routerParserAnalysis` region (`:2241-:2372`), its LEG F cell (`:2454-:2482`) and its wrapper-fixture block (`:2484-:2551`) were read at the tip by the drafter. **Only lines `:2324-:2330` and `:2549-:2551` are touched.**

## THE MODE — read this twice

**CODE_PATCH, ONE file, MODIFIED IN PLACE** (`--- a/<path>` / `+++ b/<path>`, the path exactly as on the `File:` line above). There is no new file and no second file. This subject is BOTH the product (it carries the analyser LEG F is built on) and the suite that grades it — that is what the ticket is about — so the fix and the cell that pins it land in the same file, in two region-disjoint hunks.

## Self-testing — test hunks: 2

REBRIEF by Wednesday at 17:17:12 AEST on 2026-09-23 (the ONE rebrief Kam's 2026-09-16 counter allows; round 1 at 10:5x failed A3 because the harness had no mode for a product that IS its own test — a harness/brief defect, not the model). Nothing else in this brief changed. The checker now applies **hunk 2 (E2, the W6 cell) ALONE at the tip — it must go RED** — then **hunk 1 (E1, the fix) on top — it must go GREEN**. So keep the two hunks in this order: E1 first (`@@ -2324`), E2 second (`@@ -2549`).

## What is wrong (one paragraph)

`routerParserAnalysis`'s guard walk (`:2319-:2334`) decides whether the wrapper feeding a router's routes reaches a control-byte guard. Its second clause at **`:2327`** — `if (ts.isIdentifier(m) && (guardSyms.has(m.text) || guardedWrappers.has(m.text))) { hit = true; return; }` — hits on a bare **identifier**, so a guard-bound local that is merely *named* inside the wrapper counts exactly as if it had been invoked. The file's own docblock at `:2313-:2317` says the opposite in words ("F-09: a guard MENTIONED is not a guard MOUNTED"), and the LEG F failure message at `:2475-:2476` defines `guarded: false` as "the parser runs and nothing after it inspects the body". The measured consequence (ticket KS-1143 item 1, GF-1): turning `services/api-gateway/src/routes/admin.ts:560` `controlByteGuard(req, res, next);` into `void controlByteGuard; next();` leaves the declared entry `'api-gateway/routes/admin.ts': { routes: 19, guarded: true }` (`:2226`) satisfied and the whole suite green, while nineteen parsing admin routes run with the guard never invoked. This task makes the clause hit only on a **call**, and adds one fixture cell that pins it. **The parser-side twin at `:2302` is NOT touched** (ticket item 3, R-1: it over-reports in the SAFE direction and is explicitly "the builder's call"), and **item 2 (GF-2, the guard-BEFORE-parser order) is NOT in this task** — the ticket marks it "Wednesday rates", i.e. an unruled decision.

## The exact change — 2 SMALL EDITS (≤ 3), each its own hunk with real context

**E1 (hunk 1, header `@@ -2324,7 +2324,7 @@`)** — one `-` line, one `+` line: the clause at `:2327` becomes a call-node test. Leading context `:2324-:2326`, trailing context `:2328-:2330`, all six copied byte for byte with their leading spaces (`:2324` and `:2329`/`:2330` have 6 spaces; `:2325-:2328` have 8).

```
@@ -2324,7 +2324,7 @@
       const walk = (m: ts.Node): void => {
         if (hit) return;
         if (guardCallName(m, b)) { hit = true; return; }
-        if (ts.isIdentifier(m) && (guardSyms.has(m.text) || guardedWrappers.has(m.text))) { hit = true; return; }
+        if (ts.isCallExpression(m) && ts.isIdentifier(m.expression) && (guardSyms.has(m.expression.text) || guardedWrappers.has(m.expression.text))) { hit = true; return; }
         ts.forEachChild(m, walk);
       };
       walk(body);
```

**E2 (hunk 2, header `@@ -2549,3 +2549,7 @@`)** — a PURE INSERTION of 4 `+` lines between `:2550` (`  });`, the close of cell W5) and `:2551` (`});`, the close of the `KS-828 — LEG F sees the guard LEAVE a wrapped router` describe at `:2484`). Both anchors are non-blank ASCII; `:2549` is non-blank. The new cell sits INSIDE that describe, so `wrapperModule` (`:2502`) and `routerParserSites` are in scope exactly as they are for W1-W5.

```
@@ -2549,3 +2549,7 @@
     expect(routerParserSites(src, 'x.ts')).toEqual({ routes: 1, guarded: 'none' });
   });
+  it('W6 KS-1143 GF-1 - a MENTION of a guard-bound local inside the wrapper is NOT a mount', () => {
+    const src = wrapperModule('      void g; next();', '  const g = rejectControlBytes();');
+    expect(routerParserSites(src, 'x.ts')).toEqual({ routes: 2, guarded: false });
+  });
 });
```

**Do NOT change:** `:2302` (the parser-side identifier clause — ticket item 3, deliberately left alone), `:2326` (`guardCallName`, which is what keeps W2/W3 green), `:2318` (`const guardedWrappers = new Set<string>();`), the declared map at `:2225-:2228`, the LEG F cell at `:2454-:2481`, cells W1-W5 (`:2519-:2550`), and every other line of the file. Do NOT rename the new cell: the checker names it by the literal prefix `W6 KS-1143 GF-1`.

**Both `+` lines are ASCII only and carry NO backslash (0, counted by the writer), NO backtick (0) and NO `$`.** `wrapperModule`'s two arguments are deliberately written WITHOUT a trailing newline escape: the helper concatenates them between `:2510` and `:2512`, and `'      void g; next();' + '    });'` on one physical line is valid TypeScript, exactly as `'  const g = rejectControlBytes();' + "  const raw = express.json({ limit: '1mb' });"` is. Do not "fix" this by adding an escape.

## Where (parsed into the checklist — every **must change** line must appear as a `-` line in your diff)

* `:2327` — **must change**: `        if (ts.isIdentifier(m) && (guardSyms.has(m.text) || guardedWrappers.has(m.text))) { hit = true; return; }`
* `:2326` — (correct) `        if (guardCallName(m, b)) { hit = true; return; }` — stays (context)
* `:2550` — (correct) `  });` — stays; E2 is INSERT-ONLY and is anchored here, so it has no must-change line

## THIS IS VITEST

`repo.test_runner` begins with `vitest`. The file already imports what it needs (`describe/it/expect` from `'vitest'`, `typescript` as `ts`); **add no import**, `vi.mock` nothing, and never write `jest.*`.

## The test — ONE new cell in the EXISTING suite (no new file)

File: `Blockchain/Dev/packages/shared/src/__tests__/ks781-p3-3-body-parser-order.test.ts`
The input's `reference_test` is `Blockchain/Dev/packages/shared/src/__tests__/ks780-normalise-org-id-one-implementation.test.ts` — a small sibling source-structural guard in the same package, there only to show you that these guards need no mock, no database and no app boot. **You do not edit it.** The mocking shape to copy is the block this cell joins: cells **W1 (`:2519`), W2 (`:2524`), W3 (`:2529`), W4 (`:2534`), W5 (`:2541`)** — each builds a source string with `wrapperModule(inside, before)` (`:2502-:2517`) and asserts `routerParserSites(src, 'x.ts')` against a `{ routes, guarded }` literal. There is no I/O, no database and no app boot: the analyser parses a string with the TypeScript AST. Copy that shape and nothing else.

Cells (every cell RED or CONTROL, nothing optional):
- RED `it('W6 KS-1143 GF-1 - a MENTION of a guard-bound local inside the wrapper is NOT a mount')`: a wrapper whose body names `g` (`void g;`) and calls only `next()` must read `{ routes: 2, guarded: false }`. **At the untouched tip this cell FAILS** — `:2327` hits on the bare identifier `g` and the analyser answers `guarded: true`. It passes only with E1 applied. That is the red.
- CONTROL `W2` (`:2524`, untouched): the same wrapper *invoking* the guard-bound local (`g(req, res, next);`) still reads `guarded: true` — green on both trees, because a call is still a call.
- CONTROL `W4` (`:2534`, untouched): a guard bound at module level and never invoked inside the wrapper still reads `guarded: false` — green on both trees.

## Red cells

- W6 KS-1143 GF-1 - a MENTION of a guard-bound local inside the wrapper is NOT a mount

## Output

Exactly ONE ```diff block, nothing outside it: `--- a/Blockchain/Dev/packages/shared/src/__tests__/ks781-p3-3-body-parser-order.test.ts` / `+++ b/Blockchain/Dev/packages/shared/src/__tests__/ks781-p3-3-body-parser-order.test.ts`, then the TWO hunks above exactly as shown (`@@ -2324,7 +2324,7 @@`, then `@@ -2549,3 +2549,7 @@`), in that order. Every `+` line is its OWN physical line (the INPUT JSON shows this brief's line breaks as the two characters backslash and n inside a JSON string — DECODE them; a `+` line that carries a backslash is a FAIL). Every context line keeps its leading space.

## Premises (measured by reading the tip at 06:1x)

- **The `-` line.** `:2327` byte for byte, 8 leading spaces; `grep -cF` over the file at the tip = **1** (byte-unique).
- **The anchors.** `:2324`, `:2325`, `:2326`, `:2328`, `:2329`, `:2330` are non-blank ASCII; `:2549`, `:2550`, `:2551` are non-blank ASCII. No blank line appears as context in either hunk, and no blank line appears in either hunk at all.
- **Scope of the file.** `routerParserAnalysis` at `:2241`; its two readers `parserRouteCount` (`:2365`) and `routerParserSites` (`:2370`). The ticket cites `:2318` for this clause — that number is from the gate's head `04807ea0e`; **at this tip the clause is `:2327`** and `:2318` is `const guardedWrappers = new Set<string>();`. The brief's numbers are the tip's.
- **Why W2/W3 cannot regress.** `:2326` `guardCallName(m, b)` runs BEFORE the changed clause and already recognises a guard factory call and a guard-bound local's invocation; W3's inline `rejectControlBytes()(req, res, next);` has a CallExpression (not an Identifier) as its callee, so it is caught there, not here.
- **The real corpus.** `ROUTER_MODULE_PARSER_SITES` (`:2225-:2228`) declares exactly two entries: `api-gateway/routes/admin.ts { routes: 19, guarded: true }` and `api-gateway/routes/proxy.ts { routes: 1, guarded: 'none' }`. `admin.ts` binds the guard at `:555` and **invokes** it at `:560` (`      controlByteGuard(req, res, next);`, byte-unique, 6 leading spaces) inside the `mockBodyParser` wrapper (`:557-:562`), so the tightened clause still reads `{ 19, true }` there.
- **Surface.** A unit suite that parses strings and reads service sources from disk. No network, no database, no credentials. **Not an auth surface** — nothing here verifies a token; the subject is a static analyser over body-parser ordering.

## UNMEASURED — stated rather than glossed

The drafter **did not run the suite** (a drafter writes briefs; the checker runs). Two things are therefore reasoned, not measured: (1) that no OTHER cell in this 5425-line file depends on a bare-identifier guard mention — the fixed point's "another wrapper that is itself guarded" leg would also stop hitting on a wrapper passed by NAME rather than called, and no such shape was found in the two declared corpus files, but the whole file was not executed; (2) that `{ routes: 2, guarded: false }` is W6's exact reading. If either is wrong the checker's A5 (green at the tip) fires and the round is cheap.

## Collision

`packages/shared/src/__tests__/ks781-p3-3-body-parser-order.test.ts` is named by no held READY (checked against `night/candidates.md`'s ⚠ list and HELD list at 06:1x) and KS-1143 has **zero rows in `night/done.md`**. KS-953 is a CLASS ticket about the line-number pins in this same file and is SET ASIDE as decision-class — it changes different lines (`ROUTER_MODULE_PARSER_SITES`' line pins, not the guard walk) and nothing is queued on it.

## Notes for the raise (not for the model)

- **Refs KS-1143 item 1 (GF-1) only. Does not close the ticket** — items 2 (GF-2, guard-before-parser) and 3 (R-1, the parser-side twin at `:2302`) are untouched and are named in the PR body as remaining.
- **Raise tier: TIER 2** (a `packages/shared` unit suite; no product service file changes). The diff changes no runtime code at all — `admin.ts` is read, never edited.
- The ticket's fix shapes are the gate's PROPOSALS, explicitly "not ratified". E1 is the ticket's proposal verbatim in its first form (the inline predicate, not the `guardCallName(m, b)` helper variant); a raiser who prefers the helper form can refactor in the same PR without changing W6.
