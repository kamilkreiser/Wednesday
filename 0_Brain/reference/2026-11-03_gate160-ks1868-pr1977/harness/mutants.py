#!/usr/bin/env python3
# G160 mutants: one exact replace at one changed site, run the PR's two new test files (vitest), and for every
# mutant ALSO re-run the recorder cells for that site against a transpile of the mutated file (build_mut),
# comparing with base+ordinaryError. Restores the file by `git checkout --` and asserts the blob sha.
import json, os, subprocess, sys, shutil
W = '/Volumes/DevMASTER/WEDNESDAY/0_Brain/reference/2026-11-03_gate160-ks1868-pr1977'
R = W + '/repo'; A = R + '/Blockchain/Dev/services/auth'; VT = R + '/Blockchain/Dev/node_modules/.bin/vitest'
GITC = ['git', '-C', '/Volumes/DevMASTER/WEDNESDAY/0_Brain/reference/2026-11-03_gate160-ks1868-pr1977/repo']
BLOB = {'db': 'dc592bec6a78027ab8a99bc21827ff015351e49d', 'session': 'b87ba0f46d1f8516e7f7e9b524891b9f38e50489'}
FILE = {'db': 'src/db.ts', 'session': 'src/services/session.ts'}
ANCHOR = {'P': ('db', "pool.on('error'"), 'M': ('db', '// Ignore errors'),
          'L': ('session', "redis.on('error'"), 'C': ('session', '} catch (err: any) {')}
COMMON = [
  ('1', 'const m = err?.message;', 'const m = err.message;'),
  ('2', 'reason = m === undefined || m === null ? m : String(m);', 'reason = m as any;'),
  ('3', "reason = 'unreadable thrown value';", 'reason = String(err);'),
  ('4', 'reason = m === undefined || m === null ? m : String(m);', 'reason = m === undefined || m === null ? m : `${m}`;'),
  ('5', 'reason = m === undefined || m === null ? m : String(m);', 'reason = m === undefined ? m : String(m);'),
]
EXTRA = {
  'P': [('6', "{ error: reason }", "{ error: err as any }")],
  'M': [('6', "error: reason });", "error: err });")],
  'L': [('6', "redisAvailable = false;\n    });", "\n    });"), ('7', "{ error: reason }", "{ error: err as any }")],
  'C': [('6', "redisAvailable = false;\n  }\n}", "\n  }\n}"), ('7', "{ error: reason }", "{ error: err }")],
}
T1 = 'src/__tests__/ks1868-auth-db-pool-error-and-migration-catch-unreadable-throw.test.ts'
T2 = 'src/__tests__/ks1868-auth-session-listener-and-init-catch-unreadable-throw.test.ts'
PATHOF = {'P': 'pool', 'M': 'migrate', 'L': 'listener', 'C': 'connect'}

def sha(f): return subprocess.check_output(GITC + ['hash-object', A + '/' + f]).decode().strip()
def restore(k):
    subprocess.check_call(GITC + ['checkout', '-q', '--', 'Blockchain/Dev/services/auth/' + FILE[k]])
    assert sha(FILE[k]) == BLOB[k], 'restore failed ' + k

def vitest(tag):
    out = W + '/logs/mut_' + tag + '.json'
    rc = subprocess.call(['node', W + '/harness/vt.js', out, T1, T2])
    r = json.load(open(out))
    return rc, r['numPassedTests'], r['numFailedTests'], r['numTotalTests']

def recorder(site, mid, k):
    # transpile mutated tree into build_mut (copy head build then overwrite the mutated file)
    bm = W + '/harness/build_mut/' + site + mid  # one fresh dir per mutant; nothing is ever deleted
    shutil.copytree(W + '/harness/build_head', bm)
    js = subprocess.check_output(['node', '-e', '''
const ts=require(process.argv[1]);const fs=require("fs");
process.stdout.write(ts.transpileModule(fs.readFileSync(process.argv[2],"utf8"),{compilerOptions:{target:ts.ScriptTarget.ES2022,module:ts.ModuleKind.CommonJS,esModuleInterop:true}}).outputText)''',
        R + '/Blockchain/Dev/node_modules/typescript', A + '/' + FILE[k]]).decode()
    open(bm + '/' + FILE[k].replace('src/', '').replace('.ts', '.js'), 'w').write(js)
    res = subprocess.check_output(['node', W + '/harness/mut_recorder.js', PATHOF[site], bm]).decode().strip()
    return res

results = []
for site, (k, anchor) in ANCHOR.items():
    for (mid, old, new) in COMMON + EXTRA[site]:
        tag = site + mid
        p = A + '/' + FILE[k]; src = open(p).read()
        i = src.index(anchor); j = src.index(old, i)
        # the site block ends within ~700 chars of its anchor; refuse a match that has walked into another site
        assert j - i < 700, tag + ' replace target too far from anchor'
        open(p, 'w').write(src[:j] + new + src[j + len(old):])
        try:
            rc, ps, fl, tot = vitest(tag)
            rec = recorder(site, mid, k)
        finally:
            restore(k)
        killed = fl > 0 or rc != 0
        line = {'mutant': tag, 'file': k, 'old': old, 'new': new, 'vitest_rc': rc, 'pass': ps, 'fail': fl, 'total': tot,
                'killed_by_tests': killed, 'recorder': rec}
        results.append(line); print(json.dumps(line)[:400], flush=True)
json.dump(results, open(W + '/logs/mutants.json', 'w'), indent=1)
print('killed by tests', sum(r['killed_by_tests'] for r in results), 'of', len(results))
