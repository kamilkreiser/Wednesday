#!/usr/bin/env python3
"""make_commission_gate37.py — writes COMMISSION.md for gate37 (the directory this script lives in). Every SHA / tree / count in it is READ from
pins_gate37.json, stopcounts_gate37.json, pgprobe_gate37.json, fill_1.out and predict_1.out beside it (never typed); the prose rows are the drafter's.
Shape copied from gate36's make_commission (gate35 -> gate34 lineage), re-keyed to gate37's two rows (T1 x2), no stack, one base."""
import json, os, re
D = os.path.dirname(os.path.abspath(__file__)); K = json.load(open(D + '/kit.json')); kit = K['kit']
P = json.load(open('%s/pins_%s.json' % (D, kit))); S = json.load(open('%s/stopcounts_%s.json' % (D, kit))); PG = json.load(open('%s/pgprobe_%s.json' % (D, kit)))
fill = open(D + '/fill_1.out').read()
def lands(n):
    m = re.search(r'#%s (\d+)->(\d+)' % n, fill); return 'declared %s -> lands %s' % (m.group(1), m.group(2)) if m else '?'
F = PG['runs']['F_update_cost_inprocess']
WHY = {
 '1327': ('KS-888 REVOKE', '**T1 KEY REVOCATION**: security index.ts — DELETE /api/keys/:id opts into `dbSaveApiKey(apiKey, { rethrow: true })` inside its own try; a failed save answers 503 (the mint\'s infrastructure classifier, copied inline — MEASURED byte-identical to the mint\'s) or 500, and the in-memory revoke (`apiKey.isActive = false`, before the try) is KEPT. Mint, validate, the key list and revokePriorConnectorKeys: handler regions MEASURED byte-equal merge-base vs head. A Spark golden (READY == golden == checker patch, MEASURED) applied strict: product blob == head; the test file == head after EXACTLY the four DECLARED hand-written lines (header :5-7, describe :98 — every fullName renamed). NOT COVERED (disclosed): in-process only; replicas and restarts still see the key active; nothing retries.'),
 '1328': ('KS-1335 last_attempted_at', '**T1 SCHEMA MIGRATION**: a nullable `last_attempted_at TIMESTAMPTZ` on svc_teams_webhooks at all three DDL sites (init 06, the CORE CREATE, the guarded add-column in startup-migrations.ts — runs at gateway start on main, platform and tenant DBs), the notify window ordered by it NULLS FIRST, ONE stamp after the deadline guard and before safeOutboundRequest (placement A), the skipped row NOT stamped. MEASURED on PGlite (%s): %s; the stamp UPDATE in-process median %s ms (a lower bound — no network). READ: a stamp that throws reports the row FAILED with no request made; the head route on an UNMIGRATED schema fails 42703 (deploy order).' % (PG['engine'][:16], ', '.join(k for k, v in PG['_summary'].items() if v), F['median_ms'])),
}
rows = []
for n in sorted(K['prs']):
    pr = P['prs'][n]
    files = ', '.join('%s +%s/-%s' % (os.path.basename(x.split('\t')[2]), x.split('\t')[0], x.split('\t')[1]) for x in pr['numstat'])
    rows.append('| #%s | %s | %s | `%s` | %d on `%s` | %s | %s | %s |' % (n, WHY[n][0], K['prs'][n]['tier'], pr['head'], len(pr['commits']), pr['merge_base'][:12], files, lands(n), WHY[n][1]))
out = ['# COMMISSION — DRAFT the round-37 batch gate kit "%s" over %d PRs (T1 x2). Do NOT launch.' % (kit, len(K['prs'])), '',
 'Commissioned by Wednesday to the drafter on 2026-09-28 (~20:37 AEST) for Seat B 39th\'s round: #1327 (KS-888 REVOKE) and #1328 (KS-1335), both on',
 'Secuura\'s `develop` 63db8a38354c (heads read by ls-remote at 20:37 AEST; re-read at pin). Both raised by Seat B 39th, which merges its own on Wednesday\'s',
 'signed GO — the GO SUBJECT must name "Seat B 39th", with no `#` before the PR numbers: `GO (Seat B 39th): merge 1327 1328 on gate37` (routing line',
 '`QA/Secuura-batch1327`). #1327: when the revoke\'s DB save fails, 503 (infrastructure) or 500 (other), KEEP the in-memory revoke; mint unchanged; validate',
 'UNCHANGED in this PR (Kam ruled at 20:22:15 that validate never refuses because of a failed usage write — a separate PR later); the existing ks888 test',
 'file is edited in place, its header :5-7 and describe :98 reworded, so every fullName changes. The gate MUST verify at runtime: no unhandled rejection or',
 'process exit under a failing revoke save; the key stops validating in-process after a failed-save revoke; mint and validate behave exactly as at',
 'develop; the KS-577 order holds on the rotate path. NOT COVERED, disclosed: in-process only (other replicas and restarts still see the key; nothing',
 'retries). #1328: `last_attempted_at` via the guarded add-column pattern (startup-migrations.ts:522-528 shape), stamped ONCE after the deadline guard and',
 'before safeOutboundRequest (Wednesday\'s ruling, placement A); the DEADLINE-SKIPPED branch (:1299-1302) deliberately NOT stamped; R3 rewritten. The gate',
 'verifies the ordering with real rows if a Postgres is available (say plainly if not), the skipped row NULL, the migration twice, and the extra',
 'happy-path UPDATE against the aggregate deadline. Merge order #1327 -> #1328. END_TREE in the drafter\'s own clone (both orders). Controls both ways.',
 'Subjects declared WITHOUT `(#n)`, landing <= 92, own key only; name any commit messages that must not be pasted. The MERGE ADDENDUM uses gate35\'s',
 'one-line-per-PR shape. Shape copied from `gatesets/2026-09-28_gate36/`. The drafter writes only in this kit directory and its own scratchpad: it did',
 'NOT add the routing line (README §4).', '',
 '## The batch — every head re-read by the drafter from origin (ls-remote + a fetch into a `--shared --no-checkout` scratch clone + the PULLS API; all agree)',
 '| PR | ticket | tier | head | commits on merge-base | files | subject (no `(#n)`) | why this tier, from the DIFF |', '|---|---|---|---|---|---|---|---|'] + rows + ['',
 'Tiers per 0_Brain/learnings/2026-09-05_qa-gate-tiers-and-the-two-nogo-cap.md: T1 = security surfaces (key revocation named), data destruction and erasure, anything deploying to dev / demo; T2 = tests-only, docs, config/CI, follow-ups whose MECHANISM a prior gate measured. #1327 is key revocation (T1; gate35 measured the MINT half, not the revoke, so it is not a tier-2 follow-up); #1328 is a schema change the gateway applies at its next start on every database it reaches (T1 — additive and nullable, not the destruction class).',
 'Linear: both PRs link their ticket as `contributes`; none `closes` (linear_reads_1.out); no PR title, body or commit message puts a closing word before a key, and none carries a FOREIGN hyphenated key (keyscan_1.out) — no commit message must be withheld on MG-3 grounds; the merger still composes each squash body (both messages end in a Co-Authored-By trailer; #1328\'s names "KS934" un-hyphenated; the test files carry KS-1194 (#1327) and KS-934 (#1328) hyphenated as CONTENT).',
 'NOT STACKED (measured): neither head is the other\'s ancestor; the pair\'s merge-base is develop itself. MG-11 as it LANDS: each title is the declared subject, WITHOUT the (#n) suffix (both <= 92; no SHORT subject this round).', '',
 '## Develop at the pin',
 'Pinned over develop **`%s`** (tree `%s`), READ by ls-remote and fetched — gate36\'s #1323-#1326 squashes in (MERGED). ONE merge-base, MEASURED: `%s` for both (each head\'s one commit has it as parent; develop has not moved since). END_TREE **`%s`** (%s), identical in both orders (%d merge-tree calls, each with the PR\'s own merge-base).' % (
     P['develop'], P['develop_tree'], P['merge_bases'][0][:12], P['end_tree'], P['end_shortstat'], P['merge_tree_calls']),
 'The launch action\'s step 3b re-pins on any move.', '',
 '## Overlaps — NONE declared, NONE found',
 '- Kit: two disjoint path sets and no shared service (#1328 touches api-gateway\'s startup-migrations.ts, #1327 only security). Every other OPEN PR at the pin (%d, the PULLS API census): disjoint from every kit path (#809, KS-693, sits in #1328\'s m365-integration service and shares no file).' % len(P['inflight']),
 '- `merged_blob_paths` (a genuine overlap) NONE and `noop_paths` (a squash-stack no-op) NONE — two different declarations, each asserted empty by predict (c).', '',
 '## Fleet STOP (READ, bounded region, NOT-FOUND control)']
for n in sorted(K['prs']):
    s = S[n]
    out.append('- #%s `%s` (%d lines, rc %s): %s' % (n, os.path.basename(s['log']), s['lines'], s['rc'],
        ('%s · %s · %s · %s; "%s"' % (s['pre_push_hook_base'], s['fixture_guard'], s['run_shell_suites_region'], s['shell_suites'], s['verdict_line'])) if s['preflight_ran'] else 'NO PREFLIGHT — NOT APPLICABLE'))
out += ['- By path class no kit PR changes the count (TypeScript routes, a migration array, a docker init SQL file and vitest cell files — no `*.test.sh`): after this merge 28/0 · 6/0 · 49/0 · 60 of 60.', '']
out += ['## LEGITIMATE SHAPES — the drafter\'s READ predictions (the gate MEASURES every row; a row saying MEASURED is a drafter\'s run, still not the gate\'s evidence)', '| PR | prediction | predicted-by |', '|---|---|---|']
for l in open(D + '/predict_1.out').read().splitlines():
    m = re.match(r'^  #(\d+) (.*)$', l)
    if m and not m.group(2).startswith(('PRODUCT files', 'NO product file')):
        out.append('| #%s | %s | drafter %s (predict_1.out) |' % (m.group(1), m.group(2).replace('|', '/')[:1300], 'MEASURED' if 'MEASURED' in m.group(2)[:140] else 'READ'))
open(D + '/COMMISSION.md', 'w').write('\n'.join(out) + '\n')
print('wrote', D + '/COMMISSION.md', len(out), 'lines')
