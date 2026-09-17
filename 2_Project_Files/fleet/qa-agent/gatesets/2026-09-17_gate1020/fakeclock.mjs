// fakeclock.mjs — #1020 (KS-769) drafter clock injection. Loaded with NODE_OPTIONS=--import=file://<this>.
// When QA_FAKE_NOW is set (an ISO instant), `new Date()` with no arguments and `Date.now()` return that instant
// in THIS process and in every node child that inherits NODE_OPTIONS (node --test file workers, spawned gates).
// npm's own CLI process is left on the real clock (argv[1] matches npm-cli / /npm/), so `npm audit` spawned by
// audit-gate.mjs is not perturbed. Arguments to `new Date(x)` are untouched. Timers are untouched.
const now = process.env.QA_FAKE_NOW;
const argv1 = process.argv[1] || '';
if (now && !/npm-cli|[\\/]npm[\\/]/.test(argv1)) {
  const fixed = Date.parse(now);
  if (Number.isNaN(fixed)) throw new Error('fakeclock: QA_FAKE_NOW is not a parseable instant: ' + now);
  const Real = Date;
  class FakeDate extends Real {
    constructor(...a) {
      if (a.length === 0) super(fixed);
      else super(...a);
    }
    static now() {
      return fixed;
    }
  }
  globalThis.Date = FakeDate;
  if (process.env.QA_FAKE_ANNOUNCE) {
    process.stderr.write('[fakeclock] ' + new Date().toISOString() + ' pid ' + process.pid + ' ' + argv1 + '\n');
  }
}
