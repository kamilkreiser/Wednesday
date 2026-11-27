#!/bin/bash
# braindb.sh - a LOCAL, REBUILDABLE Postgres full-text index over this seat's markdown brain.
# The files stay the master; the index is disposable. Data directory: <this lane>/pgdata-<seat>/
# on the drive. On demand only: no service, no launchd job, no TCP listener (Unix socket only).
#
#   braindb.sh init                 create the cluster (refuses if the directory exists)
#   braindb.sh start | stop | status
#   braindb.sh up                   init if missing, start if stopped, rebuild if check is red
#   braindb.sh rebuild              drop and reload everything from the files
#   braindb.sh check                rc 0 when (path, sha256) on disk equals the index, else rc 1 + up to 20 paths
#   braindb.sh search "<words>" [--kind K | --all] [--limit N]   rules and lessons first by default
#   braindb.sh at <trigger> [--top N]
#   braindb.sh doctor               one line for doctor.sh; starts nothing; rc 0 ok, rc 1 warn
# rebuild, check, search and at bring the server up themselves when it is down (init if there is no
# cluster yet); search and at also build the index when there is none. BRAINDB_NO_AUTOSTART=1 turns
# that off. Every command that talks to the server first asks it for its data directory and refuses
# (rc 4) unless that is the one the command is addressed to.
#
# Seat: the tree's folder name (WEDNESDAY, TUESDAY, FRIDAY). WED_AGENT, when set, must agree with it.
# Overrides (tests): BRAINDB_ROOT (tree to index; needs BRAINDB_PGDATA too), BRAINDB_PGDATA,
# BRAINDB_SOCKDIR, BRAINDB_SCOPE, BRAINDB_PGBIN, BRAINDB_PORT (names the socket file only).
# macOS bash 3.2. No `cd`. stderr is never discarded.
set -u

die() { echo "braindb: $*" >&2; exit 1; }

PY="${BRAINDB_PYTHON:-python3}"
command -v "$PY" >/dev/null || die "python3 not found on PATH"
SELF="${BASH_SOURCE[0]}"
case "$SELF" in /*) ;; *) SELF="$PWD/$SELF" ;; esac
LANE="$("$PY" -c 'import os,sys; print(os.path.dirname(os.path.realpath(sys.argv[1])))' "$SELF")" || die "cannot locate myself"
SELF="$LANE/braindb.sh"
CODE_ROOT="${LANE%/2_Project_Files/brain-db}"
[ "$CODE_ROOT" != "$LANE" ] || die "expected to live at <tree>/2_Project_Files/brain-db, found $LANE"

# --- which seat. The TREE decides; WED_AGENT may only agree (two sources that disagree are refused, and an
# unrecognised tree is refused, never defaulted to a seat). tools/seat_note.sh is the fleet's copy of that
# rule; where a copied tree lacks it, the same rule is applied here over seat_resolve.sh.
RESOLVER="$CODE_ROOT/2_Project_Files/fleet/cockpit/seat_resolve.sh"
NOTE_LIB="$CODE_ROOT/2_Project_Files/tools/seat_note.sh"
if [ -f "$NOTE_LIB" ]; then
  # shellcheck disable=SC1090
  . "$NOTE_LIB"
  seat_note_dir "$CODE_ROOT" braindb || exit 2
  SEAT="$SEAT_NOTE_SEAT"
else
  [ -f "$RESOLVER" ] || die "seat resolver not found: $RESOLVER"
  # shellcheck disable=SC1090
  . "$RESOLVER"
  seat_resolve "$CODE_ROOT"
  _TREE_LOWER="$(basename "$CODE_ROOT" | tr '[:upper:]' '[:lower:]')"
  case "$_TREE_LOWER" in tuesday|wednesday|friday) ;; *) _TREE_LOWER="" ;; esac
  if [ -z "$_TREE_LOWER" ] || [ "${TREE_SEAT:-}" != "$_TREE_LOWER" ]; then
    echo "braindb: REFUSED: cannot tell which seat this tree is; run from a WEDNESDAY, TUESDAY or FRIDAY tree (tree: $CODE_ROOT)" >&2; exit 2
  fi
  if [ -n "${WED_AGENT:-}" ] && [ "$WED_AGENT" != "$TREE_SEAT" ]; then
    echo "braindb: REFUSED: WED_AGENT='$WED_AGENT' but this tree ('$(basename "$CODE_ROOT")') is seat '$TREE_SEAT'; unset WED_AGENT, or run from the matching tree" >&2; exit 2
  fi
  SEAT="$TREE_SEAT"
fi
case "$SEAT" in wednesday|tuesday|friday) ;; *) die "unknown seat '$SEAT' (wednesday|tuesday|friday)" ;; esac

if [ -n "${BRAINDB_ROOT:-}" ] && [ -z "${BRAINDB_PGDATA:-}" ]; then
  die "BRAINDB_ROOT is set without BRAINDB_PGDATA: a fixture tree may never be loaded into the drive cluster"
fi
ROOT="${BRAINDB_ROOT:-$CODE_ROOT}"
PGDATA="${BRAINDB_PGDATA:-$LANE/pgdata-$SEAT}"
SOCKDIR="${BRAINDB_SOCKDIR:-/tmp/wed-braindb-$(id -u)-$SEAT}"
SCOPE="${BRAINDB_SCOPE:-$LANE/scope/$SEAT.scope}"
PORT="${BRAINDB_PORT:-5432}"
PIDFILE="$PGDATA/postmaster.pid"
LOG="$PGDATA/braindb-server.log"
LOCKFILE="$PGDATA.lock"
PGBIN=""

find_pgbin_soft() { # sets PGBIN; rc 1 when the binaries are not found
  local d
  for d in "${BRAINDB_PGBIN:-}" /opt/homebrew/opt/postgresql@15/bin /usr/local/opt/postgresql@15/bin; do
    if [ -n "$d" ] && [ -x "$d/postgres" ] && [ -x "$d/pg_ctl" ] && [ -x "$d/initdb" ] && [ -x "$d/psql" ]; then
      PGBIN="$d"; return 0
    fi
  done
  if command -v postgres >/dev/null && command -v pg_ctl >/dev/null && command -v initdb >/dev/null && command -v psql >/dev/null; then
    PGBIN="$(dirname "$(command -v postgres)")"; return 0
  fi
  return 1
}
find_pgbin() {
  find_pgbin_soft || die "Postgres binaries not found (looked in \$BRAINDB_PGBIN, /opt/homebrew/opt/postgresql@15/bin, /usr/local/opt/postgresql@15/bin, PATH). See PORTABILITY.md."
}

bin_major() { "$PGBIN/postgres" --version | sed -E 's/^[^0-9]*([0-9]+).*/\1/'; }

need_scope() { # a seat with no scope file gets NOTHING created or started
  [ -f "$SCOPE" ] || die "no scope file for seat '$SEAT' at $SCOPE. A seat is indexed only through its own confirmed allow-list (see proposed/INSTRUCTIONS-for-other-seats.md, step 1). Nothing was created or started."
}

# --- process helpers: a server is "ours" only by its data directory, never by its name -----------
pid_alive() { [ -n "$(ps -p "$1" -o pid= | tr -d ' ')" ]; }
pid_is_ours() { # $1 = pid; true when that process was started with -D <our data directory>
  local cmd
  cmd="$(ps -ww -p "$1" -o command=)"
  case "$cmd " in *" -D $PGDATA "*) return 0 ;; esac
  return 1
}
read_pidfile() { # sets PF_PID, PF_DIR; rc 1 when there is no usable pid file
  PF_PID=""; PF_DIR=""
  [ -f "$PIDFILE" ] || return 1
  PF_PID="$(sed -n 1p "$PIDFILE" | tr -d ' ')"
  PF_DIR="$(sed -n 2p "$PIDFILE")"
  case "$PF_PID" in ''|*[!0-9]*) return 1 ;; esac
  return 0
}
running() { # rc 0 when our server is up
  read_pidfile || return 1
  [ "$PF_DIR" = "$PGDATA" ] || return 1
  pid_alive "$PF_PID" || return 1
  pid_is_ours "$PF_PID"
}
stale_pid_recovery() { # prints the one recovery line for a pid file that is in the way; moves NOTHING
  local q; q="$(dirname "$PGDATA")/_quarantine_$(date +%F)"
  echo "braindb: TO RECOVER (a person or the coordinator runs this; the tool does not, because a wrong guess here would touch a live process that is not ours):" >&2
  echo "braindb:   mkdir -p \"$q\" && mv -n \"$PIDFILE\" \"$q/postmaster.pid.stale-$PF_PID\"   then: braindb.sh start" >&2
}
foreign_pidfile_guard() { # the pid file names a LIVE process that is not this index's server: say so and stop
  read_pidfile || return 0
  if [ "$PF_DIR" != "$PGDATA" ]; then
    echo "braindb: STALE PID FILE: $PIDFILE names data directory '$PF_DIR', not '$PGDATA'. Nothing was started or stopped and the file was left in place." >&2
    stale_pid_recovery; exit 1
  fi
  if pid_alive "$PF_PID" && ! pid_is_ours "$PF_PID"; then
    echo "braindb: STALE PID FILE: $PIDFILE names pid $PF_PID, which is alive but is NOT this index's server (it was not started with -D $PGDATA). This happens after a power cut or a pulled drive, when the old pid number is reused. Nothing was started or stopped and the file was left in place." >&2
    stale_pid_recovery; exit 1
  fi
  return 0
}

check_sockdir() {
  local sock="$SOCKDIR/.s.PGSQL.$PORT"
  [ "${#sock}" -lt 104 ] || die "REFUSED: the socket path is ${#sock} bytes, macOS allows 103: set BRAINDB_SOCKDIR to a shorter directory"
  if [ ! -e "$SOCKDIR" ] && [ ! -L "$SOCKDIR" ]; then
    mkdir -m 700 "$SOCKDIR" || die "cannot create the socket directory $SOCKDIR"
  fi
  [ ! -L "$SOCKDIR" ] || die "REFUSED: the socket directory $SOCKDIR is a symlink"
  [ -d "$SOCKDIR" ] || die "REFUSED: $SOCKDIR exists and is not a directory"
  [ "$(stat -f '%u' "$SOCKDIR")" = "$(id -u)" ] || die "REFUSED: $SOCKDIR is not owned by this user"
  [ "$(stat -f '%Lp' "$SOCKDIR")" = "700" ] || die "REFUSED: $SOCKDIR is not mode 700 (it is $(stat -f '%Lp' "$SOCKDIR"))"
}

export_env() {
  export BRAINDB_ROOT_EFF="$ROOT" BRAINDB_SCOPE_EFF="$SCOPE" BRAINDB_SEAT="$SEAT" BRAINDB_PGDATA_EFF="$PGDATA"
  export BRAINDB_SOCKDIR_EFF="$SOCKDIR" BRAINDB_PORT_EFF="$PORT" BRAINDB_PGBIN_EFF="$PGBIN" BRAINDB_LOCK_EFF="$LOCKFILE"
}
indexer() { export_env; "$PY" "$LANE/braindb_index.py" "$@"; }
# locked <internal command>: run it in a fresh braindb.sh while holding the cluster's lock, so two commands
# can never run initdb or pg_ctl on one data directory at the same time (the second waits its turn).
locked() { "$PY" "$LANE/braindb_lock.py" "$LOCKFILE" 150 /bin/bash "$SELF" "$@"; }

cmd_init() {
  find_pgbin
  if [ -e "$PGDATA" ] || [ -L "$PGDATA" ]; then
    die "REFUSED: $PGDATA already exists. The index is disposable: to start over, move it aside (mv -n \"$PGDATA\" \"$(dirname "$PGDATA")/_quarantine_\$(date +%F)/\") and run init, start, rebuild."
  fi
  "$PGBIN/initdb" -D "$PGDATA" --auth-local=peer --auth-host=reject --encoding=UTF8 --locale=C --no-instructions \
    || die "initdb failed for $PGDATA"
  cat >> "$PGDATA/postgresql.conf" <<'CONF'

# --- brain-db (written by braindb.sh init) ---------------------------------------------
# A rebuildable search index. No network listener, ever: Unix socket only.
listen_addresses = ''
unix_socket_permissions = 0700
max_connections = 10
shared_buffers = 64MB
logging_collector = off
CONF
  [ "$?" -eq 0 ] || die "could not write the brain-db settings into postgresql.conf"
  echo "init: cluster created at $PGDATA (Postgres $(cat "$PGDATA/PG_VERSION"), seat $SEAT). Stopped. Next: start, rebuild."
}

cmd_start() {
  find_pgbin
  [ -d "$PGDATA" ] || die "no cluster at $PGDATA (run: braindb.sh init)"
  [ -f "$PGDATA/PG_VERSION" ] || die "$PGDATA has no PG_VERSION file: not a Postgres cluster"
  local have want
  have="$(tr -d ' \n' < "$PGDATA/PG_VERSION")"; want="$(bin_major)"
  if [ "$have" != "$want" ]; then
    die "REFUSED: the cluster at $PGDATA was made by Postgres $have and the binaries here are Postgres $want. The index is disposable, so rebuild it: move the directory aside (mv -n \"$PGDATA\" \"$(dirname "$PGDATA")/_quarantine_\$(date +%F)/\"), then init, start, rebuild."
  fi
  if running; then
    echo "start: already running (pid $PF_PID, $PGDATA)"; return 0
  fi
  foreign_pidfile_guard
  check_sockdir
  if ! "$PGBIN/pg_ctl" -D "$PGDATA" -l "$LOG" -w -t 60 \
    -o "-c listen_addresses='' -c unix_socket_directories='$SOCKDIR' -c unix_socket_permissions=0700 -c port=$PORT" start; then
    # another command may have brought it up between our test and our start: that is success, not failure
    if running; then
      echo "start: already running (pid $PF_PID, $PGDATA; started by another command meanwhile)"; return 0
    fi
    die "the server did not start; last lines of $LOG follow
$(tail -15 "$LOG")"
  fi
  running || die "pg_ctl reported a start but no server of ours is running for $PGDATA"
  echo "start: running (pid $PF_PID, socket $SOCKDIR/.s.PGSQL.$PORT, no TCP listener)"
}

cmd_stop() {
  find_pgbin
  if ! read_pidfile; then
    echo "stop: not running (no pid file in $PGDATA)"; return 0
  fi
  if [ "$PF_DIR" != "$PGDATA" ]; then
    echo "braindb: REFUSED: $PIDFILE names data directory '$PF_DIR', not '$PGDATA'; nothing stopped" >&2
    stale_pid_recovery; exit 1
  fi
  if ! pid_alive "$PF_PID"; then
    echo "stop: not running (pid $PF_PID in the pid file is gone; the stale file is left for the next start to clear)"; return 0
  fi
  if ! pid_is_ours "$PF_PID"; then
    echo "braindb: REFUSED: pid $PF_PID is alive but was not started with -D $PGDATA; it is not this index's server and was not touched" >&2
    stale_pid_recovery; exit 1
  fi
  local pid="$PF_PID"
  "$PGBIN/pg_ctl" -D "$PGDATA" -m fast -w -t 60 stop || die "pg_ctl stop failed for pid $pid"
  if pid_alive "$pid"; then die "pid $pid is still alive after stop"; fi
  echo "stop: stopped pid $pid ($PGDATA)"
}

cmd_status() {
  find_pgbin
  echo "seat: $SEAT   tree: $ROOT"
  echo "data directory: $PGDATA$([ -d "$PGDATA" ] || echo '  (not created: run init)')"
  if [ -f "$PGDATA/PG_VERSION" ]; then
    echo "cluster version: $(tr -d ' \n' < "$PGDATA/PG_VERSION")   binaries: $("$PGBIN/postgres" --version)"
  fi
  if running; then
    echo "server: RUNNING (pid $PF_PID, socket $SOCKDIR/.s.PGSQL.$PORT)"
    if [ -f "$SCOPE" ]; then indexer info; fi
    return 0
  fi
  echo "server: STOPPED"
  return 3
}

cmd_ensure() { # under the lock: init if there is no cluster, start if it is stopped
  running && return 0
  if [ ! -e "$PGDATA" ] && [ ! -L "$PGDATA" ]; then cmd_init || return 1; fi
  cmd_start
}

ensure_up() { # bring the server up for a command that needs it; its messages go to stderr
  [ "${BRAINDB_NO_AUTOSTART:-}" = "1" ] && return 0
  running && return 0
  locked __ensure >&2
}

cmd_up() {
  need_scope
  find_pgbin
  running || locked __ensure || return 1
  if indexer check; then return 0; fi
  indexer rebuild && indexer check
}

cmd_doctor() { # ONE line for doctor.sh. Starts nothing, stops nothing. rc 0 = ok or not adopted, rc 1 = warn.
  if ! find_pgbin_soft; then echo "WARN brain-db: Postgres 15 binaries missing | brew install postgresql@15 (PORTABILITY 25 and the brain-db item)"; return 1; fi
  if [ ! -f "$SCOPE" ]; then echo "OK brain-db: not adopted on this seat (no scope/$SEAT.scope)"; return 0; fi
  if [ ! -f "$PGDATA/PG_VERSION" ]; then echo "WARN brain-db: no cluster yet | run 2_Project_Files/brain-db/braindb.sh up"; return 1; fi
  local have want out rc first
  have="$(tr -d ' \n' < "$PGDATA/PG_VERSION")"; want="$(bin_major)"
  if [ "$have" != "$want" ]; then echo "WARN brain-db: cluster is Postgres $have, binaries are Postgres $want | quarantine pgdata-$SEAT (mv -n) and run braindb.sh up"; return 1; fi
  out="$(BRAINDB_NO_AUTOSTART=1 indexer check 2>&1)"; rc=$?
  first="$(printf '%s\n' "$out" | sed -n 1p)"
  case "$rc" in
    0) echo "OK brain-db: index current, $PGDATA (${first#check: })"; return 0 ;;
    3) echo "OK brain-db: server stopped (on demand; the next search starts it), $PGDATA"; return 0 ;;
    1) echo "WARN brain-db: index stale, $PGDATA | braindb.sh rebuild (${first#check: })"; return 1 ;;
    4) echo "WARN brain-db: ANOTHER cluster is answering on this seat's socket directory $SOCKDIR | $first"; return 1 ;;
    *) echo "WARN brain-db: check could not run (rc $rc) | $first"; return 1 ;;
  esac
}

case "${1:-}" in
  init)    locked __init ;;
  start)   locked __start ;;
  stop)    locked __stop ;;
  __init)  cmd_init ;;
  __start) cmd_start ;;
  __stop)  cmd_stop ;;
  __ensure) cmd_ensure ;;
  status)  cmd_status ;;
  up)      cmd_up ;;
  doctor)  cmd_doctor ;;
  rebuild|check|search|at)
           need_scope; find_pgbin; ensure_up || exit 1; indexer "$@" ;;
  ""|-h|--help|help)
           sed -n '2,22p' "$SELF" ;;
  *)       die "unknown command '$1' (init start stop status up rebuild check search at doctor)" ;;
esac
