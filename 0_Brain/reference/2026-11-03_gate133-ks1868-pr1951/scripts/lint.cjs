// usage: node lint.cjs <cwd> files... ; ESLint API with cwd set (no shell cd)
const [cwd, ...files] = process.argv.slice(2);
process.chdir(cwd);
const { ESLint } = require(require.resolve('eslint', { paths: [cwd] }));
(async () => {
  const eslint = new ESLint({ cwd });
  const res = await eslint.lintFiles(files);
  const f = await eslint.loadFormatter('stylish');
  console.log(f.format(res) || 'no problems');
  const errs = res.reduce((a, r) => a + r.errorCount, 0), warns = res.reduce((a, r) => a + r.warningCount, 0);
  console.log(`files=${res.length} errors=${errs} warnings=${warns}`);
  process.exit(errs ? 1 : 0);
})();
