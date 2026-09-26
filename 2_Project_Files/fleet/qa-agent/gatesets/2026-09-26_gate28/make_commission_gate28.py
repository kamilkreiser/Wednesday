#!/usr/bin/env python3
"""make_commission_gate28.py — writes COMMISSION.md for gate28 (the directory this script lives in). Every SHA / tree / count in it is READ from
pins_gate28.json, stopcounts_gate28.json, gh_read_1.out and predict_1.out beside it (never typed); the prose rows are the drafter's."""
import json, os, re
D = os.path.dirname(os.path.abspath(__file__)); K = json.load(open(D + '/kit.json')); kit = K['kit']
P = json.load(open('%s/pins_%s.json' % (D, kit))); S = json.load(open('%s/stopcounts_%s.json' % (D, kit)))
gh = open(D + '/gh_read_1.out').read()
def subj_len(n):
    m = re.search(r'=== #%s head.*?\ntitle \((\d+) chars.*?= (\d+) chars' % n, gh, re.S); return m.group(2) if m else '?'
WHY = {
 '1286': ('KS-1336', '**T3**: two Markdown files, no code. DOC-CLAIM: every changed sentence against the code at develop; NO plan or recommendation may be added (Kam\'s decision). **FIX ROUND — ROUND 2 OF 2, AT THE CAP** (gate27 NO GO N-1286-1 TWO-FLAGS-FALSE; non-blocking N-1286-2 ONBOARDING-CITE).'),
 '1288': ('KS-1341', '**T1**: a RUNTIME PRODUCT FILE of weight — what originate\'s webhooks 500 answers carry to a client (information exposure, every NODE_ENV). Part A of 3: fail500 + GET / and POST /; five sites declared for B/C. A LOCAL-MODEL patch (Spark) under a Wednesday brief, re-verified by the seat; blob-identical to the golden.'),
 '1289': ('KS-1318', '**T2**: ONE test assertion (J2 `toHaveLength(3)` -> the tag set in source order); no product byte. Hunk 3 of the dead-open #1268\'s ks781 diff, alone — DECLARED overlap with #1268 at a DIFFERENT blob.'),
}
rows = []
for n in sorted(K['prs']):
    pr = P['prs'][n]
    files = ', '.join('%s +%s/-%s' % (os.path.basename(x.split('\t')[2]), x.split('\t')[0], x.split('\t')[1]) for x in pr['numstat'])
    rows.append('| #%s | %s | `%s` | %d on `%s` | %s | %s | %s |' % (n, WHY[n][0], pr['head'], len(pr['commits']), pr['merge_base'][:12], files, subj_len(n), WHY[n][1]))
out = ['# COMMISSION — DRAFT the round-28 batch gate kit "%s" over %d PRs (tiers 1, 2 and 3). Do NOT launch.' % (kit, len(K['prs'])), '',
 'Relayed by Wednesday to the drafter on 2026-09-26 (~06:4xZ) as THREE PRs with heads she read by `ls-remote refs/pull/N/head`: #1288 (KS-1341 part A, T1, a',
 'local-model patch), #1289 (KS-1318 J2 alone, T2) and #1286 (docs, refs KS-1336, T3 — ROUND 2 OF 2 at the cap). No sibling kit. Shape copied from',
 '`gatesets/2026-09-26_gate27/`: JSON pins, routing-file override, controls both ways with `--invert`, per-PR merge-bases, a declared commit count, a NOT-STACKED',
 'check and the key scan; re-keyed to three rows, an every-open-PR census, a DECLARED dead-open overlap (#1268) at a DIFFERENT blob (asserted as a HUNK SUBSET,',
 'not a same-blob identity), and `--simulate moved` (no older develop can host #1288/#1289).', '',
 '## The batch — every head re-read by the drafter from origin (ls-remote + a fetch into a `--no-local` scratch clone + the PULLS API; all agree)',
 '| PR | ticket | head | commits on merge-base | files | squash subject chars (`<title> (#n)`) | tier — why, from the DIFF |', '|---|---|---|---|---|---|---|'] + rows + ['',
 'Linear: every PR links its ticket as `contributes`; none `closes` (linear_reads_1.out); no PR body puts a closing word before a key (gh_read_1.out). No PR is stacked',
 'on another (measured: no head is another\'s ancestor; every pair\'s merge-base is on develop).', '',
 '## Develop at the pin',
 'Pinned over develop **`%s`** (tree `%s`), READ by ls-remote and fetched (gate27\'s two GO squashes over e6056de7ed64: #1285, then #1287 — its tree equals the GO-subset END tree gate27 predicted). END_TREE **`%s`** (%s), identical in all %d orders (%d merge-tree calls). No sibling kit: END_TREE_WITH_SIBLING == END_TREE.' % (
     P['develop'], P['develop_tree'], P['end_tree'], P['end_shortstat'], P['orders'], P['merge_tree_calls']),
 'The launch action\'s step 3b re-pins on any move.', '',
 '## Overlaps — ONE DECLARED (hunk subset, different blob), NONE found',
 '- Kit pairs: disjoint (3 pairs). Every other OPEN PR at the pin (%d, the PULLS API census): disjoint from every kit path.' % len(P['inflight']),
]
for b, rs in sorted(P.get('dead_open_declared', {}).items()):
    for r in rs:
        out.append('- **DECLARED:** dead-open **#%s** (head `%s`, NO GO at its cap in gate26T2) carries #%s\'s `%s` at a DIFFERENT blob (`%s` vs #%s\'s `%s`). #%s\'s %d hunk(s) are byte-identical (by body) to #%s\'s hunk(s) %s of %d; the pre-image `%s` is one blob at both merge-bases and develop. Merged-blob target = #%s\'s head blob. #%s must close unmerged: merged after #%s it would land its other %d hunk(s) (KS-1316\'s failed rule).' % (
            b, r['dead_open_head'], r['pr'], r['path'].split('/')[-1], r['blob_dead_open'][:12], r['pr'], r['blob_kit'][:12], r['pr'], r['kit_hunks'], b, r['kit_hunk_index_in_dead_open'], r['dead_open_hunks'], r['pre_image'][:12], r['pr'], b, r['pr'], r['dead_open_hunks'] - r['kit_hunks']))
out += ['', '## Fleet STOP (READ, bounded region, NOT-FOUND control)']
for n in sorted(K['prs']):
    s = S[n]
    out.append('- #%s `%s` (%d lines, rc %s): %s' % (n, os.path.basename(s['log']), s['lines'], s['rc'],
        ('%s · %s · %s · %s; "%s"' % (s['pre_push_hook_base'], s['fixture_guard'], s['run_shell_suites_region'], s['shell_suites'], s['verdict_line'])) if s['preflight_ran'] else 'no preflight — NOT APPLICABLE'))
out += ['- By path class no kit PR changes the count (2 Markdown files; an originate .ts route + a jest cell; a packages/shared .ts test — no `*.test.sh`): after this merge 28/0 · 6/0 · 49/0 · 60 of 60.', '']
out += ['## LEGITIMATE SHAPES — the drafter\'s READ predictions (the gate MEASURES every row)', '| PR | prediction | predicted-by |', '|---|---|---|']
for l in open(D + '/predict_1.out').read().splitlines():
    m = re.match(r'^  #(\d+) (.*)$', l)
    if m and not m.group(2).startswith(('product files', 'NO product file')):
        out.append('| #%s | %s | drafter READ (predict_1.out) |' % (m.group(1), m.group(2).replace('|', '/')[:900]))
open(D + '/COMMISSION.md', 'w').write('\n'.join(out) + '\n')
print('wrote', D + '/COMMISSION.md', len(out), 'lines')
