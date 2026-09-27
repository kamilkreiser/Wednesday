#1311 KS-1346 A: log a thrown object's type and field names, never its values
head 451a36e8e825d3001e16f5fca6bb3517a81dbe06

## BLUF
`services/originate/src/routes/systemErrors.ts`'s `fail500` logged a **non-Error** throw through `String()`, so a
thrown plain object reached the log as `[object Object]` and its content was lost. The 500 **body** was already the
constant text; what changes here is the **log**.

**The repository owner ruled on 2026-09-27: _"Type and field names only"_.**

A non-Error, non-string throw is now logged as `thrown <Ctor> with fields [a, b, c]` — its shape, never its values.
An `Error` still logs exactly its message; a string still logs exactly itself. Both are pinned by controls.

**This replaces #1296.** #1296 is closed unmerged and nothing from it ships.

## Why #1296 is replaced rather than amended — measured, not argued
#1296 used `util.inspect`, which renders the thrown object's **values**. With this PR's line tampered back to
`inspect(err)`, the four **A6** control rows — *"no VALUE of a thrown object reaches the log"* — go **RED** alongside
the four A1 rows: **8 failed / 7 passed of 15**. With this PR's line as shipped: **15 / 15**. So the cell pins the
value leak directly, not merely the message shape.

> One correction to the brief this PR was raised from, recorded rather than smoothed over: the addendum predicted
> A6 would stay **green** under that tamper. It does not, and it should not — `inspect(err)` is exactly what puts
> values in the log. The arm still discriminates; it discriminates harder than predicted.

## What changes
- `services/originate/src/routes/systemErrors.ts` (+1 / −1): one expression in `fail500`.
- NEW `services/originate/src/__tests__/ks1346a-systemerrors-fail500-logs-type-and-field-names.test.ts` (+105):
  drives all four admin routes on a real loopback listener by making each route's **own** service call reject,
  exactly as the existing part-A cells for the 500-body work do.

## Provenance
Patch produced by the **local model (the Spark) under a Wednesday brief**, re-verified by this seat. The READY block
is **byte-identical** to the brief's golden and to the run's canonical `patch.diff` (`cmp` rc 0 both; all three
6810 B, sha256 `26325d4c1a7fbba3`). Both sections apply **strict** at the base (`git apply --check -p1`, no
`--recount`, no fuzz), each with a tamper control that fires: section 1 rc 1 on a mutated context line, section 2
rc 1 on a retargeted `+++` path.

## Test Evidence

**Touched:** `routes/systemErrors.ts`; the new `ks1346a-…` cell. Base `94c9c7aa9be7f0c05f4a89cdc532ec6f2fef3812`.
Head commit +106 / −1 over exactly those two paths.

**Ran** (this worktree, `npm ci` 1936 packages, `packages/shared` built):

| what | result |
|---|---|
| RED — the new cell with the product line at the base | **4 failed / 11 passed / 15.** All four reds are `expect(received).toEqual(expected)` **assertions**; all eleven controls green, including the four A6 rows (at the base `String(err)` yields `[object Object]`, which carries no values) |
| GREEN — both files | **15 / 15** |
| EXTRA ARM — the line tampered back to `inspect(err)` | **8 failed / 7 passed / 15** — the four A1 rows **and** the four A6 rows red; A2, A3, A4, A5 stay green |
| originate suite, `jest --runInBand`, BARE at the base | **979 passed / 979**, 84 suites, 0 failed |
| originate suite, `jest --runInBand`, PATCHED at my head | **994 passed / 994**, 85 suites, 0 failed — +15, **zero new reds** |
| `tsc --noEmit` over a program **proven to contain the new cell** | **rc 0, 0 error lines.** The package tsconfig excludes `src/__tests__`; with `exclude: []` the program is **717 files and contains the cell exactly once** (control: an absent filename counts 0) |
| `npm run lint` at base / at head | rc 0 both, **0 errors / 22 warnings** both, problem **set identical** line for line |
| lint control | a planted `debugger;` in the new cell takes lint to rc 1 with `no-debugger` **at that file** — lint sees it |

Every tamper was placed by an anchor asserted to occur exactly once, and every restore verified by whole-file
sha256 against the pre-tamper hash.

**NOT run, and why:**
- **No live stack**, so the in-hook preflight's legs 3, 4 and 8 do not run. Only the gate lines this push printed
  are quoted.
- **Part B (`routes/gdpr.ts`) is a separate PR**, raised next; this one is part A only.
- **No deploy of any kind.**

**Migrations + config:** none. No migration, no `package.json`, no `package-lock.json`, no dependency, no new import.

## Not covered
- The other `fail500` call sites across the originate routers are **not** touched here; this PR is the systemErrors
  one, and part B is gdpr. Whether the remaining routers share the shape is not measured in this PR.
- Field **names** can themselves be sensitive in principle (a key called `ssn` tells a reader the object had one).
  The ruling is explicit that names are acceptable and values are not; recorded, not litigated.
- A thrown object with a null prototype renders as `thrown object with fields [...]`; no cell pins that case.

Refs KS-1346

