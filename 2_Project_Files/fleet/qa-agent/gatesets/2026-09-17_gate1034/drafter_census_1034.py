#!/usr/bin/env python3
"""drafter_census_1034.py — READ census (git grep in the drafter clone at head fd81a75f0; case-insensitive; positive controls) for lead question 4:
(a) upstream (non-gateway) service code that reads the inbound Authorization for anything beyond verifying it: re-forwarding it to another service,
    deriving an actor / audit identity from it, or reading x-user-* beside it;
(b) in-repo CLIENTS that send x-api-key AND Authorization together (the population whose request changes on an exchange failure);
(c) readers of rawAuthorization (the entry-captured caller header) anywhere.
Silence from git grep is printed as 0 only when the same-run positive control matched."""
import json, os, re, subprocess
GSD = os.path.dirname(os.path.abspath(__file__)); PA = json.load(open(GSD + '/drafter_paths.json')); C = PA['C']; H = PA['sha']['head']
def gg(pat, paths, extra=()):
    p = subprocess.run(['git', '-C', C, 'grep', '-n', '-I', '-i', '-E', *extra, pat, H, '--', *paths], capture_output=True, text=True)
    return [l[len(H) + 1:] for l in p.stdout.splitlines()], p.returncode, p.stderr.strip()[:200]
D = 'Blockchain/Dev/'
SVC = [D + 'services/', D + 'packages/shared/src/', ':!' + D + 'services/api-gateway/', ':!*__tests__*', ':!*.test.ts', ':!*.spec.ts', ':!*/dist/*']
ctl, rc, e = gg(r"headers\.authorization|headers\[.authorization.\]|get\(.authorization.\)|header\(.authorization.\)", [D + 'packages/shared/src/', ':!*__tests__*'])
print('(a) CONTROL: shared src readers of the Authorization header:', len(ctl), ctl[:4])
rd, rc, e = gg(r"headers\.authorization|headers\[.authorization.\]|get\(.authorization.\)|header\(.authorization.\)", SVC)
print('(a) upstream readers of the inbound Authorization (non-gateway, non-test):', len(rd))
fwd = [l for l in rd if re.search(r"authorization\s*[:=]\s*req\.|'?authorization'?\s*:\s*(req|authHeader|request)|Authorization:\s*req\.", l, re.I) or re.search(r"(Authorization|authorization)'?\s*:\s*req\.headers", l)]
print('(a1) lines that RE-FORWARD it onward (Authorization: req.headers…):', len(fwd))
for l in fwd[:60]: print('    ', l[:200])
by = {}
for l in rd: by.setdefault(l.split('/src/')[0].replace(D, ''), []).append(l)
print('(a2) readers per service:', {k: len(v) for k, v in sorted(by.items())})
act, rc, e = gg(r"x-user-id|x-user-email|x-user-role", SVC)
print('(a3) upstream readers of x-user-id / x-user-email / x-user-role (the headers the connector branch sets):', len(act), '| per service', {k: v for k, v in sorted(((l.split('/src/')[0].replace(D, ''), 0) for l in act))} if False else sorted({l.split('/src/')[0].replace(D, '') for l in act}))
cl, rc, e = gg(r"x-api-key", [D + 'frontend/', D + 'sdk/', D + 'packages/', D + 'systemTest/', 'Blockchain/Dev/scripts/', ':!*node_modules*', ':!*/dist/*', ':!Blockchain/Dev/services/'])
print('(b) client-side lines naming x-api-key outside services/:', len(cl))
files = sorted({l.split(':')[0] for l in cl})
both = []
for f in files:
    t = subprocess.run(['git', '-C', C, 'show', H + ':' + f], capture_output=True, text=True).stdout
    if re.search(r'authorization', t, re.I): both.append(f)
print('(b) files naming BOTH x-api-key and Authorization:', len(both), both[:40])
raw, rc, e = gg(r"rawAuthorization", ['Blockchain/Dev/', ':!*node_modules*'])
print('(c) rawAuthorization mentions anywhere (tests included):', len(raw)); [print('    ', l[:180]) for l in raw]
ctl2, rc, e = gg(r"authHeaders\(req", [D + 'services/api-gateway/src/routes/platform.ts'])
print('(c) CONTROL platform.ts authHeaders(req call sites:', len(ctl2), [l.split(':')[1] for l in ctl2])
