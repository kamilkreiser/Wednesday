#!/usr/bin/env python3
"""make_commission_gate31.py — writes COMMISSION.md for gate31 (the directory this script lives in). Every SHA / tree / count in it is READ from
pins_gate31.json, stopcounts_gate31.json, gh_read_1.out and predict_1.out beside it (never typed); the prose rows are the drafter's.
Shape copied from gate30T1's make_commission_gate30T1.py, re-keyed to gate31's mixed tiers, the stack and the item-4 WIDEN row."""
import json, os, re
D = os.path.dirname(os.path.abspath(__file__)); K = json.load(open(D + '/kit.json')); kit = K['kit']
P = json.load(open('%s/pins_%s.json' % (D, kit))); S = json.load(open('%s/stopcounts_%s.json' % (D, kit)))
gh = open(D + '/gh_read_1.out').read()
def subj_len(n):
    m = re.search(r'=== #%s head.*?\ntitle \((\d+) chars.*?= (\d+) chars' % n, gh, re.S); return m.group(2) if m else '?'
WHY = {
 '1300': ('KS-1334', '**T1**: RUNTIME PRODUCT FILE on a production security surface — the last two of adminConfig.ts\'s four UNCONDITIONAL err.message 500s (seed-demo-users :2031, migrate-tenant-data :2158; production included) through fail500, with IN-PLACE ks730c edits (C3 48->50, C4 KNOWN emptied, a part-B block). Spark on an EXCERPTED input; golden-EXACT (predict). After merge KS-1334 is NOT Done: §5f live sweep owed, and a fifth per-tenant site (a 200 body) has no ruled fix-shape.'),
 '1301': ('KS-1349', '**T2**: TEST-ONLY, STACKED on #1300 (GitHub base = #1300\'s branch; #1300\'s head is its commit\'s parent) — ks730c C1 clears the logger per NODE_ENV and asserts the whole call list. Graded by a PRODUCT TAMPER at the stacked head: the commission\'s production-only tamper is PREDICTED NOT to discriminate (C1 has no production row); the brief\'s development-only tamper does. END_TREE only in orders with #1300 first; the GO carries the RETARGET step.'),
 '1302': ('KS-1348', '**T1 (WIDENS LOG STORAGE)**: utils/logger.ts gives both production File transports `combine(json())`. The files held the literal `undefined`; they now hold every rendered field. The drafter MEASURED (logprobe_1.out) all six sentinel secret/PII fields of a logged metadata object landing in both files at head and in neither at develop; stdout carried them at both. The gate says plainly whether this is KS-1346\'s class.'),
 '1303': ('KS-1350', '**T3 (WIDEN row, joined at the pin)**: a COMMENT-ONLY edit of webhooks.ts\'s fail500 docblock (:549-:561). Graded by CODE-TOKEN EQUIVALENCE — parser leaves minus the JSDoc kind range — MEASURED IDENTICAL by the drafter with five controls that behaved.'),
}
rows = []
for n in sorted(K['prs']):
    pr = P['prs'][n]
    files = ', '.join('%s +%s/-%s' % (os.path.basename(x.split('\t')[2]), x.split('\t')[0], x.split('\t')[1]) for x in pr['numstat'])
    base = ('#%s head `%s`' % (pr['stacked_on'], pr['merge_base'][:12])) if pr.get('stacked_on') else '`%s`' % pr['merge_base'][:12]
    rows.append('| #%s | %s | `%s` | %d on %s | %s | %s | %s |' % (n, WHY[n][0], pr['head'], len(pr['commits']), base, files, subj_len(n), WHY[n][1]))
rt = P['retarget'].get('1301', {})
out = ['# COMMISSION — DRAFT the round-31 batch gate kit "%s" over %d PRs (MIXED tiers: T1, T2, T1, T3). Do NOT launch.' % (kit, len(K['prs'])), '',
 'Relayed by Wednesday to the drafter on 2026-09-27 (~05:3xZ) as #1300 (KS-1334 part B, T1), #1301 (KS-1349, T2, STACKED on #1300), #1302 (KS-1348, T1) and item 4',
 '(KS-1350, T3, not yet raised at commission time) under the WIDEN rule: if Seat B 33rd\'s KS-1350 PR exists at the pin it JOINS with a code-token-equivalence check.',
 '#1303 (KS-1350, branch feature/ks-1350-fail500-docblock-b33-4, opened 05:28:43Z) existed at the pin (gh_read_1.out WIDEN census; Wednesday\'s follow-up message',
 'confirmed head 0103e2dd5ab6). ONE kit, no sibling. The GO goes to Seat B 33rd, which raised all four and merges its own. Shape copied from `gatesets/2026-09-27_gate30T1/`',
 'and `_gate30T2/`: JSON pins, routing-file override, controls both ways with `--invert`, per-PR chain bases, a declared commit count, a stacked/not-stacked check (the',
 'declared stack asserted, every other pair NOT stacked), the key scan, a HARD WIDEN census in predict (step (a)) and in the launch action (step 2b, rc 15).', '',
 '## The batch — every head re-read by the drafter from origin (ls-remote + a fetch into a `--shared --no-checkout` scratch clone + the PULLS API; all agree)',
 '| PR | ticket | head | commits on chain base | files | squash subject chars (`<title> (#n)`) | tier — why, from the DIFF |', '|---|---|---|---|---|---|---|'] + rows + ['',
 'Linear: every PR links its ticket as `contributes`; none `closes` (linear_reads_1.out); no PR title, body or commit message puts a closing word before a key (keyscan_1.out).',
 'STACK (measured): #1301 on #1300 only; every other pair NOT stacked (no head is another\'s ancestor; every merge-base is on develop). MG-11: #1301 (93) and #1302 (96) exceed 92 as titled — the prompt mandates SHORT subjects.', '',
 '## Develop at the pin',
 'Pinned over develop **`%s`** (tree `%s`), READ by ls-remote and fetched (the last squash is #1299 KS-1339; gate30T1\'s #1292/#1294 and gate30T2\'s four landed over 3f70224a069b). END_TREE **`%s`** (%s), identical in all %d valid orders (#1300 before #1301; %d merge-tree calls). RETARGET (simulated: #1300 squashed over develop, #1301 merged with git\'s own merge-base %s): **`%s`** == develop+#1300+#1301, diff(squash, result) == %s.' % (
     P['develop'], P['develop_tree'], P['end_tree'], P['end_shortstat'], P['orders'], P['merge_tree_calls'], (rt.get('natural_merge_base') or '-')[:12], rt.get('result_tree'), rt.get('own_paths_after_retarget')),
 'The launch action\'s step 3b re-pins on any move.', '',
 '## Overlaps — ONE declared (the stack), NONE found',
 '- Kit pairs: disjoint except the declared stack pair #1300/#1301 (both edit ks730c; the final target is #1301\'s head blob). Every other OPEN PR at the pin (%d, the PULLS API census; #1296/#1297 are gate30T1\'s held KS-1346 rows): disjoint from every kit path.' % len(P['inflight']), '',
 '## Fleet STOP (READ, bounded region, NOT-FOUND control)']
for n in sorted(K['prs']):
    s = S[n]
    out.append('- #%s `%s` (%d lines, rc %s): %s' % (n, os.path.basename(s['log']), s['lines'], s['rc'],
        ('%s · %s · %s · %s; "%s"' % (s['pre_push_hook_base'], s['fixture_guard'], s['run_shell_suites_region'], s['shell_suites'], s['verdict_line'])) if s['preflight_ran'] else 'NO PREFLIGHT — NOT APPLICABLE'))
out += ['- By path class no kit PR changes the count (originate .ts route / util files and jest cells — no `*.test.sh`): after this merge 28/0 · 6/0 · 49/0 · 60 of 60.', '']
out += ['## LEGITIMATE SHAPES — the drafter\'s READ predictions (the gate MEASURES every row; a row saying MEASURED is a drafter\'s run, still not the gate\'s evidence)', '| PR | prediction | predicted-by |', '|---|---|---|']
for l in open(D + '/predict_1.out').read().splitlines():
    m = re.match(r'^  #(\d+) (.*)$', l)
    if m and not m.group(2).startswith(('product files', 'NO product file')):
        out.append('| #%s | %s | drafter %s (predict_1.out) |' % (m.group(1), m.group(2).replace('|', '/')[:1300], 'MEASURED' if 'MEASURED' in m.group(2)[:120] else 'READ'))
open(D + '/COMMISSION.md', 'w').write('\n'.join(out) + '\n')
print('wrote', D + '/COMMISSION.md', len(out), 'lines')
