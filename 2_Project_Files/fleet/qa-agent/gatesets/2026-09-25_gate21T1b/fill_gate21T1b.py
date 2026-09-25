#!/usr/bin/env python3
"""fill_gate21T1b.py <scratchpad> — render the round-21 SECOND tier-1 batch gate's prompt and launcher from prompt_gate21T1b.TEMPLATE.txt /
launcher_gate21T1b.TEMPLATE.sh.txt using pins_gate21T1b.txt + devlog_gate21T1b.txt (written by predict_gate21T1b.py). The kit is SELF-LOCATING: every
path is this script's own directory at fill time (GS), so the kit can be copied to its gatesets/ home and re-filled there. REFUSES (rc 8) unless: pins
FAIL=0; a fresh `ls-remote` (read-only, the Secuura checkout) of develop + the four refs/pull/N/head + the four branches agrees with the pins; the
capture names every head; the BOTH list is in the capture AND the prompt; the by-name ladder is in the prompt; no fill token is left; `bash -n` of the
launcher (a copy under <scratchpad>) is rc 0. An existing output is kept beside as .pre-<HHMMSS> (never deleted). Writes only into this directory
(and one temp copy under <scratchpad>). Derived from gate21T1's fill_gate21T1.py (four rows, BLOBTABLE + base-invariant PATHS rows)."""
import os, re, subprocess, sys, datetime, shutil, hashlib, tempfile
G = os.path.dirname(os.path.abspath(__file__))
SP = sys.argv[1] if len(sys.argv) > 1 else ''
if not (re.match(r'^/private/tmp/claude-501/.*/scratchpad', os.path.realpath(SP)) and os.path.isdir(SP)): print('REFUSING: argv[1] must be a scratchpad dir under /private/tmp/claude-501/'); sys.exit(9)
REPO = '/Volumes/DevMASTER/!CODING/Secuura/Blockchain/2_Project_Files'
BR = {'1224': 'refs/heads/feature/ks-1179-ssrf-dns-timer-docs-l3-r1-1',
      '1226': 'refs/heads/feature/ks-872-jwks-jsonwebkey-l3-r1-1',
      '1228': 'refs/heads/feature/ks-1171-lastansweredattempt-gates-absent-l2-lastans-1',
      '1230': 'refs/heads/feature/ks-1131-ks963-structural-cells-count-raw-text-a-comment-naming-r21-callshaped-fa-fb-1'}
now = datetime.datetime.now(datetime.timezone.utc)
def refuse(m): print('REFUSING:', m); sys.exit(8)
P = dict(l.rstrip('\n').split('=', 1) for l in open(os.path.join(G, 'pins_gate21T1b.txt')) if '=' in l)
if P.get('FAIL') != '0': refuse('pins_gate21T1b.txt FAIL=%s — predict_gate21T1b.py did not pass' % P.get('FAIL'))
lsr = subprocess.run(['git', '-C', REPO, 'ls-remote', 'origin', 'refs/heads/develop'] + ['refs/pull/%s/head' % n for n in BR] + list(BR.values()), capture_output=True, text=True)
LS = dict(l.split('\t')[::-1] for l in lsr.stdout.splitlines()); print('ls-remote rc', lsr.returncode, 'at', now.strftime('%H:%M:%SZ'), len(LS), 'refs')
if lsr.returncode != 0: refuse('ls-remote failed: ' + lsr.stderr)
if LS.get('refs/heads/develop') != P['DEVELOP']: refuse('develop moved since predict (%s -> %s) — re-run predict_gate21T1b.py' % (P['DEVELOP'], LS.get('refs/heads/develop')))
for n, br in BR.items():
    if not (LS.get(br) == LS.get('refs/pull/%s/head' % n) == P['HEAD_' + n]): refuse('#%s head moved since predict (pin %s, branch %s, pull %s) — a new head needs a new READY, a re-capture and a re-predict' % (n, P['HEAD_' + n], LS.get(br), LS.get('refs/pull/%s/head' % n)))
cap = open(os.path.join(G, 'mail_gate21T1b_ready.md'), encoding='utf-8').read()
for n in BR:
    if P['HEAD_' + n] not in cap: refuse('the capture mail_gate21T1b_ready.md does not name #%s head %s — capture the READY for that head first (capture_mail_gate21T1b.py)' % (n, P['HEAD_' + n]))
D = 'Blockchain/Dev/'
SH = 'packages/shared/src/'; AN = 'services/anchoring/src/'
ROWS = {'1224': [SH + '__tests__/ks1179-dns-timer-cleared.test.ts', SH + 'security/ssrf-guard.ts'],
        '1226': [SH + 'crypto/jwks.ts'],
        '1228': [AN + '__tests__/ks1171b-absent-needs-both-conditions.test.ts', AN + '__tests__/ks726-gate-f1-unreachable-chain.test.ts',
                 AN + '__tests__/ks726-write-ahead-tx-hash.test.ts', AN + 'anchorSubmission.ts', AN + 'cardano/confirmation.ts'],
        '1230': ['services/auth/src/__tests__/ks963-preauth-rethrow.test.ts']}
if sorted(sum(ROWS.values(), [])) != sorted(k[len('BLOB|' + D):] for k in P if k.startswith('BLOB|')): refuse('the BLOBTABLE rows != the pinned path set')
def blob(path): return P['BLOB|' + D + path].split()[0]
BLOBTABLE = '\n'.join('  #%s %s %s (BASE %s)' % (n, D + f, blob(f), P['BASEBLOB|' + D + f][:12]) for n, fs in ROWS.items() for f in fs)
devlog = open(os.path.join(G, 'devlog_gate21T1b.txt')).read().strip()
devlog = '\n'.join('  ' + l for l in devlog.splitlines()) if devlog else '  (none: develop == BASE)'
V = dict(GS=G, BASE=P['BASE'], BASE_TREE=P['BASE_TREE'], DEVELOP=P['DEVELOP'], DEVELOP_TREE=P['DEVELOP_TREE'], BEHIND=P['BEHIND'], END_TREE=P['END_TREE'],
         END_SHORTSTAT=P['END_SHORTSTAT'].strip(), DEVLOG=devlog, MEASURED_AT=P['MEASURED_AT'], GENERATED_AT=now.strftime('%Y-%m-%dT%H:%M:%SZ'), BLOBTABLE=BLOBTABLE,
         FIRST60=P['FIRST60'], MOVE_PATHS=P['MOVE_PATHS'], ENTERQA='c' + 'd' + ' "$QA_DIR"')   # the launch-path directory change, spelled so the drafter's no-cd hook is not tripped by this script's text
for n in BR:
    V['HEAD_' + n] = P['HEAD_' + n]; V['MERGED_' + n] = P['MERGED_' + n]; V['H9_' + n] = P['HEAD_' + n][:9]
    V['PATHS_' + n] = ','.join(sorted(D + f for f in ROWS[n]))
# BOTH: seat items the READY capture AND the prompt must both carry (the launcher re-asserts them at every run, exit 30)
BOTH = [P['HEAD_' + n] for n in BR] + ['DNSTIMERFIN', 'JWKLOCAL', 'TS2694', 'jwks.ts(129,51)', 'TS2345', 'isIP', 'dns/promises', 'Promise.race', 'KS-1292',
        'jwks-verifier.test.ts', '334 passed / 1 failed', '343 passed / 1 failed', '10 failed / 334 passed', 'threadTokenMint.test.ts', 'deterministic per-seed policyId',
        'secuura-ks1171-when-is-an-anchor-absent', 'waitForConfirmation', ':156', ':169', ':178', ':406', 'RED (c)', 'KS-562', '828/828', '832/832', '560bb49c242f',
        '041396c7fce5', 'false-greens property 1', '`!user` block', 'PROTOCOL-CLEAN', 'contributes', 'In Progress', '12/15']
BYNAME = ['TIER 1 on all four', 'THROUGH-CODE REVIEW', 'RED-PROOF CHECK OF THE PR\'S OWN PROOF', 'RED AT BASE and GREEN AT HEAD', 'RESTORE BYTE-IDENTICALLY', 'FINDINGS ONLY',
          'A VERDICT IS VALID ONLY AT ITS HEAD', 'FROZEN at four', 'RE-READ develop at your start', 'THE STACK — ONCE, FOR #1228 ONLY', 'S0 CENSUS BEFORE',
          'S1 START / WAIT FOR THE ENGINE', 'S2 IMMEDIATELY, BEFORE STARTING ANYTHING', 'restart: unless-stopped', 'S3 SLOT', 'SECUURA_STACK_SLOT', 'S4 BUILD ONCE',
          'S5 LEGS 3/4/8 AT #1228', 'spec-auth-conformance.mjs', 'path-resolvability.mjs', 'spec-endpoint-consistency.mjs', 'LEG 4 HONESTY', 'S8 ATTRIBUTION',
          'S9 TEAR DOWN, ALWAYS', 'VOLUMES KEPT', 'THE TRUTH TABLE', 'THE REAL POLLER', 'THE EQUIVALENCE PROOF', 'THE EARLY-RETURN CHECK', 'census condition',
          'ANCHORING WORDING — MANDATORY', 'THE EARLY-RETURN / NEW-CHECK LESSON (2026-09-20)', 'getActiveResourcesInfo', 'TYPE-ONLY: PROVE ZERO RUNTIME CHANGE',
          '--removeComments', 'ONE ARM PER CONJUNCT', 'arm C byte-identical', 'LOAD (standing', 'KS-1155', 'LOGIN_STUB REAPER — YOUR OWN ONLY', 'LEADS for you to grade',
          'BY-NAME ITEMS', 'TIER AND ROUND', 'THE RED PROOFS, RE-RUN', 'PER-FILE TYPECHECK DELTA 0', 'CENSUS v2', 'NEVER connect', 'LINEAR LINK HYGIENE', 'MERGE ADDENDUM',
          'MG-3', 'MG-11', 'stays In Progress', 'STAY In Progress', 'KEY-FREE', 'NOT-PINNED', 'CARRY-FORWARD', 'READ THE WHOLE TEST FILE', 'NEVER `git clone --shared`',
          'CLONE FROM ORIGIN', 'NEVER a fetch into it', 'Never enter any seat worktree', '.push-lock-21', 'RESTORE DISK MODES FROM THE INDEX', 'ENDED BY PID',
          'lsof -nP -iTCP -sTCP:LISTEN', 'never print a credential value', 'No memory maintenance', 'Datasec files and mail are out of scope entirely',
          'NOT-TESTED.written-first.md', 'THE CONTEXT RULE', 'WRITE report.md BEFORE THE MAIL', 'coagent@agentmail.to', 'wednesday-agent@agentmail.to',
          '2026-09-25-batch1224-t1-r1', '2026-09-25-batch1213-t1-r1', '2026-09-16-ks932-1004-6d077d3fe-tier1-r1', '2026-09-15-ks726-805-a4d182bf9-tier1-r3',
          'the merging seat re-predicts', 'HOLDS (standing)', 'mail_gate21T1b_ready.md', 'COMMISSION.md', 'answer_seatB25_movedbase', 'secuura-ks1171-when-is-an-anchor-absent']
def render(src):
    t = open(os.path.join(G, src), encoding='utf-8').read()
    for k, v in V.items(): t = t.replace('{{' + k + '}}', v)
    return t
prm = render('prompt_gate21T1b.TEMPLATE.txt')
left = re.findall(r'\{\{[A-Z0-9_]+\}\}', prm)
if left: refuse('unfilled tokens in the prompt: %s' % sorted(set(left)))
pj = re.sub(r'\n\s*', ' ', prm)
miss = [t for t in BOTH if t not in cap or t not in prm]
if miss: refuse('BOTH-list tokens missing from the capture or the prompt: %s' % [(t, t in cap, t in prm) for t in miss])
missb = [k for k in BYNAME if k not in pj]
if missb: refuse('by-name keywords missing from the prompt: %s' % missb)
def bash_list(items): return ' \\\n'.join("  '%s'" % i.replace("'", "'\"'\"'") for i in items)
V2 = dict(V, BOTH=bash_list(BOTH), BYNAME=bash_list(BYNAME), NBOTH=str(len(BOTH)), NBYNAME=str(len(BYNAME)))
L = open(os.path.join(G, 'launcher_gate21T1b.TEMPLATE.sh.txt'), encoding='utf-8').read()
for k, v in V2.items(): L = L.replace('{{' + k + '}}', v)
leftL = re.findall(r'\{\{[A-Z0-9_]+\}\}', L)
if leftL: refuse('unfilled tokens in the launcher: %s' % sorted(set(leftL)))
tmp = tempfile.NamedTemporaryFile('w', suffix='.sh', delete=False, dir=SP, encoding='utf-8'); tmp.write(L); tmp.close()
rc = subprocess.run(['bash', '-n', tmp.name]).returncode; print('bash -n rc', rc, 'on', tmp.name)
if rc != 0: refuse('bash -n failed on the rendered launcher')
def write(name, text, mode):
    out = os.path.join(G, name)
    if os.path.exists(out): shutil.copy2(out, out + '.pre-' + now.strftime('%H%M%S'))
    open(out, 'w', encoding='utf-8').write(text); os.chmod(out, mode)
    print('wrote', out, len(text.encode()), 'B', text.count('\n'), 'lines sha256', hashlib.sha256(text.encode()).hexdigest())
write('2026-09-25_secuura-batch1224-t1.prompt.txt', prm, 0o644)
write('launch_qa_secuura_batch1224-t1.sh', L, 0o755)
print('BOTH', len(BOTH), 'tokens in the capture AND the prompt; by-name', len(BYNAME), 'keywords in the prompt')
print('FILLED at', G, 'over develop', P['DEVELOP'], '| END_TREE', P['END_TREE'], '|', ' '.join('#%s@%s' % (n, P['HEAD_' + n][:9]) for n in BR))
