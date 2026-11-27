#!/usr/bin/env python3
# S3_my_scan.py — third checker's own NAMES-ONLY look at the saved real dry list (logs/<seat>/<stamp>_dry_*.files0). Opens no file
# on the drive. (1) what nb_core.secret_shape of the scratch copy says about every component (must be 0: a planned path the tool's
# own rule would exclude); (2) names the folder rule's look-alikes would miss; (3) case-fold twins the tool's ckey does not see
# (dotless i, long s) and trailing dot/space names, which an SMB share may fold; (4) other seats' and the other client's names.
import glob, os, re, sys, unicodedata, collections
logs, stamp, lane = sys.argv[1], sys.argv[2], sys.argv[3]
sys.path.insert(0, lane); import nb_core
tot = own = 0; look = collections.Counter(); odd = collections.Counter(); seat = collections.Counter(); keys = {}
twins = 0
for f in sorted(glob.glob(os.path.join(logs, "%s_dry_*.files0" % stamp))):
    setname = os.path.basename(f)[len(stamp) + 5:-7]
    for d in open(f, "rb").read().split(b"\0"):
        if not d: continue
        p = d.decode("utf-8", "replace"); tot += 1
        comps = p.split("/")
        if any(nb_core.secret_shape(c) for c in comps): own += 1
        for c in comps:
            k = unicodedata.normalize("NFKC", c).casefold().replace("​", "")
            if ("4_credentials" in k or "3_access_keys" in k): look[c] += 1
            if re.search(r"4[\W_]?cred|3[\W_]?access[\W_]?key", k): look["(loose) " + c] += 1
        last = comps[-1]
        if last.endswith(".") or last.endswith(" "): odd["trailing dot or space"] += 1
        if any(ord(ch) < 32 for ch in p): odd["control character"] += 1
        if "ı" in p or "ſ" in p or "İ" in p: odd["dotless i / long s / dotted I"] += 1
        if unicodedata.normalize("NFC", p) != p: odd["not NFC"] += 1
        for c in comps:
            lc = c.lower()
            if "tuesday" in lc or "friday" in lc: seat["tuesday/friday in a component (%s)" % ("seat tree set" if setname == "WEDNESDAY" else "project set")] += 1
            if "datasec" in lc: seat["datasec in a component"] += 1
        up = (setname, unicodedata.normalize("NFC", p).upper())
        if up in keys and keys[up] != nb_core.ckey(p): twins += 1
        keys.setdefault(up, nb_core.ckey(p))
print("paths read: %d (control: must be about 1.1 million)" % tot)
print("planned paths with a component the tool's OWN secret_shape excludes: %d" % own)
print("components that are 4_Credentials/3_Access_Keys after NFKC+casefold (look-alikes the lower() rule could miss): %d %s" % (sum(v for k, v in look.items() if not k.startswith("(loose)")), dict(look.most_common(6))))
print("names an SMB share may treat differently:", dict(odd))
print("upper-case twins that the tool's case-fold key does not see as a clash: %d" % twins)
print("seat and client words:", dict(seat))
print("CONTROL: paths ending .md: %d ; paths with 'credential' anywhere (not excluded shapes, e.g. credentials.ts): %d" % (sum(1 for k in keys if k[1].endswith(".MD")), sum(1 for k in keys if "CREDENTIAL" in k[1])))
