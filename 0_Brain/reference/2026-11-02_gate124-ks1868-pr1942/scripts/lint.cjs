// usage: node lint.cjs <cwd> <file...> ; ESLint API with an explicit cwd (no shell cd)
const path = require('path');
const [cwd, ...files] = process.argv.slice(2);
const { ESLint } = require('/Volumes/DevMASTER/WEDNESDAY/0_Brain/reference/2026-11-02_gate124-ks1868-pr1942/repo/Blockchain/Dev/node_modules/eslint');
(async () => {
  const eslint = new ESLint({ cwd });
  const res = await eslint.lintFiles(files);
  const f = await eslint.loadFormatter('stylish');
  console.log(f.format(res) || 'NO PROBLEMS');
  let e = 0, w = 0, ign = 0; for (const r of res) { e += r.errorCount; w += r.warningCount; ign += r.messages.filter((m) => /ignored/.test(m.message)).length; }
  console.log(`files=${res.length} errors=${e} warnings=${w} ignored_msgs=${ign}`);
  process.exit(e ? 1 : 0);
})().catch((x) => { console.error(x); process.exit(2); });
