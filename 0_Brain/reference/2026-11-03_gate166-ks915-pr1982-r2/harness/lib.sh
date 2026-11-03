# Gate 165 harness library. Never prints a credential value.
W=/Volumes/DevMASTER/WEDNESDAY/0_Brain/reference/2026-11-03_gate166-ks915-pr1982-r2
R=$W/repo
SCR=$W/scratch
GPATH=/opt/homebrew/bin:/usr/bin:/bin:/usr/sbin:/sbin
SCRIPT_SRC=${SCRIPT_SRC:-$R/Blockchain/Dev/scripts/restore-local-secrets.sh}

mkclone() {  # mkclone NAME -> echoes root; refuses to reuse a name (no deletes)
  local root="$SCR/$1" dev
  dev="$root/Blockchain/Dev"
  [[ -e "$root" ]] && { echo "EXISTS:$root" >&2; return 1; }
  mkdir -p "$dev/scripts"
  git -C "$root" init -q
  cp "$R/.gitignore" "$root/.gitignore"
  cp "$R/Blockchain/Dev/.gitignore" "$dev/.gitignore"
  cp "$R/Blockchain/Dev/env.example" "$R/Blockchain/Dev/.env.example" "$R/Blockchain/Dev/.env.local.example" "$dev/"
  cp "$R/Blockchain/Dev/scripts/bootstrap-env.sh" "$R/Blockchain/Dev/scripts/stack_env.sh" "$dev/scripts/"
  cp -p "$SCRIPT_SRC" "$dev/scripts/restore-local-secrets.sh"
  echo "$root"
}

run() {  # run ROOT LOG [VAR=v ...] [-- args] -> echoes rc
  local root="$1" log="$2"; shift 2
  local envs=() args=()
  while [[ $# -gt 0 ]]; do
    if [[ "$1" == "--" ]]; then shift; args=("$@"); break; fi
    envs+=("$1"); shift
  done
  ( cd "$root" && env -i HOME="$W/home" PATH="$GPATH" TMPDIR="$W/tmp" ${envs[@]+"${envs[@]}"} \
      bash "$root/Blockchain/Dev/scripts/restore-local-secrets.sh" ${args[@]+"${args[@]}"} ) >"$log" 2>&1
  echo $?
}

# Hash of every path under ROOT (excluding .git), with mode and content.
treesum() {
  ( cd "$1" && find . -path ./.git -prune -o -print | LC_ALL=C sort | while IFS= read -r f; do
      printf '%s %s ' "$f" "$(stat -f '%Lp' "$f")"
      if [[ -f "$f" ]]; then shasum -a 256 < "$f" | cut -c1-64; else echo dir; fi
    done ) | shasum -a 256 | cut -c1-16
}
outsidesum() { find "$W/home" "$W/tmp" -print | LC_ALL=C sort | shasum -a 256 | cut -c1-16; }

sha()  { shasum -a 256 "$1" | cut -c1-64; }
mode() { stat -f '%Lp' "$1"; }
# valof FILE KEY stays inside the process; callers compare or hash, never print
valof() { grep -E "^$2=" "$1" 2>/dev/null | head -n1 | cut -d= -f2-; }
hashof() { printf '%s' "$(valof "$1" "$2")" | shasum -a 256 | cut -c1-12; }
