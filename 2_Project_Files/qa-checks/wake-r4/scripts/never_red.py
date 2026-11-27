# never_red.py — which of the suite's checks never went red under ANY mutant (the lane's 115 as I ran them, plus my own 21)?
# A check that no mutant turns red is not proven able to fail. 'must succeed beside' controls are expected in this list.
import re, glob, os
Q = "/Volumes/DevMASTER/WEDNESDAY/2_Project_Files/qa-checks/wake-r4/raw"
allc = {}
for l in open(Q + "/suite_py314.txt"):
    m = re.match(r"PASS (\S+) (.*)", l)
    if m: allc[m.group(1)] = m.group(2).strip()
red = set(); n_lines = 0
for f in sorted(glob.glob(Q + "/mutants_*.txt")) + [Q + "/my_mutants.txt"]:
    for l in open(f):
        m = re.search(r":: (?:went red|red): (.*?)(?: \(passed \d+\))?$", l.strip())
        if m and (l.startswith("RED-AS-EXPECTED") or l.startswith("CAUGHT")):
            n_lines += 1; red.update(m.group(1).split())
never = [c for c in allc if c not in red]
print("checks in the suite: %d; mutant result lines read: %d; checks that went red under at least one mutant: %d; never red: %d" % (len(allc), n_lines, len(set(allc) & red), len(never)))
ctrl = [c for c in never if re.search(r"must succeed|control|comparison base|\(what the proposal describes\)", allc[c])]
print("of the never-red, %d say of themselves that they are must-succeed controls: %s" % (len(ctrl), " ".join(ctrl)))
print("the other %d:" % (len(never) - len(ctrl)))
for c in never:
    if c not in ctrl: print("  %-6s %s" % (c, allc[c][:150]))
