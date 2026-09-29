**No decision card for this one.** The ticket offers two directions — validate against the declared bounds, or widen the ruling. **This takes the first: validate**, per KS 662 and the schema's own `nonnegative()`. It does **not** widen the ruling, and that choice is stated here as a claim with its reason rather than as something ratified.

`POST /api/status/{id}/unrevoke` accepted `index: -1`, below the declared minimum. It now refuses.

2 files, +21/−2 — the product guard and a new cell file. No existing cell is re-pinned.

## Test Evidence

Re-measured on this rebased head against develop `2cb858335472`, not carried from the pre-merge base:

| | baseline at develop | this branch |
|---|---|---|
| `services/vc-issuer` | 16 files / 146 tests, 0 failed | **16 files / 150 tests, 0 failed** |
| `tsc` vc-issuer | 0 errors | 0 errors — **delta 0** |

**Red-first, test half applied ALONE with the product file asserted unchanged against develop** (measured: 0 differing product files): `services/vc-issuer` **rc 1 — 1 file failed, 2 tests failed**, 15 files / 148 tests passing.

The previous seat reported "2 failed / 9 (U1, U2)" counting the new file's own nine cells; **2 over the whole suite is the same measurement on a different denominator.**

**Arms, carried as the previous seat's measurement at `8af6ab82` and named as such** — the diff is proved byte-identical across the rebase (`cmp` rc 0), so they still hold:
- **A1** remove the `< 0` check → 2 failed / 9.
- 🔴 **A2** revert **only the message string** → **still 9/9 green.**

## 🔴 Not covered, and A2 is why it is stated here rather than discovered later

**The new refusal message is UNPINNED.** Arm A2 reverts the message text alone and the suite stays fully green, so nothing in these cells asserts what the refusal *says* — only that it refuses. A future edit could change the message to anything, including something unhelpful or misleading, and no cell here would notice.

That is a deliberate disclosure, not an oversight found afterwards: the arm was run specifically to find out, and it found this. Pinning the string would be a small follow-up; it is not in this PR because the ticket's direction is the bounds check, and widening scope on an unruled ticket is what the "does not widen the ruling" line above is refusing to do.

## Also not covered

- No built images and no local stack, so **a §5f live sweep is owed**. Nothing is deployed by this PR.
- The route's other bounds cases beyond the declared minimum are unchanged and unasserted here.

**Rebase evidence:** cut at `8af6ab82`, rebased onto `2cb858335472` after #1339 merged. `cmp` of the stored pre-rebase diff against the post-rebase diff is **rc 0, byte-identical**; patch-id equal as corroboration only. No conflict — #1339 and this branch share **zero** files.

**Push preflight: 12 of 15 legs ran, 3 skipped (legs 3, 4, 8 — local stack not up), nothing failed.** 12/15 is not a pass and is not quoted as one.

Related, cross-referenced and deliberately un-hyphenated so they are not attached to this PR: KS 662 (the declared-bounds ruling this follows) and KS 1269 (the sibling non-integer index case).

Refs KS-1371
