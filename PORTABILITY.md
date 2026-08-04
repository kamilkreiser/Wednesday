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
| 12 | Daily-rhythm scheduler (WED-16) | Machine-local: two launchd plists in `~/Library/LaunchAgents` (com.wednesday.wake 06:00, com.wednesday.close 23:00). Re-run `2_Project_Files/scheduler/install_scheduler.command` on the new Mac (plists embed the drive path at install time). Optional for true sleep-wake: `sudo pmset repeat wakeorpoweron MTWRFSU 05:58:00` | no scheduled wake/close until installer re-run; scripts guard against odd-hour coalesced fires |
