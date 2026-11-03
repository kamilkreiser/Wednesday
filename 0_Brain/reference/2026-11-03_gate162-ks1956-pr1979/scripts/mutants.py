#!/usr/bin/env python3
# Gate 162 mutants on milestoneService.ts in MY clone (repo/, at pr1979). PR tests untouched; sha256-restored after each.
# Each mutant runs the two milestone test files the PR touches (ks1956 + ks1868 write-catch) plus the ks1868 read-catch file.
import hashlib, subprocess, sys, re, json
W = '/Volumes/DevMASTER/WEDNESDAY/0_Brain/reference/2026-11-03_gate162-ks1956-pr1979'
T = W + '/repo/Blockchain/Dev/services/referral'
P = T + '/src/services/milestoneService.ts'
TESTS = ['src/__tests__/ks1956-milestone-awarded-once-per-user.test.ts',
         'src/__tests__/ks1868-milestone-service-db-write-catches-unreadable-throw.test.ts',
         'src/__tests__/ks1868-milestone-service-db-read-catches-unreadable-throw.test.ts']
orig = open(P).read(); osha = hashlib.sha256(orig.encode()).hexdigest()
M = [
 ('M1 dedupe id random again (randomUUID)', "id: milestoneRewardId(userId, milestone.id),", "id: require('crypto').randomUUID(),"),
 ('M2 ignore rows already stored (any-status map unused)', "const firstAwardedAt = awarded.get(milestone.id);", "const firstAwardedAt = undefined as Date | undefined;"),
 ('M3 failed progress read = no row (old behaviour)', "      logger.error('DB read user progress failed', { userId, error: reason });\n      return { ok: false };", "      logger.error('DB read user progress failed', { userId, error: reason });\n      return { ok: true, progress: null };"),
 ('M4 failed awarded read = empty map', "      logger.error('DB read awarded milestones failed', { userId, error: reason });\n      return null;", "      logger.error('DB read awarded milestones failed', { userId, error: reason });\n      return new Map();"),
 ('M5 early-return branch removed (only awarded guard kept as optional)', "    if (!read.ok || !awarded) {", "    if (!awarded) {"),
 ('M6 rowCount ignored (conflict answered as new)', "return result?.rowCount === 0 ? 'exists' : 'inserted';", "return 'inserted';"),
 ('M7 failed reward save still awarded', "        if (saved === 'failed') continue;\n", ""),
 ('M8 exists answered as new', "        if (saved === 'exists') continue;\n", ""),
 ('M9 BigInt replacer dropped', "JSON.stringify(progress.milestonesAchieved || [], bigintAsDecimalString)", "JSON.stringify(progress.milestonesAchieved || [])"),
 ('M10 no-DB progress read = no row', "    if (!isDbAvailable()) return { ok: false };", "    if (!isDbAvailable()) return { ok: true, progress: null };"),
 ('M11 awarded read keyed on status (CLAIMABLE only)', "WHERE user_id = $1 AND source_type = $2\n", "WHERE user_id = $1 AND source_type = $2 AND status = 'CLAIMABLE'\n"),
 ('M12 recorded achievedAt = now, not first award time', "          achievedAt: firstAwardedAt,", "          achievedAt: new Date(),"),
 ('M13 recorded total not incremented for stored rows', "        progress.currentTier = milestone.tier;\n        progress.totalMilestoneRewards += milestone.rewardAmount;\n        continue;", "        progress.currentTier = milestone.tier;\n        continue;"),
 ('M14 dedupe id per milestone only (user dropped)', "uuidv5(JSON.stringify([userId, milestoneId]), MILESTONE_REWARD_ID_NAMESPACE)", "uuidv5(JSON.stringify([milestoneId]), MILESTONE_REWARD_ID_NAMESPACE)"),
]
rows = []
for name, a, b in M:
    n = orig.count(a)
    if n != 1:
        rows.append((name, f'NOT APPLIED (anchor count {n})', '')); continue
    open(P, 'w').write(orig.replace(a, b))
    r = subprocess.run(['nice', '-n', '10', 'node', W + '/scripts/vt.cjs', *TESTS], capture_output=True, text=True)
    txt = re.sub(r'\x1b\[[0-9;]*m', '', r.stdout + r.stderr)
    fails = re.findall(r'(?:FAIL|×|✗) .*?((?:RED|control) ks\d+ [A-Z]\d+)', txt)
    summ = (re.findall(r'Tests\s+([^\n]+)', txt) or ['?'])[-1].strip()
    errs = 'TransformError' in txt or 'SyntaxError' in txt or 'Transform failed' in txt
    verdict = 'KILLED' if r.returncode != 0 and not errs else ('ERROR' if errs else 'SURVIVED')
    rows.append((name, verdict, f'rc={r.returncode} {summ} by={sorted(set(fails))}'))
    open(P, 'w').write(orig)
    assert hashlib.sha256(open(P).read().encode()).hexdigest() == osha
open(P, 'w').write(orig)
ok = hashlib.sha256(open(P).read().encode()).hexdigest() == osha
with open(W + '/logs/mutants_table.log', 'w') as f:
    for r in rows: f.write(' | '.join(r) + '\n')
    f.write(f'restore sha256 equal: {ok}\n')
print(open(W + '/logs/mutants_table.log').read())
