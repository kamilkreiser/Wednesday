"""(d) S-6: what a daemon built with AW-7's red variant answers right after a seal that erred.
Usage: qa_aw7probe.py <bin of the red build> <work dir new> <tries>"""
import json, os, subprocess, sys, time
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from qa_lib import Q, alive
BIN, ROOT, N = sys.argv[1], sys.argv[2], int(sys.argv[3])
os.makedirs(ROOT)
for i in range(N):
    q = Q(BIN, os.path.join(ROOT, f"r{i}"))
    try:
        p = q.start("a", ["--audit"]); q.start("b"); q.pair("a", "b")
        sid = q.status("a")["session"]["session_id"]
        q.ctl("a", "send", {"kind": "chat", "text": "AW7 probe"})
        arc = os.path.join(q.dir("a"), "audit", sid, "archive")
        os.chmod(arc, 0o500)
        s = q.ctl("a", "audit_seal", {})
        t0 = time.time()
        st = q.ctl_raw("a", {"v": 1, "id": 7, "cmd": "status", "args": {}})
        t1 = time.time()
        al = p.poll() is None
        ib = q.ctl_raw("a", {"v": 1, "id": 8, "cmd": "inbox_read", "args": {}})
        os.chmod(arc, 0o700)
        print(f"try {i}: seal row {s['result']['row']!r}; status answer after {t1-t0:.2f}s: "
              f"{'None' if st is None else json.dumps(st)[:160]}; alive {al}; inbox_read: {'None' if ib is None else json.dumps(ib)[:100]}; exit {p.poll()}")
    finally:
        q.cleanup()
