# QA-AUDIT-EMAIL-3 byte scan (new; tool outside the repository). Words come ONLY from the command line
# (after `--`), never from a file. Each word is searched plain, slugged, URL-encoded (three ways),
# backslash-escaped and as UTF-16LE, in any letter case. Output names the word by its index only.
# Usage: python3 -I -B qa3_scan.py <label>=<file> ... -- <word> ...
import sys, re, urllib.parse
a = sys.argv[1:]; k = a.index('--'); files = a[:k]; words = [w for w in a[k + 1:] if len(w) >= 3]
def forms(w):
    out = {w, re.sub(r'[^a-z0-9]+', '-', w.lower()).strip('-'), urllib.parse.quote(w), urllib.parse.quote(w, safe=''),
           urllib.parse.quote_plus(w), re.sub(r'([ !()&\'"$])', r'\\\1', w)}
    out = {f for f in out if len(f) >= 3}
    return [f.encode().lower() for f in out] + [f.encode('utf-16-le').lower() for f in {w}]
F = [(i, forms(w)) for i, w in enumerate(words)]
tot = 0
for spec in files:
    label, path = spec.split('=', 1)
    data = open(path, 'rb').read(); low = data.lower()
    lines = data.split(b'\n'); starts = [0]
    for l in lines: starts.append(starts[-1] + len(l) + 1)
    import bisect
    hits = {}
    for i, fs in F:
        for f in fs:
            p = low.find(f)
            while p >= 0:
                ln = bisect.bisect_right(starts, p)
                hits.setdefault((ln, i), lines[ln - 1][:110] if b'\x00' not in lines[ln - 1][:110] else b'<binary>')
                p = low.find(f, p + 1)
    tot += len(hits)
    print(f'{label}: {len(hits)} hits (line, word#)')
    for (ln, i), txt in sorted(hits.items()):
        print(f'   {label}:{ln} word#{i}')
print('total', tot, 'words', len(words))
