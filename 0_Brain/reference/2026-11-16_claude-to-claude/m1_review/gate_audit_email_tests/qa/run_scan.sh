#!/bin/bash
# words built at run time: identity, host, folder names under the workspace's !CODING (levels 1-2), plus words passed as "$@"
Q=/private/tmp/claude-501/qae; C="/Volumes/Laptop-DEV/!CODING"
W=("$(whoami)" "$(hostname)" "$(hostname -s)" "$HOME" "$@")
while IFS= read -r d; do n=$(basename "$d"); case "$n" in *.*|[0-9]_*|_*|debug|tmp|references|reports|coagent|"Claude to Claude"|Claude|CACHEDIR.TAG) ;; *) W+=("$n");; esac; done < <(find "$C" -mindepth 1 -maxdepth 2 -type d)
echo "words: ${#W[@]}"
python3 -B $Q/qa/qa_scan.py --files "${FILES[@]}" --words "${W[@]}"
