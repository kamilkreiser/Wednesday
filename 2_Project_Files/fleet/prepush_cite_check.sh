#!/bin/bash
# prepush_cite_check.sh — ADVISORY ONLY. Called by send_brief.sh; never blocks, always exits 0.
# Ledger 2026-10-19 w=3: three times the coordinator ruled a git push route (force-push, "push through
# the repo's core.sshCommand", "reachable once #NNNN merges") without reading the target repo's
# .githooks/pre-push, whose refusal branches then refused the push.
# Usage: prepush_cite_check.sh <body-file>     (or body on stdin with no argument)
# Prints one ADVISORY line to stderr iff the body instructs a push, cites no `pre-push:<digit>` line,
# and does not state the push is outside the hook's path.
set -u
if [ $# -ge 1 ]; then BODY_TXT="$(cat "$1")"; else BODY_TXT="$(cat)"; fi
PUSH_RE='git push|force-push|force push|--force|--force-with-lease|ALLOW_FORCE|push from the branch|push with the transport'
CITE_RE='pre-push:[0-9]'
EXEMPT_RE='not a push|pre-push is not in|not in this path'
if printf '%s\n' "$BODY_TXT" | grep -qiE -e "$PUSH_RE"; then
  if ! printf '%s\n' "$BODY_TXT" | grep -qiE -e "$CITE_RE" \
     && ! printf '%s\n' "$BODY_TXT" | grep -qiE -e "$EXEMPT_RE"; then
    echo "ADVISORY (2026-10-19 w=3): this mail instructs a push but cites no .githooks/pre-push line; read the target hook's refusal branches and cite them, or state the push is not in the hook's path" >&2
  fi
fi
exit 0
