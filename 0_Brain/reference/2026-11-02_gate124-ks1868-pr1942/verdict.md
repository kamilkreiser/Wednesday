# QA Gate 124 verdict: Secuura/Distributed_Secuura PR 1942 (KS-1868, originate certifications.ts issue + recertify catches; held Spark passes O79-A1..A5, 8 hunks), TIER 1 (the certificate ISSUE and CHARGE path)

## BLUF
**GO WITH NOTES (TIER 1). Nothing has to be fixed before merge.**

I ran the real `certificationsRouter` on a loopback listener (scripts/probe.test.ts). The parts that are real: `certificationRepo` (reserveCertificationRow, saveCertification, deleteCertification, getCertification), `chargeEvents`, and the winston logger. The logger's formats ran, and each transport's `log()` was captured instead of written.

Only these were replaced: `../db`, the lineage `documentRepo`, auth, notifications, events and the provenance writers. The `../db` stand-in is stateful. It applies the reservation and authoritative INSERTs, the ISSUE event, charge_events, the legacy UPDATE, the compensating DELETE and the holder SELECT to in-memory tables.

Faults were injected RAW in three ways:
- at a db statement, either before it applies or after it has applied;
- at a repo boundary;
- as the anchoring-fetch rejection.

145 cells ran at base e2a2426d and at head: 20 failure positions over all 8 sites (development and PRODUCTION), 7 thrown values, and 5 controls. Results are in logs/probe_{base,head}.jsonl, logs/probe_table.log and logs/probe_checks.log.

**Q2, money and issuance (the headline).** At every site, an unreadable value at head gets exactly what an ordinary Error gets. The judge (scripts/table.py) compares status, body, persisted state (certification rows, ISSUE events, charge_events, derived document, legacy row status), SQL sequence, anchoring calls and deletes:
- **141 OK, 0 DIFF, 4 PRE-EXISTING** (base == head, G124-F4).
- A planted change of one head cell's state gives DIFF=1, so the instrument fires.
- At head: 0 escaped handlers, 0 unhandled rejections, 0 cells reaching the outer catch. At base, 76 cells ended in the outer catch's 500 "Failed to issue certification" / "Failed to issue verification certificate".

**Does head newly CHARGE, ISSUE or DELETE anything an ordinary Error path would not? No.** Against BASE it does all three for this value class, and in each case it reaches the ordinary-Error outcome:
- **Newly issues and charges vs base:** the reservation, anchoring (development) and recertify-anchoring catches. Base answered 500 and the request went no further. Head issues the certificate with its 2 charge events (recertify: 1).
- **Newly charges vs base:** the lineage-save and legacy-UPDATE catches. Base had already saved the certification row and its ISSUE event, then answered 500 with 0 charge events. Head answers 201 with 2.
- **Newly deletes vs base:** the PRODUCTION anchoring catch. Base answered 500 and left the reservation row; head answers 503 and the compensating delete removes it.
- **Response only (no state change):** the charge catch (base 500 after issue, head 201, same charge rows), the holder check (500 -> the generic 400) and the compensating-delete catch (500 -> 503).

The author's measured consequences all re-measure, with one correction (G124-F1).

**Q1, held-patch identity: 0 byte differences.**
- All 5 `patch.diff` sha256 values equal the brief.
- Each patch is contained in its held READY file (`in` True 5/5; a planted one-byte change is not contained).
- section_1+section_2 equals patch.diff 5/5.
- Strict apply at e2a2426d, forward (A1..A5) and reverse (A5..A1): every `--check` rc 0, offsets only, no fuzz. Both orders give the same tree `92465ae9`.
- The product and all 5 test blobs are **byte-equal to PR head**. Only the two author-written fragments are not in the passes.

**Q3, the A1/A2 thrown-string log change.** Measured: in 10 of the 65 readable or control cells the log changed from base to head, and **all 10 are the two anchoring catches**. Base logged `error: undefined`; head logs `String(value)`. That gives:
- a thrown string: the string;
- a thrown plain object: `"[object Object]"`, with no field names or values.

At the other 6 sites a thrown string and an object already logged identically at base. I judge this **inside both Kam cards** (§7).

**Q4.**
- **Red-first:** 27/43, every failure by `expect(`, all 16 controls pass.
- **Green:** 43/43.
- **Originate suite:** 2163/2163 (180 files) -> 2206/2206 (185 files); 43 new, 0 vanished, 0 passed->not.
- **tsc with tests:** 0 errors at base (208 test files) and head (213). A planted TS2322 is reported.
- **eslint:** 0/0 on 6 files; a planted file gives 1 error + 1 warning.
- **docs-fragments:** rc 0. A planted `<div>` gives rc 1, restored by sha.
- **Mutants: 57/57 killed, all by assertion, each only in its own site's test file.**
- **merge-tree:** clean onto 58b5042c AND onto develop as it moved to fbacb63a during the gate, which merged PRs 1940/1941. 0 shared paths, union order-independent.

## Heads
- **START** (logs/head_start.log, 2026-11-02T11:12:57Z):
  - PR 1942 `966909efd5f7c754f58409f09b7b53359116f3da` (equals the commission); develop `58b5042ccdb5a06a213ba53f5d4f7644f5f52549` (equals the commission); merge-base/parent `e2a2426d221d`.
  - PR 1941 `33644960`, PR 1940 `96208f37`.
  - 1 commit, Kam Kreiser <kamil.kreiser@secuura.ai>, "Refs KS-1868: certificate issue and recertify catches read a thrown value safely".
- **END** (logs/head_end.log, 11:31:49Z; re-read at the end of logs/merge_tree_dev2.log):
  - **PR 1942 UNCHANGED `966909ef`.**
  - Develop MOVED to `fbacb63af446ecbb81a7a08de8c236a34c8b20f4`: `3e688ee2` (KS-1939 = PR 1940) and `fbacb63a` (KS-1868 verification = PR 1941) were merged. See G124-F6.
  - Local HEAD `966909ef`, working tree clean. The product was sha256-restored after every swap: RESTORE_OK for probes and runs, TSCB_RESTORE_OK, `restore True` 57/57 for the mutants.
- **Diffstat, three-dot** (logs/diffstat.log): **8 files, +1176/-8.** That is certifications.ts +55/-8, 5 new tests (173/223/227/225/227) and 1 fragment pair (22/24). Nothing is outside the declared paths. This matches the READY mail.
- **PR body not read** (no Secuura gh login). I used the V 17th READY (evidence/v17_ready_pr1942.txt) and the committed flow fragment.
- Node v26.8.1 only: **no figure was measured on Node 24.**

## FINDINGS
- **G124-F1 (INFO; correction to the fragment/body wording; measured).** The body/fragment says: "anchoring catch on issue, 500 with nothing saved, then 201 (non-production)". Through the real repository, base in NON-production ALSO leaves the reservation row:
  - The pre-anchor `reserveCertificationRow` has already written the `documents` row (status issued, `anchoringStatus: failed`, no anchor) with **no ISSUE event and 0 charges**, and the request answers 500.
  - A client retry after that 500 issues a second certification, leaving the first row orphaned.
  - Head answers 201 and the authoritative save completes that same row. Head is strictly better.
  - The author's harness mocked the reservation as a no-op, which is why it saw "nothing saved". Production is as stated: 500 with the reservation row left, then 503 with it deleted.
  - Fix the wording: "500 with the pre-anchor reservation row left in place (no ISSUE event, no charge) in every environment".
- **G124-F2 (INFO; Q3 / ks1346 judgement; measured).** The A1/A2 delta is exactly as the brief and Wednesday's ruling state:
  - A thrown string: undefined -> the string.
  - A thrown plain object: undefined -> `"[object Object]"`. A planted `{password, token}` puts neither the field names nor the values in any console line, at base or head.
  - An ordinary Error is unchanged.
  - No response body carries thrown text (0 of 145 cells, base and head).
  - I counted 10 changed cells against the author's "8 of 393", because my probe adds a legacy-path issue cell and a production recertify cell. It is the same two lines and the same two value kinds.
  - Reachability: the value comes from `fetch()` to the internal anchoring service. Its real rejections are `TypeError('fetch failed')` and the `AbortSignal.timeout` DOMException, both Errors. A thrown string here needs a non-standard fetch. Read, not run.
- **G124-F3 (INFO; ks1346-adjacent improvement; read, consistent with G123-F4).** At the 6 sites that used `X instanceof Error ? X.message : String(X)`, an Error whose `message` is a readable OBJECT used to hand that object to winston, which printed its field values. Head prints `String(message)`, so `"[object Object]"` or the object's own toString text.
  - This holds for an Error whose message getter RETURNS an object with a throwing toJSON (my `gtj` value): at base it got no ordinary outcome (500 at every site); at head it gets the ordinary outcome, with `"[object Object]"` logged rather than the constant. This is correct: that message is readable by `String()`.
- **G124-F4 (INFO, pre-existing, base == head; measured).** When the `INSERT INTO charge_events` statement itself rejects with an unreadable value, the real `chargeEvents.createChargeEvent` catch (`err?.message`, chargeEvents.ts ~:186) throws a readable TypeError first:
  - Its own "Failed to persist charge event to DB" line is skipped.
  - The route's chargeErr catch logs the TypeError text, not the constant.
  - Outcome: 201, cert issued, 0 charges, at base and head alike.
  - These are the 4 PRE-EXISTING cells. A follow-up KS-1868 site (same class as G105-F3).
- **G124-F5 (RECOMMENDED follow-up; pre-existing, base == head for every value including an ordinary Error; measured).** The case: the reservation INSERT lands and then the call rejects (for example a connection reset after commit), and anchoring is unavailable in PRODUCTION.
  - `provisionalWritten` stays false, so the compensating delete is skipped. `removed` is set to the placeholder `1`, so the "removed no row" alarm also stays silent.
  - The route answers the 503 "nothing was written" while a certification row with no anchor remains, and **no line names it**.
  - This is not this PR (cells "A3 reserve post, PROD + anchor fails", 503 + 1 row, base == head). It belongs with KS-1633's reconciliation.
- **G124-F6 (INFO; develop moved during the gate; measured).** Develop went 58b5042c -> fbacb63a, merging PR 1940 and PR 1941: 12 paths, all in verification.ts / verificationV2.ts, their tests and fragments, **0 shared with PR 1942**.
  - merge-tree onto fbacb63a: rc 0, tree `111d5263`, exactly the PR's 8 paths. That tree equals the union tree I had built earlier from 58b5042c+1940+1941+1942 in both orders.
  - `certifications.ts` is the same blob (`0d2881b4`) at base and at 58b5042c. The forward-move rule is satisfied (no shared path). "Develop NOT merged in" stands.
- **G124-F7 (INFO, ops).** My first tsc/eslint pass overlapped the mutant run, which swaps the product. It was discarded to logs/_quarantine/*_DURING_MUTANTS.log and re-run on a sha-verified clean head (logs/static2_run.log). The figures above are from the re-run.
- **G124-F8 (INFO).** docs-fragments prints the known cheat ADVISORY at :6235, which is on develop (G90-F7 / G123).
- No FIX-BEFORE-MERGE item.

## Q1. Held-patch identity (logs/identity_sha.log, logs/identity.log; scripts/identity.py, scripts/identity.sh)
| pass | patch sha256 (12) | = brief | contained in held READY | sections concat = patch |
|---|---|---|---|---|
| O79-A1 | 6e2c8b6ad3ff | True | True | True (2) |
| O79-A2 | a66f10897fda | True | True | True (2) |
| O79-A3 | 0a4ecc944169 | True | True | True (2) |
| O79-A4 | df0f48219de0 | True | True | True (2) |
| O79-A5 | ac3a5ed70e1e | True | True | True (2) |
- The apply source is the unsuffixed model dir. As the brief says, the `-control` dirs of A2/A3 hold different bytes, and the `-control-r2` dirs are byte-equal.
- Forward offsets: A3 +6, A4 +18, A5 +17. Reverse: A4 +6, A3 +5/+11/+17, A2 +11, A1 +41. There is no fuzz in either order. Both orders give tree `92465ae9`.
- certifications.ts and the 5 tests are SAME as pr1942, blob for blob.
- (The fragments-path comparison in identity.sh broke on the path's space. That is an instrument fault; the fragments are not part of the passes.)

## Q2. The hunks (logs/product_diff.log)
- Each of the 8 hunks wraps the site's read as follows, then logs `error: reason`:
  ```
  let reason: string; try { reason = String(X instanceof Error ? X.message : X); } catch { reason = 'unreadable thrown value'; }
  ```
  The holder site uses `errMsg`, which still feeds the `includes('invalid input syntax'|'uuid')` 400 branches.
- Previous reads:
  - `X instanceof Error ? X.message : String(X)` at holder :407, reserveErr :581, delErr :655, saveErr :747, updateErr :783, chargeErr :816;
  - `err?.message` at issue anchoring :632 and recertify anchoring :1446.
- Unchanged: every message text, level, other key, control-flow statement and response. There is no new log line and no new key.
- This is the coercing form G105-F1 recommended, so a message getter that returns a hostile object is also handled.
- `git grep` confirms the other unguarded reads in the file (outer catches :919/:1052 etc.) are untouched.

## Q2 (the key question). Behaviour, measured (logs/probe_table.log)
The ordinary Error result is the same at base and head. "Unreadable" means a revoked Proxy, a throwing message getter, or a getter returning a revoked Proxy. Rows are certification rows / ISSUE events / charge events.

| site (injection) | ordinary Error, base = head | unreadable, base | unreadable, head |
|---|---|---|---|
| A4 holder SELECT users | 400 "could not validate", nothing written | **500**, nothing written | 400, same |
| A3 reserve INSERT pre | 201, 1 / 1 / 2 | **500**, 0 rows | 201, 1 / 1 / 2 |
| A3 reserve INSERT post (row landed) | 201, 1 / 1 / 2 | **500**, reservation row, 0 events, 0 charges | 201, 1 / 1 / 2 |
| A2 issue anchoring rejects, dev (lineage and legacy) | 201 anchoringStatus failed, 1 / 1 / 2 (+ derived doc / legacy row certified) | **500**, reservation row left, 0 events, 0 charges (G124-F1) | 201, as ordinary |
| A2 issue anchoring rejects, PROD | 503, row compensated (0 rows) | **500**, reservation row LEFT, no delete | **503, row deleted** |
| A5 PROD delete rejects (pre / applied-then-throws) | 503, row remains / removed | **500**, same rows | 503, same rows, error line with constant |
| A3 lineage saveDocument pre / post | 201, 1 / 1 / 2, derived 0 / 1 | **500**, cert + ISSUE saved, **0 charges** | 201, 1 / 1 / 2 |
| A4 legacy UPDATE pre / post | 201, 1 / 1 / 2, legacy draft / certified | **500**, cert + ISSUE saved, **0 charges** | 201, 1 / 1 / 2 |
| A3 charge #1 pre / post, #2 pre / post | 201, charges 0 / 1 / 1 / 2 | **500**, same charges, cert issued | 201, same charges |
| A3 charge db INSERT (through real chargeEvents) | 201, 0 charges | 201 (TypeError text) | 201, same (G124-F4, base == head) |
| A1 recertify anchoring rejects, dev | 201, verification cert + 1 charge | **500**, nothing | 201, cert + 1 charge |
| A1 recertify anchoring rejects, PROD | 503, nothing | **500**, nothing | 503, nothing |

- Controls (lineage, legacy, holderId, recertify, PROD ordinary anchoring fail + delete OK) are base == head.
- At head, readable values (Error, string, plain object) never change status, body or state. Only the A1/A2 log value changes (F2).
- Read vs run. RUN: the router, real repo/charge/logger, the catches, bodies, persisted model state, NODE_ENV=production per cell. READ: real PostgreSQL/RLS/`withTenant` (modelled as pass-through), the gateway, the real anchoring service, multi-tenant pools.

## Q4. Re-measure (Node v26.8.1; NOT on Node 24)
- **Red-first** (logs/red_base.json): 27 failed / 16 passed of 43, all by `expect(`, 0 suite failures, every control passes. Per file: recertify 5/7, issue-anchoring 4/6, delete 3/5, holder+update 6/10, reserve+save+charge 9/15. This equals the author.
- **Green:** 43/43.
- **Whole originate suite:** 180 files 2163/2163 -> 185 files 2206/2206 (logs/whole_{base,head}.log, runs_analysis.log). Load1 10-24.
- **tsc:** plain rc 0. With tests (scripts/tsconfig.tests.json): rc 0 at base (208 test files) and head (213). A planted TS2322 gives rc 2.
- **eslint** (scripts/lint.cjs, cwd = originate): 6 files, 0 errors, 0 warnings. A planted file gives 1 error + 1 warning, rc 1.
- **docs-fragments:** rc 0, "flow 117 legacy + 84 new, cheat 112 legacy + 84 new". A planted `<div>` in the PR's cheat fragment gives rc 1 "tags are not balanced". FRAG_RESTORED, rc 0 after.
- Not re-run: the author's two recorders (393 checks, 6 tampers). My probe stands in their place.

## Q5. Mutants (scripts/mutants.py; product only, all 5 new test files per run, sha256 restore True 57/57; logs/mutants_table.log, mutants_rows.json)
| mutant | A4 holder | A3 reserve | A2 issue anchor | A5 delete | A3 save | A4 update | A3 charge | A1 recertify |
|---|---|---|---|---|---|---|---|---|
| M0 revert the read (unguarded) | K | K | K | K | K | K | K | K |
| M1 drop the inner try | K | K | K | K | K | K | K | K |
| M2 fallback -> 'x' | K | K | K | K | K | K | K | K |
| M3 constant for every value | K | K | K | K | K | K | K | K |
| M4 swallow the wrong value (`String(X)`) | K (C1) | K | K | K | K | K | K | K |
| M5 rethrow in the fallback | K | K | K | K | K | K | K | K |
| M6 fallback -> undefined | K | K | K | K | K | K | K | K |
| M7 holder fallback -> 'uuid' (wrong 400) | K | | | | | | | |

**57/57 killed, every one by assertion** (no suite crash, unlike G105-F6 / G123-F5). Each kill lands only in its own site's test file. 0 survivors.

## Q6. merge-tree (logs/merge_tree.log, logs/merge_tree_dev2.log)
- **Onto 58b5042c:** rc 0, tree `b2d1fd56`, SAME_PATHS (the 8). Develop moved 50 paths since the base, 0 shared (control 50). PR 1940 (5 paths) and PR 1941 (8 paths) share **0 paths** with 1942 (both touch verification*.ts only). The union develop+1940+1941+1942 in both orders is rc 0 with an identical tree `111d5263`.
- **Onto fbacb63a** (develop at end, 1940+1941 merged): rc 0, tree `111d5263`, SAME_PATHS. 0 of the 12 moved paths are shared.

## Q7. Kam's ks1346 rule (card secuura-ks1346-logging-thrown-objects-leaks-secrets = a; card secuura-ks1348-log-files-persist-secrets = a)
- **No new log line, no new key.** 8 existing `error:` values change their source only.
- **Thrown objects (KS-1346: "type and field NAMES, never values"):**
  - head logs a thrown plain object as `"[object Object]"`, with no field names or values (measured, F2);
  - an Error with an object message now logs `String(message)` instead of the object's field values (F3, an improvement);
  - an unreadable value logs the constant.
- **Message text (KS-1348: "Error message text still reaches the files"):**
  - An ordinary Error's message is logged unchanged, as at base.
  - The A1/A2 thrown-string change makes those two lines log the string as message text, the house form already merged in PR 1924 and used by the other 6 sites at base.
  - That is inside KS-1348's option text, and it is not the object-leak class KS-1346 ruled on.
- **Compliant**, and Wednesday's ruling (a) is consistent with both cards' text. Residual (not this PR): an object's own `toString` text would now be logged (G123-F4 class).

## Notes for the PR body
1. G124-F1 (info, wording): the base issue-anchoring outcome is "500 with the pre-anchor reservation row left (no ISSUE event, no charge)" in non-production too, not "nothing saved". Measured through the real certificationRepo.
2. Gate 124 confirms the tier-1 table through the real router, repository, chargeEvents and logger, including PRODUCTION: 141/141 unreadable-or-readable cells equal the ordinary/base outcome. It also confirms head newly issues, charges or deletes nothing that an ordinary Error would not.
3. G124-F2 (info): the A1/A2 delta is confirmed. Note that a non-Error fetch rejection is not produced by standard fetch.
4. G124-F4 / F5 (follow-ups): the `chargeEvents.createChargeEvent` catch (`err?.message`); the reservation-landed-then-rejected PRODUCTION path that answers 503 with a silent leftover row (KS-1633).
5. G124-F6 (info): develop is now fbacb63a (1940 + 1941 merged), 0 shared paths, merge-tree clean.

## NOT TESTED
- The real PR body (no gh auth).
- Real PostgreSQL / Prisma / RLS and `withTenant` transactions (modelled). Multi-tenant `tenantPool`. A real boot, the gateway, the real anchoring service.
- Node 24; the four platform suites; CI; the pre-push hook legs (quoted from the READY mail).
- docs-fragments on the merged tree (needs a worktree; the merged tree equals the predicted union, and the only other fragment pairs are 1940's and 1941's).
- The author's recorders and tampers.
- Whether any value of these shapes occurs in production. All values are synthetic, and I found no caller-controlled path that yields one.

Processes: every background run I started (install, runs.sh, mutants.py, the monitor and the wait loop) has exited. `ps` shows 0 gate-124 processes (logs/ps_end.log). Writes went only under this workdir: nothing in !CODING, no node_modules/.vite in Wednesday's tree, and the two apply worktrees were removed by `git worktree remove`.
