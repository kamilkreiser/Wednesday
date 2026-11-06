// Gate 210 Q4. Predictions are written HERE, before any run. Each mutant: apply an exact-string edit, tsc, vitest on the
// ks1534 pair + ks1232 + ks1531 pins, report red cells vs prediction, restore, assert sha256 equal.
import fs from 'node:fs'; import crypto from 'node:crypto'; import { spawnSync } from 'node:child_process'; import path from 'node:path';
const G = process.argv[2], OUT = process.argv[3];
const sha = (f) => crypto.createHash('sha256').update(fs.readFileSync(f)).digest('hex');
const PRED = path.join(G, 'src/services/connectorAllowList.ts'), HEALTH = path.join(G, 'src/services/health.ts'), VER = path.join(G, 'src/routes/verification.ts');
const LOOP = "if (typeof list[i] !== 'string') return true;";
const GUARD = 'if (Array.isArray(rawAllowedTypes) && allowListHoldsANonString(rawAllowedTypes)) {';
const CONST = 'message: CONNECTOR_ALLOW_LIST_NOT_ALL_STRINGS_MESSAGE } });';
const OLD = "message: 'Connector document-type allow-list is not a list; refusing until it is corrected' } });";
const FOR = 'for (let i = 0; i < list.length; i += 1) {';
const M = [
 { id:'S1 predicate checks list[0] only (seat)', f:PRED, from:FOR, to:'for (let i = 0; i < Math.min(list.length, 1); i += 1) {', want:['R1','R2','R3','R4','R5'] },
 { id:'S2 guard off in verification.ts (seat)', f:VER, from:GUARD, to:'if (false as boolean) {', want:['G6','R2','R3','R4'] },
 { id:'S3 health.ts answers the older text (seat)', f:HEALTH, from:CONST, to:OLD, want:['G6','R1','R4'] },
 { id:'S4 predicate uses some() (seat)', f:PRED, from:FOR+'\n    '+LOOP+'\n  }\n  return false;', to:"return list.some((x) => typeof x !== 'string');", want:['R1','R2','R3','R4','R5'] },
 { id:'O1 own: a hole is skipped (i in list)', f:PRED, from:LOOP, to:"if (i in list && typeof list[i] !== 'string') return true;", want:['R1','R2','R3','R4','R5'] },
 { id:'O2 own: null/undefined let through (x == null)', f:PRED, from:LOOP, to:"if (typeof list[i] !== 'string' && list[i] != null) return true;", want:['R1','R2','R3','R4','R5'] },
 { id:'O3 own: first and last element only', f:PRED, from:FOR+'\n    '+LOOP+'\n  }\n  return false;', to:"return list.length > 0 && (typeof list[0] !== 'string' || typeof list[list.length - 1] !== 'string');", want:['R1?','SURVIVOR expected for the middle: no fixture is longer than 2'], note:'holes and last-position shapes are still caught' },
 { id:"O4 own: '' counted as a non-string", f:PRED, from:LOOP, to:"if (typeof list[i] !== 'string' || list[i] === '') return true;", want:['SURVIVOR expected: no cell pins an empty-string element'] },
];
const res = [];
for (const m of M) {
  const s0 = sha(m.f); const orig = fs.readFileSync(m.f, 'utf8');
  if (orig.split(m.from).length !== 2) { res.push({ id:m.id, error:'from-string not unique' }); continue; }
  fs.writeFileSync(m.f, orig.replace(m.from, () => m.to));
  const t = spawnSync('npx', ['tsc','--noEmit','-p','.'], { cwd:G, encoding:'utf8' });
  const jf = OUT + '/mut_' + m.id.split(' ')[0] + '.json';
  spawnSync('npx', ['vitest','run','src/__tests__/ks1534','src/__tests__/ks1232','src/__tests__/ks1531','--reporter=json','--outputFile='+jf], { cwd:G, encoding:'utf8' });
  const r = JSON.parse(fs.readFileSync(jf));
  const red = []; for (const f of r.testResults) for (const a of f.assertionResults) if (a.status === 'failed') { const c = /KS-1534 ([A-Z]\d)/.exec(a.title); red.push(c ? c[1] : path.basename(f.name)+'::'+a.title); }
  fs.writeFileSync(m.f, orig);
  res.push({ id:m.id, tscRc:t.status, tscOut:(t.stdout||'').split('\n').slice(0,3).join(' | ').slice(0,300), tests:r.numTotalTests, red:[...new Set(red)].sort(), want:m.want, restored: sha(m.f) === s0 });
}
fs.writeFileSync(OUT + '/q4_mutants.json', JSON.stringify(res, null, 1));
console.log(res.map((x) => JSON.stringify(x)).join('\n'));
