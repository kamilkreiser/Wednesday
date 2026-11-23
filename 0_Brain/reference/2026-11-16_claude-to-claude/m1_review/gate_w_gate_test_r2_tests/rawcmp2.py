"""QA-W-GATE-TEST-R2: all 14 committed raw/ copies at a commit against the saved PC mails, line by line, by program.
usage: rawcmp2.py <repo> <commit> [<spoil-file> <spoil-line-1based> <old> <new>]   (the optional args make a red control on a copy in memory)
Each placeholder may stand only for text of its own class: <session-id>/<prompt-id>/<event-uuid> = a UUID, <tool-use-id> = toolu_[A-Za-z0-9]+,
the older work-folder / mailbox placeholders = any text, summarised by sha256 prefix only (no names printed). Counts per class compared with the header."""
import hashlib, re, sys, collections, subprocess
repo, commit = sys.argv[1:3]
spoil = sys.argv[3:7] if len(sys.argv) >= 7 else None
W = "/Volumes/Laptop-DEV/FRIDAY/0_Brain/reference/2026-11-16_claude-to-claude/windows/"
D = "spikes/W1-windows-exec-hook/raw/"
PAIRS = [("stageA_WO-15_part1.txt", "2026-11-23_WO-15_results_part1.md"), ("stageA_WO-15_part2.txt", "2026-11-23_WO-15_results_part2.md"),
 ("stageA2_WO-17.txt", "2026-11-23_WO-17_results.md"), ("stageB_WO-18_part1.txt", "2026-11-23_WO-18_results_part1.md"),
 ("stageB_WO-18_part2.txt", "2026-11-23_WO-18_results_part2.md"), ("stageB_WO-18_part3.txt", "2026-11-23_WO-18_results_part3.md"),
 ("stageB_WO-18_part4.txt", "2026-11-23_WO-18_results_part4.md"), ("stageB_WO-18_note.txt", "2026-11-23_WO-18_results_note.md"),
 ("stageC_WO-19.txt", "2026-11-23_WO-19_results.md"), ("stageA3_WO-20.txt", "2026-11-23_WO-20_results.md"),
 ("stageC2_WO-21_part1.txt", "2026-11-23_WO-21_results_part1.md"), ("stageC2_WO-21_part2.txt", "2026-11-23_WO-21_results_part2.md"),
 ("stageC2_WO-21_part3.txt", "2026-11-23_WO-21_results_part3.md"), ("stageC2_WO-21_part4.txt", "2026-11-23_WO-21_results_part4.md")]
UU = r"[0-9a-f]{8}-[0-9a-f]{4}-[0-9a-f]{4}-[0-9a-f]{4}-[0-9a-f]{12}"
CLS = {"<session-id>": UU, "<prompt-id>": UU, "<event-uuid>": UU, "<tool-use-id>": r"toolu_[A-Za-z0-9]+",
       "<coordinator-mailbox>": r".+?", "<work-folder-slug>-": r".+?", "<work-folder-name>": r".+?", "<WORK-FOLDER>": r".+?", "<work-folder>": r".+?"}
PH = list(CLS)
SPLIT = re.compile("(" + "|".join(re.escape(p) for p in sorted(PH, key=len, reverse=True)) + ")")
grand_bad = 0; grand = collections.Counter(); cons = 0
for raw, orig in PAIRS:
    ob = open(W + orig, "rb").read(); osha = hashlib.sha256(ob).hexdigest()
    o = ob.decode("utf-8").split("\n")
    rr = subprocess.run(["git", "-C", repo, "show", "%s:%s%s" % (commit, D, raw)], capture_output=True, check=True).stdout.decode("utf-8").split("\n")
    if spoil and spoil[0] == raw:
        i = int(spoil[1]) - 1; assert spoil[2] in rr[i], "spoil text not on that line"; rr[i] = rr[i].replace(spoil[2], spoil[3], 1)
    nh = 0
    while nh < len(rr) and rr[nh].startswith("# "): nh += 1
    hdr = " ".join(rr[:nh]); r = rr[nh:]
    named = re.search(r"sha256[^)]*?([0-9a-f]{64})", hdr)
    mh = o.index("---") + 1 if o[0].startswith("From:") else 0
    o2 = o[mh:]
    bad = []; caps = collections.Counter(); vals = collections.defaultdict(set)
    if len(o2) != len(r): bad.append("LINE COUNT orig %d copy %d" % (len(o2), len(r)))
    for i, (a, b) in enumerate(zip(o2, r)):
        if a == b: continue
        parts = SPLIT.split(b)
        if len(parts) == 1: bad.append("line %d: ORIG %r | COPY %r" % (i + 1 + nh, a[:160], b[:160])); continue
        rx = "".join("(%s)" % CLS[p] if p in CLS else re.escape(p) for p in parts)
        m = re.fullmatch(rx, a)
        if not m: bad.append("line %d: no class-true match. COPY %r" % (i + 1 + nh, b[:160])); continue
        g = 1; got = {}
        for p in parts:
            if p in CLS:
                v = m.group(g); g += 1; caps[p] += 1; vals[p].add(v); got.setdefault(p, []).append(v)
        # consistency: a session id inside transcript_path must be the line's session_id
        if "<session-id>" in got and len(set(got["<session-id>"])) > 1:
            bad.append("line %d: two different session ids under <session-id> on one line" % (i + 1 + nh))
        if "<session-id>" in got: cons += 1
    # header-declared counts
    def num(rx):
        mm = re.search(rx, hdr); return None if not mm else sum(int(x) for x in re.findall(r"\d+", mm.group(1)))
    exp = {"<session-id>": num(r"<session-id>: (\d+ in `session_id` fields, \d+) inside"), "<prompt-id>": num(r"<prompt-id>: (\d+)"),
           "<tool-use-id>": num(r"<tool-use-id>: (\d+)"), "<event-uuid>": num(r"<event-uuid>: (\d+)"),
           "<coordinator-mailbox>": num(r"<coordinator-mailbox>: (\d+)"), "<work-folder-slug>-": num(r"<work-folder-slug>-: (\d+)"),
           "<work-folder-name>": num(r"<work-folder-name>: (\d+)"), "<WORK-FOLDER>": num(r"<WORK-FOLDER>: (\d+)"),
           "<work-folder>": num(r"-> <work-folder>: (plain \d+, JSON-escaped \d+, slash \d+|\d+ \+ \d+ \+ \d+)")}
    # placeholders inside the header itself are excluded: count in body only (body placeholders = caps, since an unchanged line has none unless the mail had it)
    body_ph = collections.Counter()
    for b in r:
        for p in SPLIT.findall(b): body_ph[p] += 1
    mism = [ "%s header %s body %d" % (p, exp[p], body_ph[p]) for p in PH if (exp[p] or 0) != body_ph[p] ]
    grand_bad += len(bad) + len(mism)
    print("== %-24s lines %5d=%5d  sha %s  unexplained %d  header-vs-body count mismatches %d" % (raw, len(o2), len(r), "MATCH" if named and named.group(1) == osha else "MISMATCH", len(bad), len(mism)))
    print("     replaced:", ", ".join("%s %d (distinct originals %d)" % (p, caps[p], len(vals[p])) for p in PH if caps[p]))
    for x in bad[:10] + mism: print("     !!", x)
    for p in PH: grand[p] += caps[p]
print("TOTAL replaced:", dict(grand))
print("lines carrying <session-id> with one session id per line:", cons)
print("RAW COPIES: unexplained + header mismatches:", grand_bad)
