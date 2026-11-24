#!/usr/bin/env python3
"""QA-DAEMON-NOTES item 9: produce the 'killed after the 5 s wait' diagnosis line: the guard is stopped
(SIGSTOP) when the daemon is told to stop. Usage: python3 -B qa_guard_killed.py <bin dir> <work dir (new)>"""
import os, signal, sys, time
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from qa_lib import Q, alive
q = Q(sys.argv[1], sys.argv[2])
try:
    q.start("a")
    assert q.ctl("a", "invite", {})["ok"] is True
    rel = q.status("a")["relay"]
    os.kill(rel["guard_pid"], signal.SIGSTOP)
    t0 = time.time()
    code = q.stop("a")
    print(f"daemon exit {code} after {time.time()-t0:.1f}s; guard alive {alive(rel['guard_pid'])}; relay alive {alive(rel['relay_pid'])} (an orphan relay is the pre-existing path when the guard is killed)")
    for l in q.stderr("a").splitlines():
        if "relay guard" in l or "stop not confirmed" in l or "relay child stopped" in l:
            print("LINE: " + l)
finally:
    print("cleanup killed:", q.cleanup())
