#1287 KS-1318 + KS-1142: re-raise the proven entrypoint-corpus file on its own
head 4dac00147f8861250bab6abbea2fec34b14b62f2

## BLUF
#1268 carried three tickets and failed at the two-NO-GO cap on **ks1316's** guard-reachability rule,
so it ships nothing and stays open. **KS-1318's and KS-1142's work is in a different file**, was
proven in **both** rounds, and is not implicated in what failed. This raises that one file alone so it
is not lost with the vehicle.

**Nothing of ks781 is in this change, and no part of the rule that failed.**

## The file is not re-typed — it is the same blob, and you can check that
It is written from the object store at the exact blob both #1268 rounds carried:

```
$ git rev-parse HEAD:Blockchain/Dev/packages/shared/src/__tests__/entrypoint-corpus.test.ts
8a4ce36a3a96d2e511faf9b19eba14593d8e99fa
```

That is the blob the tier-2 report records at line 488. Content-addressed, so it is not a copy of
what some worktree happened to hold — it is the object itself. One file, one path.

## What the file does, unchanged from its proven form
- **KS-1318** — the combined default-shapes control asserts the three tags with `toEqual` **in source
  order**, rather than asserting their **count**. A swapped or renamed tag now reds instead of passing
  on arithmetic.
- **KS-1142** — K1's literal is hoisted and K1b reads `CORPUS` from the source text, with the subset
  reason stated in the cell. The corpus is pinned by **one** declaration instead of two
  hand-maintained literals in two files that could drift apart silently.

## Test Evidence
Verified on **develop as it stands** (`e6056de7ed640e3a441bc7e33853601bf9040084`), not on #1268's
older base — the point of this PR is that the file is independently good *here*.

| suite | result |
|---|---|
| `entrypoint-corpus.test.ts` alone | **30 / 30** |
| `packages/shared` **BARE** (develop as it stands) | **48 files / 944 tests / 0 failed** |
| `packages/shared` **PATCHED** | **48 files / 945 tests / 0 failed** |
| `tsc --noEmit` | **rc 0, zero `error TS`** |

Delta **+1 cell**. The whole package is green **with no ks781 change present**, which is the
load-bearing fact: this file does not depend on the rule that failed.

Control against the other failure mode: the change is **not** a no-op — it differs from develop by
**+73 / −29** on that path.

**Push gate:** `28/0 · 6/0 · 49/0 · 60 passed, 0 failed, 0 skipped (of 60)`. Preflight **12/15 legs
ran, 3 SKIPPED (3, 4, 8 — local stack not up), nothing failed** — not quoted as a pass. This worktree
contains develop's current tip, so the quadruple is a reading at `e6056de7ed64`.

## NOT covered
- **ks1316's guard-reachability rule is not here**, in any form. Its residue (parenthesised return
  forms reading `guarded: false`) is being tracked separately.
- #1268 is **not** closed by this PR, and should not be — that disposition is Kam's.
- No product code. No migration, no config, no lockfile.

Refs KS-1318
Refs KS-1142

