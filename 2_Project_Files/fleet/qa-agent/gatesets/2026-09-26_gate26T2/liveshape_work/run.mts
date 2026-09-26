import { readFileSync, readdirSync, statSync } from 'node:fs';
import { join, basename } from 'node:path';
const { readChildOutput } = await import(process.argv[2]);
const ev = process.argv[3];
const table = readFileSync(join(ev, 'evidence/liveshape/13_L2_table.md'), 'utf8').split('\n').filter(l => l.startsWith('| ') && !l.startsWith('| shape') );
const oracle = {}; for (const l of table) { const c = l.split('|').map(x => x.trim()); oracle[c[1]] = c[c.length - 4]; }
// ^ the oracle column is read from the ROW'S END: a Tests line carries its own pipes
const files = {};
const walk = d => { for (const n of readdirSync(d)) { const p = join(d, n); const s = statSync(p); if (s.isDirectory()) walk(p); else if (n.endsWith('.stdout')) { const k = basename(n, '.stdout'); if (k in oracle && !(k in files)) files[k] = p; } } };
walk(ev);
const fmt = r => r === null ? 'NULL' : `{${r.passed},${r.failed}}`;
let wrong = 0, n = 0;
for (const k of Object.keys(oracle)) {
  if (!files[k]) { console.log(`${k.padEnd(10)} NO CAPTURE FOUND`); continue; }
  const got = fmt(readChildOutput(readFileSync(files[k], 'utf8'))); n++;
  const ok = got === oracle[k]; if (!ok) wrong++;
  console.log(`${k.padEnd(10)} round3=${got.padEnd(6)} oracle=${oracle[k].padEnd(6)} ${ok ? 'PASS' : 'WRONG'}`);
}
console.log(`REAL CAPTURES: ${n} read, ${wrong} WRONG`);
// SYNTHETIC (drafter-composed; the gate must capture each LIVE before it counts under the rule)
const blk = (p, f, t) => ` Test Files  ${f}\n      Tests  ${t}\n   Start at  04:30:01\n   Duration  130ms (transform 8ms)\n`;
const real = readFileSync(files['S14'], 'utf8');
const syn = {
  'SYN-H1s killed after a lookalike INCLUDING Start at (stdout only; childSuiteCounts refuses on status 143)': '\n RUN  v4.1.11 /x\n\nstdout | a.test.ts > lookalike\n' + blk(0, '1 passed (1)', '7 passed (7)'),
  'SYN-H4s process.on(exit) writes a COMPLETE lookalike AFTER vitest\'s real block (status 1, NOT refused)': real + blk(0, '1 passed (1)', '7 passed (7)'),
  'SYN-H4t exit-hook writes only `   Start at  hh:mm:ss` after the real block': real + '   Start at  04:30:09\n',
  'SYN-ERRLINE an `Errors  1 error` line between Tests and Start at': '\n Test Files  1 passed (1)\n      Tests  2 passed (2)\n     Errors  1 error\n   Start at  04:30:01\n',
  'SYN-TYPEERR a `Type Errors  1 error` line between Tests and Start at': '\n Test Files  1 passed (1)\n      Tests  2 passed (2)\n Type Errors  1 error\n   Start at  04:30:01\n',
  'SYN-CRLF the real S14 block with CRLF line ends': real.replace(/\n/g, '\r\n'),
};
for (const [k, v] of Object.entries(syn)) console.log(`${fmt(readChildOutput(v)).padEnd(6)} ${k}`);
