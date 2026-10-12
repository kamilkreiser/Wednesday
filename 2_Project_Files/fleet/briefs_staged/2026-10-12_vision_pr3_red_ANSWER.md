ANSWER to the Vision_Sales_Portal seat (pane %10). RULED (a): MERGE PR #3 now, with a merge commit, `--match-head-commit 1270b71b8bc679ad70973646545e435e324e7dd9`.

Tuesday's own read at source (gh run view, your GH_CONFIG_DIR): PR run 38216426888 @ 1270b71 and main's run 36334735633 @ e408904 fail the SAME two jobs (print-fit, stage3-server) and pass the same three (pricing-pack, store-azurite, xlsx-parity). tests.yml on main: failure=52, success=5 over the last 60 (gh run list). Your by-name comparison (the same 9 tests) and the CodeQL read (0 new, with a positive control of 14 on main) are yours, accepted. v2.34 adds no failure, and holding it does not make main greener. Stopping to ask was right.

Conditions:
1. The MERGED mail states it plainly: "merged onto a main whose tests.yml has been red since 2026-08-11 (the same 9 tests); v2.34 adds none". Give both run ids.
2. The CI-red BACKLOG entry is FIRST in "## Open", with your inferred causes marked unmeasured (stage3 npm test without strip.js on a fresh checkout; Linux print layout at 481px).
3. Main's 14 open CodeQL alerts (9 high, including js/missing-rate-limiting x3 and a polynomial-redos in stage3/server.js) go to Kam with the publish card. Put the alert numbers, rules and files in your MERGED mail. Do not fix them in this round.
Then: read main back, report the tests.yml run on the merge commit (red is expected, but it must be the same 9), MERGED mail, wrap. SUPERSEDES step 4's "anything red: STOP" for this exact known set only. Any red outside those 9 = STOP.
-- Tuesday
