#!/bin/bash
# Launch_New_Machine.command — bring a FRESH Mac up as Tuesday's machine (the Datasec seat and every
# Datasec project's dev tooling). Built for the M5 Mac Studio (128 GB) that replaces Kamils-Mac-mini.
#
# Kam, live board 2026-11-09 13:0x, verbatim:
#   "I will be moving you and all datasec dev to a new machine.  This is a new m5 studio 128Gb.  Please
#    create a new launch script in your tuesday folder called launch.New_Machine and install all apps,
#    services, tools etc used for all projects.  I will set up claude cmd but other than that its a new
#    machine"
# Named Launch_New_Machine.command (not launch.New_Machine) because the root folder holds only the
# Launch_*.command launchers (Kam, 2026-09-05; doctor.sh warns on anything else), and .command is what makes
# it double-clickable. Said to Kam on the board in the receipt; his word renames it.
#
# WHAT IT INSTALLS, and where every item came from (measured on Kamils-Mac-mini 2026-11-09 13:1x, not recalled):
#   formulae  = `brew leaves` on the mini + python@3.14 (both on-drive venvs point at it) + rsync (nas_push.sh
#               refuses macOS openrsync) + jq (statusline).
#   apps      = /Applications on the mini (all drag-installed there; installed here as casks, names checked
#               against the Homebrew API the same hour) + NVIDIA Sync (the Spark's ssh alias comes from it).
#   NOT installed, deliberately: .NET (HPSM-POC and the MPS Calculator carry their OWN SDK in
#   <project>/.tools/dotnet, which travels with the drive and is wired by their launchers); Ornith/oMLX/Ollama
#   and TRMNL (Studio-Wednesday only — Kam 2026-09-22 "Ornith is a studio agent. not a Datasec workflow");
#   postgresql@15 (Secuura's pre-push leg only); Tailscale (Kam 2026-09-09: not on Tuesday's machine);
#   bicep and pwsh (not on the mini today: the .ps1 files are Azure Cloud Shell scripts). Claude Code (Kam's).
#
# WHAT IT NEVER DOES: copy, sync, move or delete project data (the drive is plugged in, it is not copied);
# write inside any project under !CODING (rule 1 — it only reads them); restore credentials or tokens
# (they never travel by script); run Kam's June credential bundle (2026-09-09 trap: it restores the DEAD
# Secuura tenant as the default az subscription on a Datasec machine).
#
# Usage:
#   double-click / ./Launch_New_Machine.command   install, asking before every optional or sudo step
#   ./Launch_New_Machine.command --check           measure only, change nothing; exit 1 if anything required is missing
#   ./Launch_New_Machine.command --dry-run         print every action it would take, change nothing
#   ./Launch_New_Machine.command --yes             take the default at the y/N prompts (still stops for passwords/GUI)
# Re-runnable: every step skips what is already present, so a second run is a repair, not a duplicate.
# Log: ~/Library/Logs/tuesday_new_machine_<timestamp>.log (stderr is never discarded).
set -u

MODE="install"; ASSUME_YES=0
for a in "$@"; do
  case "$a" in
    --check)   MODE="check" ;;
    --dry-run) MODE="dry" ;;
    --yes)     ASSUME_YES=1 ;;
    -h|--help) sed -n '2,36p' "$0"; exit 0 ;;
    *) echo "Unknown option: $a (use --check, --dry-run, --yes)" >&2; exit 2 ;;
  esac
done

# ── Self-locate: this file lives in the TUESDAY tree root; the workspace is its parent. ──
SOURCE="${BASH_SOURCE[0]}"
while [ -L "$SOURCE" ]; do
  DIR="$(cd -P "$(dirname "$SOURCE")" && pwd)"; SOURCE="$(readlink "$SOURCE")"
  case "$SOURCE" in /*) ;; *) SOURCE="$DIR/$SOURCE" ;; esac
done
HERE="$(cd -P "$(dirname "$SOURCE")" && pwd)"
WS="$(cd -P "$HERE/.." && pwd)"
DATASEC="$WS/!CODING/Datasec"
PF="$HERE/2_Project_Files"

STAMP="$(date '+%Y%m%d_%H%M%S')"
LOG="$HOME/Library/Logs/tuesday_new_machine_$STAMP.log"
mkdir -p "$HOME/Library/Logs"
exec > >(tee -a "$LOG") 2>&1

# ── Result ledger (bash 3.2: indexed arrays only) ──
RESULTS=(); N_FAIL=0; N_MANUAL=0
rec() { RESULTS+=("$(printf '%-9s %s' "$1" "$2")"); case "$1" in FAIL) N_FAIL=$((N_FAIL+1)) ;; MANUAL) N_MANUAL=$((N_MANUAL+1)) ;; esac; }
hdr() { echo; echo "── $1 ──────────────────────────────────────────────"; }
# run: execute in install mode; print in dry/check mode. Returns the command's rc.
run() {
  if [ "$MODE" = "install" ]; then echo "  \$ $*"; "$@"; return $?; fi
  echo "  [${MODE}] would run: $*"; return 0
}
# ask "<question>" <default y|n> -> 0 for yes. Never asks outside install mode.
ask() {
  [ "$MODE" = "check" ] && return 1
  [ "$MODE" = "dry" ] && { echo "  [dry] would ask: $1 (assuming yes)"; return 0; }
  local d="$2" ans
  if [ "$ASSUME_YES" = 1 ]; then [ "$d" = y ]; return $?; fi
  if [ "$d" = y ]; then read -r -p "  $1 [Y/n] " ans; ans="${ans:-y}"; else read -r -p "  $1 [y/N] " ans; ans="${ans:-n}"; fi
  case "$ans" in y|Y|yes|YES) return 0 ;; *) return 1 ;; esac
}
pause_for() { [ "$MODE" = "install" ] || return 0; read -r -p "  $1 — press Enter when done " _; }

echo "══════════════════════════════════════════════════════════════════"
echo " Tuesday — new machine bring-up   (mode: $MODE)"
echo "══════════════════════════════════════════════════════════════════"
echo "  Tree:      $HERE"
echo "  Workspace: $WS"
echo "  Log:       $LOG"

# ═════ 0. PREFLIGHT ═════════════════════════════════════════════════
hdr "0. Preflight"
if [ "$(id -u)" = 0 ]; then echo "  Do not run this as root (Homebrew refuses root). Run it as Kam."; exit 2; fi
if [ "$(basename "$HERE")" != "TUESDAY" ]; then
  echo "  REFUSED: this script installs Tuesday's machine and must run from the TUESDAY tree (found: $HERE)."; exit 2
fi
ARCH="$(uname -m)"; OSV="$(sw_vers -productVersion 2>&1)"; HOST="$(scutil --get ComputerName 2>&1)"
echo "  Machine:   $HOST · macOS $OSV · $ARCH · $(sysctl -n hw.memsize 2>&1 | awk '{printf "%d GB", $1/1073741824}') RAM"
[ "$ARCH" = "arm64" ] && rec OK "Apple Silicon ($ARCH)" || rec FAIL "architecture is $ARCH — the on-drive venvs and .NET SDKs are arm64"
if [ -d "$DATASEC" ]; then rec OK "workspace present: $(ls -1 "$DATASEC" | wc -l | tr -d ' ') entries under !CODING/Datasec"
else rec FAIL "no !CODING/Datasec under $WS — is the drive plugged in and mounted?"; fi
case "$HERE" in
  /Volumes/Laptop-DEV/TUESDAY) rec OK "mount path unchanged (/Volumes/Laptop-DEV)" ;;
  *) rec WARN "mount path is $HERE, not /Volumes/Laptop-DEV/TUESDAY — stored absolute paths (repo core.sshCommand, plists) must be re-pointed; doctor.sh's travel-pointers check lists them, each project's launcher self-heals its own at first launch" ;;
esac
echo "  Internal disk free: $(df -h / | awk 'NR==2{print $4}')"

# ═════ 1. XCODE COMMAND LINE TOOLS (git, clang) ═════════════════════
hdr "1. Xcode Command Line Tools"
if xcode-select -p >/dev/null 2>&1; then rec OK "Xcode CLT at $(xcode-select -p)"
elif [ "$MODE" = "check" ]; then rec FAIL "Xcode CLT missing"
else
  run xcode-select --install
  [ "$MODE" = "dry" ] && rec PLANNED "xcode-select --install (GUI dialog)"
  if [ "$MODE" = "install" ]; then
    echo "  A macOS dialog has opened: click Install and accept the licence. Waiting (up to 45 min)..."
    i=0; while ! xcode-select -p >/dev/null 2>&1 && [ $i -lt 180 ]; do sleep 15; i=$((i+1)); done
    xcode-select -p >/dev/null 2>&1 && rec INSTALLED "Xcode CLT" || rec FAIL "Xcode CLT still missing after 45 min"
  fi
fi

# ═════ 2. HOMEBREW (the one step that needs Kam's password) ═════════
hdr "2. Homebrew"
BREW=/opt/homebrew/bin/brew
if [ -x "$BREW" ]; then rec OK "Homebrew $("$BREW" --version 2>&1 | head -1)"
elif [ "$MODE" = "check" ]; then rec FAIL "Homebrew missing"
elif [ "$MODE" = "dry" ]; then
  echo "  [dry] would run the official Homebrew installer (https://brew.sh; asks Kam's password)"
  rec PLANNED "Homebrew (official installer, sudo password)"
else
  echo "  Homebrew's installer will ask for your Mac password (sudo). That is expected."
  HBI="$(curl -fsSL https://raw.githubusercontent.com/Homebrew/install/HEAD/install.sh)" || { echo "  could not download the Homebrew installer"; }
  if [ -n "${HBI:-}" ]; then /bin/bash -c "$HBI"; fi
  [ -x "$BREW" ] && rec INSTALLED "Homebrew" || rec FAIL "Homebrew install did not produce $BREW"
fi
[ -x "$BREW" ] && eval "$("$BREW" shellenv)"

# ~/.zprofile: the Homebrew installer does NOT write it (measured on the mini 2026-09-09). Append a marked block once.
ZP="$HOME/.zprofile"; MARK="# >>> tuesday new-machine PATH block"
if [ -f "$ZP" ] && grep -qF "$MARK" "$ZP"; then rec OK "~/.zprofile PATH block present"
elif [ -f "$ZP" ] && grep -qF 'brew shellenv' "$ZP"; then rec OK "~/.zprofile already runs brew shellenv"
elif [ "$MODE" = "check" ]; then rec FAIL "~/.zprofile does not put Homebrew on PATH"
else
  if [ "$MODE" = "install" ]; then
    [ -f "$ZP" ] && cp -p "$ZP" "$ZP.pre-newmachine-$STAMP"
    cat >> "$ZP" <<'ZPEOF'
# >>> tuesday new-machine PATH block (Launch_New_Machine.command)
# Homebrew on Apple Silicon lives at /opt/homebrew and is NOT on the default PATH.
eval "$(/opt/homebrew/bin/brew shellenv)"
# Docker Desktop bundles the CLI + compose v2 here; /usr/local/bin links appear only after its admin prompt.
[ -d "/Applications/Docker.app/Contents/Resources/bin" ] && PATH="$PATH:/Applications/Docker.app/Contents/Resources/bin"
[ -d "$HOME/.docker/bin" ] && PATH="$PATH:$HOME/.docker/bin"
export PATH
# <<< tuesday new-machine PATH block
ZPEOF
    zsh -lc 'command -v brew' >/dev/null 2>&1 && rec INSTALLED "~/.zprofile PATH block (verified in a fresh login shell)" || rec FAIL "~/.zprofile written but a fresh login shell still has no brew"
  else run "append the PATH block to $ZP"; fi
fi

# ═════ 3. COMMAND-LINE TOOLS (formulae) ═════════════════════════════
hdr "3. Command-line tools"
# formula:command-that-proves-it-runs
# formula:command-that-proves-it-runs:required(1)/optional(0)
# jq and rsync are optional because macOS ships working copies (/usr/bin/jq, /usr/bin/rsync = openrsync);
# the brew rsync is needed only by the NAS push leg (nas_push.sh refuses openrsync). Both still get installed.
FORMULAE="azure-cli:az:1 ffmpeg:ffmpeg:1 gh:gh:1 git-crypt:git-crypt:1 gitleaks:gitleaks:1 jira-cli:jira:1 jq:jq:0 node:node:1 pandoc:pandoc:1 poppler:pdftoppm:1 python@3.14:/opt/homebrew/opt/python@3.14/bin/python3.14:1 rsync:/opt/homebrew/bin/rsync:0 tmux:tmux:1 unison:unison:1 uv:uv:1"
# ver <cmd>: print the first meaningful line of a version flag that SUCCEEDS; rc 1 if none does. (No pipe
# inside the test — a `| head -1` would hand back head's rc and the check could never fail.)
ver() {
  local out flag
  for flag in --version -V -v -version version; do   # pdftoppm answers -v; jira-cli only `version`
    if out="$("$1" $flag 2>&1)"; then printf '%s\n' "$out" | grep -v '^WARNING' | grep -m1 .; return 0; fi
  done
  printf '%s\n' "$out" | head -1; return 1
}
for pair in $FORMULAE; do
  f="${pair%%:*}"; rest="${pair#*:}"; c="${rest%:*}"; req="${rest##*:}"
  # Homebrew 7 moved some of these to casks (azure-cli is a cask on the M5 Studio, 2026-11-09): accept either.
  if [ -x "$BREW" ] && { "$BREW" list --formula "$f" >/dev/null 2>&1 || "$BREW" list --cask "$f" >/dev/null 2>&1; }; then have=1; else have=0; fi
  if [ $have = 0 ]; then
    case "$MODE" in
      check) [ "$req" = 1 ] && rec FAIL "$f not installed" || rec WARN "$f not installed (optional; macOS ships $(command -v "$(basename "$c")" 2>/dev/null || echo 'no copy'))"; continue ;;
      dry)   echo "  [dry] would run: brew install $f"; rec PLANNED "brew install $f"; continue ;;
    esac
    [ -x "$BREW" ] || { rec FAIL "$f: no Homebrew"; continue; }
    run "$BREW" install "$f" || { rec FAIL "brew install $f failed (see log)"; continue; }
  fi
  if v="$(ver "$c")"; then
    [ $have = 1 ] && rec OK "$f — $v" || rec INSTALLED "$f — $v"
  else rec FAIL "$f installed but no version flag of '$c' ran: $v"; fi
done
command -v npm >/dev/null 2>&1 && rec OK "npm $(npm --version 2>&1)" || rec FAIL "npm missing (comes with node)"

# ═════ 4. APPS (casks) ══════════════════════════════════════════════
hdr "4. Apps"
install_cask() { # $1 token  $2 app bundle name  $3 required(1)/optional(0)
  local tok="$1" app="$2" req="$3"
  if [ -d "/Applications/$app" ]; then rec OK "$app present"; return; fi
  if [ "$MODE" = "check" ]; then [ "$req" = 1 ] && rec FAIL "$app missing" || rec INFO "$app missing (optional)"; return; fi
  if [ "$req" = 0 ] && ! ask "Install optional app $app?" y; then rec SKIPPED "$app (optional, declined)"; return; fi
  if [ "$MODE" = "dry" ]; then echo "  [dry] would run: brew install --cask $tok"; rec PLANNED "brew install --cask $tok"; return; fi
  [ -x "$BREW" ] || { rec FAIL "$app: no Homebrew"; return; }
  run "$BREW" install --cask "$tok" || { rec FAIL "brew install --cask $tok failed (see log)"; return; }
  if [ -d "/Applications/$app" ]; then
    local sig; sig="$(spctl -a -vv -t exec "/Applications/$app" 2>&1 | tr '\n' ' ')"
    case "$sig" in *accepted*) rec INSTALLED "$app (Gatekeeper: accepted)" ;; *) rec WARN "$app installed but Gatekeeper said: $sig" ;; esac
  else rec WARN "$tok installed but /Applications/$app not found (a pkg installer may name it differently)"; fi
}
install_cask iterm2             "iTerm.app"              1
install_cask google-chrome      "Google Chrome.app"      1
install_cask visual-studio-code "Visual Studio Code.app" 1
install_cask docker-desktop     "Docker.app"             1
install_cask obsidian           "Obsidian.app"           1
install_cask superwhisper       "superwhisper.app"       1
install_cask nvidia-sync        "NVIDIA Sync.app"        0
install_cask brave-browser      "Brave Browser.app"      0
install_cask logi-options+      "logioptionsplus.app"    0

# ═════ 5. DOCKER DESKTOP FIRST LAUNCH ═══════════════════════════════
hdr "5. Docker"
DOCKER="$(command -v docker 2>/dev/null || true)"; [ -z "$DOCKER" ] && [ -x /Applications/Docker.app/Contents/Resources/bin/docker ] && DOCKER=/Applications/Docker.app/Contents/Resources/bin/docker
if [ -n "$DOCKER" ] && "$DOCKER" info >/dev/null 2>&1; then rec OK "Docker daemon answering ($("$DOCKER" --version 2>&1))"
elif [ ! -d /Applications/Docker.app ]; then rec FAIL "Docker Desktop not installed"
elif [ "$MODE" = "install" ]; then
  open -a Docker
  echo "  Docker Desktop is starting: accept its terms (and the helper prompt) on screen. Waiting up to 10 min..."
  DOCKER=/Applications/Docker.app/Contents/Resources/bin/docker; i=0
  while ! "$DOCKER" info >/dev/null 2>&1 && [ $i -lt 60 ]; do sleep 10; i=$((i+1)); done
  "$DOCKER" info >/dev/null 2>&1 && rec INSTALLED "Docker daemon up ($("$DOCKER" --version 2>&1))" || rec MANUAL "Docker Desktop: open it, accept the terms, then re-run --check"
else rec MANUAL "Docker Desktop installed but its daemon is not running (first launch needs Kam's click)"; fi

# ═════ 6. TUESDAY'S OWN MACHINE-LOCAL LAYER (writes only inside this tree) ═
hdr "6. Tuesday tree: modes, hook, venvs"
# 6a exec bits (a copy that drops POSIX modes strips them — PORTABILITY 16/17). The authority is GIT'S OWN
# recorded mode: a file git tracks as 100755 that is not executable on disk lost its bit; a file git tracks
# as 100644 is meant to be plain (measured 2026-11-09: 185 such .sh files, chmodding them would have
# put 185 mode changes into git). Restoring the recorded mode leaves `git status` clean.
NX=""
if [ -d "$HERE/.git" ]; then
  NX="$(git -C "$HERE" -c core.quotePath=false ls-files -s 2>&1 | awk -F'\t' '{split($1,a," "); if (a[1]=="100755") print $2}' | while IFS= read -r f; do [ -e "$HERE/$f" ] && [ ! -x "$HERE/$f" ] && printf '%s\n' "$HERE/$f"; done)"
  NXC="$(printf '%s' "$NX" | grep -c . )"
  if [ "$NXC" = 0 ]; then rec OK "exec bits match git's recorded modes"
  elif [ "$MODE" = "install" ]; then printf '%s\n' "$NX" | while IFS= read -r f; do [ -n "$f" ] && chmod u+x "$f"; done; rec INSTALLED "exec bits restored on $NXC scripts git records as executable"
  elif [ "$MODE" = "dry" ]; then rec PLANNED "chmod u+x on $NXC scripts git records as executable"
  else rec FAIL "$NXC scripts git records as executable have lost the bit"; fi
else rec FAIL "no .git in $HERE — the tree did not come across whole"; fi
# 6b key and .env modes (public .pub keys are meant to be readable and are excluded)
LOOSE="$(find "$HERE/3_Access_Keys" -type f ! -name '*.pub' -perm +044 2>/dev/null; [ -f "$HERE/4_Credentials/.env" ] && find "$HERE/4_Credentials/.env" -perm +044 2>/dev/null)"
LC="$(printf '%s' "$LOOSE" | grep -c . )"
if [ "$LC" = 0 ]; then rec OK "keys and .env are owner-only"
elif [ "$MODE" = "install" ]; then printf '%s\n' "$LOOSE" | while IFS= read -r f; do [ -n "$f" ] && chmod 600 "$f"; done; rec INSTALLED "chmod 600 on $LC key/.env files"
else rec FAIL "$LC key/.env files are group/other-readable (ssh will refuse the deploy key)"; fi
# 6c the repo pre-commit hook (untracked by design; the tracked master is fleet/hooks/pre-commit)
HK="$HERE/.git/hooks/pre-commit"; HM="$PF/fleet/hooks/pre-commit"
if [ -f "$HK" ] && cmp -s "$HK" "$HM"; then rec OK "pre-commit hook matches the tracked master"
elif [ "$MODE" = "install" ]; then [ -f "$HK" ] && cp -p "$HK" "$HK.pre-newmachine-$STAMP"; cp "$HM" "$HK" && chmod +x "$HK" && rec INSTALLED "pre-commit hook from fleet/hooks/pre-commit"
else rec FAIL "pre-commit hook missing or drifted"; fi
# 6d on-drive venvs (they point at /opt/homebrew/opt/python@3.14 — fine once it exists)
for v in "tools/media/.venv:faster_whisper" "coordination/.venv:treequest"; do
  d="${v%%:*}"; m="${v#*:}"
  if [ ! -x "$PF/$d/bin/python" ]; then rec INFO "venv $d not present on this drive"; continue; fi
  if [ "$MODE" = "dry" ]; then rec PLANNED "test venv $d imports $m"; continue; fi
  if out="$("$PF/$d/bin/python" -c "import $m" 2>&1)"; then rec OK "venv $d imports $m"
  else rec WARN "venv $d cannot import $m: $(printf '%s' "$out" | tail -1) — rebuild per PORTABILITY item 9/11"; fi
done

# ═════ 7. PLAYWRIGHT BROWSERS (user cache only — writes nothing in the projects) ═
hdr "7. Playwright browsers"
PWC="$HOME/Library/Caches/ms-playwright"
if ls -d "$PWC"/chromium-* >/dev/null 2>&1; then rec OK "Playwright Chromium in $PWC ($(ls -d "$PWC"/chromium-* | xargs -n1 basename | tr '\n' ' '))"
else
  PWS=""
  for p in "$DATASEC"/*/2_Project_Files; do
    for b in "$p/node_modules/.bin/playwright" "$p/web/node_modules/.bin/playwright"; do [ -x "$b" ] && PWS="$PWS
$b"; done
  done
  PWN="$(printf '%s' "$PWS" | grep -c . )"
  if [ "$PWN" = 0 ]; then rec INFO "no project Playwright binary found; projects install browsers on first test run"
  elif [ "$MODE" = "check" ]; then rec WARN "Playwright browsers not cached; $PWN project binaries could install them"
  elif ask "Install Playwright Chromium for $PWN Datasec projects (downloads to $PWC only)?" y; then
    printf '%s\n' "$PWS" | while IFS= read -r b; do [ -n "$b" ] && run "$b" install chromium; done
    if [ "$MODE" = "dry" ]; then rec PLANNED "playwright install chromium x$PWN"
    elif ls -d "$PWC"/chromium-* >/dev/null 2>&1; then rec INSTALLED "Playwright Chromium"
    else rec WARN "Playwright install ran but no chromium-* in $PWC"; fi
  else rec SKIPPED "Playwright browsers (declined)"; fi
fi
# .NET: per-project, on the drive. Check only.
for p in "HPSM-POC" "Datasec MPS Commercial Calculator"; do
  dn="$DATASEC/$p/.tools/dotnet/dotnet"
  if [ -x "$dn" ] && sdk="$("$dn" --list-sdks 2>&1 | awk '{print $1}' | tr '\n' ' ')"; then rec OK ".NET SDK $sdk in $p/.tools/dotnet (travels with the drive)"
  else rec WARN "$p: no runnable .tools/dotnet — that project's agent reinstalls it (its SETUP_RUNBOOK step 9)"; fi
done

# ═════ 8. SCHEDULED JOBS (launchd) + Full Disk Access ════════════════
hdr "8. Tuesday's scheduled jobs"
IAJ="$PF/scheduler/install_all_jobs.sh"
if WED_AGENT=tuesday bash "$IAJ" --check >/dev/null 2>&1; then rec OK "all com.tuesday.* jobs installed and loaded"
elif [ "$MODE" = "check" ]; then rec FAIL "com.tuesday.* jobs missing (run without --check to install)"
else
  echo "  Arms Tuesday's wake/close/shift-change/chatsync/sweep/escalation jobs on THIS Mac."
  echo "  The old Mac's copies go quiet by themselves once the drive is no longer plugged into it."
  if ask "Install Tuesday's scheduled jobs now?" y; then
    run env WED_AGENT=tuesday bash "$IAJ"
    if [ "$MODE" = "install" ]; then
      WED_AGENT=tuesday bash "$IAJ" --check && rec INSTALLED "com.tuesday.* jobs" || rec FAIL "install_all_jobs.sh --check still reports missing jobs (see log)"
    else rec PLANNED "install_all_jobs.sh for tuesday"; fi
  else rec SKIPPED "scheduled jobs (declined) — run: WED_AGENT=tuesday bash $IAJ"; fi
fi
# Full Disk Access: launchd jobs reading an external drive exit 126 without it, and no prompt ever appears.
CS="$(launchctl print "gui/$(id -u)/com.tuesday.chatsync" 2>/dev/null | awk -F'= ' '/last exit code/{print $2; exit}')"
case "$CS" in
  0) rec OK "launchd jobs can read the drive (chatsync last exit 0)" ;;
  126|*"126"*) rec MANUAL "Full Disk Access for /bin/bash: jobs exit 126" ;;
  *) rec MANUAL "Full Disk Access for /bin/bash (and /opt/homebrew/bin/rsync for the NAS leg): not yet proven — chatsync last exit '${CS:-none yet}'" ;;
esac
if [ "$MODE" = "install" ] && [ "$CS" != 0 ]; then
  echo "  Opening Privacy & Security → Full Disk Access. Click +, press Cmd+Shift+G, type /bin/bash, add it;"
  echo "  repeat for /opt/homebrew/bin/rsync."
  open "x-apple.systempreferences:com.apple.preference.security?Privacy_AllFiles" 2>&1
  pause_for "Grant Full Disk Access to /bin/bash and /opt/homebrew/bin/rsync"
fi

# ═════ 9. NO SLEEP (an agent turn dies when the Mac sleeps — PORTABILITY 19) ═
hdr "9. Sleep"
SL="$(pmset -g 2>&1 | awk '$1=="sleep"{print $2; exit}')"
if [ "$SL" = 0 ]; then rec OK "system sleep is off"
elif [ "$MODE" = "check" ]; then rec WARN "system sleep is ${SL:-unknown} min — running agents die when it sleeps"
elif ask "Turn off system sleep so agent sessions survive the night (sudo pmset -a sleep 0 disksleep 0; asks your password)?" y; then
  run sudo pmset -a sleep 0 disksleep 0 && { [ "$MODE" = "install" ] && rec INSTALLED "system sleep off" || rec PLANNED "pmset sleep 0"; } || rec FAIL "pmset failed"
else rec SKIPPED "sleep settings (declined)"; fi

# ═════ 10. WHAT ONLY KAM CAN DO (GUI, logins, secrets) ═══════════════
hdr "10. Kam's steps (recorded, not automated)"
if command -v claude >/dev/null 2>&1 || [ -x "$HOME/.local/bin/claude" ]; then rec OK "Claude Code present"
else rec MANUAL "Claude Code: install it (Kam). Then launch Launch_Tuesday.command and /login once on this Mac."; fi
if [ -d "$HOME/.ssh" ] && [ -n "$(ls -A "$HOME/.ssh" 2>/dev/null)" ]; then rec OK "~/.ssh has $(ls "$HOME/.ssh" | wc -l | tr -d ' ') entries"
else rec MANUAL "~/.ssh is empty: copy ~/.ssh from the Mac mini (AirDrop/USB), then chmod 700 ~/.ssh; chmod 600 its private keys. Project deploy keys are on the drive and need nothing."; fi
if ssh -G Spark 2>/dev/null | awk '/^hostname /{print $2}' | grep -qv '^spark$'; then rec OK "ssh alias 'Spark' resolves"
else rec MANUAL "NVIDIA Sync: open it and pair with the Spark so 'ssh Spark' works; then: bash $PF/local-model/spark/tunnel.sh check"; fi
rec MANUAL "Voice: System Settings → Accessibility → Spoken Content → Manage Voices → Moira (Enhanced), en_IE (the mini's choice; speak.sh falls back without it)"
rec MANUAL "gh/az: per-project tokens may not survive the move — each project's launcher prompts gh auth login / az login --tenant <its tenant> on first use. Never run the June credential bundle here."
rec MANUAL "Apps: sign in to Chrome, Superwhisper, Obsidian (open the vault at $WS/Notes (MASTER)) as you normally do"

# ═════ 11. VERIFY ═══════════════════════════════════════════════════
hdr "11. doctor.sh (Tuesday)"
if [ "$MODE" = "dry" ]; then rec PLANNED "WED_AGENT=tuesday bash 2_Project_Files/doctor.sh"
else
  DOUT="$HOME/Library/Logs/tuesday_new_machine_${STAMP}_doctor.txt"
  WED_AGENT=tuesday bash "$PF/doctor.sh" > "$DOUT" 2>&1; drc=$?
  W="$(grep -c '⚠' "$DOUT")"; F="$(grep -ciE '✗|FAIL' "$DOUT")"
  echo "  doctor rc=$drc · warnings $W · fail lines $F · full output: $DOUT"
  grep -E '⚠|✗' "$DOUT" | head -25
  [ "$drc" = 0 ] && rec OK "doctor.sh rc 0 ($W warnings)" || rec WARN "doctor.sh rc $drc ($W warnings, $F fail lines) — read $DOUT"
fi

echo
echo "══════════════════════════════════════════════════════════════════"
echo " Summary (mode: $MODE)   FAIL: $N_FAIL   Kam's steps: $N_MANUAL"
echo "══════════════════════════════════════════════════════════════════"
for r in "${RESULTS[@]}"; do echo "  $r"; done
echo
echo "  Next: double-click Launch_Tuesday.command. Repos are refreshed by each launcher; to clone anything"
echo "  missing use $WS/Bootstrap_From_GitHub.command (it needs gh logged in)."
echo "  Log: $LOG"
if [ "$MODE" != "check" ] && [ -t 0 ]; then echo; read -r -n 1 -p "Press any key to close..." _; echo; fi
[ "$N_FAIL" = 0 ]
