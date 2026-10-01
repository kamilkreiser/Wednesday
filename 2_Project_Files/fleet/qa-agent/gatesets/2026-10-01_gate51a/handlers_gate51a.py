#!/usr/bin/env python3
"""handlers_gate51a.py — the drafter's PREDICTION for requirement 3 (THE RUNTIME TRUTH): for each of the 11 operations in kit.json `operations`, read
the handler at the HEAD (blob from the SCRATCH clone) and print file:line for (a) the route registration, (b) the validator applied to req.body
(within 12 lines of the route), (c) the schema's fields with which are REQUIRED (a zod field line without .optional() / .default( / .nullish();
for a TRUTHY check, the named field), then a verdict REJECTS-EMPTY when at least one field is required (an absent JSON body reaches the handler
as {} under express.json() — body-parser 1.x sets `req.body = req.body || {}`), else ACCEPTS-EMPTY. Also prints each service's express.json
mount line and the express / body-parser versions the root lock resolves at the head.
CONTROL (kit.json control_operations): PATCH /api/platform/tenants/{id}, which the PR body LEAVES OUT because its partial-update schema accepts {}
— the SAME instrument must read ACCEPTS-EMPTY there. A verdict that matches its expectation is OK; any other is a FAIL.
This is a static reading. It is NOT a request: the gate reads each handler itself and cites file:line at the head.
Overrides (controls): --tree <sha> (read the handlers at another commit). rc 0 PASS / rc 1 FAIL. Usage: handlers_gate51a.py <scratchpad> [--tree sha]"""
import json, os, re, subprocess, sys
G = os.path.dirname(os.path.abspath(__file__)); K = json.load(open(os.path.join(G, 'kit.json'), encoding='utf-8'))
A = sys.argv[1:]; SP = A[0]
P = json.load(open(os.path.join(G, 'pins_gate51a.json'), encoding='utf-8'))
CL = os.path.join(SP, 'g51a_sp', 'clone'); T = A[A.index('--tree') + 1] if '--tree' in A else P['pr_pins']['head']
def show(path):
    r = subprocess.run(['git', '-C', CL, 'show', '%s:%s' % (T, path)], capture_output=True, text=True)
    if r.returncode: raise SystemExit('REFUSING: git show %s:%s rc %d' % (T[:12], path, r.returncode))
    return r.stdout.splitlines()
def first(lines, needle, start=0):
    for i in range(start, len(lines)):
        if needle in lines[i]: return i
    return None
def fields(lines, i):
    """the z.object({ ... }) block opening at line i: (name, required, lineno) per top-level field"""
    out = []; depth = 0
    for j in range(i, min(i + 60, len(lines))):
        l = lines[j]
        if j > i and depth == 1:
            m = re.match(r'^\s*([A-Za-z_][A-Za-z0-9_]*)\s*:\s*(z\..*|[A-Za-z_].*)$', l)
            if m:
                opt = bool(re.search(r'\.optional\(\)|\.default\(|\.nullish\(\)|\.partial\(\)', l))
                k = j; tail = l
                while not opt and k + 1 < len(lines) and not re.search(r',\s*(//.*)?$', tail) and k < j + 5:
                    k += 1; tail = lines[k]; opt = bool(re.search(r'\.optional\(\)|\.default\(|\.nullish\(\)', tail))
                out.append((m.group(1), not opt, j + 1))
        depth += l.count('{') - l.count('}')
        if j > i and depth <= 0: break
    return out
print('handlers_gate51a | tree %s | clone %s' % (T[:12], CL))
lock = json.loads('\n'.join(show('Blockchain/Dev/package-lock.json')))
print('RUNTIME root lock at %s: express %s | body-parser %s' % (T[:12], lock['packages'].get('node_modules/express', {}).get('version'), lock['packages'].get('node_modules/body-parser', {}).get('version')))
for svc, f in K['express_json'].items():
    ls = show(f); i = first(ls, 'express.json(')
    print('MOUNT %s: %s:%s %s' % (svc, f, i + 1 if i is not None else 'ABSENT', ls[i].strip() if i is not None else ''))
bad = []; rows = []
for o in K['operations'] + K.get('control_operations', []):
    want = o.get('expect', 'REJECTS-EMPTY'); ls = show(o['file']); r = first(ls, o['route'])
    if r is None: bad.append('%s route anchor absent' % o['id']); print('FAIL %s %s: route anchor %r ABSENT in %s' % (o['id'], o['op'], o['route'], o['file'])); continue
    v = first(ls, o['validator'], r)
    if v is None or v - r > 12: bad.append('%s validator not within 12 lines' % o['id']); print('FAIL %s %s: validator %r not within 12 lines of %s:%d' % (o['id'], o['op'], o['validator'], o['file'], r + 1)); continue
    sc = o['schema']
    if sc.startswith('TRUTHY:'):
        fl = [(sc.split(':', 1)[1], True, v + 1)]; how = 'truthy check'
        status = ' '.join(ls[v:v + 2]); four = '400' in status
    elif sc.startswith('INLINE1:'):
        body = sc.split(':', 1)[1]; fl = [(m.group(1), not bool(re.search(r'\.optional\(\)', m.group(0))), v + 1) for m in re.finditer(r'([A-Za-z_]+):\s*z\.[^,}]*', body)]; how = 'inline zod .parse'; four = True
    elif sc.startswith('INLINE:'):
        s = first(ls, 'z.object({', r)
        fl = fields(ls, s) if s is not None and s < v else []; how = 'inline zod .safeParse'; four = '400' in ' '.join(ls[v:v + 3])
    else:
        sl = show(o['schema_file']); s = first(sl, sc)
        fl = fields(sl, s) if s is not None else []; how = 'named zod %s' % ('.safeParse' if 'safeParse' in o['validator'] else '.parse')
        four = '400' in ' '.join(ls[v:v + 3]) or 'parse(req.body)' in ls[v]
    req = [n for n, q, _ in fl if q]; verdict = 'REJECTS-EMPTY' if req and four else 'ACCEPTS-EMPTY'
    ok = verdict == want
    if not ok: bad.append('%s reads %s, want %s' % (o['id'], verdict, want))
    print('%s %s %s | route %s:%d | validator :%d (%s) | fields %s | required %s | %s (want %s)%s' % (
        'OK  ' if ok else 'FAIL', o['id'], o['op'], o['file'].replace('Blockchain/Dev/services/', ''), r + 1, v + 1, how,
        ['%s%s:%d' % (n, '' if q else '?', ln) for n, q, ln in fl], req or 'NONE', verdict, want, '  <- CONTROL' if 'expect' in o else ''))
    rows.append(o['id'])
n_ops = len(K['operations']); n_ok = n_ops - sum(1 for b in bad if not b.startswith('TENANT'))
print('HANDLERS %s: %d of %d operations REJECTS-EMPTY at %s | control %s | %d FAIL' % (
    'PASS' if not bad else 'FAIL', sum(1 for o in K['operations'] if o['id'] in rows and not any(b.startswith(o['id'] + ' ') for b in bad)), n_ops, T[:12],
    ', '.join('%s %s' % (c['id'], 'OK' if not any(b.startswith(c['id']) for b in bad) else 'FAIL') for c in K.get('control_operations', [])) or 'none', len(bad)))
for b in bad: print('  - ' + b)
raise SystemExit(1 if bad else 0)
