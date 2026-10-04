# guards_gate55.sh — SOURCED (never run) by c2_regen_gate55.sh and c3_cells_gate55.sh. bash 3.2 / zsh safe.
# The two guards every writing subcommand passes BEFORE it writes anything:
#   guard_ws <ws> <base|head>  WS must be a directory OUTSIDE the forbidden root (/Volumes/DevMASTER/!CODING/: the shared checkout and every
#                              builder worktree live there), the REPO ROOT of a checkout with Blockchain/Dev/services/transfer, CLEAN
#                              (`git status --porcelain` empty), and its HEAD^{tree} must equal the side's tree (kit base_tree / kit
#                              expected_tree). Tree identity, not commit identity: a by-SHA worktree in the tester's clone passes, and so
#                              does the drafter's scratch export whose commits differ but whose trees were proven equal.
#   guard_out <dir>            lib_gate55.guard_out: the LEXICAL path is tested first, then the realpath of its nearest existing ancestor,
#                              and only then is the directory created (gate54a's first guard created Secuura/x before refusing it).
# Sets WSR, TRANSFER, DEV, OUTR. G55_FORBIDDEN_ROOT / G55_REPORTS_ROOT are CONTROLS-ONLY (the launcher refuses a launch with any G55_* set).
GS="${GS:?GS unset}"
KJ() { python3 -c 'import json,sys; v=json.load(open(sys.argv[1]))[sys.argv[2]]; print(v if isinstance(v,str) else json.dumps(v))' "$GS/kit.json" "$1"; }
KB() { python3 -c 'import json,sys; print(json.load(open(sys.argv[1]))[sys.argv[2]][sys.argv[3]])' "$GS/kit.json" "$1" "$2"; }
FORBID="${G55_FORBIDDEN_ROOT:-$(KJ forbidden_root)}"
sha() { shasum -a 256 "$1" | awk '{print $1}'; }
guard_ws() {
  _ws="$1"; _side="$2"
  case "$_side" in base) _want="$(KJ base_tree)";; head) _want="$(KJ expected_tree)";; *) echo "REFUSING: side '$_side' is not base|head"; exit 2;; esac
  [ -d "$_ws" ] || { echo "REFUSING: WS $_ws is not a directory"; exit 2; }
  _l="$(python3 -c 'import os,sys; print(os.path.abspath(sys.argv[1]))' "$_ws")"; _r="$(/bin/realpath "$_ws")"
  case "$_l/" in "$FORBID"*) echo "REFUSING: WS $_l is inside $FORBID — the shared checkout and the builder's worktrees are READ ONLY; use a worktree in YOUR scratch clone (nothing written)"; exit 2;; esac
  case "$_r/" in "$FORBID"*) echo "REFUSING: WS $_l resolves to $_r inside $FORBID (nothing written)"; exit 2;; esac
  [ -d "$_r/Blockchain/Dev/services/transfer" ] || { echo "REFUSING: $_r has no Blockchain/Dev/services/transfer (WS is the REPO ROOT of your worktree)"; exit 2; }
  _t="$(git -C "$_r" rev-parse 'HEAD^{tree}' 2> /dev/null)"
  [ "$_t" = "$_want" ] || { echo "REFUSING: WS HEAD^{tree} is '$_t'; the $_side side needs tree $_want (kit)"; exit 2; }
  _d="$(git -C "$_r" status --porcelain 2> /dev/null | wc -l | tr -d ' ')"
  [ "$_d" = 0 ] || { echo "REFUSING: WS $_r has $_d dirty path(s) before this step (a stale plant?) — name them, restore by blob, re-run"; exit 2; }
  WSR="$_r"; DEV="$_r/Blockchain/Dev"; TRANSFER="$_r/$(KJ transfer_dir)"
  echo "  WS $WSR | HEAD $(git -C "$WSR" rev-parse HEAD) | tree $_t == kit $_side tree | clean"
}
guard_out() {
  OUTR="$(python3 -c 'import sys; sys.path.insert(0, sys.argv[1]); from lib_gate55 import guard_out; print(guard_out(sys.argv[2]))' "$GS" "$1")"; _rc=$?
  [ "$_rc" = 0 ] || { echo "$OUTR"; exit 2; }
}
clean_or_fail() {  # clean_or_fail <tag>: git status --porcelain into OUT, 0 lines wanted
  git -C "$WSR" status --porcelain > "$OUTR/$1.status.out" 2> "$OUTR/$1.status.err"; _rc=$?
  _n="$(wc -l < "$OUTR/$1.status.out" | tr -d ' ')"
  echo "  worktree status after $1: rc $_rc, $_n dirty path(s) (want 0)"
  [ "$_rc" = 0 ] && [ "$_n" = 0 ]
}
put_blob() {  # put_blob <blob-id> <ws-relative path>: write a blob's bytes into the WS working file (read-only cat-file; the WS is yours)
  git -C "$WSR" cat-file blob "$1" > "$WSR/$2" 2> "$OUTR/put_blob.err"
}
quarantine() {  # quarantine <ws-relative path> <tag>: MOVE into OUT/quarantine (never rm)
  mkdir -p "$OUTR/quarantine" && mv "$WSR/$1" "$OUTR/quarantine/$2.$(date -u +%H%M%S).$(basename "$1")" && echo "  quarantined $1 -> $OUTR/quarantine/"
}
