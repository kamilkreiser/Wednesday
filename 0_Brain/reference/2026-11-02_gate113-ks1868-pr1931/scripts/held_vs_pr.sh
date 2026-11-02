#!/bin/bash
# For each O73 auth run dir: apply out.md.checker/patch.diff strictly on a temp index of base 968f1707, compare resulting blobs to PR head's blobs.
REPO=/Volumes/DevMASTER/WEDNESDAY/0_Brain/reference/2026-11-02_gate113-ks1868-pr1931/repo
RU=/Volumes/DevMASTER/WEDNESDAY/2_Project_Files/local-model/runs
BASE=968f17070208efc1e888308bdea49de5112a42e8; HEAD=bafab56a1edc99eac9b80bd74c402917f3a14cf5
for d in "$RU"/spark_secuura_2026-11-02_ks_1868_o73_p[3456]_*; do
  P="$d/out.md.checker/patch.diff"
  [ -f "$P" ] || { echo "$(basename "$d"): no patch.diff"; continue; }
  TMPI=/private/tmp/claude-501/-Volumes-DevMASTER-WEDNESDAY/a974be12-1abe-4d9a-9532-9c46296d28fc/scratchpad/idx_$(basename "$d")
  GIT_INDEX_FILE="$TMPI" git -C "$REPO" read-tree $BASE
  OUT=$(GIT_INDEX_FILE="$TMPI" git -C "$REPO" apply --cached "$P" 2>&1); RC=$?
  echo "## $(basename "$d") apply_rc=$RC sha=$(shasum -a 256 "$P" | cut -c1-12) $OUT"
  if [ $RC = 0 ]; then
    for f in $(git -C "$REPO" diff --name-only $BASE $HEAD -- 'Blockchain/Dev/services'); do
      A=$(GIT_INDEX_FILE="$TMPI" git -C "$REPO" ls-files -s -- "$f" | awk '{print $2}')
      B=$(git -C "$REPO" rev-parse "$HEAD:$f")
      Bs=$(git -C "$REPO" rev-parse "$BASE:$f" 2>/dev/null)
      [ "$A" = "$Bs" ] && continue
      [ "$A" = "$B" ] && echo "   EQUAL  $f ${A:0:8}" || echo "   DIFF   $f patch=${A:0:8} pr=${B:0:8}"
    done
  fi
done
