# usage: python3 -B -I scan.py <word>... -- <file>...   Byte scan: each word in plain, JSON/backslash-escaped, URL-encoded,
# slug (lower, non-alnum->-), underscore slug, escaped-slash spellings; case-insensitive; prints hits per file. Words only on the command line.
import sys, re, urllib.parse
a = sys.argv[1:]; k = a.index("--"); words = a[:k]; files = a[k+1:]
pats = set()
for w in words:
    if not w: continue
    for v in {w, w.replace("/", "\\/"), w.replace("\\", "\\\\"), urllib.parse.quote(w, safe=""), urllib.parse.quote(w),
              re.sub(r"[^A-Za-z0-9]+", "-", w).strip("-"), re.sub(r"[^A-Za-z0-9]+", "_", w).strip("_"), w.replace(" ", "")}:
        if len(v) >= 3: pats.add(v.lower().encode())
# id shapes
rx = [re.compile(rb"toolu_[0-9A-Za-z]{6,}"), re.compile(rb"msg_[0-9A-Za-z]{6,}"), re.compile(rb"req_[0-9A-Za-z]{6,}"),
      re.compile(rb"[0-9a-f]{8}-[0-9a-f]{4}-[0-9a-f]{4}-[0-9a-f]{4}-[0-9a-f]{12}"), re.compile(rb"[A-Za-z0-9._+-]+@[A-Za-z0-9-]+\.[A-Za-z.]+")]
tot = 0
for f in files:
    b = open(f, "rb").read(); lo = b.lower(); n = 0
    for p in pats: n += lo.count(p)
    for r in rx: n += len(r.findall(b))
    print(f"{f}: {len(pats)} word patterns + {len(rx)} id/mail shapes, hits {n}"); tot += n
print("TOTAL", tot)
