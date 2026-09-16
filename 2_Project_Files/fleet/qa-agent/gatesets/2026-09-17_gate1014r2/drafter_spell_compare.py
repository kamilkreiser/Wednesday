#!/usr/bin/env python3
"""drafter_spell_compare.py LABEL... — classify rows_spell_<label>.json. Oracle from the ALLOW-LIST's purpose (an admin restricts a connector to a set of
document types; the intended set per connector is written HERE, independently of the route): a restricted connector must not create a type outside it.
  V1 GATEWAY-WIDENING  admitted (201) and the gateway's RESOLVED docType code (enforcement hit counter) is outside the intended set         -> Blocker class
  V2 ORIGINATE-DEFAULT admitted, forwarded, the gateway resolved NO type, and originate (READ) stores a type outside the intended set          -> residue class
  V3 READ-SURFACE      admitted, forwarded, originate's read-surface documentType (data.documentType || type, READ) is outside the intended set -> residue class
  FALSE-REFUSAL        the allow-list refused a shape that the unrestricted control resolves to an INTENDED type                                   -> record
  SAME-KEY             allow-list refusal names a key; resolve it through the catalogue (id exact, or code case-insensitively) and compare with the
                       code enforcement resolves for the SAME shape under the unrestricted control; 'mismatch' = the two read different keys.
Planted controls: a V1 row injected into a copy must be flagged; a clean refusal must not."""
import json, sys, collections, copy
GS = '/Volumes/DevMASTER/WEDNESDAY/2_Project_Files/fleet/qa-agent/gatesets/2026-09-17_gate1014r2'
INTENDED = {'sk_restricted_DOCUMENT': {'DOCUMENT'}, 'sk_restricted_SSD': {'SSD_DOCUMENT'}, 'sk_restricted_lowercase_document': {'DOCUMENT'}, 'sk_restricted_STRING_misconfig': {'SSD_DOCUMENT'}}
def load(l): return json.load(open(f'{GS}/rows_spell_{l}.json'))
def classify(d):
    cat = d['meta']['catalogue']
    def resolve(ref):
        if not isinstance(ref, str) or not ref: return None
        for t in cat:
            if t['id'] == ref or (t['code'] or '').upper() == ref.upper(): return t['code']
        return None
    ctl = {r['shape']: r for r in d['rows'] if r['principal'] == 'sk_write_unrestricted'}
    out = collections.defaultdict(list)
    for r in d['rows']:
        if r['principal'] not in INTENDED: continue
        I = INTENDED[r['principal']]; admitted = r['status'] == 201
        gw = (r['enforcement'] or {}).get('code') if r['enforcement'] and r['enforcement']['ok'] else None
        o = r['originate_read'] or {}
        if admitted and gw and gw not in I: out['V1'].append(r)
        if admitted and r['forwarded'] and not gw and o.get('storedType') and o['storedType'].upper() not in I: out['V2'].append(r)
        if admitted and r['forwarded'] and o.get('readSurfaceType') and o['readSurfaceType'].upper() not in I: out['V3'].append(r)
        c = ctl.get(r['shape']); cgw = (c['enforcement'] or {}).get('keyCode') if c and c['enforcement'] else None  # enforcement's own key, via the key probe
        if r['allowlist_refused'] and cgw in I: out['FALSE-REFUSAL'].append(r)
        if r['allowlist_refused']:
            named = r['allowlist_named']; rn = resolve(named)
            same = (rn == cgw) if (rn or cgw) else True
            if c and c['enforcement'] is None and c['status'] == 403 and c['code'] == 'FORBIDDEN': same = None  # control never reached enforcement
            if same is False and cgw is None and c and c['enforcement'] and c['enforcement'].get('err') == 'VALIDATION_ERROR': same = 'nonstring'  # enforcement refuses a non-string key 400 before resolving; the allow-list refused it 403 first
            elif same is False and cgw is None and rn and c and c['enforcement'] and not c['enforcement']['ok']: same = 'probe-limit'  # the key probe could not pass this type's provider/other gates (QA-EDIT-UNJUDGED)
            out['SAMEKEY-' + ('unjudged' if same is None else ('unjudged-' + same) if isinstance(same, str) else 'same' if same else 'mismatch')].append((r, named, rn, cgw))
    return out
def brief(r): return '%s | %s -> %s %s allow=%s named=%s enf_hits=%d wf_hits=%d fwd=%s gw=%s originate=%s' % (r['principal'], r['shape'], r['status'], r['code'], r['allowlist_refused'], r['allowlist_named'], r['enforce_hits'], r['workflow_hits'], r['forwarded'], (r['enforcement'] or {}).get('code'), r['originate_read'])
labels = sys.argv[1:]
data = {l: load(l) for l in labels}
for l in labels:
    d = data[l]; c = classify(d)
    print('=== %s rows %d | V1 %d V2 %d V3 %d FALSE-REFUSAL %d SAMEKEY same %d mismatch %d unjudged %d nonstring %d probe-limit %d | fwd-body-identical %s' % (l, len(d['rows']), len(c['V1']), len(c['V2']), len(c['V3']), len(c['FALSE-REFUSAL']), len(c['SAMEKEY-same']), len(c['SAMEKEY-mismatch']), len(c['SAMEKEY-unjudged']), len(c['SAMEKEY-unjudged-nonstring']), len(c['SAMEKEY-unjudged-probe-limit']), collections.Counter(r['forwarded_body_identical'] for r in d['rows'] if r['forwarded'])))
    for k in ('V1', 'V2', 'V3', 'FALSE-REFUSAL'):
        for r in c[k]: print('  ', k, brief(r))
    for (r, named, rn, cgw) in c['SAMEKEY-mismatch']: print('   SAMEKEY-mismatch', r['principal'], r['shape'], 'allow-list named', repr(named), '->', rn, '| enforcement (control) resolved', cgw)
# row-level diffs across trees for the restricted principals
def outcome(r): return (r['status'], r['code'], r['allowlist_refused'], r['enforce_hits'], r['workflow_hits'], r['forwarded'])
for a, b in zip(labels, labels[1:]):
    ia = {(r['principal'], r['shape']): r for r in data[a]['rows']}; ib = {(r['principal'], r['shape']): r for r in data[b]['rows']}
    assert set(ia) == set(ib)
    diffs = [k for k in ia if outcome(ia[k]) != outcome(ib[k])]
    print('--- DIFF %s -> %s: %d rows; by principal %s' % (a, b, len(diffs), dict(collections.Counter(k[0] for k in diffs))))
    for k in diffs: print('    %-34s %-44s %s -> %s' % (k[0], k[1], outcome(ia[k])[:3], outcome(ib[k])[:3]))
# planted controls on the first label
d0 = copy.deepcopy(data[labels[-1]]); rows = d0['rows']
tgt = next(r for r in rows if r['principal'] == 'sk_restricted_DOCUMENT' and r['shape'] == 'dt:SSD')
tgt.update(status=201, code=None, allowlist_refused=False, enforce_hits=1, forwarded=True, enforcement={'ok': True, 'code': 'SSD_DOCUMENT', 'status': None, 'err': None}, originate_read={'precheck': None, 'storedType': 'SSD_DOCUMENT', 'readSurfaceType': 'SSD_DOCUMENT'})
c0 = classify(d0)
print('PLANTED: injected V1 (sk_restricted_DOCUMENT dt:SSD admitted as SSD_DOCUMENT) flagged', any(r is tgt for r in c0['V1']), '| clean refusal ty:REFERENCE not flagged', not any(r['principal'] == 'sk_restricted_DOCUMENT' and r['shape'] == 'ty:REFERENCE(standard)' for k in ('V1', 'V2', 'V3') for r in c0[k]))
