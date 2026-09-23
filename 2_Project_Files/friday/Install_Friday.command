#!/bin/bash
# Install_Friday.command — the ONE file Kam downloads to set up FRIDAY on his laptop.
#
# Kam, live board 2026-09-23 10:49:26 (verbatim): "…create a folder for Friday with all the instructions
# and a launch file so that when I click that launch file the first time it goes through the configuration
# process, asks me for the relevant logins and configures itself pulling down from GitHub all the files it
# needs for the newly configured Friday launcher… Once it's ready, create one file that I can download and
# install onto this machine for that…"
#
# WHAT IT DOES, in order (nothing is deleted, anything already done is skipped):
#   1. asks where the FRIDAY folder should go (it must be named FRIDAY — that name is what tells the
#      shared launcher which seat it is);
#   2. signs you in to GitHub as the account that owns the Wednesday repo (kamilkreiser), in a login
#      space that belongs to Friday alone — your other GitHub logins on this Mac are not touched;
#   3. downloads the repo into FRIDAY/, and moves that login into FRIDAY/4_Credentials/;
#   4. installs Friday's live-board certificate from this download into FRIDAY/4_Credentials/;
#   5. starts FRIDAY/Launch_Friday.command, which runs the first-time setup (the logins) and then Friday.
# It contains NO passwords or keys. The certificate it installs travels BESIDE it in the download.
#
# macOS bash 3.2 compatible.
set -u
REPO="kamilkreiser/Wednesday"
HERE="$(cd -P "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
say()  { printf '%s\n' "$*"; }
ok()   { say "  ✓ $*"; }
warn() { say "  ⚠ $*"; }
die()  { say ""; say "  ✗ $*"; say ""; printf 'Press Enter to close… '; read -r _; exit 1; }

clear
say "=============================================================="
say "  FRIDAY — installer"
say "=============================================================="
say ""

# ── 1. Where ──────────────────────────────────────────────────────────────────────────────────
DEFAULT_PARENT="$HOME"
for c in /Volumes/DevMASTER /Volumes/KK_DEV_Local; do [ -d "$c/!CODING" ] && { DEFAULT_PARENT="$c"; break; }; done
say "Where should the FRIDAY folder go? (the folder that CONTAINS it)"
printf '  Parent folder [%s]: ' "$DEFAULT_PARENT"; read -r PARENT
PARENT="${PARENT:-$DEFAULT_PARENT}"
PARENT="${PARENT%/}"
[ -d "$PARENT" ] || die "'$PARENT' does not exist."
TARGET="$PARENT/FRIDAY"

if [ -d "$TARGET/.git" ]; then
  ok "FRIDAY is already installed at $TARGET — going straight to its launcher."
  exec bash "$TARGET/Launch_Friday.command"
fi
if [ -e "$TARGET" ] && [ -n "$(ls -A "$TARGET" 2>/dev/null)" ]; then
  die "$TARGET exists and is not empty (and is not a Friday install). Move it aside, or choose another parent."
fi

# ── 2. Tools needed to download ───────────────────────────────────────────────────────────────
command -v git >/dev/null 2>&1 || die "git is missing. Run:  xcode-select --install   then run this installer again."
if ! command -v gh >/dev/null 2>&1; then
  if command -v brew >/dev/null 2>&1; then
    say "GitHub CLI (gh) is missing — installing it with Homebrew…"; brew install gh || die "brew install gh failed (output above)."
  else
    die "GitHub CLI (gh) is missing and Homebrew is not installed. Install Homebrew (https://brew.sh), then: brew install gh"
  fi
fi

# ── 3. Sign in (Friday's own login space) ─────────────────────────────────────────────────────
BOOT_GH="$HOME/.friday-bootstrap/gh-config"
mkdir -p "$BOOT_GH"; chmod 700 "$HOME/.friday-bootstrap" "$BOOT_GH"
say ""
say "Signing in to GitHub. Use the account that owns the Wednesday repo (kamilkreiser)."
if ! GH_CONFIG_DIR="$BOOT_GH" gh auth status >/dev/null 2>&1; then
  GH_CONFIG_DIR="$BOOT_GH" gh auth login --hostname github.com --git-protocol https --web || die "GitHub sign-in did not complete."
fi
WHO="$(GH_CONFIG_DIR="$BOOT_GH" gh api user -q .login 2>&1)"
if ! GH_CONFIG_DIR="$BOOT_GH" gh api "repos/$REPO" -q .full_name >/dev/null 2>&1; then
  die "Signed in as '$WHO', which cannot see $REPO. Run this again and sign in as kamilkreiser:  GH_CONFIG_DIR=$BOOT_GH gh auth logout"
fi
ok "signed in as $WHO — can see $REPO"

# ── 4. Download ───────────────────────────────────────────────────────────────────────────────
say ""; say "Downloading Friday into $TARGET (a few minutes — the repo is large)…"
GH_CONFIG_DIR="$BOOT_GH" gh repo clone "$REPO" "$TARGET" || die "the download failed (output above). Nothing else was changed."
ok "downloaded ($(git -C "$TARGET" rev-parse --short HEAD))"
git -C "$TARGET" check-ignore -q "4_Credentials/.env" || die "safety check failed: 4_Credentials/ is not git-ignored in the download. Stopping before any login is stored there."
mkdir -p "$TARGET/4_Credentials"; chmod 700 "$TARGET/4_Credentials"
if [ ! -e "$TARGET/4_Credentials/.gh-config" ]; then
  mv "$BOOT_GH" "$TARGET/4_Credentials/.gh-config" && ok "GitHub login moved into FRIDAY/4_Credentials/.gh-config"
fi
# Pushes use Friday's own login, set for THIS repo only (never the Mac's global git config):
# the empty helper first cancels any inherited one (e.g. the macOS keychain), then gh supplies the token.
git -C "$TARGET" config --replace-all credential.https://github.com.helper ""
git -C "$TARGET" config --add credential.https://github.com.helper "!GH_CONFIG_DIR='$TARGET/4_Credentials/.gh-config' gh auth git-credential"
git -C "$TARGET" config user.name  "Kam Kreiser"
git -C "$TARGET" config user.email "kreiser.org@me.com"
# The repo's commit guard lives in a tracked master; a fresh clone does not carry .git/hooks.
if [ -f "$TARGET/2_Project_Files/fleet/hooks/pre-commit" ] && [ ! -f "$TARGET/.git/hooks/pre-commit" ]; then
  cp "$TARGET/2_Project_Files/fleet/hooks/pre-commit" "$TARGET/.git/hooks/pre-commit" && chmod +x "$TARGET/.git/hooks/pre-commit" \
    && ok "commit guard installed (.git/hooks/pre-commit)"
fi

# ── 5. The live-board certificate that came in this download ──────────────────────────────────
DC="$TARGET/4_Credentials/dashboard-cloud"; mkdir -p "$DC"; chmod 700 "$DC"
for sub in "friday-seat/" ""; do
  if [ -f "$HERE/${sub}friday-seat.pem" ] && [ -f "$HERE/${sub}friday-seat.crt" ]; then
    cp "$HERE/${sub}friday-seat.pem" "$HERE/${sub}friday-seat.crt" "$DC/" && chmod 600 "$DC/friday-seat.pem" "$DC/friday-seat.crt" \
      && ok "live-board certificate installed"
    break
  fi
done
[ -f "$DC/friday-seat.pem" ] || warn "no friday-seat certificate beside this installer — Friday cannot use the live board until it is added (setup step 5)."

chmod +x "$TARGET/Launch_Friday.command" "$TARGET/2_Project_Files/friday/"*.sh 2>/dev/null
say ""
say "=============================================================="
say "  Installed. From now on, start Friday by double-clicking:"
say "     $TARGET/Launch_Friday.command"
say "  Starting the first-time setup now…"
say "=============================================================="
sleep 2
FRIDAY_BUNDLE_DIR="$HERE" exec bash "$TARGET/Launch_Friday.command"
