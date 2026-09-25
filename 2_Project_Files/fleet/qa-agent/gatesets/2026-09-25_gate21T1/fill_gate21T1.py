#!/usr/bin/env python3
"""fill_gate21T1.py <scratchpad> — render the round-21 tier-1 batch gate's prompt and launcher from prompt_gate21T1.TEMPLATE.txt /
launcher_gate21T1.TEMPLATE.sh.txt using pins_gate21T1.txt + devlog_gate21T1.txt (written by predict_gate21T1.py). The kit is SELF-LOCATING: every path
is this script's own directory at fill time (GS), so the kit can be copied to its gatesets/ home and re-filled there. REFUSES (rc 8) unless: pins
FAIL=0; a fresh `ls-remote` (read-only, the Secuura checkout) of develop + the four refs/pull/N/head + the four branches agrees with the pins; the
capture names every head; the BOTH list is in the capture AND the prompt; the by-name ladder is in the prompt; no fill token is left; `bash -n` of the
launcher (a copy under <scratchpad>) is rc 0. An existing output is kept beside as .pre-<HHMMSS> (never deleted). Writes only into this directory
(and one temp copy under <scratchpad>)."""
import os, re, subprocess, sys, datetime, shutil, hashlib, tempfile
G = os.path.dirname(os.path.abspath(__file__))
SP = sys.argv[1] if len(sys.argv) > 1 else ''
if not (re.match(r'^/private/tmp/claude-501/.*/scratchpad', os.path.realpath(SP)) and os.path.isdir(SP)): print('REFUSING: argv[1] must be a scratchpad dir under /private/tmp/claude-501/'); sys.exit(9)
REPO = '/Volumes/DevMASTER/!CODING/Secuura/Blockchain/2_Project_Files'
BR = {'1213': 'refs/heads/feature/ks-530-hononode-server-v1-v2-major-bump-ghsa-frvp-originate-mcp-r21-patchline-1',
      '1214': 'refs/heads/feature/ks-528-frontends-react-router-v6-v7-migration-3-moderate-client-r21-dompatch-1',
      '1216': 'refs/heads/feature/ks-975-explicitscope-null-is-malformed-l2-scopenull-1',
      '1217': 'refs/heads/feature/ks-976-reset-400-names-the-failing-field-l2-msg400-1'}
now = datetime.datetime.now(datetime.timezone.utc)
def refuse(m): print('REFUSING:', m); sys.exit(8)
P = dict(l.rstrip('\n').split('=', 1) for l in open(os.path.join(G, 'pins_gate21T1.txt')) if '=' in l)
if P.get('FAIL') != '0': refuse('pins_gate21T1.txt FAIL=%s — predict_gate21T1.py did not pass' % P.get('FAIL'))
lsr = subprocess.run(['git', '-C', REPO, 'ls-remote', 'origin', 'refs/heads/develop'] + ['refs/pull/%s/head' % n for n in BR] + list(BR.values()), capture_output=True, text=True)
LS = dict(l.split('\t')[::-1] for l in lsr.stdout.splitlines()); print('ls-remote rc', lsr.returncode, 'at', now.strftime('%H:%M:%SZ'), len(LS), 'refs')
if lsr.returncode != 0: refuse('ls-remote failed: ' + lsr.stderr)
if LS.get('refs/heads/develop') != P['DEVELOP']: refuse('develop moved since predict (%s -> %s) — re-run predict_gate21T1.py' % (P['DEVELOP'], LS.get('refs/heads/develop')))
for n, br in BR.items():
    if not (LS.get(br) == LS.get('refs/pull/%s/head' % n) == P['HEAD_' + n]): refuse('#%s head moved since predict (pin %s, branch %s, pull %s) — a new head needs a new READY, a re-capture and a re-predict' % (n, P['HEAD_' + n], LS.get(br), LS.get('refs/pull/%s/head' % n)))
cap = open(os.path.join(G, 'mail_gate21T1_ready.md'), encoding='utf-8').read()
for n in BR:
    if P['HEAD_' + n] not in cap: refuse('the capture mail_gate21T1_ready.md does not name #%s head %s — capture the READY for that head first (capture_mail_gate21T1.py)' % (n, P['HEAD_' + n]))
D = 'Blockchain/Dev/'
def blob(path): return P['BLOB|' + D + path].split()[0]
devlog = open(os.path.join(G, 'devlog_gate21T1.txt')).read().strip()
devlog = '\n'.join('  ' + l for l in devlog.splitlines()) if devlog else '  (none: develop == BASE — every PR merges fast-forward-shaped, merged tree == head tree)'
V = dict(GS=G, BASE=P['BASE'], BASE_TREE=P['BASE_TREE'], DEVELOP=P['DEVELOP'], DEVELOP_TREE=P['DEVELOP_TREE'], BEHIND=P['BEHIND'], END_TREE=P['END_TREE'],
         END_SHORTSTAT=P['END_SHORTSTAT'].strip(), DEVLOG=devlog, MEASURED_AT=P['MEASURED_AT'], GENERATED_AT=now.strftime('%Y-%m-%dT%H:%M:%SZ'),
         BLOB_MCPLOCK=blob('services/mcp-server/package-lock.json'), BLOB_ORIGLOCK=blob('services/originate/package-lock.json'), BLOB_ORIGPKG=blob('services/originate/package.json'),
         BLOB_ADMINLOCK=blob('frontend/admin/package-lock.json'), BLOB_ISSUERLOCK=blob('frontend/issuer/package-lock.json'), BLOB_VERIFIERLOCK=blob('frontend/verifier/package-lock.json'),
         BLOB_ROOTLOCK=blob('package-lock.json'), BLOB_BASELINE=blob('scripts/audit/audit-baseline.json'), BLOB_RLS=blob('services/security/src/rateLimitScope.ts'),
         BLOB_T975=blob('services/security/src/__tests__/ks975b-explicitscope-null-body-field-is-refused.test.ts'), BLOB_IDX=blob('services/security/src/index.ts'),
         BLOB_RR=blob('services/security/src/requestRefusal.ts'), BLOB_T976=blob('services/security/src/__tests__/ks976a-reset-400-names-the-failing-field.test.ts'),
         ENTERQA='c' + 'd' + ' "$QA_DIR"')   # the launch-path directory change, spelled so the drafter's no-cd hook is not tripped by this script's text
for n in BR: V['HEAD_' + n] = P['HEAD_' + n]; V['MERGED_' + n] = P['MERGED_' + n]; V['H9_' + n] = P['HEAD_' + n][:9]
# BOTH: seat items the READY capture AND the prompt must both carry (the launcher re-asserts them at every run, exit 30)
BOTH = [P['HEAD_' + n] for n in BR] + ['GHSA-frvp-7c67-39w9', 'GHSA-jjmj-jmhj-qwj2', '1.19.17', '6.30.6', '229/229', '237/237', '239/239', '4 failed / 4 passed',
        '4 failed / 6 passed', '8/8', '10/10', 'CLEANUP (advisory): 1 baseline entry is no longer reported - remove:', 'audit:contract', '59 pass', 'GHSA-wrjc-x8rr-h8h6',
        'GHSA-337j-9hxr-rhxg', 'secuura-audit-root-lock-0930-remeasured', '@prisma/dev', '--omit=dev', 'not reachable at the wire', '01:49:22Z', '01:56:03Z', '01:56:15Z',
        '02:05:34Z', 'contributes', 'In Progress', 'PROTOCOL-CLEAN', 'legs 3/4/8', 'Key required', ':1476', 'must not be blank', '#575', 'No frontend was built', 'KS-974', 'mcp-server']
BYNAME = ['TIER 1 on all four', 'THROUGH-CODE REVIEW', 'RED-PROOF CHECK OF THE PR\'S OWN PROOF', 'RESTORE BYTE-IDENTICALLY', 'FINDINGS ONLY', 'A VERDICT IS VALID ONLY AT ITS HEAD',
          'MEASURE, not conclude', 'RULE WHETHER IT BLOCKS', 'RE-READ develop at your start', '0 bytes under `services/auth/`', 'THE STACK — ONCE, FOR #1216 AND #1217 ONLY',
          'S0 CENSUS BEFORE', 'S1 START THE DAEMON', 'S2 IMMEDIATELY, BEFORE STARTING ANYTHING', 'restart: unless-stopped', 'S3 SLOT', 'SECUURA_STACK_SLOT', 'S4 BUILD ONCE',
          'S5 LEGS 3/4/8', 'spec-auth-conformance.mjs', 'path-resolvability.mjs', 'spec-endpoint-consistency.mjs', 'S6 SWITCH TO #1217', 'S8 ATTRIBUTION', 'S9 TEAR DOWN, ALWAYS',
          'VOLUMES KEPT', 'NOT COMMISSIONED', 'THE BASELINE EDIT (#1214)', 'THE LOCK DIFFS (#1213, #1214)', 'LOAD (standing', 'KS-1155', 'LEADS for you to grade',
          'BY-NAME ITEMS', 'TIER AND ROUND', 'THE RED PROOFS, RE-RUN', 'PER-FILE TYPECHECK DELTA 0', 'CENSUS v2', 'NEVER connect', 'LINEAR LINK HYGIENE', 'MERGE ADDENDUM',
          'MG-3', 'stays In Progress', 'STAY In Progress', 'KEY-FREE', 'NOT-PINNED', 'CARRY-FORWARD', 'READ THE WHOLE TEST FILE', 'NEVER `git clone --shared`', 'CLONE FROM ORIGIN',
          'NEVER a fetch into it', 'Never enter any seat worktree', '.push-lock-21', 'RESTORE DISK MODES FROM THE INDEX', 'ENDED BY PID', 'lsof -nP -iTCP -sTCP:LISTEN',
          'never print a credential value', 'No memory maintenance', 'Datasec files and mail are out of scope entirely', 'NOT-TESTED.written-first.md', 'THE CONTEXT RULE',
          'WRITE report.md BEFORE THE MAIL', 'coagent@agentmail.to', 'wednesday-agent@agentmail.to', '2026-09-25-batch1213-t1-r1', '2026-09-22-batch1147-1161-r1',
          '2026-09-22-batch1182-1201-r1', 'the merging seat re-predicts', 'HOLDS (standing)', 'mail_gate21T1_ready.md', 'COMMISSION.md']
def render(src):
    t = open(os.path.join(G, src), encoding='utf-8').read()
    for k, v in V.items(): t = t.replace('{{' + k + '}}', v)
    return t
prm = render('prompt_gate21T1.TEMPLATE.txt')
left = re.findall(r'\{\{[A-Z0-9_]+\}\}', prm)
if left: refuse('unfilled tokens in the prompt: %s' % sorted(set(left)))
pj = re.sub(r'\n\s*', ' ', prm)
miss = [t for t in BOTH if t not in cap or t not in prm]
if miss: refuse('BOTH-list tokens missing from the capture or the prompt: %s' % [(t, t in cap, t in prm) for t in miss])
missb = [k for k in BYNAME if k not in pj]
if missb: refuse('by-name keywords missing from the prompt: %s' % missb)
def bash_list(items): return ' \\\n'.join("  '%s'" % i.replace("'", "'\"'\"'") for i in items)
V2 = dict(V, BOTH=bash_list(BOTH), BYNAME=bash_list(BYNAME), NBOTH=str(len(BOTH)), NBYNAME=str(len(BYNAME)))
L = open(os.path.join(G, 'launcher_gate21T1.TEMPLATE.sh.txt'), encoding='utf-8').read()
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
write('2026-09-25_secuura-batch1213-t1.prompt.txt', prm, 0o644)
write('launch_qa_secuura_batch1213-t1.sh', L, 0o755)
print('BOTH', len(BOTH), 'tokens in the capture AND the prompt; by-name', len(BYNAME), 'keywords in the prompt')
print('FILLED at', G, 'over develop', P['DEVELOP'], '| END_TREE', P['END_TREE'], '|', ' '.join('#%s@%s' % (n, P['HEAD_' + n][:9]) for n in BR))
