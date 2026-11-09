#!/bin/bash
# copy_datasec_to_datasecdev.sh - copy !CODING/Datasec from Laptop-DEV to Datasec_DEV (Kam 2026-11-09 16:3x:
# "Lets try a new drive. I put in another drive called Datasec_DEV lets use this as your new drive").
# Active projects first, so a full drive leaves only idle ones behind. -S keeps sparse files sparse.
# UUID guard before every project: a drop or a remount elsewhere can never redirect writes.
SRC='/Volumes/Laptop-DEV/!CODING/Datasec'
MNT='/Volumes/Datasec_DEV'
DST="$MNT/!CODING/Datasec"
UUID='36BFD36F-0DA2-45D9-A87F-562E99538556'
RS=/opt/homebrew/bin/rsync
guard() {
  /sbin/mount | /usr/bin/grep -q " on $MNT (" || { echo "GUARD: $MNT not mounted"; return 1; }
  [ "$(/usr/sbin/diskutil info "$MNT" 2>/dev/null | /usr/bin/awk -F': *' '/Volume UUID/{print $2; exit}')" = "$UUID" ] || { echo "GUARD: UUID mismatch"; return 1; }
}
FIRST=("NexusAI" "HPSM-POC" "Datasec MPS Commercial Calculator" "Datasec Security Composer" "Vision_Sales_Portal" "ATTIO")
guard || exit 9
mkdir -p "$DST" || exit 9
worst=0
copy_one() {
  local name="$1"
  guard || { echo "STOP before $name"; exit 9; }
  echo "$(date '+%F %T') START $name"
  if [ -d "$SRC/$name" ]; then "$RS" -aHXS --info=stats1 "$SRC/$name/" "$DST/$name/"; else "$RS" -aHXS --info=stats1 "$SRC/$name" "$DST/"; fi
  local rc=$?
  echo "$(date '+%F %T') END $name rc=$rc  free=$(/bin/df -h "$MNT" | /usr/bin/awk 'NR==2{print $4}')"
  [ $rc -gt $worst ] && worst=$rc
}
for p in "${FIRST[@]}"; do copy_one "$p"; done
for path in "$SRC"/* "$SRC"/.[!.]*; do
  [ -e "$path" ] || continue
  name="$(basename "$path")"
  skip=0; for p in "${FIRST[@]}"; do [ "$p" = "$name" ] && skip=1; done
  [ $skip = 1 ] && continue
  copy_one "$name"
done
echo "COPY WORST RC=$worst"
date '+%F %T'
