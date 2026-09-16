#!/bin/bash
# Point Kam's PERSONAL ollama at the DevMASTER store, everywhere it is read from.
#
# Kam, 2026-09-16 13:46: "yes, create a folder and move ollama. change all the reference pointers".
# Run this ONLY after move_ollama_store.sh --verify passes: a pointer at a half-copied store is worse
# than no pointer, because ollama would report the models missing rather than failing loudly.
#
# THREE readers, and all three need it — this is the "enumerate every surface" step. Setting only the
# shell one is the common half-fix: the Ollama desktop app is launched by launchd and never reads
# ~/.zshrc, so it would keep using ~/.ollama and the 141 GB could never be reclaimed.
#   1. interactive shells      -> a line in ~/.zshrc
#   2. GUI apps, this session  -> launchctl setenv (dies at logout)
#   3. GUI apps, after reboot  -> a LaunchAgent that re-runs the setenv at login
#
# The FLEET's own store is deliberately NOT changed: night_run.sh and start_ollama.sh pin
# 2_Project_Files/local-model/models unconditionally, because the fleet's weights travel with the
# WEDNESDAY folder (the portability rule) and must not follow a global that Kam may re-point.
#
# Usage: bash set_ollama_pointers.sh [--check]
set -u
STORE="/Volumes/DevMASTER/SYSTEM/ollama/models"
AGENT="$HOME/Library/LaunchAgents/com.kam.ollama-models.plist"
ZSHRC="$HOME/.zshrc"
MARK="# OLLAMA_MODELS -> DevMASTER (Wednesday, 2026-09-16, on Kam's instruction)"

report() {
  echo "store exists:        $([ -d "$STORE" ] && echo "yes ($(du -sh "$STORE" 2>/dev/null | awk '{print $1}'))" || echo NO)"
  echo "shell (~/.zshrc):    $(/usr/bin/grep -c 'OLLAMA_MODELS' "$ZSHRC" 2>/dev/null || echo 0) line(s)"
  echo "launchctl (session): $(launchctl getenv OLLAMA_MODELS 2>/dev/null || echo '<unset>')"
  echo "LaunchAgent (boot):  $([ -f "$AGENT" ] && echo present || echo absent)"
  # The claim is "the fleet does not follow the global", so MEASURE that rather than grepping for a
  # word: resolve the runner's own expression with a deliberately wrong global in the environment.
  local resolved
  resolved="$(OLLAMA_MODELS=/deliberately/wrong bash -c 'LM_DIR="'"$(dirname "${BASH_SOURCE[0]}")"'"; echo "${NIGHT_OLLAMA_MODELS:-$LM_DIR/models}"')"
  echo "fleet store resolves to: $resolved"
  case "$resolved" in
    /deliberately/wrong*) echo "  ⚠ THE FLEET FOLLOWS THE GLOBAL — night_run.sh must pin its own path" ;;
    *) echo "  ok — pinned; a global OLLAMA_MODELS cannot redirect the fleet" ;;
  esac
}
[ "${1:-}" = "--check" ] && { report; exit 0; }

[ -d "$STORE" ] || { echo "REFUSED — $STORE does not exist. Run move_ollama_store.sh first." >&2; exit 2; }
BLOBS="$(find "$STORE" -type f 2>/dev/null | wc -l | tr -d ' ')"
[ "$BLOBS" -ge 50 ] || { echo "REFUSED — only $BLOBS files under $STORE; the copy looks incomplete. Verify before pointing anything at it." >&2; exit 3; }

# 1. interactive shells
if /usr/bin/grep -q 'OLLAMA_MODELS' "$ZSHRC" 2>/dev/null; then
  echo "~/.zshrc already sets OLLAMA_MODELS — left alone, read it yourself:"; /usr/bin/grep -n 'OLLAMA_MODELS' "$ZSHRC"
else
  cp "$ZSHRC" "$ZSHRC.pre-0916-ollama" 2>/dev/null
  printf '\n%s\nexport OLLAMA_MODELS="%s"\n' "$MARK" "$STORE" >> "$ZSHRC"
  echo "~/.zshrc: line added (backup at ~/.zshrc.pre-0916-ollama)"
fi

# 2. this login session's GUI apps
launchctl setenv OLLAMA_MODELS "$STORE" && echo "launchctl setenv: done (this session)"

# 3. every session after a reboot
mkdir -p "$(dirname "$AGENT")"
cat > "$AGENT" <<PLIST
<?xml version="1.0" encoding="UTF-8"?>
<!DOCTYPE plist PUBLIC "-//Apple//DTD PLIST 1.0//EN" "http://www.apple.com/DTDs/PropertyList-1.0.dtd">
<plist version="1.0">
<dict>
  <key>Label</key><string>com.kam.ollama-models</string>
  <key>ProgramArguments</key>
  <array>
    <string>/bin/launchctl</string><string>setenv</string>
    <string>OLLAMA_MODELS</string><string>$STORE</string>
  </array>
  <key>RunAtLoad</key><true/>
</dict>
</plist>
PLIST
launchctl unload "$AGENT" 2>/dev/null
launchctl load "$AGENT" 2>/dev/null && echo "LaunchAgent: loaded (survives reboot)"

echo; report
echo
echo "Ollama.app must be QUIT and reopened to pick the new store up — a running app keeps the env it started with."
