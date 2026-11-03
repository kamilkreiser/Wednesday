// ESLint API with cwd = Blockchain/Dev so the flat config there applies. argv: files...
const path = require('path');
const DEV = path.resolve(__dirname, '../repo/Blockchain/Dev');
const { ESLint } = require(path.join(DEV, 'node_modules/eslint'));
(async () => {
  const e = new ESLint({ cwd: DEV });
  const res = await e.lintFiles(process.argv.slice(2));
  let errs = 0, warns = 0;
  for (const r of res) for (const m of r.messages) { console.log(path.relative(DEV, r.filePath) + ':' + m.line + ' ' + (m.severity === 2 ? 'error' : 'warn') + ' ' + (m.ruleId || '-') + ' ' + m.message); m.severity === 2 ? errs++ : warns++; }
  console.log(`files=${res.length} errors=${errs} warnings=${warns}`);
  process.exitCode = errs ? 1 : 0;
})();
