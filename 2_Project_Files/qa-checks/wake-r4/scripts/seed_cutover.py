# seed_cutover.py — what the cut-over's FIRST handover write needs, on a scratch copy of the real pickup (the real tree is read only).
import os, re, subprocess, sys
sys.path.insert(0, os.path.join(os.path.dirname(os.path.abspath(__file__)), "r3_copies"))
from qlib import *
r = mk_real("seed", "seed_%d" % os.getpid())
rc, o, e = ho(r, "seed", "--from-legacy")
blk_ = o.encode("utf-8")
print("dry seed on a scratch copy of the real NEXT-PICKUP.md (%d bytes): rc %d; block %d bytes; cap 10000; over by %d; files written: %s"
      % (os.path.getsize(os.path.join(T(r), "NEXT-PICKUP.md")), rc, len(blk_), len(blk_) - 10000, sorted(f for f in os.listdir(T(r)) if f.startswith("STATE"))))
for l in e.split("\n"):
    if re.search(r"WOULD BE REFUSED|the block is \d+ bytes|standing section|-> (FLOOR|FIRST WORK|OWED|OPEN CARDS|GRANTS IN PLAY)|none stated", l): print("    " + l.strip()[:260])
parts = re.split(r"(?m)^(?=## )", o)
print("parts of the seeded block: %s" % ", ".join("%s %d B" % (p.split("\n")[0][3:], len(p.encode())) for p in parts if p.startswith("## ")))
print("GRANTS IN PLAY as seeded: %r" % [p for p in parts if p.startswith("## GRANTS IN PLAY")][0][:120])
rc2, o2, e2 = ho(r, "seed", "--from-legacy", "--run")
print("seed --run: rc %d; state file written: %s | %s" % (rc2, os.path.exists(st(r)), e2.strip().split("\n")[0][:150]))
if len(blk_) > 10000:
    # the tempting shortcut: raise the cap for this one write
    rc3, o3, e3 = ho(r, "write", "--stdin", data=blk_, env={"HANDOVER_CAP_BYTES": "12000", "HANDOVER_ALLOW_XCLOCK": "seeded verbatim from the legacy pickup"})
    print("the shortcut, HANDOVER_CAP_BYTES=12000 for this one write: rc %d; state written %s | %s" % (rc3, os.path.exists(st(r)), (e3.strip().split("\n")[0] if rc3 else o3.strip().split("\n")[-1])[:160]))
    rc4, o4, e4 = ho(r, "check"); print("  then `handover.sh check` with the default cap (as doctor runs it): rc %d | %s" % (rc4, o4.strip().split("\n")[0][:200]))
    rc5, o5, e5 = wp(r, "--today", "2026-11-27"); print("  then the pack build with the default cap (as the launcher runs it): rc %d | %s" % (rc5, (e5.strip().split("\n")[-1] or o5)[:260]))
    r2 = mk_real("seed_cut", "seed_%d" % os.getpid())
    lines = o.split("\n")
    # a hand cut of the kind a seat would make: drop whole lines from the END of the largest part until the block fits, and fill GRANTS IN PLAY
    cut = blk_
    big = max((p for p in parts if p.startswith("## ")), key=lambda p: len(p.encode()))
    bl = big.rstrip("\n").split("\n")
    while len(cut) > 9900 and len(bl) > 2:
        bl.pop(); cut = o.replace(big, "\n".join(bl) + "\n- (cut by hand at the cut-over: the rest is in the legacy pickup)\n\n").encode("utf-8")
    cut = cut.replace(b"- none stated in the legacy block", b"- (filled by hand at the cut-over from the pack's part d)")
    rc6, o6, e6 = ho(r2, "write", "--stdin", data=cut, env={"HANDOVER_ALLOW_XCLOCK": "seeded verbatim from the legacy pickup"})
    rc7, o7, e7 = ho(r2, "check"); rc8, o8, e8 = wp(r2, "--today", "2026-11-27")
    print("a block cut by hand to %d bytes and written with write --stdin: rc %d %s; check rc %d; pack build rc %d (%s)" % (len(cut), rc6, (e6.strip().split("\n")[0][:200] if rc6 else ""), rc7, rc8, "state: STATE file" in o8))
