#!/bin/bash
# Gate 180 Q2: G174-F2 through the WHOLE script (head, or SCRIPT_SRC=round2). Escape forms: artifact outside the sandbox?
# Control per form: the same line under a plain unsandboxed `set -a; .` (artifact suffixed .ctl). Same-line forms: what
# an unsandboxed set -a reads (consumers_full) vs the script's verdict.
set -uo pipefail
source /Volumes/DevMASTER/WEDNESDAY/0_Brain/reference/2026-11-04_gate180-ks915-pr1989-r3/harness/lib.sh
source $W/harness/cells.sh
TAG=${1:-q3}; L=$W/runs/$TAG; A=$W/tmp/${TAG}-art; mkdir -p "$L" $W/tmp/$TAG $A; RUNTMP=$W/tmp/$TAG
M=gate180rmt; N=$'\n'
GB=$W/runs/golden/golden_blankadmin.env.bin; GL=$W/scratch/golden/Blockchain/Dev/.env.local
ctl() { local id="$1" line="$2" f=$W/tmp/$TAG/$1.ctl.env; printf '%s\n' "${line//$A\//$A/ctl-}" > $f
  ( env -i PATH=/usr/bin:/bin bash -c 'cd "$2"; set -a; . "$1"' _ $f $W/tmp/$TAG ) >/dev/null 2>&1; [[ -e $A/ctl-$id ]] && echo CREATED || echo absent; }
esc() { local id="$1" line="$2"; NOCONS=1 gcell $id "$line$N" '' ''
  printf '      artifact(script)=%s  artifact(unsandboxed control)=%s\n' "$([[ -e $A/$id ]] && echo CREATED || echo absent)" "$(ctl $id "$line")"; }
echo "bash: $(/bin/bash --version | head -1)"
echo "== A. PATH escape forms (must not execute; must be refused) =="
esc e01 "X=1; PATH=/usr/bin:/bin; touch $A/e01"
esc e02 "export PATH=/usr/bin:/bin; touch $A/e02"
esc e03 "declare PATH=/usr/bin:/bin; touch $A/e03"
esc e04 "PATH=/usr/bin:/bin touch $A/e04"
esc e05 "read PATH <<< /usr/bin; touch $A/e05"
esc e06 "printf -v PATH /usr/bin; touch $A/e06"
esc e07 "eval 'PATH=/usr/bin:/bin'; touch $A/e07"
esc e08 "f(){ local PATH=/usr/bin:/bin; touch $A/e08; }; f"
esc e09 "declare +r PATH; PATH=/usr/bin; touch $A/e09"
esc e10 "(PATH=/usr/bin:/bin; touch $A/e10)"
esc e11 "trap 'PATH=/usr/bin:/bin; touch $A/e11' EXIT"
esc e12 "for PATH in /usr/bin; do touch $A/e12; done"
esc e13 "PATH+=:/usr/bin; touch $A/e13"
esc e14 "unset PATH; touch $A/e14"
esc e15 "{ PATH=/usr/bin:/bin; touch $A/e15; } 2<&-"
esc e16 "exec 2<&-; PATH=/usr/bin:/bin; touch $A/e16"
echo "== B. same-line forms (must be REFUSED, not under-read) =="
gcell s1 "PATH=/usr/bin:/bin; POSTGRES_HOST=$M.host$N" '' ''
gcell s2 "PATH=/usr/bin:/bin; declare -x POSTGRES_\"\"HOST=$M.host$N" '' ''
gcell s3 "PATH+=:/x; declare -x POSTGRES_\"\"HOST=$M.host$N" '' ''
echo "== C. same-line forms with the reader's stderr redirected on THAT line or earlier (stderr-closing residual) =="
gcell z1 "{ PATH=/usr/bin:/bin; declare -x POSTGRES_\"\"HOST=$M.host; } 2<&-$N" '' ''
gcell z2 "{ PATH=/usr/bin:/bin; declare -x POSTGRES_\"\"HOST=$M.host; } 2<&1$N" '' ''
gcell z3 "exec 2<&-${N}PATH=/usr/bin:/bin; declare -x POSTGRES_\"\"HOST=$M.host$N" '' ''
gcell z4 "PATH=/usr/bin:/bin 2<&-; declare -x POSTGRES_\"\"HOST=$M.host$N" '' ''
echo "== D. benign (must be accepted) =="
gcell b1 "ENV=dev${N}SHELL=/bin/zsh${N}NODE_ENV=development${N}MY_PATH=/opt/x$N" '' ''
gcell b2 "PYTHONPATH=/opt/py${N}MANPATH=/usr/share/man${N}PATH_PREFIX=/x${N}NPM_PATH=/y$N" '' ''
gcell b3 "# PATH=/usr/bin is only a comment$N" '' ''
