// c3_probe_gate56a.mjs — gate56a C3 probe: imports the REAL modules of ONE side (an extracted scripts/audit dir) and asks them, under the
// clock c3_freeze_clock_gate56a.mjs pinned, whether each fuse has lapsed. Prints ONE JSON line to stdout. Writes nothing.
//   baseline <auditDir>          : today = utcToday(); for every `accepted` row, isLapsed(entry, today) — the exact pair audit-gate.mjs:191/:197
//                                  and audit-locks.mjs:283/:289 use. Output {mode, today, lapsed:[ids], expires:{id:date}}.
//   lockdisc <auditDir> <locks>  : validateOutOfScope(<locks JSON array>) with the module's own OUT_OF_SCOPE_LOCKS — the call
//                                  findStandaloneLockDirs makes (lock-discovery.mjs:312) for leg 7, and the leg-5 contract case makes.
//                                  Output {mode, today, threw, lapsed (message names `has LAPSED`), message, entries:[[dir, expires]]}.
//   clock                        : {today: utcToday-equivalent of new Date(), now: Date.now()} — the clock self-test.
import { readFileSync } from 'node:fs';
import { pathToFileURL } from 'node:url';
import { join } from 'node:path';

const [mode, dir, locksFile] = process.argv.slice(2);
const out = (o) => process.stdout.write(JSON.stringify(o) + '\n');
if (mode === 'clock') {
  out({ mode, today: new Date().toISOString().slice(0, 10), iso: new Date().toISOString(), now: Date.now() });
} else if (mode === 'baseline') {
  const bc = await import(pathToFileURL(join(dir, 'baseline-contract.mjs')).href);
  const acc = JSON.parse(readFileSync(join(dir, 'audit-baseline.json'), 'utf8')).accepted ?? {};
  const today = bc.utcToday();
  const lapsed = Object.keys(acc).filter((id) => bc.isLapsed(acc[id], today));
  const expires = Object.fromEntries(Object.entries(acc).filter(([, e]) => e.expires).map(([id, e]) => [id, e.expires]));
  out({ mode, today, lapsed, expires, rows: Object.keys(acc).length });
} else if (mode === 'lockdisc') {
  const ld = await import(pathToFileURL(join(dir, 'lock-discovery.mjs')).href);
  const bc = await import(pathToFileURL(join(dir, 'baseline-contract.mjs')).href);
  const locks = JSON.parse(readFileSync(locksFile, 'utf8'));
  let threw = false;
  let message = '';
  try {
    ld.validateOutOfScope(locks);
  } catch (e) {
    threw = true;
    message = String(e.message);
  }
  out({
    mode,
    today: bc.utcToday(),
    threw,
    lapsed: /has LAPSED/.test(message),
    message: message.slice(0, 400),
    entries: [...ld.OUT_OF_SCOPE_LOCKS].map(([d, e]) => [d, e.expires]),
    locks: locks.length,
  });
} else {
  console.error('usage: c3_probe_gate56a.mjs clock | baseline <auditDir> | lockdisc <auditDir> <locks.json>');
  process.exit(2);
}
