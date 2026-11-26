import re, subprocess, sys
C=sys.argv[1]
def rows(sha):
    s = subprocess.run(["git","-C",C,"show",f"{sha}:scripts/red-controls-daemon.sh"],capture_output=True,check=True).stdout.decode().split("\n")
    i = s.index("ROWS=("); j = s.index(")", i)
    return [l for l in s[i+1:j] if l.startswith('  "COAGENT_RED')], s
b, _ = rows("5e11609"); h, hs = rows("d79ae1c")
print("rows base", len(b), "head", len(h), "base rows identical & in order at head:", h[:len(b)] == b)
for r in h[len(b):]: print("  new:", r, "fields", len(r.strip().strip('"').split("|")))
st = open(sys.argv[2]).read()
rx = re.search(r"RED_ONLY='([^']+)'", st).group(1)
print("builder regex (STATUS):", rx)
sel = [r for r in h if re.search(rx, r.strip().strip('"').split("|")[1])]
print("selected", len(sel), "variants", len({r.split('|')[1] for r in sel}))
# script's own test line
print([l for l in hs if "RED_ONLY" in l])
