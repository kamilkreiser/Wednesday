# B396 drafter report (2026-10-21 10:25-10:30 AEDT, clock from `date`)

Brief: `2026-10-21_B396_SEAT-G22_hpsmpoc-pr175-delta-gate-tier2.md` (37 lines, long paragraphs; slots `@STAMP_TIME@`, `@LAUNCH_AUTH@` 1 each; last line `READ-WHOLE-BY-TUESDAY: PENDING`). Read whole: B395 brief, B390 brief, B391 STATUS, `model-routing.md:92,109`. Incorporates your 10:28 correction (gated head `89bdb18e`, main `3aeeacc5`, check 7 merged lock).

## Measurements (read verbs; `gh api` GETs under the project GH_CONFIG_DIR; `git --no-optional-locks ls-remote`)
- `ls-remote`: main `3aeeacc59529f958cb6c6fe41d79650d6fa0cc53`; `refs/pull/175/head` `89bdb18e7bdfbed95f2ca3c435fbbc53c7eff37e`; `refs/pull/170/head` `b5ea627e…`; branch `b380/hosted-first-impression-235-234` same as #175 head; no `b396*`/`b397*`; no `.tools/b396`, `.tools/b397`; ports 7540-7559 listeners 0 (control: unfiltered 11).
- PR #175: open, not draft, base `3aeeacc5`, commits 3, files 9, +463/-10, `mergeable_state` blocked. Commit `89bdb18e` parents `383fa090`, `3aeeacc5`. `compare 383fa090...89bdb18e` = 4 files (3 #168 api Feedback files + `web/package-lock.json`). The 9 files: infra baseline test, lock, package.json, instrumentation.ts, bff.keepalive.test.ts, bff.ts, upstreamAgent.ts, warmup-render(.test).ts; no `api/`.
- `compare 383fa090...b5ea627e` = exactly 4 -232 files (Caller.cs, FirstVisitWarmup.cs, the two FirstVisitWarmup test files): none of the 9 touched.
- PR #172 merged 2026-10-20T23:26:18Z (3aeeacc, lock only). Open PRs: 175, 174 (dependabot vite 8.3.4, lock +146/-80, likely redundant now), 173, 171, 170, 169.
- CI at `89bdb18e` 10:28: all in_progress except CodeQL neutral; at the old head 383fa090: web build failure (vite audit), 2 Analyze legs success.
- Not run: npm, node, vitest, dotnet, merge-tree, Jira.

## What changed versus your instruction
- Merge commit: B396 allows "2 own commits + 1 merge"; a Blocker is any other own commit. The expectation "1,845 passed" and "1,518 + 13 NotExecuted" rests on B391 counts (the merge adds 3 Feedback api files from #168, which are in a different test project, so the HpsmPoc.Api.Tests count should be unchanged; the seat reports any difference).
- Check 7 (merged lock) added verbatim from your correction; the 20 vite-family keys are to be read from #172's diff (B395 STATUS may exist by then).
- #174 (dependabot) added to the merge predictions; Note-level.

## Questions (recommended answers)
1. Should #174 be closed by you now that #172 landed? Recommend yes (redundant; its lock +146/-80 is a superset-looking bump); B396 only reports.
2. Stamp slots: `@STAMP_TIME@` (e.g. "stamped by Tuesday at <time> AEDT (brief read whole by Tuesday s133, N lines + this report)") and `@LAUNCH_AUTH@` (same authority wording as B395: Kam's 2026-10-16 grant + terminal words 2026-10-21 ~07:2x + the 2026-09-01 three-hop QA gate rule tiered 2026-09-05). Fill the Stamp time slot with a full stop at the end, then a space and the authority slot follows on the same line.
3. Run the API suite (SQLite) in a tier-2 delta gate? Recommend yes: it is the stand-alone proof; load was 2.0 at 10:26.
