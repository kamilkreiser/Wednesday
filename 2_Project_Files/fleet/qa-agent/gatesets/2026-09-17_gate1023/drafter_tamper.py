#!/usr/bin/env python3
"""drafter_tamper.py [ROW ...] — #1023 (KS-1207) drafter tamper table on the HEAD tree (2f74491eb) of the drafter's OWN clone. The seat's 6 rows RE-DERIVED in
DRAFTER forms (the seat's exact forms live in Seat A's records, which the drafter may not enter — the gate names the seat's forms if it can read them) plus drafter G
rows from directions the seat did not take. Per row: anchor count == 1 (else VOID), marker (sha changed), project tsc --noEmit -p . rc (non-zero = VOID), the WHOLE
api-gateway suite (denominator 56 / 550, pending 0), reds classified AssertionError vs other, restore by bytes (sha256 equal) + git diff --quiet HEAD. Derived from the
#1019r2 drafter_tamper.py."""
import hashlib, json, os, subprocess, sys, datetime
GSD = os.path.dirname(os.path.abspath(__file__))
PA = json.load(open(GSD + '/drafter_paths.json')); W = PA['W']; WT = PA['trees']['head']; DEVT = PA['trees']['dev']
GW = WT + '/Blockchain/Dev/services/api-gateway'; AU = GW + '/src/middleware/auth.ts'; BIN = WT + '/Blockchain/Dev/node_modules/.bin/'
REQ = "    if (presentedKey && !meta && required) {\n      res.status(401).json({ success: false, error: { code: 'UNAUTHORIZED', message: 'Invalid API key' } });\n      return;\n    }\n"
CONN = "    if (apiKey && meta) {\n"
SESS = "      if (decoded.sessionId) {\n"
VCATCH = "    apiKeyCache.set(key, { result: meta, expiresAt: Date.now() + 60_000 });\n    return meta;\n  } catch {\n    return null;\n  }\n"
BEARER_RUN = "      runWithTenantId((req.headers['x-tenant-id'] as string | undefined) || decoded.tenantId, () => clientRateLimit(req, res, next));\n"
DEV_AUTH = open(DEVT + '/Blockchain/Dev/services/api-gateway/src/middleware/auth.ts').read()
ROWS = [
 ('T0', None, None, 0, 'seat', 'no edit'),
 ('TBYPASS', REQ, REQ + "    if (presentedKey && !meta) {\n      next();\n      return;\n    }\n", 10, 'seat', 'the old immediate next() on an optional failed key (drafter form)'),
 ('TSKIPSESSION', SESS, "      if (decoded.sessionId && !req.headers['x-api-key']) {\n", 5, 'seat', 'the session check skipped whenever a key header is present (drafter form)'),
 ('TNOBEARER', REQ, REQ + "    if (presentedKey && !meta && !(req.headers.authorization || '').startsWith('Bearer ')) {\n      res.status(401).json({ success: false, error: { code: 'UNAUTHORIZED', message: 'Invalid API key' } });\n      return;\n    }\n", 5, 'seat', 'shape A: a failed key with no Bearer refused 401 (drafter form)'),
 ('TREQ', "    if (presentedKey && !meta && required) {\n", "    if (presentedKey && !meta && required && false) {\n", 1, 'seat', 'a required mount no longer refuses a failed key (drafter form)'),
 ('TI', CONN, "    // tamper TI: inert comment\n" + CONN, 0, 'seat', 'inert'),
 ('REDPROOF', 'WHOLE', DEV_AUTH, 10, 'seat', 'auth.ts = develop 581c9db0d bytes (blob 7c985bdce): the READY says 10 red / 16 green of 26'),
 ('G-PRECEDENCE', CONN, "    if (apiKey && meta && !(req.headers.authorization || '').startsWith('Bearer ')) {\n", None, 'drafter', 'a live Bearer beats a VALID key (principal precedence swapped): no seat cell sends JWT + valid key'),
 ('G-ERRMETA', VCATCH, VCATCH.replace("  } catch {\n    return null;\n", "  } catch {\n    return { connectorId: 'qa-errored', scopes: [], organizationId: '', rateLimit: 100, rateLimitWindow: 60 };\n"), None, 'drafter', 'meta TRUTHY on an errored validation (fetch threw): no seat cell makes validation throw or 5xx'),
 ('G-JUNKBUCKET', REQ, REQ + "    if (presentedKey && !meta) {\n      await getRedisClient()?.incr('ratelimit:qa-junk-bucket');\n    }\n", None, 'drafter', 'a failed key consumes a limiter bucket on the fall-through'),
 ('G-TENANTDROP', BEARER_RUN, "      runWithTenantId(apiKey ? undefined : ((req.headers['x-tenant-id'] as string | undefined) || decoded.tenantId), () => clientRateLimit(req, res, next));\n", None, 'drafter', 'the Bearer fall-through loses its tenant context when a key header was presented'),
 ('G-PREFIXFREE', "    const presentedKey = Boolean(apiKey && apiKey.startsWith('sk_'));\n", "    const presentedKey = Boolean(apiKey);\n", None, 'drafter', 'any x-api-key value (not only sk_) is treated as a presented key'),
 ('T0-after', None, None, 0, 'seat', 'no edit, after'),
]
def ts(): return datetime.datetime.now().astimezone().strftime('%H:%M:%S %Z')
def sha(p): return hashlib.sha256(open(p, 'rb').read()).hexdigest()
def P(*a): print(' '.join(str(x) for x in a), flush=True)
ONLY = set(sys.argv[1:])
P('drafter_tamper', datetime.datetime.now().astimezone().strftime('%Y-%m-%d %H:%M:%S %Z'), '| tree', WT, '| HEAD', subprocess.run(['git', '-C', WT, 'rev-parse', 'HEAD'], capture_output=True, text=True).stdout.strip())
out = []
for rid, anchor, repl, pred, by, names in ROWS:
    if ONLY and rid not in ONLY: continue
    row = dict(id=rid, predicted=pred, predicted_by=by, names=names)
    row['porcelain_before'] = len(subprocess.run(['git', '-C', WT, 'status', '--porcelain', '--untracked-files=no'], capture_output=True, text=True).stdout.splitlines())
    orig = open(AU, 'rb').read(); osha = sha(AU)
    if anchor == 'WHOLE':
        open(AU, 'w').write(repl); row['marker'] = sha(AU) != osha
    elif anchor is not None:
        n = orig.decode().count(anchor); row['anchor_count'] = n
        if n != 1: row['VOID'] = 'anchor count %d' % n; out.append(row); P(json.dumps(row)); continue
        open(AU, 'wb').write(orig.decode().replace(anchor, repl).encode()); row['marker'] = sha(AU) != osha
    try:
        p = subprocess.run([BIN + 'tsc', '--noEmit', '-p', '.'], cwd=GW, capture_output=True, text=True); row['tsc_rc'] = p.returncode
        if p.returncode: row['tsc_head'] = (p.stdout + p.stderr)[:400]
        jf = W + '/tamper_%s.json' % rid; env = dict(os.environ); env.pop('NODE_ENV', None)
        v = subprocess.run([BIN + 'vitest', 'run', '--reporter=json', '--outputFile=' + jf], cwd=GW, capture_output=True, text=True, env=env)
        open(W + '/tamper_%s.stderr.txt' % rid, 'w').write(v.stderr)
        d = json.load(open(jf))
        row.update(files=len(d['testResults']), tests=d['numTotalTests'], failed=d['numFailedTests'], pending=d['numPendingTests'])
        row['denominator_ok'] = (row['files'], row['tests']) == (56, 550) and row['pending'] == 0
        reds, other = [], []
        for f in d['testResults']:
            if f['status'] != 'passed' and not f['assertionResults']: other.append('FILE-LOAD ' + f['name'].split('/')[-1] + ': ' + (f.get('message') or '')[:160])
            for t in f['assertionResults']:
                if t['status'] == 'failed':
                    msg = (t.get('failureMessages') or [''])[0]; item = f['name'].split('/')[-1] + ' :: ' + t['title'][:140]
                    reds.append(item)
                    if 'AssertionError' not in msg: other.append(item + ' :: ' + msg.split('\n')[0][:160])
        row['reds'] = len(reds); row['non_assertion'] = other; row['red_list'] = reds
        row['as_predicted'] = (pred is None) or (row['reds'] == pred)
        row['VALID'] = row['tsc_rc'] == 0 and row['denominator_ok'] and not [o for o in other if o.startswith('FILE-LOAD')]
    finally:
        if anchor is not None:
            open(AU, 'wb').write(orig); row['restored_sha_equal'] = sha(AU) == osha
        row['git_diff_quiet'] = subprocess.run(['git', '-C', WT, 'diff', '--quiet', 'HEAD'], capture_output=True).returncode == 0
    rl = row.pop('red_list', []); P(ts(), json.dumps(row))
    for r in rl: P('   RED', r)
    row['red_list'] = rl; out.append(row)
json.dump(out, open(GSD + '/tamper_rows.json', 'w'), indent=1)
P('drafter_tamper end', ts())
