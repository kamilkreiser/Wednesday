# QA-SCANNER-NEXT name scan: words come ONLY from argv (never written to a file); prints file:line and the
# word's NUMBER, never the word. Reads files as bytes. Spellings per word: plain, lower, upper, URL-encoded,
# backslash-escaped blanks, slug (-, _), backslash path. Short words (<5) match only as whole words.
# Usage: scan.py <file>... -- <word>...
import sys, re
a = sys.argv[1:]; k = a.index("--"); files, words = a[:k], a[k+1:]
def spellings(w):
    s = {w, w.lower(), w.upper(), w.replace(" ", "%20"), w.replace(" ", "\\ "), w.replace("!", "%21"),
         w.replace(" ", "-").lower(), w.replace(" ", "_").lower(), w.replace("/", "\\"), w.replace("/", "\\\\"),
         w.replace(" ", "%20").replace("!", "%21")}
    return {x for x in s if x}
pats = []
for n, w in enumerate(words, 1):
    for s in spellings(w):
        e = re.escape(s.encode())
        if len(w) < 5: e = rb"(?<![A-Za-z0-9])" + e + rb"(?![A-Za-z0-9])"
        pats.append((n, re.compile(e, re.I)))
ids = [("uuid", re.compile(rb"[0-9a-f]{8}-[0-9a-f]{4}-[0-9a-f]{4}-[0-9a-f]{4}-[0-9a-f]{12}", re.I)),
       ("tool/msg/req id", re.compile(rb"\b(toolu|msg|req|sess|session)_[A-Za-z0-9]{8,}")),
       ("api key", re.compile(rb"sk-ant-[A-Za-z0-9_-]{8,}"))]
tw = ti = 0; nsp = len(pats)
for f in files:
    data = open(f, "rb").read()
    for ln, line in enumerate(data.split(b"\n"), 1):
        hit = sorted({n for n, p in pats if p.search(line)})
        for n in hit: print(f"WORD {f}:{ln} word#{n}"); tw += 1
        for nm, p in ids:
            for m in p.finditer(line): print(f"ID {f}:{ln} {nm} {m.group(0)[:13].decode('latin1')}..."); ti += 1
print(f"scanned {len(files)} files, {nsp} spellings of {len(words)} words: {tw} word hits, {ti} id shapes")
