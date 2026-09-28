#!/usr/bin/env python3
"""make_commission_gate38.py — writes COMMISSION.md for gate38 (the directory this script lives in). Every SHA / tree / count in it is READ from
pins_gate38.json, stopcounts_gate38.json, pgprobe_gate38.json, fill_1.out and predict_1.out beside it (never typed); the prose rows are the drafter's.
Shape copied from gate37's make_commission (gate36 -> gate35 lineage), re-keyed to gate38's three rows (T1 x3), no stack, one base."""
import json, os, re
D = os.path.dirname(os.path.abspath(__file__)); K = json.load(open(D + '/kit.json')); kit = K['kit']
P = json.load(open('%s/pins_%s.json' % (D, kit))); S = json.load(open('%s/stopcounts_%s.json' % (D, kit))); PG = json.load(open('%s/pgprobe_%s.json' % (D, kit)))
fill = open(D + '/fill_1.out').read()
def lands(n):
    m = re.search(r'#%s (\d+)->(\d+)' % n, fill); return 'declared %s -> lands %s' % (m.group(1), m.group(2)) if m else '?'
R = PG['runs']
def dbs(k): d = R[k].get('db', {}); return '039 tracked %s, fn %s, policy %s' % (d.get('tracked_039'), d.get('fn_auth_find_oauth_app_by_client_id') or 'ABSENT', d.get('oauth_apps_auth_lookup_policy'))
WHY = {
 '1330': ('KS-1352 verify', '**T1 VERIFY TRUTH** (a public credential route, a shared package): the shared VC verifier gains two credential-id-keyed resolvers (the stored issuer record; the status list\'s own bit) and fails a credential either marks revoked; the status check now runs without a submitted credentialStatus; an unknown id ABSTAINS (pass-through — the OPEN card\'s default a). Wired into credentials/verify AND presentations/verify (the seat drove NO presentation cell). Plus BACKLOG.md (+23, the pre-existing red). READ: the only new failure conditions are the two `found && revoked` tests and a resolver THROW (fail-closed on a lookup error).'),
 '1332': ('KS-1054 health + 039', '**T1 SCHEMA / START-UP**: 039 guards `auth_find_oauth_app_by_client_id` on oauth_apps existing and the owner/grant loop skips an absent function; runStartupMigrations returns + records `{ ran, applied, failed, lastRunAt, error? }`, served on /health and /health/ready, codes unchanged. **MEASURED by the drafter on a real PostgreSQL 18.3: on a BARE database the head records 039 at boot 1 with the function skipped, and boot 2 NEVER creates it (nor the oauth_apps_auth_lookup policy) — the base heals at boot 2** (FRESH-DB-039-NEVER-COMPLETES). READ: CORE-stage throws are not counted; `error` is never set.'),
 '1334': ('KS-888 validate pin', '**T2 TEST-ONLY PIN**: three cells in the ks888 file pin validate\'s log-only usage write (Kam ruled a); NO product byte (MEASURED). MEASURED: the PR == the canonical patch. CONTRADICTION (READ): the body says the cells are GREEN at the untouched tip by design, the checker says RED-FIRST "1 failed / 19 run" at the tip — the gate rules which holds.'),
 '1333': ('KS-1124 F4', '**T1 CERTIFICATION STATUS** (a verify answer): both certification routes save `status: \'failed\'` when anchoring failed (Kam ruled b); the success leg unchanged. MEASURED: the PR == the canonical patch (READY block == golden == checker patch.diff; strict `git apply` at the merge-base gives the head\'s blobs exactly). READ: documents.ts :1098 / :1532 / :1338 read only `anchor_failed` (a bare \'failed\' reads anchored there — "Nothing gets worse", the body).'),
}
rows = []
for n in sorted(K['prs']):
    pr = P['prs'][n]
    files = ', '.join('%s +%s/-%s' % (os.path.basename(x.split('\t')[2]), x.split('\t')[0], x.split('\t')[1]) for x in pr['numstat'])
    rows.append('| #%s | %s | %s | `%s` | %d on `%s` | %s | %s | %s |' % (n, WHY[n][0], K['prs'][n]['tier'], pr['head'], len(pr['commits']), pr['merge_base'][:12], files, lands(n), WHY[n][1]))
out = ['# COMMISSION — DRAFT the round-38 batch gate kit "%s" over %d PRs (T1 x3 + T2 x1). Do NOT launch.' % (kit, len(K['prs'])), '',
 'Commissioned by Wednesday to the drafter on 2026-09-29 (~00:55 AEST) for Seat B 40th\'s round: #1330 (KS-1352) and #1332 (KS-1054), base develop 0d156d12cc0f;',
 'develop has since moved to 3d706c21f65e by two merge commits that are not ours (#1329 KS-1354, #1331 KS-1365); END_TREE on the CURRENT develop, orders proven.',
 'Possibly #1333 / #1334 under Seat B 40th\'s ADDENDUM 1 (KS-1124 F4 TIER 1; a KS-888 validate log-only TEST-ONLY pin TIER 2) — poll up to 45 min and',
 'include what appears (their canonical patches must EQUAL the PR diffs). #1333 appeared at 2026-09-28T15:08:42Z and #1334 at 15:24:30Z (branch -b40-4);',
 'BOTH are IN this kit. All raised by Seat B 40th, which merges its own on Wednesday\'s signed GO — the GO SUBJECT names "Seat B 40th",',
 'no `#`: `GO (Seat B 40th): merge 1330 1332 1333 1334 on gate38` (routing line `QA/Secuura-batch1330`, NOT added by the drafter). #1330: both revoke routes;',
 'verify fails for a record OR status list marking revoked; unknown ids PASS THROUGH (Wednesday\'s ruling; card secuura-ks1352-unknown-credential-id-verify-policy',
 'default a; KS-1368 filed) — measure that pass-through is exactly what ships and nothing wider; presentations/verify and the gateway paths the seat names.',
 '#1332: keep serving + flag failed start-up migrations on /health AND /health/ready with 200 + a field; the stage order via a guard on 039 :224-228 (Kam',
 'ruled a). The seat NEVER executed 039: the gate MUST run the two-sided fresh-DB drill on a REAL PostgreSQL (fresh DB at base vs head, the guarded SQL parses',
 'and runs, boot twice, /health and /health/ready bodies as served); the TS2322 x4 widening: the including-program delta zero. STANDING REQUIREMENTS',
 '(Wednesday\'s ledger 2026-09-29): (1) develop\'s `packages/shared` 1 failed / 945 since #1327 (the KS-764 guard, :77 / :97) is reported PRE-EXISTING unless a PR',
 'changes its count; (2) every suite referencing a changed path is RUN (git grep across Blockchain/Dev); in particular the KS-764 guard at #1332\'s head.', '',
 '## The batch — every head re-read by the drafter from origin (ls-remote + a fetch into a `--shared --no-checkout` scratch clone + the PULLS API; all agree)',
 '| PR | ticket | tier | head | commits on merge-base | files | subject (no `(#n)`) | why this tier, from the DIFF |', '|---|---|---|---|---|---|---|---|'] + rows + ['',
 'Tiers per 0_Brain/learnings/2026-09-05_qa-gate-tiers-and-the-two-nogo-cap.md: T1 = security surfaces, data destruction and erasure, anything deploying to dev / demo; T2 = tests-only, docs, config/CI, follow-ups whose MECHANISM a prior gate measured.',
 'Linear: every PR links its ticket as `contributes`; none `closes` (linear_reads_1.out); no title, body or commit message carries a closing word before a key or a FOREIGN hyphenated key (keyscan_1.out).',
 'NOT STACKED (measured): no head is another\'s ancestor; one merge-base. MG-11 as it LANDS: each title is the declared subject, WITHOUT the (#n) suffix (all <= 92).', '',
 '## Develop at the pin',
 'Pinned over develop **`%s`** (tree `%s`), READ by ls-remote and fetched. ONE merge-base, MEASURED: `%s` for all four. END_TREE **`%s`** (%s), identical in all %d orders (%d merge-tree calls, each with the PR\'s own merge-base).' % (
     P['develop'], P['develop_tree'], P['merge_bases'][0][:12], P['end_tree'], P['end_shortstat'], P['orders'], P['merge_tree_calls']),
 'The launch action\'s step 3b re-pins on any further move.', '',
 '## Overlaps — NONE declared, NONE found',
 '- Kit: four disjoint path sets. Every other OPEN PR at the pin (%d, the PULLS API census): disjoint from every kit path.' % len(P['inflight']),
 '- `merged_blob_paths` NONE and `noop_paths` NONE — two different declarations, each asserted empty by predict (c).', '',
 '## The drafter\'s real-Postgres drill (#1332; pgprobe_1.out, %s)' % PG.get('engine', '?')[:40],
 '- BARE-base: boot 1 %s; boot 2 %s.' % (dbs('BARE-base boot 1'), dbs('BARE-base boot 2')),
 '- BARE-head: boot 1 %s (recorded %s); boot 2 %s (recorded %s).' % (dbs('BARE-head boot 1'), json.dumps(R['BARE-head boot 1'].get('recorded')), dbs('BARE-head boot 2'), json.dumps(R['BARE-head boot 2'].get('recorded'))),
 '- INIT (docker/init-seeded): base %s; head %s — the guard is inert there.' % (dbs('INIT-base boot 1'), dbs('INIT-head boot 1')),
 '- Controls: %s.' % PG['controls'], '',
 '## Fleet STOP (READ, bounded region, NOT-FOUND control)']
for n in sorted(K['prs']):
    s = S[n]
    if s.get('log') == 'ABSENT': out.append('- #%s: NO push log in the seat record at drafting — UNREAD.' % n); continue
    out.append('- #%s `%s` (%d lines): %s · %s · %s · %s; "%s"' % (n, os.path.basename(s['log']), s['lines'], s['pre_push_hook_base'], s['fixture_guard'], s['run_shell_suites_region'], s['shell_suites'], s['verdict_line']))
out += ['- By path class no kit PR changes the count (no `*.test.sh`); #1332 changes 039, which ks949_main_seed_idempotence.test.sh executes on a docker/init-seeded DB (guard inert) — the gate runs it. After this merge 28/0 · 6/0 · 49/0 · 60 of 60.', '']
out += ['## LEGITIMATE SHAPES — the drafter\'s READ predictions (the gate MEASURES every row; a row saying MEASURED is a drafter\'s run, still not the gate\'s evidence)', '| PR | prediction | predicted-by |', '|---|---|---|']
for l in open(D + '/predict_1.out').read().splitlines():
    m = re.match(r'^  #(\d+) (.*)$', l)
    if m and not m.group(2).startswith(('PRODUCT files', 'NO product file')):
        out.append('| #%s | %s | drafter %s (predict_1.out) |' % (m.group(1), m.group(2).replace('|', '/')[:1500], 'MEASURED' if 'MEASURED' in m.group(2)[:160] else 'READ'))
open(D + '/COMMISSION.md', 'w').write('\n'.join(out) + '\n')
print('wrote', D + '/COMMISSION.md', len(out), 'lines')
