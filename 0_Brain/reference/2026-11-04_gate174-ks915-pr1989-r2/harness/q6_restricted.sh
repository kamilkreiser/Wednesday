#!/bin/bash
# Q6: drive the head script's bash-reader -c string, CUT from restore-local-secrets.sh line 278 (not retyped), on one-line
# files; report whether each probe's side effect (a file outside the sandbox) happened. Control: the same line unsandboxed.
W=/Volumes/DevMASTER/WEDNESDAY/0_Brain/reference/2026-11-04_gate174-ks915-pr1989-r2
S=$W/repo/Blockchain/Dev/scripts/restore-local-secrets.sh
T=$W/tmp/q6; mkdir -p $T; CALLER_LOCALE=(-u LC_ALL)
CSTR="$(sed -n '278p' "$S" | sed -E "s/^[^']*-c '//; s/' *\\\\\$//")"
printf 'reader -c string cut from line 278: %s chars; contains enable -n history kill: %s; set -r: %s\n' "${#CSTR}" "$([[ $CSTR == *'enable -n history kill; HISTFILE=/dev/null; set -r;'* ]] && echo y || echo N)" "$([[ $CSTR == *'set -r'* ]] && echo y || echo N)"
echo "bash: $(/bin/bash --version | head -1)"
probe() {  # probe ID LINE ARTIFACT
  local id="$1" line="$2" art="$3" sb out rc
  printf '%s\n' "$line" > $T/$id.env
  sb="$(mktemp -d "$T/rls-ks915.XXXXXX")"; mkdir "$sb/empty"; ln -s "$T/$id.env" "$sb/e"
  out="$(env -u BASH_ENV -u ENV -u SHELLOPTS -u BASHOPTS -u PS4 -u CDPATH -u GLOBIGNORE "${CALLER_LOCALE[@]}" PATH="$sb/empty" HOME="$sb" TMPDIR="$T" \
      /bin/bash --norc --noprofile -c "$CSTR" rls "$sb" </dev/null 2>$T/$id.err | tr '\0' '|')"; rc=$?
  local created=absent; [[ -e $art ]] && created=CREATED
  # control: the same line, unsandboxed (plain set -a; .), artifact name suffixed .ctl
  local ctl_art="$art.ctl" ctl=absent; printf '%s\n' "${line//$art/$ctl_art}" > $T/$id.ctl.env
  ( cd $T && env -i PATH=/usr/bin:/bin TMPDIR=$T /bin/bash -c 'set -a; . "$1"' _ $T/$id.ctl.env ) >/dev/null 2>&1; [[ -e $ctl_art ]] && ctl=CREATED
  printf '%-4s sandboxed=%-7s unsandboxed_control=%-7s record=%s stderr=%s | %s\n' "$id" "$created" "$ctl" "$(printf '%s' "$out" | cut -d'|' -f1-2)" "$(head -c 110 $T/$id.err | tr '\n' ' ' | sed "s|$W|<W>|g")" "$(printf '%q' "$line" | sed "s|$W|<W>|g")"
}
A=$T/art
probe x1 "history -s gate174; history -w $A-x1" $A-x1
probe x2 "HISTFILE=$A-x2; history -s gate174; history -w" $A-x2
probe x3 "enable history; history -s gate174; history -w $A-x3" $A-x3
probe x4 "builtin history -w $A-x4" $A-x4
probe x5 "command history -w $A-x5" $A-x5
probe x6 "builtin enable history; history -w $A-x6" $A-x6
probe x7 "command enable history; history -w $A-x7" $A-x7
probe x8 "set -o history; HISTFILE=$A-x8; shopt -s histappend; echo gate174" $A-x8
probe x9 "set -o history; echo gate174; fc -l > $A-x9" $A-x9
probe xa "set -o history; echo gate174; fc -e : -1" $A-xa
probe xb "set -o history; echo gate174; FCEDIT=touch fc -1" $A-xb
probe xc "trap 'history -w $A-xc' EXIT" $A-xc
probe xd "exec 3<>$A-xd" $A-xd
probe xe "command -p touch $A-xe" $A-xe
probe xf "builtin printf hi > $A-xf" $A-xf
probe xg "exec /usr/bin/touch $A-xg" $A-xg
probe xh "kill -0 \$\$ && builtin printf '%s\\0' @@RLS-KS915@@ 0 kill-ran" /nonexistent
probe xi "enable kill; kill -0 \$\$" /nonexistent
probe xj "HISTFILE=$A-xj; set -o history; history -a" $A-xj
probe xk "read -r x <<GATE
hi
GATE
echo ok" /nonexistent
probe xl "PATH=/usr/bin; touch $A-xl" $A-xl
probe xm "type -P touch && hash -p /usr/bin/touch t; t $A-xm" $A-xm
probe xn "enable -f /usr/lib/libz.dylib x; enable -n set; set +r" /nonexistent
probe xo "set +r; echo hi > $A-xo" $A-xo
probe xp "shopt -u restricted_shell; echo hi > $A-xp" $A-xp
echo "files left in $T outside sandboxes (not .env/.err/.ctl*): $(ls $T | grep -v -E '\.(env|err)$|\.ctl|^rls-ks915' | tr '\n' ' ')"
echo "sandbox dirs left by this harness (it does not clean them): $(ls -d $T/rls-ks915.* | wc -l | tr -d ' ')"
