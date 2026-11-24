#!/usr/bin/env python3
"""QA-POLICY-OWNER-MODE byte scan. usage: python3 -B -I qscan.py <file>... -- <word>...
Words come ONLY from the command line (never written to a file). Each word is searched case-insensitively as bytes in
four spellings: plain, URL-encoded, backslash-escaped (JSON/Rust string), slug (non-alnum -> '-'), plus UTF-16LE.
Also: tool-use / request / message ids and any UUID. Prints one line per hit: file:line:kind (never the word itself,
only its index, so the output is safe to quote)."""
import re, sys, urllib.parse
i = sys.argv.index('--'); files, words = sys.argv[1:i], [w for w in sys.argv[i+1:] if w]
pats = []
for n, w in enumerate(words):
    forms = {w, urllib.parse.quote(w, safe=''), urllib.parse.quote(w), w.replace('/', '\\/').replace('\\', '\\\\'),
             re.sub(r'[^A-Za-z0-9]+', '-', w).strip('-')}
    for f in forms:
        if len(f) >= 3:
            pats.append((f'w{n}', re.compile(re.escape(f.encode()), re.I)))
    pats.append((f'w{n}-utf16', re.compile(re.escape(w.encode('utf-16-le')), re.I)))
pats += [('toolu', re.compile(rb'toolu_[A-Za-z0-9]{6,}')), ('req', re.compile(rb'\breq_[A-Za-z0-9]{8,}')),
         ('msg', re.compile(rb'\bmsg_0[A-Za-z0-9]{6,}')),
         ('uuid', re.compile(rb'[0-9a-fA-F]{8}-[0-9a-fA-F]{4}-[0-9a-fA-F]{4}-[0-9a-fA-F]{4}-[0-9a-fA-F]{12}'))]
hits = 0; total = 0
for fn in files:
    data = open(fn, 'rb').read(); total += len(data)
    for kind, p in pats:
        for m in p.finditer(data):
            hits += 1
            print(f'{fn}:{data.count(b"\n", 0, m.start()) + 1}:{kind}')
print(f'SCAN files {len(files)} bytes {total} words {len(words)} hits {hits}')
