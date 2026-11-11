#!/bin/bash
# dedupe_admin_react.sh — ONE React for frontend/admin vitest runs (Spark o136, 2026-11-11). Idempotent, no cd, bash 3.2.
# WHY: the harness-supplied vitest config for frontend/admin (spark/tiers/vitest_configs/frontend-admin.config.mjs) runs the WORKSPACE
# ROOT's vitest + jsdom + testing-library + react-dom, but the page's react and its libs (lucide-react, radix) resolve react from
# frontend/admin/node_modules: two copies, so a hook throws "Cannot read properties of null (reading 'useState'/'useContext')".
# Node resolves by REALPATH, so only a filesystem fix covers CJS libs the bundler never sees. This replaces the deps store's
# frontend/admin/node_modules/{react,react-dom,scheduler} (same versions required) by symlinks to the root's copies. It touches
# ONLY the Wednesday-owned deps store (spark/cache/deps, gitignored); never a repo checkout. The originals are MOVED, not deleted,
# to $DEPS/_orig_admin_react/. build_deps.sh calls this before it writes LOCK_KEY (npm ci recreates the dirs).
set -uo pipefail
HERE="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
DEPS="${SPARK_DEPS:-$HERE/cache/deps}"
D="$DEPS/Blockchain/Dev"
[ -d "$D/frontend/admin/node_modules" ] && [ -d "$D/node_modules" ] || { echo "dedupe_admin_react: no admin or root node_modules in $DEPS (nothing to do)"; exit 0; }
mkdir -p "$DEPS/_orig_admin_react"
for p in react react-dom scheduler; do
  a="$D/frontend/admin/node_modules/$p"; r="$D/node_modules/$p"
  [ -d "$r" ] || { echo "dedupe_admin_react: root has no $p — HARNESS" >&2; exit 5; }
  if [ -L "$a" ]; then echo "dedupe_admin_react: $p already a symlink -> $(readlink "$a")"; continue; fi
  va="$(sed -n 's/.*"version": "\(.*\)".*/\1/p' "$a/package.json" | head -1)"; vr="$(sed -n 's/.*"version": "\(.*\)".*/\1/p' "$r/package.json" | head -1)"
  if [ "$va" != "$vr" ]; then echo "dedupe_admin_react: $p admin $va != root $vr — NOT linked (versions must match)" >&2; exit 5; fi
  mv "$a" "$DEPS/_orig_admin_react/$p" && ln -s "$r" "$a" && echo "dedupe_admin_react: $p $va -> root copy (original kept in _orig_admin_react)"
done
