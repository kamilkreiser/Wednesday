#!/bin/bash
# no_rm_arms.sh — red-proof arms for pretooluse_no_rm.sh. Run:  bash <this file>
# Each arm feeds a Bash-tool-shaped hook JSON to the hook and compares the rc to the expectation.
# The arm STRINGS live in this FILE, not in a Bash tool command — because the hook is in the
# Bash tool's own path, a command that carries `rm /Volumes/...` as test data is refused before
# it runs (2026-09-14 15:4x, the second live fire). Exit 1 if any arm disagrees.
H="$(cd -P "$(dirname "${BASH_SOURCE[0]}")/.." && pwd)/pretooluse_no_rm.sh"
fails=0
arm() { # label, command-text, expected-rc
  printf '%s' "$2" | python3 -c 'import json,sys;print(json.dumps({"tool_input":{"command":sys.stdin.read()}}))' \
    | bash "$H" >/dev/null 2>/tmp/no_rm_arm_err.txt; rc=$?
  if [ "$rc" -eq "$3" ]; then echo "ok   $1 rc=$rc"; else echo "FAIL $1 rc=$rc expected $3"; sed -n 1,3p /tmp/no_rm_arm_err.txt; fails=$((fails+1)); fi
}
arm "A rm project file"        'rm /Volumes/DevMASTER/WEDNESDAY/0_Brain/x.md' 2
arm "B rm -f var path"         'rm -f "$R/out.txt"' 2
arm "C rm scratch literal"     'rm -rf /private/tmp/claude-501/-Volumes-DevMASTER-WEDNESDAY/abc/clone' 0
arm "D rm /tmp literal"        'rm /tmp/claude-501/norm_err.txt' 0
arm "E git rm"                 'git -C /Volumes/DevMASTER/WEDNESDAY rm 0_Brain/x.md' 2
arm "F git rm --cached"        'git -C /Volumes/DevMASTER/WEDNESDAY rm --cached 0_Brain/x.md' 0
arm "G find -delete project"   'find /Volumes/DevMASTER/WEDNESDAY/2_Project_Files -name "*.pyc" -delete' 2
arm "H find -delete scratch"   'find /private/tmp/claude-501/x -name "*.out" -delete' 0
arm "I prose in heredoc"       $'cat > /private/tmp/x <<\'EOF\'\nthe rm hook refuses; never rm a file\nEOF' 0
arm "J chained after &&"       'ls /x && rm /Volumes/DevMASTER/WEDNESDAY/y' 2
arm "K docker --rm flag"       'docker run --rm -it alpine ls' 0
arm "L rmdir"                  'rmdir /Volumes/DevMASTER/WEDNESDAY/emptydir' 0
arm "M git grep rm"            'git -C /Volumes/DevMASTER/WEDNESDAY grep -n "rm -f" -- "*.sh"' 0
arm "N cmd subst rm"           'echo $(rm /Volumes/DevMASTER/WEDNESDAY/z)' 2
arm "O backticked prose (the 15:4x false positive)" $'bash /x/note_entry.sh --stdin <<\'EOF\'\nbuilt `pretooluse_no_rm.sh` (refuses `rm` / `unlink` / `git rm` (not `--cached`) / `find -delete` outside)\nEOF' 0
arm "P backtick subst rm (NOT caught — accepted, stated)" 'echo `rm /Volumes/DevMASTER/WEDNESDAY/z`' 0
arm "Q unlink project"         'unlink /Volumes/DevMASTER/WEDNESDAY/0_Brain/x.md' 2
arm "R rm after pipe"          'ls | rm /Volumes/DevMASTER/WEDNESDAY/y' 2
# 2026-11-23: quoted heredoc bodies are data UNLESS the opener feeds a shell reading stdin as a script.
arm "S note line BEGINS with rm (the 02:0x false positive)" $'bash /x/note_entry.sh --stdin <<\'EOF\'\nrm -f was aimed at a path that did not exist; disclosed\nEOF' 0
arm "T prose rm after ; and | in cat heredoc" $'cat > /private/tmp/x <<\'EOF\'\nit said; rm /Volumes/DevMASTER/WEDNESDAY/y | and stopped\nEOF' 0
arm "U bash reads heredoc as script"  $'bash <<\'EOF\'\nrm /Volumes/DevMASTER/WEDNESDAY/y\nEOF' 2
arm "V bash -s with args"             $'bash -s arg1 <<\'EOF\'\nrm /Volumes/DevMASTER/WEDNESDAY/y\nEOF' 2
arm "W ssh heredoc"                   $'ssh box <<\'EOF\'\nrm /home/u/y\nEOF' 2
arm "X real rm AFTER the heredoc end" $'cat > /private/tmp/x <<\'EOF\'\nhi\nEOF\nrm /Volumes/DevMASTER/WEDNESDAY/y' 2
arm "Y unquoted heredoc not stripped" $'cat > /private/tmp/x <<EOF\nrm /Volumes/DevMASTER/WEDNESDAY/y\nEOF' 2
arm "Z cat heredoc piped into sh"     $'cat <<\'EOF\' | sh\nrm /Volumes/DevMASTER/WEDNESDAY/y\nEOF' 2
arm "AA <<- dash form into zsh"       $'zsh <<-\'EOF\'\n\trm /Volumes/DevMASTER/WEDNESDAY/y\n\tEOF' 2
arm "AB double-quoted tag prose"      $'cat > /private/tmp/x <<"EOF"\nrm is never used here\nEOF' 0
arm "AC source /dev/stdin heredoc"    $'source /dev/stdin <<\'EOF\'\nrm /Volumes/DevMASTER/WEDNESDAY/y\nEOF' 2
echo "fails=$fails"; exit $(( fails > 0 ))
