"""QA byte scan: words come from argv only (never written to a file). Usage:
namescan.py --files f1 f2 ... --words w1 w2 ...   Each word is searched case-insensitively as bytes
in spellings: plain, URL-encoded, backslash-escaped, slug (spaces->-/_ removed), lowercase-joined.
Also id shapes: toolu_, msg_0, req_0, UUIDs, and secret-looking strings without a fake marker."""
import sys, re, urllib.parse
a = sys.argv[1:]
fi = a.index('--files'); wi = a.index('--words')
files = a[fi+1:wi]; words = a[wi+1:]
def spellings(w):
    s = {w, urllib.parse.quote(w), urllib.parse.quote(w, safe=''), w.replace(' ', '\\ '), w.replace('/', '\\/'),
         w.replace(' ', '-'), w.replace(' ', '_'), w.replace(' ', ''), w.replace('/', '\\'), w.replace('!', '\\!')}
    return {x.lower().encode() for x in s if x}
sp = {w: spellings(w) for w in words}
idre = [re.compile(rb'toolu_[A-Za-z0-9]{6,}'), re.compile(rb'\bmsg_[A-Za-z0-9]{10,}'), re.compile(rb'\breq_[A-Za-z0-9]{10,}'),
        re.compile(rb'[0-9a-fA-F]{8}-[0-9a-fA-F]{4}-[0-9a-fA-F]{4}-[0-9a-fA-F]{4}-[0-9a-fA-F]{12}')]
keyre = re.compile(rb'(?:ghp_|gho_|github_pat_|glpat-|xox[bpars]-|AKIA|ASIA|AIza|sk-ant-|sk_live_|npm_|hf_|SG\.|shpat_|dop_v1_)[A-Za-z0-9_\-\.]{12,}')
fake = re.compile(rb'(?i)fake|qa|deadbeef|0000|x0x0|example')
hits = 0
for f in files:
    b = open(f, 'rb').read(); low = b.lower()
    for w, ss in sp.items():
        for s in ss:
            i = low.find(s)
            while i >= 0:
                ln = b.count(b'\n', 0, i) + 1
                print(f"WORD  {f}:{ln}: word#{words.index(w)} spelling {s!r}"[:200]); hits += 1
                i = low.find(s, i + 1)
    for r in idre:
        for m in r.finditer(b):
            print(f"ID    {f}:{b.count(b'\n',0,m.start())+1}: {m.group()[:60]!r}")
    for m in keyre.finditer(b):
        if not fake.search(m.group()):
            print(f"KEY?  {f}:{b.count(b'\n',0,m.start())+1}: {m.group()[:16]!r}...")
print(f"scanned {len(files)} files, {sum(len(v) for v in sp.values())} spellings of {len(words)} words: {hits} word hits")
