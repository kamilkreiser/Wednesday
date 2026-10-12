# Gate verdict: PR #1458 (KS-1194 part 2), MFA auto-approve fail-closed

**Verdict: GO.** Head `c384811896142717dd498e0a41c6c178baf4ca57`. 0 Major, 0 Minor, 2 notes (neither blocks).
Gate: independent Opus QA, read-only. Run 2026-10-12 ~16:50 AEST in my own clone (scratchpad `g1458`, cloned with `--no-hardlinks` from the seat's s-v3-l05 clone). Nothing was pushed, commented or written to the board.

## Identity
- `ls-remote origin`: `refs/pull/1458/head` = c384811…, develop = a31b7757705e… (matches the brief).
- PR base (merge-base) = 65d7722f8. Develop a31b77577 = 65d7722 + #1456 (KS-1006) + #1457 (KS-1236).
- `merge-tree --write-tree a31b77577 c384811`: clean, tree `fa19fd706d18…`. This matches the seat's `predicted_tree_ks1194p2.txt`. The diff of develop against that tree is the same 2 files, +184/-1.

## (1) Diff: exactly the described change
| File | + | - |
|---|---|---|
| services/auth/src/routes/users.ts | 6 | 1 |
| services/auth/src/__tests__/ks1194-part2-mfa-auto-approve-never-acknowledges-an-unpersisted-level.test.ts (new) | 178 | 0 |

- users.ts: the change is a single line, `updateUser(...)` → `updateUserOrThrow(user.id, { verificationLevel: 'STANDARD' }, 'Verification auto-approve')`, plus a 5-line comment, at :1293-1298. Nothing else changed.
- Note A (not a defect): the brief says "two test cells". The file actually has **5**: 3 RED, 1 POSITIVE and 1 CONTROL. The commit message describes those 5 accurately.

## (2) Red/green, my runs
| Tree | Result |
|---|---|
| Head (new file) | 5/5 green |
| Base users.ts (65d7722) + new test | 3 failed (all RED cells), POSITIVE and CONTROL green. Base answers `[200, undefined, false, true]` where the test expects 503. |
| Develop users.ts (a31b775) + merged tree | 3 failed / 2 passed (same 3 RED cells) |
| Plant 1: product line reverted (same as base) | 3 RED cells red |
| Plant 2: `updateUserOrThrow(...).catch(() => null)` (swallow restored) | 2 red (0-row, empty read-back). The log cell stays green, which is correct because the log line is still emitted. |
| Plant 3: operation name changed to `'Verification auto approve'` | 2 red (0-row message prefix, log operation) |
| Plant 4: the write deleted | 4 red, including POSITIVE (the level is not raised) |

All plants were reverted afterwards (`git status` clean).

## (3) Suite / tsc / lint
- Auth suite on the head: **82 files / 880 tests passed**, matching the seat's figures. On the base: 81 / 875. On the predicted merge tree fa19fd7: **84 / 894**. There were 0 failures and 0 timeouts, so nothing needed re-running.
- `tsc --noEmit -p services/auth/tsconfig.json`: rc 0 on the head and on the merge tree. That tsconfig excludes `src/__tests__`, so I also type-checked the new test file on its own: rc 0. Control: a planted `const zz: number = 'x'` gave 1 error.
- `eslint src`: 0 errors, 15 warnings. None of them are in users.ts or the new file. Control: test files are linted (5 test files appear in the warning list).

## (4) Semantics
- **Throw:** if updateUser returns null (a 0-row UPDATE, or the read-back finds no row), `updateUserOrThrow` (userRepo.ts:960-977) logs one error line with `{userId, operation, columns}` and throws `ServiceUnavailableError`. errorHandler (errorHandler.ts:290ff) turns that into **HTTP 503**, body `{success:false, error:{code:'SERVICE_UNAVAILABLE', message:'Verification auto-approve could not be confirmed. Please retry — if you already succeeded, you may not need to.'}}`.
  - Leaks: none. The body carries no userId, column, SQL or stack; those go to the server log only.
  - If updateUser throws (an infrastructure error), it propagates exactly as before. That path is unchanged.
- **Success still approves:** the POSITIVE cell gives 200, APPROVED, currentLevel STANDARD, and the stored value is `standard`. It runs against the real userRepo over a stateful db stub.
- **Ordering / partial write:** none. The auto-approve branch writes **no** `verification_upgrade_requests` row; it returns before `saveVerificationRequest`. Its only write is the level.
  - Read-back-empty case: the level may have landed while the client gets 503. A retry then gets 400 "already STANDARD", which is consistent with the "you may not need to" wording. This is the house helper's deliberate behaviour.
- **Callers / tests that depended on the old swallow:** none.
  - 5 test files hit `/me/verification`. None exercises the MFA auto-approve branch: the `mfaEnabled: true` hits in the part-1 file are KS-1006 disable fixtures.
  - The full suite is green.
  - No frontend calls `me/verification` (0 of 365 tracked frontend files). Control: `users/me` has 14 hits across 4 frontend files.
- **Residual (ii) unchanged:** residual (ii) is the #1032 round-2 N-1 record (`5_Project_History/2026-09-18_seatA-8th/tickets/n1-KS-1194-comment.md`): the request reads APPROVED over a level that was never raised, after two pool faults. It lives in the review approve path (users.ts ~:1370-1440: save APPROVED first, then raise the level, re-read on failure, keep APPROVED when the level cannot be read) is outside the diff hunk. The diff touches only :1293-1298.

## (5) Published API spec
- `docs/openapi/secuura-api.yaml`: 0 hits for `me/verification`. Control: `users/me` has 10 hits.
- `auth.openapi.ts:68` explicitly lists `/me/verification` as "not registered". So 503 is not a contract change on any published operation, and no spec edit is needed.

## Notes (do not block)
- **A.** There are 5 cells, not 2. The brief's wording is wrong; the PR's own wording is right.
- **B.** The cell for "UPDATE lands, read-back empty" depends on a hard-coded order of `users` reads (`['ok','ok','empty']`, i.e. 3 reads). It is documented as measured, but if a future refactor adds a read, that cell will fail loudly rather than pass falsely. So it is acceptable.

## Not checked
- A real Postgres or RLS run. The stub covers the 0-row and empty-read-back shapes only.
- The GitHub CI status of the PR. I made no `gh` call.
