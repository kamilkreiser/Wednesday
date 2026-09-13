#!/bin/bash
# dead_banner_check.sh — is this coordinator pane showing Claude Code's OWN hard-stop
# banner ("Context limit reached · /compact or /clear to continue")?
#   usage: dead_banner_check.sh <tmux pane id>      rc 0 = DEAD banner present, rc 1 = not
#          dead_banner_check.sh --stdin              (same predicate over stdin, for red-proofs)
#
# WHY (2026-09-14 06:53, second self-kill in 8 h — ledger w=2): the DEAD leg in
# wake_watch.sh and the re-check in wednesday_rotate.sh --dead both did a bare
# `grep -q 'Context limit reached'` over the last 60 pane lines. That literal appears in
# ORDINARY tool output whenever a seat diagnoses the previous kill — a cat'd DIFF.md
# (23:39:43), a daily note written by heredoc (06:53:53), a `tail` of the runner log —
# and the leg killed a healthy 29% seat both times. A bare literal is a check that
# cannot discriminate the banner from a sentence ABOUT the banner.
#
# THE PREDICATE — a line counts as the banner only if ALL hold:
#   1. it contains the literal `Context limit reached`;
#   2. it contains NO quote or backtick (' " `) — every false positive so far was a quoted
#      grep pattern, a quoted pane name, or a quoted string in a script/diff; the UI banner
#      is plain text;
#   3. it is NOT a tool-output line: no `⎿` (Claude Code's result prefix) and no `$ ` command
#      echo on the line;
#   4. it is NOT a prose/markdown line about the banner: no `#`, no `—`/`;` (the runner's
#      own "DEAD — Context limit reached; the coordinator cannot act" wording), no `grep`.
# What it does NOT exclude, deliberately: the `·` and `/compact` half of the banner is NOT
# required — that wording is a 2026-09-02 reading of the UI and may change; requiring it
# would make a blind leg, which is the six-hour failure this leg exists to prevent.
# Red-proof: dead_banner_check.sh --selftest (runs the known false positives + one true).
set -u
pred() {
  LC_ALL=C.UTF-8 grep -F 'Context limit reached' \
    | grep -v -F -e "'" -e '"' -e '`' -e '⎿' -e '$ ' -e '#' -e '—' -e ';' -e 'grep' \
    | grep -q .
}
case "${1:-}" in
  --stdin) pred ;;
  --selftest)
    fail=0
    t() { # $1 expected rc, $2 label, stdin = pane text
      if printf '%s\n' "$3" | "$0" --stdin; then got=0; else got=1; fi
      if [ "$got" = "$1" ]; then echo "ok   rc=$got  $2"; else echo "FAIL rc=$got want $1  $2"; fail=$((fail+1)); fi
    }
    t 0 "true banner (plain UI line)"            "Context limit reached · /compact or /clear to continue"
    t 0 "true banner, indented 2"                "  Context limit reached · /compact or /clear to continue"
    t 1 "quoted grep pattern (DIFF.md 09-13)"   "+  if capture-pane | grep -q 'Context limit reached'; then"
    t 1 "runner log line (tail, 06:5x)"         "  ⎿  2026-09-14 06:53:53 WAKE: pane 'wednesday' DEAD — Context limit reached; the coordinator cannot act"
    t 1 "daily-note heredoc text (06:52)"       "     DEAD leg (\`capture-pane -S -60 | grep 'Context limit reached'\`) matched the literal"
    t 1 "script comment (rotate line 9)"        "# dead pane 94 times (\"Context limit reached · /compact or /clear to continue\")"
    t 1 "prose about it, unquoted, with dash"   "the seat hit Context limit reached — and the leg killed it"
    t 1 "empty"                                 ""
    [ "$fail" = 0 ] && echo "selftest PASS" || { echo "selftest FAIL ($fail)"; exit 9; }
    ;;
  "") echo "usage: dead_banner_check.sh <pane-id> | --stdin | --selftest" >&2; exit 2 ;;
  *)
    TMUX_BIN="${TMUX_BIN:-tmux}"
    "$TMUX_BIN" capture-pane -t "$1" -p -S -60 2>/dev/null | pred
    ;;
esac
