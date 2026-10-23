#!/bin/bash
# stub cockpit: MODE=nospace_once|nospace_always|other|ok ; counts adds in $S/count
C="$STUB_DIR/count"; [ "$1" = layout ] && { echo "stub layout applied"; exit 0; }
n=$(( $(cat "$C" 2>/dev/null || echo 0) + 1 )); echo $n > "$C"
case "$MODE" in
  ok) echo "pane '$2' added (%999)"; exit 0;;
  nospace_once) [ $n -eq 1 ] && { echo "size or position no space for a new pane"; exit 1; }; echo "pane '$2' added (%999)"; exit 0;;
  nospace_always) echo "size or position no space for a new pane"; exit 1;;
  other) echo "usage_gate: REFUSED"; exit 3;;
esac
