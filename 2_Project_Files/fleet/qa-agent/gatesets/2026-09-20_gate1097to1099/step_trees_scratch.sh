#!/bin/bash
# step_trees_scratch.sh — the merged tree after EACH step of the suggested merge order #1097 -> #1098 -> #1099 (auth last) over develop c87458bdd,
# by merge-tree --write-tree in a fresh `git clone --shared --no-checkout` under the session scratchpad (write verbs there only). A squash of a
# fast-forwardable single-commit PR yields the same tree as this 3-way merge; each step is controlled against scratch-index composition.
set -u
REPO='/Volumes/DevMASTER/!CODING/Secuura/Blockchain/2_Project_Files'
SCRATCH='/private/tmp/claude-501/-Volumes-DevMASTER-WEDNESDAY/fd1ce61d-09bc-4b11-b5ed-43cb67420198/scratchpad'
DEV=c87458bdd8a9dd5ae3a082612e467cda5539aebc
H1097=f5364217952c1cb4d3755fbf8604b3edde124c42; H1098=efce14bed4a8adda15bca124fa60ae7d894fa6a6; H1099=b68aaf9b4581e67369be33d8ebcf4d61886c039b
echo "step_trees_scratch $(date '+%Y-%m-%d %H:%M:%S %Z')"
W="$(mktemp -d "${SCRATCH:?}/steps1097-XXXXXX")"; C="$W/clone"
git clone -q --shared --no-checkout "$REPO" "$C" || exit 3
cur=$DEV; ix="$W/index"; GIT_INDEX_FILE="$ix" git -C "$C" read-tree "$DEV" || exit 4
for pair in "1097:$H1097" "1098:$H1098" "1099:$H1099"; do
  n=${pair%%:*}; h=${pair#*:}
  t="$(git -C "$C" merge-tree --write-tree --merge-base="$DEV" "$cur" "$h")" || { echo "CONFLICT at #$n"; exit 5; }
  cur="$(git -C "$C" commit-tree "$t" -p "$cur" -m "scratch squash-equivalent #$n")" || exit 6
  while IFS=$'\t' read -r meta path; do set -- $meta; GIT_INDEX_FILE="$ix" git -C "$C" update-index --cacheinfo "$2,$4,$path" || exit 7; done < <(git -C "$C" diff --raw --no-abbrev "$DEV" "$h")
  it="$(GIT_INDEX_FILE="$ix" git -C "$C" write-tree)"
  echo "  after #$n: merged tree $t | index composition $it | equal: $([ "$t" = "$it" ] && echo True || echo False)"
  [ "$t" = "$it" ] || exit 8
done
echo "STEPS OK (scratch dir left in place, never deleted: $W)"
