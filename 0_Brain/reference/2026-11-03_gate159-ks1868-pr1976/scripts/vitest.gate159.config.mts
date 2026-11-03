// Gate 159: the service's own vitest config, plus aliases that point @secuura/shared (and its subpath exports) at a
// fresh build of packages/shared from this PR's tree (tree edf16d9a, identical at base, head and develop), because the
// checkout's installed shared dist is stale (missing boundedJson, zod3-compat, emitter exports).
import { defineConfig, mergeConfig } from 'vitest/config';
import * as path from 'node:path';
import * as fs from 'node:fs';
import base from './vitest.config';

const DIST = '/Volumes/DevMASTER/WEDNESDAY/0_Brain/reference/2026-11-03_gate159-ks1868-pr1976/wt_head/Blockchain/Dev/packages/shared/dist_gate159';
const PKG = '/Volumes/DevMASTER/WEDNESDAY/0_Brain/reference/2026-11-03_gate159-ks1868-pr1976/wt_head/Blockchain/Dev/packages/shared/package.json';
const exportsMap = JSON.parse(fs.readFileSync(PKG, 'utf8')).exports as Record<string, string>;
const alias = Object.entries(exportsMap)
  .sort((a, b) => b[0].length - a[0].length)
  .map(([k, v]) => ({
    find: new RegExp('^@secuura/shared' + (k === '.' ? '' : k.slice(1)).replace(/[/.-]/g, (c) => '\\' + c) + '$'),
    replacement: path.join(DIST, v.replace(/^\.\/dist\//, '')),
  }));

export default mergeConfig(base, defineConfig({
  resolve: { alias },
}));
