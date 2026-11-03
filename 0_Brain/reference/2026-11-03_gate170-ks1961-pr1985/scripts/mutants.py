# QA gate 170 mutants (adapted from gate 168's scripts/mutants.py): head a0a91f65 product files only, tests untouched.
# Each run: the PR's 7 changed test files. Every anchor must match exactly once; sha256-restored after every run.
import hashlib, subprocess, json, os
W = '/Volumes/DevMASTER/WEDNESDAY/0_Brain/reference/2026-11-03_gate170-ks1961-pr1985'
D = W + '/repo/Blockchain/Dev'; A = D + '/services/api-gateway'; V = D + '/node_modules/.bin/vitest'
env = dict(os.environ, TMPDIR=W + '/tmp', HOME=W + '/home')
SEC = A + '/src/middleware/security.ts'; RL = A + '/src/middleware/rateLimitEnforce.ts'
TESTS = ['auth.test.ts', 'ks1868-brute-force-redis-catch-unreadable-throw.test.ts', 'ks1868-rate-limit-enforce-message-coercion-unreadable-throw.test.ts',
         'ks1961-brute-force-guard-fails-closed.test.ts', 'ks1961-rate-limit-header-step-fails-closed.test.ts', 'ks480-connector-auth.test.ts', 'security.test.ts']
COMMITTED_GUARD = "    } else if (!res.writableEnded) {\n      res.end();\n    }\n  } catch {\n    // Nothing more can be written; next() is still never called.\n  }\n}\n\nexport function createBruteForceProtection"
M = [
  # --- gate 168's set, re-anchored where head changed ---
  ('M1 guard read catch calls next() (fail open)', SEC, "      refuseLogin(res, error);\n      return;", "      next();\n      return;"),
  ('M2 no deadline (raw store read)', SEC, "const record: unknown = await Promise.race([redisService.getBruteForceData(key), deadline]);", "const record: unknown = await redisService.getBruteForceData(key);"),
  ('M3 deadline 2000 -> 30000 ms', SEC, "const BRUTE_FORCE_READ_TIMEOUT_MS = 2_000;", "const BRUTE_FORCE_READ_TIMEOUT_MS = 30_000;"),
  ('M4 shape check removed', SEC, "    if (!isLockoutRecord(record)) throw new MalformedLockoutRecord();\n", ""),
  ('M5 shape check ignores blockedUntil', SEC, "&& (r.blockedUntil === undefined || Number.isFinite(r.blockedUntil))", ""),
  ('M6 shape check accepts arrays', SEC, "if (typeof v !== 'object' || Array.isArray(v)) return false;", "if (typeof v !== 'object') return false;"),
  ('M7 guard refusal 503 -> 500', SEC, "res.status(503).json({ success: false, error: { code: 'SERVICE_UNAVAILABLE', message: 'Unable to check failed-login state, please retry' } });", "res.status(500).json({ success: false, error: { code: 'SERVICE_UNAVAILABLE', message: 'Unable to check failed-login state, please retry' } });"),
  ('M8 guard log names the value, not the type', SEC, "winstonLogger.error(line, { thrownType: thrownTypeOf(error) });", "winstonLogger.error(line, { thrownType: thrownTypeOf(error), error: (() => { try { return String((error as any)?.message ?? error); } catch { return 'x'; } })() });"),
  ('M9 guard committed-response branch does not end', SEC, COMMITTED_GUARD, "    }\n  } catch {\n    // Nothing more can be written; next() is still never called.\n  }\n}\n\nexport function createBruteForceProtection"),
  ('M10 thrownTypeOf returns typeof only', SEC, "    const name: unknown = Object.getPrototypeOf(value)?.constructor?.name;\n    return typeof name === 'string' && name !== '' ? name : 'object';", "    return typeof value;"),
  ('M11 limiter refusal block removed (falls to next())', RL, "    if (refusal) {\n      refuseUnavailable(res, clientId, refusal.step, { thrownType: thrownTypeOf(refusal.thrown) });\n      return;\n    }\n", ""),
  ('M12 fallback catch back to fail open', RL, "        refusal = { step: 'in-memory-fallback', thrown: fallbackErr };\n        outcome = null;", "        outcome = null;"),
  ('M13 header-step catch back to fail open', RL, "        refusal = { step: 'response-write', thrown: writeErr };\n      }", "        refused = false;\n      }"),
  ('M14 limiter refusal 503 -> 429', RL, "      res.status(503).json(REFUSED_BODY);", "      res.status(429).json(REFUSED_BODY);"),
  ('M15 limiter committed branch does not end', RL, "    } else if (!res.writableEnded) {\n      res.end();\n    }\n  } catch {\n    // Nothing more can be written; next() is still never called.\n  }\n}\n\nfunction sendRateLimited", "    }\n  } catch {\n    // Nothing more can be written; next() is still never called.\n  }\n}\n\nfunction sendRateLimited"),
  ('M16 limiter refusal log names the thrown value', RL, "refuseUnavailable(res, clientId, refusal.step, { thrownType: thrownTypeOf(refusal.thrown) });", "refuseUnavailable(res, clientId, refusal.step, { thrownType: thrownTypeOf(refusal.thrown), error: String((refusal.thrown as any)?.message ?? refusal.thrown) } as any);"),
  ('M17 allowance check: any positive number', RL, "return typeof v === 'number' && Number.isSafeInteger(v) && v > 0;", "return typeof v === 'number' && v > 0;"),
  ('M18 allowance check: finite instead of safe integer', RL, "return typeof v === 'number' && Number.isSafeInteger(v) && v > 0;", "return typeof v === 'number' && Number.isFinite(v) && v > 0;"),
  # --- round 2's new code ---
  ('M19 malformed refusal removed entirely (develop reading)', RL, "    if (malformedField) {\n      refuseUnavailable(res, clientId, 'configured-allowance', { field: malformedField, valueType: typeof user[malformedField] });\n      return;\n    }\n", ""),
  ('M20 malformed rateLimit not refused (window still is)', RL, "    const malformedField = user.rateLimit && !isCleanPositiveInteger(user.rateLimit)\n      ? 'rateLimit'\n      :", "    const malformedField = false\n      ? 'rateLimit'\n      :"),
  ('M21 malformed window not refused (rateLimit still is)', RL, "      : user.rateLimitWindow && !isCleanPositiveInteger(user.rateLimitWindow)\n        ? 'rateLimitWindow'", "      : false\n        ? 'rateLimitWindow'"),
  ('M22 malformed refusal also calls next()', RL, "refuseUnavailable(res, clientId, 'configured-allowance', { field: malformedField, valueType: typeof user[malformedField] });\n      return;", "refuseUnavailable(res, clientId, 'configured-allowance', { field: malformedField, valueType: typeof user[malformedField] });\n      next();\n      return;"),
  ('M23 malformed -> round-1 default instead of refusal', RL, "    if (malformedField) {\n      refuseUnavailable(res, clientId, 'configured-allowance', { field: malformedField, valueType: typeof user[malformedField] });\n      return;\n    }\n    const limit = user.rateLimit || DEFAULT_MACHINE_RATE_LIMIT;\n    const windowMs = (user.rateLimitWindow || DEFAULT_MACHINE_RATE_WINDOW) * 1000;", "    const limit = isCleanPositiveInteger(user.rateLimit) ? user.rateLimit : DEFAULT_MACHINE_RATE_LIMIT;\n    const windowMs = (isCleanPositiveInteger(user.rateLimitWindow) ? user.rateLimitWindow : DEFAULT_MACHINE_RATE_WINDOW) * 1000;"),
  ('M24 falsy rateLimit also refused (truthy guard dropped)', RL, "    const malformedField = user.rateLimit && !isCleanPositiveInteger(user.rateLimit)", "    const malformedField = !isCleanPositiveInteger(user.rateLimit)"),
  ('M25 falsy window also refused (truthy guard dropped)', RL, "      : user.rateLimitWindow && !isCleanPositiveInteger(user.rateLimitWindow)", "      : !isCleanPositiveInteger(user.rateLimitWindow)"),
  ('M26 malformed refusal logs the value', RL, "valueType: typeof user[malformedField] });", "valueType: typeof user[malformedField], value: String(user[malformedField]) } as any);"),
  ('M27 malformed refusal 503 -> 429', RL, "    if (malformedField) {\n      refuseUnavailable(", "    if (malformedField) {\n      res.status(429).json(REFUSED_BODY); return;\n      refuseUnavailable("),
  ('M28 degrade line logs the thrown text again', RL, "    thrownType: err === undefined ? undefined : thrownTypeOf(err),", "    thrownType: err === undefined ? undefined : thrownTypeOf(err),\n    error: err instanceof Error ? String(err.message) : err ? String(err) : undefined,"),
  ('M29 guard 429 write back outside the try (round-1 shape)', SEC, "      } catch (writeError) {\n        refuseLogin(res, writeError, 'lockout-response');\n      }", "      } catch (writeError) {\n        throw writeError;\n      }"),
  ('M30 guard 429-write catch calls next()', SEC, "        refuseLogin(res, writeError, 'lockout-response');", "        next();"),
  ('M31 guard 429-write refusal uses the read line', SEC, "        refuseLogin(res, writeError, 'lockout-response');", "        refuseLogin(res, writeError);"),
]
def sha(p): return hashlib.sha256(open(p, 'rb').read()).hexdigest()
def run():
    out_json = W + '/tmp/mut.json'
    if os.path.exists(out_json): os.replace(out_json, W + '/tmp/mut.prev.json')
    r = subprocess.run([V, 'run', '--root', A, '--reporter=json', '--outputFile=' + out_json] + ['src/__tests__/' + t for t in TESTS], capture_output=True, text=True, env=env, timeout=900)
    try:
        d = json.load(open(out_json))
        fails = [(f['name'].split('/')[-1], a['title'][:90], (a.get('failureMessages') or [''])[0].split('\n')[0][:110]) for f in d['testResults'] for a in f['assertionResults'] if a['status'] == 'failed']
        fileErr = [f['name'].split('/')[-1] + ': ' + f.get('message', '')[:120] for f in d['testResults'] if f.get('status') == 'failed' and not f['assertionResults']]
        return r.returncode, d['numPassedTests'], d['numTotalTests'], fails, fileErr
    except Exception as e:
        return r.returncode, None, None, [('harness', str(e), '')], []
rows = []
rc, p, t, f, fe = run(); rows.append(dict(mutant='CONTROL unmutated', rc=rc, passed=p, total=t, failing=len(f), fileErrors=fe))
print(json.dumps(rows[-1]), flush=True)
for name, path, old, new in M:
    orig = open(path).read(); h0 = sha(path)
    if orig.count(old) != 1:
        rows.append(dict(mutant=name, result='NOT APPLIED', count=orig.count(old))); print(json.dumps(rows[-1]), flush=True); continue
    open(path, 'w').write(orig.replace(old, new))
    try:
        rc, p, t, f, fe = run()
    finally:
        open(path, 'w').write(orig)
    ok = sha(path) == h0
    byAssert = sum(1 for x in f if 'AssertionError' in x[2] or 'expected' in x[2])
    rows.append(dict(mutant=name, result='KILLED' if (rc != 0 and f) else ('ERRORED' if rc != 0 else 'SURVIVED'), rc=rc, passed=p, total=t, failing=len(f), byAssertion=byAssert, sample=f[:2], fileErrors=fe, restored=ok))
    print(json.dumps(rows[-1]), flush=True)
with open(W + '/logs/mutants_table.jsonl', 'w') as fh:
    for x in rows: fh.write(json.dumps(x) + '\n')
