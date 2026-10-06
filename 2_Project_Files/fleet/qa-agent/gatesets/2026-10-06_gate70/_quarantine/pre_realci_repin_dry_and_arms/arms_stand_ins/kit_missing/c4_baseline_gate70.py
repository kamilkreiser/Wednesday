#!/usr/bin/env python3
"""c4_baseline_gate70.py — THE TWO BASELINE ROWS of #1397 (KS-1425). Read verbs only; the fuse runs the REPO'S OWN isLapsed / validateBaseline
(baseline-contract.mjs read from the HEAD by `git show` into a FRESH scratch dir; the file has 0 imports) under node.

  rows --repo R --head H [--base B]
     B1  PURE TEXTUAL APPEND: head bytes minus ONE contiguous inserted span == the base bytes, byte for byte (so `$comment` and every
         pre-existing row are byte-equal by construction); the span is +14 -0 lines. B1rt (INFO) measures the author's premise that the
         file does not survive a json round-trip (drafter: it DOES, under ensure_ascii=False / node JSON.stringify — README D-2)
     B2  rows 22 -> 24; the first 22 ids in the base ORDER; every base row json-equal too (a second instrument for the same claim)
     B3  the new ids are EXACTLY {GHSA-hp3w-g68c-fv3c, GHSA-rj75-hqrm-r3gf}, packages sprintf-js / postcss-selector-parser
     B4  SHAPE == KS-1403's braces row (GHSA-vfj7-8cjw-p6xm): the same keys in the same ORDER (package, reason, ticket, decidedAt, expires)
     B5  ticket KS-1425, decidedAt 2026-10-06, expires 2026-10-31 on both
     B6  each reason names the card AND carries Kam's ruling verbatim; the rj75 reason says it covers 6.1.4 ONLY BY INTENT and names the
         7.x refresh; 0 new row is a fixed (critical/high) id
     B7  no pre-existing row re-dated and none removed (dated rows before == after); 0 rows lost
  fuse --repo R --head H --scratch DIR
     F1  validateBaseline(head accepted) == []   CONTROL: the same call on a copy with one NEW row's `expires` deleted reports it
     F2  both new rows LIVE at 2026-10-30, LAPSED at 2026-10-31 (isLapsed is `expires <= today`, UTC)
     F3  CONTROL: a grandfathered no-expires row (GHSA-2mjp-6q6p-2qxm) never lapses, even at 2099-01-01
  --selftest   planted: an edited old row, a re-dated row, a removed row, a reordered key, a 6th key, a wrong ticket — each FAILS B1-B7.
rc 0 / 1."""
import json, os, subprocess, sys, tempfile
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from lib_gate70 import K, Tally, git_bytes, roundtrip_exact

BL = K['baseline']


def insertion(b, h):
    p = 0
    while p < min(len(b), len(h)) and b[p] == h[p]: p += 1
    s = 0
    while s < min(len(b), len(h)) - p and b[len(b) - 1 - s] == h[len(h) - 1 - s]: s += 1
    pure = len(b) == p + s and len(h) > len(b)
    return pure, h[p:len(h) - s], p


def row_findings(braw, hraw):
    f = {}
    pure, span, at = insertion(braw, hraw)
    f['B1'] = [] if pure else ['NOT a pure insertion (the base is not head minus one span)']
    b = json.loads(braw); h = json.loads(hraw); ba, ha = b['accepted'], h['accepted']
    f['B2'] = []
    if b.get('$comment') != h.get('$comment'): f['B2'].append('$comment changed')
    if list(ha)[:len(ba)] != list(ba): f['B2'].append('base ids not the head prefix in order')
    if any(ha.get(k) != v for k, v in ba.items()): f['B2'].append('a base row changed: %s' % [k for k, v in ba.items() if ha.get(k) != v][:3])
    if (len(ba), len(ha)) != (BL['rows_before'], BL['rows_after']): f['B2'].append('rows %d -> %d (kit %d -> %d)' % (len(ba), len(ha), BL['rows_before'], BL['rows_after']))
    new = [k for k in ha if k not in ba]
    f['B3'] = [] if set(new) == set(BL['new_rows']) and all(ha[k].get('package') == BL['new_rows'][k]['package'] for k in new if k in BL['new_rows']) else ['new ids %s' % new]
    shape = list(ba.get(BL['shape_row'], {}))
    f['B4'] = [] if shape == BL['key_order'] and all(list(ha[k]) == shape for k in new) else ['shape %s vs braces %s' % ([list(ha[k]) for k in new], shape)]
    f['B5'] = ['%s %s' % (k, (ha[k].get('ticket'), ha[k].get('decidedAt'), ha[k].get('expires'))) for k in new
               if (ha[k].get('ticket'), ha[k].get('decidedAt'), ha[k].get('expires')) != (BL['ticket'], BL['decidedAt'], BL['expires'])]
    f['B6'] = []
    for k in new:
        r = ha[k].get('reason', '')
        if BL['card'] not in r or BL['ruling_verbatim'] not in r: f['B6'].append('%s reason lacks the card / the ruling verbatim' % k)
        if k in K['fixed_ids'] or k in (K['plan']['proxy-addr']['ghsa'], K['plan']['source-map-js']['ghsa']): f['B6'].append('%s is a FIXED critical/high id' % k)
    rj = ha.get('GHSA-rj75-hqrm-r3gf', {}).get('reason', '')
    if 'GHSA-rj75-hqrm-r3gf' in ha and not ('6.1.4 ONLY' in rj and '7.1.6' in rj): f['B6'].append('rj75 reason does not state 6.1.4 ONLY + the 7.x refresh')
    dated_b = dict((k, v.get('expires')) for k, v in ba.items() if v.get('expires'))
    f['B7'] = [] if all(ha.get(k, {}).get('expires') == e for k, e in dated_b.items()) and set(ba) <= set(ha) else ['a dated row re-dated or a row removed']
    return f, span, at


def cmd_rows(repo, base, head):
    t = Tally(); path = K['baseline_path']
    braw, hraw = git_bytes(repo, base, path), git_bytes(repo, head, path)
    f, span, at = row_findings(braw, hraw)
    lines = span.count(b'\n')
    print('INSERTION at byte %d: %d bytes, %d newline(s); base %d bytes, head %d bytes' % (at, len(span), lines, len(braw), len(hraw)))
    j = json.loads(braw)
    rt = dict(('ensure_ascii=%s indent %d' % (ea, n), len((json.dumps(j, indent=n, ensure_ascii=ea) + '\n').encode())) for ea in (False, True) for n in (2, 4))
    t.info('B1rt', 'PREMISE CHECK (the commit body says the file does not survive a json round-trip, 19,858 / 20,586 vs 19,810): base round-trips '
           'byte-exact under ensure_ascii=False indent 2: %s; sizes %s; non-ASCII chars %d. A textual append yields the same bytes either way — rule the CLAIM, not the method'
           % (roundtrip_exact(braw)[0], rt, sum(1 for c in braw.decode() if ord(c) > 127)))
    f['B1'] += [] if lines == BL['numstat'][0] else ['inserted lines %d != kit %d' % (lines, BL['numstat'][0])]
    for c in ('B1', 'B2', 'B3', 'B4', 'B5', 'B6', 'B7'):
        t.check(c, not f[c], f[c][:3] if f[c] else 'ok')
    return t.end()


FUSE_JS = r"""
const [mod, blPath, livePath] = process.argv.slice(2);
const { isLapsed, validateBaseline } = await import('file://' + mod);
const bl = JSON.parse((await import('node:fs')).readFileSync(blPath, 'utf8')).accepted;
const ids = JSON.parse(livePath);
const out = { validate: validateBaseline(bl) };
const planted = structuredClone(bl); delete planted[ids.newIds[0]].expires; out.validatePlanted = validateBaseline(planted);
out.rows = {};
for (const id of ids.newIds) out.rows[id] = { live: isLapsed(bl[id], ids.live), dead: isLapsed(bl[id], ids.dead) };
out.control = { id: ids.ctl, lapsed: isLapsed(bl[ids.ctl], ids.ctlDate) };
console.log(JSON.stringify(out));
"""


def cmd_fuse(repo, head, scratch):
    t = Tally()
    os.makedirs(scratch, exist_ok=True); d = tempfile.mkdtemp(prefix='fuse_', dir=scratch)
    mod = os.path.join(d, 'baseline-contract.mjs'); open(mod, 'wb').write(git_bytes(repo, head, 'Blockchain/Dev/scripts/audit/baseline-contract.mjs'))
    blp = os.path.join(d, 'audit-baseline.json'); open(blp, 'wb').write(git_bytes(repo, head, K['baseline_path']))
    js = os.path.join(d, 'fuse.mjs'); open(js, 'w').write(FUSE_JS)
    ids = json.dumps({'newIds': sorted(BL['new_rows']), 'live': BL['fuse_live'], 'dead': BL['fuse_dead'], 'ctl': BL['fuse_control_no_expiry_row'], 'ctlDate': BL['fuse_control_date']})
    p = subprocess.run(['node', js, mod, blp, ids], capture_output=True, text=True)
    print('NODE rc %d (module = the HEAD\'s baseline-contract.mjs, copied to %s)' % (p.returncode, d)); print(p.stdout.strip()); print(p.stderr.strip()[:400])
    if p.returncode != 0: print('LOAD FAILURE: the fuse did not run — NOT a pass'); return 1
    o = json.loads(p.stdout)
    t.check('F1', o['validate'] == [] and any(x.get('id') == sorted(BL['new_rows'])[0] for x in o['validatePlanted']),
            'validateBaseline(head) %s | CONTROL (one new row\'s expires deleted) %s' % (o['validate'], o['validatePlanted']))
    t.check('F2', all(v == {'live': False, 'dead': True} for v in o['rows'].values()), 'isLapsed at %s / %s: %s' % (BL['fuse_live'], BL['fuse_dead'], o['rows']))
    t.check('F3', o['control']['lapsed'] is False, 'CONTROL no-expires row %s at %s lapsed=%s' % (o['control']['id'], BL['fuse_control_date'], o['control']['lapsed']))
    return t.end()


def selftest():
    res = []
    def rep(c, m): res.append(bool(c)); print('%s %s' % ('PASS' if c else 'FAIL', m))
    rs = 'r ' + BL['card'] + ' ' + BL['ruling_verbatim']
    base = {'$comment': 'c', 'accepted': {}}
    for i in range(BL['rows_before'] - 1): base['accepted']['GHSA-old-%d' % i] = {'package': 'p', 'reason': 'r', 'ticket': 'KS-1', 'decidedAt': '2026-01-01', 'expires': '2026-10-31'}
    base['accepted'][BL['shape_row']] = dict((k, 'x') for k in BL['key_order'])
    def row(pkg, extra=''): return {'package': pkg, 'reason': rs + extra, 'ticket': BL['ticket'], 'decidedAt': BL['decidedAt'], 'expires': BL['expires']}
    def render(d):
        t = json.dumps(d, indent=2) + '\n'; return t.replace('": "', '":  "', 1).encode()   # one odd space: like the real file, not a round-trip
    good = json.loads(json.dumps(base)); good['accepted']['GHSA-hp3w-g68c-fv3c'] = row('sprintf-js'); good['accepted']['GHSA-rj75-hqrm-r3gf'] = row('postcss-selector-parser', ' 6.1.4 ONLY 7.1.6')
    B = render(base); Hg = render(good)
    lines = Hg.decode().count('\n') - B.decode().count('\n')
    f, _, _ = row_findings(B, Hg); bad = [c for c, v in f.items() if v]
    rep(not bad, 'the planned append passes (%d inserted lines in the synthetic) %s' % (lines, bad or ''))
    def mut(fn):
        h = json.loads(json.dumps(good)); fn(h); return render(h)
    arms = {'edited old row': lambda h: h['accepted']['GHSA-old-0'].update(reason='changed'),
            're-dated old row': lambda h: h['accepted']['GHSA-old-1'].update(expires='2026-11-30'),
            'removed old row': lambda h: h['accepted'].pop('GHSA-old-2'),
            'reordered keys': lambda h: h['accepted'].update({'GHSA-hp3w-g68c-fv3c': dict(reversed(list(h['accepted']['GHSA-hp3w-g68c-fv3c'].items())))}),
            '6th key': lambda h: h['accepted']['GHSA-hp3w-g68c-fv3c'].update(severity='moderate'),
            'wrong ticket': lambda h: h['accepted']['GHSA-rj75-hqrm-r3gf'].update(ticket='KS-1403'),
            'reason without the ruling': lambda h: h['accepted']['GHSA-hp3w-g68c-fv3c'].update(reason='r'),
            'a critical id baselined': lambda h: h['accepted'].update({'GHSA-jqcg-44mw-7w3h': row('proxy-addr')})}
    for nm, fn in arms.items():
        f, _, _ = row_findings(B, mut(fn)); rep(any(f.values()), 'PLANTED %s FAILS (%s)' % (nm, [c for c, v in f.items() if v]))
    rt = (json.dumps(good, indent=2) + '\n').encode(); f, _, _ = row_findings(B, rt)
    rep(f['B1'], 'PLANTED a canonical re-serialisation (the odd space normalised away) FAILS B1: not a pure insertion')
    print('SELFTEST %d/%d' % (sum(res), len(res))); return 0 if all(res) else 1


def main():
    A = sys.argv[1:]
    def opt(k, d=None): return A[A.index(k) + 1] if k in A and A.index(k) + 1 < len(A) else d
    if '--selftest' in A: return selftest()
    if not A: print(__doc__); return 2
    head = opt('--head', K['pr']['head_expected'])
    if A[0] == 'rows': return cmd_rows(opt('--repo'), opt('--base', K['pr']['parents'][0]), head)
    if A[0] == 'fuse':
        if not opt('--scratch'): print('REFUSED: --scratch <dir> required'); return 2
        return cmd_fuse(opt('--repo'), head, opt('--scratch'))
    print(__doc__); return 2


if __name__ == '__main__':
    sys.exit(main())
