#!/usr/bin/env python3
"""c2_product_gate67.py — C2 PRODUCT + C3B ATTACKER VIEW for #1394 (KS-723), gate67. READ verbs only; runs against any repo holding
the head and the base (the shared checkout is fine). Every figure is derived from blobs, never from the READY.

  W1 diff shape: d784..head is exactly the 5 kit paths, +354/-0, every hunk an addition; the registry gains ONE registerPath
     (get /api/anchors/tx/{txHash}); the test file is new with exactly 5 `it(` cells, 3 named RED and 2 named control.
  W2 SECURITY vs the REAL middleware: the declared op carries security [{bearerAuth: []}]; in anchoring index.ts the route
     `app.get('/api/anchors/tx/:txHash'` is registered AFTER `app.use('/api', jwtAuthenticate())` (so the service verifies the JWT),
     and the gateway proxy mounts `/api/anchors` with `authenticateToken(true)`. Declared == enforced at both hops.
  W3 ENVELOPE vs the REAL handler: the handler's 200 is `res.json({ success: true, data: formatAnchorResponse(anchor) })` and its 404 is
     `{ success: false, error: { code, message } }`; the declared 200 is {success, data: $ref Anchor}, the 404 $ref ErrorResponse.
     Compares formatAnchorResponse's emitted keys to the published Anchor properties / required (INFO for undeclared extras).
  W4 SPEC: the yaml at head == the base's parsed document plus EXACTLY one new path key; every other path and every component
     unchanged; paths 309 -> 310; wc -c of both blobs (bytes, NOT the generator's character count) and the non-ASCII char count.
  W5 ATTACKER VIEW — the gateway edge is spec-driven (api-gateway specRouteMap.ts: METHOD gate 405 + AUTH gate 401 for matched paths).
     Faithful Python port of buildSpecMethodMap/resolveSpecRoute, run on the base spec and the head spec over every route the anchoring
     service registers (+ method fuzz). Prints every (method, path) whose edge decision CHANGED. A change that LOOSENS (was refused at
     the edge, now passes) is a FAIL; tightening is reported.
  W6 GET /api/anchors/{id} is NOT declared at the head (Kam's card secuura-ks723-whose-to-raise-1005 = a), and the what-if: declaring
     it would 405 which live POST routes (re-derives the PR's stated reason).
  W7 NOT TESTED (named): anchoring tsconfig excludes src/__tests__, so the new test file is outside `tsc -p services/anchoring`.
--selftest: the W5 port against planted spec edits (a loosening edit must FAIL, a tightening must not) + W6 what-if control.
rc 0 all PASS / rc 1 any FAIL / rc 2 refused."""
import copy, json, os, re, sys
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from lib_gate67 import K, git, Tally, resolvable
import yaml

H, B = K['head'], K['base']
OP_PATH = '/api/anchors/tx/{txHash}'
HTTP = ['get', 'post', 'put', 'patch', 'delete', 'head', 'options']


def show(repo, rev, p): return git(repo, 'show', '%s:%s' % (rev, p))


# ---- faithful port of services/api-gateway/src/specRouteMap.ts ----
def build_map(spec):
    entries = []
    for path, ops in (spec.get('paths') or {}).items():
        if not isinstance(ops, dict): continue
        methods, authed = set(), set()
        for m, op in ops.items():
            if m.lower() not in HTTP: continue
            methods.add(m.upper())
            sec = (op or {}).get('security') if isinstance(op, dict) else None
            if isinstance(sec, list) and any(isinstance(s, dict) and 'bearerAuth' in s for s in sec): authed.add(m.upper())
        if not methods: continue
        src = re.sub(r'\\\{[^}]+\\\}', '[^/]+', re.sub(r'[.*+?^${}()|\[\]\\]', lambda x: '\\' + x.group(0), path))
        entries.append({'rx': re.compile('^' + src + '$'), 'methods': methods, 'authed': authed, 'path': path, 'lit': '{' not in path})
    entries.sort(key=lambda e: (0 if e['lit'] else 1, -len(e['path'])))
    return entries


def resolve(entries, p):
    ms, au, matched, sp = set(), set(), False, ''
    for e in entries:
        if not e['rx'].match(p): continue
        if not matched: sp = e['path']
        matched = True; ms |= e['methods']; au |= e['authed']
    return matched, ms, au, sp


def edge(entries, method, p, bearer):
    """the gateway's spec-driven edge decision: 'pass' (falls through to proxy), '405', '401'."""
    matched, ms, au, sp = resolve(entries, p)
    if not matched: return 'pass(unmatched)'
    if method not in ms: return '405'
    if method in au and not bearer: return '401'
    return 'pass(matched)'


def anchoring_routes(index_ts):
    out = []
    for m in re.finditer(r"app\.(get|post|put|patch|delete)\('(/api/[^']+)'", index_ts):
        out.append((m.group(1).upper(), m.group(2), index_ts.count('\n', 0, m.start()) + 1))
    return out


def concrete(p): return re.sub(r':[A-Za-z_]+', 'X0abc', p)


def edge_diff(base_spec, head_spec, paths):
    bm, hm = build_map(base_spec), build_map(head_spec)
    changes = []
    for p in paths:
        for meth in [m.upper() for m in HTTP if m not in ('head', 'options')]:
            for bearer in (True, False):
                a, b = edge(bm, meth, p, bearer), edge(hm, meth, p, bearer)
                if a != b: changes.append((meth, p, bearer, a, b))
    return changes


def loosens(a, b):
    return a in ('405', '401') and b.startswith('pass')


def run(repo, t):
    names = git(repo, 'diff', '--name-only', B, H).splitlines()
    ns = git(repo, 'diff', '--numstat', B, H).splitlines()
    adds = sum(int(x.split('\t')[0]) for x in ns); dels = sum(int(x.split('\t')[1]) for x in ns)
    reg_d = git(repo, 'diff', '-U0', B, H, '--', K['registry_file'])
    reg_minus = [l for l in reg_d.splitlines() if l.startswith('-') and not l.startswith('---')]
    regH, regB = show(repo, H, K['registry_file']), show(repo, B, K['registry_file'])
    nreg = regH.count('sharedRegistry.registerPath(') - regB.count('sharedRegistry.registerPath(')
    test = show(repo, H, K['test'])
    cells = re.findall(r"\bit\('([^']*(?:\\'[^']*)*)'", test)
    red = [c for c in cells if c.startswith('RED ')]; ctl = [c for c in cells if c.startswith('control ')]
    t.check('W1', sorted(names) == sorted(K['files']) and (adds, dels) == (354, 0) and not reg_minus and nreg == 1
            and len(cells) == 5 and len(red) == 3 and len(ctl) == 2 and K['base_blobs'][K['test']] is None,
            'paths %d == kit 5 %s | +%d/-%d | registry -lines %d, registerPath +%d | test cells %d (RED %d, control %d), new file %s' % (
                len(names), sorted(names) == sorted(K['files']), adds, dels, len(reg_minus), nreg, len(cells), len(red), len(ctl), K['base_blobs'][K['test']] is None))

    specH, specB = yaml.safe_load(show(repo, H, K['spec'])), yaml.safe_load(show(repo, B, K['spec']))
    op = (specH['paths'].get(OP_PATH) or {}).get('get') or {}
    idx = show(repo, H, K['route_file'])
    auth_line = [i + 1 for i, l in enumerate(idx.split('\n')) if re.search(r"app\.use\('/api',\s*jwtAuthenticate\(\)\)", l)]
    route_line = [i + 1 for i, l in enumerate(idx.split('\n')) if "app.get('/api/anchors/tx/:txHash'" in l]
    imp = re.search(r'authenticate as jwtAuthenticate[^\n]*@secuura/shared', idx) is not None
    prox = show(repo, H, K['gateway_proxy'])
    gm = re.search(r"router\.use\('/api/anchors',\s*\n\s*authenticateToken\((true)\)", prox)
    t.check('W2', op.get('security') == [{'bearerAuth': []}] and len(auth_line) == 1 and len(route_line) == 1 and route_line[0] > auth_line[0] and imp and gm,
            "declared security %s | service: app.use('/api', jwtAuthenticate()) at index.ts:%s, route at index.ts:%s (after: %s), jwtAuthenticate = @secuura/shared authenticate: %s | gateway proxy /api/anchors authenticateToken(true): %s" % (
                op.get('security'), auth_line, route_line, bool(route_line and auth_line and route_line[0] > auth_line[0]), imp, bool(gm)))
    t.info('W2-key', 'the gateway AUTH gate also admits an `x-api-key: sk_…` (connectorApiKey); the op declares bearerAuth only — same as its siblings POST /api/anchors, GET /api/anchors/document/{documentId}, /thread-state/{documentId} (%s). Platform S, the named poller, may call with sk_: the contract does not say so.' % (
        [(p, (specH['paths'][p].get('get') or specH['paths'][p].get('post') or {}).get('security')) for p in ('/api/anchors', '/api/anchors/document/{documentId}')]))

    # W3 envelope
    s0 = route_line[0] if route_line else 0
    body = '\n'.join(idx.split('\n')[s0 - 1:s0 + 14])
    ok200 = re.search(r'res\.json\(\{\s*success:\s*true,\s*data:\s*formatAnchorResponse\(anchor\),?\s*\}\)', body) is not None
    ok404 = re.search(r"res\.status\(404\)\.json\(\{ success: false, error: \{ code: 'NOT_FOUND', message: '[^']+' \} \}\)", body) is not None
    other_status = sorted(set(re.findall(r'res\.status\((\d+)\)', body)))
    sch = op.get('responses', {}).get('200', {}).get('content', {}).get('application/json', {}).get('schema', {})
    e404 = op.get('responses', {}).get('404', {}).get('content', {}).get('application/json', {}).get('schema', {})
    fm = re.search(r'function formatAnchorResponse\(anchor: Anchor\) \{(.*?)\n\}', idx, re.S)
    emitted = set(re.findall(r'^\s{4}(\w+):', fm.group(1), re.M)) if fm else set()
    emitted |= set(re.findall(r'\{ (simulated): true, (simulatedTxRef):', fm.group(1))[0]) if fm and re.search(r'\{ simulated: true, simulatedTxRef:', fm.group(1)) else set()
    anc = specH['components']['schemas']['Anchor']; props = set(anc['properties']); req = set(anc.get('required', []))
    er = specH['components']['schemas']['ErrorResponse']
    t.check('W3', ok200 and ok404 and sch.get('properties', {}).get('data', {}).get('$ref') == '#/components/schemas/Anchor'
            and set(sch.get('properties', {})) == {'success', 'data'} and sch.get('type') == 'object'
            and e404.get('$ref') == '#/components/schemas/ErrorResponse' and req <= emitted and other_status == ['404'],
            'handler 200 {success:true, data: formatAnchorResponse(anchor)} %s, 404 {success:false, error:{code,message}} %s, other res.status() in handler %s | declared 200 %s data->%s | 404 -> %s | Anchor.required %d all emitted %s' % (
                ok200, ok404, other_status, sorted(sch.get('properties', {})), sch.get('properties', {}).get('data', {}).get('$ref'), e404.get('$ref'), len(req), req <= emitted))
    t.info('W3-extra', 'formatAnchorResponse emits keys NOT in the published Anchor (additionalProperties unset, so allowed but undocumented; same $ref the sibling /document/{documentId} already used): %s | declared-not-emitted %s | ErrorResponse requires %s' % (
        sorted(emitted - props), sorted(props - emitted), er.get('required')))
    t.info('W3-codes', 'declared 400/401/403/429/500/502/503 come from commonErrorResponses; the handler itself emits only 200/404 (401 = jwtAuthenticate; 429/502/503 = gateway); a dbGetAnchorByTx failure is swallowed to `undefined` -> 404, so a DB outage answers 404 "Anchor not found for transaction", not 500/503 (pre-existing, index.ts dbGetAnchorByTx)')

    # W4 spec
    rawH, rawB = show(repo, H, K['spec']), show(repo, B, K['spec'])
    bH, bB = len(rawH.encode('utf-8')), len(rawB.encode('utf-8'))
    newp = sorted(set(specH['paths']) - set(specB['paths'])); gone = sorted(set(specB['paths']) - set(specH['paths']))
    chg = [p for p in specB['paths'] if p in specH['paths'] and specB['paths'][p] != specH['paths'][p]]
    comp_same = specB.get('components') == specH.get('components')
    rest_same = {k: v for k, v in specB.items() if k != 'paths'} == {k: v for k, v in specH.items() if k != 'paths'}
    t.check('W4', newp == [OP_PATH] and not gone and not chg and comp_same and rest_same and list(op) and set(specH['paths'][OP_PATH]) == {'get'},
            'paths %d -> %d, new %s, removed %s, changed %d, components identical %s, top-level identical %s | wc -c %s -> %s bytes (+%d); chars %d -> %d; non-ASCII chars at head %d; occurrences of "/api/anchors/tx/" %d -> %d' % (
                len(specB['paths']), len(specH['paths']), newp, gone, len(chg), comp_same, rest_same, format(bB, ','), format(bH, ','), bH - bB,
                len(rawB), len(rawH), sum(1 for ch in rawH if ord(ch) > 127), rawB.count('/api/anchors/tx/'), rawH.count('/api/anchors/tx/')))

    # W5 attacker view
    routes = anchoring_routes(idx)
    paths = sorted({concrete(p) for _, p, _ in routes} | {'/api/anchors/tx/abc', '/api/anchors/tx/abc/extra', '/api/anchors/tx', '/api/anchors/tx/'})
    ch = edge_diff(specB, specH, paths)
    loose = [c for c in ch if loosens(c[3], c[4])]
    t.check('W5', not loose and ch and all(c[1] == '/api/anchors/tx/X0abc' or c[1] == '/api/anchors/tx/abc' for c in ch),
            'edge decisions over %d anchoring routes (%d concrete paths x 5 methods x bearer/none): %d CHANGED, %d LOOSENED; changed: %s' % (
                len(routes), len(paths), len(ch), len(loose), sorted({'%s %s %s: %s -> %s' % (m, p, 'bearer' if b else 'nobearer', a, z) for m, p, b, a, z in ch})))
    t.info('W5-why', 'tightening only: GET /api/anchors/tx/* without bearer/sk_ is now 401 AT THE EDGE (before: the proxy mount authenticateToken(true) 401 one hop later); POST/PUT/PATCH/DELETE now 405 at the edge (before: proxied to anchoring, which has no such route -> its 404). The route was ALREADY served to any authenticated caller; dbGetAnchorByTx has NO tenant / org filter (SELECT * FROM anchor_store WHERE transaction_hash = $1) — pre-existing, unchanged, now DOCUMENTED (tx hashes are public on chain; anchor rows carry documentId).')

    # W6 /api/anchors/{id}
    t.check('W6a', '/api/anchors/{id}' not in specH['paths'] and not any(re.fullmatch(r'/api/anchors/\{[^}]+\}', p) for p in specH['paths']),
            'GET /api/anchors/{id} (index.ts:827) NOT declared at the head (no /api/anchors/{param} path) — KS-723 stays OPEN for it (card secuura-ks723-whose-to-raise-1005 = a)')
    wi = copy.deepcopy(specH); wi['paths']['/api/anchors/{id}'] = {'get': {'security': [{'bearerAuth': []}], 'responses': {}}}
    hm, wm = build_map(specH), build_map(wi)
    single = sorted({(m, concrete(p)) for m, p, _ in routes if re.fullmatch(r'/api/anchors/[^/]+', concrete(p))})
    broke = [(m, p) for m, p in single if edge(hm, m, p, True).startswith('pass') and edge(wm, m, p, True) == '405']
    t.info('W6b', 'WHAT-IF control: declaring GET /api/anchors/{id} would 405 at the edge: %s (live single-segment anchoring routes %s) — the PR body\'s stated reason, re-derived' % (broke, single))

    tc = json.loads(show(repo, H, K['anchoring_tsconfig']))
    t.check('W7', 'src/__tests__' in tc.get('exclude', []),
            'NOT TESTED (named, not a pass): anchoring tsconfig exclude %s -> the new test file is OUTSIDE `tsc -p services/anchoring`; vitest transpiles without type-checking; no typecheck script in services/anchoring/package.json' % tc.get('exclude'))


def selftest(repo):
    res = []
    def rep(c, m): res.append(c); print('%s %s' % ('PASS' if c else 'FAIL', m))
    specH = yaml.safe_load(show(repo, H, K['spec'])); idx = show(repo, H, K['route_file'])
    paths = sorted({concrete(p) for _, p, _ in anchoring_routes(idx)})
    rep(len(anchoring_routes(idx)) >= 10, 'route reader finds %d anchoring app.<verb> routes (control: >= 10)' % len(anchoring_routes(idx)))
    # LOOSENING plant: drop bearerAuth from POST /api/anchors -> unauth POST would pass the edge gate
    lo = copy.deepcopy(specH); lo['paths']['/api/anchors']['post'].pop('security', None)
    ch = edge_diff(specH, lo, paths); rep(any(loosens(c[3], c[4]) for c in ch), 'PLANT loosening (POST /api/anchors loses bearerAuth): W5 sees a LOOSENED edge decision %s' % [c for c in ch if loosens(c[3], c[4])][:2])
    # LOOSENING plant 2: declare POST on the new op path -> POST no longer 405 at the edge
    lo2 = copy.deepcopy(specH); lo2['paths'][OP_PATH]['post'] = {'responses': {}}
    ch = edge_diff(specH, lo2, ['/api/anchors/tx/abc']); rep(any(loosens(c[3], c[4]) for c in ch), 'PLANT loosening (POST declared on tx path): seen %s' % ch[:2])
    # TIGHTENING control: identical spec -> 0 changes
    rep(edge_diff(specH, specH, paths) == [], 'CONTROL identical spec: 0 edge changes')
    # KS-118 union control: two paths collapsing to one regex union their methods
    u = {'paths': {'/a/{x}': {'get': {}}, '/a/{y}': {'delete': {}}}}; m = build_map(u)
    rep(resolve(m, '/a/1')[1] == {'GET', 'DELETE'}, 'port fidelity: KS-118 union of methods across collapsing paths %s' % resolve(m, '/a/1')[1])
    rep(edge(build_map({'paths': {'/a/b': {'get': {'security': [{'bearerAuth': []}]}}}}), 'GET', '/a/b', False) == '401', 'port fidelity: bearerAuth op without bearer -> 401')
    print('SELFTEST %d/%d' % (sum(res), len(res))); return 0 if all(res) else 1


def main():
    A = sys.argv[1:]
    repo = A[A.index('--repo') + 1] if '--repo' in A else K['checkout']
    for n, s in (('head', H), ('base', B)):
        if not resolvable(repo, s): print('REFUSED: %s unresolvable: %s not in %s' % (n, s, repo)); return 2
    if '--selftest' in A: return selftest(repo)
    t = Tally(); run(repo, t); return t.end()


if __name__ == '__main__':
    sys.exit(main())
