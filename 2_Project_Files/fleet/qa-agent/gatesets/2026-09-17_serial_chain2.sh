#!/bin/bash
# 2026-09-17_serial_chain2.sh — the 22:08 Wednesday seat's replacement for 2026-09-17_serial_chain.sh.
# WHY: chain 1's launch() wrote each --check to "$LOG.<name>.check" with <name> = "QA/Secuura-1029";
# the slash made the redirect fail (rc 1) before the launcher ran, so #1029 was FALSELY refused at
# 22:18:09 while its own --check was rc 0. Here the check file name is SANITISED and the refusal
# prints the check file's tail into the log, so a refusal can be read.
# Serial: #1029 (launched by hand 22:2x) must end -> #1031 -> #1031 must end -> #1032 (only once its
# drafted launcher exists and its --check is rc 0). Each launch re-runs the usage gate and --check.
# Survives a rotation (nohup, stdin/out/err redirected). Bound 360 min. CHAIN_DRY=1: one launch()
# of #1031 with --check but NO cockpit add, then exit (the exercise before arming).
W=/Volumes/DevMASTER/WEDNESDAY
Q=$W/2_Project_Files/fleet/qa-agent
LOG=$Q/gatesets/2026-09-17_serial_chain2.log
log() { echo "$(date '+%F %T') $*" >> "$LOG"; }
load1() { sysctl -n vm.loadavg | awk '{print $2}'; }
procs() { pgrep -f "$1" | wc -l | tr -d ' '; }
launch() { # $1 pane name  $2 launcher
  local safe; safe=$(printf '%s' "$1" | tr -c 'A-Za-z0-9._-' '_')
  local cf="$Q/gatesets/2026-09-17_serial_chain2.$safe.check"
  bash "$W/2_Project_Files/fleet/usage_gate.sh" --check >> "$LOG" 2>&1 || { log "$1: usage gate refused — NOT launched"; return 1; }
  bash "$2" --check > "$cf" 2>&1; local c=$?
  log "$1: --check rc=$c (output $cf, $(wc -c < "$cf" | tr -d ' ') B)"
  if [ $c -ne 0 ]; then log "$1: check refused — NOT launched; tail:"; tail -5 "$cf" >> "$LOG"; return 1; fi
  if [ "${CHAIN_DRY:-0}" = 1 ]; then log "$1: DRY — would cockpit add now"; return 0; fi
  bash "$W/2_Project_Files/fleet/cockpit/cockpit.sh" add "$1" "bash '$2'" >> "$LOG" 2>&1; log "$1: cockpit add rc=$?"
}
L31="$Q/launchers/launch_qa_secuura_ks1213_1031.sh"
L32="$Q/launchers/launch_qa_secuura_ks1194_1032.sh"
if [ "${CHAIN_DRY:-0}" = 1 ]; then log "DRY run (pid $$)"; launch "QA/Secuura-1031" "$L31"; log "DRY rc=$?"; exit 0; fi
log "START chain2 (pid $$)"
stage=1031; i=0
while [ $i -lt 360 ]; do
  L=$(load1)
  b29=$(procs 'launch_qa_secuura_ks1180p1_10[2]9'); b31=$(procs 'launch_qa_secuura_ks1213_10[3]1'); b32=$(procs 'launch_qa_secuura_ks1194_10[3]2')
  if [ "$stage" = 1031 ] && [ "$b29" = 0 ] && [ "$(echo "$L < 30" | bc)" = 1 ]; then
    log "stage 1031: b29=$b29 load=$L"
    if launch "QA/Secuura-1031" "$L31"; then stage=1032; sleep 120; else log "stage 1031 refused — retry in 10 min"; sleep 600; fi
  elif [ "$stage" = 1032 ] && [ "$b31" = 0 ] && [ "$b29" = 0 ] && [ "$(echo "$L < 30" | bc)" = 1 ]; then
    if [ ! -f "$L32" ]; then
      [ $((i % 15)) = 0 ] && log "stage 1032: launcher not drafted yet ($L32) — waiting"
    else
      log "stage 1032: b31=$b31 load=$L"
      if launch "QA/Secuura-1032" "$L32"; then stage=done; else log "stage 1032 refused — retry in 10 min"; sleep 600; fi
    fi
  fi
  [ "$stage" = done ] && { log "chain2 complete"; exit 0; }
  sleep 60; i=$((i+1))
done
log "BOUND HIT at stage=$stage"
