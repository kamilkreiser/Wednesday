// clock_probe.mjs — unit calls on the SHIPPED modules of one tree (argv[2] = <tree>/Blockchain/Dev).
// Prints: the process clock, utcToday(), isLapsed(real entry) and validateOutOfScope(real corpus) outcome.
// Run once per instant with QA_FAKE_NOW + the fakeclock preload; one run without it is the real-clock control.
import { pathToFileURL } from 'node:url';
const dev = process.argv[2];
const bc = await import(pathToFileURL(dev + '/scripts/audit/baseline-contract.mjs').href);
const ld = await import(pathToFileURL(dev + '/scripts/audit/lock-discovery.mjs').href);
const entry = ld.OUT_OF_SCOPE_LOCKS.get('Blockchain/Dev/mobile/secuura-app');
const clock = new Date();
const syd = new Intl.DateTimeFormat('en-AU', { timeZone: 'Australia/Sydney', dateStyle: 'full', timeStyle: 'long' }).format(clock);
let vos = 'passes';
try {
  const { locks } = ld.findTrackedLocks(dev);
  ld.validateOutOfScope(locks);
} catch (e) {
  vos = 'THROWS ' + (/has LAPSED/.test(e.message) ? '(LAPSED)' : e.message.split('\n')[1] || e.message);
}
console.log(
  JSON.stringify({
    fake: process.env.QA_FAKE_NOW || null,
    clock: clock.toISOString(),
    sydney: syd,
    utcToday: bc.utcToday(),
    expires: entry.expires,
    isLapsed: bc.isLapsed(entry),
    validateOutOfScope: vos,
  }),
);
