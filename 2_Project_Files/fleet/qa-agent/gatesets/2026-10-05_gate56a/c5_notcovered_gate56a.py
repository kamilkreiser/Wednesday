#!/usr/bin/env python3
"""c5_notcovered_gate56a.py — gate56a C5 NOT COVERED + AUTHORITY, for ONE PR (READ ONLY: Wednesday's card store, the grant file, the
ANSWER brief, the PR body file; prints only).
  A1 THE RULED CARD: kit authority_card in decisions.json has status `ruled`, ruled_choice == kit (a), ruled_ts == kit, and the chosen
     option's label == kit authority_label (printed verbatim — the literal the PR must carry: pr3 "31 Oct" -> 2026-10-31).
  A2 THE GRANT: kit grant_file exists and carries Kam's words verbatim: "board taps are enough for audit re-dates"; its scope line ("moving
     an existing dated row's date ... Adding a NEW baseline row, removing one, or widening one ... is not a re-date") is printed — C4 S1/S2
     are the measurement that this PR stays inside it.
  A3 THE VALUE: pr3 — the card label names "31 Oct" and the kit value is 2026-10-31 (the ANSWER: "write 2026-10-31 anyway (the ruled
     literal)"); pr4 — the ANSWER brief carries "write `2027-01-01`" and names the ADDENDUM's 2026-12-31 as WRONG.
  B1-B5 THE BODY (--body-file; the tester reads the matched sentence, never just the regex): B1 the card id; B2 the grant file name;
     B3 a valid-through statement (pr3 "valid through 30 Oct", pr4 "valid through 31 Dec"); B4 the rows / entry named (pr3 both GHSA ids,
     pr4 the mobile tree dir); B5 "no deploy" and a no-live-sweep / not-covered sentence.
  NOT COVERED (printed, each with its reason): no live `npm audit` / registry sweep (C3's leg-6 run used a CANNED report; leg 7's network
     half not run); no push preflight run end-to-end; nothing deployed or built; pr4's "81 advisories (2 critical, 45 high)" not re-measured;
     the react-router v7 migration (KS 528's real fix) not tested; the OTHER dated rows (3 lapse 2026-10-15, 2 on 2026-10-31) are not this
     gate's; .github/workflows/security-scan.yml runs the same audit-gate.mjs in CI and was not run.
--selftest: the given body must PASS; each body statement removed must FAIL its own row.
Usage: c5_notcovered_gate56a.py --which pr3|pr4 --body-file f [--selftest]   rc 0 PASS / 1 FAIL / 2 usage"""
import io, contextlib, json, os, re, sys
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from lib_gate56a import K, now, Checks, pr_cfg, opt_factory

A = sys.argv[1:]
if not A or '--help' in A or '-h' in A or '--which' not in A or '--body-file' not in A:
    print(__doc__); raise SystemExit(0 if ('--help' in A or '-h' in A) else 2)
opt = opt_factory(A); W = opt('--which'); P = pr_cfg(W); BF = opt('--body-file')
if not os.path.isfile(BF):
    print('REFUSING: body file %s absent' % BF); raise SystemExit(2)


def find_card(d, cid):
    if isinstance(d, dict):
        if d.get('id') == cid:
            return d
        for v in d.values():
            r = find_card(v, cid)
            if r: return r
    elif isinstance(d, list):
        for v in d:
            r = find_card(v, cid)
            if r: return r
    return None


VT = {'pr3': r'valid through 30 Oct', 'pr4': r'valid through 31 Dec'}[W]
NAMES = P['rows'] if W == 'pr3' else [P['entry_dir']]
BODY_RX = [('B1 card id', re.escape(P['authority_card'])), ('B2 grant file', re.escape(os.path.basename(K['grant_file']))), ('B3 valid-through', VT),
           ('B4 names', r'(?s)' + '.*'.join(re.escape(x) for x in NAMES)), ('B5 no deploy / not covered', r'(?is)no deploy.{0,400}(no live sweep|not covered)|(no live sweep|not covered).{0,400}no deploy')]


def authority():
    C = Checks()
    card = find_card(json.load(open(K['decisions_json'], encoding='utf-8')), P['authority_card']) or {}
    lab = next((o.get('label') for o in card.get('options', []) if o.get('key') == card.get('ruled_choice')), None)
    C.chk('A1 ruled card', card.get('status') == 'ruled' and card.get('ruled_choice') == P['authority_choice'] and card.get('ruled_ts') == P['authority_ruled_ts'] and lab == P['authority_label'],
          '%s status %s choice %s ruled_ts %s | ruled option label %r (kit %r)' % (P['authority_card'], card.get('status'), card.get('ruled_choice'), card.get('ruled_ts'), lab, P['authority_label']))
    g = open(K['grant_file'], encoding='utf-8').read() if os.path.isfile(K['grant_file']) else ''
    sc = re.search(r'\*\*Scope is re-dates only:\*\*[^\n]*\n[^\n]*\n[^\n]*', g)
    C.chk('A2 grant', K['grant_quote'] in g, '%s present %s | verbatim %r present %s | scope: %r' % (K['grant_file'], bool(g), K['grant_quote'], K['grant_quote'] in g, (sc.group(0) if sc else 'NOT FOUND')[:300]))
    if W == 'pr3':
        C.chk('A3 value', lab is not None and '31 Oct' in lab and P['new'] == '2026-10-31', 'card label names "31 Oct": %s | kit value %s' % (lab is not None and '31 Oct' in (lab or ''), P['new']))
    else:
        ans = open(K['seat_briefs'][2], encoding='utf-8').read() if os.path.isfile(K['seat_briefs'][2]) else ''
        C.chk('A3 value', 'write `2027-01-01`' in ans and '"2026-12-31" was WRONG' in ans and P['new'] == '2027-01-01',
              '%s carries "write `2027-01-01`" %s and names 2026-12-31 WRONG %s | kit value %s | %s' % (os.path.basename(K['seat_briefs'][2]), 'write `2027-01-01`' in ans, '"2026-12-31" was WRONG' in ans, P['new'], P['authority_value_ruling']))
    return C


def body_checks(body, C):
    for tag, rx in BODY_RX:
        m = re.search(rx, body or '', re.I)
        snip = body[max(0, m.start() - 40):m.end() + 40].replace('\n', ' ')[:220] if m else 'ABSENT'
        C.chk(tag, m is not None, 'body: %r' % snip)
    return C


print('c5_notcovered_gate56a %s | %s %s | body %s' % (now(), W, P['ticket'], BF))
BODY = open(BF, encoding='utf-8').read()
if '--selftest' in A:
    arms = [('T0 the given body', BODY, None)] + [('T-%s removed' % t.split()[0], re.sub(rx, '[removed by selftest]', BODY, flags=re.I), t.split()[0]) for t, rx in BODY_RX]
    ok = 0
    for name, b, want in arms:
        with contextlib.redirect_stdout(io.StringIO()):
            C = body_checks(b, Checks())
        f = C.failed(); good = (not f) if want is None else any(x.startswith(want) for x in f)
        ok += good; print('SELFTEST %s %s: want %s | failed %s' % ('OK' if good else 'MISS', name, 'PASS' if want is None else 'FAIL on ' + want, f or 'NONE'))
    print('SELFTEST %s %d of %d' % ('OK' if ok == len(arms) else 'BROKEN', ok, len(arms))); raise SystemExit(0 if ok == len(arms) else 1)
C = body_checks(BODY, authority())
print('NOT COVERED (each with its reason): no live npm audit / registry sweep (C3 leg-6 run used a CANNED report; leg 7 network half not run) | '
      'no push preflight run end-to-end | nothing deployed or built | %s | the react-router v7 migration (the real KS 528 fix) not tested | '
      'the other dated rows (3 lapse 2026-10-15, 2 on 2026-10-31) are not this gate\'s | security-scan.yml (CI) runs the same audit-gate.mjs and was not run' % (
          'the mobile tree\'s "81 advisories (2 critical, 45 high)" not re-measured' if W == 'pr4' else 'the accepted advisories remain OPEN (accepted, not fixed)'))
n = C.nfail(); print('C5 %s %s: %d FAIL of %d' % (W, 'PASS' if n == 0 else 'FAIL', n, len(C.res))); raise SystemExit(1 if n else 0)
