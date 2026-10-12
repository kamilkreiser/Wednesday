"""Mutation run at the head worktree (scratch only). Mutant table copied VERBATIM from the author's
mutants1533r2.py (17 mutants). Each edit ASSERTS its anchor occurs exactly once and that the mutated text is
present in the file before the run (a silent no-op mutator would print a green that means nothing), then
restores and asserts the sha256 matches the baseline. Instruments per mutant: (a) the PR's own file,
(b) the gate harness (memory mode; GATE_DB=1 for the subset given on argv)."""
import hashlib, re, subprocess, sys, json, os, importlib.util
W = '/private/tmp/claude-501/-Volumes-DevMASTER-WEDNESDAY/f2077cbf-bb12-49ee-8d59-f5f537b335e0/scratchpad/g1521r1'
SEC = W + '/head/Blockchain/Dev/services/security'
C = SEC + '/src/index.ts'
spec = importlib.util.spec_from_file_location('vm', W + '/harness/v_mutants_table.py'); vm = importlib.util.module_from_spec(spec); spec.loader.exec_module(vm)
M = vm.M
P = open(C, encoding='utf8').read(); BASE = hashlib.sha256(P.encode()).hexdigest()[:16]
PG = set(sys.argv[1:])
def vfile():
    r = subprocess.run(['npx', 'vitest', 'run', 'src/__tests__/ks1533-key-mint-organisation-arm.test.ts'], cwd=SEC, capture_output=True, text=True)
    o = r.stdout + r.stderr; m = re.search(r'^\s+Tests\s+(.*)$', o, re.M)
    return r.returncode, (m.group(1).strip() if m else 'NO TESTS LINE')
def gate(tag, mode):
    r = subprocess.run(['bash', W + '/run.sh', 'head', mode, f'mut-{tag}-{mode}'], capture_output=True, text=True)
    line = r.stdout.strip().splitlines()[0]
    rc = int(re.search(r'rc=(\d+)', line).group(1)); t = line.split('rc=')[1]
    return rc, t
print('baseline index.ts sha256/16', BASE)
rc, l = vfile(); print('UNMUTATED PR file: rc=%d %s' % (rc, l)); assert rc == 0
grc, gl = gate('BASE', 'mem'); print('UNMUTATED gate harness (mem): %s' % gl); assert grc == 0
res = []
for name, old, new in M:
    tag = name.split()[0]
    n = P.count(old)
    assert n == 1, f'ANCHOR MISS {tag}: {n}'
    open(C, 'w', encoding='utf8').write(P.replace(old, new, 1))
    landed = open(C, encoding='utf8').read()
    assert new in landed and landed != P, f'MUTANT DID NOT LAND {tag}'
    try:
        vrc, vl = vfile()
        grc, gl = gate(tag, 'mem')
        prc, pl = gate(tag, 'pg') if tag in PG else (None, None)
    finally:
        open(C, 'w', encoding='utf8').write(P)
    ok = hashlib.sha256(open(C, encoding='utf8').read().encode()).hexdigest()[:16] == BASE
    assert ok, 'RESTORE FAILED'
    res.append(dict(m=name, vfile=('KILLED' if vrc else 'survived'), vline=vl, gate_mem=('KILLED' if grc else 'survived'), gline=gl,
                    gate_pg=(None if prc is None else ('KILLED' if prc else 'survived')), pline=pl))
    print('%-70s PRfile=%-8s [%s] | gate-mem=%-8s [%s] | gate-pg=%s [%s] restored=%s' % (name, res[-1]['vfile'], vl, res[-1]['gate_mem'], gl, res[-1]['gate_pg'], pl, ok))
json.dump(res, open(W + '/out/mutants.json', 'w'), indent=1)
print('PR file killed %d/%d; gate harness killed %d/%d' % (sum(r['vfile'] == 'KILLED' for r in res), len(res), sum(r['gate_mem'] == 'KILLED' for r in res), len(res)))
