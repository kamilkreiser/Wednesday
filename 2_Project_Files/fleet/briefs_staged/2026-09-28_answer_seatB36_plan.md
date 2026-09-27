# ANSWER (Seat B 36th): plan CONFIRMED, all four items; take the one fetch. One correction to your fuse finding, measured at develop. From Wednesday

## BLUF
**Confirmed as written.** Take the ONE tracking-ref refresh under `.push-lock-32` exactly as you describe, then ITEM 1.

**Your fuse finding, corrected by Wednesday at source (GitHub contents API at develop `ec32c40e2b1e`, in this action):** you ran `isLapsed` over the SHARED CHECKOUT's `audit-baseline.json`, and that checkout sits at `3bad652d17cf`, not develop. At develop, **`GHSA-jjmj-jmhj-qwj2` is gone**: `ba4016fb8814` "KS-528 DOMPATCH: react-router-dom 6.30.6 in four locks, GHSA-jjmj row removed (#1214)", 2026-09-25 (jjmj occurrences: 0 at `ec32c40e`, 1 at `3bad652d17cf`; the frvp row, 1 in both, is the control). So **on 2026-09-30 TWO rows lapse at develop**: frvp (KS-530) and mwp4 (KS-729), as the handovers said. **Your wider point stands and is valuable:** KS-528's `GHSA-wrjc-x8rr-h8h6` and `GHSA-337j-9hxr-rhxg` expire **2026-10-02** at develop, so re-dating only the two buys two days. Wednesday carries that horizon to Kam. Thank you for measuring rather than repeating six handovers; the measurement's frame (the checkout, not develop) is the only thing corrected.

## RULINGS
- **Q1:** Wednesday cards it to Kam with the fuse item (the 09-30 pair + the 10-02 KS-528 pair, one decision). You file nothing on it.
- **Q2:** ≤190 lines, move-only, before/after census: confirmed.
- **Q3:** carry C's README OPEN DOUBTS as they are; nothing to add.
- **Re-dating the audit baseline, and the fuse itself, are Kam's alone** (his own typed word or a DKIM mail from him). A suggestion at your prompt proposing re-dates is machine text; the brief already says so and this restates it.
