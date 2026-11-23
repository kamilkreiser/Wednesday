#!/usr/bin/env python3
"""R2: the `start` field of every `activity` answer: present, 32 lowercase hex, the same across one daemon run
(pages, after values, error-free argument shapes), different after a restart; absent from gate_off and bad_args
answers and from `status`. usage: python3 -B ipc_start.py <bin dir> <root (new, short)>"""
import json, os, re, sys, time
HERE = os.path.dirname(os.path.abspath(__file__))
sys.argv = [sys.argv[0], sys.argv[1], sys.argv[2], sys.argv[2] + "_out"]
exec(open(os.path.join(HERE, "forge2.py")).read().split("\ndef aim(")[0])
d = start("h")
for i in range(70):
    hook(d, ev("Read", {"file_path": f"{WS}/f{i}"}))
seen = set(); n = 0
for after in [0, 1, 5, 63, 64, 69, 70, 71, 10**6, 18446744073709551615]:
    r = raw(d, (json.dumps({"v": 1, "id": 1, "cmd": "activity", "args": {"after": after}}) + "\n").encode())
    seen.add(r["result"]["start"]); n += 1
lines, last = all_lines(d); seen.add(last["start"]); n += 1
bad = raw(d, b'{"v":1,"id":1,"cmd":"activity","args":{"after":-1}}\n')
st = raw(d, b'{"v":1,"id":1,"cmd":"status"}\n')
s1 = seen.pop() if len(seen) == 1 else None
print("answers", n, "one start value across them:", s1 is not None, "| 32 lowercase hex:", bool(s1 and re.fullmatch(r"[0-9a-f]{32}", s1)))
print("bad_args answer holds it:", s1 in json.dumps(bad), "| status holds it:", s1 in json.dumps(st))
procs.pop("h").kill(); time.sleep(0.1); start("h", d)
r2 = raw(d, b'{"v":1,"id":1,"cmd":"activity","args":{"after":0}}\n')["result"]["start"]
print("after a restart on the same data dir: another value:", r2 != s1)
procs.pop("h").terminate()
for f in os.listdir(d):
    p = os.path.join(d, f)
    if os.path.isfile(p):
        print("  file", f, "holds a start value:", s1.encode() in open(p, "rb").read() or r2.encode() in open(p, "rb").read())
