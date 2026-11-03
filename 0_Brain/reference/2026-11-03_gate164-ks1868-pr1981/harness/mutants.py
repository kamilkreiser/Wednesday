# G164 mutants: one exact replace per mutant at ONE site (A = revokePriorConnectorKeys :314, B = saveKeyAndRetirePriors :427).
# For each: (1) mutate the clone's index.ts, run the PR's test file (vitest, cwd = security), restore by git checkout and
# assert the blob; (2) transpile a mutated copy of src_head into build_mut/<id> and run the recorder for that site.
import json, os, re, subprocess, sys, shutil
W = '/Volumes/DevMASTER/WEDNESDAY/0_Brain/reference/2026-11-03_gate164-ks1868-pr1981'
R = W + '/repo'; H = W + '/harness'; IDX = R + '/Blockchain/Dev/services/security/src/index.ts'
HEAD_BLOB = 'd7a5674ba4c10e3844858d08f975b4b43eeefd44'
TEST = 'src/__tests__/ks1868-security-rotate-message-coercion-unreadable-throw.test.ts'
G = 'reason = String(err instanceof Error ? err.message : err);'
MUT = {
  'X1': 'reason = err instanceof Error ? err.message : String(err);',          # revert to base
  'X2': 'reason = String(err);',                                                # never read message
  'X3': 'reason = `${err instanceof Error ? err.message : err}`;',              # template literal
  'X4': 'reason = JSON.stringify(err instanceof Error ? err.message : err);',   # JSON instead of String
  'X5': 'reason = String(err instanceof Error ? err.message : String(err));',  # harmless? (equivalent candidate)
  'X6': 'reason = String((err as any)?.message ?? err);',                      # optional read, no instanceof
}
ANCH = {'A': 'KS-577: revoke-on-rotate FAILED', 'B': "ROLLBACK TO SAVEPOINT ks1549_retire');"}
KINDS = 'ordinaryError,plainString,null,undefined,revokedProxy,messageGetterThrows,symbolMessage,bigintMessage,messageToJSONThrows,messageIsRevokedProxy,cyclicMessage,nullProtoMessage,nullMessage,messageToStringThrows'
def blob(): return subprocess.run(['git', 'hash-object', IDX], capture_output=True, text=True).stdout.strip()
def mutate(src, site, rep):
    occ = [m.start() for m in re.finditer(re.escape(G), src)]
    assert len(occ) == 2, occ
    pos = occ[0] if site == 'A' else occ[1]
    if site == 'A':  # A's log line comes AFTER the guard; B's ROLLBACK comes BEFORE it
        a = src.find(ANCH['A'], pos); assert 0 < a - pos < 700
    else:
        a = src.rfind(ANCH['B'], 0, pos); assert 0 < pos - a < 700
    return src[:pos] + rep + src[pos + len(G):]
res = {}
for mid, rep in MUT.items():
    for site in 'AB':
        k = f'{mid}{site}'; assert blob() == HEAD_BLOB
        orig = open(IDX).read(); m = mutate(orig, site, rep); open(IDX, 'w').write(m)
        oj = f'{W}/logs/mut_{k}_vitest.json'
        rc = subprocess.run(['node', H + '/vt.js', oj, TEST]).returncode
        subprocess.run(['git', '-C', R, 'checkout', '--', IDX], check=True); assert blob() == HEAD_BLOB
        try:
            j = json.load(open(oj)); failed = [t['title'] for f in j['testResults'] for t in f['assertionResults'] if t['status'] != 'passed']
            tot = j['numTotalTests']
        except Exception as e:
            failed = ['<no json: %s>' % e]; tot = None
        # recorder
        md = f'{H}/mut/{k}'; shutil.rmtree(md, ignore_errors=True); shutil.copytree(H + '/src_head', md)
        open(md + '/index.ts', 'w').write(mutate(open(H + '/src_head/index.ts').read(), site, rep))
        bd = f'{H}/build_mut/{k}'; subprocess.run(['node', H + '/transpile.js', md, bd], check=True, capture_output=True)
        site_name = 'direct' if site == 'A' else 'route'
        mj = f'{W}/logs/mut_{k}_matrix.json'
        subprocess.run(['node', H + '/run_matrix.js', mj, bd, site_name, KINDS], check=True, capture_output=True)
        res[k] = {'vitest_rc': rc, 'tests_total': tot, 'tests_failed': failed, 'matrix': mj}
        print(k, 'rc', rc, 'failed', len(failed), flush=True)
json.dump(res, open(W + '/logs/mutants.json', 'w'), indent=1)
