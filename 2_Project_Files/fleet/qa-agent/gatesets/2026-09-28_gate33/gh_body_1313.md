#1313 KS-1121: resolve a credential by exact id only; drop the substring fallback
head 380e1e022ccfc6685346947bd9ff8eb08a0a07b7

## BLUF
`services/vc-issuer/src/repositories/credentialRepo.ts`'s `getById` resolved a credential by **substring**. After
the exact lookup missed it ran a second query — `SELECT credential FROM vc_credentials_store WHERE id LIKE $1
LIMIT 1` with `` `%${id}%` `` — and the in-memory path scanned every entry for `key.includes(id) ||
value.id.includes(id)`. **A caller holding a fragment of someone else's credential id got that credential back.**

**The repository owner ruled on 2026-09-16: _"delete the substring branch exactly as #966 did for presentations"_.**

Both branches are deleted.

## Two behaviour changes, both intended, both stated plainly
1. **`GET /api/credentials/:id` answers 404 for any id that is not an exact stored id.** A fragment resolves
   nothing.
2. **A revoke addressed by a fragment of an id revokes nothing.** `revoke()` resolves through `getById`, so it
   inherits the rule. That is the ruling's direct consequence, not a separate decision — and it is pinned by its
   own cell rather than left implied.

## What changes
- `services/vc-issuer/src/repositories/credentialRepo.ts` (+2 / −14): the `LIKE` query and the `includes()` scan
  are removed; the JSDoc is reworded to say exact-id-only.
- `services/vc-issuer/src/__tests__/credentialRepo.test.ts` (+29 / −5): the cell that *pinned* partial-match
  lookup is replaced by three cells — exact-id-only across seven fragment shapes (including the SQL wildcards `%`
  and `_`), revoke-by-fragment mutating nothing, and a DB-path cell asserting an unknown id costs **exactly one**
  lookup query and that it is **never** a `LIKE`.

## Provenance
Patch produced by the **local model (the Spark) under a Wednesday brief**, re-verified here. The canonical source
is the checker's `patch.diff`; measured against the READY block it is **byte-identical** (`cmp` rc 0, both 3277 B,
sha256 `7762a4be3080c4a7`), and the raise tool reported the difference as *"(none — they are identical)"*. All four
hunks apply **strict** at the base, and both tamper controls fire.

## Test Evidence

**Touched:** `repositories/credentialRepo.ts`, `__tests__/credentialRepo.test.ts`, both in place. Base
`94c9c7aa9be7f0c05f4a89cdc532ec6f2fef3812`. Head commit **+31 / −19** over exactly those two paths.

**Ran** (this worktree, `npm ci` 1936 packages, `packages/shared` built; vc-issuer runs **vitest**):

| what | result |
|---|---|
| RED — the new cells with the product at the base | **3 failed / 8 passed / 11.** All three reds are `AssertionError` (`expected { …(8) } to be undefined`, and the fragment-labelled one) — assertions, not load failures |
| GREEN — both files | **11 / 11** |
| vc-issuer suite, `vitest run`, BARE at the base | **134 passed / 134**, 14 files |
| vc-issuer suite, `vitest run`, PATCHED at my head | **136 passed / 136**, 14 files — +2, **zero new reds** |
| `tsc --noEmit` over a program **proven to contain the test file** | 541 files with `exclude: []`, the cell counted exactly once, control name 0. **rc 2 at BOTH trees** — see the disclosure below |
| `npm run lint` at base / at head | rc 0 both. Base **0 problems**; head **1 warning** — see the disclosure below |

## Disclosed: two pre-existing conditions this change touches, neither fixed here
Both were raised before pushing and the coordinator ruled the PR ships as-is with them stated.

**1. A fourth read of a pre-existing type gap.** `tsc` error sets, measured at both trees over the same program:

| tree | TS2339 set (`credentialRepo.test.ts`) |
|---|---|
| base | `118:39` revoked · `119:39` revocationReason · `120:39` revokedAt — **3** |
| head | **`72:63` revoked (NEW)** · `142:39` revoked · `143:39` revocationReason · `144:39` revokedAt — **4** |

118–120 and 142–144 are the same three lines shifted +24 by the hunk (verified by reading both files). `72:63` is
inside the new revoke cell. The type genuinely lacks the fields: `packages/shared/src/vc/types.ts`'s
`VCCredentialStatus` declares `id`, `type`, `statusPurpose?`, `statusListIndex?`, `statusListCredential?` and no
`revoked`, `revocationReason` or `revokedAt`. **Observation, not a conclusion:** line 32 writes `revoked: false`
inside a `credentialStatus` object literal at both trees and does **not** error, so the gap is reachable on a read
and not on that construction. Not chased further.

**2. A new `prefer-const` warning, created by the ruled deletion.** At the base, `let result` is assigned twice —
the exact query, then the `LIKE` fallback. Deleting the fallback leaves it assigned once, so
`credentialRepo.ts:95:11 warning 'result' is never reassigned. Use 'const' instead` now fires. Lint exits 0 at both
trees; the count goes 0 → 1.

Both are carried to a follow-up ticket rather than fixed inside a security PR.

**NOT run, and why:**
- **No live stack**, so the in-hook preflight's legs 3, 4 and 8 do not run. Only the gate lines this push printed
  are quoted.
- **No deploy of any kind.**

**Migrations + config:** none. No migration, no `package.json`, no `package-lock.json`, no dependency, no new import.

## Not covered
- Both disclosures above.
- **Callers that relied on fragment lookup would now 404.** No consumer sweep was run; the ruling is explicit that
  the substring path goes, and `#966` set the precedent for presentations.
- The DB-path cell asserts the *shape* of the remaining query (one lookup, no `LIKE`). It does not exercise a real
  database.

Refs KS-1121

