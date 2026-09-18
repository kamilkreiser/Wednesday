#!/bin/bash
set -u
S=/private/tmp/claude-501/-Volumes-KK-T9-External-HDD-TUESDAY/aca1c960-d0ad-4d64-83b7-9ad23a56ae72/scratchpad/fh
case "$S" in /private/tmp/claude-501/*/scratchpad/*) ;; *) echo REFUSED; exit 9;; esac
mkdir -p "$S"
if [ ! -d "$S/origin.git" ]; then
  git init -q --bare -b main "$S/origin.git"
  git clone -q "$S/origin.git" "$S/seed" 2>/dev/null
  git -C "$S/seed" -c user.email=t@t -c user.name=t commit -q --allow-empty -m init
  git -C "$S/seed" push -q origin main
  for b in a b c d e f g h; do git -C "$S/seed" push -q origin main:refs/heads/br-$b; done
  git clone -q "$S/origin.git" "$S/work"; git clone -q "$S/origin.git" "$S/pusher"
fi
W="$S/work"
old_pull(){ git -C "$W" pull --rebase -q; }
new_sync(){ git -C "$W" fetch -q --no-write-fetch-head origin main && git -C "$W" rebase -q --autostash origin/main; }
new_retry(){ { git -C "$W" fetch -q --no-write-fetch-head origin main || { sleep 1; git -C "$W" fetch -q --no-write-fetch-head origin main; }; } && git -C "$W" rebase -q --autostash origin/main; }
old_vs_fetch_ctl(){ git -C "$W" pull --rebase -q; }
plain_fetch(){ git -C "$W" fetch -q origin; }
pusher(){ git -C "$S/pusher" -c user.email=p@p -c user.name=p commit -q --allow-empty -m p && git -C "$S/pusher" push -q origin main || git -C "$S/pusher" pull -q --rebase; }
run(){ # $1 label, $2 fg fn, rest = bg fns
  local label=$1 fg=$2; shift 2; local pids=""
  for b in "$@"; do ( end=$((SECONDS+30)); while [ $SECONDS -lt $end ]; do $b >/dev/null 2>&1; done ) & pids="$pids $!"; done
  local fail=0 race=0 other=""
  for i in $(seq 1 120); do out=$($fg 2>&1); rc=$?; if [ $rc -ne 0 ]; then fail=$((fail+1)); case "$out" in *"multiple branches"*) race=$((race+1));; *) other="$out";; esac; fi; done
  kill $pids 2>/dev/null; wait $pids 2>/dev/null
  echo "$label: syncs=120 failed=$fail multiple-branches=$race${other:+ last-other=[$(printf '%s' "$other"|head -1)]}"
}
run "ARM-3    retry fg vs retry bg + pusher" new_retry new_retry pusher
run "ARM-CTL  old pull fg vs plain fetch bg + pusher" old_vs_fetch_ctl plain_fetch pusher
echo "work HEAD==origin/main after: $( [ "$(git -C "$W" rev-parse HEAD)" = "$(git -C "$W" rev-parse origin/main)" ] && echo yes || echo no)"
