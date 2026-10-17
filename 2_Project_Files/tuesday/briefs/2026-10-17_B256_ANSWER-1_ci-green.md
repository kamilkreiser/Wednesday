From Tuesday (Kam's Datasec coordinator seat), Datasec / HPSM-POC, to seat B256 (pane Datasec/HPSM-POC-F4). ANSWER-1 to your `STOPPED: NEEDS TUESDAY` (B256_STATUS.md, 15:22 AEDT).

## BLUF
Main's `ci` on `787d159` is now GREEN. Resume your brief from **step 5**, unchanged. Everything you have not done stays as the brief says (backup first, way back kept, live checks, `DEPLOYED:` / `STOPPED:` final line).

## What Tuesday did and measured (gh as kamilDatasec, the project's own GH_CONFIG_DIR)
- Ruled the 2 failures a runner/timing flake, not the change: `HostedDemoConcurrentStartTests.Two_hosts_starting_together…` and `ImportFileStoredHashMigrationTests.ImportFileStoredSha256…` ("Cannot release the application lock … `__EFMigrationsLock`"), job 117304131543. PR head `7a2c7ae` tree `a5ac7f54761e` (GitHub commits API) equals main `787d159` tree `a5ac7f54761e` (rev-parse), and PR run 39000249834 was `success`.
- Ran `gh run rerun 39001143811 --failed` (rc 0) at ~15:23 AEDT. **Attempt 2: `completed success`** at 15:34:59 AEDT (`gh run view 39001143811`: attempt 2, conclusion success, headSha 787d159089d8).
- CodeQL on `787d159`: Analyze (actions / csharp / javascript-typescript / python) all `success` (check-runs API).

## For your records
- Use **run 39001143811 attempt 2** as main's CI for this deploy; fetch its artifacts as the brief names (the artifacts are per run; say in your STATUS which attempt's artifact ids you used).
- Record the attempt-1 failure in Open as a ticket candidate: the `__EFMigrationsLock` timeout class (B174 R2-3 first sight; second sight here). Do not file it yourself; Tuesday's records seat files it.
- Nothing else changes: no Jira, no mail, no records branch.
