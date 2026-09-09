# Portability checklist — bringing Wednesday up on another Mac

DevMASTER is the master copy (Kam, 2026-08-25 — one drive for Wednesday and the dev
code; before that the T9 SSD was the master, 2026-07-31 rule). Plug it into any Mac and
everything should be here. These are the ONLY machine-local dependencies; run
through this list on a new machine.

| # | Dependency | On a new Mac | Degrades to |
|---|---|---|---|
| 1 | Claude Code CLI + Kam's login | Install Claude Code, log in to the Max account | Nothing works without it |
| 2 | "Matilda (Premium)" voice (Kam's pick, 2026-07-31) | System Settings → Accessibility → Spoken Content → System Voice → Manage Voices… → English (Australia) → download Matilda (Premium). **macOS 26.6 (2026-09-02): the pane did not show the download option on the new laptop — try System Settings → Accessibility → Read & Speak → System Voice → Manage Voices, or skip; the fallback chain works** | speak.sh falls back: Matilda Enhanced → Moira Enhanced → compact Moira (robotic) |
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
| 12 | Daily-rhythm scheduler (WED-16) | Machine-local: three launchd plists in `~/Library/LaunchAgents` (com.wednesday.shiftchange 05:30 fleet wrap, com.wednesday.wake 06:00, com.wednesday.close 23:00). Re-run `2_Project_Files/scheduler/install_scheduler.command` **from the drive** on the new Mac (plists embed the drive path at install time). ⚠️ **AND RE-RUN IT WHENEVER THE DRIVE'S MOUNT PATH CHANGES ON AN EXISTING MACHINE — this item said “on the new Mac” only, and that omission is what bit on 2026-09-07:** the plists were installed 2026-09-02 pointing at `/Volumes/KK_DEV_Local/…`, the drive later mounted elsewhere, and all three jobs failed every fire with exit 127 for two days while `doctor.sh` ticked them green. **doctor now stats the plist's script path and warns by name (fixed 2026-09-08), so this can no longer be silent.** Kam ruled 2026-09-08: leave dead jobs dead, re-install on the target machine as a bring-up step — never re-arm session-spawning jobs mid-migration. Optional for true sleep-wake: `sudo pmset repeat wakeorpoweron MTWRFSU 05:28:00` | no scheduled shift-change/wake/close until installer re-run; scripts guard against odd-hour coalesced fires |

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
21. **Report PDFs — md2pdf deps (added 2026-08-28):** `2_Project_Files/tools/md2pdf/md2pdf.sh`
    renders every report in the house style Kam asked to keep ("The PDF looks great. Keep
    this style going forward"). Machine-local: `pandoc` (brew), **Google Chrome** (headless
    print-to-pdf), `pdftoppm` (brew `poppler`, for the eyeball raster). doctor.sh warns when
    any is missing. Fallback if Chrome is absent: `soffice --headless --convert-to pdf` on
    the pandoc HTML (uglier, still a PDF).

## New-Mac bring-up, done end to end (2026-09-02 — Kam's laptop died; replacement MacBook Pro from the KK_DEV_Local travel drive)

The order that worked, so the next dead machine costs an hour, not an evening. Items 1–21
above are the per-dependency detail; this is the run-sheet.

1. **Already there on a firmware-fresh Mac with Kam's Apple ID:** Xcode (so git/CLT), Chrome,
   Brave, Claude.app + `~/.local/bin/claude`, Superwhisper, Office, `jq` (macOS 26 ships it).
   Python is the system 3.9 — not enough for the venvs (item 9/11).
2. **Homebrew needs Kam's password** — the only sudo step. `/bin/bash -c "$(curl -fsSL
   https://raw.githubusercontent.com/Homebrew/install/HEAD/install.sh)"` in a Terminal window
   he can type into (an agent's shell has no TTY for the prompt; opening the window for him via
   `osascript … do script` worked). Then `eval "$(/opt/homebrew/bin/brew shellenv)"` in
   `~/.zprofile`.
3. **GUI apps that need NO password** (download + copy into /Applications, clear quarantine):
   Docker Desktop (`desktop.docker.com/mac/main/arm64/Docker.dmg`), iTerm2
   (`iterm2.com/downloads/stable/latest`), VS Code
   (`update.code.visualstudio.com/latest/darwin-arm64/stable`), Obsidian (GitHub releases —
   the `latest` release is the ANDROID apk; take the newest release whose asset ends in `.dmg`;
   the DMG mounts with a space in its volume name).
4. **Brew formulae, non-interactive:** `node gh azure-cli unison tmux pandoc poppler ffmpeg
   python@3.14 uv git-crypt` — ~4 min. `python@3.14` is what BOTH on-drive venvs
   (`tools/media/.venv`, `coordination/.venv`) point at via `/opt/homebrew/opt/python@3.14`;
   once it exists they work unchanged (proven: faster_whisper + treequest import).
5. **Tailscale is a pkg cask = sudo:** `brew install --cask tailscale-app` in Kam's Terminal.
   First launch then needs TWO GUI approvals — the VPN configuration, then Log in to the
   tailnet (`tail99c01e.ts.net`; the Studio is `mac-studio`). Until both, the CLI BLOCKS
   (doctor's call is now bounded to 4 s).
6. **Docker first launch:** `open -a Docker`, Kam accepts the terms + helper prompt; the
   `/usr/local/bin/docker` symlink appears after that. Fallback added to `~/.zprofile`:
   `PATH=$PATH:/Applications/Docker.app/Contents/Resources/bin` (compose v2 is bundled there).
7. **`wednesday` command:** `/opt/homebrew/bin/wednesday` recreated (execs the launcher on
   DevMASTER, else KK_DEV_Local, else fails politely).
8. **Kam's own credential bundle:** `Setup and System/Machine_Credentials/install_credentials.command`
   (his 2026-06-10 design; interactive passphrase prompts → he double-clicks it). Captured
   tokens age — expect `gh auth login` / `az login` afterwards.
9. **Still GUI-only, per machine:** Matilda Premium voice (item 2); scheduler + its TCC grant
   (items 12/15) — installed on the laptop 2026-09-02 on Kam's word: installer → first kickstart
   exits 126 → Full Disk Access for `/bin/bash` (System Settings → Privacy & Security → Full Disk
   Access → + → Cmd+Shift+G `/bin/bash`) → re-kickstart exits 0 and the on-drive log shows the
   script ran. Known consequence: with the travel drive in the laptop at home at 06:00, the
   laptop AND the Studio each boot a Wednesday; unmounted drive = the laptop's jobs no-op.
   Calendar TCC was already granted on this machine.
10. **Verify:** `doctor.sh` (now also checks node/npm/gh/az/unison/docker), then
    `git -C WEDNESDAY pull --rebase` (the drive's repo lags origin by the Studio's last commits;
    stash the sync churn first — never drop it).

## Machine-local: the repo pre-commit hook (added 2026-09-02 19:4x)

`.git/hooks/pre-commit` (untracked by design) carries TWO refusals: the 2026-08-04 artifact
classes (`__pycache__`/`.pyc`/`.pkl`/`logs/`/`state/`/`out*/`/`seat_scratch/`/`node_modules/`)
and, since 2026-09-02 (ledger w=5, conflict markers reached origin twice in one day through a `;`
chain), **any staged text file carrying a `<<<<<<< ` / `=======` / `>>>>>>> ` line**. After any
fresh clone or a `.git` that did not travel, re-create it.

**SUPERSEDED 2026-09-08 — there is now a TRACKED master copy, so this is one command:**

    cp 2_Project_Files/fleet/hooks/pre-commit .git/hooks/pre-commit && chmod +x .git/hooks/pre-commit

The old instruction ("copy the body from the Studio, or from the 2026-08-04 history entry plus
the 2026-09-02 daily note") asked a stranded seat to reconstruct a guard from a month-old commit
message — a mechanism recorded by its story rather than its path. `doctor.sh` now warns when the
hook is missing AND when it has DRIFTED from the tracked master, because an armed-looking hook
that no longer matches is worse than an absent one. Exercised in all four states 2026-09-08.

---

## Kamils-Mac-mini — Tuesday's machine, brought up 2026-09-09 (what is machine-local HERE)

**This is the record of an actual bring-up, so the next one is a checklist and not an investigation.**
Fresh macOS 27.0 install, arm64. `doctor.sh` went **19 warnings -> 3**. Kam's hands were needed
exactly ONCE.

**The only step that needed his password:** the Homebrew installer. An agent shell has no TTY for a
sudo prompt, so this is his by construction, not by policy:
`/bin/bash -c "$(curl -fsSL https://raw.githubusercontent.com/Homebrew/install/HEAD/install.sh)"`

**`~/.zprofile` DID NOT EXIST and the Homebrew installer does not create it.** It prints the
instruction and leaves it. Without it `brew` and everything it installs vanish from PATH at the next
shell. Written 2026-09-09 with `eval "$(/opt/homebrew/bin/brew shellenv)"` plus the Docker bundle-path
fallback, and **verified by sourcing a fresh login shell** rather than by reading it back.

**Installed by Homebrew (all verified by RUNNING them, not by brew's exit code):** `node` 26.8.1 ·
`npm` 11.19.0 · `gh` 2.100.0 · `az` 2.90.0 · `unison` · `tmux` · `pandoc` 3.11 · `poppler` ·
`ffmpeg` 9.0.1 · `uv` 0.12.10 · `git-crypt` 0.8.0 · `python@3.14` (3.14.7 — what both on-drive venvs
point at).

**GUI apps installed WITHOUT a password — `/Applications` is admin-writable, so an agent can do these:**
Superwhisper 2.18.3 · iTerm2 3.7.0 · VS Code · Google Chrome · Docker Desktop · Obsidian 1.13.7.
**Every one had `spctl -a -vv -t exec` run against it BEFORE the copy** — all returned
`accepted / Notarized Developer ID`. Verify before installing, never after.
**Superwhisper's download URL is not in its web page** (JS app). Get it from the Homebrew cask API
instead — `https://formulae.brew.sh/api/cask/superwhisper.json` gives the exact build URL and the
target app name. Ask the resolver, not the text.

**Voice:** Matilda is NOT available on this machine and the System Voice picker shows a short list.
The fuller list is **System Settings -> Accessibility -> Spoken Content -> (i) beside System Voice ->
Manage Voices**. Kam chose **Moira**, then installed **Moira (Enhanced)** (en_IE) on 2026-09-09;
`speak.sh`'s fallback chain selects it automatically. Doctor's `Matilda Premium not downloaded`
warning is therefore EXPECTED on this machine.

**Scheduler:** `install_scheduler.command` is agent-aware from 2026-09-09 (Kam ruled `parameterise`).
Run it with `WED_AGENT=tuesday`; it refuses an unknown agent and refuses if the matching
`Launch_<Agent>.command` is absent. It arms `com.tuesday.shiftchange/.wake/.close/.nassync` and
**writes `WED_AGENT` into each plist**, because launchd does NOT inherit the environment and a correct
label with a defaulting script still boots the wrong seat.
**Known collision, unresolved and Kam's:** `com.tuesday.close` and `com.tuesday.nassync` both fire at
**23:00** — his "sync at 11pm" predates Tuesday having a close ritual at all. 23:30 for the sync is
the recommendation; his time was left alone.

**Docker:** the first launch prompts are Kam's. Docker Desktop **no longer creates
`/usr/local/bin/docker`** unless the optional admin prompt is accepted; the CLI lives in the app
bundle and reaches PATH only through `~/.zprofile`. `doctor.sh` was corrected 2026-09-09 to ask
Docker itself (daemon probe) rather than to test PATH.

🔴 **THE TRAP THIS MACHINE TAUGHT — read before running `install_credentials.command` anywhere.**
The bundle restores CONFIG, never tokens (Keychain does not sync), and it was captured **2026-06-10**,
so `gh` and `az` come back UNAUTHENTICATED — expected, not broken. Worse: **the June bundle predates
the 2026-06-25 Secuura decommission, so it restored the DEAD tenant `4012a4e8…` as the default
subscription in `~/.azure`, and `kksecura` as the global `gh` account — onto a Datasec-only machine.**
Both were inert (no valid token). The seat was unaffected because the launcher scopes
`AZURE_CONFIG_DIR` / `GH_CONFIG_DIR` to `4_Credentials/`, which is that pattern earning its keep.
**Cause and durable fix:** [[0_Brain/learnings/2026-09-09_quarantine-by-rename-is-not-removal-on-an-additive-sync]]
— quarantine by MOVING into an ignored directory, and fix the BUNDLE, not the machine, or the next
restore repeats it.

**Deliberately NOT on this machine:** Tailscale (Kam, 2026-09-09: *"no tailscale needed on this
machine for now"*) — so the mini is LAN-reachable only. Office, Brave, and the Matilda voice are also
absent; none is needed by the fleet.

**Still GUI-only and still Kam's, unchanged from the run-sheet:** the scheduler's Full Disk Access
grant for `/bin/bash`, Calendar TCC, auto-login and sleep settings for headless use.

## Headless second agent (TUESDAY) — bring-up (added 2026-09-08, Kam's two-machine commission)

**Read `0_Brain/tasks/FIRST-BOOT-TUESDAY.md` first — it is what SHE reads. This is what KAM does.**

🔴 **CORRECTED 2026-09-09 08:0x by Tuesday's first boot, by measurement.** This section used to
open *"the machine is a Time Machine restore of the Studio, so items 1–9 of the run-sheet above
are already satisfied."* **On the machine that actually arrived — `Kamils-Mac-mini`, macOS 27.0,
arm64 — that is false in every part.** Kam's own words at 07:5x: *"this is a new machine freshly
installed."* Measured in the same action as this sentence: **no Homebrew** (`/opt/homebrew` absent),
**no node, npm, gh, az, tmux, unison, docker, pandoc, poppler**, python is the system **3.9.6** (the
venvs need `python@3.14`), and **`/Applications` held only `Claude.app`, `Safari.app` and
`Utilities`** — no Chrome, no Office, no Superwhisper. Xcode CLT and Apple git 2.54.0 WERE present,
and `jq` ships with the OS; those two lines of item 1 survive.

**So the rule is: do not assume the restore happened.** A bring-up section whose first sentence
asserts a provenance ("this machine is a restore of X") is asserting a fact about hardware nobody
has measured — and it silently excuses the next reader from running items 1–9. **Run `doctor.sh`
FIRST and let it tell you which of items 1–9 are actually satisfied on the machine in front of you;
it checks node/npm/gh/az/unison/docker/tmux/homebrew by name.** On 2026-09-09 it printed 19
warnings on a machine this file called ready.

**The full run-sheet above (items 1–10) therefore APPLIES on a fresh install.** What follows is
what is Tuesday-specific ON TOP of it — the gaps that exist whether the machine was restored or
built from nothing:

1. **The drive.** Tuesday's tree is `/Volumes/KK_T9_External_HDD/TUESDAY` (2.1 GB, provisioned
   2026-09-08). It is a working copy of the SAME repo — not a fork — so it pulls and pushes to
   `kamilkreiser/Wednesday` like any other clone.
2. **Her Claude account — the only true blocker, and only Kam can do it.** The keychain entry is
   machine-local; the config dir travels, the secret does not.

       CLAUDE_CONFIG_DIR=/Volumes/KK_T9_External_HDD/TUESDAY/4_Credentials/.claude claude

   then `/login` with the **Datasec** Claude account. Once per machine per agent. Tested
   2026-09-08: an empty config dir answers *"Not logged in · Please run /login"* and builds its
   own `.claude.json`/`projects`/`sessions`, so the namespaces are genuinely separate.
3. **Launch her with `Launch_Tuesday.command`** in that folder — never `Launch_Wednesday.command`,
   which would boot her as Wednesday, reading Wednesday's ledger and Wednesday's inbox. (The
   hostname map is only a fallback; the launcher FILE is what decides.)
4. **Her credentials are deliberately narrow.** She holds the shared fleet keys only (Linear WED
   workspace, AgentMail). **She does NOT hold `MSGRAPH_*`** for the Datasec mailbox/calendar —
   arguably hers, but moving a client's credentials into a seat is Kam's call and it is still open.
   She does not hold the other client's calendar feed and never should.
5. **Her inbox is `tuesday-agent@agentmail.to`** (created 2026-09-08). `inbox_digest.sh` and her
   boot prompt are keyed on the agent, so she never polls Wednesday's.
6. **The `.git/hooks/pre-commit` gap applies to her** — see the section above; one command.
7. **Verify the ssh pointer heals.** Her `.git/config` inherited a key path under `/Volumes/DevMASTER`.
   With DevMASTER unmounted (the normal state on her machine) the launcher rewrites it to her own
   tree's key at boot and prints `[repo] HEALED core.sshCommand`. If DevMASTER happens to be
   mounted the pointer resolves and the heal correctly does nothing.
8. **Headless specifics, all GUI, all Kam's:** auto-login ON (Tailscale's GUI variant starts at
   LOGIN, not boot — without auto-login the machine is unreachable after a reboot) · sleep OFF ·
   Screen Sharing ON so a monitor is optional · ~~Tailscale's two approvals and tailnet login~~ ·
   Matilda Premium voice · Calendar TCC if she is to read one · Docker's first-launch prompts.

   🔴 **TAILSCALE RULED OUT 2026-09-09 by Kam, verbatim: *"no tailscale needed on this machine
   for now."*** So `doctor.sh`'s `⚠ Tailscale.app missing` on `Kamils-Mac-mini` is an EXPECTED
   state, not an open gap — **do not re-raise it, and do not install it on this machine without
   his word.** `doctor.sh` is a shared file both seats run and Tailscale IS wanted on the Studio,
   so the check was deliberately left alone rather than suppressed.

   **What his ruling costs, stated so he can correct it in seconds rather than discover it:**
   Tailscale was the remote-access path for this box. Without it the mini is reachable only on
   the local network (Screen Sharing / SSH over LAN), so **if it is ever run genuinely headless
   and away from Kam, there is no way in.** That is the condition that reopens this — not a date.
   *"For now"* is his scope word and it carries no expiry he set
   ([[0_Brain/learnings/2026-09-06_a-scoped-override-carries-its-own-expiry]]); the trigger to ask
   again is **"this machine needs to be reached from outside the LAN"**, and nothing else.
9. **She does NOT serve a dashboard.** Kam asked for one website; it is served from the Studio and
   her stream renders there under the TUESDAY toggle. `WED_DASHBOARD=1` overrides that if a lone
   Tuesday machine ever genuinely needs its own.
10. **The travel case, which is the weak one.** Both agents from one drive on one machine: the
    physical separation disappears and only `pathguard.py` remains — and it gates WRITES, never
    reads. Test it deliberately before relying on it: run both seats from the single drive and
    verify the toggle still separates them, the guard still refuses, and neither corrupts the
    other's chat stream.

## Nightly NAS sync (added 2026-09-08, s153 — Kam's 14:57 commission)

11. **The launchd job is MACHINE-LOCAL and does not travel.** `com.wednesday.nassync` fires
    `2_Project_Files/scheduler/nas_sync.sh` at **03:30** on the Studio; Tuesday's machine gets
    `com.tuesday.nassync` at **23:00**. Both are installed by the same self-locating
    `scheduler/install_scheduler.command`, which picks the hour from `WED_AGENT` and puts the agent
    in the label so two machines cannot collide in `launchctl`. **On any new machine, or after any
    drive move, re-run that installer** — the plists point at absolute on-drive paths and a stale
    one fires a script that is not there. `doctor.sh` sweeps the job for this seat's agent and warns
    if it is not loaded (exercised both ways 2026-09-08).
12. **`confirmbigdel = true` lives in Kam's file, not this repo** —
    `/Volumes/DevMASTER/!SYNC FILES/devnas.prf`, changed on his explicit authorisation 2026-09-08
    15:37, backup beside it as `.pre-confirmbigdel-2026-09-08`. **It is not carried by this repo and
    it is not carried by the drive sync** (`!SYNC FILES` syncs, but a fresh workspace built any
    other way will not have it). **Check it on any new workspace:** with `batch = true` it ABORTS the
    run on a whole-replica delete, which is the whole point of an unattended job. Its honest scope:
    whole-replica only — the gradual case is `nas_sync.sh`'s deletion alarm.
13. **The alarm's recovery path is per-machine.** Deleted files land in `~/.unison/backup` on
    whichever Mac ran the leg (`backup = Name *`, `maxbackups = 5`, `backuploc = central`) — **not on
    the drives**. So a deletion propagated from Tuesday's machine is recoverable only there. Worth
    knowing before assuming the T9 holds a copy.
