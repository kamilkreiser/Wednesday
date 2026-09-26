import { readFileSync, readdirSync } from 'node:fs'; import { join } from 'node:path';
const [,, r2, r3, F] = process.argv;
const A = (await import(r2)).readChildOutput, B = (await import(r3)).readChildOutput;
const fmt = r => r === null ? 'NULL' : `{${r.passed},${r.failed}}`;
for (const s of readdirSync(F).filter(x => !x.includes('.')).sort()) {
  const o = JSON.parse(readFileSync(join(F, s, 'oracle.json'), 'utf8')); const out = readFileSync(join(F, s, 'stdout.txt'), 'utf8');
  console.log(`${s}: oracle {${o.numPassedTests},${o.numFailedTests}} | round2 ${fmt(A(out))} | round3 ${fmt(B(out))}`);
}
