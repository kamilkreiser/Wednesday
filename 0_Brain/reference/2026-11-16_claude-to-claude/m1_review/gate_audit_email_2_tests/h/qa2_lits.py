# QA-AUDIT-EMAIL-2: every string literal of the given Rust files, in the five placements of redaction.rs:73-79 (own extractor).
# Usage: python3 -B qa2_lits.py <out prefix> <files...>
import sys, json, re
OUT = sys.argv[1]; items = []; counts = {}
def lits(src):
    i = 0; n = len(src); out = []
    while i < n:
        if src.startswith('//', i): i = src.find('\n', i); i = n if i < 0 else i; continue
        m = re.compile(r'b?r(#*)"').match(src, i)
        if m and (i == 0 or not (src[i-1].isalnum() or src[i-1] == '_')):
            close = '"' + m.group(1); j = src.find(close, m.end()); out.append(src[m.end():j]); i = j + len(close); continue
        if src[i] == "'" :  # char literal or lifetime: skip a char literal only
            m = re.compile(r"'(\\u\{[0-9a-fA-F]+\}|\\.|[^\\'])'").match(src, i)
            if m: i = m.end(); continue
        if src[i] == '"' and not (i > 0 and (src[i-1].isalnum() or src[i-1] == '_')):
            j = i + 1; buf = []
            while src[j] != '"':
                if src[j] == '\\':
                    c = src[j + 1]
                    if c == 'n': buf.append('\n'); j += 2
                    elif c == 't': buf.append('\t'); j += 2
                    elif c == 'r': buf.append('\r'); j += 2
                    elif c == '0': buf.append('\0'); j += 2
                    elif c in '\\"\'': buf.append(c); j += 2
                    elif c == 'x': buf.append(chr(int(src[j+2:j+4], 16))); j += 4
                    elif c == 'u': k = src.index('}', j); buf.append(chr(int(src[j+3:k], 16))); j = k + 1
                    elif c == '\n':
                        j += 2
                        while src[j] in ' \t\n': j += 1
                    else: buf.append('\\' + c); j += 2
                else: buf.append(src[j]); j += 1
            out.append(''.join(buf)); i = j + 1; continue
        i += 1
    return out
seen = set()
for f in sys.argv[2:]:
    name = f.split('/')[-1]; c = 0
    for v in lits(open(f, encoding='utf-8').read()):
        if v in seen: continue
        seen.add(v); c += 1
        for k, t in enumerate([v, 'word ' * 40 + v, 'line one\nline two ' + v + ' trailing', 'prefix text (' + v + ') suffix', v + '\n' + v]):
            items.append({'sec': 'lit', 'tpl': f'{name}#{k}', 'text': t, 'planted': []})
    counts[name] = c
with open(OUT + '.hex', 'w') as h, open(OUT + '.meta.jsonl', 'w') as m:
    for it in items:
        h.write(it['text'].encode().hex() + '\n'); x = dict(it); x.pop('text'); m.write(json.dumps(x) + '\n')
print('distinct literals per file (first file wins a duplicate):', counts, 'distinct', len(seen), 'inputs', len(items))
