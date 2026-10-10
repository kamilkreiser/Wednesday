#!/bin/bash
# zsh_wordsplit_arms.sh — red-proof arms for pretooluse_zsh_wordsplit.sh. Run:  bash <this file>
# Each arm feeds a Bash-tool-shaped hook JSON on stdin and compares the rc (2 = refused, 0 = passed);
# a refusal must also name the hook on stderr. The arm strings live in this FILE, not in a Bash
# tool command, because the hook sits in the Bash tool's own path.
# HOOK_UNDER_TEST=<path> runs the arms against another copy (the red run: a missing hook).
H="${HOOK_UNDER_TEST:-$(cd -P "$(dirname "${BASH_SOURCE[0]}")/.." && pwd)/pretooluse_zsh_wordsplit.sh}"
ERR=$(mktemp "${TMPDIR:-/tmp}/zsh_ws_arm.XXXXXX"); P=0; F=0
arm() { # label, command-text, expected-rc
  printf '%s' "$2" | python3 -c 'import json,sys;print(json.dumps({"tool_input":{"command":sys.stdin.read()}}))' \
    | bash "$H" >/dev/null 2>"$ERR"; rc=$?
  named=yes; [ "$3" = 2 ] && ! grep -q "pretooluse_zsh_wordsplit" "$ERR" && named=no
  if [ "$rc" -eq "$3" ] && [ "$named" = yes ]; then P=$((P+1)); echo "ok   $1 rc=$rc"
  else F=$((F+1)); echo "FAIL $1 rc=$rc expected $3 (stderr names hook: $named)"; sed -n 1,2p "$ERR"; fi
}
arm "A var with space, command position"   'G="git -C /x"; $G status' 2
arm "B for-list quoted items, set -- \$p"  'for p in "%4 B09" "%5 B10"; do set -- $p; echo $1; done' 2
arm "C braces form \${G}"                  "G='git -C /x'; \${G} log -1" 2
arm "D for y in \$LIST"                    'L="a b c"; for y in $L; do echo $y; done' 2
arm "E after &&"                           'G="git -C /x" && echo hi && $G status' 2
arm "F A wrapped in bash -c"               'bash -c '\''G="git -C /x"; $G status'\''' 0
arm "G B wrapped in bash -c"               'bash -c '\''for p in "%4 B09" "%5 B10"; do set -- $p; echo $1; done'\''' 0
arm "H no-whitespace value"                'W=/abs/tool.sh; $W --check' 0
arm "I quoted use"                         'G="git -C /x"; "$G"' 0
arm "J heredoc body"                       $'cat > /private/tmp/x.md <<\'EOF\'\nG="git -C /x"; $G status\nEOF' 0
arm "K echo \$HOME"                        'echo $HOME' 0
arm "L bash \$SCRIPT args"                 'S="/abs/my tool.sh"; bash "$S" --x' 0
arm "M bash -c inside a longer command"    'echo start; bash -c '\''G="git -C /x"; $G status'\''' 0
arm "N set -- quoted"                      'for p in "a b" "c d"; do set -- "$p"; echo "$1"; done' 0
arm "O bash heredoc-fed"                   $'bash <<\'EOF\'\nG="git -C /x"; $G status\nEOF' 0
got=$(printf 'not json' | bash "$H" 2>/dev/null; echo $?)
if [ "$got" = 0 ]; then P=$((P+1)); echo "ok   fail-open on bad input"; else F=$((F+1)); echo "FAIL fail-open got $got"; fi
echo "== $P pass, $F fail"; [ "$F" = 0 ]
