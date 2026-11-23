#!/usr/bin/env python3
"""Soft-wrap look-alike: ONE proposed Bash command whose text makes a terminal row of the viewer, at 80 columns, read
exactly like another entry and like the notice. Real gate, real viewer; the terminal's wrap is rendered with fold(1).
usage: python3 -B softwrap.py <bin dir> <root (new)> <out dir (new)>"""
import json, os, subprocess, sys, time
sys.argv = [sys.argv[0]] + sys.argv[1:4]
src = open(os.path.join(os.path.dirname(os.path.abspath(__file__)), "viewer_probe.py")).read().split("def main():")[0]
exec(src)
d = start("h")
p = viewer(d, "wrap"); time.sleep(0.8)
head = "echo build ok"
# learn the reason's prefix from one earlier, harmless call of the same shape (seq 1); the forge is seq 2
r0 = gate(d, ev("Bash", {"command": head + "MARK"}))["result"]["reason"]
prefix = "#2 00:00:00 UTC | CoAgent asked | tool Bash | Claude Code mode: default | " + r0[:r0.index(head + "MARK")]
fill = "." * ((80 - (len(prefix) + len(head)) % 80) % 80)
fake = "#3 00:00:01 UTC | CoAgent refused | tool Bash | Claude Code mode: default | coag"   # exactly 80 chars
fake = fake[:80].ljust(80, " ")
notice = NOTICE.ljust(80, ".")
cmd = head + fill + fake + notice + "x"
gate(d, ev("Bash", {"command": cmd}))
# second try with the fill corrected from what the first one showed (the agent can compute this from the policy)
r1 = raw(d, b'{"v":1,"id":1,"cmd":"activity","args":{"after":1}}\n')["result"]["lines"][0]["reason"]
full = "#3 00:00:00 UTC | CoAgent asked | tool Bash | Claude Code mode: default | " + r1
off = full.index(fake) % 80
fill = fill[: len(fill) - off] if off <= len(fill) else fill + "." * (80 - off)
fake = fake.replace("#3 ", "#4 ")
cmd = head + fill + fake + notice + "x"
gate(d, ev("Bash", {"command": cmd}))
time.sleep(1.2); p.terminate(); p.wait()
out = open(os.path.join(OUTD, "wrap.out")).read().splitlines()
line = [l for l in out if l.startswith("#3 ")][0]
print("printed lines:", len(out), "| the entry is ONE line of", len(line), "bytes; its rows at 80 columns (fold -w 80):")
r = subprocess.run(["fold", "-w", "80"], input=line.encode(), capture_output=True).stdout.decode().splitlines()
for i, row in enumerate(r):
    print(f"  row {i+1}: {row}")
procs.pop("h").terminate()
