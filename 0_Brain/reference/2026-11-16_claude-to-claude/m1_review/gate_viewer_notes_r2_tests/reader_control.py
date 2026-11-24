"""Control: the reader (m2.reader) must FLAG the first check's MJ-1 rows when given the ROUND-1 layout (the first
check's own model of b898a7c, taken from vn_first.py), and pass the honest twin. usage: python3 -B reader_control.py"""
import os, sys
S = os.path.dirname(os.path.abspath(__file__)); sys.path.insert(0, S)
import m2
src = open(os.path.join(S, "vn_first.py")).read()
code = src.split("def guard(s):")[1].split("# ---------------------------------------------------------------- inputs")[0]
ns = {}
exec("import unicodedata\nMARK='    | '\nWIDTH=72\nINVIS=[]\ndef guard(s):" + code, ns)
cases = [(1, "Read", "default | Claude Code mode: plan"), (2, "Read", "default"), (3, "Read", "auto | Claude Code mode: plan"),
         (4, "Read", "plan\U0010fffd"), (5, "mcp__plugin_coagent_link__send | CoAgent allowed", "default"),
         (7, "mcp__github__list_issues\U0010fffd", "default"), (12, "Read", "default | Claude Code mode: plan")]
for seq, t, m in cases:
    l = {"seq": seq, "at_ms": 0, "event": "PreToolUse", "tool": t, "mode": m, "decision": "ask", "reason": "coagent asks: x (Other, T3)"}
    old = ns["wrap"](ns["render"](l))
    new = m2.rows_of(l)
    print(f"#{seq} round-1 first row {old[0]!r}\n      reader: {m2.reader(old)[0]}\n   head first row {new[0]!r}\n      reader: {m2.reader(new)[0]}")
