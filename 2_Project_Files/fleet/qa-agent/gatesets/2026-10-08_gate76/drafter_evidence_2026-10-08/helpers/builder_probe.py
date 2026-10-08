#!/usr/bin/env python3
"""builder_probe.py — the OWED gate75 item: run the inherited R-lane builder (Seat R 17th's build_addendumra17_gate75.py, a byte copy READ out
of R 17th's record folder into the drafter's scratchpad; sha256/16 asserted) against each gate76 head's REAL shape, trailers included, in
the drafter's scratch clone. SYNTHETIC GO / ADDENDUM text (never mailed), the staged squash bodies, the real handovers. The GO clause keeps
`Seat R 17th` because the builder hard-codes that ordinal in its regex: the probe measures the SHAPE, and the ordinal re-key is a named
item. Usage: builder_probe.py <kit dir> <clone> <scratch dir> <M sha>"""
import hashlib, json, os, subprocess, sys

KD, CL, SC, M = sys.argv[1:5]
K = json.load(open(os.path.join(KD, 'kit.json'), encoding='utf-8')); MI = json.load(open(os.path.join(KD, 'merge_inputs', 'MERGE_INPUTS.json'), encoding='utf-8'))
B = os.path.join(SC, 'builder', 'build_addendumra17_gate75.py')
assert hashlib.sha256(open(B, 'rb').read()).hexdigest()[:16] == '04ed62b4ff18b3d3', 'the builder copy is not R 17th\'s 04ed62b4ff18b3d3'
D0 = K['develop_at_draft']; HIST = '/Volumes/DevMASTER/!CODING/Secuura/Blockchain/5_Project_History/'
C = json.load(open(os.path.join(KD, 'composed_2026-10-08', 'chain.json')))
SIM1 = C['steps'][0]['sim_commit']; T2 = C['steps'][1]['tree']; FB2, CB2 = C['steps'][1]['flow_blob'], C['steps'][1]['cheat_blob']


def go(d, head, b, end, t, flow, cheat, subj, body, note, pr, gate='gate76'):
    lines = ['GO (Seat R 17th): merge %s on %s' % (pr, gate), 'qm Q2 STRICT / qm green: as declared', '- develop D: ' + d, '- PR head: ' + head, '- PR base B: ' + b,
             '- END_TREE: ' + end, "- Target tree T': " + t]
    if flow: lines += ['flow `%s` = %s' % (K['docs']['flow'], flow), 'cheat `%s` = %s' % (K['docs']['cheat'], cheat)]
    raw = open(body, 'rb').read()
    lines += ['Declared squash subject: `%s`' % subj, '%d chars, LANDS %d' % (len(subj), len(subj)),
              'body: %d bytes, sha256 %s' % (len(raw), hashlib.sha256(raw).hexdigest()), 'merge_note: `%s`' % note]
    return '\n'.join(lines) + '\n'


def run(name, env_over, gotext):
    d = os.path.join(SC, 'builder', name); os.makedirs(d, exist_ok=True)
    open(os.path.join(d, 'GO.txt'), 'w').write(gotext); open(os.path.join(d, 'ADD.txt'), 'w').write('ACTIONS VERDICT (Wednesday): 0 new failures\n')
    env = dict(os.environ); env.pop('GIT_SSH_COMMAND', None)
    env.update({'RA17_REC': d, 'RA17_WT': CL, 'RA17_SEAT': 'Seat R 17th', 'RA17_GO': os.path.join(d, 'GO.txt'), 'RA17_ADDENDUM': os.path.join(d, 'ADD.txt'),
                'RA17_GATE': 'gate76', 'RA17_HIST_ROOT': HIST, 'RA17_HEAD_TRAILER': 'refuse'})
    env.update(env_over)
    p = subprocess.run([sys.executable, '-I', B], capture_output=True, text=True, env=env)
    tail = (p.stdout + p.stderr).strip().split('\n')
    last = [l for l in tail if 'AssertionError' in l or 'REFUSED' in l or 'addendum written' in l]
    msg = (tail[-1] if p.returncode else (last[0] if last else tail[-1]))[:300]
    print('%-44s rc %d | %s' % (name, p.returncode, msg))
    return p.returncode, msg


def hsum(f):
    raw = open(os.path.join(HIST, f), 'rb').read(); return hashlib.sha256(raw).hexdigest()[:16]


R7, R8 = K['rows']['1427'], K['rows']['1428']
b7, b8 = MI['1427']['file'], MI['1428']['file']
w7, w8 = 'HANDOVER-seatR18-2026-10-08.md', 'HANDOVER-seatG4-2026-10-08.md'
n7 = 'Merged by Seat R 17th on the authority of %s sha256 %s' % (w7, hsum(w7)); n8 = 'Merged by Seat R 17th on the authority of %s sha256 %s' % (w8, hsum(w8))
common8 = {'RA17_PR': '1428', 'RA17_OWN_KEYS': 'KS-593', 'RA17_EXPECT_PATHS': '9', 'RA17_MODE_CENSUS': json.dumps({'100644': 9}), 'RA17_WRAP': w8,
           'RA17_WRAP_DIGEST': hsum(w8), 'RA17_BODY': b8, 'RA17_BODY_DIGEST': MI['1428']['sha256'][:16], 'RA17_GO_CLAUSE': 'GO (Seat R 17th): merge 1428 on gate76'}
common7 = {'RA17_PR': '1427', 'RA17_OWN_KEYS': 'KS-1274', 'RA17_WRAP': w7, 'RA17_WRAP_DIGEST': hsum(w7), 'RA17_BODY': b7,
           'RA17_BODY_DIGEST': MI['1427']['sha256'][:16], 'RA17_GO_CLAUSE': 'GO (Seat R 17th): merge 1427 on gate76'}
res = {}
# P1 #1428 FIRST: on-develop, docs = the head blobs
res['P1_1428_first_on_develop_docs_head'] = run('P1_1428_first', dict(common8, RA17_NO_MERGE_IN='1', RA17_LANDING='on-develop', RA17_DOCS='head'),
    go(D0, R8['head_expected'], D0, R8['end_tree'], R8['end_tree'], R8['flow_blob_head'], R8['cheat_blob_head'], MI['1428']['subject'], b8, n8, '1428'))
# P2 #1427 SECOND, merge-in, the GO's PR head = M (the commit that is squashed)
res['P2_1427_second_mergein_head_is_M'] = run('P2_1427_second_M', dict(common7, RA17_NO_MERGE_IN='0', RA17_LANDING='merge-in', RA17_DOCS='merged', RA17_EXPECT_PATHS='6',
    RA17_MODE_CENSUS=json.dumps({'100644': 5, '100755': 1})), go(SIM1, M, D0, R7['end_tree'], T2, FB2, CB2, MI['1427']['subject'], b7, n7, '1427'))
# P3 #1427 SECOND, merge-in, the GO's PR head = the GATED head (parents [D0])
res['P3_1427_second_mergein_head_is_gated'] = run('P3_1427_second_H', dict(common7, RA17_NO_MERGE_IN='0', RA17_LANDING='merge-in', RA17_DOCS='merged', RA17_EXPECT_PATHS='6',
    RA17_MODE_CENSUS=json.dumps({'100644': 5, '100755': 1})), go(SIM1, R7['head_expected'], D0, R7['end_tree'], T2, FB2, CB2, MI['1427']['subject'], b7, n7, '1427'))
# P4 #1427 FIRST (the reverse order), on-develop, docs head: the shape fits
res['P4_1427_first_on_develop_docs_head'] = run('P4_1427_first', dict(common7, RA17_NO_MERGE_IN='1', RA17_LANDING='on-develop', RA17_DOCS='head', RA17_EXPECT_PATHS='6',
    RA17_MODE_CENSUS=json.dumps({'100644': 5, '100755': 1})),
    go(D0, R7['head_expected'], D0, R7['end_tree'], R7['end_tree'], R7['flow_blob_head'], R7['cheat_blob_head'], MI['1427']['subject'], b7, n7, '1427'))
# P5 #1427 with the PR TITLE as the subject (`KS 1274: …`, de-hyphenated): REFUSED by the subject-opens-with-own-keys assert
res['P5_1427_title_as_subject'] = run('P5_1427_title', dict(common7, RA17_NO_MERGE_IN='1', RA17_LANDING='on-develop', RA17_DOCS='head', RA17_EXPECT_PATHS='6',
    RA17_MODE_CENSUS=json.dumps({'100644': 5, '100755': 1})),
    go(D0, R7['head_expected'], D0, R7['end_tree'], R7['end_tree'], R7['flow_blob_head'], R7['cheat_blob_head'], R7['pr_title'], b7, n7, '1427'))
# P6 #1428 with the commit-message residue planted into the body: REFUSED by the builder's CLOSING regex
pb = os.path.join(SC, 'builder', '1428.body.residue.txt'); open(pb, 'w', encoding='utf-8').write(open(b8, encoding='utf-8').read() + '\nNARROWING: this does not close KS-593.\n')
rawp = open(pb, 'rb').read()
res['P6_1428_residue_planted_in_body'] = run('P6_1428_residue', dict(common8, RA17_NO_MERGE_IN='1', RA17_LANDING='on-develop', RA17_DOCS='head', RA17_BODY=pb,
    RA17_BODY_DIGEST=hashlib.sha256(rawp).hexdigest()[:16]),
    go(D0, R8['head_expected'], D0, R8['end_tree'], R8['end_tree'], R8['flow_blob_head'], R8['cheat_blob_head'], MI['1428']['subject'], pb, n8, '1428'))
# P7 the GO clause naming the NEXT seat (the real merge seat will not be R 17th): REFUSED by the hard-coded ordinal
res['P7_go_clause_other_ordinal'] = run('P7_ordinal', dict(common8, RA17_NO_MERGE_IN='1', RA17_LANDING='on-develop', RA17_DOCS='head', RA17_GO_CLAUSE='GO (Seat R 20th): merge 1428 on gate76'),
    go(D0, R8['head_expected'], D0, R8['end_tree'], R8['end_tree'], R8['flow_blob_head'], R8['cheat_blob_head'], MI['1428']['subject'], b8, n8, '1428').replace('Seat R 17th): merge', 'Seat R 20th): merge'))
json.dump(res, open(os.path.join(SC, 'builder', 'probe_result.json'), 'w'), indent=1)
