#!/bin/bash
# Seat X 8th: `ssh -v` for the push driver, with a UTC time on every stderr line, so the next push death names its second (Wednesday's ANSWER to X 5th, 06:15:29Z).
# Used as core.sshCommand: git appends the host and the command, this script puts `-v` first. usage: X8_SSHLOG=<file> bash sshv_x8.sh [ssh options] host command
# stdin and stdout (the git protocol) pass through untouched. stderr goes to the log with a time on each line (every line, debug ones included);
# the NON-debug lines also go to the caller's stderr, so a failed push still prints "Connection to ... closed by remote host." into push.out as before.
# bash 3.2 safe: process substitution; the reader ends when ssh closes its stderr.
[ -n "${X8_SSHLOG:-}" ] || { echo "sshv_x8.sh: X8_SSHLOG is not set" >&2; exit 64; }
exec ssh -v "$@" 2> >(while IFS= read -r l; do
  printf '%s %s\n' "$(date -u +%H:%M:%SZ)" "$l" >> "$X8_SSHLOG"
  if [ "${l#debug[0-9]:}" = "$l" ]; then printf '%s\n' "$l" >&2; fi
done)
