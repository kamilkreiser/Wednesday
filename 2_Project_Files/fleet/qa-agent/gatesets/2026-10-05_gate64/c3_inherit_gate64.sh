#!/bin/bash
# c3_inherit_gate64.sh — ITEM 3 / COUPLING probe for #1389 (KS-1330): what does a suite INHERIT from the runner that launches it?
# The head runner launches each suite ASYNC (`bash suite > log 2>&1 &` + `wait`, no `set -m`); develop's ran it in a foreground
# `| tee` pipeline. The runner header (KS-1330 item 3) claims two MEASURED inherited conditions: (1) SIGINT is IGNORED in the suite,
# (2) the suite's stdin is /dev/null. This probe measures both, for each runner given, in a throw-away git repo under --out:
#   * one probe suite at Blockchain/Dev/scripts/__tests__/zz_probe.test.sh records (a) can it INSTALL an INT handler (the harness's
#     sig_installable method: install, then look), (b) `stat -L` of its fd 0: dev, inode, rdev — and the same for /dev/null;
#   * the RUNNER is started in the FOREGROUND of this script with stdin redirected from a REGULAR marker file, so "the suite's stdin is
#     /dev/null" can only be true if the RUNNER substituted it (a gate shell whose own stdin is already /dev/null would otherwise make
#     the reading meaningless — the marker is the discriminator).
# Verdict lines per runner:  INT-in-suite installable=<yes|no>  |  suite fd0 == /dev/null <yes|no>  |  suite fd0 == marker <yes|no>
# Expected (the claim): head -> INT no, fd0 /dev/null yes; develop -> INT yes, fd0 marker yes (the CONTROL that differs).
# G1 as in c3_redfirst: refuses rc 4 when THIS shell has SIGINT ignored on entry (a backgrounded probe would read "no" for both runners).
# Usage: c3_inherit_gate64.sh --out <dir> --runner <label>=<runner file> [--runner <label>=<file> ...]
# rc 0 measured (the readings are REPORTED; the gate rules) / 4 INSTRUMENT (G1, or a probe that wrote nothing) / 9 usage.
set -u
OUT=""; RUNNERS=()
while [ $# -gt 0 ]; do
  case "$1" in --out) OUT="$2"; shift 2;; --runner) RUNNERS+=("$2"); shift 2;; *) echo "usage: see header"; exit 9;; esac
done
[ -n "$OUT" ] && [ "${#RUNNERS[@]}" -gt 0 ] || { echo "usage: --out <dir> --runner <label>=<file> ..."; exit 9; }
mkdir -p "$OUT"
case "$(cd "$OUT" && pwd -P)" in /Volumes/DevMASTER/\!CODING/*) echo "REFUSED: --out is inside !CODING"; exit 9;; esac
_t="$( ( trap 'x' INT 2>/dev/null; trap -p INT ) 2>/dev/null )"
[ -n "$_t" ] || { echo "INSTRUMENT: SIGINT is IGNORED on entry to this shell — run in the FOREGROUND"; exit 4; }
echo "G1 this shell: INT installable ($_t) | this shell's own fd0: $(stat -L -f 'dev %d ino %i rdev %Hr,%Lr' /dev/stdin 2>&1)"
NULLID="$(stat -L -f 'dev %d ino %i rdev %Hr,%Lr' /dev/null)"
MARK="$OUT/stdin_marker.txt"; echo "a regular file standing in for an operator's stdin" > "$MARK"
MARKID="$(stat -L -f 'dev %d ino %i rdev %Hr,%Lr' "$MARK")"
echo "/dev/null: $NULLID | marker: $MARKID"
rc_all=0
for spec in "${RUNNERS[@]}"; do
  label="${spec%%=*}"; rf="${spec#*=}"
  [ -f "$rf" ] || { echo "no runner file $rf"; exit 9; }
  R="$OUT/repo_$label"
  if [ -e "$R" ]; then mv "$R" "$OUT/_quarantine_repo_${label}_$(date -u +%H%M%S)"; fi
  mkdir -p "$R/Blockchain/Dev/scripts/__tests__" "$R/systemTest/__tests__"
  cp "$rf" "$R/Blockchain/Dev/scripts/run-shell-suites.sh"
  rec="$OUT/probe_$label.txt"; : > "$rec"
  cat > "$R/Blockchain/Dev/scripts/__tests__/zz_probe.test.sh" <<PROBE
#!/usr/bin/env bash
t="\$( ( trap 'x' INT 2>/dev/null; trap -p INT ) 2>/dev/null )"
[ -n "\$t" ] && echo "int_installable=yes" >> "$rec" || echo "int_installable=no" >> "$rec"
echo "fd0=\$(stat -L -f 'dev %d ino %i rdev %Hr,%Lr' /dev/stdin 2>&1)" >> "$rec"
echo "probe ran"
exit 0
PROBE
  git -C "$R" init -q && git -C "$R" add -A && git -C "$R" -c user.email=probe@invalid -c user.name=probe commit -qm probe || { echo "fixture repo failed"; exit 4; }
  ( cd "$R/Blockchain/Dev" && bash scripts/run-shell-suites.sh < "$MARK" > "$OUT/runner_$label.out" 2> "$OUT/runner_$label.err" ); rrc=$?
  ii="$(sed -n 's/^int_installable=//p' "$rec")"; fd0="$(sed -n 's/^fd0=//p' "$rec")"
  [ -n "$ii" ] && [ -n "$fd0" ] || { echo "INSTRUMENT: the probe suite under $label wrote nothing (runner rc $rrc; see $OUT/runner_$label.out)"; rc_all=4; continue; }
  # compare by INODE + RDEV only: through /dev/fd the `dev` field reads devfs's, not the file system's (measured on the drafter's
  # first run, c3_inherit_ex1: the develop suite's fd0 had the marker's inode but devfs's dev, and read as "neither")
  isnull=no; [ "${fd0#* * }" = "${NULLID#* * }" ] && isnull=yes
  ismark=no; [ "${fd0#* * }" = "${MARKID#* * }" ] && ismark=yes
  echo "RESULT $label (runner sha256 $(shasum -a 256 "$rf" | cut -c1-16), runner rc $rrc, tally: $(grep '^shell suites:' "$OUT/runner_$label.out")) | INT-in-suite installable=$ii | suite fd0 == /dev/null $isnull | suite fd0 == marker $ismark | fd0 '$fd0'"
done
exit $rc_all
