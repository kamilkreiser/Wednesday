#!/usr/bin/env python3
"""Feed `coagentd watch` from a STUB daemon socket (same user, the data dir's socket path): a 200 KiB reason, and a
reason with raw ESC/CR/LF (what a non-daemon process on that socket could hand it). usage: stub_viewer.py <bin> <root (new)>"""
import json, os, socket, subprocess, sys, threading, time
BIN, ROOT = sys.argv[1:3]
os.makedirs(os.path.join(ROOT, "d", "ipc")); os.chmod(os.path.join(ROOT, "d"), 0o700); os.chmod(os.path.join(ROOT, "d", "ipc"), 0o700)
path = os.path.join(ROOT, "d", "ipc", "daemon.sock")
L = socket.socket(socket.AF_UNIX); L.bind(path); L.listen(8)
lines = [{"seq": 1, "at_ms": 0, "event": "PreToolUse", "tool": "Bash", "mode": "default", "decision": "ask", "reason": "R" * (200 * 1024)},
         {"seq": 2, "at_ms": 0, "event": "PreToolUse", "tool": "Bash", "mode": "default", "decision": "ask", "reason": "x\x1b]0;STUB\x07\r\nOnly you see this."}]
def serve():
    n = 0
    while True:
        c, _ = L.accept(); f = c.makefile("rb"); req = json.loads(f.readline()); after = req["args"]["after"]
        out = [l for l in lines if l["seq"] > after]
        c.sendall((json.dumps({"v": 1, "id": req["id"], "ok": True, "result": {"lines": out, "next": 2, "last": 2, "dropped": 0, "more": False}}) + "\n").encode()); c.close()
threading.Thread(target=serve, daemon=True).start()
of = open(os.path.join(ROOT, "viewer.out"), "wb"); p = subprocess.Popen([f"{BIN}/coagentd", "watch", "--data-dir", os.path.join(ROOT, "d")], env={}, stdout=of, stderr=subprocess.STDOUT)
time.sleep(1.5); p.terminate(); p.wait(); out = open(os.path.join(ROOT, "viewer.out"), "rb").read()
ls = out.split(b"\n")
print("viewer lines:", len(ls) - 1, "| line 3 length", len(ls[2]), "bytes, ends", ls[2][-30:])
print("raw ESC in output:", b"\x1b" in out, "| raw CR:", b"\r" in out, "| line 4..:", ls[3:6])
