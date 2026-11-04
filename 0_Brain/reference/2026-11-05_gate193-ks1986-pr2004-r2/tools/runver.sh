#!/bin/bash
# Gate 193: overlay verification.ts from <commit> (or a file path with -f), run the PG harness as <label>,
# restore the head blob and check it. usage: runver.sh <label> <commit> | runver.sh <label> -f <file>
W=/Volumes/DevMASTER/WEDNESDAY/0_Brain/reference/2026-11-05_gate193-ks1986-pr2004-r2
R=$W/repo; REL=Blockchain/Dev/services/originate/src/routes/verification.ts
HEADC=4432db224a5867fdb6afaabf56df08cdf640d067
L="$1"
if [ "$2" = "-f" ]; then cp "$3" $R/$REL; echo "$L overlay from file, blob $(git -C $R hash-object $R/$REL)"
else git -C $R show "$2:$REL" > $R/$REL; echo "$L overlay blob $(git -C $R hash-object $R/$REL) expected $(git -C $R rev-parse $2:$REL)"; fi
bash $W/tools/pgrun.sh "$L"
git -C $R checkout -- $REL
echo "restored blob equal head: $([ "$(git -C $R hash-object $R/$REL)" = "$(git -C $R rev-parse $HEADC:$REL)" ] && echo yes || echo NO)"
tail -2 $W/runs/pg_$L.log
