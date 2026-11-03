#!/bin/bash
# Q5: the PR's own suite at head, red-first without the script, and mutants on the refusal predicates.
set -uo pipefail
W=/Volumes/DevMASTER/WEDNESDAY/0_Brain/reference/2026-11-03_gate166-ks915-pr1982-r2
R=$W/repo
MUT=$W/mut; mkdir -p "$MUT"
L=$W/runs/q5; mkdir -p "$L"
ORIG=$R/Blockchain/Dev/scripts/restore-local-secrets.sh
echo "script sha256 at head: $(shasum -a 256 "$ORIG" | cut -c1-12)"

mktree() {  # mktree NAME -> minimal tree the suite needs; script left out (caller adds)
  local t="$MUT/$1"; [[ -e "$t" ]] && { echo "EXISTS $t" >&2; return 1; }
  mkdir -p "$t/Blockchain/Dev/scripts/__tests__" "$t/Blockchain/Dev/services/auth/src/repositories"
  cp "$R/.gitignore" "$t/"
  cp "$R/Blockchain/Dev/env.example" "$R/Blockchain/Dev/.env.local.example" "$R/Blockchain/Dev/docker-compose.yml" "$t/Blockchain/Dev/"
  cp "$R/Blockchain/Dev/services/auth/src/repositories/userRepo.ts" "$t/Blockchain/Dev/services/auth/src/repositories/"
  cp "$R/Blockchain/Dev/scripts/bootstrap-env.sh" "$R/Blockchain/Dev/scripts/stack_env.sh" "$t/Blockchain/Dev/scripts/"
  cp "$R/Blockchain/Dev/scripts/__tests__/restore_local_secrets.test.sh" "$t/Blockchain/Dev/scripts/__tests__/"
  echo "$t"
}
suite() {  # suite TREE LOG -> "rc pass fail fatal"
  local t="$1" log="$2" rc
  ( cd "$W/tmp" && env -i HOME="$W/home" PATH=/opt/homebrew/bin:/usr/bin:/bin:/usr/sbin:/sbin TMPDIR="$W/tmp" \
      bash "$t/Blockchain/Dev/scripts/__tests__/restore_local_secrets.test.sh" ) > "$log" 2>&1; rc=$?
  echo "rc=$rc ok=$(grep -c '^ok ' "$log") FAIL=$(grep -c '^FAIL ' "$log") FATAL=$(grep -c FATAL "$log")"
}

echo "== suite at PR head, in the clone =="
( cd "$W/tmp" && env -i HOME="$W/home" PATH=/opt/homebrew/bin:/usr/bin:/bin:/usr/sbin:/sbin TMPDIR="$W/tmp" \
    bash "$R/Blockchain/Dev/scripts/__tests__/restore_local_secrets.test.sh" ) > "$L/head.log" 2>&1
echo "head: rc=$? ok=$(grep -c '^ok ' "$L/head.log") FAIL=$(grep -c '^FAIL ' "$L/head.log") $(tail -1 "$L/head.log")"

echo "== red-first: same suite, script absent =="
t=$(mktree redfirst) && echo "redfirst: $(suite "$t" "$L/redfirst.log")"

# mutants: NAME|perl substitution applied to the script
MUTANTS=(
  'mA_contains_localhost|s/""\|localhost\|127\.0\.0\.1\|::1\|postgres\|\/\*\)/""|localhost|*localhost*|127.0.0.1|::1|postgres|\/*)/'
  'mB_contains_postgres|s/""\|localhost\|127\.0\.0\.1\|::1\|postgres\|\/\*\)/""|localhost|127.0.0.1|::1|postgres|*postgres*|\/*)/'
  'mC_no_hostaddr|s/host\|hostaddr\)/host)/'
  'mD_no_lower_host|s/case "\$\(lower "\$1"\)" in/case "\$1" in/'
  'mE_schemeless_ok|s/(\*:\/\/\*\) rest="\$\{url#\*:\/\/\}" ;;\n    \*\) )return 1/$1return 0/s'
  'mF_no_lower_nodeenv_shell|s/"\$\(lower "\$\{NODE_ENV:-\}"\)"/"\${NODE_ENV:-}"/'
  'mG_no_lower_nodeenv_file|s/"\$\(lower "\$\(read_key "\$FILE_SRC" NODE_ENV\)"\)"/"\$(read_key "\$FILE_SRC" NODE_ENV)"/'
  'mH_no_quote_strip|s/^  if \[\[ \$\{#v\} -ge 2.*\n//m'
  'mI_no_query_check|s/(  is_local_host "\$host" \|\| return 1\n)/$1  return 0\n/'
  'mJ_no_bracket_close_check|s/    \[\[ "\$host" == \*\\\]\* \]\] \|\| return 1\n//'
  'mK_no_shell_db_refuse|s/url_is_local "\$DATABASE_URL" \|\| refuse/url_is_local "\$DATABASE_URL" || true || refuse/'
  'mL_no_file_db_refuse|s/url_is_local "\$\(read_key "\$FILE_SRC" DATABASE_URL\)" \|\| refuse/url_is_local "\$(read_key "\$FILE_SRC" DATABASE_URL)" || true || refuse/'
  'mM_no_shell_nodeenv_refuse|s/  refuse NODE_ENV "the shell environment" "is production"/  true/'
  'mN_no_file_nodeenv_refuse|s/  refuse NODE_ENV "\$FILE_NAME" "is production"/  true/'
  'mO_bootstrap_before_refuse|s/(# ── 1\. Refuse first)/bash "\$SCRIPT_DIR\/bootstrap-env.sh" >\/dev\/null 2>&1 || true\n$1/'
  'mP_empty_url_refused|s/\[\[ -z "\$url" \]\] && return 0/[[ -z "\$url" ]] \&\& return 1/'
  'mQ_no_socket_dir|s/postgres\|\/\*\)/postgres)/'
  'mR_no_postgres_service|s/::1\|postgres\|/::1|/'
  'mS_no_ipv6_loopback|s/127\.0\.0\.1\|::1\|/127.0.0.1|/'
  'mT_no_ipv4_loopback|s/localhost\|127\.0\.0\.1\|/localhost|/'
  'mU_read_key_last|s/\| head -n1 \| cut -d= -f2-\)" \|\| true/| tail -n1 | cut -d= -f2-)" || true/'
  'mV_no_empty_host|s/case "\$\(lower "\$1"\)" in\n    ""\|/case "\$(lower "\$1")" in\n    /'
  'mW_refuse_exit_1|s/nothing was written." 3/nothing was written." 1/'
  'mX_no_chmod_local|s/  chmod 600 "\$ENV_LOCAL_FILE"\n/  :\n/'
  'mY_set_x|s/^set \+x$/set -x/m'
  'mZ_print_value|s/(  unset value\n)/  echo "\$value"\n$1/'
)
echo "== mutants =="
for m in "${MUTANTS[@]}"; do
  name="${m%%|*}"; expr="${m#*|}"
  t=$(mktree "$name") || continue
  perl -0pe "$expr" "$ORIG" > "$t/Blockchain/Dev/scripts/restore-local-secrets.sh"; chmod 755 "$t/Blockchain/Dev/scripts/restore-local-secrets.sh"
  if cmp -s "$ORIG" "$t/Blockchain/Dev/scripts/restore-local-secrets.sh"; then echo "$name: MUTATION DID NOT APPLY"; continue; fi
  bash -n "$t/Blockchain/Dev/scripts/restore-local-secrets.sh" || { echo "$name: syntax error"; continue; }
  res=$(suite "$t" "$L/$name.log")
  if [[ "$res" == rc=0* ]]; then verdict=SURVIVED; else verdict=killed; fi
  echo "$name: $verdict ($res) first-fail: $(grep -m1 '^FAIL ' "$L/$name.log" | cut -c1-110)"
done
