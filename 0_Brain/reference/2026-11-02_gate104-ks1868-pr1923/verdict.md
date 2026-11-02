# QA Gate 104 verdict: Secuura/Distributed_Secuura PR 1923 (KS-1868, originate: signatories O67-P1/P2, thirdPartyVerifiers O67-P3/P4, retentionScheduler O68-P3; 12 hunks, +84/-12 product), TIER 1

## BLUF
**GO WITH NOTES. Nothing has to be fixed before merge.** I ran the real `signatoriesRouter` and `thirdPartyVerifiersRouter` on a loopback listener, with only the db, auth and logger replaced (scripts/probe.test.ts). The db stand-in is STATEFUL: it holds the signatory and verifier status, and it can fail in three ways: before the write, after the write is applied, or from the `logger.info` after the write. I also ran the real `retentionScheduler` twice (scripts/probe2.test.ts): R1 with `enforceRetention` replaced, and R2 with the REAL `gdprService.enforceRetention` over a db stand-in holding three policies. Both probes ran at base and at head, 104 + 19 cells each (logs/probe_table.log).
- **A (signatory revoke/reinstate, verifier suspend/reinstate).** In every failure position, an unreadable value at head gives exactly the ordinary-Error outcome: the route's constant 500, the same db calls, and the SAME persisted status. A failure before the write leaves the signatory active (or revoked) and the verifier active (or suspended), as it was. A failure after the write leaves the new status, as an ordinary Error does. One `logger.error` line with `unreadable thrown value`. At base the request got **NO ANSWER** and no log line, and the persisted state was the same as at head. **The change produces no authority state that an ordinary Error does not produce:** 104/104 mechanical checks, 0 DIFF.
- **B (retention).** At the PR's site (`runEnforcement`), an unreadable rejection from `enforceRetention` now logs `Scheduled enforcement failed` with the constant, exactly as an ordinary Error does. The next scheduled run fires at base and at head (2 calls each), and nothing is deleted or kept differently. **But see G104-F1:** through the REAL `enforceRetention`, this site never receives an unreadable value. The gap that changes deletions is one layer down, in `gdprService.ts:499/:503`. That file is not in this PR, and base == head there (measured).
- **C (read routes, verify, records).** Head unreadable == head ordinary in status, body, db calls and log context. Ordinary Error, thrown string and success control: base == head byte-for-byte.
- **D (ks1346).** The new log lines carry only the constant or the pre-existing `String(error)`. No actor email, signatory id or verifier id appears in any error line (probe flags false).
- **E (apply order).** All 5 passes' `patch.diff` sha256 match the brief, and section_1+section_2 == patch.diff (5/5). A strict sequential apply at base 04ff5262 (P1, P2, P3, P4, P3-retention; `--check` rc 0 with empty output) gives a service tree **identical to PR head**. A control against base differs, so the instrument fires. P2 and P4 apply at offset +18 with exact context (no fuzz). The reverse order (P2 before P1, P4 before P3) gives the same bytes, because the hunks are disjoint.

## Heads
- START (logs/head_start.log, 03:09:18Z): PR head `d91960f84e09eac49598737f69a9a1c3b4d5c4cf` (matches the brief), develop `c0f9af13f94b...` (matches), merge-base `04ff5262ad52`. One commit by Kam Kreiser, "Refs KS-1868: originate signatory, verifier and retention catches guard an unreadable throw".
- END (logs/head_end.log, 03:27:52Z): PR head is UNCHANGED. **develop MOVED to `86e12156`** (one commit, KS-1868 kyc). The head did not move, so I did not stop, and I re-ran merge-tree on the new develop (Q6). The local clone is at d91960f8 with a clean working tree. The product files were sha256-restored after every swap (RESTORE_OK each time).
- Diffstat (logs/diffstat.log), three-dot: **10 files, +770/-12**. That is 3 product files (signatories.ts +42/-6, thirdPartyVerifiers.ts +35/-5, retentionScheduler.ts +7/-1), 5 new tests and 1 fragment pair. Nothing is outside the declared paths. This matches the author's mails.
- **PR body not read** (no Secuura gh login here). I used the author's READY and BUILT AND PROVEN mails (evidence/). Body wording I could not see is NOT verified.

## FINDINGS
- **G104-F1 (RECOMMENDED; pre-existing, NOT in this PR; measured, base == head).** The real GDPR retention sweep `enforceRetentionImpl` reads the thrown value unguarded in its per-policy catch (`gdprService.ts:499`) and in its outer catch (`:503`). Probe R2 measured what happens when one policy's DELETE rejects:
  - With an ordinary Error or a string, the sweep logs `Retention enforcement failed` and **continues**: the later policies' DELETE, deletion-log INSERT and `last_enforcement_at` stamp all run.
  - With an unreadable value (a revoked Proxy, or a throwing getter), the :499 read throws, the exception leaves the loop, and :503 logs the new TypeError (or the getter's Error). **Every later policy is skipped for that run:** no DELETE or anonymisation, no deletion-log row, no stamp. A failure on policy 1 skipped 2 policies; a failure on policy 2 skipped 1.
  - So for the job as a whole, data deletion differs from the ordinary-Error path, and it differs at both base and head. This PR neither causes it nor changes it.
  - It also means O68-P3 (this PR's `runEnforcement` site) is defensive only. Through the real `enforceRetention`, that catch always receives a readable value (cells "policy SELECT revokedProxy/throwingGetter": `Scheduled enforcement failed` with the TypeError text at base AND head).
  - **Fix (a follow-up KS-1868 pass, not this PR):** at `gdprService.ts:499` and `:503`, apply the same guard. `let reason: string; try { reason = err instanceof Error ? err.message : String(err); } catch { reason = 'unreadable thrown value'; }`, then log `{ dataType: policy.data_type, error: reason }` / `{ error: reason }`. Also add one cell that asserts policy 2's DELETE still runs after policy 1 rejects with a revoked Proxy.
  - The same unguarded form appears 17 times in gdprService.ts at head (consent, DSR, erasure :917, export :978-1028, :1603). No KS-1868 pass or brief in fleet/briefs_staged covers gdprService.
  - **PR-body wording:** "the retention job behaves as for an ordinary Error" holds for `runEnforcement`, not for the sweep. The body should say that, and name G104-F1.
- **G104-F2 (INFO, pre-existing, base == head).** When a revoke, reinstate or suspend write lands and a LATER step throws (the `logger.info` after it, or a rejection after the write), the route answers 500 "Failed to revoke signatory" (and so on) although the status DID change. The same is true for an ordinary Error. The caller is told the action failed when it took effect. It is not changed by this PR.
- **G104-F3 (INFO, candidates, read).** Five same-shape unguarded reads remain in these two files, and no pass covers them: nominate `signatories.ts:126` (`error.code`) and `:132`; register `thirdPartyVerifiers.ts:103` (`error.code`) and `:109`; approve `:199`.
  - At approve, a throw after the UPDATE (status active, `api_key_hash` set) loses the one-time API key for the ordinary-Error path as well.
  - The author listed :132, :109 and :199. The `error.code` reads at :126 and :103 are a second unguarded read in the same catches, and a fix there must guard both.
- **G104-F4 (INFO, read).** In production at base, the escaped `runEnforcement` rejection reaches `index.ts:75`'s `unhandledRejection` handler. That handler logs `Unhandled promise rejection` and does NOT exit, and the `setInterval` keeps firing. So base never crashed the scheduler or the process; the change only replaces that line with the ordinary one. A real boot was not run.
- **G104-F5 (INFO, mutant tooling).** M3 (the catch rethrows) makes each test FILE fail to run: jest's own `formatNodeAssertErrors` calls `Array.isArray` on the revoked Proxy and crashes. So M3 is red in all 12 sites, but **not by assertion**. I record it as "killed by suite crash". (At gate 101 the same mutant hung; here `--forceExit` was used.)
- **G104-F6 (INFO, ks1346-adjacent, pre-existing).** `String(error)` for an ordinary Error logs its message, and a planted `SECRETVAL` in a message appears at base and head alike. That is unchanged behaviour, and a Prisma error message can carry parameter text. The `logger.info` lines also log the caller-supplied revocation and suspension `reason`, which is pre-existing too.
- **G104-F7 (INFO).** docs-fragments `check` prints the cheat ADVISORY at :6235. The same advisory appears on develop without this PR (G90-F7 / G101-F7).
- No FIX-BEFORE-MERGE item.

## Q3. Behaviour, measured (section 3)
Method: jest, the real router modules, express on 127.0.0.1:0, real `fetch` with a 1.5 s abort ("NO ANSWER"). `../db` is a stateful stand-in that classifies each SQL statement and applies it to an in-memory status map. `authenticate` passes, and a middleware sets `req.user`. The logger records every call. Modes per write route: `pre` (reject, nothing applied), `applied` (status changed, then reject), `loginfo` (status changed, then `logger.info` throws the value). Values: ordinary Error, string, revoked Proxy, Error with a throwing `message` getter. Base = the merge-base product files; head = the PR.

| route (mode) | ordinary Error, base = head | unreadable, base | unreadable, head |
|---|---|---|---|
| sig revoke (pre) | 500 "Failed to revoke signatory", status **active** | NO ANSWER, active, no log | 500 same body, **active**, log `unreadable thrown value` |
| sig revoke (applied / loginfo) | 500, status **revoked** | NO ANSWER, revoked | 500, **revoked** |
| sig reinstate (pre) | 500, **revoked** | NO ANSWER, revoked | 500, **revoked** |
| sig reinstate (applied / loginfo) | 500, **active** | NO ANSWER, active | 500, **active** |
| sig PATCH (pre / applied / loginfo) | 500 "Failed to update signatory" | NO ANSWER | 500 same |
| ver suspend (pre) | 500 "Failed to suspend verifier", **active** | NO ANSWER, active | 500, **active** |
| ver suspend (applied / loginfo) | 500, **suspended** | NO ANSWER, suspended | 500, **suspended** |
| ver reinstate (pre / applied) | 500, suspended / active | NO ANSWER, same state | 500, same state |
| sig GET /, /check, /:id; ver GET /, /:id/records (pre) | 500 constant | NO ANSWER | 500 constant |
| ver verify (lookup / insert / loginfo) | 500, records 0 / 0 / **1** | NO ANSWER, same records | 500, same records |

Success controls: 200, with the status changed exactly once, at both versions. Mechanical judge (scripts/table.py): for every head unreadable cell, the status, body, persisted state, db calls and log context equal the head ordinary-Error cell, with exactly one error line carrying the constant. For every ordinary, string and success cell, base == head: **104 OK, 0 DIFF.**

Retention (probe2; logs/probe2_*.jsonl):
- R1 (enforceRetention rejects once, then resolves; startup 5 ms, interval 60 ms):
  - Ordinary and string: base = head, `Scheduled enforcement failed` with the message, 2 runs.
  - Unreadable: base gives 2 runs and NO error line (jest attributes the escaped error to the cell); head gives 2 runs and `Scheduled enforcement failed` with `unreadable thrown value`.
- R2 (the real enforceRetention, 3 policies, user_sessions / verification_requests / share_records): every cell base == head. The results are in G104-F1.

## Q4. Re-measure (Node v26.8.1; NOT measured on Node 24)
- **Red-first** (logs/red_base.json): the 5 new files with the base product give **24 failed / 25 passed of 49**, split 6/12, 6/12, 6/12, 4/8 and 2/5. Every failed cell is a `RED ... R1/R2` cell, and all 24 carry an `expect(` failure message. Every control passed. Jest also lists the product's escaped exception as the FIRST message of each one, as the author disclosed.
- **Green:** head **49/49** (logs/head_new.json).
- **Whole originate suite:** base without the new files **163 files, 1999/1999**; head **168 files, 2048/2048**. Cell by cell: 49 new, 0 vanished, 0 passed -> not passed (logs/suite_summary.log). This matches the author's figures exactly.
- **tsc:** the plain `tsconfig.json --noEmit` gives rc 0. With the tests in the program (scripts/tsconfig.tests.json, 198 test files including the 5 new ones): rc 0, **0 errors**. A planted TS2322 gives rc 2 and is reported, and was moved to quarantine.
- **eslint** (8 changed files): **0 problems, rc 0**. A planted file gives `no-debugger` plus `no-unused-vars`, rc 1.
- **docs-fragments check:** rc 0, "74 new … OK". A planted unbalanced `<div>` in the PR's cheat fragment gives rc 1, "tags are not balanced"; the fragment was restored by sha256. On the merge tree (c0f9af13): rc 0, "76 new … OK".
- Quoted, not re-run: the pre-push hook (PREFLIGHT INCOMPLETE 13/16, legs 3, 4 and 8 skipped) and the author's own one-hunk reverts and recordings.

## Q5. Mutants (scripts/mutants.py; one site per run, product only, tests untouched, sha256 restore checked: restore True on all 108; logs/mutants_run.log, mut_*.log)
12 guard sites x 9 mutants:
- **M0** (revert the guard), **M1** (drop the inner try), **M2** (catch -> `String(v)`), **M4** (constant for all), **M6** (readable branch -> `'x'`), **M7** (the log ignores `reason`), **M8** (constant text changed), **M9** (log line removed): **KILLED at all 12 sites by assertion**. That is 2 to 4 cells each (M6 at runEnforcement: 1 cell), all failing by `expect(`.
- **M3** (catch rethrows): the test file fails to run at all 12 sites (G104-F5). It is red, but not by assertion.
- **0 survivors.** The thrown-string control cells kill M6 everywhere, so the G90-F3-type gap does not occur in this PR.

## Q6. merge-tree
- Onto develop at START `c0f9af13`: rc 0, tree `52f9f769`. The result changes exactly the PR's 10 paths (SAME_PATHS). Develop changed 23 paths since the base, 0 of them shared with the PR.
- Onto develop at END `86e12156` (moved during my work, by one KS-1868 kyc commit): rc 0, tree `d5a493a3`, SAME_PATHS, 28 develop paths since the base, **0 shared** (logs/merge_tree_end.log).

## Q7. Kam's ks1346 rule
Every changed log line now logs `reason`, which is either the same expression as before (`String(error)`, or for retention `err.message` / `String(err)`) or the constant `unreadable thrown value`. There is no new key and no new value. Probe flags at head across all error lines: actor email false, signatory id false, verifier id false. Unreadable cells carry only the constant. A thrown non-Error object still logs as `[object Object]`: no values, unchanged. **Compliant.** Pre-existing items are in G104-F6.

## Notes for the PR body
1. G104-F1 (recommended): qualify the retention statement. It holds for `runEnforcement`. The sweep's own catches (`gdprService.ts:499/:503`) still stop the sweep on an unreadable value and skip the later policies' deletions at base and head. Name this as the follow-up KS-1868 site with the fix above.
2. G104-F3 (info): add `signatories.ts:126` and `thirdPartyVerifiers.ts:103` (`error.code`) to the candidates beside :132/:109/:199.
3. G104-F2 (info): revoke, reinstate and suspend can answer 500 after the status has changed, for any thrown value. This is pre-existing.
4. Tier-1 statement confirmed by gate 104 through the real routes with stateful persistence, in all three failure positions.

## NOT TESTED
- The real PR body (no gh auth); a real PostgreSQL or Prisma; a real boot of originate (the `unhandledRejection` handler was read, not run); the gateway hop; Node 24; the four platform suites; CI; the pre-push hook legs (quoted).
- Whether an unreadable thrown value can occur at any of these sites in reality. The values here are synthetic; Prisma rejects with Error subclasses.
- Real Postgres transaction semantics. The `applied` mode is a model of a write followed by a rejection.
- The Linear ticket text.
