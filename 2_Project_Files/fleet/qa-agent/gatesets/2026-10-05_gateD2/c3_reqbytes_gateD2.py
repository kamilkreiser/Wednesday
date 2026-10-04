#!/usr/bin/env python3
"""c3_reqbytes_gateD2.py — compare the request-bytes probe's BASE (node-forge) and HEAD (der.ts) outputs case by case.
  Q1 same case set, >= 20 cases; Q2 every case byte-identical; Q3 the two ruled quirks are PRESENT in the base bytes themselves (so the
  equality is not vacuous): nonce 0000112233445566 encodes as 02 07 00 11 22 .. (ONE zero stripped, one kept) and ff00112233445566 as
  02 08 ff 00 .. (NO sign prefix: a negative INTEGER).
  --selftest: one flipped byte in a head copy must FAIL Q2; a base file without the quirk must FAIL Q3; identical real-shaped files PASS.
Usage: c3_reqbytes_gateD2.py <base.json> <head.json> | --selftest     rc 0 PASS / 1 FAIL / 2 usage"""
import json, sys, io, contextlib


def judge(b, h):
    res = []
    g1 = sorted(b) == sorted(h) and len(b) >= 20; res.append(g1); print('%s Q1 case sets equal (%d / %d, want >= 20)' % ('PASS' if g1 else 'FAIL', len(b), len(h)))
    diff = sorted(k for k in b if h.get(k) != b[k]); g2 = not diff; res.append(g2)
    print('%s Q2 byte-identical: %d differing case(s) %s' % ('PASS' if g2 else 'FAIL', len(diff), [(k, b[k][-30:], (h.get(k) or '')[-30:]) for k in diff[:3]]))
    k1 = 'SHA-256|0000112233445566|true|-'; k2 = 'SHA-256|ff00112233445566|true|-'
    q1 = '0207001122334455' + '66' in (b.get(k1) or ''); q2 = '0208ff00112233445566' in (b.get(k2) or '')
    g3 = q1 and q2; res.append(g3); print('%s Q3 the forge quirks are in the BASE bytes: one-zero strip %s | no sign prefix %s' % ('PASS' if g3 else 'FAIL', q1, q2))
    return all(res)


A = sys.argv[1:]
if not A or A[0] in ('-h', '--help'): print(__doc__); raise SystemExit(0 if A else 2)
if A[0] == '--selftest':
    k1 = 'SHA-256|0000112233445566|true|-'; k2 = 'SHA-256|ff00112233445566|true|-'
    B = {('c%d' % i): '3042%02x' % i for i in range(22)}; B[k1] = '30..02070011223344556601'; B[k2] = '30..0208ff00112233445566'
    H = dict(B); F = dict(B); F['c3'] = F['c3'][:-1] + ('0' if F['c3'][-1] != '0' else '1'); NQ = dict(B); NQ[k2] = '30..020900ff00112233445566'
    arms = [('T0 identical', B, H, True), ('T1 one flipped nibble', B, F, False), ('T2 base without the sign quirk', NQ, NQ, False)]; ok = 0
    for n, b, h, want in arms:
        buf = io.StringIO()
        with contextlib.redirect_stdout(buf): got = judge(b, h)
        ok += got == want; print('SELFTEST %s %s: want %s got %s' % ('OK' if got == want else 'MISS', n, want, got))
    print('SELFTEST %s %d of %d' % ('OK' if ok == len(arms) else 'BROKEN', ok, len(arms))); raise SystemExit(0 if ok == len(arms) else 1)
if len(A) != 2: print(__doc__); raise SystemExit(2)
r = judge(json.load(open(A[0])), json.load(open(A[1])))
print('REQBYTES %s' % ('PASS' if r else 'FAIL')); raise SystemExit(0 if r else 1)
