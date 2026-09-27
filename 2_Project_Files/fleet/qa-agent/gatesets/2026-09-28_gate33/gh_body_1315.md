#1315 KS-1220: pin padded wildcards carried by non-ASCII whitespace in ks839
head f02ae1a09d90d8254c027e8e89b9069c9c153000

## BLUF
The `ks839` cells already pinned that a **padded** wildcard grants nothing — but every carrier they used was
**ASCII** whitespace. A second tokenizer written as `entry.split(/[ \t\n,]+/)` would pass all six of them while a
wildcard padded with a **no-break space**, a **vertical tab**, an **ideographic space**, a **line separator** or a
**byte-order mark** still reached the allow list. One cell closes that, over five carriers. `EXPECTED_CELLS` goes
6 → 7.

**Test-only. No product line changes.**

Every carrier is built with `String.fromCharCode`, so every added line in this diff is plain ASCII and the file
stays readable in a review pane.

## Proved discriminating, not merely green
| tree | result |
|---|---|
| my head, product untouched | **8 / 8** |
| my head, guard tampered to the ASCII-only tokenizer | **1 failed / 7 passed of 8** — exactly the new cell, by assertion |
| the **base** cells (six of them), **same tamper** | **7 / 7 — green** |

That last row is the point: the pre-existing cells cannot see this defect, and the new one can.

**The tamper site was located by an anchor string asserted to occur exactly once**, never by line number — and in
the right file. There are two files called `oauth.ts` in this service; the guard is in
`src/services/oauth.ts` (**1** occurrence of the anchor) and **not** in `src/routes/oauth.ts` (**0**). Both were
grepped before anything was planted. Restored by content with a whole-file sha256 compared to the pre-tamper hash.

## Provenance
Patch produced by the **local model (the Spark) under a Wednesday brief**, re-verified by this seat: the diff
applies **strict** at the base (`git apply --check -p1`, no `--recount`, no fuzz) and its tamper control fires.
Note there are two held READYs for this ticket; this PR is built from the **2026-09-27** one, not the 2026-09-17
file of the same key.

## Test Evidence

**Touched:** `services/auth/src/__tests__/ks839-a-wildcard-allow-list-grants-nothing.test.ts`, in place. Base
`94c9c7aa9be7f0c05f4a89cdc532ec6f2fef3812`. Head commit **+15 / −1**, one file.

**Ran** (this worktree, `npm ci` 1936 packages, `packages/shared` built; `services/auth` runs **vitest**):

| what | result |
|---|---|
| the cell file at my head, untouched product | **8 / 8** |
| RED via the product tamper | **1 failed / 7 passed of 8**, by assertion |
| the same tamper against the base cells | **7 / 7** — the blindness, demonstrated |
| auth suite, `vitest run`, BARE at the base | **835 passed / 835**, 77 files |
| auth suite, `vitest run`, PATCHED at my head | **836 passed / 836**, 77 files — +1, **zero new reds** |
| `tsc --noEmit` over a program **proven to contain the cell** | 719 files with `exclude: []`, the cell counted exactly once, control name 0. rc 2 at **both** trees with an **identical 37-error set** — all pre-existing, none mine |
| `npm run lint` at base / at head | rc 0 both, problem **set identical**, 15 problems at each |
| lint control | a planted `debugger;` in the cell takes lint to rc 1 with `no-debugger` **at that file** |

**NOT run, and why:**
- **No live stack**, so the in-hook preflight's legs 3, 4 and 8 do not run. Only the gate lines this push printed
  are quoted.
- **The product is unchanged.** The tamper exists to show the cell can see a regression, not to propose one.
- **No deploy of any kind.**

**Migrations + config:** none.

## Not covered
- Five carriers, not an exhaustive Unicode whitespace sweep. `U+00A0`, `U+000B`, `U+3000`, `U+2028` and `U+FEFF`
  are covered; the rest of the `White_Space` property is not.
- The cell exercises the scope validator directly. It does not drive a token request end to end.
- The 37 pre-existing `tsc` errors in this service are untouched and identical at both trees.

Refs KS-1220

