# census_check.py — re-measure BEFORE and AFTER. (1) a scratch COPY of wake_census.sh run with --root on the real tree (sizes only, writes nothing)
# and --pack on a pack built in scratch from copies of the real sources; (2) my own sum of the same files' sizes, independent of the script.
import datetime, glob, os, re, subprocess, sys
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from qlib import *
root = mk_real("census")
rc, o, e = wp(root, "--today", datetime.date.today().isoformat())
pack = os.path.join(root, "0_Brain/wake/WAKE-wednesday.md")
print("scratch pack build: rc %d, %d bytes" % (rc, os.path.getsize(pack)))
before_ls = sorted(os.listdir(R + "/0_Brain/tasks"))
p = subprocess.run(["/bin/bash", os.path.join(root, "2_Project_Files/wake/wake_census.sh"), "--seat", "wednesday", "--root", R, "--pack", pack], stdout=subprocess.PIPE, stderr=subprocess.PIPE, env=ENV())
out = p.stdout.decode()
print("wake_census.sh rc %d; stderr %r; real tasks listing unchanged by it: %s; real 0_Brain/wake exists: %s" % (p.returncode, p.stderr.decode()[:100], sorted(os.listdir(R + "/0_Brain/tasks")) == before_ls, os.path.exists(R + "/0_Brain/wake")))
print(out)
today = datetime.date.today(); yday = today - datetime.timedelta(days=1)
B = R + "/0_Brain"
files = [R + "/CLAUDE.md", B + "/CLAUDE.md", B + "/identity/persona.md", B + "/identity/voice-protocol.md", B + "/people/kam.md", B + "/learnings/_rules_card_wednesday.md",
         B + "/learnings/_ledger.md", B + "/tasks/NEXT-PICKUP.md", B + "/tasks/EXPIRING-GRANTS.md", B + "/tasks/TASKS.md", B + "/projects_index/INDEX.md", B + "/tasks/WEEK-INSTRUCTION.md",
         B + "/daily/%s.md" % yday.isoformat(), B + "/daily/%s.md" % today.isoformat()]
sz = dict((f, os.path.getsize(f)) for f in files if os.path.isfile(f))
missing = [f for f in files if f not in sz]
ent = [f for f in glob.glob(B + "/projects_index/entries/*") if os.path.isfile(f)]
ent_b = sum(os.path.getsize(f) for f in ent)
conf = [f for f in ent if "(conflict_on_" in os.path.basename(f) or ".pre-" in os.path.basename(f)]
conf_b = sum(os.path.getsize(f) for f in conf)
total = sum(sz.values()) + ent_b; clean = total - conf_b
kept = sum(sz[f] for f in (files[0], files[1], files[11], files[12], files[13]) if f in sz)
notes = sum(sz[f] for f in (files[12], files[13]) if f in sz)
pb = os.path.getsize(pack); after = pb + kept; alt = after - notes
pct = lambda a, b: "%.1f%%" % ((a - b) * 100.0 / a)
print("MY OWN SUM (independent of the script), measured %s:" % datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S"))
print("  files missing from the list: %s; entries: %d files %d bytes, of which conflict/backup copies %d files %d bytes" % (missing or "none", len(ent), ent_b, len(conf), conf_b))
print("  BEFORE with the conflict copies: %d bytes (~%d tokens); BEFORE without them: %d bytes (~%d tokens)" % (total, (total + 3) // 4, clean, (clean + 3) // 4))
print("  AFTER as proposed (pack %d + rules files + week instruction + two notes %d): %d bytes (~%d tokens); with earlier notes on demand: %d bytes (~%d tokens)" % (pb, kept, after, (after + 3) // 4, alt, (alt + 3) // 4))
print("  REDUCTION against BEFORE without conflict copies: %s (notes on demand: %s); against BEFORE with them: %s (notes on demand: %s)" % (pct(clean, after), pct(clean, alt), pct(total, after), pct(total, alt)))
m1 = re.search(r"TOTAL, with INDEX.md and entries whole\s+(\d+)", out); m2 = re.search(r"TOTAL, without the \d+ sync-conflict / backup copies\s+(\d+)", out); m3 = re.search(r"pack \+ rules files \+ week instruction \+ two daily notes\s+(\d+)", out)
print("  the script's three figures equal mine: with %s, without %s, after %s" % (m1 and int(m1.group(1)) == total, m2 and int(m2.group(1)) == clean, m3 and int(m3.group(1)) == after))
print("  (the legacy pickup and today's note grow while seats work, so these differ from STATUS.md's 13:28 figures by that growth)")
