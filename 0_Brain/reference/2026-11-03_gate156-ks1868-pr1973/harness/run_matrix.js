'use strict';
// Runs cell.js for every (version x site x kind) in its own process; writes logs/matrix.json + a table.
const { spawnSync } = require('child_process');
const fs = require('fs');
const path = require('path');
const H = __dirname;
const W = path.resolve(H, '..');
const KINDS = ['ordinaryError', 'plainString', 'number42', 'null', 'undefined', 'revokedProxy', 'messageGetterThrows', 'symbolMessage',
  'objToStringThrows', 'messageToStringThrows', 'bigintMessage', 'messageToJSONThrows', 'messageIsRevokedProxy'];
const SITES = ['pool', 'hookBoot', 'hookRecovery'];
const out = [];
for (const site of SITES) for (const kind of KINDS) for (const version of ['base', 'head']) {
  const r = spawnSync(process.execPath, [path.join(H, 'cell.js'), version, site, kind], { cwd: path.join(W, 'logs/cwd'), encoding: 'utf8', timeout: 20000 });
  const line = (r.stdout || '').split('\n').find((l) => l.startsWith('G156REC '));
  const rec = line ? JSON.parse(line.slice(8)) : { version, site, kind };
  rec.status = r.status;
  rec.stderrFirst = (r.stderr || '').split('\n').filter(Boolean).slice(0, 3).join(' | ').slice(0, 300);
  out.push(rec);
}
fs.writeFileSync(path.join(W, 'logs/matrix.json'), JSON.stringify(out, null, 1));
const hookMsg = (r, msg) => (r.logs || []).filter((l) => l.message === msg).map((l) => `${l.errorType}:${l.error}`).join(',') || '-';
const rows = [];
for (const r of out) {
  const msg = r.site === 'pool' ? 'DB pool unexpected error' : 'DB ready boot work failed';
  const thenEv = (r.events || []).find((e) => e && typeof e === 'object' && 'then' in e);
  rows.push([r.site, r.kind, r.version, `exit=${r.status}`, r.alive ? 'alive' : 'DEAD', `flag=${r.flagAfter}`,
    `then=${thenEv ? thenEv.then : '-'}`, `emitRet=${(r.events || []).includes('emit returned')}`,
    `wallet=${r.walletRead ? (r.walletRead.ok ? 'read:' + r.walletRead.value : 'throw') : '-'}`, `log=${hookMsg(r, msg)}`,
    r.alive ? '' : `stderr=${r.stderrFirst}`].join('\t'));
}
fs.writeFileSync(path.join(W, 'logs/matrix.tsv'), rows.join('\n') + '\n');
console.log(rows.join('\n'));
