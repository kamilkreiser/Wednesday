#!/usr/bin/env python3
"""drafter_g2_check.py — the G2 claim made precise: for every probe cell that reaches the upstream on BOTH trees, the set of watched headers carrying the
client's SPOOF value is identical head vs dev; list every cell that reaches upstream on head only, with its spoofed set; x-verification-level / x-user-* spoof
rows by context. Positive control: a planted spoof name on one head row must make the equality check report 1 mismatch."""
import json, os, collections, copy
GS = os.path.dirname(os.path.abspath(__file__)); O = GS + '/out'
SP = {'x-verification-level': 'enhanced', 'x-user-email': 'spoof@qa1028.invalid', 'x-user-id': 'spoof-user', 'x-user-role': 'super_admin', 'x-organization-id': 'spoof-org', 'x-tenant-id': 'spoof-tenant', 'x-tenant-slug': 'spoof'}
def load(t):
    d = json.load(open(O + '/rows_%s.json' % t)); out = {}
    for m in ('test', 'prod'):
        for r in d[m]: out[(m, r['mount'], r['ctx'], r['token'], r['spoof'])] = r
    return out
H, D = load('head'), load('dev')
def spoofed(r):
    s = json.load(open(O + '/rows_head.json'))  # unused; keeps file read explicit
    return None
WATCH_SPOOF = {'x-verification-level': 'enhanced', 'x-user-email': 'spoof@qa1028.invalid', 'x-user-id': 'spoof-user', 'x-user-role': 'super_admin', 'x-organization-id': 'spoof-org',
  'x-tenant-id': 'spoof-tenant', 'x-tenant-slug': 'spoof', 'x-wallet-address': 'addr_spoof_qa1028', 'x-auth-method': 'spoof', 'x-mfa-enabled': 'true', 'x-session-id': 'spoof',
  'x-scopes': 'admin:*', 'x-connector-id': 'spoof', 'x-api-key-scopes': 'admin:*', 'x-verified': 'true', 'x-kyc-level': 'enhanced'}
def sset(r): return frozenset(n for x in (r.get('fwd') or []) for n, v in x['h'].items() if r['spoof'] == 'SPOOF' and v is not None and WATCH_SPOOF.get(n) == v)
def compare(H, D):
    both = [k for k in H if (H[k].get('fwd') and D[k].get('fwd'))]; mism = [k for k in both if sset(H[k]) != sset(D[k])]; return both, mism
both, mism = compare(H, D)
print('cells reaching upstream on both trees', len(both), '| spoofed-set mismatches', len(mism), mism[:5])
H2 = copy.deepcopy(H); k0 = both[0]; H2[k0]['spoof'] = 'SPOOF'; H2[k0]['fwd'][0]['h']['x-kyc-level'] = 'enhanced'; H2[k0]['fwd'][0]['h']['x-user-id'] = 'spoof-user'
print('positive control (planted on', k0, '):', len(compare(H2, D)[1]), 'mismatch (want >= 1)')
only_head = [k for k in H if H[k].get('fwd') and not D[k].get('fwd')]
print('cells reaching upstream on head only', len(only_head), collections.Counter((k[2], k[3]) for k in only_head))
print('   their spoofed sets', collections.Counter(tuple(sorted(sset(H[k]))) for k in only_head))
for t, T in (('head', H), ('dev', D)):
    ident = collections.Counter((k[0], k[1], k[2], n) for k, r in T.items() for n in sset(r) if n in SP)
    print(t, 'rows forwarding a CLIENT identity/level header (x-verification-level, x-user-*, x-organization-id, x-tenant-*):', sum(ident.values()), sorted(ident.items()))
print('internal-message leak rows head/dev', sum(bool(r.get('leaksInvalidValue')) for r in H.values()), sum(bool(r.get('leaksInvalidValue')) for r in D.values()),
      '| 5xx messages head', collections.Counter(r.get('msg') for r in H.values() if r['status'] >= 500), '| dev', collections.Counter(r.get('msg') for r in D.values() if r['status'] >= 500))
