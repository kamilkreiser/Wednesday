#!/usr/bin/env python3
"""pgprobe_gate37.py <scratchpad> — the drafter's REAL-POSTGRES measurement for #1328 (KS-1335), the gate37 kit (kit.json and pins_gate37.json beside
this script; run AFTER predict_gate37.py). Every SQL text is EXTRACTED from the scratch clone (g37_sp/clone.git) at #1328's merge-base and at its head —
never typed here: the svc_teams_webhooks CREATE in api-gateway CORE_MIGRATIONS, the `svc_teams_webhooks schema alignment` DO block beside it, the CREATE
in docker/init/06-m365-tables.sql, and the notify route's SELECT (ORDER BY) and stamp UPDATE in m365-integration index.ts. They are handed to
pgprobe_gate37.mjs, which runs them on PGlite (the Postgres engine in-process: no socket, no port, no container; never the native :5432). Measures:
A/A2 migration idempotence (runs twice), B the upgrade of an existing deployment (rows kept byte-equal, the new column NULL), C the rotation with real
rows (head vs the merge-base ORDER BY as the control), D the deadline-SKIPPED rows stay NULL and lead the next call, E the head's route SQL on an
UNMIGRATED schema (the deploy-order hazard), F the stamp UPDATE's in-process cost (a LOWER BOUND: no network). Controls CT1-CT3 inside the .mjs.
Writes pgprobe_gate37.json beside this script; prints a summary. Usage: pgprobe_gate37.py <scratchpad>"""
import json, os, re, subprocess, sys
G = os.path.dirname(os.path.abspath(__file__)); K = json.load(open(os.path.join(G, 'kit.json'), encoding='utf-8'))
P = json.load(open(os.path.join(G, 'pins_%s.json' % K['kit']), encoding='utf-8'))
CL = os.path.join(sys.argv[1], 'g37_sp', 'clone.git')
SM, INIT, M365 = 'Blockchain/Dev/services/api-gateway/src/startup-migrations.ts', 'Blockchain/Dev/docker/init/06-m365-tables.sql', 'Blockchain/Dev/services/m365-integration/src/index.ts'
def show(rev, p): return subprocess.run(['git', '--git-dir', CL, 'show', '%s:%s' % (rev, p)], capture_output=True, text=True, check=True).stdout
def one(rx, t, what):
    m = re.findall(rx, t, re.S)
    if len(m) != 1: print('REFUSING: %s matched %d times (want exactly 1)' % (what, len(m))); sys.exit(1)
    return m[0]
def extract(rev):
    sm, init, m = show(rev, SM), show(rev, INIT), show(rev, M365)
    return {'core_create': one(r'`(CREATE TABLE IF NOT EXISTS svc_teams_webhooks \(.*?\))`', sm, 'CORE CREATE svc_teams_webhooks @' + rev[:12]),
            'do_block': one(r'// svc_teams_webhooks schema alignment[^\n]*\n\s*`(DO \$\$ BEGIN.*?END \$\$)`', sm, 'the schema-alignment DO block @' + rev[:12]),
            'init_create': one(r'(CREATE TABLE IF NOT EXISTS svc_teams_webhooks \(.*?\);)', init, 'init 06 CREATE @' + rev[:12]),
            'select': one(r'`(SELECT \* FROM svc_teams_webhooks WHERE is_active = true AND events::jsonb \? \$1.*?LIMIT \$2)`', m, 'the notify SELECT @' + rev[:12]),
            'update': one(r"'(UPDATE svc_teams_webhooks SET last_attempted_at = NOW\(\) WHERE id = \$1)'", m, 'the stamp UPDATE @' + rev[:12]) if 'SET last_attempted_at' in m else None}
pr = P['prs']['1328']
X = {'base': extract(pr['merge_base']), 'head': extract(pr['head'])}
if os.environ.get('G37_PG_DUMP'): json.dump(X, open(os.environ['G37_PG_DUMP'], 'w'))   # debugging only: the extracted SQL, to a path the caller names
assert X['base']['update'] is None and X['head']['update'], 'the stamp UPDATE must be ABSENT at the merge-base and PRESENT at the head'
print('pgprobe_gate37 | #1328 merge-base %s head %s | extracted: %s' % (pr['merge_base'][:12], pr['head'][:12], {k: {kk: len(vv or '') for kk, vv in v.items()} for k, v in X.items()}))
print('  ORDER BY at the merge-base: %r | at head: %r' % (re.search(r'ORDER BY[^\n]*', X['base']['select']).group(0), re.search(r'ORDER BY[^\n]*', X['head']['select']).group(0)))
r = subprocess.run(['node', os.path.join(G, 'pgprobe_gate37.mjs')], input=json.dumps(X), capture_output=True, text=True, timeout=600)
# PGlite's WASM runtime sets its own exit status at teardown (a bare select-1 script exits 100, MEASURED): the rc is REPORTED, and the verdict is the ONE
# JSON line the .mjs prints LAST (after process.exitCode = 0) — absent that line, this refuses
js = [l for l in r.stdout.strip().splitlines() if l.startswith('{')]
print('  node rc %d (reported, not the verdict); stdout JSON lines %d; stderr tail %r' % (r.returncode, len(js), r.stderr.strip()[-300:]))
if not js: print('REFUSING: the probe printed no JSON result'); sys.exit(1)
res = json.loads(js[-1]); res['_extracted_from'] = {'merge_base': pr['merge_base'], 'head': pr['head']}
json.dump(res, open(os.path.join(G, 'pgprobe_gate37.json'), 'w'), indent=1)
print('  engine: %s' % res['engine'])
for k, v in res['runs'].items(): print('  %s: %s' % (k, json.dumps(v)))
print('  controls: %s' % res['controls'])
A, B, C, D, E, F = (res['runs'][k] for k in ('A_fresh_head_twice', 'B_upgrade_existing_rows', 'C_rotation: head ORDER BY last_attempted_at', 'D_skipped_stays_null', 'E_head_route_sql_on_unmigrated_schema', 'F_update_cost_inprocess'))
CC = res['runs']['C_rotation: CONTROL merge-base ORDER BY last_sent_at']
summ = {'idempotent (every step ok, twice)': all(s[1] == 'ok' for s in A['steps']) and all(s[1] == 'ok' for s in res['runs']['A2_core_only_head_twice']['steps']),
        'upgrade keeps rows byte-equal, new column NULL on all': B['rows_kept_byte_equal'] and B['last_attempted_at_null_rows'] == B['rows_signature_after']['n'] and not B['column_before'] and bool(B['column_after']),
        'head rotates past a failing block (call 2 reaches the 5 starved)': len(C['starved_reached_in_call2']) == 5 and not C['call2_equals_call1'],
        'control (merge-base ORDER BY) starves (call 2 == call 1)': CC['call2_equals_call1'] and not CC['starved_reached_in_call2'],
        'skipped rows stay NULL and lead call 2': D['skipped_still_null'] == D['skipped'] and D['call2_first15_are_the_skipped'],
        'head route SQL on an UNMIGRATED schema errors': E['select'].startswith('ERROR') and E['update'].startswith('ERROR'),
        'controls all behaved': all(res['controls'].values())}
print('SUMMARY %s | stamp UPDATE in-process median %s ms, p95 %s ms (%d timed) — a LOWER BOUND, no network | E: select %s' % (summ, F['median_ms'], F['p95_ms'], F['updates'], E['select'][:60]))
res['_summary'] = summ; json.dump(res, open(os.path.join(G, 'pgprobe_gate37.json'), 'w'), indent=1)
sys.exit(0 if all(summ.values()) else 1)
