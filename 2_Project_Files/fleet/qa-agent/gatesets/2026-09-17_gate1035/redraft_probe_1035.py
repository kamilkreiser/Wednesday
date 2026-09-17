#!/usr/bin/env python3
"""redraft_probe_1035.py TREE... — (derived from the dead drafter's drafter_probe_1035.py by asserted substitutions; r2: PRODUCTION census through /api/v1/documents with an
`application/vnd.qa1035+json` Content-Type — an INSTRUMENT: it passes enforceJsonContentType (application/*+json) but express.json (type application/json) does not consume
the stream, so the hand-parsing create route answers; control rows: the same request as application/json never answers (pre-existing, #1034 drafter item 7), /api/documents 307)
the REAL-app allow-list census for #1035 (KS-1204), per tree x NODE_ENV {test, production}, as a real node process (tsx).
Harness: src/qa1035-allowlist-harness.template.ts written to <tree>/Blockchain/Dev/qa_probe_1035/harness.ts (OUTSIDE services/api-gateway), MOVED to
WORKDIR/_quarantine after (never rm). Plan steps (all through the REAL routes):
  A. ONE SYSTEM_ADMIN PUT /api/admin/settings storing 20 connector configs (every allowedDocumentTypes shape below), then POST /api/documents under
     each connector's sk_ key x 12 bodies; GET /api/connector/info per connector (what the connector is TOLD).
  B. CONTAINER shapes (each its own PUT, then 3 creates under connector c-cont): integrations as an index-keyed OBJECT (what the portal Settings page
     writes back), a null entry before the real one, a duplicate id (unrestricted entry first), config a string, integrations null.
  C. the admin writer itself: PUT as SYSTEM_ADMIN / ORG_ADMIN / ISSUER_ADMIN / issuer (control 403) / no auth (control 401), each storing a STRING list.
  D. the portal Settings round-trip: store a good array list, create (control 403), GET -> Settings.tsx save transform -> PUT, create again.
Array-like OBJECT {0,length} is run in a SEPARATE child per tree x NODE_ENV x UNHANDLED_REJECTION_MODE {unset, survive}: at develop it is predicted to
THROW inside the async create handler. Every child ended by its VERIFIED pid (never pid 1, never a pattern); LISTEN rows for it re-read. Never rm."""
import subprocess, os, json, sys, datetime, time, shutil, signal
GSD = os.path.dirname(os.path.abspath(__file__)); OUTD = GSD + '/out/r2'; os.makedirs(OUTD + '/probe', exist_ok=True)
PA = json.load(open(OUTD + '/paths.json')); W = PA['W']; T = PA['trees']
GW = 'Blockchain/Dev/services/api-gateway'
def now(): return datetime.datetime.now().astimezone().strftime('%H:%M:%S %Z')
def P(*a): print(' '.join(str(x) for x in a), flush=True)
S, D = 'SSD_DOCUMENT', 'DOCUMENT'
CONFIGS = [  # label, connector id, stored config (None = the allowedDocumentTypes key ABSENT), named set N (what the stored value names)
  ('ABSENT', 'c-absent', None, 'UNRESTRICTED'), ('null', 'c-null', ['__NULL__'], 'UNRESTRICTED'), ('[]', 'c-emptyarr', [[]], 'UNRESTRICTED'),
  ('["SSD_DOCUMENT"]', 'c-arr-ssd', [[S]], [S]), ('["DOCUMENT","SSD_DOCUMENT"]', 'c-arr-two', [[D, S]], [D, S]),
  ('"SSD_DOCUMENT"', 'c-str-ssd', ['SSD_DOCUMENT'], [S]), ('""', 'c-str-empty', [''], []), ("'[\"SSD_DOCUMENT\"]' (JSON-looking string)", 'c-str-json', ['["SSD_DOCUMENT"]'], [S]),
  ('"SSD_DOCUMENT,PROPERTY_DEED" (CSV string)', 'c-str-csv', ['SSD_DOCUMENT,PROPERTY_DEED'], [S, 'PROPERTY_DEED']),
  ('{}', 'c-obj-empty', [{}], []), ('{0:"SSD_DOCUMENT"}', 'c-obj-idx', [{'0': S}], [S]), ('{"SSD_DOCUMENT":true}', 'c-obj-keyed', [{S: True}], [S]),
  ('0', 'c-num-0', [0], []), ('1', 'c-num-1', [1], []), ('false', 'c-bool-false', [False], []), ('true', 'c-bool-true', [True], []),
  ('[123]', 'c-arr-num', [[123]], []), ('[["SSD_DOCUMENT"]]', 'c-arr-nested', [[[S]]], []), ('["SSD_DOCUMENT",5,null]', 'c-arr-mixed', [[S, 5, None]], [S]),
  ('[{"code":"SSD_DOCUMENT"}]', 'c-arr-obj', [[{'code': S}]], []),
]
ARRAYLIKE = ('{0:"SSD_DOCUMENT",length:1} (array-like object)', 'c-obj-arraylike', [{'0': S, 'length': 1}], [S])
BODIES = [('untyped', {}), ('dt:SSD_DOCUMENT', {'documentType': S}), ('ty:SSD_DOCUMENT', {'type': S}), ('dt:DOCUMENT', {'documentType': D}), ('ty:DOCUMENT', {'type': D}),
          ('dt:PROPERTY_DEED', {'documentType': 'PROPERTY_DEED'}), ('both dt:SSD ty:DOC', {'documentType': S, 'type': D}), ('both dt:DOC ty:SSD', {'documentType': D, 'type': S}),
          ('ty:123 (number)', {'type': 123}), ("dt:'SSD' (substring of SSD_DOCUMENT)", {'documentType': 'SSD'}), ("dt:'[\"SSD_DOCUMENT\"]'", {'documentType': '["SSD_DOCUMENT"]'}),
          ("dt:['SSD_DOCUMENT'] (array)", {'documentType': [S]})]
def cfg_entry(cid, stored):
    if stored is None: return {'id': cid, 'config': {'name': cid}}
    v = stored[0]
    return {'id': cid, 'config': {'name': cid, 'allowedDocumentTypes': None if v == '__NULL__' else v}}
def census_plan(configs):
    steps = [{'kind': 'put', 'label': 'A store %d connector configs' % len(configs), 'as': 'SYSTEM_ADMIN', 'body': {'integrations': [cfg_entry(c[1], c[2]) for c in configs]}}]
    for lab, cid, stored, named in configs:
        for sid, b in BODIES: steps.append({'kind': 'create', 'group': 'A', 'config_label': lab, 'connector': cid, 'shape': sid, 'body': b})
        steps.append({'kind': 'info', 'config_label': lab, 'connector': cid})
    return steps
def container_plan():
    good = {'id': 'c-cont', 'config': {'allowedDocumentTypes': [S]}}
    V = [('B integrations = index-keyed OBJECT {"0": entry}', {'integrations': {'0': good}}),
         ('B integrations = [null, entry]', {'integrations': [None, good]}),
         ('B integrations = [unrestricted duplicate id, entry]', {'integrations': [{'id': 'c-cont', 'config': {}}, good]}),
         ('B integrations = [entry with config a STRING]', {'integrations': [{'id': 'c-cont', 'config': 'SSD_DOCUMENT'}]}),
         ('B integrations = null', {'integrations': None}),
         ('B control integrations = [entry]', {'integrations': [good]})]
    steps = []
    for lab, body in V:
        steps.append({'kind': 'put', 'label': lab, 'as': 'SYSTEM_ADMIN', 'body': body})
        for sid, b in (BODIES[1], BODIES[3], BODIES[0]): steps.append({'kind': 'create', 'group': 'B', 'config_label': lab, 'connector': 'c-cont', 'shape': sid, 'body': b})
    for role in ('SYSTEM_ADMIN', 'ORG_ADMIN', 'ISSUER_ADMIN', 'issuer', 'none'):
        steps.append({'kind': 'put', 'label': 'C admin write of a STRING allow-list as ' + role, 'as': role, 'body': {'integrations': [{'id': 'c-w-' + role.lower(), 'config': {'allowedDocumentTypes': 'SSD_DOCUMENT'}}]}})
    steps.append({'kind': 'put', 'label': 'D store a good ARRAY list + general', 'as': 'SYSTEM_ADMIN', 'body': {'integrations': [{'id': 'c-portal', 'config': {'allowedDocumentTypes': [S]}}], 'general': {'platformName': 'Secuura'}}})
    steps.append({'kind': 'create', 'group': 'D', 'config_label': 'D before portal save (array list)', 'connector': 'c-portal', 'shape': 'dt:DOCUMENT', 'body': {'documentType': D}})
    steps.append({'kind': 'portal-roundtrip', 'label': 'D portal Settings save, one edit general.platformName', 'edits': {'general.platformName': 'Secuura QA'}})
    steps.append({'kind': 'create', 'group': 'D', 'config_label': 'D after portal save', 'connector': 'c-portal', 'shape': 'dt:DOCUMENT', 'body': {'documentType': D}})
    steps.append({'kind': 'create', 'group': 'D', 'config_label': 'D after portal save', 'connector': 'c-portal', 'shape': 'dt:SSD_DOCUMENT', 'body': {'documentType': S}})
    return steps
PROD = {'CSRF_SECRET': 'qa1035-redrafter-stub-not-a-secret', 'DATABASE_URL': 'postgres://qa:qa@127.0.0.1:1/qa', 'REDIS_URL': 'redis://127.0.0.1:1', 'ENABLE_DEMO_SEED': 'true'}
def child(tree, D_, nodeenv, mode, plan, tag):
    pf = D_ + '/plan_%s.json' % tag; rf = OUTD + '/probe/rows_%s.json' % tag; json.dump({'steps': plan}, open(pf, 'w'))
    env = {k: v for k, v in os.environ.items() if k not in ('NODE_ENV', 'UNHANDLED_REJECTION_MODE', 'ENABLE_TEST_TOKENS', 'ENABLE_MOCK_ENDPOINTS')}
    env.update({'NODE_ENV': nodeenv, 'QA_PLAN': pf, 'QA_ROWS': rf, 'RATE_LIMIT_MAX_REQUESTS': '1000000'})
    if nodeenv == 'production': env.update(PROD)
    if mode != '(unset)': env['UNHANDLED_REJECTION_MODE'] = mode
    so, se = OUTD + '/probe/%s.stdout' % tag, OUTD + '/probe/%s.stderr' % tag
    outf = open(so, 'w'); errf = open(se, 'w'); t0 = time.time()
    ch = subprocess.Popen(['node', T[tree] + '/Blockchain/Dev/node_modules/tsx/dist/cli.mjs', D_ + '/harness.ts'], cwd=D_, env=env, stdout=outf, stderr=errf)
    ready = None; done = False
    while time.time() - t0 < 300 and ch.poll() is None:
        txt = open(so).read()
        for line in txt.splitlines():
            if line.startswith('READY '): ready = json.loads(line[6:])
            if line.startswith('DONE '): done = True
        if done: break
        time.sleep(0.4)
    row = dict(tag=tag, secs=round(time.time() - t0, 1), ready=ready, done=done, child_pid=ch.pid, exited_before_done=ch.poll())
    time.sleep(0.5); row['alive_after_plan'] = ch.poll() is None
    if ch.poll() is None:
        assert ch.pid > 1; os.kill(ch.pid, signal.SIGTERM); row['sigterm_pid'] = ch.pid
        try: ch.wait(timeout=40)
        except subprocess.TimeoutExpired: row['still_alive_after_sigterm_40s'] = True
    row['final_exit'] = ch.poll()
    gp = (ready or {}).get('pid')
    for pid in {ch.pid, gp} - {None}:
        if pid > 1 and subprocess.run(['kill', '-0', str(pid)], capture_output=True).returncode == 0:
            os.kill(pid, signal.SIGTERM); time.sleep(2); row['pid_%d_alive_after_sigterm' % pid] = subprocess.run(['kill', '-0', str(pid)], capture_output=True).returncode == 0
        ls = subprocess.run(['lsof', '-nP', '-a', '-p', str(pid), '-iTCP', '-sTCP:LISTEN'], capture_output=True, text=True)
        row['listen_rows_pid_%d_after' % pid] = len([l for l in ls.stdout.splitlines()[1:] if l.strip()])
    txt = open(so).read() + '\n' + open(se).read()
    row['markers'] = [l[:260] for l in txt.splitlines() if any(k in l for k in ('nhandled', 'UNHANDLED', 'Graceful shutdown', 'EXIT ', 'FATAL', 'TypeError', 'is not a function'))][:10]
    row['rows_file'] = os.path.exists(rf)
    P(now(), json.dumps(row))
    return row
if __name__ == '__main__':
    summary = []
    for tree in sys.argv[1:]:
        D_ = T[tree] + '/Blockchain/Dev/qa_probe_1035'; os.makedirs(D_)
        hf = D_ + '/harness.ts'; tpl = open(GSD + '/src/qa1035-allowlist-harness.r2.template.ts').read(); assert tpl.count('__GW_SRC__') == 3  # 1 in the header comment + 2 requires (run 1 asserted 2 and stopped before any child)
        open(hf, 'w').write(tpl.replace('__GW_SRC__', T[tree] + '/' + GW + '/src')); assert os.path.getsize(hf) > 3000
        try:
            XJ = 'application/vnd.qa1035+json'
            def with_ctype(steps, ct):
                return [dict(s_, ctype=ct) if s_['kind'] == 'create' else s_ for s_ in steps]
            PATHCTL = [{'kind': 'put', 'label': 'P store ["SSD_DOCUMENT"] for c-arr-ssd', 'as': 'SYSTEM_ADMIN', 'body': {'integrations': [cfg_entry('c-arr-ssd', [[S]])]}},
                       {'kind': 'create', 'group': 'P', 'config_label': 'path control /api/documents (json)', 'connector': 'c-arr-ssd', 'shape': 'dt:SSD_DOCUMENT', 'body': {'documentType': S}, 'path': '/api/documents'},
                       {'kind': 'create', 'group': 'P', 'config_label': 'path control /api/v1/documents (json)', 'connector': 'c-arr-ssd', 'shape': 'dt:SSD_DOCUMENT', 'body': {'documentType': S}, 'path': '/api/v1/documents', 'tmo': 3000},
                       {'kind': 'create', 'group': 'P', 'config_label': 'path control /api/v1/documents (+json instrument)', 'connector': 'c-arr-ssd', 'shape': 'dt:SSD_DOCUMENT', 'body': {'documentType': S}, 'path': '/api/v1/documents', 'ctype': XJ},
                       {'kind': 'create', 'group': 'P', 'config_label': 'path control /api/documents (+json instrument)', 'connector': 'c-arr-ssd', 'shape': 'dt:SSD_DOCUMENT', 'body': {'documentType': S}, 'path': '/api/documents', 'ctype': XJ}]
            summary.append(child(tree, D_, 'test', 'survive', census_plan(CONFIGS) + container_plan() + PATHCTL, '%s_test_census' % tree))
            summary.append(child(tree, D_, 'production', 'survive', with_ctype(census_plan(CONFIGS) + container_plan(), XJ) + PATHCTL, '%s_production_census' % tree))
            al = [{'kind': 'put', 'label': 'arraylike store', 'as': 'SYSTEM_ADMIN', 'body': {'integrations': [cfg_entry(ARRAYLIKE[1], ARRAYLIKE[2]), cfg_entry('c-arr-ssd', [[S]])]}},
                  {'kind': 'create', 'group': 'AL', 'config_label': ARRAYLIKE[0], 'connector': ARRAYLIKE[1], 'shape': 'dt:DOCUMENT', 'body': {'documentType': D}, 'ctype': XJ},
                  {'kind': 'create', 'group': 'AL', 'config_label': 'after: control connector ["SSD_DOCUMENT"]', 'connector': 'c-arr-ssd', 'shape': 'dt:SSD_DOCUMENT', 'body': {'documentType': S}, 'ctype': XJ}]
            for ne in ('test', 'production'):
                for mode in ('(unset)', 'survive'):
                    summary.append(child(tree, D_, ne, mode, al, '%s_%s_arraylike_%s' % (tree, ne, 'unset' if mode == '(unset)' else mode)))
        finally:
            q = W + '/_quarantine'; os.makedirs(q, exist_ok=True); dst = q + '/qa_probe_1035.%s.%s' % (tree, datetime.datetime.now().strftime('%H%M%S')); shutil.move(D_, dst); P('harness dir MOVED to', dst.split('/')[-1])
    json.dump(summary, open(OUTD + '/probe/children.json', 'w'), indent=1)
    json.dump({'configs': [(c[0], c[1], c[3]) for c in CONFIGS] + [(ARRAYLIKE[0], ARRAYLIKE[1], ARRAYLIKE[3])], 'bodies': [b[0] for b in BODIES]}, open(OUTD + '/probe/universe.json', 'w'), indent=1)
