"""n8: case durations from the PC's console logs (saved mails), F9/F10 against the other 28.  n1: stage C init line length, mail vs committed copies."""
import re, subprocess, sys
R = "/Volumes/Laptop-DEV/FRIDAY/0_Brain/reference/2026-11-16_claude-to-claude/windows/"
for wo in ("WO-18", "WO-21"):
    t = open(R + "2026-11-23_%s_results_part1.md" % wo, encoding="utf-8").read()
    rows = re.findall(r"^CASE (\S+) (\S+) rc=\S+ ([\d.]+)s", t, re.M)
    f = [(c, float(s)) for c, _, s in rows if re.match(r"F(9|10)", c)]; o = [float(s) for c, _, s in rows if not re.match(r"F(9|10)", c)]
    print("%s: %d CASE lines; F9/F10 %s; other %d cases min %.1f max %.1f" % (wo, len(rows), f, len(o), min(o), max(o)))
repo = sys.argv[1]
mail = open(R + "2026-11-23_WO-19_results.md", encoding="utf-8").read().split("\n")
L = [l for l in mail if l.startswith('{"type":"system","subtype":"init"')]
print("WO-19 mail init line(s):", [len(l) for l in L], " mail line no.", [i + 1 for i, l in enumerate(mail) if l.startswith('{"type":"system","subtype":"init"')])
for c in ("3838bd5", "9bbc466", "ce7276c"):
    cp = subprocess.run(["git", "-C", repo, "show", c + ":spikes/W1-windows-exec-hook/raw/stageC_WO-19.txt"], capture_output=True, text=True).stdout.split("\n")
    print("  committed copy at %s: init line length %s" % (c, [len(l) for l in cp if l.startswith('{"type":"system","subtype":"init"')]))
