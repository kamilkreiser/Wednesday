#!/bin/bash
# doctor.sh — machine preflight for the portable T9 drive (Kam, 2026-08-04:
# "what happens when I plug the portable drive into my laptop").
# Checks every machine-local dependency the project needs, maps each miss to
# its PORTABILITY.md item + one-line fix. Never prints secret VALUES — only
# presence of keys. Exit 0 = all hard requirements met (warns allowed).
#
# Usage: doctor.sh [--quiet]   (quiet: only problems + summary line)

set -uo pipefail
SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
PROJECT_DIR="$(cd "$SCRIPT_DIR/.." && pwd)"
QUIET="${1:-}"
HARD_FAIL=0; WARNS=0

ok()   { [ "$QUIET" = "--quiet" ] || printf "  ✓ %s\n" "$1"; }
warn() { printf "  ⚠ %-38s %s\n" "$1" "${2:-}"; WARNS=$((WARNS+1)); }
fail() { printf "  ✗ %-38s %s\n" "$1" "${2:-}"; HARD_FAIL=1; }

echo "Wednesday preflight — $(hostname -s), $(date '+%Y-%m-%d %H:%M')"

# --- Hard requirements (Wednesday cannot run properly without) ---
if command -v claude >/dev/null; then
  V=$(claude --version 2>/dev/null | grep -oE '^[0-9]+\.[0-9]+\.[0-9]+' || echo "0")
  ok "claude CLI $V"
  # Feature floor: teams/agent-view era (see delegation-v2 design)
  [ "$(printf '%s\n2.1.178\n' "$V" | sort -V | head -1)" = "2.1.178" ] || warn "claude version < 2.1.178" "npm update -g or install current — Agent Teams era features missing"
else
  fail "claude CLI missing" "install Claude Code (machine-local by nature)"
fi
command -v git    >/dev/null && ok "git"    || fail "git missing" "xcode-select --install"
command -v python3 >/dev/null && ok "python3" || fail "python3 missing" "brew install python"
command -v curl   >/dev/null && ok "curl"   || fail "curl missing" "part of macOS — PATH problem?"

[ -f "$PROJECT_DIR/4_Credentials/.env" ] && ok ".env present" || fail "4_Credentials/.env missing" "restore from password manager — never in git"
if [ -f "$PROJECT_DIR/4_Credentials/.env" ]; then
  for key in LINEAR_API_KEY AGENTMAIL_API_KEY; do
    grep -qE "^${key}=." "$PROJECT_DIR/4_Credentials/.env" && ok "$key set" || warn "$key unset in .env" "Linear/Agent Mail features degrade"
  done
fi

# --- Voice (PORTABILITY item 2) ---
if [ -x "$PROJECT_DIR/2_Project_Files/voice/speak.sh" ]; then
  if say -v '?' 2>/dev/null | grep -q "Matilda (Premium)"; then ok "voice: Matilda (Premium)"
  elif say -v '?' 2>/dev/null | grep -qE "Matilda|Moira"; then warn "Matilda Premium not downloaded" "System Settings → Spoken Content → add Matilda Premium (fallback chain active)"
  else warn "no preferred voices" "speak.sh will use default voice"; fi
else
  fail "voice/speak.sh missing or not executable" "chmod +x 2_Project_Files/voice/speak.sh"
fi

# --- Cockpit engine (PORTABILITY items 13-14) ---
command -v tmux >/dev/null && ok "tmux $(tmux -V | awk '{print $2}')" || warn "tmux missing" "brew install tmux — fleet cockpit disabled without it (PORTABILITY 13)"
[ -d /Applications/iTerm.app ] && ok "iTerm2" || warn "iTerm2 missing" "brew install --cask iterm2 — cockpit glass (PORTABILITY 14); plain 'tmux attach' still works"
command -v brew >/dev/null && ok "homebrew" || warn "homebrew missing" "needed to install tmux/iTerm2 — https://brew.sh"

# --- Scheduler (PORTABILITY item 12, machine-local launchd) ---
if launchctl list 2>/dev/null | grep -q com.wednesday.wake; then ok "scheduler launchd jobs loaded"
else warn "scheduler jobs not loaded" "run 2_Project_Files/scheduler/install.sh on this machine (PORTABILITY 12)"; fi

# --- Optional seats / mounts ---
[ -x "$PROJECT_DIR/2_Project_Files/tools/codex-cli/node_modules/.bin/codex" ] || [ -d "$PROJECT_DIR/2_Project_Files/tools/codex-cli" ] && ok "codex CLI (drive-local)" || warn "codex CLI dir missing" "gpt seat unavailable (PORTABILITY 7-9)"
[ -d "/Volumes/DevMASTER" ] && ok "DevMASTER mounted" || warn "DevMASTER not mounted" "cross-project context read-only unavailable — fine on the laptop"

# --- Repo hooks (ledger w=3 enforcement travels per-clone) ---
[ -x "$PROJECT_DIR/.git/hooks/pre-commit" ] && ok "pre-commit artifact gate" || warn "pre-commit hook missing" "re-create per learnings/2026-08-04_gitignore-artifacts-at-creation (fresh clone?)"

echo
if [ "$HARD_FAIL" = "1" ]; then
  echo "PREFLIGHT: HARD FAILURES above — fix before relying on this machine."
  exit 1
elif [ "$WARNS" -gt 0 ]; then
  echo "PREFLIGHT: OK with $WARNS warning(s) — degraded features listed above."
else
  echo "PREFLIGHT: all clear."
fi
exit 0
