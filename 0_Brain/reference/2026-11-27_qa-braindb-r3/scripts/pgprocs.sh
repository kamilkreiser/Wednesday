#!/bin/bash
# list every process whose EXECUTABLE is postgres, with its -D; select by executable, never by a text pattern
snap="$(ps -axww -o pid=,comm=)"
n=0
while read -r pid comm; do
  case "${comm##*/}" in postgres)
    n=$((n+1)); echo "pid $pid : $(ps -ww -p "$pid" -o command= | cut -c1-260)";;
  esac
done <<< "$snap"
echo "processes whose executable is postgres: $n (control: bash processes $(printf '%s\n' "$snap" | awk '{print $2}' | /usr/bin/grep -c -E '(^|/)bash$'))"
