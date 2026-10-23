# B554 DRAFTER REPORT (read-only drafter, 2026-10-24 01:36-01:45 AEDT)

Kit: `/Volumes/Laptop-DEV/TUESDAY/2_Project_Files/tuesday/briefs/2026-10-24_B554_SEAT-G70_hpsmpoc-203-gate-tier2.md` (36,647 bytes; B549's is 79,744). `.pre-stamp` copy made beside it.

## Facts measured (command -> output)
- `date` -> Sat 24 Oct 2026 01:37:15 AEDT.
- `git --no-optional-locks ls-remote origin refs/heads/main refs/heads/b548* refs/pull/203/head` -> main `ee73c2908937b6ed9d3610865b3a0e38c17270ca`; `refs/heads/b548/hpsmpoc-400-customer-name-only` and `refs/pull/203/head` both `e5c2774c21fbe451c7a9c5588eb8caec262d1af6`.
- `gh api -X GET pulls/203 --jq [state,merged,mergeable_state,head.sha,base.sha,changed_files,additions,deletions,commits]` -> `["open",false,"blocked","e5c2774c...","ee73c290...",2,142,12,1]`.
- `pulls/203/files` -> `client.describeFailure.test.ts 137 9`; `client.ts 5 3`. `git diff --numstat ee73c290 e5c2774c` -> the same. Removed lines by `git diff -U0 | grep -c '^-[^-]'`: test file 9, client.ts 3 (sum 12 = PR).
- `compare main...e5c2774c --jq [ahead,behind,total_commits,files]` -> `[1,0,1,2]`; `rev-list --left-right --count ee73c290...e5c2774c` -> `0 1`. `git diff --name-only | grep -c '^api/'` -> 0. `pulls?state=open` -> `[203]`.
- `git diff -U0` of client.ts: 400 case at head `client.ts:320`; 422 line `:317`; generic line `:333`; function `:309`.
- Commit message printed: carries `Co-Authored-By: Claude Sonnet 5.5 <noreply@anthropic.com>`, no ticket key visible.
- `commits/e5c2774c/check-runs` at 01:37 -> total 13: completed 4 (Analyze (actions) success, CodeQL neutral, dependency review success, secrets gitleaks success), in_progress 9. Main head `ee73c290` lists 19. `code-scanning/alerts?ref=refs/pull/203/head&state=open` length 0; `analyses` 1 row (`/language:actions`, results 0). Required contexts printed from `branches/main/protection/required_status_checks` (5, in the kit).
- `tmux list-panes` -> `%0 tuesday`, `%353 Datasec/MPS-G69`, `%352 Datasec/MPS-G68`, `%348 Datasec/MPS-M2R`, `%1 fleet-monitor`. No G70, no H7.
- `lsof -nP -iTCP:8880-8889 -sTCP:LISTEN` rc 1 (empty); 8890-8899 rc 1. `ls -d .tools/b554` -> No such file (control `.tools/b198` and `.tools/b549` list). `uptime` -> load 4.19 5.61 6.19.
- `models_latest.json` sonnet `model_id` -> `claude-sonnet-5-5`.
- `git grep` at head: `name-invalid` appears in `CustomerManagement.edgeTrim.test.tsx` (1) and `web/src/server/mock/customer-detail.ts` (1); the `playbook` folder holds no test asserting a name refusal (only `SnapshotLauncher.tsx` lines 83-118 and 168, `maxLength={120}`). `git grep -F 'status === 400'` at head -> `client.ts`, `feedbackApi.ts`, `partner/stores.ts` (the last two outside the PR).
- Kit checks: four-underscore lines 9 (all end in the slot, 0 slots followed by text; control printf line reads 1); non-ASCII lines 0; `@[A-Z_]+@` matches 0; no person name found by grep for the owner's first/short name.
- B549 STATUS line 218 read: the #202 coupling note (name case must stay or edgeTrim goes red; locks test widening only).
- B548 STATUS last line read whole: READY FOR QA for `e5c2774c`, matching the live head.

## Judgement calls for Tuesday at the stamp
1. **Q-1** is a slot because SnapshotLauncher's name field has no committed row; without Q-1 the gate marks screen checks (b)-(d) NOT TESTED and works at `describeFailure` level.
2. **Hard stop 3 h / target 2 h** (smaller than B549's 4 h: two paths, no Api leg). CI was only 13 of ~20 check-runs, 9 in progress at 01:37; the kit makes a pending check at most GO WITH FINDINGS. Consider launching once more checks have completed, or accept the pending rule.
3. **Port block**: 8880-8889 was free at 01:37 (B549's old block); the gate binds nothing. Tuesday re-reads `lsof` at the stamp.
4. **Builder's M10 claim**: the builder says the #202 lock rows do NOT kill a status-widened mutant with the discriminator kept (only its 7 new status-gate rows do; M10b is the one the lock rows kill). I put it in Check 2 as a claim to reproduce, not as a finding.
5. **`partner/stores.ts` and `feedbackApi.ts`** still show a 400's words outside `describeFailure`; I made it a Note for the product owner, not a finding against #203. Tuesday may want to ask whether the ruling covers them.
6. I added narrowing mutants N-L and N-I (BOTH ruling) and named M3/M4/M5/M6 as the field, code, prefix and sentence-text mutants you asked for; "prefix" has a second variant, `customer.name-`.
7. Jira: made optional (GET, `project = HPSMPOC AND`), not required.

## UNMEASURED by the drafter
Whether the suite is green at the head (2446 -> 2489 is RELAYED); any mutant, red-first run, scratch render or census; the final CI and CodeQL outcome (4 analyses expected, 1 seen); whether `mergeable_state` leaves `blocked` once checks finish; the builder's 17 of 17, 43+4 rows and 72-not-shown figures; whether the real `SnapshotLauncher`/`CustomerManagement` tests can host a fetch stub without touching committed files; the load at the actual launch.

## Files written
Only: the brief, this report, and the one `cp` of the brief to the `.pre-stamp` name. No other file, no /tmp or scratchpad file; no Artifact, Docs, mail, chat or publish tool; no `decision_queue.sh`; no Jira call; git in HPSM-POC was ls-remote, diff, show, log, rev-list, cat-file, grep with `--no-optional-locks` only; `gh api -X GET` only under the project `GH_CONFIG_DIR`; no HTTP to the app or hosted hosts; no `.tools/**` opened (only `ls`/`ls -d` of names in `.tools`). One early tool call containing a `cd` was refused by the hook and re-issued without it; one call with an unquoted split variable was likewise refused and re-issued under `bash`; neither ran.
