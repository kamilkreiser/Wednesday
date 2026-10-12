#!/usr/bin/env python3
"""Symbol-lookup falsification on the NEW pin (head tree): zero, several, wrong field, wrong-type state."""
import hashlib, json, os, re, subprocess

S = '/private/tmp/claude-501/-Volumes-DevMASTER-WEDNESDAY/f2077cbf-bb12-49ee-8d59-f5f537b335e0/scratchpad'
tree = S + '/repo2'
REL = 'Blockchain/Dev/services/governance'
FILE = 'src/__tests__/db.retry.test.ts'
path = tree + '/' + REL + '/' + FILE
sha = lambda b: hashlib.sha256(b).hexdigest()
orig = open(path, 'rb').read(); h0 = sha(orig); text = orig.decode()

def sub(old, new):
    assert text.count(old) == 1, ('anchor count', old, text.count(old))
    return text.replace(old, new)

ANCH = "jest.setTimeout(60_000);\n"
SHAPES = {
    'Z0_control': text,
    'Z1_zero_symbols(description renamed, as a jest rename would)': sub("sym.description === 'JEST_STATE_SYMBOL'", "sym.description === 'JEST_STATE_SYMBOL_RENAMED'"),
    'Z2_two_symbols(second one also 60000)': sub(ANCH, ANCH + "(globalThis as any)[Symbol('JEST_STATE_SYMBOL')] = { testTimeout: 60_000 };\n"),
    'Z3_two_symbols(second one 10000)': sub(ANCH, ANCH + "(globalThis as any)[Symbol('JEST_STATE_SYMBOL')] = { testTimeout: 10_000 };\n"),
    'Z4_state_field_renamed(state exists, no testTimeout)': sub("testTimeout?: unknown", "testTimeout?: unknown").replace("states[0]?.testTimeout", "(states[0] as any)?.testTimeoutRenamed"),
}
out = {}
for name, new in SHAPES.items():
    open(path, 'wb').write(new.encode())
    try:
        assert (sha(open(path, 'rb').read()) == h0) == (name == 'Z0_control'), 'tamper state wrong'
        jp = S + '/sym_out.json'
        if os.path.exists(jp): os.remove(jp)
        p = subprocess.run([tree + '/Blockchain/Dev/node_modules/.bin/jest', '--json', '--outputFile=' + jp, FILE],
                           cwd=tree + '/' + REL, capture_output=True, text=True)
        d = json.load(open(jp))
        fails = [(a['title'][:40], re.sub(r'\x1b\[[0-9;]*m', '', ' '.join(a['failureMessages'])[:260])) for tr in d['testResults'] for a in tr['assertionResults'] if a['status'] == 'failed']
        msg = re.sub(r'\x1b\[[0-9;]*m', '', d['testResults'][0].get('message') or '')
        out[name] = dict(rc=p.returncode, total=d['numTotalTests'], failed=fails, suite_msg=msg[:300] if not fails and p.returncode else '')
    finally:
        open(path, 'wb').write(orig)
    assert sha(open(path, 'rb').read()) == h0
    print(name, 'rc', out[name]['rc'], 'total', out[name]['total'], 'nfail', len(out[name]['failed']))
    for t, m in out[name]['failed']:
        i = m.find('Expected'); print('    ', t, '|', ' '.join(m[i:i + 110].split()))
    if out[name]['suite_msg']: print('    SUITE:', out[name]['suite_msg'][:200])
json.dump(out, open(S + '/symbol_results.json', 'w'), indent=1)
print('RESTORED OK')
