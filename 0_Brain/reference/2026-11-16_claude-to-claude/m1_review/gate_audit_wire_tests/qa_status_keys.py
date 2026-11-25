#!/usr/bin/env python3
"""QA-DAEMON-NOTES: every key path of `status` (host and guest) in five states, for one build.
Usage: python3 -B qa_status_keys.py <bin dir> <work dir (new)> > keys.txt   (diff two builds' outputs)"""
import os, sys, time
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from qa_lib import Q, keypaths

q = Q(sys.argv[1], sys.argv[2])
out = []


def dump(state, name):
    for k in sorted(keypaths(q.status(name))):
        out.append(f"{state}\t{name}\t{k}")


try:
    q.start("a", ["--keep-relay-identity"])
    q.start("b")
    dump("1-idle", "a")
    r = q.ctl("a", "invite", {})
    q.status("a")
    dump("2-invite-waiting", "a")
    j = q.ctl("b", "join", {"blob": r["result"]["line"]})
    q.wait_connected("a", "b")
    dump("3-connected", "a")
    dump("3-connected", "b")
    q.crash("a")
    time.sleep(4)
    dump("4-host-down", "b")
    q.start("a", ["--keep-relay-identity"])
    q.wait_connected("a", "b", 120)
    dump("5-host-back", "a")
    dump("5-host-back", "b")
finally:
    q.cleanup()
print("\n".join(out))
