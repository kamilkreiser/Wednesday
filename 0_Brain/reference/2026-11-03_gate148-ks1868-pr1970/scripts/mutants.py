# QA gate 148 mutants: product only, tests untouched, sha256-restored after every run.
import hashlib, subprocess, re, json, os
W = '/Volumes/DevMASTER/WEDNESDAY/0_Brain/reference/2026-11-03_gate148-ks1868-pr1970'
D = W + '/repo/Blockchain/Dev'; A = D + '/services/api-gateway'; V = D + '/node_modules/.bin/vitest'
env = dict(os.environ, TMPDIR='/private/tmp/claude-501/-Volumes-DevMASTER-WEDNESDAY/efc1d998-fa1a-49cf-954c-5ff5b12449f9/scratchpad/g148')
C = "'unreadable thrown value'"
def blk(ind, var, expr):
    i = ' ' * ind
    return f"{i}try {{\n{i}  {var} = {expr};\n{i}}} catch {{\n{i}  {var} = {C};\n{i}}}\n"
SITES = {
  'bf': dict(f='src/middleware/security.ts', t='src/__tests__/ks1868-brute-force-redis-catch-unreadable-throw.test.ts', ind=6, var='reason',
             head='String(error instanceof Error ? error.message : error)', base='error instanceof Error ? error.message : String(error)',
             nostr='(error instanceof Error ? error.message : error)',
             site_mut=("      next();\n    }\n  };\n}", "      res.status(503).end();\n    }\n  };\n}", 'fail-closed: 503 instead of next() in the Redis-error catch')),
  'rl_log': dict(f='src/middleware/rateLimitEnforce.ts', t='src/__tests__/ks1868-rate-limit-enforce-message-coercion-unreadable-throw.test.ts', ind=2, var='errorText',
             head='err instanceof Error ? String(err.message) : err ? String(err) : undefined', base='err instanceof Error ? err.message : err ? String(err) : undefined',
             nostr='err instanceof Error ? err.message : err ? err : undefined',
             site_mut=("        logDegraded('redis-command-failed', clientId, err);\n        outcome = countInMemory(clientId, windowMs);", "        logDegraded('redis-command-failed', clientId, err);\n        outcome = null;", 'fail-open: degraded ceiling dropped (outcome null)')),
  'rl_hdr': dict(f='src/middleware/rateLimitEnforce.ts', t='src/__tests__/ks1868-rate-limit-enforce-message-coercion-unreadable-throw.test.ts', ind=8, var='reason',
             head='String(writeErr instanceof Error ? writeErr.message : writeErr)', base='writeErr instanceof Error ? writeErr.message : String(writeErr)',
             nostr='(writeErr instanceof Error ? writeErr.message : writeErr)',
             site_mut=("        refused = false;\n      }", "        refused = true; res.status(503).end();\n      }", 'fail-closed: 503 on header-write failure')),
  'audit': dict(f='src/middleware/audit.ts', t='src/__tests__/ks1868-audit-write-failed-catch-unreadable-throw.test.ts', ind=10, var='reason',
             head='String(err instanceof Error ? err.message : err)', base='err instanceof Error ? err.message : String(err)',
             nostr='(err instanceof Error ? err.message : err)',
             site_mut=("            path: auditPath, // KS-1457: was req.path, the trimmed remainder behind a responding gate\n          });\n        }\n      })();", "          });\n        }\n      })();", 'log drops path')),
}
def sha(p): return hashlib.sha256(open(p, 'rb').read()).hexdigest()
rows = []
for site, s in SITES.items():
    P = A + '/' + s['f']; orig = open(P).read(); h0 = sha(P)
    B = blk(s['ind'], s['var'], s['head'])
    assert orig.count(B) == 1, (site, 'block not found exactly once')
    i = ' ' * s['ind']
    muts = {
      'M0 revert to unguarded read': orig.replace(B, f"{i}{s['var']} = {s['base']} as any;\n"),
      'M1 inner try dropped': orig.replace(B, f"{i}{s['var']} = {s['head']};\n"),
      'M2 always constant': orig.replace(B, f"{i}{s['var']} = {C};\n"),
      'M3 no String()': orig.replace(B, blk(s['ind'], s['var'], s['nostr'] + ' as any')),
      'M4 inner catch rethrows': orig.replace(B, B.replace(f"{s['var']} = {C};", "throw new Error('m4');")),
      'M5 other constant text': orig.replace(B, B.replace(C, "'unreadable value'")),
      'M6 ' + s['site_mut'][2]: orig.replace(s['site_mut'][0], s['site_mut'][1]) if orig.count(s['site_mut'][0]) == 1 else None,
    }
    for name, txt in muts.items():
        if txt is None or txt == orig:
            rows.append(dict(site=site, mutant=name, result='NOT APPLIED')); continue
        open(P, 'w').write(txt)
        r = subprocess.run([V, 'run', '--root', A, s['t']], capture_output=True, text=True, env=env, timeout=600)
        out = r.stdout + r.stderr
        open(P, 'w').write(orig); ok = sha(P) == h0
        failed = sorted(set(re.findall(r'(?:FAIL|×|✗)\s.*?\b((?:C|R)\d)\b', out)))
        tests = re.search(r'Tests\s+(.*)', out)
        assertion = 'AssertionError' in out
        rows.append(dict(site=site, mutant=name, rc=r.returncode, result='KILLED' if r.returncode else 'SURVIVED', cells=failed, tests=tests.group(1).strip() if tests else None, assertionError=assertion, timeout='timed out' in out, restore=ok))
        open(W + '/logs/mutant_' + site + '_' + name.split()[0] + '.log', 'w').write(out)
        print(json.dumps(rows[-1]), flush=True)
with open(W + '/logs/mutants_table.log', 'w') as f:
    for x in rows: f.write(json.dumps(x) + '\n')
    f.write('killed %d survived %d\n' % (sum(1 for x in rows if x.get('result') == 'KILLED'), sum(1 for x in rows if x.get('result') == 'SURVIVED')))
