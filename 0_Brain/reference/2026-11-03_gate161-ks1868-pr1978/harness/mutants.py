#!/usr/bin/env python3
# G161 mutants: one exact replace per mutant, anchored to its site (target must lie within 700 chars after the anchor),
# run the PR's 4 new test files (vitest) and the recorder cells for that file's paths against a transpile of the mutated
# file. Restore by `git checkout --` inside the gate's own clone and assert the blob sha.
import json, subprocess, shutil, os
W = '/Volumes/DevMASTER/WEDNESDAY/0_Brain/reference/2026-11-03_gate161-ks1868-pr1978'
R = W + '/repo'; A = R + '/Blockchain/Dev/services/auth'
GITC = ['git', '-C', R]
FILES = {'email': 'services/email.ts', 'password': 'services/password.ts', 'oauth': 'services/oauthState.ts', 'sweep': 'services/issuerCertSweep.ts'}
BLOB = {k: subprocess.check_output(GITC + ['rev-parse', '1062b621269dac98f618a89f10baa51ff49c8c34:Blockchain/Dev/services/auth/src/' + v]).decode().strip() for k, v in FILES.items()}
PATHS = {'email': 'acsNoSmtp,acsSmtpOk,smtp', 'password': 'verify,hibp', 'oauth': 'oauthGetdel,oauthMulti', 'sweep': 'sweepMark,sweepFind7,sweepPubExpired'}
UNREAD = "reason = 'unreadable thrown value';"
SG = 'reason = String(err instanceof Error ? err.message : err);'
PW = 'reason = m === undefined || m === null ? m : String(m);'
M = [
 ('E1', 'email', 'const result = await poller.pollUntilDone', 'reason = String(err?.message);', 'reason = err?.message;'),
 ('E2', 'email', 'const result = await poller.pollUntilDone', UNREAD, "reason = 'x';"),
 ('E3', 'email', 'const info = await transport.sendMail', 'reason = String(error.message);', 'reason = error.message;'),
 ('E4', 'email', 'const info = await transport.sendMail', UNREAD, "reason = 'x';"),
 ('E5', 'email', 'const info = await transport.sendMail', 'reason = String(error.message);', 'reason = String(error?.message);'),
 ('E6', 'email', 'const info = await transport.sendMail', "${reason}`);\n    return false;", "${reason}`);\n    throw error;"),
 ('E7', 'email', 'const result = await poller.pollUntilDone', "${reason}`);\n    return false;", "${reason}`);\n    return true;"),
 ('P1', 'password', 'return await argon2.verify', PW, 'reason = m;'),
 ('P2', 'password', 'return await argon2.verify', UNREAD, "reason = 'x';"),
 ('P3', 'password', 'return await argon2.verify', 'const m = err?.message;', 'const m = err.message;'),
 ('P4', 'password', 'return await argon2.verify', "{ error: reason });\n      return false;", "{ error: reason });\n      return true;"),
 ('P5', 'password', 'body.split', PW, 'reason = m;'),
 ('P6', 'password', 'body.split', UNREAD, "reason = 'x';"),
 ('P7', 'password', 'body.split', 'const m = err?.message;', 'const m = err.message;'),
 ('P8', 'password', 'body.split', "{ error: reason });\n    return false;", "{ error: reason });\n    return true;"),
 ('P9', 'password', 'body.split', PW, 'reason = String(m);'),
 ('O1', 'oauth', 'stored = (first', SG, 'reason = err instanceof Error ? err.message : String(err);'),
 ('O2', 'oauth', 'stored = (first', UNREAD, "reason = 'x';"),
 ('O3', 'oauth', 'stored = (first', "error: reason,\n    });\n    return false;", "error: reason,\n    });\n    return true;"),
 ('O4', 'oauth', 'stored = (first', SG, 'reason = String(err);'),
 ('S1', 'sweep', 'expiredRows = await markExpiredCerts', SG, 'reason = err instanceof Error ? err.message : String(err);'),
 ('S2', 'sweep', 'expiredRows = await markExpiredCerts', UNREAD, "reason = 'x';"),
 ('S3', 'sweep', 'expiredRows = await markExpiredCerts', '    // Continue to the expiring-soon', '    return counts;\n    // Continue to the expiring-soon'),
 ('S4', 'sweep', 'EventTypes.ISSUER_CERT_EXPIRED,', SG, 'reason = err instanceof Error ? err.message : String(err);'),
 ('S5', 'sweep', 'EventTypes.ISSUER_CERT_EXPIRED,', UNREAD, "reason = 'x';"),
 ('S6', 'sweep', 'rows = await findExpiringSoon(days)', SG, 'reason = err instanceof Error ? err.message : String(err);'),
 ('S7', 'sweep', 'rows = await findExpiringSoon(days)', UNREAD, "reason = 'x';"),
 ('S8', 'sweep', 'rows = await findExpiringSoon(days)', '      continue;\n', '\n'),
]
TESTS = ['src/__tests__/ks1868-email-send-catches-unreadable-throw.test.ts', 'src/__tests__/ks1868-issuer-cert-sweep-body-catches-unreadable-throw.test.ts',
         'src/__tests__/ks1868-oauth-state-consume-catch-unreadable-throw.test.ts', 'src/__tests__/ks1868-password-verify-hibp-catches-unreadable-throw.test.ts']
def sha(f): return subprocess.check_output(GITC + ['hash-object', A + '/src/' + f]).decode().strip()
def restore(k):
    subprocess.check_call(GITC + ['checkout', '-q', '--', 'Blockchain/Dev/services/auth/src/' + FILES[k]])
    assert sha(FILES[k]) == BLOB[k], 'restore failed ' + k
results = []
for (mid, k, anchor, old, new) in M:
    p = A + '/src/' + FILES[k]; src = open(p).read()
    i = src.index(anchor); j = src.index(old, i)
    assert j - i < 700, mid + ' target too far from anchor'
    open(p, 'w').write(src[:j] + new + src[j + len(old):])
    try:
        out = W + '/logs/mut_' + mid + '.json'
        rc = subprocess.call(['nice', '-n', '5', 'node', W + '/harness/vt.js', out] + TESTS)
        r = json.load(open(out))
        failed = [t['title'][:70] for f in r['testResults'] for t in f['assertionResults'] if t['status'] == 'failed']
        bm = W + '/harness/build_mut/' + mid
        shutil.copytree(W + '/harness/build_head', bm)
        js = subprocess.check_output(['node', '-e', 'const ts=require(process.argv[1]);const fs=require("fs");process.stdout.write(ts.transpileModule(fs.readFileSync(process.argv[2],"utf8"),{compilerOptions:{target:ts.ScriptTarget.ES2022,module:ts.ModuleKind.CommonJS,esModuleInterop:true}}).outputText)',
            R + '/Blockchain/Dev/node_modules/typescript', p]).decode()
        open(bm + '/' + FILES[k].replace('.ts', '.js'), 'w').write(js)
        rec = json.loads(subprocess.check_output(['node', W + '/harness/mut_recorder.js', PATHS[k], bm]).decode().strip())
    finally:
        restore(k)
    res = {'id': mid, 'old': old, 'new': new, 'vitest_rc': rc, 'pass': r['numPassedTests'], 'fail': r['numFailedTests'], 'total': r['numTotalTests'],
           'killed_by_tests': r['numFailedTests'] > 0, 'failed': failed[:4], 'recorder': rec}
    results.append(res)
    print(mid, 'KILLED' if res['killed_by_tests'] else 'SURVIVED', 'fail=%d/%d' % (res['fail'], res['total']), 'recorder', json.dumps(rec), flush=True)
json.dump(results, open(W + '/logs/mutants.json', 'w'), indent=1)
print('killed', sum(1 for x in results if x['killed_by_tests']), 'of', len(results))
print('HEAD', subprocess.check_output(GITC + ['rev-parse', '--short', 'HEAD']).decode().strip(), 'status_lines', len(subprocess.check_output(GITC + ['status', '--porcelain']).decode().splitlines()))
