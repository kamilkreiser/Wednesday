# QA-AUDIT-EMAIL: own extractor of every fn body and pub const of redact.rs (property a).
# Usage: python3 -B qa_bodies.py <old file> <new file>
import sys, re, hashlib
def mask_lits(s):
    # replace contents of comments, strings, chars by spaces (same length) so braces inside do not count
    out = list(s); i = 0; n = len(s)
    while i < n:
        c = s[i]
        if s.startswith('//', i):
            j = s.find('\n', i); j = n if j < 0 else j
            for k in range(i, j): out[k] = ' '
            i = j; continue
        if s.startswith('/*', i):
            j = s.find('*/', i + 2) + 2
            for k in range(i, j): out[k] = ' ' if s[k] != '\n' else '\n'
            i = j; continue
        m = re.match(r"b?r(#*)\"", s[i:])
        if m and (i == 0 or not (s[i-1].isalnum() or s[i-1] == '_')):
            close = '"' + m.group(1); j = s.find(close, i + len(m.group(0))) + len(close)
            for k in range(i, j): out[k] = ' ' if s[k] != '\n' else '\n'
            i = j; continue
        if c == '"':
            j = i + 1
            while s[j] != '"':
                j += 2 if s[j] == '\\' else 1
            for k in range(i, j + 1): out[k] = ' ' if s[k] != '\n' else '\n'
            i = j + 1; continue
        if c == "'":
            m = re.match(r"'(\\.[^']*|[^\\'])'", s[i:])
            if m:
                for k in range(i, i + len(m.group(0))): out[k] = ' '
                i += len(m.group(0)); continue
        i += 1
    return ''.join(out)
def items(src):
    ms = mask_lits(src); res = {}
    for m in re.finditer(r'(?m)^[ \t]*(pub(\([a-z]+\))? )?fn ([a-z_0-9]+)', ms):
        name = m.group(3); i = ms.index('{', m.end()); d = 0; j = i
        while True:
            if ms[j] == '{': d += 1
            elif ms[j] == '}':
                d -= 1
                if d == 0: break
            j += 1
        key = 'fn ' + name
        while key in res: key += "'"
        res[key] = src[m.start():j + 1]
    for m in re.finditer(r'(?m)^[ \t]*pub const ([A-Z_0-9]+)', ms):
        j = ms.index(';', m.end()); res['const ' + m.group(1)] = src[m.start():j + 1]
    return res
a = items(open(sys.argv[1]).read()); b = items(open(sys.argv[2]).read())
diff = 0
for k in sorted(set(a) | set(b)):
    ha = hashlib.sha256(a[k].encode()).hexdigest() if k in a else '-'
    hb = hashlib.sha256(b[k].encode()).hexdigest() if k in b else '-'
    st = 'same' if ha == hb else ('NEW ' if ha == '-' else ('GONE' if hb == '-' else 'DIFF'))
    if st != 'same': diff += 1
    print(f'{st} {k:28} {ha[:16]} {hb[:16]}')
print('fns', sum(k.startswith('fn') for k in a), sum(k.startswith('fn') for k in b), 'consts', sum(k.startswith('const') for k in a), sum(k.startswith('const') for k in b), 'not same:', diff)
