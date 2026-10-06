#!/usr/bin/env python3
r"""recompose_gate71.py — re-express an OLD-format platform-doc block (composed on d75bfe2) in develop's NEW table-matrix format
(#1402, KS-571 d, 2026-10-06). It is a PREDICTION instrument: the merge seat's docs merge-in is a RE-COMPOSITION, not a tail append.

THE RULES (inferred from #1402's own conversion, and CALIBRATED: `--calibrate` converts base's old KS-1305 blocks and diffs the
result against develop's converted KS-1305 blocks, byte for byte):
  R1 named entities other than &amp; &lt; &gt; &quot; become their characters (&mdash; -> U+2014, &rarr; -> U+2192, &hellip; ...)
  R2 a structural line (outside a prose holder and outside <pre>) loses its leading indentation
  R3 <p> ... </p>  and  <div class="note"> ... </div>  become  pmatrix tables:
       with a <strong>Lead.</strong>  -> <td class="pm-topic" rowspan="N">LEAD</td> and one row per SENTENCE of the rest
       without                        -> topic = the first sentence, detail = the rest (rowspan="1")
     a sentence ends at [.!?] followed by whitespace and an UPPERCASE letter (never before a tag: `ran. <code>` does not split)
  R4 <h2>N. / <h3>N.k  are renumbered by --num-map OLD:NEW (numbers are by ticket; a renumber is a RULING, never silent)
  R5 <pre> content is verbatim; <table> rows are kept, de-indented
TEXT CONSERVATION: `visible_text(old) == visible_text(new)` (entities decoded, whitespace collapsed, the renumber applied) is
asserted by every caller — the guard's own header names dropped text and merged words as the conversion's known failure modes.
Usage: recompose_gate71.py --calibrate --repo R --base B --develop D | --selftest      rc 0 / 1."""
import html, os, re, sys
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

KEEP_ENT = {'amp', 'lt', 'gt', 'quot'}
SPLIT = re.compile(r'(?<=[.!?])(\s+)(?=[A-Z])')


def unent(s):
    return re.sub(r'&([a-zA-Z]+);', lambda m: m.group(0) if m.group(1) in KEEP_ENT else html.unescape(m.group(0)), s)


def sentences(s):
    """split s into pieces; each piece keeps its trailing whitespace; the next starts at the capital."""
    out, last = [], 0
    for m in SPLIT.finditer(s):
        out.append(s[last:m.end(1)]); last = m.end(1)
    out.append(s[last:])
    return [x for x in out if x != '']


def matrix(content):
    """content = the text between the opening and closing tag of a prose holder (newlines and indentation included)."""
    m = re.match(r'^\s*(<strong>.*?</strong>)(.*)$', content, re.S)
    if m and re.sub(r'<[^>]+>', '', m.group(1)).rstrip().endswith(('.', ':', '?', '!')):
        lead, rest = m.group(1), m.group(2)
        rows = sentences(rest)
        return ('<table class="pmatrix"><tr><td class="pm-topic" rowspan="%d">%s</td>' % (len(rows), lead)
                + '</tr><tr>'.join('<td>%s</td>' % r for r in rows) + '</tr></table>')
    parts = sentences(content)
    if len(parts) < 2:
        return '<table class="pmatrix"><tr><td colspan="2">%s</td></tr></table>' % content
    return '<table class="pmatrix"><tr><td class="pm-topic" rowspan="1">%s</td><td>%s</td></tr></table>' % (parts[0], ''.join(parts[1:]))


def renum(line, num_map):
    def h2(m):
        n = int(m.group(2)); return '%s%d.' % (m.group(1), num_map.get(n, n))
    def h3(m):
        n = int(m.group(2)); return '%s%d.%s' % (m.group(1), num_map.get(n, n), m.group(3))
    line = re.sub(r'^(\s*<h2[^>]*>\s*)(\d+)\.', h2, line)
    return re.sub(r'^(\s*<h3[^>]*>\s*)(\d+)\.(\d+)', h3, line)


def recompose(block, num_map=None):
    """block: the old-format block text (lines joined by \n, no trailing newline required). Returns the new-format text."""
    num_map = num_map or {}
    L = unent(block).split('\n'); out = []; i = 0
    while i < len(L):
        l = L[i]; s = l.strip()
        if re.match(r'<pre\b', s):
            j = i
            while j < len(L) and '</pre>' not in L[j]: j += 1
            if j == len(L): raise ValueError('recompose: <pre> at block line %d has no </pre> in the block' % (i + 1))
            out.append(l.lstrip()); out += L[i + 1:j + 1]; i = j + 1; continue
        if s == '<p>' or s == '<div class="note">':
            close = '</p>' if s == '<p>' else '</div>'
            j = i + 1
            while j < len(L) and L[j].strip() != close: j += 1
            if j == len(L): raise ValueError('recompose: %s at block line %d has no %s line in the block' % (s, i + 1, close))
            content = '\n' + '\n'.join(L[i + 1:j]) + '\n' + L[j][:len(L[j]) - len(L[j].lstrip())]
            m = matrix(content)
            out.append(m if s == '<p>' else '<div class="note">%s</div>' % m); i = j + 1; continue
        out.append(renum(l, num_map).lstrip()); i += 1
    return '\n'.join(out)


def visible_text(s, num_map=None):
    s = unent(s)
    if num_map is not None:
        s = '\n'.join(renum(x, num_map) for x in s.split('\n'))
    s = re.sub(r'<!--.*?-->', ' ', s, flags=re.S); s = re.sub(r'<[^>]+>', ' ', s)
    return re.sub(r'\s+', ' ', html.unescape(s)).strip()


def calibrate(repo, base, develop):
    from lib_gate71 import git_bytes, K
    D = K['docs']; res = []
    for doc, path, start_rx in (('flow', D['flow'], r'<h2>\s*%d\.' ), ('cheat', D['cheat'], None)):
        bt = git_bytes(repo, base, path).decode().split('\n'); dt = git_bytes(repo, develop, path).decode().split('\n')
        if doc == 'flow':
            i = [k for k, l in enumerate(bt) if re.search(r'<h2>\s*22\.', l)][0]; j = [k for k, l in enumerate(dt) if re.search(r'<h2>\s*24\.', l)][0]
        else:
            i = [k for k, l in enumerate(bt) if 'KS-1305</h2>' in l][0] - 1; j = [k for k, l in enumerate(dt) if 'KS-1305</h2>' in l][0] - 1
        e = [k for k, l in enumerate(bt) if l.strip() == '</body>'][0]; f = [k for k, l in enumerate(dt) if l.strip() == '</body>'][0]
        old, new = '\n'.join(bt[i:e]), '\n'.join(dt[j:f])
        got = recompose(old, {22: 24} if doc == 'flow' else {})
        same = got == new
        nd = sum(1 for a, b in zip(got.split('\n'), new.split('\n')) if a != b) + abs(len(got.split('\n')) - len(new.split('\n')))
        vt = visible_text(old, {22: 24} if doc == 'flow' else {}) == visible_text(new)
        print('CALIBRATE %s KS-1305: recompose(base old block) == develop\'s #1402 block BYTE FOR BYTE: %s (%d B vs %d B, %d differing lines) | visible text conserved: %s' % (
            doc, same, len(got.encode()), len(new.encode()), nd, vt))
        if not same:
            for k, (a, b) in enumerate(zip(got.split('\n'), new.split('\n'))):
                if a != b: print('   first diff line %d\n   got: %r\n   dev: %r' % (k + 1, a[:160], b[:160])); break
        res.append(same and vt)
    return 0 if all(res) else 1


def selftest():
    res = []
    def rep(c, m): res.append(bool(c)); print('%s %s' % ('PASS' if c else 'FAIL', m))
    rep(sentences('A b. C d. <code>x</code>. E') == ['A b. ', 'C d. <code>x</code>. ', 'E'], 'sentence split: before a capital, never before a tag')
    m = matrix('\n  <strong>Lead.</strong> One. Two.\n  ')
    rep(m == '<table class="pmatrix"><tr><td class="pm-topic" rowspan="2"><strong>Lead.</strong></td><td> One. </td></tr><tr><td>Two.\n  </td></tr></table>', 'lead paragraph -> topic + one row per sentence')
    m = matrix('\n  First one. Rest here. More.\n  ')
    rep(m.startswith('<table class="pmatrix"><tr><td class="pm-topic" rowspan="1">\n  First one. </td><td>Rest here. More.'), 'lead-less paragraph -> first sentence topic, rest detail')
    rep(renum('  <h2>23. x</h2>', {23: 28}) == '  <h2>28. x</h2>' and renum('<h3>23.4 y</h3>', {23: 28}) == '<h3>28.4 y</h3>', 'renumber h2 / h3 by map')
    old = '  <h2>9. T (KS-1)</h2>\n  <p>\n    <strong>W.</strong> A &mdash; b. C d.\n  </p>\n  <pre><code>x\n  y</code></pre>'
    new = recompose(old)
    rep(visible_text(old) == visible_text(new), 'visible text conserved through recompose')
    rep(visible_text(old) != visible_text(new.replace('C d.', 'C.')), 'PLANTED dropped word: visible-text conservation FAILS')
    rep('<p>' not in new and 'pmatrix' in new and '—' in new and '&mdash;' not in new, 'no <p> left, pmatrix present, &mdash; -> U+2014')
    print('SELFTEST %d/%d' % (sum(res), len(res))); return 0 if all(res) else 1


def main():
    A = sys.argv[1:]
    from lib_gate71 import opt
    if '--selftest' in A: return selftest()
    if '--calibrate' in A and opt(A, '--repo'):
        return calibrate(opt(A, '--repo'), opt(A, '--base', 'd75bfe2deb8075583cfb55af0921e4964e7c6f0e'), opt(A, '--develop'))
    print(__doc__); return 2


if __name__ == '__main__':
    sys.exit(main())
