#!/bin/bash
# 2026-09-17_serial_chain.sh — survives a Wednesday rotation (launched with nohup, stdin/out/err redirected).
# Serialises tonight's remaining QA gates and restarts Ornith when load allows:
#   #1030 (running) -> launch #1029 -> launch #1031 ; Ornith night_run.sh when 1-min load < 12.
# Each launch re-runs the usage gate and the launcher's own --check first; a refusal stops that launch (logged).
# Log: gatesets/2026-09-17_serial_chain.log. Bounds: 300 min total.
W=/Volumes/DevMASTER/WEDNESDAY
Q=$W/2_Project_Files/fleet/qa-agent
LOG=$Q/gatesets/2026-09-17_serial_chain.log
N=$W/2_Project_Files/local-model/night
log() { echo "$(date '+%F %T') $*" >> "$LOG"; }
load1() { sysctl -n vm.loadavg | awk '{print $2}'; }
procs() { pgrep -f "$1" | wc -l | tr -d ' '; }
launch() { # $1 name  $2 launcher
  bash "$W/2_Project_Files/fleet/usage_gate.sh" --check >> "$LOG" 2>&1 || { log "$1: usage gate refused — NOT launched"; return 1; }
  bash "$2" --check > "$LOG.$1.check" 2>&1; local c=$?
  log "$1: --check rc=$c"; [ $c -ne 0 ] && { log "$1: check refused — NOT launched"; return 1; }
  bash "$W/2_Project_Files/fleet/cockpit/cockpit.sh" add "$1" "bash '$2'" >> "$LOG" 2>&1; log "$1: cockpit add rc=$?"
}
log "START chain (pid $$)"
stage=1029; ornith_done=0; i=0
while [ $i -lt 300 ]; do
  L=$(load1)
  if [ $ornith_done = 0 ] && [ "$(echo "$L < 12" | bc)" = 1 ] && [ ! -e "$N/log/.night_run.lock" ]; then
    log "ornith: load $L < 12 — night_run.sh"; bash "$N/night_run.sh" >> "$LOG.ornith" 2>&1; log "ornith: END rc=$?"; ornith_done=1
  fi
  b30=$(procs 'launch_qa_secuura_ks1211_10[3]0'); b29=$(procs 'launch_qa_secuura_ks1180p1_10[2]9'); b31=$(procs 'launch_qa_secuura_ks1213_10[3]1')
  if [ "$stage" = 1029 ] && [ "$b30" = 0 ] && [ "$(echo "$L < 30" | bc)" = 1 ]; then
    log "stage 1029: b30=$b30 load=$L"; launch "QA/Secuura-1029" "$Q/launchers/launch_qa_secuura_ks1180p1_1029.sh"; stage=1031; sleep 120
  elif [ "$stage" = 1031 ] && [ "$b29" = 0 ] && [ "$b30" = 0 ] && [ "$(echo "$L < 30" | bc)" = 1 ]; then
    log "stage 1031: b29=$b29 b30=$b30 load=$L"; launch "QA/Secuura-1031" "$Q/launchers/launch_qa_secuura_ks1213_1031.sh"; stage=done
  fi
  [ "$stage" = done ] && [ $ornith_done = 1 ] && { log "chain complete"; exit 0; }
  sleep 60; i=$((i+1))
done
log "BOUND HIT at stage=$stage ornith_done=$ornith_done"
