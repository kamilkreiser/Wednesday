# Gate verdict: PR #1479 (KS-1188 F3), medium tier

**VERDICT: GO WITH NOTE**
Head: f55d6cf176fc5a564a8cfa571ca7f2c6ffb41462 (found in seat worktree s-v3-l05b; own clone in scratchpad, no shared-repo writes).
Base db0df454; develop 0ae2339e (as in the seat's local origin/develop; I could NOT fetch remote, so "develop moved" is unchecked).
Predicted tree by my merge-tree/merge: 9c65d8df6c25 = matches the claim.

## By my runs
1. Diff: exactly 2 files, +183/-5 (passwordLoginGate.ts +24/-5 net as described, plus new test 159 lines). Only the burn call is wrapped; nothing else touched.
2. New file: base source restored -> 3 red / 3 green (the 3 RED cells); head 6/6.
   Mutations (head, one at a time): ===500 -> 3 red; instanceof -> 3 red (confirms KS-1467 reasoning); no-rethrow (swallow) -> 1 red (control); drop 503 check -> 1 red (control); drop "if you signed in" -> 1 red; drop alternatives -> 2 red; drop "spent" -> 2 red; throw plain Error -> 2 red. All killed.
3. services/auth head: 85 files / 900 tests green. Predicted merged tree: 88 files / 919 tests green. tsc --noEmit rc 0 on both (tests are excluded from the project tsconfig; new test file checked by a separate tsconfig: 0 errors; control file with a type error was detected). eslint on the two changed files: 0 errors 0 warnings on head and merged; whole src on merged: 0 errors, 15 warnings (not in changed files). Control: planted debugger flagged.
4. Questions (probe test, head):
   - Enumeration/oracle: with the burn faulted, valid code -> 503 reworded; invalid code -> uniform {refused}, no UPDATE, lockout +1; user with null or empty backup codes + same code -> uniform refused, no UPDATE. Message is one constant, identical for 0-row and read-back failure. The 503-vs-401 distinction pre-exists (the gate's own comment says so) and the old text also named "Backup-code sign-in"; the new text is conditional and adds no new information. Leak to an attacker inducing a DB fault: the 503 status already says "code was valid"; the new wording adds nothing beyond that.
   - Only the burn: the try wraps one await; other 503s (reencrypt, lockout, user lookup) are outside it. Grep: old text "Backup-code sign-in could not be confirmed. Please retry" is asserted nowhere (only userRepo helper and unrelated KS-1050/1052/1194 tests on other operations); callers auth.ts, oauth.ts, wallet.ts just propagate; no frontend reads it.
   - Swallow/reclassify: non-503 AppError (404) rethrown as the same object; null and string throws rethrown unchanged (optional chaining safe).
   - Burn once: UPDATE count = 1 in the faulted case (no retry added).
Not run (as the seat said): four platform suites, real Postgres leg, frontend wording.

## Defects
Major: none.
Minor:
1. passwordLoginGate.ts:66-71 a const (and its import) sits in the middle of the import block, before `import { STATUSES_MAY_RECEIVE_CREDENTIAL }`. Cosmetic; lint passes.
2. ks1188-f3 test: no cell asserts the burn runs exactly once, and the invalid-code/healthy controls are not mutation-killed by the wrapper (they guard other paths). I verified once-only by probe; suggest adding it.
3. Wording tells the user to spend another backup code even when the fault was pre-burn (code still valid). Accepted trade (ruled option A, true in both cases).
Note: frontend does not display the string as far as grep shows; real-Postgres leg remains unrun.
