// c3_freeze_clock_gate56a.mjs — gate56a C3 clock pin, loaded with `node --import <this file>` BEFORE the code under test.
// faketime-free: replaces globalThis.Date with a subclass whose ZERO-ARGUMENT constructor and Date.now() return the instant in
// FROZEN_NOW_ISO (e.g. 2026-10-10T12:00:00.000Z). Every other Date use (Date.parse, new Date(value), toISOString of a given value) is the
// real Date, untouched — so isIsoDate()'s round-trip `new Date(`${value}T00:00:00Z`)` behaves exactly as in production, and only
// utcToday()'s `new Date().toISOString().slice(0, 10)` (baseline-contract.mjs:92-94) sees the pinned clock.
// FROZEN_NOW_ISO unset -> this file does NOTHING (the real clock; the self-test's control arm).
// Writes nothing; prints one line to stderr naming the pinned instant so every run's evidence names its clock.
const iso = process.env.FROZEN_NOW_ISO;
if (iso) {
  const RealDate = Date;
  const T = RealDate.parse(iso);
  if (Number.isNaN(T)) {
    console.error(`c3_freeze_clock: REFUSING: FROZEN_NOW_ISO=${JSON.stringify(iso)} is not a parseable instant`);
    process.exit(97);
  }
  class FrozenDate extends RealDate {
    constructor(...a) {
      if (a.length === 0) super(T);
      else super(...a);
    }
    static now() {
      return T;
    }
  }
  globalThis.Date = FrozenDate;
  console.error(`c3_freeze_clock: clock pinned to ${new RealDate(T).toISOString()}`);
}
