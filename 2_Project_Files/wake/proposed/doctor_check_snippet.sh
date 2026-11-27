
# --- Wake pack fresh + handover is ONE block (WED-170 step 1, 2026-11-27; Kam, live board
# 11:43:52 "Go, steps 1 to 3 in that order"). A seat that boots on a wake pack
# (0_Brain/wake/WAKE-<seat>.md) reads it INSTEAD of the rules card, ledger, pickup and grants
# files, so a pack older than its sources is a seat booting on stale state. The launcher builds
# it in-path; this is the backstop. A seat's handover (0_Brain/tasks/STATE-<seat>.md) is written
# only through handover.sh; `check` goes red when it was appended to by hand (the stack the
# 2026-09-18 NEXT-PICKUP warning below could report but never prevent).
# A seat is "on the pack" once its state file exists (the cut-over's first step). From then on a
# MISSING pack is a warning too: a build that has never succeeded must not be silent. A seat with
# no state file is untouched: adopting the pack is that seat's own step. The seat is the one
# handover.sh resolves from the tree (never typed here); its refusal is shown, never discarded.
WP="$PROJECT_DIR/2_Project_Files/wake/wake_pack.py"
HO="$PROJECT_DIR/2_Project_Files/wake/handover.sh"
if [ -f "$HO" ]; then
  WK_OUT="$(bash "$HO" --where 2>&1)"; WK_RC=$?
  WK_SEAT="$(printf '%s\n' "$WK_OUT" | sed -n 's/^seat: *//p')"
  if [ "$WK_RC" -ne 0 ] || [ -z "$WK_SEAT" ]; then
    warn "handover.sh cannot tell which seat this tree is" "$(printf '%s' "$WK_OUT" | head -2 | tr '\n' ' ') — the wake pack and handover checks were NOT run"
  else
    WK_STATE="$PROJECT_DIR/0_Brain/tasks/STATE-${WK_SEAT}.md"
    WK_PACK="$PROJECT_DIR/0_Brain/wake/WAKE-${WK_SEAT}.md"
    if [ -f "$WP" ] && [ -f "$WK_PACK" ]; then
      WP_OUT="$(python3 "$WP" --seat "$WK_SEAT" --check 2>&1)"; WP_RC=$?
      if [ "$WP_RC" -eq 0 ]; then ok "$(printf '%s' "$WP_OUT" | tail -1 | sed 's/^OK: //')"
      else warn "wake pack STALE, missing a source or over budget" "$(printf '%s' "$WP_OUT" | head -2 | tr '\n' ' ') — rebuild: python3 2_Project_Files/wake/wake_pack.py --seat ${WK_SEAT}"
      fi
    elif [ -f "$WK_STATE" ]; then
      warn "NO wake pack for the ${WK_SEAT} seat" "this seat is cut over (its state file exists) but $WK_PACK is not there: the launcher's build failed or never ran, and the seat booted on the legacy reads — run: python3 2_Project_Files/wake/wake_pack.py --seat ${WK_SEAT}"
    fi
    if [ -f "$WK_STATE" ]; then
      HO_OUT="$(bash "$HO" check 2>&1)"; HO_RC=$?
      if [ "$HO_RC" -eq 0 ]; then ok "$(printf '%s' "$HO_OUT" | tail -1 | sed 's/^handover: //')"
      else warn "handover is NOT one clean block" "$(printf '%s' "$HO_OUT" | head -2 | tr '\n' ' ') — rewrite it: 2_Project_Files/wake/handover.sh write --stdin"
      fi
    fi
  fi
fi
