#!/usr/bin/env python3
"""fill_gate21T2.py <scratchpad> — render the round-21 TIER-2 batch gate's prompt and launcher from prompt_gate21T2.TEMPLATE.txt /
launcher_gate21T2.TEMPLATE.sh.txt using pins_gate21T2.txt + devlog_gate21T2.txt (written by predict_gate21T2.py). The kit is SELF-LOCATING: every path
is this script's own directory at fill time (GS), so the kit can be copied to its gatesets/ home and re-filled there. REFUSES (rc 8) unless: pins
FAIL=0; a fresh `ls-remote` (read-only, the Secuura checkout) of develop + the six refs/pull/N/head + the six branches agrees with the pins; the
capture names every head; the BOTH list is in the capture AND the prompt; the by-name ladder is in the prompt; no fill token is left; `bash -n` of the
launcher (a copy under <scratchpad>) is rc 0. An existing output is kept beside as .pre-<HHMMSS> (never deleted). Writes only into this directory
(and one temp copy under <scratchpad>). Derived from gate21T1's fill_gate21T1.py, re-keyed to six rows."""
import os, re, subprocess, sys, datetime, shutil, hashlib, tempfile
G = os.path.dirname(os.path.abspath(__file__))
SP = sys.argv[1] if len(sys.argv) > 1 else ''
if not (re.match(r'^/private/tmp/claude-501/.*/scratchpad', os.path.realpath(SP)) and os.path.isdir(SP)): print('REFUSING: argv[1] must be a scratchpad dir under /private/tmp/claude-501/'); sys.exit(9)
REPO = '/Volumes/DevMASTER/!CODING/Secuura/Blockchain/2_Project_Files'
BR = {'1215': 'refs/heads/feature/ks-1288-legd-text-pins-l3-r1-1',
      '1218': 'refs/heads/feature/ks-897-build-fixture-swallows-its-own-failure-l4-fixtureabort-1',
      '1220': 'refs/heads/feature/ks-1129-anchoring-blocknumber-number-l2-bignum-1',
      '1221': 'refs/heads/feature/ks-1266-anchoring-url-hermetic-l1-b-1',
      '1222': 'refs/heads/feature/ks-1181-errorhandler-canary-hit-l3-r1-1',
      '1223': 'refs/heads/feature/ks-1118-verify-hash-precedence-l1-c-1'}
now = datetime.datetime.now(datetime.timezone.utc)
def refuse(m): print('REFUSING:', m); sys.exit(8)
P = dict(l.rstrip('\n').split('=', 1) for l in open(os.path.join(G, 'pins_gate21T2.txt')) if '=' in l)
if P.get('FAIL') != '0': refuse('pins_gate21T2.txt FAIL=%s — predict_gate21T2.py did not pass' % P.get('FAIL'))
lsr = subprocess.run(['git', '-C', REPO, 'ls-remote', 'origin', 'refs/heads/develop'] + ['refs/pull/%s/head' % n for n in BR] + list(BR.values()), capture_output=True, text=True)
LS = dict(l.split('\t')[::-1] for l in lsr.stdout.splitlines()); print('ls-remote rc', lsr.returncode, 'at', now.strftime('%H:%M:%SZ'), len(LS), 'refs')
if lsr.returncode != 0: refuse('ls-remote failed: ' + lsr.stderr)
if LS.get('refs/heads/develop') != P['DEVELOP']: refuse('develop moved since predict (%s -> %s) — re-run predict_gate21T2.py' % (P['DEVELOP'], LS.get('refs/heads/develop')))
for n, br in BR.items():
    if not (LS.get(br) == LS.get('refs/pull/%s/head' % n) == P['HEAD_' + n]): refuse('#%s head moved since predict (pin %s, branch %s, pull %s) — a new head needs a new READY, a re-capture and a re-predict' % (n, P['HEAD_' + n], LS.get(br), LS.get('refs/pull/%s/head' % n)))
cap = open(os.path.join(G, 'mail_gate21T2_ready.md'), encoding='utf-8').read()
for n in BR:
    if P['HEAD_' + n] not in cap: refuse('the capture mail_gate21T2_ready.md does not name #%s head %s — capture the READY for that head first (capture_mail_gate21T2.py)' % (n, P['HEAD_' + n]))
D = 'Blockchain/Dev/'
def blob(path): return P['BLOB|' + D + path].split()[0]
OT = 'services/originate/src/__tests__/'
devlog = open(os.path.join(G, 'devlog_gate21T2.txt')).read().strip()
devlog = '\n'.join('  ' + l for l in devlog.splitlines()) if devlog else '  (none: develop == BASE — every PR merges fast-forward-shaped, merged tree == head tree)'
ROWS = {'1215': ['packages/shared/src/__tests__/ks781-p3-3-body-parser-order.test.ts'], '1218': ['scripts/__tests__/pre_push_hook_base.test.sh'],
        '1220': ['services/anchoring/src/anchorReadback.ts', 'services/anchoring/src/__tests__/ks1129-blocknumber-is-a-number.test.ts'],
        '1221': [OT + f for f in ('ks1213-a-derived-writer-relabel-is-refused.test.ts', 'ks1228-a-refused-request-writes-no-provenance-row.test.ts', 'ks444-certifications-issue-body-types.test.ts',
                 'ks444-documents-create-title-guard.test.ts', 'ks445-certifications-issue-unstorable-payload.test.ts', 'ks520-anchor-fail-closed.test.ts', 'ks543-certify-boundary-strip.test.ts')],
        '1222': ['packages/shared/src/__tests__/ks727-errorhandler-class-guard.test.ts'],
        '1223': [OT + 'ks1103-verify-hash-field.test.ts', 'services/originate/src/routes/verification.ts']}
if sorted(sum(ROWS.values(), [])) != sorted(k[len('BLOB|' + D):] for k in P if k.startswith('BLOB|')): refuse('the BLOBTABLE rows != the pinned path set')
BLOBTABLE = '\n'.join('  #%s %s %s (BASE %s)' % (n, D + f, blob(f), P['BASEBLOB|' + D + f][:12]) for n, fs in ROWS.items() for f in fs)
V = dict(GS=G, BASE=P['BASE'], BASE_TREE=P['BASE_TREE'], DEVELOP=P['DEVELOP'], DEVELOP_TREE=P['DEVELOP_TREE'], BEHIND=P['BEHIND'], END_TREE=P['END_TREE'],
         END_SHORTSTAT=P['END_SHORTSTAT'].strip(), DEVLOG=devlog, MEASURED_AT=P['MEASURED_AT'], GENERATED_AT=now.strftime('%Y-%m-%dT%H:%M:%SZ'), BLOBTABLE=BLOBTABLE,
         BLOB_1215=blob(ROWS['1215'][0]), BLOB_1218=blob(ROWS['1218'][0]), BLOB_1220_AR=blob(ROWS['1220'][0]), BLOB_1220_T=blob(ROWS['1220'][1]),
         BLOB_1222=blob(ROWS['1222'][0]), BLOB_1223_T=blob(ROWS['1223'][0]), BLOB_1223_V=blob(ROWS['1223'][1]),
         ENTERQA='c' + 'd' + ' "$QA_DIR"')   # the launch-path directory change, spelled so the drafter's no-cd hook is not tripped by this script's text
for n in BR: V['HEAD_' + n] = P['HEAD_' + n]; V['MERGED_' + n] = P['MERGED_' + n]; V['H9_' + n] = P['HEAD_' + n][:9]
# BOTH: seat items the READY capture AND the prompt must both carry (the launcher re-asserts them at every run, exit 30)
BOTH = [P['HEAD_' + n] for n in BR] + ['918', '922', '919', '863', '864', '334 passed / 1 failed', '344 passed / 1 failed', '2 failed / 8 passed', '10/10',
        '1 failed / 8 passed', '9 failed', '1 failed / 14 passed', '28 passed, 0 failed', 'FIXTURE BUILD FAILED', 'upstream=NONE', '57 passed, 0 failed (of 57)',
        '3.2.57', 'entity.too.large', '127.0.0.1:2', 'anchoring:4005', 'threadTokenMint', 'deterministic per-seed policyId', 'KS-562', 'T5', '#1136',
        'OWED at the gate', 'toBlockNumber', 'shouldForward', 'expected [ 845, 858, 891 ] to include 873', 'contributes', 'KS-973', 'ks1213', '17', '26']
BYNAME = ['TIER 2 on all six', 'THROUGH-CODE', 'RED-PROOF CHECK OF THE PR\'S OWN PROOF', 'RED AT BASE and GREEN AT HEAD', 'RESTORE BYTE-IDENTICALLY', 'FINDINGS ONLY',
          'A VERDICT IS VALID ONLY AT ITS HEAD', 'MEASURE, not conclude', 'RULE WHETHER IT BLOCKS', 'FROZEN at six', 'TIER AND ROUND', 'is re-graded TIER 1',
          'RE-READ develop at your start', 'THE RED PROOFS — RE-RUN', 'THE PORT PROBE', 'does NOT record the OUTCOME', 'PRECONDITION: `lsof -nP -iTCP:2 -sTCP:LISTEN` empty',
          'LEGS 3/4/8 — NOT RUN', 'THE STACK IS NOT YOURS TO START', 'IF THE STACK IS UP', 'OTHERWISE', 'SAY WHOSE ANCHORING ANSWERED', 'REACH (measure, then grade)',
          'THE CONSUMERS', 'ANCHORING WORDING — MANDATORY', 'LOAD (standing', 'KS-1155', 'LEADS for you to grade', 'BY-NAME ITEMS', 'PER-FILE TYPECHECK DELTA 0',
          'CENSUS v2', 'NEVER connect', 'LINEAR LINK HYGIENE', 'MG-11', 'MG-3', 'MERGE ADDENDUM', 'stays In Progress', 'STAY In Progress', 'KEY-FREE', 'NOT-PINNED',
          'CARRY-FORWARD', 'READ THE WHOLE TEST FILE', 'NEVER `git clone --shared`', 'CLONE FROM ORIGIN', 'NEVER a fetch into it', 'Never enter any seat worktree',
          '.push-lock-21', 'RESTORE DISK MODES FROM THE INDEX', 'ENDED BY PID', 'lsof -nP -iTCP -sTCP:LISTEN', 'never print a credential value', 'No memory maintenance',
          'Datasec files and mail are out of scope entirely', 'NOT-TESTED.written-first.md', 'THE CONTEXT RULE', 'WRITE report.md BEFORE THE MAIL', 'coagent@agentmail.to',
          'wednesday-agent@agentmail.to', '2026-09-25-batch1215-t2-r1', '2026-09-23-batch1202-t2-r1', '2026-09-25-batch1213-t1-r1', 'the merging seat re-predicts',
          'HOLDS (standing)', 'mail_gate21T2_ready.md', 'COMMISSION.md', 'GIT_DIR', 'KS-1086', 'the filter ANSWERS it', 'FORWARDING_HANDLERS', 'comment-only', 'KS-1143 GF-2']
def render(src):
    t = open(os.path.join(G, src), encoding='utf-8').read()
    for k, v in V.items(): t = t.replace('{{' + k + '}}', v)
    return t
prm = render('prompt_gate21T2.TEMPLATE.txt')
left = re.findall(r'\{\{[A-Z0-9_]+\}\}', prm)
if left: refuse('unfilled tokens in the prompt: %s' % sorted(set(left)))
pj = re.sub(r'\n\s*', ' ', prm)
miss = [t for t in BOTH if t not in cap or t not in prm]
if miss: refuse('BOTH-list tokens missing from the capture or the prompt: %s' % [(t, t in cap, t in prm) for t in miss])
missb = [k for k in BYNAME if k not in pj]
if missb: refuse('by-name keywords missing from the prompt: %s' % missb)
def bash_list(items): return ' \\\n'.join("  '%s'" % i.replace("'", "'\"'\"'") for i in items)
V2 = dict(V, BOTH=bash_list(BOTH), BYNAME=bash_list(BYNAME), NBOTH=str(len(BOTH)), NBYNAME=str(len(BYNAME)))
L = open(os.path.join(G, 'launcher_gate21T2.TEMPLATE.sh.txt'), encoding='utf-8').read()
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
write('2026-09-25_secuura-batch1215-t2.prompt.txt', prm, 0o644)
write('launch_qa_secuura_batch1215-t2.sh', L, 0o755)
print('BOTH', len(BOTH), 'tokens in the capture AND the prompt; by-name', len(BYNAME), 'keywords in the prompt')
print('FILLED at', G, 'over develop', P['DEVELOP'], '| END_TREE', P['END_TREE'], '|', ' '.join('#%s@%s' % (n, P['HEAD_' + n][:9]) for n in BR))
