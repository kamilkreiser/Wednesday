#!/bin/zsh
# QA-MEASURE-2-R2 task 1: the seat's two tools from my clone at the head, fed planted lines built IN MEMORY (/dev/fd), never
# written to disk. The searched words are derived at run time from CLAUDE_CONFIG_DIR (as redact.py does) and masked as <n1>/<n2>
# in everything printed. usage: zsh qm2r_tools.sh <spike folder of the clone at the head> <seat scratch root>
D="$1"; export M2_SCR="$2"
N1=$(basename "$(dirname "$(dirname "$CLAUDE_CONFIG_DIR")")"); N2=$(basename "$(dirname "$CLAUDE_CONFIG_DIR")")
m() { sed "s#$N1#<n1>#g; s#$N2#<n2>#g; s#$HOME#<home>#g"; }
echo "== redact.py selftest"; python3 -I -B $D/redact.py selftest 2>&1 | tail -1 | m
V=( "\"installLocation\":\"<HOME>/sub/$N1/$N2/.claude/plugins/marketplaces/x\""        # V1 exactly the slipped shape
    "C:\\Users\\x\\sub\\$N1\\$N2\\.claude\\plugins\\marketplaces\\x"                     # V2 Windows backslashes
    "\"p\":\"C:\\\\Users\\\\x\\\\sub\\\\$N1\\\\$N2\\\\.claude\\\\plugins\\\\marketplaces\""  # V3 JSON-escaped backslashes
    "file:///Users/x/sub%2F$N1%2F$N2%2F.claude%2Fplugins%2Fmarketplaces%2Fx"            # V4 percent-encoded
    "$N1/$N2/.claude/plugins/marketplaces/x"                                             # V5 relative, STARTS with the name
    "\"cwd\":\"$N1/0_x/y\""                                                              # V6 relative, the name alone (no credentials component)
    "/sub/${N1:l}/${N2:u}/.claude/plugins/marketplaces/x"                               # V7 other case
    "-Users-x-sub-$N1-$N2--claude-plugins" )                                             # V8 slug
i=0; for v in "${V[@]}"; do i=$((i+1))
  r=$(python3 -I -B $D/redact.py scan <(printf '%s\n' "$v") | tail -1 | python3 -I -c 'import sys,ast; t=sys.stdin.read(); d=ast.literal_eval(t[t.index("{"):]); print("coordinator_name %d credentials_component %d" % (d["coordinator_name"], d["credentials_component"]))')
  s=$(python3 -I -B $D/scan_bytes.py --roots /nonexistent-root --names "$N1" "$N2" --control <(printf '%s\n' "$v") | grep CONTROL | python3 -I -c 'import sys,ast; t=sys.stdin.read(); d=ast.literal_eval(t[t.index("{"):]); print("name1 %d name2 %d forms %s" % (d.get("name1",0), d.get("name2",0), d.get("_forms")))')
  echo "V$i redact.py scan: $r || scan_bytes.py --names: $s"
done
