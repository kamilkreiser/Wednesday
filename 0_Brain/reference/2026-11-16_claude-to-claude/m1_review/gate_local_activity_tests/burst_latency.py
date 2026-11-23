#!/usr/bin/env python3
"""Gate latency through the REAL hook while 50 local clients hammer `activity {after:0}` on a record full of large lines.
usage: python3 -B burst_latency.py <bin dir> <root (new)>"""
import json, os, subprocess, sys, threading, time
sys.argv = [sys.argv[0], sys.argv[1], sys.argv[2], os.path.join(sys.argv[2] + "_out.txt")]
exec(open(os.path.join(os.path.dirname(os.path.abspath(__file__)), "ipc_probe.py")).read().split("def main():")[0])
d = start("h", True)
big = " ".join(f"/tmp/w{i:02d}" + "q" * 1790 for i in range(34))
for i in range(80):
    gate(d, bash(f"ls n{i} " + big))
def hook_time(n):
    t0 = time.time()
    p = subprocess.run([f"{BIN}/coagent-hook", "--data-dir", d], env={"PATH": "/usr/bin:/bin"}, input=json.dumps(bash(f"echo lat{n}")).encode(), capture_output=True)
    return time.time() - t0, p.returncode
base = [hook_time(i)[0] for i in range(10)]
stopf = threading.Event()
def hammer():
    while not stopf.is_set():
        try: req(d, "activity", {"after": 0})
        except Exception: pass
ths = [threading.Thread(target=hammer) for _ in range(50)]; [t.start() for t in ths]
time.sleep(1)
lat = [hook_time(100 + i) for i in range(20)]
stopf.set(); [t.join() for t in ths]
say(f"hook latency idle: max {max(base):.2f}s; under 50 activity hammer clients: max {max(l[0] for l in lat):.2f}s median {sorted(l[0] for l in lat)[10]:.2f}s; exit codes {sorted(set(l[1] for l in lat))}")
stop("h")
