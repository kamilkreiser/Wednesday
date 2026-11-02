# Gate 153 mutants: product only, PR tests untouched, sha256-restored after every run. Usage: python3 -I mutants.py
import hashlib, json, re, subprocess, sys, os
W = '/Volumes/DevMASTER/WEDNESDAY/0_Brain/reference/2026-11-03_gate153-ks1868-pr1969'
T = W + '/repo/Blockchain/Dev/services/referral'
FILES = {
  'src/db.ts': ['src/__tests__/ks1868-referral-db-pool-error-and-ready-hook-unreadable-throw.test.ts'],
  'src/services/milestoneService.ts': ['src/__tests__/ks1868-milestone-service-db-read-catches-unreadable-throw.test.ts', 'src/__tests__/ks1868-milestone-service-db-write-catches-unreadable-throw.test.ts'],
  'src/services/referralService.ts': ['src/__tests__/ks1868-referral-service-db-read-catches-unreadable-throw.test.ts'],
  'src/services/fraudDetection.ts': ['src/__tests__/ks1868-fraud-detection-load-from-db-catch-unreadable-throw.test.ts'],
}
BLOCK = re.compile(r"( *)let reason: string \| null \| undefined;\n\s*try \{\n\s*const m = err\?\.message;\n\s*reason = m === undefined \|\| m === null \? m : String\(m\);\n\s*\} catch \{\n\s*reason = 'unreadable thrown value';\n\s*\}\n( *[^\n]*reason[^\n]*\n)")
def sha(p): return hashlib.sha256(open(p, 'rb').read()).hexdigest()
def mutate(src, k, mid):
  ms = list(BLOCK.finditer(src)); m = ms[k]; ind = m.group(1); blk = m.group(0); log = m.group(2)
  body = blk[: len(blk) - len(log)]
  if mid == 'M0_revert': new = ind + 'const reason = err?.message;\n' + log
  elif mid == 'M1_inner_rethrow': new = body.replace("reason = 'unreadable thrown value';", 'throw err;') + log
  elif mid == 'M2_constant_always': new = body.replace('reason = m === undefined || m === null ? m : String(m);', "void m; reason = 'unreadable thrown value';") + log
  elif mid == 'M3_string_dropped': new = body.replace('reason = m === undefined || m === null ? m : String(m);', 'reason = m as any;') + log
  elif mid == 'M4_log_removed': new = body + ind + 'void reason;\n'
  elif mid == 'M5_rethrow_after_log': new = body + log + ind + 'throw err;\n'
  return src[: m.start()] + new + src[m.end():]
MUTS = ['M0_revert', 'M1_inner_rethrow', 'M2_constant_always', 'M3_string_dropped', 'M4_log_removed', 'M5_rethrow_after_log']
rows = []
for rel, tests in FILES.items():
  p = T + '/' + rel; orig = open(p).read(); h0 = sha(p); n = len(BLOCK.findall(orig))
  for k in range(n):
    line = orig[: list(BLOCK.finditer(orig))[k].start()].count('\n') + 1
    for mid in MUTS:
      open(p, 'w').write(mutate(orig, k, mid))
      log = f"{W}/logs/mutants/{os.path.basename(rel)}_{k}_{mid}.log"
      r = subprocess.run(['nice', '-n', '10', 'node', W + '/scripts/vt.cjs', *tests], cwd=W + '/logs/child_cwd', capture_output=True, text=True)
      out = r.stdout + r.stderr; open(log, 'w').write(out + f'\nrc={r.returncode}\n')
      failed = sorted(set(re.findall(r'FAIL .*?> ((?:RED|control) ks1868 [RC]\d+)', out)))
      tm = re.search(r'Tests\s+(.*)', out)
      by_assert = 'AssertionError' in out; tsx_err = 'Transform failed' in out or 'SyntaxError' in out
      open(p, 'w').write(orig); ok = sha(p) == h0
      row = dict(file=rel, site=k, line=line, mutant=mid, rc=r.returncode, verdict='KILLED' if r.returncode != 0 else 'SURVIVED', cells=failed, tests=tm.group(1) if tm else None, byAssertion=by_assert, transformErr=tsx_err, restore=ok)
      rows.append(row); print(json.dumps(row), flush=True)
      if not ok: print('RESTORE FAIL', rel); sys.exit(2)
json.dump(rows, open(W + '/logs/mutants_table.json', 'w'), indent=1)
print('done', sum(r['verdict'] == 'KILLED' for r in rows), '/', len(rows))
