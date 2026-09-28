#!/usr/bin/env python3
"""make_commission_gate39.py — writes COMMISSION.md for gate39 (the directory this script lives in). Every SHA / tree / count in it is READ from
pins_gate39.json, stopcounts_gate39.json, pgprobe_gate39.json, fill_1.out and predict_1.out beside it (never typed); the prose rows are the drafter's.
Shape copied from gate38's make_commission (gate37 -> gate36 lineage), re-keyed to gate39's two rows (T2 + T1), no stack, TWO merge-bases."""
import json, os, re
D = os.path.dirname(os.path.abspath(__file__)); K = json.load(open(D + '/kit.json')); kit = K['kit']
P = json.load(open('%s/pins_%s.json' % (D, kit))); S = json.load(open('%s/stopcounts_%s.json' % (D, kit))); PG = json.load(open('%s/pgprobe_%s.json' % (D, kit)))
fill = open(D + '/fill_1.out').read()
def lands(n):
    m = re.search(r'#%s (\d+)->(\d+)' % n, fill); return 'declared %s -> lands %s' % (m.group(1), m.group(2)) if m else '?'
R = PG['runs']; SUM = PG['_summary']
def four(k):
    d = R[k].get('db', {}) if isinstance(R.get(k), dict) else {}
    ft = d.get('four_tables') if isinstance(d.get('four_tables'), list) else []
    return '039 %s · fn %s · policy %s · %s' % (d.get('tracked_039'), 'present' if d.get('fn_auth_find_oauth_app_by_client_id') else 'ABSENT', d.get('oauth_apps_auth_lookup_policy'),
                                               ', '.join('%s %s' % (x['t'], 'RLS+FORCE+TI' if (x['rls'] and x['force'] and x['ti'] == 1) else 'RLS+FORCE, NO POLICY' if (x['rls'] and x['force']) else 'NO RLS') for x in ft))
def rm(k): x = R.get(k, {}); return 'rc %s · %s · FAILED %s' % (x.get('rc'), x.get('summary'), [f[:3] for f in x.get('failed_files', [])])
WHY = {
 '1337': ('KS-888 the KS 764 guard', '**T2 TEST-ONLY GUARD**: both copies of the security revoke pattern in the KS-764 guard widened to the revoke shape of the MERGED #1327 (whitespace, whole // lines, one `try {`). MEASURED: the PR == the held Spark patch (READY block == golden == checker patch.diff, sha256 34f81565ed609004; strict `git apply` at 215cc6875e2b gives the head blob; a context-line mutation refuses, a hunk-offset mutation still applies). EMULATED (READ): the new pattern matches security index.ts at develop, misses under all five broken-revoke arms, and the rejected loose window matches under all five; the CALL_SITES cell reds at develop and #1332\'s head, greens at #1337\'s head and END_TREE.'),
 '1332': ('KS-1054 round 2', '**T1 SCHEMA / START-UP, ROUND 2 of 2**: 038a creates the four CORE tables before 039; CORE-stage catches count; `error` set. **MEASURED by the drafter on a real PostgreSQL 18.3 over a unix socket, all three paths: 039 completes at the first boot / pass with the OAuth lookup and its policy (N-1332-1\'s function / policy half CLOSED; the arm "038a removed" brings it back) — BUT certifications ends RLS + FORCE with NO tenant_isolation policy on every head path, where the merge-base\'s bare database heals it at boot 2; an app role cannot INSERT into certifications at head (MEASURED), and can at the merge-base.** pg_dump -t: (i) == (ii); (iii) == develop\'s seeded path except charge_events (closed at head); bare != seeded for oauth_apps / svc_webhooks (docker/init\'s indexes + CHECK — pre-existing).'),
}
rows = []
for n in K['merge_order']:
    pr = P['prs'][n]
    files = ', '.join('%s +%s/-%s' % (os.path.basename(x.split('\t')[2]), x.split('\t')[0], x.split('\t')[1]) for x in pr['numstat'])
    rows.append('| #%s | %s | %s | `%s` | %d on `%s` | %s | %s | %s |' % (n, WHY[n][0], K['prs'][n]['tier'], pr['head'], len(pr['commits']), pr['merge_base'][:12], files, lands(n), WHY[n][1]))
out = ['# COMMISSION — DRAFT the round-39 batch gate kit "%s" over %d PRs (T2 + T1). Do NOT launch.' % (kit, len(K['prs'])), '',
 'Commissioned by Wednesday to the drafter on 2026-09-29 (~04:50 AEST) for Seat B 41st\'s queue (Secuura/Blockchain): #1337 (KS-888 / the KS 764 guard, TIER 2,',
 'test-only) and #1332 ROUND 2 of 2 (KS-1054, TIER 1, schema + start-up; a fast-forward of round 1 f5381338, gate38\'s NO GO). Develop 215cc6875e2b; END_TREE on the',
 'current develop with the orders proven; **MERGE ORDER #1337 FIRST** (#1332\'s branch still carries the pre-existing KS-764 guard red that #1337 fixes). Routing token',
 '`QA/Secuura-batch1337` (Wednesday adds the inbox_routing line). GO subject shape `GO (Seat B 41st): merge 1337 1332 on gate39`; the addendum one line per PR',
 '(`- #N · head <sha12> · subject: …`); own key only, no `(#n)`, declared + 8 <= 92. #1337\'s patch must equal the held Spark patch; packages/shared must go 1 failed /',
 '945 -> 945 / 945; the guard must still RED on a broken revoke (the brief-writer\'s arms). #1332: the gate MUST drive, on a real PostgreSQL over a unix socket (no',
 'TCP), the paths the seat did NOT — (i) a bare DB through the GATEWAY runner, booted twice; (ii) a bare DB through scripts/run-migrations.sh THEN a gateway boot;',
 '(iii) a docker/init-seeded DB then a gateway boot — on each: 039 recorded, the lookup function non-null, the oauth_apps_auth_lookup policy, tenant_isolation on',
 'the four tables, a second boot changes nothing; pg_dump --schema-only -t of the four tables byte-identical across (i), (ii), (iii) and develop\'s seeded path',
 '(filter pg_dump 18\'s \\restrict nonce); /health and /health/ready SERVED with the failed count and `error`, a CORE-stage throw counted. N-1332-5 and N-1332-4 are',
 'named, UNRAISED by ruling — not a NO GO this round. This is the LAST round under the 2-NO-GO cap. STANDING: the KS-764 red is pre-existing on develop and on',
 '#1332\'s branch and must be green on END after #1337; every suite that references a changed path is RUN (the guard\'s allowlist reads startup-migrations.ts; ks949,',
 'ks720, ks667, ks1071; the migrations directory\'s numbering). Check the seat\'s claim that 006 / 008 / 047 now succeed and that no other migration\'s behaviour',
 'changes because of 038a\'s lexical position.', '',
 '**DISK (Wednesday):** /Volumes/DevMASTER is FULL (~1.5 GiB free). The QA agent\'s clones, worktrees, `npm ci`, builds and Postgres data dirs go on the Data volume',
 '(its session scratchpad under /private/tmp/claude-501/), socket dirs a short `/tmp/q39g.*`; the report dir holds TEXT only; it STOPS on any ENOSPC (kit rule 56).', '',
 '## The batch — every head re-read by the drafter from origin (ls-remote + a fetch into a `--shared --no-checkout` scratch clone + the PULLS API; all agree), in MERGE ORDER',
 '| PR | ticket | tier | head | commits on merge-base | files | subject (no `(#n)`) | why this tier, from the DIFF |', '|---|---|---|---|---|---|---|---|'] + rows + ['',
 'Tiers per 0_Brain/learnings/2026-09-05_qa-gate-tiers-and-the-two-nogo-cap.md: T1 = security surfaces, data destruction and erasure, anything deploying to dev / demo; T2 = tests-only, docs, config/CI, follow-ups whose MECHANISM a prior gate measured.',
 'Linear: every PR links its ticket as `contributes`; none `closes` (linear_reads_1.out); no title, body or commit message carries a closing word before a key or a FOREIGN hyphenated key (keyscan_1.out).',
 'NOT STACKED (measured): no head is another\'s ancestor; TWO merge-bases. MG-11 as it LANDS: each title is the declared subject, WITHOUT the (#n) suffix (both <= 92).', '',
 '## Develop at the pin, and the orders',
 'Pinned over develop **`%s`** (tree `%s`), READ by ls-remote and fetched. Merge-bases MEASURED: %s. END_TREE **`%s`** (%s), identical in all %d orders (%d merge-tree calls, each with the PR\'s own merge-base).' % (
     P['develop'], P['develop_tree'], ', '.join('#%s `%s`' % (n, P['prs'][n]['merge_base'][:12]) for n in K['merge_order']), P['end_tree'], P['end_shortstat'], P['orders'], P['merge_tree_calls']),
 'THE ORDER (EMULATED guard state per intermediate develop, predict (d2)): ' + ' || '.join('%s: %s' % (o, ' -> '.join('%s tree %s %s' % (s['after'], s['tree'][:12], s['CALL_SITES_cell']) for s in st)) for o, st in P.get('order_proof', {}).items()),
 'The launch action\'s step 3b re-pins on any further move.', '',
 '## Overlaps — NONE declared, NONE found',
 '- Kit: two disjoint path sets. Every other OPEN PR at the pin (%d, the PULLS API census): disjoint from every kit path.' % len(P['inflight']),
 '- `merged_blob_paths` NONE and `noop_paths` NONE — two different declarations, each asserted empty by predict (c).', '',
 '## The drafter\'s real-Postgres drill (#1332; pgprobe_1.out, %s; unix socket only, 0 inet sockets; controls %s)' % (PG.get('engine', '?')[:40], 'ALL PASS' if all(PG['controls'].values()) else PG['controls']),
 '- Controls: merge-base bare boot 1 fails 039 (%s); round 1 bare boot 1 records 039 with the function ABSENT (%s); "038a removed" arm, boot 2: %s.' % (four('i base boot 1'), four('i r1 boot 1'), four('arm head-minus-038a boot 2')),
 '- Merge-base bare boot 2 (the healed reference): %s.' % four('i base boot 2'),
 '- (i) head bare -> gateway: boot 1 %s; boot 2 %s. Second boot changes: %s.' % (four('i head boot 1'), four('i head boot 2'), SUM.get('(i) head: a second boot changes nothing (whole schema) — else [the tables it changes, +/- lines]')),
 '- (ii) head bare -> run-migrations.sh (%s) -> gateway: boot 1 %s; boot 2 %s. Second boot changes: %s.' % (rm('ii head run-migrations pass 1'), four('ii head boot 1'), four('ii head boot 2'), SUM.get('(ii) head: a second boot changes nothing (whole schema) — else [the tables it changes, +/- lines]')),
 '- (iii) head docker/init -> gateway: boot 1 %s; boot 2 %s. Second boot changes: %s.' % (four('iii head boot 1'), four('iii head boot 2'), SUM.get('(iii) head: a second boot changes nothing (whole schema) — else [the tables it changes, +/- lines]')),
 '- develop seeded path (no 038a): boot 2 %s.' % four('dev boot 2'),
 '- Compose runner alone: merge-base pass 1 %s, pass 2 %s; head pass 1 %s, pass 2 %s.' % (rm('rm base pass 1'), rm('rm base pass 2'), rm('rm head pass 1'), rm('rm head pass 2')),
 '- pg_dump -t equality per table across (i) / (ii) / (iii) / develop seeded: %s; (i) == (ii): %s; (iii) == develop seeded: %s; merge-base bare end state == head (i): %s.' % (
     SUM.get("pg_dump -t of the four tables byte-identical across (i), (ii), (iii) and develop's seeded path — per table"), SUM.get('pg_dump -t: the two BARE paths (i) == (ii) per table'),
     SUM.get('pg_dump -t: the two SEEDED paths (iii) == (dev) per table'), SUM.get("pg_dump -t: the MERGE-BASE's bare end state (boot 2, CORE-created tables) == head (i) per table — so a bare-vs-seeded difference is PRE-EXISTING where True")),
 '- **AS AN APP ROLE (NOSUPERUSER NOBYPASSRLS, tenant GUC set, rolled back) — INSERT into certifications:** %s.' % SUM.get('AS AN APP ROLE (tenant GUC set): certifications INSERT+count per database — base bare boot 2 vs head (i) (ii) (iii) vs develop seeded'),
 '- CORE-stage throw on boot 2 (two-sided): head recorded %s; round 1 recorded %s.' % (json.dumps(R['ct head boot 2 CORE-THROW'].get('recorded')), json.dumps(R['i r1 boot 2 CORE-THROW'].get('recorded'))),
 '- /bin/sh glob order around 038a on this host: %s.' % PG.get('glob_order_this_host'), '',
 '## Fleet STOP (READ, bounded region, NOT-FOUND control)']
for n in K['merge_order']:
    s = S[n]
    if s.get('log') == 'ABSENT': out.append('- #%s: NO push log at drafting — UNREAD.' % n); continue
    out.append('- #%s `%s` (%d lines): %s · %s · %s · %s; "%s"' % (n, os.path.basename(s['log']), s['lines'], s['pre_push_hook_base'], s['fixture_guard'], s['run_shell_suites_region'], s['shell_suites'], s['verdict_line']))
out += ['- By path class no kit PR changes the count (no `*.test.sh`); #1332 adds 038a, which ks949_main_seed_idempotence.test.sh and run_migrations_failure_exit_code.test.sh execute — the gate runs both. After this merge 28/0 · 6/0 · 49/0 · 60 of 60.', '']
out += ['## LEGITIMATE SHAPES — the drafter\'s READ predictions (the gate MEASURES every row; a row saying MEASURED is a drafter\'s run, still not the gate\'s evidence)', '| PR | prediction | predicted-by |', '|---|---|---|']
for l in open(D + '/predict_1.out').read().splitlines():
    m = re.match(r'^  #(\d+) (.*)$', l)
    if m and not m.group(2).startswith(('PRODUCT files', 'NO product file')):
        out.append('| #%s | %s | drafter %s (predict_1.out) |' % (m.group(1), m.group(2).replace('|', '/')[:1500], 'MEASURED' if 'MEASURED' in m.group(2)[:160] else 'READ'))
open(D + '/COMMISSION.md', 'w').write('\n'.join(out) + '\n')
print('wrote', D + '/COMMISSION.md', len(out), 'lines')
