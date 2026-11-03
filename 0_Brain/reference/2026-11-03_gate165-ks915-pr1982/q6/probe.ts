import { checkPasswordStrength, minLengthForRole } from './policy.ts';
import { readFileSync } from 'node:fs';
// reads generated values from the gate's scratch .env files; prints only verdicts
const files = process.argv.slice(2);
let n = 0, strongDefault = 0, strongAdmin = 0; const cats = new Set<string>(); let minLen = 1e9, maxLen = 0;
for (const f of files) {
  const line = readFileSync(f, 'utf8').split('\n').find(l => l.startsWith('ADMIN_USER_PASSWORD='));
  if (!line) continue; const v = line.slice('ADMIN_USER_PASSWORD='.length); if (!v) continue;
  n++; minLen = Math.min(minLen, v.length); maxLen = Math.max(maxLen, v.length);
  cats.add([/[a-z]/.test(v)?'lower':'', /[A-Z]/.test(v)?'upper':'', /[0-9]/.test(v)?'digit':'', /[^a-zA-Z0-9]/.test(v)?'special':''].filter(Boolean).join('+'));
  if (checkPasswordStrength(v).isStrong) strongDefault++;
  if (checkPasswordStrength(v, { minLength: minLengthForRole('SYSTEM_ADMIN') }).isStrong) strongAdmin++;
}
console.log(JSON.stringify({ values: n, minLen, maxLen, classSets: [...cats], isStrong_default: strongDefault, isStrong_SYSTEM_ADMIN_min14: strongAdmin, bcrypt72ByteLimitOk: maxLen <= 72 }));
// control: the suite's own STRONG-shaped sample from the policy tests
console.log('control Str0ngP@ssw0rd! isStrong=' + checkPasswordStrength('Str0ngP@ssw0rd!').isStrong + ' ; control 48 hex-shaped "ab"*24 isStrong=' + checkPasswordStrength('a1'.repeat(24)).isStrong);
