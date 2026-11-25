#!/usr/bin/env python3
"""QA-POLICY-AT-R2 byte scan (copied from the QA-POLICY-AT check's qpa_scan.py; adds c2c card ids and, for NEW lines, the hit masked in context). usage: python3 -B -I qpx_scan.py <file>[=<basefile>]... -- <word>...
Words come ONLY from the command line (never written to a file). Each word, case-insensitive, as bytes: plain,
URL-encoded, backslash-escaped, slug, UTF-16LE; plus toolu_/req_/msg_0 ids and UUIDs. Output: one line per (file, line)
with the word INDEXES that hit (never the word), tagged 'base-identical' when the whole line is byte-identical to a
line of the base file, else 'NEW'."""
import re, sys, urllib.parse
i = sys.argv.index('--'); specs, words = sys.argv[1:i], [w for w in sys.argv[i + 1:] if w]
pats = []
for n, w in enumerate(words):
    forms = {w, urllib.parse.quote(w, safe=''), urllib.parse.quote(w), w.replace('\\', '\\\\').replace('/', '\\/'),
             re.sub(r'[^A-Za-z0-9]+', '-', w).strip('-')}
    for f in forms:
        if len(f) >= 3:
            pats.append((f'w{n}', re.compile(re.escape(f.encode()), re.I)))
    pats.append((f'w{n}u16', re.compile(re.escape(w.encode('utf-16-le')), re.I)))
pats += [('toolu', re.compile(rb'toolu_[A-Za-z0-9]{6,}')), ('req', re.compile(rb'\breq_[A-Za-z0-9]{8,}')),
         ('msg', re.compile(rb'\bmsg_0[A-Za-z0-9]{6,}')),
         ('uuid', re.compile(rb'[0-9a-fA-F]{8}-[0-9a-fA-F]{4}-[0-9a-fA-F]{4}-[0-9a-fA-F]{4}-[0-9a-fA-F]{12}')),
         ('cardid', re.compile(rb'[a-z]+-c2c-[a-z0-9-]+'))]
CTX = {}
tot_lines = tot_new = tot_bytes = 0
for spec in specs:
    fn, _, base = spec.partition('=')
    data = open(fn, 'rb').read(); tot_bytes += len(data)
    lines = data.split(b'\n')
    baselines = set(open(base, 'rb').read().split(b'\n')) if base else None
    hit = {}
    for kind, p in pats:
        for m in p.finditer(data):
            ln = data.count(b'\n', 0, m.start()) + 1
            hit.setdefault(ln, set()).add(kind)
            a, b = max(0, m.start() - 4), min(len(data), m.end() + 4)
            CTX.setdefault((fn, ln), []).append(data[a:m.start()].decode('utf-8', 'replace') + f'<{kind}>' + data[m.end():b].decode('utf-8', 'replace')
                                                if kind.startswith('w') else data[m.start():m.end()].decode('utf-8', 'replace'))
    nf = 0
    for ln in sorted(hit):
        tag = ('base-identical' if lines[ln - 1] in baselines else 'NEW') if baselines is not None else 'no-base'
        nf += tag != 'base-identical'
        print(f'{fn}:{ln}: {",".join(sorted(hit[ln]))} {tag}' + (f'  ctx {CTX[(fn, ln)]}' if tag != 'base-identical' else ''))
    print(f'FILE {fn}: lines with hits {len(hit)}, not base-identical {nf}')
    tot_lines += len(hit); tot_new += nf
print(f'SCAN files {len(specs)} bytes {tot_bytes} words {len(words)} lines-with-hits {tot_lines} not-base-identical {tot_new}')
