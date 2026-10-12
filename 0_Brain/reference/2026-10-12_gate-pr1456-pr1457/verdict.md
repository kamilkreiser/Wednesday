# QA gate — PR #1456 (KS-1006) and PR #1457 (KS-1236) — 2026-10-12

Independent Opus gate. Read-only toward Secuura: no pushes, merges, comments, board writes or deploys.
My own clone: `scratchpad/gate` (`git clone --no-hardlinks` from `worktrees/s-v3-l05b`; the KS-1006 head was fetched from `worktrees/s-v3-l05`). `npm ci` and the shared build were run inside the clone.
On the remote (`ls-remote`): develop = `65d7722f83a6`, `refs/pull/1456/head` = `745fbff4…`, `refs/pull/1457/head` = `13d3bf19…`. Both heads exist, each is a single commit, and the merge-base of each is develop.

## Verdicts
- **#1456 @ 745fbff461f83df0ddec14c37104b4e2f55c8eac — GO WITH NOTE**
- **#1457 @ 13d3bf195a3f7d93d345c694adac04adb98798ed — GO WITH NOTE**

No Major defects in either PR.

## Evidence (my runs)
| Check | base 65d7722 | #1456 | #1457 |
|---|---|---|---|
| Diff | — | users.ts +8/-1; new ks1006 test +131. Nothing else. | users.ts +20/-1; new ks1236 test +175; ks1194 test +7/-5. Nothing else. |
| Full services/auth vitest | 81 files / 875 pass | 82 / 880 pass | 82 / 884 pass (matches the seat logs) |
| New tests with base product code | — | 3 fail, 2 pass (the 3 RED cells fail; the CONTROL and POSITIVE cells pass) | 5 fail, 4 pass (4 RED cells plus the pre-read-fail cell fail; the reject, positive, equal and SOCIAL controls pass) |
| Planted red: product line reverted | — | the 3 RED cells fail | `if(false)`: the 4 RED cells fail |
| Extra mutants | — | drop verifyTOTP: the wrong-code CONTROL fails | `>=`: the EQUAL control fails. No uppercase: the lowercase cell fails. Swallow the pre-read error: the pre-read-fail cell fails |
| tsc --noEmit | 0 errors | 0 | 0 (control: a planted type error was caught; note tsconfig excludes `__tests__`) |
| eslint src | 0 errors, 15 warnings | identical | identical |

**ks1194 file (#1457).** The diff changes the doc comment and 4 `userReadPlan` arrays only: each array gets a leading `'ok'`. No `expect` line is touched.
- Read-back branch reverted to a blind restore at the head: 3/6 fail. The same mutant at the base: the same 3/6 fail, so the shifted cells bite exactly as before.
- Plans un-shifted at the head: 4/6 fail, so the shift is necessary. F-2 log-truth does not catch the blind mutant on either the base or the head. That gap was there before this PR.

**Spec.** `/api/users/me/mfa/disable` is registered at `auth.openapi.ts:2211` and in `docs/openapi/secuura-api.yaml`, and it already documents 400 "MFA not enabled, or invalid code". `/verification/{requestId}/review` is registered nowhere: 0 hits in both specs, against the mfa/disable control. So "no spec change needed" is true for both PRs. For #1457 it is true only because the route is undocumented, which was already the case.

## Defects / notes
**#1456**
1. Minor — `users.ts:1121` says a no-secret account "can still disable through POST /api/auth/mfa/disable (password or backup code)". That overclaims. A passwordless (wallet or social) account with no secret AND no backup codes cannot satisfy either route (`mfa.ts` else-branch).
2. Minor — the ks1006 test header (`:10-11`) calls this "a latent shape, not a live bypass". That understates it. `decryptMfaSecret` (`userRepo.ts:172-189`) returns `undefined` when the DEK is missing or destroyed, or when decryption fails. So on the base, a decrypt fault let any 6-character string disable MFA. The fix is therefore more valuable than the PR says.
3. A legitimate user with a secret and a valid code still disables: the POSITIVE cell uses the real `verifyTOTP` and gets 200. This route never had a backup-code or admin path, so none is broken.

**#1457**
4. Minor — race, neither claimed nor addressed. The level check (`users.ts:1381-1384`) and the write (`:1404`) are separate statements. A raise that lands between them can still be lowered. The window is now milliseconds rather than days. Closing it needs a conditional UPDATE.
5. Minor — `users.ts:1272-1275` keeps a local order that leaves out NONE and SOCIAL, and says they "cannot be compared". The canonical order exists: `VERIFICATION_LEVEL_ORDER` in `packages/shared/src/verification/policy-engine.ts`, `NONE<BASIC<SOCIAL<STANDARD<…`. The outcome is still safe because the zod schema limits targets to STANDARD and above, all of which rank above NONE and SOCIAL. The comment is inaccurate, though, and the list duplicates the shared one.
6. Note — a refused stale request stays PENDING. Until an admin rejects it, submit will refuse any new request from that subject with "already pending". This is consistent with the "reviewer rejects" design and is covered by the CONTROL reject cell.
7. Note — for a tenant-scoped admin, the subject is now read twice (`:1364` and `:1381`). This is harmless.

Also: `ls-remote` shows sibling branches `…-1` for both tickets (`f132c92`, `1c7c01a`). They are not these PRs; check that they are not stale duplicates.
