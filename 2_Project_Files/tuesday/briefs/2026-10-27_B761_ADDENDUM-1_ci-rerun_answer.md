From Tuesday, Datasec / HPSM-POC, to seat Datasec/HPSM-POC-D33 (brief B761). ADDENDUM-1, the answer to your STOPPED question. Read it with the brief; where they differ, THIS FILE WINS. Nothing else in the brief changes.

**Your stop was right.** Tuesday read the run at source: run 40324213487 at 4c067e4f600d814f8b80672369a687f1702b43ed, attempt 1, `completed / cancelled`; the jobs not green were `web e2e (playbook-mobile-2)` cancelled and the summary `web (Next.js)` failure (the dependency-review job is skipped on a push, as always). Main is still 4c067e4f.

**The answer: YES.** Tuesday has started `gh run rerun 40324213487 --failed` (rc 0; the run then read `queued`). The cause was the runner (the Playwright install taking 17 minutes against the 20-minute job cap), not the code, so a re-run of the failed jobs on the SAME sha is the fix and no code changes.

**What you do:**
1. Wait on the run with your bounded `ci_wait.sh` poll (plain GET every 5 minutes). This attempt gets a NEW 30-minute bound from the moment you read this file, still never past 06:10 AEDT.
2. Resume from the FETCH (BUILD 3) only when the run reads `completed / success` on a later attempt, with every job you quote green (both npm audit steps, the web build, web unit tests, every web e2e shard including playbook-mobile-2, the api job and both api on SQL Server jobs) and both artifacts `deploy-web-<T>` and `deploy-api-<T>` `expired=false`. Quote the attempt number.
3. Every other line of the brief is unchanged: the same TARGET MAIN, the same rulings (UAT THEN DEMO, WEB ONLY both legs, rulings 6 and 13 as stamped), and the same clock (no deploy START after 06:45, DONE by 07:30, PART A passed by 06:30 or the demo is left as it is).
4. If the re-run is cancelled or fails again, or still runs at the bound: STOP with the job names and states. Do not re-run it yourself and do not hand-fetch.
