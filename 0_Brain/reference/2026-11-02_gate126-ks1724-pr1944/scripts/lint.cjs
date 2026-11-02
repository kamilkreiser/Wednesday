// ESLint API with cwd = <tree>/Blockchain/Dev (no shell cd). usage: node lint.cjs <tree> <file...>
const path = require('path');
const tree = process.argv[2]; const D = `/Volumes/DevMASTER/WEDNESDAY/0_Brain/reference/2026-11-02_gate126-ks1724-pr1944/${tree}/Blockchain/Dev`;
const { ESLint } = require(path.join(D, 'node_modules/eslint'));
(async () => {
  const eslint = new ESLint({ cwd: D });
  const files = process.argv.slice(3);
  const res = await eslint.lintFiles(files);
  let e = 0, w = 0, ignored = 0;
  for (const r of res) { e += r.errorCount; w += r.warningCount; if (r.messages.some(m => /ignored/i.test(m.message))) ignored++; for (const m of r.messages) console.log(path.relative(D, r.filePath), m.line, m.severity === 2 ? 'error' : 'warn', m.ruleId, m.message); }
  console.log(`files ${res.length} errors ${e} warnings ${w} ignored ${ignored}`);
  process.exit(e ? 1 : 0);
})().catch(err => { console.error(err); process.exit(2); });
