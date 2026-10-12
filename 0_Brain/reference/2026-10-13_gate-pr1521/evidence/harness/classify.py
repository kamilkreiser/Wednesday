"""Classify the gate matrix against an oracle written BEFORE reading the results.
Oracle (expected status) per the PR's own stated contract + gateway Guardrail 1 (platform.ts:517-528):
  - platform role (super_admin): 201 unless a non-string connectorId (400).
  - provisioner: other_tenant 403; non-string connectorId 400; else 201, EXCEPT rotate with a connector
    that is not its own -> expected 403 under Guardrail 1 ("rotation stays platform-admin-only").
  - ORG_ADMIN / org_admin / ISSUER_ADMIN (org A1): other_org 403, other_tenant 403;
    then any connectorId present -> 403 (string) or 400 (non-string); else 201.
  - orgless issuer_admin: own_org/other_org 403, other_tenant 403; connectorId -> 403/400; orgless 201.
  - ADMIN: other_tenant 403; connectorId -> 403/400; else 201 (other_org 201 = UNDECIDED policy).
  - platform_admin, user, scopeless_connector: 403 always (decideMint runs first).
FAIL = observed status differs, OR a victim key retired by a caller other than super_admin.
"""
import json, sys
from collections import Counter

d = json.load(open(sys.argv[1]))
NONSTR = {'malformed_array', 'malformed_obj'}

def expect(c):
    r, t, cn, rot = c['role'], c['target'], c['connector'], c['rotate']
    if r in ('platform_admin', 'user', 'scopeless_connector'):
        return 403
    if r == 'super_admin':
        return 400 if cn in NONSTR else 201
    if r == 'provisioner':
        if cn in NONSTR:
            return 400
        if t == 'other_tenant':
            return 403
        if rot and cn not in ('absent', 'own', 'malformed_empty'):
            return 403  # Guardrail 1
        return 201
    if r in ('ORG_ADMIN', 'org_admin_lc', 'ISSUER_ADMIN'):
        if cn in NONSTR:
            return 400
        if t in ('other_org', 'other_tenant'):
            return 403
        return 201 if cn == 'absent' else 403
    if r == 'orgless_issuer_admin':
        if cn in NONSTR:
            return 400
        if t != 'orgless':
            return 403
        return 201 if cn == 'absent' else 403
    if r == 'ADMIN':
        if cn in NONSTR:
            return 400
        if t == 'other_tenant':
            return 403
        return 201 if cn == 'absent' else 403
    raise ValueError(r)

mism, retire = [], []
for c in d['cells']:
    e = expect(c)
    if c['status'] != e:
        mism.append((c['role'], c['target'], c['connector'], c['rotate'], 'exp', e, 'got', c['status'], c['msg']))
    if c['victimActive'] is False and c['role'] != 'super_admin':
        retire.append((c['role'], c['target'], c['connector'], c['rotate'], c['status'], c['retired'], c['retiredOrgs']))
print('mode', d['mode'], 'cells', len(d['cells']))
print('status histogram', Counter(c['status'] for c in d['cells']))
print('mismatches', len(mism))
for m in mism: print('  ', m)
print('victim retired by non-platform caller', len(retire))
for r in retire: print('  ', r)
print('--- smuggle'); [print('  ', s) for s in d['smuggle']]
print('--- org variants'); [print('  ', s) for s in d['orgvariants']]
print('--- race', d.get('race')); print('--- race2', d.get('race2'))
