#!/usr/bin/env python3
# Gate 163 mutants on routes/milestones.ts + routes/referrals.ts in MY clone (repo/, at pr/1980). PR tests untouched;
# sha256-restored after each. Each mutant runs the new ks1957 file + the KS-444 file with vitest's json reporter.
# Also a 'RED' pseudo-mutant: both route files at base (66cbe4e52), to classify every red-first failure.
import hashlib, subprocess, json, os, sys
W = '/Volumes/DevMASTER/WEDNESDAY/0_Brain/reference/2026-11-03_gate163-ks1957-pr1980'
REL = 'Blockchain/Dev/services/referral'
T = W + '/repo/' + REL
MS = T + '/src/routes/milestones.ts'; RF = T + '/src/routes/referrals.ts'
TESTS = ['src/__tests__/ks1957-award-routes-owner-or-platform.test.ts', 'src/__tests__/qualify.validation.test.ts']
OUTJ = '/private/tmp/claude-501/-Volumes-DevMASTER-WEDNESDAY/6b87194c-7310-4eff-9191-a63be490f43e/scratchpad/g163/mut.json'
os.makedirs(os.path.dirname(OUTJ), exist_ok=True)
sha = lambda p: hashlib.sha256(open(p, 'rb').read()).hexdigest()
orig = {MS: open(MS).read(), RF: open(RF).read()}; osha = {p: sha(p) for p in orig}
CHK_IF = "if (!isOwner && !isPlatformRole(caller.role as string | undefined)) {"
QUAL_IF = "if (!isPlatformRole((req as any).user?.role)) {"
OWNER = "const isOwner = typeof caller.userId === 'string' && caller.userId !== '' && caller.userId === userId;"
M = [
  ('M1 /check guard removed', MS, CHK_IF, "if (false) {"),
  ('M2 /qualify guard removed', RF, QUAL_IF, "if (false) {"),
  ('M3 owner compare loose (String(userId) ===)', MS, OWNER, "const isOwner = String(caller.userId) === userId;"),
  ('M4 owner: drop the non-empty test', MS, OWNER, "const isOwner = typeof caller.userId === 'string' && caller.userId === userId;"),
  ('M5 owner: drop the typeof string test (=== kept)', MS, OWNER, "const isOwner = caller.userId !== '' && caller.userId === userId;"),
  ('M6 owner compare case-insensitive', MS, OWNER, "const isOwner = typeof caller.userId === 'string' && caller.userId !== '' && caller.userId.toLowerCase() === userId.toLowerCase();"),
  ('M7 owner inverted (!==)', MS, OWNER, "const isOwner = typeof caller.userId === 'string' && caller.userId !== '' && caller.userId !== userId;"),
  ('M8 /check || -> && (owner AND platform needed)', MS, CHK_IF, "if (!isOwner || !isPlatformRole(caller.role as string | undefined)) {"),
  ('M9 /check siblings fail-open form', MS, CHK_IF, "if (caller.userId && caller.userId !== userId && !isPlatformRole(caller.role as string | undefined)) {"),
  ('M10 /check role = String(role).toUpperCase() set test (KS-1591)', MS, CHK_IF, "if (!isOwner && !['SYSTEM_ADMIN','SUPER_ADMIN'].includes(String(caller.role).toUpperCase())) {"),
  ('M11 /qualify role = String(role).toUpperCase() set test (KS-1591)', RF, QUAL_IF, "if (!['SYSTEM_ADMIN','SUPER_ADMIN'].includes(String((req as any).user?.role).toUpperCase())) {"),
  ('M12 /check admits ADMIN as platform', MS, CHK_IF, "if (!isOwner && !(isPlatformRole(caller.role as string | undefined) || caller.role === 'ADMIN')) {"),
  ('M13 /qualify admits ADMIN as platform', RF, QUAL_IF, "if (!(isPlatformRole((req as any).user?.role) || (req as any).user?.role === 'ADMIN')) {"),
  ('M14 /qualify admits any principal with a role', RF, QUAL_IF, "if (!(req as any).user?.role) {"),
  ('M15 /qualify admits the referee (body userId === caller)', RF, QUAL_IF, "if (!isPlatformRole((req as any).user?.role) && (req as any).user?.userId !== req.body?.userId) {"),
  ('M16 /qualify lets no principal through', RF, QUAL_IF, "if ((req as any).user && !isPlatformRole((req as any).user?.role)) {"),
  ('M17 /check lets no principal through', MS, CHK_IF, "if ((req as any).user && !isOwner && !isPlatformRole(caller.role as string | undefined)) {"),
  ('M18 /check role trimmed', MS, CHK_IF, "if (!isOwner && !isPlatformRole(typeof caller.role === 'string' ? caller.role.trim() : (caller.role as any))) {"),
  ('M19 /check 403 -> 401', MS, "return res.status(403).json({ success: false, error: { code: 'FORBIDDEN', message: 'Not authorised' } });\n    }\n\n    // Get qualified", "return res.status(401).json({ success: false, error: { code: 'FORBIDDEN', message: 'Not authorised' } });\n    }\n\n    // Get qualified"),
  ('M20 /qualify guard moved after the body parse', RF, None, None),
]
def run(name):
  if os.path.exists(OUTJ): os.replace(OUTJ, OUTJ + '.prev')
  r = subprocess.run(['node', W + '/scripts/vt.cjs', *TESTS, '--reporter=json', '--outputFile=' + OUTJ], capture_output=True, text=True, timeout=600)
  try: j = json.load(open(OUTJ))
  except Exception as e: return {'name': name, 'rc': r.returncode, 'error': 'no json ' + str(e)}
  fails = []
  for f in j['testResults']:
    for a in f['assertionResults']:
      if a['status'] != 'passed':
        msg = (a.get('failureMessages') or [''])[0].split('\n')[0][:110]
        fails.append((a['title'][:90], msg))
  kinds = sorted({m.split(':')[0] for _, m in fails})
  return {'name': name, 'rc': r.returncode, 'total': j['numTotalTests'], 'failed': j['numFailedTests'], 'passed': j['numPassedTests'], 'kinds': kinds, 'fails': fails}
res = []
try:
  res.append(run('HEAD (unmutated)'))
  # RED: base route files
  for p, rel in ((MS, 'routes/milestones.ts'), (RF, 'routes/referrals.ts')):
    open(p, 'w').write(subprocess.run(['git', '-C', W + '/repo', 'show', '66cbe4e52d5afadc9d13ca141200026cc68d5095:' + REL + '/src/' + rel], capture_output=True, text=True).stdout)
  res.append(run('RED: both route files at base'))
  for p in orig: open(p, 'w').write(orig[p])
  for name, path, a, b in M:
    s = orig[path] if path else None
    if name.startswith('M20'):
      path = RF; s = orig[RF]
      guard = "    if (!isPlatformRole((req as any).user?.role)) {\n      return res.status(403).json({ success: false, error: { code: 'FORBIDDEN', message: 'Not authorised' } });\n    }\n"
      parse = "    const { userId } = qualifyReferralSchema.parse(req.body);\n"
      assert s.count(guard) == 1 and s.count(parse) == 1, name
      new = s.replace(guard, '').replace(parse, parse + guard)
    else:
      assert s.count(a) == 1, (name, s.count(a))
      new = s.replace(a, b)
    open(path, 'w').write(new)
    out = run(name); res.append(out)
    open(path, 'w').write(orig[path])
    print(f"{name}: failed {out.get('failed')}/{out.get('total')} kinds={out.get('kinds')}", flush=True)
finally:
  for p in orig: open(p, 'w').write(orig[p])
  ok = all(sha(p) == osha[p] for p in orig)
  res.append({'restore': 'OK' if ok else 'FAIL'})
  json.dump(res, open(W + '/logs/mutants.json', 'w'), indent=1)
  print('restore', 'OK' if ok else 'FAIL')
