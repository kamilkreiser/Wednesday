#!/bin/bash
# words built at run time (never written to a file): identity, hosts, home, workspace and drive parts, folder names under !CODING (levels 1-2), plus "$@"
Q=/private/tmp/claude-501/qae2; C="/Volumes/Laptop-DEV/!CODING"
W=("$(whoami)" "$(hostname)" "$(hostname -s)" "$(scutil --get ComputerName)" "$(scutil --get LocalHostName)" "$HOME" "$@")
while IFS= read -r d; do n=$(basename "$d"); case "$n" in *.*|[0-9]_*|_*|debug|tmp|references|reports|coagent|"Claude to Claude"|Claude|CACHEDIR.TAG|docs|tests|src|scripts|tools|target) ;; *) W+=("$n");; esac; done < <(find "$C" -mindepth 1 -maxdepth 2 -type d 2>/dev/null)
echo "words: ${#W[@]}" >&2
python3 -B $Q/h/qa2_scan.py --files "${FILES[@]}" --words "${W[@]}"
