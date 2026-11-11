#!/bin/bash
# devmaster_linkwatch.sh: record WHY /Volumes/DevMASTER drops off the Mac mini.
# Kam, terminal 2026-11-12 ~09:0x: "Can you monitor if its the stick or the OS that is doing this".
#
# WHERE IT RUNS (2026-09-20 lesson, a guard inside the thing it guards): NOT from the drive.
# install: copy this file to ~/Library/Application Support/wednesday/devmaster_linkwatch.sh and load
# launchd job com.wednesday.dmlinkwatch (KeepAlive). Logs: ~/Library/Logs/wednesday_devmaster_linkwatch/.
#
# HOW TO READ A DROP (state.log + events.log, same minute):
#  HARDWARE/LINK: kernel "[Port-USB-C@N: CIO] active: NO" or "hardware connection lost" or
#                 "cableChangeOccurred: powering off" FIRST, disk ABSENT from diskutil, no powerd sleep or
#                 diskarbitrationd eject/unmount BEFORE it. The unsafe-shutdown counter goes up by one.
#  OS-INITIATED:  a diskarbitrationd unmount/eject or a powerd sleep line BEFORE any link line, and the disk
#                 stays PRESENT in diskutil while the volume is ABSENT.
#  THERMAL (SSD): nvme_temp near 82 C (warning) / 85 C (critical) in the minutes before. The ENCLOSURE's bridge
#                 chip has no sensor we can read: a link drop with a cool SSD under heavy load is consistent
#                 with the bridge overheating, a power dip or the cable. That part is NOT measured.
set -u
D="$HOME/Library/Logs/wednesday_devmaster_linkwatch"
mkdir -p "$D"
SMART=/opt/homebrew/bin/smartctl
ts() { date '+%Y-%m-%d %H:%M:%S'; }
PRED='(process == "kernel" AND (eventMessage CONTAINS "Port-USB-C" OR eventMessage CONTAINS "hardware connection lost" OR eventMessage CONTAINS "UGREEN" OR eventMessage CONTAINS "cableChangeOccurred" OR eventMessage CONTAINS "IOThunderboltSwitch" OR eventMessage CONTAINS[c] "over-current" OR eventMessage CONTAINS[c] "overcurrent" OR eventMessage CONTAINS "unclean unmount" OR eventMessage CONTAINS "apfs_vfsop_unmount")) OR process == "diskarbitrationd" OR (process == "powerd" AND (eventMessage CONTAINS[c] "sleep" OR eventMessage CONTAINS[c] "wake")) OR (process == "logger" AND eventMessage CONTAINS "dmlinkwatch-selftest")'
/usr/bin/log stream --style compact --predicate "$PRED" >> "$D/events.log" 2>> "$D/stream.err" &
SP=$!
trap 'kill "$SP" 2>/dev/null' EXIT
echo "$(ts) START pid $$ stream pid $SP" >> "$D/state.log"

nvme() { # temp, unsafe shutdowns, warning-temp minutes
  local dev="$1"
  [ -n "$dev" ] && [ -x "$SMART" ] || { echo "nvme=unreadable"; return; }
  "$SMART" -a "$dev" 2>&1 | awk -F: '/^Temperature:/{t=$2} /Unsafe Shutdowns/{u=$2} /Warning  Comp. Temperature Time/{w=$2} END{gsub(/ /,"",t);gsub(/ /,"",u);gsub(/ /,"",w);printf "nvme_temp=%s unsafe_shutdowns=%s warn_temp_min=%s", t,u,w}'
}
prev=""; n=0
while :; do
  kill -0 "$SP" 2>/dev/null || { echo "$(ts) STREAM DIED (rc unknown): exiting for launchd to restart" >> "$D/state.log"; exit 3; }
  if [ -d /Volumes/DevMASTER/WEDNESDAY ]; then m=MOUNTED; else m=ABSENT; fi
  dev=$(diskutil list external physical 2>/dev/null | awk '/^\/dev\/disk/{d=$1} /Samsung|4\.0 TB/{if(d!=""){print d; exit}}')
  if [ -n "$dev" ]; then p="disk_present($dev)"; else p=disk_absent; fi
  s="$m $p"
  if [ "$s" != "$prev" ] || [ $((n % 6)) -eq 0 ]; then
    line="$(ts) $( [ "$s" != "$prev" ] && echo CHANGE || echo tick ) $s (was ${prev:-start}) load1=$(sysctl -n vm.loadavg | awk '{print $2}') $(nvme "$dev")"
    echo "$line" >> "$D/state.log"
    # RE-ARM ON REMOUNT (2026-11-12 ledger: Kam's messages unread ~30 min after the 09:17 drop because
    # every drop kills wake_watch_runner and wedges live_chat_poll, and nothing re-armed them).
    case "$prev" in ABSENT*) if [ "$m" = MOUNTED ]; then
      sleep 20
      W=/Volumes/DevMASTER/WEDNESDAY; C="$W/2_Project_Files/fleet/cockpit"
      for p in $(pgrep -f 'cockpit/live_chat_poll\.sh --seat wednesday'); do kill "$p"; done
      python3 -I -c 'import subprocess,sys; log=open(sys.argv[2],"a"); p=subprocess.Popen(["bash",sys.argv[1],"--seat","wednesday"],stdin=subprocess.DEVNULL,stdout=log,stderr=subprocess.STDOUT,start_new_session=True); print(p.pid)' "$C/live_chat_poll.sh" "$C/logs/live_chat_poll.log" > "$D/rearm_poll.out" 2>&1
      WED_AGENT=wednesday bash "$C/arm_wake_watch.sh" > "$D/rearm_wake.out" 2>&1
      echo "$(ts) REARMED after remount: poll pid $(cat "$D/rearm_poll.out") | $(tail -1 "$D/rearm_wake.out")" >> "$D/state.log"
    fi ;; esac
    prev="$s"
  fi
  n=$((n + 1))
  sleep 10
done
