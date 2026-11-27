#!/bin/bash
# manifest.sh <out file>: sha256 of every lane file outside pgdata/quarantine, stat listing of pgdata, sha256 of the first checker's folder
L=/Volumes/DevMASTER/WEDNESDAY/2_Project_Files/brain-db
C=/Volumes/DevMASTER/WEDNESDAY/0_Brain/reference/2026-11-27_qa-braindb
{
find "$L" -type f -not -path '*/pgdata-*' -not -path '*/_quarantine_*' -not -name '*.pyc' -print0 | sort -z | xargs -0 shasum -a 256
echo "-- pgdata + quarantine stat (path size mtime)"
find "$L" \( -path '*/pgdata-*' -o -path '*/_quarantine_*' -o -name '*.lock' \) -print0 | sort -z | xargs -0 stat -f '%N %z %m'
echo "-- checker folder"
find "$C" -type f -print0 | sort -z | xargs -0 shasum -a 256
} > "$1" 2>&1
wc -l "$1"
