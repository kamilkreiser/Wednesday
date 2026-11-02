const { spawnSync } = require('child_process'); const fs = require('fs');
const G = '/Volumes/DevMASTER/WEDNESDAY/0_Brain/reference/2026-11-03_gate141-ks1868-pr1957';
const D = G + '/repo/Blockchain/Dev', B = D + '/node_modules/.bin';
fs.mkdirSync(G + '/logs/_quarantine', { recursive: true });
for (const s of ['nft-certificate','transfer','wallet-connector','m365-integration','staking']) {
  const A = D + '/services/' + s;
  const news = fs.readdirSync(A + '/src/__tests__').filter((f) => f.startsWith('ks1868-') && /db-pool/.test(f)).map((f) => 'src/__tests__/' + f);
  const r = spawnSync(B + '/eslint', ['src/db.ts', ...news], { cwd: A, encoding: 'utf8' });
  fs.writeFileSync(G + '/logs/eslint_' + s + '.log', (r.stdout || '') + (r.stderr || '') + '\nfiles=' + ['src/db.ts', ...news].join(',') + '\nrc=' + r.status + '\n');
  console.log(s, 'eslint rc', r.status, news.length + 1, 'files');
  const pl = A + '/src/zz_g141_planted.ts';
  fs.writeFileSync(pl, 'export function f(): number { const unused = 1; debugger; return 2; }\n');
  const p = spawnSync(B + '/eslint', ['src/zz_g141_planted.ts'], { cwd: A, encoding: 'utf8' });
  fs.writeFileSync(G + '/logs/eslint_planted_' + s + '.log', (p.stdout || '') + (p.stderr || '') + '\nrc=' + p.status + '\n');
  fs.renameSync(pl, G + '/logs/_quarantine/zz_g141_planted_' + s + '.ts');
  console.log(s, 'planted rc', p.status);
}
