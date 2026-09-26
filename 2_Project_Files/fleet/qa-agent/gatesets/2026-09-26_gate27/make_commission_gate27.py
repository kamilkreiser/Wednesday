#!/usr/bin/env python3
"""make_commission_gate27.py — writes COMMISSION.md for gate27 (the directory this script lives in). Every SHA / tree / count in it is READ from
pins_gate27.json, stopcounts_gate27.json, gh_read_1.out, probe1278_1.out and probe1285_1.out beside it (never typed); the prose rows are the drafter's."""
import json, os, re
D = os.path.dirname(os.path.abspath(__file__)); K = json.load(open(D + '/kit.json')); kit = K['kit']
P = json.load(open('%s/pins_%s.json' % (D, kit))); S = json.load(open('%s/stopcounts_%s.json' % (D, kit)))
gh = open(D + '/gh_read_1.out').read()
def subj_len(n):
    m = re.search(r'=== #%s head.*?\ntitle \((\d+) chars.*?= (\d+) chars' % n, gh, re.S); return m.group(2) if m else '?'
WHY = {
 '1278': ('KS-1314', '**T2**: two systemTest/ test files (no product byte); a CHECKER (parserImportSites + the new callsReadYaml): THE READER RULE. **FIX ROUND — ROUND 2 OF 2, AT THE CAP** (gate26T2 NO GO B-1278-1 SEMICOLON-IN-BRACES, M-1278-a). The seat chose the AST.'),
 '1285': ('KS-766', '**T2**: ONE operator script (not deployed, not imported; named only in a dead workflow\'s comments). Behaviour moves (the producer is extracted) + two self-test cases; the self-test is the red proof (no docker).'),
 '1286': ('KS-1336', '**T3**: two Markdown files, no code. DOC-CLAIM: every changed sentence against the code at develop; NO plan or recommendation may be added (Kam\'s decision).'),
 '1287': ('KS-1318 + KS-1142', '**T2 follow-up**: ONE test file, byte-identical to blob 8a4ce36a (graded in #1268 rounds 1-2); run on the current develop. #1268 (dead-open) carries the same path at the same blob — DECLARED.'),
}
rows = []
for n in sorted(K['prs']):
    pr = P['prs'][n]
    files = ', '.join('%s +%s/-%s' % (os.path.basename(x.split('\t')[2]), x.split('\t')[0], x.split('\t')[1]) for x in pr['numstat'])
    rows.append('| #%s | %s | `%s` | %d on `%s` | %s | %s | %s |' % (n, WHY[n][0], pr['head'], len(pr['commits']), pr['merge_base'][:12], files, subj_len(n), WHY[n][1]))
out = ['# COMMISSION — DRAFT the round-27 batch gate kit "%s" over %d PRs (tiers 2 and 3). Do NOT launch.' % (kit, len(K['prs'])), '',
 'Relayed by Wednesday to the drafter on 2026-09-26 (~03:0xZ) as FOUR PRs with heads she read by `ls-remote refs/pull/N/head`: #1278 (KS-1314 fix round, ROUND 2 OF 2 at the',
 'cap), #1285 (KS-766), #1286 (docs, refs KS-1336) and #1287 (KS-1318 + KS-1142). No sibling kit. Shape copied from `gatesets/2026-09-26_gate26T2/` (and gate26T1): JSON pins,',
 'routing-file override, controls both ways with `--invert`, per-PR merge-bases, a declared commit count, a NOT-STACKED check and the key scan; re-keyed to four rows,',
 'an every-open-PR census, a DECLARED dead-open same-blob overlap (#1268) and `--simulate moved` (no older develop can host #1287).', '',
 '## The batch — every head re-read by the drafter from origin (ls-remote + a fetch into a `--no-local` scratch clone + the PULLS API; all agree)',
 '| PR | ticket | head | commits on merge-base | files | squash subject chars (`<title> (#n)`) | tier — why, from the DIFF |', '|---|---|---|---|---|---|---|'] + rows + ['',
 'Linear: every PR links its ticket(s) as `contributes`; none `closes` (linear_reads_1.out); no PR body puts a closing word before a key (gh_read_1.out). No PR is stacked',
 'on another (measured: no head is another\'s ancestor; every pair\'s merge-base is on develop).', '',
 '## Develop at the pin',
 'Pinned over develop **`%s`** (tree `%s`), READ by ls-remote and fetched (gate26\'s eleven squashes over 00de57baeb40, ending #1284). END_TREE **`%s`** (%s), identical in all %d orders (%d merge-tree calls). No sibling kit: END_TREE_WITH_SIBLING == END_TREE.' % (
     P['develop'], P['develop_tree'], P['end_tree'], P['end_shortstat'], P['orders'], P['merge_tree_calls']),
 'The launch action\'s step 3b re-pins on any move (Seat M1 merges on GOs).', '',
 '## Overlaps — ONE DECLARED (byte-identical), NONE found',
 '- Kit pairs: disjoint (6 pairs). Every other OPEN PR at the pin (%d, the PULLS API census): disjoint from every kit path.' % len(P['inflight']),
]
for b, rs in sorted(P.get('dead_open_same_blob', {}).items()):
    for r in rs:
        out.append('- **DECLARED:** dead-open **#%s** (head `%s`, NO GO at its cap in gate26T2) carries #%s\'s `%s` at the SAME blob `%s` (== #%s\'s `%s`). Merged-blob target = #%s\'s head blob. #%s must close unmerged: merged after #%s it would land its failed ks781 rule.' % (
            b, r['dead_open_head'], r['pr'], r['path'].split('/')[-1], r['blob_dead_open'], r['pr'], r['blob_kit'], r['pr'], b, r['pr']))
out += ['', '## Fleet STOP (READ, bounded region, NOT-FOUND control)']
for n in sorted(K['prs']):
    s = S[n]
    out.append('- #%s `%s` (%d lines, rc %s): %s' % (n, os.path.basename(s['log']), s['lines'], s['rc'],
        ('%s · %s · %s · %s; "%s"' % (s['pre_push_hook_base'], s['fixture_guard'], s['run_shell_suites_region'], s['shell_suites'], s['verdict_line'])) if s['preflight_ran'] else 'a systemTest/ push, no preflight — NOT APPLICABLE'))
out += ['- Declared at 00de57baeb40 (Seat B 30th handover, on #1285\'s and #1286\'s pushes; carried by gate26T2\'s report): 28/0 · 6/0 · 49/0 · 60 of 60. By path class no kit PR changes it:',
        '  #1285 edits a .sh under scripts/ that is not a `*.test.sh` in run-shell-suites.sh\'s ROOTS and is invoked by no suite (READ) — its own self-test count 20 -> 22 is a SEPARATE count. The gate measures membership (`--list`).', '']
out += ['## LEGITIMATE SHAPES — the drafter\'s predictions (the gate MEASURES every row)', '| PR | shape | predicted | predicted-by |', '|---|---|---|---|']
for l in open(D + '/probe1278_1.out').read().splitlines()[1:]:
    m = re.match(r'^(.{62}) (hits=\d+|callsReadYaml=\w+) want=(\S+)', l)
    if m: out.append('| #1278 | %s | %s (drafter wanted %s) | drafter PROBE (probe1278_1.out: the REAL head function under node 24, typescript 6.0.3; not vitest) |' % (m.group(1).strip().replace('|', '/'), m.group(2).replace('|', '/'), m.group(3)))
for l in open(D + '/probe1285_1.out').read().splitlines():
    m = re.match(r'^(base|head|armT|armC): (rc \d+ \| PASS \d+ FAIL \d+) .*docker shim calls (\d+)', l)
    if m: out.append('| #1285 | self-test %s | %s; docker shim calls %s | drafter PROBE (probe1285_1.out: git-archive extracts, /bin/bash 3.2) |' % (
        {'base': 'at the merge-base', 'head': 'at the head', 'armT': 'test hunk ALONE on the merge-base', 'armC': 'head with the producer clamp restored'}[m.group(1)], m.group(2).replace('|', '/'), m.group(3)))
for l in open(D + '/predict_1.out').read().splitlines():
    if l.startswith('  #1286 ') and ('PREDICTION' in l or 'FLAG CENSUS' in l): out.append('| #1286 | %s | | drafter READ (predict_1.out) |' % l[8:].replace('|', '/')[:900])
    if l.startswith('  #1287 ') and ('BLOB' in l or 'COUPLING' in l): out.append('| #1287 | %s | | drafter READ (predict_1.out) |' % l[8:].replace('|', '/')[:900])
open(D + '/COMMISSION.md', 'w').write('\n'.join(out) + '\n')
print('wrote', D + '/COMMISSION.md', len(out), 'lines')
