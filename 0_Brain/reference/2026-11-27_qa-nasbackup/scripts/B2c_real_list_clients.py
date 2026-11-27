#!/usr/bin/env python3
# B2c — names only, from the seat's real dry-run lists: what client projects sit inside the "general" sets?
# (Datasec projects named in the workspace CLAUDE.md: NexusAI, Vision Sales Portal, myPKI, CypherKey/OTP, Lead_Bot,
#  Task_Dispatcher, Feedback_System, Marketing_Collateral, Websites.)
import glob, os, re, collections
logs = "/Volumes/DevMASTER/WEDNESDAY/2_Project_Files/nas-backup/logs/wednesday"
rx = re.compile(r"(?i)(nexus-?ai|vision[-_ ]?sales|sales[-_ ]?portal|mypki|cypherkey|lead[-_ ]?bot|task[-_ ]?dispatcher|feedback[-_ ]?system|marketing[-_ ]?collateral|hpsm)")
tot = 0
for f in sorted(glob.glob(os.path.join(logs, "*_dry_*.files0"))):
    s = os.path.basename(f).split("_dry_", 1)[1][:-7]
    names = [d.decode("utf-8", "replace") for d in open(f, "rb").read().split(b"\0") if d]
    tot += len(names)
    c = collections.Counter(); ex = {}
    for n in names:
        m = rx.search(n)
        if m:
            k = m.group(1).lower(); c[k] += 1; ex.setdefault(k, n)
    if s.endswith("Testing Agent MAIN"):
        p = collections.Counter(n.split("/")[1] for n in names if n.startswith("projects/") and n.count("/") >= 1)
        print("Testing Agent MAIN, paths per projects/<name>: %s" % dict(p.most_common(20)))
    if c:
        print("SET %-32s %s" % (s, dict(c)))
        for k in c: print("      e.g. %s" % ex[k][:170])
print("paths read:", tot)
