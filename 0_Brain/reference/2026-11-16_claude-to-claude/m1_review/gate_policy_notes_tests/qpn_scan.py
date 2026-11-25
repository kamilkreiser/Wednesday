#!/usr/bin/env python3
"""QA-POLICY-NOTES byte scan. usage: python3 -B -I qpn_scan.py <file>[=<basefile>]... -- <word>...
Words come ONLY from the command line at run time (never written to a file). Each word is searched case-insensitively
as bytes: plain, URL-encoded, backslash-escaped, slug (non-alnum -> '-'), and UTF-16LE; also toolu_/req_/msg_0 ids and
UUIDs. Prints file:line:kind per hit (the word's index, never the word). With file=basefile, each hit line is also
checked for being byte-identical to SOME line of the base file ('old' = present in base, 'NEW' = not)."""
import re, sys, urllib.parse
i = sys.argv.index('--'); specs, words = sys.argv[1:i], [w for w in sys.argv[i + 1:] if w]
pats = []
for n, w in enumerate(words):
    forms = {w, urllib.parse.quote(w, safe=''), urllib.parse.quote(w), w.replace('\\', '\\\\').replace('/', '\\/'),
             re.sub(r'[^A-Za-z0-9]+', '-', w).strip('-')}
    for f in forms:
        if len(f) >= 3:
            pats.append((f'w{n}', re.compile(re.escape(f.encode()), re.I)))
    pats.append((f'w{n}-utf16', re.compile(re.escape(w.encode('utf-16-le')), re.I)))
pats += [('toolu', re.compile(rb'toolu_[A-Za-z0-9]{6,}')), ('req', re.compile(rb'\breq_[A-Za-z0-9]{8,}')),
         ('msg', re.compile(rb'\bmsg_0[A-Za-z0-9]{6,}')),
         ('uuid', re.compile(rb'[0-9a-fA-F]{8}-[0-9a-fA-F]{4}-[0-9a-fA-F]{4}-[0-9a-fA-F]{4}-[0-9a-fA-F]{12}'))]
hits = new = total = 0
for spec in specs:
    fn, _, base = spec.partition('=')
    data = open(fn, 'rb').read(); total += len(data)
    lines = data.split(b'\n')
    baselines = set(open(base, 'rb').read().split(b'\n')) if base else None
    seen = set()
    for kind, p in pats:
        for m in p.finditer(data):
            ln = data.count(b'\n', 0, m.start()) + 1
            hits += 1
            tag = ''
            if baselines is not None:
                old = lines[ln - 1] in baselines
                tag = ' old' if old else ' NEW'
                new += 0 if old else 1
            print(f'{fn}:{ln}:{kind}{tag}')
print(f'SCAN files {len(specs)} bytes {total} words {len(words)} hits {hits} not-on-a-base-line {new}')
