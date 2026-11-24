#!/bin/bash
# runs preview/demo/setup.sh of base and head into scratch roots with 4 stub executables, diffs COMMANDS.txt
set -u
CL=/private/tmp/claude-501/qwt/clone; W=/private/tmp/claude-501/qwt/setup_t; rm -rf "$W"; mkdir -p "$W/bin"
for n in coagentd coagent coagent-mcp coagent-hook; do printf '#!/bin/sh\nexit 0\n' > "$W/bin/$n"; chmod +x "$W/bin/$n"; done
for v in base head; do
  rev=$([ $v = base ] && echo 039b9875b69918c2a83e95d84f7f8169358b59d5 || echo cf541edfee9a08a703af0b2a5fbf3a8764e6fec4)
  mkdir -p "$W/src_$v"; git -C "$CL" archive $rev preview | tar -x -C "$W/src_$v"
  ( HOME=/private/tmp/claude-501/qwt/setup_t/home bash "$W/src_$v/preview/demo/setup.sh" "$W/root_$v" "$W/bin" > "$W/out_$v.txt" 2> "$W/err_$v.txt"; echo "$v exit=$?" )
  sed -e "s#$W/root_$v#<ROOT>#g" -e "s#$W/src_$v#<SRC>#g" "$W/root_$v/COMMANDS.txt" > "$W/norm_$v.txt"
  echo "$v headings: $(grep -o '^## [0-9]*\.' "$W/norm_$v.txt" | tr -d '#. \n' | sed 's/\([0-9]\)/\1 /g')"; ls -ld "$W/root_$v" | cut -c1-12
done
echo "--- diff base head (normalised)"; diff "$W/norm_base.txt" "$W/norm_head.txt"; echo "diff-exit=$?"
echo "--- stdout == COMMANDS.txt ?"; cmp "$W/out_head.txt" "$W/root_head/COMMANDS.txt" && echo same
echo "--- stderr"; cat "$W/err_head.txt" | head -5
