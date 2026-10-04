#!/usr/bin/env python3
"""make_sim_gate55.py — builds the gate55 EXERCISE fixtures (SIM: never launched, never evidence) into THIS sim/ directory only.
PR number 9001 is fictional (the real PR is not raised). Every sha and numstat is READ from the shared checkout with READ-ONLY verbs
(git log / diff --numstat), never typed. Arms:
  ok/          PULLS answers for SIM #9001 at the drafted head 16784d620080, body = SIM_body_ok.md     + lsremote_ok.txt
  moved/       the same PR at B 58th's PRE-DOC head 2971e504efce (3 paths)                             + lsremote_moved.txt
  badbody/     the drafted head, a body with a hyphenated foreign key, a closing keyword and no Refs line
  census_*/    open-PR lists for gh_census_gate55.py (clean / co-tenant over-reach / a second KS-1015 PR / client human)
Usage: make_sim_gate55.py   (rc 0)"""
import json, os, subprocess, sys
D = os.path.dirname(os.path.abspath(__file__)); sys.path.insert(0, os.path.dirname(D))
from lib_gate55 import K, git
R = K['checkout']; HEAD = K['expected_head']; DEV = K['base']; PRE = '2971e504efce3c9a695f8a0a47cab5f3fabfd043'; PR = '9001'
BODY = open(os.path.join(D, 'SIM_body_ok.md'), encoding='utf-8').read()
TITLE = 'KS-1015: the delegation GET spec declares the envelope its handler returns'
def files(a, b):
    return [{'filename': l.split('\t')[2], 'additions': int(l.split('\t')[0]), 'deletions': int(l.split('\t')[1])} for l in git(R, 'diff', '--numstat', a, b).splitlines() if l]
def pr(head, body, title=TITLE, n=PR, branch=K['branch_planned'], state='open'):
    return {'number': int(n), 'state': state, 'merged': False, 'mergeable': True, 'mergeable_state': 'clean', 'title': title, 'body': body,
            'user': {'login': 'kksecura'}, 'created_at': 'SIM', 'head': {'sha': head, 'ref': branch}, 'base': {'ref': 'develop', 'sha': DEV}}
def put(sub, name, obj):
    os.makedirs(os.path.join(D, sub), exist_ok=True); json.dump(obj, open(os.path.join(D, sub, name), 'w'), indent=1)
def ls(name, head):
    open(os.path.join(D, name), 'w').write('%s\trefs/heads/develop\n%s\trefs/pull/%s/head\n%s\trefs/heads/%s\n' % (DEV, head, PR, head, K['branch_planned']))
put('ok', 'pr_%s.json' % PR, pr(HEAD, BODY)); put('ok', 'files_%s.json' % PR, files(DEV, HEAD)); ls('lsremote_ok.txt', HEAD)
put('moved', 'pr_%s.json' % PR, pr(PRE, BODY)); put('moved', 'files_%s.json' % PR, files(DEV, PRE)); ls('lsremote_moved.txt', PRE)
# live1375/: the SIM PULLS answer re-numbered #1375 (refs/pull/1375/head == 16784d620080 by the drafter's ls-remote 2026-10-04T15:54:29Z), so
# c1's P1 can be exercised against REAL origin refs while the API half stays a replay (the drafter does not read the Secuura .env)
put('live1375', 'pr_1375.json', pr(HEAD, BODY, n='1375')); put('live1375', 'files_1375.json', files(DEV, HEAD))
bad = BODY.replace('Refs KS-1015', 'Closes KS-1015').replace('PR A (#1374, KS 1402)', 'PR A (#1374, KS-1402)')
put('badbody', 'pr_%s.json' % PR, pr(HEAD, bad)); put('badbody', 'files_%s.json' % PR, files(DEV, HEAD))
# census fixtures: the PR under gate is SIM #9001; others are fictional numbers 9101.. carrying REAL file lists where they model a real lane
d3 = '9884b5588d7ca1061ea424a1782f385da1c36a49'
def opr(n, title, head, ref, user='kksecura'):
    return {'number': int(n), 'title': title, 'head': {'sha': head, 'ref': ref}, 'base': {'ref': 'develop'}, 'user': {'login': user}}
d4files = files(K['base_parent'], d3)   # Seat D 3rd's pushed KS-1404 lane: timestamping + root lock + baseline + the two docs
d4docs = [f for f in d4files if f['filename'].startswith('Projects Documents/') or f['filename'].startswith('Blockchain/Dev/services/timestamping/')]
hum = [{'filename': 'Blockchain/Dev/frontend/README.md', 'additions': 1, 'deletions': 0}]
base_pulls = [opr(PR, TITLE, HEAD, K['branch_planned']), opr('1360', 'client change (SIM stand-in for #1360)', '1' * 40, 'peter/x', 'PeterObeden')]
put('census_clean', 'pulls.json', base_pulls + [opr('9101', 'KS-1404: real RFC 3161 verification (SIM)', d3, 'feature/ks-1404-rfc3161-real-verification-d4-1')])
put('census_clean', 'files_9101.json', d4docs); put('census_clean', 'files_1360.json', hum)
put('census_clean', 'pr_%s.json' % PR, pr(HEAD, BODY))
put('census_overreach', 'pulls.json', base_pulls + [opr('9101', 'KS-1404: real RFC 3161 verification (SIM)', d3, 'feature/ks-1404-rfc3161-real-verification-d4-1')])
put('census_overreach', 'files_9101.json', d4docs + [{'filename': K['openapi_ts'], 'additions': 1, 'deletions': 0}]); put('census_overreach', 'files_1360.json', hum)
put('census_overreach', 'pr_%s.json' % PR, pr(HEAD, BODY))
put('census_second1015', 'pulls.json', base_pulls + [opr('9102', 'KS-1015: another pair (SIM)', '2' * 40, 'feature/ks-1015-other-b99-1')])
put('census_second1015', 'files_9102.json', [{'filename': 'Blockchain/Dev/services/auth/src/x.ts', 'additions': 1, 'deletions': 0}]); put('census_second1015', 'files_1360.json', hum)
put('census_second1015', 'pr_%s.json' % PR, pr(HEAD, BODY))
# census_1375/: the dry-run replay for the REAL PR number (the API half SIM, the ls-remote half real); compare_ok.txt: the SIM launcher's
# compare line, built from the real numstat (the drafter does not call the compare endpoint)
c13 = [opr('1375', TITLE, HEAD, K['branch_planned']), base_pulls[1], opr('9101', 'KS-1404: real RFC 3161 verification (SIM)', d3, 'feature/ks-1404-rfc3161-real-verification-d4-1')]
put('census_1375', 'pulls.json', c13); put('census_1375', 'files_9101.json', d4docs); put('census_1375', 'files_1360.json', hum)
put('census_1375', 'pr_1375.json', pr(HEAD, BODY, n='1375'))
open(os.path.join(D, 'compare_ok.txt'), 'w').write('%s ahead=1 behind=0 files=%d paths=%s\n' % (DEV, len(K['files']), ','.join(sorted(f['filename'] for f in files(DEV, HEAD)))))
print('SIM fixtures written under %s (PR %s fictional; head %s / pre-doc %s; develop %s)' % (D, PR, HEAD[:12], PRE[:12], DEV[:12]))
