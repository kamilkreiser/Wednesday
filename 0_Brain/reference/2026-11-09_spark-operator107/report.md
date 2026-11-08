# Spark operator 107 report (2026-11-09 03:57-04:20 AEDT). Secuura only.

## BLUF
- 4 HELD passes (the stop limit), all in `packages/shared`, all from tickets filed by gates 176/177 (KS-1971..KS-1974). 3 passed round 1; the 4th (KS-1974) failed round 1 on MY sequencing error (below) and passed its one rebrief. No model output was hand-edited; every golden is BYTE-IDENTICAL.
- Work clones landed on the BOOT volume (`/private/tmp/spark_work_o107`, 5 clones, 1.8 GB), none in `spark/cache/work` (`ls ... | grep -c o107` = 0). DevMASTER free 14 GiB at start and end (never under 10). Load1 3.6-6.8.
- Job 1 (a): no KS ticket numbered 2127 or higher exists (Linear `number gte 2127`, all states: 0 nodes). Pool is therefore (b), the widened screen.
- Pin: develop 2935f723 at start, every round, and end (tip_start/r2/r3/r4/end.out). Open PRs 44 / 295 files at start and end; planted control services/originate = 16 entries both times; none of my 4 product files or 4 new test names is in any open PR (HITS lines in prscan_end.out and the end scan).
- Mistake to own: for KS-1974 I chained `--control` and the queue append in one command without gating on the control, so a model round ran on a brief whose control had FAILED (04:13:28, FAIL at A4: test cell R3, a revoked Proxy as the message, crashes vitest's `toEqual` with a TypeError instead of failing by assertion; the model answered the golden byte for byte, so the FAIL is the brief's, not the model's). That round counts as round 1; the brief was rebuilt without R3 (round 2 of 2), control-passed first, then passed. The first brief dir is in night/_quarantine_2026-11-09/briefs_unused/.

## Held passes (`ls night | grep O107`)
1. `READY_KS-1972-KS-1972-O107-P1_spark-dsv4flash_BRIEFED-CODEPATCH2-EVENT-INDEXER-PASS-7of7_2026-11-09.diff.md`
   hold_ready: `golden: BYTE-IDENTICAL; touched=2 product_plus=9 product_minus=0 red=3/5 green=5/5 suite=1597->1602 strict=True` (hold_KS-1972-O107-P1.out). event-indexer.ts `isRateLimited` guarded (the existing expression is moved unchanged into a new private `readsAsRateLimited`, because the builder refuses re-indented lines and blank context lines; so one added private method). NOT covered: lines 133/321 default-path `console.error(error.message)`; the real setInterval/Blockfrost path. Tier 2 (indexer polling, callback/log only). Behaviour change for the PR: `poll()` resolves and `onError` is called instead of `poll()` rejecting, for a value whose read throws.
2. `READY_KS-1971-KS-1971-O107-P2_spark-dsv4flash_BRIEFED-CODEPATCH2-SSRF-GUARD-PASS-7of7_2026-11-09.diff.md`
   `golden: BYTE-IDENTICAL; touched=2 product_plus=1 product_minus=1 red=4/6 green=6/6 suite=1597->1603 strict=True`. One line in ssrf-guard.ts `resolvePublicAddresses`: `reason = String((err as Error).message);` (the template literal is untouched). NOT covered: the request-construction catch (line 591) and `done({... error: (err as Error).message})` (line 638), which the ticket also mentions; dispatchEvent downstream. SECURITY SURFACE (SSRF guard): TIER 1 GATE OWED; fail-closed either way (nothing becomes a pass).
3. `READY_KS-1973-KS-1973-O107-P3_spark-dsv4flash_BRIEFED-CODEPATCH2-VERIFIER-PASS-7of7_2026-11-09.diff.md`
   `golden: BYTE-IDENTICAL; touched=2 product_plus=13 product_minus=2 red=5/8 green=8/8 suite=1597->1605 strict=True`. Two hunks in vc/verifier.ts (the inner Ed25519 catch; the `verifyIssuerDID` catch). NOT covered: the outer catch's `Signature verification error: ${msg}` template (KS-1974), ServiceClient.healthCheck, health-dashboard. SECURITY SURFACE (credential verification): TIER 1 GATE OWED; both outcomes stay `valid: false`.
4. `READY_KS-1974-KS-1974-O107-P4_spark-dsv4flash_BRIEFED-CODEPATCH2-IDENTUS-CLIENT-PASS-7of7_2026-11-09.diff.md`
   `golden: BYTE-IDENTICAL; touched=2 product_plus=1 product_minus=1 red=2/4 green=4/4 suite=1597->1601 strict=True`. One line in identus-client.ts: `errorMessage = String(err instanceof Error ? err.message : err);`. PART of KS-1974 only. NOT covered: verifier outer-catch template, ServiceClient.healthCheck, health-dashboard (api-gateway). Tier 2 (result field). Rebrief of round 1 (see BLUF).
Disjointness: P1 event-indexer.ts, P2 ssrf-guard.ts, P3 verifier.ts, P4 identus-client.ts: four different files; raise in any order. Each holds one NEW test file (ks1971..ks1974 names). All four ran the whole packages/shared suite: the baseline has 1 pre-existing red (`verifyMessageSignature (CIP-8/CIP-30) KS-278`, 1596/1597 at the tip, no new red after).

## Job 1: tickets
(a) KS-2127 and higher: none exist (fetch_ge2127.py, tickets_ge2127.out = 0).
(b) Pool: all 761 open KS tickets fetched with comments (open_tickets.json; states Backlog 544, In Progress 173, Todo 34, In Review 7, Blocked 3); Backlog/Todo not named in operators 102-106's reports = 521 (cand.json). Screened by title (the 110 newest by title, the rest by a keyword filter on comment/doc/test/cell/pin/stale/README/header), then these were READ WHOLE (description + all comments):
| ticket | verdict | reason |
|---|---|---|
| KS-1972 | BRIEFED P1, HELD | event-indexer isRateLimited, one file, spelled-out shape; no open PR |
| KS-1971 | BRIEFED P2, HELD | one-line ssrf-guard fix, shape in the ticket; security surface, tier 1 gate named |
| KS-1973 | BRIEFED P3, HELD | two catches in vc/verifier.ts; security surface, tier 1 gate named |
| KS-1974 | BRIEFED P4 (identus client part), HELD | 4-file ticket; only the identus piece briefed |
| KS-2017 | not briefed | originate certifications.ts outer catch (now line 935): the msg is also used by 3 later `.includes` checks and `error?.name/code/stack` reads; a full fix is more than the String(error) the ticket names, and a route-level jest harness for the issue handler is a large test. Claude seat |
| KS-2036 | not briefed | share-line log (certifications.ts:1385) is simple, but the second line is adminConfig.ts, in open PR 2087 (KS-1600); needs a ruling-shaped test on the logger. Claude seat or next screen (item 1 alone is briefable) |
| KS-2029 | not briefed | one-line type fix in an e2e fixture; no runnable red test, no tier fits |
| KS-2028 | not briefed | eslint config coverage for tests/e2e: tooling decision |
| KS-2072 | not briefed | owner's call (print vs require keg) |
| KS-2030 | not briefed | systemTest python fixtures need a real linked-wallet actor; design |
| KS-2007 | not briefed | guard-walk reader change (security guard test infra) |
| KS-2087 | not briefed | six-item sign-off ticket, needs a runtime sweep |
| KS-1681 | not briefed | maintainer call (add a doc vs cite as external) |
| KS-1418 | not briefed | flow-doc attribution needs facts I cannot read at source (a gate's host/date) |
| KS-1338 | not briefed | guard reader change |
| KS-1764 | not briefed | delete-or-keep undecided |
Title-screened and NOT read whole (UNMEASURED beyond the title): the other ~500 candidates, mostly old behaviour/decision/security/infra tickets that earlier operators (100/101) already passed over; the keyword filter could miss a briefable one.

## Tickets listed for a Claude seat
KS-2017 (full outer-catch fix, route-level test), KS-2036 (log line, decision on adminConfig after PR 2087), KS-2029 (one-line e2e type fix, trivial), KS-1974 remainder (verifier template line 424, ServiceClient.healthCheck, health-dashboard), KS-1971 remainder (lines 591, 638), KS-1904 (related same-class sites, not read). KS-2110 (drafted by 106, security surface, tier 1 gate to be named) was NOT run: I stopped at the 4-held limit; the brief is ready for the next operator.

## Round log (done.md row times, 2026-11-09)
04:05:47 PASS ks_1972_o107_p1 (81 s, model 36.8 s) | 04:08:25 PASS ks_1971_o107_p2 (84 s, 42.9 s) | 04:11:11 PASS ks_1973_o107_p3 (93 s, 50.1 s) | 04:13:28 FAIL ks_1974_o107_p4 (79 s; brief defect, see BLUF) | 04:16:08 PASS ks_1974_o107_p4b (71 s, 29.0 s).
Direct controls (CONTROL-PASS first for P1, P2, P3, P4b; golden BYTE-IDENTICAL; ctl_*.out): P1 04:03, P2 04:06, P3 04:09, P4 CONTROL-FAIL (the defect above), P4b CONTROL-PASS.
Dry-run refusals fixed before any model call: P1 draft 1 (re-indented lines are "context, not additions") and draft 2 (blank context line) -> pure-insert edit, 1-line context (those two drafts are in night/_quarantine_2026-11-09/briefs_unused/).

## Disk, before and after
DevMASTER 14 GiB free before (disk_start.out) and after (disk_end.out); boot volume 273 -> 270 GiB free. Footprint on the boot volume: /private/tmp/spark_work_o107, 5 dirs, 1.83 GB, left in place (never delete). DevMASTER gain: run dirs only (small). Never under 10 GiB. Nothing is running (spark_status: queue 0, drainer not running, round none); queue.md has only comment lines (WHY EMPTY line appended).

## UNMEASURED
- Prose/accuracy of the new comments and the behaviour claims beyond the checker's red/green; the goldens are mine, the model output is BYTE-IDENTICAL to them (Wednesday reads the goldens).
- No tier gate has been run on any of the four; P2 and P3 are security surfaces (tier 1 gate owed).
- Real DNS, real Blockfrost, a real resolver/Identus agent were not run.
- The 4 patches were checked at 2935f723; develop was unmoved through the run, so no drift measured.
- The ~500 older candidates were not read whole (see Job 1).
- The pre-existing red cell (`verifyMessageSignature` KS-278) in the packages/shared baseline: not investigated.
- Scratch/evidence: gen/ (brieflib.py, spec_p1..p4.py, fetch scripts), open_tickets.json, cand.json, read_batch*.txt.
