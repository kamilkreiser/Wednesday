# Spark operator 42, 2026-11-01 (Secuura only). Filed by the operator.
BLUF: two NON-security, log-only KS-1868 sites in services/analytics (the O40 siblings exportService dbSaveExport, scheduledJobs dbSaveAlertRule) both PASS 7/7 on the ORIGINAL briefs, byte-identical to the goldens, HELD. Nothing raised, pushed, merged; no board touch; no git write verb in !CODING (the only write verb, git fetch, ran in the cache clone spark/cache/src).

## Method
- Read O41 (incl. UNBLOCKED RUN) and O40 reports whole; copied gen/mk41.py and tasks41.py to gen/mk42.py and gen/tasks42.py (tip, counts, op number, two new tasks; brief prose is O41's). prscan.py from O35 re-run. Tunnel: tunnel.sh check = UP (200). Load average 8.58 at 15:52, 7.15 at 15:59 (round.sh run under nice 10, one request at a time).
- Tip: git fetch origin develop into the cache clone: FETCH_HEAD 85c56a3d1eb92c8399dcfd3d6ee2a717cf356428 (fetch.out/fetch.err, rc 0). Matches Wednesday's ls-remote.

## Partition evidence
- prscan.out: "19 PRs 108 files" (open_prs.json). Positive control: services/auth in 7 file entries (partition.out).
- partition.out: open PRs touching services/analytics: 1360 package-lock.json; 948, 649, 575 package.json. NO src file of analytics is in any open PR. #1889 is merged: the diff 3d036184..85c56a3d1eb9 over services/analytics lists only exportService.ts, scheduledJobs.ts and the two O40 tests (4 files, 134 insertions, 2 deletions), i.e. the O40 loadFromDb fixes.
- Not checked: other seats' unpushed local work beyond PRs; the S9 brief was not re-read (neither file is tenant-context / tenant-pool-manager / tenant-provisioning / vc-issuer).

## Screening (log-only check, read at 85c56a3d1eb9)
- exportService.ts dbSaveExport catch (:55, read :56): logger.info only; method returns void; message not stored on the record. Log-only. Excluded by name: exportService.ts:160 (stores message on the export record) is untouched.
- scheduledJobs.ts dbSaveAlertRule catch (:58, read :59): logger.info only; both callers end in .catch(() => {}). Log-only.
- scheduledJobs.ts dbSaveAlert (:85): same shape, log-only; NOT taken (limit of 2 sites, and it shares P2's file). Left.
- Not in any held O34-O41 site (held list: loadFromDb x2, analyticsService, metricsCollector, hash.ts, scenario.ts, presentations, credentialRepo, audit-logger, response-cache, gracefulShutdown, demo-service index.ts, nft provider.ts, demo state.ts).

## Sites
- P1: Blockchain/Dev/services/analytics/src/services/exportService.ts:56 in ExportService.dbSaveExport. err instanceof Error ? err.message : String(err) is read inside the logger.info argument; a revoked Proxy or throwing message getter makes the catch throw, no log, and dbSaveExport rejects into createExport/processExport. Fix: inner try into reason, fallback 'unreadable thrown value'. New test ks1868-export-service-db-save-unreadable-throw.test.ts (C1, R1, R2; private method reached by a type cast).
- P2: .../analytics/src/services/scheduledJobs.ts:59 in dbSaveAlertRule. Same shape and fix. New test ks1868-scheduled-jobs-save-alert-rule-unreadable-throw.test.ts, reached through new ScheduledJobs(...).addAlertRule (callers swallow the rejection, so at the tip the log line is simply lost); the constructor's default-rule saves are flushed and the log mock reset before the rule under test.
- Briefs: night/briefs/ks_1868_o42_p1_analytics_exportservice_dbsaveexport_unreadable_throw/ and ..._p2_analytics_scheduledjobs_dbsavealertrule_unreadable_throw/ (written by gen/mk42.py; mk42.out).

## Results (each from the named file)
- lint_p1.out / lint_p2.out: brief_lint rc 0 (both).
- dry_p1.out / dry_p2.out: round.sh --dry-run rc 0 both; input built at 85c56a3d1eb9, 31538 B (P1), 35189 B (P2). No refusal.
- control_p1.out / control_p2.out: CONTROL-PASS, golden BYTE-IDENTICAL, 78 s (P1), 36 s (P2), first time.
- round_p1.out: PASS (checker rc 0 + A2a anchor OK), golden BYTE-IDENTICAL, 64 s round, 27.792 s model, 12433+1052 tok. round_p2.out: PASS, BYTE-IDENTICAL, 70 s, 31.235 s model, 13893+1178 tok. out.md.meta.json: thinking false, thinking_chars 0 (both). My cmp of out.md.checker/section_1.diff vs its -control run: identical (rc 0, both).
- checker.out (read by me), both runs: A1 pass; A2 strict apply; A3/A3c/A3x pass; A4 red-first 2 failed / 3 run, controls green, assertion reds; A5 3/3 green after; A6 baseline 50 -> after 53, no new red; A7 tsc rc 0 (baseline rc 0); A2a anchor hunks=1 ok=1. RESULT: PASS (7/7).
- hold_p1.out / hold_p2.out (hold_ready): golden BYTE-IDENTICAL; touched=2, product +7/-1, red 2/3, green 3/3, suite 50->53, strict. Both rc 0.
- Observation: checker.out prints "MISMATCHED HEADER" for each section (the "--- diff --git" pairing in its own section scan) while still applying strict and passing A2; same text shape appears with the golden in the -control run. Not investigated; flagged.

## Held
- /Volumes/DevMASTER/WEDNESDAY/2_Project_Files/local-model/night/READY_KS-1868-O42-P1_spark-dsv4flash_BRIEFED-CODEPATCH2-EXPORTSERVICE-DBSAVEEXPORT-PASS-7of7_2026-11-01.diff.md
- /Volumes/DevMASTER/WEDNESDAY/2_Project_Files/local-model/night/READY_KS-1868-O42-P2_spark-dsv4flash_BRIEFED-CODEPATCH2-SCHEDULEDJOBS-DBSAVEALERTRULE-PASS-7of7_2026-11-01.diff.md
- Renamed from hold_ready's doubled prefix / BRIEFED-CODEPATCH2 duplication (mv -n). hold_ready stamps "by Wednesday"; the source reads were the operator's. Wednesday should re-read. Rows appended to spark/done.md, line to spark/queue.md.

## UNMEASURED
- eslint on the new files; real analytics service boot; the other ~240 sites; live-lane overlap beyond open PRs; the S9 brief; whether such a thrown value ever occurs; goldens are operator-authored (proved by --control only); exactly why the checker prints MISMATCHED HEADER.
- Both patches touch different files; P2 and the left dbSaveAlert:85 would touch the same file if later taken (hunk offset only).

## Decision for Wednesday
- Tier of the raise: analytics logging, not a security surface by path. Whether to batch P1+P2 with other O40-class analytics patches in one PR is Wednesday's call.
