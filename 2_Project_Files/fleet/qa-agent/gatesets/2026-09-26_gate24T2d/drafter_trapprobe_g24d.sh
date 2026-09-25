#!/bin/bash
# drafter_trapprobe_g24d.sh — the DRAFTER's own probe of #1250 ROUND 2 (a PREDICTION instrument for the kit; the gate re-measures in its own clone
# with the REAL suite). Three runners, read with `git show` from the kit's scratch clone (never the checkout): develop's (== BASE's: #1250 is not on
# develop), round 1 c78f4093fb53 and round 2 2b8dcb824dd2. For each runner x arm it builds a throwaway tree under <kit>/_sp/trapprobe/<stamp>/ with
# TWO fixture suites — a.test.sh starts a GRANDCHILD `sleep 30 &` (its pid written to a file), then sleeps 4 s in the foreground; b.test.sh prints a
# marker — runs the runner in the background under a LONG TMPDIR (> 80 chars, so the KS-1135 substitution fires), signals it after 1.5 s, and records:
# rc, whether b ran, the verdict line, whether the named /tmp/rss dir survives, whether suite a's own bash and its grandchild are still alive 2 s
# after the signal (ORPHAN-ON-SIGNAL), and any `No such file` line (the round-1 lost-log symptom).
# ARMS: TERM-pid (plain `&`), INT-pid-m (INT to the pid, the driver under `set -m` — THE HARNESS'S OWN SHAPE, run_shell_suites.test.sh signal_run),
# INT-pid (INT to the pid, plain `&`, no job control), INT-group-m (INT to the group, `set -m`), and the hook-like pair TERM-pid-ign / INT-group-ign
# (the driver holds SIGINT as SIG_IGN before starting the runner: `trap '' INT`).
# Then RULE-2 itself: `trap -p INT` inside a background bash, with and without `set -m`, and under an INT-ignoring parent.
# Kills only its OWN processes, by pid (the runner, and at the end any of its own grandchild sleepers still alive). Deletes nothing: every /tmp/rss.*
# dir a run leaves is REPORTED by name. Usage: drafter_trapprobe_g24d.sh <kit dir>
set -u
K="${1:?kit dir}"; CL="$K/_sp/g24d_sp/clone.git"; P="$K/_sp/trapprobe/$(date -u +%H%M%S)"; mkdir -p "$P"
LONG="$P/$(printf 'z%.0s' $(seq 1 100))"; mkdir -p "$LONG"
LEFT_PIDS=""
probe() { # $1 runner label, $2 rev, $3 arm
  local R="$P/$1.$3"; mkdir -p "$R/Blockchain/Dev/scripts/__tests__"
  git --git-dir "$CL" show "$2:Blockchain/Dev/scripts/run-shell-suites.sh" > "$R/Blockchain/Dev/scripts/run-shell-suites.sh"
  printf '#!/bin/bash\necho "a: start"; sleep 30 & echo $! > "%s/grandchild.pid"; echo $$ > "%s/suite_a.pid"; sleep 4; echo "a: end"\n' "$R" "$R" > "$R/Blockchain/Dev/scripts/__tests__/a.test.sh"
  printf '#!/bin/bash\necho "b: RAN AFTER THE SIGNAL"\n' > "$R/Blockchain/Dev/scripts/__tests__/b.test.sh"
  local sig how ign=""
  case "$3" in
    TERM-pid) sig=TERM; how=pid ;; INT-pid) sig=INT; how=pid ;; INT-pid-m) sig=INT; how=pidm ;; INT-group-m) sig=INT; how=group ;;
    TERM-pid-ign) sig=TERM; how=pid; ign=1 ;; INT-group-ign) sig=INT; how=group; ign=1 ;;
  esac
  (
    [ -n "$ign" ] && trap '' INT
    [ "$how" = pidm ] || [ "$how" = group ] && set -m
    TMPDIR="$LONG" bash "$R/Blockchain/Dev/scripts/run-shell-suites.sh" > "$R/runner.out" 2> "$R/runner.err" &
    pid=$!
    sleep 1.5
    if [ "$how" = group ]; then kill -"$sig" -"$pid"; else kill -"$sig" "$pid"; fi
    wait "$pid"; echo "$?" > "$R/rc"
  ) > "$R/driver.out" 2>&1
  sleep 2
  local dir sa gc
  dir="$(sed -n 's|.*the suites ran under \(/tmp/rss\.[A-Za-z0-9]*\) .*|\1|p' "$R/runner.out" "$R/runner.err" | head -1)"
  sa="$(cat "$R/suite_a.pid" 2>/dev/null)"; gc="$(cat "$R/grandchild.pid" 2>/dev/null)"
  local sa_alive=no gc_alive=no
  [ -n "$sa" ] && kill -0 "$sa" 2>/dev/null && sa_alive=YES
  [ -n "$gc" ] && kill -0 "$gc" 2>/dev/null && { gc_alive=YES; LEFT_PIDS="$LEFT_PIDS $gc"; }
  printf '%-8s %-14s rc=%-4s b_ran=%s verdict=%s dir=%s left=%s suiteA_alive=%s grandchild_alive=%s nosuchfile=%s | stderr: %s\n' "$1" "$3" "$(cat "$R/rc")" \
    "$(grep -c 'b: RAN AFTER THE SIGNAL' "$R/runner.out")" "$(grep -c '^shell suites:' "$R/runner.out")" "${dir:-NONE}" \
    "$([ -n "$dir" ] && [ -d "$dir" ] && echo YES || echo no)" "$sa_alive" "$gc_alive" "$(cat "$R/runner.out" "$R/runner.err" | grep -c 'No such file')" \
    "$(tr '\n' ' ' < "$R/runner.err" | cut -c1-140)"
}
echo "drafter_trapprobe_g24d.sh $(date -u +%FT%TZ) | bash $BASH_VERSION | /bin/bash $(/bin/bash -c 'echo $BASH_VERSION') | long TMPDIR ${#LONG} chars | load $(uptime | sed 's/.*averages*: //')"
for arm in TERM-pid INT-pid-m INT-pid INT-group-m TERM-pid-ign INT-group-ign; do
  probe develop 4db87c3e4b98b8e366c3dd60d5f399917bad5086 "$arm"
  probe round1 c78f4093fb531bceb94a8e9defb59350d8c60b73 "$arm"
  probe round2 2b8dcb824dd2c5cd4b92757934d7de9d28813a22 "$arm"
done
echo "--- RULE 2 as the seat states it ('bash ignores SIGINT in any background job whatever the parent'), measured in three shapes:"
echo "  plain \`&\` (no job control):     trap -p INT inside = [$( ( bash -c 'trap "echo x" INT; trap -p INT' & wait ) 2>&1 )]"
echo "  \`set -m\` then \`&\` (the harness): trap -p INT inside = [$( ( set -m; bash -c 'trap "echo x" INT; trap -p INT' & wait ) 2>&1 )]"
echo "  INT-ignoring parent, \`set -m\`:   trap -p INT inside = [$( ( trap '' INT; set -m; bash -c 'trap "echo x" INT; trap -p INT' & wait ) 2>&1 )]"
echo "--- own leftover grandchild sleepers (ORPHAN-ON-SIGNAL): pids [${LEFT_PIDS# }] — ended BY PID now:"
for p in $LEFT_PIDS; do kill -TERM "$p" 2>/dev/null; echo "  kill -TERM $p rc=$?"; done
echo "--- /tmp/rss.* dirs named by these runs and still present (REPORTED, never removed):"
sed -n 's|.*the suites ran under \(/tmp/rss\.[A-Za-z0-9]*\) .*|\1|p' "$P"/*/runner.out "$P"/*/runner.err | sort -u | while read -r d; do [ -d "$d" ] && echo "  $d"; done
echo "done $(date -u +%FT%TZ)"
