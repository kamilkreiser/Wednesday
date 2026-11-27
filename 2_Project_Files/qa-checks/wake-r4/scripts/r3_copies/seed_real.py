# seed_real.py — the seed on a SCRATCH COPY of the real legacy pickup: dry, then --run. What does the block carry, what stays behind?
# The block's text goes to scratch only; this prints counts and line numbers.
import hashlib, os, re, shutil, sys
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from qlib import *
root = mk("seed", "seed_real")
src = R + "/0_Brain/tasks/NEXT-PICKUP.md"
leg = os.path.join(T(root), "NEXT-PICKUP.md"); shutil.copy(src, leg); h0 = hashlib.sha256(rd(leg)).hexdigest()
L = rd(leg).decode("utf-8", "replace").split("\n")
heads = [(i + 1, l) for i, l in enumerate(L) if l.startswith("## ")]
print("legacy copy: %d bytes, %d lines, %d '## ' headings; sha256 %s (the real file's now: %s)" % (len(rd(leg)), len(L), len(heads), h0[:16], hashlib.sha256(open(src, "rb").read()).hexdigest()[:16]))
print("text BEFORE the first '## ' heading (the file's own header, lines 1 to %d): %d non-blank lines" % (heads[0][0] - 1, sum(1 for l in L[:heads[0][0] - 1] if l.strip())))
other_levels = [(i + 1, l[:70]) for i, l in enumerate(L) if re.match(r"^#{1,6} ", l) and not l.startswith("## ")]
print("headings of other levels in the file: %d %s" % (len(other_levels), other_levels[:6]))
standing = [(n, l) for n, l in heads[1:] if re.search(r"OWED|STANDING|NEXT[- ]PICKUP|GRANT|HOLD|OPEN|CARD|RULE|ALWAYS|NEVER|DO NOT", l)]
print("headings outside the newest block that carry a standing-looking word (OWED, STANDING, NEXT-PICKUP, GRANT, HOLD, OPEN, CARD, RULE, ALWAYS, NEVER, DO NOT): %d" % len(standing))
for n, l in standing[:40]:
    print("   line %d: %s" % (n, l[:110]))
rc, o, e = ho(root, "seed", "--from-legacy")
open(os.path.join(BASE, "seed_real_dry_block.txt"), "w").write(o); open(os.path.join(BASE, "seed_real_dry_report.txt"), "w").write(e)
print("DRY: rc %d; block %d bytes; files in tasks: %s; legacy unchanged: %s" % (rc, len(o.encode()), sorted(os.listdir(T(root))), hashlib.sha256(rd(leg)).hexdigest() == h0))
print("the dry report:\n" + "\n".join("    " + l[:230] for l in e.strip().split("\n")))
# newest block: every non-blank line carried?
end = heads[1][0] - 1 if len(heads) > 1 else len(L)
newest = [l for l in L[heads[0][0]:end] if l.strip()]
miss = [l for l in newest if l not in o]
print("newest block (lines %d to %d): %d non-blank lines; missing from the seeded block: %d; its heading text carried: %s" % (heads[0][0], end, len(newest), len(miss), heads[0][1][3:].strip() in o))
for n, l in heads[1:]:
    hd = l[3:].strip().lstrip("\U0001F534\U0001F7E1\U0001F7E2⚠️*_ ").strip().upper()
    if hd.startswith("OWED") or hd.startswith("STANDING"):
        nxt = [m for m, _ in heads if m > n]; stop = (nxt[0] - 1) if nxt else len(L)
        body = [x for x in L[n:stop] if x.strip()]
        print("standing section line %d (%s...): %d non-blank lines to line %d; carried into the block: %d of %d" % (n, l[:40], len(body), stop, sum(1 for x in body if x in o), len(body)))
parts = {}
cur = None
for l in o.split("\n"):
    if l.startswith("## "): cur = l[3:]; parts[cur] = []
    elif cur: parts[cur].append(l)
print("parts of the seeded block (bytes): %s" % dict((k, len("\n".join(v).encode())) for k, v in parts.items()))
print("parts written as 'none stated in the legacy block': %s" % [k for k, v in parts.items() if any("none stated in the legacy block" in x for x in v)])
# what the second and third newest blocks hold that the newest does not point at (the seat's pack will no longer show them)
for k in (1, 2):
    if len(heads) > k + 1:
        n, l = heads[k]; stop = heads[k + 1][0] - 1
        print("NOT carried, block %d from the top: line %d, %d non-blank lines, heading: %s" % (k + 1, n, sum(1 for x in L[n:stop] if x.strip()), l[:100]))
rc2, o2, e2 = ho(root, "seed", "--from-legacy", "--run")
print("RUN on the scratch copy: rc %d | %s" % (rc2, (o2.strip().split("\n")[-1] if o2.strip() else e2.strip().split("\n")[0])[:160]))
rc3, o3, e3 = ho(root, "check"); print("check: rc %d | %s" % (rc3, o3.strip()[:140]))
rc4, o4, e4 = ho(root, "show"); print("show returns the dry block byte for byte: %s" % (o4 == o))
rc5, o5, e5 = ho(root, "seed", "--from-legacy", "--run"); print("second --run: rc %d | %s" % (rc5, e5.strip()[:120]))
print("legacy copy unchanged after --run: %s; files: %s" % (hashlib.sha256(rd(leg)).hexdigest() == h0, sorted(os.listdir(T(root)))))
hdr = rd(st(root)).split(b"\n---\n")[0].decode()
print("header records an x-clock override: %s" % ([l for l in hdr.split("\n") if l.startswith("xclock_override")] or "no"))
# the pack built on this tree now carries the STATE block; does it still say anything about the legacy file's other sections?
r2 = mk_real("seed_pack", "seed_real"); shutil.copy(st(root), st(r2))
rc6, o6, e6 = wp(r2, "--today", "2026-11-27"); pk = open(os.path.join(r2, "0_Brain/wake/WAKE-wednesday.md"), encoding="utf-8").read() if rc6 == 0 else ""
print("pack built with that STATE block: rc %d, %d bytes; mentions NEXT-PICKUP.md: %d times; carries the standing OWED lines: %s" % (rc6, len(pk.encode()), pk.count("NEXT-PICKUP.md"), "carried from the legacy file's standing section" in pk))
