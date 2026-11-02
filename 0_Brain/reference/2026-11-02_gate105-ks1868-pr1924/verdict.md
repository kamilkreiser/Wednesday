# QA Gate 105 verdict: Secuura/Distributed_Secuura PR 1924 (KS-1868, originate certifications.ts: O69-P1 list/lineage/evidence-bundle, O69-P2 revoke/verify/share, O69-P3 recertify; 7 hunks, +49/-7 product), TIER 1

## BLUF
**GO WITH NOTES. Nothing has to be fixed before merge.** I ran the real `certificationsRouter` on a loopback listener with the REAL `certificationRepo` and the REAL `chargeEvents` (scripts/probe.test.ts). Only `../db` is replaced, by a STATEFUL stand-in that classifies each SQL statement and applies it to in-memory `documents`, `certification_events`, `share_records` and `charge_events` tables. Auth, logger, notifications, events and documentRepo are also replaced. The repo and charge functions are wrapped so that a fault can be injected RAW at the repo boundary, either BEFORE the real call or AFTER it has applied its writes. Further faults come from a db statement (pre or post), from `logger.info` throwing after its line, from a notification throwing synchronously, and from the anchoring fetch rejecting. Anchoring is a real second loopback server. 179 cells were run at base fcfa5dfd and at head, with 4 values (ordinary Error, string, revoked Proxy, Error with a throwing `message` getter).
- **A (revoke, recertify/issuance, share).** In every failure position, an unreadable value at head gives exactly the ordinary-Error outcome: the route's constant 500, the same SQL statements, the same anchoring and notification calls, and the SAME persisted state.
  - Revoke: before the write, the certificate stays `certified`. After the document INSERT (or the event INSERT, the save, or the notification), it is `revoked`, for an ordinary Error too.
  - Recertify: before the save, no verification certificate exists. After the save, the certificate exists (and the charge is recorded after createChargeEvent), for an ordinary Error too.
  - Share: the shares written before the failure persist, for an ordinary Error too.
  - **Nothing is newly issued, revoked, shared or charged by the change.** At base the same cells got NO ANSWER, with the same persisted state. Mechanical judge: **3161 OK, 0 DIFF**. A planted copy gives 5 DIFF, so the instrument fires.
- **B (evidence-bundle, lineage, verify).** Success bodies (normalised for generated ids and timestamps) and the Content-Disposition header are identical at base and head. Every failing cell's body is the route's constant 500 body, with no certification, holder, share or charge field in it. Nothing new is disclosed.
- **C (ks1346).** The changed log lines carry `reason` only: the same expression as before, or the constant. In all 86 unreadable cells the route's error line holds no holder id, certificate data, recipient email, note or revocation reason (judge flags). See G105-F7 for pre-existing items.
- **D (order).** All 3 `patch.diff` sha256 match the V15 brief (ee6bc738..., c91f61e7..., 0317440f...), and section_1+section_2 == patch.diff (3/3). A strict sequential apply P1 -> P2 -> P3 at base fcfa5dfd (`--check` rc 0 for each section) gives a service tree **identical to PR head**, while the control against base differs. P2 applies at offset +6 and P3 at +24, both with exact context and no fuzz.
- **E.** `:70` (initRepo), `:407` (issuance errMsg) and `:879` (issue-route msg) are byte-identical at base and head. They are listed as follow-ups, together with further sites that the author did not list (G105-F5).
- **One RECOMMENDED item (G105-F1):** the guard form leaves a sub-class of unreadable values unanswered, at base and head alike. This same file already fixed that sub-class at `:1096` (KS-1844, gate 36 F1). The fix is one token per site and was measured.

## Heads
- START (logs/head_start.log, 03:40:15Z): PR head `c4159470a859ed9cf0cb7ffc8f1004e4cac9b8e7` (matches the brief). develop was already `968f17070208` (past 86e12156). merge-base `fcfa5dfdba9b`. One commit by Kam Kreiser <kamil.kreiser@secuura.ai>, "Refs KS-1868: originate certification route catches guard an unreadable throw".
- END (logs/head_end.log, 04:02:19Z): PR head and develop are both UNCHANGED. The working tree is clean. The product file was sha256-restored after every swap (RESTORE_OK each time, and the final sha equals `pr1924:` 0c8ac40a...).
- Diffstat (logs/diffstat.log), three-dot: **6 files, +474/-7**: certifications.ts +49/-7, 3 new tests (+125/+127/+129) and 1 fragment pair (+22/+22). Nothing is outside the declared paths. This matches the READY mail.
- **PR body not read** (no Secuura gh login here). I used the author's READY and BUILT AND PROVEN mails (evidence/) and the committed fragments.

## FINDINGS
- **G105-F1 (RECOMMENDED; pre-existing, base == head; measured).** The new guard is `reason = error instanceof Error ? error.message : String(error)`. It does not coerce `message`. For an Error whose `message` getter RETURNS a hostile non-string, `reason` is that object, and the REAL winston logger's KS-1348 `redactLogValue` then throws inside `logger.error`, outside the try. Two such values were measured: a getter returning a revoked Proxy, and a getter returning an object whose `toJSON` throws. The request gets **NO ANSWER**.
  - probe2 (the real logger, 9 sites x 6 values, logs/show2_*.log): 18/18 hostile-message cells give NO ANSWER at base AND at head, with the same persisted state. For example, revoke after the save leaves the certificate `revoked` with no answer, and recertify after the save leaves a certificate issued with no answer. The ordinary Error, string, revoked Proxy and throwing getter behave as in the main probe.
  - It is not newly produced, so it is not FIX-BEFORE-MERGE. But it is in the class this PR claims to close, and this same file's KS-1844 catch (`:1094-1096`) already records the exact defect and uses the coercing form.
  - **Fix (7 sites, 1012/1177/1249/1354/1521/1615/1729):** `reason = String(error instanceof Error ? error.message : error);`
  - Measured (scripts/fixcheck.sh): 18/18 cells then answer the constant 500 with unchanged persisted state, logging `unreadable thrown value` (revoked-Proxy message) or `[object Object]` (toJSON object). The PR's 28 cells stay 28/28 green. The product file was restored by sha256.
  - If it is not fixed here, the PR body should qualify "an unreadable value now gets the ordinary-Error answer" and name this sub-class.
- **G105-F2 (RECOMMENDED follow-up; pre-existing, base == head; measured).** In recertify, the anchoring inner catch `:1445` logs `{ error: err?.message }` unguarded.
  - An ORDINARY anchoring-fetch rejection is swallowed: the route continues and **issues** the verification certificate with `anchoringStatus: failed` (201, outside production).
  - An unreadable rejection throws inside that catch, and the outer (PR) catch answers 500 with **no certificate issued and no charge**.
  - So the outcomes differ, but in the conservative direction, and identically at base and head. Fix (follow-up): guard `:1445` the same way.
- **G105-F3 (INFO, measured).** Through the real repository layer, a driver-level unreadable rejection never reaches these route catches raw. `getCertification`, `listCertifications`, `saveCertification`, `saveShare`, `getSharesByCertification` (`err?.message?.includes(...)`) and `createChargeEvent` / `getChargeEventsByCertification` (`err?.message`) each throw a readable TypeError (or the getter's Error) from their own catch. The route then logs that text, at base and head alike ("db ... pre/post" cells: 500 at both).
  - Those repo catches skip their own `DB read failed` / `Failed to persist ...` line for such a value. That is pre-existing, and not this PR.
  - Raw unreadable values reach the PR's catches only from the repo boundary, a synchronous notification throw, or a `logger.info` throw (`Charge event created`, `Certification shared`, `Verification certificate issued`). All of these were exercised.
- **G105-F4 (INFO, pre-existing, base == head).** Several routes write and then answer 500. This holds for any thrown value, so the caller is told the action failed when part of it took effect:
  - revoke after the save: `revoked`, 500;
  - recertify after the save: verification certificate issued (plus the charge, after createChargeEvent), 500;
  - share: earlier shares persisted, with no `share` charge when createChargeEvent fails, 500;
  - verify / evidence-bundle after createChargeEvent: charge recorded, 500.
  The author disclosed the charge case; the revoke, issuance and share cases are added here.
- **G105-F5 (INFO, follow-up candidates, read).** These same-shape unguarded reads remain in certifications.ts at head:
  - the three the author listed: `:70` (initRepo), `:407` (errMsg, issuance holder check), `:879` (msg, plus `:886` `error.stack`);
  - ones the author did not list: issue-route inner catches `:585` (reserveErr), `:659` (delErr), `:751` (saveErr), `:787` (updateErr), `:820` (chargeErr), and recertify `:1445` (G105-F2);
  - in neighbouring files: certificationRepo.ts catches (`getCertification`, `listCertifications`, `saveCertification`, `saveShare`, `getSharesByCertification`) and chargeEvents.ts `err?.message`.
- **G105-F6 (INFO, mutant tooling).** M3 (the catch rethrows) makes each test FILE fail to run, because jest-circus `formatNodeAssertErrors` calls `Array.isArray` on the revoked Proxy. So M3 is red at all 7 sites, but **not by assertion**. This is the same as G104-F5.
- **G105-F7 (INFO, ks1346-adjacent, pre-existing).** An ordinary Error's message is logged verbatim: a planted `SECRETVAL` appears at base and head alike. `Certification shared` logs `recipientEmail`, which the real logger redacts (KS-1348 key ending `email`). Revoke's `reason` is not logged. All unchanged.
- **G105-F8 (INFO).** docs-fragments `check` prints the cheat ADVISORY at :6235. It is the same advisory as G104-F7, and it is on develop.
- No FIX-BEFORE-MERGE item.

## Q2. The hunks
There are 7 identical hunks (logs/product_diff.log). In each one, `logger.error('<ctx>', { error: error instanceof Error ? error.message : String(error) })` becomes `let reason: string; try { reason = <same expression>; } catch { reason = 'unreadable thrown value'; }` followed by `logger.error('<ctx>', { error: reason })`. The contexts are list, revoke, verify, share, "Failed to issue verification certificate", lineage and evidence bundle. The `res.status(500).json(<constant>)` lines are untouched, and nothing else in the try bodies changes.

## Q3. Behaviour, measured (logs/probe_{base,head}.jsonl, show_*.log, probe_table.log)
| route: failure position | ordinary Error (base = head) | unreadable, base | unreadable, head |
|---|---|---|---|
| list: repo / db SELECT | 500 constant | NO ANSWER (repo) / 500 TypeError text (db) | 500 constant, same |
| revoke: get, save pre, doc INSERT pre | 500, **certified** | NO ANSWER / 500, certified | 500, **certified** |
| revoke: doc INSERT post, event INSERT post, save post, notify throws | 500, **revoked** | NO ANSWER / 500, revoked | 500, **revoked** |
| verify: get, charge pre | 500, no charge | NO ANSWER, no charge | 500, no charge |
| verify: charge INSERT post, charge post, log "Charge event created" | 500, charge recorded | NO ANSWER, recorded | 500, recorded |
| share: get, saveShare#1 pre | 500, 0 new shares | NO ANSWER | 500, 0 new |
| share: saveShare#1 post, #2 pre, notify#1, log#1 | 500, 1 new share | NO ANSWER, 1 | 500, 1 |
| share: charge pre / post / log | 500, 2 shares, no charge / charge | NO ANSWER, same | 500, same |
| recertify: get, save pre | 500, **no new certificate** | NO ANSWER, none | 500, **none** |
| recertify: doc INSERT post, save post, charge pre | 500, certificate issued | NO ANSWER / 500, issued | 500, issued |
| recertify: charge post, log charge, log "Verification certificate issued" | 500, issued + charge | NO ANSWER, same | 500, same |
| recertify: anchoring fetch rejects | **201, issued** (anchoring failed) | 500, none | 500, none (G105-F2, base == head) |
| lineage: get, shares, charges read | 500 | NO ANSWER | 500 |
| lineage: events SELECT | 200 (swallowed by getLineageEvents) | 200 | 200 |
| bundle: get, shares, charges read, charge pre | 500, no charge | NO ANSWER | 500 |
| bundle: charge post / log | 500, evidence_export charge recorded | NO ANSWER, recorded | 500, recorded |

Totals: base gives NO ANSWER in 68 cells and head in 0. Those 68 head cells log exactly one route line with `unreadable thrown value`. The other 18 unreadable cells come through the real repo's own catch, carry readable TypeError or getter text, and are base == head.

Judge (scripts/table.py), for every head unreadable cell compared with the head ordinary-Error cell:
- status, body, persisted state, SQL sequence, anchoring calls, notifications and Content-Disposition are equal;
- the route error-line count is equal, and the reason is the constant or readable text;
- the base persisted state equals the head persisted state.

For every ordinary, string and success cell, every field including all log lines is equal at base and head. Result: **3161 OK, 0 DIFF**. The planted control (logs/probe_table_planted.log) gives 5 DIFF, rc 0.

## Q4. Re-measure (Node v26.8.1; NOT measured on Node 24)
- **Red-first** (logs/red_base.json): the 3 new files with the base product give 14 failed / 14 passed of 28 (6/12, 6/12, 2/4). Every failed cell is a RED R1/R2 cell and fails by `expect(`. Every control passed.
- **Green:** head 28/28.
- **Suite:** base without the new files **169 files, 2035/2035**; head **172 files, 2063/2063**. 28 new, 0 vanished, 0 passed -> not passed. This equals the author's figures.
- **tsc:** the plain config gives rc 0. With the tests in the program (scripts/tsconfig.tests.json): base 260 files, 0 errors; head 263 files, 0 errors. A planted TS2322 gives rc 2 and is reported, then quarantined.
- **eslint** (4 changed .ts files): 0 problems, rc 0. A planted file gives `no-debugger` and `no-unused-vars`, rc 1.
- **docs-fragments:** rc 0, "75 new ... OK". A planted unbalanced `<div>` in the PR's cheat fragment gives rc 1, "tags are not balanced"; the fragment was restored by sha256.
- Quoted, not re-run: the pre-push hook (PREFLIGHT INCOMPLETE 13/16, legs 3, 4 and 8 skipped).

## Q5. Mutants (scripts/mutants.py; 7 sites x 9; product only, tests untouched, restore True 63/63; logs/mutants_run.log)
- M0, M1, M2, M4, M6, M7, M8 and M9 are **KILLED at all 7 sites by assertion** (1 to 4 cells each).
- M3 is red by suite crash (G105-F6).
- **0 survivors.**

## Q6. merge-tree (develop 968f1707 = start = end)
rc 0, tree `cbfbdd81`. The result changes exactly the PR's 6 paths (SAME_PATHS). Develop has changed 24 paths since the merge-base, **0 of them shared** with the PR.

## Q7. Kam's ks1346 rule
**Compliant.** Each changed line logs `reason`: the pre-existing expression or the constant. There is no new key and no new value. Pre-existing items are in G105-F7.

## Notes for the PR body
1. G105-F1 (recommended): either adopt `String(error instanceof Error ? error.message : error)` at the 7 sites, as `:1096` already does (measured to close 18/18 hostile-message cells), or qualify the tier-1 statement: "an Error whose message getter returns a non-string still gets no answer, as before".
2. G105-F2 (recommended follow-up): recertify `:1445` anchoring catch.
3. G105-F4 / F5 (info): write-then-500 cases (revoke, issuance, share); the extra follow-up sites :585/:659/:751/:787/:820/:1445 and the repo catches.
4. The tier-1 statement is confirmed by gate 105 through the real routes, the real repository and charge layers, and stateful persistence, before and after every write.

## NOT TESTED
- The real PR body (no gh auth); real PostgreSQL / Prisma and transaction semantics (the "post" positions model a write followed by a rejection); a real originate boot; the gateway hop; Node 24; the four platform suites; CI; the pre-push legs (quoted).
- NODE_ENV=production for recertify (where an anchoring failure gives 503).
- Whether an unreadable value can occur at these sites in reality (all values are synthetic).
- Reverse apply order (the hunks are disjoint; not run). The Linear ticket text.
