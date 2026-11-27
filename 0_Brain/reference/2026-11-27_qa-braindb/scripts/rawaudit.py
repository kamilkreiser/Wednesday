import os, re, subprocess, glob
W = "/Volumes/DevMASTER/WEDNESDAY"
def q(sql):
    r = subprocess.run(["/opt/homebrew/opt/postgresql@15/bin/psql","-X","-At","-h","/tmp/wed-braindb-501-wednesday","-d","braindb","-c",sql], stdout=subprocess.PIPE)
    return [l for l in r.stdout.decode().split("\n") if l]
idx = set(q("select path from brain.files"))
print("indexed paths:", len(idx))
print("path like chat:", [p for p in idx if "chat" in p.lower()])
L = sorted(glob.glob(W + "/0_Brain/learnings/20*.md"))
print("lesson files on disk matching 20*.md:", len(L))
# independent raw read of each lesson head: any line in the first 25 lines that looks like a tier naming datasec
odd = []
for p in L:
    rel = os.path.relpath(p, W)
    raw = open(p, "rb").read()
    head = raw[:3000].decode("utf-8", "replace")
    lines = head.split("\n")[:25]
    tierlines = [l for l in lines if re.match(r"(?i)^\s*\W*tier\s*:", l)]
    names_ds = any(re.search(r"(?i)datasec|hpsm|oxpd|nexus|coagent", l) for l in tierlines)
    starts = raw[:3] == b"---"
    bom = raw[:3] == b"\xef\xbb\xbf"
    crlf = b"\r\n" in raw[:400]
    closed = head.find("\n---", 3) != -1
    ntier = len(tierlines)
    flag = []
    if not starts: flag.append("no-leading---")
    if bom: flag.append("BOM")
    if crlf: flag.append("CRLF")
    if starts and not closed: flag.append("unclosed")
    if ntier > 1: flag.append("tier-lines=%d" % ntier)
    if ntier == 0: flag.append("no-tier-line")
    if any(re.match(r"^\s*[A-Z]\w*\s*:", l) and re.match(r"(?i)^\s*tier", l) and not l.lstrip().startswith("tier") for l in tierlines): flag.append("tier-key-case")
    if names_ds and rel in idx: flag.append("INDEXED-BUT-TIER-NAMES-OTHER-CLIENT")
    if flag: odd.append((rel, flag, [t.strip()[:60] for t in tierlines], rel in idx))
print("lessons with any frontmatter oddity:", len(odd))
for o in odd: print("  ", o)
# rules index: malformed rows
tsv = open(W + "/0_Brain/learnings/_rules_index.tsv", encoding="utf-8").read().split("\n")
bad = [(n, len(l.split("\t"))) for n, l in enumerate(tsv, 1) if l.strip() and not l.startswith("#") and len(l.split("\t")) != 7]
print("rules-index data lines:", sum(1 for l in tsv if l.strip() and not l.startswith("#")), "malformed (not 7 fields):", bad)
keys = [l.split("\t")[0] for l in tsv if l.strip() and not l.startswith("#") and len(l.split("\t")) == 7]
print("keys with leading/trailing space or slash:", [k for k in keys if k != k.strip() or "/" in k])
seatvals = {}
for l in tsv:
    if l.strip() and not l.startswith("#") and len(l.split("\t")) == 7:
        seatvals[l.split("\t")[2]] = seatvals.get(l.split("\t")[2], 0) + 1
print("seats column values:", seatvals)
bases = set(k.split("#")[0] for k in keys)
names = set(os.path.basename(p) for p in L)
norow = sorted(n for n in names if n not in bases)
print("lessons on disk with NO rules-index row:", len(norow), "of which indexed:", sum(1 for n in norow if "0_Brain/learnings/" + n in idx))
for n in norow: print("   no-row:", n, "indexed" if "0_Brain/learnings/" + n in idx else "not-indexed")
# section markers
mk = re.compile(r"^<!--\s*tier:\s*(.*?)\s*-->\s*$")
anymark = re.compile(r"(?i)<!--\s*tier")
for p in L:
    rel = os.path.relpath(p, W)
    if rel not in idx: continue
    lines = open(p, encoding="utf-8", errors="replace").read().split("\n")
    for i, l in enumerate(lines):
        if anymark.search(l):
            m = mk.match(l)
            nxt = lines[i+1] if i+1 < len(lines) else ""
            val = m.group(1) if m else "(not matched by anchored regex)"
            if re.search(r"(?i)datasec", l) or not m or not nxt.startswith("#"):
                # find the extent: lines to next heading, and whether a deeper heading follows directly
                j = i + 2
                while j < len(lines) and not re.match(r"^#{1,6}\s", lines[j]): j += 1
                lvl = len(re.match(r"^(#*)", nxt).group(1))
                nlvl = len(re.match(r"^(#*)", lines[j]).group(1)) if j < len(lines) else 0
                print("  marker in INDEXED lesson %s line %d: value=%r next-line-is-heading=%s level=%d next-heading-level=%d %s" % (os.path.basename(p), i+1, val, nxt.startswith("#"), lvl, nlvl, "SUBSECTION-FOLLOWS (would survive the drop)" if nlvl > lvl and re.search(r"(?i)datasec", l) else ""))
