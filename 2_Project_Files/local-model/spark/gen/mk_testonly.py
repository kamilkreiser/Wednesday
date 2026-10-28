#!/usr/bin/env python3
"""mk_testonly.py <spec.py> - build a TEST-ONLY (tier test_only) brief: ONE existing test modified in place, a planted tamper in the product proves the new cell can go red.
Spec T = dict(dir, ticket, title, intro, product, test, ref, tamper_line, tamper_from, tamper_to, statement_ok, edit=(old,new) on the test file, red=[cell titles], controls=[...],
what_wrong, where, unmeasured, scope, runner). Output: night/briefs/<dir>/{KS-n.md,golden.diff,spark.pins}. Honours GEN_BRIEFS/GEN_TIP/GEN_OVERWRITE (see mk.py)."""
import sys, os, importlib.util
HERE = os.path.dirname(os.path.abspath(__file__)); sys.path.insert(0, HERE)
import mk2
def build(T):
    old = mk2.rd(T['test']); new = old
    # op5 2026-10-28: T['edit'] may be ONE (old,new) tuple (unchanged) or a LIST of them (several hunks in the one test file)
    for o, n in ([T['edit']] if isinstance(T['edit'], tuple) else T['edit']):
        assert old.count(o) == 1, 'edit anchor not unique'
        new = new.replace(o, n)
    prod = mk2.rd(T['product']).split('\n')
    assert prod[T['tamper_line'] - 1] == T['tamper_from'], (prod[T['tamper_line'] - 1], T['tamper_from'])
    diff = mk2.udiff(T['test'], old, new)
    d = mk2.BR + T['dir']
    if os.path.exists(d + '/golden.diff') and not os.environ.get('GEN_OVERWRITE'): sys.exit('REFUSED: %s exists (GEN_OVERWRITE=1 to replace)' % d)
    os.makedirs(d, exist_ok=True)
    open(d + '/golden.diff', 'w', encoding='utf-8').write(diff)
    open(d + '/spark.pins', 'w').write(f"# test_only: ONE existing test modified in place, the tamper planted in the product by the checker; line = the tamper line at the tip.\ntier=test_only\ntest_file={T['test']}\nref={T['ref']}\nline={T['tamper_line']}\n")
    k = T['ticket']
    s = f"# {k} {T['title']}\n\n{T['intro']}\n\nFile: `{T['product']}`  (product, NOT modified: it is the tamper target only)\nTest file: `{T['test']}`  (EXISTING, modified in place: {T.get('nh_txt', '1 hunk, the new cell added at the end of an existing describe')})\n"
    s += f"Tip: `{mk2.TIP}` (origin/develop by `git ls-remote` on 2026-10-28; every line number and quote below was read from the cache clone at exactly this sha)\nRunner: `{T['runner']}`\nTier: `test_only` (the `## Tamper` block below)\nRung: **{T['rung']}**\n\n"
    s += "## The mode - read this twice\n\nTEST-ONLY, MODIFY IN PLACE. Your diff contains EXACTLY ONE file: the EXISTING test file above, with the ordinary header `--- a/...` / `+++ b/...` and " + T.get('nh_word', 'ONE hunk') + ". **No hunk for the product file.** Do NOT create a new test file. The checker reddens your new cell by planting the tamper named below into a clone of the product file, then expects the test file GREEN at the untouched tip. A diff that touches the product file is refused at A3.\n\n"
    s += "## What is wrong (one paragraph)\n\n" + T['what_wrong'] + "\n\n## Where\n\n" + T['where'] + "\n\n"
    s += "## The exact change - " + T.get('nh_head', 'ONE EDIT in the TEST file (one hunk)') + "\n\nApply this hunk to the EXISTING test file. The `+` lines are byte-exact: copy them; do not paraphrase a comment, do not re-indent.\n\n```diff\n" + diff.split('+++ b/' + T['test'] + '\n', 1)[1] + "```\n\n"
    s += f"## Tamper (test-only mode - the checker plants this in a clone of the product file to prove your cell can go red)\nline: {T['tamper_line']}\nfrom: `{T['tamper_from']}`\nto: `{T['tamper_to']}`\nstatement_ok: {T['statement_ok']}\n\n"
    s += "## Red cells\n" + ''.join(f"- {c}\n" for c in T['red']) + "\n## Cells and controls\n\n" + T['cells'] + "\n\n"
    s += "## UNMEASURED - stated rather than glossed\n\n" + T['unmeasured'] + "\n\n## Scope\n\n" + T['scope'] + "\n\n"
    s += "## Output\n\nExactly ONE fenced ```diff block, nothing outside it: one file section (the test file). Every `+` line on its own physical line. Every context line keeps its leading space. Count the hunk header: old and new line counts must match the hunk body.\n"
    open(d + f'/{k}.md', 'w', encoding='utf-8').write(s)
    print('wrote', d, len(diff), 'bytes golden')
if __name__ == '__main__':
    sp = importlib.util.spec_from_file_location('s', sys.argv[1]); m = importlib.util.module_from_spec(sp); sp.loader.exec_module(m); build(m.T)
