#!/bin/bash
# copy_datasec_retry.sh - copy !CODING/Datasec from Laptop-DEV to DevDRIVE_Studio, resuming after drive drops.
# Kam 2026-11-09 16:12:48 (live board): "no. don't cap. keep copying. not sure why it dropped".
# Uncapped. Before EVERY attempt it proves the destination is the real volume (mounted, UUID below),
# so a drop can never send writes anywhere else. Gives up after MAX attempts; rc of the last rsync is printed.
SRC='/Volumes/Laptop-DEV/!CODING/Datasec/'
MNT='/Volumes/DevDRIVE_Studio'
DST="$MNT/!CODING/Datasec/"
UUID='45997621-42C4-49ED-885A-55EFE695A042'
MAX=8
LOG="${1:?usage: copy_datasec_retry.sh <logfile>}"
mounted_ok() {
  /sbin/mount | /usr/bin/grep -q " on $MNT (" || return 1
  [ "$(/usr/sbin/diskutil info "$MNT" 2>/dev/null | /usr/bin/awk -F': *' '/Volume UUID/{print $2; exit}')" = "$UUID" ]
}
n=0; rc=99
while [ $n -lt $MAX ]; do
  n=$((n+1))
  w=0
  until mounted_ok; do
    [ $w -ge 120 ] && { echo "$(date '+%F %T') attempt $n: volume not back after 60 min - giving up"; echo "COPY RC=$rc attempts=$n"; exit 1; }
    [ $w = 0 ] && echo "$(date '+%F %T') attempt $n: waiting for $MNT (UUID $UUID) to mount"
    sleep 30; w=$((w+1))
  done
  echo "$(date '+%F %T') attempt $n: start"
  /opt/homebrew/bin/rsync -aHX --info=stats1,progress2 "$SRC" "$DST"
  rc=$?
  echo "$(date '+%F %T') attempt $n: rsync rc=$rc"
  # 0 = complete. 23/24 = some files not transferred: a drop mid-run ALSO ends 23 (pass 1 did), so 23/24 stops
  # only when the PREVIOUS attempt also ended 23/24 (two full runs agree the residue is the unreadable files).
  [ $rc = 0 ] && break
  case "$prev:$rc" in 23:23|23:24|24:23|24:24) break ;; esac
  prev=$rc
  sleep 20
done
echo "COPY RC=$rc attempts=$n"
date '+%F %T'
