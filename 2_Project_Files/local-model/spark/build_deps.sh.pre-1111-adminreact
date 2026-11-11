#!/bin/bash
# build_deps.sh [commit]  — (re)build spark/cache/deps, the Wednesday-owned node_modules store for Spark rounds (2026-11-03).
# WHY: round.sh used to link node_modules FROM the Secuura checkout, which nobody keeps in step with develop; PR 1953
# (zod 3 -> 4) made every round HARNESS-fail on the shared build. Now deps/ is a clone of the same remote checked out
# detached at develop (or the given commit) with `npm ci --ignore-scripts` per lockfile dir; deps/LOCK_KEY = "<key> <commit>".
# round.sh compares LOCK_KEY with the round tip's key (lock_key.sh) and finishes HARNESS on mismatch.
# Idempotent: does nothing when LOCK_KEY already matches develop and node_modules exist (BUILD_DEPS_FORCE=1 rebuilds).
# Refuses while a round/drainer is live (spark/state/round.lock, queue.lock) and holds round.lock itself while it runs.
# Reads origin URL + core.sshCommand from the Secuura checkout (git config --get; key read in place, never copied);
# writes nothing there. Sequential npm ci, every rc logged, stderr kept. bash 3.2, no cd.
# Env: SPARK_SECUURA_CHECKOUT, SPARK_CACHE, SPARK_STATE, SPARK_DEPS.
set -uo pipefail
HERE="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
SECUURA="${SPARK_SECUURA_CHECKOUT:-/Volumes/DevMASTER/!CODING/Secuura/Blockchain/2_Project_Files}"
CACHE="${SPARK_CACHE:-$HERE/cache}"
STATE="${SPARK_STATE:-$HERE/state}"
DEPS="${SPARK_DEPS:-$CACHE/deps}"
SUBDIR="Blockchain/Dev"
say() { echo "build_deps: $*"; }

for l in "$STATE/round.lock" "$STATE/queue.lock"; do
  if [ -d "$l" ]; then
    p="$(cat "$l/pid" 2>/dev/null)"
    if [ -n "$p" ] && kill -0 "$p" 2>/dev/null; then
      say "REFUSED — $l is held by live pid $p ($(cat "$l/what" 2>/dev/null)); wait for the round/drainer to finish" >&2; exit 3
    fi
  fi
done
mkdir -p "$CACHE" "$STATE"
LOCK="$STATE/round.lock"   # taken so that no round starts mid-install
if ! mkdir "$LOCK" 2>/dev/null; then say "REFUSED — could not take $LOCK (stale or a round just started); inspect it" >&2; exit 3; fi
echo $$ > "$LOCK/pid"; echo "build_deps since $(date '+%F %T')" > "$LOCK/what"
trap 'rm -f "$LOCK/pid" "$LOCK/what" "$LOCK/work"; rmdir "$LOCK" 2>/dev/null' EXIT

URL="$(git -C "$SECUURA" config --get remote.origin.url)"; SSHCMD="$(git -C "$SECUURA" config --get core.sshCommand)"
case "$URL" in git@*|ssh://*|https://*) ;; *) say "HARNESS — Secuura origin is not a remote URL ($URL)" >&2; exit 5 ;; esac
if [ -n "${1:-}" ]; then COMMIT="$1"
else COMMIT="$(git -C "$SECUURA" ls-remote origin refs/heads/develop | awk '/refs\/heads\/develop$/{print $1}')"; fi
echo "$COMMIT" | grep -qE '^[0-9a-f]{40}$' || { say "could not resolve develop (got ${COMMIT:-nothing})" >&2; exit 5; }

if [ ! -d "$DEPS/.git" ]; then
  say "cloning $URL -> $DEPS"
  GIT_SSH_COMMAND="$SSHCMD" git clone --no-checkout "$URL" "$DEPS"; rc=$?
  [ "$rc" -eq 0 ] || { say "clone FAILED rc=$rc" >&2; exit 5; }
fi
git -C "$DEPS" remote set-url origin "$URL"
[ -n "$SSHCMD" ] && git -C "$DEPS" config core.sshCommand "$SSHCMD"
git -C "$DEPS" config gc.auto 0
if [ "$(git -C "$DEPS" cat-file -t "$COMMIT" 2>/dev/null)" != "commit" ]; then
  git -C "$DEPS" fetch origin "+refs/heads/develop:refs/remotes/origin/develop"; rc=$?
  [ "$rc" -eq 0 ] || { say "fetch FAILED rc=$rc" >&2; exit 5; }
fi
[ "$(git -C "$DEPS" cat-file -t "$COMMIT" 2>/dev/null)" = "commit" ] || { say "commit $COMMIT not in deps clone after fetch" >&2; exit 5; }
KEY="$(bash "$HERE/lock_key.sh" "$DEPS" "$COMMIT")" || exit 5
if [ -z "${BUILD_DEPS_FORCE:-}" ] && [ -f "$DEPS/LOCK_KEY" ] && [ "$(awk '{print $1}' "$DEPS/LOCK_KEY")" = "$KEY" ] && [ -d "$DEPS/$SUBDIR/node_modules" ]; then
  say "current: LOCK_KEY already built ($(cat "$DEPS/LOCK_KEY")); nothing to do"; exit 0
fi
rm -f "$DEPS/LOCK_KEY"
git -C "$DEPS" checkout -q --detach -f "$COMMIT" || { say "checkout FAILED" >&2; exit 5; }
say "deps at $COMMIT, lock key $KEY"

DIRS="$(find "$DEPS/$SUBDIR" -maxdepth 3 -name package-lock.json -not -path '*/node_modules/*' | sed 's#/package-lock.json$##' | LC_ALL=C sort)"
FAILS=0; N=0
while IFS= read -r d; do
  [ -z "$d" ] && continue
  N=$((N+1)); t0=$(date +%s)
  say "[$N] npm ci --ignore-scripts  ${d#"$DEPS/"}"
  npm --prefix "$d" ci --ignore-scripts --no-audit --no-fund --loglevel=error; rc=$?
  say "[$N] rc=$rc  ${d#"$DEPS/"}  ($(( $(date +%s) - t0 ))s)"
  if [ "$rc" -ne 0 ]; then
    # OPTIONAL dirs (no round ever uses them; the Secuura checkout has no node_modules there either) are logged, not fatal.
    # mobile/secuura-app: npm ci ERESOLVE (react-native-modal peer conflict in its own committed lock), 2026-11-03.
    case "${d#"$DEPS/"}" in
      Blockchain/Dev/mobile/secuura-app) say "[$N] WARNING optional dir failed rc=$rc (logged, not fatal)" ;;
      *) FAILS=$((FAILS+1)) ;;
    esac
  fi
done <<< "$DIRS"
if [ "$FAILS" -ne 0 ]; then say "FAILED — $FAILS of $N npm ci runs failed; LOCK_KEY NOT written" >&2; exit 1; fi
echo "$KEY $COMMIT" > "$DEPS/LOCK_KEY"
say "DONE — $N npm ci runs rc=0; LOCK_KEY: $(cat "$DEPS/LOCK_KEY")"
