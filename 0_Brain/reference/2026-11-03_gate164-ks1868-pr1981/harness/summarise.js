// G164: compare every cell's END STATE with base+ordinaryError for the same (env, site). argv: matrix.json [refVersion=base]
const fs = require('fs');
const [file, refV = 'base'] = process.argv.slice(2);
const cells = JSON.parse(fs.readFileSync(file, 'utf8'));
const STATE = { route: ['rotateStatus', 'newKeyIssued', 'hasPKR', 'priorKeysRevoked', 'newKeyValid', 'newRowActive', 'priorValidAfterInProcess', 'priorRowActive', 'activeRows', 'died', 'mainError'],
  direct: ['directOutcome', 'priorInMemoryActive', 'priorValidAfterInProcess', 'priorRowActive', 'activeRows', 'died', 'mainError'] };
const siteOf = (s) => s.replace(/Up$/, '');
const st = (c) => STATE[siteOf(c.site)].map((f) => `${f}=${JSON.stringify(c[f])}`).join(' ');
const refs = {};
for (const c of cells) if (c.version === refV && c.kind === 'ordinaryError' && !/Up$/.test(c.site)) refs[c.env + '/' + c.site] = c;
const lines = []; const tally = {};
for (const c of cells) {
  if (c.noResult) { lines.push(`NORESULT ${c.version} ${c.env} ${c.site} ${c.kind} ${c.stderr}`); continue; }
  const ref = refs[c.env + '/' + siteOf(c.site)];
  const same = !/Up$/.test(c.site) && st(c) === st(ref);
  const logged = (c.failLines || []).map((l) => l.error ?? l.raw);
  // permissive: a credential valid in this cell that is not valid in the reference
  const valid = (x) => (x.newKeyValid === true ? 1 : 0) + (x.priorValidAfterInProcess === true ? 1 : 0) + (x.priorRowActive === true ? 1 : 0);
  const more = !/Up$/.test(c.site) && (valid(c) > valid(ref) || (c.activeRows ?? 0) > (ref.activeRows ?? 0));
  const key = `${c.version} ${c.env} ${c.site}`;
  tally[key] = tally[key] || { cells: 0, eqRef: 0, morePermissive: 0, died: 0, loggedText: 0, faultFired: 0 };
  const t = tally[key]; t.cells++; if (same) t.eqRef++; if (more) t.morePermissive++; if (c.died) t.died++; if (logged.length === 1 && typeof logged[0] === 'string') t.loggedText++; if (c.faultFired > 0) t.faultFired++;
  lines.push(`${same ? 'EQ ' : /Up$/.test(c.site) ? 'CTL' : 'DIF'}${more ? ' MORE-PERMISSIVE' : ''}\t${c.version}\t${c.env}\t${c.site}\t${c.kind}\t${st(c)}\tlogged=${JSON.stringify(logged)}\tfault=${c.faultFired}\texit=${c.exit}`);
}
console.log(lines.join('\n'));
console.log('\nTALLY (reference = ' + refV + ' + ordinaryError, same env and site)');
for (const [k, t] of Object.entries(tally)) console.log(k.padEnd(32), JSON.stringify(t));
