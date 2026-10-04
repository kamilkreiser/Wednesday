#!/bin/bash
# nas_push_arms.sh — red-proof arms for scheduler/nas_push.sh (Kam 2026-10-04: one-way NAS leg, card wed-nassync-rearm-shape-1004 => a).
# Every arm runs on scratch trees under /private/tmp; none touches DevMASTER content or the NAS.
set -u
HERE="$(cd -P "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
PUSH="$HERE/../../scheduler/nas_push.sh"
T="$(mktemp -d /private/tmp/naspush_arms.XXXXXX)"
export NASPUSH_LOG="$T/push.log"
PASS=0; FAIL=0
ok()  { echo "PASS  $1"; PASS=$((PASS+1)); }
bad() { echo "FAIL  $1"; FAIL=$((FAIL+1)); }
hash_tree() { (cd "$1" && find . -type f -print0 | sort -z | xargs -0 shasum -a 256 | shasum -a 256 | cut -c1-16); }

mk() { # fresh SRC + DST pair
  rm -rf "$T/src" "$T/dst"; mkdir -p "$T/src/a/node_modules" "$T/src/Datasec" "$T/dst"
  echo one > "$T/src/a/new.txt"; echo v2 > "$T/src/a/changed.txt"; echo nm > "$T/src/a/node_modules/x.js"; echo dz > "$T/src/Datasec/secret.txt"
  mkdir -p "$T/dst/a"; echo v1 > "$T/dst/a/changed.txt"; touch -t 202001010000 "$T/dst/a/changed.txt"; echo keep > "$T/dst/nas_only.txt"
  touch "$T/dst/.devnas-sync-state"
}
run() { NASPUSH_TEST_SRC="$T/src" NASPUSH_TEST_DST="$T/dst" bash "$PUSH" > "$T/out.txt" 2>&1; echo $?; }

# 1-6: the happy path, and everything it must NOT do
mk; B0="$(hash_tree "$T/src")"; rc="$(run)"
[ "$rc" = 0 ] && ok "1 happy path rc 0" || bad "1 happy path rc=$rc ($(tail -2 "$T/out.txt"))"
[ "$(cat "$T/dst/a/new.txt" 2>/dev/null)" = one ] && ok "2 new file copied to NAS" || bad "2 new file not copied"
[ "$(cat "$T/dst/nas_only.txt" 2>/dev/null)" = keep ] && ok "3 NAS-only file NOT deleted" || bad "3 NAS-only file gone"
[ "$(hash_tree "$T/src")" = "$B0" ] && ok "4 source tree byte-identical after the run" || bad "4 SOURCE CHANGED"
[ "$(cat "$T/dst/a/changed.txt")" = v2 ] && [ "$(cat "$T"/dst/_nas_push_overwritten/*/a/changed.txt 2>/dev/null)" = v1 ] && ok "5 overwritten NAS file kept in _nas_push_overwritten" || bad "5 overwrite not backed up"
[ ! -e "$T/dst/a/node_modules" ] && [ ! -e "$T/dst/Datasec" ] && ok "6 excludes hold (node_modules, Datasec not copied)" || bad "6 excluded paths copied"

# 7: refuses without the NAS marker (an empty mount point / wrong volume)
mk; rm -f "$T/dst/.devnas-sync-state"; rc="$(run)"
[ "$rc" = 2 ] && [ ! -e "$T/dst/a/new.txt" ] && ok "7 no marker -> refused rc 2, nothing copied" || bad "7 marker refusal rc=$rc"

# 8: refuses dst inside src
mk; mkdir -p "$T/src/inner"; touch "$T/src/inner/.devnas-sync-state"
rc="$(NASPUSH_TEST_SRC="$T/src" NASPUSH_TEST_DST="$T/src/inner" bash "$PUSH" > "$T/out.txt" 2>&1; echo $?)"
[ "$rc" = 2 ] && ok "8 dst inside src -> refused rc 2" || bad "8 nesting refusal rc=$rc"

# 9: refuses test paths outside /private/tmp (real paths can never be smuggled through test mode)
rc="$(NASPUSH_TEST_SRC=/Volumes/DevMASTER/WEDNESDAY NASPUSH_TEST_DST="$T/dst" bash "$PUSH" > "$T/out.txt" 2>&1; echo $?)"
[ "$rc" = 2 ] && ok "9 test path outside /private/tmp -> refused rc 2" || bad "9 test-path refusal rc=$rc"

# 10: the hold file refuses rc 3 (planted in a COPY of the scheduler dir, never the real one)
mkdir -p "$T/sched"; cp "$PUSH" "$T/sched/nas_push.sh"; touch "$T/sched/NASPUSH_HOLD_wednesday"; mk
rc="$(NASPUSH_TEST_SRC="$T/src" NASPUSH_TEST_DST="$T/dst" bash "$T/sched/nas_push.sh" > "$T/out.txt" 2>&1; echo $?)"
[ "$rc" = 3 ] && [ ! -e "$T/dst/a/new.txt" ] && ok "10 hold file -> refused rc 3, nothing copied" || bad "10 hold refusal rc=$rc"

# 11: the run-time cap kills a run (a 30 MB file throttled to 100 KB/s, cap 5 s)
mk; dd if=/dev/zero of="$T/src/big.bin" bs=1m count=30 2>"$T/dd.err"
cp "$PUSH" "$T/sched/nas_push_slow.sh"; rm -f "$T/sched/NASPUSH_HOLD_wednesday"
sed -i '' 's/^ARGS=( -rlt /ARGS=( --bwlimit=100 -rlt /' "$T/sched/nas_push_slow.sh"
rc="$(NASPUSH_MAX_SECONDS=5 NASPUSH_TEST_SRC="$T/src" NASPUSH_TEST_DST="$T/dst" bash "$T/sched/nas_push_slow.sh" > "$T/out.txt" 2>&1; echo $?)"
[ "$rc" = 4 ] && ok "11 run-time cap -> killed rc 4" || bad "11 cap rc=$rc"
[ ! -e "$T/dst/big.bin" ] || [ "$(stat -f %z "$T/dst/big.bin")" = "$(stat -f %z "$T/src/big.bin")" ] && ok "12 killed run left no half file" || bad "12 half file left"

# 13: the forbidden-flag guard fires (a --delete smuggled into ARGS must refuse)
cp "$PUSH" "$T/sched/nas_push_del.sh"; sed -i '' 's/^ARGS=( -rlt /ARGS=( --delete -rlt /' "$T/sched/nas_push_del.sh"; mk
rc="$(NASPUSH_TEST_SRC="$T/src" NASPUSH_TEST_DST="$T/dst" bash "$T/sched/nas_push_del.sh" > "$T/out.txt" 2>&1; echo $?)"
[ "$rc" = 2 ] && [ -e "$T/dst/nas_only.txt" ] && ok "13 --delete smuggled in -> refused rc 2, NAS-only file kept" || bad "13 forbidden-flag guard rc=$rc"

echo "nas_push_arms: $PASS PASS, $FAIL FAIL (scratch $T)"
[ "$FAIL" -eq 0 ]
