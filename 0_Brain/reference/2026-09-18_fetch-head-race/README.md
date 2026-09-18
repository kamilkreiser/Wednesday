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
