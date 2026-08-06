# Browser-verify before deliver — ritual

Promoted at the 2026-08-06 consolidation (Kam-approved). Earned it: ~12 uses
across the 08-05 dashboard rounds with zero broken deliveries to Kam, and it
caught two defects that a builder's own report had missed.

**When:** before telling Kam (or scoring an agent on) any change with a visible
surface — dashboard rounds, portals, web UIs, generated pages.

## The loop

1. **Node/service check first.** Confirm the thing is actually serving: health
   endpoint or a 200 on the page. A UI check against a dead server produces
   confident nonsense.
2. **Fingerprint the browser BEFORE machine-relative checks.**
   `navigator.hardwareConcurrency` + `screen.width×height` vs local
   `sysctl -n hw.ncpu` and display resolution. The extension's `isLocal` is a
   heuristic — see [[../learnings/2026-08-05_browser-extension-islocal-untrustworthy]].
   Wrong machine → every localhost result is about someone else's computer.
3. **Drive the real controls**, not their wrappers. Target a stable `#id`,
   re-query immediately before interacting (never reuse a handle across a
   re-render), and confirm the click landed via state change or network call.
   See [[../learnings/2026-08-06_selector-discipline-in-ui-verification]].
4. **Round-trip every stateful change** — set it, reload, confirm it persisted,
   then undo it and confirm that persisted too. A save that works once and
   corrupts the store on the second call is the classic miss.
5. **Console must be clean.** Read it; don't assume. Any error is a finding.
6. **No dialogs.** `alert()`/`confirm()`/`prompt()` block automation entirely —
   if one appears, that is a defect to report, not an obstacle to click through.
7. **Screenshot the result** and attach it to the receipt.

## Reporting rule

State what you verified AND what you did not. "Views save/apply/delete verified
in-browser; the destructive archive path was NOT live-tested" is a better
receipt than a green tick covering both. If a check surprised you, suspect your
own test before the build.

**Related:** [[delegation-protocol]], [[../learnings/2026-08-05_verify-the-chain-not-the-legs]]
