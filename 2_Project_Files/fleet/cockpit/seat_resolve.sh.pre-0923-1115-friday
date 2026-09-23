#!/bin/bash
# seat_resolve.sh — THE coordinator seat + pane resolver (2026-09-13, Tuesday's
# 19:1x finding; learnings/2026-09-09_the-seat-resolver-is-the-layer-above-every-
# agent-aware-fix.md). SOURCED, never executed, by:
#   wednesday_rotate.sh   (which pane to respawn)
#   wake_watch.sh         (DEAD check + "skip my own pane" in the idle tripwire)
#   arm_wake_watch.sh     (tap target + the WED_AGENT it hands to --dead)
# Three scripts held three copies of the same lookup and they disagreed: rotate
# and wake_watch looked for @cockpit_name == $SEAT while arm_wake_watch and the
# cockpit itself still used the literal "wednesday" — so on the mini (pane named
# "wednesday", seat tuesday) --self refused, --dead refused, and the DEAD case
# handed --dead no WED_AGENT at all. ONE copy here; the callers only call it.
#
# macOS bash 3.2: no declare -A, no ${var,,}, no timeout. No `cd` (the tool cwd
# persists); absolute paths only.
#
# Provides (all pure — no env test hooks; tests pass explicit arguments):
#   seat_resolve [project_dir]
#       Sets TREE_SEAT (from the tree's folder name: TUESDAY -> tuesday, anything
#       else -> wednesday — the same rule Launch_Wednesday.command uses) and
#       SEAT (= $WED_AGENT if set, else TREE_SEAT). Default project_dir = the tree
#       this file lives in (…/2_Project_Files/fleet/cockpit -> three levels up).
#       Does NOT validate SEAT — callers keep their own "unknown seat" refusals.
#   coord_pane_id <tmux-target> [seat] [tree_seat]
#       Prints the coordinator pane id for <seat> (default $SEAT / $TREE_SEAT) in
#       the tmux session of <tmux-target> (session-wide: list-panes -s). rc 0 on
#       success; rc 1 with ONE stderr line naming every name it looked for.
#       Resolution order:
#         1. the pane whose @cockpit_name == seat                      -> found
#         2. seat != "wednesday" AND a pane named the LEGACY "wednesday" exists
#            (cockpit.conf still names pane 0 "wednesday" on every tree):
#            THE GUARD — adopt it IF AND ONLY IF
#              (g1) tree_seat == seat: the tree this resolver runs from says the
#                   seat that is running here IS the one asked for (a Tuesday tree
#                   on the mini adopting the mini's "wednesday"-named pane), and
#              (g2) the pane's own start command, if it names a seat launcher at
#                   all (…/<TREE>/Launch_Wednesday.command), was started from a
#                   tree of the SAME seat — so a real Wednesday pane launched
#                   from a WEDNESDAY tree is never adopted by a Tuesday tree on a
#                   machine where both trees exist in one tmux server.
#            Either guard failing REFUSES (never a guess).                -> found
#         3. nothing                                                      -> refuse
#       seat == "wednesday" looks ONLY for "wednesday" (a "tuesday" pane is never
#       cross-adopted), so Wednesday's behaviour on the Studio is byte-identical.
#
# Uses ${TMUX_BIN:-tmux}; the caller sets TMUX_BIN (tests point it at a wrapper
# that adds `-L <scratch socket>`).

COORD_LEGACY_NAME="wednesday"

seat_from_tree_name() { # $1 = a directory path -> prints the seat its NAME implies
  case "$(basename "$1")" in
    TUESDAY|Tuesday|tuesday) echo tuesday ;;
    *)                       echo wednesday ;;
  esac
}

seat_resolve() { # [project_dir] -> sets TREE_SEAT, SEAT
  local dir="${1:-}"
  if [ -z "$dir" ]; then
    dir="$(cd -P "$(dirname "${BASH_SOURCE[0]}")/../../.." && pwd)"
  fi
  TREE_SEAT="$(seat_from_tree_name "$dir")"
  SEAT="${WED_AGENT:-$TREE_SEAT}"
}

coord_pane_id() { # <tmux-target> [seat] [tree_seat] -> prints pane id (rc 0) or refuses (rc 1)
  local target="$1" seat="${2:-${SEAT:-}}" tree="${3:-${TREE_SEAT:-}}"
  local rows id row legacy_id start start_tree looked
  [ -n "$seat" ] || { echo "coord_pane_id: no seat given and SEAT is unset (call seat_resolve first)" >&2; return 1; }
  rows="$("${TMUX_BIN:-tmux}" list-panes -s -t "$target" -F '#{pane_id}|#{@cockpit_name}|#{pane_start_command}' 2>/dev/null)" \
    || { echo "coord_pane_id: cannot list panes of tmux target '$target'" >&2; return 1; }
  # 1. exact seat name wins, always.
  id="$(printf '%s\n' "$rows" | awk -F'|' -v s="$seat" '$2==s{print $1; exit}')"
  if [ -n "$id" ]; then printf '%s\n' "$id"; return 0; fi
  looked="@cockpit_name '$seat'"
  # 2. legacy fallback, guarded.
  if [ "$seat" != "$COORD_LEGACY_NAME" ]; then
    looked="$looked or legacy '$COORD_LEGACY_NAME'"
    row="$(printf '%s\n' "$rows" | awk -F'|' -v s="$COORD_LEGACY_NAME" '$2==s{print; exit}')"
    if [ -n "$row" ]; then
      legacy_id="${row%%|*}"
      if [ "$tree" != "$seat" ]; then
        echo "coord_pane_id: REFUSED — pane $legacy_id is named '$COORD_LEGACY_NAME' but this tree's seat is '$tree', not '$seat'; a '$seat' seat may only adopt the legacy pane on its own tree (looked for $looked)" >&2
        return 1
      fi
      start="${row#*|}"; start="${start#*|}"
      start_tree="$(printf '%s' "$start" | sed -nE 's#.*/([^/]+)/Launch_(Wednesday|Tuesday)\.command.*#\1#p' | head -1)"
      if [ -n "$start_tree" ] && [ "$(seat_from_tree_name "/$start_tree")" != "$seat" ]; then
        echo "coord_pane_id: REFUSED — pane $legacy_id ('$COORD_LEGACY_NAME') was started from tree '$start_tree', which is not a '$seat' tree; not adopting another seat's coordinator (looked for $looked)" >&2
        return 1
      fi
      printf '%s\n' "$legacy_id"; return 0
    fi
  fi
  echo "coord_pane_id: REFUSED — no coordinator pane in tmux target '$target' (looked for $looked)" >&2
  return 1
}
