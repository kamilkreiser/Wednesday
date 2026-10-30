#!/usr/bin/env python3
"""loosegen.py <specX.py> [dir-suffix]  - build the LOOSE (rung 4) twin of an existing spec with mk2.build.
The product diff is NOT given in the brief: the model writes the product lines from `## What is wrong` / `## Where`; the new test is still given whole.
To avoid the hunk-arithmetic failure of ks_1240_p9 (the A2a off-by-one), every hunk's header and its unchanged context lines are DICTATED (the p9b shape), generated from the
golden diff, not typed. The twin lands in night/briefs/<dir><suffix>/ (default suffix _loose); it is a CALIBRATION of the Spark, not a second candidate for the same ticket.
Honours GEN_BRIEFS / GEN_TIP / GEN_OVERWRITE like mk.py."""
import sys, os, re, importlib.util
HERE = os.path.dirname(os.path.abspath(__file__)); sys.path.insert(0, HERE)
import mk21 as mk2
def load(path):
    sp = importlib.util.spec_from_file_location('s', path); m = importlib.util.module_from_spec(sp); sp.loader.exec_module(m); return m
def product_hunks(S):
    out = []
    for path, edits in S['products']:
        old = mk2.rd(path); new = old
        for e in edits:
            if callable(e): new = e(new); continue
            o, n = e; assert new.count(o) == 1, (path, o[:50]); new = new.replace(o, n)
        d = mk2.udiff(path, old, new).split('\n')
        hunks = []; cur = None
        for l in d:
            if l.startswith('@@'): cur = [l, []]; hunks.append(cur)
            elif cur is not None and l != '' : cur[1].append(l)
        out.append((path, hunks))
    return out
def dictation(S):
    t = ["**HUNK HEADERS ARE DICTATED (a loose brief's weak point is the hunk arithmetic: copy the headers, do not recount).** The product edit has the following hunks, in this order. For each: the header is exact, the `-` lines are the old file's lines you remove (shown), the context lines are unchanged (shown, each starts with one space in your diff), and the `+` lines are YOURS to write from the contract above.\n"]
    k = 0
    for path, hunks in product_hunks(S):
        for h, lines in hunks:
            k += 1
            pre = []; minus = []; plus = 0; post = []; state = 0
            for l in lines:
                if l.startswith(' '):
                    (pre if state == 0 else post).append(l[1:]); 
                elif l.startswith('-'): minus.append(l[1:]); state = 1
                elif l.startswith('+'): plus += 1; state = 1
            t.append(f"- Hunk {k}, file `{path}`: header exactly `{h}`.")
            t.append("  - unchanged lines BEFORE your change (verbatim): " + (" | ".join('`%s`' % x for x in pre) if pre else "none"))
            t.append("  - old lines you REMOVE (verbatim): " + (" | ".join('`%s`' % x for x in minus) if minus else "none (insert only)"))
            t.append(f"  - lines you ADD: {plus}")
            t.append("  - unchanged lines AFTER your change (verbatim): " + (" | ".join('`%s`' % x for x in post) if post else "none"))
    t.append("\nA hunk's old count is its unchanged-before + removed + unchanged-after lines; its new count is unchanged-before + added + unchanged-after. The header above already says it.")
    return "\n".join(t)
if __name__ == '__main__':
    m = load(sys.argv[1]); S = dict(m.S); suf = sys.argv[2] if len(sys.argv) > 2 else '_loose'
    S['dir'] = S['dir'] + suf
    S['title'] = S['title'] + ' [LOOSE twin: calibration only, not a second candidate]'
    S['intro'] = S['intro'] + " THIS IS THE LOOSE (rung 4) TWIN of `%s`: the product diff is not given, the headers are dictated. It exists to measure the Spark, NOT to be raised; the dictated twin's golden is the same patch." % m.S['dir']
    S['rung'] = '4 (LOOSE twin: product lines written by the model, hunk headers dictated; the new test given whole)'
    S['rung_raw'] = '**' + S['rung'] + '**'
    S['loose'] = "The product edit is described by behaviour in `## What is wrong` and `## Where`; no diff and no `+` line is given for it. Write it yourself: minimal, only what those two sections require.\n\n" + dictation(m.S)
    if os.environ.get('LOOSE_EXTRA'): S['loose'] += "\n\n" + os.environ['LOOSE_EXTRA']   # a re-brief line (e.g. the new-file header form), recorded in the brief
    mk2.build(S)
