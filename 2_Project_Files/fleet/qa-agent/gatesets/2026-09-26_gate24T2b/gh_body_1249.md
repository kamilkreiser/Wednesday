#1249 KS-1144 J2CONTROL: give J2's walk a positive control, and record what the "recorded once" line pins
head 6eb283d058184f1f0fabdc3c3184a817db4fb94b

## ⚠ Stacked PR — declared overlap

This branches from **#1248's head** (`2b4960172644`), not from `develop`, and touches **the same file**
(`ks781-p3-3-body-parser-order.test.ts`). That is the declared grouping: #1248 changes the *product*
predicate (the guard walk), this one changes J2's *control* scaffolding, so a red arm stays bisectable
between the two. **The equality target for this PR is the MERGED blob, not the head blob.** #1248 merges
first.

## What this changes

**GF-3 — J2's structural pin had no positive control.** The walk was inline in the cell, with nothing
showing it could find anything: with its three `shapes.push(...)` calls each made `void 0;` the whole file
stayed green — J2 passing with its walk dead. It is now `defaultShapesOf(source)`, with four control cells
feeding it each shape alone plus all three at once.

Measured: **disabling the walk now reds the four controls and does NOT red J2** — the finding restated as a
measurement rather than repeated as a claim.

The object-literal default (`export default { a, b }`, which the real `request-limits.ts` ends with) stays
deliberately invisible, and that exclusion now has its own assertion. Without it, J2's `toEqual([])` on the
real module would be asserting the absence of something the walk never looks for.

**GF-4 — the finding is wrong, and the assertion stays.** It reports that
`recorded once, not once per export site` "cannot fail" because `exported` is a `Map<string, Set<string>>`
and a Set cannot hold `jsonParser` twice. That is true, and it is precisely what the line **pins**:
`addExport` maps an `exportedAs` of `default` back to the **local** name, so the CONTROL fixture — the
modifier export plus `export { jsonParser as default }` — adds the string `jsonParser` **twice**, and only
the Set makes the answer carry it once.

**Measured on this branch's base: replacing that Set with an array reds that cell alone** — 1 failed / 237
passed. So it is a live pin on de-duplication. It is **kept**, with the measurement written beside it in the
code, rather than dropped. This is the one place I have not followed the ticket's proposal, and the reason is
a measurement, not a preference.

## Test Evidence

**Touched:** `Blockchain/Dev/packages/shared/src/__tests__/ks781-p3-3-body-parser-order.test.ts`. One file,
one commit, no `package.json`, no lockfile.

**Ran** (all by the author, on this head; node v24.7.0, vitest 4.1.11):

- `npm test` in `packages/shared` — **47 files / 934 passed / 0 failed**, rc 0, **0 timeouts**, at load 6.84.
  The base for this branch is #1248's head, which measured **930**; so **930 → 934**, exactly the four new
  cells. (#1248 itself is 928 → 930 over `develop`.)
- `npm run build` (tsc) — rc 0.
- `npm run lint` — rc 1, and the finding set is **identical to develop's** (`diff` empty; a control was run to
  show the comparison can detect a change). The single error is the pre-existing `no-control-regex` at
  `:539`, red on `develop` too and already on the backlog.
- **Tamper matrix, 4 arms, all red** (`tamper1144.sh`; restores from a saved byte copy with a sha256
  assertion, never `git checkout`; the runner redirects rather than pipes):

| arm | what it flips | reds |
|---|---|---|
| B1 | the three `shapes.push(...)` disabled — the GF-3 defect | **the four new controls, and NOT J2** |
| B2 | `Set` → array in `addExport` — the GF-4 pin | the `recorded once` control — **only that one** |
| B3 | the walk also sees an object-literal default | the exclusion assertion, and J2 |
| B4 | J2's own expectation flipped | J2 — **only that one** |

B1 is the finding itself: before this change that tamper reddened **nothing at all**.

**NOT run / NOT covered:**

- **R-2 is context only**, no change asked, and nothing here touches it.
- The three default shapes cannot all be legal TypeScript in one module (a module has at most one default
  export), which is why they are `it.each` rows as well as one combined fixture. `createSourceFile` parses
  the combined one happily; `tsc` would not accept it. Stated rather than left to be discovered.
- This guard reads the whole `services/` + `packages/` tree by **text**, so a later merge from another lane
  can move its verdict.
- No environment, no docker, no database, no migration, no config. **Nothing deployed.**

## Which gate ran, and it is not a clean pass

`Blockchain/Dev/` path, so the hook ran — 6 min 20 s. Verbatim:

```
PREFLIGHT INCOMPLETE — 12/15 legs ran, 3 SKIPPED. Nothing failed.
  legs 3 4 8 — local stack not up; you can clear this by starting it.
  This is NOT a pass. Do not quote it as one — say which legs ran.
```

Fleet STOP count, read anchored to each suite's section header (with a control that returns NOT FOUND for a
header that does not exist): `pre_push_hook_base` **28/0**, fixture guard **6/0**, shell suites **60 passed,
0 failed, 0 skipped (of 60)**. No line starting `FIXTURE BUILD FAILED`. `packages/shared` was built before
the push, which is what makes the runner read 60/0 rather than 59/1.

**Migrations + config:** none.

Refs KS-1144

