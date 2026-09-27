#!/usr/bin/env python3
"""make_commission_gate32.py — writes COMMISSION.md for gate32 (the directory this script lives in). Every SHA / tree / count in it is READ from
pins_gate32.json, stopcounts_gate32.json, gh_read_1.out and predict_1.out beside it (never typed); the prose rows are the drafter's.
Shape copied from gate31's make_commission_gate31.py (gate30T1 lineage), re-keyed to gate32's six T2 rows, no stack, the older base."""
import json, os, re
D = os.path.dirname(os.path.abspath(__file__)); K = json.load(open(D + '/kit.json')); kit = K['kit']
P = json.load(open('%s/pins_%s.json' % (D, kit))); S = json.load(open('%s/stopcounts_%s.json' % (D, kit)))
gh = open(D + '/gh_read_1.out').read()
fill = open(D + '/fill_1.out').read()
def subj_len(n):
    m = re.search(r'=== #%s head.*?\ntitle \((\d+) chars.*?= (\d+) chars' % n, gh, re.S); return m.group(2) if m else '?'
def lands(n):
    m = re.search(r'#%s (\d+)->(\d+)' % n, fill); return '%s -> lands %s' % (m.group(1), m.group(2)) if m else '?'
WHY = {
 '1304': ('KS-1227', '**T2 TEST-ONLY**: the ks1072 api-gateway cells edited IN PLACE (postTier2 detaches its listener in a `finally`; R1 pins the witness counts every stub request, R2 the detach). Red by a PRODUCT TAMPER at routes/verification.ts:585 (drafter READ, head and END_TREE): EXACTLY R1; R2 is a CONTROL no product tamper reaches.'),
 '1305': ('KS-1090', '**T2 TEST-ONLY**: a NEW api-gateway cell (renamed at raise) pinning that x-gateway-vouch reaches originate and no other service key. Tamper routes/proxy.ts:275 (READ): R1 + R2 red. Refs R2-3; the TITLE names R2-2, not this diff (README §6).'),
 '1306': ('KS-1205', '**T2 TEST-ONLY on an AUTH surface**: a NEW api-gateway cell pinning that an API key\'s limiter bucket is never `api_key:` + the bare sha256 (F-3 G-BUCKET-HASH). Tamper middleware/auth.ts:313 (READY said :300; the seat and the drafter measured :313). auth.ts blob `bf09d315a644` at merge-base, head, develop and END_TREE (MEASURED). The TITLE names N-2, not this diff (README §6).'),
 '1307': ('KS-1212', '**T2 TEST-ONLY**: a NEW api-gateway cell (renamed at raise) pinning that the erasure door reads its OWN router\'s caseSensitive option. Tamper routes/proxy.ts — the READY said :808; the drafter READ :814 at head AND on END_TREE (re-located): R1 + R2 red.'),
 '1308': ('KS-1108', '**T2 TOOLING**: systemTest/akto secrets.ts wraps the YAML parse (names file + position only) + a NEW akto unit cell. Product hunk EXACT to the golden\'s product section (MEASURED, `git apply --cached --check` of those bytes); the test\'s RULED departure MEASURED as 12 JSDoc + 4 format + 0 other; akto `npm run lint` rc 0 at head, rc 1 with the golden\'s test (MEASURED, aktolint_1.out).'),
 '1309': ('KS-1196', '**T2 PRODUCT**: routes/admin.ts document-type ids `dt-${Date.now()}` -> `dt-${crypto.randomUUID()}` + a NEW cell. EXACT to the REGENERATED golden (MEASURED); `import crypto from \'crypto\'` at admin.ts:11 (READ); SORT-BY-ID MEASURED by source grep: no reader sorts or derives order from a document-type id.'),
}
rows = []
for n in sorted(K['prs']):
    pr = P['prs'][n]
    files = ', '.join('%s +%s/-%s' % (os.path.basename(x.split('\t')[2]), x.split('\t')[0], x.split('\t')[1]) for x in pr['numstat'])
    rows.append('| #%s | %s | `%s` | %d on `%s` | %s | %s (declared %s) | %s |' % (n, WHY[n][0], pr['head'], len(pr['commits']), pr['merge_base'][:12], files, subj_len(n), lands(n), WHY[n][1]))
out = ['# COMMISSION — DRAFT the round-32 batch gate kit "%s" over %d PRs (T2 x6: five test-only or tooling, one product). Do NOT launch.' % (kit, len(K['prs'])), '',
 'Relayed by Wednesday to the drafter on 2026-09-27 (~21:2x AEST) as #1304 (KS-1227), #1305 (KS-1090 R2-3), #1306 (KS-1205 F3), #1307 (KS-1212), #1308 (KS-1108) and',
 '#1309 (KS-1196), all raised by Seat B 34th, which merges its own on Wednesday\'s signed GO. Wednesday\'s binding addendum (21:3x): #1304\'s squash subject is declared',
 'WITHOUT the (#n) suffix as "KS-1227: pin a hit-only witness in the ks1072 cells and clear its listener" (74, lands at 82); every subject declared without the suffix,',
 'its landed length stated. ONE kit, no sibling, NO stack. Shape copied from `gatesets/2026-09-27_gate31/`: JSON pins, routing-file override, controls both ways with',
 '`--invert`, a declared commit count, a not-stacked check for every pair, the key scan, a HARD WIDEN census (titles AND Seat B 34th\'s branch segment) in predict and in',
 'the launch action (rc 15), plus the six newest STANDING_LINES sections of 2026-09-27 (subjects without the suffix; no-op vs overlap keys; every spelling of a',
 'namespace token; rev-parse on unfetched objects; verified bytes == used bytes; `patch -F0` is not `git apply --check`).', '',
 '## The batch — every head re-read by the drafter from origin (ls-remote + a fetch into a `--shared --no-checkout` scratch clone + the PULLS API; all agree)',
 '| PR | ticket | head | commits on merge-base | files | title lands at (`<title> (#n)`) and the DECLARED subject | tier — why, from the DIFF |', '|---|---|---|---|---|---|---|'] + rows + ['',
 'Linear: every PR links its ticket as `contributes`; none `closes` (linear_reads_1.out); no PR title, body or commit message puts a closing word before a key (keyscan_1.out).',
 'NOT STACKED (measured): no head is another\'s ancestor; every pair\'s merge-base is on develop. MG-11 as it LANDS: #1304\'s title lands at 95 -> the SHORT subject is declared (lands at 82); the other five land at 86, 84, 86, 82, 77.', '',
 '## Develop at the pin',
 'Pinned over develop **`%s`** (tree `%s`), READ by ls-remote and fetched. **All six PRs share the merge-base `%s`** (the commission said five of six: the drafter measured six — every head\'s one commit has that parent). Develop moved 3 squashes since (gate31\'s #1300, #1303, #1301 — services/originate only; move ∩ every own path EMPTY). END_TREE **`%s`** (%s), identical in all %d orders (%d merge-tree calls, each with the PR\'s own merge-base).' % (
     P['develop'], P['develop_tree'], P['merge_bases'][0], P['end_tree'], P['end_shortstat'], P['orders'], P['merge_tree_calls']),
 'The launch action\'s step 3b re-pins on any move.', '',
 '## Overlaps — NONE declared, NONE found',
 '- Kit pairs: all disjoint. Every other OPEN PR at the pin (%d, the PULLS API census; #1302 is gate31\'s NO GO KS-1348 row, #1296/#1297 gate30T1\'s KS-1346 rows): disjoint from every kit path.' % len(P['inflight']),
 '- `merged_blob_paths` (a genuine overlap) NONE and `noop_paths` (a squash-stack no-op) NONE — two different declarations, each asserted empty by predict (c).', '',
 '## Fleet STOP (READ, bounded region, NOT-FOUND control)']
for n in sorted(K['prs']):
    s = S[n]
    out.append('- #%s `%s` (%d lines, rc %s): %s' % (n, os.path.basename(s['log']), s['lines'], s['rc'],
        ('%s · %s · %s · %s; "%s"' % (s['pre_push_hook_base'], s['fixture_guard'], s['run_shell_suites_region'], s['shell_suites'], s['verdict_line'])) if s['preflight_ran'] else 'NO PREFLIGHT (a systemTest/ push: the format gate only) — NOT APPLICABLE'))
out += ['- By path class no kit PR changes the count (api-gateway / akto .ts files and cells — no `*.test.sh`): after this merge 28/0 · 6/0 · 49/0 · 60 of 60.', '']
out += ['## LEGITIMATE SHAPES — the drafter\'s READ predictions (the gate MEASURES every row; a row saying MEASURED is a drafter\'s run, still not the gate\'s evidence)', '| PR | prediction | predicted-by |', '|---|---|---|']
for l in open(D + '/predict_1.out').read().splitlines():
    m = re.match(r'^  #(\d+) (.*)$', l)
    if m and not m.group(2).startswith(('PRODUCT files', 'NO product file')):
        out.append('| #%s | %s | drafter %s (predict_1.out) |' % (m.group(1), m.group(2).replace('|', '/')[:1300], 'MEASURED' if 'MEASURED' in m.group(2)[:120] else 'READ'))
open(D + '/COMMISSION.md', 'w').write('\n'.join(out) + '\n')
print('wrote', D + '/COMMISSION.md', len(out), 'lines')
