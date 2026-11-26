# QA-AUDIT-EMAIL byte scan (tool outside the repository). Words come ONLY from the command line.
# Usage: python3 -B qa_scan.py --files <f>... --words <w>...
import sys, urllib.parse
a = sys.argv[1:]; i = a.index('--words'); files = a[1:i]; words = [w for w in a[i + 1:] if w]
def spellings(w):
    s = {w, w.replace(' ', '-'), w.replace(' ', '_'), w.replace(' ', ''), urllib.parse.quote(w), urllib.parse.quote_plus(w),
         urllib.parse.quote(w, safe='').lower(), w.replace(' ', '\\ '), w.replace('/', '\\/'), w.replace('/', '\\\\')}
    out = set()
    for x in s:
        out.add(('utf8', x.lower().encode()))
        out.add(('utf16le', x.lower().encode('utf-16-le')))
    return out
hits = 0
for f in files:
    data = open(f, 'rb').read(); low = data.lower()
    for wi, w in enumerate(words):
        for kind, sp in spellings(w):
            if len(sp) < 3: continue
            p = low.find(sp)
            while p >= 0:
                hits += 1
                ls = data.rfind(b'\n', 0, p) + 1; le = data.find(b'\n', p); le = len(data) if le < 0 else le
                line = data[:p].count(b'\n') + 1
                print(f'HIT word#{wi} {kind} {f.split("/")[-1]}:{line} @{p} | {data[ls:le][:160]!r}')
                p = low.find(sp, p + 1)
print(f'files {len(files)} words {len(words)} hits {hits}')
