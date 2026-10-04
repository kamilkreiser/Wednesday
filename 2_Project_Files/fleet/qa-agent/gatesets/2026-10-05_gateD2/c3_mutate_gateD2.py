#!/usr/bin/env python3
"""c3_mutate_gateD2.py — the gateD2 C3 MUTATION planter. Disables ONE guard line in the product (by exact string, asserting it occurs ONCE)
so the KS 1404 cells can be shown to be able to fail. It writes ONLY the one file it is given, which must lie in a SCRATCH worktree under
/private/tmp/claude-501/ (refused otherwise, before any write). The caller restores from the head blob and proves sha256 equality.
Arms (file relative to services/timestamping/src; MUST-GO-RED cells are judged by c3_parse_gateD2.py mutation):
  sig       tsa/rfc3161-verify.ts  `if (!sigOk) return refuse(`                      -> if (false) ...   want cell 2 red
  indef     tsa/rfc3161-verify.ts  `if (findIndefinite(asn.result)) {`                -> if (false) {     want cell 11f red
  imprint   tsa/rfc3161-verify.ts  `if (imprint.length !== expected.length || ...`   -> if (false) {     want cell 3b red
  chain     tsa/rfc3161-verify.ts  `if (!chain?.result) {`                            -> if (false) {     want cell 6 red
  anchors   tsa/rfc3161-verify.ts  `if (anchors.length === 0) return refuse(...)`     -> removed          want cell 7 red
  eku       tsa/rfc3161-verify.ts  `if (!purposes.includes(OID.timeStamping)) {`     -> if (false) {     want cell 8 red
  md        tsa/rfc3161-verify.ts  `if (!declared.equals(actual)) return refuse(`    -> if (false) ...   want cell 10b red
  validity  tsa/rfc3161-verify.ts  `if (genTime < signer.notBefore.value || ...`     -> if (false) {     want cell 9 red
  mockpath  tsa/qualified-tsa.ts   `if (tokenBuf.length === 0 || tokenBuf[0] !== 0x30) {` -> if (false) {  REPORT only (a JSON token then
            meets the DER parser, which refuses it too: defence in depth, so no cell is expected to go red alone)
Usage: c3_mutate_gateD2.py list | plant <arm> <services/timestamping dir>   rc 0 planted / 1 the anchor string is not exactly once / 2 refusal"""
import os, sys
ARMS = {
    'sig': ('tsa/rfc3161-verify.ts', "if (!sigOk) return refuse(", "if (false) return refuse("),
    'indef': ('tsa/rfc3161-verify.ts', "if (findIndefinite(asn.result)) {", "if (false) {"),
    'imprint': ('tsa/rfc3161-verify.ts', "if (imprint.length !== expected.length || !imprint.equals(expected)) {", "if (false) {"),
    'chain': ('tsa/rfc3161-verify.ts', "if (!chain?.result) {", "if (false) {"),
    'anchors': ('tsa/rfc3161-verify.ts', "if (anchors.length === 0) return refuse('no trust anchor configured');", "/* gD2 mutation: fail-closed guard removed */"),
    'eku': ('tsa/rfc3161-verify.ts', "if (!purposes.includes(OID.timeStamping)) {", "if (false) {"),
    'md': ('tsa/rfc3161-verify.ts', "if (!declared.equals(actual)) return refuse(", "if (false) return refuse("),
    'validity': ('tsa/rfc3161-verify.ts', "if (genTime < signer.notBefore.value || genTime > signer.notAfter.value) {", "if (false) {"),
    'mockpath': ('tsa/qualified-tsa.ts', "if (tokenBuf.length === 0 || tokenBuf[0] !== 0x30) {", "if (false) {"),
}
A = sys.argv[1:]
if not A or A[0] in ('-h', '--help'): print(__doc__); raise SystemExit(0 if A else 2)
if A[0] == 'list':
    for k, (f, a, b) in ARMS.items(): print('%-9s %s | %r -> %r' % (k, f, a, b))
    raise SystemExit(0)
if A[0] != 'plant' or len(A) != 3 or A[1] not in ARMS: print(__doc__); raise SystemExit(2)
f, a, b = ARMS[A[1]]; p = os.path.abspath(os.path.join(A[2], 'src', f))
if not p.startswith('/private/tmp/claude-501/'): print('REFUSING: %s is not in a scratch worktree under /private/tmp/claude-501/ (nothing written)' % p); raise SystemExit(2)
t = open(p, encoding='utf-8').read(); n = t.count(a)
if n != 1: print('MUTATION %s: anchor occurs %d times in %s (want exactly 1) — NOT planted; the product moved: re-key the arm' % (A[1], n, p)); raise SystemExit(1)
open(p, 'w', encoding='utf-8').write(t.replace(a, b, 1)); print('MUTATION %s planted in %s: %r -> %r' % (A[1], p, a, b))
