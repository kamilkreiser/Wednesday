# Spark operator 63, 2026-11-02: KS-1868 originate (2 held, 1 skipped, 0 failed, no rebrief)

## BLUF
HELD: O63-P1 (routes/systemErrors.ts, the two ingest catches, reuses the file's own fail500) and O63-P2 (services/errorTrackingService.ts trackError catch :65, inline `let reason` guard). Both controls CONTROL-PASS first time, both model rounds PASS 7/7 on the ORIGINAL brief, golden BYTE-IDENTICAL, strict=True. SKIPPED: O63-P3 platformOrganizations.ts (all three sites) and errorTrackingService.ts getRecentErrors :135, with reasons below. Tip 03977e89a343ad7362760e4fb0270602fb6da5ce at start (tip_start.out) and end (tip_end.out). Open-PR scan start 22 PRs/125 files, end 22 PRs/125 files; no open PR lists systemErrors.ts, errorTrackingService.ts or platformOrganizations.ts (originate appears only as package.json in 575/949/1726 and integration tests in 1790/1792/1794); planted control services/originate printed 11 entries at both scans (my own recount of the files printed 6; discrepancy not chased, both non-zero).

## Originate gate answers
- Existing guard: the grep (guard_grep.out) found NO describeThrown. systemErrors.ts has its own `fail500` (KS-730/KS-1772, describes in a try, logs in another, always sends the constant 500) already used by 4 admin routes: P1 reuses it. certifications.ts:1086 has the inline `let reason` pattern: P2 copies it.
- Suite baseline: harness baseline at the tip (checker.out of the controls) = 1999 tests, 0 failed, 0 failed suites, GREEN; tsc rc 0. Control rounds 110 s and 93 s (baseline + after suite + tsc, no model); model rounds 148 s and 220 s. So well under the 10 min limit. (My own jest run in the spark cache clone showed 37 red suites, 19 red tests, 36 s wall: that is the cache's stale @secuura/shared build, TS2305 on signEmitterHop; it is NOT the harness clone's state; suite_base.err/out. Relevant only as a trap for anyone running jest in the cache.)

## Held (ls night | grep O63; held_files.txt)
READY_KS-1868-KS-1868-O63-P1_spark-dsv4flash_BRIEFED-CODEPATCH2-BRIEFED-CODEPATCH2-ORIGINATE-SYSTEMERRORS-INGEST-CLIENT-ERRORS-CATCHES-PASS-7of7_2026-11-02.diff.md
READY_KS-1868-KS-1868-O63-P2_spark-dsv4flash_BRIEFED-CODEPATCH2-BRIEFED-CODEPATCH2-ORIGINATE-TRACKERROR-CATCH-PASS-7of7_2026-11-02.diff.md

## O63-P1: systemErrors.ts POST /ingest (:134) and POST /client-errors (:165)
- hold_ready: `golden: BYTE-IDENTICAL; touched=2 product_plus=2 product_minus=4 red=4/8 green=8/8 suite=1999->2007 strict=True`. Model 45.2 s (round 148 s). Test: src/__tests__/ks1868-system-errors-ingest-catches-p1-unreadable-throw.test.ts (real loopback listener, shape of ks1780-system-errors).
- Fix: the two lines of each catch (logger.error + res.status(500)) become `fail500(res, '<same context>', err);`. Hunks 30 lines apart.
- Callers: unauthenticated ingest routes, called by other services / the React error boundary over HTTP.
- Today vs after: response BODY is the same constant 500 for every value. Unreadable value (revoked Proxy / throwing message getter): today the catch throws, nothing logged, no response (hang); after: logged `thrown value that could not be described` under the same context, constant 500 (what an ordinary Error gets, control C1). Persisted: nothing.
- BEHAVIOUR CHANGE for the PR: (1) as above. (2) log TEXT for a thrown value that is neither Error nor string (e.g. plain object): `[object Object]` today, `thrown <Ctor> with fields [keys]` after (KS-1346's form already used by the file's other six routes). Errors and strings log identically; existing ks730a A3/A4 pin that and stay green (suite 1999 -> 2007, no new red).
- Tier: 2 (admin-adjacent ingest, no money/keys, response unchanged).

## O63-P2: errorTrackingService.ts trackError catch (:65)
- hold_ready: `golden: BYTE-IDENTICAL; touched=2 product_plus=7 product_minus=1 red=2/5 green=5/5 suite=1999->2004 strict=True`. Model 33.8 s (round 220 s, incl. waiting behind nothing: queue gap). Test: src/__tests__/ks1868-error-tracking-track-error-p2-unreadable-throw.test.ts (mocks ../db and the logger; outcome read via .then('resolved','REJECTED')).
- Fix: one hunk; `let reason` + try/catch 'unreadable thrown value'; log line now `{ error: reason }`.
- Callers: errorHandler.ts (fire-and-forget), index.ts :79/:84 (.catch), and the two awaited calls in routes/systemErrors.ts.
- Today vs after: unreadable insert failure: today trackError REJECTS (breaking its "never throws" doc); after logs the constant reason and resolves, as an ordinary Error already does. KNOCK-ON the raise seat must state: for such a value only, the two ingest routes go from 500 to `201 { success: true }`, which is what they already answer for an ordinary DB error. Persisted: nothing (insert failed either way).
- Tier: 2. If Kam does not want the 500->201 knock-on, drop the pass; it is independent of P1 (different file).

## SKIPPED
- platformOrganizations.ts :112, :145, :168 (O63-P3): erase-connector is GDPR organisation erasure (hard limit 3: GDPR erasure = SKIP). Also each catch calls `sendRefusal(res, err)` first, which does `err instanceof OrganisationErasure...Error`; on a revoked Proxy that throws before the message line, so a message-line fix is half a fix (same Zod-style problem). The :145 site is the post-transaction failure log whose 500 tells the retrying platform "nothing was erased": response semantics need a human call.
- errorTrackingService.ts getRecentErrors :135 (part of the assigned list): its return value IS the body of GET /api/system-errors; for an unreadable value the route's 500 would become a 200 with an empty list (what an ordinary Error already yields). Client-visible body change, hard limit 3, so not briefed; Wednesday/Kam can overrule (it is the same guard, one more hunk).
- No Zod pre-check site was met in P1/P2 (the isZodError site at :187 is already guarded by KS-1780).

## Raise-seat notes
strict=True both; P1 hunks and P2 hunk are in different files, any order, one PR possible. Refs KS-1868 only. Reds: P1 R1/R2 x 2 routes (4), P2 R1/R2 (2); controls C1/C2 (+C3 in P2). Test names in the briefs start `RED ks1868 R1/R2`, `control ks1868 C1/C2`.

## Round log (spark/done.md rows)
- Controls queued 08:2x (queued_controls.txt) behind o62: 08:32:01 CONTROL-PASS P1 (110 s); 08:33:35 CONTROL-PASS P2 (93 s)
- P1 model queued at 08:32, PASS 08:36:03 (148 s, 45.2 s model, BYTE-IDENTICAL); P2 model queued 08:33 behind o64's control, PASS 08:46:45 (220 s, 33.8 s model, BYTE-IDENTICAL).
- Lint rc 0 x2; dry runs rc 0 (input 36464 B / 30811 B). Counter: 1 original brief each, 0 rebriefs.

## UNMEASURED
Whole-suite CI with the patches beyond the harness A6; eslint; real Postgres; whether an unreadable value is reachable in production; platformOrganizations and getRecentErrors patched behaviour (read only, no cells); the other originate candidates (anchors.ts, verification*.ts, reanchorInFlight.ts: not read).
Evidence: this folder (tip_*, prscan_*, open_prs*.json, guard_grep.out, suite_base.*, lint_*, dry_*, hold_*, held_files.txt, done_rows.txt, *.tip.ts, gen/mk63.py t63_p1/p2.ts.txt hold63.sh prscan63.py).
