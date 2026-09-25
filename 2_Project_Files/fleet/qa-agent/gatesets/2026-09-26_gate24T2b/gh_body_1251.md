#1251 KS-1147 ESCAPEDHOST: a loopback host escaped inside a string fixture is the accepted spelling
head 8020adae99129f4b7194fef32f1ea5b762819d90

## What this changes

R-5 from the #980 delta gate. A test file that carries a listen call as a **string fixture** inside a
`"`-delimited literal can only spell a double-quoted host as `\"127.0.0.1\"`. Written to disk that body is
exactly this guard's own accepted spelling — but the file's **bytes** carry the backslashes,
`maskCommentsWithState` preserves string contents by design and copies them through, and the host check
wanted a bare `'` or `"` as the first non-space character after the comma. A `\` is neither, so a
correctly-bound listener was reported **host-less**: a false RED, in the direction that costs a reader time
on a listener that is already right.

The host check now tolerates an optional escape on each side of the address.

Independent of the `ks781` stack (#1248 / #1249) — same package, different file, branched from `develop`.

## Two things I measured that changed what shipped

**1. The fixture has to be the whole enclosing literal.** My first draft asserted on a bare
`app.listen(0, \"127.0.0.1\")` snippet. That has no opening quote, so the mask enters `dq` at the first
`\"` and reaches EOF still inside it — the scanner announced a **desynchronised mask** and the cell failed
for a reason that has nothing to do with the host check. This file already records the same trap for
docblock body lines: *a fragment that never occurs without its delimiters is not a fixture.* The cells now
feed `const fixture = "const s = app.listen(0, \"127.0.0.1\");";`, which is the shape the gate described.

**2. My extra strictness was not load-bearing, so it does not ship.** An earlier draft required the
closing escape to *repeat* the opener's, so a mismatched pair (`\"127.0.0.1"`) stayed a violation.
**Relaxing that back to independent escapes reddened nothing — 25/25.** No representative fixture
distinguishes the two, because a mismatched pair does not occur in a well-formed source file. Untested
strictness in a guard is what several of this file's own findings are about, so the simpler regex — the
gate's own proposal — is what ships, with the measurement written beside it.

## Test Evidence

**Touched:** `Blockchain/Dev/packages/shared/src/__tests__/ks860-test-listeners-bind-loopback.test.ts`.
One file, one commit. No `package.json`, no lockfile.

**Ran** (all by the author, on this head; node v24.7.0, vitest 4.1.11):

- `npm test` in `packages/shared` — **47 files / 930 passed / 0 failed**, rc 0, **0 timeouts**, at load 4.78.
- **BASE measured, not inferred**: develop's blob for this file put in place, the suite re-run, then restored
  and the restore verified by sha256 → **47 files / 928 passed / 0 failed**. So **928 → 930**, exactly the
  two new cells.
- `npm run build` (tsc) — rc 0.
- `npm run lint` — rc 1, finding set **identical to develop's** (`diff` empty; control run). The one error is
  the pre-existing `no-control-regex` at `:539`, red on `develop` too and already on the backlog.
- **Red-proof before the fix:** the escaped-host cell was **red**; the control cell (a wrong or missing host
  must stay a violation) was **green**. So the new cells discriminate the fix rather than the file.
- **Tamper matrix, 3 arms, all red** (`tamper1147.sh`; restores sha256-asserted, never `git checkout`):

| arm | what it flips | reds |
|---|---|---|
| C1 | revert the widening — the defect itself | the escaped-host cell — **only that one** |
| C2 | stop checking the address (any `[0-9a-f.:]+`) | the wrong-host control — **only that one** |
| C4 | make the host check never match | 6 cells, including the tree census and the pre-existing accepted-spelling control |

(C3 was the fourth arm and is gone from the matrix because it became the shipped form — see point 2 above.)

**The tree census still passes.** The guard walks every test file under `services/` and `packages/`, and the
🔴 census cell is green at this head, so the widening has not made a real offender invisible: C2 is the arm
that would catch that, and it reds.

**NOT run / NOT covered:**

- **Nothing on develop trips this today** — the merged tree is green either way. This is the guard's
  boundary, recorded by the gate as R-5, not a live defect.
- The sibling boundary the same gate noted (Tg-D: `listen(3000)` with no host passes `\s*0\s*`) is the
  regex's **declared** narrowness — port 0 only — and is not touched here.
- This guard reads the whole `services/` + `packages/` tree by **text**, so a later merge from another lane
  can move its verdict.
- No environment, no docker, no database, no migration, no config. **Nothing deployed.**

## Which gate ran, and it is not a clean pass

`Blockchain/Dev/` path, so the hook ran. Verbatim:

```
PREFLIGHT INCOMPLETE — 12/15 legs ran, 3 SKIPPED. Nothing failed.
  legs 3 4 8 — local stack not up; you can clear this by starting it.
  This is NOT a pass. Do not quote it as one — say which legs ran.
```

Fleet STOP count, read anchored to each suite's section header, with a control returning NOT FOUND for a
header that does not exist: `pre_push_hook_base` **28/0**, fixture guard **6/0**, shell suites **60 passed,
0 failed, 0 skipped (of 60)**. No line starting `FIXTURE BUILD FAILED`.

**Migrations + config:** none.

Refs KS-1147

