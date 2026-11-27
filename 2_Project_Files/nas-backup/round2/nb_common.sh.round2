#!/bin/bash
# nb_common.sh — SOURCED by nas_backup.sh, nas_backup_nightly.sh and nas_backup_watch.sh. Resolves the SEAT and
# the python to run, then the caller hands over to nb_core.py. It decides nothing else.
#
# THE SEAT: resolved by fleet/cockpit/seat_resolve.sh (the one resolver), then held to two stricter rules that
# install_all_jobs.sh learned the hard way (2026-09-16): (1) the tree's folder NAME must be WEDNESDAY, TUESDAY or
# FRIDAY (seat_resolve defaults anything else to wednesday; a backup that guesses its seat writes into the wrong
# client's folder); (2) an inherited WED_AGENT that DISAGREES with the tree REFUSES, it never wins.
#
# macOS bash 3.2. Never discards stderr.
NB_HERE="$(cd -P "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
NB_REAL_TREE="$(cd -P "$NB_HERE/../.." && pwd)"
NB_TREE="$NB_REAL_TREE"
# TEST MODE (tests/run.sh): NB_TEST_TREE names a scratch tree; nb_core.py refuses it unless it and NB_TEST_ROOT
# live under /private/tmp. The resolver itself is always the real one.
if [ -n "${NB_TEST_ROOT:-}" ] && [ -n "${NB_TEST_TREE:-}" ]; then NB_TREE="$NB_TEST_TREE"; fi

nb_resolve_seat() {
  local resolver="$NB_REAL_TREE/2_Project_Files/fleet/cockpit/seat_resolve.sh"
  if [ ! -f "$resolver" ]; then
    echo "nas-backup: REFUSED — the seat resolver is missing at $resolver; nothing run" >&2; return 2
  fi
  # shellcheck source=/dev/null
  . "$resolver"
  seat_resolve "$NB_TREE"
  local strict=""
  case "$(basename "$NB_TREE")" in
    WEDNESDAY|Wednesday|wednesday) strict=wednesday ;;
    TUESDAY|Tuesday|tuesday)       strict=tuesday ;;
    FRIDAY|Friday|friday)          strict=friday ;;
  esac
  if [ -z "$strict" ]; then
    echo "nas-backup: REFUSED — cannot tell which seat this tree is: $NB_TREE (its folder name is not WEDNESDAY, TUESDAY or FRIDAY); nothing run" >&2; return 2
  fi
  if [ "$strict" != "$TREE_SEAT" ]; then
    echo "nas-backup: REFUSED — the resolver says '$TREE_SEAT' and the folder name says '$strict'; nothing run" >&2; return 2
  fi
  if [ -n "${WED_AGENT:-}" ] && [ "$WED_AGENT" != "$strict" ]; then
    echo "nas-backup: REFUSED — the tree says '$strict' and WED_AGENT says '$WED_AGENT'. Two independent sources disagree, so this tool will not pick one; nothing run" >&2; return 2
  fi
  NB_SEAT="$strict"
  return 0
}

nb_find_python() {
  NB_PY=""
  local c
  for c in "${NB_PYTHON:-}" /opt/homebrew/bin/python3 /usr/local/bin/python3 /usr/bin/python3; do
    if [ -n "$c" ] && [ -x "$c" ]; then NB_PY="$c"; return 0; fi
  done
  echo "nas-backup: REFUSED — no python3 found (looked at /opt/homebrew/bin, /usr/local/bin, /usr/bin); nothing run" >&2
  return 2
}
