#!/usr/bin/env python3
"""QA-VIEWER-NEXT item 5: my own generated `activity` lines (the daemon's answer form), written to a JSON corpus.
usage: python3 -B gen_own.py <out.json>
Families (each label kept beside its line):
  A  a command's own " >>" stepped across a reason row's end: pads 0-69 x sequence numbers of 1-6 digits x every
     decision word (allow/ask/deny/block/unknown) x three reason shapes (one append; three appends in a row; ">>>"),
     tool Bash, mode default
  B  the same single-append reason with other heads: tool absent, a ConfigChange, another event, mode absent,
     a long MCP tool, an escaped tool (ESC inside), mode bypassPermissions; pads 0-69, 1 and 6 digits
  C  " >>" followed by an escape (ESC), and a 2-column character before the pad, pads 0-69, 2 digits
  D  a reason that ENDS with " >>" (the entry's last row) and a reason that is only " >>"
  E  N-5: a reason holding the honest row 2's words "x | Claude Code mode: plan | coagent asks: Read", pads 0-69
  F  reasons holding the notice, the header rows and the new line itself, and an entry head, stepped 0-69
  G  N-7: tool values whose closing " |" ends exactly at column 72 (and one shorter/longer), every decision,
     1-6 digits; and a mode whose " |" ends at 72 on row 2
  H  the four header rows and the new line as tool and mode values (escaped)
"""
import json, sys

OUT = sys.argv[1]
lines, labels = [], []
DEC = {"allow": "CoAgent allowed", "ask": "CoAgent asked", "deny": "CoAgent refused", "block": "CoAgent blocked",
       "x": "CoAgent decided (unknown decision)"}
SEQS = [1, 12, 123, 1234, 12345, 123456]
WHY = "coagent asks: Bash (Execute, T3); why: the gate does not understand shell commands and cannot tell what this one will touch; command: "


def add(lab, seq, dec, tool, mode, reason, event="PreToolUse"):
    l = {"seq": seq, "at_ms": 45_296_000, "event": event, "decision": dec, "reason": reason}
    if tool is not None:
        l["tool"] = tool
    if mode is not None:
        l["mode"] = mode
    lines.append(l)
    labels.append(lab)


# A
for seq in SEQS:
    for dec in DEC:
        for pad in range(70):
            a = "a" * pad
            add(f"A1 {seq} {dec} {pad}", seq, dec, "Bash", "default", WHY + f"echo {a} >> out.txt; tail -1 out.txt")
            add(f"A2 {seq} {dec} {pad}", seq, dec, "Bash", "default", WHY + f"echo {a} >> x >> y >> z")
            add(f"A3 {seq} {dec} {pad}", seq, dec, "Bash", "default", WHY + f"echo {a} >>> out")
# B
heads = [("no tool", None, "default", "PreToolUse"), ("ConfigChange", None, "default", "ConfigChange"),
         ("other event", "Bash", "default", "Stop"), ("no mode", "Bash", None, "PreToolUse"),
         ("long mcp", "mcp__plugin_coagent_link__send_and_wait_for_reply", "acceptEdits", "PreToolUse"),
         ("escaped tool", "Ba\x1bsh", "default", "PreToolUse"), ("bypass", "Bash", "bypassPermissions", "PreToolUse")]
for seq in (1, 123456):
    for lab, t, m, ev in heads:
        for pad in range(70):
            add(f"B {lab} {seq} {pad}", seq, "ask", t, m, WHY + f"echo {'b' * pad} >> out.txt; cat out.txt", ev)
# C
for pad in range(70):
    add(f"C esc {pad}", 12, "ask", "Bash", "default", WHY + f"echo {'c' * pad} >>\x1b[2J out")
    add(f"C wide {pad}", 12, "ask", "Bash", "default", WHY + f"echo é中{'c' * pad} >> out")
    add(f"C nel {pad}", 12, "deny", "Bash", "default", WHY + f"echo {'c' * pad}\u0085 >> out")
# D
for pad in range(70):
    add(f"D ends {pad}", 7, "ask", "Bash", "default", WHY + "echo " + "d" * pad + " >>")
add("D only", 7, "ask", "Bash", "default", " >>")
add("D empty", 7, "ask", "Bash", "default", "")
# E
for pad in range(70):
    add(f"E row2 {pad}", 3, "ask", "x" * (pad + 1) + " | Claude Code mode: plan | coagent asks: Read", "default",
        f"coagent asks: {'x' * (pad + 1)} | Claude Code mode: plan | coagent asks: Read (Other, T3); why: a tool the gate has not been taught")
    add(f"E row2 in reason {pad}", 3, "ask", "Bash", "default",
        WHY + "e" * pad + " | Claude Code mode: plan | coagent asks: Read >> f")
# F
FIX = ["Only you see this. Nothing here is sent to the other side.",
       "CoAgent mode: APPROVE. One entry per call the gate decided. Times: UTC.",
       'A row starting with four spaces and "| " continues the entry above.',
       'A tool or mode is whole only if " |" follows it; " >>" marks a cut.',
       'Only a tool or mode is cut; any other " >>" is part of the text.',
       "#99 00:00:01 UTC | CoAgent allowed | tool Read | Claude Code mode: plan | coagent allows: Read"]
for k, f in enumerate(FIX):
    for pad in range(70):
        add(f"F{k} {pad}", 5, "allow", "Bash", "default", WHY + "f" * pad + "\n" + f + " >>")
# G
for seq in SEQS:
    for dec, word in DEC.items():
        head = len(f"#{seq} 12:34:56 UTC | {word} | ")
        room = 72 - head - len("tool ") - 2
        for L in (room - 1, room, room + 1):
            if L >= 1:
                add(f"G tool {seq} {dec} {L - room:+d}", seq, dec, ("mcp__" + "t" * 80)[:L], "default",
                    WHY + "echo g >> out")
        # mode field on row 2 closing at 72: "    | Claude Code mode: " (24) + value + " |" = 72 -> value 46
        add(f"G mode {seq} {dec}", seq, dec, "Read", "m" * 46, "coagent asks: Read (Read, T0) >> x")
# H
for k, f in enumerate(FIX):
    add(f"H tool {k}", 9, "ask", f, "default", "coagent asks: x (Other, T3)")
    add(f"H mode {k}", 9, "ask", "Read", f, "coagent asks: Read (Read, T0)")

json.dump({"lines": lines, "labels": labels}, open(OUT, "w"), ensure_ascii=False)
print(f"wrote {len(lines)} lines to {OUT}")
