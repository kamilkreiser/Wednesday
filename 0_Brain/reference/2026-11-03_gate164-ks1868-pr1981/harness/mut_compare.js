// G164: per mutant, recorder cells vs (a) the base+ordinaryError STATE reference and (b) head's logged text for the same kind/env/site.
const fs = require('fs'); const W = require('path').resolve(__dirname, '..');
const all = JSON.parse(fs.readFileSync(W + '/logs/matrix_all.json'));
const M = JSON.parse(fs.readFileSync(W + '/logs/mutants.json'));
const F = { route: ['rotateStatus','newKeyIssued','hasPKR','priorKeysRevoked','newKeyValid','newRowActive','priorValidAfterInProcess','priorRowActive','activeRows','died','mainError'], direct: ['directOutcome','priorInMemoryActive','priorValidAfterInProcess','priorRowActive','activeRows','died','mainError'] };
const st = (c) => F[c.site].map((f) => JSON.stringify(c[f])).join('|');
const txt = (c) => JSON.stringify((c.failLines || []).map((l) => l.error));
for (const [id, r] of Object.entries(M)) {
  const cells = JSON.parse(fs.readFileSync(r.matrix));
  let stateDiff = [], textDiff = [];
  for (const c of cells) {
    const ref = all.find((x) => x.version === 'base' && x.kind === 'ordinaryError' && x.site === c.site && x.env === c.env);
    const hd = all.find((x) => x.version === 'head' && x.kind === c.kind && x.site === c.site && x.env === c.env);
    if (st(c) !== st(ref)) stateDiff.push(`${c.env[0]}:${c.kind}`);
    else if (txt(c) !== txt(hd)) textDiff.push(`${c.env[0]}:${c.kind}=${txt(c)} (head ${txt(hd)})`);
  }
  console.log(`${id} tests: ${r.tests_failed.length}/${r.tests_total} failed | recorder ${cells.length} cells: state!=ref ${stateDiff.length} [${stateDiff.filter(s=>s.startsWith('d')).join(',')}] | text!=head ${textDiff.length} ${textDiff.filter(s=>s.startsWith('d')).slice(0,4).join('; ')}`);
}
