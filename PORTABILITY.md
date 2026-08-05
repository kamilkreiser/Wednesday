# Portability checklist — bringing Wednesday up on another Mac

The T9 SSD is the master copy (Kam's rule, 2026-07-31): plug it into any Mac and
everything should be here. These are the ONLY machine-local dependencies; run
through this list on a new machine.

| # | Dependency | On a new Mac | Degrades to |
|---|---|---|---|
| 1 | Claude Code CLI + Kam's login | Install Claude Code, log in to the Max account | Nothing works without it |
| 2 | "Matilda (Premium)" voice (Kam's pick, 2026-07-31) | System Settings → Accessibility → Spoken Content → System Voice → Manage Voices… → English (Australia) → download Matilda (Premium) | speak.sh falls back: Matilda Enhanced → Moira Enhanced → compact Moira (robotic) |
| 3 | Volume name/mount path | Drive must mount as `/Volumes/KK_T9_External_HDD` (default). If renamed, launcher still works (self-locating) but memory notes referencing the path go stale | — |
| 4 | DevMASTER workspace | Optional read-only context; launcher reports "NOT mounted" and continues | Reduced cross-project awareness |
| 5 | git + ssh | Xcode CLT (`xcode-select --install`). Deploy key lives ON the drive (`3_Access_Keys/github_deploy_rw`, gitignored) — no keychain dependency, portable by design | — |
| 6 | Claude Code auto-memory | Lives in `~/.claude` per machine — NOT portable. Wednesday's real memory is `0_Brain/` (on-drive) by design; treat auto-memory as a cache | — |

Keep this file updated whenever a new machine-local dependency appears.
| 7 | `claude` CLI for the coordination harness's claude seat | Install Claude Code on the new machine (`~/.local/bin/claude`); Max login is per-machine | claude seat fails; gpt seat still works |
| 8 | Codex CLI (gpt seat) | ON-DRIVE: binary at `2_Project_Files/tools/codex-cli/`, auth at `4_Credentials/.codex/` (CODEX_HOME) — portable across Apple-Silicon Macs. npm package bundles per-platform binaries; on a different architecture re-run `npm install` in that folder | gpt seat fails until reinstall |
| 9 | Python for the coordination venv | venv at `2_Project_Files/coordination/.venv` is machine-tied (symlinks to system python). Recreate on a new machine: `python3 -m venv .venv && .venv/bin/pip install treequest` (needs Python 3.11+) | harness won't run until recreated |
| 10 | `wednesday` terminal command | Machine-local: `/opt/homebrew/bin/wednesday` (execs the on-drive launcher; fails politely if T9 unmounted). Recreate on a new machine by copying that 6-line script | typed command won't exist until recreated |
| 11 | Media pipeline (course ingestion) | ON-DRIVE: yt-dlp + faster-whisper venv at `2_Project_Files/tools/media/`; whisper model downloads into `tools/media/models/` (on-drive, portable). Needs machine ffmpeg (`brew install ffmpeg`) | transcription fails until ffmpeg installed |
| 12 | Daily-rhythm scheduler (WED-16) | Machine-local: three launchd plists in `~/Library/LaunchAgents` (com.wednesday.shiftchange 05:30 fleet wrap, com.wednesday.wake 06:00, com.wednesday.close 23:00). Re-run `2_Project_Files/scheduler/install_scheduler.command` on the new Mac (plists embed the drive path at install time). Optional for true sleep-wake: `sudo pmset repeat wakeorpoweron MTWRFSU 05:28:00` | no scheduled shift-change/wake/close until installer re-run; scripts guard against odd-hour coalesced fires |

13. **tmux** (machine-local, brew): `brew install tmux` — the fleet cockpit
    engine (2_Project_Files/fleet/cockpit/). Scripts are pure shell + tmux
    CLI and travel with the drive; only the binary is machine-local.
14. **iTerm2** (machine-local, brew cask): `brew install --cask iterm2` —
    the cockpit glass. View: `tmux -CC attach -t fleet`. Optional `it2`
    Python API not currently load-bearing.
15. **Scheduler TCC grant (machine-local, GUI-only — REQUIRED for WED-16):**
    launchd-spawned background jobs are DENIED access to removable volumes by
    macOS TCC (no prompt is ever shown; bash exits 126 "Operation not
    permitted" reading anything on the T9 — diagnosed 2026-08-04 23:4x after
    both scheduled fires failed). One-time fix per machine: System Settings →
    Privacy & Security → Full Disk Access → add `/bin/bash` (or at minimum
    grant it Removable Volumes access), then `launchctl kickstart
    gui/$UID/com.wednesday.close` to verify exit 0. ALSO machine-local:
    launchd stdio logs live at `~/Library/Logs/wednesday_{close,wake}.{out,err}`
    (launchd cannot even open stdio paths on the external drive — plists +
    installer point there since 2026-08-04; the scripts' own logs still land
    on-drive in scheduler/logs/ once execution is possible).
16. **Executable bits on scripts (check after every copy of the project):**
    copying the project through anything that doesn't preserve POSIX
    permissions (cloud-sync round trip, archive extraction, some copy tools)
    strips `chmod +x` from every `.sh`/`.command` file. Symptom: Finder says
    "could not be executed because you do not have appropriate access
    privileges" when double-clicking a launcher (hit 2026-08-05 on
    KK_DEV_Local). Fix from the project root:
    `find . -name "*.sh" -o -name "*.command" | xargs chmod +x`
17. **jq** (statusline dependency) — `tools/statusline.sh` (drive-local copy of
    the DevMASTER shared helper, added 2026-08-05) needs `jq` on each machine:
    `brew install jq`. doctor.sh checks it; missing = statusline degrades to
    the bare `[Wednesday]` label. Launcher refreshes the drive-local copy from
    DevMASTER when mounted and falls back to it when not.
18. **Calendar TCC grant (per machine, per terminal host):** the dashboard's
    `tools/calendar_probe` (EventKit, read-only, compiled on-drive) needs a
    one-time "Allow Full Access" calendar prompt approved on each machine —
    granted on the laptop 2026-08-05; the Studio will prompt on first run.
    doctor.sh warns if the probe can't read calendars.
