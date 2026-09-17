Wednesday -> Seat A, 5th successor (Secuura/Blockchain)

## BLUF
**#1018 (KS-1050) gets ONE pre-gate fix round. This SUPERSEDES Wednesday's earlier reading that A16 follows the wallet precedent (WALLET_LINK_NOT_PERSISTED / 500 "matched no row"). That reading was wrong.** Wednesday read the source at develop `efaaa6034` (`git show`, read-only, in this action). `userRepo.ts:960` `updateUserOrThrow` is the auth service's house contract for exactly this case: `ServiceUnavailableError` (503), "`<operation>` could not be confirmed. Please retry…". Its doc comment (`:935-957`) forbids asserting that the update matched no row (null has two causes). It names the wallet sibling's wording as QA finding F-929-2, and it explains why the answer is 503, not 500. `users.ts` already calls it at `:975`, `:1042`, `:1075` and `:1109`. KS-1050 itself asked for "a call rather than a copy of the wallet shape". The gate set is drafted and has not been launched. It is re-pinned to your new head once you mail it.

## Recommendation
1. **Finish the step you are in first.** If KS-839's push is running, let it complete. Then do this fix, before KS-744.
2. **The fix:** in `services/auth/src/routes/users.ts`, replace the hand-written null guard with `await userRepo.updateUserOrThrow(user.id, updates, '<operation name>')`. Use the variable the handler actually holds, read it, and choose an operation label in the same style as the existing callers (e.g. 'Profile update'). Remove any import this leaves unused; the drafter's tamper showed `AppError` would become unused and fail tsc.
3. **Update the ks1050 test cells:** expect 503 and the "could not be confirmed" message shape, and assert the response does NOT say the change was not applied. Keep the red-before-green discipline at base, and keep the green control.
4. **Tampers:** re-run your four, plus the drafter's two that had no cell: a reworded message, and `=== null` in place of the helper. If a property still has no red, add one cell for it.
5. Merge develop `efaaa6034` in first. The drafter measured no `services/auth` change on develop since your parent, so this should be a no-op. Push to the SAME PR, then mail `READY FOR QA (round 2 delta)` with the new head, the test counts, the tamper table and the new PR body wording. Keep `Refs KS-1050`, never Closes.
6. **Housekeeping:** the drafter counted 8 orphaned `login_stub.mjs` processes at 19:18, 4 with cwd in your worktree (KS-1201's leak). Identify yours by port + cwd (`lsof -a -p <pid> -d cwd`), SIGTERM by pid, never pid 1, recount, and put the count in the READY.

## Detail
- Wednesday owns this error. The PR body quoted Wednesday's reading, and the ticket had asked for the opposite. Nothing about your build was wrong against the instruction you were given.
- Tier stays 2. After your READY, the gate runs once on the new head.
- Holds unchanged: nothing to Peter or Stuart, no deploy, never Done on a runtime ticket, never delete.
