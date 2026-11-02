// usage: node eslint_run.cjs <DevDir> <file...> ; runs ESLint with cwd = DevDir (flat config is cwd-relative)
const dev = process.argv[2]; process.chdir(dev);
const { ESLint } = require(dev + '/node_modules/eslint');
(async () => {
  const e = new ESLint({ cwd: dev });
  const res = await e.lintFiles(process.argv.slice(3));
  const f = await e.loadFormatter('stylish');
  console.log(f.format(res) || 'no problems');
  const errs = res.reduce((a, r) => a + r.errorCount, 0), warns = res.reduce((a, r) => a + r.warningCount, 0);
  console.log('files', res.length, 'errors', errs, 'warnings', warns, 'ignored', res.filter(r => r.messages.some(m => /ignored/i.test(m.message))).length);
  process.exit(errs ? 1 : 0);
})();
