#!/usr/bin/env python3
"""c5_handler_gate55.py — gate55 C5: the spec now declares what the HANDLER returns. READ ONLY on git objects (show / cat-file / rev-parse);
prints only. Every claim prints file:line at the head so the gate can quote it.
  H0  THE RUNTIME DID NOT MOVE: every kit runtime_unchanged file (the handler, the chain service, its types, the transfer index, the shared
      response schemas) is blob-equal base == head — the PR changes the CONTRACT, never the behaviour it describes.
  H1  THE HANDLER: exactly ONE `router.get('/:id',` in routes/delegations.ts; its body printed as a line range.
  H2  SUCCESS SHAPE emitted: inside that body, the res.json literal with `success: true` and `data: { delegation, chain }`, and `chain` bound to
      `delegationService.buildDelegationChain(delegation)` — each with file:line.
  H3  ERROR PATHS reaching this handler: the handler's own `res.status(404).json({ success: false, error: { code: 'NOT_FOUND', message } })`;
      and in services/transfer/src/index.ts `app.use('/api', jwtAuthenticate())` registered BEFORE `app.use('/api/delegations', ...)` (so a
      bad token is a 401 from the shared middleware before the handler runs) — file:line each.
  H4  THE CHAIN the service returns: the keys of buildDelegationChain()'s `return {` literal, and the `interface DelegationChain` fields with
      their optionality (`?`) and TS types.
  H5  THE SPEC at head (the YAML, parsed): GET /api/delegations/{id} 200 is NOT a bare $ref; required [success, data]; success enum [true];
      data.required {delegation, chain}; data.delegation $ref Delegation; chain.properties == H4's return keys, chain.required == H4's
      NON-optional fields, each type consistent with the TS type (string/string, number/integer, boolean/boolean, X[]/array).
  H6  THE ERROR SHAPES: each status this handler path can emit (401, 404) is declared and references ErrorResponse, whose schema requires
      success (enum [false]) and error {code, message} — the keys H3 found in the handler's literal.
  H7  MUST-HIT CONTROL: the H5 comparator applied to the BASE yaml MUST FAIL (base declared the bare Delegation — the drift KS-1015 names).
  INFO statuses declared but not emitted by this handler (pre-existing); async handler with no try/catch on Express 4 (READ ONLY, pre-existing);
       the Delegation component's required set vs the TS `interface Delegation` (pre-existing, unchanged by this PR).
--selftest: H5/H6 on SIM-mutated copies of the parsed head spec (each must fail) and on the real head (must pass).
Usage: c5_handler_gate55.py --repo <clone or checkout> [--base sha] [--head sha] [--selftest]   rc 0 PASS / 1 FAIL / 2 usage"""
import copy, io, contextlib, json, os, re, sys
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from lib_gate55 import K, now, Checks, has_commit, show, blob_id
try:
    import yaml
    YL = getattr(yaml, 'CSafeLoader', yaml.SafeLoader)
except ImportError:
    print('REFUSING: python3 has no PyYAML (`python3 -c "import yaml"`); this instrument parses the spec — say NOT RUN, or use your own parser'); raise SystemExit(2)

A = sys.argv[1:]
if not A or '--help' in A or '-h' in A or '--repo' not in A:
    print(__doc__); raise SystemExit(0 if ('--help' in A or '-h' in A) else 2)
def opt(n, d=None): return A[A.index(n) + 1] if n in A else d
REPO = opt('--repo'); BASE = opt('--base', K['base']); HEAD = opt('--head', K['expected_head'])
for s in (BASE, HEAD):
    if not re.fullmatch(r'[0-9a-f]{40}', s) or not has_commit(REPO, s): print('REFUSING: %s is not a 40-hex commit in %s' % (s, REPO)); raise SystemExit(2)
PATH, METHOD = K['spec_operation']; SHORT = lambda p: p.split('/src/')[-1] if '/src/' in p else p

def lines(sha, f):
    t = show(REPO, sha, f)
    if t is None: raise SystemExit('REFUSING: %s absent at %s' % (f, sha[:12]))
    return t.split('\n')

def read_handler():
    L = lines(HEAD, K['handler_file']); rx = re.compile(K['handler_route_rx'])
    hits = [i for i, l in enumerate(L) if rx.search(l)]
    if len(hits) != 1: return L, hits, None, None
    s = hits[0]; e = next((i for i in range(s + 1, len(L)) if re.match(r'^(router\.|/\*\*)', L[i])), len(L)) - 1
    while e > s and not L[e].strip(): e -= 1
    return L, hits, s, e

def chain_contract():
    S = lines(HEAD, K['chain_service_file']); T = lines(HEAD, K['chain_types_file'])
    i = next((k for k, l in enumerate(S) if re.search(r'async buildDelegationChain\(', l)), None)
    keys = []; rline = None
    if i is not None:
        for k in range(i, len(S)):
            if re.match(r'^\s*return \{\s*$', S[k]):
                rline = k
                for m in range(k + 1, len(S)):
                    if re.match(r'^\s*\};?\s*$', S[m]): break
                    mm = re.match(r'^\s*([A-Za-z_]\w*)\s*[:,]', S[m]); keys.append(mm.group(1)) if mm else None
                break
            if k > i and re.match(r'^  \S', S[k]) and not S[k].startswith('  }'): break
    j = next((k for k, l in enumerate(T) if re.match(r'^export interface DelegationChain \{', l)), None); fields = {}
    if j is not None:
        for k in range(j + 1, len(T)):
            if T[k].startswith('}'): break
            mm = re.match(r'^\s*(\w+)(\?)?:\s*([^;]+);', T[k])
            if mm: fields[mm.group(1)] = (bool(mm.group(2)), mm.group(3).strip(), k + 1)
    return i, rline, keys, j, fields

TS2OAS = lambda ts: 'array' if ts.endswith('[]') else {'string': 'string', 'number': 'integer', 'boolean': 'boolean'}.get(ts, '?' + ts)

def judge_spec(spec, keys, fields, label, C):
    op = (spec.get('paths') or {}).get(PATH, {}).get(METHOD) or {}
    s = (((op.get('responses') or {}).get('200') or {}).get('content') or {}).get('application/json', {}).get('schema') or {}
    data = (s.get('properties') or {}).get('data') or {}; dp = data.get('properties') or {}; ch = dp.get('chain') or {}; cp = ch.get('properties') or {}
    nonopt = sorted(k for k, (o, _, _) in fields.items() if not o)
    types = {k: (v or {}).get('type') for k, v in cp.items()}; want_types = {k: TS2OAS(t) for k, (_, t, _) in fields.items()}
    env = '$ref' not in s and sorted(s.get('required') or []) == ['data', 'success'] and ((s.get('properties') or {}).get('success') or {}).get('enum') == [True]
    dat = sorted(data.get('required') or []) == ['chain', 'delegation'] and (dp.get('delegation') or {}).get('$ref') == '#/components/schemas/Delegation'
    chn = sorted(cp) == sorted(keys) and sorted(ch.get('required') or []) == nonopt and types == want_types
    C.chk('H5 spec 200 == handler [%s]' % label, env and dat and chn,
          'envelope (no $ref, required [success,data], success enum [true]): %s [got $ref %r, required %s] | data (required {delegation,chain}, delegation $ref Delegation): %s | chain props %s == service return keys %s; required %s == non-optional %s; types %s == TS %s: %s' % (
              env, s.get('$ref'), s.get('required'), dat, sorted(cp), sorted(keys), sorted(ch.get('required') or []), nonopt, types, want_types, chn))
    return env and dat and chn

def judge_errors(spec, emitted, hkeys, label, C):
    op = (spec.get('paths') or {}).get(PATH, {}).get(METHOD) or {}; R = op.get('responses') or {}
    er = ((spec.get('components') or {}).get('schemas') or {}).get('ErrorResponse') or {}; ep = er.get('properties') or {}
    erq = set(er.get('required') or []); succ = (ep.get('success') or {}).get('enum'); err_req = set(((ep.get('error') or {}).get('required')) or [])
    refs = {st: (((R.get(st) or {}).get('content') or {}).get('application/json', {}).get('schema') or {}).get('$ref') for st in emitted}
    ok = all(v == '#/components/schemas/ErrorResponse' for v in refs.values()) and {'success', 'error'} <= erq and succ == [False] and {'code', 'message'} <= err_req and hkeys
    C.chk('H6 error shapes [%s]' % label, ok, 'emitted %s -> declared refs %s | ErrorResponse required %s, success enum %s, error.required %s | handler 404 literal has success:false + error.code + error.message: %s' % (
        sorted(emitted), refs, sorted(erq), succ, sorted(err_req), hkeys))
    return ok

def main(selftest=False):
    C = Checks()
    same = {SHORT(f): blob_id(REPO, BASE, f) == blob_id(REPO, HEAD, f) != 'ABSENT' for f in K['runtime_unchanged']}
    C.chk('H0 runtime unchanged', len(same) >= 1 and all(same.values()), 'blob-equal base == head (and present): %s' % same)
    L, hits, s, e = read_handler(); hf = SHORT(K['handler_file'])
    C.chk('H1 handler', s is not None, '%s: `router.get(\'/:id\'` at line(s) %s (want exactly 1) | body %s:%s-%s' % (hf, [h + 1 for h in hits], hf, (s or 0) + 1, (e or 0) + 1))
    body = L[s:e + 1] if s is not None else []
    def where(rx): return [s + 1 + k for k, l in enumerate(body) if re.search(rx, l)]
    rj = where(r'^\s*res\.json\(\{\s*$'); st = where(r'^\s*success: true,'); dt = where(r'^\s*data: \{\s*$'); dl = where(r'^\s*delegation,\s*$'); cl = where(r'^\s*chain,\s*$')
    bc = where(r'const chain = await delegationService\.buildDelegationChain\(delegation\)')
    C.chk('H2 success shape emitted', len(rj) == 1 and len(st) == 1 and len(dt) == 1 and len(dl) == 1 and len(cl) == 1 and len(bc) == 1,
          '%s: res.json({ :%s | success: true :%s | data: { :%s | delegation, :%s | chain, :%s | chain = await delegationService.buildDelegationChain(delegation) :%s' % (hf, rj, st, dt, dl, cl, bc))
    nf = where(r"res\.status\(404\)\.json\(\{ success: false, error: \{ code: 'NOT_FOUND', message: ")
    M = lines(HEAD, K['handler_mount_file']); mf = SHORT(K['handler_mount_file'])
    am = [i + 1 for i, l in enumerate(M) if re.search(K['auth_mount_rx'], l)]; dm = [i + 1 for i, l in enumerate(M) if re.search(K['handler_mount_rx'], l)]
    order = len(am) == 1 and len(dm) == 1 and am[0] < dm[0]
    C.chk('H3 error paths', len(nf) == 1 and order, '%s: 404 NOT_FOUND literal :%s | %s: app.use(\'/api\', jwtAuthenticate()) :%s BEFORE app.use(\'/api/delegations\', delegationRoutes) :%s: %s' % (hf, nf, mf, am, dm, order))
    i, rline, keys, j, fields = chain_contract()
    sf, tf = SHORT(K['chain_service_file']), SHORT(K['chain_types_file'])
    C.chk('H4 the chain contract', i is not None and rline is not None and len(keys) >= 4 and j is not None and sorted(keys) == sorted(fields),
          '%s: buildDelegationChain :%s, return { :%s keys %s | %s: interface DelegationChain :%s fields %s | keys == fields: %s' % (
              sf, (i or 0) + 1, (rline or 0) + 1, keys, tf, (j or 0) + 1, {k: ('optional ' if o else '') + t + ' :%d' % ln for k, (o, t, ln) in fields.items()}, sorted(keys) == sorted(fields)))
    HY = yaml.load(show(REPO, HEAD, K['spec_yaml']), Loader=YL); BY = yaml.load(show(REPO, BASE, K['spec_yaml']), Loader=YL)
    judge_spec(HY, keys, fields, 'HEAD %s' % HEAD[:12], C)
    judge_errors(HY, ['401', '404'], len(nf) == 1, 'HEAD', C)
    cc = Checks()
    with contextlib.redirect_stdout(io.StringIO()): base_ok = judge_spec(BY, keys, fields, 'BASE', cc)
    bs = (((BY['paths'][PATH][METHOD]['responses']['200'] or {}).get('content') or {}).get('application/json') or {}).get('schema')
    C.chk('H7 must-hit control', not base_ok, 'the same comparator on the BASE yaml (%s): %s (want FAIL) — base declared %s' % (BASE[:12], 'PASS' if base_ok else 'FAIL', bs))
    op = HY['paths'][PATH][METHOD]; dec = sorted(op['responses']); emitted = ['200', '401', '404']
    print('INFO declared %s; emitted on this path %s; declared but not emitted by this handler: %s (pre-existing; the shared commonErrorResponses set)' % (dec, emitted, sorted(set(dec) - set(emitted))))
    tc = [s + 1 + k for k, l in enumerate(body) if re.search(r'\btry\b|\.catch\(', l)]
    pj = show(REPO, HEAD, K['transfer_dir'] + '/package.json') or '{}'; exv = json.loads(pj).get('dependencies', {}).get('express', '?')
    print('INFO %s:%s-%s is async with try/catch lines %s; express %s: a rejected getDelegation()/buildDelegationChain() is not routed to a 500 envelope by Express 4 (READ ONLY, pre-existing, not this PR\'s; the spec\'s 500 is the shared set)' % (hf, (s or 0) + 1, (e or 0) + 1, tc or 'NONE', exv))
    dreq = sorted(HY['components']['schemas']['Delegation'].get('required') or [])
    TT = lines(HEAD, K['chain_types_file']); k0 = next((k for k, l in enumerate(TT) if re.match(r'^export interface Delegation \{', l)), None); tsreq = []
    if k0 is not None:
        for l in TT[k0 + 1:]:
            if l.startswith('}'): break
            mm = re.match(r'^\s*(\w+):\s', l); tsreq.append(mm.group(1)) if mm else None
    print('INFO Delegation component required %s | TS interface Delegation non-optional %s | equal %s (the component is UNCHANGED by this PR; a difference is pre-existing)' % (dreq, sorted(tsreq), dreq == sorted(tsreq)))
    if selftest:
        arms = [('S0 the real head spec', HY, None)]
        def mut(fn):
            y = copy.deepcopy(HY); fn(y['paths'][PATH][METHOD]['responses']['200']['content']['application/json']['schema'], y); return y
        arms += [
            ('S1 the 200 back to a bare $ref Delegation', mut(lambda s, y: (s.clear(), s.update({'$ref': '#/components/schemas/Delegation'}))), 'H5'),
            ('S2 chain.totalDepth typed string', mut(lambda s, y: s['properties']['data']['properties']['chain']['properties']['totalDepth'].update({'type': 'string'})), 'H5'),
            ('S3 invalidReason made required', mut(lambda s, y: s['properties']['data']['properties']['chain']['required'].append('invalidReason')), 'H5'),
            ('S4 chain loses isValid', mut(lambda s, y: s['properties']['data']['properties']['chain']['properties'].pop('isValid')), 'H5'),
            ('S5 data.delegation inlined (no $ref)', mut(lambda s, y: s['properties']['data']['properties'].update({'delegation': {'type': 'object'}})), 'H5'),
            ('S6 success enum [false]', mut(lambda s, y: s['properties']['success'].update({'enum': [False]})), 'H5'),
            ('S7 the 404 points at Delegation', mut(lambda s, y: y['paths'][PATH][METHOD]['responses']['404']['content']['application/json'].update({'schema': {'$ref': '#/components/schemas/Delegation'}})), 'H6'),
            ('S8 ErrorResponse drops error.message from required', mut(lambda s, y: y['components']['schemas']['ErrorResponse']['properties']['error']['required'].remove('message')), 'H6'),
        ]
        ok = 0
        for name, y, want in arms:
            c2 = Checks()
            with contextlib.redirect_stdout(io.StringIO()):
                judge_spec(y, keys, fields, name, c2); judge_errors(y, ['401', '404'], True, name, c2)
            f = c2.failed(); good = (not f) if want is None else any(x.startswith(want) for x in f)
            ok += good; print('SELFTEST %s %s: want %s | failed %s' % ('OK' if good else 'MISS', name, 'PASS' if want is None else 'FAIL on ' + want, f or 'NONE'))
        print('SELFTEST %s %d of %d' % ('OK' if ok == len(arms) else 'BROKEN', ok, len(arms))); return ok == len(arms)
    n = C.nfail(); print('C5 HANDLER %s: %d FAIL of %d checks | base %s | head %s' % ('PASS' if n == 0 else 'FAIL', n, len(C.res), BASE[:12], HEAD[:12])); return n == 0

print('c5_handler_gate55 %s | repo %s | base %s | head %s | %s %s | mode %s' % (now(), REPO, BASE[:12], HEAD[:12], METHOD.upper(), PATH, 'selftest' if '--selftest' in A else 'gate'))
raise SystemExit(0 if main('--selftest' in A) else 1)
