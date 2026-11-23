"""QA-W-GATE-TEST-R2: the owner's other classes over every ADDED line of main...head (the lane's own additions), with a positive
control per class run on a real source (counts only; no hit text is printed for controls, so no name lands in this output).
usage: namescan.py <repo> <main> <head>"""
import re, subprocess, sys
repo, main, head = sys.argv[1:4]
W = "/Volumes/Laptop-DEV/FRIDAY/0_Brain/reference/2026-11-16_claude-to-claude/windows/"
CL = {
 "account name":        (r"kamil|kreis|\bkam\b", re.I, ["/Volumes/Laptop-DEV/CLAUDE.md"]),
 "home path":           (r"/Users/[A-Za-z]|C:\\\\?Users\\\\?[A-Za-z]|/home/[a-z]", re.I, ["SYNTH:C:\\Users\\someone\\x and /Users/someone/y"]),
 "machine name":        (r"smashhome|DESKTOP-[A-Z0-9]{4,}|LAPTOP-[A-Z0-9]{4,}", re.I, [W + "2026-11-21_machine-report.md"]),
 "mail address":        (r"[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Za-z]{2,}", 0, [W + "2026-11-23_WO-18_results_part1.md"]),
 "network address":     (r"\b(?:\d{1,3}\.){3}\d{1,3}\b|\b[0-9a-f]{1,4}(?::[0-9a-f]{1,4}){7}\b", re.I, [W + "2026-11-21_machine-report.md"]),
 "token":               (r"sk-ant-[A-Za-z0-9_-]{8,}|ghp_[A-Za-z0-9]{20,}|gho_[A-Za-z0-9]{20,}|github_pat_|AKIA[0-9A-Z]{16}|Bearer [A-Za-z0-9._-]{20,}|-----BEGIN [A-Z ]*PRIVATE KEY|am_[A-Za-z0-9]{24,}", 0, ["SYNTH:Authorization: Bearer abcdefghijklmnopqrstuvwxyz0123"]),
 "helper work folder":  (r"C:\\\\?c2c|C:/c2c|C--c2c|\bc2c\\\\", re.I, [W + "2026-11-23_WO-18_results_part2.md"]),
 "volume/workspace path": (r"/Volumes/|Laptop-DEV|FRIDAY/|!CODING|/private/tmp/|T9", 0, ["SYNTH:/Volumes/Laptop-DEV/FRIDAY/x and !CODING"]),
}
diff = subprocess.run(["git", "-C", repo, "diff", "--no-color", "-U0", main + "..." + head], capture_output=True, check=True).stdout.decode("utf-8", "replace")
added = [l[1:] for l in diff.split("\n") if l.startswith("+") and not l.startswith("+++")]
print("added lines main...head:", len(added))
print("%-24s %12s %18s" % ("class", "added hits", "positive control"))
for name, (rx, fl, ctl) in CL.items():
    hits = [l for l in added if re.search(rx, l, fl)]
    c = 0
    for s in ctl:
        txt = s[6:] if s.startswith("SYNTH:") else open(s, encoding="utf-8", errors="replace").read()
        c += sum(1 for l in txt.split("\n") if re.search(rx, l, fl))
    print("%-24s %12d %18d" % (name, len(hits), c))
    if name == "volume/workspace path":
        rest = [h for h in hits if not re.search(r"^# .*Original, unchanged: Friday's FRIDAY/0_Brain/reference/", h)]
        print("      of which raw-copy header lines naming the saved mail by its vault-relative path: %d; other: %d" % (len(hits) - len(rest), len(rest))); hits = rest
    for h in hits[:6]:
        m = re.search(rx, h, fl); print("      HIT:", repr(h[max(0, m.start() - 50):m.end() + 30]))
