#!/usr/bin/env python3
"""fill_gate21T2b.py <scratchpad> — render the round-21 SECOND tier-2 batch gate's prompt and launcher from prompt_gate21T2b.TEMPLATE.txt /
launcher_gate21T2b.TEMPLATE.sh.txt using pins_gate21T2b.txt + devlog_gate21T2b.txt (written by predict_gate21T2b.py). The kit is SELF-LOCATING: every
path is this script's own directory at fill time (GS), so the kit can be copied to its gatesets/ home and re-filled there. REFUSES (rc 8) unless: pins
FAIL=0; a fresh `ls-remote` (read-only, the Secuura checkout) of develop + the five refs/pull/N/head + the five branches agrees with the pins; the
capture names every head; the BOTH list is in the capture AND the prompt; the by-name ladder is in the prompt; no fill token is left; `bash -n` of the
launcher (a copy under <scratchpad>) is rc 0. An existing output is kept beside as .pre-<HHMMSS> (never deleted). Writes only into this directory
(and one temp copy under <scratchpad>). Derived from gate21T2's fill_gate21T2.py, re-keyed to five rows."""
import os, re, subprocess, sys, datetime, shutil, hashlib, tempfile, json
G = os.path.dirname(os.path.abspath(__file__))
SP = sys.argv[1] if len(sys.argv) > 1 else ''
if not (re.match(r'^/private/tmp/claude-501/.*/scratchpad', os.path.realpath(SP)) and os.path.isdir(SP)): print('REFUSING: argv[1] must be a scratchpad dir under /private/tmp/claude-501/'); sys.exit(9)
REPO = '/Volumes/DevMASTER/!CODING/Secuura/Blockchain/2_Project_Files'
BR = {'1225': 'refs/heads/feature/ks-1291-dead-post-save-issuername-guard-l1-j-1',
      '1227': 'refs/heads/feature/ks-1252-spec-example-guard-e7-ulid-ish-prefix-l4-e7prefix-1',
      '1229': 'refs/heads/feature/ks-865-check-no-latest-tags-silently-skips-l4-examinedcount-1',
      '1231': 'refs/heads/feature/ks-1281-vc-issuer-boot-warns-could-not-ensure-vc_credentials_store-r21-existencecheck-1',
      '1232': 'refs/heads/feature/ks-1128-the-platform-tenant-seeds-catch-logs-platform-tenant-seed-r21-seedwarn-1'}
now = datetime.datetime.now(datetime.timezone.utc)
def refuse(m): print('REFUSING:', m); sys.exit(8)
P = dict(l.rstrip('\n').split('=', 1) for l in open(os.path.join(G, 'pins_gate21T2b.txt')) if '=' in l)
if P.get('FAIL') != '0': refuse('pins_gate21T2b.txt FAIL=%s — predict_gate21T2b.py did not pass' % P.get('FAIL'))
lsr = subprocess.run(['git', '-C', REPO, 'ls-remote', 'origin', 'refs/heads/develop'] + ['refs/pull/%s/head' % n for n in BR] + list(BR.values()), capture_output=True, text=True)
LS = dict(l.split('\t')[::-1] for l in lsr.stdout.splitlines()); print('ls-remote rc', lsr.returncode, 'at', now.strftime('%H:%M:%SZ'), len(LS), 'refs')
if lsr.returncode != 0: refuse('ls-remote failed: ' + lsr.stderr)
if LS.get('refs/heads/develop') != P['DEVELOP']: refuse('develop moved since predict (%s -> %s) — re-run predict_gate21T2b.py' % (P['DEVELOP'], LS.get('refs/heads/develop')))
for n, br in BR.items():
    if not (LS.get(br) == LS.get('refs/pull/%s/head' % n) == P['HEAD_' + n]): refuse('#%s head moved since predict (pin %s, branch %s, pull %s) — a new head needs a new READY, a re-capture and a re-predict' % (n, P['HEAD_' + n], LS.get(br), LS.get('refs/pull/%s/head' % n)))
cap = open(os.path.join(G, 'mail_gate21T2b_ready.md'), encoding='utf-8').read()
for n in BR:
    if P['HEAD_' + n] not in cap: refuse('the capture mail_gate21T2b_ready.md does not name #%s head %s — capture the READY for that head first (capture_mail_gate21T2b.py)' % (n, P['HEAD_' + n]))
D = 'Blockchain/Dev/'
def blob(path): return P['BLOB|' + D + path].split()[0]
def mode(path): return P['BLOB|' + D + path].split()[1]
devlog = open(os.path.join(G, 'devlog_gate21T2b.txt')).read().strip()
devlog = '\n'.join('  ' + l for l in devlog.splitlines()) if devlog else '  (none: develop == BASE — every PR merges fast-forward-shaped, merged tree == head tree)'
ROWS = {'1225': ['services/originate/src/routes/documents.ts'],
        '1227': ['scripts/spec-examples/check/contract.mjs', 'scripts/__tests__/ks1252_1253_e7_prefix_guard.test.sh'],
        '1229': ['scripts/check-no-latest-tags.sh', 'scripts/run-migrations.sh', 'scripts/__tests__/check_no_latest_tags.test.sh'],
        '1231': ['services/vc-issuer/src/repositories/credentialRepo.ts', 'services/vc-issuer/src/__tests__/ks1281-vc-store-no-runtime-ddl.test.ts'],
        '1232': ['services/api-gateway/src/startup-migrations.ts', 'services/api-gateway/src/__tests__/ks1128-platform-tenant-seed-failure-warns.test.ts']}
if sorted(sum(ROWS.values(), [])) != sorted(k[len('BLOB|' + D):] for k in P if k.startswith('BLOB|')): refuse('the BLOBTABLE rows != the pinned path set')
BLOBTABLE = '\n'.join('  #%s %s %s (%s; BASE %s)' % (n, D + f, blob(f), mode(f), P['BASEBLOB|' + D + f][:12]) for n, fs in ROWS.items() for f in fs)
EXPECT = {n: sorted(D + f for f in fs) for n, fs in ROWS.items()}
V = dict(GS=G, BASE=P['BASE'], BASE_TREE=P['BASE_TREE'], DEVELOP=P['DEVELOP'], DEVELOP_TREE=P['DEVELOP_TREE'], BEHIND=P['BEHIND'], MOVED_N=P['MOVED_N'], END_TREE=P['END_TREE'],
         END_SHORTSTAT=P['END_SHORTSTAT'].strip(), DEVLOG=devlog, MEASURED_AT=P['MEASURED_AT'], GENERATED_AT=now.strftime('%Y-%m-%dT%H:%M:%SZ'), BLOBTABLE=BLOBTABLE,
         BLOB_1225=blob(ROWS['1225'][0]), BLOB_1227_C=blob(ROWS['1227'][0]), BLOB_1227_T=blob(ROWS['1227'][1]),
         BLOB_1229_N=blob(ROWS['1229'][0]), BLOB_1229_R=blob(ROWS['1229'][1]), BLOB_1229_T=blob(ROWS['1229'][2]),
         BLOB_1231_P=blob(ROWS['1231'][0]), BLOB_1231_T=blob(ROWS['1231'][1]), BLOB_1232_P=blob(ROWS['1232'][0]), BLOB_1232_T=blob(ROWS['1232'][1]),
         EXPECT_JSON=json.dumps(EXPECT, sort_keys=True),
         ENTERQA='c' + 'd' + ' "$QA_DIR"')   # the launch-path directory change, spelled so the drafter's no-cd hook is not tripped by this script's text
for n in BR: V['HEAD_' + n] = P['HEAD_' + n]; V['MERGED_' + n] = P['MERGED_' + n]; V['H9_' + n] = P['HEAD_' + n][:9]
# BOTH: seat items the READY capture AND the prompt must both carry (the launcher re-asserts them at every run, exit 30)
BOTH = [P['HEAD_' + n] for n in BR] + ['74 / 863', '46 files / 918', '1 failed / 862', '863/863', ':616', 'E-01', 'PROTOCOL-DIFF #3',
        '6 passed, 2 failed', '7 passed, 1 failed', '8 passed, 0 failed', '58 passed, 0 failed (of 58)', '1,242', 'len12', 'credit_<v4>', '0/14',
        'check-spec-examples.mjs', '3 passed, 4 failed', '7 passed, 0 failed', 'deploy-staging.yml', 'b2c70381a', 'KS-1031', 'BACKLOG.md', '3.2.57',
        'bare 127/127 over 12 files', 'patched 129/129 over 13', 'red-first 1-of-2', 'provisionAppRole', 'bare 750/750 over 81', 'patched 754/754 over 82',
        'red-first 2-of-4', '918/918 -> 918/918', '828/828 -> 828/828', '57/57 -> 57/57', 'in-process fake pg', ':1142', 'ATTRIBUTED', '#1230']
BYNAME = ['TIER 2 on all five', 'THROUGH-CODE', "RED-PROOF CHECK OF THE PR'S OWN PROOF", 'RED AT BASE and GREEN AT HEAD', 'RESTORE BYTE-IDENTICALLY', 'FINDINGS ONLY',
          'A VERDICT IS VALID ONLY AT ITS HEAD', 'MEASURE, not conclude', 'RULE WHETHER IT BLOCKS', 'FROZEN at five', 'TIER AND ROUND', 'RE-READ develop at your start',
          'BASE-INVARIANT', 'THE RED PROOFS — RE-RUN', 'THE REMOVAL PROOF', 'LEGITIMATE SHAPES', 'LEGS 3/4/8 — NOT RUN', 'THE STACK IS NOT YOURS TO START',
          'IF THE STACK IS UP', 'OTHERWISE', 'SAY WHOSE ORIGINATE ANSWERED', 'REACH (measure, then grade)', 'THE SUBSTRATE (#1231', 'UNMEASURED', 'FAKE PG ONLY',
          'THE NARROWING (#1227)', 'LOAD (standing', 'KS-1155', 'LOGIN_STUB (standing', 'LEADS for you to grade', 'BY-NAME ITEMS', 'PER-FILE TYPECHECK DELTA 0',
          'CENSUS v2', 'NEVER connect', 'LINEAR LINK HYGIENE', 'MG-11', 'MG-3', 'MERGE ADDENDUM', 'STAY In Progress', 'stays In Progress', 'KEY-FREE', 'NOT-PINNED',
          'CARRY-FORWARD', 'READ THE WHOLE TEST FILE', 'NEVER `git clone --shared`', 'CLONE FROM ORIGIN', 'NEVER a fetch into it', 'Never enter any seat worktree',
          '.push-lock-21', 'RESTORE DISK MODES FROM THE INDEX', 'ENDED BY PID', 'lsof -nP -iTCP -sTCP:LISTEN', 'never print a credential value', 'No memory maintenance',
          'Datasec files and mail are out of scope entirely', 'NOT-TESTED.written-first.md', 'THE CONTEXT RULE', 'WRITE report.md BEFORE THE MAIL', 'coagent@agentmail.to',
          'wednesday-agent@agentmail.to', '2026-09-25-batch1225-t2-r1', '2026-09-25-batch1215-t2-r1', '2026-09-22-batch1170-1179-r1', '2026-09-18-ks679-922-30c773ee8-tier2-r2',
          '2026-09-06-s139-ks490-3-852-8acf0d260-tier2', '2026-09-23-batch1202-t2-r1', 'the merging seat re-predicts', 'HOLDS (standing)', 'mail_gate21T2b_ready.md',
          'COMMISSION.md', 'GIT_DIR', 'KS-1086', 'KS-318', 'ARCHIVED', 'NOT in this gate', 'Ornith', 'PASS 7/7', 'BUILD THE SCHEMA THE PRODUCT DEPLOYS',
          'run-code-guards.sh:82', 'bootstrap_login_diagnosis.test.sh', 'fd6335f08', 'd37b0576-a575-411a-b642-3e82c12af835']
def render(src):
    t = open(os.path.join(G, src), encoding='utf-8').read()
    for k, v in V.items(): t = t.replace('{{' + k + '}}', v)
    return t
prm = render('prompt_gate21T2b.TEMPLATE.txt')
left = re.findall(r'\{\{[A-Z0-9_]+\}\}', prm)
if left: refuse('unfilled tokens in the prompt: %s' % sorted(set(left)))
pj = re.sub(r'\n\s*', ' ', prm)
miss = [t for t in BOTH if t not in cap or t not in prm]
if miss: refuse('BOTH-list tokens missing from the capture or the prompt: %s' % [(t, t in cap, t in prm) for t in miss])
missb = [k for k in BYNAME if k not in pj]
if missb: refuse('by-name keywords missing from the prompt: %s' % missb)
def bash_list(items): return ' \\\n'.join("  '%s'" % i.replace("'", "'\"'\"'") for i in items)
V2 = dict(V, BOTH=bash_list(BOTH), BYNAME=bash_list(BYNAME), NBOTH=str(len(BOTH)), NBYNAME=str(len(BYNAME)))
L = open(os.path.join(G, 'launcher_gate21T2b.TEMPLATE.sh.txt'), encoding='utf-8').read()
for k, v in V2.items(): L = L.replace('{{' + k + '}}', v)
leftL = re.findall(r'\{\{[A-Z0-9_]+\}\}', L)
if leftL: refuse('unfilled tokens in the launcher: %s' % sorted(set(leftL)))
tmp = tempfile.NamedTemporaryFile('w', suffix='.sh', delete=False, dir=SP, encoding='utf-8'); tmp.write(L); tmp.close()
rc = subprocess.run(['bash', '-n', tmp.name]).returncode; print('bash -n rc', rc, 'on', tmp.name)
if rc != 0: refuse('bash -n failed on the rendered launcher')
def write(name, text, mode_):
    out = os.path.join(G, name)
    if os.path.exists(out): shutil.copy2(out, out + '.pre-' + now.strftime('%H%M%S'))
    open(out, 'w', encoding='utf-8').write(text); os.chmod(out, mode_)
    print('wrote', out, len(text.encode()), 'B', text.count('\n'), 'lines sha256', hashlib.sha256(text.encode()).hexdigest())
write('2026-09-25_secuura-batch1225-t2.prompt.txt', prm, 0o644)
write('launch_qa_secuura_batch1225-t2.sh', L, 0o755)
print('BOTH', len(BOTH), 'tokens in the capture AND the prompt; by-name', len(BYNAME), 'keywords in the prompt')
print('FILLED at', G, 'over develop', P['DEVELOP'], '| END_TREE', P['END_TREE'], '|', ' '.join('#%s@%s' % (n, P['HEAD_' + n][:9]) for n in BR))
