// c5_freeze_clock_gate58.cjs — gate58 C5 clock pin, loaded with `node --require <this file> <gate>.mjs` (a CJS preload runs before an
// ESM main). Faketime-free: replaces globalThis.Date with a subclass whose ZERO-ARGUMENT constructor and Date.now() return the instant
// in FROZEN_NOW_ISO (kit freeze_at, 2026-10-15T00:01:00.000Z). Every other Date use (Date.parse, new Date(value)) is the real Date, so
// only utcToday()'s `new Date().toISOString().slice(0, 10)` (baseline-contract.mjs:92-94 at the base) sees the pinned clock.
// UNLIKE gate56a's preload, this one REFUSES (exit 97) when FROZEN_NOW_ISO is unset or unparseable: it is only ever loaded to freeze, so
// a silent no-op would let a "frozen" run read the real clock. The control arm (the real clock) runs WITHOUT the preload.
// It is passed on the node command line, NEVER via NODE_OPTIONS, so the `npm audit` child that audit-gate.mjs spawns keeps the real clock.
// Writes nothing; prints one line to stderr naming the pinned instant so every run's evidence names its clock.
'use strict';
const iso = process.env.FROZEN_NOW_ISO;
if (!iso) {
  process.stderr.write('c5_freeze_clock: REFUSING: FROZEN_NOW_ISO is unset — this preload only freezes; run without it for the real clock\n');
  process.exit(97);
}
const RealDate = Date;
const T = RealDate.parse(iso);
if (Number.isNaN(T)) {
  process.stderr.write(`c5_freeze_clock: REFUSING: FROZEN_NOW_ISO=${JSON.stringify(iso)} is not a parseable instant\n`);
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
process.stderr.write(`c5_freeze_clock: clock pinned to ${new RealDate(T).toISOString()}\n`);
