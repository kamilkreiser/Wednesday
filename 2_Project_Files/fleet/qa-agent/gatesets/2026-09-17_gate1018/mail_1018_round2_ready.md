SUBJECT: [Secuura/Blockchain -> Wednesday] READY FOR QA (round 2 delta): #1018 KS-1050 @efd677e98c917a52f8af442c9fcfde756166070e (TIER 2)
TS: 2026-09-17T10:02:56.000Z
AUTH: {'spf': 'pass', 'dkim': 'pass', 'dmarc': 'pass'}
Seat A

## BLUF
READY FOR QA (round 2 delta): #1018 KS-1050 at `efd677e98c917a52f8af442c9fcfde756166070e` (tier 2).
- **The fix:** PATCH `/me` now calls `userRepo.updateUserOrThrow(user.id, updates, 'Profile update')`. A 0-row update answers **503 `SERVICE_UNAVAILABLE` "Profile update could not be confirmed. Please retry — if you already succeeded, you may not need to."** `AppError` left the import.
- **The harness** now runs the real `userRepo` over a stateful db stub, with real subject-DEK crypto and a fixed test DEK. It has 3 red cells and 1 control; the third red cell is new and pins the helper's refusal log.
- **Red-proof and tampers:** 9 / 9 rows as predicted, 0 VOID. Every row ran the whole auth suite at 63 files / 755 tests and was restored by sha. G-MSG reds 2 cells and G-NULLONLY reds 1, where round 1 scored 0 for both.
- **Develop merged in twice** (`efaaa6034`, then `19f1e5475` after #1025 landed mid-build), each tree equal to its prediction. Push PROTOCOL-CLEAN. The in-hook preflight ran 12/15 legs, 3 SKIPPED (no stack), nothing failed. 4 stubs of mine ended by verified pid, 0 remain.

## Recommendation
1. **Gate the head `efd677e98`** (tier 2). The round-2 change is `c08cec102`; the two merge commits only bring develop in.
2. **KS-1050's only comment (`413d3b05`) still describes round 1's 500 shape as your reading. I recommend a short correcting facts comment after the gate verdict** saying round 2 replaced it with the helper's 503, per your 09:19:37Z ANSWER. Reason: the ticket is what a human reads, and right now it states a contract that is no longer on the PR. Nothing is posted until you say.
3. **The launcher ticket you asked for would be a DUPLICATE.** I searched `KS-907`, `other live session`, `live claude session`, `SECUURA_SEAT_SCAN` and `seat registry`. **KS-1085 finding 2** (Backlog, filed by s176 on 09-11) already records "the KS-907 seat registry counted a session running in `Testing Agent MAIN`", with its mechanism marked *not verified*. Today's boot identifies the mechanism at source: the argv-scan arm (`Launch_Claude.command:327-339`; the label `(live claude session on this project)` comes only from `:338`), not the registry arm.
   - **Default, on your OK:** ONE facts comment on KS-1085 carrying that evidence, and no new ticket. The draft is `5_Project_History/2026-09-17_seatA-6th/tickets/b-KS-1085-finding2-mechanism.md`.
   - If you still want a separate ticket, say so and I file the draft beside it.
4. **Next, per your 09:45:00Z ANSWER:** #1026 KS-839 round 2 starts now in my worktree (the `parseScopeString` split at `:353`, the 8 padded carriers, the controls, the tampers + G-TRIMSTAR reversed). KS-744 stays held until #1026's round-2 READY.

## Detail

### Head and push
- Branch `feature/ks-1050-usersts933-answers-success-true-over-a-0-row-profile-update`, fast-forward `267bd8624` → `efd677e98c917a52f8af442c9fcfde756166070e`, three new commits:
  - `9c66589bb`: merge of develop `efaaa6034` (parents `267bd8624`, `efaaa6034`), tree = the `merge-tree` prediction `0d351b735`;
  - `c08cec102`: the round-2 change (parent `9c66589bb`), `users.ts` +4 −6 and the ks1050 test rebuilt +124 −64 (2 files, +128 −70);
  - `efd677e98`: merge of develop `19f1e5475` (parents `c08cec102`, `19f1e5475`), tree = prediction `ce49c7bfd`. #1025 changed only `scripts/audit/audit-baseline.json`; the auth and shared subtrees are byte-identical to `c08cec102`'s (`89aad911c` / `dbd72dea0`).
- **Origin, read in the send action below:** `refs/heads/<branch>` = `refs/pull/1018/head` = `efd677e98c917a52f8af442c9fcfde756166070e`. PR REST after the body PATCH: open, 4 commits, changed_files 2, mergeable true / `unstable`.
- The #1018 reviews endpoint read 0 reviews immediately before the push.
- Push 09:55:40Z → 10:00:53Z, rc 0. push_protocol verify: PROTOCOL-CLEAN, fast-forward, config sha identical, worktrees identical, 113 heads identical, other refs changed 0.
- In-hook preflight: `PREFLIGHT INCOMPLETE — 12/15 legs ran, 3 SKIPPED. Nothing failed.` Legs 3, 4 and 8 skipped (no local stack): not a pass of those. Leg 1 `spec is in sync`; leg 5 59 / 59 audit-contract cases; legs 6/7 audit-gate 33 advisories / 34 baselined and audit-locks 43 locks / 32 matched / 32 baselined; shell suites 35 / 35.

### The change
`routes/users.ts` at the head:
```
16: import { BadRequestError, NotFoundError, ServiceUnavailableError, ValidationError } from '../middleware/errorHandler'; // KS-1018: …   (byte-equal to develop's line)
    // KS-1050: "success: true" over a write that did not land tells the user their
    // profile changed when it did not. The helper refuses with a retryable 503.
    const updated = await userRepo.updateUserOrThrow(user.id, updates, 'Profile update');
```
The response block after it is unchanged. The spec already declares 503 for PATCH `/api/users/me` (`auth.openapi.ts:985`), so there is no spec change.

### Cells (ks1050, the real repo)
- 🔴 C1: rowCount 0 → 503, `success: false`, code `SERVICE_UNAVAILABLE`, message `^Profile update could not be confirmed\. Please retry`, and the body matches none of `/not applied|matched no row|did not persist/i`. Exactly 1 UPDATE and 0 read-backs after it, so the null is the 0-row arm's.
- 🔴 C2: rowCount 0 → `success` is never `true`, and `User profile updated` is not logged.
- 🔴 C3: the helper's `logger.error('User update could not be confirmed — refusing to report success', { userId, operation: 'Profile update', columns: ['firstName'] })`.
- Control: rowCount 1 → 200, `firstName` 'Grace' read back through the real decrypt, stored `first_name` starts `d1:`, 1 read-back after the UPDATE, success line logged.
- Harness facts: `../db` stub with `isDbAvailable: () => true`; `services/subjectDeks` stubbed to a fixed 32-byte DEK; the caller injected inside `runWithTenantId(TENANT_ID)`, as `authenticate()` does, so no pre-auth lookup; logger spies. **Stub count: 5 `vi.mock` modules** (`../utils/logger`, `@secuura/shared/utils/logger`, `../services/subjectDeks`, `../db`, `../middleware/authenticate`) plus 2 carried from round 1 (`../services/session`, `../services/password`), so 7 in total. `userRepo`, `users.ts`, `errorHandler` and the shared crypto are all real.

### Red-proof and tamper table
Runner `5_Project_History/2026-09-17_seatA-6th/ks1050-r2/tamper.py`, output `tamper/tamper.json`, 19:53:34 → 19:54:16 AEST. Each row:
- one anchored edit (count asserted 1) or a whole-file blob swap;
- `npx tsc --noEmit -p .` (non-zero = VOID);
- the WHOLE auth suite, denominator asserted = T0's (63 / 755 / pending 0);
- restore by bytes, asserted against the HEAD blob plus `git diff --quiet HEAD`.

Every ks1050 red is an `AssertionError`, and there were 0 load failures.

| Row | Form | ks1050 reds (pred = measured) | Other reds | tsc |
|---|---|---|---|---|
| T0 | none | 0 | 0 | 0 |
| RP-BASE | `users.ts` = `7e89318bc` (no guard) | C1 `expected 200 to be 503`, C2 `expected true not to be true`, C3 | 0 | 0 |
| RP-R1 | `users.ts` = `267bd8624` (round 1) | C1 `expected 500 to be 503`, C3 | 0 | 0 |
| TN-a | `if (Date.now() > 0) return updated as unknown as User;` first inside the helper's null block | C1, C2, C3 | 6: ks1052-backup-code-burn-cause-a A1 + ks1052-credential-lifecycle ×5 (the helper's other callers) | 0 |
| TN-b | the call site back to a bare `userRepo.updateUser(user.id, updates)` | C1, C2, C3 | 0 | 0 |
| TS | `throw Object.assign(new ServiceUnavailableError(…), { statusCode: 200 })` in the helper | C1 `expected 200 to be 503` | 4: the same ks1052 pins | 0 |
| TI | inert comment on the call line | 0 | 0 | 0 |
| G-MSG | label `'Profile update'` → `'Profile change'` | C1 (`expected 'Profile change could not be confirmed…' to match`), C3 | 0 | 0 |
| G-NULLONLY | `updateUser` + `if (updated === null) throw new ServiceUnavailableError('<same message>')` | C3 | 0 | 0 |

How each was translated, as accepted in your 09:47:42Z ANSWER:
- **TN-a** does not use the literal `if (false && !updated)`. That form would leave `updated` un-narrowed at the helper's `return updated` (`Promise<User>`) and VOID the row on tsc, so the null block returns early instead.
- **TS** re-statuses the helper's error, because `users.ts` holds no status literal any more.
- **G-NULLONLY:** C1 and C2 cannot catch it, and I read that as the code being equivalent, not as a gap. Both of `updateUser`'s null sources return `null` (the 0-row arm, and `getUserById`'s not-found), and its declared return is `Promise<User | null>`, so `=== null` and `!updated` agree on every value the real repo produces. C3 is the cell that catches it: a hand-written guard skips the helper's refusal log. That is the cell added for the "property with no red" instruction.

### Suites, tsc, eslint (ratios)
- ks1050 alone 4 / 4.
- Whole auth suite 63 files / 755 tests, 0 failed, 0 pending: at `c08cec102` (T0) and re-run at `efd677e98` (755 / 755). Develop is 62 / 751 per your #1018 drafter (`7e89318bc`, no auth change since), so this is +1 file / +4 tests. I did not re-measure develop myself.
- `packages/shared` 44 / 851 at `c08cec102` (subtree identical at the head).
- `tsc --noEmit -p services/auth` rc 0.
- **Test-including program** (scratch tsconfig extending auth's, `exclude: []`, the ks1050 test in the program by `--listFilesOnly`): rc 2, 68 error lines, all in pre-existing test files; **0 in the ks1050 test, 0 in `users.ts`**. My first draft typed its server as `node:http` `Server` and joined the pre-existing TS2741 `keepAliveTimeoutBuffer` class (10 other test files have it); the head takes the type from express instead.
  - I did not measure the program at develop. Your #1018 drafter's 37 (head 43) was read at `267bd8624` on older develop, so the two counts are not comparable.
- **eslint:** `users.ts` 0, ks1050 test 0. Control: `users.ts` on stdin with an unused import appended → `no-unused-vars` fires.

### PR body wording (PATCHed and read back byte-equal)
- **Title:** `KS-1050: a profile update that matched no row answers 503 "Profile update could not be confirmed", not success`.
- **Body:** a new BLUF / Recommendation / Round 2 section (what changed, the real-repo harness, cells, red-proof, tamper table with the translations, Test Evidence, platform suites, PII) sits above `## Round 1 record (the 500 PROFILE_UPDATE_NOT_PERSISTED shape, SUPERSEDED by round 2; kept as written)`, which holds round 1's body verbatim with headings demoted one level.
- The body opens `Refs KS-1050 (https://linear.app/secuura/issue/KS-1050)`. Closing phrases 0 (regex control fires on "Closes KS-1"), at-signs 0, Claude Code footer present.

### Links and ticket
- `attachmentsForURL(pull/1018)` after the push = KS-1050 `contributes` (In Progress). Controls: pull/1026 → KS-839 `contributes`; pull/99999 → [].
- The ticket comment naming the PR is KS-1050 `413d3b05` (2026-09-16 22:42Z), the only comment, and it describes round 1. KS-1050 stays In Progress (§5f).

### Stubs
`stop_push_stubs.py` (ps rows parsed 1100): 4 targets, pids 51124 / 51444 / 51741 / 52076, started 19:58:09-12 AEST, cwd this worktree, ppid 1. Each was SIGTERM'd, 0 alive after 2 s, and my login_stub listeners now read 0. **4 more are Seat B's** (cwd `worktrees/raise-0917-b-audit-2`, started 19:58:53-55), left alone.

### NOT done / NOT covered
- a real database or RLS path producing a 0-row UPDATE;
- the other discarding `updateUser` callers (the ticket's open question);
- Schemathesis, Akto, Playwright and k6 (no stack);
- `generate-openapi --check` as a separate run (the preflight's leg 1 read the spec in sync);
- develop's auth denominator and its with-tests tsc count, not measured by me.

