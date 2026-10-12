"""Re-gate classifier for #1521 r1. Oracle written BEFORE reading head's cells (the r0 oracle, amended to the
claimed fix): identical to classify.py EXCEPT the provisioner rotate line now reads
  provisioner + rotate + ANY string connectorId (own, other, '', case-variant) -> 403  (M1 fix: inside the
  connectorId block, rotate === true is refused for a provisioner). Absent connector + rotate -> 201 (no-op).
FAIL = observed status differs from the oracle, OR any victim key retired by a caller other than super_admin,
OR a non-2xx cell wrote/retired anything (asserted inside the harness).
"""
import json, sys
from collections import Counter
d = json.load(open(sys.argv[1]))
NONSTR = {'malformed_array', 'malformed_obj'}
def expect(c):
    r, t, cn, rot = c['role'], c['target'], c['connector'], c['rotate']
    if r in ('platform_admin', 'user', 'scopeless_connector'): return 403
    if r == 'super_admin': return 400 if cn in NONSTR else 201
    if r == 'provisioner':
        if cn in NONSTR: return 400
        if t == 'other_tenant': return 403
        if rot and cn != 'absent': return 403
        return 201
    if r in ('ORG_ADMIN', 'org_admin_lc', 'ISSUER_ADMIN'):
        if cn in NONSTR: return 400
        if t in ('other_org', 'other_tenant'): return 403
        return 201 if cn == 'absent' else 403
    if r == 'orgless_issuer_admin':
        if cn in NONSTR: return 400
        if t != 'orgless': return 403
        return 201 if cn == 'absent' else 403
    if r == 'ADMIN':
        if cn in NONSTR: return 400
        if t == 'other_tenant': return 403
        return 201 if cn == 'absent' else 403
    raise ValueError(r)
mism = [c for c in d['cells'] if c['status'] != expect(c)]
retire = [c for c in d['cells'] if c['victimActive'] is False and c['role'] != 'super_admin']
print('mode', d['mode'], 'matrix cells', len(d['cells']), 'histogram', dict(sorted(Counter(c['status'] for c in d['cells']).items())))
print('oracle mismatches', len(mism))
for c in mism: print('   ', c['role'], c['target'], c['connector'], c['rotate'], 'exp', expect(c), 'got', c['status'], c['msg'])
print('matrix: victim retired by non-platform caller', len(retire))
for c in retire: print('   ', c['role'], c['target'], c['connector'], c['rotate'], c['status'])
rs = d.get('rotshapes', [])
print('R1 battery cells', len(rs), 'histogram', dict(sorted(Counter(c['status'] for c in rs).items())),
      'victim retired', sum(1 for c in rs if c['victimActive'] is not True), 'any retirement', sum(c['retired'] for c in rs),
      'rows stored with a connectorId', sum(1 for c in rs for a in c['added'] if a['connector']))
byrole = {}
for c in rs: byrole.setdefault((c['role'], c['label']), Counter())[c['status']] += 1
print('  provisioner per shape (status counts over own/victim/none org):')
for (r, l), cnt in byrole.items():
    if r == 'provisioner': print('    %-42s %s' % (l, dict(cnt)))
print('platformRotateControl', d.get('platformRotateControl'))
print('memSqlDisagree', d.get('memSqlDisagree', 0))
print('--- smuggle'); [print('  ', s['label'], s['status'], 'victimActive', s['victimActive'], s['added']) for s in d['smuggle']]
print('--- m1 (stored form / listed by platform canonical | upper | as-sent)')
for m in d.get('m1', []): print('  %-28s %-15s %s stored=%s mem=%s list(canon,upper,sent)=%s,%s,%s %s' % (m['caller'], m['variant'], m['status'], m['stored'], repr(m['memOrg']), m['listedCanonical'], m['listedUpper'], m['listedAsSent'], (m['msg'] or '')[:60]))
print('m1list (ISSUER_ADMIN of OA listing own):', {k: (v['status'], len(v['ids'])) for k, v in d.get('m1list', {}).items()})
print('--- item5 (no tenantId sent)')
for m in d.get('item5', []): print('  %-22s %-12s %s stored=%s %s' % (m['caller'], m['variant'], m['status'], m['stored'], (m['msg'] or '')[:70]))
print('--- race', d.get('race')); print('--- raceSeq', {k: v for k, v in (d.get('raceSeq') or {}).items() if k != 'priorKeysRevoked'}); print('--- racePair', d.get('racePair')); print('--- race2', d.get('race2'))
