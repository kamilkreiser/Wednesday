#!/usr/bin/env bash
# build.sh <worktree> <portal> <stage-name>: Dockerfile layout build (portal -> app, frontend/shared -> app/vendor/shared)
set -uo pipefail
WT="$1"; P="$2"; N="$3"
ST="/private/tmp/g260/stage/$N"
[ -e "$ST" ] && { echo "stage exists: $ST" >&2; exit 9; }
mkdir -p "$ST/app" || exit 8
cp "$WT/Blockchain/Dev/frontend/$P/package.json" "$WT/Blockchain/Dev/frontend/$P/package-lock.json" "$ST/app/" || exit 7
npm ci --prefix "$ST/app" --no-audit --offline > "/private/tmp/g260/logs/${N}_ci.log" 2>&1; ci=$?
mkdir -p "$ST/app/vendor" && cp -R "$WT/Blockchain/Dev/frontend/shared" "$ST/app/vendor/shared"
tar cf - -C "$WT/Blockchain/Dev/frontend/$P" --exclude node_modules --exclude dist . | tar xf - -C "$ST/app"
SHARED_DIR=./vendor/shared/src npm run build --prefix "$ST/app" > "/private/tmp/g260/logs/${N}_build.log" 2>&1; b=$?
rr=$(node -e 'try{console.log(require(process.argv[1]+"/node_modules/react-router/package.json").version)}catch(e){console.log("none")}' "$ST/app")
rrd=$(node -e 'try{console.log(require(process.argv[1]+"/node_modules/react-router-dom/package.json").version)}catch(e){console.log("none")}' "$ST/app")
echo "$N ci_rc=$ci build_rc=$b react-router=$rr react-router-dom=$rrd src_head=$(git -C "$WT" rev-parse --short=12 HEAD)"
