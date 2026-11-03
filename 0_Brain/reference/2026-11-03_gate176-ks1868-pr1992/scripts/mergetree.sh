#!/bin/bash
# mergetree.sh : Q8. All write verbs run in the gate's own clone (repo/). Shared paths + group merge in two orders + planted control.
set -u
W=/Volumes/DevMASTER/WEDNESDAY/0_Brain/reference/2026-11-03_gate176-ks1868-pr1992
g() { git -C $W/repo "$@"; }
export GIT_AUTHOR_NAME=gate176 GIT_AUTHOR_EMAIL=gate176@invalid GIT_COMMITTER_NAME=gate176 GIT_COMMITTER_EMAIL=gate176@invalid GIT_AUTHOR_DATE='2026-11-03T00:00:00Z' GIT_COMMITTER_DATE='2026-11-03T00:00:00Z'
P=$W/results
for p in 1990 1991 1992; do g diff --name-only refs/gate/develop refs/gate/$p | sort > $P/paths_$p.txt; echo "PR $p files $(wc -l < $P/paths_$p.txt) merge-base $(g merge-base refs/gate/develop refs/gate/$p | cut -c1-12)"; done
echo "shared paths 1992&1990: $(comm -12 $P/paths_1992.txt $P/paths_1990.txt | wc -l | tr -d ' ')   1992&1991: $(comm -12 $P/paths_1992.txt $P/paths_1991.txt | wc -l | tr -d ' ')   control 1992&1992: $(comm -12 $P/paths_1992.txt $P/paths_1992.txt | wc -l | tr -d ' ')"
echo "shared directories 1992 vs 1990:"; comm -12 <(sed -E 's#/[^/]+$##' $P/paths_1992.txt | sort -u) <(sed -E 's#/[^/]+$##' $P/paths_1990.txt | sort -u)
T=$(g merge-tree --write-tree refs/gate/develop refs/gate/1992); echo "develop+1992 rc $? tree ${T:0:12} (head tree $(g rev-parse 'refs/gate/1992^{tree}' | cut -c1-12))"
mk() { g commit-tree "$1" -p "$2" -p "$3" -m "$4"; }
T1=$(g merge-tree --write-tree refs/gate/develop refs/gate/1990); r1=$?; C1=$(mk $T1 refs/gate/develop refs/gate/1990 c1)
T2=$(g merge-tree --write-tree $C1 refs/gate/1991); r2=$?; C2=$(mk $T2 $C1 refs/gate/1991 c2)
T3=$(g merge-tree --write-tree $C2 refs/gate/1992); r3=$?
echo "order 1990,1991,1992: rc $r1 $r2 $r3 group tree ${T3:0:12}"
U1=$(g merge-tree --write-tree refs/gate/develop refs/gate/1992); s1=$?; D1=$(mk $U1 refs/gate/develop refs/gate/1992 d1)
U2=$(g merge-tree --write-tree $D1 refs/gate/1990); s2=$?; D2=$(mk $U2 $D1 refs/gate/1990 d2)
U3=$(g merge-tree --write-tree $D2 refs/gate/1991); s3=$?
echo "order 1992,1990,1991: rc $s1 $s2 $s3 group tree ${U3:0:12}"
F=Blockchain/Dev/packages/shared/src/security/ssrf-guard.ts
B=$(g show refs/gate/develop:$F | sed 's/refusing to contact an unverifiable destination/PLANTED gate176 conflict/' | g hash-object -w --stdin)
idx=$W/tmp/plant.index
GIT_INDEX_FILE=$idx g read-tree refs/gate/develop && GIT_INDEX_FILE=$idx g update-index --cacheinfo 100644,$B,$F && TPT=$(GIT_INDEX_FILE=$idx g write-tree)
CP=$(g commit-tree $TPT -p refs/gate/develop -m planted)
out=$(g merge-tree --write-tree --name-only $CP refs/gate/1992); rp=$?
echo "planted control vs 1992: rc $rp; output lines after the tree:"; echo "$out" | sed -n '2,6p'
