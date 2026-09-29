// clockfreeze_gate42b.mjs — a `node --import` PRELOAD that freezes the wall clock for a whole process, so the REAL, UNMODIFIED audit-gate.mjs /
// audit-locks.mjs run underneath it (their utcToday() is `new Date().toISOString().slice(0,10)`; there is no clock seam in the repo).
// The frozen instant comes ONLY from G42B_FROZEN_NOW (an ISO-8601 UTC instant, e.g. 2026-09-30T00:01:00Z). It REFUSES (exit 97, before the script
// under test runs) when the variable is unset/empty or is not a valid instant. It ANNOUNCES itself on stderr so a frozen run can never be read as a
// real one. `new Date()` with no argument and `Date.now()` return the frozen instant; `new Date(x)` / Date.parse / Date.UTC behave normally.
// Usage: G42B_FROZEN_NOW=2026-09-30T00:01:00Z node --import /abs/path/clockfreeze_gate42b.mjs scripts/audit/audit-gate.mjs
const raw = process.env.G42B_FROZEN_NOW;
if (!raw) { process.stderr.write('clockfreeze_gate42b: REFUSING — G42B_FROZEN_NOW is unset; a frozen-clock run needs an explicit instant\n'); process.exit(97); }
if (!/^\d{4}-\d{2}-\d{2}T\d{2}:\d{2}(:\d{2}(\.\d+)?)?Z$/.test(raw) || Number.isNaN(Date.parse(raw))) {
  process.stderr.write(`clockfreeze_gate42b: REFUSING — G42B_FROZEN_NOW=${JSON.stringify(raw)} is not an ISO-8601 UTC instant\n`); process.exit(97);
}
const FROZEN = Date.parse(raw);
const RealDate = Date;
class FrozenDate extends RealDate {
  constructor(...a) { if (a.length === 0) super(FROZEN); else super(...a); }
  static now() { return FROZEN; }
}
globalThis.Date = FrozenDate;
process.stderr.write(`clockfreeze_gate42b: FROZEN CLOCK ${new RealDate(FROZEN).toISOString()} (G42B_FROZEN_NOW) — this is NOT a real-clock run\n`);
