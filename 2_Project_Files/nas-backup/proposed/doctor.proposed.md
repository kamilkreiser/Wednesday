# PROPOSED block for `2_Project_Files/doctor.sh` (nothing here is applied)

Where: after the "NAS replica staleness" block (ends near line 548), before the next section. It uses the helpers doctor already has (`ok`, `warn`, `_DOC_AGENT`, `PROJECT_DIR`).

Why doctor: it is one of the three callers of the three-day check that run on their own clock (launcher boot, doctor, the nightly job). A backup job that never fires cannot report itself (2026-09-20 lesson).

```
# --- Nightly copy-only NAS backup (WED-170, Kam 2026-11-27) ---
# The three-day check reads only nas-backup/state/<seat>.json and the clock: it needs neither the NAS nor the job.
NB_DIR="$PROJECT_DIR/2_Project_Files/nas-backup"
if [ ! -x "$NB_DIR/nas_backup_watch.sh" ]; then
  warn "nas-backup/nas_backup_watch.sh missing or not executable" "restore it from git (chmod +x): without it a backup that stopped is invisible"
else
  NB_OUT="$(bash "$NB_DIR/nas_backup_watch.sh" --check 2>&1)"; NB_RC=$?
  NB_LINE="$(printf '%s\n' "$NB_OUT" | head -1)"
  if [ -e "$NB_DIR/HOLD_${_DOC_AGENT}" ]; then
    warn "nightly NAS backup HELD (by design: nas-backup/HOLD_${_DOC_AGENT})" "do NOT lift it yourself; lifting is the coordinator's word on Kam's instruction"
  elif [ "$NB_RC" -eq 3 ]; then
    warn "NO GOOD NAS BACKUP FOR 3 DAYS" "$NB_LINE — run: bash 2_Project_Files/nas-backup/nas_backup_watch.sh --flag  (it prints the ONE card for Kam; no backup runs outside the window without his word)"
  elif [ "$NB_RC" -ne 0 ]; then
    warn "nas_backup_watch.sh exited $NB_RC" "$NB_LINE"
  else
    ok "nightly NAS backup: $NB_LINE"
  fi
  # the job itself (machine-local): loaded, and its last exit
  if [ ! -e "$NB_DIR/HOLD_${_DOC_AGENT}" ] && [ -f "$PROJECT_DIR/2_Project_Files/scheduler/jobs/nasbackup.plist.template" ]; then
    if launchctl print "gui/$(id -u)/com.${_DOC_AGENT}.nasbackup" >/dev/null 2>&1; then
      NB_LEC=$(launchctl print "gui/$(id -u)/com.${_DOC_AGENT}.nasbackup" 2>/dev/null | awk '/last exit code/{print $NF}')
      case "$NB_LEC" in
        126) warn "nasbackup job last exit 126" "TCC: /bin/bash lacks Full Disk Access on this machine (PORTABILITY 15)";;
        78*) warn "nasbackup job last exit $NB_LEC" "EX_CONFIG: launchd refused the plist; out/err must live in ~/Library/Logs (PORTABILITY 22)";;
        7)   warn "nasbackup job last exit 7 (STALLED)" "a macOS privacy prompt for rsync or python3 is probably waiting on this Mac's screen (PORTABILITY 15a)";;
        *)   ok "nasbackup job loaded (last exit ${NB_LEC:-never})";;
      esac
    else
      warn "nasbackup job not loaded" "bash 2_Project_Files/scheduler/install_all_jobs.sh (from this seat's own tree, WED_AGENT unset)"
    fi
  fi
fi
# the engine dependency (already listed for nas_push.sh): Homebrew rsync 3
[ -x /opt/homebrew/bin/rsync ] || warn "Homebrew rsync missing" "brew install rsync — nas-backup refuses without rsync 3 (PORTABILITY)"
```

Note: the two `>/dev/null 2>&1` on `launchctl print` copy the form the existing per-job sweep uses (doctor.sh lines 503 to 505) to test presence only; every other call keeps its output.

Rollback: remove the block (take `doctor.sh.pre-<date>-nasbackup` first, by this project's convention). Nothing else reads it.

Exercise both paths before trusting it (2026-08-06 lesson): with a state file whose `last_good.time` is 80 hours old the block must WARN; with a fresh one it must print ok. `tests/run.sh` T8 and T9 exercise the script underneath; the doctor block itself is NOT tested (it does not exist yet).
