#!/usr/bin/env python3
"""make_commission_gate30T2.py — writes COMMISSION.md for gate30T2 (the directory this script lives in). Every SHA / tree / count in it is READ from
pins_gate30T2.json, stopcounts_gate30T2.json, gh_read_1.out and predict_1.out beside it (never typed); the prose rows are the drafter's.
Shape copied from gate29's make_commission_gate29.py, re-keyed to the gate30 rows, a sibling kit and the WIDEN rows."""
import json, os, re
D = os.path.dirname(os.path.abspath(__file__)); K = json.load(open(D + '/kit.json')); kit = K['kit']
P = json.load(open('%s/pins_%s.json' % (D, kit))); S = json.load(open('%s/stopcounts_%s.json' % (D, kit)))
gh = open(D + '/gh_read_1.out').read()
def subj_len(n):
    m = re.search(r'=== #%s head.*?\ntitle \((\d+) chars.*?= (\d+) chars' % n, gh, re.S); return m.group(2) if m else '?'
WHY = {
 '1293': ('KS-1344', '**T2**: TEST-ONLY (one hunk, +3/-1 in ks1341a): per-environment mockClear + whole call list. Its red comes from a PRODUCT tamper (webhooks.ts:563 production-only logging): A1 rows RED at head, GREEN at the tip under the same tamper.'),
 '1295': ('KS-1337', '**T2**: TOOLING — systemTest/akto preSuiteSetup.ts fileURLToPath + one vitest cell; no Blockchain/Dev path, so the push ran the format gate only (NO platform preflight): the gate runs the akto package\'s own lint + format:check + unit suite, space-free and from a SPACED path. Site 2 of 3.'),
 '1298': ('KS-1347', '**T2 (WIDEN)**: TEST FILES ONLY in services/auth (ks732 path reads via fileURLToPath + a new vitest cell). ks732 lines golden-EXACT; ONE token of the new cell renamed on review (`line` -> `_line`, TS6133). Test-inclusive tsc 37 vs 37 (rows moved). Site 1 of 2.'),
 '1299': ('KS-1339', '**T2 (WIDEN)**: TEST FILES ONLY in services/originate: ks1293 CONFIGPINNED asserts the offender list before the count (one moved line) + a new jest cell that EXECUTES the cell\'s statements read as text (new Function). Golden-EXACT.'),
}
rows = []
for n in sorted(K['prs']):
    pr = P['prs'][n]
    files = ', '.join('%s +%s/-%s' % (os.path.basename(x.split('\t')[2]), x.split('\t')[0], x.split('\t')[1]) for x in pr['numstat'])
    rows.append('| #%s | %s | `%s` | %d on `%s` | %s | %s | %s |' % (n, WHY[n][0], pr['head'], len(pr['commits']), pr['merge_base'][:12], files, subj_len(n), WHY[n][1]))
out = ['# COMMISSION — DRAFT the round-30 batch gate kit "%s" over %d PRs (tier 2). Do NOT launch.' % (kit, len(K['prs'])), '',
 'Relayed by Wednesday to the drafter on 2026-09-26 (~13:1xZ) as #1293 (KS-1344) and #1295 (KS-1337 akto site), T2, with the WIDEN rule: any Seat B 32nd KS-1347 /',
 'KS-1339 PR existing at pin time joins this kit. #1298 (KS-1347, 13:42Z) and #1299 (KS-1339, 13:52Z) existed at the pin (the predict WIDEN census caught each during',
 'the drafting simulations; Wednesday relayed both heads at 13:5xZ, equal to ls-remote). SIBLING kit gate30T1 (#1292, #1294, #1296, #1297). The GO goes to Seat B 32nd,',
 'which raised all four and merges its own. Shape copied from `gatesets/2026-09-26_gate29/` (see gate30T1\'s COMMISSION for the machinery), plus a HARD WIDEN census',
 'and a NOT-APPLICABLE fleet STOP row for #1295 (a systemTest/ push runs no platform preflight).', '',
 '## The batch — every head re-read by the drafter from origin (ls-remote + a fetch into a `--no-local` scratch clone + the PULLS API; all agree)',
 '| PR | ticket | head | commits on merge-base | files | squash subject chars (`<title> (#n)`) | tier — why, from the DIFF |', '|---|---|---|---|---|---|---|'] + rows + ['',
 'Linear: every PR links its ticket as `contributes`; none `closes` (linear_reads_1.out); no PR title, body or commit message puts a closing word before a key (keyscan_1.out).',
 'Not stacked (measured: no head is another\'s ancestor; every merge-base is on develop).', '',
 '## Develop at the pin',
 'Pinned over develop **`%s`** (tree `%s`), READ by ls-remote and fetched (gate29\'s two GO squashes over 179a4f32ec06: #1290, #1291 — its tree equals gate29\'s END_TREE `0cc6669f3a6e`). END_TREE **`%s`** (%s), identical in all %d orders (%d merge-tree calls). END_TREE_WITH_SIBLING (this kit + %s, either kit first): **`%s`**.' % (
     P['develop'], P['develop_tree'], P['end_tree'], P['end_shortstat'], P['orders'], P['merge_tree_calls'], K['sibling_kit'], P['end_tree_with_sibling']),
 'The launch action\'s step 3b re-pins on any move.', '',
 '## Overlaps — NONE declared, NONE found',
 '- Kit pairs: disjoint. Sibling kit %s: disjoint. Every other OPEN PR at the pin (%d, the PULLS API census; #1268/#1278/#1245/#1241 are CLOSED since gate29): disjoint from every kit path.' % (K['sibling_kit'], len(P['inflight'])), '',
 '## Fleet STOP (READ, bounded region, NOT-FOUND control)']
for n in sorted(K['prs']):
    s = S[n]
    out.append('- #%s `%s` (%d lines, rc %s): %s' % (n, os.path.basename(s['log']), s['lines'], s['rc'],
        ('%s · %s · %s · %s; "%s"' % (s['pre_push_hook_base'], s['fixture_guard'], s['run_shell_suites_region'], s['shell_suites'], s['verdict_line'])) if s['preflight_ran'] else 'NO PREFLIGHT (a systemTest/ path: the format gate only; every suite header reads NOT FOUND) — NOT APPLICABLE; the gate runs the package\'s own lint + unit suite'))
out += ['- By path class no kit PR changes the count (originate / auth .ts routes and test cells; a systemTest/akto .ts file + a vitest cell — no `*.test.sh`): after this merge 28/0 · 6/0 · 49/0 · 60 of 60.', '']
out += ['## LEGITIMATE SHAPES — the drafter\'s READ predictions (the gate MEASURES every row)', '| PR | prediction | predicted-by |', '|---|---|---|']
for l in open(D + '/predict_1.out').read().splitlines():
    m = re.match(r'^  #(\d+) (.*)$', l)
    if m and not m.group(2).startswith(('product files', 'NO product file')):
        out.append('| #%s | %s | drafter READ (predict_1.out) |' % (m.group(1), m.group(2).replace('|', '/')[:1100]))
open(D + '/COMMISSION.md', 'w').write('\n'.join(out) + '\n')
print('wrote', D + '/COMMISSION.md', len(out), 'lines')
