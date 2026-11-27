# seed_cap_trap.py — if the seeded block IS over the cap on the day: what happens when the cap is raised for that one write?
import os, sys
sys.path.insert(0, os.path.join(os.path.dirname(os.path.abspath(__file__)), "r3_copies"))
from qlib import *
r = mk_real("trap", "seedtrap_%d" % os.getpid())
b = blk("OVERCAP", 10086 - len(blk("OVERCAP")))
print("a %d-byte block (86 over the cap, the size the build seat measured at 17:00)" % len(b))
rc, o, e = ho(r, "write", "--stdin", data=b); print("- written with the default cap: rc %d | %s" % (rc, e.strip().split("\n")[1][:150] if rc else ""))
rc, o, e = ho(r, "write", "--stdin", data=b, env={"HANDOVER_CAP_BYTES": "12000"}); print("- written with HANDOVER_CAP_BYTES=12000 for this one call: rc %d; state file there: %s" % (rc, os.path.exists(st(r))))
rc, o, e = ho(r, "check"); print("- `handover.sh check` afterwards, default cap (as doctor runs it): rc %d | %s" % (rc, o.strip().split("\n")[0][:170]))
rc, o, e = wp(r, "--today", "2026-11-27"); print("- the pack build afterwards, default cap (as the launcher runs it): rc %d; pack written: %s | %s" % (rc, os.path.exists(os.path.join(r, "0_Brain/wake/WAKE-wednesday.md")), e.strip().split("\n")[-1][:230]))
rc, o, e = wp(r, "--today", "2026-11-27", env={"HANDOVER_CAP_BYTES": "12000"}); print("- control: the same build with the same raised cap in its environment: rc %d" % rc)
