# Portability checklist — bringing Wednesday up on another Mac

DevMASTER is the master copy (Kam, 2026-08-25 — one drive for Wednesday and the dev
code; before that the T9 SSD was the master, 2026-07-31 rule). Plug it into any Mac and
everything should be here. These are the ONLY machine-local dependencies; run
through this list on a new machine.

| # | Dependency | On a new Mac | Degrades to |
|---|---|---|---|
| 1 | Claude Code CLI + Kam's login | Install Claude Code, log in to the Max account | Nothing works without it |
| 2 | "Matilda (Premium)" voice (Kam's pick, 2026-07-31) | System Settings → Accessibility → Spoken Content → System Voice → Manage Voices… → English (Australia) → download Matilda (Premium) | speak.sh falls back: Matilda Enhanced → Moira Enhanced → compact Moira (robotic) |
| 3 | Volume name/mount path | Drive must mount as `/Volumes/DevMASTER` (default since 2026-08-25; was `/Volumes/KK_T9_External_HDD`). If renamed, launcher still works (self-locating) but memory notes referencing the path go stale | — |
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

## Tailscale remote dashboard access (added 2026-08-20)
- **Machine-local:** Tailscale.app (v1.98.2 at install), its login state
  (Kam's Apple-ID private-relay identity, tailnet `tail99c01e.ts.net`), and
  the serve config (`--http=80 / → 127.0.0.1:47787`).
- **New machine bring-up:** `brew install --cask tailscale` → open the app,
  log into the SAME tailnet (Kam authenticates — identities float, never
  assume) → `/Applications/Tailscale.app/Contents/MacOS/Tailscale serve --bg
  --http=80 --set-path=/ http://127.0.0.1:47787`.
- **Known limit:** the GUI-app variant starts at LOGIN, not boot — after a
  reboot the dashboard is tailnet-unreachable until someone logs in (same
  window as the WED-117 scheduler gap). doctor.sh warns when the backend is
  not Running. Serve config itself persists across restarts (proven 2026-08-20
  by a down/up cycle).
- HTTP-not-HTTPS is deliberate for v1: traffic rides inside WireGuard; the
  `tailscale serve` HTTPS-cert path hung on the tailnet's cert toggle
  (admin-console setting) and can be upgraded later if Kam enables it.

17. **File modes after a drive sync (found 2026-08-25, DevMASTER relocation):** Kam's
    unison engine (`!SYNC FILES/devnas-sync.sh`, `perms = 0`) does not carry modes, so
    a synced copy lands scripts non-executable AND the deploy key as 0644 — ssh refuses
    the key and every push fails "publickey". After ANY sync into a copy you will run
    from: `chmod 600 3_Access_Keys/* 4_Credentials/.env` and re-set exec bits
    (`doctor.sh` now checks both). `.git` never syncs — seed it once by copy, then it
    lives by git; `core.sshCommand` in `.git/config` names the key by ABSOLUTE path and
    must be re-pointed when the mount path changes (done 2026-08-25 for DevMASTER).

18. **Stale absolute pointers after moving to another drive/machine (found 2026-08-25,
    first travel session — full write-up in
    `0_Brain/learnings/2026-08-25_travel-drive-stale-pointers.md`):** the sync copies
    credentials perfectly but freezes every stored ABSOLUTE PATH pointing at the old
    volume. Four classes found day one: per-project repo `core.sshCommand` (6 repos
    pointing at unmounted DevMASTER + 2 at a drive dead since May; most launchers
    self-heal at launch, Secuura's only with keychain seeded or
    `SECUURA_ALLOW_ONDISK_KEY=1`); `fleet/cockpit/launchers.conf` (fixed permanently —
    cockpit.sh falls back to the running drive); hardcoded facts in collectors; strict
    parser contracts. **Post-sync ritual on the other machine: run `doctor.sh` — its
    `travel-pointers` check sweeps all project repos' core.sshCommand and warns on
    dangling pointers. Route warnings to the projects' own launchers/agents; never edit
    their repos from Wednesday's hands.**

19. **Laptop sleep kills in-flight agent turns (found 2026-08-25 evening — two s66
    wrap-turn deaths, one a 5-hour lid-closed gap):** the Studio never sleeps; the
    laptop defaults to sleeping on lid-close/idle, and every running Claude turn dies
    with "Your computer went to sleep mid-response". On the laptop, arm
    `caffeinate -dims -t <seconds>` alongside any fleet launch (same action, not
    afterwards). Recovery for a slept turn: re-verify the dead turn's writes, then
    mirror mail + resume tap (the 08-24 dead-turn rule).

20. **Case-consistency of replica names BEFORE any sync leg (found 2026-08-26 — the
    2026-08-25 NAS leg deleted six `!CODING/` folders from DevMASTER):** the NAS share's
    real directory is `!CODING/datasec` while DevMASTER/KK_DEV have `Datasec`. macOS SMB
    resolves both spellings to the same folder, unison compares case-sensitively, and the
    profile runs `prefer = newer` with `confirmbigdel = false` — so the "reconciliation"
    is a mass delete. Before "Sync All Drives" (or any single leg): diff the REAL names
    (`python3 -c 'import os; print(sorted(os.listdir(r)))'` per replica root and per
    `!CODING/`), and after every leg grep its log for `[BGN] Deleting` before trusting
    `Sync finished`. A leg cut by a shutdown writes no summary — read the body. Learning:
    `0_Brain/learnings/2026-08-26_a-sync-that-cannot-refuse-a-deletion.md`. The NAS leg
    stays OFF until the case is fixed (Kam's card `nas-case-fold-datasec`).
