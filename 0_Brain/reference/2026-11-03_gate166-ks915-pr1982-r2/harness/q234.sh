#!/bin/bash
# Q2 (no value printed), Q3 (idempotence / --rotate), Q4 (mode, gitignore, writes outside Dev).
# Prints only counts, hashes (truncated), modes, key names.
set -uo pipefail
source /Volumes/DevMASTER/WEDNESDAY/0_Brain/reference/2026-11-03_gate166-ks915-pr1982-r2/harness/lib.sh
TAG=${1:-q234}
L=$W/runs/$TAG; mkdir -p "$L"
yn() { if "$@"; then echo y; else echo n; fi; }

# every non-template value >= 8 chars in the given env files (stays in-process)
genvals() {
  local f line k v t
  for f in "$@"; do
    [[ -f "$f" ]] || continue
    while IFS= read -r line; do
      [[ "$line" =~ ^([A-Za-z_][A-Za-z0-9_]*)=(.*)$ ]] || continue
      k="${BASH_REMATCH[1]}"; v="${BASH_REMATCH[2]}"; v="${v%$'\r'}"
      [[ ${#v} -ge 8 ]] || continue
      t="$(valof "$R/Blockchain/Dev/env.example" "$k")"; [[ "$v" == "$t" ]] && continue
      t="$(valof "$R/Blockchain/Dev/.env.local.example" "$k")"; [[ "$v" == "$t" ]] && continue
      printf '%s\n' "$v"
      # also the 16-char prefix, so a truncated print is caught too
      printf '%s\n' "${v:0:16}"
    done < "$f"
  done | sort -u
}
leaks() {  # leaks VALUESFILE LOG... -> count of values found in any log
  local vf="$1"; shift; local n=0 v
  while IFS= read -r v; do for lg in "$@"; do grep -qF -- "$v" "$lg" && { n=$((n+1)); break; }; done; done < "$vf"
  echo $n
}

echo "== Q2/Q3/Q4 main sequence =="
A="$(mkclone ${TAG}-A)"; AE="$A/Blockchain/Dev/.env"; AL="$A/Blockchain/Dev/.env.local"
o0=$(outsidesum)
outside_dev0=$( ( cd "$A" && find . -path ./.git -prune -o -path ./Blockchain/Dev -prune -o -print | LC_ALL=C sort | xargs -I{} sh -c 'stat -f "%N %Lp %z" "{}"' ) | shasum -a256 | cut -c1-16)
gitcfg0=$(sha "$A/.git/config")
rc1=$(run "$A" "$L/r1.log");                 echo "run1 fresh rc=$rc1"
a1=$(hashof "$AE" ADMIN_USER_PASSWORD); s1=$(sha "$AE"); l1=$(sha "$AL")
echo "run1 ADMIN len=$(valof "$AE" ADMIN_USER_PASSWORD | tr -d '\n' | wc -c | tr -d ' ') hexonly=$([[ "$(valof "$AE" ADMIN_USER_PASSWORD)" =~ ^[0-9a-f]{48}$ ]] && echo y || echo n) ALLOW=$(valof "$AE" ALLOW_DEFAULT_SEED_PASSWORDS) mode_env=$(mode "$AE") mode_local=$(mode "$AL")"
rc2=$(run "$A" "$L/r2.log");                 echo "run2 idempotent rc=$rc2 env_sha_same=$([[ $s1 == $(sha "$AE") ]] && echo y || echo N) local_sha_same=$([[ $l1 == $(sha "$AL") ]] && echo y || echo N) admin_hash_same=$([[ $a1 == $(hashof "$AE" ADMIN_USER_PASSWORD) ]] && echo y || echo N)"
cp "$AE" "$L/before_rotate.env.bin"
rc3=$(run "$A" "$L/r3.log" -- --rotate);     a3=$(hashof "$AE" ADMIN_USER_PASSWORD)
nd=$(diff "$L/before_rotate.env.bin" "$AE" | grep -c '^[<>]')
dk=$(diff "$L/before_rotate.env.bin" "$AE" | grep '^[<>]' | sed -E 's/^[<>] ([A-Za-z_0-9]*)=.*/\1/' | sort -u | tr '\n' ' ')
echo "run3 --rotate rc=$rc3 admin_hash_changed=$([[ $a1 != $a3 ]] && echo y || echo N) diff_lines=$nd keys_changed=[$dk] lines_before=$(wc -l < "$L/before_rotate.env.bin" | tr -d ' ') lines_after=$(wc -l < "$AE" | tr -d ' ') local_sha_same=$([[ $l1 == $(sha "$AL") ]] && echo y || echo N) mode=$(mode "$AE")"
rc4=$(run "$A" "$L/r4.log");                 echo "run4 after rotate rc=$rc4 admin_hash_same_as_rotated=$([[ $a3 == $(hashof "$AE" ADMIN_USER_PASSWORD) ]] && echo y || echo N)"
rc5=$(run "$A" "$L/r5.log" -- --help);       echo "help rc=$rc5 says_GENERATES=$(yn grep -q 'GENERATES' "$L/r5.log") restores_nothing=$(yn grep -qi 'restores nothing from a store' "$L/r5.log")"
rc6=$(run "$A" "$L/r6.log" -- --bogus);      echo "unknown flag rc=$rc6"
rc7=$(run "$A" "$L/r7.log" "DATABASE_URL=postgres://u:p@gate165rmt.host/x"); echo "refusal (present .env) rc=$rc7"
rc8=$(run "$A" "$L/r8.log" "NODE_ENV=production"); echo "refusal NODE_ENV rc=$rc8"
rc9=$(run "$A" "$L/r9.log" -- --rotate --help); echo "--rotate --help rc=$rc9 env_unchanged_vs_r4=$([[ $a3 == $(hashof "$AE" ADMIN_USER_PASSWORD) ]] && echo y || echo N)"
# hostile-environment controls: xtrace forced from outside
( cd "$A" && env -i HOME="$W/home" PATH="$GPATH" TMPDIR="$W/tmp" bash -x "$A/Blockchain/Dev/scripts/restore-local-secrets.sh" --rotate ) > "$L/r10_bash-x.log" 2>&1; echo "bash -x --rotate rc=$?"
( cd "$A" && env -i HOME="$W/home" PATH="$GPATH" TMPDIR="$W/tmp" SHELLOPTS=xtrace bash "$A/Blockchain/Dev/scripts/restore-local-secrets.sh" --rotate ) > "$L/r11_shellopts.log" 2>&1; echo "SHELLOPTS=xtrace --rotate rc=$?"
o1=$(outsidesum)
outside_dev1=$( ( cd "$A" && find . -path ./.git -prune -o -path ./Blockchain/Dev -prune -o -print | LC_ALL=C sort | xargs -I{} sh -c 'stat -f "%N %Lp %z" "{}"' ) | shasum -a256 | cut -c1-16)
echo "outside HOME/TMPDIR unchanged=$([[ $o0 == $o1 ]] && echo y || echo N)  repo-root files outside Blockchain/Dev unchanged=$([[ $outside_dev0 == $outside_dev1 ]] && echo y || echo N)  .git/config unchanged=$([[ $gitcfg0 == $(sha "$A/.git/config") ]] && echo y || echo N)"
echo "Dev dir listing (names only): $(ls -A "$A/Blockchain/Dev" | tr '\n' ' ')"

# the leak search: every generated value now in .env/.env.local, plus every value .env held before the rotation
genvals "$AE" "$AL" "$L/before_rotate.env.bin" > "$L/vals.bin"
echo "Q2 instrument: values to search for = $(grep -c . "$L/vals.bin") (full values + 16-char prefixes)"
LOGS=("$L"/r[0-9].log)
echo "Q2 leaks in runs 1-9 stdout+stderr (incl --help, errors, refusals, --rotate, idempotent re-runs) = $(leaks "$L/vals.bin" "${LOGS[@]}")"
cp "$L/r3.log" "$L/planted.log.bin"; head -n1 "$L/vals.bin" >> "$L/planted.log.bin"
echo "Q2 control: planted value in a copy of run3 output found = $(leaks "$L/vals.bin" "$L/planted.log.bin")"
echo "Q2 xtrace lines (^+) in runs 1-9 = $(cat "${LOGS[@]}" | grep -c '^+')"
echo "Q2 hostile: bash -x  leaks=$(leaks "$L/vals.bin" "$L/r10_bash-x.log")  SHELLOPTS=xtrace leaks=$(leaks "$L/vals.bin" "$L/r11_shellopts.log")  (values regenerated by these --rotate runs are added below)"
genvals "$AE" > "$L/vals2.bin"
echo "Q2 hostile (new ADMIN after r10/r11): bash -x leaks=$(leaks "$L/vals2.bin" "$L/r10_bash-x.log") SHELLOPTS leaks=$(leaks "$L/vals2.bin" "$L/r11_shellopts.log")"

echo
echo "== Q3 existing-value shapes (ADMIN_USER_PASSWORD pre-set, no --rotate) =="
GOLD="$L/before_rotate.env.bin"
shape() {  # shape ID ADMINLINE [ALLOWLINE]
  local id="$1" line="$2" allow="${3-}" c e s0 rc
  c="$(mkclone ${TAG}-x$id)" || return; e="$c/Blockchain/Dev/.env"
  grep -v -E '^(ADMIN_USER_PASSWORD|ALLOW_DEFAULT_SEED_PASSWORDS)=' "$GOLD" > "$e"
  printf '%s\n' "$line" >> "$e"; [[ -n "$allow" ]] && printf '%s\n' "$allow" >> "$e"
  s0=$(sha "$e"); cp "$e" "$L/x$id.before.bin"
  rc=$(run "$c" "$L/x$id.log")
  local nd keys
  nd=$(diff "$L/x$id.before.bin" "$e" | grep -c '^[<>]')
  keys=$(diff "$L/x$id.before.bin" "$e" | grep '^[<>]' | sed -E 's/^[<>] (export )?([A-Za-z_0-9]*)[=: ].*/\2/' | sort -u | tr '\n' ' ')
  printf '%-4s rc=%s file_same=%s diff_lines=%s keys=[%s] admin_lines_now=%s msg=%s | %q %q\n' "$id" "$rc" \
    "$([[ $s0 == $(sha "$e") ]] && echo y || echo N)" "$nd" "$keys" "$(grep -c 'ADMIN_USER_PASSWORD' "$e")" \
    "$(grep -oE '(generated|kept|rotated) ADMIN_USER_PASSWORD|kept ALLOW_DEFAULT_SEED_PASSWORDS \([^)]*\)|set ALLOW_DEFAULT_SEED_PASSWORDS=true' "$L/x$id.log" | tr '\n' ';' | tr ' ' '_')" "$line" "$allow"
}
shape 1 "ADMIN_USER_PASSWORD=gate165-existing-not-secret-01" "ALLOW_DEFAULT_SEED_PASSWORDS=true"
shape 2 "ADMIN_USER_PASSWORD=\"gate165 quoted with spaces\"" "ALLOW_DEFAULT_SEED_PASSWORDS=true"
shape 3 "ADMIN_USER_PASSWORD='gate165-single'" "ALLOW_DEFAULT_SEED_PASSWORDS=false"
shape 4 "ADMIN_USER_PASSWORD=gate165-crlf"$'\r' "ALLOW_DEFAULT_SEED_PASSWORDS=true"
shape 5 "export ADMIN_USER_PASSWORD=gate165-export-form" "ALLOW_DEFAULT_SEED_PASSWORDS=true"
shape 6 "ADMIN_USER_PASSWORD = gate165-spaced" "ALLOW_DEFAULT_SEED_PASSWORDS=true"
shape 7 "ADMIN_USER_PASSWORD=" "ALLOW_DEFAULT_SEED_PASSWORDS=TRUE"
shape 8 "ADMIN_USER_PASSWORD=\"\"" "ALLOW_DEFAULT_SEED_PASSWORDS=\"true\""
shape 9 "ADMIN_USER_PASSWORD=   " ""
shape 10 "ADMIN_USER_PASSWORD=gate165-a"$'\n'"ADMIN_USER_PASSWORD=gate165-b" "ALLOW_DEFAULT_SEED_PASSWORDS=true"

echo
echo "== Q3 other keys byte-identical when the file has no trailing newline =="
c="$(mkclone ${TAG}-nonl)"; e="$c/Blockchain/Dev/.env"
grep -v -E '^ADMIN_USER_PASSWORD=' "$GOLD" | sed '$ s/$//' > "$e"; printf 'ADMIN_USER_PASSWORD=' >> "$e"   # last line blank admin, no newline
cp "$e" "$L/nonl.before.bin"; rc=$(run "$c" "$L/nonl.log")
echo "no-trailing-newline rc=$rc diff_keys=[$(diff "$L/nonl.before.bin" "$e" | grep '^[<>]' | sed -E 's/^[<>] ([A-Za-z_0-9]*)=.*/\1/' | sort -u | tr '\n' ' ')] other_lines_identical=$([[ "$(grep -v '^ADMIN_USER_PASSWORD=' "$L/nonl.before.bin" | shasum)" == "$(grep -v '^ADMIN_USER_PASSWORD=' "$e" | shasum)" ]] && echo y || echo N)"

echo
echo "== Q4 modes =="
c="$(mkclone ${TAG}-m1)"; e="$c/Blockchain/Dev/.env"; l="$c/Blockchain/Dev/.env.local"
cp "$GOLD" "$e"; chmod 644 "$e"; cp "$R/Blockchain/Dev/.env.local.example" "$l"; chmod 644 "$l"; s0=$(sha "$e")
rc=$(run "$c" "$L/m1.log"); echo "complete .env at 0644 + .env.local 0644: rc=$rc env_mode=$(mode "$e") local_mode=$(mode "$l") env_content_same=$([[ $s0 == $(sha "$e") ]] && echo y || echo N)"
c="$(mkclone ${TAG}-m2)"; e="$c/Blockchain/Dev/.env"
awk 'index($0,"ADMIN_USER_PASSWORD=")==1{print "ADMIN_USER_PASSWORD="; next}{print}' "$GOLD" > "$e"; chmod 644 "$e"
rc=$(run "$c" "$L/m2.log"); echo "incomplete .env at 0644: rc=$rc env_mode=$(mode "$e") (no .env.local present -> $( [[ -e $c/Blockchain/Dev/.env.local ]] && echo created-by-bootstrap:$(mode "$c/Blockchain/Dev/.env.local") || echo absent))"
c="$(mkclone ${TAG}-m3)"; e="$c/Blockchain/Dev/.env"
cp "$GOLD" "$e"; chmod 644 "$e"
rc=$(run "$c" "$L/m3.log" "DATABASE_URL=postgres://u:p@gate165rmt.host/x"); echo "refused run leaves pre-existing 0644 alone: rc=$rc env_mode=$(mode "$e")"
c="$(mkclone ${TAG}-m4)"; e="$c/Blockchain/Dev/.env"; tgt="$c/outside_target.env"
cp "$GOLD" "$tgt"; chmod 644 "$tgt"; ln -s ../../outside_target.env "$e"
rc=$(run "$c" "$L/m4.log"); echo "symlinked complete .env -> file outside Blockchain/Dev: rc=$rc link_still_symlink=$([[ -L $e ]] && echo y || echo n) outside_target_mode=$(mode "$tgt")"
c="$(mkclone ${TAG}-m5)"; mkdir -p "$c/.githooks"; g0=$(sha "$c/.git/config")
rc=$(run "$c" "$L/m5.log"); echo "repo with .githooks/: rc=$rc .git/config_changed=$([[ $g0 != $(sha "$c/.git/config") ]] && echo y || echo n) (bootstrap-env.sh's existing core.hooksPath write)"

echo
echo "== Q4 gitignore (in the PR-head clone, and in a scratch clone after a run) =="
for p in Blockchain/Dev/.env Blockchain/Dev/.env.local Blockchain/Dev/.env-ks915.Ab12Cd Blockchain/Dev/.env.ks915.Ab12Cd; do
  printf '%s -> %s\n' "$p" "$(git -C "$R" check-ignore -v --no-index "$p" || echo NOT-IGNORED)"
done
printf 'control env.example -> %s\n' "$(git -C "$R" check-ignore -v --no-index Blockchain/Dev/env.example || echo NOT-IGNORED)"
echo "scratch A git status --porcelain (untracked names): $(git -C "$A" status --porcelain -uall | grep -E '\.env' | tr '\n' ' ')"
