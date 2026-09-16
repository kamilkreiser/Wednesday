#!/bin/zsh
# blob_dump.sh — READ-ONLY: git show / git diff (read verbs) from the Secuura checkout into the #1008 gate set's src/.
R='/Volumes/DevMASTER/!CODING/Secuura/Blockchain/2_Project_Files'
G='/Volumes/DevMASTER/WEDNESDAY/2_Project_Files/fleet/qa-agent/gatesets/2026-09-17_gate1008'
H=dd7086d5aa574285beffc515f9371a438621f25d
DEV=93629700c3d219c1d8ca61d69150bb9b623fc1be
V=Blockchain/Dev/services/api-gateway/src/routes/verification.ts
T=Blockchain/Dev/services/api-gateway/src/__tests__/ks1087-workflow-approve-deletes-the-pending-document.test.ts
echo "blob_dump $(date '+%Y-%m-%d %H:%M:%S %Z')"
git -C "$R" show "$DEV:$V" > "$G/src/verification_develop.ts"
git -C "$R" show "$H:$V" > "$G/src/verification_head.ts"
git -C "$R" show "$H:$T" > "$G/src/ks1087_head.test.ts"
git -C "$R" diff "$DEV" "$H" > "$G/diff_develop_to_head.patch"
git -C "$R" diff -U0 "$DEV" "$H" -- "$V" > "$G/diff_U0_verification.patch"
wc -l "$G/src/verification_develop.ts" "$G/src/verification_head.ts" "$G/src/ks1087_head.test.ts" "$G/diff_develop_to_head.patch"
shasum -a 256 "$G/src/verification_develop.ts" "$G/src/verification_head.ts" "$G/src/ks1087_head.test.ts"
echo "--- git grep workflow-instances at head (whole Dev tree, filenames + counts)"
git -C "$R" grep -c 'workflow-instances' "$H" -- Blockchain/ | sed "s/^$H://"
echo "--- control: git grep -c 'verify-document' at head"
git -C "$R" grep -c 'verify-document' "$H" -- Blockchain/Dev/services/api-gateway/src/routes/verification.ts | sed "s/^$H://"
