# QA-POLICY-NEXT item 6: (1) every base line of POLICY.md outside the two changed ranges is present, in order, at the
# head; list every base line NOT kept as-is; (2) the docs_name_the_owner_origin phrases at base and head, each counted
# in the head POLICY.md. usage: python3 -B -I docs_check.py base.md head.md t25_base.rs t25_head.rs
import sys, difflib, re, ast
b = open(sys.argv[1]).read().split('\n'); h = open(sys.argv[2]).read().split('\n')
sm = difflib.SequenceMatcher(a=b, b=h, autojunk=False)
removed = []
for tag, i1, i2, j1, j2 in sm.get_opcodes():
    if tag in ('replace', 'delete'): removed += list(range(i1 + 1, i2 + 1))
print('base lines', len(b), 'head lines', len(h), 'base lines not kept as-is:', removed)
def ranges(xs):
    out = []
    for x in xs:
        if out and x == out[-1][1] + 1: out[-1][1] = x
        else: out.append([x, x])
    return out
print('as ranges:', ranges(removed))
if len(sys.argv) > 3:
    def phrases(p):
        s = open(p).read()
        a = s.index('fn docs_name_the_owner_origin'); a = s.index('for phrase in [', a); e = s.index('] {', a)
        body = s[a + len('for phrase in ['):e]
        body = '\n'.join(l for l in body.split('\n') if not l.strip().startswith('//'))
        out = []
        for m in re.finditer(r'"((?:[^"\\]|\\.)*)"', body):
            out.append(ast.literal_eval('"' + m.group(1) + '"'))
        return out
    pb, ph = phrases(sys.argv[3]), phrases(sys.argv[4])
    doc = open(sys.argv[2]).read()
    print('phrases base', len(pb), 'head', len(ph), 'base phrases are the head list prefix:', ph[:len(pb)] == pb)
    for x in ph[len(pb):]:
        print('  added, count in head POLICY.md =', doc.count(x), ':', x[:90])
    print('  old phrases each still present:', all(doc.count(x) >= 1 for x in pb), [x[:50] for x in pb if doc.count(x) < 1])
