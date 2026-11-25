#!/usr/bin/env python3
"""QA-AUDIT-WIRE exploratory: head, convener with --audit, joiner without. Prints every answer.
Usage: python3 -B qa_basic.py <bin dir> <work dir (new)>"""
import json, os, sys, time
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from qa_lib import Q

q = Q(sys.argv[1], sys.argv[2])


def show(tag, v):
    print(tag, json.dumps(v, sort_keys=True))


try:
    q.start("a", ["--audit"])
    q.start("b")
    show("status a idle", q.status("a").get("audit"))
    show("seal idle", q.ctl("a", "audit_seal"))
    q.pair("a", "b")
    st = q.status("a")
    show("status a paired", st.get("audit"))
    show("send chat", q.ctl("a", "send", {"kind": "chat", "text": "hello one"}))
    show("send request", q.ctl("a", "send", {"kind": "request", "text": "do two"}))
    show("seal 1", q.ctl("a", "audit_seal"))
    show("seal 2", q.ctl("a", "audit_seal"))
    show("seal args", q.ctl("a", "audit_seal", {}))
    show("status a", q.status("a").get("audit"))
    for root, ds, fs in os.walk(q.dir("a")):
        for f in fs:
            p = os.path.join(root, f)
            print("FILE", os.path.relpath(p, q.dir("a")), oct(os.stat(p).st_mode & 0o777), os.path.getsize(p))
        for d in ds:
            p = os.path.join(root, d)
            print("DIR ", os.path.relpath(p, q.dir("a")), oct(os.stat(p).st_mode & 0o777))
    time.sleep(1)
    show("b inbox", q.ctl("b", "inbox_read"))
finally:
    print("left", q.cleanup())
print("STDERR a:\n" + q.stderr("a"))
