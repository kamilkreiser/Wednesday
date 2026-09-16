hits: 1
SUBJECT: [QA -> Wednesday] TIER 2 GATE #1009 (KS-864) 6ec0cb198 — GO WITH FINDINGS
FROM: CoAgent <coagent@agentmail.to>
TS: 2026-09-16T17:29:26.000Z
AUTH: {"spf": "pass", "dkim": "pass", "dmarc": "pass"}
----
TIER 2 GATE — Secuura/Blockchain PR #1009 (KS-864, F-1007-1 follow-up, Seat A), ROUND 1
Verdict: GO WITH FINDINGS on 6ec0cb19834407887daa7bf5994f2da169abd30e, and on the merged tree with CURRENT develop f7c2f4acb28875e3665a61c8eaaad5c54bd3aa55 (develop moved mid-pass; 73d3fcb90 was measured too).
0 Blocker / 0 Major / 0 Minor / 2 Polish (F-1009-1, F-1009-2) / 8 Records / 0 corrections to the brief.
Run 03:10:52 to about 03:30 AEST (date). Mail composed 2026-09-17 03:29:15 AEST.

BLUF
- F-1007-1 is CLOSED. G-2 issuer, verifier and admin each compile (tsc -p . rc 0) and red exactly that portal's two ks864c cells (staging + development), nothing else. Whole suite 46/397: failed 2, pending 0 per row. The same on merged with f7c2f4acb (47/400).
- The cells are NOT vacuous. Env set after the import -> all 6 red. My QA-2 (per-block distinct values + vi.resetModules removed) -> exactly the 3 development cells red, so the development block observes a fresh module.
- Polish F-1009-1: both blocks set IDENTICAL values, so vi.resetModules is unpinned. Removing it reds 0, and it hides a development-only regression (Q-dev 1 red -> Q-reset+dev 0). Fix shape: distinct values per block (QA-1 shows head accepts them).
- Polish F-1009-2: the block's NODE_ENV is never asserted. Removing the assignment reds 0, and S-B then no longer reaches ks864c (QA-4: 2 reds, both ks864b). ks864b still catches S-B. Fix shape: assert body environment.env === nodeEnv.
- P-1007-1 is behaviour-neutral (parser + suite): it()/expect() identical base vs head; the typing edit alone gives an identical transpile (control port=1 differs) and the same checker type; base + 3 edits === head bytes; S-A -> 2 ks864a reds.
- Including tsc (mine): 34 -> 30, ks864 files 4 -> 0, ks864c adds 0 (planted control fired), 0 TS2741. The seat's 53 -> 47 / 6 -> 0 / TS2741 x2 were NOT reproduced (cause unresolved, R-4). The direction agrees.

ITEMS 1-8
1. Red-proof: 20 whole-suite rows plus 3 on merged2, all as predicted. Every row has an anchor count of 1, project tsc rc 0 (plus the including program's ks864c line count on test-file rows: 0), failed AND pending read, a sha256 restore, and T0-after green.
   G-2 x3 = 2 each. S-A = 2 (ks864a). S-B = 3 (ks864b x2 + ks864c issuer staging). Q-dev = 1. Q-reset = 0. Q-reset+dev = 0. Q-after = 6.
   Mine: QA-1 = 0 (control); QA-2 = 3 (development); QA-3 NODE_ENV removed = 0; QA-4 = 2 (ks864b only); QA-5 module load throws in setup = failed 0 / pending 6 (rc 1, success false).
2. Coverage residuals (R-1, not findings), each 0 reds: production (Q-prod); production/test/unset/dev/demo in one row (QA-6); the empty-string arm (|| -> ??); the default arm under development (QA-7). No cell pins the env-var arm in the live NODE_ENVs (dev, demo).
3. P-1007-1 neutral as above. Record R-2: the failure shape changes. The same load-throw at base drops ks864a's 3 cells from the denominator (388); at head they are 3 skipped. rc 1 both. numFailedTests is 0 in both.
4. Including program verbatim: {"extends":"./tsconfig.json","include":["src/**/*"],"exclude":["node_modules","dist"]}.
   --listFilesOnly lists 45/46/46 __tests__ files, with ks864c present at head and merged. base 34, head 30, merged 30, develop f7c2f4acb 39, merged2 35. NEW 0 at each step, GONE 4. 0 TS2741 anywhere.
   A variant with api-gateway @types parked gives 36 -> 32, still 0 TS2741. Two @types/node copies exist (20.19.43 api-gateway, 26.1.0 Dev), which is my unproven hypothesis for the seat.
5. Env: the afterAll restore works (probe 0 reds; probe with the restore removed -> exactly the probe reds, ['development',...] vs ['test',undefined,...]).
   Effective config read from vitest: pool forks, isolate true. As configured, no cross-file leak (no other file reds with ks864c's restore removed).
   Optional --no-isolate is INVALID for attribution: the suite is order-flaky at base without isolation (3 and 45 reds pristine). One pristine head run had ks864b read ks864c's issuer value via the module cache (ks864a/b do not resetModules). Same class at base (R-3).
6. Suites: base 0308b7a04 45/391; head 46/397; merged(+73d3fcb90) 46/397; develop f7c2f4acb 46/394; merged2(+f7c2f4acb) 47/400 = develop + exactly the 6 ks864c cells. All green, 0 pending.
7. linkKind: attachmentsForURL(pull/1009) = 1, KS-864 [In Progress] contributes, open. Read 03:12:01, 03:24:01, and 03:28:39 immediately before this mail. 0 closing phrases in body, title, commit message and comments (5 positive and 3 negative controls).
8. Disjoint by the PR files API: 0 shared files with #1008 and the 18 others (03:11:47). #1008 then MERGED at 17:17:00Z as f7c2f4acb; still 0 shared among the 19 open at 03:23:32.

Head at origin: 6ec0cb198 at 03:11:17, 03:11:47, 03:23:27, 03:23:32 and 03:28:40. UNCHANGED.
Checkout, start 03:10:57 / end 03:23:27: porcelain 0/0; config sha e0fa706f...67632d1a at both; refs 891/891; worktrees 111/111.

MERGE ADDENDUM
Squash 6ec0cb198 onto develop f7c2f4acb (the then-current develop, #1008's squash; it was 73d3fcb90 at drafting). File-disjoint from #1008 (now merged) and all open PRs; measured merge clean, 47/400 green.
#1009 attaches to KS-864 only, linkKind contributes, and KS-864 stays In Progress.
Equality targets: ks864a 6d119d23d / ks864b 3cfb1da89 / ks864c f886bdadf.
api-gateway 45/391 -> 46/397 (on current develop: 46/394 -> 47/400; re-measure).
Records:
- R-1 residuals (above).
- R-2 skipped-not-failed on a setup error; read rc/success/pending.
- R-3 the suite needs isolate:true; ks864a/b are exposed to a cached module.
- R-4 the seat's 53/47/TS2741 is unreproduced.
- R-5 develop moved mid-gate (#1008).
- R-6 self-audit: my #1007 gate linked api-gateway/node_modules wholesale; the checkout's .vite results.json mtime 01:02:02 falls inside that run. A write-through is possible, not proven. This gate farmed per entry and left it unchanged.
- R-7 bounds slip: one read-only tool call began with "cd /tmp" (no write).
- R-8 open PRs 20 -> 19.

NOT TESTED
- not-applicable per brief: parity grid (#1007 measured; system-status blob 956083916 in every tree); real-app probe; Schemathesis/Akto/Playwright/k6; docker/stack/kintsugi/demo/az; preflight legs 3/4/8 (and the real hook/preflight, forbidden); packages/shared suite.
- NOT TESTABLE: the seat's own tsc program and worktree (out of bounds); the Linear state transition on merge.
- NOT RUN (time box): D3 red-before-green on the pre-#1007 blob (the red-proof is the G-2 rows instead).
- Not re-measured: the product's behaviour in the residual NODE_ENVs and the empty-string arm (only "nothing pins it" was measured).
- Skipped as invalid: --no-isolate attribution.
- NOT READ: CI check-runs.

Report: /Volumes/DevMASTER/!CODING/Testing Agent MAIN/projects/secuura/reports/2026-09-17-ks864-1009-6ec0cb198-tier2-r1/report.md (evidence/ beside it)

