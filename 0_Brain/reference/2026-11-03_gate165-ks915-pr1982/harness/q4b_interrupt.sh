#!/bin/bash
# Q4b: is the full-copy temp file (.env.ks915.XXXXXX) left behind on interruption, and is it gitignored?
# Q2b: hostile xtrace on a FRESH clone (bootstrap generates values in a child bash).
set -uo pipefail
source /Volumes/DevMASTER/WEDNESDAY/0_Brain/reference/2026-11-03_gate165-ks915-pr1982/harness/lib.sh
TAG=${1:-q4b}
L=$W/runs/$TAG; mkdir -p "$L"
SHIM=$W/harness/shim; mkdir -p "$SHIM"
cat > "$SHIM/awk" <<'EOS'
#!/bin/bash
# slow awk only for the script's set_key (identified by RLS_KEY in its environment)
if [[ -n "${RLS_KEY:-}" && -n "${GATE165_SLOW:-}" ]]; then sleep 4; fi
exec /usr/bin/awk "$@"
EOS
chmod +x "$SHIM/awk"

for sig in TERM HUP KILL; do
  c="$(mkclone ${TAG}-$sig)" || continue; d="$c/Blockchain/Dev"
  # complete .env with a blank admin so set_key runs once
  ( cd "$c" && env -i HOME="$W/home" PATH="$GPATH" TMPDIR="$W/tmp" bash "$d/scripts/restore-local-secrets.sh" ) > "$L/$sig.prep.log" 2>&1
  /usr/bin/awk 'index($0,"ADMIN_USER_PASSWORD=")==1{print "ADMIN_USER_PASSWORD="; next}{print}' "$d/.env" > "$d/.env.new" && mv "$d/.env.new" "$d/.env"
  ( cd "$c" && exec env -i HOME="$W/home" PATH="$SHIM:$GPATH" TMPDIR="$W/tmp" GATE165_SLOW=1 bash "$d/scripts/restore-local-secrets.sh" ) > "$L/$sig.log" 2>&1 &
  bg=$!
  n=0; while [[ $n -lt 100 ]] && ! ls "$d"/.env.ks915.* >/dev/null 2>&1; do sleep 0.1; n=$((n+1)); done
  seen=$(ls "$d"/.env.ks915.* 2>/dev/null | wc -l | tr -d ' ')
  kill -"$sig" "$bg" 2>/dev/null; wait "$bg" 2>/dev/null; rc=$?
  sleep 5   # let the orphaned slow awk finish writing
  left=$(ls "$d"/.env.ks915.* 2>/dev/null | head -1)
  if [[ -n "$left" ]]; then
    rel="Blockchain/Dev/$(basename "$left")"
    ign=$(git -C "$c" check-ignore -q "$rel" && echo ignored || echo NOT-ignored)
    st=$(git -C "$c" status --porcelain -uall | grep -c 'ks915')
    sz=$(wc -c < "$left" | tr -d ' '); md=$(mode "$left")
    pgsame=$([[ "$(valof "$left" POSTGRES_PASSWORD | shasum)" == "$(valof "$d/.env" POSTGRES_PASSWORD | shasum)" ]] && echo y || echo n)
    echo "SIG$sig: temp_seen=$seen rc=$rc LEFT_BEHIND=y mode=$md bytes=$sz holds_same_POSTGRES_PASSWORD_as_.env=$pgsame git=$ign 'git status' lists it=$st"
  else
    echo "SIG$sig: temp_seen=$seen rc=$rc LEFT_BEHIND=n"
  fi
done

echo
echo "== hostile xtrace on a FRESH clone (bootstrap-env.sh generates in a child bash) =="
for mode_ in bash-x SHELLOPTS BASH_ENV; do
  c="$(mkclone ${TAG}-x-$mode_)" || continue; d="$c/Blockchain/Dev"
  printf 'set -x\n' > "$L/bashenv.sh"
  case $mode_ in
    bash-x)    ( cd "$c" && env -i HOME="$W/home" PATH="$GPATH" TMPDIR="$W/tmp" bash -x "$d/scripts/restore-local-secrets.sh" ) > "$L/x-$mode_.log" 2>&1 ;;
    SHELLOPTS) ( cd "$c" && env -i HOME="$W/home" PATH="$GPATH" TMPDIR="$W/tmp" SHELLOPTS=xtrace bash "$d/scripts/restore-local-secrets.sh" ) > "$L/x-$mode_.log" 2>&1 ;;
    BASH_ENV)  ( cd "$c" && env -i HOME="$W/home" PATH="$GPATH" TMPDIR="$W/tmp" BASH_ENV="$L/bashenv.sh" bash "$d/scripts/restore-local-secrets.sh" ) > "$L/x-$mode_.log" 2>&1 ;;
  esac
  rc=$?
  adm=0; other=0
  v="$(valof "$d/.env" ADMIN_USER_PASSWORD)"; [[ -n "$v" ]] && grep -qF -- "$v" "$L/x-$mode_.log" && adm=1
  for k in POSTGRES_PASSWORD REDIS_PASSWORD PII_ENCRYPTION_KEY PII_LOOKUP_HMAC_KEY GATEWAY_VOUCH_SECRET DEMO_SERVICE_KEY; do
    v="$(valof "$d/.env" "$k")"; [[ -n "$v" ]] && grep -qF -- "$v" "$L/x-$mode_.log" && other=$((other+1))
  done
  echo "$mode_: rc=$rc ADMIN_USER_PASSWORD_in_output=$adm bootstrap_keys_in_output=$other/6 xtrace_lines=$(grep -c '^+' "$L/x-$mode_.log")"
done
