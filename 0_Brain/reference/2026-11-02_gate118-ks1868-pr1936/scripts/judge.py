import json
W = '/Volumes/DevMASTER/WEDNESDAY/0_Brain/reference/2026-11-02_gate118-ks1868-pr1936'
H = json.load(open(W + '/logs/probe_head.json')); B = json.load(open(W + '/logs/probe_base.json'))
print('unhandled(total) head', H['unhandled'], 'base', B['unhandled'], 'cells', len(H['cells']), len(B['cells']))
idx = lambda d: {(c['route'], c['kind'], c['point']): c for c in d['cells']}
h, b = idx(H), idx(B)
assert set(h) == set(b)
READ = ['error', 'error23505', 'errorOtherCode', 'string']
UNR = ['revokedProxy', 'msgGetterThrows', 'msgGetterThrowsRevoked', 'codeGetterThrows', 'codeGetterThrowsRevoked', 'toPrimitiveThrows']
OTHER = ['nullValue', 'code23505MsgThrows']
def obs(c, logs=True):
    o = (c['status'], c['body'], c['keyIssued'], c['keyMatchesHash'], json.dumps(c['stmts']), c['infos'], c['unhandled'])
    return o + ((tuple(c['errs']),) if logs else ())
checks = fails = 0
def chk(name, ok):
    global checks, fails
    checks += 1
    if not ok: fails += 1; print('FAIL', name)
for key in sorted(h):
    r, k, p = key
    # A: every readable value, and the control points, are byte-identical base -> head (incl. log)
    if k in READ or p in ('none', 'rowcount0'):
        chk(f'A {key} base==head', obs(h[key]) == obs(b[key]))
    if k in UNR:
        ref_b, ref_h = b[(r, 'error', p)], h[(r, 'error', p)]
        # B: head unreadable == ordinary Error (no code) at base, response + statements + key + unhandled
        chk(f'B {key} head==baseError (no log)', obs(h[key], False) == obs(ref_b, False))
        chk(f'B {key} head==headError (no log)', obs(h[key], False) == obs(ref_h, False))
        # B2: no unreadable shape answers 409 at head
        chk(f'B2 {key} not 409', h[key]['status'] != 409)
        # B3: log line: constant, or (code-getter only) exactly the ordinary Error's log
        if k.startswith('codeGetter'):
            chk(f'B3 {key} log==baseError log', h[key]['errs'] == ref_b['errs'])
        else:
            chk(f'B3 {key} log constant', all('unreadable thrown value' in e for e in h[key]['errs']) and len(h[key]['errs']) == 1)
        chk(f'B4 {key} unhandled 0 at head', h[key]['unhandled'] == 0)
    # C: one write statement, issued once, in every scenario at both versions
    chk(f'C {key} one stmt head', len(h[key]['stmts']) == 1)
    chk(f'C {key} one stmt base', len(b[key]['stmts']) == 1)
    chk(f'C {key} stmt sql/values base==head', h[key]['stmts'] == b[key]['stmts'])
print('checks', checks, 'fails', fails)
rows = []
for key in sorted(h, key=lambda x: (x[0], x[2], x[1])):
    hb, hh = b[key], h[key]
    f = lambda c: f"{c['status']}{' key' if c['keyIssued'] else ''} unh={c['unhandled']} log={c['errs'][0] if c['errs'] else '-'}"
    rows.append(f"{key[0]:8s} | {key[2]:9s} | {key[1]:24s} | base: {f(hb)} | head: {f(hh)}")
open(W + '/logs/probe_table.log', 'w').write('\n'.join(rows) + '\n')
