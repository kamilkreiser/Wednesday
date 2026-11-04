"""G189 mutants. Each mutant: one exact textual replacement (asserted to match once) in the committed head file,
run the G189 matrix, compare to head's matrix (killed = any cell differs) and to base (looser cells), restore."""
import json, os, re, subprocess, sys, shutil

W = '/Volumes/DevMASTER/WEDNESDAY/0_Brain/reference/2026-11-04_gate189-ks1256-pr2001'
G = W + '/repo/Blockchain/Dev/services/api-gateway'
VT = W + '/repo/Blockchain/Dev/node_modules/.bin/vitest'
S = G + '/src/services/settingsStore.ts'
V = G + '/src/routes/verification.ts'
H = G + '/src/services/health.ts'
A = G + '/src/routes/admin.ts'

MUTANTS = [
  ('M1_store_miss_unreadable_reads_empty', S,
   "    return { kind: 'unreadable', reason: stored.reason };",
   "    return { kind: 'present', settings: {}, source: 'db' };"),
  ('M2_create_unreadable_503_dropped', V,
   "        if (settingsUnreadable) {\n          res.status(503)",
   "        if (false && settingsUnreadable) {\n          res.status(503)"),
  ('M3_info_unreadable_503_dropped', H,
   "    if (settingsUnreadable) {\n      res.status(503)",
   "    if (false && settingsUnreadable) {\n      res.status(503)"),
  ('M4_row_missing_reads_empty', S,
   "    if (!r.rows.length) return { ok: false, reason: 'db-row-missing' };",
   "    if (!r.rows.length) return { ok: true, settings: {} };"),
  ('M5_not_object_guard_removed', S,
   "    if (!isPlainObject(settings)) return { ok: false, reason: 'db-row-not-an-object' };",
   "    if (settings === null) return { ok: false, reason: 'db-row-not-an-object' };"),
  ('M6_db_read_failure_reads_empty', S,
   "    return { ok: false, reason: 'db-read-failed', errorClass: errorClass(err) };",
   "    return { ok: true, settings: {} as Record<string, unknown> };"),
  ('M7_admin_db_write_failure_ignored', A,
   "    if (!stored.ok) {\n      warn('Platform settings could not be stored",
   "    if (false && !stored.ok) {\n      warn('Platform settings could not be stored"),
  ('M8_admin_redis_before_db', A,
   "    const stored = await writeStoredSettings(settingsDb, merged);",
   "    await redisService.setNotificationSettings('platform-settings', merged);\n    const stored = await writeStoredSettings(settingsDb, merged);"),
]

def load(p):
    return {(r['reader'], r['redis'], r['key'], r['row']): r for r in map(json.loads, open(p))}

head = load(W + '/runs/matrix_head.jsonl')
os.makedirs(W + '/runs/mut', exist_ok=True)
rows = []
for name, path, old, new in MUTANTS:
    src = open(path).read()
    n = src.count(old)
    if n != 1:
        rows.append((name, 'NOT APPLIED (matches=%d)' % n, '', '')); continue
    bak = W + '/scratch/mutbak_' + os.path.basename(path)
    shutil.copyfile(path, bak)
    try:
        open(path, 'w').write(src.replace(old, new))
        out = W + '/runs/mut/%s.jsonl' % name
        env = {'PATH': '/opt/homebrew/bin:/usr/bin:/bin', 'HOME': W + '/home', 'TMPDIR': W + '/tmp', 'G189_OUT': out}
        r = subprocess.run([VT, 'run', '--root', G, '--config', G + '/vitest.config.ts', '--dangerouslyIgnoreUnhandledErrors',
                            'src/__tests__/g189-matrix.test.ts'], cwd=W + '/cwd', env=env, capture_output=True, text=True, timeout=600)
        open(W + '/runs/mut/%s.log' % name, 'w').write(r.stdout[-20000:] + r.stderr[-20000:])
        if r.returncode != 0 or not os.path.exists(out):
            rows.append((name, 'RUN FAILED rc=%d' % r.returncode, '', '')); continue
        t = subprocess.run([VT, 'run', '--root', G, '--config', G + '/vitest.config.ts',
                            'src/__tests__/ks1256-a-missing-settings-key-reads-the-stored-record.test.ts',
                            'src/__tests__/ks1256-settings-store-statements-on-a-real-engine.test.ts'],
                           cwd=W + '/cwd', env=env, capture_output=True, text=True, timeout=600)
        open(W + '/runs/mut/%s.prtests.log' % name, 'w').write(t.stdout[-30000:] + t.stderr[-10000:])
        tl = [l for l in re.sub(r'\x1b\[[0-9;]*m', '', t.stdout).splitlines() if 'Tests ' in l]
        prt = 'PR-tests rc=%d %s' % (t.returncode, tl[-1].strip() if tl else '?')
        m = load(out)
        diff = [k for k in head if json.dumps(head[k], sort_keys=True) != json.dumps(m[k], sort_keys=True)]
        j = subprocess.run(['python3', '-I', W + '/harness/judge.py', W + '/runs/matrix_base.jsonl', out], capture_output=True, text=True).stdout
        loose = j.split('LOOSER (ratio cells): ')[1].split('\n')[0]
        rows.append((name, 'KILLED' if diff else 'SURVIVED', len(diff), 'looser-vs-base=' + loose, prt, diff[:3]))
    finally:
        shutil.copyfile(bak, path)
for r in rows: print(r)
