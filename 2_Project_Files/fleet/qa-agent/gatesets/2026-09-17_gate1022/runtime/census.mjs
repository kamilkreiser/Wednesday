// census.mjs — preload (--import): records EVERY resolved module URL of this process (ESM and CJS) to $CENSUS_OUT via module.registerHooks.
import { registerHooks } from 'node:module';
import fs from 'node:fs';
const out = process.env.CENSUS_OUT;
fs.appendFileSync(out, `# census pid ${process.pid} argv ${JSON.stringify(process.argv.slice(1))}\n`);
registerHooks({ resolve(spec, ctx, next) { const r = next(spec, ctx); try { fs.appendFileSync(out, r.url + '\n'); } catch {} return r; } });
