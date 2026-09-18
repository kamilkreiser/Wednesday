# FETCH_HEAD race — measured 2026-09-18 by Tuesday

**Symptom:** `git pull --rebase` fails intermittently with `fatal: Cannot rebase onto multiple branches`
(safe_push rc 24, wed_claim, bare pulls). Both seats hit it (Wednesday on 09-17, Tuesday 3x on 09-18).

**Cause, measured in a throwaway repo (fhrace.sh, fhrace2.sh beside this file; paths are this seat's scratchpad):**
FETCH_HEAD is one shared file. Every `git fetch origin` and every `git pull` rewrites it, and `git pull`
then READS it. Concurrent writers leave it with more than one for-merge line.

| setup | pulls | "multiple branches" failures |
|---|---|---|
| background `git fetch -q origin` (panel_sync.sh:57 today) vs foreground pull | 150 | **85** |
| background `git fetch -q --no-write-fetch-head origin` vs foreground pull | 150 | **0** |
| background pull vs foreground pull (chat_sync + panel_sync + safe_push all pull) | 150 | **149** |
| BOTH loops: `fetch -q --no-write-fetch-head origin main && rebase -q --autostash origin/main` | 150 | **0** |
| control: no background writer | 50 | 0 |

**Therefore the one-line fix to panel_sync's fetch is NOT sufficient:** pull-vs-pull races too.

**Fix recipe (not yet applied — owed, claimed by Tuesday in wed_claim.sh):** replace every `git pull --rebase`
on this repo with `git fetch -q --no-write-fetch-head origin main && git rebase [--autostash] origin/main`, and
add `--no-write-fetch-head` to panel_sync.sh:57. Sites: tools/panel_sync.sh:57 and :187, tools/safe_push.sh:101
(it parses pull output for conflict handling; READ that before changing, and keep its rc contract),
tools/wed_claim.sh:54, tools/chat_sync.sh:79. Rules for the edit: panel_sync runs as a detached loop and
chat_sync under launchd, so never edit either in place while it runs (stop, edit, run once, re-arm the
launcher's way). Arms: the harness above against each edited script's pattern, plus each script's own
existing arms.

## APPLIED 2026-09-19 by Tuesday — commit 4fc780e24 (claim released)

**FOUND.** (1) The recipe's five-site list was complete over `tools/` and silent about the launcher:
`Launch_Wednesday.command` did its own boot `pull --rebase` (and hinted one), and `_store_guard.sh:43`
(called by wed_claim) did a plain FETCH_HEAD-writing fetch. Both are now fixed too. (2) The 09-18 harness
held origin STATIC, which hid a second, pre-existing failure: concurrent fetches updating
`refs/remotes/origin/main` while origin moves fail with `cannot lock ref`. It fails safe (nothing touched)
and the old pull pattern suffers it as well.

**CHANGED.** Every `pull --rebase` on this repo in live tooling became
`{ fetch -q --no-write-fetch-head origin main || { sleep 1; <same fetch>; }; } && rebase [--autostash] origin/main`
(autostash only where the old line had it: safe_push, wed_claim). Background fetches gained
`--no-write-fetch-head` (panel_sync advance, _store_guard, launcher's dirty-tree measure). Written by temp file +
atomic rename, modes kept. Not changed: `wednesday_rotate.sh` fetches (they write FETCH_HEAD, but nothing reads
it any more — ARM-2 below proves a plain-fetch writer is now harmless), history comments, `kam_copies_2026-09-16.sh`
(a one-off).

**TESTED, and HOW** (`fharms.sh` beside this file, scratch repos only, 120 syncs per arm, a PUSHER moving origin):
| arm | failures | multiple-branches |
|---|---|---|
| RED: old pull fg vs old pull bg | 120 | **120** (defect reproduced) |
| new fg vs new bg + pusher (no retry) | 32 | 0 (all `cannot lock ref`) |
| new fg vs UNMODIFIED plain fetch bg + pusher | 35 | 0 |
| **new WITH one retry, fg vs bg + pusher** | **4** | **0** |
| control: old pull fg vs plain fetch bg + pusher | 100 | 57 |
Real scripts in the real repo: safe_push (committed + pushed 4fc780e24, HEAD == origin); panel_sync `once`
(commit, rebase, regen, push, HEAD == origin 35b2e09c4); wed_claim check (sync ran, rc 3 = claimed, as expected);
chat_sync (3 runs incl. two launchd fires: dirty-tree SKIP with rebase's own refusal = its intended behaviour;
its clean-tree success path is the same fetch+rebase panel_sync completed, not separately exercised).
panel_sync loop stopped (argv-anchored kill) BEFORE the edit, re-armed after, detached (sess 0, tty ??).
**NOT TESTED:** the launcher's boot path (runs at the next boot — read its output then); the Studio's copy
(Wednesday's loop keeps the old code until she restarts it).
