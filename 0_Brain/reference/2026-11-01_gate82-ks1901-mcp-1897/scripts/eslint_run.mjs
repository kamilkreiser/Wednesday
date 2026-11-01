// usage: node eslint_run.mjs <Dev dir> <files...>  (ESLint Node API with cwd set, because the shell may not cd)
import { createRequire } from 'node:module';
const [dev, ...files] = process.argv.slice(2);
const { ESLint } = createRequire(dev + '/package.json')('eslint');
const e = new ESLint({ cwd: dev });
const res = await e.lintFiles(files);
const f = await e.loadFormatter('stylish');
console.log(await f.format(res));
let err = 0, warn = 0; for (const r of res) { err += r.errorCount; warn += r.warningCount; }
console.log(`files=${res.length} errors=${err} warnings=${warn}`);
process.exit(err ? 1 : 0);
