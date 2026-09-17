#!/usr/bin/env python3
"""drafter_table_1028.py — summarise out/rows_head.json vs out/rows_dev.json (the #1028 drafter real-app probe). Graders:
  G1 (the contract): BEARER / BEARER+JUNKKEY rows whose token is NO_EMAIL / NO_VLEVEL / NO_BOTH -> 2xx with >= 1 upstream hit (proxy mounts) or 2xx (local), never 5xx
  G2 (client identity header reaching upstream): any upstream hit whose forwarded value of a watched header EQUALS the client's SPOOF value (x-api-key excluded)
  G3 (internal message leak): any response body matching /Invalid value|ERR_HTTP_INVALID_HEADER/
Positive controls: the dev tree must show G1 failures (500) and the FULL token must forward 'basic'. Prints per-cell diffs head vs dev."""
import json, collections, os
GS = os.path.dirname(os.path.abspath(__file__)); O = GS + '/out'
SPOOF = {'x-verification-level': 'enhanced', 'x-user-email': 'spoof@qa1028.invalid', 'x-user-id': 'spoof-user', 'x-user-role': 'super_admin', 'x-organization-id': 'spoof-org',
         'x-tenant-id': 'spoof-tenant', 'x-tenant-slug': 'spoof', 'x-wallet-address': 'addr_spoof_qa1028', 'x-auth-method': 'spoof', 'x-mfa-enabled': 'true', 'x-session-id': 'spoof',
         'x-scopes': 'admin:*', 'x-connector-id': 'spoof', 'x-api-key-scopes': 'admin:*', 'x-verified': 'true', 'x-kyc-level': 'enhanced'}
def load(t):
    d = json.load(open(O + '/rows_%s.json' % t)); rows = []
    for mode in ('test', 'prod'):
        for r in d[mode]: r['mode'] = mode; rows.append(r)
    return rows
def key(r): return (r['mode'], r['mount'], r['ctx'], r['token'], r['spoof'])
def cell(r):
    f = r.get('fwd') or []
    lv = [x['h'].get('x-verification-level') for x in f]; em = [x['h'].get('x-user-email') for x in f]
    spoofed = sorted({n for x in f for n, v in x['h'].items() if v is not None and SPOOF.get(n) == v}) if r['spoof'] == 'SPOOF' else []
    return dict(status=r['status'], code=r['code'], hits=len(f), vlevel=lv[0] if lv else '-', email=em[0] if em else '-', rawv=(f[0]['raw'].get('x-verification-level', 0) if f else '-'),
                spoofed=spoofed, leak=r.get('leaksInvalidValue'), msg=(r.get('msg') or '')[:70], sub=(f[0]['bearerSub'] if f else '-'))
T = {t: {key(r): cell(r) for r in load(t)} for t in ('head', 'dev')}
print('rows per tree', {t: len(v) for t, v in T.items()})
for t in ('head', 'dev'):
    g1 = [(k, c['status'], c['hits'], c['msg']) for k, c in T[t].items() if k[2] in ('BEARER', 'BEARER+JUNKKEY') and k[3] in ('NO_EMAIL', 'NO_VLEVEL', 'NO_BOTH') and (c['status'] >= 500 or c['status'] < 200 or c['status'] >= 300 or (k[1] != 'settings-notifications' and c['hits'] < 1))]
    g2 = [(k, c['spoofed']) for k, c in T[t].items() if c['spoofed']]
    g3 = [(k, c['status'], c['msg']) for k, c in T[t].items() if c['leak']]
    n1 = sum(1 for k in T[t] if k[2] in ('BEARER', 'BEARER+JUNKKEY') and k[3] in ('NO_EMAIL', 'NO_VLEVEL', 'NO_BOTH'))
    print('\n== tree', t, '| G1 contract failures', len(g1), 'of', n1, '| G2 spoofed-header rows', len(g2), '| G3 leak rows', len(g3))
    for x in g1[:12]: print('   G1', x)
    by = collections.Counter((k[2], k[1], tuple(v)) for k, v in g2)
    for (ctx, mount, hs), n in sorted(by.items()): print('   G2', ctx, mount, 'rows', n, 'headers', hs)
    by3 = collections.Counter((k[3], k[1], k[0], s) for k, s, m in g3)
    for x, n in sorted(by3.items()): print('   G3', x, n, [m for k, s, m in g3 if (k[3], k[1], k[0], s) == x][0])
print('\n== controls: FULL token BEARER NONE credentials test: head', {k: T['head'][('test', 'credentials', 'BEARER', 'FULL', 'NONE')][k] for k in ('status', 'hits', 'vlevel', 'email')},
      '| dev', {k: T['dev'][('test', 'credentials', 'BEARER', 'FULL', 'NONE')][k] for k in ('status', 'hits', 'vlevel', 'email')})
print('\n== head cells, credentials (optional proxy) and documents (required proxy), BEARER, per token, test mode, NONE / SPOOF')
for mount in ('credentials', 'documents', 'settings-notifications'):
    for tok in sorted({k[3] for k in T['head'] if k[1] == mount and k[2] == 'BEARER'}):
        for sp in ('NONE', 'SPOOF'):
            k = ('test', mount, 'BEARER', tok, sp); h = T['head'][k]; d = T['dev'][k]
            f = lambda c: '%s/%s hits=%s lv=%r(raw %s) em=%r spoofed=%s leak=%s %s' % (c['status'], c['code'], c['hits'], c['vlevel'], c['rawv'], c['email'], c['spoofed'], c['leak'], c['msg'][:50])
            print('  %-22s %-16s %-5s HEAD %s\n  %-45s DEV  %s' % (mount, tok, sp, f(h), '', f(d)))
print('\n== non-BEARER contexts (head | dev), test + prod')
for k in sorted(k for k in T['head'] if k[2] not in ('BEARER',) and not (k[2] == 'BEARER+JUNKKEY' and k[3] not in ('NO_VLEVEL', 'FULL', 'NO_EMAIL'))):
    h = T['head'][k]; d = T['dev'][k]
    print('  %s | HEAD %s/%s hits=%s lv=%r em=%r sub=%s spoofed=%s | DEV %s/%s hits=%s lv=%r em=%r sub=%s spoofed=%s' % (k, h['status'], h['code'], h['hits'], h['vlevel'], h['email'], h['sub'], h['spoofed'], d['status'], d['code'], d['hits'], d['vlevel'], d['email'], d['sub'], d['spoofed']))
diff = [k for k in T['head'] if T['head'][k] != T['dev'][k]]
print('\n== head vs dev differing cells', len(diff), 'of', len(T['head']))
cls = collections.Counter((k[2], k[3]) for k in diff)
for x, n in sorted(cls.items()): print('   differ', x, n)
same_prod = [k for k in T['head'] if k[0] == 'prod' and T['head'][k]['status'] != T['head'][('test',) + k[1:]]['status']]
print('prod vs test status differences at head', len(same_prod), sorted(collections.Counter((k[1], k[2]) for k in same_prod).items())[:10])
