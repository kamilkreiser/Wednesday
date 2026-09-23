#!/usr/bin/env python3
"""fill_r2.py — render the #1210 round-2 prompt and launcher from prompt_r2.TEMPLATE.txt / launcher_r2.TEMPLATE.sh.txt using pins_r2.txt (written by
predict_r2.py) and devlog_r2.txt. REFUSES (rc 8) unless: pins FAIL=0; a fresh `ls-remote` (read-only, the Secuura checkout) of develop, the branch and
refs/pull/1210/head agrees with the pins; the capture names the head; no {{KEY}} token is left. An existing output is kept beside as .pre-<HHMMSS>
(never deleted). Writes only into this directory."""
import os, re, subprocess, sys, datetime, shutil
G = os.path.dirname(os.path.abspath(__file__))
REPO = '/Volumes/DevMASTER/!CODING/Secuura/Blockchain/2_Project_Files'
BR = 'refs/heads/feature/ks-1239-r-1-the-indexts347-rawauthorization-capture-is-dead-code-0-r16b-rawauthdead-1'
now = datetime.datetime.now(datetime.timezone.utc)
P = dict(l.rstrip('\n').split('=', 1) for l in open(os.path.join(G, 'pins_r2.txt')) if '=' in l)
def refuse(m): print('REFUSING:', m); sys.exit(8)
if P.get('FAIL') != '0': refuse('pins_r2.txt FAIL=%s — predict_r2.py did not pass' % P.get('FAIL'))
lsr = subprocess.run(['git', '-C', REPO, 'ls-remote', 'origin', 'refs/heads/develop', BR, 'refs/pull/1210/head'], capture_output=True, text=True)
LS = dict(l.split('\t')[::-1] for l in lsr.stdout.splitlines()); print('ls-remote rc', lsr.returncode, 'at', now.strftime('%H:%M:%SZ'), LS)
if lsr.returncode != 0: refuse('ls-remote failed: ' + lsr.stderr)
if LS.get('refs/heads/develop') != P['DEVELOP']: refuse('develop moved since predict (%s -> %s) — re-run predict_r2.py' % (P['DEVELOP'], LS.get('refs/heads/develop')))
if not (LS.get(BR) == LS.get('refs/pull/1210/head') == P['HEAD']): refuse('the head moved since predict (pin %s, branch %s, pull %s)' % (P['HEAD'], LS.get(BR), LS.get('refs/pull/1210/head')))
if P['HEAD'] not in open(os.path.join(G, 'mail_r2_ready.md'), encoding='utf-8').read(): refuse('the capture mail_r2_ready.md does not name the head %s — a READY for a NEW head has not been captured (run capture_mail_r2.py)' % P['HEAD'])
devlog = '\n'.join('  ' + l for l in open(os.path.join(G, 'devlog_r2.txt')).read().strip().splitlines())
V = dict(HEAD=P['HEAD'], DEVELOP=P['DEVELOP'], DEVELOP_TREE=P['DEVELOP_TREE'], BEHIND=P['BEHIND'], MERGED_TREE=P['MERGED_TREE'], DEVLOG=devlog,
         BLOB_INDEX=P['BLOB_INDEX'], BLOB_TEST=P['BLOB_TEST'], BLOB_SHARED=P['BLOB_SHARED'], MEASURED_AT=P['MEASURED_AT'],
         GENERATED_AT=now.strftime('%Y-%m-%dT%H:%M:%SZ'),
         SEAT_MERGED_NOTE=('EQUAL to the drafter\'s' if P['SEAT_MERGED_EQUAL'] == 'True' else 'DIFFERENT from the drafter\'s (develop moved since the READY; the seat\'s tree was over dd8f99cc75b9b753172a40379eaab2b6c1026180)'))
def render(src, dst, mode):
    t = open(os.path.join(G, src), encoding='utf-8').read()
    for k, v in V.items(): t = t.replace('{{' + k + '}}', v)
    left = re.findall(r'\{\{[A-Z_]+\}\}', t)
    if left: refuse('unfilled tokens in %s: %s' % (dst, sorted(set(left))))
    out = os.path.join(G, dst)
    if os.path.exists(out): shutil.copy2(out, out + '.pre-' + now.strftime('%H%M%S'))
    open(out, 'w', encoding='utf-8').write(t); os.chmod(out, mode)
    print('wrote', out, len(t.encode()), 'B', t.count('\n'), 'lines')
render('prompt_r2.TEMPLATE.txt', '2026-09-23_secuura-1210-t1r2.prompt.txt', 0o644)
render('launcher_r2.TEMPLATE.sh.txt', 'launch_qa_secuura_1210-t1r2.sh', 0o755)
print('FILLED over develop', P['DEVELOP'], 'head', P['HEAD'], 'merged tree', P['MERGED_TREE'])
