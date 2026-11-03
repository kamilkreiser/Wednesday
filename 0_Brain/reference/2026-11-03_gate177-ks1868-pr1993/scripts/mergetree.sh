#!/bin/bash
# mergetree.sh : Q8. All write verbs run in the gate's own clone (repo/). Shared paths + 4-PR group merge in two orders + planted control.
set -u
W=/Volumes/DevMASTER/WEDNESDAY/0_Brain/reference/2026-11-03_gate177-ks1868-pr1993
g() { git -C $W/repo "$@"; }
export GIT_AUTHOR_NAME=gate177 GIT_AUTHOR_EMAIL=gate177@invalid GIT_COMMITTER_NAME=gate177 GIT_COMMITTER_EMAIL=gate177@invalid GIT_AUTHOR_DATE='2026-11-03T00:00:00Z' GIT_COMMITTER_DATE='2026-11-03T00:00:00Z'
P=$W/results
for p in 1990 1991 1992 1993; do g diff --name-only refs/gate/develop refs/gate/$p | sort > $P/paths_$p.txt; echo "PR $p files $(wc -l < $P/paths_$p.txt | tr -d ' ') merge-base $(g merge-base refs/gate/develop refs/gate/$p | cut -c1-12)"; done
for p in 1990 1991 1992; do echo "shared paths 1993&$p: $(comm -12 $P/paths_1993.txt $P/paths_$p.txt | wc -l | tr -d ' ')"; done
echo "control 1993&1993: $(comm -12 $P/paths_1993.txt $P/paths_1993.txt | wc -l | tr -d ' ')"
for p in 1990 1991 1992; do echo "shared directories 1993 vs $p:"; comm -12 <(sed -E 's#/[^/]+$##' $P/paths_1993.txt | sort -u) <(sed -E 's#/[^/]+$##' $P/paths_$p.txt | sort -u) | sed 's/^/  /'; done
T=$(g merge-tree --write-tree refs/gate/develop refs/gate/1993); echo "develop+1993 rc $? tree ${T:0:12} (head tree $(g rev-parse 'refs/gate/1993^{tree}' | cut -c1-12))"
mk() { g commit-tree "$1" -p "$2" -p "$3" -m "$4"; }
chain() { local C=refs/gate/develop rcs="" t; for p in "$@"; do t=$(g merge-tree --write-tree $C refs/gate/$p); rcs="$rcs $?"; C=$(mk $t $C refs/gate/$p m$p); done; echo "order $*: rc$rcs group tree $(g rev-parse $C^{tree} | cut -c1-12)"; }
chain 1990 1991 1992
chain 1990 1991 1992 1993
chain 1993 1992 1991 1990
chain 1993 1990 1991 1992
echo "is 844fb7714826 an object in my clone: $(g cat-file -t 844fb7714826 2>&1)"
F=Blockchain/Dev/packages/shared/src/vc/verifier.ts
B=$(g show refs/gate/develop:$F | sed 's/const msg = err instanceof Error ? err.message : String(err);/const msg = "PLANTED gate177 conflict";/' | g hash-object -w --stdin)
echo "planted blob differs from develop: $([ "$B" != "$(g rev-parse refs/gate/develop:$F)" ] && echo yes || echo NO)"
idx=$W/tmp/plant.index
GIT_INDEX_FILE=$idx g read-tree refs/gate/develop && GIT_INDEX_FILE=$idx g update-index --cacheinfo 100644,$B,$F && TPT=$(GIT_INDEX_FILE=$idx g write-tree)
CP=$(g commit-tree $TPT -p refs/gate/develop -m planted)
out=$(g merge-tree --write-tree --name-only $CP refs/gate/1993); rp=$?
echo "planted control vs 1993: rc $rp; output lines after the tree:"; echo "$out" | sed -n '2,6p'
