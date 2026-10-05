> **Preflight, quoted verbatim from the in-hook log** (`s-e3-ks938-79c87b8aaa48-push.out`):
> `PREFLIGHT INCOMPLETE — 12/15 legs ran, 3 SKIPPED. Nothing failed.`
> `legs 3 4 8 — local stack not up; you can clear this by starting it.`
> `This is NOT a pass. Do not quote it as one — say which legs ran.`
> Push rc 0, lock held 560 s (07:37:42Z → 07:47:02Z), released; 0 locks on disk after.
>
> 🔴 **This PR must NOT be merged before #1382** — see *Merge ordering* below.

Refs KS-938

https://linear.app/secuura/issue/KS-938

## What this fixes

"MFA disabled" left the TOTP seed and the hashed backup codes in the row. The flag flipped, the call
answered **200 "MFA disabled successfully"**, and the credential material survived — so the seed could
be re-armed by `POST /api/users/me/mfa/verify`, which re-arms on the existing `user.mfaSecret` without
minting a new one. The case that matters is the user who disabled MFA **because** the authenticator was
compromised.

## Mechanism, and the one thing deliberately NOT changed

`userRepo.updateUser` builds its SET list with
`if (tsField in updates && updates[tsField] !== undefined)`. `mfa_secret` and `mfa_backup_codes` **are**
in `fieldMap`, so the map was never the problem — the **value** guard was. All three clearing sites
passed `undefined`, so a **partial** UPDATE landed naming only the fields that survived.

**`updateUser`'s `undefined` skip is NOT changed.** Every other caller relies on it to mean "leave this
column alone". `null` passes the guard and writes SQL NULL, and the encryption branch guards on
`typeof val === 'string'`, so a `null` can never enter it. The codebase already knew the rule —
`wallet.ts` carries "null, NOT undefined" for `walletAddress` (KS 720).

## Three sites, and why the fix is per-site rather than one shared edit

Addressed by **symbol with blobs**, because the line numbers move: at this PR's base
`routes/mfa.ts` is blob `87d3ee1079fe` and `routes/users.ts` is blob `ea9f8da97a04`.

| site | call | before |
| -- | -- | -- |
| `mfa.ts` setup-verify **revert** | `updateUser` | `mfaSecret: undefined, mfaBackupCodes: undefined` |
| `mfa.ts` `POST /mfa/disable` | `updateUserOrThrow` | `mfaSecret: undefined, mfaBackupCodes: undefined` |
| `users.ts` `POST /me/mfa/disable` | `updateUserOrThrow` | `mfaSecret: undefined`, **`mfaBackupCodes` absent entirely** |

That third row is why no single shared edit could have fixed this: the key was never in the object, so
no change to `updateUser` and no change to a value could have added it. It needed the **key added**.

## Test Evidence

Run by me (Seat E 3rd) at this PR's head `79c87b8aaa48d283a03143e5f50fa8b05b3b77c3`, node v24.7.0.

**Touched:** `services/auth/src/routes/mfa.ts`; `services/auth/src/routes/users.ts`; new
`src/__tests__/ks938-mfa-disable-nulls-seed-and-backup-codes.test.ts`; both platform-k docs (block `20.`).

**Ran:**
- **Red-first, by assertion, one arm per site:** base **3 failed | 2 passed (5)** → head **5 passed (5)**.
  Both numbers non-zero, so it is a real red and not a load failure. The three **site** cells fail at
  base and **both controls still pass** — which is what makes the three mean something. The base failure
  quotes the defect verbatim:
  `UPDATE users SET mfa_enabled = $1, verification_level = $2, updated_at = NOW() WHERE id = $3`.
- Full `services/auth` suite at the head: **79 files, 845 tests, 845 passed, 0 failed**, rc 0.
  That figure reconciles rather than floating: develop's own auth suite is 78 files / 840 tests, this PR
  adds 1 file / 5 cells, and the sibling KS 1210 branch reads 864 = 840 + its own 24.
- `tsc --noEmit`: rc 0, **0 errors**. Positive control, planted type error: **rc 2, 2 errors**; source
  restored byte-identical.
- `npm run check:openapi`: rc 0, 405 example blocks.

**How the cells are built, because it changes what they prove.** They drive the **real route handlers
over real loopback HTTP** with the real `userRepo` and the real `updateUser`, stubbing **only** `../db`
so the emitted statement can be captured, and they assert the **SQL** — not the source text, which would
still pass if the fix were commented out. The setup-verify revert is reached by making the stub throw on
`DELETE FROM mfa_pending_setups`, so all three sites are **driven**, not source-checked.

Two controls, both load-bearing:
- the same real `updateUser` driven with `undefined` must **still** omit the two columns — a cell that
  cannot tell the fix from its own fallback is not a regression test;
- an unrelated `verificationLevel`-only update must gain **no** mfa columns, so the change is scoped to
  the three call sites and not to `updateUser`.

**NOT run:** the four platform suites (Schemathesis, Akto, Playwright, k6); any live-stack verification.

**Migrations + config:** none. No migration, no lockfile, no manifest, no spec, no baseline, no
dependency change.

## Timing statement (skill section 4)

No stated timing covers `services/auth` in either platform-k doc or the test-discipline skill. Measured
at this PR's base `46c3e20cfbd2` over blobs `fc8b521e4a9e` (flow), `82dc1387af38` (cheat) and
`eaf43dfd4d98` (skill): **7** mentions of `services/auth`, **0** with a duration within 120 characters.
Regex printed so it can be re-run:
`\b\d+(?:\.\d+)?\s*(ms|s|sec|secs|seconds|m|min|mins|minutes|h|hr|hours)\b`. MUST-HIT control, same
instrument and same three files, subject `Akto`: **134** mentions, **11** with a duration — so the 0 is a
measurement, not a blind spot. No tier budget moves.

## Merge ordering — this must NOT land before #1382

#1382 (KS 1005) also changes `routes/users.ts`, and merging this first would force a re-gate of it. So
this PR waits for #1382.

Measured in a contained scratch clone rather than assumed:
- vs develop → rc 0, tree == this PR's own tree (control: a no-op merge reproduces the tree)
- vs #1382 head `80bafc849a54` → rc 1, log says `Auto-merging …/routes/users.ts` with **no conflict on
  it**; the only conflicts are the two `Projects Documents` html. Predicted tree `8b07e06645c2`
- vs #1384 head `852fc927632095fb` → rc 1, docs only. Predicted tree `17ee06f1a29e`
- vs #1381 head `82e6bfa9de85` → rc 1, docs only. Predicted tree `66eab5a99fa9`

**Same-line control, because "auto-merged" is worthless if the instrument cannot see a `users.ts`
conflict:** a synthetic commit editing develop line `966` — the line #1382 itself changes — returns
`CONFLICT (content): Merge conflict in …/routes/users.ts`. So the instrument does flag that file when a
conflict exists, and the clean reading above is a measurement.

#1382 inserts 8 lines at `:966`, so this PR's `users.ts` disable site **moves from `:1116` to `:1123`**
once it lands. The doc block cites blobs, not only line numbers, for exactly that reason.

## NOT COVERED

- **Live sweep owed** (skill section 5f). This is a runtime change and it is **not** Done on offline
  green. Nothing here was exercised against a running stack.
- **`users.ts` `POST /me/mfa/disable` verifies the TOTP only `if (user.mfaSecret && …)`** — so an account
  with no stored seed disables MFA with **no proof of possession at all**. A separate defect in the same
  handler, named here and left for its own ticket rather than widened into this PR.
- **Existing rows are NOT backfilled.** Accounts that already disabled MFA before this change still hold
  the retained seed and backup codes; nothing audits or clears them.
- `POST /api/users/me/mfa/verify` re-arming on an existing seed without minting a new one is unchanged —
  it is the amplifier for this defect, not the defect, and it stays as it is.
