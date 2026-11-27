
# --- Wake pack (WED-170 step 1; Kam, live board 2026-11-27 11:43:52: "Go, steps 1 to 3 in that
# order"). WEDNESDAY SEAT ONLY in this round: Tuesday's and Friday's boots do not change, and
# every command added here sits inside a test on AGENT = wednesday. The pack is ONE generated
# file under a token budget (2_Project_Files/wake/wake_pack.py). It is built here, before
# doctor, so doctor's freshness check reads this launch's pack. The build counts as done only
# when it exits 0 AND the pack file is there and not empty. Anything else leaves WAKE_PACK_OK=0
# with the reason in WAKE_FAIL: the seat then boots on the legacy read list, never on a stale
# pack, and the prompt block further down puts that failure in the FIRST lines the seat reads
# (an echo here scrolls away before the launcher's clear; it is not a channel).
WAKE_PACK_OK=0; WAKE_PACK=""; WAKE_SUMMARY=""; WAKE_FAIL=""
if [ "$AGENT" = "wednesday" ]; then
  WAKE_PACK="$BRAIN_DIR/wake/WAKE-${AGENT}.md"
  WAKE_PY="$PROJECT_DIR/2_Project_Files/wake/wake_pack.py"
  if [ -f "$WAKE_PY" ]; then
    WAKE_OUT="$(python3 "$WAKE_PY" --seat "$AGENT" 2>&1)"; WAKE_RC=$?
    WAKE_LAST="$(printf '%s\n' "$WAKE_OUT" | tail -1)"
    if [ "$WAKE_RC" -eq 0 ] && [ -s "$WAKE_PACK" ]; then
      WAKE_PACK_OK=1
      WAKE_SUMMARY="${WAKE_LAST#*  }"
      echo "wake pack: $WAKE_SUMMARY"
    elif [ "$WAKE_RC" -eq 0 ]; then
      WAKE_FAIL="wake_pack.py exited 0 but there is no pack (or an empty one) at $WAKE_PACK"
    else
      WAKE_FAIL="wake_pack.py rc=$WAKE_RC: ${WAKE_LAST:0:400}"
    fi
  else
    WAKE_FAIL="wake_pack.py is missing at $WAKE_PY"
  fi
  [ "$WAKE_PACK_OK" = "1" ] || echo "⚠ WAKE PACK NOT BUILT — $WAKE_FAIL — this boot uses the legacy read list, and the prompt says so in its first lines"
fi
