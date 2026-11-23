#!/usr/bin/env python3
"""QA-ALLOW-MEASURE-R2: is the hook's reason marker in the Write ask dialog? Searches the WHOLE pane byte capture
(escape sequences and all whitespace removed) and every frame. The Bash dialog is the positive control of the search.
usage: m8_marker_bytes.py <raw/M8-fresh-ask dir> [marker]"""
import re, sys, os
d = sys.argv[1]; mk = sys.argv[2] if len(sys.argv) > 2 else "M8ASK"
b = open(os.path.join(d, "pane.bytes"), "rb").read().decode("utf-8", "replace")
noesc = re.sub(r"\x1b\][^\x07\x1b]*(\x07|\x1b\\)", "", b)        # OSC
noesc = re.sub(r"\x1b\[[0-9;?<>=]*[ -/]*[@-~]", "", noesc)         # CSI
noesc = re.sub(r"\x1b[@-_]", "", noesc)
flat = re.sub(r"\s+", "", noesc)
def pos(s): return [m.start() for m in re.finditer(re.escape(s), flat)]
wq = pos("DoyouwanttocreateW8.txt"); bq = pos("Doyouwanttoproceed"); bprompt = pos("echoM8-BASH-RAN>B8.txt")
mks = pos(mk)
print("pane.bytes: %d bytes; flattened %d chars" % (len(b), len(flat)))
print("'Do you want to create W8.txt' at", wq); print("'Do you want to proceed' at", bq)
print("first Bash prompt text at", bprompt[:1]); print("marker %s at" % mk, mks)
cut = bprompt[0] if bprompt else len(flat)
print("RESULT Write segment (before the Bash prompt was typed): marker count =", sum(1 for p in mks if p < cut),
      "| 'Do you want to create' count =", sum(1 for p in wq if p < cut))
print("RESULT Bash segment (control): marker count =", sum(1 for p in mks if p >= cut), "| 'Do you want to proceed' count =", len(bq))
# also the reason's other words in the Write segment, and the 'requires confirmation' phrase
for w in ("coagentasks", "requiresconfirmation", "ALLOW-MEASUREstub", "HookPreToolUse:Write"):
    ps = pos(w); print("  %-24s Write-seg %d  Bash-seg %d" % (w, sum(1 for p in ps if p < cut), sum(1 for p in ps if p >= cut)))
# frames
fr = open(os.path.join(d, "frames.txt"), encoding="utf-8", errors="replace").read().split("=== FRAME ")[1:]
wd = [i for i, f in enumerate(fr) if "Do you want to create" in f]; bd = [i for i, f in enumerate(fr) if "Do you want to proceed" in f]
print("frames: %d; Write-dialog frames %d (marker in %d); Bash-dialog frames %d (marker in %d)" % (
    len(fr), len(wd), sum(mk in fr[i] for i in wd), len(bd), sum(mk in fr[i] for i in bd)))
first = next((i for i, f in enumerate(fr) if mk in f), None)
print("first frame with the marker:", first, (fr[first].splitlines()[0] if first is not None else ""))
print("frame header of the last Write-dialog frame:", fr[wd[-1]].splitlines()[0] if wd else None)
