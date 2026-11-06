#!/bin/bash
# send_go_merge_seat.sh <PR> <full-head> <full-pin> <full-tree> <gate-name> <ticket> <note-file> : head-pinned GO to B 97th, re-reads origin in the same action, refuses on mismatch.
set -u
PR=$1; H=$2; PIN=$3; T=$4; GATE=$5; KEY=$6; NOTE=$7; W=/Volumes/DevMASTER/WEDNESDAY
SP=${SP:-$(mktemp -d)}; SEAT=${SEAT:-Seat B 97th}
R="/Volumes/DevMASTER/!CODING/Secuura/Blockchain/2_Project_Files"
LH=$(git -C "$R" ls-remote origin refs/pull/$PR/head | cut -f1); LD=$(git -C "$R" ls-remote origin refs/heads/develop | cut -f1)
[ "$LH" = "$H" ] || { echo "REFUSED: head moved: $LH"; exit 3; }
[ "$LD" = "$PIN" ] || { echo "REFUSED: develop moved: $LD"; exit 3; }
NOW=$(date '+%H:%M:%S AEDT'); F=$SP/go_$PR.md
{ echo "$SEAT"; echo; echo "GO: merge PR $PR at $H on develop $PIN ($SEAT)."; echo "Expected result tree: $T"; echo
  echo "Wednesday's own ls-remote at $NOW: refs/pull/$PR/head = $LH and refs/heads/develop = $LD, both equal to your READY. If develop moves before you merge, recompute and send a new READY, do not merge."; echo
  cat "$NOTE"; echo
  echo "Grant this sits inside: Kam 2026-09-11 'merge anything that has been finished and tested' ($GATE at this head + Test Evidence), card secuura-wednesday-go-counts-as-kams-word-1030 = a (ruled 2026-10-30T10:08:25+11:00), and Kam 2026-11-06 10:18:02 'complete, merge, archive'. Not a signature class: develop is not production."; echo
  echo "RULED BY KAM, NOT YET IN AN ARTEFACT"; echo "- Kam 2026-11-06 10:19:24 (live board): \"and not just today but for the next 1-2 weeks.  work on these until the board is clear\"."; echo
  echo "PROVENANCE:"; echo "- PR $PR head and develop pin | Wednesday's git ls-remote origin at $NOW | read 2026-11-06"; echo "- Expected tree, items | your READY TO MERGE mail, read by Wednesday | read 2026-11-06"; } > $F
bash $W/2_Project_Files/fleet/send_brief.sh --to "Secuura/Blockchain-B" --subject "GO: merge PR $PR at ${H:0:12} on develop ${PIN:0:12} ($SEAT)" --body-file $F --kind answer > $SP/go_$PR.out 2>&1; rc=$?
echo "send rc=$rc"; sed -n '/REFUSED/,$p' $SP/go_$PR.out | cut -c1-220 | head -6; exit $rc
