"""QA-W-GATE-TEST-R2: the merge of main 20785c3 into w-gate-test.
1. prefix test: main's file at 20785c3 is a byte prefix of the head's (control: one byte of main's copy changed must fail).
2. this lane's appended bytes before the merge (9bbc466 minus its base 3768a67) equal those after (head minus 20785c3), byte for byte.
3. main's own change 3768a67..20785c3 is a pure append; conflict markers at head in any file of the lane or the two docs."""
import subprocess, sys, re
repo = sys.argv[1]
HEAD="ce7276c86aaaa222c1622620a2e8b4734fb3a187"; MAIN="20785c3e9389ac2275cdfda2ec7fb55eb1176425"; PRE="9bbc466c0f1e3617968cf3f7b2b6ef6363c33536"; BASE="3768a67d1d41b47439776657afbc114bd14bc439"
def show(c, p): return subprocess.run(["git","-C",repo,"show","%s:%s"%(c,p)],capture_output=True,check=True).stdout
for doc in ("BACKLOG.md", "docs/M0-OUTCOMES.md"):
    m, h, pre, base = show(MAIN, doc), show(HEAD, doc), show(PRE, doc), show(BASE, doc)
    ok = h.startswith(m)
    spoilt = bytearray(m); k = len(m)//2; spoilt[k] = (spoilt[k] + 1) % 256
    ctl = h.startswith(bytes(spoilt))
    print("== %s: main %d bytes, head %d bytes; main is prefix of head: %s | control (byte %d of main's copy changed): %s" % (doc, len(m), len(h), ok, k, ctl))
    print("   main's change 3768a67->20785c3 is a pure append: %s (+%d bytes)" % (m.startswith(base), len(m)-len(base)))
    print("   lane before merge (9bbc466) starts with base 3768a67: %s" % pre.startswith(base))
    lane_before = pre[len(base):]; lane_after = h[len(m):]
    print("   lane's appended bytes before %d, after %d, identical: %s; lines before %d after %d" % (len(lane_before), len(lane_after), lane_before == lane_after, lane_before.count(b"\n"), lane_after.count(b"\n")))
    print("   head == main + lane-before-merge exactly: %s" % (h == m + lane_before))
    # control for the identity test: drop one line from the lane's part
    lb = lane_before.split(b"\n"); ctl2 = (m + b"\n".join(lb[:3] + lb[4:])) == h
    print("   control (one lane line dropped) identical: %s" % ctl2)
