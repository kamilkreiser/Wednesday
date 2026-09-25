#!/bin/bash
# drafter_maskprobe_g24d.sh — does a suite RUN BY run-shell-suites.sh see SIGINT as installable? (PREDICTION instrument; the gate re-measures.)
# One fixture suite prints the same probe run_shell_suites.test.sh uses (`( trap 'x' INT; trap -p INT )` non-empty = installable), plus whether its
# stdin is a TTY/pipe/devnull. Run under develop's runner and #1250 round 2's, from a normal (non-hook) shell, stdin from a pipe. Deletes nothing.
set -u
K="${1:?kit}"; CL="$K/_sp/g24d_sp/clone.git"; P="$K/_sp/maskprobe/$(date -u +%H%M%S)"; mkdir -p "$P"
for pair in develop:4db87c3e4b98b8e366c3dd60d5f399917bad5086 round2:2b8dcb824dd2c5cd4b92757934d7de9d28813a22; do
  lab="${pair%%:*}"; rev="${pair#*:}"; R="$P/$lab"; mkdir -p "$R/Blockchain/Dev/scripts/__tests__"
  git --git-dir "$CL" show "$rev:Blockchain/Dev/scripts/run-shell-suites.sh" > "$R/Blockchain/Dev/scripts/run-shell-suites.sh"
  printf '%s\n' '#!/bin/bash' 't="$( ( trap "x" INT 2>/dev/null; trap -p INT ) 2>/dev/null )"' 'echo "SUITE-PROBE INT installable=$([ -n "$t" ] && echo yes || echo no)"' 'if read -r -t 1 line; then echo "SUITE-PROBE stdin gave: $line"; else echo "SUITE-PROBE stdin gave nothing (rc $?)"; fi' > "$R/Blockchain/Dev/scripts/__tests__/p.test.sh"
  echo "from-the-caller" | bash "$R/Blockchain/Dev/scripts/run-shell-suites.sh" > "$R/out" 2> "$R/err"; rc=$?
  echo "$lab runner rc=$rc: $(grep SUITE-PROBE "$R/out" | tr '\n' ' ')"
done
