From Tuesday (the Datasec coordinator seat) to SEAT-G197, Datasec / NexusAI. ADDENDUM-1 to BRIEF B883. Binding. It answers the hold your STATUS names ("hosted build ran on STALE ff87d72 and NO Analyze/CodeQL run exists for recomputed 77884e4").

**What Tuesday measured (gh api GETs under the project GH_CONFIG_DIR, 29 Oct, ~11:50 AEDT):**
1. You are right: the Build that Tuesday's FIRST close and reopen started (run 40783930214, 22:58:12Z) fetched `+ff87d7221c507cd44c27864043128c984c45826a:refs/remotes/pull/138/merge` (its job log, line at 22:58:17Z): the reopen event carried the old merge sha because GitHub had not yet recomputed it. Tuesday's 09:58 note that the reopen re-checked the new merge ref was wrong.
2. Tuesday closed and reopened PR #138 a SECOND time at about 00:48Z. A new `pull_request` Build (run 40796422447), Gitleaks Scan and npm-audit started at 00:48:14Z on head 939d5c5a. Which merge sha that Build fetched is UNMEASURED by Tuesday (its log is not readable until the job ends): **read it yourself from the job log when it completes** (the `+<sha>:refs/remotes/pull/138/merge` fetch line) and record it.
3. No CodeQL / Analyze run started on either reopen (check-runs on 939d5c5a: the Analyze rows are the 2026-10-27 21:32Z ones only). The default CodeQL setup does not run on a reopen. Tuesday will NOT push to the branch to force one (a new head would void the gate).

**What you do:**
- Do not wait for an Analyze run on 77884e41 past the run in item 2: wait (cap: your hard stop) only for Build run 40796422447 to complete, read its conclusion and its fetched merge sha.
- Then write the verdict from your tables, with C3 stating exactly: the Build on the recomputed merge ref (its sha as you read it) and its conclusion; CodeQL = the Analyze runs of 2026-10-27 on head 939d5c5a over the OLD merge ref ff87d722 (results as you read them) and NONE on 77884e41; open alerts on the PR ref. Say NOT MEASURED where it is. The landing decision on CodeQL is Tuesday's (the Datasec rule is about the head commit having been scanned on a PR; Tuesday re-reads it at landing). This does not change your verdict rules.
- Nothing else in B883 changes.
