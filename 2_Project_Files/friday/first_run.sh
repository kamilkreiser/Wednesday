#!/bin/bash
# first_run.sh — FRIDAY's first-time configuration (Kam, live board 2026-09-23 10:49:26, verbatim:
#   "create a folder for Friday with all the instructions and a launch file so that when I click that
#    launch file the first time it goes through the configuration process, asks me for the relevant
#    logins and configures itself pulling down from GitHub all the files it needs")
#
# Called by Launch_Friday.command when 4_Credentials/.friday_configured is absent. Safe to re-run:
# every step checks whether it is already done and says so, so a setup interrupted half way resumes
# where it stopped. Nothing here is ever deleted.
#
# SECRETS: Kam types or pastes them at the prompt (hidden input). They are written ONLY under this
# tree's 4_Credentials/ (gitignored — checked below, not assumed), mode 0600, and never echoed. No
# secret is in this file, in the repo, or in any log this script writes.
#
# macOS bash 3.2: no declare -A, no ${var,,}, no `timeout`.
set -u

SOURCE="${BASH_SOURCE[0]}"
while [ -L "$SOURCE" ]; do
  DIR="$(cd -P "$(dirname "$SOURCE")" && pwd)"; SOURCE="$(readlink "$SOURCE")"
  [[ $SOURCE != /* ]] && SOURCE="$DIR/$SOURCE"
done
TREE="$(cd -P "$(dirname "$SOURCE")/../.." && pwd)"
CRED="$TREE/4_Credentials"
ENVF="$CRED/.env"
CONF="$CRED/friday.conf"
MARK="$CRED/.friday_configured"
SELF_INBOX="friday-laptop-agent@agentmail.to"

say()  { printf '%s\n' "$*"; }
hr()   { say ""; say "──────────────────────────────────────────────────────────────"; say "$*"; say "──────────────────────────────────────────────────────────────"; }
ok()   { say "  ✓ $*"; }
warn() { say "  ⚠ $*"; }
ask_yn() { # $1 prompt, $2 default y|n -> rc 0 for yes
  local a d="$2"; printf '  %s [%s] ' "$1" "$( [ "$d" = y ] && echo Y/n || echo y/N )"; read -r a
  a="$(printf '%s' "${a:-$d}" | tr '[:upper:]' '[:lower:]')"; [ "$a" = y ] || [ "$a" = yes ]
}
env_has() { [ -f "$ENVF" ] && grep -q "^$1=" "$ENVF"; }
env_set() { # $1 name, $2 value — replaces an existing line, never prints the value
  local tmp="$ENVF.tmp.$$"
  touch "$ENVF"; chmod 600 "$ENVF"
  grep -v "^$1=" "$ENVF" > "$tmp" || true   # rc 1 = no other lines; the file exists (touched above)
  printf '%s=%s\n' "$1" "$2" >> "$tmp"
  mv "$tmp" "$ENVF"; chmod 600 "$ENVF"
}

# ── 0. This must be a FRIDAY tree, and 4_Credentials must be ignored by git ──────────────────
if [ "$(basename "$TREE")" != "FRIDAY" ]; then
  say "first_run: this tree is '$TREE' — Friday's setup only runs in a folder named FRIDAY. Stopping."; exit 2
fi
mkdir -p "$CRED" && chmod 700 "$CRED"
if ! git -C "$TREE" check-ignore -q "4_Credentials/.env" 2>/dev/null; then
  say "first_run: REFUSING — git does not ignore 4_Credentials/ in this tree, so a secret written here could be"
  say "committed. The repo's .gitignore should carry '4_Credentials/'. Fix that first."; exit 3
fi

hr "FRIDAY — first-time setup   (tree: $TREE)"
say "Friday is your LAPTOP seat. She works Secuura AND Datasec, keeps each client's logins in its own"
say "folder, and talks to you on the FRIDAY tab of the live board. This takes about 10 minutes."
say "Every step can be skipped and re-run later: just double-click Launch_Friday.command again."

# ── 1. Tools ─────────────────────────────────────────────────────────────────────────────────
hr "Step 1 of 7 — tools on this laptop"
MISSING=""
for t in git python3 curl gh tmux claude; do
  if command -v "$t" >/dev/null 2>&1; then ok "$t  ($(command -v "$t"))"; else warn "$t  NOT FOUND"; MISSING="$MISSING $t"; fi
done
if printf '%s' "$MISSING" | grep -q -E ' (gh|tmux)'; then
  if command -v brew >/dev/null 2>&1; then
    if ask_yn "Install the missing gh / tmux with Homebrew now?" y; then
      for t in gh tmux; do printf '%s' "$MISSING" | grep -q " $t" && brew install "$t"; done
    fi
  else
    warn "Homebrew is not installed. Install gh and tmux, then re-run: https://brew.sh then 'brew install gh tmux'"
  fi
fi
if ! command -v claude >/dev/null 2>&1; then
  warn "Claude Code is not installed. The official installer is:"
  say  "      curl -fsSL https://claude.ai/install.sh | bash"
  if ask_yn "Run it now?" n; then curl -fsSL https://claude.ai/install.sh | bash; fi
fi

# ── 2. Where your projects live on this laptop ───────────────────────────────────────────────
hr "Step 2 of 7 — the workspace (the folder that holds !CODING and Notes (MASTER))"
CUR=""
[ -f "$CONF" ] && CUR="$(sed -n "s/^WED_WORKSPACE=//p" "$CONF" | tr -d "'\"" | head -1)"
GUESS="$CUR"
if [ -z "$GUESS" ]; then
  for c in "$(dirname "$TREE")" /Volumes/DevMASTER /Volumes/KK_DEV_Local /Volumes/KK_T9_External_HDD; do
    [ -d "$c/!CODING" ] && { GUESS="$c"; break; }
  done
fi
say "  Friday reads your projects from <workspace>/!CODING and never writes into them."
printf '  Workspace path [%s]: ' "${GUESS:-none found — type a path, or Enter to skip}"; read -r WS
WS="${WS:-$GUESS}"
if [ -n "$WS" ] && [ -d "$WS/!CODING" ]; then
  printf "WED_WORKSPACE=%q\n" "$WS" > "$CONF"; chmod 600 "$CONF"; ok "workspace = $WS  (saved)"
elif [ -n "$WS" ]; then
  warn "'$WS' has no !CODING folder — saved anyway; Friday will say 'workspace NOT mounted' until it does."
  printf "WED_WORKSPACE=%q\n" "$WS" > "$CONF"; chmod 600 "$CONF"
else
  warn "skipped — Friday boots without project access until you re-run this step."
fi

# ── 3. Fleet mail ────────────────────────────────────────────────────────────────────────────
hr "Step 3 of 7 — fleet mail (AgentMail)"
say "  Friday's own inbox is $SELF_INBOX (already created)."
if env_has AGENTMAIL_API_KEY; then
  ok "AGENTMAIL_API_KEY already saved — Enter keeps it"
fi
say "  Paste the AgentMail API key (the one in Notes (MASTER)/Access/Agent Mail.md). Input is hidden."
printf '  AgentMail key: '; read -r -s AMK; say ""
if [ -n "$AMK" ]; then
  CODE="$(curl -s -m 20 -o /dev/null -w '%{http_code}' -H "Authorization: Bearer $AMK" "https://api.agentmail.to/v0/inboxes/$SELF_INBOX" 2>&1)"
  if [ "$CODE" = "200" ]; then env_set AGENTMAIL_API_KEY "$AMK"; ok "key works — it can see $SELF_INBOX (HTTP 200); saved"
  else warn "that key could not read $SELF_INBOX (HTTP $CODE) — NOT saved. Re-run to try again."; fi
fi
unset AMK

# ── 4. Task board (optional) ─────────────────────────────────────────────────────────────────
hr "Step 4 of 7 — Wednesday's Linear task board (optional)"
env_has LINEAR_API_KEY && ok "LINEAR_API_KEY already saved — Enter keeps it"
say "  Paste the Linear API key for the 'wednesday-agent' workspace, or press Enter to skip. Hidden."
printf '  Linear key: '; read -r -s LK; say ""
if [ -n "$LK" ]; then
  CODE="$(curl -s -m 20 -o /dev/null -w '%{http_code}' -H "Authorization: $LK" -H 'Content-Type: application/json' \
          -d '{"query":"{ viewer { id } }"}' https://api.linear.app/graphql 2>&1)"
  if [ "$CODE" = "200" ]; then env_set LINEAR_API_KEY "$LK"; ok "key works (HTTP 200); saved"
  else warn "Linear answered HTTP $CODE — NOT saved."; fi
fi
unset LK

# ── 5. The live board: Friday's seat certificate + the tools that use it ─────────────────────
hr "Step 5 of 7 — the live board (your FRIDAY tab)"
DC="$CRED/dashboard-cloud"; mkdir -p "$DC"; chmod 700 "$DC"
if [ -f "$DC/friday-seat.pem" ] && [ -f "$DC/friday-seat.crt" ]; then
  ok "Friday's seat certificate is already installed"
else
  FOUND=""
  for d in "${FRIDAY_BUNDLE_DIR:-}" "$HOME/Downloads/Friday_Installer" "$HOME/Downloads/Friday_Installer_2026-09-23" "$HOME/Downloads"; do
    [ -n "$d" ] || continue
    for sub in "" "friday-seat/"; do
      if [ -f "$d/${sub}friday-seat.pem" ] && [ -f "$d/${sub}friday-seat.crt" ]; then FOUND="$d/${sub}"; break 2; fi
    done
  done
  if [ -n "$FOUND" ]; then
    cp "${FOUND}friday-seat.pem" "${FOUND}friday-seat.crt" "$DC/" && chmod 600 "$DC/friday-seat.pem" "$DC/friday-seat.crt"
    ok "installed the seat certificate from ${FOUND}"
    say "     (Once setup is done you can delete the installer zip from Downloads — the key now lives here.)"
  else
    warn "no friday-seat.pem / .crt found next to the installer. Friday can boot, but cannot read or post to the"
    warn "live board until they are in $DC/ — re-run this step after unzipping the installer again."
  fi
fi
VENV="$TREE/2_Project_Files/dashboard-cloud/.venv"
if [ -x "$VENV/bin/python" ]; then ok "live-board tools already installed"
else
  say "  Installing the live-board tools (Python packages, ~1 minute)…"
  if python3 -m venv "$VENV" && "$VENV/bin/pip" install -q -r "$TREE/2_Project_Files/dashboard-cloud/requirements.txt"; then
    ok "live-board tools installed"
  else warn "the Python install failed (output above). Friday boots anyway; re-run this step to retry."; fi
fi

# ── 6. Per-client logins — each client in its OWN folder, never mixed ───────────────────────
hr "Step 6 of 7 — client logins (optional; each client kept separate)"
say "  Friday keeps Secuura's and Datasec's identities in separate folders:"
say "      $CRED/clients/secuura/   and   $CRED/clients/datasec/"
say "  and only ever loads ONE of them at a time (2_Project_Files/friday/friday_as.sh). Your project"
say "  launchers keep their own logins as they always have — this is only for Friday's own queries."
for C in secuura datasec; do
  CD="$CRED/clients/$C"; mkdir -p "$CD/.gh-config" "$CD/.azure"; chmod -R go-rwx "$CRED/clients"
  case "$C" in secuura) WHO="the SECUURA GitHub account" ;; datasec) WHO="the DATASEC GitHub account" ;; esac
  if GH_CONFIG_DIR="$CD/.gh-config" gh auth status >/dev/null 2>&1; then
    ok "$C: GitHub already logged in ($(GH_CONFIG_DIR="$CD/.gh-config" gh api user -q .login 2>&1))"
  elif command -v gh >/dev/null 2>&1 && ask_yn "$C: log in to GitHub as $WHO now? (a browser opens)" n; then
    GH_CONFIG_DIR="$CD/.gh-config" gh auth login --hostname github.com --git-protocol https --web \
      && ok "$C: logged in as $(GH_CONFIG_DIR="$CD/.gh-config" gh api user -q .login 2>&1)"
  else
    say "  - $C: skipped"
  fi
done

# ── 7. Done — record it, and check the seat ──────────────────────────────────────────────────
hr "Step 7 of 7 — check"
# (doctor.sh is NOT run here: Launch_Friday.command hands straight to the shared launcher, whose preflight runs
#  it on the configured tree a few seconds later — running it twice only doubles the noise Kam has to read.)
printf 'configured %s on %s\n' "$(date '+%F %T %Z')" "$(hostname -s 2>/dev/null)" > "$MARK"
ok "setup recorded ($MARK). Re-run any step later with: bash $TREE/2_Project_Files/friday/first_run.sh"
say ""
say "  NEXT: Friday starts now. The FIRST time, Claude asks you to log in (/login) — that login is"
say "  Friday's own (it lives in $CRED/.claude) and does not touch your other Claude sessions."
exit 0
