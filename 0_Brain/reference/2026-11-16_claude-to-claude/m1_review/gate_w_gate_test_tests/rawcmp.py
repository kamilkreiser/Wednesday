"""QA-W-GATE-TEST: each committed raw/ copy against its saved PC mail, line by line, by program.
Every differing line must be explained by a ruled placeholder; the captured original text per placeholder is counted."""
import hashlib, re, sys, collections, os
W = "/Volumes/Laptop-DEV/FRIDAY/0_Brain/reference/2026-11-16_claude-to-claude/windows/"
R = "/private/tmp/claude-501/qwg/clone/spikes/W1-windows-exec-hook/raw/"
PAIRS = [("stageA_WO-15_part1.txt", "2026-11-23_WO-15_results_part1.md"), ("stageA_WO-15_part2.txt", "2026-11-23_WO-15_results_part2.md"),
         ("stageA2_WO-17.txt", "2026-11-23_WO-17_results.md"), ("stageB_WO-18_part1.txt", "2026-11-23_WO-18_results_part1.md"),
         ("stageB_WO-18_part2.txt", "2026-11-23_WO-18_results_part2.md"), ("stageB_WO-18_part3.txt", "2026-11-23_WO-18_results_part3.md"),
         ("stageB_WO-18_part4.txt", "2026-11-23_WO-18_results_part4.md"), ("stageB_WO-18_note.txt", "2026-11-23_WO-18_results_note.md"),
         ("stageC_WO-19.txt", "2026-11-23_WO-19_results.md"), ("stageA3_WO-20.txt", "2026-11-23_WO-20_results.md"),
         ("stageC2_WO-21_part1.txt", "2026-11-23_WO-21_results_part1.md"), ("stageC2_WO-21_part2.txt", "2026-11-23_WO-21_results_part2.md"),
         ("stageC2_WO-21_part3.txt", "2026-11-23_WO-21_results_part3.md"), ("stageC2_WO-21_part4.txt", "2026-11-23_WO-21_results_part4.md")]
PH = ["<coordinator-mailbox>", "<work-folder-slug>-", "<work-folder-name>", "<WORK-FOLDER>", "<work-folder>"]
total_bad = 0
allcap = collections.Counter()
for raw, orig in PAIRS:
    ob = open(W + orig, "rb").read()
    osha = hashlib.sha256(ob).hexdigest()
    o = ob.decode("utf-8").split("\n")
    r = open(R + raw, encoding="utf-8").read().split("\n")
    hdr = [l for l in r[:3] if l.startswith("# ")]
    named = re.search(r"sha256[^0-9a-f]*([0-9a-f]{64})", hdr[0])
    r = r[len(hdr):]
    mailhdr = 0
    if o[0].startswith("From:"):
        mailhdr = o.index("---") + 1
    o2 = o[mailhdr:]
    caps = collections.Counter(); bad = []
    if len(o2) != len(r):
        bad.append("LINE COUNT original %d (after %d header lines) vs copy %d" % (len(o2), mailhdr, len(r)))
    for i, (a, b) in enumerate(zip(o2, r)):
        if a == b:
            continue
        parts = re.split("(" + "|".join(re.escape(p) for p in PH) + ")", b)
        rx = "".join("(?P<g%d>.+?)" % k if p in PH else re.escape(p) for k, p in enumerate(parts))
        m = re.fullmatch(rx, a)
        if not m:
            bad.append("line %d (orig %d): ORIG %r | COPY %r" % (i + 1 + len(hdr), i + 1 + mailhdr, a[:200], b[:200]))
            continue
        for k, p in enumerate(parts):
            if p in PH:
                caps[(p, m.group("g%d" % k))] += 1
    total_bad += len(bad)
    print("== %s <- %s: original %d lines (mail header %d), copy %d body lines; sha256 named %s; differing lines unexplained: %d" % (
        raw, orig, len(o), mailhdr, len(r), "MATCH" if named and named.group(1) == osha else "MISMATCH(%s vs %s)" % (named and named.group(1), osha), len(bad)))
    for k, v in sorted(caps.items()):
        print("   %-22s <- %-40r x%d" % (k[0], k[1], v))
        allcap[k] += v
    for x in bad[:20]:
        print("   UNEXPLAINED", x)
print("TOTAL unexplained differing lines:", total_bad)
print("placeholder classes (all files):")
for k, v in sorted(allcap.items()):
    print("   %-22s <- %-40r x%d" % (k[0], k[1], v))
