// FAIL conditions, stated before any run (Q3): see verdict. Reads base + head JSON, prints the table and "N of M".
import fs from 'node:fs';
const [bp, hp] = process.argv.slice(2);
const B = JSON.parse(fs.readFileSync(bp)), H = JSON.parse(fs.readFileSync(hp));
const NS = 'Connector document-type allow-list is not a list of strings; refusing until it is corrected';
const NA = 'Connector document-type allow-list is not a list; refusing until it is corrected';
const fmt = (c) => `${c.status} ${c.code ?? '-'} ${c.message ?? ''}${'enforced' in c ? ` enf=${c.enforced}` : ` echo=${c.echoed} calls=${c.calls}`}`;
let bad = 0, n = 0;
const routes = ['info', 'postNamed', 'postOther', 'postUntyped', 'postTypeKey'];
for (let i = 0; i < H.length; i++) {
  const h = H[i], b = B[i];
  const fails = [];
  for (const r of routes) {
    n++;
    const c = h[r], cb = b[r];
    const same = JSON.stringify(c) === JSON.stringify(cb);
    if (h.klass === 'nonstring') {
      const ok = c.status === 403 && c.code === 'FORBIDDEN' && c.message === NS && (r === 'info' ? c.echoed === '(none)' && c.calls === 1 : c.enforced === 0 && c.workflowed === 0);
      if (!ok) fails.push(`${r}: head not refused with constant`);
    } else if (h.klass === 'nonarray') {
      const ok = c.status === 403 && c.message === NA && same;
      if (!ok) fails.push(`${r}: non-array text moved`);
    } else if (!same) fails.push(`${r}: differs from base`);
  }
  // routes disagree?
  if (h.klass === 'nonstring' || h.klass === 'nonarray') {
    if (h.info.message !== h.postNamed.message) fails.push('routes disagree');
  }
  bad += fails.length;
  console.log(`\n## ${h.label} [${h.klass}]${fails.length ? '  **FAIL: ' + fails.join('; ') + '**' : ''}`);
  for (const r of routes) console.log(`  ${r.padEnd(11)} BASE ${fmt(b[r])}\n  ${''.padEnd(11)} HEAD ${fmt(h[r])}`);
}
console.log(`\nRESULT: ${n - bad} of ${n} route-cells as expected; ${bad} failing`);
const adm = B.filter((x) => x.klass === 'nonstring' && x.postNamed.status === 201);
console.log('BASE mixed rows that ADMITTED an SSD_DOCUMENT create (201, enforcement reached):', adm.map((x) => `${x.label} (enf=${x.postNamed.enforced})`).join(' | '));
const admH = H.filter((x) => x.klass === 'nonstring' && [x.postNamed, x.postOther, x.postUntyped, x.postTypeKey].some((c) => c.status !== 403));
console.log('HEAD non-string rows with any create not refused:', admH.length);
