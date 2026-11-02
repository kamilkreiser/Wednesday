# QA Gate 107 verdict (DELTA, TIER 1): Secuura/Distributed_Secuura PR 1924 (KS-1868, originate certifications.ts), the delta c4159470 -> 33417352 that takes G105-F1

## BLUF
**GATE 107 (DELTA, TIER 1) on PR 1924 at 33417352aa6b: GO WITH NOTES. Nothing has to be fixed before merge.**

The delta is exactly the 7-token change that gate 105 measured as the G105-F1 fix. It closes G105-F1. With the REAL winston logger, an Error whose `message` getter returns a revoked Proxy, or an object whose `toJSON` throws, now gets the route's constant 500. Before the change it got NO ANSWER. The persisted state is the same as for an ordinary Error, and the same as gate 105 measured.

I also probed the shape the author did not add: a `message` that returns an object whose `toString` throws. Three related shapes went with it: a throwing `Symbol.toPrimitive`, a null-prototype object and a Symbol. `String()` does throw for the first three, but it throws INSIDE the guard's `try`, so the catch logs the constant `unreadable thrown value` and answers the ordinary 500. That is not a finding.

The notes below are INFO only. Gate 105's G105-F2 to F8 stand unchanged.

## Heads
- START (logs/head_start.log, 04:48:32Z) and END (logs/head_end.log, 04:59:33Z) are identical:
  - PR head `33417352aa6ba6a93d122722a9253d0504ecbcab`
  - develop `cd9c4a7dd3b87f4810d16b40352a63330d1d6793`
- Parents (logs/commit.log): `rev-list --parents` gives exactly one parent, `c4159470a859ed9cf0cb7ffc8f1004e4cac9b8e7`, and `rev-list --count c4159470..33417352` = 1.
- Commit: author Kam Kreiser <kamil.kreiser@secuura.ai>, subject "Refs KS-1868: originate certification catches coerce a non-string error message".
- Not merged up: merge-base(PR, develop) = `fcfa5dfdba9b`, the same base as gate 105.
  - develop is 4 commits and **31 paths** past it (logs/develop_paths.log).
  - **0 of those paths are shared** with the PR's 6 (logs/shared_paths.log).
  - `git merge-tree --write-tree develop PR` gives rc 0, tree `09a60fbc`, and the result changes exactly the PR's 6 paths (SAME_PATHS; logs/mergetree.log, mt_paths.log).
- Clone: a copy of gate 105's clone (push URL `no_push_qa_gate`, read-only use), fetched to the new head. The working tree was clean at END, and the product sha256 at END is `18e43169e1b2fba8...` (= the PR head).
- **PR body not read:** there is no Secuura gh login on this host (`gh auth status` with Wednesday's GH_CONFIG_DIR: not logged in). I used the author's READY mail (evidence/v15_ready_for_delta_check.txt).

## Check 1. Product diff c4159470..33417352 (logs/product_delta.diff, delta_numstat.log)
- FOUND: `certifications.ts` is **7 added / 7 removed**. Each pair is exactly
  `-        reason = error instanceof Error ? error.message : String(error);`
  `+        reason = String(error instanceof Error ? error.message : error);`
  - The lines are 1012 (list), 1177 (revoke), 1249 (verify), 1354 (share), 1521 (recertify), 1615 (lineage) and 1729 (evidence bundle). These are gate 105's seven lines.
  - Nothing else in any product file changed, and the mode is 100644 -> 100644 for all 6 paths (`git diff --raw`).
- The other changed paths:
  - the three PR test files: +49, +93 and +100, additions only;
  - the two docs fragments: 6/6 each, consisting of figures plus one "What this does not prove" sentence (logs/frag_delta.diff, read whole).
- The three-dot diff from base is 6 files, +716/-7, as the mail says.
- HOW: `git diff -U0` and `--raw`, read.

## Check 2. Red/green and mutants (scripts/cells.sh, cells.py; logs/cells_*.json/.txt)
- **At 33417352: 55/55 green** (logs/cells_head.txt).
- **With the c4159470 product** (taken from git, the tests at the new head): 37 passed, **18 failed**. The failures are exactly the R3, R4, R5 and R6 cells (7+7+2+2).
  - **All 18 are by assertion.** Each carries an `expect(received).toEqual` mismatch with `status: 'NO ANSWER'` against 500 (logs/cells_c415_failmsgs.txt, 18/18). Jest also attributes the logger's own throw to the cell as its first message (`getPrototypeOf on a proxy that has been revoked` / `ks1868 toJSON threw`); this is the real G105-F1 failure, not a harness crash.
  - 0 suites failed to run.
  - The 9 new controls (C3 x7, C4 x2) pass.
  - **The 28 original cells (R1, R2, C1, C2) pass at both products.**
- Count: 27 new cells (R3, R4, C3 x 7 routes, plus R5, R6, C4 x revoke and recertify). This matches the author's figure.
- **Mutants** (one of the 7 changes undone, placement asserted, product only, tests untouched, sha256-restored, RESTORE_OK each time):

  | mutant | product sha | result |
  |---|---|---|
  | line 1177 (revoke) | 7ca751a9 | 4 red, exactly revoke R3/R4/R5/R6, all by assertion |
  | line 1521 (recertify) | 76f1545f | 4 red, exactly recertify R3/R4/R5/R6, all by assertion |
  | line 1012 (list) | 0b9ea66e | 2 red, exactly list R3/R4, all by assertion |

  No other cell went red. 0 survivors.
- NOT run: mutants at 1249, 1354, 1615 and 1729 (the author reports 7/7). Mutant forms other than "undo" were not run either; gate 105 ran 9 forms x 7 sites on the guard.

## Check 3. Does the fix close G105-F1, with the REAL logger? (scripts/probe3.test.ts, probe.sh, judge.py; logs/probe3_{c415,head}.jsonl, show3_*.log, judge3*.log)
- HOW: this is gate 105's probe2, unchanged except for added values.
  - The real `certificationsRouter`, the REAL `certificationRepo` and `chargeEvents`, and the **real winston logger** run (only wrapped to record each call, then call the original).
  - `../db` is replaced by a stateful in-memory stand-in, and auth, notifications, events and documentRepo are stubbed.
  - Faults are injected raw at the repo boundary, pre or post the real write.
  - The probe covers 9 failure positions over 7 routes x 12 values = 108 cells, run against the c4159470 product and against the 33417352 product.
- Values: ord (an ordinary Error), str, rp (a revoked Proxy), tg (a throwing getter), **msgproxy** (the getter returns a revoked Proxy) and **msgobj** (the getter returns an object whose toJSON throws). Gate 107 added:
  - **msgtostr** (the getter returns an object whose toString throws);
  - **msgprim** (Symbol.toPrimitive throws);
  - **msgnull** (`Object.create(null)`);
  - **msgsym** (a Symbol);
  - **objtostr** (a thrown non-Error whose toString throws);
  - **nullproto** (a thrown null-prototype object).
- At c4159470: 18 cells fail, the 18 msgproxy/msgobj cells at 9 positions, each with **NO ANSWER** (G105-F1 reproduced).
  - msgtostr, msgprim and msgnull answered 500 there, but logged a NON-string reason (`{}`). msgsym logged an undefined reason.
- **At 33417352: 108/108 answer.**
  - msgproxy, msgtostr, msgprim, msgnull, objtostr, nullproto, rp and tg log `unreadable thrown value`; msgobj logs `[object Object]`; msgsym logs `Symbol(g107sym)`.
  - Every route error line now carries exactly one string reason.
- **toString-throws question:** `String()` does throw for msgtostr, msgprim and msgnull (and for objtostr and nullproto via `String(error)`). The throw happens inside the guard's `try { reason = String(...) }`, so it is caught and becomes the constant.
  - It does not escape the catch, so it is not a finding.
  - The ordinary-Error path is unaffected: `String()` of a string message is the identity, and the ord cells log the same message at both products.
- Judge (head, every cell against the same position's ordinary-Error cell): status, body, persisted state, SQL sequence, anchoring calls, notifications, Content-Disposition and fired are equal, plus one string reason, plus the head state equals the c4159470 state. Result: **1080 OK, 0 DIFF** (logs/judge3.log).
  - Planted control (logs/judge3_planted.log): 2 planted defects give 3 DIFF, rc 1.
  - c4159470 self-judge (logs/judge3_c415self.log): 90 DIFF, so the instrument fires on the old product.

## Check 4. Stored state (scripts/vs105.py; logs/vs105_*.log)
- Revoke after the save: `revoked` for an ordinary Error and for every hostile value. Recertify after the save: the verification certificate is stored for ordinary and hostile values alike, and after createChargeEvent the charge is recorded for both. Share after saveShare#1: 1 new share. Verify and bundle after the charge: the charge is recorded.
- In every case this is identical to the ordinary-Error control (Check 3 judge).
- Against gate 105's own recordings, over the 54 common cells (6 shared values x 9 positions), comparing status, body, state, SQL, anchoring and notifications:
  - my 33417352 run vs gate 105's measured fix (probe2_fix): **324 OK, 0 DIFF**;
  - my c4159470 run vs gate 105's head (probe2_head): **324 OK, 0 DIFF**;
  - my 33417352 run vs gate 105's head: 36 DIFF, all `status` and `body` of the 18 msgproxy/msgobj cells (NO ANSWER -> constant 500). The persisted state did not differ.
- **Nothing is newly issued, revoked, shared or charged** compared with gate 105's measurements.
- The author's own R5/R6/C4 after-the-write cells (revoke `revoked`, recertify `verification_certificate`) pass at the head and are red by assertion at c4159470 (Check 2).

## Check 5. Ratios (Node v26.8.1; NOT measured on Node 24)
- **Whole originate suite at 33417352** (logs/whole_head.json): **172 suites, 2090/2090 passed**, 0 failed, 0 pending, rc 0. Gate 105's head was 172 suites / 2063, so this is +27, which equals the new cells.
- **tsc:**
  - With the tests in the program (scripts/tsconfig.tests.json): rc 0, 263 src files (logs/tsc_files.log, tsc_tests.log).
  - Plain config: rc 0. The first plain run hit rc 2 TS6053 because my own eslint planted file was transiently present; I re-ran it clean after the file was quarantined.
  - A planted TS2322 test file gives rc 2 and is reported (logs/tsc_planted.log), then quarantined.
- **eslint** (certifications.ts plus the 3 test files): rc 0, 0 problems (logs/eslint.log). The planted file gives rc 1, with `no-debugger` and `no-unused-vars`.
- **docs-fragments check:** rc 0, "flow 117 legacy + 75 new, cheat 112 legacy + 75 new ... OK" (logs/frag_head.log), with the same :6235 cheat ADVISORY as G105-F8. A planted unbalanced `<div>` in the PR's cheat fragment gives rc 1, "tags are not balanced" (logs/frag_planted.log). The fragment was restored by sha256 (RESTORE_OK).
- Not run: the pre-push hook (quoted by the author: PREFLIGHT INCOMPLETE 13/16), and the author's 58-of-58 base-vs-head recordings.

## Check 6. PR body
- **UNMEASURED:** the live body could not be read here (no gh auth).
  - The author's READY mail (section 6) claims that "## Gate 105 notes" carries F1 TAKEN with measurements, and that 0 occurrences remain of "14 of 28" or "2063 of 2063".
- Measured instead on the committed fragments at 33417352 (logs/frag_stale.log):
  - "14 of 28" 0, "14 passed" 0, "2063" 0, " 28 cells" 0, "28 / 0" 0;
  - positive controls: "55 cells" 2 and "2090" 4.
- Wednesday should eyeball the live body, or have a seat with Secuura gh auth do it.

## FINDINGS
- **G107-F1 (INFO, measured).** A shape the author did not add, a `message` getter returning an object whose toString throws (and Symbol.toPrimitive throwing, a null-prototype object, a Symbol), is handled. `String()` throws inside the guard's try and the catch logs the constant; the route answers the ordinary 500 with the ordinary persisted state (Check 3, 1080 OK / 0 DIFF). There is no throw inside the catch, and the ordinary-Error path is unchanged. Optional: add a msgtostr cell to lock this in. It is not required.
- **G107-F2 (INFO, log-content change, measured).** For an Error whose `message` is a readable NON-string, the logged reason changes:
  - At c4159470, the raw object went to the logger (logged as `{}` after redaction) or `undefined` for a Symbol, and the request still got 500.
  - At 33417352 it is coerced: `[object Object]`, `Symbol(...)`, or the constant if coercion throws.
  - So the fragments' "Readable values behave exactly as before" holds for the response and the persisted state, not byte-for-byte for the log text of non-string messages. This is more conservative under Kam's ks1346 rule (no object values reach the log).
- **G107-F3 (INFO, docs wording).** The fragments' "What to know" paragraph still names only "a revoked Proxy, an Error whose message getter throws". It does not mention that a getter returning a hostile non-string is now coerced. The figures and the "does not prove" sentence are updated correctly. Optional.
- **Carried from gate 105, unchanged by this delta (not re-measured except state):** G105-F2 (recertify `:1445` anchoring catch, recommended follow-up), F3, F4 (write-then-500), F5 (follow-up sites), F6, F7 and F8.
- **No FIX-BEFORE-MERGE item.**

## UNMEASURED / NOT TESTED
- The live PR body (Check 6) and the Linear ticket.
- Node 24, a real PostgreSQL / Prisma, a real originate boot, the gateway hop, the four platform suites, CI, and the pre-push legs.
- Mutants at 4 of the 7 lines (1249, 1354, 1615, 1729) and non-"undo" mutant forms in this delta.
- NODE_ENV=production for recertify.
- Whether any of these hostile values occur in reality (all values are synthetic).
- The probe's stateful db stand-in models "post" as write-then-reject, not real transaction semantics.
