// Independent scan: every tracked package-lock.json at a given sha, every @azure/msal-node entry, vulnerable range >=5.0.0-beta.0 <7.1.0
import { execFileSync } from 'node:child_process';
import { createRequire } from 'node:module';
const [,, repo, sha, semverDir] = process.argv;
const require = createRequire(semverDir + '/');
const semver = require('semver');
const files = execFileSync('git', ['-C', repo, 'ls-tree', '-r', '--name-only', sha], {maxBuffer: 1<<26}).toString().split('\n').filter(f => f.endsWith('package-lock.json'));
let vuln = 0, copies = 0;
for (const f of files) {
  const j = JSON.parse(execFileSync('git', ['-C', repo, 'show', `${sha}:${f}`], {maxBuffer: 1<<28}));
  const hits = Object.entries(j.packages || {}).filter(([k]) => k.endsWith('node_modules/@azure/msal-node'));
  for (const [k, e] of hits) {
    copies++;
    const v = semver.satisfies(e.version, '>=5.0.0-beta.0 <7.1.0', { includePrerelease: true });
    if (v) vuln++;
    console.log(`${v ? 'VULN' : 'ok  '} ${f} :: ${k} ${e.version}`);
  }
}
console.log(`locks=${files.length} msal-node copies=${copies} vulnerable=${vuln}`);
