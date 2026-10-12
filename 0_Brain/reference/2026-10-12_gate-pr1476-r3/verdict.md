# Round-3 delta gate: PR #1476 (KS-806)

**Head:** `5edcffd12503920c67f66c93df1d12daef9a4cd2`, the child of `5350664`. Base is `f5a2402`.
**Develop used for the merge prediction:**
- Live develop is `9a958d5b1f4bd312762c190ce1cd4b9f90d4303b` (ls-remote, fetched into my clone only). The predicted merge is tree `ad9d12a1`; it merges with no conflict.
- I also checked worktree develop `1b7b8d7d`. It gives the same result.

**Gate:** independent Opus QA, read-only.
- Everything ran in my own clone, `scratchpad/r3` plus worktrees `scratchpad/g3/{H,P,M,M2,D,MP}`.
- Postgres was my own cluster on port 56243. It is now stopped and deleted.
- I wrote no shared ref, database, PR or board.

## VERDICT: NO GO as it stands. The fix is mechanical: rebase and update one test cell.

The three fixes are correct, and I could not refute them. However, the predicted merge turns develop's auth suite red (Major-1).

## Evidence
1. **The delta is exactly as claimed.** 7 files, +158/-10:
   - `wallet.ts`: the candidate order
   - `users.ts:600`: the admin/create guard
   - `auth.ts:1088`: the social guard
   - the `walletEmail.ts` comment
   - 3 test files
2. **The 9 new RED cells.** On `5350664`: 9 failed and the 63 others passed. On head: 72/72. On the merged tree: 72/72.
3. **Full auth suite:**

   | Tree | Run 1 | Run 2 |
   |---|---|---|
   | head | 86 files / 938 tests, all green | same |
   | merged | 976/977 (Major-1) | not run |

4. **tsc, eslint, check:test-types.** All three pass on both head and merged:
   - tsc: rc 0.
   - eslint: 0 errors (15 warnings).
   - check:test-types on the merged tree: 42/42 errors, all already in the baseline, 0 new.
   - Planted controls show each check does catch an error: check:test-types rc 1, tsc rc 2, eslint 1 error.
5. **Mutants: 9 of 11 killed.**
   - W4 (drop the Set dedupe) survived. It is equivalent.
   - C2 survived (Minor-1).
6. **Fuzz.** I tried 11.1M single-code-point substitutions or insertions: 83 normalise to the synthetic email, and 0 of those bypass the guard. Controls are OK.
   - `lookupHash` does no normalisation beyond `lower().trim()`.
7. **Real Postgres** (`logs/probe_*.out`; control = the same probe on `5350664`):

   | Cell | Head | Control (`5350664`) |
   |---|---|---|
   | E1 exact casing after a lowercase login | Returns the legacy account; creates 0 rows | Returns a different account |
   | E4 admin/create: 5 admin roles (incl. ORG_ADMIN in another tenant) × 4 variants (exact, upper, padded, `\n`) | All 400; 0 squat rows; the wallet then logs in with its id present in the DB | 201/409; login 500 or a phantom id |
   | E4 oracle (existing vs unseen wallet) | 400/400 | 409/201 |
   | Controls: ordinary email / look-alike domain / non-admin | 201 / 201 / 403 | |

   **On (B):** the presented casing is checked by the signature before the lookup. The challenge must equal the body, and `cip8.ts:160` compares the signer's bech32 address case-insensitively. So the presented casing can only ever be a casing of the wallet's own address. Bech32 also has no two distinct addresses that differ only by case.

## Defects
- **Major-1: the merge breaks the auth suite.**
  - What fails: `ks963-preauth-rethrow.test.ts:293`, from KS-1131 `b4a245f`, which reached develop on 2026-10-12. Its allow-set expects `['query']` but receives `['canonicalWalletAddress','Set','query']`.
  - Cause: `wallet.ts:188` and `:198` add calls before the first `query`.
  - Develop alone: 22/22. Merging the round-2 head gives the same red.
  - Fix: rebase, then extend the cell's allow-set to the pure helpers.
- **Minor-1:** no cell pins the guard at `auth.ts:1088` before the LINK branch. The mutant that moves it into `if (!user)` (the create block, `:1160`) survives.
  - Gap: the C cells set `emailAccountExists=false`.
- **Residual (already present in round 2, not new):** E2. A SUSPENDED legacy row stored in mixed case is refused for its own casing (401), but a lowercase login mints a fresh ACTIVE account (200). That is suspension evasion through the declared double-account path. A canonical-case suspended row is refused in every casing (E3).
- **Noise:** admin/create with an array as the email returns 500 with 0 rows. It does the same on the control.

## Not done
- Real-Postgres social callback. That path is covered by the unit cells and the mutants only.

**Other create paths:**
- No email-change route exists: the admin PATCH allow-list and the profile update both omit email.
- Password reset updates the hash only.
- Gateway and originate inserts are fixed seed lists.
- No Extranet callers were found.
