#!/bin/bash
# Drive the head script's bash-reader command line VERBATIM (copied from restore-local-secrets.sh lines 262-268,
# minus the node pipe) on single-line files; report whether each probe's side effect happened. No consumer bash runs here.
W=/Volumes/DevMASTER/WEDNESDAY/0_Brain/reference/2026-11-03_gate173-ks915-pr1989
T=$W/tmp/q6b; mkdir -p $T; CALLER_LOCALE=(-u LC_ALL)
probe() {  # probe ID LINE EXPECTED_ARTIFACT
  local id="$1" line="$2" art="$3" sb out
  printf '%s\n' "$line" > $T/$id.env
  sb="$(mktemp -d "$T/rls-ks915.XXXXXX")"; mkdir "$sb/empty"; ln -s "$T/$id.env" "$sb/e"
  env -u BASH_ENV -u ENV -u SHELLOPTS -u BASHOPTS -u PS4 "${CALLER_LOCALE[@]}" "$BASH" --norc --noprofile -n "$sb/e" </dev/null >/dev/null 2>&1; local n=$?
  out="$(env -u BASH_ENV -u ENV -u SHELLOPTS -u BASHOPTS -u PS4 -u CDPATH -u GLOBIGNORE "${CALLER_LOCALE[@]}" PATH="$sb/empty" HOME="$sb" \
      "$BASH" --norc --noprofile -c 'cd "$1" || exit 90; set -r; set -a; . e; s=$?; printf "%s\0%s\0%s\0%s\0%s\0%s\0%s\0" "@@RLS-KS915@@" "$s" "${DATABASE_URL-}" "${NODE_ENV-}" "${PGHOST-}" "${PGHOSTADDR-}" "${PGSERVICE-}"' \
      rls "$sb" </dev/null 2>$T/$id.err | tr '\0' '|' )"
  printf '%-4s parse_rc=%s artifact=%-8s fields=%s stderr=%s | %s\n' "$id" "$n" "$([[ -e $art ]] && echo CREATED || echo absent)" "$(printf '%s' "$out" | sed "s|$W|<W>|g" | cut -c1-80)" "$(head -c 120 $T/$id.err | tr '\n' ' ' | sed "s|$W|<W>|g")" "$(printf '%q' "$line" | sed "s|$W|<W>|g")"
}
probe x1 "history -s gate173; history -w $T/x1_created" $T/x1_created
probe x2 "HISTFILE=$T/x2_created; history -s gate173; history -w" $T/x2_created
probe x3 "command -p touch $T/x3_created" $T/x3_created
probe x4 "hash -p /usr/bin/touch tt; tt $T/x4_created" $T/x4_created
probe x5 "echo hi > $T/x5_created" $T/x5_created
probe x6 "builtin printf hi > $T/x6_created" $T/x6_created
probe x7 "read -r NODE_ENV < $W/harness/prodword.txt" /nonexistent
probe x8 "exec /usr/bin/touch $T/x8_created" $T/x8_created
probe x9 "/usr/bin/touch $T/x9_created" $T/x9_created
probe xa "enable -f /usr/lib/libz.dylib x" /nonexistent
probe xb "history -s 'NODE_ENV=production'; history -w $T/xb_created" $T/xb_created
echo "content of xb_created (crafted, not a secret): $(cat $T/xb_created 2>/dev/null)"
echo "control: same x3 line WITHOUT set -r/empty PATH creates it:"; env PATH=/usr/bin:/bin bash -c ". $T/x3.env"; ls $T/x3_created >/dev/null 2>&1 && echo "  x3 control CREATED" || echo "  x3 control absent"
