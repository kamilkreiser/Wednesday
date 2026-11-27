#!/bin/bash
# manifest.sh <out file>: sha256 of every lane file outside pgdata/quarantine/pyc; stat listing of pgdata, quarantine, lock;
# sha256 of both earlier checkers' folders; sha256 of the real brain's learnings folder (lesson files, rules index, ledger: hash only, no content read)
L=/Volumes/DevMASTER/WEDNESDAY/2_Project_Files/brain-db
C1=/Volumes/DevMASTER/WEDNESDAY/0_Brain/reference/2026-11-27_qa-braindb
C2=/Volumes/DevMASTER/WEDNESDAY/0_Brain/reference/2026-11-27_qa-braindb-r3
B=/Volumes/DevMASTER/WEDNESDAY/0_Brain/learnings
{
echo "-- lane files"
find "$L" -type f -not -path '*/pgdata-*' -not -path '*/_quarantine_*' -not -name '*.pyc' -print0 | sort -z | xargs -0 shasum -a 256
echo "-- pgdata + quarantine + lock stat (path size mtime)"
find "$L" \( -path '*/pgdata-*' -o -path '*/_quarantine_*' -o -name '*.lock' \) -print0 | sort -z | xargs -0 stat -f '%N %z %m'
echo "-- first checker folder"
find "$C1" -type f -print0 | sort -z | xargs -0 shasum -a 256
echo "-- second checker folder"
find "$C2" -type f -print0 | sort -z | xargs -0 shasum -a 256
echo "-- real brain learnings (all files, incl. rules index)"
find "$B" -type f -print0 | sort -z | xargs -0 shasum -a 256
} > "$1" 2>&1
wc -l "$1"
