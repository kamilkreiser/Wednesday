#!/bin/bash
# install_receipt.command — arm the Ornith DAILY RECEIPT launchd job (Kam 2026-09-15 18:19: "know progress continues
# through the week and does not stop"; Monday-loop piece (e)). Same shape as install_night.command: the plist is
# written to ~/Library/LaunchAgents (machine-local — PORTABILITY item), the script it points at lives on the drive.
# `--render-only <path>` writes the substituted plist to <path> and touches launchctl NOT AT ALL (the lint arm).
# Disarm: launchctl bootout gui/$(id -u)/com.<agent>.ornith-receipt
set -u
SELF_DIR="$(cd -P "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
AGENTS_DIR="$HOME/Library/LaunchAgents"
mkdir -p "$AGENTS_DIR"
AGENT="${WED_AGENT:-wednesday}"
case "$AGENT" in
  wednesday) ;;
  tuesday) echo "install_receipt: REFUSING — the Ornith receipt is Wednesday's seat only." >&2; exit 2 ;;
  *) echo "install_receipt: REFUSING — WED_AGENT='$AGENT' is not a known agent." >&2; exit 2 ;;
esac
[ -f "$SELF_DIR/daily_receipt.sh" ] || { echo "install_receipt: REFUSING — no daily_receipt.sh beside this installer at $SELF_DIR" >&2; exit 3; }
LABEL="com.$AGENT.ornith-receipt"
PLIST="$AGENTS_DIR/$LABEL.plist"
TEMPLATE="$SELF_DIR/com.wednesday.ornith-receipt.plist"
[ "${1:-}" = "--render-only" ] && PLIST="${2:?--render-only needs a path}"
sed -e "s|__RECEIPT__|$SELF_DIR/daily_receipt.sh|g" \
    -e "s|__AGENT__|$AGENT|g" \
    -e "s|__HOME__|$HOME|g" \
    -e "s|__LABEL__|$LABEL|g" \
    "$TEMPLATE" > "$PLIST"
if [ "${1:-}" = "--render-only" ]; then echo "rendered (NOT installed) → $PLIST"; plutil -lint "$PLIST"; exit $?; fi
launchctl bootout "gui/$(id -u)/$LABEL" 2>/dev/null || true
launchctl bootstrap "gui/$(id -u)" "$PLIST"
if launchctl print "gui/$(id -u)/$LABEL" >/dev/null 2>&1; then echo "OK: $LABEL loaded → 06:45 daily → $SELF_DIR/daily_receipt.sh --post"; else echo "FAILED: $LABEL not loaded"; exit 4; fi
