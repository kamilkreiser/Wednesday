#!/bin/bash
# safe_pull_arms.sh — red/green arms for tools/safe_pull.sh, run against a SCRATCH origin + clones
# (never the real repo). Usage: safe_pull_arms.sh <scratch-dir>
set -u
SP="$(cd "$(dirname "$0")/.." && pwd)/tools/safe_pull.sh"
X="${1:?usage: safe_pull_arms.sh <scratch-dir>}"; rm -rf "$X/sp_arms"; mkdir -p "$X/sp_arms"; cd "$X/sp_arms" || exit 2
D=0_Brain/dashboard/data; PASS=0; FAIL=0
ok()  { echo "PASS  $1"; PASS=$((PASS+1)); }
bad() { echo "FAIL  $1"; FAIL=$((FAIL+1)); }
q() { git -C "$1" -c user.email=a@b -c user.name=arms "${@:2}" >/dev/null 2>&1; }
fresh() {  # $1 name → origin.git + $1 (ours) + $1_up (upstream writer)
  rm -rf "$1" "$1_up" "$1.git"; git init -q --bare "$1.git"
  git clone -q "$1.git" "$1_up" 2>/dev/null; mkdir -p "$1_up/$D" "$1_up/notes"
  echo '[{"id":"c1"}]' > "$1_up/$D/decisions.json"; echo '{"a":1}' > "$1_up/$D/views.json"
  echo '{"n":1}' > "$1_up/$D/news.json"; echo base > "$1_up/notes/n.md"
  q "$1_up" add -A; q "$1_up" commit -m base; q "$1_up" push -q origin HEAD:main
  git clone -q -b main "$1.git" "$1" 2>/dev/null; git -C "$1" config user.email a@b; git -C "$1" config user.name arms
  mkdir -p "$1/2_Project_Files/fleet/state"; echo "2_Project_Files/fleet/state/" > "$1/.git/info/exclude"
}
up() { (cd "$1_up" && q . pull -q origin main && eval "$2" && q . add -A && q . commit -m up && q . push -q origin HEAD:main); }
run() { WED_REPO="$PWD/$1" bash "$SP" ${2:-} >"$1.out" 2>&1; echo $?; }

# A1 dirty outside data -> rc 2, untouched
fresh a1; echo x >> a1/notes/n.md; rc=$(run a1); [ "$rc" = 2 ] && git -C a1 diff --quiet HEAD -- $D && ok "A1 dirty note refused rc 2" || bad "A1 rc=$rc"
# A2 pre-staged file outside data -> rc 2
fresh a2; echo y >> a2/notes/n.md; git -C a2 add notes/n.md; rc=$(run a2); [ "$rc" = 2 ] && ok "A2 pre-staged outside refused" || bad "A2 rc=$rc"
# A3 dry-run touches nothing
fresh a3; echo '{"n":9}' > a3/$D/news.json; rc=$(run a3 --dry-run); [ "$rc" = 0 ] && grep -q 9 a3/$D/news.json && [ -z "$(git -C a3 log --oneline origin/main..HEAD)" ] && ok "A3 dry-run rc 0, nothing touched" || bad "A3 rc=$rc"
# A4 generated feed dirty, upstream moved elsewhere -> pulled, feed restored, copy kept
fresh a4; up a4 'echo up >> notes/n.md'; echo '{"n":42}' > a4/$D/news.json
rc=$(run a4); [ "$rc" = 0 ] && grep -q 42 a4/$D/news.json && grep -q up a4/notes/n.md && ls a4/2_Project_Files/fleet/state/safe_pull/*/$D/news.json >/dev/null 2>&1 \
  && ok "A4 feed restored after pull, copy kept" || { bad "A4 rc=$rc"; cat a4.out; }
# A5 state list conflict -> unioned, both cards present, rebase finished
fresh a5; up a5 "echo '[{\"id\":\"c1\"},{\"id\":\"up2\"}]' > $D/decisions.json"; echo '[{"id":"c1"},{"id":"mine3"}]' > a5/$D/decisions.json
rc=$(run a5); [ "$rc" = 0 ] && grep -q up2 a5/$D/decisions.json && grep -q mine3 a5/$D/decisions.json && [ ! -d a5/.git/rebase-merge ] \
  && [ "$(python3 -c "import json;print(len(json.load(open('a5/$D/decisions.json'))))")" = 3 ] && ok "A5 decisions.json unioned 3 cards" || { bad "A5 rc=$rc"; cat a5.out; }
# A6 state NON-list conflict -> rc 3, rebase aborted, our commit kept, feed restored
fresh a6; up a6 "echo '{\"a\":2}' > $D/views.json"; echo '{"a":3}' > a6/$D/views.json; echo '{"n":7}' > a6/$D/news.json
rc=$(run a6); [ "$rc" = 3 ] && [ ! -d a6/.git/rebase-merge ] && grep -q '"a":3' a6/$D/views.json && grep -q 7 a6/$D/news.json \
  && ok "A6 non-list conflict refused rc 3, tree restored" || { bad "A6 rc=$rc"; cat a6.out; }
# A7 conflict outside data (a committed note) -> rc 3, aborted
fresh a7; up a7 'echo theirs > notes/n.md'; echo mine > a7/notes/n.md; q a7 commit -am mine
rc=$(run a7); [ "$rc" = 3 ] && [ ! -d a7/.git/rebase-merge ] && grep -q mine a7/notes/n.md && ok "A7 outside conflict refused rc 3" || { bad "A7 rc=$rc"; cat a7.out; }
# A8 the script never uses --autostash and never drops a stash (source read)
! grep -nE -- '--autostash[^-]|stash (drop|pop|clear)' "$SP" | grep -v '^[0-9]*:#' | grep -q . && ok "A8 no autostash/drop in source" || bad "A8"
echo "== $PASS pass, $FAIL fail"; [ "$FAIL" = 0 ]
