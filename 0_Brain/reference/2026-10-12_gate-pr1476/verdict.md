# Gate verdict: PR #1476 (KS-806, synthetic wallet email collision)

**Head:** `acfb8ffd4825c4c28d4e7a8c5e2b8aea90bdf90f`. Develop is still `96342090c8fca190c62bcbeaa517247bf9cd5dbf` (ls-remote 2026-10-12). Merge-base `f5a2402`.
**Predicted merge tree:** `b1c2df4dc1732f6c84435d0c62540cc1aa75a2e2` (clean, my own `merge-tree`), which matches the seat's `b1c2df4dc173`.
**Gate:** independent Opus QA, run read-only. Everything ran in my own clone at `scratchpad/g1476`. The Postgres was my own throwaway cluster on port 55473, which I have since stopped and deleted. I did not touch any shared database.

## VERDICT: GO WITH NOTE (one Major, which should be fixed in this PR or in a follow-up opened at merge)

The fix does what it says between two wallets. Merged, the result is much safer than develop. On develop, every first-time preview-testnet wallet after the first one gets no row and is given a phantom id; this was measured on real Postgres. The new email format, however, opens a new route into the same bug class (Major-1).

## What I ran and what it showed
1. **Diff matches the description exactly:** 3 files, +148/-3. They are `wallet.ts` (helper plus one call site), a comment in `passwordLoginGate.ts`, and the new ks806 test. There is no migration.
2. **ks806 tests:** on base, 5 of 6 are red and the CONTROL passes. On head and on the merged tree, 6 of 6 are green. ks806, ks796 and ks942 together give 22/22 on both head and merged.
3. **Mutations** (7 in total, file restored after each):
   - Killed: old slice, hash of an 8-character prefix, random value per call, raw address in the email, constant email.
   - Survived: `M6` (lowercase the address before hashing), which is benign.
   - Survived: `M4` (hash truncated to 8 hex characters, about 32 bits). See Minor-3.
4. **Full auth suite:**

   | Tree | Files | Tests | Runs |
   |---|---|---|---|
   | head | 85 | 900 | 2 |
   | merged | 88 | 919 | 1 |
   | base | 87 | 913 | run 2 |

   Base run 1 had one 5-second timeout in ks949 (from machine load). Run 2 was clean.
5. **tsc and eslint:** source tsc is rc 0 on all trees, and eslint shows 0 errors (15 warnings, same as base). The tests-included tsc goes from 88 errors on base to 89 on merged. The extra one is ks806:73, `Server` against `node:http`, the same environment noise as the 45 existing `keepAliveTimeoutBuffer` hits on base.
6. **Real-Postgres leg.** All init SQL and 49/49 migrations applied. The app connected as `secuura_app` under RLS, using the real route, real `/register`, real userRepo and the real 039 lookup. Logs are in `logs/probe_*.out`.

   | Cell | Head | Base |
   |---|---|---|
   | P1: a legacy old-email user logs in again | Found by `wallet_address`; same id, hash and updated_at unchanged | Same |
   | P2: a wallet that previously lost a collision | Gets its own row; the holder's row is untouched | No row; holder's updated_at rewritten; phantom id (the control) |
   | P3: first-time wallet | One row, and the returned id is that row | 0 rows (the control) |
   | P4: concurrent first logins, same address | Always one row, but in 4 of 5 rounds one response carries an id that is **not in the DB** | (not given) |

7. **Case canonicalisation and collisions:** 160 bits of SHA-256 makes collisions and second preimages infeasible. However, the address is hashed exactly as the client sent it, with no canonicalisation (Minor-2).
8. **Lockout and PII:** existing users keep their email, so their lockout counters are unchanged. The email is encrypted at rest and looked up via a keyed HMAC, and the local part is a hash of a public address, so there is no PII.
9. **Consumers of `wallet.local`:** across the whole repo, only `wallet.ts`, `passwordLoginGate.ts` (a comment) and three tests reference it. There are no admin, frontend or migration parsers. As a control, the same grep does find `anonymized.local`.

## Defects

**Major-1: the new email can be registered, so anyone can squat a public address's future account.**
- Sites: `routes/auth.ts:134` (`z.string().trim().email()`) and `users.ts:242` (stub), against `wallet.ts:217/229` and `userRepo.ts:692`.
- `w-<hex>@wallet.local` passes zod. The old `addr_tes...@` form returned 400 (cell P5c).
- On real Postgres (cell P5): `/register` with `w-sha256(victimAddr)` returns 201. The victim's first wallet login then returns 200, UPDATEs the squatter's row (updated_at changed) and mints tokens for a phantom id. The wallet gets 0 rows, and this repeats on every login.
- This is exactly the "fabricated object, not in the table" class that KS-806 names.
- Same root (P6): `/register` returns 409 for an existing wallet's email and 201 for an unseen one, so anyone can check whether a public address has an account. This oracle is new; on base both return 201.
- Fix: reserve `@wallet.local` in register, stub and email-change. Make the wallet create path insert-or-fail rather than upsert, i.e. require that the returned row's `wallet_address` matches.

**Minor-2:** `wallet.ts:194` hashes the raw string, while `cip8.ts:160` compares addresses case-insensitively and `isValidCardanoAddress` checks only the prefix and length. One wallet re-cased gives 2 real accounts (P7). That evades suspension on the original account, though it does not take anything over. Fix: lowercase the address before both the hash and the lookup.

**Minor-3:** no test pins the 160-bit width; `M4` (32 bits) survives.

**Minor-4 (existing before this PR, still present):** concurrent first logins for one address mint a token for an id not in the DB (P4), because `createUser` returns its input object rather than the stored row.
