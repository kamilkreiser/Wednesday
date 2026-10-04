# Reboot recovery — 2026-10-04 ~18:20 (written by a Claude Code session at Kam's request)

## What happened
- The `com.wednesday.nassync` job (unison DevMASTER <-> NAS `/Volumes/Development`) started 03:30 today and was
  STILL RUNNING at Kam's 17:50 reboot (~14 h). The reboot killed it (`~/Library/Logs/devnas-sync.log`, rc=2).
- During that run unison saw a set of WEDNESDAY paths as "deleted on the NAS side" and propagated those
  deletions (`<---- deleted`) onto DevMASTER. Only WEDNESDAY was affected.
- Lost on DevMASTER: Launch_Wednesday/Cockpit/Tuesday/Friday.command (+ all .pre-* backups), CLAUDE.md,
  PORTABILITY.md, 2_Project_Files/PORTS.md, ~200 tracked files (dashboard-cloud, coordination, voice, doctor.sh.pre-*),
  and ~245k untracked/ignored files (fleet/qa-agent, local-model/runs, coordination/.venv + seat_scratch,
  friday/spark, tools/*, 4_Credentials/.codex + .azure/cliextensions, 1_Project_Definition/Research, scheduler logs/state).
- 0_Brain and 5_Project_History content were NOT lost (only NAS AppleDouble `._*` and old `conflict_on` files differed).

## What was done
1. PAUSED the NAS sync: `launchctl bootout gui/501/com.wednesday.nassync` so it could not push the
   deletions onto the NAS (the NAS was the only full copy of the untracked files). This is why preflight reports
   1 scheduled job missing. It's deliberate. Don't re-arm it until Kam okays it.
2. Restored every deleted TRACKED file from git HEAD (df309a6f7, your 17:48 commit, so it's the newest version).
3. Filled the remaining gaps from the NAS with GNU rsync `--ignore-existing` (it never overwrote a DevMASTER file;
   it skipped `._*`, .DS_Store, .playwright-mcp, .git). Re-check showed 0 files still missing vs NAS; git shows 0 deletions.
4. NAS dates: its WEDNESDAY copy is STALE (0_Brain ~02 Oct, 5_Project_History 03 Oct, Launch_Wednesday 25 Sep,
   CLAUDE.md 08 Sep). DevMASTER/git is the newest, so the NAS was used only to fill missing files and never as a source of truth.
5. Started the cockpit (Launch_Cockpit.command) and accepted the preflight. Its only HARD fail was live_chat_poll
   not running, which is normal on a cold boot after a reboot.

## Things for you to look at
- Some resurrected NAS-only files may have been deliberately deleted on DevMASTER before (e.g. old qa-agent
  scratch, `(conflict_on_…)` files). They were restored because losing data is worse than having clutter. Sweep at leisure.
- Root cause to fix: nassync can run for 14 h and get killed mid-run by a reboot or sleep, and it propagated NAS-side
  "deletions". Consider a pre-flight that aborts if the NAS listing looks incomplete, or a run-time cap, before re-arming.
