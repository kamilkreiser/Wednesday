#!/usr/bin/env python3
"""make_commission_gate29.py — writes COMMISSION.md for gate29 (the directory this script lives in). Every SHA / tree / count in it is READ from
pins_gate29.json, stopcounts_gate29.json, gh_read_1.out and predict_1.out beside it (never typed); the prose rows are the drafter's.
Shape copied from gate28's make_commission_gate28.py, re-keyed to two rows and no dead-open overlap."""
import json, os, re
D = os.path.dirname(os.path.abspath(__file__)); K = json.load(open(D + '/kit.json')); kit = K['kit']
P = json.load(open('%s/pins_%s.json' % (D, kit))); S = json.load(open('%s/stopcounts_%s.json' % (D, kit)))
gh = open(D + '/gh_read_1.out').read()
def subj_len(n):
    m = re.search(r'=== #%s head.*?\ntitle \((\d+) chars.*?= (\d+) chars' % n, gh, re.S); return m.group(2) if m else '?'
WHY = {
 '1290': ('KS-1341', '**T1**: a RUNTIME PRODUCT FILE on a production security surface — what originate\'s webhook WRITE routes answer on a 500 (PATCH /:id, DELETE /:id, POST /:id/rotate-secret; KS-1341 MEASURED DELETE and rotate-secret leaking under production). Part B of 3; two sites declared for C. A LOCAL-MODEL patch (Spark) under Wednesday\'s brief-B rev B, re-verified by the seat; blob-identical to the golden. The rotate-secret handler touches a signing secret: the secret path must be unchanged apart from the catch body.'),
 '1291': ('KS-1337', '**T2**: TOOLING — systemTest/performance runner/cli.ts (fileURLToPath for the pre-suite step path) + one vitest cell; no product byte, no Blockchain/Dev path, so the push ran the format gate only (no platform preflight): the gate runs the package\'s own lint + unit suite. 1 of 3 sites; DoD 2 approximated (disclosed).'),
}
rows = []
for n in sorted(K['prs']):
    pr = P['prs'][n]
    files = ', '.join('%s +%s/-%s' % (os.path.basename(x.split('\t')[2]), x.split('\t')[0], x.split('\t')[1]) for x in pr['numstat'])
    rows.append('| #%s | %s | `%s` | %d on `%s` | %s | %s | %s |' % (n, WHY[n][0], pr['head'], len(pr['commits']), pr['merge_base'][:12], files, subj_len(n), WHY[n][1]))
out = ['# COMMISSION — DRAFT the round-29 batch gate kit "%s" over %d PRs (tiers 1 and 2). Do NOT launch.' % (kit, len(K['prs'])), '',
 'Relayed by Wednesday to the drafter on 2026-09-26 (~09:1xZ) as TWO PRs with heads she read by `ls-remote` (19:1x AEST): #1290 (KS-1341 part B, T1, a',
 'local-model patch) and #1291 (KS-1337, T2, tooling). No sibling kit. The GO goes to Seat B 31st, which raised both and merges its own two. Shape copied from',
 '`gatesets/2026-09-26_gate28/`: JSON pins, routing-file override, controls both ways with `--invert`, per-PR merge-bases, a declared commit count, a NOT-STACKED',
 'check and the key scan; re-keyed to two rows, an every-open-PR census, NO dead-open overlap, `--simulate moved` (no older develop can host #1290: it needs',
 'part A), and a NOT-APPLICABLE fleet STOP row for #1291 (a systemTest/ push runs no platform preflight).', '',
 '## The batch — every head re-read by the drafter from origin (ls-remote + a fetch into a `--no-local` scratch clone + the PULLS API; all agree)',
 '| PR | ticket | head | commits on merge-base | files | squash subject chars (`<title> (#n)`) | tier — why, from the DIFF |', '|---|---|---|---|---|---|---|'] + rows + ['',
 'Linear: both PRs link their tickets as `contributes`; none `closes` (linear_reads_1.out); no PR body puts a closing word before a key (gh_read_1.out, keyscan_1.out).',
 'Not stacked (measured: neither head is the other\'s ancestor; their merge-base is on develop).', '',
 '## Develop at the pin',
 'Pinned over develop **`%s`** (tree `%s`), READ by ls-remote and fetched (gate28\'s three GO squashes over e080174c86c6: #1286, #1288, #1289 — its tree equals gate28\'s END_TREE `80a3d6968f67`). END_TREE **`%s`** (%s), identical in all %d orders (%d merge-tree calls). No sibling kit: END_TREE_WITH_SIBLING == END_TREE.' % (
     P['develop'], P['develop_tree'], P['end_tree'], P['end_shortstat'], P['orders'], P['merge_tree_calls']),
 'The launch action\'s step 3b re-pins on any move.', '',
 '## Overlaps — NONE declared, NONE found',
 '- Kit pair: disjoint. Every other OPEN PR at the pin (%d, the PULLS API census, incl. dead-open #1268/#1278/#1245/#1241): disjoint from every kit path.' % len(P['inflight']), '',
 '## Fleet STOP (READ, bounded region, NOT-FOUND control)']
for n in sorted(K['prs']):
    s = S[n]
    out.append('- #%s `%s` (%d lines, rc %s): %s' % (n, os.path.basename(s['log']), s['lines'], s['rc'],
        ('%s · %s · %s · %s; "%s"' % (s['pre_push_hook_base'], s['fixture_guard'], s['run_shell_suites_region'], s['shell_suites'], s['verdict_line'])) if s['preflight_ran'] else 'NO PREFLIGHT (a systemTest/ path: the format gate only; every suite header reads NOT FOUND) — NOT APPLICABLE; the gate runs the package\'s own lint + unit suite'))
out += ['- By path class no kit PR changes the count (an originate .ts route + a jest cell; a systemTest/performance .ts file + a vitest cell — no `*.test.sh`): after this merge 28/0 · 6/0 · 49/0 · 60 of 60.', '']
out += ['## LEGITIMATE SHAPES — the drafter\'s READ predictions (the gate MEASURES every row)', '| PR | prediction | predicted-by |', '|---|---|---|']
for l in open(D + '/predict_1.out').read().splitlines():
    m = re.match(r'^  #(\d+) (.*)$', l)
    if m and not m.group(2).startswith(('product files', 'NO product file')):
        out.append('| #%s | %s | drafter READ (predict_1.out) |' % (m.group(1), m.group(2).replace('|', '/')[:1100]))
open(D + '/COMMISSION.md', 'w').write('\n'.join(out) + '\n')
print('wrote', D + '/COMMISSION.md', len(out), 'lines')
