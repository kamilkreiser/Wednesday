// fuseproof_gate42b.mjs — the drafter's OFFLINE predicate proof (NOT leg 6/7: no advisory is fetched). It imports the REPO's OWN
// baseline-contract.mjs (extracted from the head commit by `git show`, passed as argv[2]) and prints, for one baseline file (argv[3]), utcToday()
// as the contract computes it and every row isLapsed() would call LAPSED at that instant — i.e. the rows that CAN lapse; the real legs lapse only
// the subset that is also REPORTED. argv[4] (optional) is the EXPECTED lapse set, comma-joined ('' = none): rc 0 iff it matches, rc 1 otherwise.
// Run under clockfreeze_gate42b.mjs to move the clock. Usage: node [--import clockfreeze] fuseproof_gate42b.mjs <contract.mjs> <baseline.json> [expected]
import { readFileSync } from 'node:fs';
import { pathToFileURL } from 'node:url';
const [contract, baseline, expected] = process.argv.slice(2);
const { utcToday, isLapsed } = await import(pathToFileURL(contract).href);
const acc = JSON.parse(readFileSync(baseline, 'utf8')).accepted ?? {};
const today = utcToday();
const lapsed = Object.keys(acc).filter((id) => isLapsed(acc[id], today)).sort();
console.log(`utcToday ${today} | rows ${Object.keys(acc).length} checked | can-lapse ${lapsed.length}: ${lapsed.map((id) => `${id} (${acc[id].ticket}, expires ${acc[id].expires})`).join(', ') || 'none'}`);
if (expected !== undefined) {
  const want = expected === '' ? [] : expected.split(',').sort();
  const ok = Object.keys(acc).length > 0 && JSON.stringify(want) === JSON.stringify(lapsed);
  console.log(`${ok ? 'MATCH' : 'NO MATCH'}: expected ${want.join(',') || 'none'}`);
  process.exit(ok ? 0 : 1);
}
