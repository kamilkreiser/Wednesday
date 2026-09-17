#!/usr/bin/env python3
"""drafter_hang_1034.py TREE... — the cache-get-throws LEAD, measured on a REAL node process (tsx), not under vitest. Per tree x NODE_ENV {test, production}
x UNHANDLED_REJECTION_MODE {unset (= 'exit', resolveUnhandledRejectionMode's default), survive (compose/bicep's value, READ)}:
  R1 OK key -> expect 200 + 1 upstream hit (and PATCHED-GET ok: same-instance control)
  R2 cachethrow key (the instrument) -> response? (client timeout 5 s)
  wait 1.5 s: child alive? exit code?
  R3 OK key (new) -> served / refused (ECONNREFUSED) / no response
  R4 GET /health
Then the child is ended by its VERIFIED pid (SIGTERM; never pid 1, never a pattern), waited, and the LISTEN census for its pid re-read.
The harness lives at <tree>/Blockchain/Dev/qa_hang_1034/ (OUTSIDE services/api-gateway) and is MOVED to WORKDIR/_quarantine after. Never rm; stderr kept."""
import subprocess, os, json, sys, datetime, time, shutil, signal, uuid, http.client, select
GSD = os.path.dirname(os.path.abspath(__file__)); OUTD = GSD + '/out'; os.makedirs(OUTD + '/hang', exist_ok=True)
PA = json.load(open(GSD + '/drafter_paths.json')); W = PA['W']; T = PA['trees']
GW = 'Blockchain/Dev/services/api-gateway'
def ts(): return datetime.datetime.now().astimezone().strftime('%H:%M:%S.%f')[:-3] + datetime.datetime.now().astimezone().strftime(' %Z')
def P(*a): print(' '.join(str(x) for x in a), flush=True)
def req(port, path, headers, timeout=5.0):
    try:
        c = http.client.HTTPConnection('127.0.0.1', port, timeout=timeout); c.request('GET', path, headers=headers); r = c.getresponse(); b = r.read()[:160]; c.close()
        return 'HTTP %d %s' % (r.status, b.decode('utf-8', 'replace').replace('\n', ' ')[:100])
    except Exception as e:
        return 'NO-RESPONSE/ERR %s: %s' % (type(e).__name__, str(e)[:80])
PROD = {'CSRF_SECRET': 'qa1034-drafter-stub-not-a-secret', 'DATABASE_URL': 'postgres://qa:qa@127.0.0.1:1/qa', 'REDIS_URL': 'redis://127.0.0.1:1', 'ENABLE_TEST_TOKENS': '', 'ENABLE_MOCK_ENDPOINTS': '', 'RATE_LIMIT_MAX_REQUESTS': '100000'}
summary = []
for tree in sys.argv[1:]:
    D = T[tree] + '/Blockchain/Dev/qa_hang_1034'; os.makedirs(D)
    # run 1 wrote harness.cts: tsx did not transform the required index.ts (ESM translator), nothing booted; run 2's patch commented out the write (empty harness)
    hf = D + '/harness.ts'; open(hf, 'w').write(open(GSD + '/src/qa1034-hang-harness.template.cts').read().replace('__GW_SRC__', T[tree] + '/' + GW + '/src'))
    assert os.path.getsize(hf) > 1000, 'harness empty'
    try:
        for nodeenv in ('test', 'production'):
            for mode in ('(unset)', 'survive'):
                tag = '%s_%s_%s' % (tree, nodeenv, 'unset' if mode == '(unset)' else mode)
                env = {k: v for k, v in os.environ.items() if k not in ('NODE_ENV', 'UNHANDLED_REJECTION_MODE')}
                env['NODE_ENV'] = nodeenv
                if nodeenv == 'production': env.update(PROD)
                if mode != '(unset)': env['UNHANDLED_REJECTION_MODE'] = mode
                outf = open(OUTD + '/hang/%s.stdout' % tag, 'w+'); errf = open(OUTD + '/hang/%s.stderr' % tag, 'w+')
                t0 = time.time()
                ch = subprocess.Popen(['node', T[tree] + '/Blockchain/Dev/node_modules/tsx/dist/cli.mjs', hf], cwd=D, env=env, stdout=outf, stderr=errf)
                ready = None
                while time.time() - t0 < 90 and ch.poll() is None:
                    outf.flush(); txt = open(OUTD + '/hang/%s.stdout' % tag).read()
                    for line in txt.splitlines():
                        if line.startswith('READY '): ready = json.loads(line[6:])
                    if ready: break
                    time.sleep(0.3)
                row = dict(tag=tag, boot_s=round(time.time() - t0, 1), ready=ready, child_pid=ch.pid, early_exit=ch.poll())
                if ready:
                    assert ready['pid'] > 1
                    port = ready['port']; pre = '/api/v1' if nodeenv == 'production' else '/api'  # run 3 used /api in production: 307 before auth
                    row['R1_ok_key'] = req(port, pre + '/credentials/qa1034h', {'x-api-key': 'sk_qa1034h_ok_' + uuid.uuid4().hex}); row['R1_t'] = ts()
                    row['R2_cachethrow_key'] = req(port, pre + '/credentials/qa1034h', {'x-api-key': 'sk_qa1034h_cachethrow_' + uuid.uuid4().hex}); row['R2_t'] = ts()
                    time.sleep(1.5)
                    row['alive_after_R2'] = ch.poll() is None; row['exit_after_R2'] = ch.poll()
                    row['R3_ok_key_after'] = req(port, pre + '/credentials/qa1034h', {'x-api-key': 'sk_qa1034h_ok_' + uuid.uuid4().hex}); row['R3_t'] = ts()
                    row['R4_health'] = req(port, '/health', {})
                    row['alive_at_end'] = ch.poll() is None
                if ch.poll() is None:
                    pid = ch.pid; assert pid > 1
                    os.kill(pid, signal.SIGTERM); row['sigterm_pid'] = pid
                    try: ch.wait(timeout=40)
                    except subprocess.TimeoutExpired: row['still_alive_after_sigterm_40s'] = True
                row['final_exit'] = ch.poll()
                gp = (ready or {}).get('pid')
                if gp and gp > 1:
                    alive = subprocess.run(['kill', '-0', str(gp)], capture_output=True).returncode == 0
                    row['gateway_pid'] = gp; row['gateway_pid_alive_after_parent_exit'] = alive
                    if alive:
                        os.kill(gp, signal.SIGTERM); time.sleep(2); row['gateway_pid_alive_after_sigterm'] = subprocess.run(['kill', '-0', str(gp)], capture_output=True).returncode == 0
                    ls2 = subprocess.run(['lsof', '-nP', '-a', '-p', str(gp), '-iTCP', '-sTCP:LISTEN'], capture_output=True, text=True)
                    row['listen_rows_for_gateway_pid_after'] = len([l for l in ls2.stdout.splitlines()[1:] if l.strip()])
                ls = subprocess.run(['lsof', '-nP', '-a', '-p', str(ch.pid), '-iTCP', '-sTCP:LISTEN'], capture_output=True, text=True)
                row['listen_rows_for_child_pid_after'] = len([l for l in ls.stdout.splitlines()[1:] if l.strip()])
                outf.flush(); errf.flush()
                so = open(OUTD + '/hang/%s.stdout' % tag).read(); se = open(OUTD + '/hang/%s.stderr' % tag).read()
                row['stdout_markers'] = [l[:140] for l in so.splitlines() if l.startswith(('PATCHED-GET', 'UPSTREAM-HIT', 'EXIT'))]
                row['stderr_markers'] = [l[:220] for l in (so + '\n' + se).splitlines() if any(k in l for k in ('nhandled', 'UNHANDLED', 'shutdown', 'Shutdown', 'Forcing exit', 'unhandledRejection mode', 'qa1034 instrument'))][:12]
                P(json.dumps(row)); summary.append(row)
    finally:
        q = W + '/_quarantine'; os.makedirs(q, exist_ok=True); dst = q + '/qa_hang_1034.%s.%s' % (tree, datetime.datetime.now().strftime('%H%M%S')); shutil.move(D, dst); P('harness dir MOVED to', dst.split('/')[-1])
json.dump(summary, open(OUTD + '/hang_rows.json', 'w'), indent=1)
