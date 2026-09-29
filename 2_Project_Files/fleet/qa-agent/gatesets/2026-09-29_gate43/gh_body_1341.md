**Kam's ruling, option (b), verbatim** (card `secuura-ks1352-unknown-id-policy-after-gate38`, `ruled_ts` 2026-09-29T08:06:25.830535+10:00):

> **[b] Fail closed on no record (Recommended)** — No issuer record: verified false with the reason 'no issuer record'. Closes the id-edit trick. Cost, measured by the seat: a stack with no database refuses every credential, and a genuine credential whose database write was lost stops verifying.

## What changes

The refusal sits in the verifier's stored arm in `packages/shared/src/vc/verifier.ts`, **inside the existing `if (this.config.storedRecordResolver)` guard**, so a consumer that never wired that arm is untouched. Stated as a claim with its reason, not as ratified: placing it inside the guard is what keeps unwired consumers unaffected, and arm A3 below is what makes that guard demonstrably load-bearing rather than decorative.

3 files, +213/−9: the product file, a new cell file, and **exactly one re-pin** of an existing cell.

## The re-pin is one cell, and it is the cell the ticket names

KS 1368's own text says: *"Cell `C2` … asserts that an id with no stored record still verifies true, so option 1 cannot be changed by accident — whichever option is chosen, that cell is the one to edit."* That is `services/vc-issuer/src/__tests__/ks1352-revoked-credential-fails-verify.test.ts:166`, and **its title moved with its assertion** — a cell that flips its assertion and keeps its old title is a cell that lies about itself. F0, R1, R2, R3 and C1 are byte-unchanged.

## Test Evidence

Re-measured on this rebased head against develop `2cb858335472` (not carried from the pre-merge base):

| | baseline at develop | this branch |
|---|---|---|
| `services/vc-issuer` | 16 files / 146 tests, 0 failed | **17 files / 155 tests, 0 failed** |
| `packages/shared` | 48 files / 945 tests, 0 failed | **48 files / 945 tests, 0 failed** |
| `tsc` vc-issuer | 0 errors | 0 errors — **delta 0** |
| `tsc` packages/shared | 0 errors | 0 errors — **delta 0** |

**Red-first, with the test half applied ALONE and the product file asserted unchanged against develop:** `services/vc-issuer` **rc 1 — 2 files failed, 5 tests failed** (15 files / 150 tests passing). The 5 are the 4 new `RED KS-1375` cells plus the re-pinned `C2`. The earlier seat reported this as "4 failed / 9" counting only the new file's own cells; **5 is the same measurement over the whole suite** — 4 in the new file plus C2 in the re-pinned one.

⚠ **`packages/shared` is consumed as BUILT DIST, and this matters to anyone re-running the above.** `npm run build -w @secuura/shared` must follow every checkout or edit, or a change to `packages/shared/src` is invisible to vc-issuer. Measured the hard way on this branch: without the rebuild, the test-half-alone arm and the whole-branch arm returned **identical** counts (2 files / 5 tests failed both times), because both were loading develop's verifier. Identical arms are impossible for a working red-then-green pair, and that impossibility is what exposed it.

**Arms, carried as the previous seat's measurement at `8af6ab82` and named as such** (the diff is proved byte-identical across the rebase, `cmp` rc 0, so they still hold):
- **A1** refusal removed → all four RED cells fail.
- **A2** reason reworded → the same four fail, so the card's exact wording is **pinned, not decorative**.
- **A3** refusal moved OUTSIDE the `storedRecordResolver` guard → **C4 alone** reds, which is what proves that guard load-bearing.

**Rebase evidence:** cut at `8af6ab82`, rebased onto `2cb858335472` after #1339 merged. `cmp` of the stored pre-rebase diff against the post-rebase diff is **rc 0, byte-identical**; patch-id equal as corroboration only (patch-id normalises whitespace and cannot see a whitespace-only change — measured four ways, so `cmp` is the load-bearing half). No conflict: #1339 and this branch share **zero** files.

## The measured cost is narrower than the card's wording

The card says a DB-less stack "refuses every credential". Measured: the vc-issuer suite already runs DB-less and **a credential issued in the same process still verifies from the memory store, on both routes**. So the real cost is *a DB-less stack refuses every credential it did not itself issue*. Exactly one existing cell assumed otherwise, and that cell is C2.

## Not covered

- `determineStatus` (`verifier.ts:562`) maps `!checks.status → 'revoked'` unconditionally, so a no-record refusal still reports `docStatus: 'revoked'` — the exact mislabel KS 1368's option 2 chose its wording to avoid. The reason string carries the distinction; `docStatus` cannot without widening the published status enum.
- DID-resolver wiring on both verify routes.
- The in-process status list forgetting a revoke on restart.
- The production path: every Ed25519 credential already fails with `No DID resolver configured`, read by an earlier gate and not driven here.

**RUNTIME change: a §5f live sweep is owed.** Nothing is deployed by this PR.

Refs KS-1375
Refs KS-1368
