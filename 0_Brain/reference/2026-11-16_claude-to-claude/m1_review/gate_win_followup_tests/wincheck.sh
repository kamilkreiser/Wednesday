#!/bin/bash
# QA-WIN-FOLLOWUP: Windows type-checks and clippy in the kit method (xwin.sh). Kit C step (cargo-xwin):
# ring's C code is compiled for the target; nothing is linked or run.
W=/private/tmp/claude-501/qwf
X="--locked --target x86_64-pc-windows-msvc"
DT="-p coagent-daemon --lib --bins --test win_rules --test win_datadir --test win_guest --test win_guards"
run(){ n=$1; shift; $W/xwin.sh "$@" > $W/logs/xwin_$n.log 2>&1; rc=$?; echo "$n exit $rc; non-manifest warnings/errors: $(grep -E '^(warning|error)' $W/logs/xwin_$n.log | grep -v 'rand_core\|generated 1 warning' | sort | uniq -c | head -4 | tr '\n' ' ') tail: $(tail -1 $W/logs/xwin_$n.log | cut -c1-90)"; }
case "${1:-head}" in
head)
run head_daemon_check $W/h hwin check $X $DT
run head_daemon_clippy $W/h hwin clippy $X $DT -- -D warnings
run head_relay_check $W/h hwin check $X -p coagent-relay --tests
run head_relay_clippy $W/h hwin clippy $X -p coagent-relay --tests -- -D warnings
run head_cli_check $W/h hwin check $X -p coagent-cli --tests
run head_cli_clippy $W/h hwin clippy $X -p coagent-cli --tests -- -D warnings
run base_cli_check $W/b bwin check $X -p coagent-cli --tests ;;
mut) shift; for m in "$@"; do run mut_$m $W/m_$m m_${m}_win2 clippy $X -p coagent-daemon --lib -- -D warnings; done ;;
esac
