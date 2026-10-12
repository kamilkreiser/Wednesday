# Delta gate: PR #1476 round 2 (KS-806)

**Head:** `5350664167a090e48e3d47de6e013e5ab6e33684`, the child of `acfb8ff`. The delta is 7 files, +280/-34.
**Gate:** independent Opus QA, read-only. Everything ran in my own clone (`scratchpad/d1476`, made with `--no-hardlinks` from worktree `s-v3-l05d`). Postgres was my own throwaway cluster on port 55474, which I have stopped and deleted. I did not touch any shared database, ref, PR or board.

## VERDICT: GO WITH NOTE

Major-1 is closed on both public register paths. Minor-2 and Minor-3 are closed. Three new Minors remain. The cheapest one, Minor-A (one line), should be fixed in this PR if possible; otherwise it should be filed at merge.

## Evidence

1. **Tests.** The ks806 files plus `auth.integration`: 77/77 green.
   - Full auth suite, run 1: 920/922. Run 2: 921/922.
   - The only failures were 5-second timeouts in `ks949` (it walks the repo tree, and machine load was about 22). Run alone, ks949 passes 30/30. The previous gate saw the same flake on base.
   - Source tsc: rc 0. eslint: 0 errors.
2. **Mutations.** 9 of 9 were killed:
   - each of the 2 refines removed
   - hash slice cut to 8 characters
   - no lowercasing
   - legacy fallback dropped
   - substring domain check
   - case-sensitive domain check
   - raw casing stored
   - hash of the raw (not lowercased) address
3. **Fuzz** (30 variants against the head schema): **0 bypasses.**
   - Variants tried: uppercase, padding with spaces, tab or newline, trailing dot, `+tag`, `x <a@wallet.local>`, `<…>`, U+2024 / U+FF0E / fullwidth / ı / ⅼ homoglyphs, zero-width space, BOM, NBSP, NUL, `[wallet.local]`, quoted local part, `%` routing, double `@`, NFKC.
   - zod `.email()` rejects every non-ASCII form.
   - The refine checks the domain after the last `@`, lowercased, which is the same normalisation `createUser` uses (`lower().trim()`).
   - `xn--wallet-.local` passes, but it cannot collide with a wallet email.
4. **Address formats.** `/challenge` accepts only `addr1`, `addr_test1` and `stake*` prefixes, so every address is bech32. `cip8.ts:160` compares against CSL's lowercase bech32. Lowercasing before the hash therefore matches it exactly. Hex, base58 and Byron addresses cannot reach this code.
5. **Real Postgres** (`logs/probe_head.out`).

   | Cell | Case | Result |
   |---|---|---|
   | D1 | Returning legacy user | Found; row unchanged |
   | D2 | Wallet that previously lost a collision | Gets its own row; the holder's row is untouched |
   | D3 | First-time wallet | One row; canonical address stored; returned id is that row |
   | D4 | Both casing orders | Each is one account, with the same email |
   | D6 | `/register`, `/register` in uppercase, `/users/stub` with the future email | 400, 400, 400; 0 rows. The wallet then logs in normally |
   | D7 | The 409/201 oracle | Closed: 400/400 |

## Defects

- **Minor-A: `admin/create` is an exploitable squat vector, but only for admin roles.**
  - Site: `users.ts:582`, with `:629` and `:659`.
  - It takes any email, with no validation, from `SYSTEM_ADMIN`, `SUPER_ADMIN` or `ORG_ADMIN`. `ORG_ADMIN` is a role an admin *inside a customer tenant* holds.
  - **Measured on real Postgres (cell D8):**
    - An ORG_ADMIN in another tenant gets 201. The victim wallet then gets a 500 on every login, from the RLS USING violation on ON CONFLICT, so that wallet is permanently denied.
    - An ORG_ADMIN in the default tenant, or a SYSTEM_ADMIN, causes the phantom id and rewrites the squatter's row: the original KS-806 class.
    - It also gives a cross-tenant oracle: 409 if the wallet has an account, 201 if not.
  - This is not a regression, because on develop the old shared email was squattable the same way.
  - Fix: add `isReservedWalletEmail` here.
  - The comment at `walletEmail.ts:12`, "reserved on every path", is currently false.
- **Minor-B: legacy rows stored in a non-canonical casing get shadowed.**
  - Site: `wallet.ts:196`, which looks up the canonical address first.
  - Cell D5: after one login in the canonical casing creates a new account, the legacy row is unreachable *even through its own casing*. In the cell, the first login with the exact casing found the legacy row; after the canonical login, the same exact-casing login returned the new account instead.
  - The seat's claim "still found by that casing" holds only until that happens.
  - Fix: try the raw casing first. This is not a hijack, because a signature is required.
- **Minor-C: social sign-up is an unguarded create path.**
  - Site: `auth.ts:1158/1181`.
  - Any provider email reaches `createUser`. It is impractical to exploit today, because MSA (consumers), GitHub and Facebook each require a deliverable, verified address.
  - It needs the same guard for defence in depth.
- **Already declared by the seat, and confirmed:**
  - `/link` stores the raw casing (`wallet.ts:499`), so one wallet becomes 2 accounts (cell D9).
  - `/status` is not canonicalised.
  - The OpenAPI text does not mention the reservation.
  - The KS-1486 race (not re-run).

## Not checked
- Whether any deployed environment gives ORG_ADMIN to customers in practice.
- Other services' user inserts: these are seed-only fixed lists in the gateway and originate.
