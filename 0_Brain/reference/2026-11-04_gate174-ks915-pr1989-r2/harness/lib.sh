# Gate 173 harness library (adapted from gate 166 lib.sh + the PR suite's new_clone). Never prints a credential value.
W=/Volumes/DevMASTER/WEDNESDAY/0_Brain/reference/2026-11-04_gate174-ks915-pr1989-r2
R=$W/repo
SCR=$W/scratch
NM="/Volumes/DevMASTER/!CODING/Secuura/Blockchain/2_Project_Files/Blockchain/Dev/node_modules"
GPATH=/Users/kamilkreiser/.docker/bin:/opt/homebrew/bin:/usr/bin:/bin:/usr/sbin:/sbin
SCRIPT_SRC=${SCRIPT_SRC:-$R/Blockchain/Dev/scripts/restore-local-secrets.sh}
mkclone() {  # mkclone NAME [nodeps] -> echoes root; refuses to reuse a name (no deletes)
  local root="$SCR/$1" dev; dev="$root/Blockchain/Dev"
  [[ -e "$root" ]] && { echo "EXISTS:$root" >&2; return 1; }
  mkdir -p "$dev/scripts"; git -C "$root" init -q
  cp "$R/.gitignore" "$root/.gitignore"; cp "$R/Blockchain/Dev/.gitignore" "$dev/.gitignore"
  cp "$R/Blockchain/Dev/env.example" "$dev/env.example"; cp "$R/Blockchain/Dev/.env.local.example" "$dev/.env.local.example"
  cp "$R/Blockchain/Dev/scripts/bootstrap-env.sh" "$R/Blockchain/Dev/scripts/stack_env.sh" "$dev/scripts/"
  cp "$R/Blockchain/Dev/docker-compose.yml" "$dev/docker-compose.yml"; cp "$R/docker-compose.local.yml" "$root/docker-compose.local.yml"
  [[ "${2:-}" == nodeps ]] || ln -s "$NM" "$dev/node_modules"
  cp -p "$SCRIPT_SRC" "$dev/scripts/restore-local-secrets.sh"
  echo "$root"
}
RUNPATH=${RUNPATH:-$GPATH}
run() {  # run ROOT LOG [VAR=v ...] [-- args] -> echoes rc
  local root="$1" log="$2"; shift 2; local envs=() args=()
  while [[ $# -gt 0 ]]; do if [[ "$1" == "--" ]]; then shift; args=("$@"); break; fi; envs+=("$1"); shift; done
  ( cd "$root" && env -i HOME="$W/home" PATH="$RUNPATH" TMPDIR="${RUNTMP:-$W/tmp}" ${envs[@]+"${envs[@]}"} \
      bash "$root/Blockchain/Dev/scripts/restore-local-secrets.sh" ${args[@]+"${args[@]}"} ) >"$log" 2>&1
  echo $?
}
treesum() { ( cd "$1" && find . -path ./.git -prune -o -print | LC_ALL=C sort | while IFS= read -r f; do
      printf '%s %s ' "$f" "$(stat -f '%Lp' "$f")"; if [[ -f "$f" && ! -L "$f" ]]; then shasum -a 256 < "$f" | cut -c1-64; else echo x; fi
    done ) | shasum -a 256 | cut -c1-16; }
outsidesum() { { find "$W/home" -print; find "${RUNTMP:-$W/tmp}" -maxdepth 1 -print; } | LC_ALL=C sort | shasum -a 256 | cut -c1-16; }
sha()  { shasum -a 256 "$1" | cut -c1-64; }
mode() { stat -f '%Lp' "$1" 2>/dev/null; }
valof() { grep -E "^$2=" "$1" 2>/dev/null | head -n1 | cut -d= -f2-; }
