#!/bin/bash
# operator 25: pii-store screen in a scratch git repo (scratchpad). usage: screen_pii.sh <script> <base>
SRC="$1"; B="$2/pii"
mkdir -p "$B/Blockchain/Dev/scripts" "$B/Blockchain/Dev/services/x/node_modules/y/node_modules/z"
cp "$SRC" "$B/Blockchain/Dev/scripts/check-no-pii-store.sh"
git -C "$B" init -q
echo '{}' > "$B/Blockchain/Dev/ks256-pii-data.json"
echo "--- A: untracked ks256-pii-data.json (expect WARNING)"
bash "$B/Blockchain/Dev/scripts/check-no-pii-store.sh"; echo "rc=$?"
echo "--- B: probe the git option used at :56"
git -C "$B" ls-files --others --exclude-standard=false '*pii*.json' '*ks256-pii-data*'; echo "git rc=$?"
echo "--- C: tracked pii file"
echo '{}' > "$B/Blockchain/Dev/foo-pii.json"; git -C "$B" add Blockchain/Dev/foo-pii.json
bash "$B/Blockchain/Dev/scripts/check-no-pii-store.sh"; echo "rc=$?"
echo "--- D: untracked *pii*.json variant only (not ks256 name) - warning leg should name it"
B2="$2/pii2"; mkdir -p "$B2/Blockchain/Dev/scripts"; cp "$SRC" "$B2/Blockchain/Dev/scripts/check-no-pii-store.sh"; git -C "$B2" init -q
echo '{}' > "$B2/Blockchain/Dev/pii-data.local.json"
bash "$B2/Blockchain/Dev/scripts/check-no-pii-store.sh"; echo "rc=$?"
echo "--- E: ks256 store only inside nested node_modules (find -not -path ./node_modules/* does not cover)"
B3="$2/pii3"; mkdir -p "$B3/Blockchain/Dev/scripts" "$B3/Blockchain/Dev/services/x/node_modules/z"; cp "$SRC" "$B3/Blockchain/Dev/scripts/check-no-pii-store.sh"; git -C "$B3" init -q
echo '{}' > "$B3/Blockchain/Dev/services/x/node_modules/z/ks256-pii-data.json"
bash "$B3/Blockchain/Dev/scripts/check-no-pii-store.sh"; echo "rc=$?"
