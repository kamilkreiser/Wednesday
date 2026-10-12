#!/usr/bin/env python3
"""Mutation harness: apply each shape to the governance db.retry test file, run ONLY that file under jest,
record which test cells fail (from jest --json), restore byte-identical (sha asserted). Each edit asserts its anchor."""
import hashlib, json, os, re, subprocess, sys

S = '/private/tmp/claude-501/-Volumes-DevMASTER-WEDNESDAY/f2077cbf-bb12-49ee-8d59-f5f537b335e0/scratchpad'
TREES = {'OLD(develop 69878dc5)': S + '/repodev', 'NEW(head 7624c699)': S + '/repo2'}
REL = 'Blockchain/Dev/services/governance'
FILE = 'src/__tests__/db.retry.test.ts'
ANCHOR = re.compile(r'^jest\.setTimeout\(60_000\);$', re.M)
PIN_NAME_OLD = 'KS-1328: this file sets its own 60 s budget'
PIN_NAME_NEW = 'KS-1328: this file RUNS on its own 60 s budget'

SHAPES = {
    '0_control_unmutated': None,
    '1_deleted': '',
    '2_lowered_30s': 'jest.setTimeout(30_000);',
    '3_multiline_block_comment': '/*\njest.setTimeout(60_000);\n*/',
    '4_template_literal': 'const _tpl = `\njest.setTimeout(60_000);\n`;\nvoid _tpl;',
    '5_in_afterAll': 'afterAll(() => {\njest.setTimeout(60_000);\n});',
    '6_in_beforeAll': 'beforeAll(() => {\njest.setTimeout(60_000);\n});',
    '7_uncalled_function': 'function _neverCalled() {\njest.setTimeout(60_000);\n}\nvoid _neverCalled;',
    '8_false_condition': 'if (Number(1) === 2) {\njest.setTimeout(60_000);\n}',
    # extras of the gate's own
    '9_in_beforeEach_runtime': 'beforeEach(() => {\njest.setTimeout(60_000);\n});',
    '10_legit_late_toplevel_after_describe': '__LATE__',
    '11_legit_indented_toplevel_in_block': '{\njest.setTimeout(60_000);\n}',
}


def sha(b):
    return hashlib.sha256(b).hexdigest()


def run(tree):
    out = S + '/shape_out.json'
    if os.path.exists(out):
        os.remove(out)
    p = subprocess.run(
        [S + '/' + os.path.basename(tree) + '/Blockchain/Dev/node_modules/.bin/jest', '--json', '--outputFile=' + out,
         FILE],
        cwd=tree + '/' + REL, capture_output=True, text=True)
    d = json.load(open(out))
    fails, passes, other = [], 0, []
    for tr in d['testResults']:
        if tr.get('message') and not tr['assertionResults']:
            other.append(tr['message'][:300])
        for a in tr['assertionResults']:
            if a['status'] == 'failed':
                fails.append(a['title'])
            elif a['status'] == 'passed':
                passes += 1
    return p.returncode, passes, fails, other, d['numTotalTests'], (d['testResults'][0].get('message') or '')[:600]


results = {}
for tname, tree in TREES.items():
    path = tree + '/' + REL + '/' + FILE
    orig = open(path, 'rb').read()
    h0 = sha(orig)
    text = orig.decode()
    assert len(ANCHOR.findall(text)) == 1, 'anchor count != 1 in ' + tname
    pin = PIN_NAME_OLD if tname.startswith('OLD') else PIN_NAME_NEW
    for sname, repl in SHAPES.items():
        if repl is None:
            new = text
        elif repl == '__LATE__':
            assert text.rstrip().endswith('});')
            new = ANCHOR.sub('', text, count=1) + '\njest.setTimeout(60_000);\n'
        else:
            new = ANCHOR.sub(lambda m: repl, text, count=1)
        if repl is not None:
            assert new != text, 'mutation did not change file: ' + sname
        open(path, 'wb').write(new.encode())
        try:
            landed = sha(open(path, 'rb').read()) != h0 if repl is not None else sha(open(path, 'rb').read()) == h0
            assert landed, 'tamper state not as expected: ' + sname
            rc, passes, fails, other, total, msg = run(tree)
        finally:
            open(path, 'wb').write(orig)
        assert sha(open(path, 'rb').read()) == h0, 'RESTORE FAILED ' + sname
        results.setdefault(sname, {})[tname] = dict(rc=rc, total=total, passes=passes, fails=fails, load_errors=other,
                                                      pin_red=any(f.startswith(pin) for f in fails),
                                                      only_pin_red=(len(fails) == 1 and fails[0].startswith(pin)),
                                                      msg=msg if (fails or other) else '')
        print(sname, tname, 'rc', rc, 'total', total, 'fails', [f[:50] for f in fails], 'load_err', len(other),
              flush=True)
    assert sha(open(path, 'rb').read()) == h0
json.dump(results, open(S + '/shapes_results.json', 'w'), indent=1)
print('ALL RESTORED OK')
