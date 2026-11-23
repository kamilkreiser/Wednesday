#!/usr/bin/env python3
"""QA-ALLOW-MEASURE-R2 item 6: analysis of my own run. Whole pane byte stream (escapes and whitespace removed), split at
the moment the Bash prompt was typed: is the hook's marker in the Write segment (the Write dialog) and in the Bash segment
(control of the search)? Plus frames with each dialog and the marker.   usage: qa2_repro_analyse.py <run dir> <marker>"""
import os, re, sys
d, mk = sys.argv[1], sys.argv[2]
b = open(os.path.join(d, "pane.bytes"), "rb").read().decode("utf-8", "replace")
x = re.sub(r"\x1b\][^\x07\x1b]*(\x07|\x1b\\)", "", b); x = re.sub(r"\x1b\[[0-9;?<>=]*[ -/]*[@-~]", "", x); x = re.sub(r"\x1b[@-_]", "", x)
flat = re.sub(r"\s+", "", x)
P = lambda s: [m.start() for m in re.finditer(re.escape(s), flat)]
cut = (P("echoQA2-BASH-RAN>QB8.txtIfrefused") or [len(flat)])[0]
print("pane.bytes %d bytes" % os.path.getsize(os.path.join(d, "pane.bytes")))
for w in ("DoyouwanttocreateQW8.txt", "Doyouwanttoproceed", mk, "coagentasks", "requiresconfirmation", "HookPreToolUse:Write", "HookPreToolUse:Bash"):
    ps = P(w); print("  %-26s Write segment %d | Bash segment %d" % (w, sum(p < cut for p in ps), sum(p >= cut for p in ps)))
fr = open(os.path.join(d, "frames.txt"), encoding="utf-8", errors="replace").read().split("=== FRAME ")[1:]
wd = [f for f in fr if "Do you want to create QW8.txt" in f]; bd = [f for f in fr if "Do you want to proceed" in f]
print("frames %d; Write-dialog frames %d (marker in %d); Bash-dialog frames %d (marker in %d)" % (len(fr), len(wd), sum(mk in f for f in wd), len(bd), sum(mk in f for f in bd)))
