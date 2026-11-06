// Gate 210 Q4 re-run of S2, S3 (first forms were inadmissible: TS6133 unused import under tsc), and O3 with a middle-position row.
import fs from 'node:fs'; import crypto from 'node:crypto'; import { spawnSync } from 'node:child_process'; import path from 'node:path';
const G = process.argv[2], OUT = process.argv[3], TABLE = process.argv[4];
const sha = (f) => crypto.createHash('sha256').update(fs.readFileSync(f)).digest('hex');
const PRED = path.join(G, 'src/services/connectorAllowList.ts'), HEALTH = path.join(G, 'src/services/health.ts'), VER = path.join(G, 'src/routes/verification.ts');
const GUARD = 'if (Array.isArray(rawAllowedTypes) && allowListHoldsANonString(rawAllowedTypes)) {';
const CONST = 'message: CONNECTOR_ALLOW_LIST_NOT_ALL_STRINGS_MESSAGE } });';
const OLDT = "'Connector document-type allow-list is not a list; refusing until it is corrected'";
const M = [
 { id:'S2b', f:VER, from:GUARD, to:'if ((false as boolean) && Array.isArray(rawAllowedTypes) && allowListHoldsANonString(rawAllowedTypes)) {', want:['G6','R2','R3','R4'] },
 { id:'S3b', f:HEALTH, from:CONST, to:`message: [${OLDT}, CONNECTOR_ALLOW_LIST_NOT_ALL_STRINGS_MESSAGE][0] } });`, want:['G6','R1','R4'] },
];
const res = [];
for (const m of M) {
  const s0 = sha(m.f); const orig = fs.readFileSync(m.f, 'utf8');
  if (orig.split(m.from).length !== 2) throw new Error('not unique ' + m.id);
  fs.writeFileSync(m.f, orig.replace(m.from, () => m.to));
  const t = spawnSync('npx', ['tsc','--noEmit','-p','.'], { cwd:G, encoding:'utf8' });
  const jf = OUT + '/mut_' + m.id + '.json';
  spawnSync('npx', ['vitest','run','src/__tests__/ks1534','src/__tests__/ks1232','src/__tests__/ks1531','--reporter=json','--outputFile='+jf], { cwd:G, encoding:'utf8' });
  const r = JSON.parse(fs.readFileSync(jf));
  const red = []; for (const f of r.testResults) for (const a of f.assertionResults) if (a.status === 'failed') { const c = /KS-1534 ([A-Z]\d)/.exec(a.title); red.push(c ? c[1] : path.basename(f.name)+'::'+a.title); }
  fs.writeFileSync(m.f, orig);
  res.push({ id:m.id, tscRc:t.status, tscOut:(t.stdout||'').slice(0,200), tests:r.numTotalTests, red:[...new Set(red)].sort(), want:m.want, restored: sha(m.f) === s0 });
}
// What O3 admits: real routes, a middle-position non-string, on the unmutated head and under O3.
const FOR = "for (let i = 0; i < list.length; i += 1) {\n    if (typeof list[i] !== 'string') return true;\n  }\n  return false;";
const O3 = "return list.length > 0 && (typeof list[0] !== 'string' || typeof list[list.length - 1] !== 'string');";
const tf = path.join(G, 'src/__tests__/gate210-table.test.ts');
fs.writeFileSync(tf, fs.readFileSync(TABLE, 'utf8').replace("// gate's own extras, beyond the commission's 17", `["MIDDLE ['SSD_DOCUMENT',1,'X']", ['SSD_DOCUMENT', 1, 'X'], 'nonstring'],`));
const runTable = (name) => { const o = OUT + '/q4_table_' + name + '.json'; spawnSync('npx', ['vitest','run','src/__tests__/gate210-table.test.ts'], { cwd:G, encoding:'utf8', env:{...process.env, G210_OUT:o} }); const row = JSON.parse(fs.readFileSync(o)).find((x) => x.label.startsWith('MIDDLE')); return { name, info:[row.info.status,row.info.message,row.info.echoed], postNamed:[row.postNamed.status,row.postNamed.message,row.postNamed.enforced] }; };
res.push(runTable('head'));
const s0 = sha(PRED); const orig = fs.readFileSync(PRED,'utf8'); if (orig.split(FOR).length !== 2) throw new Error('FOR');
fs.writeFileSync(PRED, orig.replace(FOR, () => O3)); res.push(runTable('O3')); fs.writeFileSync(PRED, orig); res.push({ O3restored: sha(PRED) === s0 });
fs.renameSync(tf, OUT + '/../probe/parked/gate210-table.test.ts.middle-copy');
console.log(res.map((x) => JSON.stringify(x)).join('\n'));
