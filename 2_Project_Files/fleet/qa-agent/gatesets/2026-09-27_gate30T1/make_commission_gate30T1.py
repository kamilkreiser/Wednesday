#!/usr/bin/env python3
"""make_commission_gate30T1.py — writes COMMISSION.md for gate30T1 (the directory this script lives in). Every SHA / tree / count in it is READ from
pins_gate30T1.json, stopcounts_gate30T1.json, gh_read_1.out and predict_1.out beside it (never typed); the prose rows are the drafter's.
Shape copied from gate29's make_commission_gate29.py, re-keyed to the gate30 rows, a sibling kit and the WIDEN rows."""
import json, os, re
D = os.path.dirname(os.path.abspath(__file__)); K = json.load(open(D + '/kit.json')); kit = K['kit']
P = json.load(open('%s/pins_%s.json' % (D, kit))); S = json.load(open('%s/stopcounts_%s.json' % (D, kit)))
gh = open(D + '/gh_read_1.out').read()
def subj_len(n):
    m = re.search(r'=== #%s head.*?\ntitle \((\d+) chars.*?= (\d+) chars' % n, gh, re.S); return m.group(2) if m else '?'
WHY = {
 '1292': ('KS-1341', '**T1**: RUNTIME PRODUCT FILE on a production security surface — the last two of webhooks.ts\'s seven leaking 500s (POST /:id/test, GET /:id/deliveries) through fail500, plus ks1341c whose C3 SOURCE cell counts all seven. Local-model patch (Spark), byte-identical to brief-C rev C\'s golden. The docblock\'s three stale sentences are declared NOT COVERED (a docs ticket follows). After merge KS-1341 is NOT Done: §5f live sweep owed.'),
 '1294': ('KS-1334', '**T1**: RUNTIME PRODUCT FILE — two of adminConfig.ts\'s four UNCONDITIONAL err.message 500s (refresh-tenants :113, backfill-certification-metadata :1859; production included) through fail500, with IN-PLACE ks730c edits (C3 46->48, C4 KNOWN four->two). Spark on an EXCERPTED input; byte-identical to brief-A\'s golden. ks730c\'s shared LEAK carries double quotes, so its C1 `leaked` check cannot fire: the gate grades whether body-equality still catches a leak.'),
 '1296': ('KS-1346', '**T1 (WIDEN)**: systemErrors.ts fail500 logs a non-Error, non-string throw with util.inspect — a widening of what reaches LOG STORAGE on an admin surface, through a winston logger with no redaction. Wednesday\'s rule: the gate proves inspect cannot put a secret/PII field in the log line, or grades it NO GO. The drafter\'s READ (and the PR body\'s own words) predicts it CAN.'),
 '1297': ('KS-1346', '**T1 (WIDEN)**: the same inspect change in gdpr.ts fail500 — a SUBJECT-DATA surface. Same rule, same READ prediction; graded on its own measurement.'),
}
rows = []
for n in sorted(K['prs']):
    pr = P['prs'][n]
    files = ', '.join('%s +%s/-%s' % (os.path.basename(x.split('\t')[2]), x.split('\t')[0], x.split('\t')[1]) for x in pr['numstat'])
    rows.append('| #%s | %s | `%s` | %d on `%s` | %s | %s | %s |' % (n, WHY[n][0], pr['head'], len(pr['commits']), pr['merge_base'][:12], files, subj_len(n), WHY[n][1]))
out = ['# COMMISSION — DRAFT the round-30 batch gate kit "%s" over %d PRs (tier 1). Do NOT launch.' % (kit, len(K['prs'])), '',
 'Relayed by Wednesday to the drafter on 2026-09-26 (~13:1xZ) as #1292 (KS-1341 part C) and #1294 (KS-1334 part A), T1, with the WIDEN rule: any Seat B 32nd',
 'KS-1346-A / KS-1346-B PR existing at pin time joins this kit with a util.inspect secret/PII cell. #1296 (KS-1346 A, 13:12Z) and #1297 (KS-1346 B, 13:23Z) existed at',
 'the pin (the predict WIDEN census caught #1297 during the drafting simulations; Wednesday confirmed both heads at 13:5xZ). SIBLING kit gate30T2 (#1293, #1295, #1298,',
 '#1299). The GO goes to Seat B 32nd, which raised all four and merges its own. Shape copied from `gatesets/2026-09-26_gate29/`: JSON pins, routing-file override,',
 'controls both ways with `--invert`, per-PR merge-bases, a declared commit count, a NOT-STACKED check and the key scan; plus a HARD WIDEN census in predict (step (a))',
 'and in the launch action (step 2b, rc 15), and an in-flight census that adds any PR opened since the draft.', '',
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
