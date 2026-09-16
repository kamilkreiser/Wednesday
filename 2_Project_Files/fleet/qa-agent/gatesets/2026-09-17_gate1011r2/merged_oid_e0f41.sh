#!/bin/zsh
# merged_oid_e0f41.sh — merged-tree OID for head 6dc825644 + develop e0f41a8fa. READ on the checkout (cat-file); merge-tree --write-tree only in the drafter's OWN clone.
R='/Volumes/DevMASTER/!CODING/Secuura/Blockchain/2_Project_Files'
C=/private/tmp/claude-501/-Volumes-DevMASTER-WEDNESDAY/76d545ac-4e62-4400-be44-c9ce11c3c344/scratchpad/gate1011r2_draft_cjm5soog/clone
echo "merged_oid $(date '+%Y-%m-%d %H:%M:%S %Z')"
echo "checkout cat-file e0f41a8fa: $(git -C "$R" cat-file -t e0f41a8fafd64fa31524390cfeab320e822f3d15 2>&1)"
echo "clone cat-file e0f41a8fa: $(git -C "$C" cat-file -t e0f41a8fafd64fa31524390cfeab320e822f3d15 2>&1)"
if git -C "$C" cat-file -e e0f41a8fafd64fa31524390cfeab320e822f3d15 2>/dev/null; then
  T=$(git -C "$C" merge-tree --write-tree 6dc8256448b50de6a15519001a4f7032ace1ae19 e0f41a8fafd64fa31524390cfeab320e822f3d15); rc=$?
  echo "merge-tree --write-tree head e0f41a8fa rc=$rc tree $T"
  echo "api-gateway subtree $(git -C "$C" rev-parse $T:Blockchain/Dev/services/api-gateway)"
fi
