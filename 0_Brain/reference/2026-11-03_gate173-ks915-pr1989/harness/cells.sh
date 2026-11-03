# Generic cell runner (sourced after lib.sh). Needs $TAG, $L, $GB (golden blank-admin .env), $GL (golden .env.local), $M.
consumers_full() {  # CLONE -> dotenv(dev .env)/bash/compose dev entry/compose root entry, labels only; reads the files AS THEY ARE NOW
  local c="$1" d="$1/Blockchain/Dev" a b x y; shift
  a=$(node "$W/harness/classify.js" dotenv "$NM" "$M" "$d/.env")
  b=$(cd "$W/tmp" && env -i PATH=/usr/bin:/bin "$@" bash -c 'set -a; . "$1" >/dev/null 2>&1; printf "%s\0" "${DATABASE_URL-}" "${NODE_ENV-}" "${PGHOST-}" "${PGHOSTADDR-}" "${PGSERVICE-}" "${POSTGRES_HOST-}"' _ "$d/.env" 2>/dev/null | node "$W/harness/classify.js" bashvals "$NM" "$M")
  x=$(cd "$d" && env -i PATH="$GPATH" HOME="$W/home" "$@" docker compose config --format json 2>/dev/null | node "$W/harness/classify.js" compose "$NM" "$M")
  y=$(cd "$c" && env -i PATH="$GPATH" HOME="$W/home" "$@" docker compose -f docker-compose.local.yml config --format json 2>/dev/null | node "$W/harness/classify.js" compose "$NM" "$M")
  echo "AFTER: dotenv[$a] bash[$b] dev[$x] root[$y]"
}
# gcell ID DEV_BODY ROOT_BODY LOCAL_BODY [VAR=v ...] [-- args]
gcell() {
  local id="$1" body="$2" rbody="$3" lbody="$4"; shift 4
  local c e t0 t1 rc o0 o1 envs=() args=() a0
  while [[ $# -gt 0 ]]; do if [[ "$1" == "--" ]]; then shift; args=("$@"); break; fi; envs+=("$1"); shift; done
  c="$(mkclone ${TAG}-$id ${NODEPS:-})" || return; e="$c/Blockchain/Dev/.env"
  { cat "$GB"; printf '%s' "$body"; } > "$e"; chmod 644 "$e"
  { cat "$GL"; printf '%s' "$lbody"; } > "$c/Blockchain/Dev/.env.local"; chmod 644 "$c/Blockchain/Dev/.env.local"
  [[ -n "$rbody" ]] && printf '%s' "$rbody" > "$c/.env"
  [[ -n "${PREP:-}" ]] && eval "$PREP"
  cp "$e" "$L/$id.pre.env.bin"; a0=$(valof "$e" ADMIN_USER_PASSWORD | shasum -a 256 | cut -c1-12)
  t0=$(treesum "$c"); o0=$(outsidesum)
  if [[ -n "${TIMEOUT:-}" ]]; then
    ( cd "$c" && exec perl -e 'alarm shift; exec @ARGV' "$TIMEOUT" env -i HOME="$W/home" PATH="$RUNPATH" TMPDIR="${RUNTMP:-$W/tmp}" ${envs[@]+"${envs[@]}"} bash "$c/Blockchain/Dev/scripts/restore-local-secrets.sh" ${args[@]+"${args[@]}"} ) >"$L/$id.log" 2>&1; rc=$?
  else
    rc=$(RUNPATH="$RUNPATH" run "$c" "$L/$id.log" ${envs[@]+"${envs[@]}"} -- ${args[@]+"${args[@]}"})
  fi
  t1=$(treesum "$c"); o1=$(outsidesum)
  printf '%-5s rc=%-3s tree_same=%s outside_same=%s admin_changed=%s admin_now_set=%s mode=%s tmpcopies=%s marker_in_log=%s | %s | args=%s | dev=%q root=%q local=%q\n' "$id" "$rc" \
    "$([[ $t0 == $t1 ]] && echo y || echo N)" "$([[ $o0 == $o1 ]] && echo y || echo N)" \
    "$([[ $a0 == $(valof "$e" ADMIN_USER_PASSWORD | shasum -a 256 | cut -c1-12) ]] && echo n || echo Y)" \
    "$([[ -n "$(valof "$e" ADMIN_USER_PASSWORD)" ]] && echo y || echo n)" "$(mode "$e")" \
    "$(ls -a "$c/Blockchain/Dev" | grep -c '^\.env-ks915')" "$(grep -c "$M" "$L/$id.log")" "${envs[*]-}" "${args[*]-}" "$body" "$rbody" "$lbody"
  printf '      why: %s\n' "$(grep -oE 'refused[^.]*|cannot check safely: [^.]*|after the write[^.]*|docker compose config shows[^.]*|docker compose config gave[^.]*' "$L/$id.log" | head -1 | cut -c1-170)"
  [[ -z "${NOCONS:-}" ]] && printf '      %s\n' "$(consumers_full "$c" ${envs[@]+"${envs[@]}"})"
  LASTCLONE="$c"
}
