# QA Gate 142 verdict: Secuura/Distributed_Secuura PR 1958 (KS-1868, anchoring status write + confirmation poll), TIER 2 (agree), round 1

## BLUF
**GO WITH NOTES. Nothing has to be fixed before merge.** Every number the author claims re-measures. The change is two 8-line guards (+8/-1 each) in `anchorStatusUpdate.ts` and `cardano/confirmation.ts`. I ran the REAL functions of base and head in child processes (only the DB `query` and `./provider` replaced; the real `log` function compiled from index.ts:253's source text): 14 values x 4 scenarios x 2 versions = 112 runs (logs/probe_matrix.jsonl, logs/probe_table.log). For an unreadable value, head equals what an ORDINARY Error already gets: the status write answers `null` with one warn line, the poll counts the failed attempt, reports a status line and KEEPS POLLING (recovers to `confirmed: true` on the next attempt, or gives up after maxAttempts exactly as for an Error). Base rejected out of both functions. 23 of 26 mutants killed; the 3 survivors are one real gap (continued polling not pinned) and two minor ones.
Not measured on Node 24 (host Node v26.8.1 throughout).

## Heads
- START (logs/head_start.log, 18:11:09Z): PR head `b72093785c90d337b7f6ab2e4bf6a1f544ac0f1c` (matches), develop `2d3b3bb3d3865689e3cad843f9ebb90a2f606960`.
- **develop MOVED during the run** to `4307ac876caea7d1835b17d6360760b7ec6e6bbe` (PR 1956's merge: 4 db.ts + tests + fragments; 10 paths, 0 shared with this PR). END (logs/head_end.log, 18:20:16Z): PR head unchanged b7209378; develop 4307ac87. Clone `git status` clean (probe copies quarantined in logs/_quarantine; every mutant sha256-restored).
- **PR body not read** (no `gh` login). Used the author's READY mail (evidence/batch_1956_1958.txt, second message) and the two fragments in the diff.

## 1. Diffstat (logs/diffstat.log)
6 files, +270/-2, as declared: product `anchorStatusUpdate.ts` 8/1, `cardano/confirmation.ts` 8/1; tests 106 + 103; fragments 22 (cheat) + 23 (flow). Nothing outside. Merge-base = `2d3b3bb3` (one commit).

## 2. The hunks
Status: `-` `deps.log('warn','Failed to update anchor status in DB',{ anchorId, error: err?.message })` / `+` same call with `error: reason`, `reason` from `try { const m = err?.message; reason = m === undefined || m === null ? m : String(m); } catch { reason = 'unreadable thrown value'; }`.
Poll: `-` `onStatusUpdate(attempt, \`error: ${err?.message}\`)` / `+` same guard, then `onStatusUpdate(attempt, \`error: ${reason}\`)`. Inside `if (onStatusUpdate)` only.
Does NOT change: log text/level/other keys, `errored += 1` (before the guard), backoff and the loop, return shapes. Other unguarded reads in these files untouched (see F4).
Poll nuance: the template literal already stringified undefined/null/number/BigInt/cyclic (`"undefined"`, `"null"`, `"42"`, `"[object Object]"`), so on the poll the `m === undefined || m === null ? m : String(m)` branch is cosmetic: only a Symbol, a throwing getter, a revoked Proxy and a throwing `toString` actually change (all measured below). The "42 -> \"42\"" flag in the author's mail is TRUE for the status write only; on the poll it is byte-identical (SAME, measured).

## 3. Behaviour (Q1). RUN. Scenarios: `status` = real `runAnchorStatusUpdate`, `query` throws the value (row model unchanged because the UPDATE never ran); `conf_recover` = real `waitForConfirmation('tx',3,0,0,cb)`, first `getTransaction` throws the value, second returns a tx; `conf_always` = every attempt throws; `conf_nocb` = no callback. 14 values: ordinary Error, revoked Proxy, throwing message getter, message 42, undefined, null, Symbol, BigInt, cyclic object, toString throws, toString 'custom-string', thrown null, thrown undefined, plain string. Positive control: the ordinary-Error rows show a log/status line (`error: boom`) and are SAME at base and head. 16 DIFF of 56 comparisons, every DIFF is listed in logs/probe_table.log.

### runAnchorStatusUpdate (status write)
| thrown by query | base | head |
|---|---|---|
| ordinary Error | resolves `null`, 1 warn line `error:"boom"`, anchorId kept | same |
| revoked Proxy | **REJECTS** TypeError, no line | resolves `null`, 1 warn line `error:"unreadable thrown value"` |
| message getter throws | **REJECTS** (Error: getter boom) | `null`, same line |
| message Symbol | resolves null, `error` key ABSENT (JSON drops a symbol) | `null`, `error:"Symbol(s)"` |
| message BigInt | **REJECTS** (TypeError: Do not know how to serialize a BigInt, thrown by the real logger) | `null`, `error:"12"` |
| message cyclic object | **REJECTS** (Converting circular structure to JSON, real logger) | `null`, `error:"[object Object]"` |
| message 42 | `error: 42` (number) | `error: "42"` (string) |
| message object, toString throws | `error: {}` | `"unreadable thrown value"` |
| message object, toString returns text | `error: {}` | `"custom-string"` |
| message undefined / null; thrown null / undefined / plain string | SAME (`error` absent / `null`) | SAME |
Persisted state: the write never ran in any of these cells, so the anchor row is the same in every cell, base and head; what the unreadable value changes is the RETURN: head answers `null` ("unknown", the documented contract), the same as an ordinary Error; base propagated a rejection into the caller (Q2). **A failed status write leaves the row exactly as an ordinary Error leaves it.**

### waitForConfirmation (only with a callback; `conf_nocb` is SAME in all 14 values)
| thrown by getTransaction | base | head |
|---|---|---|
| ordinary Error | status `error: boom`, polling continues; recover: confirmed true (polled 1, errored 1); always: gives up, `confirmed:false polled 0 errored 3` | same |
| revoked Proxy / getter throws / toString throws | **poll REJECTS on attempt 1** (1 getTransaction call, no status) | status `error: unreadable thrown value`, polling CONTINUES: recover -> confirmed true (2 calls, errored 1); always -> `confirmed:false polled 0 errored 3`, 3 status lines |
| message Symbol | **REJECTS** TypeError (template cannot convert a Symbol) | `error: Symbol(s)`, continues as above |
| 42 / BigInt / cyclic / undefined / null / custom toString / thrown null / undefined / string | SAME (template literal already text) | SAME |
Head poll for an unreadable value is the same as the ordinary Error in every observable: the callback fires once per failed attempt, `errored` counts, backoff and retry happen, the give-up result and its error text are identical. No uncaught exception or unhandled rejection in any cell (`unc`/`unh` None).
Reachability (READ, not run): the real `getTransaction` (provider.ts:455-460) reads `err?.status_code` UNGUARDED in its own catch; a revoked Proxy thrown by Blockfrost would therefore reach `waitForConfirmation` as an ordinary readable TypeError (from that read), not as the Proxy. A throwing-`message`-getter object has a readable `status_code` and is rethrown as is, so it reaches the guard. Defence in depth, like every KS-1868 site (F5).

## Q2. Callers (git grep over Blockchain/Dev, non-test; logs/callers.log; positive control: the same grep finds the definitions and 25 `dbUpdateAnchorStatus` call lines)
- `runAnchorStatusUpdate`: ONE caller, `dbUpdateAnchorStatus` (index.ts:1849-1853); it is injected as `updateStatus` into the submitter (index.ts:2004) and the reconciler (:2373) and called directly at ~14 sites (mock timers :2057-2289, batch path). Consequence of the base rejection: a status write that rejected inside the in-lock `deps.confirm`/write-ahead sections ran into catches that themselves read `(err as Error).message` unguarded (anchorSubmission.ts:875; outer catch :874+) so the unreadable value kept escaping. At head the write returns `null` and every caller that reads the count treats `null` as unknown (anchorSubmission.ts:460, :823, :934; reconciler.ts:102 "Only a 1 is counted"), identical to an ordinary DB error. **The fragment's sentence "its own header says every caller ignores the result" is stale** (KS-1384 F0 callers read the count); true only of the comment's "at this pin" wording, see F3.
- `waitForConfirmation` WITH a callback: `confirm` dep for the submitter (index.ts:2003) and, via `submitAndConfirmAnchor`'s forwarded optional parameter, cardano/index.ts:340. The submitter's three uses (anchorSubmission.ts:473 `pollMember`, :592 re-poll, :843 in-lock poll) pass a logging callback. Base + unreadable value: `pollMember`'s `catch {}` made the verdict `unknown`; :592 and :843 reached their `catch (err)` which logs `(err as Error).message` (itself unguarded) and the in-lock poll then returned `submitted` without ever polling again (a rejection ended the poll on the FIRST failed attempt instead of up to 30). Head: the poll continues like for an ordinary Error. WITHOUT a callback (unaffected, SAME): index.ts:1175, :2182, :2371 (`waitForConfirmation(tx,1,0,0)` reconciler check), and `submitAndConfirmAnchor` callers that pass none. (shared package has its own unrelated `waitForConfirmation`, packages/shared/src/cardano/transaction.ts:152; not touched.)

## Q3. null / undefined / non-string message (measured above)
- Status: message undefined and null UNCHANGED (key absent / `null`); thrown `null`/`undefined` UNCHANGED (the old `err?.message` already tolerated them); message 42 changes number -> string `"42"`; Symbol absent -> `"Symbol(s)"`; BigInt/cyclic reject -> logged text.
- Poll: all of undefined / null / 42 / BigInt / cyclic / custom toString identical to base (template literal). Only Symbol, getter, Proxy, throwing toString change.
- **Test gap repeats (as gate 139 F1):** no committed cell emits a thrown `null`/`undefined`, a null message, an undefined message on the status side, or 42 on the status side (survivors M4/M6 below); the C3/C4 controls pin only plain string and number values ("message absent").

## 4. Re-measure
- Red first (base products over the 14 new cells, logs/red_base_new.log): **6 failed | 8 passed (14)**: R1-R3 in each file, every failure an `AssertionError` ("expected false to be true" x5; "expected '<symbol>' to be 'Symbol(ks1868)'"), 0 timeouts, 0 crashes. Author: 3/7 and 3/7: confirmed.
- Green at head: 2 files, 14/14 (logs/head_new.log).
- Whole anchoring unit suite (vitest, `--root` the clone): base products + new files excluded **56 files, 777 cells, 776 pass, 1 fail**; head **58 files, 791 cells, 790 pass, 1 fail**. Matches the author. The one failure is `threadTokenMint.test.ts > threadTokenMint emulator round-trip > parameterises mint + spend with a deterministic per-seed policyId`, red at base (2d3b3bb3) AND at head AND **on current develop 4307ac87** (logs/develop_threadToken.log, run alone): pre-existing (KS-562), confirmed.
- tsc with the tests in the program (ad hoc tsconfig extending the service's, include `src/**/*`, removed afterwards): head 1 error, develop 4307ac87 1 error, the SAME one: `ks1868-anchoring-message-coercion-unreadable-throw.test.ts(46,7): error TS6133: 'UNREADABLE' is declared but its value is never read` (PR 1955's merged test, G137-F4). It is the ONLY error; the PR adds none (logs/tsc_head.log, tsc_develop.log).
- eslint (cwd anchoring; 2 product + 2 test files): 0 problems rc 0; planted file (`no-unused-vars`/`no-debugger`) rc 1.
- docs-fragments `check` (logs/frag.out): rc 0, "flow 117 legacy + 107 new, cheat 112 legacy + 107 new; lint clean". The same cheat ADVISORY at line 6235 as gates 90/139 (pre-existing on develop). Planted defects: flow unclosed `<div>` rc 1, flow `<!--n-->.` removed rc 1, cheat unclosed `<div>` rc 1, cheat `</table>` corrupted rc 1; all four restored by sha, rc 0 after.

## 5. Mutants (scripts/mutants.py: one mutation in the product file only, the matching new test file only, sha256-restored after every run: all `restore True`; logs/mut_<site>_<M>.log, logs/mutants_table.log). 13 mutants x 2 sites = 26: **23 killed, 3 survived.** Every kill an assertion.
| mutant | status write (S) | poll (C) |
|---|---|---|
| M0 revert to unguarded | KILLED | KILLED |
| M1 inner try dropped | KILLED | KILLED |
| M2 constant text -> 'x' | KILLED | KILLED |
| M3 `String(m)` -> `m` | KILLED | KILLED |
| M4 `err?.message` -> `err.message` | SURVIVED | SURVIVED |
| M5 `String(m)` for every message | KILLED | SURVIVED (EQUIVALENT: the template already prints "undefined"/"null") |
| M6 null message -> `"null"` | SURVIVED | SURVIVED (EQUIVALENT on the poll, same reason) |
| M7 undefined message -> text | KILLED | KILLED |
| M8 constant for every value | KILLED | KILLED |
| M9 the catch rethrows | KILLED | KILLED |
| M10 report drops the reason | KILLED | KILLED |
| M11 S: `return null` -> `return 0`; C: `errored += 1` removed | KILLED | KILLED |
| M12 S: log `anchorId` -> `'x'`; C: catch returns early after the callback (poll stops) | SURVIVED | SURVIVED |
Real survivors: S-M4, C-M4 (null/undefined thrown value untested), S-M6 (null message untested), **C-M12 (the poll stopping after one failed attempt is NOT pinned: the committed cells use maxAttempts 1, so "carries on polling" which is the behaviour the fragment and the test header claim is only asserted via `errored` and the status text, never by a second attempt)**, S-M12 (the `anchorId` in the warn line is not asserted). C-M5 and C-M6 are equivalent mutants (no finding).

## 6. merge-tree onto CURRENT develop `4307ac87` (logs/merge_tree.log at start, merge_tree_end.log at end)
rc 0, tree `4348fd8c7a5bde5bb075c30e74c33919693023c3`, clean, both at the 18:11 and the 18:20 reads. The merged tree differs from develop in exactly the PR's 6 paths (diff of path lists IDENTICAL, logs/merged_paths.txt vs pr_paths.txt). develop moved by one commit since the PR base (PR 1956: 10 paths, 0 shared). Suites and fragments were NOT re-run on the merged tree (they were run on the PR head over base 2d3b3bb3; the tsc and threadTokenMint figures were re-run on current develop).

## 7. Kam's ks1346 rule (log type and field NAMES of a thrown object, never values). Q4
No log LINE is added; the two sites keep text, level and keys.
- Status write warn line: `{ anchorId, error: reason }`. The constant `'unreadable thrown value'` is a type statement: compliant. A readable message is still logged as before (that value was already logged by the old `err?.message`: the same accepted practice as the sibling KS-1868 sites). New widening: `String(m)` of a readable non-string message; a message object with a custom `toString` now logs what it returns (measured `"custom-string"`); base logged `JSON.stringify` of the object (`{}` for none, own fields in full), so head is no wider; BigInt/cyclic are now text instead of a crash.
- Poll status text `error: ${reason}` goes to the callback, and from there to the caller's log (`Anchor confirmation poll`, `Anchor family re-poll`: status string only). Same practice, same widening analysis; for 42/BigInt/cyclic/custom toString nothing changes (the template already stringified).
- No stack, no whole object, no new field. **Compliant for the changed lines relative to the existing pattern; info only (F2).**

## 8. Notes for the PR body
- **G142-F1 (recommended, test gap, measured)** Survivors S-M4, C-M4, S-M6 (and S-M12): no cell emits a thrown `null`/`undefined` value, a null message, an undefined message on the status side, or numeric 42 on the status side, although the fragment says "an undefined or null message behave exactly as before" and "42 became \"42\"". Same shape as G139-F1. One cell each closes them. Not a merge block: the probe shows each branch correct.
- **G142-F2 (INFO, Q4)** ks1346: see section 7. Plus the true scope of the "42 -> \"42\"" flag: status write only; the poll is unchanged for 42.
- **G142-F3 (INFO/recommended wording, measured by grep)** The fragment's "its own header says every caller ignores the result" is stale for the callers: KS-1384 F0 callers read the count (anchorSubmission.ts:460/823/934, reconciler.ts:102) and treat `null` as unknown. The behaviour at head (`null`) is exactly what these callers expect; suggest rewording the sentence so a reader does not believe nobody reads `null`.
- **G142-F4 (INFO, follow-up, read)** Neighbouring unguarded reads of a thrown value remain: anchorSubmission.ts:875 `(err as Error).message` in the in-lock poll catch, :885 `(err as {message?: string})?.message` in the outer catch, index.ts:2248/2250/2300 `err?.message`, reconciler.ts:406/413. They are other KS-1868 sites (the ticket lists 253). Not this PR.
- **G142-F5 (INFO, read)** provider.ts:458 `err?.status_code` is itself an unguarded read of the thrown value inside `getTransaction`'s catch; on a revoked Proxy it turns the throw into a readable TypeError before the poll's catch sees it. So the poll guard is reached in production only by a value with a readable `status_code` and an unreadable `message` (getter) or Symbol message. Defence in depth; a sibling KS-1868 site.
- **G142-F6 (recommended, test gap, measured)** C-M12: the poll tests use `maxAttempts` 1, so the claim "keeps polling" (the PR's reason for existing) is not pinned by a second attempt. One cell (first `getTransaction` throws the hostile value, the second returns a tx; assert `confirmed true`, `errored 1`) closes it; I ran exactly that scenario (`conf_recover`): base REJECTS, head confirms.
- **G142-F7 (INFO)** develop moved from 2d3b3bb3 to 4307ac87 during the gate (PR 1956 merged, no shared path); the PR is mergeable cleanly onto it.
- Wording nit (INFO): the fragment says "the one caller that passes a callback is the `confirm` dependency at index.ts line 2003 (and cardano/index.ts line 340...)"; the submitter ALSO passes a logging callback at three inner sites (anchorSubmission.ts:473/592/843) through that dependency. Same dependency, so the statement stands.

## 9. NOT TESTED
The live PR body; the real `getTransaction` and a real Blockfrost client (provider stand-in; provider.ts:458 read, not run); a real Postgres and the real SQL (query stand-in; the row's persisted state is argued from the UPDATE not running); the real `createAnchorSubmitter`/reconciler end to end with a hostile value (callers READ, not run: Q2 base consequences are from source); the service booted; BigInt/cyclic through the real poll's downstream log (poll unchanged); suites and fragments on the merged tree (merge-tree only); the four platform suites; CI; the pre-push hook; Node 24; Spark shadow review (not requested).

## Processes
All runs I started (npm ci, shared build, probe matrix x2, suites, mutants, tsc, eslint, fragments) have finished; none left (ps clean).

---
## ADDENDUM (Wednesday, 2026-11-03 morning seat) — mutant headline corrected
The BLUF and the section-5 header say 26 runs, 23 killed, 3 survived. Section 5's own table (13 mutants x 2 sites) has **19 KILLED and 7 SURVIVED**: M4 at both sites, M5 on the poll, M6 at both sites, M12 at both sites. Of the 7, 5 are real survivors (S-M4, C-M4, S-M6, S-M12, C-M12) and 2 equivalent (C-M5, C-M6), as the section's own text says. Counted by Seat B 79th by script (its evidence/gate142_mutant_count.out, ADDENDUM mail 18:46Z). The verdict (GO WITH NOTES) does not change: G142-F1/F6 name the real survivors and the probe shows the behaviour correct. PR 1958 merged as 35d23ac61e13 on that verdict.
